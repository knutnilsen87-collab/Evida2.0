from __future__ import annotations

from hashlib import sha256
from typing import Any


def process_pdf_fixture(filename: str, text: str, mime_type: str = "application/pdf") -> dict[str, Any]:
    if mime_type != "application/pdf":
        return {"status": "validation_failed", "pages": [], "chunks": [], "user_message": "Filen kan ikke behandles."}
    low_confidence = "LOW_CONFIDENCE" in text
    page = {
        "page_number": 1,
        "ocr_status": "low_confidence" if low_confidence else "complete",
        "ocr_text": text,
        "text_hash": sha256(text.encode("utf-8")).hexdigest(),
        "warnings": ["Denne siden er usikkert lest. Se over teksten for du bruker den som kilde."] if low_confidence else [],
    }
    chunk = {
        "chunk_index": 0,
        "text": text,
        "text_hash": page["text_hash"],
        "source_span": {"page": 1},
    }
    return {
        "filename": filename,
        "status": "needs_review" if low_confidence else "source_verified",
        "pages": [page],
        "chunks": [chunk],
        "sha256": sha256(text.encode("utf-8")).hexdigest(),
    }
