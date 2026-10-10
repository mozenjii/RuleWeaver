# 11 - EU bank, Head of Regulatory Compliance Technology

## 1. Verdict
No law requires this, and 15 US SNAP rules are irrelevant to a bank or insurer. I would not buy; I would accept a free, self-hosted, non-critical proof of concept on an EU regulation I actually track.

## 2. Assumptions challenged
1. **Hosted SaaS is a hard sell.** For a bank it is a non-starter: customer data to a Pakistan-based sole trader means GDPR Chapter V transfers (I know of no Pakistan adequacy decision; verify) plus DORA exposure. The API should never receive personal data. Self-hosted Apache-2.0 code needs only open-source governance, not a vendor.
2. **People pay for currency, sign-off, support.** Agree on currency. Expert sign-off does not transfer accountability: the management body keeps it (DORA Art. 5; EBA outsourcing guidelines). It is only credible from qualified EU/UK lawyers with professional indemnity cover, and "not legal advice" disclaimers contradict selling it.
3. **Agencies too slow.** Banks are slower for a solo vendor (6-12 months onboarding, my estimate). Go through law firms, consultancies or regtech integrators.
4. **Runtime is not an "AI system".** Probably right: Regulation (EU) 2024/1689 Art. 3(1) and Recital 12 exclude rules defined solely by humans. I still need a written classification memo. The LLM authoring step is a separate question. Annex III 5(b)/5(c) targets the bank's own scoring and pricing models, which are not statute and not encodable from law text. The Digital Omnibus may have moved dates; verify.
5. **Differentiator is provenance + sign-off + "unknown".** Real but narrow; "unknown" instead of default denial is the best idea. My real alternatives are Excel, GRC suites and regulatory-change tools, not OpenFisca or Catala.

## 3. REQUIRED to sell
- Self-hosted, no data to vendor [procurement; GDPR Art. 28 and Ch. V otherwise].
- DORA (Reg. 2022/2554) Art. 30 contract terms, plus Art. 30(3) (audit access, incident support, BCP, exit, termination) if supporting a critical or important function [legal]. Whether a plain licence is an "ICT service" is unclear; support and rule-pack updates clearly are.
- Register of information entry: provider identifier (likely an LEI, which a sole trader may lack; unsure) and subcontractor chain naming the LLM providers [legal].
- Due diligence: financial standing, key-person plan, BCP, ISO 27001 or SOC 2 equivalent [procurement].
- SBOM, signed releases, vulnerability policy; Cyber Resilience Act (Reg. 2024/2847) duties, dates unsure [legal/procurement].
- EU/UK sources: EUR-Lex (Formex/Akoma Ntoso), legislation.gov.uk, national transposition, EU languages, point-in-time versions [buyer must-have].
- A domain that matters: consumer credit (CCD2, Dir. 2023/2225, applying 20 Nov 2026), AML thresholds (AMLR 2024/1624), MiFID, PSD2/3, CRR, Solvency II/IDD [buyer must-have].
- Named qualified legal reviewers, insurance, EU/UK entity or legal representative [procurement].
- Benchmark and measured reviewer catch rates [buyer must-have].

## 4. NOT required / wasteful
- OpenFisca export: no bank uses it.
- Hash-chained log: no supervisor requires it; export to my GRC/SIEM.
- 41 diagnostics, mutation testing, API keys, metering: overbuilt for zero users.
- Supervisors do not ask for rules-as-code. Clause-level trails help internal audit and regulatory-change management, which is where I see value. EBA reporting already ships machine-readable validation rules.

## 5. Deal-breakers
- Solo founder as sole support for a critical function.
- Hosted, or hosted in Pakistan.
- No EU/UK content.
- Unqualified sign-off sold as assurance.
- No assurance artefacts or insurance.
- No benchmark.

## 6. Commercial (estimates)
- Free or fixed-fee PoC (EUR 10-30k, 3 months) on one regulation, non-critical, our reviewers in the loop.
- Production: annual subscription per rule pack, mid five figures, only with EU/UK sign-off partner and entity. Onboarding costs more than the licence, so I would buy via an integrator.

## 7. Top 3 changes
1. Pick one live EU/UK slice (CCD2 or AMLR thresholds), build EUR-Lex and legislation.gov.uk ingestion, partner with an EU law firm or university for named review.
2. Reposition from calculation API to a self-hosted regulatory-change impact and traceability tool; publish a DORA due-diligence pack (SBOM, security policy, AI Act classification memo, exit plan, subprocessor list). Sell through a partner entity.
3. Stop adding features. Produce evidence: lawyer-run benchmark, published seeded-fault catch rates, independent validation.
