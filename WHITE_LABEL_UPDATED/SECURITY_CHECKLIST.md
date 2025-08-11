# 🔐 Security Checklist

Secrets & Auth
- Strong `SECRET_KEY`, `JWT_SECRET_KEY` (32+ chars)
- Rotate credentials periodically
- Limit Notion/Slack scopes to what’s needed

CORS & Headers
- `CORS_ORIGINS` allows only required origins
- Set security headers on frontend (Next.js) and backend

Access & RBAC
- Roles configured per client (Admin/Manager/User)
- Protected routes enforced; tokens validated

Data Protection
- Use HTTPS only (Render enforces)
- Backups configured; validate restores
- Data retention policy agreed with client

Monitoring & Alerts
- `SENTRY_DSN` configured; alerting rules set
- 4xx/5xx logs monitored

Compliance
- WCAG accessibility
- GDPR/Privacy: consent & deletion requests respected
