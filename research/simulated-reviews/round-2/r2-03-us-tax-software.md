# R2 - #03 US tax-software CTO

## 1. Does anyone pay?
Not for the engine or SNAP. Credible buyers have change-detection pain:
- **#01 payroll VP**: $15-40k pilot, then $20-60k/yr, priced against displacing 0.25-0.5 of a compliance engineer. Headcount-anchored, so believable.
- **#06 govtech integrator**: $40-80k pilot, or $90-150/hr IV&V in an existing budget line.
- **#08 EU payroll**: EUR 15-30k pilot, EUR 1-3k/month/country (needs an EU partner).

I distrust $5-25k figures (#02, #16, #18): below my onboarding cost. Five-figure pilots are plausible; a recurring business is unproven.

## 2. Disagreements
- **#15 (privacy counsel)**: "7216 not triggered; Pakistan access is procurement, not law." True for SNAP. In tax, 7216 and Safeguards vendor oversight bind me regardless; support access, crash dumps and tracebacks count.
- **#17 (cross-border)**: "no entity or insurance before a small pilot." My onboarding requires a counterparty with E&O and cyber cover; a sole proprietor fails even at $15k. (#17's W-8BEN royalty trap is right: contract as services.)
- **#19 (OSS model)**: "sell signed packs, $1-3k/month." #02, #04, #10 and #11 note accountability stays with the buyer. Sign-off is evidence, not liability transfer, so the premium is smaller than #19 assumes.

**Changed my mind**: #20 plus the verified facts. Parameters sit outside the approval gate and 6 of 10 shipped values are empty. In tax, annual parameters are most of my update, so the gate misses what I would buy. #01 and #06 sharpened the wedge: oracle plus blast-radius report.

## 3. Attack on the consensus
"Annual maintained, signed packs" is a services business on IRS-set deadlines (the annual Rev. Proc. and form-instruction window, mid-season legislation), run by one person with a day job and no backup. One maintainer carries one or two packs; nobody priced capacity.

"Entity, insurance, pentest, SOC 2 first" front-loads $10-80k (#16's figures) before any buyer sees correctness evidence. Spend on evidence first.

"SNAP is only a demo" is too kind: a demo whose shipped package returns "unknown" fails. #02's unverified point that the 2025 reconciliation law outran the CFR applies doubly to tax: statute leads, regulations lag, so eCFR-only is wrong where I pay (unverified).

## 4. Final call
- **Domain**: US federal income-tax indexed parameters plus one credit (EITC or CTC), benchmarked on IRS worked examples.
- **Buyer**: engineering teams at tax and payroll software vendors.
- **Delivery**: self-hosted CLI in the buyer's CI, synthetic households only, sold as services. No return data keeps 7216 out of scope and Safeguards oversight light. Output is a clause-traced diff and impact report against the buyer's engine. TY2026 shadow pilot (Jan-Apr 2027), $15-40k fixed.
- **Stop**: the hosted API, metering and OpenFisca polish.

Verdict: still no buy today, but my reasoning changed: I would pay for the oracle and diff, not solo-vendor packs.
