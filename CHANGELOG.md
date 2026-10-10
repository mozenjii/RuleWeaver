# Changelog

Notable changes to RuleWeaver. Versions follow [semantic versioning](https://semver.org);
the version lives in `src/ruleweaver/__init__.py` and a release is cut by pushing a tag
that matches it (see `.github/workflows/release.yml`).

## Unreleased

### Product plan and documentation

- Define the self-hosted compiler and verifier scope in ADR-032, with separately
  versioned content packs, change-impact reports and independent known-answer parity.
- Revise ADR-021/022 and the intended-purpose statement (R-25); record commercial
  legal review as pending rather than treating the proposed posture as a conclusion.
- Align specifications, architecture, roadmap, backlog and repository layout with
  Built / Partial / Planned evidence. Record expired FY2026 coverage, larger-household
  gaps and missing source-version binding instead of claiming current policy readiness.
- Reconcile local project memory with the current implementation and verification.


### Content

- The SNAP example computes. It carries the official FY2026 tables for the 48 states and
  DC — poverty guidelines, maximum allotments, standard deductions, the shelter cap and
  the minimum benefit — each value citing the row of the FNS memo or HHS notice it came
  from. Both documents are stored with their checksums. The income limits the rules
  compute equal the limits FNS published for household sizes one to eight.
- The source corpus reads memos and notices (plain text, HTML, or a PDF through a pinned
  text rendering) as well as eCFR XML, and `validate --sources` now checks the citation
  on every parameter value, not only on the parameter.
- The baseline scenario no longer supplies its own tables, and the amendment example is
  regenerated from the current package: raising the earned income deduction to 25% moves
  the baseline household's net income from 586.50 to 474.00 and its allotment from 609
  to 642.

### Safety

- Parameter tables pass the approval gate like rules. An unapproved table supplies no
  values, so anything reading it is unknown; changing a number or its source makes the
  approval stale, so an annual uprating is reviewed. Each value can cite where it was
  published. New diagnostics: `RW3011` (a table with no values) and `RW7004` (a value with
  no source).
- An edit approves only the corrected rule; it used to approve the rule it corrected.
- The review app plants faults at a disclosed rate and measures the catch rate, which no
  longer counts unreviewed faults as misses.
- Every page of the review app needs an identity, and cross-site decisions are refused.
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
- A parameter value's end date is exported as `value: null`; the last figure used to
  apply for ever. Text in parameter files is quoted, and each table cites its own
  publication.

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
