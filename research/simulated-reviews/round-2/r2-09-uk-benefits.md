# R2 - #09 UK benefits calculator Product Lead

## 1. The basic question
The only need I believe is recurring change cost: re-checking which households move after each amending SI and the April uprating. Every report prices the engine and SNAP at zero. Most credible buyers: #12 Big-4 (GBP 20-50k pilot; they bring qualified signers and liability), #08 EU payroll (EUR 15-30k pilot, EUR 1-3k/month for impact reports), and me (GBP 8-15k, estimate). The price sits below a headcount and the pain repeats yearly. Ceiling: a small services niche, not a software business.

## 2. Disagreements
- **#10 (EU public digital):** "Never buy a vendor-written rule pack." UK councils and charities buy calculators as commodity; DWP interprets Universal Credit (UC), not them. Council Tax Reduction schemes are council policy that vendors encode for them. Your "no" fits national-law interpretation, not UK calculators.
- **#17 (cross-border advisor):** Entity and insurance are "premature before a small pilot." Not here. Housing-association and charity onboarding wants a company number, PI certificate and processor terms before a GBP 10k purchase order. A Pakistani sole proprietor fails at the form.
- **#02 (US nonprofit), #10:** "Sign-off must be mine / has no legal weight." True for firms with analysts. Small UK charities and housing associations have none, so they buy sign-off.

**Changed my mind:** #20 plus the verified facts. Uprating is a parameter change, yet parameters sit outside the approval gate, 6 of 10 are empty, and seeded faults are never wired. What I said I would pay for is the least built. #14: "solely by natural persons" is weak when an LLM drafts; I was too relaxed on H4.

## 3. Attacking the consensus
Weakest part: "self-hosted plus paid maintained packs". Self-hosting suits buyers with engineers (payroll, tax, banks), who say they already employ the experts and pay zero for software. Buyers who lack expertise and would pay for upkeep (small charities, housing associations, small councils) cannot run Python and Docker. The consensus customer exists only as an intermediary: the calculator vendor who embeds. Also, the credential assumption is US-shaped: as I understand it, benefits advice is not a reserved legal activity in the UK (verify), so a quality-assured welfare-rights adviser can sign, cheaper than a solicitor or CPA. And a "demo" whose headline answer is "unknown" is not a demo.

## 4. Final call
- **Domain:** UK, England first, UC amounts and annual uprating impact. One language, one XML source with point-in-time versions, open reuse licence, cheap Cyber Essentials.
- **Buyer:** UK calculator vendors and advice-sector integrators.
- **Delivery:** signed rule-pack JSON plus test vectors, hosted by the vendor. Not SaaS, not end-customer self-hosting.
- **Stop:** hosted-API, metering and OpenFisca work. Spend the time on parameter extraction, gating and sourced tables.

**Verdict:** direction unchanged, timing worse. Round 1: "would pay GBP 8-15k for a UC pilot." Now: a free shadow run first; I pay only after parameters are sourced, gated and parity-tested.
