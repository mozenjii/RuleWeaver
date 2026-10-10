# 13 — Repository Structure

This maps the actual tracked tree on 2026-10-10, not a proposed skeleton. Directory
listings below are selective; the named paths exist. Local tooling, runtime databases,
virtual environments and caches are not project deliverables.

```text
RuleWeaver/
├── README.md
├── CHANGELOG.md
├── LICENSE
├── SECURITY.md
├── Dockerfile
├── .dockerignore
├── .gitattributes
├── .gitignore
├── pyproject.toml
├── .github/workflows/
│   ├── tests.yml
│   └── release.yml
├── docs/                         numbered specifications, decisions and evidence
├── research/
│   ├── README.md                 simulated-review caveats
│   ├── REQUIREMENTS.md           single requirement-status tracker
│   └── simulated-reviews/
│       ├── 00-verified-facts.md   historical findings, some since repaired
│       ├── round-1/
│       ├── round-2/
│       └── round-3/
├── memory/
│   ├── WORKING_MEMORY.md         shared temporary handoff
│   └── LOCAL_SESSION_PROMPT.md   historical task instructions
├── schemas/
│   └── ruleweaver-0.1.schema.json
├── examples/snap/
│   ├── rules.json
│   ├── scenarios/baseline.json
│   ├── amendments/earned-deduction-25pct.json
│   └── sources/
│       ├── manifest.json
│       ├── 7cfr-271.2.xml
│       ├── 7cfr-273.9.xml
│       ├── 7cfr-273.10.xml
│       ├── fns-snap-cola-fy2026.pdf
│       ├── fns-snap-cola-fy2026.txt
│       └── hhs-poverty-guidelines-2025.htm
├── src/ruleweaver/
│   ├── __init__.py
│   ├── __main__.py
│   ├── cli.py
│   ├── approval.py
│   ├── hashing.py
│   ├── ir/
│   │   ├── expressions.py
│   │   └── rules.py
│   ├── runtime/
│   │   ├── evaluator.py
│   │   └── values.py
│   ├── verify/
│   │   ├── diagnostics.py
│   │   ├── types.py
│   │   └── validators.py
│   ├── testgen/
│   │   ├── boundaries.py
│   │   ├── dates.py
│   │   └── mutation.py
│   ├── ingest/
│   │   ├── corpus.py
│   │   ├── document.py
│   │   ├── ecfr.py
│   │   ├── markers.py
│   │   └── plain.py
│   ├── compile/
│   │   ├── pipeline.py
│   │   ├── segment.py
│   │   ├── extract.py
│   │   ├── providers.py
│   │   ├── schemas.py
│   │   ├── prompts.py
│   │   └── prompts/
│   │       ├── segment.v1.md
│   │       └── extract-rule.v1.md
│   ├── models/
│   │   ├── base.py
│   │   ├── guard.py
│   │   └── providers.py
│   ├── review/
│   │   ├── app.py
│   │   ├── identity.py
│   │   ├── decisions.py
│   │   ├── store.py
│   │   ├── adversarial.py
│   │   ├── seeding.py
│   │   └── templates/
│   ├── service/
│   │   ├── api.py
│   │   └── keys.py
│   ├── diff/
│   │   ├── semantic.py
│   │   └── impact.py
│   └── adapters/openfisca/
│       ├── lowering.py
│       ├── codegen.py
│       ├── equivalence.py
│       └── yaml_tests.py
└── tests/                        flat test modules, not unit/golden subdirectories
```

## Module ownership and implementation stance

**Built** supported semantics live in `ir/`, `runtime/`, `verify/`, `testgen/` and
`ingest/`; their limits are mapped in `docs/03_ARCHITECTURE.md`. Source facts stay in
`ingest/`; interpretation stays in the typed IR. Approval policy is in `approval.py`,
independent of the HTTP presentation. The low-level runtime does not read a review log.

**Partial** complete review and provenance live across `review/`, `compile/` and the
source/gate modules (R-05/R-06/R-07/R-11/R-29/R-43/R-45). `review/seeding.py` wires queue
faults; it is not merely an unused adversarial helper. `ingest/plain.py` verifies one
canonical memo/notice text, including pinned PDF rendering; structured clauses remain
R-18. `diff/` owns package changes and scenario impact, not structural source diff R-16.

**Built, frozen:** `service/` is a calculation service, not an unbuilt top-level `api/`;
`adapters/openfisca/` is maintained subset export; `compile/`/`models/` provide optional
proposals. No top-level `compiler/`, `web/`, `benchmark/` or plugin SDK is implemented.

**Planned:** pack release R-38, user parity R-17, unified provenance R-43 and independently
annotated benchmark R-42. No placeholder directory is introduced for them by this pass.
The wheel/image release workflow is software packaging, not a released content pack.

## Proof entry points

`tests/test_snap_tables.py` checks figures against pinned sources and tests expiry and
size-nine unknown. `tests/test_parameter_gate.py` covers sourced/datable table approvals.
`tests/test_seeding.py`, `test_review_app.py`, `test_identity.py`, `test_review_store.py`
cover review behavior and its limits. `tests/test_service.py` covers HTTP gating/records.
`tests/test_openfisca_equivalence.py` checks adapter consistency, not independent policy
truth. `tests/test_optional_extras.py` guards the provider-free base deployment.

Keep the tree factual. New project behavior belongs in the existing docs and requirement
tracker; do not publish machine-local configuration as documentation.
