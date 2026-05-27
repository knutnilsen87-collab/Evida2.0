# Owner Defaults and Remaining Decisions

This file prevents Codex from blocking unnecessarily.

## Defaults Codex should use

| Question | Default Codex should implement |
|---|---|
| Jurisdiction | Norway-first, with `jurisdiction` field for future expansion |
| User-facing language | Norwegian |
| Internal technical language | English |
| Hosting | EU/EEA-only by default |
| Database | PostgreSQL |
| Object storage | S3-compatible, local MinIO in dev |
| AI provider | Provider interface + mock/dev provider; production configured by environment |
| OCR provider | Provider interface + mock/local adapter; production configured by environment |
| Legal source integration | Manual verified `LegalSource` object first; external connectors later |
| Client portal | Not in Pilot Candidate; scaffold feature flag `client_portal_enabled=false` |
| Data training | Disabled by default |
| Audit deletion | Not allowed |
| Hard deletion of cases/documents | Not allowed through UI; use retention/deletion workflow |
| Export | Requires gate pass + approval |
| Assistant actions | Can guide and prepare suggestions; cannot perform critical actions without preview/approval |

## Human decisions still useful but not blocking local implementation

The owner should eventually decide:

1. Final production hosting vendor.
2. Final production AI provider.
3. Final production OCR provider.
4. Final legal source provider/integration.
5. Exact data retention periods.
6. Final incident response owner.
7. Final penetration test vendor.
8. Final support model.
9. Whether client portal becomes official-release scope or post-release.

## Codex behavior

Codex must not stop for these decisions during implementation unless production deployment, credentials or legal authority content is required.
