# 01 — Project Status

**Evidence date:** 2026-10-10. **Plan:** ADR-032, self-hosted compiler/verifier;
change impact plus independent known-answer verification. Requirement status and priority
live in `research/REQUIREMENTS.md`. This is an evidence snapshot, not a second backlog.

## Built supported components

| Capability | Evidence |
|---|---|
| Typed closed IR, rules/entities/parameters/spans | `src/ruleweaver/ir/`, `tests/test_schema_artifact.py` |
| Deterministic Decimal evaluation, effective periods, exceptions/overrides, unknowns and trace | `src/ruleweaver/runtime/`, `tests/test_snap_evaluation.py`, `tests/test_allotment.py` |
| Schema/type/reference/dependency/date/source checks | `src/ruleweaver/verify/`, `tests/test_validators.py`, `tests/test_types.py`, `tests/test_provenance_validation.py` |
| Boundary/date candidates, mutation harness | `src/ruleweaver/testgen/`, `tests/test_date_generation.py`, `tests/test_mutation.py` |
| eCFR hierarchical clauses, memo/notice canonical text, hashed snapshots/renderings | `src/ruleweaver/ingest/`, `tests/test_ingest.py`, `tests/test_markers.py` |
| Rules and sourced dated tables in review gate | `src/ruleweaver/approval.py`, `tests/test_approval.py`, `tests/test_parameter_gate.py` |
| Source/item review, edit decisions, planted faults and aggregate metrics | `src/ruleweaver/review/app.py`, `seeding.py`, `tests/test_review_app.py`, `tests/test_seeding.py` |
| Calculation service with gating/replay records and limits, frozen | `src/ruleweaver/service/`, `tests/test_service.py` |
| OpenFisca code/YAML export and executed differential harness, frozen | `src/ruleweaver/adapters/openfisca/`, `tests/test_openfisca.py`, `tests/test_openfisca_equivalence.py` |
| Optional segmentation and rule proposals with prompt/run hashes, frozen | `src/ruleweaver/compile/`, `models/`, `tests/test_compile.py`, `tests/test_models.py` |
| Software build/test/release configuration | `pyproject.toml`, `Dockerfile`, `.github/workflows/tests.yml`, `.github/workflows/release.yml`; configuration exists, no release performed in this session |

The supported core is built; the first-version deliverable is incomplete. A passing
fixture is not an independently reviewed benchmark or qualified legal interpretation.

## Partial components and planned claims

| Claim not yet fully built | Requirement and present boundary |
|---|---|
| Current SNAP coverage | R-37 FY2027 absent; FY2026 tables end 30 September 2026. R-36 nine-plus increments absent. R-22 current-law/2025 changes not audited |
| Complete dated source-linked impact report | R-16: semantic package diff, dependency closure and scenario outcomes exist; structural source diff, affected-test list and durable report do not |
| Independent user known-answer parity | R-17: not built; OpenFisca comparisons use the native evaluator as oracle |
| Immutable versioned hashed content pack | R-38: not built; separate source hashes, packages and software releases are not the pack |
| Universal deployed approval enforcement | R-39: service/default export gated; CLI `--require-approval` optional and direct evaluator ungated |
| Administrator-resistant audit | R-05: keyed chain/checkpoints absent; current unkeyed log can be rewritten/rehashed by an administrator |
| Distinct reviewer identity and separation | R-06: shared-secret session/proxy plumbing exists; per-person binding and author/approver separation absent |
| Qualification, reviewer privacy and accessibility assurance | R-07/R-11/R-29 not built; aggregate metrics do not pseudonymise stored identities |
| Missing-fact reasons and integrator disposition | R-10 not built; unknown/trace exists |
| Signed artifacts, SBOM, complete supply-chain controls | R-13 not built; software release workflow is not that evidence |
| Structured HTML/PDF and UK point-in-time ingestion | R-18 Partial canonical text/pinned renderings only; R-19 not built |
| Currency/multiple jurisdictions and portable rules/test vectors | R-21/R-23 not built |
| Complete optional authoring separation/metadata | R-26 Partial; no independently measured live extraction accuracy |
| Local/EU-hosted authoring | R-27 not built, deferred |
| Zero-access support protocol | R-31 not built; self-hosting alone cannot guarantee no supporter access |
| Automated definitions/parameters/concepts and cross-document linking | R-40 not built; current passes consume an existing vocabulary |
| Exception/combinatorial/property test tooling | R-41 Partial; boundary/date/mutation tooling exists |
| Independently annotated public benchmark | R-42 not built; no independent expert annotation/runner/metrics release |
| Complete provenance relation and source-version binding | R-43 Partial spans/run/review records; changing snapshot bytes alone does not move embedded-span approval hashes |
| Contradiction/completeness, multi-axis time and documented semantic gaps | R-44 not built; period compatibility/prorating, bound validation and diagnostic severity differ from parts of the spec |
| Full ambiguity/test/dependency/history review surface | R-45 Partial rule/table decisions and diagnostics; full workflow/dual encoding absent |
| England Universal Credit and April uprating | R-46 not started; owner chooses whether to begin |

R-25 documentation is complete: ADR-021/022 now state intended purpose/non-reliance,
not legal classification or compliance dates. Counsel review remains required before
commercial use. R-32–R-35 founder decisions have no completion evidence.

## Verified baseline and content evidence

The pulled baseline `77184e6` passed **554 tests** after installing
`.[dev,review,openfisca]`. Ruff passed; mypy passed on **55 source files**. Windows needs
a fresh `--basetemp` inside `.pytest_cache/` on the repository's drive for the nested
OpenFisca runner; the initial cross-drive run failed at a protected junction. No source
change was required to pass. Final integration results are recorded in shared memory.

`tests/test_snap_tables.py` re-reads FY2026 figures from pinned FNS/HHS snapshots and tests
income-limit edges for household sizes 1–8. It explicitly tests unknown on 1 October 2026
and for size nine. The FNS memo is an Alaska redistribution; the manifest calls for
comparison against FNS's own copy before reliance. Tests prove consistency with stored
sources, not current-law completeness.

The synthetic mutation suite enforces detection of its planted faults
(`tests/test_mutation.py`); its constructed tables are not published policy figures.
OpenFisca comparisons report matches/mismatches/gaps; they are not independent user parity.
The guarded allotment remains unexported and float-rounding differences remain visible
(ADR-031). Native evaluation remains the semantic reference.

## Next work and risks

Follow P0 R-37 → R-05 → R-06 → R-36 → R-39, then the P1 report/parity/pack and hardening
sequence in `docs/09_IMPLEMENTATION_ROADMAP.md`. Do not describe the demo as current
policy until its rule coverage and figures are verified. Qualified reviewer arrangements,
commercial governance, independent known-answer cases and the next corpus still need
owner/operator decisions.

Risks: plausible but wrong interpretations; stale sources/tables; weak approval identity;
rewritable audit evidence; generation/tests sharing mistakes; unhandled unknowns; incomplete
source-version binding; spec/runtime mismatches; over-expansion into subjective law or
hosted data flows. Current implementation evidence must remain separate from intended
controls and hypothetical market demand.
