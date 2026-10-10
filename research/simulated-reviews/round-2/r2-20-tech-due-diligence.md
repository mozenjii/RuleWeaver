# R2 - #20 Technical due diligence

## 1. Will anyone pay?
Probably one or two small pilots, never for software. Credible payers hold a ground-truth oracle: #09 (UK calculator vendor, GBP 8-15k, parity against its live calculator), #02 (benefits nonprofit, $10-25k, known-answer cases), #06 (integrator, $40-80k, one state). They can score a pack without trusting the founder. I discount #01, #03, #04, #11: "free shadow run" is $0 and their conditions are unmet. All prices are simulated.

## 2. Disagreements
- **#16 (security)**: pentest, cosign, SLSA and CodeQL before a first pilot cost $5-20k against a $10-25k fee. A non-production self-hosted pilot needs SECURITY.md, SBOM, lockfile and the healthcheck, CSRF and limit fixes: days, not dollars.
- **#06**: SAM.gov UEI, state registration and VPAT are prime-contractor problems. Oracle, pilot, entity, in that order (#17).
- **#18/#19 ("verified content is the moat")**: #19 concedes pack copyright is thin, and an LLM plus a calculator can re-derive public law. The defensible assets are validated review history and an SLA: services.
- **#14**: EU entry via tax/VAT is where the IR is least proven (no currency, brackets or accumulators).

**Changed my mind:** #05 ("a parameter table with tests is cheaper than an LLM pipeline"). I listed measured LLM extraction as a must-have; for a first sale it is not. Also #13/#16: `/evaluate` returns no package hash or chain head, so no decision can be re-run, and `reviewer` is a free string inside an immutable chain.

## 3. Attacking the consensus
The weakest link is "maintained, credentialed-reviewer-signed rule packs". The repo has no pack: the service loads raw JSON plus a database log, with no signed, versioned, dated artifact. Parameters, the annually changing part, sit outside the gate. Approvals key on `rule_id`, not package. Reviewer credentials are not recorded. Ingestion never fetches and the structural source diff is unbuilt, so the October update is manual. The consensus is a services promise on a prototype, and margin is thin: signer subcontract, legal ($5-15k per #15) and insurance can swallow a $10-25k pilot. #02's unverified point that 7 CFR may predate the 2025 reconciliation law could mean the golden corpus encodes superseded rules.

## 4. Final call
**Domain/buyer/delivery:** US, one state's SNAP income and deductions, for a benefits-screening vendor or nonprofit (#02 type) that supplies its known-answer cases; self-hosted container plus a dated pack and an October change-impact report; a US-credentialed co-signer; the founder contracting as a services sole proprietor (#17). Smallest technical delta (15 rules exist; one state manual needs HTML/PDF ingestion) and the only path with an available oracle. Not UK Universal Credit: far larger, and PolicyEngine UK already models it.

**Stop:** all platform work (metering, API keys, OpenFisca polish, more diagnostics) until one external oracle comparison is published.

**Verdict:** still "would not buy"; the LLM requirement is dropped, the pack requirement is harder.
