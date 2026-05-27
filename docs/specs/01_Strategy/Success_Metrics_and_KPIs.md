# Advokat AI — Success Metrics and KPIs

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

## Product KPIs

| KPI | Pilot target | Official release target |
|---|---:|---:|
| Successful document ingestion | ≥ 95% of pilot files | ≥ 99% supported files |
| OCR/page processing completion | ≥ 95% pages | ≥ 99% pages |
| Source-backed factual claims | 100% required or marked missing | 100% enforced |
| Export blocked on critical issues | 100% | 100% |
| Audit coverage of critical actions | 100% | 100% |
| User can complete first guided workflow | ≥ 80% pilot users | ≥ 90% |
| Assistant helpfulness score | ≥ 4.2/5 | ≥ 4.5/5 |
| Time to understand blocked state | < 60 sec median | < 30 sec median |
| Critical security findings open | 0 P0/P1 | 0 P0/P1 |

## UX falloff metrics

Track:
- abandoned onboarding flow
- repeated same-question assistant loops
- failed export attempts
- time spent on warnings
- users who do not reach first successful source-backed draft
- users who disable/ignore assistant guidance

