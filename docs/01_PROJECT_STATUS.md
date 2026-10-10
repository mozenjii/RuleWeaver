# 01 — Project Status

**Status date:** 2026-10-10  
**Phase:** the pipeline runs end to end — verified source, extraction, review gate,
deterministic evaluation, OpenFisca export

> **2026-08-17 review.** The spec pack was reviewed against verified external research.
> Architecture held; scope and three assumptions did not. See ADR-017 to ADR-022 in
> `11_DECISIONS.md`. Material changes:
>
> - **v0.1 rescoped** to a deterministic core (vocabulary + hand-encoded fixture + typed
>   IR + evaluator + validators + mutation harness). The former ten-point definition is
>   now v1.0.
> - **M0 was not closable as written** — its exit criteria depended on backlog items
>   scheduled after it. Resolved by ADR-017.
> - **Exception priority and temporal semantics are not open questions.** Worked answers
>   exist (prioritised defaults; multi-axis validity). Adopt, do not re-derive — ADR-020.
> - **Adapter plan reduced.** OpenFisca export is code generation, not serialization.
>   Catala and LegalRuleML are design references only — ADR-019.
> - **The human approval gate needs evidence it works.** Independent expert encoders agree
>   ~0% without a shared vocabulary, and automation bias degrades even expert review —
>   ADR-018, ADR-021.
> - **Deterministic runtime is now a legal position**, not only an engineering one —
>   ADR-022.

This file must stay brutally accurate. Do not mark an item complete because a placeholder, interface, or demo exists.

## Completed decisions

### Product

- [x] RuleWeaver chosen as the project.
- [x] Primary goal defined: compile natural-language rules into source-linked, testable, executable rule representations.
- [x] Primary public-interest wedge: tax and public-benefit rules.
- [x] Generic legal chatbot explicitly rejected.
- [x] Autonomous legal decision-making explicitly rejected.

### Architecture

- [x] Standards-first architecture approved.
- [x] Canonical RuleWeaver IR approved as the center of the system.
- [x] LLM used for semantic proposals, not final runtime evaluation.
- [x] Human approval required before executable use.
- [x] Ambiguity/abstention must be first-class.
- [x] Provenance must be first-class.
- [x] Tests are part of policy intent, not only code QA.
- [x] OpenFisca selected as first executable target.
- [x] Catala selected as a later high-assurance target.
- [x] LegalRuleML selected as an interchange target.
- [x] Akoma Ntoso selected as a legal-document interoperability target.
- [x] W3C PROV chosen as provenance-model inspiration/interop.

### Research completed enough to begin

- [x] OpenFisca architecture, variables, parameters, formulas, and YAML testing reviewed.
- [x] OpenFisca guidance to start with simple authoritative rules and reliable interpretations reviewed.
- [x] Catala's literate-programming and high-assurance approach reviewed.
- [x] Akoma Ntoso and LegalRuleML standards reviewed at architectural level.
- [x] W3C PROV reviewed at architectural level.
- [x] Georgetown/Beeck Center LLM-to-rules experiments reviewed.
- [x] Better Rules methodology and policy-intent test concept reviewed.
- [x] 2026 PROLEG legislation-to-executable-rules work reviewed.

## Implementation state

Checked items are built and covered by tests. Everything unchecked is genuinely absent.

### Foundation

- [x] Python package bootstrapped.
- [x] CI configured.
- [x] code quality tooling configured (ruff, mypy; both clean).
- [x] diagnostics framework defined.
- [x] serialization/version strategy implemented.

### Source model

- [x] source document object.
- [x] hierarchy/section model — reconstructed from CFR paragraph markers.
- [x] source spans.
- [x] source hashes — verified against the manifest on every load.
- [ ] cross-reference model.
- [x] effective-version model.

### Rule IR

- [x] production schema.
- [x] expression system.
- [x] entities and variables.
- [x] parameter model.
- [x] temporal semantics.
- [x] exceptions/priority semantics.
- [x] ambiguity representation.
- [x] interpretation/review state.
- [ ] provenance relation model.

### Runtime and verification

- [x] evaluator.
- [x] type checker — operand and assignment types, `RW2003`-`RW2008`.
- [x] reference resolver.
- [x] dependency graph.
- [x] cycle detection.
- [x] temporal validator.
- [ ] contradiction diagnostics.
- [ ] completeness diagnostics.
- [x] execution trace.

### Test generation

- [x] threshold boundary generator.
- [x] date-transition generator.
- [ ] exception generator.
- [ ] combinatorial case generator.
- [ ] property-based test framework.
- [x] approved human test fixture format.

### Ingestion/compiler

- [x] eCFR XML ingestion — 468 clauses, 0.9% with an uncertain position.
- [ ] PDF ingestion.
- [ ] Akoma Ntoso ingestion.
- [x] clause segmentation — six categories, only `computable` is extracted.
- [x] definition extraction — definitions are addressable by term.
- [ ] parameter extraction.
- [x] rule extraction — proposals are checked against the source and forced to
      `needs_review`.
- [ ] cross-reference linking.
- [x] ambiguity proposal — including injection findings escalated as blocking.
- [x] prompt/version registry — assets on disk, hashed into every run record.
- [x] provider-neutral model interface.

### Review

- [x] review decision model.
- [x] approval workflow.
- [x] source/rule side-by-side UI.
- [x] edit/reject/approve UX.
- [x] audit log.
- [x] authenticated reviewer identity — signed tokens or a trusted proxy; the
      application refuses to start with neither.
- [x] approval enforced at execution — the evaluator will not run unapproved rules.

### Adapters

- [x] OpenFisca mapping specification validated with examples — 13 of 15 fixture rules
      export; the guarded allotment and the overridden standard deduction are refused
      with a stated reason (ADR-031).
- [x] OpenFisca code generator — refuses unapproved rules; reports the four-state gap.
- [x] OpenFisca test exporter — households written as OpenFisca YAML tests with
      evaluator-derived expectations; `openfisca test` runs them in CI.
- [x] equivalence verified by running the generated package under OpenFisca —
      `adapters/openfisca/equivalence.py`, run in CI against openfisca-core 45. Every
      exported variable agrees across eight SNAP households; a planted float-rounding
      hazard is reported as a mismatch.
- [ ] LegalRuleML export — dropped, see ADR-019.
- [ ] Catala export — reference only, see ADR-019.

### Version change analysis

- [x] source version differ.
- [x] semantic rule differ.
- [x] downstream dependency impact analysis.
- [ ] affected test analysis.

### Benchmark

- [ ] corpus selected.
- [x] source licensing reviewed.
- [ ] annotation schema.
- [ ] gold rules.
- [ ] gold source links.
- [ ] gold tests.
- [ ] metrics implementation.
- [ ] reproducible benchmark runner.

## Immediate next milestone

**M0 — Executable IR without LLMs.**

Before building the AI compiler, create a tiny fictional benefit policy by hand and prove that RuleWeaver can represent, validate, execute, trace, and test it.

Exit criteria:

- at least 10 hand-authored rules;
- parameters that change by date;
- at least one exception;
- at least one dependency chain;
- source spans attached to every rule;
- deterministic evaluation;
- generated boundary tests;
- explicit `UNKNOWN` behavior;
- execution trace explaining which rule/parameter caused the result.

## Health indicators

Keep these up to date once implementation starts:

| Indicator | Current |
|---|---|
| Core package exists | Yes — `src/ruleweaver/{ir,runtime,verify,testgen,diff,ingest,compile,adapters,review}` |
| IR schema version | 0.1.0 |
| Source corpus | 3 sections, 468 clauses, sha256-verified on every load |
| Clause hierarchy certainty | 464/468 confident; 4 flagged (0.9%) |
| Golden policy corpora | 1 (SNAP, 15 rules from 7 CFR 271.2, 273.9 and 273.10) |
| Provenance verified against source | **16/16 spans resolve to verbatim clause text** |
| Deterministic rule features implemented | 12 expression nodes, exceptions, overrides, 4-state values, trace |
| Tests | 436 passing with every extra; 349 pass and 14 skip on the base install |
| Mutation score | **22/22 caught (100%)** |
| Lint / type check | ruff clean, mypy clean (50 files) — both enforced in CI |
| Deployable artefacts | Wheel, sdist, Docker image — all built and exercised in CI |
| CI | **Green** since 2026-10-10. It was red on every push from 2026-08-16 |
| Validators implemented | 41 distinct `RWxxxx` diagnostics across 6 families |
| Test generators | boundary + date transition |
| Amendment impact | semantic diff + dependency closure + outcome comparison |
| CLI | `validate`, `evaluate`, `boundaries`, `diff`, `ingest`, `extract`, `approvals`, `export`, `review`, `token`, `schema` |
| Model interface | Provider-neutral; Claude + GPT adapters; injection guard |
| LLM compiler passes implemented | **2 — segmentation and rule extraction** |
| Prompt assets | 2, versioned on disk and hashed into every run record |
| Approval enforced at execution | Yes — `ruleweaver evaluate --require-approval` |
| Reviewer identity | Signed tokens or trusted proxy; fails closed with neither |
| Review gate | Hash-chained append-only log, derived status, seeded-error catch rate |
| Review application | FastAPI + Jinja, one container; SQLite or PostgreSQL |
| Approved adapter targets | **1 built (OpenFisca, code generator), executed and compared** |
| External contributors | 0 |
| Public benchmark release | No |
| First external pilot | No |

### M0 exit criteria

| Criterion | State |
|---|---|
| At least 10 hand-authored rules | **Met** — 15 |
| Parameters that change by date | **Met** — dated `ParameterValue` intervals |
| At least one exception | **Met** — 2, both substitutive |
| At least one dependency chain | **Met** — gross income → deductions → net income → eligibility |
| Source spans attached to every rule | **Met** — all 15 cite a clause |
| Deterministic evaluation | **Met** — fixed-point evaluator, no model in the path |
| Generated boundary tests | **Met** — generator probes every threshold at x-1/x/x+1 |
| Explicit `UNKNOWN` behaviour | **Met** — propagates to the decision, raises on `__bool__` |
| Execution trace explaining the result | **Met** — records rule, target, scope, and base/exception/override |

**M0 is closed.** All nine criteria met.

The mutation harness is what makes that claim worth anything. Its first run scored 44%,
and each of the ten survivors was a real hole: the suite could not detect a deleted
"notwithstanding" override, could not distinguish conjunction from disjunction in the
final decision, and never exercised four floor guards. Those are now closed and the score
is 17/17.

### What ingestion found, 2026-08-20

Two things that were wrong the whole time and that nothing could have caught without the
source snapshots being parsed and checked:

**Fourteen of the fifteen rules quoted text that is not in the clause they cite.** The
quotes were paraphrases, truncations, and composites spliced across paragraphs with an
ellipsis. Every one now carries contiguous text lifted from the cited clause, `RW1001`
enforces it, and a test asserts all 16 spans resolve.

**Every recorded source digest failed on a Windows checkout.** `core.autocrlf` rewrote the
line endings of the snapshots, so the manifest could not verify against the files on disk.
`.gitattributes` now pins them. The check is what made a silent corruption visible, which
is the argument for running it on every load rather than trusting the checkout.

### What CI had been hiding, found 2026-10-10

**CI failed on every push from 2026-08-16 to 2026-10-10.** It installed only the dev
extra and six test modules needed the review extra, so collection failed and no test ran.
The 389 passing tests this file reported had not been run by CI in that time.

Underneath: `ruleweaver.approval`, the execution gate, imported FastAPI by way of
`review/__init__`. On the base install the README describes, `evaluate --require-approval`,
`export` and `token` all died on `ModuleNotFoundError`. A base-install CI job now catches
that class of mistake (ADR-030).

Pydantic 2.14 changed how it describes a decimal, and the published schema drifted with no
change to RuleWeaver. The decimal's schema is now pinned in the IR. The exact-match schema
test still fails under Pydantic 2.6, the declared floor, for unrelated emission
differences that predate this; it holds from 2.13.

### What running the OpenFisca export found, 2026-10-10

The generated package had never been executed. Run under openfisca-core 45 beside the
evaluator, it:

1. could not be loaded by OpenFisca's file loader (a relative import);
2. declared no input variables, so no household could be entered;
3. selected exceptions **highest** priority first — the spec says lowest wins, and the
   fixture has one exception per rule, so nothing could see it;
4. dropped the allotment's guard and computed a benefit amount for households that fail
   the income test;
5. emitted the overridden standard-deduction rule beside its override, as two classes
   with one name, correct only by file order;
6. applied every rule to months before it was law;
7. could not read any dimensioned table — the index helper was not vectorised;
8. could not index the fixture's sparse test tables at all, because OpenFisca requires a
   complete grid.

All eight are fixed or refused with a diagnostic, and pinned by tests. A blank income is
read by OpenFisca as no income and makes a household **eligible** — `RW8001` now says the
gap can approve as well as deny.

### Open findings — need a decision

- **The allotment is not exported.** OpenFisca cannot represent "no value" for an
  ineligible household. Exporting it as zero would be the `RW8001` gap applied to the
  benefit amount itself; that is a policy call (ADR-031).
- **Rounding up after binary-float arithmetic can be a dollar off.** 100 × 0.07 rounds up
  to 8 in OpenFisca and 7 in the evaluator. The SNAP gross limit has that shape and does
  not trip it for any of the 1,000 poverty-line values that make it a whole dollar, but
  nothing in the adapter prevents it in general.

### Resolved since

- **`--partial` ignored an unapproved "notwithstanding" clause** and gave the baseline
  household a standard deduction of 180, below the 204 minimum. An approved rule that an
  unapproved rule overrides is now withheld, and its value is unknown.

### Deployment, 2026-10-10

- Docker image for the reviewer application: installs the built wheel, runs as a
  non-root user, keeps the audit log on a `/data` volume, health-checks `GET /healthz`,
  and refuses to start without an identity provider. CI builds and runs it.
- PostgreSQL driver through the `postgres` extra; the database password is masked in
  startup output.
- Tag-driven releases publish the wheel, sdist and image (`.github/workflows/release.yml`).
- OpenFisca YAML tests generated from the evaluator and run with `openfisca test`.

### Next milestone

Source ingestion beyond eCFR — plain text, HTML and PDF. Today RuleWeaver can only read
US federal regulations in eCFR XML, which limits who can use it more than anything else.

## Known risks already identified

1. Treating ambiguous law as deterministic logic.
2. Generating plausible but wrong cross-references.
3. Losing the distinction between source text and an interpretation.
4. Under-specifying temporal semantics.
5. Building an IR around one country's benefit vocabulary.
6. Overfitting to OpenFisca and losing target neutrality.
7. Generating tests that simply mirror the generated rule instead of independent policy intent.
8. Hiding errors behind model confidence.
9. Expanding to high-discretion legal domains too early.
10. Spending too much time on UI before compiler semantics are stable.
