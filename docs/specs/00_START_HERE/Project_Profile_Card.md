# Advokat AI — Project Profile Card

**Package version:** Codex-ready developer package v0.4  
**Date:** 2026-05-27  
**Product class:** Legal AI case workspace / juridisk kontrollplattform  
**Release model:** No MVP. Build toward Pilot Candidate, then Release Candidate, then Official Release.

## Binding product premise

Advokat AI is a legal operating system for document-driven case work. The user works inside one calm, source-controlled case room. Internally, specialized agents help with documents, OCR, facts, evidence, chronology, legal sources, risk, drafts and quality control.

The first shippable milestone is **Pilot Candidate**, not MVP. Pilot Candidate must be safe for real legal documents inside controlled pilot agreements. Official Release requires full Definition of Done, legal sign-off, security sign-off, compliance sign-off, QA evidence and operational readiness.

## Non-negotiable rules

1. No factual claim without source or explicit `missing_source` status.
2. No critical action without preview and explicit approval where required.
3. No final export without control gate.
4. No hidden AI uncertainty.
5. No shared memory across cases.
6. No unlogged critical operation.
7. No AI-generated legal conclusion presented as authoritative legal advice.
8. Human legal responsibility remains with the user/organization.
9. Every material operation must be traceable to actor, case, object, version and source basis.
10. System design must minimize user cognitive load and make complex legal work feel manageable.

## Canonical release phases

| Phase | Name | Purpose |
|---|---|---|
| 1 | Foundation | Core architecture, case isolation, document pipeline, audit, permissions and source model |
| 2 | Pilot Candidate | Real documents, controlled pilot users, source graph, drafts, control gates and legal assistant UX |
| 3 | Release Candidate | Full QA, security, compliance, performance, legal review and operational hardening |
| 4 | Official Release | Public release-ready version with complete Definition of Done |

## Project profile

| Field | Value |
|---|---|
| Project name | Advokat AI |
| Product category | Legal AI case workspace / juridisk saksrom |
| Primary platform | Web app, desktop-first responsive |
| Primary users | Lawyers, legal associates, case handlers, legal teams |
| Secondary users | Compliance, security, administrators, reviewers |
| First operational release | Pilot Candidate |
| Official release condition | Full DoD + legal/security/compliance/QA sign-off |
| Core job-to-be-done | Turn legal documents into controlled facts, evidence, chronology, argument and drafts with source traceability |
| Main risk | False confidence, missing sources, privacy breach, unauthorized export, audit gaps |
| Main differentiator | Calm legal assistant + source-controlled legal workspace + control gates |
| Default language | Norwegian first; English-ready architecture |
| Default jurisdiction | Norway first; configurable for future jurisdictions |

# Information Needed From Owner

This package is intentionally detailed enough for Codex/dev team to start. The items below should still be decided by the owner before production hardening. Defaults are provided so development is not blocked.

## P0 — must decide before Pilot Candidate

| Decision | Why it matters | Default in package |
|---|---|---|
| Primary jurisdiction(s) | Legal source handling, language, templates, disclaimers | Norway first, EU privacy/compliance |
| Hosting region | Personal data and legal document storage | EU/EEA region only |
| Document storage provider | Real documents require secure object storage | S3-compatible EU bucket |
| Auth provider | Login, MFA, roles, enterprise access | OIDC/SAML-ready abstraction |
| LLM provider policy | Whether legal docs may be sent to external AI APIs | Provider abstraction, no training, no retention where contract allows |
| OCR provider | Accuracy/cost/privacy tradeoff | Local/dev OCR + pluggable production OCR |
| Pilot customer type | Access model and onboarding | Law firm/internal legal team |
| Data retention rules | Legal/compliance and deletion behavior | Configurable per tenant/case |
| Human sign-off owner | Who may approve export/legal output | Case owner or appointed legal reviewer |
| Brand/product language | UI/copy tone | Norwegian first, English-ready |

## P1 — must decide before Official Release

| Decision | Why it matters | Default in package |
|---|---|---|
| Legal source integration | Accuracy of laws/cases | Manual verified legal source object first |
| Client portal | External collaboration risk | Post-pilot unless explicitly approved |
| Bates standard | Court/exhibit practice varies | Configurable label pattern |
| Audit export format | Enterprise/compliance needs | JSON + CSV + PDF report later |
| Pricing/packaging | Product operations | Not specified for dev |
| Support and incident SLA | Operations | Draft policy included |
| AI Act classification review | Compliance | Required release gate |
| DPIA owner | Privacy compliance | Required release gate |

