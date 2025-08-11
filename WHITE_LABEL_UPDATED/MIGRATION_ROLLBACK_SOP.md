# 🔄 Migration Rollback SOP (Alembic)

Identify head and history
```bash
alembic current
alembic history --verbose | cat
```

Rollback one revision
```bash
alembic downgrade -1
```

Rollback to specific revision
```bash
alembic downgrade <revision_id>
```

Forward again
```bash
alembic upgrade head
```

Notes
- Always snapshot DB before downgrades
- Coordinate downtime if schema is widely used
