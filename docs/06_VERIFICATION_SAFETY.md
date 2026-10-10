# 06 — Verification, Safety, and Trust Model

RuleWeaver produces reviewable interpretations of benefit/tax rules. Official sources retain authority. The intended self-hosted workflow requires a person to approve both rules and parameter tables before deployed execution. It provides change impact plus independent verification, not an authoritative legal determination. See ADR-032 and `docs/10_BACKLOG.md`; intended-purpose statements are not legal advice and need counsel review before commercial use (R-25).

## Threats and current controls

A plausible result can conceal a wrong interpretation, omitted exception, scope/definition mistake, wrong effective date, threshold error, stale table, false citation or adapter drift. Source text can contain instruction-like content. A user can mistake a passing test or signed-in reviewer for sufficient policy assurance.

| Control | State and evidence | Remaining requirement |
|---|---|---|
| Typed closed expression AST and deterministic evaluator | **Built:** `src/ruleweaver/ir/expressions.py`, `runtime/evaluator.py`, `tests/test_snap_evaluation.py`; runtime has no model dependency. | Complete optional authoring packaging separation is **Partial**, R-26. |
| Structural verification and source-span checking | **Built** for implemented checks: `src/ruleweaver/verify/validators.py`, `types.py`, `tests/test_validators.py`, `tests/test_provenance_validation.py`. Corpus checking requires a supplied corpus. | Completeness/contradiction and extended temporal validation are **Planned**, R-44. |
| Hash-bound rule and parameter approval | **Built:** `src/ruleweaver/approval.py`, `tests/test_approval.py`, `tests/test_parameter_gate.py`: changes to approved structured objects or cited spans invalidate approval. | Universal deployed enforcement is **Planned**, R-39. |
| Durable review events and hash chain | **Partial:** `src/ruleweaver/review/store.py`, `tests/test_review_store.py`: append API and unkeyed chain verification. | Administrator-resistant keyed chain, external key and exported checkpoints are **Planned**, R-05. A database administrator can rewrite and recompute today's chain. |
| Reviewer authentication | **Partial:** `src/ruleweaver/review/identity.py`, `tests/test_identity.py`: signed token/trusted-proxy mechanisms and fail-closed configuration. | Shared-secret token minting does not establish independent reviewer identities or author/approver separation; **Planned**, R-06. |
| Review fault seeding | **Built:** `src/ruleweaver/review/seeding.py`, `tests/test_seeding.py`: planted mutants, notice and aggregate catch rate; mutant decisions cannot approve/reject the real rule. | Reviewer qualification R-07, pseudonymous chain with separate identity map R-11 and accessible review R-29 are **Planned**. Aggregate metrics do not make stored identities pseudonymous. |
| Request protections | **Built** for tested application routes: `tests/test_review_app.py`, `tests/test_service.py` cover Origin/CSRF and authenticated reads, request/rate limits and non-echoing validation responses (R-14). | These tests do not certify a production deployment or third-party proxy configuration. |
| Replay record in calculation responses | **Built:** `src/ruleweaver/service/api.py`, `tests/test_service.py`: package hash, review-chain head and execution trace (R-08). | Full release provenance and lineage remain **Planned**, R-38/R-43. |

## Approval is a deployment invariant with a remaining gap

**Built:** the calculation service and default OpenFisca export consult approval. Rule/parameter edits move the relevant hashes. Unapproved parameter values can be withheld, yielding unknown; overridden base rules are also withheld where dropping an unapproved override would otherwise change the interpretation (`tests/test_approval.py`, `tests/test_parameter_gate.py`).

**Planned, R-39:** enforce approval for every deployed execution entry point. CLI evaluation currently exposes optional `--require-approval`; direct `Evaluator` use is ungated. The intended rule that drafts cannot determine deployed results is stronger than current coverage. A status field or model confidence must never replace review-log evidence.

**Planned:** record reviewer qualifications R-07, bind individual identities and separate author/approver R-06, and preserve pseudonymous reviewer IDs with a separately deletable identity map R-11. Hosting locally does not itself satisfy these requirements.

## Unknown, ambiguity and unsupported results

**Built:** `src/ruleweaver/runtime/values.py` and `evaluator.py` distinguish true, false, unknown and evaluation error; missing input is not silently false or zero. `tests/test_snap_evaluation.py` and `tests/test_parameter_gate.py` exercise propagation. `src/ruleweaver/ir/rules.py` carries blocking ambiguities, and validators diagnose unresolved blocking cases.

**Planned, R-10:** unknown must expose reason codes, missing facts and integrator-selected block/hold/person-routing policy. A trace or generic unknown sentinel is not this facility. **Planned, R-44/R-45:** systematic ambiguity/completeness detection and review of resolutions. Unsupported source concepts and human judgment must remain visible rather than being guessed away.

## Provenance and source integrity

**Built:** source manifests pin bytes and PDF renderings (`src/ruleweaver/ingest/corpus.py`, `tests/test_ingest.py`); typed spans connect rules, exceptions, parameters and individual parameter values to sources (`src/ruleweaver/ir/rules.py`, `tests/test_provenance_validation.py`). Review events bind reviewer actions to structured/source hashes (`review/decisions.py`, `tests/test_review.py`). Model call metadata records prompt/input/output hashes (`models/base.py`, `tests/test_models.py`).

**Planned, R-43:** joined derivation and compilation/review/test lineage must answer which run proposed an object, which validations ran, which tests a reviewer approved, and which build produced its artifact. Separate records are not a complete relation graph. PROV export is outside the roadmap; internal traceability remains required.

## Verification independence

**Built:** deterministic boundary/date generation and mutation execution (`src/ruleweaver/testgen/`, `tests/test_date_generation.py`, `tests/test_mutation.py`) and supported OpenFisca differential checks (`tests/test_openfisca_equivalence.py`). These detect some defects but can share the same interpretation mistake.

**Planned:** independent parity against user known-answer cases R-17; a public independently annotated benchmark R-42; broader exception/combinatorial/property generation R-41 and explicit test review R-45. Preserve origins such as human policy intent, source worked example, structural boundary, mutation and adapter differential. Never overwrite human-approved intent tests with newly proposed tests.

## Change and release safety

**Partial, R-16:** `src/ruleweaver/diff/semantic.py`, `impact.py` and `tests/test_amendment_impact.py` compare IR revisions, follow dependencies and rerun supplied scenarios. A dated source-to-rule-to-test change-impact deliverable is still needed. Changes must retain the previous snapshot, invalidate affected approval and require review before a new approved content pack.

**Planned:** versioned hashed content-pack artifact R-38, signed artifacts/SBOM R-13, current-law SNAP review R-22, nine-plus household increments R-36 and FY2027 tables R-37. FY2026 data is a dated reference, not proof of current benefit entitlement.

## Source handling and self-hosting

**Built:** optional proposal handling fences untrusted source text and escalates suspicious instructions (`src/ruleweaver/models/guard.py`, `tests/test_compile.py`). Model output remains typed data; the deterministic adapter lowers supported IR rather than executing arbitrary model-written programs. These controls do not establish prompt-injection immunity.

Self-hosting with no supporter access to household data is the intended deployment model. **Planned, R-31:** operational zero-access support protocol; external authoring providers must not receive personal case data by default. The calculation service, OpenFisca and model authoring are frozen maintenance options. No hosted offering or certification is implied.

## Reconciled review safeguards

**Built:** signed reviewer/item tokens for cookie-authenticated decisions, alongside Origin checks; approval blocks validation errors and edits validate the corrected package before recording. `tests/test_review_app.py` proves these routes. Complete source-version binding and universal deployed validation remain R-43/R-39.
