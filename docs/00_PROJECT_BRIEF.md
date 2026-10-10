# 00 — Project Brief

## Purpose and value

RuleWeaver is a self-hosted compiler and verifier for computable benefit and tax
rules. It connects an executable interpretation to the source clauses and published
figures that support it. The intended deliverable is **change impact plus independent
verification**: which rules, parameters, tests and results a change affects, together
with parity against the operator's own known-answer cases.

**Partial:** semantic package comparison, dependency closure and scenario outcome
comparison exist in `src/ruleweaver/diff/semantic.py` and
`src/ruleweaver/diff/impact.py`, exercised by `tests/test_amendment_impact.py`.
The complete dated, source-linked change report is not built (R-16).
**Planned:** the independent known-answer parity command is not built (R-17).

The owner has chosen to make the first version work well before pursuing sales.
The private simulated review exercises supply hypotheses and
risk questions; their participants, prices and preferences are not market evidence.
ADR-032 in `docs/11_DECISIONS.md` records the revised plan.

## Intended users

Rules engineers maintain the typed interpretation and its tests. Policy reviewers
compare each interpretation and parameter table with the cited source. Program
maintainers examine annual updates and affected outcomes. Integrators supply
independent known-answer cases and decide how to handle unresolved results.
These are intended users, not evidence of customers or external adoption.

## Deployment and approval boundary

The deployment model is self-hosted: source artifacts, review records and household
inputs belong in the operator's environment. Zero-access support is the intended
operating practice; a protocol enforcing it is not built (R-31). Self-hosting alone
does not prove that a supporter cannot access personal data.

**Built:** the evaluator in `src/ruleweaver/runtime/evaluator.py` computes supported
rules deterministically without a model call (`tests/test_snap_evaluation.py`).
**Partial:** `src/ruleweaver/approval.py` gates both rules and parameter tables by
matching current content/source hashes to review decisions
(`tests/test_approval.py`, `tests/test_parameter_gate.py`). The calculation service
uses that gate (`tests/test_service.py::TestTheGate`). Approval enforcement across
all deployed execution paths is not built (R-39): the CLI uses optional
`--require-approval`, and direct evaluator calls do not consult a review log.

The target is execution only after explicit human approval. Model confidence must
never authorize a rule. Outputs are technical evidence for review, not legal advice
or an official benefit or tax determination. The intended-purpose and non-reliance
positions are recorded under R-25; counsel review is required before commercial use.

## Content boundary

**Built:** the SNAP reference fixture contains 15 rules and sourced FY2026 federal
tables for the 48 states and DC (`examples/snap/rules.json`,
`examples/snap/sources/manifest.json`, `tests/test_snap_tables.py`). This is a
bounded reference demo, not a complete current SNAP implementation.

**Partial:** FY2026 values end on 30 September 2026; the fixture cannot provide
current table-dependent answers on 10 October 2026. FY2027 content is not built
(R-37). Correct income-limit increments for households of nine or more are not built
(R-36), and the effect of 2025 legislation on the fixture has not been audited
(R-22). These limitations must remain visible in every demonstration.

**Planned:** benefits in England, starting with Universal Credit and the April
uprating, are the leading next content candidate (R-46). That corpus is not started;
the owner decides whether to start it. Point-in-time ingestion and explicit currency
support are also not built (R-19, R-21).

## Build, maintain and exclude

| Stance | Scope | Evidence or remaining requirement |
|---|---|---|
| BUILD | Source snapshots, typed IR and deterministic evaluation | Built supported subset: `src/ruleweaver/ingest/`, `src/ruleweaver/ir/`, `src/ruleweaver/runtime/`; broader ingestion Partial (R-18), UK ingestion Planned (R-19) |
| BUILD | Verification and human approval of rules and figures | Built checks and gate: `src/ruleweaver/verify/`, `src/ruleweaver/approval.py`; universal gate Partial (R-39), richer semantics Planned (R-44) |
| BUILD | Review application and accountable sign-off | Partial: `src/ruleweaver/review/`, `tests/test_review_app.py`; administrator-resistant audit, per-person identity, qualification, pseudonyms and accessibility not built (R-05, R-06, R-07, R-11, R-29) |
| BUILD | Change impact, independent parity and content-pack artifact | Partial comparison (R-16); parity and immutable versioned pack Planned (R-17, R-38) |
| FREEZE | Calculation service | Built bounded HTTP evaluation: `src/ruleweaver/service/`, `tests/test_service.py`; retain for self-hosted or synthetic-data use |
| FREEZE | OpenFisca export | Built supported subset: `src/ruleweaver/adapters/openfisca/`, `tests/test_openfisca_equivalence.py`; maintain only; AGPL note under R-28 |
| FREEZE | Optional model authoring | Partial: two proposal passes in `src/ruleweaver/compile/`, `tests/test_compile.py`; separate packaging and complete metadata not built (R-26) |

Catala, LegalRuleML, PROV export, Akoma Ntoso, OCR, a plugin SDK and hosted
multi-tenant SaaS are removed from the active roadmap. Pre-hosted SOC 2, ISO 27001
and FedRAMP work is also excluded. Standards may remain historical design references.

## Quality bar and next decisions

Correctness must stand without optional model authoring or an adapter. Tests produced
from the same evaluator demonstrate consistency; only independent policy-intent cases
can supply independent verification. An independently annotated public benchmark is
not built (R-42).

The remaining claims and their priorities live in `docs/10_BACKLOG.md`.
The first work is current SNAP content and approval/audit hardening, followed by the
change report, parity and content-pack boundary. No deadline substitutes for evidence.
The owner still needs to decide the next corpus (R-46) and arrange the qualified
reviewer and other founder decisions in R-32–R-35.
