# 📝 Shadow Goose — Onboarding Questionnaire (Pre‑filled)

## 1) Contacts & Timeline
- Primary Points of Contact: Alan McCarthy • Impact Director • alan@shadow-goose.com
- Technical Owner(s): Alan McCarthy
- Decision Maker(s) for Sign‑off: Alan McCarthy
- Target Staging Date: 15 September 2025
- Target Production Go‑Live Date: 1 October 2025
- Time Zone(s): Australia/Melbourne

## 2) Domains & DNS
- Staging Web Domain: staging.shadow-goose.org
- Staging API Domain: api.staging.shadowgoose.org
- Production Web Domain: app.shadowgoose.org
- Production API Domain: api.shadowgoose.org
- DNS Host/Provider: Cloudflare
- SSL: Render-managed TLS (Let’s Encrypt)
- Domain Constraints/Policies: None

## 3) Branding
- App Display Name: Shadow Goose Entertainment
- Logos: /assets/logo-light.svg, /assets/logo-dark.svg
- Brand Colours (Hex): Primary #1A1A1A, Secondary #FFFFFF, Accent #FF6600, Background #F5F5F5
- Typography: Heading - Poppins, Body - Open Sans
- Favicon & Social Image: /assets/favicon.png, /assets/social.png
- Email Branding Logo URL: https://shadow-goose.com
- Tone/Aesthetic Notes: Bold, authentic, slightly quirky

## 4) Environment & Secrets
- Secret Sharing Method: 1Password
- DATABASE_URL: Supplied via 1Password
- SECRET_KEY: Supplied via 1Password
- JWT_SECRET_KEY: Supplied via 1Password
- REDIS_URL: Not used
- SENTRY_DSN: Supplied via 1Password
- CORS Origins: ["https://shadow-goose.com", ...]

## 5) Roles, Access & Authentication
- Role Matrix: Admin - Full access; Manager - Create/edit projects; User - View/edit assigned items
- Admin Users: Alan McCarthy • alan@shadow-goose.com.au
- SSO/IdP: Google Workspace
- Password Policy: Min 12 chars, MFA required, 90-day rotation

## 6) Integrations
- Notion Workspace: Shadow Goose HQ

## 7) Analytics & Monitoring
- Primary KPIs & Targets: Grant success rate 40%+, audience growth 400% in 4 months
- Enable Frontend Analytics at Launch?: Yes
- Sentry Recipients/Escalation Channel: Alan McCarthy

## 8) Data & ML
- Seed Data for UAT: Existing projects & grant entries
- ML Features at Launch: Yes (grant matching, insights)
- Data Sensitivity/Compliance Notes: PII compliance, retention 7 years

## 9) UAT Plan
- Test Users: Alan McCarthy • Admin; Kiara X • Manager; Stephen Y • User
- UAT Window: 15–22 September 2025
- Extra Acceptance Criteria: Mobile optimisation, API latency <200ms
- Triage Channel for Bugs/Questions: Slack #dev-uat

## 10) Support & Ops
- Preferred Support Channel: Slack
- SLA / Response Expectations: 1 business day
- Backup/Restore Expectations: Daily automated backups, 14-day retention
- Post-Go-Live Meeting Cadence: Fortnightly

## 11) Risks & Constraints
- Known Risks: API rate limits, user adoption speed
- Mitigations: Caching, staged rollout

## 12) Approvals
- Discovery Approved By: Alan McCarthy • Strategic Officer • 8 August 2025
- Security/Privacy Approval: Alan McCarthy
- Final Go-Live Approver: Alan McCarthy
