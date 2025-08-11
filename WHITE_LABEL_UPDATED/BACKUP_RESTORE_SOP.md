# 🗃️ Backup & Restore SOP

PostgreSQL (Render managed)

Backup (do not store secrets in repo)
```bash
# Backup database
pg_dump "$DATABASE_URL" --format=custom --file backups/navimpact_$(date +%F).dump
```

Restore (to a new database)
```bash
# Restore database
pg_restore --clean --no-owner --dbname "$DATABASE_URL" backups/navimpact_YYYY-MM-DD.dump
```

Checklist
- Pause writes
- Verify dump size and integrity
- Restore to staging first; validate app
- Resume production

Retention
- Keep daily for 7 days, weekly for 4 weeks, monthly for 6 months
