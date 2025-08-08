#!/usr/bin/env python3

import os
import sys
import requests
import json

def check_deployment():
    print("=== Shadow Goose Deployment Diagnosis ===")
    
    # Check 1: Current deployment version
    try:
        response = requests.get("https://shadow-goose-api-staging.onrender.com/health", timeout=10)
        print(f"✅ Health endpoint: {response.status_code}")
        print(f"   Response: {response.text}")
    except Exception as e:
        print(f"❌ Health endpoint failed: {e}")
    
    # Check 2: New endpoints
    try:
        response = requests.get("https://shadow-goose-api-staging.onrender.com/", timeout=10)
        print(f"✅ Root endpoint: {response.status_code}")
        print(f"   Response: {response.text}")
    except Exception as e:
        print(f"❌ Root endpoint failed: {e}")
    
    # Check 3: Frontend
    try:
        response = requests.get("https://shadow-goose-web-staging.onrender.com", timeout=10)
        print(f"✅ Frontend: {response.status_code}")
    except Exception as e:
        print(f"❌ Frontend failed: {e}")
    
    # Check 4: Environment variables (if we can access them)
    print("\n=== Environment Analysis ===")
    print("DATABASE_URL set:", "yes" if os.getenv("DATABASE_URL") else "no")
    print("SECRET_KEY set:", "yes" if os.getenv("SECRET_KEY") else "no")
    
    print("\n=== Diagnosis Complete ===")
    print("If new endpoints are not available, the deployment needs to be manually triggered.")

if __name__ == "__main__":
    check_deployment() 