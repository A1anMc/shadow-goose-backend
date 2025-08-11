# Shadow Goose Entertainment - Development Guide

## Project Overview

**Client:** Shadow Goose Entertainment
**Platform:** NavImpact (White-label Grant Management)
**Environment:** Staging & Production
**API Version:** 4.0.0

## Architecture

### Backend (FastAPI)
- **Language:** Python 3.9+
- **Framework:** FastAPI
- **Database:** PostgreSQL (planned), In-memory (current)
- **Authentication:** JWT Bearer Tokens
- **Deployment:** Render

### Frontend (Next.js)
- **Language:** TypeScript
- **Framework:** Next.js
- **Styling:** Tailwind CSS
- **Branding:** Shadow Goose Entertainment
- **Deployment:** Render

## Development Setup

### Prerequisites
- Python 3.9+
- Node.js 18+
- Git
- PostgreSQL (for database integration)

### Backend Setup
```bash
# Clone repository
git clone https://github.com/A1anMc/shadow-goose-backend.git
cd shadow-goose-backend

# Install dependencies
pip install -r requirements.txt

# Run locally
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Setup
```bash
# Clone repository
git clone https://github.com/A1anMc/shadow-goose-frontend.git
cd shadow-goose-frontend

# Install dependencies
npm install

# Run locally
npm run dev
```

## Environment Variables

### Backend (.env)
```bash
DATABASE_URL=postgresql://user:password@host/database
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret
CORS_ORIGINS=["http://localhost:3000"]
```

### Frontend (.env.local)
```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_CLIENT=shadow-goose
NEXT_PUBLIC_APP_NAME=Shadow Goose Entertainment
```

## API Development

### Adding New Endpoints

1. **Create Pydantic Model:**
```python
class NewResource(BaseModel):
    name: str
    description: str = ""
```

2. **Add Endpoint:**
```python
@app.post("/api/new-resource")
def create_new_resource(data: NewResource, current_user = Depends(get_current_user)):
    # Implementation
    return {"message": "Created"}
```

3. **Add Documentation:**
- Update API_DOCUMENTATION.md
- Add to API_RULES.md
- Include in testing

### Authentication Flow

1. **Login:** `POST /auth/login`
2. **Get Token:** Extract from response
3. **Use Token:** Include in Authorization header
4. **Validate:** Server validates on each request

### Error Handling

```python
from fastapi import HTTPException

# Raise specific errors
raise HTTPException(status_code=404, detail="Resource not found")
```

## Frontend Development

### Adding New Pages

1. **Create Page:** `pages/new-page.tsx`
2. **Add Routing:** Next.js auto-routing
3. **Add Navigation:** Update sidebar/menu
4. **Add Styling:** Use Tailwind classes

### API Integration

```typescript
// Example API call
const response = await fetch('/api/projects', {
  headers: {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json',
  },
});
```

### Branding Integration

```typescript
import { getBranding } from '../src/lib/branding';

const branding = getBranding();
// Use branding.colors, branding.name, etc.
```

## Testing

### Backend Testing
```bash
# Run tests
pytest

# Test specific endpoint
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"test","password":"test"}'
```

### Frontend Testing
```bash
# Run tests
npm test

# Test build
npm run build
```

## Deployment

### Staging Deployment
- **Backend:** `https://shadow-goose-api-staging.onrender.com`
- **Frontend:** `https://shadow-goose-web-staging.onrender.com`
- **Auto-deploy:** On push to main branch

### Production Deployment
- **Backend:** `https://shadow-goose-api.onrender.com`
- **Frontend:** `https://shadow-goose-web.onrender.com`
- **Manual deployment:** Triggered from staging

## Database Integration

### Current Status
- Using in-memory storage
- PostgreSQL connection ready
- Database models defined

### Migration Steps
1. Set DATABASE_URL environment variable
2. Update main.py to use database
3. Test database connection
4. Migrate existing data

## Monitoring & Logging

### Health Checks
- **Backend:** `GET /health`
- **Frontend:** `GET /api/health`
- **Monitor:** Response time < 100ms

### Error Tracking
- Log all API errors
- Track 4xx and 5xx responses
- Monitor authentication failures

## Security Guidelines

### Authentication
- Always validate JWT tokens
- Check user permissions
- Sanitize user inputs
- Use HTTPS in production

### Data Protection
- Encrypt sensitive data
- Validate all inputs
- Implement rate limiting
- Follow OWASP guidelines

## Performance Optimization

### Backend
- Use async/await for I/O operations
- Implement caching where appropriate
- Optimize database queries
- Monitor response times

### Frontend
- Optimize bundle size
- Use code splitting
- Implement lazy loading
- Cache API responses

## Code Standards

### Python (Backend)
- Follow PEP 8
- Use type hints
- Add docstrings
- Write unit tests

### TypeScript (Frontend)
- Use strict mode
- Add proper types
- Follow ESLint rules
- Write component tests

## Git Workflow

### Branch Strategy
- `main`: Production-ready code
- `develop`: Development branch
- `feature/*`: Feature branches
- `hotfix/*`: Emergency fixes

### Commit Messages
```
feat: add new project creation endpoint
fix: resolve authentication token issue
docs: update API documentation
test: add integration tests for projects
```

## Troubleshooting

### Common Issues

1. **Deployment Not Updating**
   - Check Render dashboard
   - Verify GitHub connection
   - Check build logs

2. **Authentication Failing**
   - Verify JWT token format
   - Check token expiration
   - Validate user credentials

3. **Database Connection Issues**
   - Check DATABASE_URL format
   - Verify PostgreSQL access
   - Test connection locally

### Debug Commands

```bash
# Check API health
curl https://shadow-goose-api-staging.onrender.com/health

# Test authentication
curl -X POST https://shadow-goose-api-staging.onrender.com/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"test","password":"test"}'

# Check frontend
curl https://shadow-goose-web-staging.onrender.com
```

## Resources

### Documentation
- [API Documentation](./API_DOCUMENTATION.md)
- [API Rules](./API_RULES.md)
- [UAT Checklist](./UAT_CHECKLIST.md)
- [Branding Implementation](./BRANDING_IMPLEMENTATION.md)

### External Links
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Next.js Documentation](https://nextjs.org/docs)
- [Tailwind CSS](https://tailwindcss.com/)
- [Render Dashboard](https://dashboard.render.com/)

### Team Contacts
- **Project Manager:** Alan McCarthy (alanmccarthy00@gmail.com)
- **Technical Lead:** Alan McCarthy
- **UAT Coordinator:** Alan McCarthy

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 4.0.0 | 2025-08-08 | Initial API with authentication and projects |
| 3.0.0 | 2025-08-08 | Refactored to in-memory storage |
| 2.0.0 | 2025-08-08 | Added database integration |
| 1.0.0 | 2025-08-08 | Basic authentication setup |
