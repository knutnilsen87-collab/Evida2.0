# Advokat AI — Codex PR Backlog Exact Build Order v1

Codex must implement the product in this order unless a blocking technical reason appears.

Each PR should be a vertical, verifiable slice.

---

# PR 0 — Repo foundation

## Goal
Create runnable monorepo skeleton.

## Must create
- `apps/web`
- `services/api`
- `services/worker`
- `packages/schemas`
- `packages/ui`
- `packages/config`
- `packages/auth`
- `packages/audit`
- `packages/assistant`
- `packages/source-integrity`
- `infra/docker-compose.yml`
- `.env.example`
- root `package.json`
- root `AGENTS.md`
- `README.md`

## Acceptance
- local stack starts
- health endpoint returns ok
- frontend loads
- test scripts exist
- no product feature yet beyond shell

---

# PR 1 — Database and canonical schemas

## Goal
Implement canonical domain model.

## Must implement
- SQL migrations from `SQL_Schema_Pilot_Candidate_v1.sql`
- Python/Pydantic models
- TypeScript/Zod schemas
- enum constants
- seed data

## Acceptance
- migrations run on empty DB
- seed tenant/user/case created
- schema tests pass
- no duplicate domain models

---

# PR 2 — Auth, tenant isolation, RBAC

## Goal
User access is safe by default.

## Must implement
- local dev auth
- current user endpoint
- RBAC middleware
- tenant filter enforcement
- case membership enforcement
- permission matrix
- denied-access audit event

## Acceptance
- cross-tenant tests pass
- role tests pass
- every case endpoint enforces membership

---

# PR 3 — Audit foundation

## Goal
Every material operation becomes traceable.

## Must implement
- audit writer
- audit API
- audit UI advanced view
- audit event schema constants
- append-only protection

## Acceptance
- update/delete audit blocked
- create case emits audit
- denied access emits audit

---

# PR 4 — Case room UI shell

## Goal
User can create/open a calm legal case room.

## Must implement
- `/cases`
- `/cases/new`
- `/cases/[caseId]`
- stable layout
- assistant panel shell
- readiness cards
- Norwegian user copy
- useful-only status mapping

## Acceptance
- E2E create/open case
- no technical copy shown
- assistant receives screen context

---

# PR 5 — Document upload and processing

## Goal
Real documents can enter the case.

## Must implement
- init upload
- complete upload
- storage adapter
- document list
- document detail
- worker queue
- PDF validation
- page extraction adapter/mock
- OCR adapter/mock
- chunking
- hashing
- document status mapping

## Acceptance
- valid PDF fixture creates pages/chunks
- low-confidence OCR fixture becomes needs_review
- upload emits audit
- no raw job copy shown to user

---

# PR 6 — Source refs, facts, evidence

## Goal
User can create source-grounded facts.

## Must implement
- source refs
- fact claims
- evidence items
- fact/source linking UI
- source status evaluation
- missing source warnings

## Acceptance
- documented fact requires source
- missing source shown clearly
- source ref audit emitted

---

# PR 7 — Timeline and risks

## Goal
User can build chronology and track weak points.

## Must implement
- timeline events
- date uncertainty
- risk items
- links to source refs
- assistant explanation hooks

## Acceptance
- unknown/approx date works
- risk shown calmly
- unresolved critical risk affects export gate later

---

# PR 8 — Assistant v1: collaboration partner and program guide

## Goal
Assistant can answer product-use questions and guide user.

## Must implement
- assistant sessions/messages
- chat endpoint
- context builder
- intent classifier
- topic fingerprinting
- answer fingerprinting
- anti-repetition logic
- quality gate
- guided actions
- mock provider
- assistant panel integration
- golden tests

## Acceptance
- ASSIST golden tests pass
- same question phrased differently does not produce same answer
- no technical jargon in product answers
- assistant offers guided next step

---

# PR 9 — Draft editor and source coverage

## Goal
User can write source-controlled legal drafts.

## Must implement
- draft list
- draft editor
- draft sections
- paragraph source status
- source coverage endpoint
- assistant check-my-work
- warnings

## Acceptance
- missing source section detected
- coverage report works
- draft update audit emitted

---

# PR 10 — Export gate and approvals

## Goal
Critical export is safe.

## Must implement
- export preview endpoint
- gate checks
- gate UI
- blocked reasons
- approval decision
- stale approval detection
- assistant why-blocked integration

## Acceptance
- missing sources block export
- approval tied to gate result
- assistant explains exact blockers

---

# PR 11 — Export packages

## Goal
Approved work can be exported.

## Must implement
- export package creation
- manifest
- source appendix
- storage
- download endpoint
- audit lineage

## Acceptance
- export impossible without valid gate + approval
- manifest includes source/audit refs
- export audit emitted

---

# PR 12 — Operations and release gates

## Goal
Pilot Candidate readiness.

## Must implement
- Docker compose polish
- health checks
- backup/restore scripts
- monitoring stubs
- release scripts
- QA suite
- status table update

## Acceptance
- `pnpm verify` passes
- pilot release checklist complete
- open risks documented

---

# PR 13 — Release Candidate hardening

## Goal
Prepare official release path.

## Must implement
- performance tests
- accessibility checks
- security review checklist
- compliance review checklist
- incident response runbook
- admin/audit improvements
- provider failure behavior

## Acceptance
- release candidate gates pass
- no P0/P1 open issues
