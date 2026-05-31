from __future__ import annotations

from hashlib import sha256
from typing import Any

from fastapi import Depends, FastAPI, Header, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse
from pydantic import BaseModel, Field

from .domain import USER_STATUS, User, digest_text, new_id, now_iso, store
from .local_ui import render_local_ui

app = FastAPI(title="Advokat AI Pilot Candidate API", version="0.4.0")


def current_user(x_user_id: str | None = Header(default=None)) -> User:
    if not x_user_id:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Innlogging kreves")
    user = store.users.get(x_user_id)
    if not user:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Ukjent bruker")
    return user


def require_case(user: User, case_id: str, permission: str = "case:read") -> dict[str, Any]:
    case = store.cases.get(case_id)
    if not case or case["tenant_id"] != user.tenant_id or not store.user_role_for_case(user, case_id):
        store.audit(user, "access_denied", "Tilgang ble stoppet", case_id=case_id, object_type="Case", object_id=case_id)
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Saken finnes ikke eller du mangler tilgang")
    if not store.can(user, permission, case_id):
        store.audit(user, "access_denied", "Handlingen er ikke tillatt", case_id=case_id, object_type="Case", object_id=case_id)
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Du har ikke tilgang til denne handlingen")
    return case


def ensure_permission(user: User, permission: str, case_id: str) -> None:
    require_case(user, case_id, "case:read")
    if not store.can(user, permission, case_id):
        store.audit(user, "access_denied", "Handlingen er ikke tillatt", case_id=case_id)
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Du har ikke tilgang til denne handlingen")


class CaseCreate(BaseModel):
    title: str = Field(min_length=1)
    case_type: str = "civil"
    jurisdiction: str = "NO"
    description: str = ""
    sensitivity_level: str = "standard"


class DocumentUploadInit(BaseModel):
    filename: str
    mime_type: str = "application/pdf"
    size_bytes: int = 0


class DocumentUploadComplete(BaseModel):
    upload_token: str
    sha256: str | None = None
    text: str = "Dette er et juridisk dokument med faktum og dato 2026-05-27."


class SourceRefCreate(BaseModel):
    document_id: str
    page_id: str | None = None
    chunk_id: str | None = None
    quote: str | None = None
    bates_label: str | None = None
    confidence: float = 0.98


class FactCreate(BaseModel):
    text: str
    source_ref_ids: list[str] = []


class TimelineCreate(BaseModel):
    title: str
    description: str = ""
    event_date: str | None = None
    date_status: str = "unknown"
    source_ref_ids: list[str] = []


class RiskCreate(BaseModel):
    title: str
    description: str = ""
    severity: str = "medium"
    status: str = "open"


class DraftCreate(BaseModel):
    title: str
    draft_type: str = "notat"
    sections: list[dict[str, Any]] = []


class DraftPatch(BaseModel):
    title: str | None = None
    sections: list[dict[str, Any]] | None = None


class ApprovalCreate(BaseModel):
    target_type: str
    target_id: str
    decision: str = "approved"
    comment: str = ""


class AssistantRequest(BaseModel):
    message: str
    case_id: str | None = None
    session_id: str | None = None
    context: dict[str, Any] = {}
    preferred_answer_level: str = "simple"


@app.get("/health")
@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/api/dev/reset")
def reset() -> dict[str, str]:
    store.seed()
    return {"status": "reset"}


@app.get("/", include_in_schema=False)
def root() -> RedirectResponse:
    return RedirectResponse(url="/ui")


@app.get("/ui", response_class=HTMLResponse, include_in_schema=False)
def local_ui() -> str:
    return render_local_ui()


@app.get("/v1/me")
def me(user: User = Depends(current_user)) -> dict[str, Any]:
    return user.__dict__


@app.get("/v1/cases")
def list_cases(user: User = Depends(current_user)) -> list[dict[str, Any]]:
    return [
        {**case, "overview": store.case_overview(case["id"])}
        for case in store.cases.values()
        if case["tenant_id"] == user.tenant_id and store.user_role_for_case(user, case["id"])
    ]


@app.post("/v1/cases", status_code=201)
def create_case(payload: CaseCreate, user: User = Depends(current_user)) -> dict[str, Any]:
    if not store.can(user, "case:create"):
        store.audit(user, "access_denied", "Opprettelse av sak ble stoppet")
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Du kan ikke opprette sak")
    case_id = new_id()
    case = {
        "id": case_id,
        "tenant_id": user.tenant_id,
        "title": payload.title,
        "case_type": payload.case_type,
        "jurisdiction": payload.jurisdiction or "NO",
        "description": payload.description,
        "sensitivity_level": payload.sensitivity_level,
        "status": "active",
        "created_by": user.id,
        "created_at": now_iso(),
        "updated_at": now_iso(),
    }
    store.cases[case_id] = case
    store.case_members[case_id] = {user.id: "case_owner"}
    store.audit(user, "case_created", "Sak opprettet", case_id=case_id, object_type="Case", object_id=case_id)
    return {**case, "overview": store.case_overview(case_id)}


@app.get("/v1/cases/{case_id}")
def get_case(case_id: str, user: User = Depends(current_user)) -> dict[str, Any]:
    case = require_case(user, case_id)
    store.audit(user, "case_opened", "Sak apnet", case_id=case_id, object_type="Case", object_id=case_id)
    return {**case, "overview": store.case_overview(case_id)}


@app.patch("/v1/cases/{case_id}")
def update_case(case_id: str, payload: dict[str, Any], user: User = Depends(current_user)) -> dict[str, Any]:
    case = require_case(user, case_id, "case:update")
    for key in ["title", "case_type", "jurisdiction", "description", "sensitivity_level", "status"]:
        if key in payload:
            case[key] = payload[key]
    case["updated_at"] = now_iso()
    store.audit(user, "case_updated", "Sak oppdatert", case_id=case_id, object_type="Case", object_id=case_id)
    return {**case, "overview": store.case_overview(case_id)}


@app.post("/v1/cases/{case_id}/documents:init-upload")
def init_upload(case_id: str, payload: DocumentUploadInit, user: User = Depends(current_user)) -> dict[str, Any]:
    ensure_permission(user, "document:write", case_id)
    token = new_id()
    store.upload_tokens[token] = {**payload.model_dump(), "case_id": case_id, "created_by": user.id}
    return {"upload_token": token, "upload_url": f"memory://uploads/{token}", "expires_in_seconds": 900}


@app.post("/v1/cases/{case_id}/documents:complete-upload", status_code=201)
def complete_upload(case_id: str, payload: DocumentUploadComplete, user: User = Depends(current_user)) -> dict[str, Any]:
    ensure_permission(user, "document:write", case_id)
    token = store.upload_tokens.get(payload.upload_token)
    if not token or token["case_id"] != case_id:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Opplastingen er ikke gyldig")
    doc_hash = payload.sha256 or sha256(payload.text.encode("utf-8")).hexdigest()
    for existing in store.documents.values():
        if existing["case_id"] == case_id and existing["sha256"] == doc_hash:
            return existing
    doc_id = new_id()
    document = {
        "id": doc_id,
        "tenant_id": user.tenant_id,
        "case_id": case_id,
        "filename": token["filename"],
        "mime_type": token["mime_type"],
        "size_bytes": token["size_bytes"],
        "storage_uri": f"memory://documents/{doc_id}",
        "sha256": doc_hash,
        "page_count": 0,
        "status": "uploaded",
        "user_status": USER_STATUS["uploaded"],
        "uploaded_by": user.id,
        "text": payload.text,
        "created_at": now_iso(),
        "updated_at": now_iso(),
    }
    store.documents[doc_id] = document
    store.audit(user, "document_uploaded", "Dokument lastet opp", case_id=case_id, object_type="Document", object_id=doc_id)
    return document


@app.get("/v1/cases/{case_id}/documents")
def list_documents(case_id: str, user: User = Depends(current_user)) -> list[dict[str, Any]]:
    require_case(user, case_id)
    return [d for d in store.documents.values() if d["case_id"] == case_id]


@app.get("/v1/cases/{case_id}/documents/{document_id}")
def get_document(case_id: str, document_id: str, user: User = Depends(current_user)) -> dict[str, Any]:
    require_case(user, case_id)
    doc = store.documents.get(document_id)
    if not doc or doc["case_id"] != case_id:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Dokumentet finnes ikke")
    pages = [p for p in store.pages.values() if p["document_id"] == document_id]
    chunks = [c for c in store.chunks.values() if c["document_id"] == document_id]
    store.audit(user, "document_opened", "Dokument apnet", case_id=case_id, object_type="Document", object_id=document_id)
    return {**doc, "pages": pages, "chunks": chunks}


@app.post("/v1/cases/{case_id}/documents/{document_id}:process")
def process_document(case_id: str, document_id: str, user: User = Depends(current_user)) -> dict[str, Any]:
    ensure_permission(user, "document:write", case_id)
    doc = store.documents.get(document_id)
    if not doc or doc["case_id"] != case_id:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Dokumentet finnes ikke")
    if doc["mime_type"] != "application/pdf":
        doc["status"] = "validation_failed"
        doc["user_status"] = USER_STATUS["validation_failed"]
        return doc
    text = doc.get("text", "")
    page_id = new_id()
    low_confidence = "LOW_CONFIDENCE" in text
    page = {
        "id": page_id,
        "tenant_id": user.tenant_id,
        "case_id": case_id,
        "document_id": document_id,
        "page_number": 1,
        "ocr_status": "low_confidence" if low_confidence else "complete",
        "user_status": "Ma ses over" if low_confidence else "Tekst lest",
        "ocr_text": text,
        "ocr_confidence": 0.41 if low_confidence else 0.98,
        "text_hash": digest_text(text),
        "bates_label": "A-0001",
        "warnings": ["Denne siden er usikkert lest. Se over teksten for du bruker den som kilde."] if low_confidence else [],
    }
    chunk_id = new_id()
    chunk = {
        "id": chunk_id,
        "tenant_id": user.tenant_id,
        "case_id": case_id,
        "document_id": document_id,
        "page_id": page_id,
        "chunk_index": 0,
        "text": text,
        "text_hash": digest_text(text),
        "source_span": {"page": 1},
    }
    store.pages[page_id] = page
    store.chunks[chunk_id] = chunk
    doc["page_count"] = 1
    doc["status"] = "needs_review" if low_confidence else "source_verified"
    doc["user_status"] = USER_STATUS[doc["status"]]
    doc["updated_at"] = now_iso()
    store.audit(user, "document_processed", "Dokument behandlet", case_id=case_id, object_type="Document", object_id=document_id)
    return {**doc, "pages": [page], "chunks": [chunk]}


@app.post("/v1/cases/{case_id}/source-refs", status_code=201)
def create_source_ref(case_id: str, payload: SourceRefCreate, user: User = Depends(current_user)) -> dict[str, Any]:
    ensure_permission(user, "fact:create", case_id)
    if not (payload.page_id or payload.chunk_id or payload.bates_label):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Kilden ma vise til side, tekstutdrag eller Bates-merke")
    if payload.document_id not in store.documents or store.documents[payload.document_id]["case_id"] != case_id:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Dokumentet finnes ikke")
    source_id = new_id()
    source = {
        "id": source_id,
        "tenant_id": user.tenant_id,
        "case_id": case_id,
        "document_id": payload.document_id,
        "page_id": payload.page_id,
        "chunk_id": payload.chunk_id,
        "quote": payload.quote,
        "bates_label": payload.bates_label,
        "confidence": payload.confidence,
        "status": "valid" if payload.confidence >= 0.8 else "needs_review",
        "user_status": "Gyldig kilde" if payload.confidence >= 0.8 else "Ma ses over",
        "created_by": user.id,
        "created_at": now_iso(),
    }
    store.source_refs[source_id] = source
    store.audit(user, "source_ref_created", "Kilde markert", case_id=case_id, object_type="SourceRef", object_id=source_id)
    return source


@app.get("/v1/cases/{case_id}/facts")
def list_facts(case_id: str, user: User = Depends(current_user)) -> list[dict[str, Any]]:
    require_case(user, case_id)
    return [f for f in store.facts.values() if f["case_id"] == case_id]


@app.post("/v1/cases/{case_id}/facts", status_code=201)
def create_fact(case_id: str, payload: FactCreate, user: User = Depends(current_user)) -> dict[str, Any]:
    ensure_permission(user, "fact:create", case_id)
    valid_sources = [sid for sid in payload.source_ref_ids if sid in store.source_refs and store.source_refs[sid]["case_id"] == case_id]
    fact_id = new_id()
    fact = {
        "id": fact_id,
        "tenant_id": user.tenant_id,
        "case_id": case_id,
        "text": payload.text,
        "source_ref_ids": valid_sources,
        "source_status": "documented" if valid_sources else "missing_source",
        "user_status": USER_STATUS["documented"] if valid_sources else USER_STATUS["missing_source"],
        "confidence_label": "documented" if valid_sources else "undocumented",
        "created_by": user.id,
        "created_at": now_iso(),
        "updated_at": now_iso(),
    }
    store.facts[fact_id] = fact
    store.audit(user, "fact_claim_created", "Faktapastand opprettet", case_id=case_id, object_type="FactClaim", object_id=fact_id)
    return fact


@app.patch("/v1/cases/{case_id}/facts/{fact_id}")
def update_fact(case_id: str, fact_id: str, payload: dict[str, Any], user: User = Depends(current_user)) -> dict[str, Any]:
    ensure_permission(user, "fact:update", case_id)
    fact = store.facts.get(fact_id)
    if not fact or fact["case_id"] != case_id:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Faktapastanden finnes ikke")
    source_ref_ids = payload.get("source_ref_ids", fact.get("source_ref_ids", []))
    if payload.get("source_status") == "documented" and not source_ref_ids:
        raise HTTPException(status.HTTP_409_CONFLICT, "Faktapastanden kan ikke markeres som dokumentert uten kilde")
    fact.update({k: v for k, v in payload.items() if k in {"text", "source_ref_ids", "source_status"}})
    fact["user_status"] = USER_STATUS.get(fact["source_status"], fact["source_status"])
    fact["updated_at"] = now_iso()
    store.audit(user, "fact_claim_updated", "Faktapastand oppdatert", case_id=case_id, object_type="FactClaim", object_id=fact_id)
    return fact


@app.get("/v1/cases/{case_id}/timeline")
def list_timeline(case_id: str, user: User = Depends(current_user)) -> list[dict[str, Any]]:
    require_case(user, case_id)
    return [e for e in store.timeline.values() if e["case_id"] == case_id]


@app.post("/v1/cases/{case_id}/timeline", status_code=201)
def create_timeline(case_id: str, payload: TimelineCreate, user: User = Depends(current_user)) -> dict[str, Any]:
    ensure_permission(user, "timeline:write", case_id)
    event_id = new_id()
    event = {"id": event_id, "tenant_id": user.tenant_id, "case_id": case_id, **payload.model_dump(), "created_by": user.id, "created_at": now_iso()}
    store.timeline[event_id] = event
    store.audit(user, "timeline_event_created", "Hendelse opprettet", case_id=case_id, object_type="TimelineEvent", object_id=event_id)
    return event


@app.post("/v1/cases/{case_id}/risks", status_code=201)
def create_risk(case_id: str, payload: RiskCreate, user: User = Depends(current_user)) -> dict[str, Any]:
    ensure_permission(user, "risk:write", case_id)
    risk_id = new_id()
    risk = {"id": risk_id, "tenant_id": user.tenant_id, "case_id": case_id, **payload.model_dump(), "created_by": user.id, "created_at": now_iso()}
    store.risks[risk_id] = risk
    store.audit(user, "risk_item_created", "Risiko registrert", case_id=case_id, object_type="RiskItem", object_id=risk_id)
    return risk


@app.get("/v1/cases/{case_id}/drafts")
def list_drafts(case_id: str, user: User = Depends(current_user)) -> list[dict[str, Any]]:
    require_case(user, case_id)
    return [d for d in store.drafts.values() if d["case_id"] == case_id]


@app.post("/v1/cases/{case_id}/drafts", status_code=201)
def create_draft(case_id: str, payload: DraftCreate, user: User = Depends(current_user)) -> dict[str, Any]:
    ensure_permission(user, "draft:write", case_id)
    draft_id = new_id()
    sections = payload.sections or [{"heading": "Faktum", "content": "", "source_ref_ids": []}]
    for idx, section in enumerate(sections):
        section.setdefault("id", new_id())
        section.setdefault("section_index", idx)
        section.setdefault("source_ref_ids", [])
        section["source_status"] = "documented" if section["source_ref_ids"] else "missing_source"
        section["user_status"] = USER_STATUS[section["source_status"]]
    draft = {
        "id": draft_id,
        "tenant_id": user.tenant_id,
        "case_id": case_id,
        "title": payload.title,
        "draft_type": payload.draft_type,
        "sections": sections,
        "status": "draft",
        "user_status": USER_STATUS["draft"],
        "created_by": user.id,
        "created_at": now_iso(),
        "updated_at": now_iso(),
    }
    store.drafts[draft_id] = draft
    store.audit(user, "draft_created", "Utkast opprettet", case_id=case_id, object_type="DraftDocument", object_id=draft_id)
    return draft


@app.patch("/v1/cases/{case_id}/drafts/{draft_id}")
def update_draft(case_id: str, draft_id: str, payload: DraftPatch, user: User = Depends(current_user)) -> dict[str, Any]:
    ensure_permission(user, "draft:write", case_id)
    draft = store.drafts.get(draft_id)
    if not draft or draft["case_id"] != case_id:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Utkastet finnes ikke")
    if payload.title is not None:
        draft["title"] = payload.title
    if payload.sections is not None:
        draft["sections"] = payload.sections
    for idx, section in enumerate(draft["sections"]):
        section.setdefault("id", new_id())
        section.setdefault("section_index", idx)
        section.setdefault("source_ref_ids", [])
        section["source_status"] = "documented" if section["source_ref_ids"] else "missing_source"
        section["user_status"] = USER_STATUS[section["source_status"]]
    draft["updated_at"] = now_iso()
    store.audit(user, "draft_updated", "Utkast oppdatert", case_id=case_id, object_type="DraftDocument", object_id=draft_id)
    return draft


@app.post("/v1/cases/{case_id}/drafts/{draft_id}:check-sources")
def check_sources(case_id: str, draft_id: str, user: User = Depends(current_user)) -> dict[str, Any]:
    require_case(user, case_id)
    draft = store.drafts.get(draft_id)
    if not draft or draft["case_id"] != case_id:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Utkastet finnes ikke")
    missing = [s for s in draft["sections"] if not s.get("source_ref_ids")]
    status_value = "blocked" if missing else "pass"
    result = {
        "status": status_value,
        "user_status": USER_STATUS[status_value],
        "missing_source_count": len(missing),
        "blockers": [{"message": "Dette avsnittet mangler kilde.", "section_id": s["id"]} for s in missing],
    }
    store.audit(user, "draft_source_checked", "Kilder i utkast sjekket", case_id=case_id, object_type="DraftDocument", object_id=draft_id)
    return result


@app.post("/v1/cases/{case_id}/exports:preview")
@app.post("/v1/cases/{case_id}/control-gates/export:preview")
def export_preview(case_id: str, payload: dict[str, Any], user: User = Depends(current_user)) -> dict[str, Any]:
    ensure_permission(user, "export:preview", case_id)
    draft_id = payload.get("draft_id")
    draft = store.drafts.get(draft_id)
    if not draft or draft["case_id"] != case_id:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Utkastet finnes ikke")
    blockers = []
    for section in draft["sections"]:
        if not section.get("source_ref_ids"):
            blockers.append({"type": "missing_source", "message": "Et avsnitt mangler kilde.", "object_id": section["id"]})
    for risk in store.risks.values():
        if risk["case_id"] == case_id and risk["status"] == "open" and risk["severity"] == "critical":
            blockers.append({"type": "critical_risk", "message": "En kritisk risiko ma avklares.", "object_id": risk["id"]})
    gate_id = new_id()
    status_value = "blocked" if blockers else "needs_approval"
    gate = {
        "id": gate_id,
        "tenant_id": user.tenant_id,
        "case_id": case_id,
        "gate_type": "export",
        "target_type": "DraftDocument",
        "target_id": draft_id,
        "status": status_value,
        "user_status": USER_STATUS[status_value],
        "blockers": blockers,
        "warnings": [],
        "user_summary": "Eksport er stoppet." if blockers else "Utkastet er klart for godkjenning.",
        "created_by": user.id,
        "created_at": now_iso(),
    }
    store.gate_results[gate_id] = gate
    store.audit(user, "export_preview_created", "Eksport kontrollert", case_id=case_id, object_type="ControlGate", object_id=gate_id)
    return gate


@app.post("/v1/cases/{case_id}/approvals", status_code=201)
@app.post("/v1/cases/{case_id}/control-gates/approvals", status_code=201)
def approve(case_id: str, payload: ApprovalCreate, user: User = Depends(current_user)) -> dict[str, Any]:
    ensure_permission(user, "export:approve", case_id)
    approval_id = new_id()
    approval = {"id": approval_id, "tenant_id": user.tenant_id, "case_id": case_id, **payload.model_dump(), "decided_by": user.id, "created_at": now_iso()}
    store.approvals[approval_id] = approval
    store.audit(user, "approval_decision_created", "Godkjenning registrert", case_id=case_id, object_type="ApprovalDecision", object_id=approval_id)
    return approval


@app.post("/v1/cases/{case_id}/exports", status_code=201)
def create_export(case_id: str, payload: dict[str, Any], user: User = Depends(current_user)) -> dict[str, Any]:
    ensure_permission(user, "export:create", case_id)
    gate = store.gate_results.get(payload.get("gate_result_id"))
    approval = store.approvals.get(payload.get("approval_id"))
    draft_id = payload.get("draft_id")
    if not gate or gate["case_id"] != case_id or gate["target_id"] != draft_id:
        raise HTTPException(status.HTTP_409_CONFLICT, "Eksport krever gyldig kontroll")
    if gate["status"] == "blocked":
        raise HTTPException(status.HTTP_409_CONFLICT, "Eksport er blokkert")
    if not approval or approval["case_id"] != case_id or approval["target_id"] != gate["id"] or approval["decision"] != "approved":
        raise HTTPException(status.HTTP_409_CONFLICT, "Eksport krever godkjenning")
    export_id = new_id()
    export = {
        "id": export_id,
        "tenant_id": user.tenant_id,
        "case_id": case_id,
        "draft_id": draft_id,
        "export_type": payload.get("export_type", "bundle"),
        "status": "ready",
        "storage_uri": f"memory://exports/{export_id}",
        "manifest": {"gate_result_id": gate["id"], "approval_id": approval["id"], "source_appendix": True},
        "export_gate_result_id": gate["id"],
        "approval_id": approval["id"],
        "created_by": user.id,
        "created_at": now_iso(),
    }
    store.exports[export_id] = export
    store.audit(user, "export_package_created", "Eksportpakke opprettet", case_id=case_id, object_type="ExportPackage", object_id=export_id)
    return export


@app.get("/v1/cases/{case_id}/audit")
def audit(case_id: str, user: User = Depends(current_user)) -> list[dict[str, Any]]:
    ensure_permission(user, "audit:read", case_id)
    return [e for e in store.audit_events if e["case_id"] == case_id]


@app.get("/v1/cases/{case_id}/drafts/{draft_id}/source-coverage")
def source_coverage(case_id: str, draft_id: str, user: User = Depends(current_user)) -> dict[str, Any]:
    return check_sources(case_id, draft_id, user)


@app.post("/v1/assistant/chat", status_code=201)
@app.post("/v1/cases/{case_id}/assistant/chat", status_code=201)
def assistant_chat(payload: AssistantRequest, case_id: str | None = None, user: User = Depends(current_user)) -> dict[str, Any]:
    if case_id and not payload.case_id:
        payload.case_id = case_id
    if payload.case_id:
        require_case(user, payload.case_id)
    session_id = payload.session_id or new_id()
    store.assistant_sessions.setdefault(session_id, {"id": session_id, "tenant_id": user.tenant_id, "case_id": payload.case_id, "user_id": user.id, "created_at": now_iso()})
    message = payload.message.lower()
    context = payload.context
    gate = None
    if payload.case_id and ("eksport" in message or context.get("visible_state", {}).get("export_status") == "blocked"):
        gates = [g for g in store.gate_results.values() if g["case_id"] == payload.case_id]
        gate = gates[-1] if gates else None
    intent = "what_next"
    answer = "Neste trygge steg er a laste opp dokumentene saken bygger pa."
    guided_label = "Vis meg hvordan"
    if "mangler kilde" in message or "kilde" in message:
        intent = "source_help"
        answer = "Mangler kilde betyr at en pastand ikke kan spores til dokument, side eller tekstutdrag enna. Neste steg er a markere riktig del av dokumentet som kilde."
        guided_label = "Finn kilde sammen med meg"
    if "eksport" in message:
        intent = "why_blocked"
        if gate and gate["blockers"]:
            first = gate["blockers"][0]["message"]
            answer = f"Eksport er stoppet fordi {len(gate['blockers'])} punkt ma ryddes. Forst: {first}"
        elif gate:
            answer = "Eksporten er klar for menneskelig godkjenning for pakken kan opprettes."
        else:
            answer = "Jeg ma se eksportkontrollen for a forklare blokkeringen presist. Kjor forhandsvisning av eksport forst."
        guided_label = "Ga gjennom blokkeringene"
    if "avgjor" in message or "vinne" in message or "juridisk konklusjon" in message:
        intent = "legal_judgment_boundary"
        answer = "Jeg kan hjelpe deg a strukturere fakta, kilder og risiko, men endelig juridisk vurdering ma tas av ansvarlig jurist."
        guided_label = "Sjekk grunnlaget"
    if "hva gjor jeg" in message or "hva gjør jeg" in message:
        overview = store.case_overview(payload.case_id) if payload.case_id else {}
        answer = f"Neste steg er: {overview.get('next_action', 'opprett en sak')}. Jeg kan ga gjennom det med deg."
    previous = [m for m in store.assistant_messages.values() if m["session_id"] == session_id and m["topic_fingerprint"] == intent]
    if previous:
        answer = "Sagt litt enklere: " + answer
    quality_gate = {"passed": True, "checks": {"context_specific": True, "not_repetitive": not previous, "no_technical_jargon": True, "has_next_step": True}}
    msg_id = new_id()
    response = {
        "message_id": msg_id,
        "session_id": session_id,
        "answer": answer,
        "mode": intent,
        "answer_level": payload.preferred_answer_level,
        "detected_intent": intent,
        "topic_fingerprint": intent,
        "is_semantic_repeat": bool(previous),
        "repeat_strategy": "change_explanation_mode" if previous else "full_contextual_answer",
        "referenced_objects": [],
        "next_best_action": {"label": guided_label, "action_type": "do_it_with_me"},
        "guided_actions": [{"action_type": "do_it_with_me", "label": guided_label, "requires_approval": False, "may_change_data": False, "steps": []}],
        "safety_flags": ["not_legal_advice", "requires_human_review_before_export"],
        "quality_gate": quality_gate,
    }
    store.assistant_messages[msg_id] = {"id": msg_id, "session_id": session_id, "tenant_id": user.tenant_id, "case_id": payload.case_id, "user_id": user.id, "role": "assistant", "content_redacted": answer, "intent": intent, "topic_fingerprint": intent, "answer_fingerprint": digest_text(answer), "created_at": now_iso()}
    store.audit(user, "assistant_message_created", "Assistent svarte", case_id=payload.case_id, object_type="AssistantMessage", object_id=msg_id)
    return response


@app.post("/v1/assistant/guided-mode", status_code=201)
def guided_mode(payload: dict[str, Any], user: User = Depends(current_user)) -> dict[str, Any]:
    case_id = payload.get("case_id")
    if case_id:
        require_case(user, case_id)
    action = {"id": new_id(), "case_id": case_id, "action_type": payload.get("action_type", "do_it_with_me"), "status": "started", "steps": payload.get("steps", [])}
    store.audit(user, "assistant_guided_action_created", "Veiledning startet", case_id=case_id, object_type="AssistantGuidedAction", object_id=action["id"])
    return action
