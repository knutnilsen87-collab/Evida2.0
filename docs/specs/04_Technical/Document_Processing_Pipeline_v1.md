# Advokat AI — Document Processing Pipeline v1

## 1. Purpose

The document pipeline turns uploaded legal documents into source-verifiable pages, chunks and source references.

It must support real legal documents in Pilot Candidate.

---

# 2. Supported file types

Pilot Candidate required:
- PDF
- scanned PDF
- image files: PNG/JPEG/TIFF
- DOCX import may be supported through conversion interface but is not required for first PDF pipeline

Official Release target:
- PDF
- scanned PDF
- DOCX
- EML/MSG email import
- PNG/JPEG/TIFF
- bundled document sets

---

# 3. State machine

## Document states

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

## Failure/block states

```text
validation_failed
virus_blocked
ocr_failed
partial_ocr_failed
corrupted
quarantined
processing_failed
```

## User-facing status mapping

| Internal | User-facing |
|---|---|
| `uploaded` | «Lastet opp» |
| `validating` | «Kontrollerer fil» |
| `virus_scanning` | «Sikkerhetskontrollerer» |
| `extracting_pages` | «Deler opp dokumentet» |
| `ocr_running` | «Leser tekst» |
| `chunking` | «Klargjør som kilde» |
| `indexing` | «Gjør dokumentet søkbart» |
| `needs_review` | «Må ses over» |
| `source_verified` | «Klar som kilde» |
| `partial_ocr_failed` | «Noen sider må ses over» |
| `processing_failed` | «Kunne ikke behandles» |
| `quarantined` | «Stoppet av sikkerhetskontroll» |

---

# 4. Pipeline steps

## Step 1 — Init upload

API:
`POST /v1/cases/{case_id}/documents:init-upload`

Creates:
- document upload token
- signed upload URL or local upload target
- expected content type
- max size
- idempotency key

No document record is final until complete-upload.

## Step 2 — Complete upload

API:
`POST /v1/cases/{case_id}/documents:complete-upload`

Creates:
- `Document`
- `DocumentVersion`
- `AuditEvent(document_uploaded)`
- worker job `document.process`

Must calculate:
- file sha256
- storage uri
- size bytes
- initial status `uploaded`

## Step 3 — Validation

Checks:
- supported MIME type
- readable file
- page count if PDF
- size limit
- no encrypted unsupported PDF unless explicitly supported
- file hash matches upload metadata

Failure:
- status `validation_failed`
- user copy: «Filen kunne ikke leses som et støttet dokument.»

## Step 4 — Malware/virus scan

For local dev:
- mock scanner returns pass

Production:
- provider interface

Failure:
- status `quarantined`
- no further processing
- audit event `document_quarantined`

## Step 5 — Page extraction

Creates one `Page` per page.

Fields:
- document_id
- page_number
- image_hash optional
- text_hash nullable until OCR
- bates_label optional
- exhibit_label optional
- ocr_status `pending`

## Step 6 — OCR

OCR provider returns:
- text
- confidence
- bounding boxes optional
- language
- warnings

Page status:
- `ocr_complete` if confidence acceptable
- `ocr_low_confidence` if uncertain
- `ocr_failed` if failed

Document state:
- `source_verified` only if all required pages are readable/verified
- `needs_review` if any page is uncertain
- `partial_ocr_failed` if some pages failed

## Step 7 — Chunking

Chunking rules:
- chunk by page first
- preserve page boundaries
- target 700–1200 tokens per chunk
- overlap 100–150 tokens where continuous text
- never merge across documents
- preserve quote spans
- store source span JSON

Each chunk stores:
- chunk_index
- page_id
- text
- text_hash
- source_span
- embedding_ref optional

## Step 8 — Hashing

Required:
- document sha256
- page text hash when OCR exists
- page image hash if rendered image exists
- chunk text hash

Hash mismatch later must produce:
- document status `needs_review`
- user copy: «Dokumentet ser ut til å være endret siden analysen ble gjort.»

## Step 9 — Indexing

Index:
- document metadata
- OCR text
- chunks
- source anchors

Vector embeddings optional behind interface.

## Step 10 — Source readiness evaluation

Document is `source_verified` when:
- validation passed
- scan passed
- all pages processed or intentionally excluded
- no critical OCR failure
- hashes stored
- page count known

Document is `needs_review` when:
- OCR uncertain
- page missing text
- hash mismatch
- page count mismatch
- image-only page requires manual review

---

# 5. Idempotency

Every worker job must be idempotent.

Use:
- job_id
- document_version_id
- input_hash
- step_name
- attempt_count

If a job is retried, it must not duplicate pages/chunks.

---

# 6. Retry policy

| Failure | Retry? | Max | Notes |
|---|---:|---:|---|
| temporary storage read error | yes | 3 | exponential backoff |
| OCR provider timeout | yes | 3 | mark page uncertain after max |
| unsupported file | no | 0 | validation_failed |
| malware/quarantine | no | 0 | blocked |
| database constraint | no | 0 | developer error |
| chunking transient error | yes | 2 | safe idempotent retry |

---

# 7. Audit events

Emit:
- `document_upload_initiated`
- `document_uploaded`
- `document_validation_started`
- `document_validation_failed`
- `document_scan_passed`
- `document_quarantined`
- `document_processing_started`
- `document_pages_extracted`
- `document_ocr_completed`
- `document_ocr_needs_review`
- `document_chunking_completed`
- `document_source_verified`
- `document_processing_failed`

---

# 8. API response behavior

Do not show raw job state unless advanced.

Default response should include:
- document id
- user-facing status
- whether user can act
- next useful action
- warnings summary

Example:

```json
{
  "document_id": "uuid",
  "status": "needs_review",
  "user_status": "Må ses over",
  "summary": "2 sider er usikkert lest.",
  "next_action": {
    "label": "Se usikre sider",
    "href": "/cases/.../documents/... ?filter=needs_review"
  }
}
```

---

# 9. Tests required

- PDF upload success
- scanned PDF with OCR success
- partial OCR failure
- unsupported file
- cross-tenant document access denied
- duplicate complete-upload idempotency
- page/chunk uniqueness
- hash mismatch detection
- document status mapping user copy
