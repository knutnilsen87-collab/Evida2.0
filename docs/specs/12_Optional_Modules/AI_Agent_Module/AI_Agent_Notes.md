# Advokat AI — AI Agent Notes

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

## AI legal assistant / collaboration partner

The AI chat assistant is a first-class product surface. It must feel like a calm legal assistant and collaboration partner, not a generic chatbot.

### Assistant jobs
- Explain every part of the program in the user's own language.
- Help the user understand what they are seeing.
- Recommend safe next steps.
- Guide the user through workflows without mental overload.
- Explain warnings, blocked states, missing sources and export gates.
- Help with legal work product while preserving source discipline.
- Make onboarding happen through real work, not manuals.

### Desired user feeling
The user should repeatedly feel: **“Dette var jo lett.”**

### Interaction rule
When answering product-use questions, the assistant must use this sequence by default:

1. Give a short answer.
2. Explain it simply.
3. Show the next concrete action.
4. Offer “vis meg” / guided mode.
5. Reveal deeper details only if requested.

### Guided modes
The assistant must support:
- `explain_this`: explain current screen/object/warning
- `show_me_how`: highlight UI and walk the user through steps
- `do_it_with_me`: interactive step-by-step guided completion
- `check_my_work`: inspect readiness, missing sources, risks and next steps
- `why_blocked`: explain blocked/export-prevented states
- `what_next`: recommend next best action
- `legal_work_help`: help structure facts, evidence, chronology, argument and draft

### Falloff prevention
The app must detect signs of confusion:
- repeated navigation between same screens
- long idle time on blocked state
- repeated assistant queries about same topic
- abandoned workflow
- repeated failed export/control gate attempts

When detected, the app must offer:
- simpler explanation
- guided walkthrough
- reduced UI complexity
- next best step
- “do this together with me”

## Agent catalog

| Agent | Purpose | Output |
|---|---|---|
| Document Agent | classify/inspect documents | document summary, issue flags |
| OCR Agent | page text extraction | OCR status, text, confidence |
| Source Agent | create/check source anchors | SourceRef, coverage |
| Fact Agent | propose fact claims | FactClaim candidates |
| Chronology Agent | propose timeline | TimelineEvent candidates |
| Evidence Agent | map evidence | EvidenceItem candidates |
| Argument Agent | structure legal arguments | Argument candidates |
| Risk Agent | identify risks/conflicts | RiskItem candidates |
| Draft Agent | create drafts | DraftDocument |
| Quality Agent | run final checks | gate findings |

All agents are bounded, audited and non-authoritative.

