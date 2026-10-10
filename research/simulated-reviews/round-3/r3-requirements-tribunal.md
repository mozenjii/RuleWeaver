# R3 Requirements Tribunal

Counts use round-1 reports only (round 2 is cross-contaminated). "unc." = author marked uncertain. Dates and Pakistan-adequacy claims are unverified.

## 1. Required before the first paid pilot

**All models, all markets (free, do first):** written employer IP/moonlighting release (12 demands; contract matter, no statute cited); strike "named reviewer", "reviewed", "not AI" claims until code and a signer back them (13; FTC Act s.5, US; facts 5-6); make the artefact work (complete parameters, parameters inside the gate, fix edit, wire seeding; facts 1-3); one buyer-supplied oracle benchmark; B2B-only MSA, services not licence, liability cap.

**A. Self-hosted engine + packs**

| Market | Required |
|---|---|
| US | State HTML/PDF ingestion; SBOM, SECURITY.md, signed release; zero-data-access support; W-8BEN. Entity+E&O for regulated/public buyers (04,05,06), else at signed LOI. |
| UK | legislation.gov.uk point-in-time ingestion; insured UK partner or entity (09,12); Cyber Essentials (09,16; verify). |
| EU | EU entity or prime (08,10,11,14); CRA posture before paid packs (unc.); pseudonymised reviewer IDs, metrics off by default; DORA Art 30 clauses for financial buyers (unc.). |

**B. Hosted API** (rule: public text or synthetic data only; then none of this applies)

| Market | Required if real personal data |
|---|---|
| US | SOC 2 (Type I bridge), CCPA service-provider DPA (11 CCR 7051), US residency; BAA for PHI (45 CFR 164.504(e)); IRC 7216 bars tax data; SNAP confidentiality 7 USC 2020(e)(8) (unc.). |
| UK | UK GDPR Art 28 DPA, IDTA/Addendum for Pakistan admin access, DPIA support. |
| EU | EU region, Art 28 DPA, SCCs + transfer assessment, 24h breach contact, ISO 27001/SOC 2; Art 27 representative (unc.). |

**C. Services**

| Market | Required |
|---|---|
| US | MSA capped at 12 months' fees (#17); tested wire rail; UPL posture: attorney-reviewed, flat-fee reviewers, no revenue share (ABA 5.4; state-specific, unc.). |
| UK | Partner supplies PI certificate and named reviewer; B2B reverse charge (#17, unc.). |
| EU | EU/UK prime for public tenders (Directive 2014/24 Art 58; #10, unc.); zero-access GDPR; CRA probably not triggered without a supplied product (unc.). |

## 2. Contradiction rulings

1. **Hosted vs self-hosted.** Self-hosted by default: 18/20 want no customer data at the vendor (#07 hosts public text only). #09's round 2 retreats to "hosted by the vendor, not SaaS": the integrator hosts. Hosted personal data from a Pakistan-based solo operator triggers GDPR Art 28/Chapter V (unc.). Self-hosting is clean only with zero-access support (#13).
2. **"Unknown."** Return unknown + missing-fact list + reason code; the integrator sets per-variable policy (block, route to human, hold, fail closed); never default silently, including through export. Demanded by 6 (01,02,04,08,12,13). No statute requires it; GDPR Art 22 (SCHUFA C-634/21, unc.) makes human routing the real safeguard.
3. **Hash chain.** Not required as a mechanism (13 say not a purchase driver). Buyers need authenticated reviewer identity (04,07,16,20), exportable history, package hash + rule version per response (04,13). Keep it, pseudonymise reviewer IDs (Art 17 collision, #13), stop marketing it.
4. **Sign-off.** Make the signer role buyer-assignable. 15 want a credentialed signer; 3 (02,06,10) want their own staff; 04,10,11 say it moves no accountability (DORA Art 5). Buyer's staff for enterprise/public, partner reviewers for buyers without analysts. Founder never signs.
5. **Entity.** Not legally required (no statute cited); 18/20 demand it as procurement. IP release and claims fix now; entity/insurance at signed LOI with deposit (#17, #16 r2), earlier for regulated or public buyers (04,05,06,09,11), or use an insured partner prime. Get a broker quote now: insurability of a Pakistan-based sole proprietor is unverified (15,16,17).
6. **SOC 2/ISO, self-hosted.** Not legally required. 4 ask for it or equivalent (04,05,08,11); 6 say N/A (06,09,13,15,16,17). Answer "N/A, self-hosted" with SBOM, signing, disclosure policy, continuity plan. Banks still diligence self-hosting vendors (04,07,11): run regulated pilots on public text, non-production.
7. **OpenFisca.** Freeze, do not extend. 11 say not required; 3 keep (10,14,19). OpenFisca-Core is AGPL-3.0-or-later: customers serving generated packages over a network take AGPL terms. Label export lossy and AGPL-adjacent; opinion before EU sale (#19, unc.).
8. **Seeded faults.** Keep the capability, retract the claim until wired. 6 want published catch rates (01,07,11,12,14,20); per-person scoring is monitoring (GDPR Art 88, DPIA; BetrVG 87(1) Nr.6, #08; FR/NL unc.). Default aggregate, pseudonymised, off.
9. **Formats.** UK XML now only if the pilot is UK (10 of 20 round-2 final calls chose UK). EU later, per first EU buyer's source: 5 asked for EUR-Lex/Akoma Ntoso, but DE/FR/NL use national XML (#08). US pilots need HTML/PDF state sources (10 demanded).
10. **CRA.** LEGALLY REQUIRED (unc.) for paid EU packs/support shipped with the engine: Reg. 2024/2847 manufacturer duties; reporting from 11 Sep 2026, main duties 11 Dec 2027 per 14/16, dates unverified. Pure hosting likely outside (#19); #16 and #19 disagree whether splitting free engine from paid packs helps. EU counsel before the first paid EU deal.

## 3. Top 10 by independent demand

| # | Requirement | Demands | Class |
|---|---|---|---|
| 1 | Entity, liability cap, E&O/cyber | 18 (#17 timing dissent) | PROCUREMENT |
| 2 | No customer data at vendor | 18 (#09 dissent) | BUYER; LEGAL if hosted |
| 3 | Real buyer-jurisdiction content | 17 | BUYER |
| 4 | Continuity: second maintainer/escrow | 17 | PROCUREMENT |
| 5 | SBOM, signed releases, vuln policy | 15 | PROCUREMENT; LEGAL EU (CRA, unc.) |
| 6 | Ingest buyer's real sources | 15 | BUYER |
| 7 | Credentialed sign-off | 15 (3 against) | BUYER; not legal anywhere |
| 8 | Published external benchmark | 14 | BUYER |
| 9 | Update SLA / amendment-impact report | 13 | BUYER |
| 10 | Truthful-claims audit | 13 | LEGAL (FTC Act s.5) |

Next: employer IP release (12; sequenced first); DPA/SCC pack (11; only with hosting or data access).

**NOT REQUIRED / WASTEFUL:** API keys/metering (17 say so), diagnostics/mutation counts as sales points (12), OpenFisca polish (11), Catala/LegalRuleML, FedRAMP (06,16), ISO 42001/CE mark (14), pentest before production (only #16). AI Act: nothing required for the deterministic runtime if outside Art 3(1) (#14 gut 55-65%, unc.).
