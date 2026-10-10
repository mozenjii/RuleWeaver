# R3 Product-scope panel: decision list

Effort: S = days, M = 1-3 weeks, L = over a month. Prices are simulated.

**Segment assumed.** A UK benefits-calculator vendor, Universal Credit core plus April uprating, self-hosted fixed-fee pilot. Nine round-2 final calls point here (#09, #10, #12-#17, #19): an oracle (the vendor's live calculator), a recurring update event, a structured source, no offshore-access clauses. Dissent: #20, #02, #05, #06, #18 prefer one US state's SNAP (code is closer). [C] items serve both; start [UK]/[US] ingestion only after a signed LOI.

## FIX NOW

1. **Seeded faults never run** (fact 1; #20, #16, #07, #08). Nothing calls `should_seed`/`record_seed`, yet `review --seed-rate` help, README "Built", /metrics text, ADR-021 and STATUS imply they do. Relabel "designed, not wired". S, docs.
2. **"Edit" always returns 400** (fact 2). `detail.html` offers it; `submit` in `review/app.py` never reads `edited_to`. Remove the option; untick STATUS. S, engineering.
3. **Shipped SNAP package computes nothing** (fact 3). Six empty (fpl_annual, standard_deduction, standard_deduction_minimum, shelter_cap, max_allotment, minimum_benefit); `serve` cannot supply values, and my API run returned null eligibility. `baseline.json` values carry no source. Label "structure only". S, docs.
4. **NOTICE, healthz** (facts 5, 6): already fixed in HEAD d5d0db5 with tests. Log in CHANGELOG. S, docs.
5. **Audit-trail wording** (fact 7; #16, #20, #04, #11). Unkeyed SHA-256 in the same database; `ruleweaver token <name>` mints any identity. Say "detects casual edits, not an administrator". S, docs.
6. **Legal-position text.** ADR-021 ("compliance evidence", Art 14), ADR-022 ("entire legal position", Art 22, "Omnibus in force 27 Jul 2026", unverified), `review/store.py` docstring, STATUS line 23 (#14, #13, #10, #15). Replace with intended-purpose, non-reliance text. S docs; counsel review M.
7. **Doc contradictions.** README/CHANGELOG/STATUS omit `serve`; backlog lists the service unbuilt. Test counts: README 346/427, STATUS 436; I ran 447 passed, 1 skipped. README calls Catala/LegalRuleML "selected"; STATUS says dropped (ADR-019). Schema `$id` names nonexistent `mozenjii/NICXON`. S, docs.
8. **OpenFisca-Core is AGPL** (fact 4). Say so in README and `export` output; call the equivalence test "consistency, not correctness" (#19, #20). S, docs/legal.
9. **Hardening (verified).** GET `/`, `/rule/*`, `/metrics` need no identity; no CSRF check on decide; API `/docs` open; a 51-member request gets a 422 echoing the household (#16, #13). S-M, engineering.
10. **Supply chain** (#16 R2, #20 R2). SECURITY.md, role mailbox (pyproject lists a personal Gmail), hashed lockfile, pinned image and actions, split release job (write tokens live during `pip install`), SBOM. S-M, engineering.
11. **Employer IP release**, written, before outreach (#17, #16, #18). S, legal.

## BUILD (first paid pilot)

1. [C] **Parameters as sourced, dated, gated objects.** `approved_subset` keeps parameters whole; `ParameterValue` has no source. Add source/date, approval events, availability diagnostic, complete pilot tables. Uprating is a parameter change (#20, #09, #01, #03). M, engineering.
2. [C] **Oracle-parity command** against the buyer's known-answer cases, with a published result: the only sellable evidence (#20 R2, #09, #12, #02). M, engineering.
3. [C] **Change-impact report as the deliverable.** `diff/impact.py` exists; add structural source diff, affected-test list and a dated readable report. The convergent purchase driver (#01, #04, #06-#08, #11, #12, #18). M, engineering.
4. [C] **Pack release artefact:** versioned, hashed package, tables and review-log export with chain head; "valid as of" date in the evaluate record (#20 R2, #02). S-M, engineering.
5. [UK] legislation.gov.uk point-in-time ingestion, currency on `money` (absent; #20), UC core; verify reuse licence. L. [US alt] state-manual HTML ingestion; remove hard-coded "7 CFR" in `ingest/ecfr.py`. L.
6. **Reviewer privacy:** opaque reviewer IDs in the chain, per-person timing off by default (#13, #08). S-M, engineering.
7. **Commercial/legal:** free shadow run on synthetic data, then deposit (#01-#03, #11, #17-#19); bounded services contract (#15 R2, #17); insured partner as prime supplying a named reviewer, since none exists (#16 R2, #09, #12). Entity, pentest, SOC 2 only when a contract demands. S-M.

## FREEZE (keep, stop investing)

- Hosted API, keys, metering (`service/`, 378 lines): synthetic-data sandbox only (#13 R2).
- Fault-seeding wiring, dual-encoding: buyers' analysts own the signature (#02, #04, #06, #10, #11).
- OpenFisca adapter (1,046 lines): maintain only (#01, #03, #20; #10 dissents).
- LLM extraction: optional; no live accuracy recorded; #20 R2 dropped it as must-have.
- Mutation harness, diagnostics: add none (#02, #09, #14).

## CUT / DE-EMPHASISE

- Pitch, delete text not code: "named reviewer", "anti-rubber-stamping", "approved against the regulation", Annex III/Art 14/"not an AI system"/Art 22 claims (#15, #10, #14, #17).
- Federal-15 SNAP as a market story (fixture only); hosted SaaS, per-call pricing (#09, #12).
- Roadmap deletions: Catala, LegalRuleML, PROV, Akoma Ntoso, OCR, plugin SDK (#20, #09); EU entry until a pilot is paid (#13 R2, #14 R2, #11); HR/payroll lead (#07; rejected by #01, #04, #06, #08, #15, #18).
- Pre-pilot SOC 2, ISO 27001, FedRAMP, pentest (#16 R2, #19).

Unverified: SNAP 2025-law effect; Omnibus, CRA, DUAA dates.
