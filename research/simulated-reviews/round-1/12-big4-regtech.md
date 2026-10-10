# 12 - Big-4 regtech partner (UK/EU, US colleagues)

## 1. Verdict
Not needed by my firm today: 15 US SNAP rules with no external validation is a methodology prototype, not an asset I can put a name next to. I would not buy or white-label it, but I would fund a small fixed-fee pilot if the founder moves to a UK/EU domain where I supply the qualified reviewers.

## 2. Assumptions challenged
1. **Hosted SaaS is a hard sell.** Agree, for a sharper reason: a one-person Pakistan-based processor means GDPR Art. 28 plus Chapter V transfers (no adequacy; SCCs and transfer assessment; UK IDTA/Addendum). We would self-host anyway, so the metered API is irrelevant.
2. **Buyers pay for currency, sign-off, support.** Mostly, but sign-off must come from a qualified professional (tax adviser, solicitor, CPA); the founder works in HR operations. Provenance earns money only where an auditor or regulator will ask "why did the system compute this".
3. **Government too slow.** Directly, yes. But the public sector values provenance and open source, and buys through primes. A solo founder reaches it as our subcontractor.
4. **Runtime not an AI system.** Plausible (Art. 3(1), Recital 12: rules defined solely by humans), but a legal position, not a fact. The LLM authoring stage is an AI system, and a public-authority deployer using this for benefit eligibility (Annex III) changes the analysis. Digital Omnibus may have shifted dates by late 2026; verify. I need a written legal opinion, not an ADR.
5. **Differentiator is provenance + sign-off + "unknown".** Claimed, not evidenced: seeded-fault catch rates are the only proof and none are published. In tax, "unknown" must route to a named professional. Rivals include vendors with content teams and free PolicyEngine, OpenFisca, Catala.

## 3. REQUIRED to sell
- Known-answer benchmark with published error and fault-catch rates. [buyer must-have]
- Methodology pack: authoring standard, review SOP, recorded reviewer qualifications (identity is not competence), change control. ISQM 1 reviews will ask. [procurement]
- UK/EU ingestion (legislation.gov.uk XML, EUR-Lex/Akoma Ntoso) plus guidance and case-law layer; statute text alone is not the rule. [buyer must-have]
- Clean IP chain: employer claim excluded (full-time job); DCO/CLA for contributors. [procurement]
- Contracting entity we can onboard (KYC, tax forms, sanctions screening); professional indemnity and cyber insurance. [procurement]
- DPA template, sub-processor list, transfer mechanism. [legal]
- SBOM, signed releases, vulnerability policy; check Cyber Resilience Act duties and dates (uncertain). [legal/procurement]
- Independence screen: no tooling into systems of record of audit clients (EU Audit Regulation 537/2014 Art. 5; SEC/PCAOB rules). Removes much of my client base. [legal]

## 4. NOT required / wasteful
- 41 diagnostics, mutation testing, 462 tests: polish ahead of any benchmark.
- Metered API and keys: contradicts self-host plus rule packs.
- OpenFisca export: benefits microsimulation only, not tax or payroll engines.
- SNAP as proof domain: irrelevant to my practice; per-response disclaimers give no protection.
- Keep: amendment impact analysis (what clients would pay for) and seeded-fault testing (as quality evidence).

## 5. Deal-breakers
- No external validation; no qualified human sign-off.
- Unclear employer IP rights; bus factor one.
- No UK/EU sources, so no pilot with my clients.
- Marketing "AI Act exempt" without an opinion.
- No insurance or contracting entity.
- Our name used without our quality review and independence clearance.

## 6. Commercial (estimates, not data)
- Today: GBP 0; no white-label. Apache-2.0 code means acquisition buys no exclusivity; the assets are methodology, review data, reviewer network, brand.
- Pilot: 8-12 weeks, GBP 20-50k fixed fee, one domain, our SMEs sign off, founder subcontracts engineering.
- If it works: rule-pack revenue share (15-30% of our client fee, a guess) or annual per-jurisdiction pack priced against the client's in-house maintenance cost.
- Partner route: subcontractor on a delivered engagement first.

## 7. Top 3 changes
1. Pick one bounded UK/EU domain (rates-and-thresholds payroll or VAT slice, or a means-tested benefit) where a qualified professional will sign. Ingest legislation.gov.uk, build a known-answer benchmark, publish fault-catch results.
2. Build the commercial chassis: entity, insurance, IP assignment, DCO, DPA, SBOM/signing, AI Act opinion. Sell a self-hosted engine plus partner-reviewed rule packs; do not try to be the content publisher.
3. Stop feature work. Write the assurance pack (methodology, validation report, reviewer-qualification model); chase a funded pilot or public-sector subcontract.
