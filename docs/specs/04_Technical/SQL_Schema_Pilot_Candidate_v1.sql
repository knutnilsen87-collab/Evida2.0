-- Advokat AI Pilot Candidate SQL Schema v1
-- PostgreSQL 15+
-- This schema is designed for Codex implementation.
-- It enforces tenant/case isolation patterns, auditability, source integrity
-- and release-critical legal workflow state.

CREATE EXTENSION IF NOT EXISTS "pgcrypto";
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Optional when vector search is enabled:
-- CREATE EXTENSION IF NOT EXISTS vector;

-- ---------------------------------------------------------------------------
-- Utility
-- ---------------------------------------------------------------------------

CREATE OR REPLACE FUNCTION set_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = now();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- ---------------------------------------------------------------------------
-- Tenancy, users, roles
-- ---------------------------------------------------------------------------

CREATE TABLE tenants (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name TEXT NOT NULL,
  region TEXT NOT NULL DEFAULT 'EU' CHECK (region IN ('EU','EEA','NO')),
  data_training_allowed BOOLEAN NOT NULL DEFAULT FALSE,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TRIGGER trg_tenants_updated_at
BEFORE UPDATE ON tenants
FOR EACH ROW EXECUTE FUNCTION set_updated_at();

CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id UUID NOT NULL REFERENCES tenants(id),
  email TEXT NOT NULL,
  display_name TEXT,
  role TEXT NOT NULL CHECK (role IN (
    'tenant_admin',
    'case_owner',
    'legal_reviewer',
    'case_editor',
    'case_viewer',
    'external_collaborator',
    'auditor'
  )),
  status TEXT NOT NULL DEFAULT 'active' CHECK (status IN ('active','disabled','invited')),
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  UNIQUE (tenant_id, email)
);

CREATE INDEX idx_users_tenant ON users(tenant_id);
CREATE TRIGGER trg_users_updated_at
BEFORE UPDATE ON users
FOR EACH ROW EXECUTE FUNCTION set_updated_at();

-- ---------------------------------------------------------------------------
-- Cases
-- ---------------------------------------------------------------------------

CREATE TABLE cases (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id UUID NOT NULL REFERENCES tenants(id),
  title TEXT NOT NULL,
  case_type TEXT NOT NULL,
  jurisdiction TEXT NOT NULL DEFAULT 'NO',
  description TEXT,
  sensitivity_level TEXT NOT NULL DEFAULT 'standard'
    CHECK (sensitivity_level IN ('standard','sensitive','highly_sensitive')),
  status TEXT NOT NULL DEFAULT 'active'
    CHECK (status IN ('active','archived','locked','deleted_pending')),
  created_by UUID NOT NULL REFERENCES users(id),
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  UNIQUE (tenant_id, id)
);

CREATE INDEX idx_cases_tenant ON cases(tenant_id);
CREATE INDEX idx_cases_tenant_status ON cases(tenant_id, status);
CREATE TRIGGER trg_cases_updated_at
BEFORE UPDATE ON cases
FOR EACH ROW EXECUTE FUNCTION set_updated_at();

CREATE TABLE case_members (
  tenant_id UUID NOT NULL REFERENCES tenants(id),
  case_id UUID NOT NULL REFERENCES cases(id) ON DELETE CASCADE,
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  role TEXT NOT NULL CHECK (role IN (
    'case_owner',
    'legal_reviewer',
    'case_editor',
    'case_viewer',
    'external_collaborator',
    'auditor'
  )),
  permissions JSONB NOT NULL DEFAULT '{}',
  added_by UUID REFERENCES users(id),
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  PRIMARY KEY (case_id, user_id),
  CONSTRAINT case_members_tenant_case_fk
    FOREIGN KEY (tenant_id, case_id) REFERENCES cases(tenant_id, id) DEFERRABLE INITIALLY DEFERRED
);


CREATE INDEX idx_case_members_tenant_case ON case_members(tenant_id, case_id);
CREATE INDEX idx_case_members_user ON case_members(user_id);

-- ---------------------------------------------------------------------------
-- Documents and processing
-- ---------------------------------------------------------------------------

CREATE TABLE documents (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id UUID NOT NULL REFERENCES tenants(id),
  case_id UUID NOT NULL REFERENCES cases(id) ON DELETE CASCADE,
  filename TEXT NOT NULL,
  mime_type TEXT NOT NULL,
  size_bytes BIGINT,
  storage_uri TEXT NOT NULL,
  sha256 TEXT NOT NULL CHECK (length(sha256) = 64),
  page_count INT,
  status TEXT NOT NULL DEFAULT 'uploaded' CHECK (status IN (
    'uploaded',
    'validating',
    'virus_scanning',
    'validated',
    'extracting_pages',
    'ocr_pending',
    'ocr_running',
    'chunking',
    'hashing',
    'indexing',
    'needs_review',
    'source_verified',
    'validation_failed',
    'virus_blocked',
    'ocr_failed',
    'partial_ocr_failed',
    'corrupted',
    'quarantined',
    'processing_failed'
  )),
  user_status TEXT NOT NULL DEFAULT 'Lastet opp',
  uploaded_by UUID NOT NULL REFERENCES users(id),
  current_version_id UUID,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  CONSTRAINT documents_tenant_case_fk
    FOREIGN KEY (tenant_id, case_id) REFERENCES cases(tenant_id, id)
);

CREATE INDEX idx_documents_tenant_case ON documents(tenant_id, case_id);
CREATE INDEX idx_documents_status ON documents(tenant_id, case_id, status);
CREATE UNIQUE INDEX uq_documents_case_sha ON documents(tenant_id, case_id, sha256);

CREATE TRIGGER trg_documents_updated_at
BEFORE UPDATE ON documents
FOR EACH ROW EXECUTE FUNCTION set_updated_at();

CREATE TABLE document_versions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id UUID NOT NULL REFERENCES tenants(id),
  case_id UUID NOT NULL REFERENCES cases(id) ON DELETE CASCADE,
  document_id UUID NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
  version_no INT NOT NULL,
  sha256 TEXT NOT NULL CHECK (length(sha256) = 64),
  storage_uri TEXT NOT NULL,
  created_by UUID REFERENCES users(id),
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  UNIQUE(document_id, version_no),
  CONSTRAINT document_versions_case_fk
    FOREIGN KEY (tenant_id, case_id) REFERENCES cases(tenant_id, id)
);

CREATE INDEX idx_document_versions_doc ON document_versions(document_id);

ALTER TABLE documents
  ADD CONSTRAINT documents_current_version_fk
  FOREIGN KEY (current_version_id) REFERENCES document_versions(id);

CREATE TABLE pages (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id UUID NOT NULL REFERENCES tenants(id),
  case_id UUID NOT NULL REFERENCES cases(id) ON DELETE CASCADE,
  document_id UUID NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
  page_number INT NOT NULL CHECK (page_number > 0),
  ocr_status TEXT NOT NULL DEFAULT 'pending' CHECK (ocr_status IN (
    'pending',
    'running',
    'complete',
    'low_confidence',
    'failed',
    'manually_verified'
  )),
  user_status TEXT NOT NULL DEFAULT 'Ikke lest ennå',
  ocr_text TEXT,
  ocr_confidence NUMERIC(4,3) CHECK (ocr_confidence IS NULL OR (ocr_confidence >= 0 AND ocr_confidence <= 1)),
  text_hash TEXT,
  image_hash TEXT,
  bates_label TEXT,
  exhibit_label TEXT,
  warnings JSONB NOT NULL DEFAULT '[]',
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  UNIQUE(document_id, page_number),
  CONSTRAINT pages_case_fk
    FOREIGN KEY (tenant_id, case_id) REFERENCES cases(tenant_id, id)
);

CREATE INDEX idx_pages_document ON pages(document_id);
CREATE INDEX idx_pages_case_status ON pages(tenant_id, case_id, ocr_status);
CREATE TRIGGER trg_pages_updated_at
BEFORE UPDATE ON pages
FOR EACH ROW EXECUTE FUNCTION set_updated_at();

CREATE TABLE chunks (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id UUID NOT NULL REFERENCES tenants(id),
  case_id UUID NOT NULL REFERENCES cases(id) ON DELETE CASCADE,
  document_id UUID NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
  page_id UUID REFERENCES pages(id) ON DELETE CASCADE,
  chunk_index INT NOT NULL CHECK (chunk_index >= 0),
  text TEXT NOT NULL,
  text_hash TEXT NOT NULL,
  source_span JSONB NOT NULL DEFAULT '{}',
  embedding_ref TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  UNIQUE(document_id, chunk_index),
  CONSTRAINT chunks_case_fk
    FOREIGN KEY (tenant_id, case_id) REFERENCES cases(tenant_id, id)
);

CREATE INDEX idx_chunks_document ON chunks(document_id);
CREATE INDEX idx_chunks_case ON chunks(tenant_id, case_id);

CREATE TABLE document_processing_jobs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id UUID NOT NULL REFERENCES tenants(id),
  case_id UUID NOT NULL REFERENCES cases(id) ON DELETE CASCADE,
  document_id UUID NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
  document_version_id UUID REFERENCES document_versions(id),
  job_type TEXT NOT NULL CHECK (job_type IN (
    'validate',
    'virus_scan',
    'extract_pages',
    'ocr',
    'chunk',
    'hash',
    'index',
    'full_process'
  )),
  status TEXT NOT NULL DEFAULT 'queued' CHECK (status IN (
    'queued','running','succeeded','failed','retrying','cancelled'
  )),
  input_hash TEXT,
  attempt_count INT NOT NULL DEFAULT 0,
  max_attempts INT NOT NULL DEFAULT 3,
  error_code TEXT,
  user_message TEXT,
  technical_message TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  UNIQUE(document_id, document_version_id, job_type, input_hash)
);

CREATE INDEX idx_doc_jobs_status ON document_processing_jobs(status, created_at);
CREATE INDEX idx_doc_jobs_case ON document_processing_jobs(tenant_id, case_id);
CREATE TRIGGER trg_doc_jobs_updated_at
BEFORE UPDATE ON document_processing_jobs
FOR EACH ROW EXECUTE FUNCTION set_updated_at();

-- ---------------------------------------------------------------------------
-- Sources, facts, evidence, timeline
-- ---------------------------------------------------------------------------

CREATE TABLE source_refs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id UUID NOT NULL REFERENCES tenants(id),
  case_id UUID NOT NULL REFERENCES cases(id) ON DELETE CASCADE,
  document_id UUID NOT NULL REFERENCES documents(id),
  page_id UUID REFERENCES pages(id),
  chunk_id UUID REFERENCES chunks(id),
  quote TEXT,
  bates_label TEXT,
  status TEXT NOT NULL DEFAULT 'valid' CHECK (status IN ('valid','needs_review','invalid')),
  user_status TEXT NOT NULL DEFAULT 'Gyldig kilde',
  confidence NUMERIC(4,3) CHECK (confidence IS NULL OR (confidence >= 0 AND confidence <= 1)),
  created_by UUID REFERENCES users(id),
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  CONSTRAINT source_refs_case_fk
    FOREIGN KEY (tenant_id, case_id) REFERENCES cases(tenant_id, id),
  CONSTRAINT source_refs_must_reference_page_or_chunk
    CHECK (page_id IS NOT NULL OR chunk_id IS NOT NULL OR bates_label IS NOT NULL)
);

CREATE INDEX idx_source_refs_case ON source_refs(tenant_id, case_id);
CREATE INDEX idx_source_refs_document ON source_refs(document_id);
CREATE INDEX idx_source_refs_page ON source_refs(page_id);

CREATE TABLE fact_claims (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id UUID NOT NULL REFERENCES tenants(id),
  case_id UUID NOT NULL REFERENCES cases(id) ON DELETE CASCADE,
  text TEXT NOT NULL,
  source_status TEXT NOT NULL DEFAULT 'missing_source' CHECK (source_status IN (
    'documented',
    'missing_source',
    'disputed',
    'assumed',
    'needs_review'
  )),
  confidence_label TEXT NOT NULL DEFAULT 'undocumented' CHECK (confidence_label IN (
    'documented',
    'likely',
    'assumed',
    'disputed',
    'undocumented'
  )),
  created_by UUID REFERENCES users(id),
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  CONSTRAINT fact_claims_case_fk
    FOREIGN KEY (tenant_id, case_id) REFERENCES cases(tenant_id, id)
);

CREATE INDEX idx_fact_claims_case ON fact_claims(tenant_id, case_id);
CREATE INDEX idx_fact_claims_source_status ON fact_claims(tenant_id, case_id, source_status);
CREATE TRIGGER trg_fact_claims_updated_at
BEFORE UPDATE ON fact_claims
FOR EACH ROW EXECUTE FUNCTION set_updated_at();

CREATE TABLE fact_claim_source_refs (
  fact_claim_id UUID NOT NULL REFERENCES fact_claims(id) ON DELETE CASCADE,
  source_ref_id UUID NOT NULL REFERENCES source_refs(id) ON DELETE CASCADE,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  PRIMARY KEY (fact_claim_id, source_ref_id)
);

CREATE TABLE evidence_items (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id UUID NOT NULL REFERENCES tenants(id),
  case_id UUID NOT NULL REFERENCES cases(id) ON DELETE CASCADE,
  title TEXT NOT NULL,
  evidence_type TEXT NOT NULL CHECK (evidence_type IN ('document','image','statement','note','other')),
  description TEXT,
  created_by UUID REFERENCES users(id),
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  CONSTRAINT evidence_items_case_fk
    FOREIGN KEY (tenant_id, case_id) REFERENCES cases(tenant_id, id)
);

CREATE INDEX idx_evidence_case ON evidence_items(tenant_id, case_id);
CREATE TRIGGER trg_evidence_updated_at
BEFORE UPDATE ON evidence_items
FOR EACH ROW EXECUTE FUNCTION set_updated_at();

CREATE TABLE evidence_source_refs (
  evidence_item_id UUID NOT NULL REFERENCES evidence_items(id) ON DELETE CASCADE,
  source_ref_id UUID NOT NULL REFERENCES source_refs(id) ON DELETE CASCADE,
  relation TEXT NOT NULL DEFAULT 'supports' CHECK (relation IN ('supports','weakens','context')),
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  PRIMARY KEY (evidence_item_id, source_ref_id)
);

CREATE TABLE timeline_events (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id UUID NOT NULL REFERENCES tenants(id),
  case_id UUID NOT NULL REFERENCES cases(id) ON DELETE CASCADE,
  title TEXT NOT NULL,
  description TEXT,
  event_date DATE,
  date_status TEXT NOT NULL DEFAULT 'unknown' CHECK (date_status IN ('exact','approximate','unknown')),
  created_by UUID REFERENCES users(id),
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  CONSTRAINT timeline_events_case_fk
    FOREIGN KEY (tenant_id, case_id) REFERENCES cases(tenant_id, id)
);

CREATE INDEX idx_timeline_case_date ON timeline_events(tenant_id, case_id, event_date);
CREATE TRIGGER trg_timeline_updated_at
BEFORE UPDATE ON timeline_events
FOR EACH ROW EXECUTE FUNCTION set_updated_at();

CREATE TABLE timeline_event_source_refs (
  timeline_event_id UUID NOT NULL REFERENCES timeline_events(id) ON DELETE CASCADE,
  source_ref_id UUID NOT NULL REFERENCES source_refs(id) ON DELETE CASCADE,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  PRIMARY KEY (timeline_event_id, source_ref_id)
);

CREATE TABLE risk_items (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id UUID NOT NULL REFERENCES tenants(id),
  case_id UUID NOT NULL REFERENCES cases(id) ON DELETE CASCADE,
  title TEXT NOT NULL,
  description TEXT,
  severity TEXT NOT NULL DEFAULT 'medium' CHECK (severity IN ('low','medium','high','critical')),
  status TEXT NOT NULL DEFAULT 'open' CHECK (status IN ('open','mitigated','accepted','closed')),
  affected_object_type TEXT,
  affected_object_id UUID,
  created_by UUID REFERENCES users(id),
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  CONSTRAINT risk_items_case_fk
    FOREIGN KEY (tenant_id, case_id) REFERENCES cases(tenant_id, id)
);

CREATE INDEX idx_risk_case_status ON risk_items(tenant_id, case_id, status);
CREATE TRIGGER trg_risk_updated_at
BEFORE UPDATE ON risk_items
FOR EACH ROW EXECUTE FUNCTION set_updated_at();

-- ---------------------------------------------------------------------------
-- Drafts and source coverage
-- ---------------------------------------------------------------------------

CREATE TABLE draft_documents (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id UUID NOT NULL REFERENCES tenants(id),
  case_id UUID NOT NULL REFERENCES cases(id) ON DELETE CASCADE,
  title TEXT NOT NULL,
  draft_type TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'draft' CHECK (status IN (
    'draft',
    'source_checked',
    'review_required',
    'approved',
    'export_ready',
    'exported',
    'missing_source',
    'unresolved_conflict',
    'policy_blocked',
    'insufficient_coverage'
  )),
  user_status TEXT NOT NULL DEFAULT 'Utkast',
  created_by UUID REFERENCES users(id),
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  CONSTRAINT draft_documents_case_fk
    FOREIGN KEY (tenant_id, case_id) REFERENCES cases(tenant_id, id)
);

CREATE INDEX idx_drafts_case ON draft_documents(tenant_id, case_id);
CREATE INDEX idx_drafts_status ON draft_documents(tenant_id, case_id, status);
CREATE TRIGGER trg_drafts_updated_at
BEFORE UPDATE ON draft_documents
FOR EACH ROW EXECUTE FUNCTION set_updated_at();

CREATE TABLE draft_sections (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id UUID NOT NULL REFERENCES tenants(id),
  case_id UUID NOT NULL REFERENCES cases(id) ON DELETE CASCADE,
  draft_id UUID NOT NULL REFERENCES draft_documents(id) ON DELETE CASCADE,
  section_index INT NOT NULL,
  heading TEXT,
  content TEXT NOT NULL DEFAULT '',
  source_status TEXT NOT NULL DEFAULT 'missing_source'
    CHECK (source_status IN ('documented','partial','missing_source','needs_review')),
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  UNIQUE(draft_id, section_index),
  CONSTRAINT draft_sections_case_fk
    FOREIGN KEY (tenant_id, case_id) REFERENCES cases(tenant_id, id)
);

CREATE INDEX idx_draft_sections_draft ON draft_sections(draft_id);
CREATE INDEX idx_draft_sections_source_status ON draft_sections(tenant_id, case_id, source_status);
CREATE TRIGGER trg_draft_sections_updated_at
BEFORE UPDATE ON draft_sections
FOR EACH ROW EXECUTE FUNCTION set_updated_at();

CREATE TABLE draft_section_source_refs (
  draft_section_id UUID NOT NULL REFERENCES draft_sections(id) ON DELETE CASCADE,
  source_ref_id UUID NOT NULL REFERENCES source_refs(id) ON DELETE CASCADE,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  PRIMARY KEY (draft_section_id, source_ref_id)
);

-- ---------------------------------------------------------------------------
-- Assistant
-- ---------------------------------------------------------------------------

CREATE TABLE assistant_sessions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id UUID NOT NULL REFERENCES tenants(id),
  case_id UUID REFERENCES cases(id) ON DELETE CASCADE,
  user_id UUID NOT NULL REFERENCES users(id),
  current_summary TEXT,
  last_intent_fingerprint TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  ended_at TIMESTAMPTZ
);

CREATE INDEX idx_assistant_sessions_case ON assistant_sessions(tenant_id, case_id);
CREATE INDEX idx_assistant_sessions_user ON assistant_sessions(user_id);

CREATE TABLE assistant_messages (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  session_id UUID NOT NULL REFERENCES assistant_sessions(id) ON DELETE CASCADE,
  tenant_id UUID NOT NULL REFERENCES tenants(id),
  case_id UUID REFERENCES cases(id) ON DELETE CASCADE,
  user_id UUID REFERENCES users(id),
  role TEXT NOT NULL CHECK (role IN ('user','assistant','system')),
  content_redacted TEXT NOT NULL,
  content_storage_policy TEXT NOT NULL DEFAULT 'redacted_summary'
    CHECK (content_storage_policy IN ('redacted_summary','full_text_allowed','do_not_store_full_text')),
  intent TEXT,
  topic_fingerprint TEXT,
  answer_fingerprint TEXT,
  referenced_objects JSONB NOT NULL DEFAULT '[]',
  safety_flags JSONB NOT NULL DEFAULT '[]',
  quality_gate JSONB NOT NULL DEFAULT '{}',
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_assistant_messages_session ON assistant_messages(session_id, created_at);
CREATE INDEX idx_assistant_messages_topic ON assistant_messages(tenant_id, case_id, topic_fingerprint);

CREATE TABLE assistant_guided_actions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  assistant_message_id UUID NOT NULL REFERENCES assistant_messages(id) ON DELETE CASCADE,
  tenant_id UUID NOT NULL REFERENCES tenants(id),
  case_id UUID REFERENCES cases(id) ON DELETE CASCADE,
  action_type TEXT NOT NULL CHECK (action_type IN (
    'explain_this',
    'show_me_how',
    'do_it_with_me',
    'check_my_work',
    'why_blocked',
    'what_next',
    'legal_work_help'
  )),
  label TEXT NOT NULL,
  payload JSONB NOT NULL DEFAULT '{}',
  requires_approval BOOLEAN NOT NULL DEFAULT FALSE,
  may_change_data BOOLEAN NOT NULL DEFAULT FALSE,
  status TEXT NOT NULL DEFAULT 'created' CHECK (status IN ('created','started','completed','cancelled')),
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  completed_at TIMESTAMPTZ
);

CREATE INDEX idx_guided_actions_case ON assistant_guided_actions(tenant_id, case_id);

-- ---------------------------------------------------------------------------
-- Control gates, approvals and exports
-- ---------------------------------------------------------------------------

CREATE TABLE control_gate_results (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id UUID NOT NULL REFERENCES tenants(id),
  case_id UUID NOT NULL REFERENCES cases(id) ON DELETE CASCADE,
  gate_type TEXT NOT NULL CHECK (gate_type IN ('export','external_share','bulk_change','sensitive_action')),
  target_type TEXT NOT NULL,
  target_id UUID NOT NULL,
  status TEXT NOT NULL CHECK (status IN ('pass','blocked','needs_approval')),
  user_summary TEXT NOT NULL,
  blockers JSONB NOT NULL DEFAULT '[]',
  warnings JSONB NOT NULL DEFAULT '[]',
  evidence_refs JSONB NOT NULL DEFAULT '[]',
  created_by UUID REFERENCES users(id),
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  CONSTRAINT control_gate_case_fk
    FOREIGN KEY (tenant_id, case_id) REFERENCES cases(tenant_id, id)
);

CREATE INDEX idx_control_gate_case ON control_gate_results(tenant_id, case_id, gate_type, target_type, target_id);

CREATE TABLE approval_decisions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id UUID NOT NULL REFERENCES tenants(id),
  case_id UUID NOT NULL REFERENCES cases(id) ON DELETE CASCADE,
  target_type TEXT NOT NULL CHECK (target_type IN ('export_gate','export_package','external_share','bulk_change','sensitive_action')),
  target_id UUID NOT NULL,
  decision TEXT NOT NULL CHECK (decision IN ('approved','rejected')),
  comment TEXT,
  decided_by UUID NOT NULL REFERENCES users(id),
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  CONSTRAINT approval_case_fk
    FOREIGN KEY (tenant_id, case_id) REFERENCES cases(tenant_id, id)
);

CREATE INDEX idx_approvals_target ON approval_decisions(tenant_id, case_id, target_type, target_id);

CREATE TABLE export_packages (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id UUID NOT NULL REFERENCES tenants(id),
  case_id UUID NOT NULL REFERENCES cases(id) ON DELETE CASCADE,
  draft_id UUID NOT NULL REFERENCES draft_documents(id),
  export_type TEXT NOT NULL CHECK (export_type IN ('pdf','docx','bundle')),
  status TEXT NOT NULL DEFAULT 'created' CHECK (status IN ('created','ready','failed')),
  storage_uri TEXT,
  manifest JSONB NOT NULL DEFAULT '{}',
  export_gate_result_id UUID NOT NULL REFERENCES control_gate_results(id),
  approval_id UUID NOT NULL REFERENCES approval_decisions(id),
  created_by UUID NOT NULL REFERENCES users(id),
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  CONSTRAINT export_packages_case_fk
    FOREIGN KEY (tenant_id, case_id) REFERENCES cases(tenant_id, id)
);

CREATE INDEX idx_exports_case ON export_packages(tenant_id, case_id);

-- ---------------------------------------------------------------------------
-- Audit
-- ---------------------------------------------------------------------------

CREATE TABLE audit_events (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id UUID NOT NULL REFERENCES tenants(id),
  case_id UUID REFERENCES cases(id) ON DELETE SET NULL,
  actor_user_id UUID REFERENCES users(id),
  action TEXT NOT NULL,
  object_type TEXT,
  object_id UUID,
  summary TEXT NOT NULL,
  metadata JSONB NOT NULL DEFAULT '{}',
  correlation_id TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_audit_tenant_case_time ON audit_events(tenant_id, case_id, created_at DESC);
CREATE INDEX idx_audit_action ON audit_events(tenant_id, action, created_at DESC);
CREATE INDEX idx_audit_object ON audit_events(object_type, object_id);

-- Prevent normal update/delete on audit events.
CREATE OR REPLACE FUNCTION prevent_audit_mutation()
RETURNS TRIGGER AS $$
BEGIN
  RAISE EXCEPTION 'audit_events are append-only';
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_audit_no_update
BEFORE UPDATE ON audit_events
FOR EACH ROW EXECUTE FUNCTION prevent_audit_mutation();

CREATE TRIGGER trg_audit_no_delete
BEFORE DELETE ON audit_events
FOR EACH ROW EXECUTE FUNCTION prevent_audit_mutation();

-- ---------------------------------------------------------------------------
-- Idempotency
-- ---------------------------------------------------------------------------

CREATE TABLE idempotency_keys (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id UUID NOT NULL REFERENCES tenants(id),
  user_id UUID REFERENCES users(id),
  key TEXT NOT NULL,
  request_hash TEXT NOT NULL,
  response_status INT,
  response_body JSONB,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  expires_at TIMESTAMPTZ NOT NULL DEFAULT (now() + interval '24 hours'),
  UNIQUE(tenant_id, key)
);

-- ---------------------------------------------------------------------------
-- Release-critical views/check helpers
-- ---------------------------------------------------------------------------

CREATE VIEW case_source_readiness AS
SELECT
  c.tenant_id,
  c.id AS case_id,
  COUNT(fc.id) FILTER (WHERE fc.source_status = 'missing_source') AS missing_source_count,
  COUNT(ds.id) FILTER (WHERE ds.source_status IN ('missing_source','needs_review')) AS draft_sections_missing_source_count,
  COUNT(p.id) FILTER (WHERE p.ocr_status IN ('low_confidence','failed')) AS pages_needing_review
FROM cases c
LEFT JOIN fact_claims fc ON fc.case_id = c.id
LEFT JOIN draft_sections ds ON ds.case_id = c.id
LEFT JOIN pages p ON p.case_id = c.id
GROUP BY c.tenant_id, c.id;

-- ---------------------------------------------------------------------------
-- Notes for Codex
-- ---------------------------------------------------------------------------

-- Enforcement requiring "documented fact has at least one source ref" should be
-- implemented in service-level transaction logic and integration tests because
-- it depends on join table existence. Do not rely only on UI validation.
--
-- Export creation must verify:
-- - gate result status is pass/needs_approval with valid approval
-- - approval target matches gate result
-- - draft has no missing-source sections
-- - case has no critical unresolved risk
-- - audit event is emitted
--
-- Every SELECT in services/api must include tenant_id and permission checks.
