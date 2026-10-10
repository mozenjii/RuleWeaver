"""The reviewer application.

One FastAPI process, server-rendered, no JavaScript build step. The whole surface is a
queue, a side-by-side view of clause and rule, and a decision form — which is what the
work actually is for a policy reviewer.

Two design choices carry weight:

**Reviewer identity is authenticated, never self-declared.** The audit log's value is
entirely in "who approved this", so identity resolution is a pluggable dependency rather
than a form field — see `identity.py`. With nothing configured the application refuses to
start rather than falling back to a name the client supplies.

**Review duration is measured in the browser.** The number ADR-021 needs is how long a
human looked at the rule, not how long the request took. The template stamps a monotonic
clock when the rule renders and submits the delta.
"""

from __future__ import annotations

from collections.abc import Callable
from pathlib import Path
from typing import Any

from fastapi import FastAPI, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import text

from ..approval import rule_digest, source_digest
from ..ir.rules import Rule, RulePackage
from ..verify import validate
from .adversarial import AdversarialQueue
from .decisions import Decision, ReviewEvent, Status
from .identity import resolver_from_env
from .seeding import pending_seed, plant_seeds
from .store import ReviewStore

TEMPLATES = Path(__file__).parent / "templates"


def _rule(package: RulePackage, rule_id: str):
    rule = package.rule(rule_id)
    if rule is None:
        raise HTTPException(404, f"unknown rule: {rule_id}")
    return rule


def _rule_hash(package: RulePackage, rule_id: str) -> str:
    """The digest the runtime gate will check this approval against.

    Delegated to `approval` rather than computed here. The reviewer records a hash and the
    gate recomputes it; if the two ever disagreed, every approval would read as stale — or
    worse, a stale one would read as current.
    """
    return rule_digest(_rule(package, rule_id))


def _source_hash(package: RulePackage, rule_id: str) -> str:
    """Digest of the source spans a rule cites.

    Hashing the citations rather than the rule means an approval goes stale when the
    clause it rests on is re-fetched and differs — which is the case that matters and the
    one nobody remembers to check.
    """
    return source_digest(_rule(package, rule_id))


def _correction(raw: str, rule_id: str) -> dict:
    """The corrected rule from the review form, or a 400 saying what is wrong with it.

    It must be a valid rule and keep the rule's id: an edit corrects one rule, it does
    not swap in a different one.
    """
    import json

    from ..ir.rules import Rule

    if not raw.strip():
        raise HTTPException(400, "an edit must include the corrected rule")
    try:
        rule = Rule.model_validate(json.loads(raw))
    except Exception as exc:
        raise HTTPException(400, f"the corrected rule is not a valid rule: {exc}") from exc
    if rule.id != rule_id:
        raise HTTPException(400, f"an edit of {rule_id} cannot change the rule id")
    return rule.model_dump(mode="json", by_alias=True)


def create_app(
    package: RulePackage,
    store: ReviewStore,
    *,
    reviewer_resolver: Callable[[Request], str] | None = None,
    seed_rate: float = 0.0,
    salt: str = "",
) -> FastAPI:
    """The reviewer application.

    `seed_rate` is the share of rules shown first as a planted fault. It is off by
    default for a library caller; `ruleweaver review` turns it on at 10%.
    """
    app = FastAPI(title="RuleWeaver review", docs_url=None, redoc_url=None)
    templates = Jinja2Templates(directory=str(TEMPLATES))
    # Fails closed when nothing is configured. Recording approvals against an
    # identity the client chose is worse than refusing to start: it produces a
    # log that looks like evidence.
    resolve_reviewer = reviewer_resolver or resolver_from_env()

    def status_of_with(log, rule_id: str) -> Status:
        return log.status(
            rule_id,
            rule_hash=_rule_hash(package, rule_id),
            source_hash=_source_hash(package, rule_id),
        )

    report = validate(package)
    if seed_rate > 0:
        plant_seeds(package, store, seed_rate=seed_rate, salt=salt,
                    statuses={r.id: status_of_with(store.load_log(), r.id)
                              for r in package.rules})

    def current_queue() -> AdversarialQueue:
        return AdversarialQueue(store.load_log(), seed_rate=seed_rate, salt=salt)

    def status_of(rule_id: str) -> Status:
        return status_of_with(store.load_log(), rule_id)

    def shown(rule_id: str, log) -> tuple[Rule | None, dict | None]:
        """The rule a reviewer sees: a pending planted fault, or the rule itself."""
        seed = pending_seed(store, log, rule_id) if seed_rate > 0 else None
        if seed is not None:
            return Rule.model_validate(seed["mutated_rule"]), seed
        return package.rule(rule_id), None

    @app.get("/healthz")
    def healthz():
        """For a load balancer or orchestrator. Checks the audit log can be reached.

        A review application that serves pages but cannot write decisions is down, not
        degraded, so an unreachable database is a 503 rather than a cheerful "ok".
        Unauthenticated, and says nothing about the rules or reviewers.
        """
        try:
            with store.engine.connect() as connection:
                connection.execute(text("SELECT 1"))
        except Exception:
            return JSONResponse({"status": "unavailable"}, status_code=503)
        return {"status": "ok"}

    @app.get("/", response_class=HTMLResponse)
    def queue(request: Request):
        rows: list[dict[str, Any]] = [
            {
                "rule": rule,
                "status": status_of(rule.id),
                "diagnostics": [d for d in report.diagnostics if d.rule_id == rule.id],
            }
            for rule in package.rules
        ]
        # Unreviewed first — a queue sorted by id buries the work.
        order = {Status.UNREVIEWED: 0, Status.STALE: 1, Status.EDIT_PENDING: 2,
                 Status.AMBIGUOUS: 3, Status.HUMAN_JUDGMENT_REQUIRED: 4,
                 Status.REJECTED: 5, Status.APPROVED: 6}
        rows.sort(key=lambda r: order.get(r["status"], 9))
        return templates.TemplateResponse(
            request, "queue.html",
            {"rows": rows, "package": package, "seed_rate": seed_rate,
             "pending": sum(1 for r in rows if r["status"] is Status.UNREVIEWED)},
        )

    @app.get("/rule/{rule_id}", response_class=HTMLResponse)
    def detail(request: Request, rule_id: str):
        if package.rule(rule_id) is None:
            raise HTTPException(404, f"unknown rule: {rule_id}")
        log = store.load_log()
        rule, _ = shown(rule_id, log)
        return templates.TemplateResponse(
            request, "detail.html",
            {
                "rule": rule,
                "package": package,
                "status": status_of(rule_id),
                "history": log.events_for(rule_id),
                "diagnostics": [d for d in report.diagnostics if d.rule_id == rule_id],
                "ambiguities": [a for a in package.ambiguities if rule_id in a.affects],
                "decisions": list(Decision),
            },
        )

    @app.post("/rule/{rule_id}/decide")
    def submit(
        request: Request,
        rule_id: str,
        decision: str = Form(...),
        note: str = Form(""),
        duration_seconds: float = Form(0.0),
        edited_to: str = Form(""),
    ):
        reviewer = resolve_reviewer(request)
        try:
            chosen = Decision(decision)
        except ValueError as exc:
            raise HTTPException(400, f"unknown decision: {decision}") from exc

        correction = None
        if chosen is Decision.EDIT:
            correction = _correction(edited_to, rule_id)

        displayed, seeded = shown(rule_id, store.load_log())

        try:
            event = ReviewEvent(
                rule_id=rule_id,
                reviewer=reviewer,
                decision=chosen,
                # What the reviewer actually saw — the mutant, when one was shown.
                rule_hash=rule_digest(displayed) if displayed is not None
                else _rule_hash(package, rule_id),
                source_hash=_source_hash(package, rule_id),
                duration_seconds=duration_seconds or None,
                note=note or None,
                seeded_error_id=seeded["id"] if seeded else None,
                edited_to=correction,
            )
        except ValueError as exc:
            # A rejection without a reason. Send them back rather than storing a
            # decision the next reviewer cannot act on.
            raise HTTPException(400, str(exc)) from exc

        store.append(event)
        return RedirectResponse(f"/rule/{rule_id}", status_code=303)

    @app.get("/metrics", response_class=HTMLResponse)
    def metrics(request: Request):
        queue = current_queue()
        for seed in store.seeds():
            from .adversarial import SeededError

            queue.register(SeededError(
                id=seed["id"], rule_id=seed["rule_id"], description=seed["description"],
                mutated_rule=seed["mutated_rule"],
                expected_decision=Decision(seed["expected_decision"]),
                seeded_at=seed["seeded_at"],
            ))
        m = queue.metrics()
        intact, broken_at = store.verify_chain()
        return templates.TemplateResponse(
            request, "metrics.html",
            {"metrics": m, "warnings": m.warnings(),
             "chain_intact": intact, "broken_at": broken_at},
        )

    return app
