# 08 - EU payroll vendor, Head of Product (DE/FR/NL)

## 1. Verdict
Not needed by me as built: my pain is annual upkeep of parameters and collective agreements against official specs (German BMF Programmablaufplan, French DSN, Dutch loonaangifte), not turning statute prose into rules, and none of my sources are ingested. I would not buy from a solo non-EU founder for production; I would fund a small self-hosted pilot of change monitoring and impact analysis.

## 2. Assumptions challenged
- H1 (SaaS hard sell): understated. Employee data never leaves my stack; I embed engines as libraries. A hosted API is a non-starter.
- H2 (pay for currency and sign-off): half right. Sign-off must come from a locally qualified, insured, DE/FR/NL-speaking party, not a solo founder in Pakistan.
- H3 (private first): agree for payroll.
- H4 (not an AI system): plausible (Art. 3(1), recital 12: deterministic execution), but I am not a lawyer. It ignores Annex III point 4 (employment): seeded-fault scoring of reviewers could itself be worker evaluation. High-risk dates may have moved under the digital omnibus; verify. Bigger exposures are GDPR, CRA, contract liability.
- H5 (differentiator): wrong competitors. My alternatives are in-house encoding, official specs and incumbent payroll engines. "Unknown" is a problem: payroll must yield a payslip or a defined hold state.
- Deeper: German Lohnsteuer is an official algorithm (PAP); SV ceilings come by ordinance. Parameters and official specs, not prose for an LLM.

## 3. REQUIRED to sell
- [legal] GDPR Art. 28 DPA and Art. 32 TOMs if the vendor ever touches employee data (support, logs). Remote access from Pakistan is a Chapter V transfer: SCCs plus transfer assessment (no adequacy decision for Pakistan, to my knowledge). Art. 27 representative: unsure it applies to a pure B2B processor; get advice. Payroll holds Art. 9 data (church tax, union dues, sickness).
- [legal] Cyber Resilience Act (Reg. 2024/2847): a commercial open-source supplier is a manufacturer. Reporting duties from about Sept 2026, rest Dec 2027 (verify). Needs vulnerability handling, SBOM.
- [legal] Works councils, when I deploy the review app on my own staff: BetrVG 87(1) Nr. 6, French CSE consultation (L2312-38, unsure), Dutch WOR art. 27 (sub-clause unsure). Scoring named reviewers triggers this; default to aggregated, pseudonymised metrics.
- [procurement] EU contracting entity, professional-indemnity and cyber insurance, ISO 27001 or equivalent, pen-test, NIS2 supplier questionnaire, continuity/escrow plan (Apache-2.0 covers code, not rule packs), DE/FR/NL docs.
- [buyer must-have] Real sources: gesetze-im-internet XML, Legifrance/KALI (DILA XML), wetten.overheid.nl BWB, Staatscourant, plus PDFs for collective agreements (many not openly published in DE). Akoma Ntoso is largely irrelevant nationally.
- [buyer must-have] A path to official channels (ELStAM/DEUEV via ITSG, DSN, Belastingdienst). Whether national certification of payroll software is mandatory: unsure; verify.
- [buyer must-have] Shadow-run on my regression corpus with zero unexplained diffs.
- [buyer must-have] Defined fallback when a value is "unknown".

## 4. NOT required / wasteful
OpenFisca export (no payroll value). SNAP content (zero transfer). Hash-chained audit log, API keys and metering if embedded as a library. UK/US formats before one EU country works. 41 diagnostics and mutation testing: overbuilt for a pilot. Seeded-fault scoring: good science, works-council liability unless anonymised.

## 5. Deal-breakers
- Employee data to a hosted API run by one non-EU person without DPA/SCCs.
- "Reviewed rule packs" without a named, insured, local-language expert.
- No DE/FR/NL rule set and no benchmark against an official spec.
- No continuity plan; founder's full-time HR-ops job (IP or moonlighting clause) will surface in due diligence.
- "Unknown" with no operational fallback.

## 6. Commercial (my estimates, unvalidated)
- Pilot: fixed fee EUR 15-30k, 8-12 weeks, self-hosted: one country's annual parameter set plus diff/impact against my engine.
- Ongoing: EUR 1-3k per month per country for monitoring and impact reports, only with SLA and insurance.
- No engine licence fee (Apache-2.0; I can fork). Full procurement: 6-9 months.

## 7. Top 3 changes
1. Reposition as a change-monitoring, impact-analysis and provenance layer for payroll vendors. Start with parameters (ceilings, rates); ingest one real DE/FR/NL source; benchmark against a golden set.
2. Build the trust structure: EU partner (payroll or law firm) as named reviewer and contracting entity, DPA/SCC pack, CRA posture, library-only delivery.
3. Define payroll-grade "unknown" (hold and manual-case states) and make reviewer metrics works-council-safe by default, with BR/CSE/OR documentation.
