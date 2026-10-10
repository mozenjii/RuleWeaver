"""The OpenFisca export, executed.

tests/test_openfisca.py checks what the adapter writes. This file runs it: each household
is evaluated by the deterministic evaluator and by the generated country package under
OpenFisca, and every exported variable is compared.

The first run of this harness found five defects that every structural test had passed:
the package could not be loaded by OpenFisca, it declared no input variables so no
household could be entered, exception priority was inverted, a guarded rule was computed
for households its guard excludes, and no dimensioned parameter could be read. Each has a
case below that fails if it comes back.

The SNAP tables used are the 48-states-and-DC rows of the conftest overrides. The
`lowmax` rows exist only at household size three, so they are not a complete grid, and
OpenFisca cannot index a table that is not — the export reports that as RW8007 rather
than inventing the missing cells.
"""

from __future__ import annotations

import copy
import json
from decimal import Decimal

import pytest

pytest.importorskip("openfisca_core", reason="the equivalence harness needs OpenFisca")

from conftest import FIXTURE, household, member, with_tables
from ruleweaver.adapters.openfisca import export
from ruleweaver.adapters.openfisca.equivalence import compare, load
from ruleweaver.ir import RulePackage
from ruleweaver.runtime import Context, Evaluator, ParameterTable

GROSS = "var.household.meets_gross_income_test"
ELIGIBLE = "var.household.is_income_eligible"


@pytest.fixture(scope="module")
def snap(tmp_path_factory):
    package = with_tables(RulePackage.model_validate(
        json.loads(FIXTURE.read_text(encoding="utf-8"))))
    result = export(package, require_approval=False)
    system = load(result, tmp_path_factory.mktemp("openfisca"))
    return package, result, system, Evaluator(package, ParameterTable(package))


def run(snap, ctx: Context):
    package, result, system, evaluator = snap
    return compare(package, result, system, evaluator, ctx)


def value(comparison, variable: str):
    [row] = [r for r in comparison.rows if r.variable == variable and r.scope == "household"]
    return row


HOUSEHOLDS = {
    "working parent, shelter cap binds": household(
        [member(34, "1500"), member(8), member(6)], shelter="900"),
    "elderly couple, no gross test, no cap": household(
        [member(70, "0", "1200"), member(68)], shelter="1100"),
    "single earner over the gross limit": household([member(40, "5000")], shelter="500"),
    "disabled member": household(
        [member(30, "800", disabled=True), member(5), member(3)], shelter="300"),
    "no income at all": household([member(25)]),
    "mixed earned and unearned income": household(
        [member(45, "900", "650"), member(43, "400"), member(12)], shelter="1450"),
}


class TestAgreement:
    @pytest.mark.parametrize("name", sorted(HOUSEHOLDS))
    def test_every_exported_variable_agrees(self, snap, name):
        comparison = run(snap, HOUSEHOLDS[name])
        assert comparison.ok, str(comparison)
        assert not comparison.gaps, "every input was supplied; nothing should be unknown"

    def test_every_exported_rule_is_compared(self, snap):
        package, result, _, _ = snap
        comparison = run(snap, HOUSEHOLDS["working parent, shelter cap binds"])
        compared = {r.variable for r in comparison.rows}
        targets = {r.then.assign.target for r in package.rules if r.id in result.exported}
        assert compared == targets
        assert len(targets) == 13

    def test_both_exceptions_are_exercised(self, snap):
        """A comparison in which no exception fires would say nothing about exceptions."""
        _, _, _, evaluator = snap
        fired = set()
        for ctx in HOUSEHOLDS.values():
            trace = evaluator.run(copy.deepcopy(ctx)).trace
            fired |= {step.via for step in trace if step.via.startswith("exception:")}
        # The two on exported rules. The minimum-benefit exception fires too, but it sits
        # on the allotment, which is guarded and so not exported.
        assert {"exception:exception.snap.shelter_cap_applies",
                "exception:exception.snap.gross_test_waived_elderly_disabled"} <= fired


class TestThresholds:
    """The two-person gross limit is 130% of 21150 / 12 = 2291.25, rounded up to 2292.

    OpenFisca holds money as 32-bit floats and the evaluator as decimals, so the exact
    limit is where the two would part if they were going to.
    """

    def test_income_exactly_at_the_gross_limit_passes_in_both(self, snap):
        comparison = run(snap, household([member(30, "2292"), member(2)]))
        assert comparison.ok, str(comparison)
        assert value(comparison, GROSS).expected is True

    def test_one_cent_over_fails_in_both(self, snap):
        comparison = run(snap, household([member(30, "2292.01"), member(2)]))
        assert comparison.ok, str(comparison)
        assert value(comparison, GROSS).expected is False


class TestTheUnknownGap:
    def test_a_missing_income_is_a_gap_not_agreement(self, snap):
        """RW8001, observed. The evaluator cannot decide; OpenFisca reads the blank as
        zero and calls the household eligible. That is an approval nobody made."""
        ctx = household([member(34, "1500"), member(8)])
        del ctx.members[0]["var.member.earned_income"]
        comparison = run(snap, ctx)

        assert comparison.ok, "a gap is not a mismatch"
        eligible = value(comparison, ELIGIBLE)
        assert eligible.verdict == "gap"
        assert eligible.actual is True
        assert eligible not in comparison.matches


class TestDates:
    def test_rules_not_yet_in_force_compute_nothing(self, snap):
        """Formulas are dated from the rule's effective_from. Undated, OpenFisca applied
        every rule to every month, including the ones before it was law."""
        package, result, system, evaluator = snap
        ctx = copy.deepcopy(HOUSEHOLDS["working parent, shelter cap binds"])
        ctx.on_date = "2025-12-01"
        comparison = compare(package, result, system, evaluator, ctx)
        assert not comparison.matches and not comparison.mismatches
        assert all(row.actual in (0, False) for row in comparison.gaps)

    def test_mid_month_dates_are_refused(self, snap):
        ctx = copy.deepcopy(HOUSEHOLDS["no income at all"])
        ctx.on_date = "2026-01-15"
        with pytest.raises(ValueError, match="first of a month"):
            run(snap, ctx)


def synthetic() -> RulePackage:
    """The cases the SNAP fixture cannot show: two exceptions that both hold, and a
    member formula that reads a household value."""
    def ref(identifier):
        return {"op": "ref", "id": identifier}

    def lit(v):
        return {"op": "literal", "value": v}

    def at_least(n):
        return {"op": "gte", "left": ref("var.household.size"), "right": lit(n)}

    def substitute(target, v):
        return {"assign": {"target": target, "value": lit(v)}}

    def variable(identifier, entity, value_type, *, is_input=False):
        return {"id": identifier, "entity": entity, "value_type": value_type,
                "periodicity": "month", "input": is_input}

    def parameter(identifier, v):
        return {"id": identifier, "value_type": "decimal",
                "values": [{"effective_from": "2020-01-01", "value": v}]}

    source = [{"source_id": "synthetic", "citation": "7 CFR 0.0"}]
    return RulePackage.model_validate({
        "schema_version": "0.1.0", "package_id": "synthetic", "jurisdiction": "nowhere",
        "entities": [{"id": "household", "label": "Household"},
                     {"id": "household_member", "label": "Member", "kind": "member",
                      "member_of": "household"}],
        "variables": [
            variable("var.household.size", "household", "integer", is_input=True),
            variable("var.member.income", "household_member", "money", is_input=True),
            variable("var.household.tier", "household", "money"),
            variable("var.member.share", "household_member", "money"),
            variable("var.household.levy", "household", "money"),
        ],
        "parameters": [parameter("param.base", "100"), parameter("param.rate", "0.07")],
        "rules": [
            {"id": "rule.tier", "kind": "calculation", "effective_from": "2026-01-01",
             "when": lit(True), "sources": source,
             "then": {"assign": {"target": "var.household.tier", "value": lit(10)}},
             "exceptions": [
                 {"id": "exc.second", "priority": 2, "effect": "substitute",
                  "when": at_least(1), "substitute": substitute("var.household.tier", 30)},
                 {"id": "exc.first", "priority": 1, "effect": "substitute",
                  "when": at_least(2), "substitute": substitute("var.household.tier", 20)},
             ]},
            {"id": "rule.share", "kind": "calculation", "effective_from": "2026-01-01",
             "when": lit(True), "sources": source,
             "then": {"assign": {"target": "var.member.share", "value": {
                 "op": "divide",
                 "args": [ref("var.member.income"), ref("var.household.size")]}}}},
            # 100 x 0.07 is 7 exactly. In binary floating point it is 7.000000000000001,
            # and rounding up turns that into 8.
            {"id": "rule.levy", "kind": "calculation", "effective_from": "2026-01-01",
             "when": lit(True), "sources": source,
             "then": {"assign": {"target": "var.household.levy", "value": {
                 "op": "round", "mode": "up", "to": "1", "arg": {
                     "op": "multiply",
                     "args": [{"op": "parameter", "id": "param.base", "args": {}},
                              {"op": "parameter", "id": "param.rate", "args": {}}]}}}}},
        ],
    })


class TestSynthetic:
    @pytest.fixture(scope="class")
    def synth(self, tmp_path_factory):
        package = synthetic()
        result = export(package, require_approval=False)
        system = load(result, tmp_path_factory.mktemp("synthetic"))
        return package, result, system, Evaluator(package, ParameterTable(package))

    def ctx(self, size: int) -> Context:
        return Context(
            household={"var.household.size": Decimal(size)},
            members=[{"var.member.income": Decimal("300")} for _ in range(size)],
            on_date="2026-01-01")

    def test_the_lowest_numbered_matching_exception_wins_in_both(self, synth):
        """Both exceptions hold for a household of three. The spec says priority 1 wins.
        The adapter used to sort descending and pick 30."""
        comparison = compare(*synth[:3], synth[3], self.ctx(3))
        tier = value(comparison, "var.household.tier")
        assert tier.verdict == "match", str(comparison)
        assert tier.actual == 20

    def test_a_single_matching_exception_still_applies(self, synth):
        comparison = compare(*synth[:3], synth[3], self.ctx(1))
        tier = value(comparison, "var.household.tier")
        assert tier.verdict == "match", str(comparison)
        assert tier.actual == 30

    def test_rounding_up_a_float_product_is_caught(self, synth):
        """A known hazard of running decimal law on binary floats, planted here so the
        harness is shown to fail when the runtimes disagree. Rounding up is where a
        representation error of 1e-15 becomes a whole dollar.

        The SNAP gross limit is the same shape — a product of parameters, rounded up —
        and does not trip it: every one of the 1,000 poverty-line values that make the
        limit a whole dollar rounds the same way in both. That is a property of those
        numbers, not of the adapter.
        """
        comparison = compare(*synth[:3], synth[3], self.ctx(1))
        levy = value(comparison, "var.household.levy")
        assert levy.expected == 7
        assert levy.actual == 8
        assert levy in comparison.mismatches
        assert not comparison.ok

    def test_a_member_formula_reads_its_households_value(self, synth):
        comparison = compare(*synth[:3], synth[3], self.ctx(3))
        shares = [r for r in comparison.rows if r.variable == "var.member.share"]
        assert len(shares) == 3
        assert all(r.verdict == "match" and r.expected == 100 for r in shares), str(comparison)


class TestOpenFiscasOwnRunner:
    """The households above, written as OpenFisca YAML tests and run by `openfisca test`.

    That is the evidence a user of the exported package can rerun without RuleWeaver.
    """

    @pytest.fixture(scope="class")
    def written(self, snap, tmp_path_factory):
        from ruleweaver.adapters.openfisca.yaml_tests import test_file

        package, result, _, evaluator = snap
        root = tmp_path_factory.mktemp("country")
        result.write(root / "snapcountry")
        cases = dict(HOUSEHOLDS)
        missing = household([member(34, "1500"), member(8)])
        del missing.members[0]["var.member.earned_income"]
        cases["a member's income is missing"] = missing
        tests = root / "snap.yaml"
        tests.write_text(test_file(package, result, evaluator, cases), encoding="utf-8")
        return root, tests

    def openfisca_test(self, root, tests):
        import os
        import subprocess
        import sys
        from pathlib import Path

        runner = Path(sys.executable).parent / "openfisca"
        return subprocess.run(
            [str(runner), "test", str(tests), "--country-package", "snapcountry"],
            capture_output=True, text=True, check=False,
            env={**os.environ, "PYTHONPATH": str(root)})

    def test_the_exported_tests_pass_under_openfisca(self, written):
        run_ = self.openfisca_test(*written)
        assert run_.returncode == 0, run_.stdout + run_.stderr

    def test_an_unknown_is_left_out_rather_than_asserted(self, written):
        """OpenFisca says this household is eligible; the evaluator cannot decide. A test
        expecting True would pass and enshrine the gap."""
        _, tests = written
        text = tests.read_text(encoding="utf-8")
        block = text[text.index("a member's income is missing"):]
        assert "left out" in block
        assert "is_income_eligible" not in block

    def test_a_wrong_expectation_fails_under_openfisca(self, written, tmp_path):
        """A test file OpenFisca cannot fail is not evidence."""
        root, tests = written
        broken = tmp_path / "broken.yaml"
        text = tests.read_text(encoding="utf-8")
        assert "    net_monthly_income: 594.0000" in text
        broken.write_text(text.replace("    net_monthly_income: 594.0000",
                                       "    net_monthly_income: 600"), encoding="utf-8")
        assert self.openfisca_test(root, broken).returncode != 0


class TestTheShippedTables:
    """The package as shipped, with the official FY2026 tables, run under OpenFisca."""

    @pytest.fixture(scope="class")
    def official(self, tmp_path_factory):
        package = RulePackage.model_validate(json.loads(FIXTURE.read_text(encoding="utf-8")))
        result = export(package, require_approval=False)
        system = load(result, tmp_path_factory.mktemp("official"))
        return package, result, system, Evaluator(package, ParameterTable(package))

    @pytest.mark.parametrize("name", sorted(HOUSEHOLDS))
    def test_every_exported_variable_agrees(self, official, name):
        comparison = run(official, copy.deepcopy(HOUSEHOLDS[name]))
        assert comparison.ok, str(comparison)
        assert not comparison.gaps

    def test_a_value_ends_with_its_fiscal_year(self, official):
        """Without a closing `null` the FY2026 figures would apply in OpenFisca for ever,
        while the evaluator answers unknown from 1 October 2026."""
        _, result, _, _ = official
        shelter = result.files["parameters/snap/shelter_cap/48_dc.yaml"]
        assert "2026-10-01:\n    value: null" in shelter
