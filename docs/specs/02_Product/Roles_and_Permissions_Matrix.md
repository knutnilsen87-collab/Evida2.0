# Advokat AI — Roles and Permissions Matrix

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

## Roles

| Role | Description |
|---|---|
| `tenant_admin` | Manages tenant settings, users, security settings |
| `case_owner` | Primary responsible lawyer/legal owner |
| `legal_reviewer` | Can review and approve legal output |
| `case_editor` | Can upload, analyze, edit drafts, propose changes |
| `case_viewer` | Read-only case access |
| `external_collaborator` | Limited scoped access; disabled by default for pilot |
| `auditor` | Read-only access to audit/export/compliance records |
| `system_agent` | Non-human actor; cannot approve/export/share |

## Permission matrix

| Action | tenant_admin | case_owner | legal_reviewer | case_editor | case_viewer | external | auditor | agent |
|---|---|---|---|---|---|---|---|---|
| Create case | yes | yes | no | no | no | no | no | no |
| Upload document | yes | yes | yes | yes | no | scoped | no | no |
| View document | scoped | yes | yes | yes | yes | scoped | metadata | scoped |
| Edit fact claim | scoped | yes | yes | yes | no | no | no | propose |
| Approve fact claim | no | yes | yes | no | no | no | no | no |
| Generate draft | scoped | yes | yes | yes | no | no | no | propose |
| Approve export | no | yes | yes | no | no | no | no | no |
| Export | no | yes | yes | no | no | no | no | no |
| Invite user | yes | yes | no | no | no | no | no | no |
| View audit | yes | yes | yes | limited | no | no | yes | write-only |

