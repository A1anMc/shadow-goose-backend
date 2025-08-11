import os
import json
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
import jwt
from datetime import datetime, timedelta

app = FastAPI(title="Shadow Goose API", version="4.0.0")

# Configuration
SECRET_KEY = os.getenv("SECRET_KEY", "shadow-goose-secret-key-2025-staging")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Test user
TEST_USER = {
    "username": "test",
    "password": "test",
    "email": "test@shadow-goose.com",
    "role": "admin",
}


# Pydantic models
class LoginRequest(BaseModel):
    username: str
    password: str


class ProjectCreate(BaseModel):
    name: str
    description: str = ""
    status: str = "draft"


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
users_db = [
    {"id": 1, "username": "test", "email": "test@shadow-goose.com", "role": "admin"}
]


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = jwt.decode(
            credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM]
        )
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
    return {
        "message": "Shadow Goose API v4.0.0",
        "status": "running",
        "features": ["auth", "projects"],
    }


@app.get("/health")
def health():
    return {"status": "ok", "version": "4.0.0"}


@app.get("/debug")
def debug():
    return {
        "version": "4.0.0",
        "database_url": os.getenv("DATABASE_URL", "not_set"),
        "secret_key": "set" if os.getenv("SECRET_KEY") else "not_set",
        "features": ["in_memory_storage", "project_management", "user_management"],
    }


@app.post("/auth/login")
def login(login_data: LoginRequest):
    if (
        login_data.username == TEST_USER["username"]
        and login_data.password == TEST_USER["password"]
    ):
        access_token = create_access_token(data={"sub": login_data.username})
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "id": 1,
                "username": TEST_USER["username"],
                "email": TEST_USER["email"],
                "role": TEST_USER["role"],
            },
        }
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")


@app.get("/auth/user")
def get_user_info(current_user=Depends(get_current_user)):
    return {
        "username": current_user["username"],
        "email": current_user["email"],
        "role": current_user["role"],
    }


@app.get("/api/projects")
def get_projects(current_user=Depends(get_current_user)):
    user_projects = [p for p in projects_db if p["created_by"] == current_user["id"]]
    return {"projects": user_projects}


@app.post("/api/projects")
def create_project(project_data: ProjectCreate, current_user=Depends(get_current_user)):
    project = {
        "id": len(projects_db) + 1,
        "name": project_data.name,
        "description": project_data.description,
        "status": project_data.status,
        "created_by": current_user["id"],
        "created_at": datetime.utcnow().isoformat(),
        "updated_at": datetime.utcnow().isoformat(),
    }
    projects_db.append(project)
    return project
