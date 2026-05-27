# Advokat AI — Release Gates and Automated Checks v1

## 1. Release principles

No release can be called ready without verification.

Pilot Candidate and Official Release have different gates.

---

# 2. Pilot Candidate gates

Pilot Candidate can use real legal documents under controlled pilot agreements only if:

## Automated gates
- backend tests pass
- frontend tests pass
- migrations apply
- OpenAPI validates
- document pipeline tests pass
- RBAC tests pass
- tenant isolation tests pass
- audit immutability tests pass
- export gate tests pass
- assistant golden tests pass
- no technical copy appears in default UI tests

## Manual gates
- pilot data handling approved
- pilot users/tenants configured
- pilot agreement exists
- legal responsibility disclaimer approved
- incident response owner assigned
- data retention default approved

---

# 3. Release Candidate gates

Release Candidate requires Pilot Candidate gates plus:

- performance test for large PDF set
- backup restore test
- security review
- compliance review
- legal workflow review
- export package review
- accessibility review
- monitoring/alerting configured
- provider failover/degraded behavior tested

---

# 4. Official Release gates

Official Release requires:

## Product
- all critical workflows complete
- all visible UI useful and non-technical
- assistant collaboration experience passes golden tests
- user onboarding through assistant works
- export control is reliable
- source graph and audit trail reliable

## Legal/compliance
- DPIA/personvernkonsekvensvurdering completed where applicable
- data processing agreements ready
- terms/privacy policy approved
- AI provider policy approved
- data retention/s deletion policy approved
- legal disclaimers approved
- jurisdiction scope documented

## Security
- threat model complete
- penetration test complete or accepted
- secrets handling reviewed
- access control reviewed
- audit immutability reviewed
- backup/restore tested
- incident response tested

## Engineering
- no open P0/P1 issues
- all release tests pass
- migrations reproducible
- rollback plan documented
- observability dashboards exist
- error budget/alert policy defined
- dependency/license scan complete

---

# 5. Suggested root scripts

Codex should create these scripts:

```json
{
  "scripts": {
    "verify": "pnpm lint && pnpm test && pnpm test:contracts && pnpm test:e2e",
    "lint": "pnpm -r lint",
    "test": "pnpm -r test",
    "test:contracts": "pnpm --filter contracts test",
    "test:e2e": "pnpm --filter web test:e2e",
    "openapi:validate": "swagger-cli validate docs/openapi.yaml",
    "db:migrate": "cd services/api && alembic upgrade head",
    "db:test-migrate": "cd services/api && pytest tests/test_migrations.py",
    "assistant:golden": "cd services/api && pytest tests/assistant/test_golden.py",
    "release:pilot": "pnpm verify && pnpm assistant:golden"
  }
}
```

Exact tooling may vary, but equivalent commands must exist.

---

# 6. Release status file

Codex should maintain:

`09_Project_Control/Specified_Implemented_Validated_Status.md`

For each feature:

| Feature | Specified | Implemented | Tests | Validated | Notes |
|---|---:|---:|---:|---:|---|
| Case room | yes | no | no | no |  |
| Document pipeline | yes | no | no | no |  |
