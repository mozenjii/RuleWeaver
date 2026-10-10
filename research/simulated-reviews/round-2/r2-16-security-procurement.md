# R2 - #16 Vendor security and procurement reviewer

## 1. Is it needed, will anyone pay?
All 20 said "would not buy as built"; the only money on offer is for services around a pilot. Most credible: #09 (UK benefits-calculator vendor: GBP 8-15k pilot, GBP 10-25k/yr pack) and #08 (EU payroll vendor: EUR 15-30k pilot, EUR 1-3k/month per country). They own engines, want change-impact reports, self-host, and name sums that fit discretionary budgets. I discount #03 ($50-150k/yr) and #04 ($40-120k): they need new corpora, SOC 2/TPRM and 6-12 month cycles. Recurring revenue is unproven: #20 shows the update path (parameters) is the least-built part.

## 2. Disagreements
- **#17 (cross-border):** calls release automation and insurance premature. Signed, SBOM'd releases are the cheapest procurement evidence there is, and #01, #04, #06, #07 list insurance as a deal-breaker. But #17 changed my mind on a US LLC: Form 5472 penalties and uncertain Pakistani rules favour an insured partner as contracting prime.
- **#07 (legal-tech PM):** host monitoring, start SOC 2 readiness, lead with HR compliance. Anything hosted makes the founder a production vendor; SOC 2 readiness burns months for a buyer who is absent; HR compliance sits beside the founder's employer, magnifying the IP conflict.
- **#09 (UK):** a "UK-hosted stateless API" is still a Pakistan-run processor needing an IDTA for admin access. Library only.

Changed my mind: the orchestrator facts plus #20. I treated gaps as hygiene (SBOM, signing). Faults are never seeded, "edit" is broken, NOTICE promises a named reviewer who does not exist. A security pack over unwired claims is theatre; misrepresentation fails vendor review fastest (#15, FTC Act s.5). #13 also: free-text reviewer names in an immutable chain collide with erasure.

## 3. Attacking the consensus
The weakest part is the bundle "entity, insurance, IP release, security pack first" plus "$10-40k pilots".
- #01, #02, #03, #11 offer a **$0 shadow run** first; payment follows passing it. A $10-25k pilot roughly equals pentest plus legal setup (#15: $5-15k) plus insurance, so early pilots lose money.
- Sequence by gate. Shadow run: employer release (the true gate), written no-data scope, SECURITY.md, SBOM, signed release. Entity, insurance, pentest come with the first paid production contract.
- "Credentialed-reviewer-signed packs" assumes a signer and an insurer exist; neither does. Nobody has tested whether a Pakistan-based sole proprietor writing eligibility rules is insurable. The seller of sign-off is the partner (#12, #08); the founder is a subcontractor under the prime's flow-down.

## 4. Final call
- **Pursue:** UK means-tested benefit (Universal Credit core plus uprating) from legislation.gov.uk XML; buyer a UK benefits-calculator vendor (#09); founder subcontracts under an insured UK partner supplying the named welfare-rights reviewer; self-hosted library, zero data access, GBP 8-15k fixed pilot. Smallest procurement (Cyber Essentials), no CRA on UK-only sales (UK cyber legislation uncertain), none of SNAP's Pub 1075 or work-location bars.
- **Stop:** building the hosted calculation API (keys, metering, `/v1/validate`). Most reports call it unwanted, and it alone makes the founder a processor needing SOC 2.
- **Verdict:** direction unchanged (self-hosted pilot only); severity raised from "not procurable" to "not yet truthful". Wire the gate and correct the claims before any security pack.
