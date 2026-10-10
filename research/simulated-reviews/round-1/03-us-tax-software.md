# 03 - US tax-software CTO

## 1. Verdict
Not needed in its current form: 15 SNAP rules from eCFR alone touch nothing in my annual cycle (IRC, Treasury regs, Rev. Procs, IRS form instructions, state law, MeF schemas). I would not buy today; I would run a free shadow-mode pilot on one federal credit as a differential-test oracle.

## 2. Assumptions challenged
1. **Hosted SaaS is a hard sell** -> For tax it is a near-ban. A calc API receiving income/dependents/SSN receives tax return information; sending it to a vendor is a disclosure under IRC 7216 and Treas. Reg. 301.7216-1 to -3, and offshore handling needs taxpayer consent with SSN-specific limits (verify current text, Rev. Proc. 2013-14). A Pakistan-operated host, or US-hosted with Pakistan admin access, fails my counsel.
2. **People pay for currency, sign-off, support** -> Agree. I pay for correctness proven against my test decks, turnaround days after IRS releases, and named credentialed (CPA/EA/tax attorney) liability. The engine is free to me.
3. **Gov too slow, private first** -> Agree. But my cycle is season-gated: TY2026 content is effectively frozen now (10 Oct 2026), so production is TY2027; only shadow runs fit TY2026.
4. **Not an AI system (EU)** -> Outside my market. Authoring inputs are public law, so no 7216 exposure there; exposure is runtime only.
5. **Differentiator is provenance/sign-off/unknown** -> My alternatives are in-house code and incumbent content vendors, not OpenFisca. "Unknown" maps to an interview prompt for a missing fact; I like that. Provenance helps audit defense, but neither beats a CPA signature.

## 3. REQUIRED to sell
- No return data ever reaches you: self-host only, telemetry off, logs/tracebacks scrubbed of SSN/income [legal: 7216; 6713].
- Written security documentation I can flow down: policy, vuln disclosure, SBOM, signed releases [legal: FTC Safeguards Rule, 16 CFR 314.4(f) service-provider oversight; GLBA; IRS Pub 4557 WISP].
- Test vectors compatible with my MeF Assurance Testing and Pub 1345 duties [legal/procurement].
- Source coverage: IRC (USLM XML), 26 CFR, Rev. Procs/Notices, IRS form/instruction PDFs, state DOR sources [buyer must-have].
- Parameter extraction for indexed amounts (now hand-encoded) [buyer must-have].
- Named US-credentialed reviewer plus E&O/cyber insurance [procurement].
- Language-neutral output (JSON plus test vectors); I do not run Python/OpenFisca in production [buyer must-have].
- US contracting entity, W-8BEN, MSA, source-code escrow (bus factor one), employer IP clearance [procurement].
- Update SLA tied to IRS release dates and mid-season legislation [buyer must-have].

## 4. Not required / wasteful
- EU/UK formats, Akoma Ntoso, EU AI Act work: zero value to me.
- Hosted API, API keys, metering: I self-host.
- OpenFisca export: I will not run it.
- Hash-chained log, seeded-fault testing: good evidence, not a purchase driver.
- 41 diagnostics, 462 tests: overbuilt versus 15 rules; coverage is the gap.
- SNAP corpus: a demo, not a tax asset.
- Per-response "not legal advice" text: my UI owns disclaimers.

## 5. Deal-breakers
- Any path for return data to leave my environment without 7216 consent.
- Hosted-only delivery.
- No credentialed tax signer, insurance, or US counterparty.
- No tax-law coverage.
- Content arriving after my freeze or after the season opens.
- Single founder with no escrow.

## 6. Commercial (my estimates, not data)
- Shadow pilot, one federal credit (EITC or CTC), TY2026, Jan-Apr 2027: free, or US$15k-40k fixed-fee, milestone-paid.
- If it matches my parallel tests: annual rule-pack/delta subscription ~US$50k-150k/yr for federal plus a few states, with SLA, escrow, E&O.
- Invoiced via a US entity; no per-call pricing.

## 7. Top 3 changes
1. **Re-wedge to tax as a verifier.** Ingest IRC (USLM), 26 CFR, Rev. Procs, form-instruction PDFs; build parameter extraction; encode one federal credit; benchmark against IRS worked examples; sell as an independent second implementation diffed against my engine with clause-level traces.
2. **Make "no taxpayer data" structural.** Sealed, signed, self-hosted rule packs only; scrub logs; draft a 7216/Safeguards vendor addendum; stop pitching the hosted API to tax buyers.
3. **Buy the credibility the founder cannot self-supply.** Contract a US CPA/EA reviewer, form a US entity or partner with a US firm, get E&O and escrow, clear employer IP, and ship an annual "what changed" diff with dated delivery commitments.

Flag: re-verify 7216 offshore/SSN rules, FTC breach-notice thresholds and Pub 1345; they may have changed by late 2026.
