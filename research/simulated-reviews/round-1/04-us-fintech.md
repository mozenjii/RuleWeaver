# 04 - Head of Compliance, US consumer neobank (EWA + benefits deposit, partner bank)

## 1. Verdict
Not required for me today, and I would not buy: it encodes 15 SNAP eligibility rules, while my exposure is state EWA, fee-cap, licensing and disclosure obligations it cannot ingest. The idea (clause-linked, effective-dated obligations with a reviewer trail) is exam-valuable, so I would fund a pilot if state coverage, attorney sign-off and bank-ready vendor packaging existed.

## 2. Assumptions challenged
- **H1 hosted SaaS is a hard sell**: partly. I would never send customer NPI (GLBA) to a one-person vendor, but my best use case needs no customer data (statutes in, fee-cap/disclosure logic out). Self-hosting does not escape third-party risk management (TPRM); the bank still diligences the vendor, patching and support.
- **H2 pay for currency and sign-off**: agree on currency and change alerts. Sign-off is evidence only; I and the bank keep the compliance judgment. A non-lawyer founder cannot supply it; a law-firm partner is needed.
- **H3 private first**: agree, but my buyer (compliance/legal budget) differs from benefits software. SNAP work does not transfer.
- **H4 AI Act**: an EU question. In the US the label is irrelevant; the partner bank applies model-risk guidance (SR 11-7 / OCC 2011-12) to anything computing customer outcomes and will ask about the LLM in the authoring chain.
- **H5 differentiator**: provenance matters to examiners. "Unknown" helps only if it maps to a configurable fail-closed outcome with reason codes. My real alternatives are spreadsheets, law-firm 50-state surveys and change-monitoring content vendors, not OpenFisca.
- **Needed at all?** Only a minority of my obligations compute (fee caps, APR/APY math, Reg E clocks). Most are duties (disclose, notify, do not mislead). The tool extracts only "computable" clauses, skipping my largest exam exposure. CFPB posture in late 2026 is uncertain; state regulators and AGs are active, so do not assume federal retreat.

## 3. REQUIRED to sell
- State statute/regulation ingestion (HTML/PDF) for EWA, fee caps, licensing, with effective dates [buyer must-have].
- Named, qualified attorney sign-off with identity recorded [buyer must-have; exam].
- TPRM package: SOC 2 Type II or equivalent, SBOM, signed releases, patch SLA, subcontractor list (LLM providers), BCP, cyber/E&O insurance [procurement; Interagency TPRM Guidance, June 2023].
- Key-person continuity: second maintainer, escrow or fork rights, exit path [procurement].
- Model-risk documentation: inventory entry, conceptual soundness, test evidence, change control, validator access [procurement; SR 11-7 / OCC 2011-12].
- Point-in-time reproducibility ("which rule applied on date X to customer Y"), exam-readable export (PDF/CSV), retention matched to the bank's policy, independent timestamping or WORM storage [buyer must-have; exam].
- Change monitoring with impact on my fee schedules and disclosures, not households [buyer must-have].
- Inputs are product parameters, not NPI; GLBA service-provider terms if NPI is touched [legal; GLBA, Safeguards Rule/Interagency Guidelines].
- US contracting entity, US governing law, indemnity [procurement; offshore sole operator draws enhanced diligence].

## 4. NOT required / wasteful (for me)
- OpenFisca export: models households, not fee caps.
- SNAP content, Akoma Ntoso/EU formats, Catala/LegalRuleML.
- Hosted API, keys, metering: I want a library or batch job.
- Hash-chaining as a selling point: examiners want completeness, identity and retention, not the mechanism.
- 41 diagnostics, mutation testing, 462 tests: useful in validation, not a purchase driver.
- Seeded reviewer faults: keep them out of the production audit record.

## 5. Deal-breakers
- Zero state coverage, no consumer-finance content.
- No qualified lawyer in the approval chain, or marketing as "compliant" or "certified" (UDAAP/FTC Act s.5 exposure).
- Customer NPI sent to an uncertified hosted vendor.
- Sole part-time operator, no insurance, no continuity.
- "Unknown" with no defined operational outcome.

## 6. Commercial (my estimates, not data)
- Engine free (Apache-2.0); I pay for content.
- Fixed-fee pilot: roughly $20k-50k for 3-5 states of EWA/fee/disclosure obligations with attorney sign-off.
- Maintained pack: roughly $40k-120k/year per product line.
- Cycle likely 6-12 months with bank TPRM. Nothing before SOC 2 or equivalent.

## 7. Top 3 changes
1. First pack = US consumer-finance obligations: state EWA/fee-cap/disclosure rules plus Reg E/Z/DD from eCFR (already ingestible), with a state HTML/PDF ingester.
2. Add an obligations-register mode for all clause categories (not just computable), mapped to owner, control and test, with change alerts; this is what an exam asks for.
3. Partner a law firm for named sign-off, then build the TPRM/model-risk package (SOC 2 path, SBOM, insurance, second maintainer) before selling.
