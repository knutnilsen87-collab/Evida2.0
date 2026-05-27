# services/api AGENTS.md

Backend rules:
- Enforce tenant_id and case membership on every case resource.
- Emit audit events for material operations.
- Use ErrorEnvelope with Norwegian user_message.
- Put control gate logic here, not in frontend.
- Do not call provider-specific AI/OCR code outside adapters.
