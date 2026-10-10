# 10 - EU public-sector digital innovation lead (Rules-as-Code)

## 1. Verdict
Not needed by my agency as it stands: it solves "transcribe a US regulation", while my bottleneck is legal interpretation, maintenance and integration in my own language and formats. I would not buy from a solo non-EU founder; I would co-fund it through a grant or pilot, with an EU body between us.

## 2. Assumptions challenged
- **H1 hosted SaaS hard sell**: understated. A hosted API run outside the EU is an automatic no (GDPR Chapter V; Pakistan has no adequacy decision, to my knowledge). Self-hosted is fine. I'd never buy a vendor-written "rule pack" of my national law; interpretation is my legal department's job.
- **H2 pay for currency + expert sign-off**: wrong for public sector. Vendor sign-off has no legal weight; delegating interpretation is an administrative-law problem. I'd pay for training, integration, maintenance.
- **H3 government too slow**: half right. Procurement is slow; grants, hackathons, design-partner agreements and sub-threshold direct awards are not. Government is funder/co-developer, not customer.
- **H4 not an AI system**: plausible for the deterministic runtime (Art. 3(1), recital 12 exclude rules defined solely by natural persons), but the Commission's Feb 2025 guidelines make it case-by-case, and authoring uses an LLM. That claim belongs to my counsel, not your marketing. Outside the AI Act, GDPR Art. 22 and national automated-decision rules still apply. Annex III 5(a) timing may have moved under the Digital Omnibus; I can't confirm late-2026 status.
- **H5 differentiator**: provenance is Catala's core design; OpenFisca parameters carry references. Human sign-off is a process my legal team already runs. Genuinely distinctive: LLM-assisted authoring behind hard checks, and "unknown" instead of default denial. Unproven without a benchmark.

## 3. REQUIRED to sell
- [legal] GDPR: reviewer-identity audit log plus seeded-fault catch rates is employee-monitoring data (Art. 88; staff co-determination in several states). Need DPIA support, aggregate-only/disableable metrics, retention config.
- [legal] AI Act: counsel's scope memo; Art. 4 AI literacy for LLM-authoring staff; map review gate to Art. 14(4)(b) automation bias; a fully LLM-off path.
- [legal] Cyber Resilience Act (Reg. 2024/2847) if sold commercially: SBOM, vulnerability handling; reporting duties from Sept 2026 (verify).
- [buyer must-have] EU/UK ingestion: Akoma Ntoso (e.g. German LegalDocML.de), ELI identifiers, EUR-Lex Formex/HTML, legislation.gov.uk XML, national XML. Plus PDF/HTML: circulars aren't XML.
- [buyer must-have] Local, EU-hosted or open-weight LLM endpoint.
- [buyer must-have] One non-US benefit, benchmarked against hand-encoding in Catala/OpenFisca/RegelSpraak (time, errors).
- [buyer must-have] Named co-maintainers. Bus factor one is disqualifying.
- [procurement] Counterparty meeting Directive 2014/24 selection criteria (Art. 58 financial standing, insurance; ESPD). A solo founder can't; need an EU integrator/foundation/university as prime.
- [procurement] Multilingual UI and prompts; EN 301 549/WCAG for the reviewer app (Web Accessibility Directive 2016/2102, I believe, covers staff-facing apps).

## 4. NOT required / wasteful
- API keys, metering, hosted calc API before any customer exists.
- 462 tests and 22/22 mutation score as selling points; internal quality.
- Catala/LegalRuleML adapters; SNAP rule packs for EU buyers; hash-chaining (a signed append-only table passes my audit).
- Interoperable Europe Act (Reg. 2024/903) work: practical effect on such a tool is uncertain; mapping to the European Interoperability Framework is cheap, nothing more.

## 5. Deal-breakers
- Hosted-only, or non-EU-operated runtime holding personal data.
- US-only corpus.
- Vendor "sign-off" presented as authoritative.
- Mandatory US-hosted LLM.
- Unsupported "not AI" assertion.
- No EU entity, insurance or continuity plan.
- Unclear IP versus founder's employer.

## 6. Commercial (my estimates, not data)
No licence purchase (Apache-2.0). Fundable routes: NLnet/NGI-type grant (tens of thousands EUR; continuity after 2027 uncertain); pre-commercial procurement or innovation partnership (Directive 2014/24 Art. 14 R&D exemption / Art. 31), roughly EUR 50-100k for one national benefit's feasibility, via an EU prime; 3-month fixed-fee pilot EUR 15-40k under national direct-award limits (limits vary; EU thresholds roughly EUR 140k central / 216k sub-central, verify). Support EUR 10-30k/yr, only from an insured EU entity.

## 7. Top 3 changes
1. Prove it on EU law: one member-state benefit; Akoma Ntoso/legislation.gov.uk plus PDF/HTML; published benchmark against hand-encoded Catala/OpenFisca.
2. Position as community open source: contribute upstream, apply for grants, find an EU host organisation; park hosted API, metering, rule-pack business.
3. Ship a compliance pack: AI Act/GDPR memos, configurable staff metrics, local LLM option, SBOM, accessibility.
