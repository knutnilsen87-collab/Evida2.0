# Advokat AI — Technical Architecture Spec

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

## Canonical domain objects

| Object | Purpose | Minimum required fields |
|---|---|---|
| `Case` | Isolated legal workspace | `id`, `tenant_id`, `title`, `case_type`, `jurisdiction`, `status`, `created_by`, `created_at`, `updated_at` |
| `CaseMember` | Case-level access | `case_id`, `user_id`, `role`, `permissions`, `added_by`, `created_at` |
| `Document` | Source file | `id`, `case_id`, `filename`, `mime_type`, `storage_uri`, `sha256`, `page_count`, `status`, `uploaded_by`, `created_at` |
| `DocumentVersion` | Immutable version record | `id`, `document_id`, `version_no`, `sha256`, `storage_uri`, `created_by`, `created_at` |
| `Page` | Verifiable document page | `id`, `document_id`, `page_number`, `ocr_status`, `text_hash`, `image_hash`, `bates_label`, `exhibit_label` |
| `Chunk` | Analysis unit | `id`, `document_id`, `page_id`, `chunk_index`, `text`, `text_hash`, `embedding_ref`, `source_span` |
| `SourceRef` | Citation anchor | `id`, `case_id`, `document_id`, `page_id`, `chunk_id`, `quote`, `bates_label`, `confidence` |
| `FactClaim` | Factual assertion | `id`, `case_id`, `claim_text`, `claim_status`, `source_refs[]`, `confidence`, `created_by`, `review_status` |
| `TimelineEvent` | Chronology item | `id`, `case_id`, `event_date`, `date_precision`, `title`, `description`, `fact_claim_ids[]`, `source_refs[]` |
| `EvidenceItem` | Evidence object | `id`, `case_id`, `type`, `title`, `supports_claim_ids[]`, `weakens_claim_ids[]`, `source_refs[]`, `risk_flags[]` |
| `Argument` | Legal argument structure | `id`, `case_id`, `position`, `elements[]`, `fact_claim_ids[]`, `legal_source_ids[]`, `risk_ids[]` |
| `LegalSource` | Law/case/preparatory work/source | `id`, `jurisdiction`, `type`, `title`, `citation`, `url_or_ref`, `verified_status` |
| `RiskItem` | Weakness/uncertainty/conflict | `id`, `case_id`, `risk_type`, `severity`, `description`, `affected_objects[]`, `mitigation`, `status` |
| `DraftDocument` | Generated/edited legal draft | `id`, `case_id`, `draft_type`, `title`, `content`, `source_coverage`, `status`, `created_by`, `updated_at` |
| `ApprovalDecision` | Human approval record | `id`, `case_id`, `object_type`, `object_id`, `decision`, `approved_by`, `reason`, `created_at` |
| `AuditEvent` | Immutable audit event | `id`, `tenant_id`, `case_id`, `actor_type`, `actor_id`, `action`, `object_type`, `object_id`, `before_ref`, `after_ref`, `created_at` |
| `AgentRun` | AI/agent operation | `id`, `case_id`, `agent_type`, `input_refs[]`, `output_refs[]`, `status`, `confidence`, `uncertainty_flags[]`, `created_at` |
| `ExportPackage` | Final export bundle | `id`, `case_id`, `draft_document_ids[]`, `included_document_ids[]`, `control_gate_result`, `approved_by`, `export_hash`, `created_at` |

## High-level architecture

```text
apps/web
  Next.js UI, assistant panel, case room, document viewer, draft editor

services/api
  FastAPI REST API, auth enforcement, domain services

services/worker
  document processing, OCR, chunking, embeddings, agent jobs

packages/schemas
  Pydantic + JSON Schema canonical contracts

packages/policy
  permissions, gates, action authorization

packages/agent-core
  agent contracts, tool registry, provider adapters

packages/ui-contracts
  shared UI enums and view models

infra
  docker compose, migrations, deployment manifests
```

## Runtime flow

1. User uploads document.
2. API stores original in object storage.
3. API creates `Document` and `AuditEvent`.
4. Worker extracts pages and OCR.
5. Worker chunks text and creates `Chunk` records.
6. Worker creates source anchors.
7. Agent proposes fact claims.
8. User reviews facts.
9. Draft uses approved/source-backed facts.
10. Export gate validates readiness.
11. Human approval creates `ApprovalDecision`.
12. Export package generated and hashed.

## Boundaries

- UI never decides permissions.
- Agents never approve outputs.
- Workers never bypass API policy for user-facing actions.
- Object storage is never accessed directly by frontend without signed URLs.
- Audit writes are append-only.

