# 🛡️ Threat Model Checklist

Assets
- PII, grant data, credentials, tokens

Attack Surfaces
- API endpoints, authentication, integrations (Slack/Notion)

Threats
- Injection, auth bypass, CSRF, SSRF, data exfiltration

Controls
- Input validation, authz checks, rate limiting, secrets management

Reviews
- Security review per release; dependency scans; pen-test annually
