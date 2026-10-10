"""The calculation service: approved rules, evaluated over HTTP.

What a customer integrates with. It sends a household and receives every value the
approved rules determine, with the rule that produced each one available as a trace.
Three behaviours are the product, not details:

**Only approved rules run.** Every request goes through `approved_subset`. If a package
has rules nobody has approved, the response says so (`gate.complete` is false) and every
value resting on them is null and listed in `unknown` — never a default, never a guess.

**Unknown is an answer.** A value the rules cannot determine from the facts supplied is
returned as null and named in `unknown`. "We cannot tell" and "not eligible" are different
answers, and a caller that conflates them is the one making the decision.

**Inputs are checked strictly.** A misspelled variable is rejected, not ignored. Ignoring
it would leave the real variable unsupplied, and in OpenFisca-style systems that is how a
typo becomes a zero income and an eligibility decision.

Money and other decimals are returned as strings, so no client parses 594.0000 into a
binary float on the way in.

No `from __future__ import annotations` here: FastAPI resolves dependency annotations at
runtime, and a postponed `Caller` defined inside `create_api` would silently become a
query parameter instead of an authentication check.
"""

import copy
import time
from collections import defaultdict, deque
from datetime import UTC, date, datetime
from decimal import Decimal, InvalidOperation
from typing import Annotated, Any

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from sqlalchemy import text
from sqlalchemy.engine import Engine

from .. import __version__
from ..approval import approved_subset
from ..hashing import digest
from ..ir.rules import RulePackage
from ..review.store import ReviewStore
from ..runtime import Context, Evaluator, ParameterTable
from ..runtime.values import UNKNOWN, Value, is_unknown
from ..verify import validate
from .keys import ApiKey, KeyStore

# Says only what the code can back. An earlier version claimed "a named reviewer"
# approved the rules; nothing named one, and an unsubstantiated claim about who checked
# a benefit calculation is the kind a consumer-protection regulator reads literally.
NOTICE = (
    "Computed by RuleWeaver from the rules this deployment's review log records as "
    "approved; `record` identifies the exact package and review state used. It is not "
    "legal advice and not an official determination."
)

MAX_MEMBERS = 50
MAX_BODY_BYTES = 1_000_000


class EvaluateRequest(BaseModel):
    on_date: date
    household: dict[str, Any] = Field(default_factory=dict)
    members: list[dict[str, Any]] = Field(default_factory=list, max_length=MAX_MEMBERS)
    trace: bool = False


def _json(value: Value) -> Any:
    if is_unknown(value):
        return None
    if isinstance(value, Decimal):
        return format(value, "f")
    return value


def _coerce(package: RulePackage, values: dict[str, Any], where: str,
            entity: str) -> tuple[dict[str, Value], list[str]]:
    """Typed inputs, or the reasons they were refused."""
    out: dict[str, Value] = {}
    errors: list[str] = []
    for identifier, raw in values.items():
        declared = package.variable(identifier)
        if declared is None:
            errors.append(f"{where}: {identifier} is not a variable in this package")
            continue
        if not declared.input:
            errors.append(f"{where}: {identifier} is computed by the rules, not supplied")
            continue
        if (declared.entity == "household") != (entity == "household"):
            errors.append(f"{where}: {identifier} belongs to the {declared.entity}")
            continue
        if raw is None:
            continue  # Explicitly unknown is allowed; it stays unknown.
        if declared.value_type == "boolean":
            if not isinstance(raw, bool):
                errors.append(f"{where}: {identifier} must be true or false")
                continue
            out[identifier] = raw
        elif declared.value_type in ("integer", "decimal", "money"):
            try:
                if isinstance(raw, bool):
                    raise InvalidOperation
                number = Decimal(str(raw))
                if not number.is_finite():
                    raise InvalidOperation
            except InvalidOperation:
                errors.append(f"{where}: {identifier} must be a number")
                continue
            out[identifier] = number
        else:
            if not isinstance(raw, str):
                errors.append(f"{where}: {identifier} must be a string")
                continue
            out[identifier] = raw
    return out, errors


def create_api(packages: dict[str, RulePackage], engine: Engine, *,
               docs: bool = False, max_body_bytes: int = MAX_BODY_BYTES,
               requests_per_minute: int | None = 600) -> FastAPI:
    """The service over `packages`, reading approvals and keys from `engine`.

    Packages are loaded by the operator, not uploaded by customers: a rule package is the
    law as reviewed, and a caller does not get to supply its own.
    """
    store = ReviewStore(engine)
    keys = KeyStore(engine)
    package_hashes = {pid: digest(p.model_dump(mode="json"))
                      for pid, p in packages.items()}
    app = FastAPI(title="RuleWeaver", version=__version__,
                  description="Approved, source-linked rules, evaluated deterministically.",
                  docs_url="/docs" if docs else None, redoc_url=None,
                  openapi_url="/openapi.json" if docs else None)
    recent: dict[str, deque[float]] = defaultdict(deque)

    @app.middleware("http")
    async def limit_body(request: Request, call_next):
        length = request.headers.get("content-length")
        if length is not None and (not length.isdigit() or int(length) > max_body_bytes):
            return JSONResponse({"detail": f"request body over {max_body_bytes} bytes"},
                                status_code=413)
        return await call_next(request)

    @app.exception_handler(RequestValidationError)
    async def validation_without_echo(request: Request, exc: RequestValidationError):
        """FastAPI's default 422 echoes the offending input back. Here that input is a
        household's income and disability status, so only where and why are returned."""
        return JSONResponse(status_code=422, content={"detail": [
            {"loc": list(error.get("loc", ())), "msg": error.get("msg", ""),
             "type": error.get("type", "")} for error in exc.errors()]})

    def caller(request: Request) -> ApiKey:
        authorization = request.headers.get("Authorization", "")
        key = keys.resolve(authorization[7:].strip()) \
            if authorization.lower().startswith("bearer ") else None
        if key is None:
            raise HTTPException(401, "a valid API key is required",
                                headers={"WWW-Authenticate": "Bearer"})
        if requests_per_minute is not None:
            now = time.monotonic()
            window = recent[key.id]
            while window and now - window[0] > 60:
                window.popleft()
            if len(window) >= requests_per_minute:
                raise HTTPException(429, "rate limit exceeded",
                                    headers={"Retry-After": "60"})
            window.append(now)
        return key

    Caller = Annotated[ApiKey, Depends(caller)]

    def package_or_404(package_id: str) -> RulePackage:
        package = packages.get(package_id)
        if package is None:
            raise HTTPException(404, f"no package {package_id!r}")
        return package

    @app.get("/healthz", include_in_schema=False)
    @app.get("/v1/health")
    def health():
        try:
            with engine.connect() as connection:
                connection.execute(text("SELECT 1"))
        except Exception:
            return JSONResponse({"status": "unavailable"}, status_code=503)
        return {"status": "ok", "version": __version__}

    @app.get("/v1/packages")
    def list_packages(key: Caller):
        log = store.load_log()
        listing = []
        for package_id, package in sorted(packages.items()):
            _, report = approved_subset(package, log)
            listing.append({
                "id": package_id, "jurisdiction": package.jurisdiction,
                "description": package.description, "rules": len(package.rules),
                "approved": len(report.approved) - len(report.withheld),
                "complete": report.ok,
            })
        return {"packages": listing}

    @app.post("/v1/packages/{package_id}/evaluate")
    def evaluate(package_id: str, body: EvaluateRequest, key: Caller):
        package = package_or_404(package_id)
        household, errors = _coerce(package, body.household, "household", "household")
        members: list[dict[str, Value]] = []
        for i, raw in enumerate(body.members):
            member, member_errors = _coerce(package, raw, f"members[{i}]", "member")
            members.append(member)
            errors += member_errors
        if errors:
            raise HTTPException(422, {"errors": errors})

        log, head = store.snapshot()
        subset, report = approved_subset(package, log)
        ctx = Context(household=household, members=members,
                      on_date=body.on_date.isoformat())
        evaluated = Evaluator(subset, ParameterTable(subset)).run(copy.deepcopy(ctx))
        keys.record(key, "evaluate", package_id)

        computed = [v for v in package.variables if not v.input]
        outputs_household = {v.id: _json(evaluated.household.get(v.id, UNKNOWN))
                             for v in computed if v.entity == "household"}
        outputs_members = [{v.id: _json(m.get(v.id, UNKNOWN))
                            for v in computed if v.entity != "household"}
                           for m in evaluated.members]
        unknown = sorted({k for k, v in outputs_household.items() if v is None}
                         | {k for m in outputs_members for k, v in m.items() if v is None})
        response: dict[str, Any] = {
            "package_id": package_id,
            "on_date": ctx.on_date,
            "outputs": {"household": outputs_household, "members": outputs_members},
            "unknown": unknown,
            "gate": {
                "complete": report.ok,
                "approved": len(report.approved) - len(report.withheld),
                "blocked": sorted(report.blocked),
                "withheld": sorted(report.withheld),
            },
            # Enough to answer "why did you compute this?" months later: the exact
            # package, the review state it was gated by, and the rules that ran.
            "record": {
                "package_hash": package_hashes[package_id],
                "review_log_head": head,
                "rules_applied": sorted(r.id for r in subset.rules),
                "engine_version": __version__,
            },
            "notice": NOTICE,
        }
        if body.trace:
            response["trace"] = [
                {"rule": step.rule_id, "target": step.target, "scope": step.scope,
                 "via": step.via, "value": _json(step.value)}
                for step in evaluated.trace]
        return response

    @app.post("/v1/validate")
    def validate_package(document: dict[str, Any], key: Caller):
        """Check a rule package a customer is authoring. Nothing is stored or run."""
        keys.record(key, "validate")
        try:
            package = RulePackage.model_validate(document)
        except Exception as exc:
            return {"ok": False, "diagnostics": [
                {"code": "RW0000", "severity": "error", "message": line}
                for line in str(exc).splitlines() if line.strip()]}
        report = validate(package)
        return {"ok": report.ok, "diagnostics": [
            {"code": d.code, "severity": d.severity, "message": d.message,
             "rule_id": d.rule_id} for d in report.diagnostics]}

    @app.get("/v1/usage")
    def usage(key: Caller, since: date | None = None):
        start = datetime.combine(since, datetime.min.time(), UTC) if since else None
        return {"organisation": key.organisation,
                "since": since.isoformat() if since else None,
                "calls": keys.usage(key.organisation, start)}

    return app
