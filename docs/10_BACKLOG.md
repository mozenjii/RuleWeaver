# 10 — Backlog and Requirements

This is the single source of truth for project requirement status and priority.
Requirements preserve the revised scope in ADR-032 and verified implementation gaps.
Simulated review exercises informed hypotheses, not customer demand or legal conclusions;
the raw working material is private and is not part of the published repository.
See `09_IMPLEMENTATION_ROADMAP.md` for dependencies and acceptance evidence and
`01_PROJECT_STATUS.md` for the current implementation snapshot.

**Priorities.** P0: a claim the project makes that the code does not yet back — fix the
code. P1: needed for a first version people can actually use. P2: after the first real
user. **Status:** ✅ done · 🟡 partial · ⬜ not started.

The rule from here on: the project claims only what the code does, and the code is built
up to what the project should be able to claim. Missing capabilities remain explicit
requirements; they are not deleted to make the current implementation look complete.

**Owner's revised plan (ADR-032, 2026-10-10):** build a good self-hosted compiler and
verifier first. The deliverable is change impact plus independent known-answer parity.
SNAP is the reference demo; England Universal Credit is a candidate, not started content.
This file is the single source of truth for requirement status. Documentation labels
are evidence snapshots, not separate completion trackers.

**Execution order:** remaining P0 work is R-37 → R-05 → R-06 → R-36 → R-39.
R-25 is the completed documentation prerequisite. R-36 and R-37 are promoted from P1
because the current example cannot support those claimed date/household ranges.
Then P1: R-16, R-17, R-38; R-07, R-10, R-11, R-13, R-29; R-18, R-19,
R-21, R-22, R-23, R-26, R-43, R-45. See the roadmap for dependencies and exit evidence.

## A. Make the claims true

| ID | Requirement | Pri | Status |
| --- | --- | --- | --- |
| R-01 | Seeded faults are actually planted in the review queue, reviewers are told such tests exist, and catch-rate metrics are aggregate and pseudonymised by default | P0 | 🟡 |
| R-02 | "Edit" works from the form and approves only the corrected rule | P0 | ✅ |
| R-03 | Parameters are sourced, dated objects inside the approval gate, with a diagnostic for missing values | P0 | ✅ |
| R-04 | The shipped example package computes: complete tables, each value sourced | P0 | ✅ |
| R-05 | The audit chain resists an administrator: keyed chain with a key held outside the database, plus checkpoint export and verify | P0 | ⬜ |
| R-06 | One identity per reviewer (OIDC/SSO or per-user keys), not one shared secret that can mint any name; author and approver kept separate | P0 | ⬜ |
| R-07 | A reviewer's qualification is recorded with each sign-off, and the signer role is assignable to the buyer's own staff | P1 | ⬜ |
| R-08 | Every API answer carries a replayable record (package hash, review-log head, rules applied) | P0 | ✅ |
| R-09 | The API notice states only what the code backs | P0 | ✅ |
| R-10 | "Unknown" comes with the missing facts and a reason code; the integrator sets a per-variable policy (block, route to a person, hold) | P1 | ⬜ |
| R-11 | Reviewer identities are pseudonymous in the chain, with a separate deletable identity map | P1 | ⬜ |

## B. Security and supply chain

| ID | Requirement | Pri | Status |
| --- | --- | --- | --- |
| R-12 | SECURITY.md, a disclosure policy and a security contact | P0 | ✅ |
| R-13 | SBOM, signed release artefacts, pinned actions and base image, least-privilege release job, dependency scanning | P1 | ⬜ |
| R-14 | Review app: CSRF/Origin check, identity on read pages. API: request size and rate limits, `/docs` switchable, validation errors that do not echo household data | P0 | ✅ |
| R-15 | Container health check works for both applications | P0 | ✅ |

## C. Content, ingestion and the core product

| ID | Requirement | Pri | Status |
| --- | --- | --- | --- |
| R-16 | Change-impact report as a deliverable: what changed in the source, which rules, tests and results it moves, dated and readable | P1 | 🟡 |
| R-17 | Parity command against a user's own known-answer cases, with a publishable result | P1 | ⬜ |
| R-18 | HTML and PDF ingestion (state manuals, guidance, bulletins) — memos and notices load as one checked text today; clause structure still missing | P1 | 🟡 |
| R-19 | legislation.gov.uk point-in-time ingestion | P1 | ⬜ |
| R-20 | EU sources (national XML, EUR-Lex) for the first EU domain | P2 | ⬜ |
| R-21 | Currency on money values; more than one jurisdiction in a package | P1 | ⬜ |
| R-22 | Check the SNAP fixture against current law (2025 legislation may have changed it) | P1 | ⬜ |
| R-23 | Language-neutral export: JSON rules plus test vectors | P1 | ⬜ |
| R-24 | Obligation-register mode for clauses that are duties, not calculations | P2 | ⬜ |
| R-36 | Households of nine or more. The pinned FY2026 memo gives rounded per-member increments ($459 net, $596 gross); implement the source-specific rule instead of extrapolating table rows | P0 | ⬜ |
| R-37 | Retrieve and verify the official FY2027 tables for the period starting 1 October 2026; the current package answers unknown after 30 September 2026 | P0 | ⬜ |

## D. Compliance posture

| ID | Requirement | Pri | Status |
| --- | --- | --- | --- |
| R-25 | Intended-purpose and non-reliance statement; ADR-021/022 rewritten so they state positions, not conclusions | P0 | ✅ |
| R-26 | LLM authoring optional and packaged separately; the runtime ships with no model dependency; every proposal stamped with model, version and prompt hash | P1 | 🟡 |
| R-27 | Option to use a local or EU-hosted model for authoring | P2 | ⬜ |
| R-28 | AGPL note on the OpenFisca export | P0 | ✅ |
| R-29 | Reviewer app meets WCAG 2.1 AA, with a conformance statement | P1 | ⬜ |
| R-30 | EU Cyber Resilience Act readiness before any paid EU distribution | P2 | ⬜ |
| R-31 | Zero-access support protocol; DPA/SCC templates kept for any deployment that touches personal data | P2 | ⬜ |

## E. Not code — for the founder

| ID | Requirement |
| --- | --- |
| R-32 | Written release from the employer covering moonlighting and IP |
| R-33 | Entity, liability cap, insurance — at the first signed letter of intent |
| R-34 | A qualified reviewer, through a partner, for each jurisdiction |
| R-35 | A second maintainer, or escrow |

## Explicitly not needed now

Hosted multi-tenant SaaS, per-call billing, SOC 2 / ISO 27001 before a hosted offering,
FedRAMP, Catala / LegalRuleML / PROV exports, OCR, a plugin SDK. These are outside the active scope under ADR-032.

## F. Gaps exposed by the revised documentation audit

These preserve unimplemented claims rather than calling a design or software-release
workflow a built feature. No implementation is added by this documentation pass.

| ID | Requirement | Pri | Status |
| --- | --- | --- | --- |
| R-38 | Immutable content-pack artifact: version and hash covering source manifest/snapshots, rules, dated tables, approval-log export/head, test vectors, verification results and valid-as-of context; verify before use | P1 | ⬜ |
| R-39 | Enforce approval and deterministic validation on every deployed execution path for rules and parameters; keep draft CLI/library execution explicitly separated and labelled | P0 | 🟡 |
| R-40 | Automated concept/definition/parameter extraction and source cross-reference linking as optional proposal passes, with diagnostics and source evidence | P2 | ⬜ |
| R-41 | Exception and dependency/combinatorial test generation plus a property-based suite; preserve human policy-intent tests separately | P2 | 🟡 |
| R-42 | Public independently annotated benchmark: gold source links, rules, tests, ambiguity labels, metrics and reproducible runner | P2 | ⬜ |
| R-43 | Typed provenance relations, binding approvals to verified source versions, and durable end-to-end source/run/review/test lineage inside the content pack, without a standards-export dependency | P1 | 🟡 |
| R-44 | Mechanically scoped contradiction/completeness checks and multi-axis time; close documented period compatibility/prorating, clamp-bound, exception-tie and override-severity gaps without silently weakening the spec | P2 | ⬜ |
| R-45 | Review surface for ambiguity resolution, policy-intent/test approval and dependency/change history; blind dual-encoding workflow if required by the content owner | P1 | 🟡 |
| R-46 | England Universal Credit core plus April-uprating reference content, including source/reuse verification and independent known-answer cases; start only after the owner's decision | P2 | ⬜ |

## Proof required for closure

- Supported scope, dates, jurisdiction and source evidence are explicit.
- A requirement closes on implementation plus meaningful tests, not a skeleton or doc.
- A semantic bug gets a regression case; human-approved intent tests are preserved.
- Approval applies to rules and table values; missing/unknown does not become false.
- Independent known-answer cases remain independent of the evaluated implementation.
- New gaps get an ID in the requirement tracker instead of disappearing from claims.

## Evidence for completed and partial claims

Paths below are repository-relative. Passing tests show the checked scope, not legal
correctness, current-law coverage, reviewer qualification or market demand.

| Requirement | Evidence and boundary |
|---|---|
| R-01 | `src/ruleweaver/review/seeding.py`, `tests/test_seeding.py`: queue faults and aggregate metrics; stored reviewer pseudonymisation remains R-11, and no qualified-human detection claim is established |
| R-02 | `src/ruleweaver/review/app.py`, `tests/test_review_app.py`: edited rule submitted and original remains unapproved |
| R-03 | `src/ruleweaver/approval.py`, `tests/test_parameter_gate.py`: rule and table hashes, embedded-span changes stale approvals, unsourced/empty value diagnostics |
| R-04 | `examples/snap/rules.json`, `tests/test_snap_tables.py`: pinned FY2026 figures for the 48 states/DC and tested sizes 1–8; R-22/R-36/R-37 remain open |
| R-08/R-09/R-14/R-15 | `src/ruleweaver/service/api.py`, `src/ruleweaver/review/app.py`, `tests/test_service.py`, `tests/test_review_app.py`, `Dockerfile`: replay records, bounded inputs, authenticated pages, health checks; not a hosted service or certified deployment |
| R-12 | `SECURITY.md`: disclosure policy and contact; not a security certification |
| R-16 | `src/ruleweaver/diff/semantic.py`, `src/ruleweaver/diff/impact.py`, `tests/test_amendment_impact.py`: package changes/dependency closure/scenario comparison; structural source diff, affected-test list and durable dated report remain missing |
| R-18 | `src/ruleweaver/ingest/plain.py`, `src/ruleweaver/ingest/corpus.py`, `tests/test_ingest.py`: canonical memo/notice text, HTML stripping, PDF with separately hashed text rendering; no clause-aware HTML/PDF parser |
| R-25 | `docs/11_DECISIONS.md` ADR-021/022: revised intended purpose and non-reliance; counsel review remains required before commercial use |
| R-26 | `pyproject.toml`, `tests/test_optional_extras.py`, `src/ruleweaver/compile/pipeline.py`: optional SDKs and hashed prompts/run records; stable model-version attestation and provider completeness not established |
| R-28 | `src/ruleweaver/adapters/openfisca/codegen.py`, `docs/08_ADAPTERS_INTEROP.md`: dependency licence note; not legal advice on a particular deployment |
