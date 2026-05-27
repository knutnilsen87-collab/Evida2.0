# Advokat AI — Codex-Executable Test Matrix v1

This matrix defines tests Codex must implement or scaffold.

A feature is not done unless relevant tests pass.

---

# 1. Test categories

| Category | Required for |
|---|---|
| Unit | Pure domain logic, validators, state mappers |
| Contract | API request/response, schemas |
| Integration | DB/API/worker interactions |
| Permission | RBAC and tenant/case isolation |
| Audit | Material action emits audit |
| E2E | Critical user flows |
| Golden assistant | Assistant behavior and answer quality |
| Release gate | Official release readiness |

---

# 2. Foundation tests

| Test ID | Type | Scenario | Expected |
|---|---|---|---|
| FOUNDATION-001 | integration | local health endpoint | returns `{status: ok}` |
| FOUNDATION-002 | integration | migrations apply to empty DB | all tables created |
| FOUNDATION-003 | integration | seed data loads | tenant, users, case exist |
| FOUNDATION-004 | contract | OpenAPI validates | no schema errors |
| FOUNDATION-005 | unit | user-facing status mapping | no technical statuses leak |

---

# 3. Auth/RBAC/tenant tests

| Test ID | Type | Scenario | Expected |
|---|---|---|---|
| AUTH-001 | permission | unauthenticated request to `/v1/cases` | 401 |
| AUTH-002 | permission | case_viewer creates case | 403 |
| AUTH-003 | permission | case_editor creates fact in accessible case | 201 |
| AUTH-004 | permission | case_viewer creates fact | 403 |
| AUTH-005 | permission | user from tenant A fetches tenant B case | 403 or 404; no data leak |
| AUTH-006 | audit | denied sensitive access | audit event emitted |
| AUTH-007 | permission | external_collaborator reads only allowed case | allowed |
| AUTH-008 | permission | auditor reads audit but cannot edit case | read allowed, edit denied |
| AUTH-009 | integration | all case queries include tenant filter | cross-tenant fixture inaccessible |

---

# 4. Case room tests

| Test ID | Type | Scenario | Expected |
|---|---|---|---|
| CASE-001 | integration | create case with title/type | case created, audit emitted |
| CASE-002 | unit | default jurisdiction omitted | `NO` |
| CASE-003 | integration | overview with no documents | next action `Last opp dokumenter` |
| CASE-004 | integration | overview with missing sources | next action `Fiks manglende kilder` |
| CASE-005 | e2e | user creates and opens case | case overview shown |

---

# 5. Document pipeline tests

| Test ID | Type | Scenario | Expected |
|---|---|---|---|
| DOC-001 | integration | init upload | returns upload URL/token |
| DOC-002 | integration | complete upload | document record + audit |
| DOC-003 | worker | valid PDF processed | pages/chunks/hash created |
| DOC-004 | worker | scanned PDF OCR success | pages OCR complete |
| DOC-005 | worker | one low-confidence OCR page | document `needs_review`; user message shown |
| DOC-006 | worker | unsupported file type | `validation_failed`, no OCR job |
| DOC-007 | worker | duplicate complete-upload idempotency | one document only |
| DOC-008 | integration | document hash mismatch after reprocess | status `needs_review` |
| DOC-009 | permission | user without access fetches document | 403/404 |
| DOC-010 | audit | processing lifecycle | audit events emitted |
| DOC-011 | UI | status `ocr_low_confidence` | user sees «Denne siden er usikkert lest...» |

---

# 6. Source/fact/evidence tests

| Test ID | Type | Scenario | Expected |
|---|---|---|---|
| SRC-001 | integration | create source ref to page | source ref status valid |
| SRC-002 | integration | create source ref without page/chunk/bates | 400 |
| SRC-003 | integration | create documented fact with source | source_status documented |
| SRC-004 | integration | create fact without source | source_status missing_source |
| SRC-005 | integration | mark fact documented without source | blocked |
| SRC-006 | UI | missing source fact | user sees «Mangler kilde» |
| SRC-007 | audit | source ref created | audit emitted |
| SRC-008 | integration | evidence links to source refs | relation stored |
| SRC-009 | integration | timeline event with unknown date | allowed with date_status unknown |

---

# 7. Draft/source coverage tests

| Test ID | Type | Scenario | Expected |
|---|---|---|---|
| DRAFT-001 | integration | create draft | draft created |
| DRAFT-002 | integration | draft section without source | coverage partial/blocked |
| DRAFT-003 | integration | all sections sourced | coverage pass |
| DRAFT-004 | UI | missing source paragraph | inline warning shown |
| DRAFT-005 | audit | draft updated | audit emitted |
| DRAFT-006 | e2e | user creates draft and checks work | assistant/check flow opens |

---

# 8. Export/control gate tests

| Test ID | Type | Scenario | Expected |
|---|---|---|---|
| EXPORT-001 | integration | draft has missing source section | export gate status `blocked` |
| EXPORT-002 | integration | low-confidence OCR page used as source | gate `blocked` or `needs_approval` |
| EXPORT-003 | integration | critical unresolved risk | gate blocked |
| EXPORT-004 | integration | all source checks pass | gate `needs_approval` or `pass` depending policy |
| EXPORT-005 | integration | create export without gate | 409 |
| EXPORT-006 | integration | create export with stale gate result | 409 |
| EXPORT-007 | integration | create export without approval when required | 409 |
| EXPORT-008 | integration | create export after gate pass + approval | export package created |
| EXPORT-009 | audit | export package created | audit emitted with gate/approval refs |
| EXPORT-010 | UI | export blocked | user sees useful blocker summary, not raw codes |
| EXPORT-011 | assistant | ask why export blocked | assistant summarizes exact blockers |

---

# 9. Assistant golden tests

| Test ID | Type | Scenario | Expected |
|---|---|---|---|
| ASSIST-001 | golden | user asks «Hva gjør jeg nå?» on empty case | suggests upload documents |
| ASSIST-002 | golden | user asks «Hva betyr mangler kilde?» | simple explanation + next step |
| ASSIST-003 | golden | user repeats same question differently | not same answer; builds on prior |
| ASSIST-004 | golden | user asks why export blocked | uses gate result; lists blockers |
| ASSIST-005 | golden | user seems confused | switches to simpler explanation |
| ASSIST-006 | golden | user asks final legal judgment | sets human legal boundary |
| ASSIST-007 | golden | user asks product help on document screen | uses current screen/document context |
| ASSIST-008 | golden | assistant answer includes technical jargon | quality gate fails |
| ASSIST-009 | golden | assistant proposes critical action | requires preview/approval |
| ASSIST-010 | golden | provider unavailable | deterministic fallback, no fabrication |

---

# 10. Visible UI/copy tests

| Test ID | Type | Scenario | Expected |
|---|---|---|---|
| COPY-001 | unit | internal status mapping | all mapped to Norwegian user copy |
| COPY-002 | UI | default case overview | no raw technical statuses |
| COPY-003 | UI | document error | calm actionable message |
| COPY-004 | UI | audit view | technical details only visible to allowed role |
| COPY-005 | UI | blocked export | no `export_gate_blocked` visible |
| COPY-006 | UI | OCR warning | no `confidence threshold` visible |

---

# 11. Audit tests

| Test ID | Type | Scenario | Expected |
|---|---|---|---|
| AUDIT-001 | integration | case created | audit event |
| AUDIT-002 | integration | document uploaded | audit event |
| AUDIT-003 | integration | source ref created | audit event |
| AUDIT-004 | integration | draft updated | audit event |
| AUDIT-005 | integration | export preview | audit event |
| AUDIT-006 | integration | approval decision | audit event |
| AUDIT-007 | integration | export created | audit event |
| AUDIT-008 | integration | update audit event | blocked |
| AUDIT-009 | integration | delete audit event | blocked |

---

# 12. Release gate tests

| Test ID | Type | Scenario | Expected |
|---|---|---|---|
| RELEASE-001 | script | run all backend tests | pass |
| RELEASE-002 | script | run all frontend tests | pass |
| RELEASE-003 | script | run OpenAPI validation | pass |
| RELEASE-004 | script | run migrations from empty DB | pass |
| RELEASE-005 | script | run permission suite | pass |
| RELEASE-006 | script | run assistant golden tests | pass |
| RELEASE-007 | script | run export gate suite | pass |
| RELEASE-008 | script | run audit immutability suite | pass |
| RELEASE-009 | manual | legal review sign-off | recorded |
| RELEASE-010 | manual | security review sign-off | recorded |
| RELEASE-011 | manual | compliance review sign-off | recorded |
| RELEASE-012 | manual | pilot owner sign-off | recorded |

---

# 13. Codex implementation rule

If Codex implements a feature from this package, it must add or update the relevant tests in this matrix.

Do not mark done with “tests not added” unless:
- feature is pure documentation, or
- a test blocker is explicitly documented in the plan and follow-up issue.
