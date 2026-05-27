# AGENTS.md — Advokat AI Repository Instructions for Codex

## Purpose

This file gives Codex persistent implementation instructions for the Advokat AI repository.

Codex must build the product exactly according to the package documentation:

> **Bygg dette produktet nøyaktig slik, med denne arkitekturen, disse skjermene, disse dataobjektene, disse reglene, disse modulgrensene og disse akseptansekriteriene.**

## Product identity

Advokat AI is not a generic chatbot and not a generic document manager.

It is a controlled legal case workspace where:
- every fact claim is source-linked or explicitly marked as missing source
- real legal documents can be used in Pilot Candidate
- all critical actions require preview/control gate
- final export is blocked until readiness checks pass
- the AI assistant feels like a legal collaboration partner
- onboarding happens through contextual assistant guidance
- all visible UI information must be useful to the user

## Read these first

Before coding, read:

1. `00_START_HERE/CODEX_MASTER_INSTRUCTION.md`
2. `00_START_HERE/Codex_Execution_Instructions.md`
3. `04_Technical/Technical_Architecture_Spec.md`
4. `04_Technical/Canonical_Domain_Model_v1.md`
5. `04_Technical/OpenAPI_Pilot_Candidate_v1.yaml`
6. `04_Technical/SQL_Schema_Pilot_Candidate_v1.sql`
7. `04_Technical/Assistant_Architecture_and_Actions_v1.md`
8. `03_Design/AI_Assistant_UX_Contract_v1.md`
9. `03_Design/Screen_by_Screen_UI_Contracts_v1.md`
10. `06_QA/Test_Matrix_Codex_Executable_v1.md`

## Repository shape

Implement the repository as:

```text
/apps
  /web
/services
  /api
  /worker
/packages
  /schemas
  /ui
  /config
  /auth
  /audit
  /assistant
  /source-integrity
/infra
  /docker
  /migrations
/tests
  /contract
  /integration
  /e2e
  /golden
/docs
```

## Module boundaries

### `apps/web`
Owns:
- routes
- screens
- UI state
- user-facing copy
- assistant panel shell
- guided overlays

Must not own:
- legal source validation logic
- export gate rules
- RBAC decisions
- audit persistence
- document processing

### `services/api`
Owns:
- REST API
- auth enforcement
- RBAC enforcement
- business workflows
- control gate evaluation
- audit event creation
- database access

Must not own:
- OCR internals
- UI copy variations except API error codes/messages
- direct provider-specific AI code outside provider interface

### `services/worker`
Owns:
- document processing jobs
- OCR jobs
- page extraction
- chunking
- hashing
- source indexing
- async artifact creation

Must not own:
- user permissions
- user-visible control gate decisions
- final legal conclusions

### `packages/schemas`
Owns:
- canonical shared types
- enum values
- OpenAPI-derived models
- validation schemas

No private incompatible object variants are allowed.

### `packages/assistant`
Owns:
- assistant context object
- intent fingerprinting
- answer fingerprinting
- guided action schemas
- response quality checks
- product-help/legal-work separation

Must not bypass:
- export gates
- approval requirements
- RBAC
- audit requirements

### `packages/audit`
Owns:
- audit event schema
- audit writer interface
- append-only event conventions

### `packages/source-integrity`
Owns:
- source ref validation
- quote anchoring
- fact claim source status
- document/page/chunk hashing rules

## Build commands

Use these commands by default after scaffolding:

```bash
# repo install
pnpm install

# frontend
pnpm --filter web lint
pnpm --filter web test
pnpm --filter web build

# backend
cd services/api && python -m pytest
cd services/api && ruff check .
cd services/api && mypy .

# worker
cd services/worker && python -m pytest
cd services/worker && ruff check .
cd services/worker && mypy .

# contract tests
pnpm test:contracts

# all checks
pnpm verify
```

If the repo has not yet been created, Codex must create scripts so these commands or equivalent commands work.

## Implementation workflow

For every meaningful task:

1. Inspect relevant specs.
2. Create or update a bounded plan.
3. Implement the smallest complete vertical slice.
4. Add or update tests.
5. Run targeted checks.
6. Preserve module boundaries.
7. Update documentation only if behavior changed.
8. Do not call success without validation evidence.

## UI rules

- No technical language in default user-facing UI.
- Every visible element must be useful.
- Default view must reduce mental load.
- Show only what helps the user understand, decide or proceed.
- Keep technical details in advanced/audit/admin views.
- Use Norwegian user-facing copy by default.
- Control states must be human-readable.

## Assistant rules

The assistant must:
- answer in context
- avoid standard/repeated answers
- recognize same question phrased differently
- build on previous answers
- vary explanation method when user remains unsure
- offer guided next step
- clearly say when human legal review is required
- never bypass control gates
- never present AI as final legal authority

## Security rules

- Enforce tenant isolation in every query.
- Enforce case membership before case access.
- Emit audit events for all material operations.
- Never store secrets in source.
- No hard deletion of audit events.
- No customer data used for model training by default.
- Use EU/EEA region defaults.
- Critical actions require idempotency keys.

## Testing expectations

Every feature must include at least one of:
- unit test
- contract test
- integration test
- e2e test
- golden assistant test
- permission test
- audit test

Features touching exports, sources, documents, permissions or assistant guidance require tests.

## Stop conditions

Stop and request human input only when:
- production secret is required
- an actual legal authority/content decision is required
- conflicting specs cannot be safely resolved
- irreversible production action is requested
- provider contract details are missing

Otherwise use package defaults and continue.
