# 20 - Technical due diligence (buyer's reviewer)

## 1. Verdict
Not needed in its current form, and I would not buy it: a tidy ~7.9k-line single-author prototype (66 commits on two days, no outside users) whose headline sign-off claims are partly unwired, and Apache-2.0 means the code buys no moat. I would fund a fixed-fee paid pilot if sections 3 and 5 close.

## 2. Assumptions challenged
- **Hosted SaaS is a hard sell** -> Agree, but the API already stores no household data; the real blocker is no proof of correctness. Self-hosted is right; multi-tenancy is unnecessary.
- **Buyers pay for currency, sign-off, support** -> Agree, and it indicts the product: the update path is least built. Parameters (annually changing numbers) have no extraction, sit outside the approval gate (`approved_subset` keeps parameters whole), and the shipped SNAP package has no values for 6 of 10. Tests inject them via `with_tables`, so serving `examples/snap/rules.json` returns unknown for the headline answer.
- **Agencies too slow** -> Agree. No native SSO, accessibility statement or SBOM.
- **Runtime not an AI system** -> Plausible (closed AST, Decimal, no eval) but counsel's call; ADR-022's "Digital Omnibus in force 27 Jul 2026" is unverified by me.
- **Differentiator = provenance + sign-off + unknown** -> "Unknown" is real. Provenance proves only that a quote lies inside the cited clause; 14 of 15 hand-written spans failed when first checked. Sign-off is weaker than claimed: `record_seed` and `should_seed` are never called outside tests, so no faults are ever seeded; the "edit" decision cannot work from the UI (`ReviewEvent` demands `edited_to`, the form sends none). The OpenFisca equivalence test compares the evaluator with an export of the same IR: consistency, not correctness.

## 3. REQUIRED to sell
- [buyer must-have] External correctness evidence: reconcile the 15 rules with official worked examples or an independent calculator.
- [buyer must-have] Parameters as sourced, dated, reviewed objects, with complete shipped tables.
- [buyer must-have] Measured LLM extraction quality and reviewer minutes per rule. Every compile test uses `RecordedProvider`; no live result is recorded.
- [buyer must-have] Ingestion of what the target publishes: HTML/PDF/DOCX plus one EU or UK format. Hierarchy is rebuilt from CFR `(a)(1)(i)` markers with "7 CFR" hard-coded; injection regexes are English-only.
- [buyer must-have] OIDC/SAML SSO and roles. One shared HMAC secret mints any reviewer identity; no author/approver separation; the hash chain resists only non-privileged edits.
- [procurement] SBOM, pinned dependencies (mostly `>=`), rate and size limits (`/v1/validate` takes unbounded JSON), vulnerability policy.
- [legal] Per-corpus rights review; ADR-023 itself says "public domain" does not generalise to UK or EU text.
- [buyer must-have] Reconciled docs: README/CHANGELOG omit the service, backlog lists it unbuilt, test counts disagree (346/427/436/462).

## 4. NOT required / overbuilt
- API keys and usage metering: billing for a SaaS with no customers.
- OpenFisca export (~1,000 lines): optional interop that loses "unknown" by design.
- Multi-tenancy, client SDKs (generate from OpenAPI later), Catala/LegalRuleML/PROV targets, Akoma Ntoso unless an EU buyer asks.
- The provider-neutral LLM layer is cheap with low lock-in; hard-coded model ids will rot.

## 5. Deal-breakers
1. Anti-rubber-stamping control not operational while docs claim it.
2. No correctness evidence; extraction unmeasured.
3. Bus factor 1, part-time founder; no contracting entity, E&O cover or escrow evident.
4. IR shaped by one fixture: no currency on `money`, no year-to-date accumulators, no state-option layering; payroll and EU benefits unproven.

## 6. Commercial (estimates, unmeasured)
Acquisition: near zero. Pilot: US$20-40k fixed for one rule pack plus six months of updates; US$2-5k/month per maintained pack if oracle tests pass. I measured ~2,500 households/s on 15 rules, single core: fine per case, low hundreds at state scale, not microsimulation.
New-domain effort (guess): one US state's payroll rules, 4-8 weeks with this tool once HTML/PDF ingestion exists, versus 2-5 weeks hand-coded without audit trail; one EU country's benefit, 6-12 weeks including a legal expert. The tool wins only on re-review after amendments.

## 7. Top 3 changes
1. Make the gate real: seed faults, fix edit, gate parameters, ship sourced complete tables, publish an external-oracle comparison.
2. Pick one buyer domain and measure end to end (ingest, propose, review minutes, accuracy) against hand-coding; that is the sales number. Defer metering and OpenFisca polish.
3. Cut procurement and bus-factor risk: SSO and roles, reconciled docs, SBOM, second maintainer, a legal entity.
