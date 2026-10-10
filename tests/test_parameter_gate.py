"""Parameters pass the approval gate, like rules.

A rule is only as right as the numbers it reads, and those numbers change every year. The
gate used to cover rules alone, so an approved rule would compute with whatever poverty
line or deduction the package held, reviewed or not.
"""

from __future__ import annotations

import json
from decimal import Decimal

import pytest

from conftest import FIXTURE, household, member, with_tables
from ruleweaver.approval import approved_subset, check, current_hashes
from ruleweaver.ir import RulePackage
from ruleweaver.ir.rules import ParameterValue, SourceSpan
from ruleweaver.review import Decision, ReviewEvent, ReviewLog, Status
from ruleweaver.runtime import Evaluator, ParameterTable
from ruleweaver.runtime.values import UNKNOWN
from ruleweaver.verify import validate

ELIGIBLE = "var.household.is_income_eligible"
NET = "var.household.net_monthly_income"


@pytest.fixture()
def package() -> RulePackage:
    return with_tables(RulePackage.model_validate(
        json.loads(FIXTURE.read_text(encoding="utf-8"))))


def approve(package: RulePackage, *, skip: tuple[str, ...] = ()) -> ReviewLog:
    log = ReviewLog()
    for item_id, (item_hash, source_hash) in current_hashes(package).items():
        if item_id not in skip:
            log.append(ReviewEvent(rule_id=item_id, reviewer="alice",
                                   decision=Decision.APPROVE,
                                   rule_hash=item_hash, source_hash=source_hash))
    return log


def run(package: RulePackage, log: ReviewLog):
    subset, report = approved_subset(package, log)
    ctx = Evaluator(subset, ParameterTable(subset)).run(
        household([member(34, "1500"), member(8), member(6)], shelter="900"))
    return ctx, report


class TestGate:
    def test_parameters_are_reviewable_items(self, package):
        hashes = current_hashes(package)
        assert all(p.id in hashes for p in package.parameters)

    def test_an_unapproved_table_gives_unknown_not_a_number(self, package):
        ctx, report = run(package, approve(package, skip=("param.snap.fpl_annual",)))
        assert report.parameters_blocked == {"param.snap.fpl_annual": Status.UNREVIEWED}
        assert not report.ok
        assert ctx.household.get(ELIGIBLE, UNKNOWN) is UNKNOWN

    def test_everything_approved_computes(self, package):
        ctx, report = run(package, approve(package))
        assert report.ok
        assert ctx.household[ELIGIBLE] is True
        assert ctx.household[NET] == Decimal("594")

    def test_changing_a_number_makes_its_approval_stale(self, package):
        """An uprating is a reviewable change, not a silent edit."""
        log = approve(package)
        rate = package.parameter("param.snap.earned_income_deduction_rate")
        uprated = rate.model_copy(update={"values": [
            v.model_copy(update={"value": Decimal("0.25")}) for v in rate.values]})
        changed = package.model_copy(update={"parameters": [
            uprated if p.id == rate.id else p for p in package.parameters]})
        report = check(changed, log)
        assert report.parameters_blocked == {rate.id: Status.STALE}

    def test_a_new_value_source_makes_the_approval_stale(self, package):
        log = approve(package)
        rate = package.parameter("param.snap.earned_income_deduction_rate")
        cited = rate.model_copy(update={"values": [v.model_copy(update={"sources": [
            SourceSpan(source_id="notice", citation="FY2027 notice")]}) for v in rate.values]})
        changed = package.model_copy(update={"parameters": [
            cited if p.id == rate.id else p for p in package.parameters]})
        assert check(changed, log).parameters_blocked == {rate.id: Status.STALE}

    def test_the_report_counts_tables_separately(self, package):
        text = str(check(package, approve(package, skip=("param.snap.shelter_cap",))))
        assert "15 approved, 0 blocked" in text
        assert "parameters: 9 approved, 1 blocked" in text


class TestDiagnostics:
    def test_an_empty_table_is_reported(self):
        shipped = RulePackage.model_validate(json.loads(FIXTURE.read_text(encoding="utf-8")))
        assert not [d for d in validate(shipped).diagnostics if d.code == "RW3011"]
        shipped.parameter("param.snap.fpl_annual").values.clear()
        codes = [(d.code, d.object_id) for d in validate(shipped).diagnostics]
        assert ("RW3011", "param.snap.fpl_annual") in codes

    def test_the_shipped_values_are_all_sourced(self):
        shipped = RulePackage.model_validate(json.loads(FIXTURE.read_text(encoding="utf-8")))
        assert not [d for d in validate(shipped).diagnostics if d.code == "RW7004"]

    def test_a_value_with_no_source_anywhere_is_reported(self, package):
        bare = package.parameter("param.snap.shelter_cap").model_copy(update={"sources": []})
        changed = package.model_copy(update={"parameters": [
            bare if p.id == bare.id else p for p in package.parameters]})
        codes = [(d.code, d.object_id) for d in validate(changed).diagnostics]
        assert ("RW7004", "param.snap.shelter_cap") in codes

    def test_a_sourced_value_is_not_reported(self, package):
        span = SourceSpan(source_id="fns", citation="FY2026 COLA memo")
        bare = package.parameter("param.snap.shelter_cap")
        sourced = bare.model_copy(update={"sources": [], "values": [
            v.model_copy(update={"sources": [span]}) for v in bare.values]})
        changed = package.model_copy(update={"parameters": [
            sourced if p.id == bare.id else p for p in package.parameters]})
        codes = [(d.code, d.object_id) for d in validate(changed).diagnostics]
        assert ("RW7004", "param.snap.shelter_cap") not in codes


class TestExport:
    def test_an_unapproved_table_is_not_exported(self, package):
        from ruleweaver.adapters.openfisca import export

        result = export(package, log=approve(package, skip=("param.snap.shelter_cap",)))
        assert not any("shelter_cap" in name for name in result.files)
        assert any(d.code == "RW8002" and "shelter_cap" in d.message
                   for d in result.diagnostics)


class TestValueSources:
    def test_a_value_carries_its_publication(self):
        value = ParameterValue(effective_from="2025-10-01", value=Decimal("672"),
                               sources=[SourceSpan(source_id="fns",
                                                   citation="FY2026 COLA memo")])
        assert value.sources[0].citation == "FY2026 COLA memo"
