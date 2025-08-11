# 🚀 New Client Onboarding Process (SOP)

Purpose
- Provide a clear, repeatable path to onboard a new client to NavImpact as a white‑label instance.
- Outcome: a branded, configured, tested deployment with monitoring and support in place.

## Phase 0 — Intake (1 day)
Owners: Sales/PM → Platform
- Capture client request and target go‑live
- Share WHITE_LABEL_UPDATED pack; confirm point of contact(s)
Artifacts: Kickoff meeting scheduled, access list
Exit: Stakeholders and dates confirmed

## Phase 1 — Discovery (1–2 days)
Owners: Platform + Client Admin
- Collect Strategic Alignment package (mission/vision/values, OKRs)
- Gather branding assets (logos, palette, fonts)
- Define roles and access (Admin/Manager/User; SSO if needed)
- List integrations (Slack/Notion) and reporting needs
Artifacts:
- `CLIENT_ROLLOUT_TEMPLATE.md` filled Sections 1–4, 11–13
- Branding assets placed under `branding/` (or shared link)
Exit: Signed off discovery doc

## Phase 2 — Environment & DNS (0.5–1 day)
Owners: Platform + DevOps
- Duplicate and fill `ENV_TEMPLATE.staging` and `ENV_TEMPLATE.production`
- Create/verify Render services (staging first)
- Configure DNS (CNAMEs) for web/API
Artifacts:
- Render staging deployed via `configs/render.staging.yaml`
- DNS records documented in rollout template
Exit: Staging URLs accessible

## Phase 3 — Branding & Configuration (1–2 days)
Owners: Platform
- Set `NEXT_PUBLIC_CLIENT`, `APP_NAME`, `BRAND_COLOR`, `BRAND_LOGO_URL`
- Apply branding in frontend; verify emails render with branding
- Configure roles/RBAC and initial users
Artifacts:
- Staging branded instance live; sample emails sent
Exit: Branding and access verified by client admin

## Phase 4 — Integrations & Analytics (0.5–1 day)
Owners: Platform + Client Admin
- Slack: set `SLACK_*`; send test message (staging)
- Notion: set `NOTION_*`; run a sample sync
- Analytics: define KPIs; enable `SENTRY_DSN`; (optionally) `NEXT_PUBLIC_ENABLE_ANALYTICS`
Artifacts:
- `INTEGRATIONS_QUICKSTART.md` followed; evidence in logs
- `ANALYTICS_SETUP.md` partially completed
Exit: Integrations validated in staging

## Phase 5 — Data & ML (0.5–1 day)
Owners: Platform
- Seed minimal data (projects/grants) if needed
- Train ML model: `python scripts/train_ml_models.py`
- Verify ML endpoints (`/api/v1/ml-analytics/*`)
Artifacts:
- Model artifacts under `app/ml_models/`
- Postman calls green (collection: `postman/NavImpact.postman_collection.json`)
Exit: ML features operational

## Phase 6 — UAT (1–2 days)
Owners: Client Admin + Platform
- Run UAT using `CHECKLISTS.md` and guide’s testing section
- Verify acceptance criteria per phase
- Collect sign‑off in rollout template
Artifacts:
- Completed UAT sign‑off checklist
Exit: Client sign‑off to go live

## Phase 7 — Production Go‑Live (0.5 day)
Owners: DevOps + Platform
- Deploy with `configs/render.yaml`
- Set production envs; configure DNS and SSL
- Run `SCRIPTS.md` verification steps; enable alerts
Artifacts:
- Production health checks green; alerts live
Exit: Public URLs operational

## Phase 8 — Post‑Go‑Live (ongoing)
Owners: Platform + Support
- Monitor per `MONITORING_GUIDE.md`, `SLOS.md`, `ALERT_RULES_EXAMPLES.md`
- Weekly ops: review Sentry, validate backups (`BACKUP_RESTORE_SOP.md`), check SLAs
- Plan next release; maintain `CHANGELOG` and `RELEASE_NOTES`
Artifacts:
- First weekly ops report; schedule for quarterly review
Exit: Handover complete; steady‑state support

---

## RACI (Summary)
- Responsible: Platform (engineering), DevOps
- Accountable: Product/PM
- Consulted: Client Admin, Security
- Informed: Stakeholders/Execs

## Entry/Exit Gates (Quick)
- Discovery signed → proceed to environment
- Staging branded + integrations validated → start UAT
- UAT sign‑off + health checks green → production

## References (Use These)
- Guide: `WHITE_LABEL_GUIDE.md`
- Template: `CLIENT_ROLLOUT_TEMPLATE.md`
- Checklists: `CHECKLISTS.md`
- Envs: `ENV_TEMPLATE.staging`, `ENV_TEMPLATE.production`
- Deploy: `configs/render.staging.yaml`, `configs/render.yaml`
- Ops: `MONITORING_GUIDE.md`, `SLOS.md`, `ALERT_RULES_EXAMPLES.md`
- Data/ML: `SCRIPTS.md`, `BACKUP_RESTORE_SOP.md`, `MIGRATION_ROLLBACK_SOP.md`

## Timeline (Typical)
- Week 0: Intake & Discovery
- Week 1: Staging setup, branding, integrations, ML, UAT
- Week 2: Production go‑live and handover
