# R2 - #08 EU payroll vendor, Head of Product

## 1. Does anyone pay?
Barely, and nobody has actually been asked. Every price in the reports is simulated, and the near-identical USD 10-40k band looks like one shared prior, not 20 data points. Most credible: #01 (US payroll VP), because his price is tied to a cost: USD 20-60k/yr only if it displaces 0.25-0.5 of a compliance engineer, after a free shadow run. Second: #09 (UK calculator vendor, GBP 8-15k pilot, GBP 10-25k/yr pack), because scope is bounded and the source is structured. Note #01, #03, #11 and I all said "free first". #20 estimates 4-8 weeks with the tool versus 2-5 hand-coded for a new rule set; the tool wins only on re-review after amendments. That is the one thing I would buy. Nobody pays for the compiler.

## 2. Disagreements
- **#07 (legal-tech PM)**: "lead with employment/HR compliance, the founder's own domain." Wrong twice. An HR-operations job is not payroll-law credentials, and encoding the employer's own domain deepens the IP/moonlighting conflict #17 calls the largest legal risk. Obligation registers are mostly duties, not computation (#04's point); the tool extracts only computable clauses.
- **#14 (AI Act)**: "enter via tax/VAT, Akoma Ntoso first." EU tax is incumbent ground with official specs, and DE/FR/NL publish national XML, not Akoma Ntoso (to my knowledge). Classification memos do not drive my purchase; vendor-risk scoring does (#17 is right).
- **#10 (EU public)**: "park the rule-pack business, chase grants." Grants fund a hobby. A private vendor with a recurring update cost is the only buyer.

Changed my mind: #13 (Art. 17 versus a hash chain holding reviewer names; Art. 22 covers deterministic calculators, so my "not AI" comfort was beside the point) and 00-verified facts 1-3. I praised seeded-fault testing as "good science". It never runs, "edit" is broken, and 6 of 10 SNAP parameters are empty. That is a claim, not a feature.

## 3. Attack on the consensus
"Buyers pay for credentialed-reviewer-signed packs" is the weakest leg. Sign-off transfers no liability (#10, #11: the management body keeps it; payroll liability stays with employer or provider). The buyers with real budgets (#01, #02, #03, #10, #11) all said they keep the signature themselves. So the payer is whoever lacks staff, the founder holds no credential, and whoever supplies the reviewer takes the customer and the margin (#12 guesses 15-30%). The founder becomes a subcontracted engineer.

Second: "entity, insurance, pentest, security pack first" is circular. #15 and #16 put legal setup, pentest and insurance at roughly USD 12-45k in year one, about the whole pilot fee, and #16/#17 say a Pakistan-based sole proprietor may be uninsurable. Sequence instead: sell the pilot on a partner's paper (reviewing firm or integrator as prime, carrying insurance and DPA). Self-fund only the employer IP release.

## 4. Final call
- **Domain/buyer/delivery:** UK payroll rates-and-thresholds (PAYE, NIC, statutory pay, minimum wage; the April cycle) for mid-size payroll software vendors. Self-hosted CLI/library emitting change-impact and parity reports against the buyer's own engine; no API. Contracted through a UK payroll or accountancy partner supplying named sign-off. Caveat: some payroll specs are HMRC guidance, not legislation, and I am unsure of HMRC software-recognition rules; verify. Not DE/FR/NL: collective agreements are non-public PDFs, three languages, official specs. I am a second customer, not the first.
- **Stop:** building the hosted calculation API, metering and OpenFisca plumbing, and stop documenting unwired controls ("named reviewer", seeded faults) as features.
- **Verdict:** direction unchanged (not needed as a compiler; I would fund change-impact only), but hardened: no pilot from me until the gate works and one external-oracle benchmark exists.
