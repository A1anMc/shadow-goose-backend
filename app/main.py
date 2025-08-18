import os
from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
import jwt
from .rules_engine import rules_engine, RuleType, ActionType, ConditionOperator
from .grants import (
    grant_service,
    Grant,
    GrantApplication,
    GrantAnswer,
    GrantComment,
    GrantStatus,
    GrantPriority,
    GrantCategory,
)
from .api_grants_endpoints import router as grants_router
import logging
import time
import psutil
from datetime import datetime, timedelta

# Configure logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
app = FastAPI(title="Shadow Goose API", version="4.5.0")

# Include routers
app.include_router(grants_router, prefix="/api", tags=["grants"])

# Configuration
ACCESS_TOKEN_EXPIRE_MINUTES = 30
ALGORITHM = "HS256"
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-here")
DATABASE_URL = os.getenv("DATABASE_URL", "not_set")

# Test user for development
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


class DeploymentRequest(BaseModel):
    environment: str
    branch_name: str
    commit_message: str
    deployment_id: str = None
    priority: str = "normal"
    security_scan_status: str = "pending"


class CommitRequest(BaseModel):
    branch_name: str
    commit_message: str
    pr_id: str = None
    files_changed: list = []


# Grant-related models


class GrantSearchRequest(BaseModel):
    category: str = None
    min_amount: float = None
    max_amount: float = None
    deadline_before: str = None
    keywords: str = None


class GrantApplicationCreate(BaseModel):
    grant_id: str
    title: str
    assigned_to: str
    collaborators: list = []


class GrantAnswerUpdate(BaseModel):
    question: str
    answer: str


class GrantCommentCreate(BaseModel):
    content: str


class UserProfile(BaseModel):
    preferred_categories: list = []
    min_amount: float = None
    max_amount: float = None
    focus_areas: list = []


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
deployments_db = []
commits_db = []


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
    for user in users_db:
        if user["username"] == username:
            return user
    raise HTTPException(status_code=401, detail="User not found")


# Add comprehensive health check endpoint and advanced monitoring
@app.get("/health")
async def health_check():
    """Comprehensive health check endpoint with dependency monitoring"""
    start_time = time.time()

    health_status = {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "4.5.0",
        "environment": os.getenv("ENVIRONMENT", "development"),
        "checks": {
            "api": "healthy",
            "grants_service": "healthy",
            "rules_engine": "healthy",
            "authentication": "healthy",
        },
        "dependencies": {},
        "performance": {"response_time_ms": 0},
    }

    # Check grants service
    try:
        grants = grant_service.get_all_grants()
        health_status["checks"]["grants_service"] = "healthy"
        health_status["dependencies"]["grants_count"] = len(grants)
    except Exception as e:
        health_status["checks"]["grants_service"] = "unhealthy"
        health_status["dependencies"]["grants_error"] = str(e)
        health_status["status"] = "degraded"

    # Check rules engine
    try:
        rules = rules_engine.get_all_rules()
        health_status["checks"]["rules_engine"] = "healthy"
        health_status["dependencies"]["rules_count"] = len(rules)
    except Exception as e:
        health_status["checks"]["rules_engine"] = "unhealthy"
        health_status["dependencies"]["rules_error"] = str(e)
        health_status["status"] = "degraded"

    # Check authentication system
    try:
        # Test JWT token creation
        test_token = create_access_token({"sub": "health_check"})
        health_status["checks"]["authentication"] = "healthy"
    except Exception as e:
        health_status["checks"]["authentication"] = "unhealthy"
        health_status["dependencies"]["auth_error"] = str(e)
        health_status["status"] = "degraded"

    # Calculate response time
    response_time = (time.time() - start_time) * 1000
    health_status["performance"]["response_time_ms"] = round(response_time, 2)

    # Log health check
    logger.info(
        "Health check completed",
        extra={
            "health_status": health_status["status"],
            "response_time_ms": response_time,
            "checks_passed": sum(
                1 for check in health_status["checks"].values() if check == "healthy"
            ),
            "total_checks": len(health_status["checks"]),
        },
    )

    # Return appropriate status code
    status_code = 200 if health_status["status"] == "healthy" else 503
    return health_status


@app.get("/metrics")
async def get_metrics():
    """Application metrics endpoint for monitoring"""
    metrics = {
        "timestamp": datetime.utcnow().isoformat(),
        "application": {
            "version": "4.5.0",
            "uptime_seconds": (
                time.time() - app.start_time if hasattr(app, "start_time") else 0
            ),
            "requests_processed": getattr(app, "request_count", 0),
        },
        "system": {
            "cpu_percent": psutil.cpu_percent(interval=1),
            "memory_percent": psutil.virtual_memory().percent,
            "disk_percent": psutil.disk_usage("/").percent,
        },
        "business": {
            "total_grants": len(grant_service.get_all_grants()),
            "total_applications": len(grant_service.get_all_applications()),
            "total_users": len(users_db),
            "total_projects": len(projects_db),
        },
    }

    logger.info("Metrics collected", extra=metrics)
    return metrics


# Add request counting middleware
@app.middleware("http")
async def add_request_count(request: Request, call_next):
    """Middleware to track request counts and performance"""
    start_time = time.time()

    # Increment request counter
    if not hasattr(app, "request_count"):
        app.request_count = 0
    app.request_count += 1

    # Process request
    response = await call_next(request)

    # Calculate response time
    process_time = time.time() - start_time

    # Log request details
    logger.info(
        "Request processed",
        extra={
            "method": request.method,
            "path": request.url.path,
            "status_code": response.status_code,
            "response_time_ms": round(process_time * 1000, 2),
            "user_agent": request.headers.get("user-agent", "unknown"),
        },
    )

    # Add response time header
    response.headers["X-Response-Time"] = str(process_time)

    return response


# Add startup event to initialize monitoring
@app.on_event("startup")
async def startup_event():
    """Initialize application on startup"""
    app.start_time = time.time()
    app.request_count = 0

    logger.info(
        "Application started",
        extra={
            "version": "4.5.0",
            "environment": os.getenv("ENVIRONMENT", "development"),
            "startup_time": app.start_time,
        },
    )

    # Initialize health check data
    logger.info("Health monitoring initialized")


@app.get("/")
def root():
    return {
        "message": "Shadow Goose API v4.5.0",
        "status": "running",
        "features": ["auth", "projects", "rules_engine", "deployment_workflows"],
    }


@app.get("/debug")
def debug():
    return {
        "version": "4.5.0",
        "database_url": "set" if DATABASE_URL != "not_set" else "not_set",
        "secret_key": "set" if os.getenv("SECRET_KEY") else "not_set",
        "features": [
            "in_memory_storage",
            "project_management",
            "user_management",
            "database_ready",
            "rules_engine",
            "deployment_workflows",
        ],
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
    try:
        user_projects = [
            p for p in projects_db if p["created_by"] == current_user["id"]
        ]
        return {"projects": user_projects}
    except Exception as e:
        return {"projects": [], "error": str(e)}


@app.post("/api/projects")
def create_project(project_data: ProjectCreate, current_user=Depends(get_current_user)):
    try:
        project = {
            "id": len(projects_db) + 1,
            "name": project_data.name,
            "description": project_data.description,
            "status": project_data.status,
            "amount": project_data.amount,
            "created_by": current_user["id"],
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
        }
        projects_db.append(project)

        # Process rules for project creation
        context = {
            "project_id": project["id"],
            "project_amount": project_data.amount,
            "user_role": current_user["role"],
            "project_status": project_data.status,
            "user_id": current_user["id"],
        }

        rule_results = rules_engine.process_rules(
            context, [RuleType.PROJECT_APPROVAL.value]
        )

        return {"project": project, "rules_processed": rule_results}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to create project: {str(e)}"
        )


@app.get("/api/database-status")
def database_status():
    return {
        "database_url_configured": DATABASE_URL != "not_set",
        "database_url_length": len(DATABASE_URL) if DATABASE_URL else 0,
        "ready_for_database_integration": True,
    }


# Deployment Workflow API Endpoints
@app.post("/api/deployments")
def create_deployment(
    deployment_data: DeploymentRequest, current_user=Depends(get_current_user)
):
    """Create a new deployment and process deployment rules"""
    try:
        deployment = {
            "id": len(deployments_db) + 1,
            "environment": deployment_data.environment,
            "branch_name": deployment_data.branch_name,
            "commit_message": deployment_data.commit_message,
            "user_role": current_user["role"],
            "deployment_id": deployment_data.deployment_id
            or f"deploy-{len(deployments_db) + 1}",
            "priority": deployment_data.priority,
            "security_scan_status": deployment_data.security_scan_status,
            "status": "pending",
            "created_by": current_user["id"],
            "created_at": datetime.utcnow().isoformat(),
        }
        deployments_db.append(deployment)

        # Process deployment rules
        context = {
            "deployment_environment": deployment_data.environment,
            "branch_name": deployment_data.branch_name,
            "commit_message": deployment_data.commit_message,
            "user_role": current_user["role"],
            "deployment_id": deployment["deployment_id"],
            "priority": deployment_data.priority,
            "security_scan_status": deployment_data.security_scan_status,
            "deployment_status": "pending",
        }

        rule_results = rules_engine.process_rules(context, [RuleType.WORKFLOW.value])

        return {"deployment": deployment, "rules_processed": rule_results}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to create deployment: {str(e)}"
        )


@app.get("/api/deployments")
def get_deployments(current_user=Depends(get_current_user)):
    """Get all deployments"""
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")

    return {"deployments": deployments_db, "total_deployments": len(deployments_db)}


@app.post("/api/deployments/{deployment_id}/status")
def update_deployment_status(
    deployment_id: str, status: str, current_user=Depends(get_current_user)
):
    """Update deployment status and trigger health check rules"""
    try:
        deployment = next(
            (d for d in deployments_db if d["deployment_id"] == deployment_id), None
        )
        if not deployment:
            raise HTTPException(status_code=404, detail="Deployment not found")

        deployment["status"] = status
        deployment["updated_at"] = datetime.utcnow().isoformat()

        # Process health check rules
        context = {
            "deployment_environment": deployment["environment"],
            "deployment_status": status,
            "deployment_id": deployment_id,
            "user_role": current_user["role"],
        }

        rule_results = rules_engine.process_rules(context, [RuleType.WORKFLOW.value])

        return {"deployment": deployment, "rules_processed": rule_results}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to update deployment: {str(e)}"
        )


# Commit Workflow API Endpoints
@app.post("/api/commits")
def create_commit(commit_data: CommitRequest, current_user=Depends(get_current_user)):
    """Create a new commit and process commit rules"""
    try:
        commit = {
            "id": len(commits_db) + 1,
            "branch_name": commit_data.branch_name,
            "commit_message": commit_data.commit_message,
            "user_role": current_user["role"],
            "pr_id": commit_data.pr_id,
            "files_changed": commit_data.files_changed,
            "status": "pending",
            "created_by": current_user["id"],
            "created_at": datetime.utcnow().isoformat(),
        }
        commits_db.append(commit)

        # Process commit rules
        context = {
            "branch_name": commit_data.branch_name,
            "commit_message": commit_data.commit_message,
            "user_role": current_user["role"],
            "pr_id": commit_data.pr_id,
            "files_changed": commit_data.files_changed,
        }

        rule_results = rules_engine.process_rules(context, [RuleType.WORKFLOW.value])

        return {"commit": commit, "rules_processed": rule_results}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to create commit: {str(e)}"
        )


@app.get("/api/commits")
def get_commits(current_user=Depends(get_current_user)):
    """Get all commits"""
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")

    return {"commits": commits_db, "total_commits": len(commits_db)}


# Rules Engine API Endpoints
@app.get("/api/rules")
def get_rules(current_user=Depends(get_current_user)):
    """Get all rules"""
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")

    return {"rules": rules_engine.rules, "total_rules": len(rules_engine.rules)}


@app.post("/api/rules")
def create_rule(rule_data: RuleCreate, current_user=Depends(get_current_user)):
    """Create a new rule"""
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")

    rule = {
        "name": rule_data.name,
        "rule_type": rule_data.rule_type,
        "description": rule_data.description,
        "conditions": rule_data.conditions,
        "actions": rule_data.actions,
    }

    success = rules_engine.add_rule(rule)
    if success:
        return {"message": "Rule created successfully", "rule": rule}
    else:
        raise HTTPException(status_code=400, detail="Failed to create rule")


@app.post("/api/rules/process")
def process_rules(context_data: RuleContext, current_user=Depends(get_current_user)):
    """Process rules against a context"""
    results = rules_engine.process_rules(context_data.context, context_data.rule_types)
    return {"results": results, "total_rules_processed": len(results)}


@app.get("/api/rules/types")
def get_rule_types():
    """Get available rule types"""
    return {
        "rule_types": [rule_type.value for rule_type in RuleType],
        "action_types": [action_type.value for action_type in ActionType],
        "condition_operators": [op.value for op in ConditionOperator],
    }


@app.get("/api/rules/examples")
def get_rule_examples():
    """Get example rules"""
    return {"examples": rules_engine.get_default_rules()}


@app.post("/api/rules/test")
def test_rule(rule_data: RuleCreate, context_data: RuleContext):
    """Test a rule against a context"""
    # Create a temporary rules engine for testing
    test_engine = rules_engine.__class__()
    test_engine.add_rule(
        {
            "name": rule_data.name,
            "rule_type": rule_data.rule_type,
            "description": rule_data.description,
            "conditions": rule_data.conditions,
            "actions": rule_data.actions,
        }
    )

    results = test_engine.process_rules(context_data.context)
    return {
        "rule_tested": rule_data.name,
        "context": context_data.context,
        "results": results,
    }


# Grant Management API Endpoints
@app.get("/api/grants")
def get_grants(current_user=Depends(get_current_user)):
    """Get all available grants"""
    try:
        grants = grant_service.get_all_grants()
        return {
            "grants": [grant.dict() for grant in grants],
            "total_grants": len(grants),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch grants: {str(e)}")


@app.get("/api/grants/{grant_id}")
def get_grant(grant_id: str, current_user=Depends(get_current_user)):
    """Get a specific grant by ID"""
    try:
        grant = grant_service.get_grant_by_id(grant_id)
        if not grant:
            raise HTTPException(status_code=404, detail="Grant not found")
        return grant.dict()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch grant: {str(e)}")


@app.post("/api/grants/search")
def search_grants(
    search_request: GrantSearchRequest, current_user=Depends(get_current_user)
):
    """Search grants with filters"""
    try:
        grants = grant_service.search_grants(
            category=(
                GrantCategory(search_request.category)
                if search_request.category
                else None
            ),
            min_amount=search_request.min_amount,
            max_amount=search_request.max_amount,
            deadline_before=(
                datetime.fromisoformat(search_request.deadline_before)
                if search_request.deadline_before
                else None
            ),
            keywords=search_request.keywords,
        )
        return {
            "grants": [grant.dict() for grant in grants],
            "total_results": len(grants),
            "filters_applied": search_request.dict(),
        }
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to search grants: {str(e)}"
        )


@app.post("/api/grants/recommendations")
def get_grant_recommendations(
    user_profile: UserProfile, current_user=Depends(get_current_user)
):
    """Get AI-recommended grants based on user profile"""
    try:
        profile_dict = user_profile.dict()
        recommendations = grant_service.get_recommended_grants(profile_dict)
        return {
            "recommendations": [grant.dict() for grant in recommendations],
            "total_recommendations": len(recommendations),
            "user_profile": profile_dict,
        }
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to get recommendations: {str(e)}"
        )


@app.get("/api/grants/categories")
def get_grant_categories():
    """Get all available grant categories"""
    return {
        "categories": [category.value for category in GrantCategory],
        "category_descriptions": {
            "arts_culture": "Arts and cultural projects",
            "community": "Community development and social impact",
            "education": "Educational programs and initiatives",
            "environment": "Environmental and sustainability projects",
            "health": "Health and wellbeing programs",
            "technology": "Technology and innovation projects",
            "youth": "Youth-focused initiatives",
            "indigenous": "Indigenous community projects",
            "disability": "Disability support and inclusion",
            "other": "Other project types",
        },
    }


# Grant Applications API Endpoints
@app.get("/api/grant-applications")
def get_grant_applications(current_user=Depends(get_current_user)):
    """Get all grant applications for the current user"""
    try:
        applications = grant_service.get_applications_by_user(current_user["username"])
        return {
            "applications": [app.dict() for app in applications],
            "total_applications": len(applications),
        }
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to fetch applications: {str(e)}"
        )


@app.get("/api/grant-applications/{application_id}")
def get_grant_application(application_id: str, current_user=Depends(get_current_user)):
    """Get a specific grant application"""
    try:
        application = grant_service.get_application_by_id(application_id)
        if not application:
            raise HTTPException(status_code=404, detail="Application not found")

        # Check if user has access to this application
        if (
            application.assigned_to != current_user["username"]
            and current_user["username"] not in application.collaborators
        ):
            raise HTTPException(status_code=403, detail="Access denied")

        return application.dict()
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to fetch application: {str(e)}"
        )


@app.post("/api/grant-applications")
def create_grant_application(
    application_data: GrantApplicationCreate, current_user=Depends(get_current_user)
):
    """Create a new grant application"""
    try:
        application = grant_service.create_application(
            grant_id=application_data.grant_id,
            title=application_data.title,
            assigned_to=application_data.assigned_to,
            collaborators=application_data.collaborators,
        )
        return {
            "message": "Grant application created successfully",
            "application": application.dict(),
        }
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to create application: {str(e)}"
        )


@app.post("/api/grant-applications/{application_id}/answers")
def update_application_answer(
    application_id: str,
    answer_data: GrantAnswerUpdate,
    current_user=Depends(get_current_user),
):
    """Update or create an answer for a grant application"""
    try:
        answer = grant_service.update_application_answer(
            application_id=application_id,
            question=answer_data.question,
            answer=answer_data.answer,
            author=current_user["username"],
        )
        return {"message": "Answer updated successfully", "answer": answer.dict()}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to update answer: {str(e)}"
        )


@app.get("/api/grant-applications/{application_id}/answers")
def get_application_answers(
    application_id: str, current_user=Depends(get_current_user)
):
    """Get all answers for a grant application"""
    try:
        answers = grant_service.get_application_answers(application_id)
        return {
            "answers": [answer.dict() for answer in answers],
            "total_answers": len(answers),
        }
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to fetch answers: {str(e)}"
        )


@app.post("/api/grant-applications/{application_id}/comments")
def add_application_comment(
    application_id: str,
    comment_data: GrantCommentCreate,
    current_user=Depends(get_current_user),
):
    """Add a comment to a grant application"""
    try:
        comment = grant_service.add_comment(
            application_id=application_id,
            content=comment_data.content,
            author=current_user["username"],
        )
        return {"message": "Comment added successfully", "comment": comment.dict()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to add comment: {str(e)}")


@app.get("/api/grant-applications/{application_id}/comments")
def get_application_comments(
    application_id: str, current_user=Depends(get_current_user)
):
    """Get all comments for a grant application"""
    try:
        comments = grant_service.get_application_comments(application_id)
        return {
            "comments": [comment.dict() for comment in comments],
            "total_comments": len(comments),
        }
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to fetch comments: {str(e)}"
        )


@app.post("/api/grant-applications/{application_id}/submit")
def submit_grant_application(
    application_id: str, current_user=Depends(get_current_user)
):
    """Submit a grant application"""
    try:
        success = grant_service.submit_application(application_id)
        if success:
            return {"message": "Application submitted successfully"}
        else:
            raise HTTPException(status_code=404, detail="Application not found")
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to submit application: {str(e)}"
        )


@app.get("/api/grant-applications/stats")
def get_application_stats(current_user=Depends(get_current_user)):
    """Get statistics for grant applications"""
    try:
        applications = grant_service.get_applications_by_user(current_user["username"])

        stats = {
            "total_applications": len(applications),
            "draft": len(
                [app for app in applications if app.status == GrantStatus.DRAFT]
            ),
            "in_progress": len(
                [app for app in applications if app.status == GrantStatus.IN_PROGRESS]
            ),
            "submitted": len(
                [app for app in applications if app.status == GrantStatus.SUBMITTED]
            ),
            "approved": len(
                [app for app in applications if app.status == GrantStatus.APPROVED]
            ),
            "rejected": len(
                [app for app in applications if app.status == GrantStatus.REJECTED]
            ),
            "withdrawn": len(
                [app for app in applications if app.status == GrantStatus.WITHDRAWN]
            ),
        }

        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch stats: {str(e)}")
