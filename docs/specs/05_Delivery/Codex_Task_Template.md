# Codex Task Template

Use this prompt for each implementation PR:

```text
You are Codex working in the Advokat AI repository.

Read:
- AGENTS.md
- 00_START_HERE/CODEX_MASTER_INSTRUCTION.md
- 05_Delivery/Codex_PR_Backlog_Exact_Build_Order_v1.md
- all specs referenced by this PR

Task:
Implement PR <number>: <name> exactly as specified.

Requirements:
- preserve module boundaries
- use canonical data objects only
- enforce tenant/case isolation
- use Norwegian user-facing copy
- emit audit events where required
- add tests from Test_Matrix_Codex_Executable_v1.md
- do not expose technical terms in default UI
- do not bypass control gates
- do not mark done without validation

Before coding:
Create a short execution plan using 00_START_HERE/PLANS.md.

After coding:
Report:
1. files changed
2. behavior implemented
3. tests added
4. validation run
5. remaining gaps, if any
```
