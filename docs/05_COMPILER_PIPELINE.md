# 05 — Compiler Pipeline

The product is a self-hosted compiler and verifier. Its intended deliverable is source-linked change impact plus independent verification against the user's own cases. Optional model authoring proposes interpretations; deterministic validation and human approval remain separate. See ADR-032 in `docs/11_DECISIONS.md` and `docs/10_BACKLOG.md` for priorities and status.

## Passes and implementation evidence

| Pass | State | Evidence and remaining requirement |
|---|---|---|
| P0 ingest snapshots | **Built** for the committed corpus | `src/ruleweaver/ingest/corpus.py`, `tests/test_ingest.py`: verifies manifest hashes, including separately pinned PDF text renderings. |
| P1 source structure | **Partial** | `src/ruleweaver/ingest/ecfr.py` and `markers.py` address eCFR clauses; `plain.py` reads plain text/HTML and pinned PDF renderings as one block. Structural HTML/PDF tables, paragraphs and references remain R-18; legislation.gov.uk remains R-19. |
| P2 clause classification | **Built**, optional and frozen | `src/ruleweaver/compile/segment.py`, `tests/test_compile.py`: classifies clauses and records non-computable/uncertain results. This does not establish extraction accuracy on independent data. |
| P3 concept extraction | **Planned** | R-40: automated definitions, parameters, entities and concept reuse. Today `compile/extract.py` takes `Vocabulary` from an existing package; it does not discover a complete vocabulary. |
| P4 rule proposal | **Built**, optional and frozen | `src/ruleweaver/compile/extract.py`, `tests/test_compile.py`: typed proposals, abstention, provenance checks and injection escalation. No proposal approval occurs here. |
| P5 reference linking | **Partial** | `src/ruleweaver/verify/validators.py`, `tests/test_validators.py` resolve declared IR references; `tests/test_provenance_validation.py` checks cited spans against a supplied corpus. Automated cross-document semantic linking remains R-40. |
| P6 ambiguity analysis | **Partial** | `src/ruleweaver/ir/rules.py` represents ambiguities; `compile/extract.py` preserves candidates; validators block unresolved blocking ambiguities. Systematic contradiction/completeness analysis remains R-44. |
| P7 verification | **Built** for implemented passes | `src/ruleweaver/verify/validators.py`, `types.py`, `tests/test_validators.py`, `tests/test_types.py`: references, types, duplicate IDs, dependency/override cycles, periods and provenance diagnostics. Additional temporal/semantic checks remain R-44; see `docs/04_RULE_IR_SPEC.md` for specification gaps. |
| P8 test generation | **Partial** | `src/ruleweaver/testgen/boundaries.py`, `dates.py`, `mutation.py`; `tests/test_date_generation.py`, `tests/test_mutation.py`: threshold/date candidates and mutation execution. Broad exception/combinatorial/property generation remains R-41. |
| P9 review | **Partial** | `src/ruleweaver/review/app.py`, `decisions.py`, `seeding.py`, `tests/test_review_app.py`, `tests/test_seeding.py`: source-linked rule/parameter review, edits, seeded faults and aggregate metrics. Distinct identities/separation R-06, qualification R-07, pseudonymity R-11, accessibility R-29 and broader review UX R-45 remain. |
| P10 approved content-pack build | **Partial** | `src/ruleweaver/approval.py`, `tests/test_approval.py`, `tests/test_parameter_gate.py`: hash-bound rule and parameter approvals, staleness and withholding. Versioned content-pack release artifact remains R-38; universal deployed gate R-39; signing/SBOM R-13. |
| P11 OpenFisca export | **Built** for supported subset, frozen | `src/ruleweaver/adapters/openfisca/`, `tests/test_openfisca.py`, `tests/test_openfisca_equivalence.py`: approval-aware export, explicit refusals and differential checks. This is adapter consistency, not independent policy parity R-17. |
| Change impact | **Partial** | `src/ruleweaver/diff/semantic.py`, `impact.py`, `tests/test_amendment_impact.py`: IR change/dependency analysis and before/after scenario results. Dated source-to-rule-to-test deliverable remains R-16. |
| Independent user parity | **Planned** | R-17: local command over independent user known-answer cases with a publishable result. |

These passes describe boundaries, not a claim that one command implements every stage. `src/ruleweaver/compile/pipeline.py` assembles a candidate from an existing vocabulary, keeps run diagnostics, and stops before approval (`tests/test_compile.py`).

## Source and interpretation boundaries

Snapshots are inputs, not instructions. Keep official origin/version, retrieval metadata and hashes. The committed SNAP corpus includes federal eCFR XML, the FNS FY2026 memo PDF with a pinned text rendering, and HHS published figures. A changed remote page must create a new snapshot, not rewrite an old approved interpretation. Structural extraction from arbitrary HTML/PDF is **Planned** under R-18; OCR is outside the roadmap.

Proposal context should include the clause, its neighbours, referenced definitions and explicitly supplied authoritative sources. Missing evidence must be recorded as missing; general model knowledge must not fill a policy fact. Full automated concept linking is **Planned** under R-40.

## Validation, tests and approval

Validation returns typed diagnostics with stable codes; passing it is evidence of implemented structural checks, not a proof of correct legal interpretation. Candidate tests must preserve origin and must not overwrite approved policy-intent tests. Broader test approval and ambiguity-resolution interfaces are **Planned** under R-45.

Intended release policy: no unapproved rule or parameter table runs in a deployed content pack. Current enforcement is narrower: the calculation service and default OpenFisca export use the gate; CLI evaluation requires opt-in `--require-approval`; direct library evaluation is ungated. Closing that difference is **Planned**, R-39, rather than a reason to weaken the policy.

## Reproducibility

**Built:** `src/ruleweaver/models/base.py` records provider/model, prompt ID/version, decoding settings, request timestamp, input/output hashes; `compile/pipeline.py` records source digests and prompt content hashes (`tests/test_models.py`, `tests/test_compile.py`). A fixed seed or temperature does not guarantee identical remote output.

**Planned:** complete run-to-review-to-approved-test lineage R-43 and the versioned hashed content-pack envelope R-38, including compiler/schema/source versions and artifact hashes. Provider-free runtime is supported by the module boundary; complete packaging separation remains **Partial**, R-26.

The self-hosted calculation service, OpenFisca adapter and model authoring remain maintained but frozen. Catala, LegalRuleML, PROV and Akoma Ntoso exports, OCR, plugin SDK and hosted multi-tenant SaaS are outside this roadmap.
