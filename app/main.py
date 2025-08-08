import os
import json
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
import jwt
from datetime import datetime, timedelta
from rules_engine import rules_engine, RuleType, ActionType, ConditionOperator

app = FastAPI(title="Shadow Goose API", version="4.3.0")

# Configuration
SECRET_KEY = os.getenv("SECRET_KEY", "shadow-goose-secret-key-2025-staging")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://final_goose_db_user:MII5440GTcgWHUGHCTWP2F0mo8SQ4Xg3@dpg-d2apq1h5pdvs73c2gbog-a/final_goose_db")

# Test user
TEST_USER = {
    "username": "test",
    "password": "test",
    "email": "test@shadow-goose.com",
    "role": "admin"
}

# Pydantic models
class LoginRequest(BaseModel):
    username: str
    password: str

class ProjectCreate(BaseModel):
    name: str
    description: str = ""
    status: str = "draft"
    amount: float = 0.0

class RuleCreate(BaseModel):
    name: str
    rule_type: str
    description: str = ""
    conditions: list
    actions: list

class RuleContext(BaseModel):
    context: dict
    rule_types: list = None

# Security
security = HTTPBearer()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage for testing (will be replaced with database)
projects_db = []
users_db = [{"id": 1, "username": "test", "email": "test@shadow-goose.com", "role": "admin"}]

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return username
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

def get_current_user(username: str = Depends(verify_token)):
    user = next((u for u in users_db if u["username"] == username), None)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.get("/")
def root():
    return {"message": "Shadow Goose API v4.3.0", "status": "running", "features": ["auth", "projects", "rules_engine"]}

@app.get("/health")
def health():
    return {"status": "ok", "version": "4.3.0"}

@app.get("/debug")
def debug():
    return {
        "version": "4.3.0",
        "database_url": "set" if DATABASE_URL != "not_set" else "not_set",
        "secret_key": "set" if os.getenv("SECRET_KEY") else "not_set",
        "features": ["in_memory_storage", "project_management", "user_management", "database_ready", "rules_engine"]
    }

@app.post("/auth/login")
def login(login_data: LoginRequest):
    if login_data.username == TEST_USER["username"] and login_data.password == TEST_USER["password"]:
        access_token = create_access_token(data={"sub": login_data.username})
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "id": 1,
                "username": TEST_USER["username"],
                "email": TEST_USER["email"],
                "role": TEST_USER["role"]
            }
        }
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")

@app.get("/auth/user")
def get_user_info(current_user = Depends(get_current_user)):
    return {
        "username": current_user["username"],
        "email": current_user["email"],
        "role": current_user["role"]
    }

@app.get("/api/projects")
def get_projects(current_user = Depends(get_current_user)):
    try:
        user_projects = [p for p in projects_db if p["created_by"] == current_user["id"]]
        return {"projects": user_projects}
    except Exception as e:
        return {"projects": [], "error": str(e)}

@app.post("/api/projects")
def create_project(project_data: ProjectCreate, current_user = Depends(get_current_user)):
    try:
        project = {
            "id": len(projects_db) + 1,
            "name": project_data.name,
            "description": project_data.description,
            "status": project_data.status,
            "amount": project_data.amount,
            "created_by": current_user["id"],
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat()
        }
        projects_db.append(project)
        
        # Process rules for project creation
        context = {
            "project_id": project["id"],
            "project_amount": project_data.amount,
            "user_role": current_user["role"],
            "project_status": project_data.status,
            "user_id": current_user["id"]
        }
        
        rule_results = rules_engine.process_rules(context, [RuleType.PROJECT_APPROVAL.value])
        
        return {
            "project": project,
            "rules_processed": rule_results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create project: {str(e)}")

@app.get("/api/database-status")
def database_status():
    return {
        "database_url_configured": DATABASE_URL != "not_set",
        "database_url_length": len(DATABASE_URL) if DATABASE_URL else 0,
        "ready_for_database_integration": True
    }

# Rules Engine API Endpoints
@app.get("/api/rules")
def get_rules(current_user = Depends(get_current_user)):
    """Get all rules"""
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    
    return {
        "rules": rules_engine.rules,
        "total_rules": len(rules_engine.rules)
    }

@app.post("/api/rules")
def create_rule(rule_data: RuleCreate, current_user = Depends(get_current_user)):
    """Create a new rule"""
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    
    rule = {
        "name": rule_data.name,
        "rule_type": rule_data.rule_type,
        "description": rule_data.description,
        "conditions": rule_data.conditions,
        "actions": rule_data.actions
    }
    
    success = rules_engine.add_rule(rule)
    if success:
        return {"message": "Rule created successfully", "rule": rule}
    else:
        raise HTTPException(status_code=400, detail="Failed to create rule")

@app.post("/api/rules/process")
def process_rules(context_data: RuleContext, current_user = Depends(get_current_user)):
    """Process rules against a context"""
    results = rules_engine.process_rules(context_data.context, context_data.rule_types)
    return {
        "results": results,
        "total_rules_processed": len(results)
    }

@app.get("/api/rules/types")
def get_rule_types():
    """Get available rule types"""
    return {
        "rule_types": [rule_type.value for rule_type in RuleType],
        "action_types": [action_type.value for action_type in ActionType],
        "condition_operators": [op.value for op in ConditionOperator]
    }

@app.get("/api/rules/examples")
def get_rule_examples():
    """Get example rules"""
    return {
        "examples": rules_engine.get_default_rules()
    }

@app.post("/api/rules/test")
def test_rule(rule_data: RuleCreate, context_data: RuleContext):
    """Test a rule against a context"""
    # Create a temporary rules engine for testing
    test_engine = rules_engine.__class__()
    test_engine.add_rule({
        "name": rule_data.name,
        "rule_type": rule_data.rule_type,
        "description": rule_data.description,
        "conditions": rule_data.conditions,
        "actions": rule_data.actions
    })
    
    results = test_engine.process_rules(context_data.context)
    return {
        "rule_tested": rule_data.name,
        "context": context_data.context,
        "results": results
    } 