# 17 - Cross-border business, tax and payments advisor

Legal/tax points are from memory, may have changed by 2026; confirm locally.

## 1. Verdict
Entity, VAT and insurance spend is premature: nothing is sellable yet (15 federal SNAP rules, no users). Before any invoice you need written employer clearance and a self-hosted, services-only offer; I would not buy today, but would fund a fixed-fee pilot with a credentialed co-signer, insurance and a continuity plan.

## 2. Assumptions challenged
- H1 hosted SaaS is a hard sell: agree, more strongly. Hosting applicant data from Pakistan raises GDPR Chapter V transfers (no Pakistan adequacy decision, to my knowledge), likely offshore-data limits in US state contracts (uncertain) and SNAP applicant confidentiality (I believe 7 U.S.C. 2020(e)(8); verify).
- H2 pay for sign-off and currency: agree, but named sign-off carries the liability. An HR-operations founder is not a benefits-policy expert; the signer must be a credentialed subcontractor.
- H3 agencies too slow: agree, plus SAM.gov registration, insurance minimums, US-counterparty preference.
- H4 AI Act: outside my lane. Annex III 5(a) (public-benefit eligibility) is what buyers' counsel will check; "probably not an AI system" is a weak procurement answer. Moot now: no EU/UK ingestion exists.
- H5 differentiator: procurement scores vendor risk (continuity, insurance, recourse), not provenance. Apache-2.0 plus OpenFisca export makes exit cheap; only services are defensible.
- Unstated: "I can sell this alongside my job." Largest legal risk.

## 3. REQUIRED before first invoice
1. [legal] Employment clearance: check moonlighting, IP-assignment and confidentiality clauses; get written employer consent and IP release covering RuleWeaver, including published Apache code. Otherwise your licence grant and IP warranties may fail.
2. [legal] Pakistan: NTN/FBR registration; declare business income beside salary; check the current IT-export tax regime and whether PSEB registration is needed (changes yearly).
3. [legal] Receive export proceeds through a bank; keep contract, invoice, bank advice (SBP rules uncertain).
4. [procurement] W-8BEN per US payer (W-8BEN-E if an entity), with Pakistani TIN. Services performed outside the US are generally foreign-source: no US withholding (treaty exists; verify). Trap: "licensed" rule packs used in the US risk royalty treatment (30% default withholding); contract as services.
5. [procurement] Tested payment rail: a small real USD wire first. Stripe availability for Pakistan-based sellers is doubtful, PayPal receiving restricted; Payoneer-style receiving is a common workaround (verify 2026).
6. [buyer must-have] One-page MSA/SOW: buyer-state or English law; cap = 12 months' fees; no uncapped indemnity for benefit-determination harm; no consequential damages. Expect insurance or escrow demands: judgments against you are hard to enforce.
7. [legal] B2B only. EU/UK businesses reverse-charge (Directive 2006/112/EC Arts 44, 196; UK equivalent): validate VAT IDs. Caveat: public bodies without a VAT ID may count as consumers, triggering non-Union OSS registration. Refuse B2C.
8. [buyer must-have] Continuity: second maintainer or escrowed private rule-pack repo; stated best-effort support hours (PKT evening is roughly US-East morning).

## 4. NOT required / wasteful
- US LLC/C-corp now: non-resident EIN is slow, Form 5472 carries a $25,000 non-filing penalty, and Pakistani limits on residents holding foreign companies are uncertain. Only if a buyer insists or you raise money.
- UK/EU company, VAT and US sales-tax registrations (avoided by not selling hosted SaaS).
- SOC 2/ISO 27001; API keys, metering, release automation for zero users; insurance before a small private pilot.

## 5. Deal-breakers
- Unresolved employer IP/moonlighting rights.
- Hosted processing of US benefit or EU personal data from Pakistan.
- Uncapped liability or any "official determination" claim.
- No E&O/cyber insurer covers a Pakistan-based sole proprietor while the buyer requires it (uncertain; ask a broker).
- Bus factor of one; no credentialed signer.
- Federal-only SNAP cannot support any state determination.

## 6. Commercial (all guesses)
- Pakistani sole proprietor: low cost beyond a local tax advisor. US LLC if forced: roughly USD 1,000-2,500/year.
- E&O/cyber: perhaps USD 1.5-5k/year for USD 1M limits, if obtainable.
- Fixed-fee pilot perhaps USD 10-25k: 50% upfront by wire, balance net-30; then an annual retainer. I would pay for sign-off and amendment updates, not code.

## 7. Top 3 changes
1. Get employer clearance and IP release in writing before any outreach.
2. Offer only a self-hosted engine plus fixed-fee services, US-only until EU/UK ingestion exists; prepare MSA, W-8BEN and a tested wire rail.
3. Recruit a credentialed co-signer and second maintainer, get one insurance quote, and pause plumbing work until a pilot exists.
