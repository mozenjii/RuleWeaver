# R2 - #14 EU AI Act specialist (rebuttal)

## 1. Who pays
Nobody pays for AI Act relief. Four reports (07, 10, 11, 12) demand a classification memo; that is a cost of selling, not revenue. The most credible buyer is #09 (UK benefits-calculator vendor, GBP 8-15k fixed pilot, Universal Credit core proven against its live calculator): a concrete test (parity), a recurring event (April uprating), one language, structured point-in-time law (legislation.gov.uk), a private buyer, no AI Act. Next: #08 (EUR 15-30k) and #12 (GBP 20-50k), both conditional on partners supplying reviewers. All 20 said "would not buy today"; every price depends on things that do not exist (credentialed signer, entity, insurance, non-SNAP content). The engine is worth $0 to everyone.

## 2. Disagreements
- **#18, #11, #12** repeat "rules defined solely by humans." Verified facts 1-2 undercut that: the UI's edit decision always fails, so a reviewer can only accept or reject LLM-drafted rules, and no fault is ever seeded. For LLM-compiled packs, "solely by natural persons" is weaker than for the hand-encoded SNAP set. My gut on runtime-not-AI drops from ~65% to ~55% for compiled packs.
- **#11** says Annex III 5(b) targets banks' own models, "not encodable from law text." CCD2-style creditworthiness rules are encodable, and a runtime scoring a consumer is 5(b)-adjacent if it is an AI system. But the obligation-register use case (04, 07, 11) evaluates firms and products, not natural persons, so it sits outside Annex III 4, 5(a) and 5(b) whatever the classification.
- **#10** says "map the review gate to Art 14(4)(b)": that repeats ADR-021's error (Art 14 concerns overseers of a high-risk system in use). #10 and #11 are right that vendor sign-off carries no legal weight for public bodies or bank management, which sinks H2 for those buyers.

**Changed my mind:** #13 (Art 22/SCHUFA reaches deterministic calculators, so "not AI" buys little commercially). #08, #10, #07 (reviewer scoring is a GDPR Art 88/works-council issue I missed). #08 over-reaches in calling it Annex III 4: a catch-rate counter is not an AI system.

## 3. Attack the consensus
Weakest part: "self-hosted plus signed packs sheds regulatory exposure." Self-hosting removes processor status, not the CRA: paid packs and support look like commercial activity (#16, #19), with reporting duties reportedly live since 11 Sep 2026 (unverified). Worse, the founder's own docs hurt: ADR-021/022 state the product targets Annex III 5(a) benefits eligibility and "doubles as Art 14 evidence." Buyer counsel will read that as intended purpose and as the provider positioning itself as high-risk-grade, while the code does not deliver it (facts 1, 2, 6: no seeding, broken edit, "named reviewer" names nobody). The consensus compliance pack rests on claims the code cannot yet support.

## 4. Final call
**Pursue:** UK; Universal Credit core; private benefits-calculator vendors/integrators (#09); self-hosted container plus JSON/OpenFisca export; human-edited packs signed by a named, insured UK welfare-rights adviser; LLM authoring optional. EU only after CRA, GDPR and DORA packs exist.

**Stop:** publishing "Annex III / Art 14 / not an AI system" assertions in README and ADRs. Replace them with a counsel-reviewed intended-purpose and non-reliance statement.

**Verdict:** unchanged on buying (no, not today); lower confidence on runtime classification.
