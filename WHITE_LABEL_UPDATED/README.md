# 📦 White‑Label Release Pack (Updated)

This folder contains everything needed to white‑label and deploy NavImpact for a client.

## Contents
- `WHITE_LABEL_GUIDE.md`: Full implementation and rollout guide
- `CLIENT_ROLLOUT_TEMPLATE.md`: Per‑client plan template
- `ENGINEERING_ROADMAP.md`: Engineering milestones & progress
- `PRODUCT_ROADMAP.md`: White‑label product roadmap
- `ENV_TEMPLATE.production`: Production env template
- `GITIGNORE.template`: Recommended `.gitignore`
- `INTEGRATIONS_QUICKSTART.md`: Slack & Notion setup
- `CHECKLISTS.md`: Acceptance, go‑live, Dara recommendations
- `SUPPORT.md`: Support and escalation
- `SCRIPTS.md`: Script commands for deployment and checks
- `branding/README.md`: Branding assets checklist

## Quick Start
1. Duplicate `ENV_TEMPLATE.production` to your envs and fill values
2. Fill `CLIENT_ROLLOUT_TEMPLATE.md` for the client
3. Prepare branding assets per `branding/README.md`
4. Follow `WHITE_LABEL_GUIDE.md` → Client Rollout Brief
5. Verify with `CHECKLISTS.md` and `SCRIPTS.md`

## Frontend Preview
See `SCRIPTS.md` for:
- Dev: `cd frontend && npm run dev`
- Static preview: `cd frontend && npm run preview`

## Notes
- Do not commit filled envs; use Render secrets
- Keep migrations tracked; store DB dumps under `backups/` (ignored)
- Integrations: set Slack/Notion envs and verify in staging
