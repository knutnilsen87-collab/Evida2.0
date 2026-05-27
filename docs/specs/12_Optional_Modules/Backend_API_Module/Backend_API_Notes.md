# Advokat AI — Backend API Notes

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

## API principles

- REST JSON API.
- All IDs are UUID.
- All write endpoints require auth and permission check.
- All critical writes create `AuditEvent`.
- All agent-triggering endpoints create `AgentRun`.
- Use idempotency keys for critical operations.
- Use signed URLs for document upload/download.

## Core endpoints

| Method | Path | Purpose |
|---|---|---|
| POST | `/v1/cases` | Create case |
| GET | `/v1/cases` | List cases user can access |
| GET | `/v1/cases/{case_id}` | Get case |
| PATCH | `/v1/cases/{case_id}` | Update case metadata |
| POST | `/v1/cases/{case_id}/documents:init-upload` | Create signed upload |
| POST | `/v1/cases/{case_id}/documents:complete-upload` | Register uploaded document |
| GET | `/v1/cases/{case_id}/documents` | List documents |
| GET | `/v1/cases/{case_id}/documents/{document_id}` | Get document |
| POST | `/v1/cases/{case_id}/documents/{document_id}:process` | Start/retry processing |
| GET | `/v1/cases/{case_id}/facts` | List fact claims |
| POST | `/v1/cases/{case_id}/facts` | Create fact claim |
| PATCH | `/v1/cases/{case_id}/facts/{fact_id}` | Update/review fact claim |
| GET | `/v1/cases/{case_id}/timeline` | List timeline |
| POST | `/v1/cases/{case_id}/timeline` | Create event |
| GET | `/v1/cases/{case_id}/drafts` | List drafts |
| POST | `/v1/cases/{case_id}/drafts` | Create draft |
| PATCH | `/v1/cases/{case_id}/drafts/{draft_id}` | Update draft |
| POST | `/v1/cases/{case_id}/drafts/{draft_id}:check-sources` | Run source check |
| POST | `/v1/cases/{case_id}/exports:preview` | Preview export gate |
| POST | `/v1/cases/{case_id}/exports` | Create export package |
| GET | `/v1/cases/{case_id}/audit` | List audit events |
| POST | `/v1/assistant/chat` | Contextual assistant chat |
| POST | `/v1/assistant/guided-mode` | Start guided mode |

## Assistant request

```json
{
  "case_id": "uuid",
  "screen": "draft_editor",
  "object_type": "DraftDocument",
  "object_id": "uuid",
  "user_message": "Hvorfor kan jeg ikke eksportere?",
  "preferred_explanation_level": "simple",
  "guided_mode_allowed": true
}
```

## Assistant response

```json
{
  "answer_short": "Eksport er blokkert fordi to avsnitt mangler kilde.",
  "answer_simple": "Systemet stopper eksport når fakta i et dokument ikke kan spores til dokument, side eller Bates.",
  "next_actions": [
    {"label": "Vis avsnittene", "action": "navigate", "target": "missing_source_paragraphs"},
    {"label": "Fiks sammen med meg", "action": "start_guided_mode", "mode": "resolve_missing_sources"}
  ],
  "confidence": 0.91,
  "uncertainty_flags": [],
  "source_refs": []
}
```

