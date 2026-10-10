"""Generating an OpenFisca country package from an approved rule package.

What comes out is a directory an OpenFisca installation can load: an entity model, a
module of `Variable` subclasses, a parameter tree as YAML, and YAML test files built from
the same scenarios the deterministic evaluator runs. The tests matter most — they are the
only thing that makes the claim "this export behaves like the IR" checkable rather than
asserted.

Two refusals are built in.

**Unapproved rules are not exported.** Export is a deployment step, and a rule nobody
signed off reaching a production calculator through an adapter would route straight around
the gate the whole project exists to enforce.

**The four-state gap is reported, every time.** OpenFisca has no unknown; a missing fact
takes the type default. `RW8001` says so on every export and the generated module repeats
it at the top of the file, because a maintainer reading the code months later is the person
who needs to know.

Order of assignment is preserved from the IR rather than recomputed. OpenFisca resolves
dependencies itself by calling variables lazily, so the generated module does not need a
topological sort — but keeping source order makes the generated file diffable against the
package it came from.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import date, timedelta
from decimal import Decimal
from math import prod
from pathlib import Path

from ...approval import check
from ...ir.expressions import Expr, Lit, Ref
from ...ir.rules import Parameter, Rule, RulePackage, Variable
from ...review.decisions import ReviewLog
from ...verify.diagnostics import Diagnostic
from .lowering import Lowered, Lowerer, Unlowerable

_VALUE_TYPES = {
    "boolean": "bool",
    "integer": "int",
    "decimal": "float",
    "money": "float",
    "date": "date",
    "string": "str",
    "enumeration": "str",
}

_PERIODS = {"day": "DAY", "month": "MONTH", "year": "YEAR"}

_UNKNOWN_WARNING = (
    "OpenFisca has no unknown state. A fact nobody supplied takes this variable's type "
    "default — 0 for a number, False for a boolean — so a missing input is "
    "indistinguishable from a genuine zero. The RuleWeaver evaluator keeps those apart "
    "and propagates unknown instead. Determinations that depend on absent facts will "
    "differ between the two, and the difference is an answer rather than a question: a "
    "denial when the missing fact would have qualified the household, an approval when "
    "it would have disqualified it — a blank income reads as no income."
)


def _identifier(name: str) -> str:
    """A Python-safe name from a rule or variable id."""
    cleaned = re.sub(r"[^0-9a-zA-Z_]", "_", name.rsplit(".", 1)[-1])
    return cleaned if not cleaned[:1].isdigit() else f"v_{cleaned}"


@dataclass
class Export:
    """Everything an export produced, including what it refused to produce."""

    files: dict[str, str] = field(default_factory=dict)
    diagnostics: list[Diagnostic] = field(default_factory=list)
    exported: list[str] = field(default_factory=list)
    skipped: dict[str, str] = field(default_factory=dict)

    @property
    def ok(self) -> bool:
        return not [d for d in self.diagnostics if d.severity in ("error", "blocking")]

    def write(self, out_dir: str | Path) -> Path:
        root = Path(out_dir)
        for name, content in self.files.items():
            path = root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
        return root

    def __str__(self) -> str:
        lines = [f"{len(self.exported)} variable(s) exported, {len(self.skipped)} skipped"]
        for rule_id, reason in sorted(self.skipped.items()):
            lines.append(f"  {rule_id}: {reason}")
        for diagnostic in self.diagnostics:
            lines.append(f"  {diagnostic}")
        return "\n".join(lines)


def _describe(expr: Expr) -> str:
    """A short name for an expression, for a refusal message."""
    if isinstance(expr, Ref):
        return expr.id
    return f"a {expr.op!r} expression"


def _lower_rule(rule: Rule) -> Lowered:
    """Lower a rule and its exceptions into one formula.

    Prioritised defaults have a faithful vectorised form. The IR already requires every
    exception on a rule to carry a distinct priority, so the order is total and the
    selection is decidable: the lowest-numbered exception whose condition holds wins, and
    the base expression is the default. That is `np.select` with the cases ascending.

    `disable_base_rule` has no such form. It says the rule produces *nothing*, and
    OpenFisca has no way to express "no value" — the variable would silently take its type
    default, turning a suppressed rule into a zero. Those rules are refused rather than
    approximated.

    A guard is refused for the same reason. When `when` does not hold the rule assigns
    nothing, and the evaluator reports the target as unknown. This used to be dropped
    silently, so the allotment — guarded by income eligibility — was computed for every
    household, eligible or not.
    """
    if not (isinstance(rule.when, Lit) and rule.when.value is True):
        raise Unlowerable(
            f"the rule applies only when {_describe(rule.when)} holds; otherwise it assigns "
            "nothing, and OpenFisca cannot represent a variable with no value, so it would "
            "become a zero")

    lowerer = Lowerer()
    base = lowerer.lower(rule.then.assign.value)
    if not rule.exceptions:
        return base

    for exception in rule.exceptions:
        if exception.effect != "substitute" or exception.substitute is None:
            raise Unlowerable(
                f"exception {exception.id} suppresses the base rule; OpenFisca cannot "
                "represent a variable with no value, so it would become a zero")
        if exception.substitute.assign.target != rule.then.assign.target:
            raise Unlowerable(
                f"exception {exception.id} assigns {exception.substitute.assign.target}, "
                f"not {rule.then.assign.target}; one formula cannot assign two variables")

    # The lowest-numbered matching exception wins (docs/04_RULE_IR_SPEC.md, priority
    # semantics), and np.select takes the first condition that holds — so ascending order.
    # This was descending until the generated package was first run beside the evaluator.
    ordered = sorted(rule.exceptions, key=lambda e: e.priority)
    conditions = []
    values = []
    for exception in ordered:
        conditions.append(lowerer.expression(exception.when))
        assert exception.substitute is not None
        values.append(lowerer.expression(exception.substitute.assign.value))

    lowerer.result.uses_numpy = True
    lowerer.result.source = (
        f"np.select([{', '.join(conditions)}], [{', '.join(values)}], "
        f"default={base.source})")
    return lowerer.result


def _entity(declared: Variable | None) -> str:
    if declared is not None and declared.entity != "household":
        return "Person"
    return "Household"


def _citation(sources: list) -> str:
    if not sources:
        return ""
    span = sources[0]
    citation = span.citation or span.source_id
    if span.quote:
        citation += f"\n        {span.quote}"
    return citation


def _variable_class(package: RulePackage, rule: Rule, lowered: Lowered) -> str:
    """One `Variable` subclass for the target of one rule.

    The formula is dated from the rule's `effective_from`, and `effective_to` becomes the
    variable's `end`. Undated, a formula applies to every period OpenFisca is asked about,
    so a rule would compute values for months before it was law.
    """
    target = rule.then.assign.target
    declared = package.variable(target)
    entity = _entity(declared)

    value_type = _VALUE_TYPES.get(declared.value_type if declared else "decimal", "float")
    period = _PERIODS.get((declared.periodicity if declared else None) or "month", "MONTH")

    args = "person, period, parameters" if entity == "Person" else "household, period, parameters"
    body = lowered.source
    if entity == "Household" and lowered.person_vars:
        # Household formulas reach members through the entity, not through a bare name.
        body = body.replace("person(", "household.members(")
    if entity == "Person" and lowered.household_vars:
        # A member formula reads a household value through the member's household, which
        # projects it onto each member. A bare `household` is not in scope.
        body = re.sub(r"(?<![.\w])household\(", "person.household(", body)

    formula = "formula_" + rule.effective_from.replace("-", "_")
    end = ""
    if rule.effective_to:
        # The IR's effective_to is exclusive; OpenFisca's end is the last day it applies.
        last = date.fromisoformat(rule.effective_to) - timedelta(days=1)
        end = f"    end = {last.isoformat()!r}\n"

    return (
        f"class {_identifier(target)}(Variable):\n"
        f'    """{rule.id}\n\n'
        f"    {_citation(rule.sources)}\n"
        f'    """\n'
        f"    value_type = {value_type}\n"
        f"    entity = {entity}\n"
        f"    definition_period = {period}\n"
        f"    label = {rule.id!r}\n"
        f"{end}\n"
        f"    def {formula}({args}):\n"
        f"        return {body}\n"
    )


def _input_class(variable: Variable) -> str:
    """A variable the caller supplies. No formula: OpenFisca reads it from the situation.

    Without these, OpenFisca refuses any household at all — it will not accept a value
    for a variable the tax-benefit system does not declare.
    """
    citation = _citation(variable.sources)
    doc = variable.id + "\n\n    Input. Supplied by the caller; nothing here computes it."
    if citation:
        doc += f"\n\n    {citation}"
    value_type = _VALUE_TYPES.get(variable.value_type, "float")
    period = _PERIODS.get(variable.periodicity or "month", "MONTH")
    return (
        f"class {_identifier(variable.id)}(Variable):\n"
        f'    """{doc}\n    """\n'
        f"    value_type = {value_type}\n"
        f"    entity = {_entity(variable)}\n"
        f"    definition_period = {period}\n"
        f"    label = {variable.id!r}\n"
    )


def _module(package: RulePackage, classes: list[str], names: list[str]) -> str:
    header = (
        f'"""Generated from {package.package_id} by RuleWeaver. Do not edit by hand.\n\n'
        f"Every variable here corresponds to one approved rule. Edit the rule package and\n"
        f"re-export; an edit made here is invisible to review, to the audit log, and to\n"
        f"the amendment-impact analysis.\n\n"
        f"WARNING — {_UNKNOWN_WARNING}\n"
        f'"""\n\n'
    )
    imports = "from openfisca_core.periods import DAY, MONTH, YEAR\n"
    imports += "from openfisca_core.variables import Variable\n"
    imports += "\nfrom .entities import Household, Person\n"
    # numpy is always needed: the parameter-index helper below is vectorised.
    imports = "import numpy as np\n\n" + imports

    # OpenFisca formulas run over arrays — one entry per household — so a parameter index
    # is an array, and the lookup must be too. The first version formatted one scalar;
    # given an array it produced the key "[3.]", which matches nothing, and no dimensioned
    # table could be read. That was invisible until the package was run.
    helper = (
        "\n\ndef _key(value):\n"
        '    """Format a parameter index, element by element.\n\n'
        "    An index that has been through np.clip is a float, and str(6.0) is \"6.0\",\n"
        "    which matches no parameter node. Whole numbers are formatted as integers so\n"
        "    the lookup finds the key the parameter file actually declares.\n"
        '    """\n'
        "    values = np.asarray(value)\n"
        "    if values.dtype.kind not in \"fiu\":\n"
        "        return values.astype(str)\n"
        "    whole = np.round(values).astype(np.int64)\n"
        "    return np.where(values == whole, whole.astype(str), values.astype(str))\n\n\n"
    )
    listing = "\n\nVARIABLES = [\n" + "".join(f"    {n},\n" for n in names) + "]\n"
    return header + imports + helper + "\n\n".join(classes) + listing


def _package_init(package: RulePackage) -> str:
    """The entry point OpenFisca's own tooling looks for.

    `openfisca test --country-package <name>` and `openfisca serve` import the package
    and instantiate `CountryTaxBenefitSystem`. Variables are added from the explicit list
    rather than with `add_variables_from_file`, which loads a file outside its package and
    so cannot follow the relative import of the entity model.
    """
    return (
        f'"""OpenFisca country package generated from {package.package_id} by RuleWeaver."""\n\n'
        "from pathlib import Path\n\n"
        "from openfisca_core.taxbenefitsystems import TaxBenefitSystem\n\n"
        "from . import entities, variables\n\n\n"
        "class CountryTaxBenefitSystem(TaxBenefitSystem):\n"
        "    def __init__(self):\n"
        "        super().__init__(entities.entities)\n"
        "        self.add_variables(*variables.VARIABLES)\n"
        '        parameters = Path(__file__).parent / "parameters"\n'
        "        if parameters.is_dir():\n"
        "            self.load_parameters(str(parameters))\n"
    )


def _entities() -> str:
    return (
        '"""Generated entity model."""\n\n'
        "from openfisca_core.entities import build_entity\n\n"
        "Household = build_entity(\n"
        '    key="household",\n'
        '    plural="households",\n'
        '    label="A benefit unit assessed together",\n'
        "    roles=[\n"
        '        {"key": "member", "plural": "members", "label": "Member"},\n'
        "    ],\n"
        ")\n\n"
        "Person = build_entity(\n"
        '    key="person",\n'
        '    plural="persons",\n'
        '    label="An individual",\n'
        "    is_person=True,\n"
        ")\n\n"
        "entities = [Household, Person]\n"
    )


def _is_grid(parameter: Parameter) -> bool:
    """Whether the coordinates in use form the full product of each dimension's keys."""
    dimensions = sorted(parameter.dimensions)
    present = {tuple(str(v.at.get(d)) for d in dimensions) for v in parameter.values}
    axes = [{key[i] for key in present} for i in range(len(dimensions))]
    return len(present) == prod(len(axis) for axis in axes)


def _parameters_yaml(package: RulePackage,
                     diagnostics: list[Diagnostic] | None = None) -> dict[str, str]:
    """One YAML file per parameter, in the tree OpenFisca expects.

    Written by hand rather than through a YAML library so the adapter stays dependency
    free — the values are dates, decimals and strings, and the shape is fixed.
    """
    files: dict[str, str] = {}
    for parameter in package.parameters:
        if not parameter.values:
            # A parameter the package declares but never populates. In RuleWeaver it
            # resolves to unknown and the determination stops; in OpenFisca the lookup
            # raises at run time, so the generated package will not load a scenario that
            # touches it. Reported rather than emitted as an empty file, which would look
            # like a table that happens to be empty.
            if diagnostics is not None:
                diagnostics.append(Diagnostic(
                    "RW8005", "error",
                    f"parameter {parameter.id} has no values and cannot be exported",
                    object_id=parameter.id,
                    suggestion="supply the published table, or drop the parameter"))
            continue
        path = parameter.id.removeprefix("param.").replace(".", "/")
        lines = ["description: " + (parameter.note or parameter.id)]
        if parameter.sources and parameter.sources[0].citation:
            lines.append(f"reference: {parameter.sources[0].citation}")

        if parameter.dimensions:
            # A dimensioned parameter becomes nested nodes keyed by coordinate, which is
            # how OpenFisca addresses a scale that is not a bracket schedule.
            if not _is_grid(parameter) and diagnostics is not None:
                # OpenFisca indexes a nested node with an array of keys only when every
                # branch has the same children. A sparse table loads, then fails on the
                # first lookup. Published tables are complete grids; a gap is a gap in
                # the data, and filling it would be inventing policy.
                diagnostics.append(Diagnostic(
                    "RW8007", "error",
                    f"parameter {parameter.id} is not a complete grid over "
                    f"{', '.join(sorted(parameter.dimensions))}; OpenFisca cannot index it",
                    object_id=parameter.id,
                    suggestion="supply a value for every combination of coordinates"))
            grouped: dict[tuple[str, ...], list] = {}
            for value in parameter.values:
                # Sorted, because the lowering indexes the dimensions in sorted order.
                key = tuple(str(value.at[d]) for d in sorted(parameter.dimensions)
                            if d in value.at)
                grouped.setdefault(key, []).append(value)
            for key, values in sorted(grouped.items()):
                node = "/".join(key)
                body = ["values:"]
                for value in sorted(values, key=lambda v: v.effective_from):
                    rendered = value.value
                    if isinstance(rendered, Decimal):
                        rendered = f"{rendered:f}"
                    body.append(f"  {value.effective_from}:")
                    body.append(f"    value: {rendered}")
                files[f"parameters/{path}/{node}.yaml"] = "\n".join(lines + body) + "\n"
        else:
            body = ["values:"]
            for value in sorted(parameter.values, key=lambda v: v.effective_from):
                rendered = value.value
                if isinstance(rendered, Decimal):
                    rendered = f"{rendered:f}"
                body.append(f"  {value.effective_from}:")
                body.append(f"    value: {rendered}")
            files[f"parameters/{path}.yaml"] = "\n".join(lines + body) + "\n"
    return files


def export(
    package: RulePackage,
    *,
    log: ReviewLog | None = None,
    require_approval: bool = True,
) -> Export:
    """Generate an OpenFisca package from the approved rules in `package`.

    `require_approval` defaults to true and should stay that way outside tests. An export
    that skips the gate hands unreviewed rules to a production calculator through the one
    path nobody is watching.
    """
    result = Export()

    approved: set[str] | None = None
    if require_approval:
        report = check(package, log or ReviewLog())
        approved = set(report.approved)
        for rule_id, status in sorted(report.blocked.items()):
            result.skipped[rule_id] = f"not approved ({status.value})"
        if report.blocked:
            result.diagnostics.append(Diagnostic(
                "RW8002", "error",
                f"{len(report.blocked)} rule(s) are not approved and were not exported",
                suggestion="review them, or pass require_approval=False for a dry run "
                           "that must not be deployed"))

    result.diagnostics.append(Diagnostic(
        "RW8001", "warning",
        "OpenFisca has no unknown state; missing inputs take the type default",
        suggestion="treat a determination that depends on an absent fact as unreliable "
                   "in the exported model",
        details={"detail": _UNKNOWN_WARNING}))

    # A "notwithstanding" rule carries the whole formula for its target; the rule it
    # overrides is subsumed, as it is in the evaluator. Emitting both produced two classes
    # with one name, and the override won only because it came later in the file.
    overriders: dict[str, str] = {}
    for rule in package.rules:
        for overridden in rule.overrides:
            overriders.setdefault(overridden, rule.id)

    candidates: list[tuple[Rule, Lowered]] = []
    assigned: dict[str, str] = {}
    for rule in package.rules:
        if approved is not None and rule.id not in approved:
            continue
        if rule.id in overriders:
            result.skipped[rule.id] = (
                f"overridden by {overriders[rule.id]}, which carries the formula for "
                f"{rule.then.assign.target}")
            continue
        target = rule.then.assign.target
        if target in assigned:
            reason = (f"{target} is already assigned by {assigned[target]}; OpenFisca has "
                      "one formula per variable")
            result.skipped[rule.id] = reason
            result.diagnostics.append(Diagnostic(
                "RW8003", "warning", f"rule could not be lowered: {reason}", rule_id=rule.id))
            continue
        try:
            lowered = _lower_rule(rule)
        except Unlowerable as exc:
            result.skipped[rule.id] = str(exc)
            result.diagnostics.append(Diagnostic(
                "RW8003", "warning", f"rule could not be lowered: {exc}",
                rule_id=rule.id))
            continue
        assigned[target] = rule.id
        candidates.append((rule, lowered))

    # OpenFisca has one flat namespace of variable names, so two ids sharing a leaf would
    # silently become one variable.
    inputs = [v for v in package.variables if v.input]
    leaves: dict[str, str] = {}
    for identifier in [v.id for v in inputs] + [r.then.assign.target for r, _ in candidates]:
        leaf = _identifier(identifier)
        if leaf in leaves and leaves[leaf] != identifier:
            result.diagnostics.append(Diagnostic(
                "RW8006", "error",
                f"{identifier} and {leaves[leaf]} both become the OpenFisca variable {leaf}",
                object_id=identifier, suggestion="rename one of them"))
        leaves.setdefault(leaf, identifier)

    # A formula that reads a variable nothing declares fails only when OpenFisca runs it.
    # Refuse it here instead, transitively — the export-time form of the evaluator's
    # unknown propagation under --partial.
    declared = {_identifier(v.id) for v in inputs}
    declared |= {_identifier(r.then.assign.target) for r, _ in candidates}
    changed = True
    while changed:
        changed = False
        for rule, lowered in list(candidates):
            missing = sorted((lowered.person_vars | lowered.household_vars) - declared)
            if not missing:
                continue
            reason = f"needs {', '.join(missing)}, which is not exported"
            result.skipped[rule.id] = reason
            result.diagnostics.append(Diagnostic(
                "RW8003", "warning", f"rule could not be lowered: {reason}", rule_id=rule.id))
            candidates.remove((rule, lowered))
            declared.discard(_identifier(rule.then.assign.target))
            changed = True

    classes = [_input_class(v) for v in inputs]
    names = [_identifier(v.id) for v in inputs]
    for rule, lowered in candidates:
        classes.append(_variable_class(package, rule, lowered))
        names.append(_identifier(rule.then.assign.target))
        result.exported.append(rule.id)

    if result.skipped and not result.exported:
        result.diagnostics.append(Diagnostic(
            "RW8004", "error", "nothing was exported",
            suggestion="an empty country package is not a successful export"))

    result.files["__init__.py"] = _package_init(package)
    result.files["entities.py"] = _entities()
    result.files["variables.py"] = _module(package, classes, names)
    result.files.update(_parameters_yaml(package, result.diagnostics))
    return result
