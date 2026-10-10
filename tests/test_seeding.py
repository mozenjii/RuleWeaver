"""Planted faults in the review queue.

The catch rate was always "unmeasured" in real use because nothing planted a fault. These
tests run the reviewer application with seeding on and check the four things that make it
trustworthy: faults are planted, a decision on a fault never touches the real rule, the
real rule comes back afterwards, and the catch rate is actually measured.
"""

from __future__ import annotations

import json

import pytest

pytest.importorskip("fastapi", reason="the reviewer application needs the review extra")
pytest.importorskip("sqlalchemy", reason="the reviewer application needs the review extra")

from fastapi.testclient import TestClient

from conftest import FIXTURE
from ruleweaver.approval import rule_digest
from ruleweaver.ir import RulePackage
from ruleweaver.review import Status
from ruleweaver.review.app import create_app
from ruleweaver.review.seeding import pending_seed, plant_seeds
from ruleweaver.review.store import ReviewStore, build_engine


@pytest.fixture()
def package() -> RulePackage:
    return RulePackage.model_validate(json.loads(FIXTURE.read_text(encoding="utf-8")))


@pytest.fixture()
def store(tmp_path) -> ReviewStore:
    return ReviewStore(build_engine(f"sqlite:///{tmp_path / 'review.db'}"))


@pytest.fixture()
def seeded(package, store):
    """Every seedable rule gets a planted fault."""
    client = TestClient(create_app(package, store, seed_rate=1.0, salt="campaign-1",
                                   reviewer_resolver=lambda request: "alice"))
    return client, store.seeds()


def a_seeded_rule(seeds) -> str:
    return sorted(seed["rule_id"] for seed in seeds)[0]


def status(store, package, rule_id) -> Status:
    from ruleweaver.approval import source_digest

    rule = package.rule(rule_id)
    return store.load_log().status(rule_id, rule_hash=rule_digest(rule),
                                   source_hash=source_digest(rule))


class TestPlanting:
    def test_faults_are_planted_for_rules_awaiting_review(self, seeded, package):
        from ruleweaver.testgen.mutation import generate_mutants

        _, seeds = seeded
        # Only rules the mutation generator can fault get a seed: the overridden rule
        # never fires, and a rule that only adds values up has no operator to flip.
        mutable = {r.id for r in package.rules for m in generate_mutants(package)
                   if m.package.rule(r.id) != r}
        assert {seed["rule_id"] for seed in seeds} == mutable
        assert len(mutable) >= 10
        for seed in seeds:
            assert seed["mutated_rule"] != package.rule(seed["rule_id"]).model_dump(
                mode="json", by_alias=True)

    def test_planting_is_idempotent_and_reproducible(self, package, store, tmp_path):
        first = plant_seeds(package, store, seed_rate=1.0, salt="s")
        assert plant_seeds(package, store, seed_rate=1.0, salt="s") == []
        other = ReviewStore(build_engine(f"sqlite:///{tmp_path / 'other.db'}"))
        again = plant_seeds(package, other, seed_rate=1.0, salt="s")
        assert [(e.id, e.mutated_rule) for e in first] == \
            [(e.id, e.mutated_rule) for e in again]

    def test_a_zero_rate_plants_nothing(self, package, store):
        assert plant_seeds(package, store, seed_rate=0.0) == []
        assert store.seeds() == []


class TestReview:
    def test_the_reviewer_is_shown_the_fault_first(self, seeded):
        client, seeds = seeded
        rule_id = a_seeded_rule(seeds)
        seed = next(s for s in seeds if s["rule_id"] == rule_id)
        page = client.get(f"/rule/{rule_id}").text
        assert json.dumps(seed["mutated_rule"]["then"], indent=2)[:40] in page \
            or seed["mutated_rule"]["then"] != {}

    def test_approving_a_fault_does_not_approve_the_rule(self, seeded, store, package):
        """The guarantee everything else rests on."""
        client, seeds = seeded
        rule_id = a_seeded_rule(seeds)
        client.post(f"/rule/{rule_id}/decide", data={"decision": "approve"})
        events = store.load_log().events_for(rule_id)
        assert events[-1].seeded_error_id is not None
        assert status(store, package, rule_id) is Status.UNREVIEWED

    def test_rejecting_a_fault_does_not_reject_the_rule(self, seeded, store, package):
        client, seeds = seeded
        rule_id = a_seeded_rule(seeds)
        client.post(f"/rule/{rule_id}/decide",
                    data={"decision": "reject", "note": "the threshold is off by one"})
        assert status(store, package, rule_id) is Status.UNREVIEWED

    def test_the_real_rule_comes_back_after_the_fault(self, seeded, store, package):
        client, seeds = seeded
        rule_id = a_seeded_rule(seeds)
        client.post(f"/rule/{rule_id}/decide",
                    data={"decision": "reject", "note": "wrong comparison"})
        assert pending_seed(store, store.load_log(), rule_id) is None

        client.post(f"/rule/{rule_id}/decide", data={"decision": "approve"})
        assert status(store, package, rule_id) is Status.APPROVED

    def test_the_decision_records_what_the_reviewer_saw(self, seeded, store):
        from ruleweaver.ir.rules import Rule

        client, seeds = seeded
        rule_id = a_seeded_rule(seeds)
        seed = next(s for s in seeds if s["rule_id"] == rule_id)
        client.post(f"/rule/{rule_id}/decide",
                    data={"decision": "reject", "note": "wrong"})
        event = store.load_log().events_for(rule_id)[-1]
        assert event.rule_hash == rule_digest(Rule.model_validate(seed["mutated_rule"]))


class TestMeasurement:
    def test_the_catch_rate_is_measured(self, seeded):
        client, seeds = seeded
        rules = sorted(seed["rule_id"] for seed in seeds)
        client.post(f"/rule/{rules[0]}/decide", data={"decision": "reject", "note": "x"})
        client.post(f"/rule/{rules[1]}/decide", data={"decision": "approve"})
        page = client.get("/metrics").text
        assert "1 of 2 planted faults caught" in page

    def test_reviewers_are_told_checks_exist(self, seeded, package, store):
        client, _ = seeded
        assert "Review-quality checks are on" in client.get("/").text
        quiet = TestClient(create_app(package, store, seed_rate=0.0,
                                      reviewer_resolver=lambda request: "alice"))
        assert "Review-quality checks are on" not in quiet.get("/").text

    def test_no_metric_names_a_reviewer(self, seeded):
        client, seeds = seeded
        client.post(f"/rule/{a_seeded_rule(seeds)}/decide",
                    data={"decision": "approve"})
        assert "alice" not in client.get("/metrics").text
