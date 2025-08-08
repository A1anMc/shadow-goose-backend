#!/bin/bash

echo "=== Shadow Goose Deployment Test ==="

# Test 1: Check current deployment
echo "1. Testing current deployment..."
curl -s https://shadow-goose-api-staging.onrender.com/health

# Test 2: Check if new endpoints are available
echo -e "\n2. Testing new endpoints..."
curl -s https://shadow-goose-api-staging.onrender.com/ || echo "Root endpoint not available"
curl -s https://shadow-goose-api-staging.onrender.com/test || echo "Test endpoint not available"

# Test 3: Check frontend
echo -e "\n3. Testing frontend..."
curl -s -o /dev/null -w "Frontend Status: %{http_code}\n" https://shadow-goose-web-staging.onrender.com

# Test 4: Check if deployment is stuck
echo -e "\n4. Checking deployment status..."
echo "If endpoints are not available, deployment may be stuck or failed"

echo -e "\n=== Deployment Test Complete ===" 