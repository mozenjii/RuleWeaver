# 09 — Implementation Roadmap

ADR-032 replaces the old expansion roadmap. Build a good self-hosted compiler/verifier
before sales deadlines. The intended deliverable is change impact plus independent
known-answer verification. Simulated reviews are hypotheses, not customer commitments.

`docs/10_BACKLOG.md` is the only requirement-status tracker. Read it before selecting
work; this document orders dependencies and states acceptance evidence, not completion.

## P0 — Restore and harden claims

The owner's requested order was R-37, R-05, R-06, R-25, R-36. R-25 is the documentation
prerequisite completed in this pass; R-39 is the newly exposed deployed-path gap.

| Order | Requirement | Acceptance evidence |
|---|---|---|
| 1 | R-37: current FY2027 tables | Retrieved official source, checksummed snapshot/rendering, per-value citations, before/on/after date tests, review of new values; never carry FY2026 forward |
| 2 | R-05: administrator-resistant audit | Key outside database, keyed verification, independent checkpoint export/verify and adversarial rewrite tests |
| 3 | R-06: distinct reviewer identity and separation | One identity per reviewer; author cannot approve own interpretation; rotation/revocation and negative tests |
| 4 | R-25: intended purpose/non-reliance | Revised ADR-021/022 with no compliance classification or unverified dates; counsel review still required before commercial use |
| 5 | R-36: nine-plus household increments | Source-specific rounded increment rules and threshold cases for supported household ranges and periods |
| 6 | R-39: deployed execution gate | Every deployed path validates and gates both rules/tables; draft CLI/library operation explicitly separated and labelled |

R-36/R-37 are promoted to P0 because the demo does not cover the claimed date/household
ranges. R-22 current-law audit remains necessary before describing the fixture as current
policy; current tables alone cannot prove current rules.

## P1 — The first usable deliverable

1. **R-16 change-impact report.** Build on existing package diff/dependency/scenario
   comparison. Add structural source changes, affected tests, dates/source links and a
   durable readable report. Expected cases must show both unchanged and moved outcomes.
2. **R-17 independent parity.** Accept the operator's own known-answer cases, preserve
   unknown/error states and output reproducible matches/mismatches tied to pack/date.
   OpenFisca-vs-native agreement is adapter consistency, not this exit criterion.
3. **R-38 content-pack artifact.** Bind immutable version/hash to source snapshots,
   rules, sourced tables, approval-log evidence, tests and verification results. R-43
   adds end-to-end lineage; R-23 adds portable JSON plus test vectors. A wheel is not a pack.
4. **Operational/review hardening:** R-07 qualification, R-10 unknown reasons and
   integrator disposition, R-11 pseudonymous IDs, R-13 SBOM/signing/pinning/scanning,
   R-29 accessibility. These are first-version evidence, not certification claims.
5. **Coverage and authoring boundaries:** R-18 structured HTML/PDF, R-19 UK point-in-time
   ingestion, R-21 currency/jurisdiction, R-22 current-law audit, R-26 optional authoring
   packaging/metadata, R-45 broader review. R-19/R-21 prepare for a possible UK corpus;
   they do not authorise starting R-46.

Review newly sourced figures through the same gate as rules. Keep independent intent
cases separate from boundary/mutation and adapter-derived cases. Do not silently resolve
missing sources or interpretation ambiguity to make a report pass.

## P2 — After evidence from use

R-20 EU sources, R-24 duty-register mode, R-27 local/EU-hosted authoring, R-30 paid EU
readiness, R-31 zero-access support protocol, R-40 extra proposal passes, R-41 extended
test tooling, R-42 independent public benchmark, R-44 richer validation/time, and R-46
England Universal Credit/April-uprating content require concrete scope and owner decisions.
Research references are not built features or legal conclusions.

R-32–R-35 are founder decisions: employer/IP permission, contracting/insurance,
qualified jurisdiction reviewer and backup maintainer. They are not coding tasks and this
roadmap does not assert any is complete. Counsel must review commercial intended use.

## Maintained and frozen

Keep tests and correctness/security maintenance for the self-hosted/synthetic calculation
service, OpenFisca supported export and optional model extraction. Do not expand them
instead of finishing the native report/parity/pack deliverable. No new target runtime is
required to make the core useful.

## Removed from the active roadmap

Catala, LegalRuleML, PROV export, Akoma Ntoso, OCR, plugin SDK, pre-user hosted multi-tenant
SaaS, and pre-hosted SOC 2/ISO 27001/FedRAMP work. Historical ADRs and references remain
history. Restoring scope requires an explicit owner decision and a demonstrated need.
