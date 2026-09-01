"""The reviewer application.

Route tests, plus the two behaviours that decide whether the gate is real: a rejection
cannot be recorded without a reason, and an approval expires when its source moves.
"""

from __future__ import annotations

import json
import re

import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient

from conftest import FIXTURE
from ruleweaver.ir import RulePackage
from ruleweaver.review import Decision
from ruleweaver.review.app import create_app
from ruleweaver.review.identity import SignedTokenResolver, mint_token
from ruleweaver.review.store import ReviewStore, build_engine

RULE = "rule.snap.gross_income_test"


@pytest.fixture()
def package() -> RulePackage:
    return RulePackage.model_validate(json.loads(FIXTURE.read_text(encoding="utf-8")))


@pytest.fixture()
def store(tmp_path) -> ReviewStore:
    return ReviewStore(build_engine(f"sqlite:///{tmp_path / 'review.db'}"))


@pytest.fixture()
def client(package, store) -> TestClient:
    app = create_app(package, store, reviewer_resolver=lambda request: "alice")
    return TestClient(app)


class TestQueue:
    def test_lists_every_rule(self, client, package):
        body = client.get("/").text
        for rule in package.rules:
            assert rule.id in body

    def test_shows_the_pending_count(self, client, package):
        assert f"<strong>{len(package.rules)}</strong> awaiting review" in client.get("/").text

    def test_explains_what_stale_means(self, client):
        # A status nobody can interpret is a status nobody acts on.
        assert "approved against a source that has" in client.get("/").text

    @pytest.mark.parametrize("path", ["/", f"/rule/{RULE}", "/metrics"])
    def test_every_page_requires_an_authenticated_reviewer(self, package, store, path):
        def reject(_request):
            raise HTTPException(401, "authentication required")

        guarded = TestClient(create_app(package, store, reviewer_resolver=reject))
        assert guarded.get(path).status_code == 401


class TestDetail:
    def test_shows_the_quoted_clause_beside_the_rule(self, client):
        body = client.get(f"/rule/{RULE}").text
        assert "130 percent of the Federal income poverty levels" in body
        assert "meets_gross_income_test" in body

    def test_offers_every_decision(self, client):
        body = client.get(f"/rule/{RULE}").text
        for decision in Decision:
            if decision is Decision.EDIT:
                continue
            assert decision.value in body
        assert 'value="edit"' not in body

    def test_unknown_rule_is_a_404(self, client):
        assert client.get("/rule/rule.nope").status_code == 404

    def test_times_the_review_in_the_browser(self, client):
        """Server-side timing would measure the network, not the reviewer."""
        assert "performance.now()" in client.get(f"/rule/{RULE}").text


class TestDecisions:
    def test_records_an_approval(self, client, store):
        r = client.post(f"/rule/{RULE}/decide",
                        data={"decision": "approve", "duration_seconds": "42.5"},
                        follow_redirects=False)
        assert r.status_code == 303
        [event] = store.events(RULE)
        assert event.decision is Decision.APPROVE
        assert event.reviewer == "alice"
        assert event.duration_seconds == 42.5

    def test_rejection_without_a_reason_is_refused(self, client, store):
        r = client.post(f"/rule/{RULE}/decide", data={"decision": "reject"})
        assert r.status_code == 400
        assert store.events(RULE) == []  # nothing stored

    def test_rejection_with_a_reason_is_recorded(self, client, store):
        r = client.post(f"/rule/{RULE}/decide",
                        data={"decision": "reject", "note": "threshold reads 130, not 100"},
                        follow_redirects=False)
        assert r.status_code == 303
        assert store.events(RULE)[0].note.startswith("threshold reads")

    def test_unknown_decision_is_refused(self, client):
        assert client.post(f"/rule/{RULE}/decide", data={"decision": "looks_fine"}).status_code == 400

    def test_edit_is_not_offered_until_an_edited_rule_can_be_applied(self, client, store):
        response = client.post(f"/rule/{RULE}/decide", data={"decision": "edit"})
        assert response.status_code == 400
        assert store.events(RULE) == []

    def test_blocking_diagnostics_cannot_be_approved(self, package, store):
        blocked = package.model_copy(deep=True)
        blocked.ambiguities[0] = blocked.ambiguities[0].model_copy(update={
            "blocking": True,
            "affects": [RULE],
            "resolution": None,
        })
        guarded = TestClient(create_app(blocked, store, reviewer_resolver=lambda request: "alice"))

        response = guarded.post(f"/rule/{RULE}/decide", data={"decision": "approve"})

        assert response.status_code == 409
        assert store.events(RULE) == []

    def test_cookie_authenticated_decisions_require_a_csrf_token(self, package, store):
        secret = "s" * 48
        app = create_app(
            package,
            store,
            reviewer_resolver=SignedTokenResolver(secret),
            csrf_secret=secret,
        )
        guarded = TestClient(app)
        guarded.cookies.set("rw_session", mint_token("alice", secret))

        missing = guarded.post(f"/rule/{RULE}/decide", data={"decision": "approve"})
        assert missing.status_code == 403

        detail = guarded.get(f"/rule/{RULE}")
        token = re.search(r'name="csrf_token" value="([^"]+)"', detail.text)
        assert token is not None
        accepted = guarded.post(
            f"/rule/{RULE}/decide",
            data={"decision": "approve", "csrf_token": token.group(1)},
            follow_redirects=False,
        )
        assert accepted.status_code == 303

    def test_history_appears_after_deciding(self, client):
        client.post(f"/rule/{RULE}/decide",
                    data={"decision": "approve", "duration_seconds": "30"})
        body = client.get(f"/rule/{RULE}").text
        assert "alice" in body and "30s" in body


class TestStaleness:
    def test_an_approval_expires_when_its_source_moves(self, package, store, tmp_path):
        """The case that matters: the clause was re-fetched and now differs. Nobody has
        to remember to re-check — the status changes on its own."""
        app = create_app(package, store, reviewer_resolver=lambda r: "alice")
        client = TestClient(app)
        client.post(f"/rule/{RULE}/decide", data={"decision": "approve"})
        assert "approved" in client.get("/").text

        # The source text underneath the rule changes.
        mutated = package.model_copy(deep=True)
        rule = next(r for r in mutated.rules if r.id == RULE)
        rule.sources[0].quote = "amended text"
        restarted = TestClient(create_app(mutated, store, reviewer_resolver=lambda r: "alice"))
        assert "stale" in restarted.get("/").text


class TestIdentity:
    def test_missing_identity_is_rejected(self, package, store):
        """An audit log whose reviewer field is optional is not an audit log."""
        from ruleweaver.review.identity import InsecureReviewerResolver

        with pytest.warns(RuntimeWarning, match="not fit for deployment|unfit|Anyone can claim"):
            resolver = InsecureReviewerResolver()
        client = TestClient(create_app(package, store, reviewer_resolver=resolver))
        assert client.post(f"/rule/{RULE}/decide", data={"decision": "approve"}).status_code == 401

    def test_the_insecure_resolver_warns_loudly(self):
        from ruleweaver.review.identity import InsecureReviewerResolver

        with pytest.warns(RuntimeWarning):
            InsecureReviewerResolver()

    def test_an_unconfigured_application_refuses_to_start(self, package, store,
                                                          monkeypatch):
        """The default used to be the insecure resolver, so a deployment that forgot to
        configure identity still served and still recorded approvals — against a name the
        client chose. That is now a startup failure."""
        from ruleweaver.review import identity

        for name in (identity.ENV_SECRET, identity.ENV_TRUSTED_HEADER,
                     identity.ENV_TRUSTED_PEERS, identity.ENV_ALLOW_INSECURE):
            monkeypatch.delenv(name, raising=False)

        with pytest.raises(identity.IdentityNotConfigured):
            create_app(package, store)


class TestMetricsPage:
    def test_unmeasured_catch_rate_is_not_shown_as_zero(self, client):
        body = client.get("/metrics").text
        assert "unmeasured" in body

    def test_reports_the_chain_as_intact(self, client):
        client.post(f"/rule/{RULE}/decide", data={"decision": "approve"})
        assert "intact" in client.get("/metrics").text

    def test_surfaces_rubber_stamping(self, package, store):
        app = create_app(package, store, reviewer_resolver=lambda r: "alice")
        client = TestClient(app)
        for rule in package.rules:
            client.post(f"/rule/{rule.id}/decide",
                        data={"decision": "approve", "duration_seconds": "2"})
        body = client.get("/metrics").text
        assert "rubber-stamping" in body

    def test_reports_a_broken_chain(self, client, store):
        from sqlalchemy import text

        client.post(f"/rule/{RULE}/decide", data={"decision": "approve"})
        with store.engine.begin() as conn:
            conn.execute(text("UPDATE review_events SET reviewer = 'mallory'"))
        assert "Chain broken" in client.get("/metrics").text
