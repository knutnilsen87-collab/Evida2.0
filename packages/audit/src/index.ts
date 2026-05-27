export interface AuditEvent {
  id: string;
  action: string;
  case_id?: string;
  object_type?: string;
  object_id?: string;
  summary: string;
  created_at: string;
}
