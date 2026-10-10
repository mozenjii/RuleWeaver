"""The approval gate.

README principle 4 — "No extracted rule is executable in an approved package until it
passes review" — was a stated principle with nothing enforcing it: the evaluator ran any
package handed to it. This module is the enforcement, and it lives outside `review/` on
purpose. Approval is a property of the *runtime*, checked by whatever executes rules; the
reviewer application is only one way to produce the evidence.

Three things are deliberate:

**The gate reads the log, never a flag on the rule.** Status is derived
(`review/decisions.py`), so a rule whose clause was re-fetched and changed falls out of
the approved set without anyone remembering to revoke it.

**Excluding a rule leaves its target unknown, not false.** A filtered package is still a
valid package: the rules that survive reference variables the excluded rules would have
assigned, and those evaluate to `unknown` and propagate. That is the same four-state
behaviour a missing input gets, and it is the honest answer — "this determination rests on
a rule nobody has approved" is not the same claim as "this household does not qualify".

**Hashing is shared with the reviewer.** `rule_digest` and `source_digest` are the
functions the review application records against. Two implementations would drift, and the
failure mode of drift is an approval that silently no longer matches.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .hashing import digest
from .ir import RulePackage
from .ir.rules import Parameter, Rule
from .review.decisions import ReviewLog, Status


def rule_digest(item) -> str:
    """Digest of a rule's or parameter's full structured form — what the reviewer approved.

    For a parameter that includes every dated value, so changing a number moves the
    hash and the old approval stops applying: an uprating is a reviewable change.
    """
    return digest(item.model_dump(mode="json", by_alias=True))


def source_digest(item) -> str:
    """Digest of the source spans an item cites, including a parameter's per-value sources.

    Separate from `rule_digest` so the two staleness causes stay distinguishable: an
    edited rule and a moved clause are different events and want different handling.
    """
    spans = [s.model_dump(mode="json") for s in item.sources]
    for value in getattr(item, "values", []):
        spans.extend(s.model_dump(mode="json") for s in value.sources)
    return digest(spans)


def current_hashes(package: RulePackage) -> dict[str, tuple[str, str]]:
    """Every reviewable item's (hash, source_hash) as it is *now*: rules and parameters.

    Parameters are reviewed like rules. A rule is only as right as the numbers it reads,
    and those numbers change every year.
    """
    items: list[Rule | Parameter] = [*package.rules, *package.parameters]
    return {item.id: (rule_digest(item), source_digest(item)) for item in items}


class NotApproved(Exception):
    """Execution was requested for rules that have not passed review."""

    def __init__(self, statuses: dict[str, Status]) -> None:
        self.statuses = statuses
        lines = "\n".join(f"  {rid}: {st.value}" for rid, st in sorted(statuses.items()))
        super().__init__(
            f"{len(statuses)} rule(s) or parameter table(s) are not approved for "
            f"execution:\n{lines}\n"
            "Review them first, or pass the package through approved_subset() and accept "
            "that determinations resting on unapproved rules will be unknown."
        )


@dataclass
class GateReport:
    """What the gate found. Reported rather than raised so a caller can show it."""

    approved: list[str] = field(default_factory=list)
    blocked: dict[str, Status] = field(default_factory=dict)
    # Parameters pass the same gate. An unapproved table supplies no values, so anything
    # reading it is unknown.
    parameters_approved: list[str] = field(default_factory=list)
    parameters_blocked: dict[str, Status] = field(default_factory=dict)
    # Approved, but not run by `approved_subset`: the reason, by rule id.
    withheld: dict[str, str] = field(default_factory=dict)

    @property
    def ok(self) -> bool:
        return not self.blocked and not self.parameters_blocked

    def __str__(self) -> str:
        if not self.approved and not self.blocked:
            return "no rules"
        parts = [f"{len(self.approved)} approved, {len(self.blocked)} blocked"]
        counts: dict[str, int] = {}
        for status in self.blocked.values():
            counts[status.value] = counts.get(status.value, 0) + 1
        for name in sorted(counts):
            parts.append(f"  {name:28} {counts[name]}")
        for rule_id, reason in sorted(self.withheld.items()):
            parts.append(f"  withheld {rule_id}: {reason}")
        if self.parameters_approved or self.parameters_blocked:
            parts.append(f"parameters: {len(self.parameters_approved)} approved, "
                         f"{len(self.parameters_blocked)} blocked")
        return "\n".join(parts)


def check(package: RulePackage, log: ReviewLog) -> GateReport:
    """Classify every rule and parameter in the package as approved or blocked."""
    report = GateReport()
    rule_ids = {r.id for r in package.rules}
    for item_id, (rh, sh) in current_hashes(package).items():
        status = log.status(item_id, rule_hash=rh, source_hash=sh)
        is_rule = item_id in rule_ids
        if status is Status.APPROVED:
            (report.approved if is_rule else report.parameters_approved).append(item_id)
        else:
            (report.blocked if is_rule else report.parameters_blocked)[item_id] = status
    report.approved.sort()
    report.parameters_approved.sort()
    return report


def approved_subset(package: RulePackage, log: ReviewLog) -> tuple[RulePackage, GateReport]:
    """The package with unapproved rules removed, plus what was removed and why.

    An approved rule that an excluded rule overrides is excluded as well, and listed in
    the report's `withheld`. Entities, variables and parameters are kept whole. Dropping a variable because the only
    rule assigning it was excluded would turn a reference to it into a validation error,
    which reports the wrong problem: the reference is fine, the approval is missing.
    """
    report = check(package, log)
    keep = set(report.approved)

    # A "notwithstanding" clause binds whether or not anyone has approved its encoding.
    # Dropping the unapproved overriding rule used to let the rule it overrides run in
    # its place: with the standard-deduction minimum unapproved, the baseline household
    # got a deduction of 180, below the 204 the regulation guarantees, where the honest
    # answer is unknown. So a rule overridden by an excluded rule is excluded too, and
    # that repeats down a chain of overrides.
    changed = True
    while changed:
        changed = False
        for rule in package.rules:
            if rule.id in keep:
                continue
            for overridden in rule.overrides:
                if overridden in keep:
                    keep.discard(overridden)
                    report.withheld[overridden] = (
                        f"overridden by {rule.id}, which is not approved")
                    changed = True

    # An unapproved parameter keeps its declaration and loses its values, so a rule that
    # reads it gets unknown rather than a number nobody has checked.
    parameters = [p if p.id in report.parameters_approved else p.model_copy(update={"values": []})
                  for p in package.parameters]
    subset = package.model_copy(update={
        "rules": [r for r in package.rules if r.id in keep], "parameters": parameters})
    return subset, report


def enforce(package: RulePackage, log: ReviewLog) -> RulePackage:
    """Return the package only if every rule in it is approved.

    Raises rather than returning a report so a caller who forgets to check cannot
    accidentally execute unapproved rules — the same reasoning as `InvalidPackage`.
    """
    report = check(package, log)
    if not report.ok:
        raise NotApproved({**report.blocked, **report.parameters_blocked})
    return package
