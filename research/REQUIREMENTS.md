# Requirements from the simulated reviews

Derived from `simulated-reviews/` (2026-10-10). Numbers in brackets are the round-1
participants who demanded the item independently, e.g. [#16, #20]. The reviews are simulated,
so a requirement here is a hypothesis about what users need, not proof.

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

| ID | Requirement | Pri | Status | Source |
|---|---|---|---|---|
| R-01 | Seeded faults are actually planted in the review queue, reviewers are told such tests exist, and catch-rate metrics are aggregate and pseudonymised by default | P0 | ✅ | #01 #07 #11 #12 #14 #20; monitoring limits #08 #13 |
| R-02 | "Edit" works from the form and approves only the corrected rule | P0 | ✅ | verified fact 2 |
| R-03 | Parameters are sourced, dated objects inside the approval gate, with a diagnostic for missing values | P0 | ✅ | #01 #03 #09 #20 |
| R-04 | The shipped example package computes: complete tables, each value sourced | P0 | ✅ | verified fact 3 |
| R-05 | The audit chain resists an administrator: keyed chain with a key held outside the database, plus checkpoint export and verify | P0 | ⬜ | #14 #16 #20 |
| R-06 | One identity per reviewer (OIDC/SSO or per-user keys), not one shared secret that can mint any name; author and approver kept separate | P0 | ⬜ | #04 #07 #16 #20 |
| R-07 | A reviewer's qualification is recorded with each sign-off, and the signer role is assignable to the buyer's own staff | P1 | ⬜ | #12 #04 #10 #11 (tribunal ruling 4) |
| R-08 | Every API answer carries a replayable record (package hash, review-log head, rules applied) | P0 | ✅ | #04 #13 |
| R-09 | The API notice states only what the code backs | P0 | ✅ | #15 |
| R-10 | "Unknown" comes with the missing facts and a reason code; the integrator sets a per-variable policy (block, route to a person, hold) | P1 | ⬜ | #01 #02 #04 #08 #12 #13 |
| R-11 | Reviewer identities are pseudonymous in the chain, with a separate deletable identity map | P1 | ⬜ | #08 #13 |

## B. Security and supply chain

| ID | Requirement | Pri | Status | Source |
|---|---|---|---|---|
| R-12 | SECURITY.md, a disclosure policy and a security contact | P0 | ✅ | #01 #02 #06 #16 #19 |
| R-13 | SBOM, signed release artefacts, pinned actions and base image, least-privilege release job, dependency scanning | P1 | ⬜ | #03 #04 #11 #16 #20 |
| R-14 | Review app: CSRF/Origin check, identity on read pages. API: request size and rate limits, `/docs` switchable, validation errors that do not echo household data | P0 | ✅ | #13 #16 #20 |
| R-15 | Container health check works for both applications | P0 | ✅ | #16 |

## C. Content, ingestion and the core product

| ID | Requirement | Pri | Status | Source |
|---|---|---|---|---|
| R-16 | Change-impact report as a deliverable: what changed in the source, which rules, tests and results it moves, dated and readable | P1 | 🟡 | #01 #04 #06 #07 #08 #11 #12 #18 |
| R-17 | Parity command against a user's own known-answer cases, with a publishable result | P1 | ⬜ | #02 #03 #05 #09 #12 #14 #18 #20 |
| R-18 | HTML and PDF ingestion (state manuals, guidance, bulletins) — memos and notices load as one checked text today; clause structure still missing | P1 | 🟡 | #01 #02 #03 #04 #06 #07 #18 #20 |
| R-19 | legislation.gov.uk point-in-time ingestion | P1 | ⬜ | #09 #10 #11 #12 #18 |
| R-20 | EU sources (national XML, EUR-Lex) for the first EU domain | P2 | ⬜ | #08 #10 #11 |
| R-21 | Currency on money values; more than one jurisdiction in a package | P1 | ⬜ | #20 |
| R-22 | Check the SNAP fixture against current law (2025 legislation may have changed it) | P1 | ⬜ | #02 #18 |
| R-23 | Language-neutral export: JSON rules plus test vectors | P1 | ⬜ | #01 #03 #09 |
| R-24 | Obligation-register mode for clauses that are duties, not calculations | P2 | ⬜ | #04 #07 |
| R-36 | Households of nine or more. The pinned FY2026 memo gives rounded per-member increments ($459 net, $596 gross); implement the source-specific rule instead of extrapolating table rows | P0 | ⬜ | found by `tests/test_snap_tables.py` |
| R-37 | Retrieve and verify the official FY2027 tables for the period starting 1 October 2026; the current package answers unknown after 30 September 2026 | P0 | ⬜ | found by R-04; publication details must be checked against the retrieved source |

## D. Compliance posture

| ID | Requirement | Pri | Status | Source |
|---|---|---|---|---|
| R-25 | Intended-purpose and non-reliance statement; ADR-021/022 rewritten so they state positions, not conclusions | P0 | ✅ | #10 #13 #14 #15; revised ADR-021/022 (2026-10-10); counsel review before commercial use remains required |
| R-26 | LLM authoring optional and packaged separately; the runtime ships with no model dependency; every proposal stamped with model, version and prompt hash | P1 | 🟡 | #10 #14 |
| R-27 | Option to use a local or EU-hosted model for authoring | P2 | ⬜ | #10 |
| R-28 | AGPL note on the OpenFisca export | P0 | ✅ | #19 |
| R-29 | Reviewer app meets WCAG 2.1 AA, with a conformance statement | P1 | ⬜ | #06 #09 #10 #18 |
| R-30 | EU Cyber Resilience Act readiness before any paid EU distribution | P2 | ⬜ | #08 #14 #16 #19 |
| R-31 | Zero-access support protocol; DPA/SCC templates kept for any deployment that touches personal data | P2 | ⬜ | #13 #16 #17 |

## E. Not code — for the founder

| ID | Requirement | Source |
|---|---|---|
| R-32 | Written release from the employer covering moonlighting and IP | 12 participants |
| R-33 | Entity, liability cap, insurance — at the first signed letter of intent | 18 participants |
| R-34 | A qualified reviewer, through a partner, for each jurisdiction | #01 #03 #09 #12 #17 |
| R-35 | A second maintainer, or escrow | 17 participants |

## Explicitly not needed now

Hosted multi-tenant SaaS, per-call billing, SOC 2 / ISO 27001 before a hosted offering,
FedRAMP, Catala / LegalRuleML / PROV exports, OCR, a plugin SDK. Each was ruled not required
by most participants; see `simulated-reviews/round-3/r3-requirements-tribunal.md`.

## F. Gaps exposed by the revised documentation audit

These preserve unimplemented claims rather than calling a design or software-release
workflow a built feature. No implementation is added by this documentation pass.

| ID | Requirement | Pri | Status | Source |
|---|---|---|---|---|
| R-38 | Immutable content-pack artifact: version and hash covering source manifest/snapshots, rules, dated tables, approval-log export/head, test vectors, verification results and valid-as-of context; verify before use | P1 | ⬜ | ADR-032; round-3 product scope BUILD 4; software wheel/image releases are not content packs |
| R-39 | Enforce approval and deterministic validation on every deployed execution path for rules and parameters; keep draft CLI/library execution explicitly separated and labelled | P0 | 🟡 | `service/api.py` and default export gate; CLI `evaluate` requires an optional flag and raw `Evaluator` is ungated |
| R-40 | Automated concept/definition/parameter extraction and source cross-reference linking as optional proposal passes, with diagnostics and source evidence | P2 | ⬜ | old pipeline/product claims; current passes are segmentation and rule proposals; frozen pending demonstrated need |
| R-41 | Exception and dependency/combinatorial test generation plus a property-based suite; preserve human policy-intent tests separately | P2 | 🟡 | boundary/date/mutation tooling exists; these additional generators/framework do not |
| R-42 | Public independently annotated benchmark: gold source links, rules, tests, ambiguity labels, metrics and reproducible runner | P2 | ⬜ | old benchmark promise; current SNAP fixture is not independent expert validation |
| R-43 | Typed provenance relations, binding approvals to verified source versions, and durable end-to-end source/run/review/test lineage inside the content pack, without a standards-export dependency | P1 | 🟡 | source spans, extraction run records, hashes and review events exist; unified relation model does not |
| R-44 | Mechanically scoped contradiction/completeness checks and multi-axis time; close documented period compatibility/prorating, clamp-bound, exception-tie and override-severity gaps without silently weakening the spec | P2 | ⬜ | old architecture, ADR-020 and `docs/04_RULE_IR_SPEC.md`; current implementation uses effective intervals |
| R-45 | Review surface for ambiguity resolution, policy-intent/test approval and dependency/change history; blind dual-encoding workflow if required by the content owner | P1 | 🟡 | rule editing, decisions and diagnostics exist; complete review surface does not |
| R-46 | England Universal Credit core plus April-uprating reference content, including source/reuse verification and independent known-answer cases; start only after the owner's decision | P2 | ⬜ | ADR-032; candidate from simulated reviews, not customer evidence |

## Evidence for completed and partial claims

Paths below are repository-relative. Passing tests show the checked scope, not legal
correctness, current-law coverage, reviewer qualification or market demand.

| Requirement | Evidence and boundary |
|---|---|
| R-01 | `src/ruleweaver/review/seeding.py`, `tests/test_seeding.py`: queue faults and aggregate metrics; not proof qualified humans detect real interpretation errors |
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
