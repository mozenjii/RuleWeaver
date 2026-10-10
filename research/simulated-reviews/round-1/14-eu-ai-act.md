# 14 - EU AI Act specialist (stress test, not legal advice)

## 1. Verdict
The AI Act neither requires RuleWeaver nor creates demand for it. The authoring LLM is an AI system (likely minimal/limited risk); the runtime is probably, not safely, outside Art 3(1). With zero EU/UK content no EU buyer can use it, so I would not buy now, only fund a fixed-fee pilot with a written classification posture.

## 2. Assumptions challenged
- **H4 (runtime not AI):** "Probably out" (gut ~65%), not safe. Recital 12 excludes rules "defined solely by natural persons"; "solely" is weak when an LLM drafts and humans approve, and collapses if your seeded-fault catch rates are low. Recital 12 also counts deriving "algorithms... from inputs": an LLM deriving rules from statute text fits, and a statically deployed ML-derived decision tree is still an AI system. Adaptiveness is only "may exhibit", so ADR-022's "no adaptiveness" is irrelevant. The Commission's Feb 2025 guidelines are non-binding; only the CJEU decides.
- **ADR-021 "doubles as Art 14 evidence":** overclaim. Art 14 covers overseers of a high-risk system in use (caseworkers), not rule reviewers at authoring.
- **ADR-022 timeline** (Omnibus "in force 27 Jul 2026", Annex III to 2 Dec 2027): I recall the Nov 2025 proposal's long-stop dates but cannot confirm adoption; verify in the OJ. Unsure on Art 4 AI literacy and any Art 50(2) grace period.
- **H1:** agree, sharper: hosting EU personal data from Pakistan makes you a third-country processor (GDPR Ch. V transfers, Art 27 representative).
- **H2:** mostly agree; buyers pay for evidence (trace supports GDPR Art 15(1)(h)/22(3); Art 86 if high-risk) and named accountability. Never sell "AI Act compliance".
- **H3:** Annex III 5(a) bites on public bodies ("by or on behalf of"). Private citizen-facing calculators and tax rules sit outside Annex III; credit 5(b), insurance 5(c), employment (point 4) matter only if the runtime is an AI system.
- **H5:** partly a liability: Catala/OpenFisca/PolicyEngine are hand-written, so their story is "no AI". You add LLM surface.

## 3. REQUIRED
- [legal] Runtime, if not an AI system: nothing under the Act.
- [legal] Authoring LLM: Art 2(12) open-source exemption excludes Art 5/50/high-risk uses. Art 50(2) marking arguably reaches generated text: stamp each proposal with model, version, prompt hash.
- [legal] Written intended purpose (Art 3(12)): not sole basis for decisions on individuals; Annex III uses need the customer's own assessment. Your marketing defines it.
- [legal] If ever high-risk: authorised representative (Art 22), Arts 9-15, 17, Annex IV, internal-control assessment, Art 49 registration. Not now.
- [legal] CRA vulnerability reporting (from 11 Sep 2026) if sold commercially.
- [procurement] Counsel-reviewed classification memo; data-flow diagram (public law text only to LLM); model-vendor terms; SBOM; EU/UK/US contracting entity; continuity/escrow for a one-person vendor; UK ATRS inputs for central government.
- [buyer must-have] Measured LLM precision/recall on held-out clauses, reviewer catch rate, one real EU/UK rule pack.

## 4. NOT required / wasteful
- Conformity assessment, CE mark, notified body, FRIA, QMS, ISO 42001 now.
- Art 50(1) disclosure (no chatbot).
- Treating 41 diagnostics and mutation testing as "AI Act answers": they earn buyer trust, not compliance.
- Legal opinion before a first private pilot.

## 5. Deal-breakers
- Marketing "AI-powered, decides eligibility" (rewrites intended purpose into Annex III).
- Asserting "not an AI system" as fact, on one definitional argument, without counsel.
- Any LLM in the runtime path, or customer data sent to an LLM.
- Hosted EU personal data from Pakistan without SCCs/representative.
- Unmeasured human review.

## 6. Commercial (guesses)
Software EUR 0 (Apache). I'd pay roughly EUR 10-25k fixed for one EU/UK rule pack plus classification memo plus named sign-off, then perhaps EUR 2-5k/month for currency and support.

## 7. Top 3 changes
1. Split the product: LLM authoring optional and separately packaged (customer's own key); runtime, IR, review, export ship LLM-free. Publish a position paper stating assumptions; correct ADR-022's adaptiveness and timeline claims.
2. Publish evidence: benchmark, reviewer catch rates, intended-purpose/limitations/logging pack; anchor the hash chain externally (a DB admin can rewrite a whole chain).
3. Enter the EU via non-Annex III domains (tax, VAT); add Akoma Ntoso/legislation.gov.uk ingestion before pursuing benefits agencies.
