# 16 - Vendor security and procurement review

## 1. Verdict
Security evidence is required to sell this, and the product is not yet procurable: no disclosure policy, SBOM, signing, pentest, insurance or continuity plan; bus factor one. Self-hosted, I would run a fixed-fee non-production pilot; I would not approve a hosted version holding household data.

## 2. Assumptions challenged
- **H1 hosted is hard:** agree. Income, citizenship and disability data make you a processor (DPA, SOC 2/ISO). No EU adequacy decision for Pakistan as far as I know (verify); many US state contracts bar offshore access (IRS Pub 1075; SNAP confidentiality, 7 CFR 272.1(c) - verify). Self-hosting removes processor role, hosted-ops audits, SLAs, residency; it keeps supply chain, CRA, vendor viability, remote-support access, rule-pack integrity, liability.
- **H2 pay for upkeep:** agree. Paid support or packs around Apache-2.0 likely count as "commercial activity" (CRA recital 18, as I recall): you are a manufacturer, not a steward.

## 3. REQUIRED
- [legal] CRA (Reg. 2024/2847): reporting duties apply from 11 Sep 2026 (live now); main duties 11 Dec 2027. Commercial EU sales: SBOM, disclosure policy and contact, free security updates (5-year support period), technical file, EU declaration (self-assessment, probably). Fines up to EUR 15M or 2.5%. UNSURE: representative/importer for a non-EU direct seller; Digital Omnibus changes; whether the library alone is steward-only.
- [legal] US federal: SAM.gov UEI; SSDF attestation (EO 14028) was loosening in 2025-26 - verify.
- [procurement] SECURITY.md, security.txt, role mailbox on your own domain (pyproject lists a personal Gmail).
- [procurement] Per release: CycloneDX/SPDX SBOM, cosign-signed image and wheel, SLSA provenance, hashed lockfile, digest-pinned base, vulnerability scan.
- [procurement] Third-party pentest (review app, API, image) with remediation letter before first paid production use.
- [procurement] CAIQ v4 (STAR L1 free) and SIG Lite, answered "N/A, self-hosted".
- [procurement] Tech E&O plus cyber, commonly $1-2M with certificate. A Pakistan-based sole proprietor may be uninsurable by standard carriers; eligibility decisioning may be excluded.
- [procurement] Continuity: engine escrow is moot (Apache-2.0). Needed: escrow or perpetual licence for proprietary packs, runbooks, named backup maintainer, key-person clause.
- [procurement] IP chain of title: employer release (founder is employed full-time).
- [buyer must-have] UK Cyber Essentials (cheap; UK public buyers often require it - verify).
- [buyer must-have] Repo fixes:
  - Dockerfile: floating base tag; HEALTHCHECK hits `/healthz` but `serve` exposes `/v1/health`; API deployment undocumented.
  - release.yml: write token held during unpinned `pip install` and pytest; mutable action tags and `:latest`; no SBOM, signature, scan. tests.yml: no `permissions:`, CodeQL, pip-audit, Dependabot. pyproject: `>=` floors.
  - api.py: `/docs` open; no rate or body limits; `/v1/validate` runs the full validator on arbitrary JSON; each `/evaluate` reloads the whole audit log; no key expiry; no access logs.
  - review app: no CSRF/Origin check on `POST /rule/{id}/decide`.

## 4. NOT required / wasteful
- SOC 2 and ISO 27001 for self-hosted only: no law requires them; buyers accept N/A plus compensating evidence. If hosted later: Type I as bridge, then Type II; EU public buyers favour ISO 27001:2022. Premature.
- FedRAMP/StateRAMP: cloud services, not self-hosted software.
- NIS2 does not regulate you directly; it arrives as supplier clauses.
- Engine escrow, bug bounty, red team, FIPS, HECVAT. The 462 tests are not a pentest substitute.

## 5. Deal-breakers
- No disclosure policy, SBOM or signing.
- Hosted household data without SOC 2/ISO or US residency.
- No insurable, suable legal entity; refusal of liability caps.
- One employed person, no backup, on a production approval path.
- "Named reviewer" sign-off is forgeable: one shared HMAC secret mints any reviewer, and the audit chain is unkeyed SHA-256 in the same database, so anyone with DB write can recompute it.

## 6. Commercial (estimates, flagged)
Fixed-fee self-hosted pilot with a rule pack: about $5-15k. Maintained pack plus support: low-to-mid five figures per jurisdiction per year, once pentest letter, SBOM and insurance exist. Hosted API: nothing today. Your cost: pentest $5-20k, insurance $2-8k/yr, Cyber Essentials under $1k, SOC 2 year one $25-60k (defer).

## 7. Top 3 changes
1. Supply-chain release: SECURITY.md, lockfile, digest pins, split least-privilege release job, SHA-pinned actions, SBOM, cosign, SLSA, scan, Dependabot/CodeQL; fix healthcheck, limits, CSRF.
2. Defensible sign-off: OIDC identities, signed externally anchored audit checkpoints, written trust model.
3. Commercial posture: self-hosted only, free engine separate from paid packs (CRA scope), US/EU/UK entity or reseller, insurance, backup maintainer, one pentest before first paid pilot.
