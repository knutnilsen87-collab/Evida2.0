from __future__ import annotations

from fastapi.testclient import TestClient

from advokat_ai.domain import AUDITOR_ID, EDITOR_ID, OTHER_TENANT_ID, OWNER_ID, VIEWER_ID, store
from advokat_ai.main import app


client = TestClient(app)


def auth(user_id: str = OWNER_ID) -> dict[str, str]:
    return {"x-user-id": user_id}


def setup_function() -> None:
    store.seed()


def make_processed_document(case_id: str = "case-seed") -> dict:
    init = client.post(
        f"/v1/cases/{case_id}/documents:init-upload",
        json={"filename": "bevis.pdf", "mime_type": "application/pdf", "size_bytes": 120},
        headers=auth(),
    )
    token = init.json()["upload_token"]
    doc = client.post(
        f"/v1/cases/{case_id}/documents:complete-upload",
        json={"upload_token": token, "text": "Avtalen ble signert 2026-05-27."},
        headers=auth(),
    ).json()
    return client.post(f"/v1/cases/{case_id}/documents/{doc['id']}:process", headers=auth()).json()


def test_health_endpoint_returns_ok() -> None:
    assert client.get("/health").json() == {"status": "ok"}


def test_unauthenticated_cases_request_is_401() -> None:
    assert client.get("/v1/cases").status_code == 401


def test_viewer_cannot_create_case_and_denial_is_audited() -> None:
    response = client.post("/v1/cases", json={"title": "Nei"}, headers=auth(VIEWER_ID))
    assert response.status_code == 403
    assert any(event["action"] == "access_denied" for event in store.audit_events)


def test_create_case_uses_default_jurisdiction_and_audit() -> None:
    response = client.post("/v1/cases", json={"title": "Ny sak"}, headers=auth())
    assert response.status_code == 201
    body = response.json()
    assert body["jurisdiction"] == "NO"
    assert body["overview"]["next_action"] == "Last opp dokumenter"
    assert any(event["action"] == "case_created" for event in store.audit_events)


def test_cross_tenant_case_is_inaccessible() -> None:
    response = client.get("/v1/cases/case-seed", headers=auth(OTHER_TENANT_ID))
    assert response.status_code == 404


def test_document_upload_process_and_low_confidence_status() -> None:
    init = client.post(
        "/v1/cases/case-seed/documents:init-upload",
        json={"filename": "scan.pdf", "mime_type": "application/pdf", "size_bytes": 99},
        headers=auth(),
    )
    token = init.json()["upload_token"]
    doc = client.post(
        "/v1/cases/case-seed/documents:complete-upload",
        json={"upload_token": token, "text": "LOW_CONFIDENCE skannet tekst"},
        headers=auth(),
    ).json()
    processed = client.post(f"/v1/cases/case-seed/documents/{doc['id']}:process", headers=auth()).json()
    assert processed["status"] == "needs_review"
    assert processed["pages"][0]["warnings"][0].startswith("Denne siden er usikkert lest")
    assert any(event["action"] == "document_uploaded" for event in store.audit_events)


def test_source_ref_and_fact_source_rules() -> None:
    doc = make_processed_document()
    page = doc["pages"][0]
    invalid = client.post(
        "/v1/cases/case-seed/source-refs",
        json={"document_id": doc["id"]},
        headers=auth(EDITOR_ID),
    )
    assert invalid.status_code == 400
    source = client.post(
        "/v1/cases/case-seed/source-refs",
        json={"document_id": doc["id"], "page_id": page["id"], "quote": "Avtalen ble signert"},
        headers=auth(EDITOR_ID),
    ).json()
    fact = client.post(
        "/v1/cases/case-seed/facts",
        json={"text": "Avtalen ble signert.", "source_ref_ids": [source["id"]]},
        headers=auth(EDITOR_ID),
    ).json()
    assert fact["source_status"] == "documented"
    missing = client.post(
        "/v1/cases/case-seed/facts",
        json={"text": "Uten dokumentasjon."},
        headers=auth(EDITOR_ID),
    ).json()
    assert missing["source_status"] == "missing_source"
    blocked = client.patch(
        f"/v1/cases/case-seed/facts/{missing['id']}",
        json={"source_status": "documented"},
        headers=auth(EDITOR_ID),
    )
    assert blocked.status_code == 409


def test_timeline_unknown_date_is_allowed() -> None:
    response = client.post(
        "/v1/cases/case-seed/timeline",
        json={"title": "Ukjent hendelse", "date_status": "unknown"},
        headers=auth(EDITOR_ID),
    )
    assert response.status_code == 201
    assert response.json()["date_status"] == "unknown"


def test_draft_source_check_and_export_gate() -> None:
    draft = client.post(
        "/v1/cases/case-seed/drafts",
        json={"title": "Prosesskriv", "sections": [{"heading": "Faktum", "content": "Dette mangler kilde."}]},
        headers=auth(),
    ).json()
    check = client.post(f"/v1/cases/case-seed/drafts/{draft['id']}:check-sources", headers=auth()).json()
    assert check["status"] == "blocked"
    gate = client.post("/v1/cases/case-seed/exports:preview", json={"draft_id": draft["id"]}, headers=auth()).json()
    assert gate["status"] == "blocked"
    export = client.post(
        "/v1/cases/case-seed/exports",
        json={"draft_id": draft["id"], "gate_result_id": gate["id"]},
        headers=auth(),
    )
    assert export.status_code == 409


def test_export_after_gate_and_approval() -> None:
    doc = make_processed_document()
    source = client.post(
        "/v1/cases/case-seed/source-refs",
        json={"document_id": doc["id"], "page_id": doc["pages"][0]["id"], "quote": "Avtalen"},
        headers=auth(),
    ).json()
    draft = client.post(
        "/v1/cases/case-seed/drafts",
        json={"title": "Prosesskriv", "sections": [{"heading": "Faktum", "content": "Dokumentert.", "source_ref_ids": [source["id"]]}]},
        headers=auth(),
    ).json()
    gate = client.post("/v1/cases/case-seed/exports:preview", json={"draft_id": draft["id"]}, headers=auth()).json()
    assert gate["status"] == "needs_approval"
    approval = client.post(
        "/v1/cases/case-seed/approvals",
        json={"target_type": "export_gate", "target_id": gate["id"], "decision": "approved"},
        headers=auth(),
    ).json()
    export = client.post(
        "/v1/cases/case-seed/exports",
        json={"draft_id": draft["id"], "gate_result_id": gate["id"], "approval_id": approval["id"]},
        headers=auth(),
    )
    assert export.status_code == 201
    assert export.json()["manifest"]["source_appendix"] is True


def test_auditor_reads_audit_but_cannot_edit_case() -> None:
    client.get("/v1/cases/case-seed", headers=auth())
    audit = client.get("/v1/cases/case-seed/audit", headers=auth(AUDITOR_ID))
    assert audit.status_code == 200
    edit = client.patch("/v1/cases/case-seed", json={"title": "Nope"}, headers=auth(AUDITOR_ID))
    assert edit.status_code == 403
