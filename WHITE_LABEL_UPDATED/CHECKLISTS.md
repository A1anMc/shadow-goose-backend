# ✅ Consolidated Checklists

## Acceptance Criteria Per Phase
- Phase 2: Branded pages load; health endpoints reachable; E2E tests pass; no console errors
- Phase 3: Login/logout work; protected routes enforced; roles respected; JWT valid/expiring
- Phase 4: Matching returns results; reports generate; CSV/PDF exports succeed; ML endpoints live (`/api/v1/ml-analytics/*`); grant model trained; OKR alignment dashboard populated; AI recommendations visible

## Go‑Live Checklist
- Preflight: `scripts/pre_deployment_check.sh`
- Backend health: `scripts/verify-health.sh`
- Deployment verification: `scripts/verify-deployment.sh`
- Post‑deploy monitor: `scripts/post_deployment_monitor.sh`
- Frontend preview for UAT: `cd frontend && npm run preview`

Example:
```bash
bash scripts/pre_deployment_check.sh --env production
bash scripts/verify-health.sh https://navimpact-api.onrender.com
bash scripts/verify-deployment.sh --web https://navimpact-web.onrender.com --api https://navimpact-api.onrender.com
```

## Dara Recommendations
- ML & OKR: Model trained; ML endpoints live; OKR dashboard populated; AI recommendations visible
- Slack: `SLACK_*` envs set; bot in channels; task assignment notifications firing in staging
- Notion: OAuth connected; `NOTION_*` envs set; DB IDs mapped; sync runs and logs visible
- Analytics: KPIs defined; dashboards published; `NEXT_PUBLIC_ENABLE_ANALYTICS=true` (when ready); `SENTRY_DSN` set; core events instrumented
- Branding: `NEXT_PUBLIC_CLIENT`, `APP_NAME`, `BRAND_COLOR`, `BRAND_LOGO_URL` applied across UI and emails
- Security: Strong secrets; correct `CORS_ORIGINS`; rate limiting enabled
- Performance: Health green; p95 within SLO; DB indexing verified
- Documentation: Rollout template filled; support contacts; rollback plan
- Code Quality: SOLID/DRY; tests pass for critical paths
