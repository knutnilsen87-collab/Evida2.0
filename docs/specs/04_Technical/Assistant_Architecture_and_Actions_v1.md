# Advokat AI — Assistant Architecture and Actions v1

## 1. Purpose

The assistant is a legal collaboration partner and product guide.

It must combine:
- product context
- case context
- document/source context
- conversation memory
- intent recognition
- anti-repetition logic
- guided actions
- safety/legal boundaries
- useful-only output

The assistant must not be implemented as a plain stateless chat completion.

---

# 2. Assistant service architecture

```text
Frontend Assistant Panel
  ↓
Assistant API Endpoint
  ↓
Assistant Orchestrator
  ├─ Context Builder
  ├─ Permission Filter
  ├─ Intent Classifier
  ├─ Topic/Answer Fingerprint Engine
  ├─ Retrieval/Context Selector
  ├─ Response Planner
  ├─ Provider Adapter
  ├─ Response Quality Gate
  ├─ Guided Action Builder
  └─ Audit Writer
  ↓
Assistant Response
```

---

# 3. Modules

## 3.1 Context Builder

Builds context from:
- current route
- selected object
- current case
- visible warnings
- source coverage
- document status
- draft status
- export gate status
- role/permissions
- prior conversation summary
- recent assistant answer fingerprints

Must never include data from another case.

## 3.2 Permission Filter

Before context is sent to provider:
- remove objects user cannot access
- remove raw sensitive values when not needed
- enforce tenant/case boundary
- ensure external collaborators only see allowed scopes

## 3.3 Intent Classifier

Classifies into:

| Intent | Meaning |
|---|---|
| `product_help` | user asks how program works |
| `screen_explanation` | user asks about current UI |
| `why_blocked` | user asks why action is blocked |
| `what_next` | user asks what to do next |
| `source_help` | user asks about sources/kilde |
| `document_help` | user asks about document/OCR/page |
| `draft_help` | user asks about writing/editing |
| `legal_work_help` | user asks for legal work support |
| `legal_judgment_boundary` | user asks final legal judgment |
| `settings_help` | user asks about configuration |
| `error_help` | user asks about issue/error |
| `unknown` | unclear |

## 3.4 Topic Fingerprint Engine

Creates semantic fingerprint:
- topic family
- object type
- object id if relevant
- question type
- user confusion indicator

Example:

```json
{
  "topic_family": "export_gate",
  "object_type": "draft",
  "object_id": "DRAFT-123",
  "question_type": "why",
  "normalized_intent": "why_export_blocked",
  "fingerprint": "export_gate.draft.why.missing_sources"
}
```

## 3.5 Answer Fingerprint Engine

Stores:
- response summary
- explanation level
- examples used
- next step offered
- whether guided action offered
- whether user seemed satisfied

Used to avoid repetitive answers.

## 3.6 Response Planner

Determines:
- answer mode
- explanation level
- whether to include guided action
- whether to mention previous answer
- whether legal boundary warning is needed
- whether a control gate is involved

## 3.7 Provider Adapter

Provider interface must support:
- mock provider for tests
- local/dev deterministic provider
- production provider via secrets
- structured JSON output
- timeout handling
- safety fallback

Provider-specific code must not leak outside assistant package.

## 3.8 Response Quality Gate

Checks:
- not generic
- not repetitive
- context-specific
- no hidden uncertainty
- no technical jargon
- no unauthorized action
- user-facing copy is useful
- legal boundary preserved
- contains next step when appropriate

If fails:
- rewrite with stricter instructions
- fallback to deterministic safe answer
- log assistant_quality_gate_failed event

---

# 4. Assistant database objects

## `assistant_sessions`

Fields:
- id
- tenant_id
- case_id nullable
- user_id
- started_at
- ended_at nullable
- current_summary
- last_intent_fingerprint
- created_at

## `assistant_messages`

Fields:
- id
- session_id
- tenant_id
- case_id nullable
- user_id
- role: user|assistant|system
- content_redacted
- content_storage_policy
- intent
- topic_fingerprint
- answer_fingerprint
- referenced_objects jsonb
- safety_flags jsonb
- created_at

Privacy:
- store only what is necessary
- allow redaction/summarization
- never use for model training by default

## `assistant_guided_actions`

Fields:
- id
- assistant_message_id
- tenant_id
- case_id
- action_type
- label
- payload jsonb
- requires_approval
- may_change_data
- status
- created_at
- completed_at

---

# 5. Assistant request schema

```json
{
  "session_id": "uuid",
  "message": "Hvorfor får jeg ikke eksportert?",
  "case_id": "uuid",
  "context": {
    "current_route": "/cases/{caseId}/drafts/{draftId}",
    "current_screen": "draft_editor",
    "selected_object": {"type": "draft", "id": "uuid"},
    "visible_state": {
      "missing_source_count": 3,
      "ocr_warning_count": 2,
      "export_status": "blocked"
    }
  },
  "preferred_answer_level": "simple"
}
```

---

# 6. Assistant response schema

```json
{
  "message_id": "uuid",
  "session_id": "uuid",
  "answer": "Eksport er stoppet fordi ...",
  "mode": "why_blocked",
  "answer_level": "simple",
  "detected_intent": "why_blocked",
  "topic_fingerprint": "export_gate.draft.why.missing_sources",
  "is_semantic_repeat": true,
  "repeat_strategy": "explain_difference",
  "referenced_objects": [
    {"type": "draft", "id": "uuid"}
  ],
  "next_best_action": {
    "label": "Fiks manglende kilder sammen med meg",
    "action_type": "do_it_with_me"
  },
  "guided_actions": [
    {
      "action_type": "do_it_with_me",
      "label": "Fiks manglende kilder",
      "requires_approval": false,
      "may_change_data": false,
      "steps": []
    }
  ],
  "safety_flags": [
    "not_legal_advice",
    "requires_human_review_before_export"
  ],
  "quality_gate": {
    "passed": true,
    "checks": {
      "context_specific": true,
      "not_repetitive": true,
      "no_technical_jargon": true,
      "has_next_step": true
    }
  }
}
```

---

# 7. Allowed assistant actions

Assistant may:
- explain current screen
- explain object status
- explain blocked state
- propose next step
- start guided walkthrough
- highlight UI element
- draft suggestions for user review
- summarize missing sources
- check readiness
- prepare export preview request
- create non-critical draft suggestions after user confirms
- propose fact/source links for review

Assistant may not:
- approve export
- bypass gate
- submit final document externally
- delete audit data
- grant permissions
- expose another case
- make final legal judgment
- mark uncertain source as verified without user review
- change data silently

---

# 8. Control gate integration

When assistant is asked about blocked export, it must call/read Export Gate result, not guess.

Flow:
1. user asks
2. assistant reads current gate result or triggers preview if allowed
3. assistant summarizes blockers in plain language
4. assistant offers guided action to fix first blocker
5. assistant logs event

---

# 9. Anti-repetition algorithm

Pseudo:

```python
def plan_answer(user_message, context, session_history):
    intent = classify_intent(user_message, context)
    topic_fp = make_topic_fingerprint(intent, context)
    similar = find_similar_previous_answers(topic_fp, session_history)

    if not similar:
        strategy = "full_contextual_answer"
    elif user_message_asks_new_angle(user_message, similar):
        strategy = "explain_difference"
    elif user_seems_confused(session_history):
        strategy = "change_explanation_mode"
    else:
        strategy = "short_refinement_with_next_step"

    return ResponsePlan(intent=intent, topic_fp=topic_fp, strategy=strategy)
```

---

# 10. Deterministic fallback answers

If provider fails, use safe deterministic response based on context.

Example blocked export fallback:
> «Eksport er stoppet fordi saken ikke er klar ennå. Åpne kontrollen for å se punktene som må ryddes. Jeg kan gå gjennom første punkt med deg.»

Fallback must never fabricate legal analysis.

---

# 11. Audit events

Emit:
- `assistant_message_created`
- `assistant_guided_action_created`
- `assistant_guided_action_completed`
- `assistant_quality_gate_failed`
- `assistant_legal_boundary_triggered`
- `assistant_control_gate_explained`

Audit should store references and summaries, not unnecessary sensitive full text by default.

---

# 12. Golden tests required

See:
- `06_QA/Assistant_Golden_Tests_v1.md`
- `06_QA/Test_Matrix_Codex_Executable_v1.md`
