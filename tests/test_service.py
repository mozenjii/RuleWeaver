"""The calculation service.

Most of these are about the three behaviours that are the product: only approved rules
run, unknown is returned as an answer rather than a default, and inputs are checked so a
typo cannot become a zero income.
"""

from __future__ import annotations

import json

import pytest

pytest.importorskip("fastapi", reason="the service needs the service extra")
pytest.importorskip("sqlalchemy", reason="the service needs the service extra")

from fastapi.testclient import TestClient
from sqlalchemy import text

from conftest import FIXTURE, with_tables
from ruleweaver.approval import current_hashes
from ruleweaver.cli import main
from ruleweaver.ir import RulePackage
from ruleweaver.review import Decision, ReviewEvent
from ruleweaver.review.store import ReviewStore, build_engine
from ruleweaver.service import NOTICE, KeyStore, create_api

PACKAGE_ID = "snap.income_eligibility"

BASELINE = {
    "on_date": "2026-01-01",
    "household": {"var.household.size": 3, "var.household.jurisdiction": "48_dc",
                  "var.household.shelter_expenses": "900"},
    "members": [
        {"var.member.age": 34, "var.member.receives_disability_benefit": False,
         "var.member.earned_income": "1500", "var.member.unearned_income": 0},
        {"var.member.age": 8, "var.member.receives_disability_benefit": False,
         "var.member.earned_income": 0, "var.member.unearned_income": 0},
        {"var.member.age": 6, "var.member.receives_disability_benefit": False,
         "var.member.earned_income": 0, "var.member.unearned_income": 0},
    ],
}


@pytest.fixture()
def package() -> RulePackage:
    return with_tables(RulePackage.model_validate(
        json.loads(FIXTURE.read_text(encoding="utf-8"))))


@pytest.fixture()
def engine(tmp_path):
    return build_engine(f"sqlite:///{tmp_path / 'service.db'}")


def approve(package: RulePackage, engine, *, skip: tuple[str, ...] = ()) -> None:
    store = ReviewStore(engine)
    for rule_id, (rule_hash, source_hash) in current_hashes(package).items():
        if rule_id not in skip:
            store.append(ReviewEvent(rule_id=rule_id, reviewer="alice",
                                     decision=Decision.APPROVE,
                                     rule_hash=rule_hash, source_hash=source_hash))


@pytest.fixture()
def keys(engine) -> KeyStore:
    return KeyStore(engine)


@pytest.fixture()
def api(package, engine) -> TestClient:
    return TestClient(create_api({PACKAGE_ID: package}, engine))


@pytest.fixture()
def auth(keys) -> dict[str, str]:
    _, plaintext = keys.create("acme")
    return {"Authorization": f"Bearer {plaintext}"}


def evaluate(api, auth, body=None, package_id=PACKAGE_ID):
    return api.post(f"/v1/packages/{package_id}/evaluate", json=body or BASELINE,
                    headers=auth)


class TestAuthentication:
    def test_health_needs_no_key(self, api):
        response = api.get("/v1/health")
        assert response.status_code == 200
        assert response.json()["status"] == "ok"

    @pytest.mark.parametrize("header", [None, "Bearer nonsense", "Bearer rw_wrong",
                                        "Basic dXNlcjpwYXNz"])
    def test_everything_else_needs_a_valid_key(self, api, header):
        headers = {"Authorization": header} if header else {}
        assert api.get("/v1/packages", headers=headers).status_code == 401
        assert evaluate(api, headers).status_code == 401

    def test_a_revoked_key_stops_working(self, api, keys):
        record, plaintext = keys.create("acme")
        headers = {"Authorization": f"Bearer {plaintext}"}
        assert api.get("/v1/packages", headers=headers).status_code == 200
        assert keys.revoke(record.id)
        assert api.get("/v1/packages", headers=headers).status_code == 401

    def test_only_a_digest_of_the_key_is_stored(self, keys, engine):
        _, plaintext = keys.create("acme")
        with engine.connect() as connection:
            rows = connection.execute(text("SELECT * FROM api_keys")).fetchall()
        assert plaintext not in json.dumps([list(map(str, row)) for row in rows])


class TestTheGate:
    def test_nothing_runs_until_rules_are_approved(self, api, auth):
        """Unapproved rules decide nothing: every value is null and listed as unknown."""
        body = evaluate(api, auth).json()
        assert body["gate"]["complete"] is False
        assert len(body["gate"]["blocked"]) == 15
        assert body["outputs"]["household"]["var.household.is_income_eligible"] is None
        assert "var.household.is_income_eligible" in body["unknown"]

    def test_approved_rules_produce_the_evaluators_answer(self, api, auth, package, engine):
        approve(package, engine)
        body = evaluate(api, auth).json()
        household = body["outputs"]["household"]
        assert body["gate"]["complete"] is True
        assert household["var.household.is_income_eligible"] is True
        assert household["var.household.net_monthly_income"] == "594.0000"
        assert household["var.household.standard_deduction"] == "204"
        assert body["notice"] == NOTICE

    def test_an_unapproved_override_withholds_rather_than_undercuts(self, api, auth,
                                                                    package, engine):
        """The service inherits the gate's fix: a deduction below the statutory minimum
        is never returned while the minimum is unapproved."""
        approve(package, engine, skip=("rule.snap.standard_deduction_minimum",))
        body = evaluate(api, auth).json()
        assert body["outputs"]["household"]["var.household.standard_deduction"] is None
        assert body["gate"]["withheld"] == ["rule.snap.standard_deduction_computed"]

    def test_the_trace_names_the_rule_behind_each_value(self, api, auth, package, engine):
        approve(package, engine)
        trace = evaluate(api, auth, {**BASELINE, "trace": True}).json()["trace"]
        assert {"rule": "rule.snap.excess_shelter_deduction",
                "target": "var.household.excess_shelter_deduction",
                "scope": "household",
                "via": "exception:exception.snap.shelter_cap_applies",
                "value": "402.0000"} in trace


class TestDecisionRecord:
    """Enough to answer "why did you compute this?" for one person, months later."""

    def test_the_record_pins_the_package_and_the_review_state(self, api, auth, package,
                                                               engine):
        from ruleweaver.hashing import digest

        approve(package, engine)
        record = evaluate(api, auth).json()["record"]
        _, head = ReviewStore(engine).snapshot()
        assert record["package_hash"] == digest(package.model_dump(mode="json"))
        assert record["review_log_head"] == head
        assert len(record["rules_applied"]) == 15

    def test_a_later_approval_moves_the_head(self, api, auth, package, engine):
        """Two answers given under different review states must be distinguishable."""
        before = evaluate(api, auth).json()["record"]["review_log_head"]
        approve(package, engine)
        after = evaluate(api, auth).json()["record"]["review_log_head"]
        assert before != after

    def test_withheld_and_blocked_rules_are_not_listed_as_applied(self, api, auth,
                                                                   package, engine):
        approve(package, engine, skip=("rule.snap.standard_deduction_minimum",))
        applied = evaluate(api, auth).json()["record"]["rules_applied"]
        assert "rule.snap.standard_deduction_minimum" not in applied
        assert "rule.snap.standard_deduction_computed" not in applied

    def test_the_notice_claims_no_reviewer_it_cannot_name(self):
        assert "named reviewer" not in NOTICE
        assert "not legal advice" in NOTICE

    def test_healthz_is_an_alias_for_container_health_checks(self, api):
        """The Dockerfile's HEALTHCHECK calls /healthz whichever app the image runs."""
        assert api.get("/healthz").json()["status"] == "ok"


class TestInputs:
    def test_an_explicit_null_is_unknown_not_zero(self, api, auth, package, engine):
        approve(package, engine)
        body = json.loads(json.dumps(BASELINE))
        body["members"][0]["var.member.earned_income"] = None
        result = evaluate(api, auth, body).json()
        assert result["outputs"]["household"]["var.household.is_income_eligible"] is None
        assert "var.household.gross_monthly_income" in result["unknown"]

    @pytest.mark.parametrize(("where", "key", "value", "message"), [
        ("member", "var.member.earned_incom", "1500", "is not a variable"),
        ("household", "var.household.is_income_eligible", True, "computed by the rules"),
        ("household", "var.member.age", 30, "belongs to the household_member"),
        ("member", "var.member.receives_disability_benefit", "no", "true or false"),
        ("member", "var.member.earned_income", "lots", "must be a number"),
        ("member", "var.member.earned_income", True, "must be a number"),
        ("household", "var.household.jurisdiction", 48, "must be a string"),
    ])
    def test_bad_input_is_refused_not_ignored(self, api, auth, where, key, value, message):
        """A misspelled income left unsupplied is how a typo becomes an eligibility."""
        body = json.loads(json.dumps(BASELINE))
        target = body["members"][0] if where == "member" else body["household"]
        target[key] = value
        response = evaluate(api, auth, body)
        assert response.status_code == 422
        assert any(message in error for error in response.json()["detail"]["errors"])

    def test_an_unknown_package_is_404(self, api, auth):
        assert evaluate(api, auth, package_id="nope").status_code == 404

    def test_a_household_size_is_bounded(self, api, auth):
        body = {**BASELINE, "members": BASELINE["members"] * 20}
        assert evaluate(api, auth, body).status_code == 422


class TestValidateAndUsage:
    def test_validate_reports_a_good_package(self, api, auth):
        document = json.loads(FIXTURE.read_text(encoding="utf-8"))
        body = api.post("/v1/validate", json=document, headers=auth).json()
        assert body["ok"] is True

    def test_validate_reports_a_broken_one(self, api, auth):
        body = api.post("/v1/validate", json={"package_id": "x"}, headers=auth).json()
        assert body["ok"] is False and body["diagnostics"]

    def test_usage_is_metered_per_organisation(self, api, auth, keys):
        evaluate(api, auth)
        evaluate(api, auth)
        api.post("/v1/validate", json={}, headers=auth)
        assert api.get("/v1/usage", headers=auth).json()["calls"] == \
            {"evaluate": 2, "validate": 1}

        _, other = keys.create("globex")
        other_usage = api.get("/v1/usage", headers={"Authorization": f"Bearer {other}"})
        assert other_usage.json()["calls"] == {}

    def test_usage_records_no_household_facts(self, api, auth, engine):
        evaluate(api, auth)
        with engine.connect() as connection:
            rows = connection.execute(text("SELECT * FROM usage_events")).fetchall()
        dumped = json.dumps([list(map(str, row)) for row in rows])
        assert "1500" not in dumped and "48_dc" not in dumped


class TestKeyCommand:
    def test_create_list_revoke(self, tmp_path, capsys):
        database = f"sqlite:///{tmp_path / 'keys.db'}"
        assert main(["api-key", "--database", database, "create", "acme"]) == 0
        captured = capsys.readouterr()
        plaintext = captured.out.strip()
        assert plaintext.startswith("rw_") and "\n" not in plaintext

        assert main(["api-key", "--database", database, "list"]) == 0
        listing = capsys.readouterr().out
        assert "acme" in listing and plaintext not in listing

        key_id = listing.split()[0]
        assert main(["api-key", "--database", database, "revoke", key_id]) == 0
        assert main(["api-key", "--database", database, "revoke", key_id]) == 1
