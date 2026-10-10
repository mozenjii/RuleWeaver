# 06 - US govtech integrator (Practice Lead)

## 1. Verdict
Not required in my bids today, and I would not buy: 15 federal-only SNAP rules is a demo, and a one-person offshore vendor with a day job is a key-personnel risk I cannot put in a proposal. I would watch it, and fund a small pilot if it reaches state-level coverage.

## 2. Assumptions challenged
- **Hosted SaaS is a hard sell** -> Impossible, not hard, in eligibility work (household data, IRS Pub 1075 for tax data). Self-hosted is right, but the calculation API is overbuilt for me: I want compile-time artifacts (rules, traces, tests), not a runtime service.
- **People pay for currency, sign-off, support** -> I pay for hours, not licences; Apache-2.0 means $0 software. Vendors cannot sign off on policy; the state agency owns interpretation.
- **Government too slow** -> True for direct sales. Subcontracting under a prime is the only route, and it needs references you lack.
- **EU AI Act** -> Not my market. US analogue: AI-disclosure clauses in state contracts and state AI statutes (Colorado's, delayed; check status). Disclose authoring-time LLM use.
- **Differentiator** -> Traceability matters: requirements-to-rule-to-test traceability is a contract deliverable. "Unknown" is table stakes (systems already pend cases for missing verification). PolicyEngine already models SNAP with state variation.
- **Is it needed?** My pain is state manuals, FNS memos, waivers, legacy code and fast regulatory change, not CFR text alone. Differential testing of a legacy system against an independent rules model is the useful job.

## 3. REQUIRED to sell
- US entity plus SAM.gov UEI [procurement; 2 CFR 25 for federal-funded awards].
- Per-state vendor registration [procurement].
- Offshore clause review per contract [procurement]. Data-only clauses may allow public-law encoding from Pakistan; work-location clauses (common) bar it. Pub 1075 bars offshore access to federal tax information [legal]. State in writing that no production data is needed.
- Background checks/fingerprinting for staff with system access [procurement]; a Pakistan-based person may fail US-check requirements.
- WCAG 2.1 AA / Section 508 VPAT for the reviewer UI [legal: Section 508; ADA Title II web rule for state/local, check compliance dates].
- Cyber and professional liability insurance, teaming agreement, flow-downs [procurement]. 45 CFR 95 federal software-reuse terms favour Apache-2.0.
- SBOM, SECURITY.md, vulnerability disclosure [buyer must-have].
- Named US-based lead plus continuity (bench or escrow) [buyer must-have].
- Written IP clearance from the HR employer [legal: invention-assignment risk].
- One complete state SNAP slice with a published benchmark [buyer must-have].

## 4. NOT required / wasteful
- StateRAMP/GovRAMP, FedRAMP and SOC 2, while self-hosted and never touching state data.
- API keys and usage metering (for my use).
- EU/UK formats, Akoma Ntoso, LegalRuleML, Catala.
- OpenFisca export: good for researchers, irrelevant to state systems.
- Hash-chained audit and seeded faults: good but unproven; states run their own governance. Mutation testing and amendment-impact analysis are your IV&V hooks, so lead with them.

## 5. Deal-breakers
1. Federal-only, 15 rules, no state options (BBCE, utility allowances), deductions or allotment.
2. Sole offshore founder with a full-time job elsewhere.
3. No past performance or reference.
4. Any hosted path where case data leaves the state boundary.
5. Unclear IP ownership.

## 6. Commercial (all estimates)
- Licence: $0. I pay for services.
- Pilot: roughly $40-80k fixed fee to encode one state's SNAP income, deductions and benefit calculation from its manual, with traceability matrix and generated tests.
- Bid line item: roughly $90-150/hr blended SME/IV&V inside the policy-analysis workstream, well under 1% of the bid.
- Non-exclusive teaming agreement. Expect net 45-60, pay-if-paid and 5-10% retainage; a solo founder must fund that cash flow.

## 7. Top 3 changes
1. Pick one state and finish SNAP end to end. Ingest the state manual (PDF/HTML), not just eCFR. Publish a benchmark against the state's worksheets and PolicyEngine.
2. Reposition from "compiler/API" to "independent verification and traceability for legacy eligibility rules". Cut SaaS, EU and OpenFisca work from the roadmap.
3. Fix the company before the code: US LLC or US partner with a named policy SME, resolved employer IP, VPAT, SBOM, insurance quotes.
