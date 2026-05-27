# Advokat AI — Module Boundaries and Service Contracts v1

## 1. Purpose

This document defines ownership boundaries so Codex does not place logic in the wrong layer.

Bad architecture in this product creates legal and trust risk.  
Do not mix UI, control gates, source integrity, audit and provider code.

---

# 2. Repository modules

```text
/apps/web
/services/api
/services/worker
/packages/schemas
/packages/ui
/packages/config
/packages/auth
/packages/audit
/packages/assistant
/packages/source-integrity
/infra
/tests
```

---

# 3. Module ownership

## `apps/web`

Owns:
- routes
- screen composition
- client-side UI state
- assistant panel UI
- guided overlays
- user-facing copy display
- loading/empty/error states

Does not own:
- RBAC truth
- export gate truth
- source validation truth
- audit persistence
- OCR/document processing
- provider AI calls

Allowed dependencies:
- `packages/ui`
- `packages/schemas`
- generated API client
- `packages/config`

## `services/api`

Owns:
- API controllers
- auth middleware
- RBAC enforcement
- tenant/case isolation enforcement
- domain services
- control gate evaluation
- source integrity checks
- export creation
- audit event writing
- assistant orchestration API

Does not own:
- page extraction/OCR implementation
- frontend rendering
- provider-specific code outside adapters
- raw object storage implementation details outside storage adapter

## `services/worker`

Owns:
- async jobs
- PDF validation
- file scan orchestration
- page extraction
- OCR provider adapter calls
- chunking
- hashing
- indexing
- document processing status updates

Does not own:
- user-facing gate decisions
- final export approval
- user permission model
- legal conclusions

## `packages/schemas`

Owns:
- canonical enums
- Pydantic/Zod schemas
- OpenAPI-generated DTOs
- cross-language schema definitions

Rule:
- no private incompatible schema variants

## `packages/source-integrity`

Owns:
- source ref validation
- quote anchor validation
- fact/source status rules
- draft source coverage
- source readiness summary

API service calls this package for business logic.

## `packages/assistant`

Owns:
- assistant context object
- intent classification
- topic fingerprinting
- answer fingerprinting
- guided action schema
- response quality gate
- provider adapter interface

Does not own:
- final gate decisions
- permission bypass
- direct database writes outside assistant session/message/action records

## `packages/audit`

Owns:
- audit event schema
- audit writer interface
- audit event action names
- append-only semantics helpers

## `packages/ui`

Owns:
- design-system primitives
- status chips
- empty states
- warning cards
- guided overlay components
- useful-only copy mapping
- assistant panel components

Does not own business truth.

## `packages/config`

Owns:
- typed env
- feature flags
- provider selection
- region defaults
- local/dev defaults

---

# 4. Domain services in API

## CaseService
Responsibilities:
- create/update/list cases
- overview readiness aggregation
- membership checks delegated to RBAC
- emits audit

## DocumentService
Responsibilities:
- upload init/complete
- document metadata
- processing job creation
- document status read model
- emits audit

## SourceIntegrityService
Responsibilities:
- create source refs
- validate source refs
- evaluate fact source status
- evaluate draft coverage
- detect source/document mismatch

## FactService
Responsibilities:
- CRUD fact claims
- source status transitions
- source linking

## EvidenceService
Responsibilities:
- CRUD evidence items
- source/fact links

## TimelineService
Responsibilities:
- CRUD timeline events
- date uncertainty handling

## DraftService
Responsibilities:
- CRUD draft documents/sections
- update source coverage
- prevent unsafe status transitions

## ControlGateService
Responsibilities:
- export gate preview
- external share gate
- bulk operation gate
- blocked reason generation in user language
- gate result lineage

## ApprovalService
Responsibilities:
- create approval/rejection
- tie approval to exact target
- prevent stale approval use

## ExportService
Responsibilities:
- verify gate/approval
- build export manifest
- store export package
- emit audit

## AssistantService
Responsibilities:
- context building
- intent handling
- provider orchestration
- answer quality gate
- guided actions
- assistant audit events

## AuditService
Responsibilities:
- write append-only audit events
- read audit for authorized users
- no update/delete

---

# 5. State transition ownership

| State machine | Owner |
|---|---|
| Document status | DocumentService + Worker |
| Page/OCR status | Worker |
| Fact source status | SourceIntegrityService |
| Draft status | DraftService + SourceIntegrityService |
| Export gate status | ControlGateService |
| Approval status | ApprovalService |
| Assistant session/action status | AssistantService |

---

# 6. Error handling contract

All API errors use `ErrorEnvelope`.

Rules:
- `user_message` is Norwegian and non-technical
- `technical_message` only for logs/advanced use
- include `correlation_id`
- no stack traces in API response
- emit audit for denied/sensitive operations

---

# 7. Cross-cutting invariants

Every service method receiving `case_id` must:
1. verify user authenticated
2. verify tenant
3. verify case membership/permission
4. use tenant_id in every query
5. emit audit if material operation
6. return user-facing copy, not raw internal state

---

# 8. Forbidden shortcuts

Codex must not:
- put export gate rules in frontend only
- validate source refs only in UI
- call AI provider directly from React components
- skip audit for “temporary” features
- add broad `helpers.ts` or `utils.py` for domain logic
- create duplicate status enums
- expose raw technical states in UI
