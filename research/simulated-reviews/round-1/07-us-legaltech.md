# 07 - Senior PM, US legal-tech (regulatory change + obligation management)

## 1. Verdict
As built (SNAP calculator, eCFR-only) this is not needed in corporate-legal or law-firm buying, and I would not buy it. "Executable rules with clause traces" is a real but narrow need (applicability, thresholds, deadlines); my buyers pay for change monitoring and an obligation register. I would not license or acquire the engine: Apache-2.0 means I'd pay only for content, support and evidence.

## 2. Assumptions challenged
1. **Hosted SaaS is a hard sell** -> wrong cut. Legal departments buy hosted SaaS routinely once SOC 2/ISO 27001, DPA and SSO exist. What matters is which data touches it: regulation text is public, customer facts are not. Host monitoring/authoring on public text; run the evaluator customer-side.
2. **Pay for currency, sign-off, support** -> mostly true, but "named expert sign-off" is a UPL/liability trap unless signers are licensed attorneys and customer counsel decides.
3. **Government too slow; software companies first** -> agree on government, but software companies are not my buyer. Mine are legal ops/compliance and firm innovation teams.
4. **Runtime not an "AI system" (EU AI Act)** -> plausible for the deterministic runtime (Art. 3(1); Commission guidance excludes plain rule execution; verify). But LLM authoring is AI, and buyers ask about AI disclosure and no-training terms, not classification. Application dates may have moved (Digital Omnibus); verify.
5. **Differentiator = provenance + sign-off + "unknown"** -> citations are table stakes in legal AI. Real competitors are content publishers, GRC suites and in-house LLM builds, not OpenFisca/Catala. "Unknown" is the best idea and is undersold.

## 3. REQUIRED to sell
- PDF, HTML (regulator sites, Federal Register, state agencies), Word ingestion; EUR-Lex and legislation.gov.uk formats. [buyer must-have]
- Change monitoring: scheduled fetch, diff, alert, "does this affect us?" triage. This is the category. [buyer must-have]
- Obligation register export (obligation, actor, trigger, deadline, citation, owner) to CSV/Excel, API, ServiceNow/Jira/GRC. [buyer must-have]
- Real content in a domain buyers care about; SNAP is not one. [buyer must-have]
- SOC 2 Type II or ISO 27001 (or dated roadmap), pen test, SSO, RBAC, DPA, subprocessor list naming LLM vendors, zero-retention/no-training terms. [procurement]
- US/EU contracting entity, tech E&O/cyber insurance, liability cap, continuity/escrow plan. [procurement]
- Clean IP chain: founder's employer must not own the code. [procurement]
- GDPR/UK GDPR: Art. 28 DPA, transfer mechanism (SCCs/UK addendum), Art. 27 representative where applicable; reviewer identities are personal data. [legal]
- UPL posture: B2B to counsel only, outputs "for attorney review", no consumer use, outside-counsel opinion. ABA Model Rules 1.1/1.6/5.3 and Formal Opinion 512 drive law-firm questionnaires. [legal]
- Source licensing: US federal text fine; check EU/UK reuse terms; no publisher content. [legal]
- Substantiated accuracy claims (FTC Act s.5 covers AI claims). [legal]

## 4. NOT required / wasteful
- Mutation testing, 41 diagnostics, boundary generators: invisible to buyers. Hash-chained log: an ordinary exportable audit trail suffices.
- OpenFisca export, household-free metering, SNAP pack: irrelevant here.
- Seeded-fault reviewer testing: it measures employees (EU works councils, GDPR monitoring). Make it opt-in, aggregate.
- Full evaluator: most obligations need no calculation; applicability thresholds and deadline calculators do.

## 5. Deal-breakers
- Public-facing "are you eligible?" use, or vendor-attested legal interpretation by non-lawyers (UPL).
- No security attestation plus an LLM subprocessor with undefined data use.
- Cannot ingest the buyer's source formats.
- No entity, insurance or settled IP chain.
- Accuracy claims with no benchmark.

## 6. Commercial (estimates, no data behind them)
- Fixed-fee pilot roughly $20-40k, 8-12 weeks, one domain pack my attorneys review, if security answers were adequate.
- Then roughly $20-60k/yr per maintained pack (currency + support). No licence fee for the engine.

## 7. Top 3 changes
1. **Re-point domain and product.** Lead with employment/HR compliance (founder's own domain; numeric, multi-jurisdiction: overtime thresholds, leave, pay transparency, mass-layoff notice). Next privacy (applicability thresholds, breach-notice clocks), then financial regulation (high price, long diligence). ESG last: too volatile in 2026. Build monitoring + obligation register on the existing semantic diff, plus HTML/PDF/Word and UK XML ingestion. Keep SNAP as a demo.
2. **Reposition as a counsel-reviewed applicability and deadline engine**, hosted on public text only, evaluator customer-side. Get US and EU counsel opinions (UPL, GDPR, AI Act) before outreach.
3. **Produce evidence first:** publish extraction accuracy and reviewer-catch-rate results (fault-seeding data is the only novel IP); start SOC 2 readiness, insurance, entity; resolve employer IP; sign 2-3 design partners on fixed-fee pilots.
