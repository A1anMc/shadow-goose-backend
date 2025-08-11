# 📊 Analytics Setup

KPIs & Dashboards
- Define primary KPIs and targets
- Publish executive, grants, impact dashboards

Event Instrumentation
- Frontend events: grant_viewed, grant_matched, grant_applied, task_created, task_completed, comment_added, report_generated, export_downloaded
- Naming consistency and property schemas

Environment
- `NEXT_PUBLIC_ENABLE_ANALYTICS=true` (when ready)
- `SENTRY_DSN` configured
- Confirm `NEXT_PUBLIC_API_URL`, `NEXT_PUBLIC_CLIENT`

Validation
- Verify events in staging
- Backfill dashboards with seed data if needed

Cadence
- Weekly exec snapshot, monthly KPI review, quarterly strategy review
