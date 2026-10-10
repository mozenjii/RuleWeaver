# Changelog

Notable changes to RuleWeaver. Versions follow [semantic versioning](https://semver.org);
the version lives in `src/ruleweaver/__init__.py` and a release is cut by pushing a tag
that matches it (see `.github/workflows/release.yml`).

## Unreleased

### Safety

- `--partial` no longer runs a rule whose "notwithstanding" override is unapproved. It
  used to give the SNAP baseline household a standard deduction of 180, below the 204 the
  regulation guarantees; the answer is now unknown, and the report lists the rule as
  withheld.
- The OpenFisca export no longer computes the allotment for households its income test
  excludes. Guarded rules are refused, as `disable_base_rule` already was.
- `RW8001` now says a missing fact can produce an approval as well as a denial.
- `ruleweaver review` no longer prints the database password on startup.

### OpenFisca

- The export is executed under openfisca-core 45 beside the evaluator, in CI
  (`ruleweaver.adapters.openfisca.equivalence`). Every exported variable agrees across
  eight SNAP households.
- Fixed: the package could not be loaded, declared no inputs, selected exceptions in the
  wrong priority order, emitted an overridden rule beside its override, applied rules
  before their effective date, and could not read dimensioned tables.
- New diagnostics: `RW8006` (two ids become one OpenFisca name) and `RW8007` (a
  dimensioned table that is not a complete grid).

### Deployment

- A Docker image for the reviewer application: non-root, audit log on a `/data` volume,
  health check, and PostgreSQL support through the new `postgres` extra.
- `GET /healthz` — 200 when the audit log is reachable, 503 when it is not.
- `ruleweaver --version`.
- A readable one-line error when the audit log cannot be opened.
- Tag-driven releases: a GitHub Release with the wheel and sdist, and the image on GHCR.

### Packaging and CI

- The core no longer needs the `review` extra: the execution gate, the export and
  `ruleweaver token` work on the base install. A base-install CI job keeps it that way.
- CI was red on every push from 2026-08-16; it is green, and runs ruff, mypy, every
  extra, the base install, the built wheel and the Docker image.
- The published JSON Schema no longer drifts with the installed Pydantic version.
- New `openfisca` and `postgres` extras.

## 0.1.0

The deterministic core: typed rule IR, four-state evaluator with traces, 41 validators,
boundary and date generators, mutation harness, semantic diff and amendment impact, eCFR
ingestion, LLM-assisted extraction behind six checks, the review gate and application, and
the OpenFisca code generator. Golden corpus: 15 SNAP rules from 7 CFR 271.2, 273.9 and
273.10.
