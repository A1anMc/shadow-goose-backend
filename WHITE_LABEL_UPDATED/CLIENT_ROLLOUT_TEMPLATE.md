# 🧭 Client Rollout Template

Use this template to plan and execute a white‑label rollout for a specific client.

## 1) Client Overview
- Client name:
- Primary contacts:
- Target go‑live date:
- Domains (web, API):

## 2) Brand & Assets
- Logo files (SVG/PNG):
- Color palette (hex):
- Typography (webfonts):
- Favicon & social images:

## 3) Environment & DNS
- Staging URLs (web/api):
- Production URLs (web/api):
- DNS records (CNAMEs):
- Frontend env: `NEXT_PUBLIC_API_URL`, `NEXT_PUBLIC_CLIENT`, `NEXT_PUBLIC_APP_NAME`, `NEXT_PUBLIC_APP_VERSION`
- Backend env: `DATABASE_URL`, `SECRET_KEY`, `JWT_SECRET_KEY`, `SENTRY_DSN`, `REDIS_URL`, `CORS_ORIGINS`

## 4) Roles & Access
- Role matrix:
- Admin users:
- SSO/IdP (optional):

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
- T+3 days (Staging): Branding live on staging; UAT begins
- T+7 days (Production): Go‑live; monitoring active

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

## 8) Risks & Mitigations
- Risk:
- Mitigation:

## 9) Change Management
- Versioning plan:
- Changelog link:
- Rollback plan:

## 10) Contacts & Support
- Engineering:
- DevOps:
- Client Admin:
- Support channel:

## 11) Strategic Alignment & OKRs (Tasks)
- [ ] Collect organisation documents: mission, vision, values, strategic plan
- [ ] Capture annual and quarterly OKRs (company-level and team-level)
- [ ] Document strategic direction and top 3 priorities for the next 12 months
- [ ] Define explicit goals and measurable success criteria (KPIs)
- [ ] Map OKRs/goals to platform modules (Grants, Impact, Tasks, Media)
- [ ] Align reporting templates to OKRs (dashboards, exports, scheduled reports)
- [ ] Validate values/mission alignment in UI copy and branding
- [ ] Stakeholder review and sign‑off (Executive + Functional Leads)

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

### KPIs & Outcomes
- Primary KPIs (targets):
- Supporting metrics:
- Mapping to OKRs/goals:

KPI definition template
| KPI | Definition | Target | Data source | Owner | Review cadence |
|-----|------------|--------|-------------|-------|----------------|
|     |            |        |             |       |                |

### Dashboards (publish links)
- Executive overview (OKRs, KPIs)
- Grants pipeline & win rate
- Impact & outcomes (reports, frameworks)
- Operations health (latency, error rate)

### Product Analytics (events)
- Event taxonomy standard (naming, properties)
- Core events to instrument:
  - grant_viewed, grant_applied, grant_matched
  - task_created, task_completed, comment_added
  - report_generated, export_downloaded

Event dictionary
| Event | Description | Properties | Trigger | Owner |
|-------|-------------|------------|---------|-------|
|       |             |            |         |       |

### Funnels & Cohorts
- Key funnels (e.g., Grant discovery → Match → Apply)
- Cohorts (e.g., role, project type, time period)

### Reporting Cadence
- Weekly exec snapshot
- Monthly KPI review
- Quarterly strategy review

### Data Sources & Tooling
- Backend metrics (FastAPI, DB)
- Error monitoring (Sentry)
- Frontend analytics (toggle via env)
- Scheduled exports/reports

### Privacy, Compliance, Access
- Consent and anonymisation policy
- Data retention window
- Access control (roles for dashboards and raw data)

### Env & Setup
- Frontend: `NEXT_PUBLIC_ENABLE_ANALYTICS`, `NEXT_PUBLIC_ENV`
- Monitoring: `SENTRY_DSN`
- Confirm: `NEXT_PUBLIC_API_URL`, `NEXT_PUBLIC_CLIENT`

### Implementation Tasks
- [ ] Instrument core events (frontend)
- [ ] Enable backend performance metrics and error tracing
- [ ] Configure Sentry DSN and alerting rules
- [ ] Publish core dashboards and share to stakeholders
- [ ] Validate events and metrics in staging before production

Owners
- Product/Analytics lead:
- Engineering owner:
- Client stakeholder:

---

## 13) Slack & Notion Integration

### Slack
- Workspace:
- Channels (alerts, team, exec):
- App/Bot scopes: chat:write, channels:read, incoming-webhook

Env & setup
- `SLACK_BOT_TOKEN=`
- `SLACK_SIGNING_SECRET=`
- `SLACK_DEFAULT_CHANNEL=` (e.g., #alerts)
- `SLACK_WEBHOOK_URL=` (if using incoming webhooks)

Notification mapping
| Event | Channel | Message format |
|-------|---------|----------------|
| task_assigned | #team | "Task {title} assigned to {assignee} (due {due_date})" |
| grant_deadline_7d | #alerts | "Grant {name} closes in 7 days" |
| report_generated | #exec | "{report_name} is ready" |

Message template (example)
```json
{
  "text": "Task {{title}} assigned to {{assignee}} (due {{due_date}})",
  "blocks": []
}
```

Implementation tasks
- [ ] Create Slack app, add bot to channels
- [ ] Store env vars securely
- [ ] Implement notification hooks for mapped events
- [ ] Test messages in staging

### Notion
- Workspace & owner:
- Databases to sync: Grants, Tasks, Reports
- Direction: One‑way (NavImpact → Notion) or Bi‑directional

Env & setup
- `NOTION_API_KEY=`
- `NOTION_REDIRECT_URI=` (OAuth callback)
- `NOTION_DATABASE_ID_GRANTS=`
- `NOTION_DATABASE_ID_TASKS=`

Database property mapping
| NavImpact field | Notion property | Type |
|-----------------|------------------|------|
| grant_title | Name | title |
| status | Status | select |
| deadline | Deadline | date |
| assignee | Assignee | people |

Sync plan
- Frequency: On change / hourly schedule
- Conflict policy: Last write wins / source of truth: NavImpact
- Logging: Sync logs visible in admin

Implementation tasks
- [ ] Connect Notion workspace (OAuth)
- [ ] Create or select target databases
- [ ] Map properties per table
- [ ] Configure sync schedule and logging
- [ ] Validate end‑to‑end sync in staging

Security & compliance
- Limit scopes to required permissions
- Store tokens securely; rotate per policy
- Respect retention and deletion requests

## 14) Dashboard Navigation & Tabs (UAT)

Routes to verify
- Insights (`/insights`): ML insights render; no console errors
- Integrations (`/integrations`):
  - Status (`/integrations/status`): Lists required envs
  - Slack (`/integrations/slack`): Page reachable; test button visible
  - Notion (`/integrations/notion`): Page reachable; setup info visible
- Grants (`/grants`):
  - AI Matching, Timeline, Feedback, Apply (existing)
  - Applications (`/grants/applications`): Table renders
  - Documents (`/grants/documents`): Upload/Export buttons render
- Admin (`/admin`): Users & Roles, Audit Logs, Webhooks pages render
- Notifications (`/notifications`): Inbox and Preferences render
- Compliance (`/compliance`): Data/Accessibility sections render
- Status (`/status`): Shows `/api/health` response or placeholder

Sign‑off checklist
- [ ] All routes load under client branding
- [ ] Protected sections gated once RBAC is enabled
- [ ] Links present in sidebar and sub‑navs
- [ ] Empty states/readiness messages are clear
- [ ] No 404s or broken links
