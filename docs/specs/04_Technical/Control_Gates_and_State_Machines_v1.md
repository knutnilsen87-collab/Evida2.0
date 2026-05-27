# Advokat AI — Control Gates and State Machines v1

## 1. Purpose

Control gates prevent legal-risk actions from happening too easily.

Critical operations must be previewed, explained and approved when required.

---

# 2. Critical operations

The following operations require a gate or preview:

| Operation | Gate | Approval required |
|---|---|---|
| Final export | export gate | yes when policy says |
| External sharing | external share gate | yes |
| Bulk fact/source changes | bulk change gate | maybe |
| Mark document source-verified manually | source verification gate | yes for uncertain OCR |
| Delete/retention action | data lifecycle gate | yes |
| Permission change | access control gate | yes for external users |

---

# 3. Export gate

## Inputs
- case_id
- draft_id
- draft sections
- source coverage
- fact claims
- source refs
- document/page statuses
- OCR warnings
- risk items
- approval policy
- user role

## Checks

| Check | Blocks when |
|---|---|
| missing source | draft section or documented fact lacks source |
| invalid source | source ref invalid or points to changed document |
| OCR uncertainty | source uses low-confidence/unverified page |
| unresolved critical risk | risk item critical/open |
| stale draft | draft changed after latest gate |
| stale approval | approval not tied to current gate |
| permission | user lacks export permission |
| document coverage | required document pages not processed |
| sensitive data | sensitive marker requires review |

## Output

```json
{
  "status": "blocked",
  "user_summary": "Eksport er stoppet fordi 3 påstander mangler kilde.",
  "blockers": [
    {
      "code": "missing_source",
      "user_message": "3 påstander mangler kilde.",
      "severity": "high",
      "affected_object": {
        "type": "draft_section",
        "id": "uuid",
        "label": "Avsnitt 4"
      }
    }
  ],
  "warnings": [],
  "approval_required": true
}
```

## User copy

Never show:
- `export_gate_blocked`
- `validator_failed`
- `source_ref_missing`

Show:
- «Eksport er stoppet fordi noe må kontrolleres først.»
- «3 påstander mangler kilde.»
- «2 sider må ses over før de kan brukes som kilde.»

---

# 4. Document state machine

```text
uploaded
→ validating
→ virus_scanning
→ validated
→ extracting_pages
→ ocr_pending
→ ocr_running
→ chunking
→ hashing
→ indexing
→ needs_review | source_verified
```

Blocked:
- validation_failed
- virus_blocked
- ocr_failed
- partial_ocr_failed
- corrupted
- quarantined
- processing_failed

No document may become `source_verified` if:
- page count unknown
- critical OCR failed
- hash missing
- malware scan failed
- validation failed

---

# 5. Fact claim state machine

```text
missing_source
→ documented
→ disputed | needs_review
```

Allowed states:
- documented
- missing_source
- disputed
- assumed
- needs_review

Rules:
- `documented` requires at least one valid source ref
- `assumed` cannot be presented as documented
- `disputed` must be visible in UI
- export gate must treat undocumented/assumed according to policy

---

# 6. Draft state machine

```text
draft
→ source_checked
→ review_required
→ approved
→ export_ready
→ exported
```

Blocked:
- missing_source
- unresolved_conflict
- policy_blocked
- insufficient_coverage

Rules:
- `export_ready` requires source coverage pass
- `exported` requires gate result + approval + export package
- `approved` must include approval_decision ref

---

# 7. Approval binding

Approval is valid only for:
- exact target_type
- exact target_id
- exact gate result
- exact draft version/snapshot
- same case
- same tenant

If target changes after approval:
- approval becomes stale
- export blocked

---

# 8. Assistant integration

For any blocked state, assistant must:
1. read actual gate/state result
2. explain in user language
3. list specific blockers
4. offer guided next step
5. not bypass gate

---

# 9. Audit requirements

Every gate must emit:
- `control_gate_previewed`
- `control_gate_passed` or `control_gate_blocked`
- `approval_created` where relevant
- `export_created` where relevant

Audit event must include:
- actor
- case_id
- target
- gate result id
- blocker summary
- timestamp
