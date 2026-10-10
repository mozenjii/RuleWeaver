# 02 - Head of Product, US benefits-access nonprofit

## 1. Verdict
The need is real but you solve the cheap half: federal SNAP income logic is free in PolicyEngine-US; my pain is state variation, rule freshness and four programs, and you ship 15 federal SNAP rules. I would not buy today; I would evaluate change-impact and "unknown" handling free if you showed one state end to end.

## 2. Assumptions challenged
1. **Hosted SaaS is a hard sell.** For me yes: inputs are income, disability and immigration-adjacent facts, so any call leaving my infrastructure triggers a sub-processor review I would decline. Self-hosting suits me; nonprofits without engineers cannot self-host.
2. **People pay for upkeep and named sign-off.** Upkeep, yes. Sign-off, no: I employ policy analysts and want the signature to be mine. I would pay for freshness guarantees and analyst tooling.
3. **Agencies too slow; go private.** Misses my segment: nonprofits buy fast below small thresholds but spend restricted grant money, and my agency customers push security questionnaires to you.
4. **Probably not an AI system.** Unimportant to me. EU Annex III lists eligibility for essential public benefits as high-risk; a deterministic runtime likely falls outside the Art. 3(1) definition, but ask a lawyer. US state AI laws (Colorado's effective date has moved; check) turn on "consequential decisions".
5. **Differentiator is provenance, sign-off, unknown.** Unknown is genuinely valuable: turning a missing fact into "not eligible" discourages applying. Clause traces help analysts and auditors, not end users. PolicyEngine wins on coverage; you win only with proven accuracy and change tracking.
6. **Is the source right?** CFR is not current SNAP law. The 2025 federal reconciliation act changed SNAP and Medicaid eligibility, and regulations lag statute. eCFR-only ingestion may encode superseded rules. Verify.

## 3. REQUIRED
- State-level SNAP (broad-based categorical eligibility, state utility allowances, limits) plus Medicaid MAGI, WIC, LIHEAP for my states. [buyer must-have] Those rules live in state plans, waivers and manuals, not eCFR.
- Freshness SLA and a dated "rules valid as of" field in every response (SNAP changes each October, poverty guidelines annually). [buyer must-have]
- Published accuracy benchmark on known-answer households versus PolicyEngine-US. [buyer must-have]
- Data minimization: per-program "facts required" list; unknown acceptable for immigration status. [legal; verify] CCPA/CPRA treat immigration and health data as sensitive; Washington's My Health My Data Act may apply; agency data terms flow down.
- Wording that never discourages applying, plus your not-legal-advice line. [buyer must-have; deceptive-claims risk]
- Procurement pack: security questionnaire answers, vulnerability disclosure, SBOM, signed releases, cyber/E&O insurance, foreign-vendor tax forms. [procurement]
- Continuity: second named maintainer or escrow. [procurement]
- Plain-language, translatable explanations. [buyer must-have]

## 4. NOT required or wasteful (for me)
- Seeded faults; hash-chained audit log (git suffices).
- 41 diagnostics, mutation testing: I buy accuracy, not rigor theatre.
- Metering and API keys if self-hosted.
- Akoma Ntoso, EU/UK, Catala, LegalRuleML.
- OpenFisca export, unless it works with PolicyEngine-US (unsure it is compatible).

## 5. Deal-breakers
- Federal-only coverage; rules older than current law or without dated validity.
- One part-time maintainer, no SLA, no backup.
- Hosted service receiving household data without a DPA and sub-processor list; some agency-linked contracts require US-based PII access, which a Pakistan-based solo operator could not meet.
- "Official determination" framing, or silent defaults replacing unknown.
- No benchmark.

## 6. Commercial (estimates, not data)
- License: expect $0; PolicyEngine is free and funders favor open source.
- Fixed-fee pilot: roughly $10-25k, 3 months, one state, SNAP plus one program, scored against my known-answer cases.
- If it passes: annual maintained rule pack, perhaps low-to-mid five figures for my states, with a hard cap rather than per-call pricing (volume spikes at enrollment).

## 7. Top 3 changes
1. Drop the federal-15 story. Go deep on one state (SNAP plus WIC adjunctive or Medicaid MAGI), benchmarked against PolicyEngine-US and the state's calculator. Position as a verification layer.
2. Productize unknown: "minimum missing facts / next best question", facts-required lists, and October and January change-impact reports.
3. Add HTML/PDF ingestion for state manuals and USDA memos; confirm current-law correctness first. Stay self-hosted; skip multi-tenant SaaS and EU work until one US pilot is paid.
