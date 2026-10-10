# 09 - UK benefits calculator Product Lead

## 1. Verdict
Not needed as an engine: I already have calculators, and PolicyEngine UK/OpenFisca cover runtime. The authoring and amendment-impact workflow interests me, but it has zero UK coverage (SNAP is irrelevant to my buyers), so I would not buy today; I would pay for a fixed-fee Universal Credit (UC) pilot proven against my live calculator.

## 2. Assumptions challenged
- **H1 (SaaS hard sell):** Wrong for my segment. Charities, councils and housing associations lack ops capacity and routinely buy hosted calculators. The objection is data location and processor terms. Offer in-browser execution or a UK-hosted stateless API; self-host suits integrators like me.
- **H2 (pay for currency, sign-off, support):** Mostly right. I pay for fast April uprating, regression evidence, and a named, insured welfare-rights reviewer. A solo HR-ops founder signing off is not credible.
- **H3 (agencies too slow):** Right for DWP; wrong for councils and charities at low value (quotes/direct award). Fastest buyer: calculator vendors.
- **H4 (not an AI system):** UK has no AI Act (check for a bill). I care about UK GDPR automated-decision rules (Arts 22A-D via DUAA 2025), DPIAs, and the Algorithmic Transparency Recording Standard (council scope uncertain). EU: rules-only execution plausibly outside Art 3(1) (Commission guidelines, 2025), but Annex III 5(a) covers benefit eligibility if it counts; Digital Omnibus timing uncertain.
- **H5 (provenance differentiates):** Narrow. Advisers and auditors value it; buyers compare accuracy to DWP outcomes. PolicyEngine UK already models UC with sourced parameters. The moat is maintenance plus impact analysis, not the audit chain.
- **Hidden assumption, law = legislation:** UK entitlement also rests on DWP guidance, tribunal case law, and hundreds of local Council Tax Reduction (CTR) schemes. Scotland, Wales, NI are separate regimes.

## 3. REQUIRED to sell
- [legal] UK GDPR Art 28 processor terms, Art 32 security, Art 35 DPIA support. Disability/health inputs are special category (Art 9).
- [legal] Restricted transfers: founder is in Pakistan. I know of no UK adequacy regulation for Pakistan (verify), so support access to customer data needs an IDTA/Addendum plus risk assessment, or zero access by design. Also a UK entity or Art 27 representative, and ICO fee (verify).
- [legal] DUAA 2025 commencement is staged by regulations; verify what is in force before contracts cite it.
- [legal] Accessibility: Public Sector Bodies (Websites and Mobile Applications) (No. 2) Accessibility Regulations 2018 (WCAG 2.1 AA; check for 2.2), Equality Act 2010. No citizen-facing UI exists. Welsh councils need bilingual output.
- [procurement] Cyber Essentials (IASME); Procurement Act 2023 (live Feb 2025); G-Cloud (next iteration and Digital Marketplace successor uncertain); PI and cyber insurance.
- [buyer] legislation.gov.uk ingestion (CLML/Akoma Ntoso) with point-in-time versions, amending SIs, uprating tables (gov.uk HTML), devolved regimes. UC first.
- [buyer] Uprating SLA (annual Social Security Benefits Up-rating Order) and parity evidence on a few hundred test households.
- [buyer] Export to my stack (JSON/JS/Python), not only OpenFisca.
- [buyer] Founder-continuity plan: Apache-2.0 helps; add escrow or a backup maintainer.

## 4. NOT required / wasteful
Catala and LegalRuleML adapters; hash-chaining (exportable approval history suffices); seeded-fault testing and mutation scores; API-key metering; PostgreSQL; PDF ingestion; US eCFR work; EU AI Act paperwork before a first UK sale; ISO 27001 now.

## 5. Deal-breakers
- Zero UK rules.
- No UK entity, insurance or Cyber Essentials.
- No named UK reviewer with liability.
- Part-time founder cannot meet the fixed April uprating deadline.
- Household data reachable from Pakistan with no transfer mechanism.
- No accessibility evidence.

## 6. Commercial (my estimates, unvalidated)
- Pilot: GBP 8-15k fixed fee to encode UC core and prove parity.
- Maintained UC pack: GBP 10-25k/yr including uprating, sign-off, support.
- Tooling: GBP 0 (Apache); GBP 5-10k/yr support.
- CTR scheme pack: GBP 1-3k per authority per year.
- End buyers (councils, charities): low single-digit GBP k/yr, mostly under tender thresholds (verify).
- I would license the method and pipeline, not the engine.

## 7. Top 3 changes
1. Drop SNAP as the lead. Build legislation.gov.uk point-in-time ingestion, encode UC core, publish parity results.
2. Sell "uprating plus amendment-impact report". Recruit a named, insured UK welfare-rights reviewer, form or partner for a UK entity, get Cyber Essentials.
3. Make privacy architectural: browser-side execution, UK-hosted stateless API with a DPA, accessible reference front end with conformance statement.
