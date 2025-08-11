# 🧭 Client Rollout — Shadow Goose

## 1) Client Overview
- Client name: Shadow Goose
- Primary contacts: Alan McCarthy • Impact Director • alan@shadow-goose.com
- Target go‑live date: Production 2025-10-01 (Staging: 2025-09-15)
- Domains (web, API):
  - Staging: web `staging.shadow-goose.org`, api `api.staging.shadowgoose.org`
  - Production: web `app.shadowgoose.org`, api `api.shadowgoose.org`
  - DNS: Cloudflare • SSL: Render-managed TLS (Let’s Encrypt)

## 2) Brand & Assets
- Logo files (SVG/PNG): `/assets/logo-light.svg`, `/assets/logo-dark.svg`
- Color palette (hex): Primary `#1A1A1A`, Secondary `#FFFFFF`, Accent `#FF6600`, Background `#F5F5F5`
- Typography (webfonts): Heading `Poppins`, Body `Open Sans`
- Favicon & social images: `/assets/favicon.png`, `/assets/social.png`

## 3) Environment & DNS
- Staging URLs (web/api): https://staging.shadow-goose.org / https://api.staging.shadowgoose.org
- Production URLs (web/api): https://app.shadowgoose.org / https://api.shadowgoose.org
- DNS records (CNAMEs):
  - web.staging → staging.shadow-goose.org
  - api.staging → api.staging.shadowgoose.org
  - web → app.shadowgoose.org
  - api → api.shadowgoose.org
- Frontend env: `NEXT_PUBLIC_API_URL`, `NEXT_PUBLIC_CLIENT=shadow-goose`, `NEXT_PUBLIC_APP_NAME=Shadow Goose Entertainment`, `NEXT_PUBLIC_APP_VERSION`
- Backend env: `DATABASE_URL`, `SECRET_KEY`, `JWT_SECRET_KEY`, `SENTRY_DSN`, `REDIS_URL (n/a)`, `CORS_ORIGINS`

## 4) Roles & Access
- Role matrix: Admin (full); Manager (create/edit projects); User (view/edit assigned)
- Admin users: Alan McCarthy • alan@shadow-goose.com.au
- SSO/IdP (optional): Google Workspace

## 5) Phased Plan
### Phase 2: Deployment
- Owners: Platform + DevOps
- Client inputs: Domains, assets, env values
- Deliverables: Services provisioned, CI/CD configured
- Acceptance: Branded pages load; health endpoints reachable; E2E pass; no console errors

### Phase 3: Authentication & Users
- Owners: Platform + Client Admin
- Client inputs: Users, roles, SSO metadata
- Deliverables: Auth flows, protected routes, RBAC
- Acceptance: Login/logout; roles enforced; JWT validity

### Phase 4: Grants & Reporting
- Owners: Platform + Grants Lead
- Client inputs: Sample applications, report templates
- Deliverables: AI matching, CSV/PDF exports, scheduled reports
- Acceptance: Matching returns results; exports succeed

## 6) Timeline
- T0 (Kickoff): Confirm branding, domains, envs, role matrix
- T+3 days (Staging): Branding live on staging; UAT begins (2025-09-15)
- T+7 days (Production): Go‑live; monitoring active (2025-10-01)

## 7) Checklists
### Go‑Live
- Preflight: `scripts/pre_deployment_check.sh`
- Backend health: `scripts/verify-health.sh`
- Deployment verification: `scripts/verify-deployment.sh`
- Post‑deploy monitor: `scripts/post_deployment_monitor.sh`

### UAT Sign‑off
- Branding consistent across pages
- Auth flows work for target roles
- Key reports/export verified
- Performance acceptable on target devices
- Mobile optimisation verified
- API p95 latency < 200ms

## 8) Risks & Mitigations
- Risk: API rate limits • Mitigation: Caching and backoff strategy
- Risk: User adoption speed • Mitigation: Staged rollout and training

## 9) Change Management
- Versioning plan: Semantic versioning per‑client (shadow-goose‑vX.Y.Z)
- Changelog link: [link]
- Rollback plan: Documented in `MIGRATION_ROLLBACK_SOP.md`

## 10) Contacts & Support
- Engineering: [name]
- DevOps: [name]
- Client Admin: Alan McCarthy
- Support channel: Slack (primary)
- SLA: 1 business day

## 11) Strategic Alignment & OKRs (Tasks)
- [ ] Capture annual/quarterly OKRs (Grant success rate 40%+, audience growth 400% in 4 months)
- [ ] Define KPIs and dashboards
- [ ] Align reporting templates to OKRs
- [ ] Stakeholder review and sign‑off

Optional tracker
| Item | Source/Link | Owner | Due | Status |
|------|-------------|-------|-----|--------|
| Mission/Vision |  |  |  |  |
| Values |  |  |  |  |
| Annual OKRs |  |  |  |  |
| Q OKRs |  |  |  |  |
| Strategic Plan |  |  |  |  |
| Reporting Templates |  |  |  |  |

---

## 12) Analytics & Insights (High‑Level)
- KPIs & Outcomes: Grant success rate, audience growth
- Dashboards: exec, grants pipeline, impact/outcomes, ops
- Product Analytics: enable at launch (frontend)
- Env & Setup: `NEXT_PUBLIC_ENABLE_ANALYTICS=true` (prod), `SENTRY_DSN`
- Owners: Engineering, Client (Alan)

## 13) Slack & Notion Integration
### Slack
- Workspace: [tbd]
- Channels: [#dev-uat, #alerts]
- Env: `SLACK_BOT_TOKEN`, `SLACK_SIGNING_SECRET`, `SLACK_DEFAULT_CHANNEL`, `SLACK_WEBHOOK_URL`

### Notion
- Workspace & owner: Shadow Goose HQ
- Database IDs: [tbd]
- Direction: [tbd]

## 14) Dashboard Navigation & Tabs (UAT)
- Verify routes: `/insights`, `/integrations/*`, `/grants/*`, `/admin`, `/notifications`, `/compliance`, `/status`
- Sign‑off: routes load under branding; protected sections gated once RBAC is enabled; no 404s

## 15) UAT Plan
- Test users: Alan (Admin), Kiara X (Manager), Stephen Y (User)
- Window: 2025-09-15 → 2025-09-22
- Triage: Slack `#dev-uat`
