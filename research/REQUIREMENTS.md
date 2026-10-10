# Requirements from the simulated reviews

Derived from `simulated-reviews/` (2026-10-10). Numbers in brackets are the round-1
participants who demanded the item independently, e.g. [#16, #20]. The reviews are simulated,
so a requirement here is a hypothesis about what users need, not proof.

**Priorities.** P0: a claim the project makes that the code does not yet back — fix the
code. P1: needed for a first version people can actually use. P2: after the first real
user. **Status:** ✅ done · 🟡 partial · ⬜ not started.

The rule from here on: the project claims only what the code does, and the code is built
up to what the project should be able to claim.

## A. Make the claims true

| ID | Requirement | Pri | Status | Source |
|---|---|---|---|---|
| R-01 | Seeded faults are actually planted in the review queue, reviewers are told such tests exist, and catch-rate metrics are aggregate and pseudonymised by default | P0 | ✅ | #01 #07 #11 #12 #14 #20; monitoring limits #08 #13 |
| R-02 | "Edit" works from the form and approves only the corrected rule | P0 | ✅ | verified fact 2 |
| R-03 | Parameters are sourced, dated objects inside the approval gate, with a diagnostic for missing values | P0 | ⬜ | #01 #03 #09 #20 |
| R-04 | The shipped example package computes: complete tables, each value sourced | P0 | ⬜ | verified fact 3 |
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
| R-12 | SECURITY.md, a disclosure policy and a security contact | P0 | ⬜ | #01 #02 #06 #16 #19 |
| R-13 | SBOM, signed release artefacts, pinned actions and base image, least-privilege release job, dependency scanning | P1 | ⬜ | #03 #04 #11 #16 #20 |
| R-14 | Review app: CSRF/Origin check, identity on read pages. API: request size and rate limits, `/docs` switchable, validation errors that do not echo household data | P0 | ⬜ | #13 #16 #20 |
| R-15 | Container health check works for both applications | P0 | ✅ | #16 |

## C. Content, ingestion and the core product

| ID | Requirement | Pri | Status | Source |
|---|---|---|---|---|
| R-16 | Change-impact report as a deliverable: what changed in the source, which rules, tests and results it moves, dated and readable | P1 | 🟡 | #01 #04 #06 #07 #08 #11 #12 #18 |
| R-17 | Parity command against a user's own known-answer cases, with a publishable result | P1 | ⬜ | #02 #03 #05 #09 #12 #14 #18 #20 |
| R-18 | HTML and PDF ingestion (state manuals, guidance, bulletins) | P1 | ⬜ | #01 #02 #03 #04 #06 #07 #18 #20 |
| R-19 | legislation.gov.uk point-in-time ingestion | P1 | ⬜ | #09 #10 #11 #12 #18 |
| R-20 | EU sources (national XML, EUR-Lex) for the first EU domain | P2 | ⬜ | #08 #10 #11 |
| R-21 | Currency on money values; more than one jurisdiction in a package | P1 | ⬜ | #20 |
| R-22 | Check the SNAP fixture against current law (2025 legislation may have changed it) | P1 | ⬜ | #02 #18 |
| R-23 | Language-neutral export: JSON rules plus test vectors | P1 | ⬜ | #01 #03 #09 |
| R-24 | Obligation-register mode for clauses that are duties, not calculations | P2 | ⬜ | #04 #07 |

## D. Compliance posture

| ID | Requirement | Pri | Status | Source |
|---|---|---|---|---|
| R-25 | Intended-purpose and non-reliance statement; ADR-021/022 rewritten so they state positions, not conclusions | P0 | ⬜ | #10 #13 #14 #15 |
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
