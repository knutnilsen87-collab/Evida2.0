# Advokat AI — Document Priority and Source of Truth

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

## Source of truth hierarchy

When documents conflict, use this order:

1. This document.
2. `11_Handoffs/CTO_Developer_Handoff.md`.
3. `04_Technical/Canonical_Domain_Model_v1.md`.
4. `04_Technical/API_Specification.md`.
5. `04_Technical/SQL_Schema_v1.sql`.
6. `06_QA/Definition_of_Done.md`.
7. `08_Security_Legal/Security_Requirements.md`.
8. `02_Product/Functional_Specification.md`.
9. `03_Design/UI_Specification.md`.
10. Other supporting docs.

## Naming rule

Use these canonical names in code:
- `Case`, not matter/project/workspace.
- `Document`, not file, except low-level storage implementation.
- `FactClaim`, not fact/assertion in core schema.
- `SourceRef`, not citation/source-link in core schema.
- `DraftDocument`, not output/doc/draft in core schema.
- `ControlGate`, not modal/check/warning in core schema.
- `AgentRun`, not job/AI run in core schema.
- `AuditEvent`, not log/event in core schema.

## Hard constraint

No document may define a private incompatible variant of a canonical object.

