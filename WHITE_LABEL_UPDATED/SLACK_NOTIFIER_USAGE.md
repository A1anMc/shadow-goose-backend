# 📣 Slack Notifier Usage

Helper: `app/services/integrations/slack_service.py`

Initialization
```python
from app.services.integrations.slack_service import SlackNotifier
notifier = SlackNotifier()
```

Send messages
```python
notifier.send_text("Deployment successful", channel="#alerts")
notifier.notify_task_assigned(title="Draft grant brief", assignee="alex@example.com", due_date="2025-08-15")
notifier.notify_grant_deadline(grant_name="Screen Australia Story Development", days_left=7)
notifier.notify_report_generated(report_name="Monthly Impact Summary")
```

Environment
- `SLACK_BOT_TOKEN`, `SLACK_SIGNING_SECRET`, `SLACK_DEFAULT_CHANNEL`, `SLACK_WEBHOOK_URL`

Notes
- Best‑effort notifications; failures should not block API responses
- Use staging channels for tests before switching to production
