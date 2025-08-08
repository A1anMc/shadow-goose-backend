import os
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# Database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://final_goose_db_user:MII5440GTcgWHUGHCTWP2F0mo8SQ4Xg3@dpg-d2apq1h5pdvs73c2gbog-a/final_goose_db")

# Create engine
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

# Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# User model
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    role = Column(String, default="user")  # admin, manager, user
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)

# Project model
class Project(Base):
    __tablename__ = "projects"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(Text)
    status = Column(String, default="draft")  # draft, active, completed, archived
    created_by = Column(Integer)  # user_id
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# Grant model
class Grant(Base):
    __tablename__ = "grants"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, index=True)
    name = Column(String, index=True)
    amount = Column(Integer)  # in cents
    status = Column(String, default="draft")  # draft, submitted, approved, rejected
    submission_date = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# Create tables
def create_tables():
    Base.metadata.create_all(bind=engine) 