# Advokat AI — MASTER TEMPLATE README

**Package version:** Codex-ready developer package v0.4  
**Date:** 2026-05-27  
**Product class:** Legal AI case workspace / juridisk kontrollplattform  
**Release model:** No MVP. Build toward Pilot Candidate, then Release Candidate, then Official Release.

## Binding product premise

Advokat AI is a legal operating system for document-driven case work. The user works inside one calm, source-controlled case room. Internally, specialized agents help with documents, OCR, facts, evidence, chronology, legal sources, risk, drafts and quality control.

The first shippable milestone is **Pilot Candidate**, not MVP. Pilot Candidate must be safe for real legal documents inside controlled pilot agreements. Official Release requires full Definition of Done, legal sign-off, security sign-off, compliance sign-off, QA evidence and operational readiness.

## Non-negotiable rules

1. No factual claim without source or explicit `missing_source` status.
2. No critical action without preview and explicit approval where required.
3. No final export without control gate.
4. No hidden AI uncertainty.
5. No shared memory across cases.
6. No unlogged critical operation.
7. No AI-generated legal conclusion presented as authoritative legal advice.
8. Human legal responsibility remains with the user/organization.
9. Every material operation must be traceable to actor, case, object, version and source basis.
10. System design must minimize user cognitive load and make complex legal work feel manageable.

## Canonical release phases

| Phase | Name | Purpose |
|---|---|---|
| 1 | Foundation | Core architecture, case isolation, document pipeline, audit, permissions and source model |
| 2 | Pilot Candidate | Real documents, controlled pilot users, source graph, drafts, control gates and legal assistant UX |
| 3 | Release Candidate | Full QA, security, compliance, performance, legal review and operational hardening |
| 4 | Official Release | Public release-ready version with complete Definition of Done |

## How Codex should use this package

Codex must treat this folder as the implementation authority. When conflicts occur, use this priority order:

1. `00_START_HERE/Document_Priority_and_Source_of_Truth.md`
2. `11_Handoffs/CTO_Developer_Handoff.md`
3. `04_Technical/Canonical_Domain_Model_v1.md`
4. `04_Technical/API_Specification.md`
5. `04_Technical/SQL_Schema_v1.sql`
6. `06_QA/Definition_of_Done.md`
7. Product/design/operations/security documents

Codex must not invent conflicting architecture. If a needed choice is not specified, use the default decisions in this package and record the assumption in `09_Project_Control/Decision_Log.md`.

## Binding architecture decisions

| Area | Decision |
|---|---|
| Repo | Monorepo |
| Frontend | Next.js App Router + TypeScript + Tailwind + shadcn/ui |
| Backend API | Python FastAPI |
| Workers | Python workers with Celery/RQ-compatible queue abstraction |
| Database | PostgreSQL with pgvector extension |
| Cache/Queue | Redis |
| Object storage | S3-compatible storage |
| Search | Postgres full-text + vector search first; OpenSearch optional later |
| OCR | Provider interface; local Tesseract/PyMuPDF for dev, cloud OCR optional for production |
| LLM | Provider adapter interface; no provider-specific business logic outside provider layer |
| Auth | OIDC/SAML-ready auth abstraction; default implementation can be Auth0/Clerk/Supabase depending owner decision |
| Deployment | Docker Compose for local, Kubernetes or managed containers for production |
| Observability | OpenTelemetry traces, structured JSON logs, metrics, audit events |
| Secrets | Managed secret store in production; `.env.example` only for local |
| Data isolation | Tenant + case isolation enforced at DB query, API policy and object storage path levels |

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

---

# v0.4 Codex execution update

This package now contains a Codex-first implementation layer.

Most important files:
- `AGENTS.md`
- `00_START_HERE/CODEX_MASTER_INSTRUCTION.md`
- `05_Delivery/Codex_PR_Backlog_Exact_Build_Order_v1.md`
- `04_Technical/OpenAPI_Pilot_Candidate_v1.yaml`
- `04_Technical/SQL_Schema_Pilot_Candidate_v1.sql`
- `03_Design/AI_Assistant_UX_Contract_v1.md`
- `04_Technical/Assistant_Architecture_and_Actions_v1.md`
- `06_QA/Test_Matrix_Codex_Executable_v1.md`

Codex should build exactly according to these instructions and should not reinterpret the project as an MVP.
