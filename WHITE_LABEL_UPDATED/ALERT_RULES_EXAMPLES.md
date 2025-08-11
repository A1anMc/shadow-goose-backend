# 🚨 Alert Rules Examples

Sentry
- When error rate > 0.5% for 5 min → Page
- New issue frequency spikes by 200% in 10 min → Page
- p95 transaction duration > 800ms for 10 min → Ticket

Uptime/HTTP monitors
- Health endpoint `/health` fails 3 times in 5 min → Page
- Frontend `/api/health` fails 3 times in 5 min → Page

Notifications
- Slack `#alerts` via webhook
- Email to on-call rotation

Maintenance windows
- Suppress alerts during scheduled deploys (label releases)
