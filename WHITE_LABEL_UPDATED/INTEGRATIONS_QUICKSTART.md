# 🔌 Integrations Quickstart (Slack & Notion)

## Slack
- Create a Slack app; add scopes: `chat:write`, `channels:read` (and/or incoming webhook)
- Add bot to target channels (e.g., `#alerts`, `#team`, `#exec`)
- Set env:
  - `SLACK_BOT_TOKEN`
  - `SLACK_SIGNING_SECRET`
  - `SLACK_DEFAULT_CHANNEL`
  - `SLACK_WEBHOOK_URL` (optional)

Backend helper: `app/services/integrations/slack_service.py`

Example usage (task assignment notification):
```python
from app.services.integrations.slack_service import SlackNotifier
SlackNotifier().notify_task_assigned(title="Draft grant brief", assignee="alex@example.com", due_date="2025-08-15")
```

## Notion
- Decide: One‑way (NavImpact → Notion) or Bi‑directional
- Set env:
  - `NOTION_API_KEY`
  - `NOTION_CLIENT_ID`, `NOTION_CLIENT_SECRET`, `NOTION_REDIRECT_URI` (OAuth)
  - `NOTION_DATABASE_ID_GRANTS`, `NOTION_DATABASE_ID_TASKS`
- Map properties (title/status/date/people) per database

Endpoints (see implementation docs if present):
- `POST /api/v1/notion/connect-workspace`
- `GET  /api/v1/notion/workspaces`
- `POST /api/v1/notion/sync-project/{id}`
- `GET  /api/v1/notion/sync-logs`

## Verification
- Send a test Slack message in staging
- Run a Notion sync on a sample record
- Confirm logs and permissions
