# Sim 01 - VP Engineering, US payroll & HR SaaS

## 1. Verdict
Not needed by us today: our bottleneck is detecting and interpreting change across 50 states and thousands of localities, not turning clauses into code, and you cover zero payroll rules (SNAP is irrelevant to payroll). I would not buy; I would accept a free shadow-mode parallel run on one narrow rule family.

## 2. Assumptions challenged
- **H1 hosted API is a hard sell.** Confirmed, stronger: I want an in-process library, not HTTP. Payroll load spikes before paydays; a third-party hop to an offshore solo vendor fails vendor review.
- **H2 pay for currency, sign-off, support.** Mostly true, but I already employ those people. I pay only if cheaper than headcount and indemnified.
- **H3 private companies first.** Right for a solo founder, wrong target: a payroll vendor competes with its own compliance team. Benefits-eligibility software is nearer your 15 rules.
- **H4 not an AI system (EU AI Act).** Plausible (no runtime inference); irrelevant to my buying. For commercial EU sales the Cyber Resilience Act (Reg. 2024/2847) and revised Product Liability Directive (2024/2853, covers software) matter more. Dates may have shifted; get counsel.
- **H5 differentiator = provenance + sign-off + "unknown".** My comparison is not OpenFisca/Catala; it is "dated tables + citation column + Git + two reviewers". Provenance helps audits, but I mostly have it. "Unknown" is wrong on payday: a pay run must yield a number or a routed exception. The one feature I want is amendment impact analysis (blast radius before shipping a tax update).
- **Rules-as-code replaces the compliance team.** No. Payroll rules are mostly dated tables plus simple formulas. Cost is monitoring bulletins, agency FAQs and local ordinances, then interpreting them. Thresholds are still hand-encoded, which is what we already do.

## 3. REQUIRED to sell to me
- Published validation against ground truth (agency worked examples, my results) [buyer must-have]
- HTML/PDF ingestion of state statutes, bulletins, municipal codes; eCFR covers FLSA/garnishment regs, not withholding tables or local law [buyer must-have]
- Parameter extraction with effective dates [buyer must-have]
- Legal entity, indemnity cap, E&O and cyber insurance; Apache-2.0 disclaims everything while we guarantee penalties to 8,000 customers [procurement]
- Named credentialed sign-off (CPA/EA/employment counsel), not the founder alone [buyer must-have]
- Written freshness SLA, e.g. material change in pack within 5 business days of publication, 24h hotfix (my estimate), second maintainer [procurement]
- Security pack: SIG Lite/CAIQ answers, signed releases, SBOM, vulnerability disclosure [procurement]
- Language-neutral output (JSON IR plus test vectors); our engine is not OpenFisca [buyer must-have]
- Per-variable "unknown" policy (route to review vs block) [buyer must-have]
- Source-text terms: codifier ToS on scraping [legal]
- If hosted: state privacy service-provider terms, DPA; EU/UK customers need GDPR Art. 28 plus SCCs/UK addendum for Pakistan (no adequacy decision, as I understand it) [legal]
- Founder's employer IP/moonlighting clearance in writing [procurement]

## 4. NOT required / wasteful
- OpenFisca export (for me), Catala/LegalRuleML talk, SNAP expansion
- HTTP API keys/metering; own reviewer app and hash-chained log (I want review in Git/PRs, logs in my SIEM)
- 41 diagnostics, mutation testing and AI Act positioning as sales points
- Keep and publish: seeded-fault catch rates, semantic diff, impact analysis.

## 5. Deal-breakers
- No entity, insurance or indemnity
- Single maintainer with a full-time job and no SLA
- PII through a hosted API
- Zero payroll coverage, no benchmark
- "Unknown" with no fallback path
- "Reviewed" claims with unnamed reviewers

## 6. Commercial (all estimates)
Today: $0 for product, $0 for SNAP. After a clean shadow run: fixed-fee 90-day pilot, $15-40k, one rule family. Then an annual maintained pack per jurisdiction family, $20-60k, justified only by displacing 0.25-0.5 of a compliance engineer (assumed loaded $150-200k), with SLA and indemnity. No per-call pricing.

## 7. Top 3 changes
1. **Pick a payroll wedge you can prove:** FLSA regular-rate overtime and federal garnishment caps (eCFR-ingestible), then minimum wage and paid sick leave for 3-5 states. Build HTML ingestion and parameter extraction; benchmark against hand-coded truth. Otherwise admit you are benefits-eligibility and sell there.
2. **Build the commercial wrapper before features:** entity, E&O/cyber, contracted credentialed reviewers, SLA, second maintainer, employer IP clearance.
3. **Make it embeddable and change-driven:** language-neutral export, in-process library, a regulation-change feed emitting impact reports and PR-style review.
