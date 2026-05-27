# Advokat AI — Analytics Tracking Plan

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

## Analytics principles

Do not track document content in analytics. Track metadata and UX events only.

## Events

| Event | Properties |
|---|---|
| `case.created` | tenant_id, user_role, case_type |
| `document.uploaded` | mime_type, size_bucket, page_count_bucket |
| `document.processing_completed` | duration_bucket, page_count_bucket, ocr_quality_bucket |
| `assistant.opened` | screen, object_type |
| `assistant.question_asked` | intent_class, screen, object_type, no content |
| `guided_mode.started` | mode, screen |
| `guided_mode.completed` | mode, steps_count, duration_bucket |
| `control_gate.failed` | gate_type, reason_codes |
| `control_gate.passed` | gate_type |
| `export.attempted` | draft_type, gate_status |
| `export.completed` | draft_type |
| `falloff_signal.detected` | signal_type, screen |
| `source_claim.created` | source_count_bucket, confidence_bucket |

