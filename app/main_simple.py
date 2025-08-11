import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Shadow Goose API", version="3.0.0")

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "Shadow Goose API v3.0.0", "status": "running"}


@app.get("/health")
def health():
    return {"status": "ok", "version": "3.0.0"}


@app.get("/test")
def test():
    return {
        "message": "Database integration test",
        "database_url": os.getenv("DATABASE_URL", "not_set"),
    }


@app.post("/auth/login")
def login():
    return {
        "access_token": "test-token",
        "token_type": "bearer",
        "user": {
            "id": 1,
            "username": "test",
            "email": "test@shadow-goose.com",
            "role": "admin",
        },
    }
