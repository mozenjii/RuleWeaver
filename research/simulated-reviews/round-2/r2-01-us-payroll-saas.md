# R2 - #01 US payroll SaaS VP Eng: rebuttal

## 1. Will anyone pay?
Barely, and not for what is built. Most credible: teams that already hand-code rules, namely #03 tax-software CTO (shadow pilot $15-40k, then $50-150k/yr) and #08 EU payroll vendor (EUR 15-30k pilot, EUR 1-3k/month/country). Both want the same job I would pay for: a self-hosted independent second implementation plus change-impact diff. #04 (neobank, $40-120k/yr) is real money but 6-12 months of bank diligence. The $10-40k cluster is simulated people anchoring on each other, not market data. #20 says a state's payroll rules take 4-8 weeks with the tool versus 2-5 hand-coded; it wins only on re-review after amendments. That is a services-sized business: one or two pilots a year.

## 2. Disagreements
- **#17 (cross-border advisor):** "No entity, no insurance" works for an unpaid shadow run, not a paid one. I cannot enforce a judgment against an offshore sole proprietor, and I guarantee penalties to my own customers.
- **#16 (security):** Pentest ($5-20k), CRA file and SBOM before a first pilot is backwards. For an embedded library I run my own SCA and code review. Nobody opens a security pack for a product with zero payroll coverage; correctness evidence comes first (#20, #12 agree).
- **#07 (legal-tech):** "Lead with HR compliance, the founder's own domain." HR operations is not rule authorship, and incumbents own payroll/tax content (#18).

Changed my mind: #20 found parameters sit outside the approval gate and 6 of 10 shipped SNAP parameters are empty. Payroll is mostly parameters that change each January and July, so the gate skips the part that changes most. The orchestrator's finding that fault seeding is never called deepens this. #07 and #04 moved me on H1: hosted monitoring and diff over public text holds no PII, and I would accept it.

## 3. Attack on the consensus
Weakest pillar: "buyers pay for credentialed-reviewer-signed packs." #02, #10, #11 and #04 said sign-off does not transfer accountability or that the signature must be theirs. Buyers who do want it are small shops that cannot afford a credentialed reviewer, whose own E&O is unlikely to cover a one-person offshore publisher. At $20-60k per pack, reviewer cost and update SLAs eat the margin. Second: "entity, insurance, security pack first" is mis-ordered; a pilot needs an NDA, an IP release and a shadow-run scope. Third: "SNAP is only a demo" ignores that it returns "unknown" for the headline answer as shipped.

## 4. Final call
- **Domain:** US employment pay rules. Federal overtime regular-rate and garnishment caps first (eCFR-ingestible today), then minimum wage and paid sick leave for 3-5 states.
- **Buyer:** compliance-engineering teams at US payroll and HRIS vendors.
- **Delivery:** self-hosted CLI/library in CI, emitting language-neutral test vectors and a change-impact report against the buyer's own engine. Free shadow run, then a fixed-fee pilot. No calculation API, no pack subscription yet.
- **Stop:** building API keys, metering, OpenFisca and hash-chain polish. Put parameters inside the approval gate, wire real fault seeding, and publish a benchmark.

Verdict unchanged: I would not buy today. I am more pessimistic about the sign-off differentiator and more specific about the shadow-run offer.
