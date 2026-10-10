# 02 — Product Specification

## Intended product

RuleWeaver is a self-hosted compiler and verifier for benefit and tax rules. Its
intended workflow preserves source evidence, proposes or accepts typed interpretations,
validates them, obtains human approval of rules **and** dated parameter tables, and
executes supported interpretations deterministically. The deliverable is change
impact plus parity against independently supplied known-answer cases.

This is the revised plan in ADR-032 (`docs/11_DECISIONS.md`). Simulated reviews
inform requirements; they are hypotheses, not customer research or purchase evidence.
`research/REQUIREMENTS.md` is the single source of truth for requirement status and
priority. The evidence below describes the current implementation and its limits.

## Users and deployment

| Intended user | Job |
|---|---|
| Rules engineer | Maintain vocabulary, rules, sourced figures and regression cases |
| Policy reviewer | Compare exact source evidence with a structured interpretation; approve or reject it |
| Program maintainer | Review annual upratings, source changes and affected results |
| Integrator | Run independent known-answer cases and define handling for unknown results |

Self-hosting is the operating model. Zero-access support is intended; its protocol
and access controls are not built (R-31). An operator's deployment and support
arrangements determine actual access to personal data.

The deterministic runtime has no model call in its execution path
(`src/ruleweaver/runtime/evaluator.py`, `tests/test_snap_evaluation.py`). Optional
model authoring belongs outside that path. Separate authoring packaging and complete
proposal metadata remain Partial (R-26); local or EU-hosted authoring is Planned
(R-27). No model confidence score grants approval.

Outputs are technical evidence for review, not legal advice or an official
benefit or tax determination. Intended-purpose and non-reliance positions belong
to R-25 and ADR-021/022; counsel review is needed before commercial use.

## Workflow and acceptance requirements

| Stage | Present capability and proof | Remaining acceptance requirement |
|---|---|---|
| 1. Preserve source | **Built:** manifests and digests checked by `src/ruleweaver/ingest/corpus.py`, `tests/test_ingest.py::TestManifestVerification`; eCFR hierarchy in `ingest/ecfr.py` and `tests/test_markers.py` | **Partial:** structured HTML/native-text PDF ingestion (R-18); **Planned:** UK point-in-time ingestion (R-19) |
| 2. Record figures | **Built:** dated parameter values with per-value source spans in `src/ruleweaver/ir/rules.py`, `tests/test_parameter_gate.py::TestDiagnostics`, `tests/test_snap_tables.py` | **Planned:** correct nine-plus increments and FY2027 values (R-36, R-37); current-law audit (R-22) |
| 3. Author interpretation | **Built:** hand-authored typed package in `examples/snap/rules.json`; proposal classification and rule extraction in `src/ruleweaver/compile/`, `tests/test_compile.py` | **Partial:** optional authoring product boundary (R-26); **Planned:** concept/definition/parameter extraction and cross-document linking (R-40) |
| 4. Verify mechanically | **Built:** schema, operand/assignment types, references, cycles, effective intervals, source spans, ambiguity and piecewise checks in `src/ruleweaver/verify/`, `tests/test_validators.py`, `tests/test_types.py`, `tests/test_provenance_validation.py` | **Planned:** contradiction/completeness diagnostics and multi-axis temporal semantics (R-44) |
| 5. Test interpretation | **Built:** threshold and date candidates in `src/ruleweaver/testgen/boundaries.py`, `dates.py`, `tests/test_date_generation.py`; mutant harness in `testgen/mutation.py`, `tests/test_mutation.py` | **Planned:** exception, combinatorial and property tooling (R-41); independent benchmark (R-42) |
| 6. Review and approve | **Built:** source/item display, approve/reject/edit and parameter review in `src/ruleweaver/review/app.py`, `tests/test_review_app.py`; seeded queue faults in `review/seeding.py`, `tests/test_seeding.py` | **Partial:** broader ambiguity/test/dependency-history workflow (R-45); **Planned:** independent reviewer identity, qualification, privacy and accessibility (R-06, R-07, R-11, R-29) |
| 7. Gate execution | **Built:** hash-matched rule/table gate in `src/ruleweaver/approval.py`, `tests/test_approval.py`, `tests/test_parameter_gate.py`; service gating in `tests/test_service.py::TestTheGate` | **Partial:** universal deployed enforcement (R-39); CLI approval is optional and direct evaluator calls remain ungated |
| 8. Explain execution | **Built:** four-state values and trace in `src/ruleweaver/runtime/`, `tests/test_snap_evaluation.py`; service record in `tests/test_service.py::TestDecisionRecord` | **Planned:** unknown reason codes/missing facts and integrator policy (R-10); full source/run/approval/test lineage (R-43) |
| 9. Compare changes | **Built:** package semantic comparison, dependent rules and before/after scenario outcomes in `src/ruleweaver/diff/`, `tests/test_amendment_impact.py` | **Partial:** dated report linking source changes and affected tests to moved outcomes (R-16) |
| 10. Verify independently | **Built:** supported OpenFisca differential execution in `src/ruleweaver/adapters/openfisca/equivalence.py`, `tests/test_openfisca_equivalence.py` | **Planned:** operator-owned known-answer parity command and publishable report (R-17); adapter consistency does not establish legal correctness |
| 11. Package evidence | **Built:** serialized IR and schema in `src/ruleweaver/ir/`, `tests/test_schema_artifact.py`; package/review hashes in service records | **Planned:** immutable versioned content pack binding sources, tables, approvals, tests and validity metadata (R-38); portable JSON/test vectors (R-23); SBOM/signing (R-13) |

## Output contract

**Built:** `RulePackage` serializes entities, variables, parameters, rules and
ambiguities (`src/ruleweaver/ir/rules.py`). Source manifests, compilation run records,
review logs and generated tests currently exist as separate artifacts
(`src/ruleweaver/ingest/corpus.py`, `compile/pipeline.py`, `review/store.py`,
`testgen/`). Their existence is not proof of a complete release unit.

**Planned — R-38:** a content pack shall bind an immutable version identifier and
hash to the source snapshots and manifest, typed rules, dated/sourced figures,
review-log export and head, approved policy-intent cases, diagnostics and generation
metadata. It shall identify its jurisdiction, supported scope and validity date.
**Planned — R-43:** relationships shall allow a reviewer to follow a result back
through the run, approval, tests and cited source without losing intermediate evidence.

**Planned — R-17:** parity shall accept the operator's independent cases and expected
results, preserve unknown/error outcomes, pin the pack/version/date, and emit a
reproducible pass/mismatch report. Reusing evaluator-derived expected values cannot
satisfy this requirement.

**Partial — R-16:** the change report shall connect source and parameter changes to
structured changes, dependent rules, affected tests and scenario outcomes. Existing
comparison functions provide part of that chain, not the full report.

## Human approval and audit

A changed rule, figure or embedded source span invalidates its old approval. That
behavior is **Built** in `src/ruleweaver/approval.py` and
`tests/test_parameter_gate.py::TestGate`; unapproved parameter values are withheld.
The gate must be used by every deployed path (**Partial**, R-39).

The hash-chained review log detects inconsistent edits (**Built**:
`src/ruleweaver/review/decisions.py`, `tests/test_review_store.py`). Resistance to an
administrator who can rewrite the database and chain is **Planned**, not built
(R-05). Signed-token or trusted-proxy identity plumbing exists (**Built**:
`review/identity.py`, `tests/test_identity.py`), but a shared signing secret can mint
arbitrary reviewer names. One identity per person and author/approver separation are
**Planned** (R-06).

Reviewer qualification (R-07), pseudonymous chain identifiers with a separate identity
map (R-11), and broader ambiguity resolution/test approval workflows (R-45) are not
built. Planted review faults are quality checks, not proof of qualified review or
legal compliance. Aggregate metrics are exercised by `tests/test_seeding.py`.

## Content scope

**Built:** SNAP is the reference corpus and demo: 15 rules plus FY2026 federal figures
for the 48 states and DC (`examples/snap/rules.json`, `tests/test_snap_tables.py`).
The table period ended on 30 September 2026. Current FY2027 content is **Planned**
(R-37); correct nine-plus income increments are **Planned** (R-36); reconciliation
with 2025 legal changes is **Planned** (R-22). A current date or a sourced historical
figure alone does not make the demo current or comprehensive.

**Planned:** England Universal Credit and the April uprating are the next-content
candidate, not an implemented corpus or a committed launch (R-46). Starting it requires
the owner's decision, UK point-in-time ingestion (R-19), currency/jurisdiction support
(R-21), and a qualified jurisdiction reviewer (R-34).

## Component stance and exclusions

Build the source layer, canonical core, verifier, rule/table approval gate, review
application, change report, independent parity and content pack. Maintain the
calculation service for self-hosted or synthetic-data use; freeze new investment.
Maintain the supported OpenFisca exporter with its AGPL note (R-28); freeze expansion.
Keep optional model authoring separate and frozen while the core product is completed.

Remove Catala, LegalRuleML, PROV export, Akoma Ntoso, OCR and a plugin SDK from the
active roadmap. Hosted multi-tenant SaaS and pre-hosted SOC 2, ISO 27001 or FedRAMP
work are excluded. General legal chat, precedent reasoning, subjective adjudication,
autonomous official determinations and automated authoritative publication are outside
this product's intended scope.

## Evidence and release criteria

A first usable version must close the P0 claim gaps and demonstrate current supported
content, explicit approval on deployed paths, and independent known-answer verification.
P1 work covers the report, pack, source coverage and operational hardening. Requirement
priority and status stay in `research/REQUIREMENTS.md` rather than competing checklists.

Measure mismatch counts on independent cases, source/test impact coverage, unknown
rates with reasons, and reproducibility of a dated pack. An independently annotated
public benchmark is **Planned** (R-42). No live extraction accuracy, reviewer time
saving, market adoption or legal compliance claim follows from the unit suite or the
simulated reviews.
