from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from hashlib import sha256
from typing import Any
from uuid import uuid4


OWNER_ID = "00000000-0000-0000-0000-000000000001"
VIEWER_ID = "00000000-0000-0000-0000-000000000002"
EDITOR_ID = "00000000-0000-0000-0000-000000000003"
OTHER_TENANT_ID = "00000000-0000-0000-0000-000000000004"
AUDITOR_ID = "00000000-0000-0000-0000-000000000005"
EXTERNAL_ID = "00000000-0000-0000-0000-000000000006"


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def new_id() -> str:
    return str(uuid4())


ROLE_PERMISSIONS: dict[str, set[str]] = {
    "tenant_admin": {"case:create", "case:read", "case:update", "fact:create", "fact:update", "draft:write", "export:approve", "audit:read"},
    "case_owner": {"case:create", "case:read", "case:update", "document:write", "fact:create", "fact:update", "timeline:write", "risk:write", "draft:write", "export:preview", "export:approve", "export:create", "audit:read"},
    "legal_reviewer": {"case:read", "fact:create", "fact:update", "timeline:write", "risk:write", "draft:write", "export:preview", "export:approve", "audit:read"},
    "case_editor": {"case:create", "case:read", "document:write", "fact:create", "fact:update", "timeline:write", "risk:write", "draft:write", "export:preview"},
    "case_viewer": {"case:read"},
    "external_collaborator": {"case:read"},
    "auditor": {"case:read", "audit:read"},
}


USER_STATUS: dict[str, str] = {
    "uploaded": "Lastet opp",
    "validating": "Kontrollerer fil",
    "virus_scanning": "Kontrollerer sikkerhet",
    "validated": "Klar til lesing",
    "extracting_pages": "Deler opp dokumentet",
    "ocr_pending": "Venter pa tekstlesing",
    "ocr_running": "Leser dokument",
    "chunking": "Gjor teksten klar",
    "hashing": "Sikrer sporbarhet",
    "indexing": "Gjor dokumentet sokbart",
    "needs_review": "Ma ses over",
    "source_verified": "Klar som kilde",
    "validation_failed": "Kunne ikke behandles",
    "virus_blocked": "Stoppet av sikkerhetskontroll",
    "ocr_failed": "Kunne ikke lese teksten",
    "partial_ocr_failed": "Noen sider ma ses over",
    "corrupted": "Filen kan ikke leses",
    "quarantined": "Stoppet av sikkerhetskontroll",
    "processing_failed": "Kunne ikke behandles",
    "documented": "Dokumentert",
    "missing_source": "Mangler kilde",
    "disputed": "Omtvistet",
    "assumed": "Antatt",
    "needs_approval": "Krever godkjenning",
    "blocked": "Stoppet",
    "pass": "Klar",
    "draft": "Utkast",
    "source_checked": "Kilder sjekket",
    "approved": "Godkjent",
    "exported": "Eksportert",
}


@dataclass
class User:
    id: str
    tenant_id: str
    email: str
    display_name: str
    role: str


@dataclass
class Store:
    tenants: dict[str, dict[str, Any]] = field(default_factory=dict)
    users: dict[str, User] = field(default_factory=dict)
    case_members: dict[str, dict[str, str]] = field(default_factory=dict)
    cases: dict[str, dict[str, Any]] = field(default_factory=dict)
    documents: dict[str, dict[str, Any]] = field(default_factory=dict)
    pages: dict[str, dict[str, Any]] = field(default_factory=dict)
    chunks: dict[str, dict[str, Any]] = field(default_factory=dict)
    source_refs: dict[str, dict[str, Any]] = field(default_factory=dict)
    facts: dict[str, dict[str, Any]] = field(default_factory=dict)
    timeline: dict[str, dict[str, Any]] = field(default_factory=dict)
    evidence: dict[str, dict[str, Any]] = field(default_factory=dict)
    risks: dict[str, dict[str, Any]] = field(default_factory=dict)
    drafts: dict[str, dict[str, Any]] = field(default_factory=dict)
    gate_results: dict[str, dict[str, Any]] = field(default_factory=dict)
    approvals: dict[str, dict[str, Any]] = field(default_factory=dict)
    exports: dict[str, dict[str, Any]] = field(default_factory=dict)
    assistant_sessions: dict[str, dict[str, Any]] = field(default_factory=dict)
    assistant_messages: dict[str, dict[str, Any]] = field(default_factory=dict)
    audit_events: list[dict[str, Any]] = field(default_factory=list)
    upload_tokens: dict[str, dict[str, Any]] = field(default_factory=dict)

    def seed(self) -> None:
        self.__init__()
        tenant_a = "tenant-a"
        tenant_b = "tenant-b"
        self.tenants[tenant_a] = {"id": tenant_a, "name": "Advokat AI Pilot", "region": "NO"}
        self.tenants[tenant_b] = {"id": tenant_b, "name": "Annen tenant", "region": "EU"}
        for user in [
            User(OWNER_ID, tenant_a, "owner@example.test", "Sakseier", "case_owner"),
            User(VIEWER_ID, tenant_a, "viewer@example.test", "Leser", "case_viewer"),
            User(EDITOR_ID, tenant_a, "editor@example.test", "Redaktor", "case_editor"),
            User(AUDITOR_ID, tenant_a, "audit@example.test", "Revisor", "auditor"),
            User(EXTERNAL_ID, tenant_a, "external@example.test", "Ekstern", "external_collaborator"),
            User(OTHER_TENANT_ID, tenant_b, "other@example.test", "Annen bruker", "case_owner"),
        ]:
            self.users[user.id] = user
        case_id = "case-seed"
        self.cases[case_id] = {
            "id": case_id,
            "tenant_id": tenant_a,
            "title": "Pilot sak",
            "case_type": "civil",
            "jurisdiction": "NO",
            "description": "Seedet pilotsak",
            "sensitivity_level": "standard",
            "status": "active",
            "created_by": OWNER_ID,
            "created_at": now_iso(),
            "updated_at": now_iso(),
        }
        self.case_members[case_id] = {
            OWNER_ID: "case_owner",
            EDITOR_ID: "case_editor",
            VIEWER_ID: "case_viewer",
            AUDITOR_ID: "auditor",
            EXTERNAL_ID: "external_collaborator",
        }
        other_case = "case-other-tenant"
        self.cases[other_case] = {
            "id": other_case,
            "tenant_id": tenant_b,
            "title": "Skjult sak",
            "case_type": "civil",
            "jurisdiction": "NO",
            "description": "",
            "sensitivity_level": "standard",
            "status": "active",
            "created_by": OTHER_TENANT_ID,
            "created_at": now_iso(),
            "updated_at": now_iso(),
        }
        self.case_members[other_case] = {OTHER_TENANT_ID: "case_owner"}

    def audit(self, user: User | None, action: str, summary: str, case_id: str | None = None, object_type: str | None = None, object_id: str | None = None, metadata: dict[str, Any] | None = None) -> dict[str, Any]:
        event = {
            "id": new_id(),
            "tenant_id": user.tenant_id if user else None,
            "case_id": case_id,
            "actor_user_id": user.id if user else None,
            "action": action,
            "object_type": object_type,
            "object_id": object_id,
            "summary": summary,
            "metadata": metadata or {},
            "created_at": now_iso(),
        }
        self.audit_events.append(event)
        return event

    def user_role_for_case(self, user: User, case_id: str) -> str | None:
        if case_id not in self.cases:
            return None
        case = self.cases[case_id]
        if case["tenant_id"] != user.tenant_id:
            return None
        return self.case_members.get(case_id, {}).get(user.id)

    def can(self, user: User, permission: str, case_id: str | None = None) -> bool:
        role = self.user_role_for_case(user, case_id) if case_id else user.role
        if not role:
            return False
        return permission in ROLE_PERMISSIONS.get(role, set())

    def case_overview(self, case_id: str) -> dict[str, Any]:
        docs = [d for d in self.documents.values() if d["case_id"] == case_id]
        facts = [f for f in self.facts.values() if f["case_id"] == case_id]
        drafts = [d for d in self.drafts.values() if d["case_id"] == case_id]
        risks = [r for r in self.risks.values() if r["case_id"] == case_id and r["status"] == "open"]
        missing_sources = len([f for f in facts if f["source_status"] == "missing_source"])
        unresolved_risks = len([r for r in risks if r["severity"] in {"high", "critical"}])
        if not docs:
            next_action = "Last opp dokumenter"
        elif any(d["status"] != "source_verified" for d in docs):
            next_action = "Se dokumentstatus"
        elif missing_sources:
            next_action = "Fiks manglende kilder"
        elif not drafts:
            next_action = "Fortsett pa utkast"
        elif unresolved_risks:
            next_action = "Se hva som stopper eksport"
        else:
            next_action = "Forhandsvis eksport"
        return {
            "document_count": len(docs),
            "missing_source_count": missing_sources,
            "unresolved_risk_count": unresolved_risks,
            "draft_count": len(drafts),
            "next_action": next_action,
        }


store = Store()
store.seed()


def digest_text(value: str) -> str:
    return sha256(value.encode("utf-8")).hexdigest()
