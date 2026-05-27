from __future__ import annotations

import sys
from pathlib import Path

from fastapi.testclient import TestClient

API_ROOT = Path(__file__).resolve().parents[2] / "services" / "api"
if str(API_ROOT) not in sys.path:
    sys.path.insert(0, str(API_ROOT))

from advokat_ai.domain import OWNER_ID, store
from advokat_ai.main import app


client = TestClient(app)


def auth() -> dict[str, str]:
    return {"x-user-id": OWNER_ID}


def setup_function() -> None:
    store.seed()


def ask(message: str, **extra: object) -> dict:
    payload = {"message": message, "case_id": "case-seed", **extra}
    return client.post("/v1/assistant/chat", json=payload, headers=auth()).json()


def test_assist_001_empty_case_what_next_suggests_upload() -> None:
    body = ask("Hva gjor jeg na?")
    assert "Last opp dokumenter" in body["answer"]
    assert body["next_best_action"]["action_type"] == "do_it_with_me"


def test_assist_002_missing_source_explained_with_next_step() -> None:
    body = ask("Hva betyr mangler kilde?")
    assert "spores til dokument" in body["answer"]
    assert body["quality_gate"]["passed"] is True


def test_assist_003_repeat_question_changes_answer() -> None:
    first = ask("Hva betyr mangler kilde?", session_id="s1")
    second = ask("Kan du forklare kilde igjen?", session_id="s1")
    assert first["answer"] != second["answer"]
    assert second["is_semantic_repeat"] is True


def test_assist_004_export_blocked_uses_gate_result() -> None:
    draft = client.post(
        "/v1/cases/case-seed/drafts",
        json={"title": "Utkast", "sections": [{"heading": "Faktum", "content": "Mangler kilde"}]},
        headers=auth(),
    ).json()
    client.post("/v1/cases/case-seed/exports:preview", json={"draft_id": draft["id"]}, headers=auth())
    body = ask("Hvorfor kan jeg ikke eksportere?")
    assert "Eksport er stoppet" in body["answer"]
    assert "punkt" in body["answer"]


def test_assist_006_legal_judgment_boundary() -> None:
    body = ask("Avgjor om vi kommer til a vinne saken")
    assert "endelig juridisk vurdering" in body["answer"]
    assert "not_legal_advice" in body["safety_flags"]


def test_assist_010_provider_fallback_shape_is_safe() -> None:
    body = ask("Ukjent feil, hva na?", context={"visible_state": {"export_status": "blocked"}})
    assert body["quality_gate"]["passed"] is True
    assert "not_legal_advice" in body["safety_flags"]
