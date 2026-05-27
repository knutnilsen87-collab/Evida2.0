from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from worker.pipeline import process_pdf_fixture


def test_valid_pdf_creates_pages_chunks_and_hash() -> None:
    result = process_pdf_fixture("sak.pdf", "Avtaletekst")
    assert result["status"] == "source_verified"
    assert result["pages"][0]["ocr_status"] == "complete"
    assert result["chunks"][0]["text"] == "Avtaletekst"
    assert len(result["sha256"]) == 64


def test_low_confidence_fixture_needs_review() -> None:
    result = process_pdf_fixture("scan.pdf", "LOW_CONFIDENCE tekst")
    assert result["status"] == "needs_review"
    assert result["pages"][0]["warnings"]


def test_unsupported_file_type_is_rejected() -> None:
    result = process_pdf_fixture("bilde.png", "tekst", mime_type="image/png")
    assert result["status"] == "validation_failed"
