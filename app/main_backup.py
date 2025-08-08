import os, json
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
import jwt
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from database import get_db, create_tables, User, Project, Grant

app = FastAPI(title="Shadow Goose API", version="2.0.0")

# Simple authentication
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Test user credentials
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

class UserInfo(BaseModel):
    username: str
    email: str
    role: str

class ProjectCreate(BaseModel):
    name: str
    description: str = ""
    status: str = "draft"

class ProjectResponse(BaseModel):
    id: int
    name: str
    description: str
    status: str
    created_by: int
    created_at: datetime
    updated_at: datetime

# Security
security = HTTPBearer()

origins = []
cors = os.getenv("CORS_ORIGINS", "")
if cors:
    try:
        origins = json.loads(cors)
    except Exception:
        origins = [o.strip() for o in cors.split(",") if o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins or ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create database tables on startup
@app.on_event("startup")
async def startup_event():
    create_tables()

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

def get_current_user(username: str = Depends(verify_token), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.get("/")
def root():
    return {"message": "Shadow Goose API v2.0.0", "status": "running"}

@app.get("/health")
def health():
    return {"status": "ok", "version": "2.0.0"}

@app.get("/debug")
def debug():
    return {
        "version": "2.0.0",
        "database_url": os.getenv("DATABASE_URL", "not_set"),
        "secret_key": "set" if os.getenv("SECRET_KEY") else "not_set",
        "features": ["database_integration", "project_management", "user_management"]
    }

@app.post("/auth/login")
def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    # Check if user exists in database
    user = db.query(User).filter(User.username == login_data.username).first()
    
    if not user:
        # Create test user if it doesn't exist
        if login_data.username == TEST_USER["username"] and login_data.password == TEST_USER["password"]:
            user = User(
                username=TEST_USER["username"],
                email=TEST_USER["email"],
                role=TEST_USER["role"]
            )
            db.add(user)
            db.commit()
            db.refresh(user)
        else:
            raise HTTPException(status_code=401, detail="Invalid credentials")
    
    access_token = create_access_token(data={"sub": user.username})
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": user.role
        }
    }

@app.get("/auth/user")
def get_user_info(current_user: User = Depends(get_current_user)):
    return UserInfo(
        username=current_user.username,
        email=current_user.email,
        role=current_user.role
    )

@app.post("/auth/logout")
def logout():
    return {"message": "Logged out successfully"}

@app.get("/api/projects")
def get_projects(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    projects = db.query(Project).filter(Project.created_by == current_user.id).all()
    return {
        "projects": [
            {
                "id": project.id,
                "name": project.name,
                "description": project.description,
                "status": project.status,
                "created_at": project.created_at,
                "updated_at": project.updated_at
            }
            for project in projects
        ]
    }

@app.post("/api/projects")
def create_project(project_data: ProjectCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    project = Project(
        name=project_data.name,
        description=project_data.description,
        status=project_data.status,
        created_by=current_user.id
    )
    db.add(project)
    db.commit()
    db.refresh(project)
    
    return {
        "id": project.id,
        "name": project.name,
        "description": project.description,
        "status": project.status,
        "created_by": project.created_by,
        "created_at": project.created_at,
        "updated_at": project.updated_at
    }

@app.get("/api/projects/{project_id}")
def get_project(project_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id, Project.created_by == current_user.id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    return {
        "id": project.id,
        "name": project.name,
        "description": project.description,
        "status": project.status,
        "created_by": project.created_by,
        "created_at": project.created_at,
        "updated_at": project.updated_at
    }

@app.put("/api/projects/{project_id}")
def update_project(project_id: int, project_data: ProjectCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id, Project.created_by == current_user.id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    project.name = project_data.name
    project.description = project_data.description
    project.status = project_data.status
    project.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(project)
    
    return {
        "id": project.id,
        "name": project.name,
        "description": project.description,
        "status": project.status,
        "created_by": project.created_by,
        "created_at": project.created_at,
        "updated_at": project.updated_at
    }

@app.delete("/api/projects/{project_id}")
def delete_project(project_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id, Project.created_by == current_user.id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    db.delete(project)
    db.commit()
    
    return {"message": "Project deleted successfully"}
