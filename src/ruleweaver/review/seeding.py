"""Planting deliberate faults in the review queue — the part of ADR-021 that was missing.

`adversarial.py` could choose which rules to seed and score the log against seeds, but
nothing ever planted one, so in real use the catch rate was always unmeasured.

A seed is a mutant of a real rule: one fault of the kind a mis-extraction actually
produces (a flipped comparison, a dropped exception, a perturbed threshold), taken from
the same generator the mutation harness uses. Until a reviewer rules on it, the queue
shows the mutant in place of the rule. The decision is recorded against the seed, never
against the rule — `ReviewLog.latest_for` skips seeded decisions — and once resolved the
real rule comes back for its own review. Approving a fault therefore costs a missed catch,
never an approval of anything.

Reviewers are told that planted faults exist and at what rate; which items are planted is
not disclosed. The metrics built on them are aggregate: nothing here reports a person.
"""

from __future__ import annotations

import hashlib

from ..ir.rules import RulePackage
from ..testgen.mutation import generate_mutants
from .adversarial import SeededError, deterministic_seed_choice
from .decisions import Status


def _pick(candidates: list, rule_id: str, salt: str):
    """A deterministic choice among a rule's mutants, so a campaign reproduces."""
    digest = hashlib.sha256(f"pick:{salt}:{rule_id}".encode()).digest()
    return candidates[int.from_bytes(digest[:4], "big") % len(candidates)]


def plant_seeds(package: RulePackage, store, *, seed_rate: float, salt: str = "",
                statuses: dict[str, Status] | None = None) -> list[SeededError]:
    """Store a seed for each rule the campaign selects, and return what was planted.

    Only rules still awaiting review are seeded — an approved rule is not in front of a
    reviewer — and a rule that already carries a seed gets no second one. A rule with no
    possible mutant (one that is unconditionally overridden, say) is skipped.
    """
    if seed_rate <= 0:
        return []
    already = {seed["rule_id"] for seed in store.seeds()}
    statuses = statuses or {}
    awaiting = [rule for rule in package.rules
                if rule.id not in already
                and statuses.get(rule.id, Status.UNREVIEWED) is not Status.APPROVED
                and deterministic_seed_choice(rule.id, seed_rate, salt)]
    if not awaiting:
        return []

    mutants = generate_mutants(package)
    planted: list[SeededError] = []
    for rule in awaiting:
        original = rule.model_dump(mode="json", by_alias=True)
        candidates = []
        for mutant in mutants:
            changed = mutant.package.rule(rule.id)
            if changed is not None and changed.model_dump(mode="json", by_alias=True) != original:
                candidates.append((mutant, changed))
        if not candidates:
            continue
        mutant, changed = _pick(candidates, rule.id, salt)
        seed_id = "seed." + hashlib.sha256(f"{salt}:{rule.id}".encode()).hexdigest()[:16]
        error = SeededError(id=seed_id, rule_id=rule.id,
                            description=f"{mutant.operator}: {mutant.description}",
                            mutated_rule=changed.model_dump(mode="json", by_alias=True))
        store.record_seed(error)
        planted.append(error)
    return planted


def pending_seed(store, log, rule_id: str) -> dict | None:
    """The seed a reviewer should see for `rule_id`, if one is still unresolved."""
    resolved = {e.seeded_error_id for e in log.events_for(rule_id) if e.seeded_error_id}
    return next((seed for seed in store.seeds()
                 if seed["rule_id"] == rule_id and seed["id"] not in resolved), None)
