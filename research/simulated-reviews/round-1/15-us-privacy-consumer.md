# 15 - US privacy/consumer counsel (stress test, not legal advice)

## 1. Verdict
No US law requires this tool. Self-hosted, it barely touches US privacy law because you never receive personal data; hosted, you become a CCPA service provider and state-law processor over sensitive data, unprepared. I would not buy today: 15 federal-only SNAP rules cannot answer for a real state household, and there is no entity, insurance or contract set.

## 2. Assumptions challenged
- **H1 hosted is a hard sell**: right result, partly wrong reason. The API is near-stateless (stores only org/action/package), an asset. Blockers are contractual: SNAP applicant data is restricted to program administration (7 USC 2020(e)(8), 7 CFR 272.1(c); moderately confident), and state contracts often require US-only storage and staff access (verify). Pakistan-based production access is a procurement problem, not a legal bar.
- **H2 pay for upkeep and sign-off**: agree, but you become warrantor of legal content. "A named reviewer approved" (in every NOTICE) is an FTC Act s.5 / state UDAP claim; if the reviewer is you, unqualified, it is deceptive. A wrong rule denying benefits invites negligent-misstatement claims.
- **H3 agencies too slow**: mostly agree (VPAT, StateRAMP-type demands, offshore-data clauses). Private benefits-tech vendors first.
- **H4 not an AI system**: do not rely on it. Colorado AI Act (SB 24-205) was delayed to 30 June 2026; I do not know if later amended, delayed or enjoined. Its "infer" test may exclude a deterministic evaluator, but California's CPPA ADMT regulations (finalised 2025, 2027 dates; verify) turn on computation replacing human decisionmaking, which a rules engine may meet. These laws bind customers, who push duties onto you by contract.
- **H5 differentiator**: provenance helps audit and denial-notice explanation, but buyers buy correctness for their state; sign-off is only as good as the signer.
- **Overbuilt**: hash-chained log, seeded faults, 41 diagnostics, metering. None is legally required.

## 3. REQUIRED to sell
Both models:
- Operating entity with liability cap; do not contract personally [buyer must-have].
- Employer IP/moonlighting release plus CLA/DCO [buyer must-have].
- Claims audit: "reviewed", "named expert", "deterministic", "no data stored" literally true [legal: FTC Act s.5].
- Scope manifest in each response: federal baseline, no state options, version, reviewer, date [legal + buyer].
- B2B only; no consumer screener. "Not legal advice" text does not cure unauthorized-practice risk [legal; state-specific, uncertain].
- Vulnerability policy, SBOM, signed releases [procurement].

Hosted only:
- DPA with CCPA service-provider terms (Civ. Code 1798.140(ag); 11 CCR 7051): purposes, no sale/share/combining, subprocessor flow-down, audit, deletion; equivalent terms in other states [legal, via customers].
- Sensitive data: disability, immigration status, medical expenses. WA My Health My Data Act may reach them (private right of action); I believe it exempts government contractors. Uncertain.
- Breach-notice plan, cyber/E&O insurance, SOC 2, US data residency [buyer must-have].
- Evidence for "no household data stored" (proxy, traceback, host logs).

## 4. NOT required / wasteful
- Self-hosted: CCPA/processor terms, breach notice, SOC 2 are not yours if you never receive data. Adopt a "send no real household data" support policy.
- HIPAA/BAA, GLBA, IRC 7216: not triggered for SNAP; GLBA and 7216 go live if you pivot to tax.
- ADA Title II / Section 508 (WCAG 2.1 AA; dates 2026/27, verify): reviewer app only, once a public buyer appears.
- Export controls: published open-source is generally outside the EAR (unverified; check encryption notification).
- OFAC: Pakistan is not comprehensively sanctioned; screen customers. Payment rails and US withholding forms are the friction (uncertain). DOJ bulk-data rule (28 CFR 202): Pakistan not a listed country (verify).

## 5. Deal-breakers
- Real household data in hosted API without entity, DPA, insurance or US-resident operator.
- "Reviewed/named expert" claims with one unqualified reviewer.
- Marketing 15 federal rules as "SNAP eligibility" without scope limits.
- Unresolved employer IP claim.

## 6. Commercial (estimates, flagged)
No license now. A fixed-fee self-hosted pilot of roughly USD 10-25k, with limited-liability MSA and a verifiable state pack. Hosted only with SOC 2 and DPA. Your legal setup: roughly USD 5-15k; insurance low thousands per year.

## 7. Top 3 changes
1. **Self-hosted first.** Hosted API becomes a synthetic-data sandbox (terms ban real data); restrict free-string inputs to enumerations.
2. **Make claims truthful and scoped.** Retire "named reviewer" until an independent qualified reviewer signs; add the scope manifest; stay B2B.
3. **Build the legal skeleton before features.** Entity, employer release, CLA/DCO, insurance, SECURITY.md/SBOM, MSA/DPA templates, counsel check on payments, tax forms, OFAC.
