# R2 - #19 Open-source business model

## 1. Basic question
Nobody has shown they need the engine, and nobody has paid anything. The convergence on $10-40k is 20 simulated buyers sharing priors, not market evidence. The most credible buyer is #09 (UK calculator vendor): GBP 8-15k pilot, then GBP 10-25k/yr for a maintained Universal Credit pack. Why: a real budget line, one English-language structured source, small enough for a solo founder, and a buyer who explicitly separates "tooling GBP 0" from "content and update service". #01's anchor (a pack must beat 0.25-0.5 of a compliance engineer) is the best pricing logic in the set. Realistic outcome, as #18 says: a services-led niche around an open asset, not a licence business.

## 2. Disagreements
- **#16 security** wants pentest, SBOM and insurance before the first paid pilot. By #16's own figures (pentest $5-20k, insurance $2-8k/yr) that costs more than a $5-15k pilot. A self-hosted non-production pilot needs employer release, engagement letter, a tested wire path and SECURITY.md; the rest follows revenue. I also doubt "free engine, paid packs" escapes the CRA cleanly: packs execute inside the engine and support covers both.
- **#12 Big-4** proposes partner-reviewed packs with revenue share. Whoever owns the reviewer relationship owns the attestation brand, leaving you as subcontracted labour on an engine anyone can fork. Keep the mark (publish a trademark policy: "RuleWeaver-reviewed" only under your review standard) and have reviewers sign with their own keys.
- **#10 EU public** says position as community open source and park the rule-pack business. Grants fund a year; they do not pay a credentialed reviewer at every amendment. A supplement, not a model.

Changed my mind: **#17** (rule packs sold as "licences" risk royalty-style US withholding, so contract as services; a US LLC is premature) and **verified facts 6 and 7**. The attestation I called the moat is an unnamed reviewer on a shared-HMAC token and an unkeyed chain: forgeable today. Fact 4 also confirms OpenFisca-core is AGPL.

## 3. Attack on the consensus
The weakest part is "buyers pay for credentialed-signed packs".
- #02, #04, #06, #10 and #11 each say sign-off does not transfer accountability; it is diligence evidence. Willingness to pay is for currency, not signature.
- Packs are JSON encoding public law: thin copyright, Apache toolchain, copyable to ten sites. You cannot sell the bits; you sell time (dated releases, SLA, impact reports). Yet the update path is the least built part: 6 of 10 SNAP parameters are empty and parameters sit outside the approval gate.
- A credentialed reviewer at professional rates against GBP 10-25k/yr leaves thin margin. Unit economics are unmeasured.
- "Entity, insurance, security pack first" is gold-plating for pilot-sized deals (#17 agrees).
- Four buyers (#01, #03, #11 and #02) offered a free shadow run, not a fee. The realistic first price may be zero.

## 4. Final call
**Domain:** UK Universal Credit core. **Buyer:** benefits-calculator and advice-tool vendors (#09 type). **Delivery:** self-hosted pack, signed dated releases and an April uprating impact report, contracted as services, with a subcontracted UK welfare-rights reviewer signing under their own key. Legislation.gov.uk text is under the Open Government Licence (verify). Engine, corpus and review app stay Apache-2.0.

**Stop:** building monetization plumbing (hosted API, keys, metering) and OpenFisca polish. Label the export lossy ("unknown" is lost) and AGPL-adjacent.

**Verdict changed?** Licence verdict: no. What I would sell: yes. Not "attestation" or a named signer, but a signed, dated update service where sign-off is evidence, not liability transfer.
