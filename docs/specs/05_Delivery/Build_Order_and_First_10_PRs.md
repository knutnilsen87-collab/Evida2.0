# Advokat AI — Build Order and First 10 PRs

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

## First 10 PRs

1. **Repo skeleton and tooling** — apps/web, services/api, services/worker, packages/schemas, infra/docker.
2. **Database and canonical schemas** — migrations for tenant/user/case/audit/document.
3. **Auth and RBAC foundation** — auth middleware, case permission checks.
4. **Case room shell** — case list, case overview, navigation, assistant panel placeholder.
5. **Document upload and storage** — signed upload, document records, SHA-256, audit.
6. **Document processing worker** — page extraction, OCR stub/provider interface, statuses.
7. **SourceRef and FactClaim flow** — source anchors, claim CRUD, review UI.
8. **Assistant v1** — context-aware product help, guided-mode contract, “why blocked”.
9. **Draft editor source coverage** — draft creation, paragraph metadata, source check.
10. **Export Gate v1** — preview, blocking reasons, approval, export package record.

## PR rule

Each PR must include:
- migration/schema change if needed
- API tests for backend changes
- UI smoke path for frontend changes
- audit behavior where applicable
- update to implemented/validated status

