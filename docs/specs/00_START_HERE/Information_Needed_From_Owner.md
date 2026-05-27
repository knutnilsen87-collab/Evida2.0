# Information Needed From Owner

This package is intentionally detailed enough for Codex/dev team to start. The items below should still be decided by the owner before production hardening. Defaults are provided so development is not blocked.

## P0 — must decide before Pilot Candidate

| Decision | Why it matters | Default in package |
|---|---|---|
| Primary jurisdiction(s) | Legal source handling, language, templates, disclaimers | Norway first, EU privacy/compliance |
| Hosting region | Personal data and legal document storage | EU/EEA region only |
| Document storage provider | Real documents require secure object storage | S3-compatible EU bucket |
| Auth provider | Login, MFA, roles, enterprise access | OIDC/SAML-ready abstraction |
| LLM provider policy | Whether legal docs may be sent to external AI APIs | Provider abstraction, no training, no retention where contract allows |
| OCR provider | Accuracy/cost/privacy tradeoff | Local/dev OCR + pluggable production OCR |
| Pilot customer type | Access model and onboarding | Law firm/internal legal team |
| Data retention rules | Legal/compliance and deletion behavior | Configurable per tenant/case |
| Human sign-off owner | Who may approve export/legal output | Case owner or appointed legal reviewer |
| Brand/product language | UI/copy tone | Norwegian first, English-ready |

## P1 — must decide before Official Release

| Decision | Why it matters | Default in package |
|---|---|---|
| Legal source integration | Accuracy of laws/cases | Manual verified legal source object first |
| Client portal | External collaboration risk | Post-pilot unless explicitly approved |
| Bates standard | Court/exhibit practice varies | Configurable label pattern |
| Audit export format | Enterprise/compliance needs | JSON + CSV + PDF report later |
| Pricing/packaging | Product operations | Not specified for dev |
| Support and incident SLA | Operations | Draft policy included |
| AI Act classification review | Compliance | Required release gate |
| DPIA owner | Privacy compliance | Required release gate |

