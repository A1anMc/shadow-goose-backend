# 🧪 Scripts Reference

Health & Deployment
```bash
bash scripts/pre_deployment_check.sh --env production
bash scripts/verify-health.sh https://navimpact-api.onrender.com
bash scripts/verify-deployment.sh --web https://navimpact-web.onrender.com --api https://navimpact-api.onrender.com
bash scripts/post_deployment_monitor.sh
```

Frontend
```bash
# Dev server (SSR preview)
cd frontend && npm run dev

# Build static export and preview locally
cd frontend && npm run preview

# If already built, serve the exported site
cd frontend && npm run start:static
```

Data & Setup
```bash
python scripts/setup_notion_env.py
python scripts/seed_db.py
python scripts/add_real_grants.py
```

ML
```bash
python scripts/train_ml_models.py
# verify model artifacts under app/ml_models/
```

Notes
- Pass non‑interactive flags where available
- Ensure env vars are set in Render before scripts that depend on them
