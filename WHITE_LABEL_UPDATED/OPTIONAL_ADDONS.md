# ➕ Optional Add‑Ons Catalog

Offer these optional enhancements during client onboarding or post‑go‑live. Each add‑on includes prerequisites, deliverables, effort estimate, and acceptance criteria.

## How to request
- Open a request referencing this doc and the client’s `CLIENT_ROLLOUT_TEMPLATE.md`
- Include desired add‑ons, target date, decision maker(s)
- We confirm feasibility, effort, and timeline with a short proposal

---

## 1) Authentication & Security
- SSO (OIDC/SAML: Okta, Azure AD, Auth0)
  - Prereq: IdP admin; metadata/redirect URIs
  - Deliverables: Login via IdP; role mapping; docs
  - Effort: M; Acceptance: Successful SSO login + role enforcement
- SCIM User Provisioning
  - Prereq: IdP SCIM support
  - Deliverables: Auto‑provision/deprovision users; audit log
  - Effort: M; Acceptance: CRUD sync works end‑to‑end
- Audit Logging & IP Allowlist
  - Deliverables: Sensitive ops log; IP allowlist (API)
  - Effort: S; Acceptance: Logs present; allowlist enforced

## 2) Integrations
- Jira/Asana Workflows
  - Prereq: API tokens; target projects
  - Deliverables: Two‑way sync (tasks/comments) or push only
  - Effort: M; Acceptance: Round‑trip test successful
- Microsoft Teams Notifications
  - Deliverables: Equivalent to Slack notifier via webhooks
  - Effort: S; Acceptance: Teams channel messages received
- Google Workspace
  - Deliverables: Calendar sync for deadlines; Drive doc links
  - Effort: M; Acceptance: Events created; links resolved
- Zapier/Webhooks
  - Deliverables: Outbound webhooks; Zapier examples
  - Effort: S; Acceptance: Sample Zap triggers reliably

## 3) Data & Analytics
- GA4 / Mixpanel Product Analytics
  - Deliverables: Event schema; dashboards; env toggles
  - Effort: S; Acceptance: Events visible; dashboards live
- Custom Dashboards (Metabase/Superset)
  - Prereq: DB read access or replica
  - Deliverables: Exec/ops dashboards; SSO (optional)
  - Effort: M; Acceptance: Stakeholder sign‑off
- Data Warehouse Export (BigQuery/Redshift/Snowflake)
  - Deliverables: Daily export jobs; schema mapping
  - Effort: M‑L; Acceptance: Verified load + data checks

## 4) AI / ML Enhancements
- Custom Grant Matching Model (Client‑tuned)
  - Deliverables: Feature engineering; retraining; A/B report
  - Effort: M‑L; Acceptance: Measurable lift vs baseline
- Impact Prediction Fine‑Tuning
  - Deliverables: Model updates + validation report
  - Effort: M; Acceptance: Accuracy/KPI thresholds met
- RAG over Client Documents
  - Prereq: Document corpus + access rules
  - Deliverables: Q&A endpoint + usage guardrails
  - Effort: M‑L; Acceptance: Precision/recall targets

## 5) Reporting
- Branded PDF Reports
  - Deliverables: Templates (exec/departmental)
  - Effort: M; Acceptance: Pixel‑perfect PDFs generated
- Scheduled Email Reports
  - Deliverables: Schedules; recipient lists; logs
  - Effort: S; Acceptance: Timely delivery + content checks

## 6) Scrapers & Data Sources
- New Grant Sources (Global/Philanthropic/Corporate)
  - Prereq: Source list + terms compliance
  - Deliverables: Scrapers + monitoring + retry
  - Effort: M per source; Acceptance: Coverage and freshness SLAs
- Client Data Pipelines
  - Deliverables: Ingest ETL + validation rules
  - Effort: M‑L; Acceptance: Data quality KPIs met

## 7) UX & Branding
- Premium Theme Pack
  - Deliverables: Advanced components + animations
  - Effort: S‑M; Acceptance: Stakeholder visual sign‑off
- Multi‑Language (i18n)
  - Deliverables: Locale switcher; translations framework
  - Effort: M; Acceptance: Language QA pass

## 8) Collaboration & Productivity
- Real‑Time Notifications (WebSockets)
  - Deliverables: Live updates for tasks/comments
  - Effort: M; Acceptance: Latency < 1s in tests
- Kanban & Calendar Views
  - Deliverables: Board + ICS calendar sync
  - Effort: M; Acceptance: Functional parity with tasks

## 9) Mobile & Offline
- PWA Install with Offline Cache
  - Deliverables: Installable app; cache key flows
  - Effort: S‑M; Acceptance: Lighthouse PWA pass

## 10) Performance & Scale
- Redis Caching & CDN
  - Deliverables: Cache layer; CDN for assets
  - Effort: M; Acceptance: p95 latency improved >20%
- Load Testing & Tuning
  - Deliverables: K6/JMeter scripts; bottleneck fixes
  - Effort: M; Acceptance: Target TPS/SLOs met

## 11) Compliance & Governance
- GDPR Tooling & Data Retention Automation
  - Deliverables: Export/delete endpoints; retention jobs
  - Effort: M; Acceptance: DSR scenario tests pass
- Departmental Compliance Suites (e.g., DFFH, DJPR)
  - Deliverables: Specialized reports + audit trails
  - Effort: M; Acceptance: Department format compliance

## 12) Deployment & Infra
- Dedicated Environment / VPC Peering
  - Prereq: Cloud account and peering details
  - Deliverables: Isolated services; network policy
  - Effort: M‑L; Acceptance: Connectivity + security tests
- On‑Prem / Private Cloud Guidance
  - Deliverables: Reference architecture + handover
  - Effort: L; Acceptance: Design review approved

## 13) Support & Training
- Premium SLA (24/7 with RTO/RPO targets)
  - Deliverables: SLA document + on‑call rotation
  - Effort: S; Acceptance: Escalation tested
- Admin Training & Workshops
  - Deliverables: 2–4 sessions + materials
  - Effort: S; Acceptance: Attendance + feedback ≥ 4/5

---

Notes
- Effort S/M/L are relative (S ≤ 2 days, M 3–7 days, L 1–3 weeks)
- Bundles available (e.g., “Enterprise Security”, “Advanced Analytics”, “AI Suite”)
