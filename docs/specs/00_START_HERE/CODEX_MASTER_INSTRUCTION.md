# Advokat AI — Codex Master Instruction

**Package version:** v0.4  
**Authority level:** Highest implementation instruction for Codex  
**Release model:** No MVP. Build Pilot Candidate → Release Candidate → Official Release.

## Binding instruction to Codex

Build this product exactly like this package specifies:

> **Bygg dette produktet nøyaktig slik, med denne arkitekturen, disse skjermene, disse dataobjektene, disse reglene, disse modulgrensene og disse akseptansekriteriene.**

Do not reinterpret the product as a generic legal chatbot, generic case-management system, generic document management system, or generic SaaS app.

This product is:

- a calm legal case room
- a source-controlled legal work platform
- a document-driven evidence and fact workspace
- a controlled AI collaboration partner
- a legal workflow system with strict control gates
- a product where every visible element must be useful to the user
- a product where user trust, source integrity and low mental load outrank flashy autonomy

## Implementation authority order

When documents conflict, use this order:

1. `00_START_HERE/CODEX_MASTER_INSTRUCTION.md`
2. `AGENTS.md`
3. `00_START_HERE/Codex_Execution_Instructions.md`
4. `04_Technical/OpenAPI_Pilot_Candidate_v1.yaml`
5. `04_Technical/SQL_Schema_Pilot_Candidate_v1.sql`
6. `04_Technical/Canonical_Domain_Model_v1.md`
7. `04_Technical/Assistant_Architecture_and_Actions_v1.md`
8. `03_Design/AI_Assistant_UX_Contract_v1.md`
9. `03_Design/Screen_by_Screen_UI_Contracts_v1.md`
10. `06_QA/Test_Matrix_Codex_Executable_v1.md`
11. All other product, design, security, operations and QA documents

If still ambiguous, choose the safest implementation that preserves:
- case isolation
- source integrity
- auditability
- control gates
- non-technical user experience
- low cognitive load
- no hidden uncertainty

## Do not ask the owner unless one of these hard blockers occurs

Codex should continue implementation using the defaults in this package unless:

1. a production secret or credential is required
2. a legal/compliance decision is not covered by package defaults
3. an irreversible production data operation is required
4. two source-of-truth documents directly contradict each other
5. a provider requires contractual/API details not present in this package
6. a jurisdiction-specific legal content answer must be authored as legal authority

## Default decisions locked for implementation

Until the owner overrides them, use these defaults:

| Area | Default |
|---|---|
| Primary jurisdiction | Norway-first, multi-jurisdiction-ready |
| Product language | Norwegian user-facing copy first, English internal code/documentation allowed |
| Tech stack | Next.js + TypeScript web app, FastAPI Python API, PostgreSQL, Redis, S3-compatible object storage, Python workers |
| Local storage | MinIO or local S3-compatible emulator |
| Production storage | EU/EEA-hosted S3-compatible encrypted object storage |
| Database | PostgreSQL 15+ |
| Vector search | pgvector optional behind interface; not required for initial skeleton |
| Auth | OIDC-compatible auth abstraction; local dev auth provider |
| RBAC | tenant_admin, case_owner, legal_reviewer, case_editor, case_viewer, external_collaborator, auditor |
| OCR | Provider interface + local/mock OCR adapter; production provider pluggable |
| AI | Provider interface; dev mock provider; production provider must be configured through secrets |
| Legal sources | Manual verified LegalSource first; external source connectors behind interface |
| Client portal | Not required for Pilot Candidate; may be scaffolded behind disabled feature flag |
| Data training | Off by default; no customer data used for model training unless explicit legal agreement |
| Region | EU/EEA-only by default |
| Audit | Append-only logical model; no hard delete of audit events |

## What Codex must build

Codex must build the product in this exact shape:

### Applications
- `apps/web` — Next.js frontend
- `services/api` — FastAPI backend
- `services/worker` — document/OCR/analysis workers
- `packages/schemas` — canonical TypeScript/Python schema definitions
- `packages/ui` — shared UI components and user-language mappings
- `packages/config` — typed environment and feature flags
- `infra` — local docker compose, database, object storage, redis
- `tests` — contract, integration, e2e and golden assistant tests

### Core modules
1. Tenant and user model
2. Case room
3. Role/permission model
4. Document upload and processing
5. Page/OCR/chunk/source reference model
6. Fact claims and evidence graph
7. Timeline and risk items
8. Draft editor with source coverage
9. AI assistant as legal collaboration partner and product guide
10. Control gates for critical actions
11. Export package generation
12. Audit trail
13. Observability and release gates

## User experience mandate

The product must feel like:

> a calm, premium, intelligent legal workspace with a built-in legal collaboration partner.

It must not feel like:
- a generic chatbot
- a technical admin panel
- a cluttered legal database
- a form-heavy legacy case system
- an AI demo where the user must guess what to do

## All visible information must be useful

Do not expose technical implementation details unless the user explicitly opens advanced/audit/admin views.

Never show user-facing strings like:
- `OCR confidence below threshold`
- `SourceRef validation failed`
- `Agent run completed with warnings`
- `chunk_hash_mismatch`
- `export_gate_blocked`

Instead show:
- «Denne siden er usikkert lest. Se over teksten før du bruker den som kilde.»
- «Denne påstanden mangler gyldig kilde.»
- «Analysen er ferdig, men det finnes punkter du bør se over.»
- «Dokumentet ser ut til å være endret siden analysen ble gjort.»
- «Eksport er stoppet fordi noe må kontrolleres først.»

## Assistant mandate

The AI assistant must feel like a legal assistant and collaboration partner.

It must:
- understand the current screen, case, document, selected object and recent user actions
- answer in the user's own natural phrasing
- explain the program without technical language
- guide the user without mental overload
- avoid repeated standard answers
- recognize semantically similar questions
- build on previous conversation
- vary explanations when the user remains unsure
- offer guided modes such as `show_me_how`, `do_it_with_me`, `why_blocked`, `check_my_work`
- clearly separate product guidance, legal work assistance and human legal judgment

It must not:
- output generic FAQ-like answers
- repeat the same standard answer when the user asks the same thing differently
- pretend uncertainty is certainty
- bypass control gates
- present AI-generated legal analysis as final legal advice

## Done means verified

A task is not done until:
- implementation matches the relevant specification documents
- tests exist and pass
- RBAC is enforced
- audit events are emitted
- source integrity is preserved
- control gates work
- UI copy is user-relevant and non-technical
- assistant behavior passes golden tests where relevant
- no critical open TODOs remain in touched paths
