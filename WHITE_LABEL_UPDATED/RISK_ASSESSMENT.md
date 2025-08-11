# ⚠️ Risk Assessment (White‑Label Deployments)

Purpose
- Identify and manage risks across technical, security, data, compliance, performance, integrations, ML, deployment, and operational domains for each client rollout.

## Scoring Matrix
- Likelihood (L/M/H) × Impact (L/M/H) → Score: Low / Medium / High / Critical
- Prefer reducing likelihood with controls; keep contingency plans for high‑impact items.

| Likelihood | Impact | Score |
|------------|--------|-------|
| Low        | Low    | Low   |
| Low        | Medium | Medium|
| Low        | High   | High  |
| Medium     | Low    | Medium|
| Medium     | Medium | High  |
| Medium     | High   | Critical |
| High       | Low    | High  |
| High       | Medium | Critical |
| High       | High   | Critical |

---

## Top Risks (Default Set)

| Risk | Category | Likelihood | Impact | Score | Mitigation | Owner | Triggers | Status |
|------|----------|------------|--------|-------|------------|-------|----------|--------|
| Env misconfiguration in production | Deployment | M | H | Critical | Use `ENV_TEMPLATE.production`; peer review; preflight checks (`SCRIPTS.md`) | DevOps | New envs; manual edits | Open |
| DNS/SSL cutover delays | Deployment | M | M | High | Staged DNS; validate certs; off-peak window | DevOps | Registrar changes; cert renewal | Open |
| SSO integration issues | Security | M | H | Critical | Test in staging; fallback local auth; document IdP mapping | Platform | New IdP; metadata changes | Open |
| Data breach via integrations | Security | L | H | High | Principle of least privilege; rotate tokens; secrets store | Security | New tokens; vendor incidents | Open |
| PII mishandling / GDPR requests | Compliance | M | H | Critical | Add export/delete endpoints; data retention jobs | Platform | DSR received; audit requests | Open |
| DB performance under load | Performance | M | M | High | Index review; Redis cache; read patterns | Platform | p95 > SLO; timeouts | Open |
| Scraper EULA/robots non‑compliance | Compliance | L | M | Medium | Review terms; throttle; caching; logging | Platform | Source changes | Open |
| Two‑way sync conflicts (Jira/Asana) | Integrations | M | M | High | Define source‑of‑truth; conflict policies; logs | Platform | Concurrent updates | Open |
| ML model accuracy below baseline | ML | M | M | High | Validation set; retraining; feature checks | Platform | Data drift; schema changes | Open |
| RAG data leakage | ML/Security | L | H | High | Access controls; allowlist sources; redaction; eval | Security | New corpora | Open |
| Email deliverability issues | Ops | M | M | High | Proper SPF/DKIM/DMARC; logs; retries | DevOps | Domain changes | Open |
| Monitoring gaps / alert fatigue | Ops | M | M | High | Configure Sentry; tune thresholds (see `SLOS.md`) | Platform | New releases; noisy alerts | Open |

---

## Category Risks & Mitigations

### Deployment & Config
- Risk: Env drift between staging and prod → Mitigation: templates + peer approvals; `configs/render.*.yaml` source‑of‑truth.
- Risk: Rollback failures → Mitigation: `MIGRATION_ROLLBACK_SOP.md`; pre‑deploy DB snapshot; feature flags.

### Security & Privacy
- Risk: Token exposure → Mitigation: Render secrets; rotate quarterly; least privilege; no secrets in logs.
- Risk: CORS misconfiguration → Mitigation: Lock `CORS_ORIGINS` to known hosts; review prior to release.
- Risk: Vulnerable deps → Mitigation: `SECURITY_SCANS.md` in CI; CVE thresholds; patch cadence.

### Data & Compliance
- Risk: PII in logs/backups → Mitigation: Scrub logs; encrypt backups; retention policy per client.
- Risk: GDPR/DSR response gaps → Mitigation: Implement export/delete endpoints; audit trails.

### Integrations
- Risk: API rate limits/quotas → Mitigation: Backoff/retry; queue; monitor vendor status.
- Risk: Schema changes upstream → Mitigation: Contract tests; versioned mappers; alert on errors.

### Performance & Scale
- Risk: p95 latency breaches → Mitigation: Redis cache; DB indexing; monitor slow queries.
- Risk: Thundering herd during reports → Mitigation: Batch/schedule; cache report results.

### ML & Analytics
- Risk: Data drift → Mitigation: Periodic eval; retraining schedule; feature stability checks.
- Risk: Misleading KPIs → Mitigation: KPI owner sign‑off; dashboard annotations; data dictionary.

### UX & Accessibility
- Risk: Branding contrast failures → Mitigation: Contrast checks; WCAG review; alt text.
- Risk: Localization bugs (i18n) → Mitigation: Pseudo‑locale testing; glossary.

### Operational
- Risk: On‑call overload → Mitigation: Escalation policies; weekly ops review; alert hygiene.
- Risk: Backup restore untested → Mitigation: Monthly restore test in staging; report.

---

## Per‑Client Risk Register (Template)

| ID | Risk | Category | Likelihood | Impact | Score | Mitigation | Owner | Due | Status |
|----|------|----------|------------|--------|-------|------------|-------|-----|--------|
| R‑01 |  |  |  |  |  |  |  |  |  |
| R‑02 |  |  |  |  |  |  |  |  |  |

Scoring notes
- Likelihood: Low/Medium/High
- Impact: Low/Medium/High
- Status: Open / Mitigating / Accepted / Closed

---

## RAID Log (Template)

- Risks: See register
- Assumptions:
  - Example: Client will provide IdP metadata and admin access by <date>
- Issues:
  - Example: DNS cutover window conflicts with client event
- Dependencies:
  - Example: Google Workspace service account approval; Slack workspace admin consent

---

## Monitoring Links
- `MONITORING_GUIDE.md`: setup, alerts, dashboards
- `SLOS.md`: latency/availability/error budgets
- `ALERT_RULES_EXAMPLES.md`: alert thresholds and channels

## Review Cadence
- Pre‑UAT: Full risk review; adjust mitigations
- Post‑Go‑Live: Weekly ops review; monthly risk report; quarterly posture audit
