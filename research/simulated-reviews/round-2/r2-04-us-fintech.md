# R2 - #04 US fintech Head of Compliance

## 1. Does anyone pay?
Most credible: #01 (payroll) and #03 (tax), because their prices anchor to a displaced cost ($20-60k/yr against 0.25-0.5 of a compliance engineer; $50-150k/yr against content vendors). Then #07 (legal-ops): $20-40k pilot, $20-60k/yr, because change monitoring plus an obligation register is an existing budget line. I discount #12's revenue share and #18's equity talk: no anchor. Nobody pays for the engine, and nobody can buy sign-off today because there is no signer. A $15-40k pilot is plausible; recurring revenue is unproven. I cut my own estimate from $40-120k to $30-80k/yr.

## 2. Disagreements
- **#16 (security):** "SOC 2 is N/A when self-hosted." Not in a bank-partnered fintech. Anything computing a fee or limit is a model (SR 11-7), and the vendor is rated on key-person risk, BCP and change control regardless of hosting. "N/A" gets you rated high-risk, not exempt.
- **#17 (cross-border):** "US LLC and insurance are premature." Regulated buyers onboard (KYC/OFAC, W-8BEN, insurance certificate) before even a non-production pilot. Employer IP release first, agreed; entity and insurance before signing.
- **#07:** leading with employment/HR as "the founder's domain" is wrong. An HR-ops employee in Pakistan has no US multi-state credibility, and #01 shows that buyer has an in-house team.

**Changed my mind:** the verified facts and #20. I called the clause audit trail exam-valuable. As built, one shared HMAC secret mints any reviewer and a database admin can recompute the chain, so in an exam it is worse than emailed approvals. Also #11: supervisors do not ask for rules-as-code. I drop "exam-driven demand"; the demand is internal audit and change management.

## 3. Attack on the consensus
Weakest claim: "buyers pay for credentialed-reviewer-signed rule packs."
1. Sign-off does not move accountability (#10, #11); the bank and I keep it.
2. A vendor-hired attorney's review is not privileged advice to me, and its liability runs to a vendor who may be uninsurable (#16, #17). It is a worse version of a law firm's 50-state memo, which brings privilege and a balance sheet.
3. "Maintained packs" ignores my change control. Any update moving a fee, limit or disclosure goes through model change management and validation, so absorbing it can cost more than the pack fee. The value is the diff and impact report saying what to review. Price the change-impact service, not the pack.

## 4. Final call
- **Pursue first:** US; state consumer-finance obligations (EWA fee caps, disclosures, licensing triggers) for fintech compliance teams and their law firms. Self-hosted CLI producing a reviewed obligation register and change-impact diff, with a US law firm as signer and contracting party. Fixed-fee, 3-state, non-production pilot, which avoids full bank TPRM.
- **Stop:** runtime plumbing (API metering, OpenFisca export, more diagnostics), and any "named reviewer" wording until a qualified signer exists.
- **Verdict:** still no purchase today; audit-trail value is a liability until fixed, and my price is lower.
