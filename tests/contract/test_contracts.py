from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def test_openapi_pilot_candidate_file_contains_core_paths() -> None:
    text = (ROOT / "docs" / "openapi.yaml").read_text(encoding="utf-8")
    for path in [
        "/v1/cases",
        "/v1/cases/{case_id}/documents:init-upload",
        "/v1/cases/{case_id}/drafts/{draft_id}/source-coverage",
        "/v1/cases/{case_id}/control-gates/export:preview",
        "/v1/cases/{case_id}/assistant/chat",
    ]:
        assert path in text


def test_sql_schema_contains_release_critical_tables() -> None:
    text = (ROOT / "infra" / "migrations" / "001_init.sql").read_text(encoding="utf-8").lower()
    for table in [
        "create table cases",
        "create table documents",
        "create table source_refs",
        "create table fact_claims",
        "create table draft_documents",
        "create table control_gate_results",
        "create table audit_events",
    ]:
        assert table in text


def test_root_scripts_expose_release_gate_commands() -> None:
    text = (ROOT / "package.json").read_text(encoding="utf-8")
    for command in ["verify", "test:contracts", "assistant:golden", "lint"]:
        assert command in text
