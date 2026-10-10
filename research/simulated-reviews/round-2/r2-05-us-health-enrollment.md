# R2 - #05 Director of Product, US Medicaid/ACA enrollment navigation

## 1. Does anyone pay?
Barely, and never for the engine. Most credible: #09 (UK calculator vendor: GBP 8-15k pilot, GBP 10-25k/yr; April uprating deadline; a live calculator to test against) and #02 (benefits nonprofit: $10-25k pilot, one state). Each names an acceptance test and a recurring update event. #03's $50-150k needs tax coverage the founder lacks. I (health system or plan) am not credible near term: BAA, offshore-PHI clauses and insurance block even a pilot. Realistic outcome: one or two $10-25k pilots, not venture scale.

## 2. Disagreements
- **#06 (govtech):** "Unknown is table stakes." Eligibility systems pend cases; screeners and navigator tools mostly do not. "Unknown" is the feature I would notice.
- **#17 (cross-border):** "No entity or insurance before a small pilot." Covered entities and plans will not sign a BAA or MSA with an uninsured foreign sole proprietor. In my segment, entity plus E&O gates the pilot.
- **#15 (privacy counsel):** Self-hosted "barely touches" privacy law. Remote support, tracebacks and logs are how PHI reaches a vendor. Zero-access support must be designed.
- **Changed my mind:** #20's verified facts. I treated "named reviewer plus approval gate" as the pitch, but seeding is never called, edit fails, 6 of 10 SNAP parameters are empty, and the only reviewer is the founder. #06 also moved me: differential testing of an existing screener is a real job; clause traces for auditors was my weaker argument.

## 3. Attacking the consensus
The weakest part is "credentialed-reviewer-signed packs." #07, #10, #11 and #13 say sign-off carries no legal weight and risks unauthorized-practice claims; in Medicaid the state decides, so a vendor signature means nothing to my auditor. I buy tested equivalence to the state's result plus freshness by a date. Also, a $10-40k pilot does not cover the chassis the reports demand (legal setup, pentest, insurance, a paid reviewer), so the first customer loses money, and a part-time founder cannot hit fixed uprating dates. Finally, Apache-2.0 plus export lets my team fork the pack; the moat is update cadence, which is the least-built part (#20).

## 4. Final call
- **Domain/buyer:** US benefits eligibility, one state, SNAP plus Medicaid MAGI, from state manuals as well as eCFR; buyer is a benefits-screening nonprofit or vendor (the #02 type), not health systems.
- **Delivery:** self-hosted library or container, zero-access support, fixed-fee pilot roughly $10-25k (estimate), scored against the buyer's known-answer cases and PolicyEngine-US.
- **Stop:** building plumbing (metering, OpenFisca polish, diagnostics) and any "named reviewer" claim until someone qualified is named.

**Verdict:** still "would not buy today." What changed: who to sell to first (not me) and what to sell: tested, current state tables, not signatures.
