"""API keys and usage metering for the calculation service.

A key is shown once, when it is created, and only its SHA-256 digest is stored. A
database dump therefore yields no usable credential. Keys are high-entropy random tokens,
not passwords, so a fast digest is the right tool; a slow password hash would add latency
to every request and no security.

Usage is recorded per organisation and endpoint — enough to bill on, and nothing about
the household that was evaluated. The service is a calculator, and keeping claimants'
facts out of its logs is the cheapest privacy control there is.
"""

from __future__ import annotations

import hashlib
import secrets
import uuid
from dataclasses import dataclass
from datetime import UTC, datetime

from sqlalchemy import Column, DateTime, Integer, MetaData, String, Table, func, select
from sqlalchemy.engine import Engine

PREFIX = "rw_"

metadata = MetaData()

api_keys = Table(
    "api_keys", metadata,
    Column("id", String(32), primary_key=True),
    Column("organisation", String(256), nullable=False, index=True),
    Column("key_hash", String(64), nullable=False, unique=True),
    # The first characters of the key, so an operator can tell keys apart in a listing
    # without the listing being able to authenticate anything.
    Column("hint", String(16), nullable=False),
    Column("created_at", DateTime(timezone=True), nullable=False),
    Column("revoked_at", DateTime(timezone=True), nullable=True),
)

usage_events = Table(
    "usage_events", metadata,
    Column("seq", Integer, primary_key=True, autoincrement=True),
    Column("organisation", String(256), nullable=False, index=True),
    Column("key_id", String(32), nullable=False),
    Column("endpoint", String(64), nullable=False),
    Column("package_id", String(256), nullable=True),
    Column("at", DateTime(timezone=True), nullable=False, index=True),
)


def _digest(key: str) -> str:
    return hashlib.sha256(key.encode()).hexdigest()


@dataclass(frozen=True)
class ApiKey:
    id: str
    organisation: str
    hint: str
    created_at: datetime
    revoked_at: datetime | None


class KeyStore:
    def __init__(self, engine: Engine) -> None:
        self.engine = engine
        metadata.create_all(engine)

    def create(self, organisation: str) -> tuple[ApiKey, str]:
        """Issue a key. The plaintext is returned once and never stored."""
        if not organisation.strip():
            raise ValueError("an API key must belong to an organisation")
        plaintext = PREFIX + secrets.token_urlsafe(32)
        record = ApiKey(id=uuid.uuid4().hex, organisation=organisation,
                        hint=plaintext[:10], created_at=datetime.now(UTC), revoked_at=None)
        with self.engine.begin() as connection:
            connection.execute(api_keys.insert().values(
                id=record.id, organisation=organisation, key_hash=_digest(plaintext),
                hint=record.hint, created_at=record.created_at))
        return record, plaintext

    def resolve(self, plaintext: str) -> ApiKey | None:
        """The live key a request presented, or None."""
        if not plaintext.startswith(PREFIX):
            return None
        with self.engine.connect() as connection:
            row = connection.execute(
                select(api_keys).where(api_keys.c.key_hash == _digest(plaintext))).first()
        if row is None or row.revoked_at is not None:
            return None
        return ApiKey(row.id, row.organisation, row.hint, row.created_at, row.revoked_at)

    def revoke(self, key_id: str) -> bool:
        with self.engine.begin() as connection:
            result = connection.execute(
                api_keys.update()
                .where(api_keys.c.id == key_id, api_keys.c.revoked_at.is_(None))
                .values(revoked_at=datetime.now(UTC)))
        return result.rowcount == 1

    def list(self) -> list[ApiKey]:
        with self.engine.connect() as connection:
            rows = connection.execute(select(api_keys).order_by(api_keys.c.created_at))
            return [ApiKey(r.id, r.organisation, r.hint, r.created_at, r.revoked_at)
                    for r in rows]

    def record(self, key: ApiKey, endpoint: str, package_id: str | None = None) -> None:
        with self.engine.begin() as connection:
            connection.execute(usage_events.insert().values(
                organisation=key.organisation, key_id=key.id, endpoint=endpoint,
                package_id=package_id, at=datetime.now(UTC)))

    def usage(self, organisation: str, since: datetime | None = None) -> dict[str, int]:
        """Calls per endpoint for one organisation."""
        query = (select(usage_events.c.endpoint, func.count())
                 .where(usage_events.c.organisation == organisation)
                 .group_by(usage_events.c.endpoint))
        if since is not None:
            query = query.where(usage_events.c.at >= since)
        with self.engine.connect() as connection:
            return {row[0]: row[1] for row in connection.execute(query)}
