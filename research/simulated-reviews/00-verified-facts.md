# 00 — Facts verified by the orchestrator against the code (read this first)

Round-1 participants made claims about the repository. These were checked directly:

CONFIRMED
1. The review app never seeds faults. `should_seed` / `register` / `record_seed` exist and are unit-tested,
   but no route in `src/ruleweaver/review/app.py` calls them, so the anti-rubber-stamping catch rate cannot
   be measured in real use. The docs claim more than the code does.
2. The "edit" decision always fails from the UI: the form offers it, the route never passes `edited_to`,
   and `ReviewEvent` rejects an edit without it (HTTP 400).
3. 6 of the 10 parameters in the shipped `examples/snap/rules.json` have no values (the published tables are
   supplied only in tests). Served as shipped, the headline eligibility answer is "unknown".
4. OpenFisca-Core is licensed AGPL-3.0-or-later (package metadata). RuleWeaver is Apache-2.0 and imports it
   only optionally; customers who serve generated OpenFisca packages over a network take on AGPL terms.
5. Docker HEALTHCHECK calls `/healthz`, which only the review app has; the calculation API exposes
   `/v1/health`. Running the image as the API fails its health check.
6. The API's NOTICE says rules were approved by "a named reviewer" but names nobody; today the only
   reviewer is the founder.
7. The audit hash chain is unkeyed SHA-256 stored in the same database; anyone with database write access
   can recompute the whole chain. One shared HMAC secret can mint a token for any reviewer name.

NOT VERIFIED (treat as claims, check before relying on them)
- Whether the 2025 federal reconciliation law changed SNAP eligibility so that 7 CFR text is out of date.
- Exact current status/dates of: EU Digital Omnibus changes to the AI Act, CRA reporting start, Colorado
  AI Act, UK Data (Use and Access) Act commencement, Pakistan data-protection law.
- All price ranges in the reports are simulated estimates, not market data.

FIXED SINCE ROUND 1 (commits on branch claude/project-continuation-8yt9bp, 31323e0)
- Fact 2: "edit" now works from the form, and an edit approves only the corrected rule (status
  edit_pending until the package holds it). Previously the log treated an edit as approval of the
  ORIGINAL rule — a latent gate bug, now closed with tests.
- Fact 5: /healthz is an alias in the calculation API too.
- Fact 6: the NOTICE no longer claims a named reviewer; every /evaluate response now carries a
  replayable record (package hash, review-log chain head, rules applied, engine version).
- Fact 1: README/STATUS now say seeding is built but not wired (catch rate always unmeasured).
STILL OPEN: facts 3 (empty tables), 4 (AGPL note), 7 (chain anchoring, shared HMAC secret), CSRF, supply-chain items.
