# 📞 Support

- Channels: Email and Slack per client contract
- Incident response: SEV levels and response times in SLOs
- Monitoring: Sentry alerts, deployment monitors, weekly health review
- Ownership: Engineering (primary), DevOps (infra), Client Admin (access)

Escalation
- SEV1: Immediate pager/phone bridge; 24/7 until resolved
- SEV2: Business hours + extended coverage until stable
- SEV3: Next business day triage

Runbooks
- Health checks: `scripts/verify-health.sh`
- Deploy verification: `scripts/verify-deployment.sh`
- Post‑deploy: `scripts/post_deployment_monitor.sh`
