# Advokat AI — Codex Execution Instructions v0.4

## Binding command

Codex must implement this product exactly as specified:

> **Bygg dette produktet nøyaktig slik, med denne arkitekturen, disse skjermene, disse dataobjektene, disse reglene, disse modulgrensene og disse akseptansekriteriene.**

This is not a brainstorming package.  
This is an execution package.

Codex should not ask open-ended product questions when a safe default is specified. Use the defaults in this package and continue.

---

# 1. Product premise

Advokat AI is a legal operating system for document-driven case work.

The user works inside one calm, source-controlled case room. Internally, specialized services and agents help with documents, OCR, facts, evidence, chronology, legal sources, risk, drafts, explanations and quality control.

The product must support real legal documents in a controlled pilot environment.

The release model is:

1. Foundation
2. Pilot Candidate
3. Release Candidate
4. Official Release

There is no MVP concept in this package.

---

# 2. Codex build target

Build a production-grade skeleton and then complete feature implementation according to the package.

The target is a full-stack application with:

- Next.js frontend
- FastAPI backend
- PostgreSQL
- Redis
- S3-compatible object storage
- Python workers
- canonical schemas
- strict RBAC
- source integrity
- audit trail
- AI assistant as collaboration partner
- control gates
- export readiness
- QA/release gates

---

# 3. Non-negotiable product rules

1. No factual claim without a source or explicit `missing_source` status.
2. No final export without export control gate.
3. No critical operation without preview.
4. No external sharing without explicit approval.
5. No hidden AI uncertainty.
6. No shared case memory across cases.
7. No unlogged critical operation.
8. No technical UI language unless advanced/audit/admin view is explicitly opened.
9. Every visible UI element must help the user understand, decide or proceed.
10. The assistant must not behave like a generic chatbot or FAQ.
11. The assistant must not repeat generic standard answers for semantically similar questions.
12. The assistant must clearly distinguish product guidance, legal work help and human legal judgment.
13. Human legal responsibility remains with the user/organization.
14. User data is not used for model training by default.
15. All critical operations must preserve audit lineage.

---

# 4. Build sequence

Codex must build in this order.

## PR 0 — Repository foundation
Create:
- monorepo structure
- package manager config
- `.env.example`
- Docker Compose for PostgreSQL, Redis, MinIO
- frontend app skeleton
- backend app skeleton
- worker skeleton
- shared schema package
- shared config package
- root verification scripts
- root `AGENTS.md`

Success:
- repo installs
- local services start
- health endpoint works
- frontend shell renders
- `pnpm verify` or equivalent exists

## PR 1 — Canonical schemas and database
Implement:
- canonical enums
- canonical domain schemas
- SQL migrations
- tenant/case/user/document/source/fact/draft/audit tables
- migration runner
- seed data

Success:
- migrations apply
- seed data loads
- schema tests pass

## PR 2 — Auth, tenant isolation and RBAC
Implement:
- local auth adapter
- user session model
- tenant isolation middleware
- case membership checks
- permission matrix
- endpoint permission tests

Success:
- unauthorized users blocked
- cross-tenant access blocked
- audit events written for denied critical access

## PR 3 — Audit system
Implement:
- audit event writer
- append-only semantics
- audit event read API
- audit UI advanced view
- event correlation IDs

Success:
- material actions produce audit events
- audit events cannot be updated/deleted through normal app paths

## PR 4 — Case room and UI shell
Implement:
- case list
- create case
- case overview
- left navigation
- top status bar
- right assistant panel
- useful-only UI copy mapping
- loading/empty/error states

Success:
- user can create/open case
- assistant panel receives screen context
- no technical copy appears in default UI

## PR 5 — Document upload and processing pipeline
Implement:
- signed upload initiation
- complete upload registration
- document status machine
- object storage adapter
- worker job queue
- PDF validation
- page extraction stub/adapter
- OCR provider interface
- chunking and hashing
- page status UI

Success:
- PDF upload registers document
- worker creates pages/chunks
- failed OCR page enters review state
- hashes are stored
- source refs can point to pages/chunks

## PR 6 — Facts, source refs and evidence graph
Implement:
- source refs
- fact claims
- fact claim source status
- evidence items
- source coverage checks
- UI create/edit/link flows

Success:
- documented fact must have source
- missing-source facts are visibly marked
- source coverage is shown in user language

## PR 7 — AI assistant as legal collaboration partner
Implement:
- assistant chat endpoint
- assistant context object
- intent fingerprinting
- answer fingerprinting
- response memory
- anti-repetition logic
- guided actions
- visible useful answer quality gate
- golden assistant tests

Success:
- assistant answers product-use questions in context
- assistant recognizes same question phrased differently
- assistant varies explanation when user remains uncertain
- assistant can return guided actions without executing critical operations

## PR 8 — Draft editor and source coverage
Implement:
- draft documents
- draft sections
- paragraph source coverage
- inline source warnings
- assistant draft help
- check-my-work flow

Success:
- user can create draft
- source coverage shown per section
- missing source blocks export readiness

## PR 9 — Control gates and approvals
Implement:
- export preview
- export gate result model
- approval decisions
- blocked reasons
- why-blocked assistant integration
- control gate UI

Success:
- export is blocked when missing sources/coverage/conflicts exist
- approval is tied to specific gate result/version
- blocked reasons are user-readable

## PR 10 — Export packages
Implement:
- export package creation
- export manifest
- source appendix
- audit lineage
- immutable export record
- download endpoint

Success:
- export only works after gate pass + approval
- exported package has manifest and source basis
- export is auditable

## PR 11 — QA hardening and release gates
Implement:
- integration tests
- e2e smoke tests
- assistant golden tests
- permission tests
- audit tests
- release gate scripts
- documentation status table

Success:
- automated checks pass
- release readiness status is explicit

---

# 5. Implementation style

Codex must prefer:
- small vertical slices
- explicit schemas
- clear module boundaries
- typed interfaces
- deterministic workers
- testable business logic
- user-language mapping
- no broad utility dumping

Codex must avoid:
- hidden magic
- duplicated domain types
- mixing UI and business rules
- direct provider calls scattered across app
- technical default UI copy
- undocumented assumptions
- unaudited critical actions

---

# 6. Required architecture

```text
User
  ↓
Next.js Web App
  ↓
FastAPI API
  ↓
Domain Services
  ├─ Auth/RBAC
  ├─ Case Service
  ├─ Document Service
  ├─ Source Integrity Service
  ├─ Assistant Service
  ├─ Control Gate Service
  ├─ Export Service
  └─ Audit Service
  ↓
PostgreSQL + Object Storage + Redis
  ↓
Worker Service
  ├─ PDF Validation
  ├─ Page Extraction
  ├─ OCR Provider
  ├─ Chunking
  ├─ Hashing
  └─ Indexing
```

Provider-specific AI/OCR/storage/auth code must be behind interfaces.

---

# 7. Assistant implementation mandate

The assistant must feel like:
- a legal assistant
- a calm colleague
- a product guide
- a collaboration partner

It must not feel like:
- a chatbot
- FAQ
- technical support bot
- generic AI wrapper

When user asks about the product, the assistant should answer in this pattern:

1. short answer
2. plain explanation
3. current-context relevance
4. next safe step
5. guided action option
6. deeper details only if requested

But the visible text must not feel templated.

---

# 8. User-facing language

Default user-facing copy is Norwegian.

Internal code and technical docs may be English.

All visible copy must pass this test:

1. Does it help the user understand?
2. Does it help the user decide?
3. Does it help the user safely proceed?
4. Is it in natural user language?
5. Does it avoid unnecessary technical detail?

If not, do not show it by default.

---

# 9. Verification rule

Do not mark a task complete unless:
- code compiles
- tests pass or missing checks are explicitly documented
- relevant API contract is satisfied
- relevant database constraints are respected
- audit events exist where required
- RBAC is tested where relevant
- assistant golden tests pass where relevant
- UI copy is user-facing and non-technical
