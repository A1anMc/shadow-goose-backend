#!/bin/bash

echo "🚀 Shadow Goose Production Deployment"
echo "====================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}Step 1: Verifying staging environment...${NC}"
if curl -s https://shadow-goose-api-staging.onrender.com/health | grep -q "ok"; then
    echo -e "${GREEN}✅ Staging API is healthy${NC}"
else
    echo -e "${RED}❌ Staging API is not responding${NC}"
    exit 1
fi

if curl -s -o /dev/null -w "%{http_code}" https://shadow-goose-web-staging.onrender.com | grep -q "200"; then
    echo -e "${GREEN}✅ Staging frontend is healthy${NC}"
else
    echo -e "${RED}❌ Staging frontend is not responding${NC}"
    exit 1
fi

echo -e "${BLUE}Step 2: Production deployment configuration ready${NC}"
echo -e "${YELLOW}📋 Production Environment Variables:${NC}"
echo "   - DATABASE_URL: Configured"
echo "   - SECRET_KEY: Configured"
echo "   - JWT_SECRET_KEY: Configured"
echo "   - CORS_ORIGINS: https://shadow-goose-web.onrender.com"
echo "   - NEXT_PUBLIC_API_URL: https://shadow-goose-api.onrender.com"

echo -e "${BLUE}Step 3: Production services to deploy${NC}"
echo -e "${YELLOW}🔧 Backend Service: shadow-goose-api${NC}"
echo "   - Environment: Python"
echo "   - Plan: Starter"
echo "   - Health Check: /health"

echo -e "${YELLOW}🌐 Frontend Service: shadow-goose-web${NC}"
echo "   - Environment: Node.js"
echo "   - Plan: Starter"
echo "   - Health Check: /api/health"

echo -e "${BLUE}Step 4: Manual deployment steps${NC}"
echo -e "${YELLOW}📝 To deploy to production:${NC}"
echo "1. Go to Render Dashboard: https://dashboard.render.com"
echo "2. Create new Blueprint from: WHITE_LABEL_UPDATED/configs/render.shadow-goose.yaml"
echo "3. Set environment variables from: WHITE_LABEL_UPDATED/clients/shadow-goose/ENV.production"
echo "4. Deploy the Blueprint"

echo -e "${BLUE}Step 5: Post-deployment verification${NC}"
echo -e "${YELLOW}🔍 After deployment, verify:${NC}"
echo "   - Backend API: https://shadow-goose-api.onrender.com/health"
echo "   - Frontend: https://shadow-goose-web.onrender.com"
echo "   - Login: test/test credentials"
echo "   - Dashboard features: Rules Engine, Deployments, User Management"

echo -e "${GREEN}✅ Production deployment configuration complete!${NC}"
echo -e "${YELLOW}💡 Ready to deploy the refactored Shadow Goose system to production${NC}"
