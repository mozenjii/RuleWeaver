# R2 - #07 Senior PM, US legal-tech

## 1. Does anyone pay?
Nobody pays for software; two or three buyers might pay for attorney-reviewed content. Most credible: #04 (neobank compliance head, $20-50k pilot, $40-120k/yr per product line) because exams force an obligation register with named attorney sign-off; #12 (Big-4 partner, GBP 20-50k pilot) because he supplies reviewers; #11 (EU bank, EUR 10-30k PoC) as a slower later version. I do not believe the benefits buyers (#02, #05, #06, #09): grant money, free PolicyEngine, in-house analysts. All prices are simulated, from people who mostly said "I would not buy."

## 2. Disagreements
- **#18 (VC):** "$5-25k per jurisdiction pack" and "sell to benefit-screening vendors." That price cannot fund a credentialed reviewer plus a maintainer, and the segment is grant-funded.
- **#17 (cross-border):** entity and insurance are "premature." In my market the MSA, liability cap and E&O certificate are page one; #04 and #16 say nothing signs without them. Agree that employer IP clearance goes first.
- **#16 (security):** SOC 2/ISO "N/A for self-hosted." Banks still diligence the vendor (#04, #11).

Changed my mind: **#04** (most obligations are duties, not computations), so emit a register for every clause, not only computable ones. **#20** (seeded faults never called, "edit" broken, 6/10 parameters empty): I called fault-seeding a keep; as shipped it is a false claim (FTC Act s.5, per #15). **#01** (payroll vendors will not buy) sank my HR/payroll lead.

## 3. Attacking the consensus
Weakest: "buyers pay for credentialed-reviewer-signed packs." #10 and #11 say sign-off does not transfer accountability; #02 and #06 say the signature must be theirs. For my buyers it adds a UPL and fee-splitting problem: a non-lawyer vendor reselling attorney interpretations, with #12's proposed 15-30% revenue share, collides with ABA Model Rule 5.4 (lawyers sharing fees with non-lawyers). Pay reviewers flat fees, never rev-share. And the thing named wanted across #01, #04, #06, #11, #12 and #20 is change and impact analysis ("what moved, what does it touch"). Packs are a liability; impact reports are the product.

## 4. Final call
- **Domain and buyer:** US consumer-finance obligations (state earned-wage-access, fee-cap and disclosure rules, plus Reg E/Z/DD that eCFR already ingests) for #04-type compliance heads at fintechs and their partner banks.
- **Delivery:** self-hosted batch tool, output is an obligation register plus amendment-impact report, with a US law firm doing flat-fee named review. US only; no hosted API; EU/UK later.
- **Stop:** building the runtime side (hosted API, metering, OpenFisca export, more diagnostics). Spend it on state HTML/PDF ingestion and one pilot.

**Verdict change:** still would not buy today. Changed: I now see "executable rules" as secondary to a register-and-impact product; employment/HR drops from first to later; fault-seeding is withdrawn as a selling point until wired and measured.
