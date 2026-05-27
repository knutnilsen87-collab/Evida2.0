# Advokat AI — Acceptance Criteria

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

## Acceptance criteria by area

### Case
- User can create case.
- Unauthorized user cannot access case.
- Case archive prevents new edits unless reopened by authorized user.
- Audit event is written.

### Document
- Upload creates immutable document record.
- Hash is calculated.
- Processing statuses are visible.
- OCR failure is explained with next action.
- User can retry processing.

### Source/fact
- Fact without source is marked `missing_source`.
- Fact with source shows document/page/Bates.
- User can approve/reject/edit.
- Export cannot silently use unsupported facts.

### Assistant
- Explains current screen.
- Explains blocked states.
- Offers guided mode.
- Does not produce legal certainty without source basis.
- Logs material agent runs.

### Export
- Preview shows all blockers.
- Export blocked if missing source/critical risk.
- Approval required.
- Export package hashed and audited.

---

# v0.4 Hard Addendum — Assistant and Useful UI

## Binding updates

1. The AI assistant must be experienced as a legal assistant and collaboration partner, not a chatbot.
2. The assistant must help with both legal work and all questions about how the program works.
3. The assistant must answer in context, use the user's own phrasing, and reduce mental load.
4. The assistant must not provide generic repeated standard answers.
5. The assistant must recognize when a new question is a reformulation of a previous topic and adapt the answer.
6. The assistant must support guided modes: `explain_this`, `show_me_how`, `do_it_with_me`, `check_my_work`, `why_blocked`, `what_next`, `legal_work_help`.
7. All visible UI information must be useful to the user.
8. Technical expressions and internal processing details are hidden by default.
9. Default UI copy must be practical, understandable Norwegian.
10. Advanced/audit/technical details are available only when relevant and authorized.

## User-experience promise

The user should repeatedly feel:

> «Dette var jo lett — jeg skjønner hva jeg skal gjøre nå.»

## Codex implementation pointer

For exact implementation rules, Codex must use:
- `03_Design/AI_Assistant_UX_Contract_v1.md`
- `03_Design/Visible_Only_Useful_UI_Rule_v1.md`
- `03_Design/Screen_by_Screen_UI_Contracts_v1.md`
- `04_Technical/Assistant_Architecture_and_Actions_v1.md`
- `06_QA/Assistant_Golden_Tests_v1.md`
