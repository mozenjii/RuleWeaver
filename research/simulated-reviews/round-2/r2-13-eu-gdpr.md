# R2 - #13 EU data-protection lawyer (not legal advice)

## 1. Does anyone pay?
Nobody pays for what exists. Every price depends on unbuilt content, a credentialed co-signer, insurance and an entity. Most credible:
- **#06 govtech integrator:** USD 40-80k pilot, then SME hours at USD 90-150/hr. They buy hours against a real bid line, not a licence.
- **#09 UK calculator vendor:** GBP 8-15k Universal Credit pilot, then GBP 10-25k/yr. They have a live calculator to test against and a fixed uprating deadline.

#03 tax (USD 50-150k/yr) is biggest, but needs a US CPA. All prices are simulated.

## 2. Disagreements
- **#15 and #16 ("self-hosted removes the processor role"):** Wrong. The review database holds reviewer identities, timings and notes in every deployment. Pilots and support put the founder in test households or DB dumps: processor role plus a Pakistan transfer. Self-hosting is clean only with a zero-access rule.
- **#09 ("UK-hosted stateless API plus DPA"):** Stateless is still processing, and Pakistan-based admin access is a restricted transfer. In-process or browser-side execution is the real fix.
- **#14 (Art 27 representative needed):** Overstated for a B2B processor.

**Changed my mind:**
- **#07:** Host public-text monitoring and authoring; run the evaluator customer-side. GDPR-clean, so my "no hosting" was too blunt.
- **Fact 1 (no seeding in the app):** Reviewer scoring is prospective. I downgrade it from deal-breaker to a DPIA gate; the live risk is docs claiming a control that does not run.
- **Fact 7 (one HMAC secret mints any reviewer):** Approvals can be attributed to the wrong person, an Art 5(1)(d) accuracy problem on top of erasure.

## 3. Attacking the consensus
The weakest part is "credentialed-reviewer-signed packs" sold through self-hosted fixed-fee pilots.
- The signer's identity goes into an immutable chain, and the signer has erasure and objection rights.
- Today's NOTICE (fact 6) says "a named reviewer" and names nobody: a misrepresentation risk.
- Counsel will not accept rule sign-off as meaningful human involvement in individual decisions under Art 22 (SCHUFA, C-634/21). Routing "unknown" and adverse outcomes to a caseworker does. The consensus over-sells sign-off and under-sells "unknown".
- Pilots are where the founder touches customer data, and nobody priced the DPA, SCC and TIA pack into the fee.

## 4. Final call
**Domain and buyer:** UK means-tested benefits (Universal Credit core), sold to calculator vendors (#09 type), with legislation.gov.uk point-in-time ingestion.
**Delivery:** in-process or browser-side library, zero founder access to personal data, a named insured UK welfare-rights reviewer, pseudonymised reviewer IDs, a UK entity, a fixed-fee pilot.
**Why UK first:** one language, structured XML, no Annex III exposure for a private vendor.

**Stop:** the hosted API, keys and metering as a product (park it as a synthetic-data sandbox), and the ADR-022 "defensible under Art 22" framing.

**Verdict changed?** Not on buying: no today, pilot yes. "No hosting" became "host public text only".
