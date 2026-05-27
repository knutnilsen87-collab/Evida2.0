# Codex One-Shot Build Prompt

Use this prompt if giving the full package to Codex.

```text
You are Codex. Build Advokat AI exactly according to this documentation package.

Binding command:
“Bygg dette produktet nøyaktig slik, med denne arkitekturen,
disse skjermene, disse dataobjektene, disse reglene,
disse modulgrensene og disse akseptansekriteriene.”

This is not a generic chatbot, generic legal document manager, or generic SaaS app.
It is a controlled legal case workspace with real-document Pilot Candidate support,
strict source integrity, auditability, control gates, and an AI assistant that feels like
a legal collaboration partner.

Read first:
1. AGENTS.md
2. 00_START_HERE/CODEX_MASTER_INSTRUCTION.md
3. 00_START_HERE/Codex_Execution_Instructions.md
4. 05_Delivery/Codex_PR_Backlog_Exact_Build_Order_v1.md
5. 04_Technical/OpenAPI_Pilot_Candidate_v1.yaml
6. 04_Technical/SQL_Schema_Pilot_Candidate_v1.sql
7. 04_Technical/Assistant_Architecture_and_Actions_v1.md
8. 03_Design/AI_Assistant_UX_Contract_v1.md
9. 03_Design/Screen_by_Screen_UI_Contracts_v1.md
10. 06_QA/Test_Matrix_Codex_Executable_v1.md

Build order:
Follow 05_Delivery/Codex_PR_Backlog_Exact_Build_Order_v1.md from PR 0 onward.

Rules:
- No MVP interpretation.
- Use Pilot Candidate → Release Candidate → Official Release model.
- No factual claim without source or missing_source status.
- No final export without gate and approval.
- No critical action without preview.
- No hidden uncertainty.
- No technical language in default UI.
- Every visible UI element must be useful.
- The assistant must not produce generic repeated standard answers.
- Preserve tenant/case isolation.
- Emit audit for material actions.
- Add tests for every feature.

Do not ask questions unless a hard blocker exists:
- missing production credential
- irreversible production action
- legal/compliance decision not covered by defaults
- direct contradiction between source-of-truth docs

Otherwise use package defaults and continue.
```
