# 03 — Architecture

RuleWeaver is a self-hosted compiler and verifier for computable benefit and tax
rules. The intended deliverable is change impact plus independent verification,
not a hosted calculation business. ADR-032 records the owner's revised plan.
`docs/10_BACKLOG.md` owns requirement status; labels here describe the bounded
implementation on 2026-10-10. Built does not mean independently correct policy.

## Component map

```text
Operator environment (self-hosted)
  Verified snapshots [Built: eCFR XML, memos/notices]
       |                    [Partial: structured HTML/PDF R-18]
       |                    [Planned: UK point-in-time R-19]
       v
  Source documents and evidence [Built]
       |                 |
  Human authoring    Optional proposal passes [Built subset; FREEZE]
       +-----------------+
               v
  Typed IR + dated/sourced parameters [Built subset]
               |
  Deterministic verification and test tooling [Built subset]
               |
  Review app + fault seeding [Built subset]
               |
  Rule AND parameter approval gate [Built]
       |       [Partial: all deployed paths R-39]
       v
  Native deterministic evaluator [Built]
       |                    |
  Change analysis       Known-answer parity [Planned R-17]
  [Partial R-16]             |
       +--------------------+
               v
  Versioned hashed content pack [Planned R-38]

Maintained, frozen surfaces: self-hosted/synthetic calculation service;
OpenFisca supported-subset export; optional model authoring.
```

The diagram is an intended flow, not proof of an implemented content-pack command.
Current source manifests, review database, candidate packages and test artifacts are
separate. The content-pack boundary has not been built.

## Components, evidence and gaps

| Component | State | Proof and boundary |
|---|---|---|
| Source snapshots and digest checks | **Built** | `src/ruleweaver/ingest/corpus.py`, `tests/test_ingest.py`: checks stored bytes before parsing; a deliberate unverified load is not release evidence |
| eCFR structure | **Built** | `src/ruleweaver/ingest/ecfr.py`, `markers.py`, `tests/test_markers.py`: addressable clauses and repeated marker levels |
| Memos, notices and published figures | **Built** text transport; **Partial** structured ingestion | `src/ruleweaver/ingest/plain.py`, `tests/test_ingest.py`: plain/HTML canonical text, PDF through a separately hashed text rendering; clause-aware HTML/PDF remains R-18 |
| UK point-in-time source layer | **Planned** | R-19; no legislation.gov.uk importer exists |
| Rule IR and effective values | **Built** subset | `src/ruleweaver/ir/rules.py`, `expressions.py`, `tests/test_schema_artifact.py`: closed AST, entities, rules, parameters, source spans and ambiguity; currency/multiple jurisdictions R-21, multi-axis time R-44 remain |
| Native evaluator and traces | **Built** | `src/ruleweaver/runtime/evaluator.py`, `values.py`, `tests/test_snap_evaluation.py`: Decimal arithmetic, unknown propagation and fixed-point rule execution; richer unknown reasons/disposition R-10 remain |
| Verification | **Built** implemented passes; **Partial** full specification | `src/ruleweaver/verify/validators.py`, `types.py`, `tests/test_validators.py`, `tests/test_types.py`, `tests/test_provenance_validation.py`; contradiction/completeness and documented spec mismatches R-44 |
| Boundary/date/mutation tooling | **Built** subset | `src/ruleweaver/testgen/`, `tests/test_date_generation.py`, `tests/test_mutation.py`; exception/combinatorial/property additions R-41 |
| Rules and parameter approval | **Built** gate; **Partial** deployment enforcement | `src/ruleweaver/approval.py`, `tests/test_approval.py`, `tests/test_parameter_gate.py`: hashes bind decisions to rules, tables and cited evidence; all deployed paths R-39 |
| Review app and fault seeding | **Built** subset; **Partial** complete workflow | `src/ruleweaver/review/app.py`, `seeding.py`, `tests/test_review_app.py`, `tests/test_seeding.py`: source/item display, edits, decisions, planted faults and aggregate metrics; ambiguity/test/dependency/history surface R-45, accessibility R-29 |
| Review persistence and identity | **Partial** | `src/ruleweaver/review/store.py`, `identity.py`, `tests/test_review_store.py`, `tests/test_identity.py`: SQLite/PostgreSQL plumbing, unkeyed chain, signed sessions/trusted proxy; keyed chain R-05, per-person identity/separation R-06, qualification R-07, pseudonyms R-11 |
| Change impact | **Partial** | `src/ruleweaver/diff/semantic.py`, `impact.py`, `tests/test_amendment_impact.py`: package changes, dependencies and scenario results; structural source diff, affected tests, dated durable deliverable R-16 |
| Independent parity | **Planned** | R-17: operator-owned known-answer cases, pinned version/date and reproducible result; adapter consistency is not this capability |
| Content-pack release | **Planned** | R-38: immutable version/hash binding sources, rules, dated tables, review-log export/head, tests and verification evidence; software-release workflow is not a content pack |
| End-to-end provenance | **Partial** | source spans in `ir/rules.py`, run records in `compile/pipeline.py`, decisions in `review/decisions.py`; unified relation/lineage contract R-43 |
| Calculation service | **Built**, FREEZE | `src/ruleweaver/service/api.py`, `keys.py`, `tests/test_service.py`: gated requests, API keys, replay record, request/rate bounds and redacted errors; retain self-hosted/synthetic use |
| OpenFisca export | **Built** subset, FREEZE | `src/ruleweaver/adapters/openfisca/`, `tests/test_openfisca_equivalence.py`: differential execution and stated gaps/refusals; maintain only, AGPL dependency note R-28 |
| Optional proposal layer | **Built** two passes, **Partial** authoring product, FREEZE | `src/ruleweaver/compile/`, `models/`, `tests/test_compile.py`, `tests/test_models.py`: segmentation/proposals, prompt hashes and run records; complete separation/metadata R-26; additional extraction/linking R-40 |
| Software packaging | **Built** configuration | `pyproject.toml`, `Dockerfile`, `.github/workflows/tests.yml`, `.github/workflows/release.yml`: wheel/image checks and tag-triggered release workflow; SBOM/signing/pinning R-13 not built |

Short filenames in this table are relative to the fully qualified directory in the same
cell. The tree and source files are mapped in `docs/13_REPO_STRUCTURE.md`.

## Approval and security boundary

The intended production contract is approval of both rules and parameter tables before
execution. Today the service always gates and export gates by default. CLI evaluation
requires `--require-approval`; `--partial` withholds unapproved dependencies. Low-level
`Evaluator` calls are ungated, and draft export has `--no-approval`. These are testing
surfaces, not a universal enforced production boundary (R-39).

A source hash proves byte identity, not authority, completeness or current law. A quote
check proves a contiguous quote exists, not that its interpretation is right. A signed
session proves possession of a deployment credential, not qualification or separation
of duties. The unkeyed log detects inconsistent edits, not an administrator who rewrites
and rehashes it. R-05/R-06/R-07 preserve those stronger intended guarantees.

Self-hosting keeps operator data in the operator's chosen environment. Zero-access
support is the intended practice, not an automatic software guarantee (R-31). Optional
remote authoring has its own data boundary and must be explicitly selected.

## Content-pack boundary — Planned (R-38)

The pack must pin source/version/retrieval and validity context, source checksums, IR and
schema version, sourced parameter values, approvals and review-log head/export, independent
test vectors, diagnostics and verification results. R-13 adds signing and supply-chain
artifacts; R-43 binds relationships across these records. Load-time verification must reject
inconsistent evidence. Current runtime records and source manifests are useful inputs,
not the completed pack contract.

SNAP is a reference fixture with FY2026 figures for the 48 states/DC, not complete current
policy. FY2027 tables R-37, nine-plus increments R-36 and current-law reconciliation R-22
are open. England Universal Credit/April uprating R-46 is an owner-controlled candidate.

## Layer rules and excluded expansion

Keep source facts separate from interpretation. Pure deterministic passes own schema,
types, references, dates, graphs, evaluation and artifact hashes. Optional models propose;
humans approve. No UI, adapter or provider may redefine canonical semantics. Diagnostics
have stable codes, severity, object identifiers and machine-readable details
(`src/ruleweaver/verify/diagnostics.py`); a unified diagnostic source-location model is
not yet provided by that dataclass (R-43).

Catala, LegalRuleML, PROV export, Akoma Ntoso, OCR, plugin SDK and pre-user hosted
multi-tenant SaaS are cut from the active roadmap. Pre-hosted SOC 2, ISO 27001 and FedRAMP
work is deferred. Historical design references do not create implementation commitments.
