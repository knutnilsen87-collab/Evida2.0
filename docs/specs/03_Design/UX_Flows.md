# Advokat AI — UX Flows

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

## Core journeys

### Journey 1 — First case with guided assistant

1. User creates case.
2. Assistant welcomes user with one sentence and asks what they want to accomplish.
3. User uploads documents.
4. Assistant explains processing statuses in simple language.
5. System shows document coverage.
6. User asks: “Hva gjør jeg nå?”
7. Assistant recommends: review extracted facts, then build chronology.
8. User accepts guided mode.
9. UI highlights next step and assistant explains each action.
10. User completes first source-backed chronology event.

### Journey 2 — Why is export blocked?

1. User tries to export draft.
2. Export Gate blocks.
3. Assistant says: “Eksport er stoppet fordi 3 avsnitt mangler kilde og 1 dokument ikke er ferdig OCR-behandlet.”
4. Assistant offers buttons: `Vis avsnittene`, `Fiks sammen med meg`, `Forklar enkelt`.
5. User selects guided fix.
6. System walks user through resolving each issue.
7. Export gate is re-run.
8. Approval requested.

### Journey 3 — Legal collaboration partner

1. User opens evidence map.
2. User asks: “Hva er svakhetene i saken?”
3. Assistant reviews source-backed facts and risk items.
4. Assistant answers with documented weaknesses, not speculation.
5. Assistant distinguishes documented, uncertain and missing evidence.
6. User asks for draft response.
7. Assistant creates outline with citations and uncertainty flags.

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
