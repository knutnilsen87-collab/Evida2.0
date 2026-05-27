# services/worker AGENTS.md

Worker rules:
- Jobs must be idempotent.
- Never duplicate pages/chunks on retry.
- Store hashes.
- Map technical failures to user-useful statuses.
- Do not make final legal/control gate decisions in worker.
