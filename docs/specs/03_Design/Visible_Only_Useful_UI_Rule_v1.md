# Visible-Only-Useful UI Rule v1

## Core rule

Every visible UI element must be useful to the user.

A visible element is allowed only if it helps the user:
1. understand what is happening
2. understand what is missing
3. take the next safe step
4. avoid risk
5. verify source basis
6. collaborate effectively
7. complete the legal workflow

If not, hide it, simplify it, or move it to advanced/audit/admin view.

---

# 1. Default user view

The default interface must not show:
- internal agent names
- raw job states
- internal pipeline details
- backend errors
- raw stack traces
- provider names
- prompt details
- chunk identifiers
- hash values
- database identifiers
- model temperature/config
- queue names
- worker state names
- technical confidence terms without translation

---

# 2. User-language translations

| Internal/system term | Default user-facing copy |
|---|---|
| `ocr_confidence_below_threshold` | «Denne siden er usikkert lest. Se over teksten før du bruker den som kilde.» |
| `source_ref_validation_failed` | «Denne påstanden mangler gyldig kilde.» |
| `export_gate_blocked` | «Eksport er stoppet fordi noe må kontrolleres først.» |
| `chunk_hash_mismatch` | «Dokumentet ser ut til å være endret siden analysen ble gjort.» |
| `agent_run_warning` | «Analysen er ferdig, men det finnes punkter du bør se over.» |
| `tenant_access_denied` | «Du har ikke tilgang til denne saken.» |
| `job_failed_retryable` | «Behandlingen stoppet. Prøv igjen, eller be administrator se på saken.» |
| `approval_required` | «Dette må godkjennes før det kan utføres.» |
| `missing_export_approval` | «Eksporten må godkjennes før den kan lastes ned.» |
| `insufficient_coverage` | «Saken mangler nok dokumentgrunnlag til at dette kan godkjennes.» |

---

# 3. Progressive technical transparency

Technical detail is available only when:
- user opens advanced details
- user has auditor/admin role
- compliance requires it
- support/debugging requires it
- legal audit trail requires it

Even then, technical details must be organized and understandable.

---

# 4. Screen-level visible utility checklist

Every screen must answer:

1. Where am I?
2. What am I looking at?
3. Is this ready, incomplete or blocked?
4. What matters now?
5. What is the safest next step?
6. Where can I ask for help?
7. What will happen if I click the primary button?

---

# 5. Error copy

Errors must be:
- human-readable
- actionable
- calm
- specific enough to help
- non-technical by default

Bad:
> 500 Internal Server Error

Good:
> «Noe gikk galt da dokumentet skulle åpnes. Prøv igjen. Hvis det fortsetter, kan administrator se tekniske detaljer i audit-loggen.»

Bad:
> 403 Forbidden

Good:
> «Du har ikke tilgang til denne saken. Be sakseier legge deg til hvis du skal arbeide her.»

---

# 6. Assistant integration

Every important warning should have:
- short explanation
- “Forklar enklere”
- “Vis meg hva jeg må gjøre”
- “Gå til første problem”
- “Sjekk arbeidet mitt”

---

# 7. Do not over-disclose AI internals

Never show default user copy like:
- «LLM-en tror ...»
- «Agenten evaluerte ...»
- «Modellen returnerte ...»
- «Prompten feilet ...»

Use:
- «Systemet fant ...»
- «Analysen viser ...»
- «Dette bør kontrolleres ...»
- «Jeg er usikker på ...»

When AI uncertainty matters, show it plainly:
> «Jeg er ikke sikker nok på denne koblingen. Se over dokumentet før du bruker den som kilde.»
