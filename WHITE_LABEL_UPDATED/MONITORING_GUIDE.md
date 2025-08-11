# 🛡️ Monitoring & Alerts Guide

Sentry
- Create project; get DSN and set `SENTRY_DSN`
- Set environment tags (staging/production)
- Sampling: traces_sample_rate 0.2–1.0 depending on traffic
- Alerts: error frequency increase, release regression, latency budget breaches

Health & Uptime
- API health: `/health`
- Frontend health: `/api/health`
- External uptime check (e.g., UptimeRobot)

Dashboards
- Error rate (<0.5% target)
- p95 latency (<500ms web; <300ms API target)
- Throughput, top endpoints, slow queries

Runbooks
- Use `SCRIPTS.md` for verification
- Rollback via `MIGRATION_ROLLBACK_SOP.md`
- Restore via `BACKUP_RESTORE_SOP.md`

Weekly Ops
- Review Sentry issues and resolve
- Check SLA metrics vs SLOs
- Verify backups and test a restore in staging monthly
