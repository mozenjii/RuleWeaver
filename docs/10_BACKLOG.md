# 10 — Backlog Routing

`research/REQUIREMENTS.md` is the single source of truth for requirement status and
priority. This file routes work; it intentionally has no competing checkboxes or done
count. `docs/09_IMPLEMENTATION_ROADMAP.md` contains dependency order and acceptance
criteria; `docs/01_PROJECT_STATUS.md` contains the current evidence snapshot.

## Select the next unit

Use the owner's P0 sequence: **R-37 → R-05 → R-06 → R-25 → R-36**, then the newly exposed
**R-39** deployed-gate gap. R-25's documentation work is complete; read the requirement
tracker for the others rather than assuming a historical backlog summary is current.

Next P1 deliverables: R-16 change report → R-17 independent parity → R-38 versioned
content pack, with R-43 lineage and R-23 portable vectors. Supporting work: R-07,
R-10, R-11, R-13, R-29; R-18, R-19, R-21, R-22, R-26, R-45. Follow the roadmap's
acceptance evidence and review the source/code before choosing a bounded ticket.

## Proof required for closure

- Supported scope, dates, jurisdiction and source evidence are explicit.
- A requirement closes on implementation plus meaningful tests, not a skeleton or doc.
- A semantic bug gets a regression case; human-approved intent tests are preserved.
- Approval applies to rules and table values; missing/unknown does not become false.
- Independent known-answer cases remain independent of the evaluated implementation.
- New gaps get an ID in the requirement tracker instead of disappearing from claims.

## Deferred work and decisions

P2 work is listed in the tracker, including R-40–R-42/R-44. R-46 is the not-started
England Universal Credit candidate and requires the owner's decision. R-32–R-35 are
founder decisions, not features to implement without an answer.

Maintain the frozen calculation service, OpenFisca export and optional authoring; do not
expand their features. Catala/LegalRuleML/PROV exports, Akoma Ntoso, OCR, plugin SDK,
pre-user hosted multi-tenant SaaS and pre-hosted certifications are outside this backlog
per ADR-032. The old 134-item expansion checklist is superseded, not evidence of readiness.
