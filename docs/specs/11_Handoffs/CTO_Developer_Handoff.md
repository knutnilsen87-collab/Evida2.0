# Advokat AI — CTO Developer Handoff

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

## AI legal assistant / collaboration partner

The AI chat assistant is a first-class product surface. It must feel like a calm legal assistant and collaboration partner, not a generic chatbot.

### Assistant jobs
- Explain every part of the program in the user's own language.
- Help the user understand what they are seeing.
- Recommend safe next steps.
- Guide the user through workflows without mental overload.
- Explain warnings, blocked states, missing sources and export gates.
- Help with legal work product while preserving source discipline.
- Make onboarding happen through real work, not manuals.

### Desired user feeling
The user should repeatedly feel: **“Dette var jo lett.”**

### Interaction rule
When answering product-use questions, the assistant must use this sequence by default:

1. Give a short answer.
2. Explain it simply.
3. Show the next concrete action.
4. Offer “vis meg” / guided mode.
5. Reveal deeper details only if requested.

### Guided modes
The assistant must support:
- `explain_this`: explain current screen/object/warning
- `show_me_how`: highlight UI and walk the user through steps
- `do_it_with_me`: interactive step-by-step guided completion
- `check_my_work`: inspect readiness, missing sources, risks and next steps
- `why_blocked`: explain blocked/export-prevented states
- `what_next`: recommend next best action
- `legal_work_help`: help structure facts, evidence, chronology, argument and draft

### Falloff prevention
The app must detect signs of confusion:
- repeated navigation between same screens
- long idle time on blocked state
- repeated assistant queries about same topic
- abandoned workflow
- repeated failed export/control gate attempts

When detected, the app must offer:
- simpler explanation
- guided walkthrough
- reduced UI complexity
- next best step
- “do this together with me”

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

## Control gates

Critical operations require explicit control gates.

| Gate | Trigger | Blocks when |
|---|---|---|
| Source Gate | Fact or paragraph used in legal output | Missing source, uncertain quote, source mismatch, OCR uncertainty above threshold |
| Document Coverage Gate | Case analysis/draft/export | Document coverage below configured threshold, unprocessed pages, corrupted file |
| Evidence Gate | Evidence map or argument generation | Unsupported claim, conflicting evidence unresolved, weak source confidence |
| Legal Source Gate | Legal source used in argument | Unverified legal source, wrong jurisdiction, stale/manual-only source |
| Privacy Gate | External sharing/export | Sensitive personal data unreviewed, redaction incomplete, access mismatch |
| Export Gate | Any final export | Missing source, unresolved conflict, critical risk, unapproved changes, audit gap |
| Agent Action Gate | Large AI operation | Scope too broad, unclear user intent, destructive operation, missing preview |
| Sharing Gate | Invite or external sharing | Role mismatch, tenant violation, unapproved recipient |

Every gate must produce:
- status: `pass | warning | fail | blocked`
- affected objects
- reason codes
- human-readable explanation
- recommended next action
- audit event
- approval requirement, if any

## CTO handoff instruction for Codex/dev team

Build Advokat AI from this package with Pilot Candidate as the first operational target.

## Golden path to implement

1. Create authenticated tenant and case.
2. Upload real PDF.
3. Process PDF into pages, OCR text, chunks, hashes.
4. Create source references.
5. Propose and review fact claims.
6. Build simple chronology.
7. Create source-backed draft.
8. Run source/export gate.
9. Require approval.
10. Create export package.
11. Show full audit trail.
12. Assistant can explain every step and guide user.

## Non-negotiable engineering guardrails

- No critical operation without audit.
- No export without gate.
- No source-free factual output in export.
- No cross-tenant/cross-case data leakage.
- No AI self-approval.
- No hidden uncertainty.
- No canonical schema drift.

