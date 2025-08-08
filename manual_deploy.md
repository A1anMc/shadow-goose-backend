# Manual Deployment Guide

## Issue Identified
The Render auto-deployment is not working. The services are stuck on old code.

## Solution: Manual Deployment Steps

### Step 1: Check Render Dashboard
1. Go to https://dashboard.render.com
2. Find the `shadow-goose-api-staging` service
3. Check if it's connected to the correct GitHub repository
4. Verify the build command: `pip install -r requirements.txt`
5. Verify the start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### Step 2: Manual Deploy
1. In the Render dashboard, click "Manual Deploy"
2. Select "Deploy latest commit"
3. Monitor the build logs for any errors

### Step 3: Environment Variables
Ensure these are set in Render:
```
DATABASE_URL=postgresql://final_goose_db_user:MII5440GTcgWHUGHCTWP2F0mo8SQ4Xg3@dpg-d2apq1h5pdvs73c2gbog-a/final_goose_db
SECRET_KEY=shadow-goose-secret-key-2025-staging
JWT_SECRET_KEY=shadow-goose-jwt-secret-2025-staging
CORS_ORIGINS=https://shadow-goose-web-staging.onrender.com
```

### Step 4: Test After Manual Deploy
```bash
# Test new endpoints
curl https://shadow-goose-api-staging.onrender.com/
curl https://shadow-goose-api-staging.onrender.com/debug
curl https://shadow-goose-api-staging.onrender.com/api/projects
```

## Alternative: Direct Code Update
If manual deploy doesn't work, we can:
1. Create a new service with the correct configuration
2. Update the environment variables directly
3. Test the database connection

## Current Status
- ✅ Code is refactored and working locally
- ✅ Dependencies are correct
- ❌ Render deployment is stuck
- 🔧 Manual intervention needed 