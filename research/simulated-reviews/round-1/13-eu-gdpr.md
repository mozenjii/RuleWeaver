# 13 - EU data-protection lawyer (stress test, not legal advice)

## 1. Verdict
GDPR does not require this product, but it makes explainability valuable. I would not buy hosted today, and would pilot self-hosted only after the reviewer log is fixed and ADR-022's Art 22 reasoning is rewritten.

## 2. Assumptions challenged
- **H1:** Right result, wrong reason. Self-hosted removes the founder from GDPR only with zero access to personal data. Remote support makes him a processor and a Pakistan transfer.
- **H4 / ADR-022:** "Not an AI system" is irrelevant to Art 22, which covers any automated processing, including deterministic calculators. Approving rules in advance is not human intervention in the individual decision. SCHUFA (C-634/21) treats a determinative output as the "decision".
- **H2, H3, H5:** Agreed, but named sign-off puts experts' identities in a permanent record that clashes with erasure. Provenance helps Art 15(1)(h)/22(3); it is not "compliance".
- **"Stores no household data, so no GDPR":** Wrong. Receiving and calculating on data is processing (Art 4(2)). Not storing it is good Art 25 design only.
- **Scope:** SNAP covers US households; GDPR bites only via an EU/UK-established customer (Art 3(1)) or monitoring EU-located reviewers (Art 3(2)(b)).

## 3. REQUIRED to sell
Roles. Self-hosted, zero access: customer is controller; founder is neither controller nor processor. Hosted or data-access support: founder is processor (household and reviewer data) and controller (account/billing data). LLM authoring: clause text is public law, so no personal data and no Art 28 (verify prompts carry nothing else).

- **[legal] Art 28(3) DPA, subprocessors, Art 30(2) record, Art 33(2) breach notice.** Hosted or data-access support only.
- **[legal] Chapter V.** No adequacy decision for Pakistan as far as I know (verify). Remote access is a transfer (EDPB 05/2021): SCCs (Decision 2021/914) plus a transfer impact assessment (Schrems II, C-311/18) covering Pakistani state-access law. UK: IDTA or Addendum. Not needed for zero-access self-hosting.
- **[legal] Art 17 vs hash chain.** `store.py` hashes free-text `reviewer`, `note`, `edited_to` into an immutable chain; erasure breaks `verify_chain`, and hashing is not anonymisation. Fix: opaque reviewer ID in the chain, deletable mapping table, notes outside it.
- **[legal] Employee monitoring.** Per-reviewer `duration_seconds` and seeded-fault outcomes are performance monitoring (Art 88; German works-council co-determination; likely DPIA). Covert seeding needs Art 5(1)(a)/13 notice: say tests exist, not which.
- **[legal] Art 9.** SNAP inputs (SSI/disability, medical deductions) are health data; the customer needs an Art 9(2) condition. Art 22(4) bars special-category ADM without 9(2)(a)/(g). UK: Data (Use and Access) Act 2025 replaced Art 22 with Arts 22A-D (verify commencement).
- **[buyer must-have] Decision record.** `/evaluate` returns `package_id` but no package hash, chain head or rule version, so a decision cannot be re-run for an Art 15/22(3) request.
- **[buyer must-have] DPIA pack:** data flows, Art 9 note, workflow routing "unknown" and adverse outcomes to a human.
- **[procurement] DPO contact, EU hosting, 24/7 breach contact.** A part-time solo founder cannot meet 24-48h breach clauses.
- **[legal, uncertain] Art 27 representative.** Probably not needed for a B2B processor serving EU-established controllers; triggered if he is a controller under Art 3(2).

## 4. NOT required / wasteful
Founder DPO. Art 28 with LLM vendors for clause text. EU-US DPF. BCRs. ISO 27001/SOC 2 now.

## 5. Deal-breakers
1. Hosted EU/UK service run from Pakistan with no SCCs, TIA or EU region.
2. Reviewer identities un-erasable in the chain.
3. Marketing "Art 22 compliant" or "not AI, so exempt".
4. Undisclosed reviewer scoring.
5. No breach capacity when hosting.

## 6. Commercial (estimates, unverified)
I would pay low-thousands EUR one-off for a DPA/SCC/TIA/DPIA pack with a pseudonymised log, plus a modest annual fee for signed rule packs and zero-access support. Not for hosted. Founder-side: DPA legal review (low thousands EUR), representative service if needed (hundreds to low thousands EUR yearly).

## 7. Top 3 changes
1. Pseudonymise reviewers, add retention/deletion, per-person metrics off by default, ship notice text.
2. No hosting; zero-access support via a redacted bundle. If hosting later, EU region only.
3. Rewrite ADR-022, add package hash plus chain head to responses, get counsel's opinion before any compliance claim. Check pydantic's 422 does not echo household input.

Verify by late 2026: Digital Omnibus GDPR changes, DUAA commencement, EU-US DPF after the Latombe challenge.
