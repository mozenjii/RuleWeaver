# Research

## `simulated-reviews/` — read this caveat first

These are the outputs of a **simulated** market, compliance and product review, run on
2026-10-10 with AI agents role-playing buyers, regulators' counsel and critics. **No real
customer, lawyer or investor was consulted.** Every price is a simulated estimate, and
agreement between participants is correlated: they read each other in round 2. Legal
points are flagged by their authors where uncertain. Nothing here is legal advice.

What the simulation *is* good for: a structured list of objections and requirements to test
against reality, and a set of claims about the code that were then checked directly.

| Round | What happened |
|---|---|
| `round-1/` | 20 independent reports: 7 US buyers, 5 EU/UK buyers and channels, 5 compliance specialists (GDPR, EU AI Act, US privacy, security/procurement, cross-border business), 3 critics (VC, open-source business model, technical due diligence). |
| `round-2/` | Each participant read the other 19 and rebutted them. |
| `round-3/` | A prosecutor ("nobody will pay"), a defender, a requirements tribunal, a product-scope panel, and a closing judgment. |
| `00-verified-facts.md` | Claims about the repository that were checked in the code, and which have since been fixed. |

## `REQUIREMENTS.md`

The requirements the reviews produced, de-duplicated and prioritised, each traced to the
reports that demanded it and tracked to done. Engineering work for the first usable
version is driven from there.
