"""Running an export under OpenFisca beside the deterministic evaluator.

The adapter's claim is that a household gets the same answer from the exported country
package as from the IR. Until this module existed that claim was structural: the package
parsed, and nobody had run it. The first run found that it could not be loaded, could not
accept a household, inverted exception priority, computed a guarded benefit for households
the guard excludes, and could not read any dimensioned table.

Each compared value gets one of three verdicts:

- **match** — both runtimes produced the same value, within `tolerance` for numbers.
  OpenFisca stores money as 32-bit floats; the evaluator uses exact decimals.
- **mismatch** — both produced a value and they differ. This is a defect in the adapter or
  in the IR's semantics, and is what the comparison exists to find.
- **gap** — the evaluator says unknown and OpenFisca produced a number anyway. This is the
  four-state gap `RW8001` reports on every export. It is expected, it is not a match, and
  it is counted separately so it can never be mistaken for agreement.

OpenFisca is imported here and nowhere else in the core, and only when a comparison runs.
"""

from __future__ import annotations

import copy
import importlib.util
import sys
import uuid
from dataclasses import dataclass, field
from decimal import Decimal
from pathlib import Path
from typing import Any, Literal

from ...ir.rules import RulePackage
from ...runtime import Context, Evaluator
from ...runtime.values import UNKNOWN, Value, is_unknown
from .codegen import Export, _identifier

Verdict = Literal["match", "mismatch", "gap"]


@dataclass(frozen=True)
class Row:
    variable: str
    scope: str
    expected: Value
    actual: Any
    verdict: Verdict

    def __str__(self) -> str:
        return (f"[{self.verdict.upper():8}] {self.scope:10} {self.variable:50} "
                f"evaluator={self.expected}  openfisca={self.actual}")


@dataclass
class Comparison:
    rows: list[Row] = field(default_factory=list)

    def _with(self, verdict: Verdict) -> list[Row]:
        return [r for r in self.rows if r.verdict == verdict]

    @property
    def matches(self) -> list[Row]:
        return self._with("match")

    @property
    def mismatches(self) -> list[Row]:
        return self._with("mismatch")

    @property
    def gaps(self) -> list[Row]:
        return self._with("gap")

    @property
    def ok(self) -> bool:
        """No mismatches. Gaps do not fail a comparison, and do not count as agreement."""
        return bool(self.rows) and not self.mismatches

    def __str__(self) -> str:
        lines = [f"{len(self.matches)} match, {len(self.mismatches)} mismatch, "
                 f"{len(self.gaps)} gap"]
        lines += [f"  {row}" for row in self.rows if row.verdict != "match"]
        return "\n".join(lines)


def load(result: Export, directory: str | Path):
    """Write an export as a uniquely named package and return its tax-benefit system.

    The name is unique so two exports loaded in one process never share a module.
    """
    name = f"ruleweaver_export_{uuid.uuid4().hex}"
    root = result.write(Path(directory) / name)
    spec = importlib.util.spec_from_file_location(
        name, root / "__init__.py", submodule_search_locations=[str(root)])
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module.CountryTaxBenefitSystem()


def _member(package: RulePackage, identifier: str) -> bool:
    declared = package.variable(identifier)
    return declared is not None and declared.entity != "household"


def _plain(value: Value) -> Any:
    return float(value) if isinstance(value, Decimal) else value


def _situation(package: RulePackage, ctx: Context, month: str) -> dict:
    """The OpenFisca situation for the inputs a context supplies.

    Only facts the context actually holds are passed. An input left out stays out, so
    OpenFisca falls back to its type default — which is the gap this module measures.
    """
    def is_input(identifier: str) -> bool:
        declared = package.variable(identifier)
        return declared is not None and declared.input

    def entries(values: dict[str, Value]) -> dict:
        return {_identifier(k): {month: _plain(v)} for k, v in values.items()
                if is_input(k) and not is_unknown(v)}

    persons = {f"member_{i}": entries(m) for i, m in enumerate(ctx.members)}
    household = entries(ctx.household)
    household["members"] = list(persons)
    return {"persons": persons, "households": {"household": household}}


def _verdict(expected: Value, actual: Any, tolerance: Decimal) -> Verdict:
    if is_unknown(expected):
        return "gap"
    if isinstance(expected, bool) or isinstance(actual, bool):
        return "match" if bool(actual) == expected else "mismatch"
    if isinstance(expected, Decimal):
        difference = abs(Decimal(str(float(actual))) - expected)
        return "match" if difference <= tolerance else "mismatch"
    return "match" if str(actual) == str(expected) else "mismatch"


def compare(
    package: RulePackage,
    result: Export,
    tax_benefit_system,
    evaluator: Evaluator,
    ctx: Context,
    *,
    tolerance: Decimal = Decimal("0.01"),
) -> Comparison:
    """Evaluate one household both ways and compare every exported variable.

    `package` must be the package `result` was exported from, and `evaluator` must read
    the same parameter values the export wrote — otherwise the comparison measures the
    difference between two tables, not between two runtimes.
    """
    if not ctx.on_date.endswith("-01"):
        # OpenFisca reads parameters at the start of the period, the evaluator on the day.
        # Comparing mid-month would attribute a mid-month parameter change to the adapter.
        raise ValueError(f"compare on the first of a month, not {ctx.on_date}")
    from openfisca_core.simulation_builder import SimulationBuilder

    month = ctx.on_date[:7]
    evaluated = evaluator.run(copy.deepcopy(ctx))
    simulation = SimulationBuilder().build_from_entities(
        tax_benefit_system, _situation(package, ctx, month))

    comparison = Comparison()
    targets = [r.then.assign.target for r in package.rules if r.id in result.exported]
    for target in targets:
        computed = simulation.calculate(_identifier(target), month)
        if _member(package, target):
            for i, member in enumerate(evaluated.members):
                expected = member.get(target, UNKNOWN)
                actual = computed[i].item()
                comparison.rows.append(Row(target, f"member[{i}]", expected, actual,
                                           _verdict(expected, actual, tolerance)))
        else:
            expected = evaluated.household.get(target, UNKNOWN)
            actual = computed[0].item()
            comparison.rows.append(Row(target, "household", expected, actual,
                                       _verdict(expected, actual, tolerance)))
    return comparison
