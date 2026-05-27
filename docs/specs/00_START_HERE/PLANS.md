# PLANS.md — Codex Execution Plan Standard

Codex must use this plan format for all non-trivial implementation work.

A task is non-trivial if it:
- changes database schema
- changes API contracts
- changes assistant behavior
- changes control gates
- changes source integrity
- changes permissions
- adds a new screen
- adds a new worker workflow
- affects export or audit

## Required plan format

```md
# Execution Plan: <task name>

## Goal
What user/system outcome this task creates.

## Source documents read
- file/path.md
- file/path.yaml
- file/path.sql

## Scope
### In scope
- ...

### Out of scope
- ...

## Affected modules
- apps/web/...
- services/api/...
- services/worker/...
- packages/...

## Canonical objects affected
- Case
- Document
- SourceRef
- FactClaim
- AuditEvent

## API changes
- endpoint
- request schema
- response schema
- error cases

## Database changes
- table
- column
- migration
- constraint
- index

## UI changes
- route
- component
- loading state
- empty state
- error state
- assistant behavior

## Permissions
- roles allowed
- roles denied
- audit events emitted

## Control gates
- gate added/changed
- blocked reasons
- approval requirements

## Test plan
- unit tests
- integration tests
- contract tests
- e2e tests
- golden assistant tests

## Rollback
How to revert safely.

## Stop conditions
When Codex must stop and ask.

## Definition of done
- [ ] code implemented
- [ ] tests added
- [ ] tests pass
- [ ] audit checked
- [ ] RBAC checked
- [ ] UI copy checked
- [ ] docs updated if behavior changed
```

## Plan discipline

Do not use a broad plan for unrelated changes.

Prefer:
- one vertical feature
- one schema change set
- one UI flow
- one worker state machine stage
- one control gate

Avoid:
- sweeping refactors
- undocumented assumptions
- changing public contracts without tests
- adding new domain objects when existing canonical objects fit
