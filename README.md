# RuleWeaver

A self-hosted compiler and verifier for computable benefit and tax rules. It links
structured interpretations and published figures to their sources, supports human
review, and runs supported rules deterministically without a model dependency.

The intended deliverable is **change impact plus independent verification**: what a
legislative change or annual uprating moves, linked to its source, with parity against
the operator's own known-answer cases. That full deliverable is **Partial**: native
package comparison exists (R-16); independent parity (R-17) and a versioned hashed content
pack (R-38) are **Planned**. Simulated reviews are hypotheses, not customer evidence.

## Evidence snapshot — 2026-10-10

| Capability | State and proof |
|---|---|
| Typed IR, Decimal evaluator, unknown propagation and traces | **Built** supported subset: `src/ruleweaver/ir/`, `runtime/`, `tests/test_snap_evaluation.py` |
| Deterministic structural/type/reference/date/provenance checks | **Built** subset: `src/ruleweaver/verify/`, `tests/test_validators.py`, `tests/test_types.py`; additional checks/spec mismatches **Planned**, R-44 |
| eCFR XML, memos/notices and sourced figures | **Built** corpus transport: `src/ruleweaver/ingest/`, `tests/test_ingest.py`, `tests/test_snap_tables.py`; structured HTML/PDF **Partial**, R-18 |
| Rule and parameter-table approval | **Built** gate: `src/ruleweaver/approval.py`, `tests/test_parameter_gate.py`; universal deployed enforcement **Partial**, R-39 |
| Source/item review, edits and planted review faults | **Built** subset: `src/ruleweaver/review/`, `tests/test_review_app.py`, `tests/test_seeding.py`; identity/audit/qualification/privacy/accessibility hardening remains R-05/R-06/R-07/R-11/R-29/R-45 |
| Boundary/date candidates and mutation harness | **Built** subset: `src/ruleweaver/testgen/`, `tests/test_mutation.py`; additional test tooling **Partial**, R-41 |
| Package change/dependency/scenario analysis | **Partial** report product: `src/ruleweaver/diff/`, `tests/test_amendment_impact.py`; full source/test/report chain R-16 |
| Calculation service | **Built**, frozen: `src/ruleweaver/service/`, `tests/test_service.py`; self-hosted or synthetic use |
| OpenFisca export/differential execution | **Built** subset, frozen: `src/ruleweaver/adapters/openfisca/`, `tests/test_openfisca_equivalence.py`; consistency evidence, not independent policy truth |
| Optional model authoring | **Built** segmentation/proposals, frozen: `src/ruleweaver/compile/`, `tests/test_compile.py`; packaging/metadata **Partial**, R-26; additional extraction/linking R-40 |

Requirement status lives in [project backlog](docs/10_BACKLOG.md).
The architecture maps evidence and gaps in [docs/03_ARCHITECTURE.md](docs/03_ARCHITECTURE.md).

## Reference content and limits

The reference demo is 15 SNAP rules with official FY2026 figures for the 48 states/DC,
checked against stored snapshots in `examples/snap/sources/`. It is not complete current
SNAP policy. The table period ended on **30 September 2026**; table-dependent answers
from 1 October 2026 are unknown until FY2027 content is built (R-37). Correct income-limit
increments for households of nine or more are not built (R-36). The effect of 2025 legal
changes has not been audited (R-22). The FNS memo came from the Alaska redistribution;
the manifest records that comparison against FNS's copy is still needed before reliance.

England Universal Credit plus the April uprating is the leading next-content candidate,
not started work (R-46). The owner decides whether to start it; UK point-in-time ingestion
(R-19), explicit currency/jurisdiction support (R-21) and qualified review remain needed.

## Install and verify

```bash
python -m venv .venv
.venv/bin/python -m pip install -e ".[dev,review,openfisca]"
.venv/bin/python -m ruff check src tests
.venv/bin/python -m mypy src
.venv/bin/python -m pytest -o addopts='' -q
```

The reconciled suite passes **558 tests** with **92.14% coverage**; CI enforces 80%.

Windows uses `.venv/Scripts/python.exe`. The pulled baseline passed **554 tests** with
these extras; mypy checked 55 source files and ruff passed. Use a fresh repository-local
temporary directory on Windows: OpenFisca's nested runner otherwise collects across
`D:`/`C:` drives and can reach protected junctions.

```powershell
$taskTemp = Join-Path (Get-Location) ('.pytest_cache/run-' + [guid]::NewGuid().ToString('N'))
.venv/Scripts/python.exe -m pytest --basetemp $taskTemp -o addopts='' -q
```

The base deployment installs no review/model SDKs. `tests/test_optional_extras.py` protects
that boundary; optional-feature tests skip when their extras are absent. No live model
accuracy or independent policy assurance follows from this suite.

## Inspect the dated demo

These commands operate on a **draft reference fixture**, not an approved deployed pack.
The scenario explicitly uses a date inside the FY2026 period.

```bash
ruleweaver ingest examples/snap/sources/manifest.json
ruleweaver validate examples/snap/rules.json --sources examples/snap/sources/manifest.json
ruleweaver evaluate examples/snap/rules.json examples/snap/scenarios/baseline.json --trace
ruleweaver diff examples/snap/rules.json examples/snap/amendments/earned-deduction-25pct.json \
  --scenario examples/snap/scenarios/baseline.json \
  --observe var.household.net_monthly_income --observe var.household.allotment
```

`tests/test_snap_tables.py` checks the dated baseline: net monthly income 586.50 and
allotment 609. The hypothetical 25% earned-income deduction amendment moves them to
474.00 and 642 (`tests/test_amendment_impact.py`). These are fixture results, not official
determinations. Boundary candidates record package behavior; they are not independent
policy-intent tests.

## Review and deployed execution

Configure signed-session identity or a trusted authenticating proxy before starting the
review app. Without either, it fails closed. Then:

```bash
ruleweaver review examples/snap/rules.json
ruleweaver approvals examples/snap/rules.json
ruleweaver evaluate examples/snap/rules.json examples/snap/scenarios/baseline.json --require-approval
```

Use the same review database for review and evaluation. The last command refuses without
matching approvals for rules and parameter tables. `--partial` withholds unapproved
items; dependent outputs remain unknown. The service always applies the gate; CLI
approval is optional and direct evaluator calls are ungated, so universal deployed-path
enforcement is not built (R-39).

Approvals bind structured objects and embedded source spans. Updated spans or table values
make approval stale. Changing a snapshot alone is not automatically detected by that gate;
complete source-version binding is not built (R-43).

The review app plants disclosed faults and reports aggregate catch rates. This is not
proof of qualified reviewers. The log is an unkeyed hash chain; administrators can rewrite
and recompute it (R-05). Shared-secret tokens can mint arbitrary names; individually bound
identity and author/approver separation are not built (R-06).

## Maintained interfaces

The calculation service is retained for self-hosted/synthetic use, with API keys, replay
records and request/rate bounds (`tests/test_service.py`). It is frozen for new investment.

```bash
ruleweaver serve examples/snap/rules.json
```

Operators configure the database, approvals and API keys before use. Interactive API docs
are off by default. Unknown reason codes and per-variable handling policy are not built
(R-10). Intended zero-access support is an operational goal, not an automatic self-hosting
guarantee (R-31).

Default OpenFisca export requires approvals; unsupported semantics are refused or reported.
`--no-approval` is a draft-only export surface. The guarded allotment is not exported;
unknown/default-state and binary-float differences are explicit (ADR-031).

```bash
ruleweaver export examples/snap/rules.json build/openfisca
```

RuleWeaver code is Apache-2.0. The exported package imports OpenFisca-Core, whose licence
is AGPL-3.0-or-later. Review applicable dependency obligations for an actual deployment;
this is not legal advice. The native runtime does not require OpenFisca.

## Documentation

- Product: [brief](docs/00_PROJECT_BRIEF.md), [spec](docs/02_PRODUCT_SPEC.md), [architecture](docs/03_ARCHITECTURE.md)
- Contract: [IR](docs/04_RULE_IR_SPEC.md), [pipeline](docs/05_COMPILER_PIPELINE.md), [safety](docs/06_VERIFICATION_SAFETY.md)
- Evidence: [status](docs/01_PROJECT_STATUS.md), [benchmark plan](docs/07_DATA_BENCHMARK_EVAL.md), [adapters](docs/08_ADAPTERS_INTEROP.md)
- Work: [roadmap](docs/09_IMPLEMENTATION_ROADMAP.md), [backlog and requirements](docs/10_BACKLOG.md), [decisions](docs/11_DECISIONS.md)
- Reference: [research map](docs/12_RESEARCH_REFERENCES.md), [actual tree](docs/13_REPO_STRUCTURE.md), [glossary](docs/14_GLOSSARY.md), [SNAP vocabulary](docs/15_VOCABULARY.md)
- Project records: [backlog](docs/10_BACKLOG.md), [changelog](CHANGELOG.md), [security policy](SECURITY.md)

The active roadmap excludes Catala/LegalRuleML/PROV export, Akoma Ntoso, OCR, plugin SDK,
pre-user hosted multi-tenant SaaS and pre-hosted certifications. Historical references do
not restore those commitments.

Outputs are technical interpretations for review, not legal advice or official decisions.
Intended-purpose and non-reliance positions require counsel review before commercial use
(ADR-021/022, R-25). Human approval and deterministic checks cannot establish legal authority.
