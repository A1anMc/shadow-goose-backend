# ✅ New Client Onboarding — One‑Page Checklist

Use this as a quick runbook. For details, see `ONBOARDING_PROCESS.md`.

## Phase 0 — Intake
- [ ] Confirm client POCs and go‑live date
- [ ] Share WHITE_LABEL_UPDATED pack

## Phase 1 — Discovery
- [ ] Gather Strategic Alignment package (mission/vision/values, OKRs)
- [ ] Collect branding assets (logos, palette, fonts)
- [ ] Define roles/RBAC and SSO (if any)
- [ ] Confirm integrations (Slack/Notion) and reporting

## Phase 2 — Environment & DNS
- [ ] Fill `ENV_TEMPLATE.staging` and create Render staging services
- [ ] Configure DNS (web/API) for staging
- [ ] Staging URLs accessible

## Phase 3 — Branding & Config
- [ ] Set `NEXT_PUBLIC_CLIENT`, `APP_NAME`, `BRAND_COLOR`, `BRAND_LOGO_URL`
- [ ] Apply branding in frontend; send sample branded email
- [ ] Configure roles/users; login verified

## Phase 4 — Integrations & Analytics
- [ ] Slack: set `SLACK_*`; send staging test message
- [ ] Notion: set `NOTION_*`; run sample sync
- [ ] Analytics: define KPIs; set `SENTRY_DSN`; (opt) enable frontend analytics

## Phase 5 — Data & ML
- [ ] Seed minimal data (projects/grants) if needed
- [ ] Train model: `python scripts/train_ml_models.py`
- [ ] Verify ML endpoints (`/api/v1/ml-analytics/*`)

## Phase 6 — UAT
- [ ] Run UAT per `CHECKLISTS.md` and guide testing
- [ ] Meet acceptance criteria per phase
- [ ] Client sign‑off recorded

## Phase 7 — Go‑Live (Prod)
- [ ] Fill `ENV_TEMPLATE.production`; set Render envs
- [ ] Deploy via `configs/render.yaml`; DNS + SSL configured
- [ ] Verify with `SCRIPTS.md`; enable alerts

## Phase 8 — Post‑Go‑Live
- [ ] Monitor per `MONITORING_GUIDE.md`, `SLOS.md`
- [ ] Weekly ops: Sentry review, backup verify, SLA checks
- [ ] Maintain `CHANGELOG` and `RELEASE_NOTES`

---

Quick References
- Templates: `CLIENT_ROLLOUT_TEMPLATE.md`, `ENV_TEMPLATE.*`
- Ops: `CHECKLISTS.md`, `SCRIPTS.md`, `MONITORING_GUIDE.md`
- Integrations: `INTEGRATIONS_QUICKSTART.md`, `SLACK_NOTIFIER_USAGE.md`
