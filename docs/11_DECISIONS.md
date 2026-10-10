# 11 — Architecture Decision Log

Use this as a lightweight ADR register. Never rewrite old accepted decisions invisibly; append superseding decisions.

## ADR-001 — Standards-first compiler architecture

**Status:** Accepted  
**Date:** 2026-08-16

### Decision

Build RuleWeaver around a canonical intermediate representation and adapters rather than generating target-specific code directly from an LLM.

### Why

- auditable;
- testable;
- provider-neutral;
- reduces arbitrary-code risk;
- enables multiple target runtimes;
- creates a durable OSS asset beyond prompts/models.

## ADR-002 — v0.1 domain is tax/public benefits

**Status:** Accepted

### Decision

Start with explicit computable rules: eligibility, thresholds, parameters, dates, calculations, and explicit exceptions.

### Rejected alternative

“Support any law from day one.”

### Why

Open-textured legal reasoning would force immature semantics and unsafe demonstrations.

## ADR-003 — LLM outside the runtime decision path

**Status:** Accepted

### Decision

LLMs create semantic proposals. Approved rules execute deterministically.

### Why

Reproducibility, auditability, safety, differential testing.

## ADR-004 — Human approval required

**Status:** Accepted

### Decision

A model-proposed rule cannot enter an approved executable package solely based on model confidence or validator success.

### Why

Policy-to-code experiments and existing rules-as-code practice emphasize human interpretation/oversight for complex rules.

## ADR-005 — Ambiguity is first-class

**Status:** Accepted

### Decision

Represent uncertainty as structured ambiguity/unknown/human-judgment states instead of forcing a single interpretation.

## ADR-006 — Provenance is mandatory

**Status:** Accepted

### Decision

Material semantic objects require source provenance and transformation/review provenance.

### Interop direction

W3C PROV concepts may be used for export/mapping.

## ADR-007 — Build a native reference evaluator

**Status:** Accepted

### Decision

Implement a small deterministic evaluator for the canonical IR even though OpenFisca will be the first target adapter.

### Why

- avoids target lock-in;
- establishes reference semantics;
- enables differential adapter testing.

## ADR-008 — OpenFisca first adapter

**Status:** Accepted

### Decision

OpenFisca is the first executable external target because its entities, variables, parameters, periods, formulas, and tests closely match the initial tax/benefit scope.

## ADR-009 — Catala is later, not core dependency

**Status:** Accepted — superseded in part by ADR-019 (target downgraded to reference-only)

### Decision

Use Catala as a later high-assurance interoperability target and design reference. Do not require it for v0.1.

## ADR-010 — Akoma Ntoso for legal document interop

**Status:** Accepted

### Decision

Preserve/use Akoma Ntoso structure and identifiers when supplied. Do not turn the Rule IR into a duplicate legal-document markup standard.

## ADR-011 — LegalRuleML is an interchange target, not the v0.1 IR

**Status:** Accepted — superseded in part by ADR-019 (export target dropped; spec retained as design reference)

### Decision

Use a smaller developer-friendly canonical IR for the first domain, with later LegalRuleML export for supported semantics.

### Why

LegalRuleML is semantically rich; implementing all of it would dramatically expand v0.1.

## ADR-012 — Policy-intent and generated tests are separate

**Status:** Accepted

### Decision

Never let generated tests masquerade as independent validation of the generated rule.

Track test provenance.

## ADR-013 — Parameters over hard-coded legislative numbers

**Status:** Accepted

### Decision

Values that change through legislation/time should normally be represented as dated parameters rather than embedded numeric literals in formulas.

## ADR-014 — Dates use explicit interval semantics

**Status:** Accepted in principle; exact implementation to finalize during M0.

### Decision

Every effective interval must have documented inclusive/exclusive semantics. No implicit host-language date behavior.

## ADR-015 — Start local/simple infrastructure

**Status:** Accepted

### Decision

Filesystem + SQLite is acceptable for early development. PostgreSQL/multi-user infrastructure comes later.

### Why

Compiler semantics are the current risk, not web scale.

## ADR-016 — Provider-neutral model interface

**Status:** Accepted

### Decision

Core compiler APIs may not depend on one proprietary model/provider.

## ADR-017 — v0.1 is redefined as a deterministic core, not the full roadmap

**Status:** Accepted
**Date:** 2026-08-17

### Decision

`v0.1` now means **Phase A (controlled vocabulary + hand-encoded fixture) plus Phase B
(typed IR, deterministic evaluator, validators, boundary tests, mutation harness)**. The
previous ten-point definition in `README.md` becomes `v1.0`.

### Why

The former `v0.1` required OpenFisca export, semantic diff and a public benchmark —
Phases 5-7 of the roadmap, realistically 3-6 person-years. No smaller release was defined
anywhere, which is how projects with good architecture never ship.

### Also resolves

M0 could not close as written. Its P0 fixture required an exception
(`10_BACKLOG.md:92`) built on IR exception types (`:45`) and evaluator exception support
(`:55`), both scheduled P1. Phase 0's exit criterion required "one entity relationship"
(`09_IMPLEMENTATION_ROADMAP.md:28`) while `04_RULE_IR_SPEC.md:375` listed that model as an
open question M0 was meant to decide. Phase A settles those questions before Phase B
depends on them.

---

## ADR-018 — Controlled vocabulary precedes extraction

**Status:** Accepted
**Date:** 2026-08-17

### Decision

No clause is encoded — by hand or by model — until the defined terms for that source are
extracted into an explicit vocabulary document. Approval of a rule is only meaningful
relative to an agreed vocabulary.

### Why

Empirical. In *Encoding legislation* (Artif Intell Law, DOI 10.1007/s10506-023-09350-1),
three experienced coders independently encoded the Australian Copyright Act 1968 and
reached **0% exact and 3% semantic agreement on rules**. After agreeing shared terms,
agreement rose to 10-30% exact and 26-53% semantic.

Qualified experts do not converge on one correct encoding. Without a fixed vocabulary,
"approve or reject this rule" is not a well-posed question, and ADR-004's human approval
gate rests on nothing.

### Consequence

Adds `docs/15_VOCABULARY.md` as a required artifact per corpus. Blocks Phase A step 2.

---

## ADR-019 — Adapter strategy revised: OpenFisca is code generation; Catala and LegalRuleML are references

**Status:** Accepted
**Date:** 2026-08-17
**Supersedes in part:** ADR-009, ADR-011

### Decision

1. **OpenFisca** remains the first and only v1.0 executable target, but the adapter is a
   **code generator**, not a serializer.
2. **Catala** is downgraded from "later target" to **design reference only**.
3. **LegalRuleML export is dropped.** Its specification is retained as the design
   reference for temporal and defeasible semantics.

### Why

- OpenFisca rules are Python `Variable` subclasses whose `formula(entity, period,
  parameters)` bodies are arbitrary vectorised NumPy. There is no declarative rule-
  authoring API. Only *parameters* are YAML — a genuine serialization target. The IR must
  therefore carry enough computational structure to lower into vectorised formulas, or
  under-expressiveness surfaces as ungeneratable code rather than lossy output.
- Catala is literate programming authored by a lawyer-programmer pair; its value is the
  human-audited law↔code correspondence. Machine-generated Catala discards exactly that
  property, so emitting it is technically possible and largely pointless.
- LegalRuleML tooling is dormant — `oasis-tcs/legalruleml` last commit July 2020, tool
  development explicitly out of scope for the TC, all four Statements of Use academic. An
  adapter with no consumer cannot be validated and is unfalsifiable weight.

### Note on the three-target premise

The targets have incompatible semantic cores — OpenFisca's imperative dated vectors,
Catala's prioritised-default logic, LegalRuleML's deontic ontology. An IR expressive
enough for all three is either lowest-common-denominator or three bespoke lowerings.
Target neutrality (ADR-007) is preserved by the native evaluator, not by shipping adapters.

---

## ADR-020 — Exception priority and temporal semantics are adopted, not invented

**Status:** Accepted
**Date:** 2026-08-17

### Decision

- **Exception precedence** adopts Catala's prioritised-default model: a base case plus
  exceptions with declared precedence.
- **Temporal semantics** adopts LegalRuleML Core's multi-axis model — assertion time,
  validity, efficacy, enforcement — rather than the current single `effective` interval.
- Exception effects gain **`substitute`** alongside `disable_base_rule`.

### Why

`04_RULE_IR_SPEC.md:374-381` files exception priority and period algebra as open questions
to settle during M0/M1. Both have published worked answers; re-deriving them is wasted
effort and will land somewhere worse.

`disable_base_rule` alone cannot express the dominant legal form — *"except that for a
household with an elderly member, the limit is $X."* Encoding substitution as
disable-plus-shadow-rule duplicates the condition, severs the source correspondence
required by `README.md:36`, and breaks amendment impact analysis, because amending the
exception clause no longer touches the rule that implements it.

Single-axis time cannot express a provision enacted mid-2026 that applies to tax years
beginning after 31 December 2025, nor recomputation of a past determination under the
rules as they stood. For a system whose promise is audit, that is disqualifying.

---

## ADR-021 — Review produces evidence, not a compliance conclusion

**Status:** Accepted position; revised for R-25 on 2026-10-10.
**Original decision date:** 2026-08-17. The prior compliance-evidence claim is withdrawn.

### Intended purpose

Review helps an operator inspect an executable interpretation against the exact source
and published figures. A recorded approval means that the deployment's log records a
person's decision against that content hash. It does not establish legal correctness,
reviewer qualification, independent identity or regulatory compliance.

### Decision and implementation boundary

- **Built:** disclosed fault planting and aggregate catch-rate metrics in
  `src/ruleweaver/review/seeding.py` and `src/ruleweaver/review/adversarial.py`, covered
  by `tests/test_seeding.py`. Seed decisions cannot approve the real rule. A measured
  catch rate is evidence about the planted sample, not assurance about all interpretations.
- **Partial:** signed sessions/trusted proxies and a hash-chained decision log exist
  (`tests/test_identity.py`, `tests/test_review_store.py`). The shared signing secret
  does not bind one identity to one reviewer (R-06). The unkeyed chain can be recomputed
  by a database administrator (R-05).
- **Planned:** author/approver separation (R-06), qualification (R-07), pseudonymous
  identities with a deletable map (R-11), accessible review (R-29), and complete test/
  ambiguity review with blind dual-encoding where required (R-45).

Human approval and deterministic checks are complementary controls. Neither a fast
approval nor a high model-confidence score establishes that a rule is right. Operators
must retain independent policy-intent cases and decide what expertise their content needs.

### Non-reliance and review trigger

RuleWeaver supplies technical evidence, not official determinations or legal advice.
No review metric or approval record is offered as proof of compliance with any statute,
regulatory article or certification. Obligations depend on actual intended purpose,
operator, jurisdiction and deployment. **Not legal advice; needs counsel review before
any commercial use.** Revisit this position when a concrete deployment, qualified
reviewer process and counsel-reviewed governance model exist.

---

## ADR-022 — Deterministic runtime and separate optional authoring

**Status:** Accepted position; revised for R-25 on 2026-10-10.
**Original decision date:** 2026-08-17. **Reinforces:** ADR-003.
The former legal-classification conclusion and unverified legislative timetable are
withdrawn; this revision makes no claim about exemption or statutory dates.

### Intended purpose

RuleWeaver is a self-hosted compiler and verifier for computable benefit and tax rules.
It preserves source evidence and supports human-controlled interpretations. Its target
outputs are change-impact and independent known-answer verification evidence for an
operator's own system, not an autonomous benefit or tax authority.

### Decision and implementation boundary

The runtime executes supported typed expressions deterministically. Optional model
providers may propose interpretations before review; they are absent from the runtime
path and are optional packaging dependencies (`pyproject.toml`,
`tests/test_optional_extras.py`, `src/ruleweaver/runtime/evaluator.py`).
This separation is an engineering and governance position, not a legal classification.

Only approved rules and parameter tables should enter deployed execution. That is
**Partial** today: the service gates every request and export gates by default; CLI
`evaluate` needs `--require-approval`, and the low-level evaluator does not consult an
approval log (`src/ruleweaver/approval.py`, `tests/test_parameter_gate.py`,
`tests/test_service.py`). R-39 covers the remaining deployed-path enforcement.

### Non-reliance

Outputs implement a bounded reviewed interpretation. They are not law, legal advice,
an official determination, an assurance of current source completeness or permission
to automate consequential decisions. Approval and disclaimers do not replace the
operator's independent validation and accountability. Unknown values must remain
unresolved and be handled by the operator, not converted into denials or approvals.

No inference about regulatory classification follows solely from deterministic
execution or optional authoring. **Not legal advice; needs counsel review before any
commercial use.** Counsel must review the actual purpose, data flows and downstream use.
No compliance deadline or exemption is asserted here.

---

## ADR-023 — Apache-2.0 for code; source law is public domain

**Status:** Accepted
**Date:** 2026-08-17

### Decision

Project code is licensed **Apache-2.0**. The SNAP source snapshots under
`examples/snap/sources/` are US federal regulations and carry no copyright.

### Why Apache rather than MIT

The project's stated aim is that other systems adopt its IR and interfaces. Apache-2.0
carries an explicit patent grant and a defensive termination clause; MIT does not. For a
format intended as shared infrastructure, contributors and adopters both benefit from
that grant being explicit rather than implied.

### Source text

US federal regulations are not subject to copyright under the government edicts doctrine,
so the snapshots are redistributable and the fixture reproduces offline without a fragile
URL fetch. `examples/snap/sources/manifest.json` records the basis alongside each hash.

**This does not generalise.** UK and Canadian legislation is Crown copyright, EU material
falls under the Open Data Directive, and agency benefit manuals frequently state no status
at all. Any future corpus needs its own rights review before redistribution — the
manifest has a `rights` block for exactly that.

### Reversible

No external contributions have been accepted yet, so this can still be changed without
relicensing anyone else's work. After the first outside contribution it cannot.

---

## ADR-024 — Approval is enforced at execution, not documented

**Status:** accepted (2026-08-20)

README principle 4 — "no extracted rule is executable in an approved package until it
passes review" — was true of the documentation and false of the code. The evaluator ran
whatever package it was handed. Review recorded decisions; nothing consulted them.

`src/ruleweaver/approval.py` is the enforcement. `ruleweaver evaluate --require-approval`
reads the log and refuses; the OpenFisca adapter refuses by default. **2026-10-10
clarification:** draft export can bypass approval with `--no-approval`; CLI evaluation
without `--require-approval` and direct evaluator calls are also ungated. The service
always applies `approved_subset`. R-39 tracks separation and enforcement of deployed
paths. Parameter tables now pass the same gate (`tests/test_parameter_gate.py`).

### Excluding a rule leaves its target unknown, not false

A filtered package is still a valid package. Rules that survive reference variables the
excluded rules would have assigned, and those evaluate to `unknown` and propagate. "This
determination rests on a rule nobody has approved" and "this household does not qualify"
are different claims, and conflating them is the specific failure this project exists to
avoid.

### Why not a flag on the rule

Status is derived from the log and embedded-span hashes. Editing the rule, table value
or cited span makes approval stale. **2026-10-10 clarification:** changing source snapshot
bytes alone does not update those hashes; complete verified source-version binding is
not built (R-43). Do not claim re-fetching alone revokes an approval.

---

## ADR-025 — Ingestion verifies digests on every load, and the check is not optional

**Status:** accepted (2026-08-20)

`load_corpus` checks each snapshot against the sha256 in the manifest before parsing it.
Failure raises. There is a `verify=False` for the case of deliberately replacing a
snapshot, and a corpus loaded that way is marked so nothing downstream mistakes it for a
verified one.

### Justified on its first run

With `core.autocrlf` enabled — the Windows default — git rewrote the line endings of every
snapshot on checkout, and every recorded digest failed. Nothing else would have noticed:
the XML still parsed, the rules still evaluated, and the provenance chain the project rests
on was quietly broken in a way that depended on each contributor's git configuration.

`.gitattributes` now pins `examples/snap/sources/*.xml` as binary. The check is what made
the corruption visible, which is the argument for running it every time rather than
trusting the checkout.

---

## ADR-026 — A quote must be contiguous text from the clause it cites

**Status:** accepted (2026-08-20)

Every `SourceSpan.quote` must appear, whitespace-normalised, inside the cited clause or its
subtree. `RW1001` enforces it whenever a corpus is available.

### What this rejects

Paraphrase, truncation that changes meaning, and composites joined with an ellipsis. All
three read as quotations and none of them can be checked. When ingestion was first pointed
at the fixture, **fourteen of the fifteen hand-encoded rules failed** — and the failures
were not sloppiness. They were the natural result of writing a quote from memory of what a
clause said rather than from the clause.

### Whitespace is normalised, nothing else

A quote transcribed from a rendered page differs from the source in line breaks and runs of
spaces. Failing on that would train reviewers to ignore the check, which is worse than the
laxity. Any other difference is a failure.

### A citation covers its subtree

"7 CFR 273.9(d)" names a subsection, not a paragraph. Quoting a child of the clause you
cite is normal legal practice, so resolution checks the clause and everything nested under
it.

---

## ADR-027 — The extraction pass is bounded by checks, not by prompt wording

**Status:** accepted (2026-08-20)

Six checks run on every proposal, in `compile/extract.py`, and none can be disabled: the
output must parse as IR; the rule must cite the clause it was shown; every quote must
resolve against the verified source; `interpretation.status` is overwritten to
`needs_review`; `model_confidence` is recorded and never branched on; and injection
findings escalate to a blocking ambiguity.

### Why the prompt is not the control

The prompt says the model may not mark its own work approved. That instruction is worth
having — it shapes the output and documents the intent — but a model can decline to follow
it, and a prompt edit can drop it without any test failing. The status is therefore
overwritten in code. A test asserts both: that the code forces the status, and that the
sentence is still in the prompt.

### A rejected proposal still comes back

Carrying its diagnostics. A reviewer needs to see what the model produced *and* why it was
refused. Returning nothing teaches them nothing and hides a systematic failure behind an
empty queue.

### Injection findings are escalated, never dropped

Modelled as a blocking ambiguity so they inherit behaviour that already exists: they block
approval, they appear beside the rule, and a person has to resolve them. Silently
discarding a flagged proposal would hide the attempt from the only party who can act on it.

---

## ADR-028 — Reviewer identity fails closed

**Status:** accepted (2026-08-20)

The reviewer application resolves identity from an HMAC-signed session token, or from a
header set by an authenticating proxy on a trusted-peer list. With neither configured it
raises `IdentityNotConfigured` and does not start.

### What changed

The previous default trusted an `X-Reviewer` header and emitted a `RuntimeWarning`. A
deployment that forgot to wire up identity still started, still served, and still recorded
approvals — against whatever name the client sent. The only signal was a warning in a log
nobody reads.

### Why an audit log with a forgeable actor is worse than none

A client-controlled actor field cannot identify who made a review decision. This is
an evidence-integrity concern, not a legal defence. ADR-021/022 were revised on
2026-10-10 to withdraw compliance conclusions. Distinct reviewer identity, separation
of duties and pseudonymous records remain unbuilt (R-06, R-11).

### Trusted-proxy support is deliberate

Most real deployments authenticate at an SSO gateway. Refusing to support that pattern
would push operators back to the insecure resolver, so it is supported — with a mandatory
list of peers the application will believe, because a header is trustworthy exactly when
nothing else can reach the port.

---

## ADR-029 — The OpenFisca adapter reports the four-state gap rather than absorbing it

**Status:** accepted (2026-08-20)

OpenFisca has no unknown. Every variable has a type default, so a fact nobody supplied is
indistinguishable from a fact that is genuinely zero. The IR spends its whole design
refusing that conflation.

The gap is not repairable inside the adapter, so every export emits `RW8001` and the
generated module repeats the warning at the top of the file.

### Why not silently approximate

An adapter that dropped four-state semantics quietly would produce a model that denies
benefits for missing paperwork while claiming to implement the same rules. That is the
exact harm the four-state evaluator exists to prevent, arriving through the one path nobody
is watching.

### Exceptions do lower faithfully

A substitutive exception becomes `np.select` over the conditions in descending priority,
with the base expression as the default. The IR already requires distinct priorities, so
the order is total and the selection is decidable. `disable_base_rule` does not lower: it
says the rule produces *nothing*, and OpenFisca would render that as a zero.

### The export is unverified

Generated, parses, every variable carries its citation — and never executed. Running it
under OpenFisca and comparing against the deterministic evaluator is the evidence that
would make this a claim about behaviour. Until then it is a claim about structure, and
`docs/01_PROJECT_STATUS.md` says so.

---

## ADR-030 — The base install is a tested deployment

**Status:** accepted (2026-10-10)

A deployment that only executes approved rules installs neither the model SDKs nor the web
stack. Packaging already said so; nothing tested it. For three weeks the execution gate
imported FastAPI through `review/__init__`, and CI — which installed the base package and
then failed at collection — never ran a test that would have shown it.

### Decision

- CI has two jobs. The matrix installs every extra and runs everything, plus ruff and mypy.
  The second installs the base package alone and runs the suite there.
- Tests that need an extra skip with a reason when it is absent. Tests that check the core
  without an extra block the extra's imports in a subprocess, so they hold on machines
  where it is installed.
- An extra's import is deferred to the code that needs it. `identity` imports FastAPI only
  to build an HTTP refusal.
- The published schema's shape for a decimal is declared in the IR, not inherited from
  whichever Pydantic is installed.

---

## ADR-031 — The OpenFisca export is executed, and what cannot be faithful is refused

**Status:** accepted (2026-10-10). **Supersedes** the exception-order sentence of ADR-029.

ADR-029 said a substitutive exception "becomes `np.select` over the conditions in
descending priority". That inverted the IR: `04_RULE_IR_SPEC.md` says the
**lowest-numbered** matching exception wins, and the evaluator does that. The cases are now
ascending. The fixture has one exception per rule, so no structural test and no SNAP
scenario could see the difference; a synthetic two-exception case now does.

### Decision

1. **The export is run, not only parsed.** `equivalence.compare` evaluates a household with
   the evaluator and with the generated package under OpenFisca, and gives each exported
   variable one of three verdicts: match, mismatch, or gap. A gap is the evaluator saying
   unknown where OpenFisca produced a number — the `RW8001` case. It is reported apart from
   matches so it can never be counted as agreement.
2. **A guarded rule is refused**, for the same reason as `disable_base_rule`. When its guard
   does not hold, the rule assigns nothing; OpenFisca would show the type default. The
   guard used to be dropped, so the allotment was computed for ineligible households.
   This leaves the allotment out of the export until someone decides that zero is an
   acceptable rendering of "not eligible, so no allotment" — a policy call, not an
   adapter one.
3. **An overridden rule is subsumed** by the rule overriding it, as in the evaluator.
4. **Formulas are dated** from `effective_from`; `effective_to` becomes OpenFisca's
   inclusive `end`, one day earlier.
5. **New refusals**: a rule needing a variable that is not exported (transitively), a
   second formula for one variable, two ids that become one OpenFisca name (`RW8006`), and
   a dimensioned table that is not a complete grid (`RW8007`). OpenFisca cannot index a
   sparse table, and filling the gaps would be inventing policy.
6. **Comparison happens on the first of a month.** OpenFisca reads parameters at the start
   of the period and the evaluator on the day; comparing mid-month would blame the adapter
   for a mid-month parameter change.

### Known limit

OpenFisca computes money in binary floats. Rounding up after float arithmetic can be off
by a whole unit: 100 × 0.07 rounds up to 8, not 7. The harness reports this — a planted
case proves it — but the adapter does not prevent it.

---

## ADR-032 — Build the self-hosted compiler and verification deliverable first

**Status:** Accepted owner's plan (2026-10-10).
**Supersedes:** active expansion plans in ADR-006/009/010/011/019 and the previous
sales-deadline roadmap. Historical design references remain; no code is removed.

### Context

The three private simulated review rounds raised useful
objections, but consulted no real customer, reviewer or counsel. Their preferences,
prices and deadlines are hypotheses, not evidence of demand. Several earlier product
claims outran the code. The owner chooses a good first version before commercial urgency.

### Decision

Build a compiler and verifier for benefit and tax rules, linking executable
interpretations and published figures to source evidence. Humans approve rules and
parameter tables; deterministic software validates and runs them. Model authoring is
optional, separate and frozen for new investment.

The valued deliverable is **change impact plus independent verification**: effects of
legislative change or annual uprating on rules, tests and results, paired with parity
against the operator's own known-answer cases. Native package diff/impact is **Partial**
(R-16); independent parity and a versioned hashed content-pack artifact are **Planned**
(R-17, R-38). Adapter-versus-evaluator agreement cannot substitute for an independent oracle.

Deployment is self-hosted. The intended support practice gives builders/supporters no
personal-data access; self-hosting alone does not enforce that. The zero-access support
protocol remains **Planned** (R-31). The product is not a hosted SaaS or an autonomous
benefit/tax authority.

US SNAP federal rules and the official FY2026 tables for the 48 states/DC remain the
reference demo (`examples/snap/rules.json`, `tests/test_snap_tables.py`). FY2027 tables,
large-household increments and current-law coverage are not built (R-37, R-36, R-22).
England Universal Credit core plus the April uprating is the leading next-content
candidate, **Planned** (R-46), subject to the owner's decision, not started work.

### Component stance

- **BUILD:** verified sources (eCFR plus memos/notices; structured HTML/PDF R-18,
  legislation.gov.uk R-19), typed IR, deterministic evaluator/verifier, approval of
  rules and tables, review app, change report R-16, parity R-17, content pack R-38.
- **HARDEN:** keyed audit/checkpoints R-05, per-reviewer identity/separation R-06,
  qualification R-07, unknown reasons/disposition R-10, pseudonyms R-11, supply-chain
  evidence R-13, accessibility R-29, universal deployed gate R-39.
- **FREEZE:** calculation service for self-hosted/synthetic use, OpenFisca export
  (maintain only, dependency licence note R-28), optional extraction. Preserve working
  tests; frozen modules receive correctness/security maintenance, not feature expansion.
- **CUT from active roadmap:** Catala, LegalRuleML, PROV export, Akoma Ntoso, OCR,
  plugin SDK and pre-user hosted multi-tenant SaaS. SOC 2, ISO 27001 and FedRAMP work
  wait for an actual hosted offering and its demonstrated requirements.

### Consequences and acceptance evidence

Requirement status lives only in `docs/10_BACKLOG.md`. Architecture and product
pages label components Built / Partial / Planned with paths/tests or requirement IDs.
Complete P0 content and gate hardening before polishing the report/parity/pack deliverable.
A software wheel, container or hash field is not a content-pack release. A review log
is not a qualified sign-off. A green synthetic suite is not policy authority or a market.

R-25 completes the documentation posture in ADR-021/022; counsel review before commercial
use remains mandatory. This ADR creates no release, tag, PR, hosted deployment or paid work.

### What would change the decision

Reconsider scope only with the owner's explicit decision supported by actual user needs,
independent parity evidence, jurisdiction-specific qualified review and deployment/privacy
requirements. Do not infer market validation from further simulated agreement. Starting
UC, expanding beyond this domain or reopening frozen components needs that decision.

---

## Pending ADRs

- Money currency and multiple jurisdictions (R-21).
- Multi-axis temporal semantics and validator/spec contradictions (R-44). ADR-020's
  multi-axis aspiration is not built: current rules/values have effective intervals.
- Content-pack release contract and durable provenance (R-38, R-43).
- Deployed versus draft execution boundary (R-39).
- Human-required predicates if a concrete computable-policy case requires them;
  subjective adjudication remains outside the current scope.

Aggregation, explicit rounding and lowest-numbered exception priority are already
specified and implemented in the supported subset. Do not reopen them as unresolved
foundations. Cut adapter/plugin plans do not belong in this pending queue.
