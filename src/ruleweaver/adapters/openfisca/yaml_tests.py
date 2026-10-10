"""OpenFisca's own test format, written from the deterministic evaluator.

The equivalence harness proves the export agrees with the evaluator, but the proof lives
in this repository. A country package is used somewhere else, by people who run
`openfisca test`, not pytest. So the same households are written out as OpenFisca YAML
tests whose expected values come from the evaluator, and they ship inside the export.

Only values the evaluator knows are asserted. Where it says unknown, OpenFisca would
produce a type default, and writing that default down as the expected answer would turn
the four-state gap into a passing test. Those values are left out, and the file says how
many were left out and why.

Written by hand rather than through a YAML library, like the parameter files, so the
adapter stays dependency free. Every scalar is emitted as JSON, which is valid YAML.
"""

from __future__ import annotations

import copy
import json
from decimal import Decimal

from ...ir.rules import RulePackage
from ...runtime import Context, Evaluator
from ...runtime.values import UNKNOWN, Value, is_unknown
from .codegen import Export, _identifier


def _scalar(value: Value) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, Decimal):
        return format(value, "f")
    return json.dumps(value)


def _member(package: RulePackage, identifier: str) -> bool:
    declared = package.variable(identifier)
    return declared is not None and declared.entity != "household"


def test_case(package: RulePackage, result: Export, evaluator: Evaluator, name: str,
              ctx: Context, *, margin: str = "0.01") -> str:
    """One OpenFisca YAML test for one household, or raise if it cannot be faithful."""
    if not ctx.on_date.endswith("-01"):
        raise ValueError(f"{name}: OpenFisca tests run per month; use the first of a "
                         f"month, not {ctx.on_date}")
    period = ctx.on_date[:7]
    evaluated = evaluator.run(copy.deepcopy(ctx))

    def inputs(values: dict[str, Value], indent: str) -> list[str]:
        lines = []
        for identifier, value in values.items():
            declared = package.variable(identifier)
            if declared is not None and declared.input and not is_unknown(value):
                lines.append(f"{indent}{_identifier(identifier)}: {_scalar(value)}")
        return lines

    members = [f"member_{i}" for i in range(len(ctx.members))]
    lines = [f"- name: {json.dumps(name)}", f"  period: {period}",
             f"  absolute_error_margin: {margin}", "  input:", "    persons:"]
    for label, member in zip(members, ctx.members, strict=True):
        lines.append(f"      {label}:")
        lines += inputs(member, "        ") or ["        {}"]
    lines += ["    households:", "      household:",
              f"        members: [{', '.join(members)}]"]
    lines += inputs(ctx.household, "        ")

    outputs: list[str] = []
    left_out = 0
    for rule in package.rules:
        if rule.id not in result.exported:
            continue
        target = rule.then.assign.target
        if _member(package, target):
            values = [m.get(target, UNKNOWN) for m in evaluated.members]
            if any(is_unknown(v) for v in values):
                left_out += 1
                continue
            rendered = f"[{', '.join(_scalar(v) for v in values)}]"
        else:
            value = evaluated.household.get(target, UNKNOWN)
            if is_unknown(value):
                left_out += 1
                continue
            rendered = _scalar(value)
        outputs.append(f"    {_identifier(target)}: {rendered}")

    if not outputs:
        raise ValueError(f"{name}: the evaluator knows no exported value for this "
                         "household, so there is nothing to test")
    if left_out:
        lines.append(f"  # {left_out} exported variable(s) left out: the evaluator says "
                     "unknown, and OpenFisca's default is not an expected answer.")
    return "\n".join([*lines, "  output:", *outputs]) + "\n"


def test_file(package: RulePackage, result: Export, evaluator: Evaluator,
              cases: dict[str, Context]) -> str:
    """A YAML test file for several households, ready for `openfisca test`."""
    header = (f"# Generated from {package.package_id} by RuleWeaver. Expected values come "
              "from the\n# deterministic evaluator; regenerate rather than edit.\n\n")
    return header + "\n".join(
        test_case(package, result, evaluator, name, ctx) for name, ctx in cases.items())
