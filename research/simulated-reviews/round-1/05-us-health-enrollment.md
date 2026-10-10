# 05 - Director of Product, US Medicaid/ACA enrollment navigation

## 1. Verdict
Not needed as shipped: I need Medicaid MAGI/CHIP/marketplace across my states; you offer 15 federal SNAP income rules, no state options, no benchmark, no users. I would not buy today; I would take a call in 12 months if you show a maintained state-specific MAGI pack, a named qualified reviewer, and a deployment where no PHI reaches you.

## 2. Assumptions challenged
1. **Hosted SaaS is a hard sell.** True, because of HIPAA. Household data a health system or plan collects in its care/enrollment role is likely PHI, so you would be a business associate (45 CFR 160.103, 164.502(e), 164.504(e)): BAA, Security Rule safeguards, breach notification, subcontractor BAAs. "Stores no household data" does not help; your servers still process it. Cleaner: run in my VPC or as a library, with only rule inputs and no identifiers.
2. **People pay for upkeep and sign-off.** Agree; the strongest of the five. FPL guidelines change yearly; state MAGI percentages and CMS rules move; 2025-26 federal Medicaid and subsidy changes may apply (verify). The engine is commodity: MAGI (42 CFR 435.603 plus state plan) is small and public.
3. **Government too slow.** Agree, but my buyers are health systems and plans; state agencies are my source of truth, not reachable customers.
4. **EU AI Act runtime.** Irrelevant to my US sale. US analogues: state AI laws on consequential decisions (Colorado's date has slipped; check) and Section 1557 decision-support tools (45 CFR 92.210; applicability to coverage screening uncertain).
5. **Differentiator = provenance + sign-off + unknown.** Weak for payer audits. Auditors ask whether the navigator followed state policy, not "which CFR clause". The state system decides; you screen. A trace to the state plan or manual would matter; 42 CFR 435 alone does not. "Unknown" is genuinely valuable: it prevents false denials and routes people to a full application.
6. **Is a compiler needed?** For MAGI, a maintained parameter table with tests is cheaper than an LLM pipeline; compilers pay off at thousands of rules.

## 3. Required to sell
- Signable BAA, or architecture provably keeping PHI out [legal: 45 CFR 164.504(e)]
- Security Rule controls; SOC 2 Type II or HITRUST [procurement]
- US contracting entity; cyber and tech E&O insurance [procurement]
- Offshore PHI access/storage: many state Medicaid/plan contracts restrict it; a Pakistan-based operator will be asked [procurement; verify per contract]
- MAGI Medicaid/CHIP by state with state FPL percentages; non-MAGI routes to full application [buyer must-have]
- Marketplace subsidy rules (26 CFR 1.36B) if I serve ACA [buyer must-have]
- Annual FPL update with SLA, sourced from Federal Register and state documents, not eCFR [buyer must-have]
- Immigration-category handling [buyer must-have]
- Named, credentialed policy reviewer; effective-dated approvals [buyer must-have]
- Concordance evidence against the state's official screener [buyer must-have]
- FHIR/SMART intake [buyer must-have]
- WCAG 2.1 AA, language access for patient/navigator UI [procurement; legal where 1557/508 apply]
- Source escrow, backup maintainer [procurement]

## 4. Not required / wasteful (for me)
- EU/UK ingestion, Akoma Ntoso, AI Act work
- Hash-chained log, seeded-fault tests, 41 diagnostics, mutation testing: fine internally; I will not score them
- OpenFisca export; API keys/metering if self-hosted
- LLM authoring: I care who signed, not how drafted
- Federal SNAP as lead product

## 5. Deal-breakers
- No Medicaid/CHIP, no state variation
- No BAA path, or PHI offshore against contract
- No currency guarantee; one person with another full-time job
- Reviewer without eligibility-policy credentials
- No reference customer or concordance data

## 6. Commercial (estimates, not data)
- I would pay for a maintained pack, not software (Apache-2.0 is $0).
- Fixed-fee one-state pilot, 3-6 months: roughly $25-60k.
- Then roughly $20-60k/yr per state pack with SLA and named reviewer.
- Per-call pricing unattractive; expect 6-12 months of security review.

## 7. Top 3 changes
1. Build MAGI Medicaid/CHIP for 1-3 states with an FPL pipeline from the Federal Register; prove concordance on a navigation partner's test cases.
2. Package zero-PHI: library/container in customer VPC, minimal inputs, data-flow document, BAA template, US entity, insurance, SOC 2 plan; settle the offshore question.
3. Sell a maintained pack with SLA, a hired credentialed reviewer and a FHIR connector; shelve EU/UK.
