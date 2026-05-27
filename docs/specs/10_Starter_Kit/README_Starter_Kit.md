# Advokat AI — README Starter Kit

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

## Proposed repo structure

```text
advokat-ai/
  apps/
    web/
  services/
    api/
    worker/
  packages/
    schemas/
    policy/
    agent-core/
    ui-contracts/
  infra/
    docker-compose.yml
    migrations/
  docs/
  tests/
    e2e/
    integration/
    contract/
```

## Codex first task

Create repo skeleton with:
- package manager
- Docker Compose
- Postgres/Redis/MinIO
- FastAPI service
- Next.js app
- shared schema package
- first migration
- health endpoints
- README setup

