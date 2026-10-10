# R2 - #12 Big-4 tax and regulatory technology partner

## 1. Who pays?
Nobody pays for the software; it is Apache-2.0 and every report prices it at zero. People pay for hours and assurance. The most credible buyer is #06 (govtech integrator): it pays by the hour ($90-150/hr, $40-80k pilot) for independent verification of legacy rules, which is how my firm buys too. Second is #09 (UK calculator vendor): GBP 8-15k pilot, with its live calculator as the ground-truth oracle. #03 (tax CTO, $50-150k/yr) names the biggest number but needs ingestion that does not exist. All figures are simulated and sit at roughly one consultant-month. I see no evidence of a recurring buyer beyond a pilot.

## 2. Disagreements
- **#07 (legal-tech PM):** "Build monitoring plus an obligation register, lead with employment compliance." That is the crowded category my firm already resells, and it deletes the founder's differentiator.
- **#19 (OSS model):** "Sell attestation via a credentialed partner." Attestation is a professional-liability product with an engagement letter, independence screen and firm rates, not a cheap add-on.
- **#14 (AI Act):** "Enter the EU via tax and VAT." Incumbents and official specs own it; #08 shows the bottleneck is parameters, not statute prose.

**Changed my mind:** #20 (technical diligence). I credited seeded-fault testing as quality evidence. Verified fact 1 says nothing seeds faults, so I withdraw that credit. #13/#08: scoring named reviewers is staff monitoring (works councils, GDPR Art. 88) in my own firm.

## 3. Attacking the consensus
The weakest part is "buyers pay for credentialed-reviewer-signed packs" at $10-40k. It assumes a signer exists. A qualified, insured reviewer carries the liability and takes the margin; the founder keeps a tooling fee worth $0. Sign-off does not transfer accountability: #02 wants the signature to be its own, #10 says vendor sign-off has no legal weight, #11 says the management body keeps accountability. So the pack is a cost centre, not a product. "Unknown" is also not a selling point in payroll or tax (#01, #08: it must yield a number or a routed hold).

## 4. Final call
- **Domain and buyer:** UK Universal Credit, bought by a UK benefits-calculator vendor (#09).
- **Why:** legislation.gov.uk is structured XML with point-in-time versions; April uprating recurs; the buyer's live calculator is a free oracle; no offshore-clause problem.
- **Delivery:** self-hosted library, fixed-fee GBP 10-25k pilot (my estimate), an insured UK welfare-rights reviewer subcontracted via a UK partner entity.
- **Gate before my name goes near it:** working fault seeding and a published parity result.
- **Stop doing:** the hosted metered API (keys, metering, multi-tenancy). It serves a SaaS with no customers.

**Verdict change:** I still would not buy or white-label. The fault-catch claim is now unproven, not a strength. I lower my pilot figure to GBP 10-25k for a founder-led job; GBP 20-50k applies only to a firm-delivered pilot.
