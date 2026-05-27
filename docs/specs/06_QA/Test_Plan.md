# Advokat AI — Test Plan

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

## Test plan

### Required test suites

- Unit tests for schemas, policies and gates.
- API tests for every endpoint.
- Worker tests for document processing state transitions.
- Integration tests for upload -> process -> fact -> draft -> export.
- Permission tests for every role.
- Audit tests for critical actions.
- Security tests for tenant/case isolation.
- Accessibility smoke tests.
- E2E tests for first-case guided flow and blocked export flow.

## Critical test cases

1. User cannot access another tenant's case.
2. User uploads PDF and processing completes.
3. OCR failure creates visible blocked state.
4. Fact claim without source cannot become export-ready.
5. Draft with missing source is blocked.
6. Export requires approval.
7. Agent cannot approve output.
8. Assistant explains why export is blocked.
9. Audit trail includes actor/object/before/after.
10. Restore from backup preserves case/document/audit integrity.

