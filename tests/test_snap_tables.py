"""The shipped SNAP tables against the documents they were copied from.

The package carries the official figures for 1 October 2025 to 30 September 2026 in the
48 states and DC. These tests do not trust that transcription: they read the stored FNS
memo and Federal Register notice, parse the published tables, and compare. Then they run
the rules on those tables and check that the income limits the evaluator applies are the
limits FNS published — which tests the rules' rounding as well as the numbers.
"""

from __future__ import annotations

import json
import re
from decimal import Decimal

import pytest

from conftest import FIXTURE, household, member
from ruleweaver.ingest import load_corpus
from ruleweaver.ir import RulePackage
from ruleweaver.runtime import Evaluator, ParameterTable
from ruleweaver.runtime.values import UNKNOWN
from ruleweaver.verify import validate

SOURCES = FIXTURE.parent / "sources"
MEMO = (SOURCES / "fns-snap-cola-fy2026.txt").read_text(encoding="utf-8")
SIZES = range(1, 9)


def _money(text: str) -> int:
    return int(text.replace("$", "").replace(",", ""))


def _rows(heading: str, count: int = 8) -> dict[int, int]:
    """The first column of figures in the table under `heading`, by household size."""
    block = MEMO[MEMO.index(heading):]
    rows: dict[int, int] = {}
    for line in block.splitlines():
        match = re.match(r"\s+(\d)\s+(\$[\d,]+)", line)
        if match:
            rows[int(match.group(1))] = _money(match.group(2))
            if len(rows) == count:
                return rows
    raise AssertionError(f"could not read the table under {heading!r}")


def _poverty_guidelines() -> dict[int, int]:
    raw = (SOURCES / "hhs-poverty-guidelines-2025.htm").read_text(encoding="utf-8")
    block = raw[raw.index("48 Contiguous States"):]
    rows: dict[int, int] = {}
    for line in block.splitlines():
        match = re.match(r"(\d)\.{5,}\s+\$?([\d,]+)", line)
        if match:
            rows[int(match.group(1))] = _money(match.group(2))
            if len(rows) == 8:
                return rows
    raise AssertionError("could not read the 48-state poverty guidelines")


@pytest.fixture(scope="module")
def package() -> RulePackage:
    return RulePackage.model_validate(json.loads(FIXTURE.read_text(encoding="utf-8")))


@pytest.fixture(scope="module")
def evaluator(package) -> Evaluator:
    return Evaluator(package, ParameterTable(package))


def shipped(package: RulePackage, parameter_id: str) -> dict:
    return {tuple(sorted(v.at.items())): Decimal(str(v.value))
            for v in package.parameter(parameter_id).values}


def at(size: int | None = None) -> tuple:
    coordinates = {"jurisdiction": "48_dc"}
    if size is not None:
        coordinates["household_size"] = str(size)
    return tuple(sorted(coordinates.items()))


class TestTranscription:
    def test_the_poverty_guidelines(self, package):
        table = shipped(package, "param.snap.fpl_annual")
        assert {size: table[at(size)] for size in SIZES} == \
            {size: Decimal(v) for size, v in _poverty_guidelines().items()}

    def test_the_maximum_allotments(self, package):
        table = shipped(package, "param.snap.max_allotment")
        published = _rows("Maximum SNAP Allotments for 48 States and D.C.")
        assert {size: table[at(size)] for size in SIZES} == \
            {size: Decimal(v) for size, v in published.items()}

    def test_the_standard_deductions(self, package):
        line = next(line for line in MEMO[MEMO.index("Standard Deductions"):].splitlines()
                    if line.startswith("48 States and D.C."))
        figures = [_money(f) for f in re.findall(r"\$[\d,]+", line)]
        # The memo's columns are household sizes "1-2", 3, 4, 5 and "6+".
        columns = [(1, 2), (3,), (4,), (5,), (6,)]
        published = {size: figure for sizes, figure in zip(columns, figures, strict=True)
                     for size in sizes}
        table = shipped(package, "param.snap.standard_deduction")
        assert {size: table[at(size)] for size in range(1, 7)} == \
            {size: Decimal(v) for size, v in published.items()}
        assert shipped(package, "param.snap.standard_deduction_minimum")[at()] == \
            Decimal(published[1])

    def test_the_shelter_cap_and_minimum_benefit(self, package):
        assert shipped(package, "param.snap.shelter_cap")[at()] == Decimal("744")
        assert "will increase to $744 for the 48 States and D.C." in " ".join(MEMO.split())
        assert shipped(package, "param.snap.minimum_benefit")[at()] == Decimal("24")
        assert "minimum benefit for the 48 States and D.C. will increase to $24" in \
            " ".join(MEMO.split())

    def test_the_minimum_benefit_follows_its_own_formula(self, package):
        """7 CFR 273.10(e)(2)(ii)(C): 8 percent of the one-person maximum, rounded."""
        one_person = shipped(package, "param.snap.max_allotment")[at(1)]
        minimum = shipped(package, "param.snap.minimum_benefit")[at()]
        assert round(one_person * Decimal("0.08")) == minimum

    def test_every_quoted_figure_is_in_its_source(self, package):
        corpus = load_corpus(SOURCES / "manifest.json")
        report = validate(package, corpus=corpus)
        assert not [d for d in report.diagnostics if d.code == "RW1001"]

    def test_a_mistyped_figure_is_caught(self, package):
        corpus = load_corpus(SOURCES / "manifest.json")
        wrong = package.model_copy(deep=True)
        value = wrong.parameter("param.snap.shelter_cap").values[0]
        value.sources[0] = value.sources[0].model_copy(
            update={"quote": "48 States and D.C. $745"})
        report = validate(wrong, corpus=corpus)
        assert any(d.code == "RW1001" and d.object_id == "param.snap.shelter_cap"
                   for d in report.diagnostics)


class TestTheLimitsFNSPublished:
    """The evaluator's income tests, at the edges of FNS's published standards."""

    @pytest.mark.parametrize("size", SIZES)
    def test_gross_income_limit(self, evaluator, size):
        limit = _rows("Gross Monthly Income Eligibility Standards")[size]
        for income, passes in ((limit, True), (limit + 1, False)):
            ctx = evaluator.run(household([member(30, unearned=str(income))], size=size))
            assert ctx.household["var.household.meets_gross_income_test"] is passes, income

    @pytest.mark.parametrize("size", SIZES)
    def test_net_income_limit(self, evaluator, size):
        limit = _rows("Net Monthly Income Eligibility Standards")[size]
        # Unearned income with no shelter cost: net income is gross minus the standard
        # deduction, so the gross that lands exactly on the limit is known.
        deduction = evaluator.run(household([member(30)], size=size)).household[
            "var.household.standard_deduction"]
        for net, passes in ((limit, True), (limit + 1, False)):
            ctx = evaluator.run(household(
                [member(30, unearned=str(net + deduction))], size=size))
            assert ctx.household["var.household.net_monthly_income"] == net
            assert ctx.household["var.household.meets_net_income_test"] is passes, net

    def test_the_baseline_household(self, evaluator):
        """A working parent with two children: $1,500 earned, $900 shelter."""
        ctx = evaluator.run(household([member(34, "1500"), member(8), member(6)],
                                      shelter="900"))
        assert ctx.household["var.household.standard_deduction"] == Decimal("209")
        assert ctx.household["var.household.net_monthly_income"] == Decimal("586.5")
        assert ctx.household["var.household.allotment"] == Decimal("609")


class TestWhatIsNotCovered:
    def test_a_household_of_nine_is_unknown_not_guessed(self, evaluator):
        """FNS sets the limits for a ninth member by adding a rounded increment ($459
        net, $596 gross), which is a dollar above recomputing from the poverty line. The
        tables stop at eight rather than extrapolate an answer that could be a dollar
        wrong at the edge; research/REQUIREMENTS.md R-36 tracks it."""
        ctx = evaluator.run(household([member(30, unearned="1000")], size=9))
        assert ctx.household.get("var.household.is_income_eligible", UNKNOWN) is UNKNOWN

    def test_after_the_fiscal_year_the_answer_is_unknown(self, evaluator):
        """The FY2026 figures end on 30 September 2026. Nothing carries them forward."""
        ctx = household([member(30, unearned="1000")])
        ctx.on_date = "2026-10-01"
        ctx = evaluator.run(ctx)
        assert ctx.household.get("var.household.is_income_eligible", UNKNOWN) is UNKNOWN

    def test_on_the_last_day_they_still_apply(self, evaluator):
        ctx = household([member(30, unearned="1000")])
        ctx.on_date = "2026-09-30"
        assert evaluator.run(ctx).household["var.household.is_income_eligible"] is True
