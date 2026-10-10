# 19 - Open-source business model

## 1. Verdict
Licensing is not your bottleneck: Apache-2.0 is right for the engine, and nothing should be closed yet because there is no user to lock in. I would not buy software or API calls today; I would sign a fixed-fee pilot for a reviewed, dated, named-reviewer rule pack.

## 2. Assumptions challenged
- **H1 hosted SaaS is a hard sell** -> Partly. No-storage metering helps, but receiving household facts is still processing (GDPR processor role). Self-host by default.
- **H2 pay for currency, sign-off, support** -> Mostly right, with a trap: named sign-off is a liability product and the founder is not the credentialed reviewer. Sell "reviewed against source text as of date X" via a credentialed partner, never legal opinion. SNAP's annual adjustments give a recurring update event; other domains must prove theirs.
- **H3** -> Agree; agencies are better credibility partners (unverified). **H4** -> outside my lens; not the CRA test.
- **H5 differentiator** -> Weak as a moat: provenance code is Apache-2.0 and copyable. The durable asset is reviewed content plus attestation. Check that "unknown" survives the OpenFisca export.
- **Open-core boundary** -> Unneeded now. Do not paywall the audit log or review app; they are your trust story.

**Licence options.** AGPL deters the embedders you want, and dual licensing needs a CLA plus a cloud-capture threat you lack. BSL/FSL contradicts the "IR as shared standard" aim. Stay Apache-2.0; revisit only if a hosting competitor appears. Your moat is content, attestation, SLA and brand.

**OpenFisca export** builds trust and lowers lock-in at little monetization cost, since the evaluator is not what is sold. Caveat: I believe OpenFisca-core is AGPL-3.0 (verify); generated packages importing it and served over a network may burden customers.

## 3. REQUIRED
- [legal] Chain of title: written confirmation your employer has no claim to the code.
- [legal] Contribution policy before the first outside PR (ADR-023: relicensing is free only until then). DCO, unless you want a closed add-on option, then CLA.
- [legal] Trademark clearance for "RuleWeaver" (USPTO, EUIPO, UKIPO) before more brand spend. Apache-2.0 s.6 grants no trademark rights; publish a trademark policy. Foreign applicants likely need local counsel (verify).
- [legal] Rule-pack terms by contract and attestation, not copyright: US federal text is public domain, your encodings have thin or uncertain copyright, EU database right may touch compiled sets.
- [legal] CRA, Reg. (EU) 2024/2847 (uncertain; check late-2026 status). Non-commercial FOSS is largely out of scope; stewards get lighter duties. But paid support or packs alongside distributed software is plausibly "commercial activity", making you a manufacturer: vulnerability handling, SBOM, security updates, conformity assessment. I recall reporting duties from Sept 2026, main obligations Dec 2027. Pure hosting is generally outside scope. Get EU counsel before the first paid EU deal.
- [buyer must-have] SECURITY.md, SBOM, signed releases; liability cap, no-legal-advice clause, defined sign-off scope; E&O insurance.
- [procurement] Contracting entity with invoicing and tax forms (W-8BEN, VAT handling).

## 4. NOT required / wasteful
- Closed rule packs, SSO or audit-export paywalls.
- Metering and API keys without a hosted customer.
- Dual licensing, CLA tooling, a foundation.
- Filing marks in three jurisdictions now.

## 5. Deal-breakers
- No employer IP release.
- Trademark conflict found after launch.
- Unaddressed AGPL flow-through via the export.
- Unnamed or uncredentialed sign-off with no liability terms.
- No CRA position before an EU sale.
- Unclear right to embed rule packs in my product.

## 6. Commercial (my estimates, not data)
Fixed-fee pilot: roughly US$10-25k for one jurisdiction pack with named sign-off, tests and six months of updates. Then perhaps US$1-3k/month per pack if updates are real; support extra. I would not pay per API call or for the engine. Comparable open-source firms lean services-led, managed-hosting or open-core; I cite none.

## 7. Top 3 changes
1. Governance before the first PR: employer release, DCO, TRADEMARK.md, SECURITY.md, NOTICE; run the trademark search.
2. Sell "reviewed rule packs" (signed, dated releases, attestation, update SLA, contract); keep engine, corpus and audit log open.
3. Freeze monetization plumbing; land one fixed-fee pilot; get written AGPL (export) and CRA opinions before any EU sale.
