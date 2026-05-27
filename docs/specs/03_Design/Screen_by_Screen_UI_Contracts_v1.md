# Advokat AI — Screen-by-Screen UI Contracts v1

Every screen must follow the visible-only-useful rule.

Default user-facing language is Norwegian.

---

# 1. Global layout

## Purpose

Give user stable orientation and low mental load.

## Layout

```text
┌─────────────────────────────────────────────────────────────┐
│ Topbar: sak, søk/kommando, status, varsler, bruker          │
├───────────────┬───────────────────────────────┬─────────────┤
│ Sidebar       │ Main work area                │ Assistant   │
│ navigation    │ active object/workflow        │ context     │
├───────────────┴───────────────────────────────┴─────────────┤
│ Bottom status: lagret, dekning, avvik, eksportstatus        │
└─────────────────────────────────────────────────────────────┘
```

## Global UI rules

- Sidebar contains stable navigation only.
- Topbar never shows raw technical state.
- Assistant panel always has current screen context.
- Bottom status shows only useful readiness/risk information.
- Technical details are behind “Vis teknisk grunnlag” for authorized users.

---

# 2. `/login`

## Purpose
Authenticate user.

## Components
- Product logo/name
- Login button
- Short trust statement
- Privacy/security link

## Copy
- «Logg inn»
- «Sikkert juridisk saksrom for dokumentdrevet arbeid.»

## States
- loading: «Logger inn ...»
- error: «Innloggingen feilet. Prøv igjen.»

## Assistant
Not shown by default.

---

# 3. `/cases`

## Purpose
Show cases user can access.

## Components
- Case list
- Create case button
- Search/filter
- Empty state
- Assistant quick help

## Primary action
«Ny sak»

## Empty state
Title:
> «Start med å opprette en sak»

Body:
> «Når saken er opprettet, kan du laste opp dokumenter og la systemet hjelpe deg å bygge fakta, kronologi og utkast.»

Assistant prompt:
> «Jeg kan forklare hvordan en sak bygges opp her.»

## Permissions
- all authenticated users see accessible cases
- create case requires `case:create`

## Audit
- case_created
- case_opened

---

# 4. `/cases/new`

## Purpose
Create a new case.

## Fields
- title
- case_type
- jurisdiction
- description optional
- sensitivity level

## Assistant behavior
If user hesitates:
> «Det holder å fylle inn en enkel arbeidstittel nå. Du kan justere detaljene senere.»

## Validation
- title required
- jurisdiction default `NO`
- sensitivity default `standard`

## Audit
- case_created

---

# 5. `/cases/[caseId]` — Case overview

## Purpose
Give calm overview of case status and next step.

## Main cards
1. Dokumentgrunnlag
2. Fakta og kilder
3. Kronologi
4. Risiko
5. Utkast
6. Eksportstatus

## Must show
- case title
- readiness summary
- document count
- missing source count
- unresolved risk count
- next recommended action

## Must not show
- job IDs
- raw hash values
- raw OCR confidence values
- internal agent names

## Assistant context
Assistant must know:
- case readiness
- next blocker
- last user action
- user's role

## Assistant default prompt
> «Spør meg om hva du bør gjøre videre i saken.»

## Primary CTA logic
- no documents → «Last opp dokumenter»
- documents processing → «Se dokumentstatus»
- missing sources → «Fiks manglende kilder»
- draft incomplete → «Fortsett på utkast»
- export blocked → «Se hva som stopper eksport»
- export ready → «Forhåndsvis eksport»

---

# 6. `/cases/[caseId]/documents`

## Purpose
Manage uploaded documents.

## Components
- Upload button
- Document table/cards
- status chips
- filters
- warnings summary

## Document statuses user-facing

| Internal | User-facing |
|---|---|
| `uploaded` | «Lastet opp» |
| `validating` | «Kontrollerer fil» |
| `processing` | «Leser dokument» |
| `ocr_complete` | «Tekst lest» |
| `needs_review` | «Må ses over» |
| `source_verified` | «Klar som kilde» |
| `failed` | «Kunne ikke behandles» |
| `quarantined` | «Stoppet av sikkerhetskontroll» |

## Empty state
> «Last opp dokumentene saken bygger på.»

## Assistant
Can explain:
- supported file types
- what OCR means in plain language
- why document needs review
- how to make a document source-ready

---

# 7. `/cases/[caseId]/documents/[documentId]`

## Purpose
Read document, inspect pages, create source refs.

## Components
- document viewer
- page list
- OCR text panel
- source selection tools
- facts linked to selected page
- assistant panel

## Primary actions
- «Marker som kilde»
- «Opprett faktapåstand»
- «Se usikre sider»
- «Forklar denne siden»

## Warning example
> «Denne siden er usikkert lest. Se over teksten før du bruker den som kilde.»

## Assistant actions
- `explain_this`
- `show_me_how`
- `do_it_with_me`
- `legal_work_help`

## Audit
- document_opened
- source_ref_created
- page_reviewed
- fact_claim_created

---

# 8. `/cases/[caseId]/facts`

## Purpose
Manage fact claims and source status.

## Components
- fact table/cards
- source status
- dispute status
- evidence links
- filters

## Fact statuses

| Internal | User-facing |
|---|---|
| `documented` | «Dokumentert» |
| `missing_source` | «Mangler kilde» |
| `disputed` | «Omtvistet» |
| `assumed` | «Antatt» |
| `needs_review` | «Må vurderes» |

## Rule
A fact can be saved as `missing_source`, but cannot support final export as documented without source.

## Assistant
Explains:
- what a fact claim is
- why a source is needed
- difference between documented, assumed and disputed
- how to link evidence

---

# 9. `/cases/[caseId]/timeline`

## Purpose
Build chronological case story.

## Components
- timeline list
- date uncertainty marker
- source-linked events
- event evidence panel

## Primary actions
- «Ny hendelse»
- «Lag hendelser fra dokument»
- «Finn hendelser uten kilde»

## Assistant
Can help:
- create timeline from selected documents
- explain date uncertainty
- identify gaps

---

# 10. `/cases/[caseId]/evidence`

## Purpose
Show evidence items and relation to facts.

## Components
- evidence list
- linked facts
- supporting/weakening indicator
- source refs

## Assistant
Can explain:
- what a piece of evidence supports
- what lacks support
- what should be reviewed

---

# 11. `/cases/[caseId]/risks`

## Purpose
Show unresolved risks and weak points.

## Components
- risk list
- severity
- affected facts/drafts
- mitigation action

## Copy
Use calm language:
- «Bør vurderes»
- «Kan svekke argumentet»
- «Mangler dokumentgrunnlag»
- «Motstrid i dokumentene»

Never use alarmist copy unless critical.

---

# 12. `/cases/[caseId]/drafts`

## Purpose
Manage legal drafts.

## Components
- draft list
- readiness status
- source coverage
- last edited

## Primary action
«Nytt utkast»

---

# 13. `/cases/[caseId]/drafts/[draftId]`

## Purpose
Write source-controlled legal draft.

## Components
- document editor
- source coverage gutter
- paragraph warnings
- source panel
- assistant panel
- check/export buttons

## User-facing warnings
- «Dette avsnittet mangler kilde.»
- «Denne kilden bør kontrolleres.»
- «Dette avsnittet bygger på en antakelse.»

## Assistant
Must support:
- `check_my_work`
- `why_blocked`
- `legal_work_help`
- `show_me_how`

## Export button behavior
If blocked:
- button says «Se hva som mangler»
- opens export gate preview
- assistant explains blockers

---

# 14. `/cases/[caseId]/export-preview`

## Purpose
Control gate before export.

## Must show
- status: ready/blocked/needs approval
- blockers
- affected documents/facts/draft sections
- what user can fix now
- approval requirement
- preview of export package

## Must not show
- raw validator codes by default
- internal gate engine names

## Assistant
Default:
> «Jeg kan forklare hvorfor eksport er stoppet og gå gjennom punktene med deg.»

## Primary action
- blocked: «Gå til første problem»
- ready: «Send til godkjenning»
- approved: «Opprett eksportpakke»

---

# 15. `/cases/[caseId]/audit`

## Purpose
Advanced/audit view for authorized roles.

## Visible to
- tenant_admin
- case_owner
- auditor
- legal_reviewer when permitted

## Can show technical detail
This is an advanced view.

## Must include
- actor
- action
- object
- timestamp
- case version
- source/gate refs
- export refs

## Must not allow
- deletion/editing of audit events

---

# 16. `/settings`

## Purpose
Tenant/user settings.

## Sections
- profile
- organization
- permissions
- security
- integrations
- data retention
- feature flags

## Assistant
Can explain settings in simple language.

---

# 17. Command palette

## Purpose
Let experienced users jump to actions.

## Trigger
Cmd/Ctrl+K

## Commands
- Søk i saken
- Last opp dokument
- Lag faktapåstand
- Finn manglende kilder
- Sjekk utkast
- Forhåndsvis eksport
- Spør assistenten
- Vis audit-logg

## Rule
Commands must respect permissions and control gates.
