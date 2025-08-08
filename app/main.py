import os, json
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
import jwt
from datetime import datetime, timedelta

app = FastAPI()

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

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/auth/login")
def login(login_data: LoginRequest):
    if login_data.username == TEST_USER["username"] and login_data.password == TEST_USER["password"]:
        access_token = create_access_token(data={"sub": login_data.username})
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "username": TEST_USER["username"],
                "email": TEST_USER["email"],
                "role": TEST_USER["role"]
            }
        }
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")

@app.get("/auth/user")
def get_user_info(username: str = Depends(verify_token)):
    if username == TEST_USER["username"]:
        return UserInfo(
            username=TEST_USER["username"],
            email=TEST_USER["email"],
            role=TEST_USER["role"]
        )
    else:
        raise HTTPException(status_code=404, detail="User not found")

@app.post("/auth/logout")
def logout():
    # For simple auth, we just return success
    # In production, you'd invalidate the token
    return {"message": "Logged out successfully"}

@app.get("/api/projects")
def get_projects(username: str = Depends(verify_token)):
    # Mock projects for testing
    return {
        "projects": [
            {
                "id": 1,
                "name": "Shadow Goose Entertainment Launch",
                "status": "active",
                "created_at": "2025-01-15T10:00:00Z"
            },
            {
                "id": 2,
                "name": "Grant Application 2025",
                "status": "draft",
                "created_at": "2025-01-10T14:30:00Z"
            }
        ]
    }
