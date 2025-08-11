import uuid
import logging
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, validator
from enum import Enum
import time

# Advanced Quality Assurance Constants
GRANT_AMOUNT_MIN = 1000.00
GRANT_AMOUNT_MAX = 100000.00
SUCCESS_SCORE_MIN = 0.0
SUCCESS_SCORE_MAX = 1.0
BUDGET_MIN = 100.00
BUDGET_MAX = 50000.00

# Currency and Localization Constants
CURRENCY_CODE = "AUD"
LOCALE = "en-AU"
DATE_FORMAT = "DD/MM/YYYY"

# Performance Monitoring
PERFORMANCE_THRESHOLDS = {
    "search_timeout_ms": 5000,
    "max_results_per_page": 100,
    "cache_ttl_seconds": 300,
}

# Audit Trail Configuration
AUDIT_ENABLED = True
AUDIT_RETENTION_DAYS = 90

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Grant Models


class GrantStatus(str, Enum):
    DRAFT = "draft"
    IN_PROGRESS = "in_progress"
    SUBMITTED = "submitted"
    APPROVED = "approved"
    REJECTED = "rejected"
    WITHDRAWN = "withdrawn"


class GrantPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class GrantCategory(str, Enum):
    ARTS_CULTURE = "arts_culture"
    COMMUNITY = "community"
    EDUCATION = "education"
    ENVIRONMENT = "environment"
    HEALTH = "health"
    TECHNOLOGY = "technology"
    YOUTH = "youth"
    INDIGENOUS = "indigenous"
    DISABILITY = "disability"
    OTHER = "other"


# Enhanced Grant model with advanced validation


class Grant(BaseModel):
    id: str = Field(
        default_factory=lambda: str(uuid.uuid4()), description="Unique grant identifier"
    )
    title: str = Field(..., min_length=5, max_length=200, description="Grant title")
    description: str = Field(
        ..., min_length=10, max_length=2000, description="Grant description"
    )
    amount: float = Field(..., gt=0, description="Grant amount in AUD")
    deadline: datetime = Field(..., description="Application deadline")
    category: GrantCategory = Field(..., description="Grant category")
    priority: GrantPriority = Field(
        default=GrantPriority.MEDIUM, description="Grant priority"
    )
    status: GrantStatus = Field(default=GrantStatus.DRAFT, description="Grant status")
    organisation: str = Field(
        ..., min_length=2, max_length=100, description="Granting organisation"
    )
    eligibility_criteria: List[str] = Field(
        default_factory=list, description="Eligibility criteria"
    )
    required_documents: List[str] = Field(
        default_factory=list, description="Required documents"
    )
    success_score: float = Field(
        default=0.5, ge=0.0, le=1.0, description="AI success prediction score"
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow, description="Creation timestamp"
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow, description="Last update timestamp"
    )

    # Advanced validation with specific error messages
    @validator("amount")
    def validate_amount(cls, v):
        if not (GRANT_AMOUNT_MIN <= v <= GRANT_AMOUNT_MAX):
            raise ValueError(
                f"Grant amount must be between {cls.format_currency(GRANT_AMOUNT_MIN)} "
                f"and {cls.format_currency(GRANT_AMOUNT_MAX)}. "
                f"Current value: {cls.format_currency(v)}"
            )
        return round(v, 2)  # Ensure 2 decimal places for currency

    @validator("success_score")
    def validate_success_score(cls, v):
        if not (SUCCESS_SCORE_MIN <= v <= SUCCESS_SCORE_MAX):
            raise ValueError(
                f"Success score must be between {SUCCESS_SCORE_MIN} and {SUCCESS_SCORE_MAX}. "
                f"Current value: {v}"
            )
        return round(v, 3)  # Ensure 3 decimal places for precision

    @validator("deadline")
    def validate_deadline(cls, v):
        if v <= datetime.utcnow():
            raise ValueError("Deadline must be in the future")
        return v

    # Currency formatting with locale awareness
    @staticmethod
    def format_currency(amount: float) -> str:
        """Format currency amount with proper locale and error handling"""
        try:
            return f"AUD ${amount:,.2f}"
        except (ValueError, TypeError) as e:
            logger.warning(f"Currency formatting failed for amount {amount}: {e}")
            return f"AUD ${amount}"

    # Date formatting with UK locale
    def format_deadline_uk(self) -> str:
        """Format deadline in UK date format with error handling"""
        try:
            return self.deadline.strftime("%d/%m/%Y")
        except (AttributeError, ValueError) as e:
            logger.warning(f"Date formatting failed for deadline {self.deadline}: {e}")
            return str(self.deadline)

    # Audit trail method
    def log_audit_event(
        self, action: str, user_id: str, details: Dict[str, Any] = None
    ):
        """Log audit event for data integrity tracking"""
        if not AUDIT_ENABLED:
            return

        audit_event = {
            "timestamp": datetime.utcnow().isoformat(),
            "action": action,
            "user_id": user_id,
            "grant_id": self.id,
            "details": details or {},
        }

        logger.info("Audit event logged", extra=audit_event)


class GrantApplication(BaseModel):
    id: str = Field(..., description="Unique application identifier")
    grant_id: str = Field(..., description="Associated grant ID")
    title: str = Field(
        ..., min_length=5, max_length=200, description="Application title"
    )
    status: GrantStatus = Field(
        default=GrantStatus.DRAFT, description="Application status"
    )
    priority: GrantPriority = Field(
        default=GrantPriority.MEDIUM, description="Application priority"
    )
    assigned_to: str = Field(..., description="Primary assignee")
    collaborators: List[str] = Field(
        default_factory=list, description="Team collaborators"
    )
    answers: Dict[str, str] = Field(
        default_factory=dict, description="Application answers"
    )
    documents: List[str] = Field(default_factory=list, description="Attached documents")
    budget: float = Field(..., gt=0, description="Project budget in AUD")
    timeline: str = Field(default="", description="Project timeline")
    impact_statement: str = Field(default="", description="Impact statement")
    created_at: datetime = Field(
        default_factory=datetime.utcnow, description="Creation timestamp"
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow, description="Last update timestamp"
    )
    submitted_at: Optional[datetime] = Field(
        default=None, description="Submission timestamp"
    )

    @validator("budget")
    def validate_budget(cls, v):
        if not (BUDGET_MIN <= v <= BUDGET_MAX):
            raise ValueError(
                f"Budget must be between {cls.format_currency(BUDGET_MIN)} "
                f"and {cls.format_currency(BUDGET_MAX)}. "
                f"Current value: {cls.format_currency(v)}"
            )
        return round(v, 2)

    @staticmethod
    def format_currency(amount: float) -> str:
        """Format currency amount with proper locale and error handling"""
        try:
            return f"AUD ${amount:,.2f}"
        except (ValueError, TypeError) as e:
            logger.warning(f"Currency formatting failed for amount {amount}: {e}")
            return f"AUD ${amount}"

    def log_audit_event(
        self, action: str, user_id: str, details: Dict[str, Any] = None
    ):
        """Log audit event for data integrity tracking"""
        if not AUDIT_ENABLED:
            return

        audit_event = {
            "timestamp": datetime.utcnow().isoformat(),
            "action": action,
            "user_id": user_id,
            "application_id": self.id,
            "details": details or {},
        }

        logger.info("Audit event logged", extra=audit_event)


class GrantAnswer(BaseModel):
    id: str = Field(..., description="Unique answer identifier")
    application_id: str = Field(..., description="Associated application ID")
    question: str = Field(..., description="Question text")
    answer: str = Field(..., description="Answer text")
    author: str = Field(..., description="Answer author")
    version: int = Field(..., ge=1, description="Answer version number")
    created_at: datetime = Field(
        default_factory=datetime.utcnow, description="Creation timestamp"
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow, description="Last update timestamp"
    )


class GrantComment(BaseModel):
    id: str = Field(..., description="Unique comment identifier")
    application_id: str = Field(..., description="Associated application ID")
    author: str = Field(..., description="Comment author")
    content: str = Field(..., description="Comment content")
    created_at: datetime = Field(
        default_factory=datetime.utcnow, description="Creation timestamp"
    )


# In-memory storage for testing (will be replaced with database)
grants_db: List[Grant] = []
applications_db: List[GrantApplication] = []
answers_db: List[GrantAnswer] = []
comments_db: List[GrantComment] = []

# Sample grants data with proper AUD amounts and updated structure
SAMPLE_GRANTS = [
    {
        "id": "grant_001",
        "title": "Victorian Creative Industries Grant",
        "description": "Supporting creative projects that contribute to Victoria's cultural landscape",
        "amount": 50000.00,
        "deadline": datetime.now() + timedelta(days=30),
        "category": GrantCategory.ARTS_CULTURE,
        "organisation": "Creative Victoria",
        "eligibility_criteria": [
            "Non-profit organisations",
            "Creative businesses",
            "Individual artists",
        ],
        "required_documents": [
            "Project proposal",
            "Budget breakdown",
            "Timeline",
            "Impact assessment",
        ],
        "success_score": 0.850,
        "created_at": datetime.now(),
        "updated_at": datetime.now(),
    },
    {
        "id": "grant_002",
        "title": "Community Impact Fund",
        "description": "Supporting community projects that create positive social impact",
        "amount": 25000.00,
        "deadline": datetime.now() + timedelta(days=45),
        "category": GrantCategory.COMMUNITY,
        "organisation": "Department of Communities",
        "eligibility_criteria": [
            "Community organisations",
            "Social enterprises",
            "Non-profits",
        ],
        "required_documents": [
            "Community consultation",
            "Impact measurement plan",
            "Partnership details",
        ],
        "success_score": 0.920,
        "created_at": datetime.now(),
        "updated_at": datetime.now(),
    },
    {
        "id": "grant_003",
        "title": "Youth Innovation Grant",
        "description": "Supporting innovative projects led by young people",
        "amount": 15000.00,
        "deadline": datetime.now() + timedelta(days=60),
        "category": GrantCategory.YOUTH,
        "organisation": "Youth Affairs Victoria",
        "eligibility_criteria": [
            "Youth-led organisations",
            "Young entrepreneurs",
            "Youth groups",
        ],
        "required_documents": [
            "Youth leadership",
            "Innovation component",
            "Community benefit",
        ],
        "success_score": 0.780,
        "created_at": datetime.now(),
        "updated_at": datetime.now(),
    },
]

# Initialize sample data
for grant_data in SAMPLE_GRANTS:
    try:
        grants_db.append(Grant(**grant_data))
        logger.info(f"Initialised grant: {grant_data['title']}")
    except Exception as e:
        logger.error(f"Error initialising grant {grant_data['title']}: {e}")


# Enhanced GrantService with performance monitoring and data quality


class GrantService:
    """Enhanced grant service with advanced quality assurance"""

    def __init__(self):
        self._cache = {}
        self._cache_timestamps = {}
        self._performance_metrics = {
            "total_requests": 0,
            "cache_hits": 0,
            "cache_misses": 0,
            "average_response_time_ms": 0,
        }

    def _log_performance(self, operation: str, start_time: float, success: bool = True):
        """Log performance metrics for monitoring"""
        response_time = (time.time() - start_time) * 1000
        self._performance_metrics["total_requests"] += 1
        self._performance_metrics["average_response_time_ms"] = (
            self._performance_metrics["average_response_time_ms"]
            * (self._performance_metrics["total_requests"] - 1)
            + response_time
        ) / self._performance_metrics["total_requests"]

        logger.info(
            "Performance metric recorded",
            extra={
                "operation": operation,
                "response_time_ms": round(response_time, 2),
                "success": success,
                "average_response_time_ms": round(
                    self._performance_metrics["average_response_time_ms"], 2
                ),
            },
        )

    def _get_cached_data(self, key: str) -> Optional[Any]:
        """Get data from cache with TTL validation"""
        if key in self._cache:
            timestamp = self._cache_timestamps.get(key, 0)
            if time.time() - timestamp < PERFORMANCE_THRESHOLDS["cache_ttl_seconds"]:
                self._performance_metrics["cache_hits"] += 1
                return self._cache[key]
            else:
                # Remove expired cache entry
                del self._cache[key]
                del self._cache_timestamps[key]

        self._performance_metrics["cache_misses"] += 1
        return None

    def _set_cached_data(self, key: str, data: Any):
        """Set data in cache with timestamp"""
        self._cache[key] = data
        self._cache_timestamps[key] = time.time()

    @staticmethod
    def get_all_grants() -> List[Grant]:
        """Get all grants with performance monitoring"""
        start_time = time.time()

        try:
            # Check cache first
            cache_key = "all_grants"
            cached_grants = grant_service._get_cached_data(cache_key)
            if cached_grants:
                grant_service._log_performance("get_all_grants", start_time)
                return cached_grants

            # Get from database
            grants = SAMPLE_GRANTS.copy()

            # Cache the result
            grant_service._set_cached_data(cache_key, grants)

            grant_service._log_performance("get_all_grants", start_time)
            logger.info(
                "All grants retrieved successfully", extra={"count": len(grants)}
            )
            return grants

        except Exception as e:
            grant_service._log_performance("get_all_grants", start_time, success=False)
            logger.error("Failed to retrieve grants", extra={"error": str(e)})
            raise

    @staticmethod
    def get_grant_by_id(grant_id: str) -> Optional[Grant]:
        """Get grant by ID with validation and error handling"""
        start_time = time.time()

        try:
            # Validate input
            if not grant_id or not isinstance(grant_id, str):
                raise ValueError("Invalid grant ID provided")

            # Check cache first
            cache_key = f"grant_{grant_id}"
            cached_grant = grant_service._get_cached_data(cache_key)
            if cached_grant:
                grant_service._log_performance("get_grant_by_id", start_time)
                return cached_grant

            # Get from database
            for grant in SAMPLE_GRANTS:
                if grant["id"] == grant_id:
                    grant_obj = Grant(**grant)

                    # Cache the result
                    grant_service._set_cached_data(cache_key, grant_obj)

                    grant_service._log_performance("get_grant_by_id", start_time)
                    logger.info(
                        "Grant retrieved successfully", extra={"grant_id": grant_id}
                    )
                    return grant_obj

            logger.warning("Grant not found", extra={"grant_id": grant_id})
            return None

        except Exception as e:
            grant_service._log_performance("get_grant_by_id", start_time, success=False)
            logger.error(
                "Failed to retrieve grant",
                extra={"grant_id": grant_id, "error": str(e)},
            )
            raise

    @staticmethod
    def search_grants(
        keywords: Optional[str] = None,
        category: Optional[GrantCategory] = None,
        min_amount: Optional[float] = None,
        max_amount: Optional[float] = None,
        deadline_before: Optional[datetime] = None,
        limit: int = PERFORMANCE_THRESHOLDS["max_results_per_page"],
    ) -> List[Grant]:
        """Search grants with comprehensive filtering and performance monitoring"""
        start_time = time.time()

        try:
            # Validate inputs
            if min_amount is not None and (
                min_amount < 0 or min_amount > GRANT_AMOUNT_MAX
            ):
                raise ValueError(
                    f"Invalid min_amount: must be between 0 and {GRANT_AMOUNT_MAX}"
                )

            if max_amount is not None and (
                max_amount < 0 or max_amount > GRANT_AMOUNT_MAX
            ):
                raise ValueError(
                    f"Invalid max_amount: must be between 0 and {GRANT_AMOUNT_MAX}"
                )

            if limit > PERFORMANCE_THRESHOLDS["max_results_per_page"]:
                limit = PERFORMANCE_THRESHOLDS["max_results_per_page"]

            # Check cache
            cache_key = f"search_{hash((keywords, category, min_amount, max_amount, deadline_before, limit))}"
            cached_results = grant_service._get_cached_data(cache_key)
            if cached_results:
                grant_service._log_performance("search_grants", start_time)
                return cached_results

            # Perform search
            results = []
            for grant_data in SAMPLE_GRANTS:
                grant = Grant(**grant_data)

                # Apply filters
                if (
                    keywords
                    and keywords.lower() not in grant.title.lower()
                    and keywords.lower() not in grant.description.lower()
                ):
                    continue

                if category and grant.category != category:
                    continue

                if min_amount is not None and grant.amount < min_amount:
                    continue

                if max_amount is not None and grant.amount > max_amount:
                    continue

                if deadline_before and grant.deadline > deadline_before:
                    continue

                results.append(grant)

                # Apply limit
                if len(results) >= limit:
                    break

            # Cache results
            grant_service._set_cached_data(cache_key, results)

            grant_service._log_performance("search_grants", start_time)
            logger.info(
                "Grant search completed",
                extra={
                    "results_count": len(results),
                    "filters_applied": {
                        "keywords": keywords,
                        "category": category,
                        "min_amount": min_amount,
                        "max_amount": max_amount,
                        "deadline_before": deadline_before,
                    },
                },
            )

            return results

        except Exception as e:
            grant_service._log_performance("search_grants", start_time, success=False)
            logger.error("Grant search failed", extra={"error": str(e)})
            raise

    @staticmethod
    def get_recommended_grants(user_profile: Dict) -> List[Grant]:
        """Get AI-recommended grants based on user profile"""
        try:
            recommendations = []

            for grant in grants_db:
                score = 0.0

                # Category preference
                if (
                    user_profile.get("preferred_categories")
                    and grant.category in user_profile["preferred_categories"]
                ):
                    score += 0.3

                # Amount range
                if (
                    user_profile.get("min_amount")
                    and grant.amount >= user_profile["min_amount"]
                ):
                    score += 0.2
                if (
                    user_profile.get("max_amount")
                    and grant.amount <= user_profile["max_amount"]
                ):
                    score += 0.2

                # Deadline urgency
                days_until_deadline = (grant.deadline - datetime.now()).days
                if days_until_deadline <= 30:
                    score += 0.2
                elif days_until_deadline <= 60:
                    score += 0.1

                # Base success score
                score += grant.success_score * 0.1

                if score > 0.3:  # Only recommend if score is reasonable
                    recommendations.append((grant, score))

            # Sort by recommendation score
            recommendations.sort(key=lambda x: x[1], reverse=True)
            result = [grant for grant, score in recommendations[:10]]

            logger.info(f"Generated {len(result)} grant recommendations")
            return result
        except Exception as e:
            logger.error(f"Error generating recommendations: {e}")
            return []

    @staticmethod
    def create_application(
        grant_id: str, title: str, assigned_to: str, collaborators: List[str] = None
    ) -> GrantApplication:
        """Create a new grant application"""
        try:
            application = GrantApplication(
                id=str(uuid.uuid4()),
                grant_id=grant_id,
                title=title,
                status=GrantStatus.DRAFT,
                priority=GrantPriority.MEDIUM,
                assigned_to=assigned_to,
                collaborators=collaborators or [],
                answers={},
                documents=[],
                budget=0.0,
                timeline="",
                impact_statement="",
                created_at=datetime.now(),
                updated_at=datetime.now(),
            )

            applications_db.append(application)
            logger.info(f"Created application: {application.title}")
            return application
        except Exception as e:
            logger.error(f"Error creating application: {e}")
            raise

    @staticmethod
    def get_applications_by_user(user_id: str) -> List[GrantApplication]:
        """Get all applications for a user (assigned or collaborating)"""
        try:
            result = [
                app
                for app in applications_db
                if app.assigned_to == user_id or user_id in app.collaborators
            ]
            logger.info(f"Retrieved {len(result)} applications for user {user_id}")
            return result
        except Exception as e:
            logger.error(f"Error retrieving applications for user {user_id}: {e}")
            return []

    @staticmethod
    def get_application_by_id(application_id: str) -> Optional[GrantApplication]:
        """Get a specific application by ID"""
        try:
            for app in applications_db:
                if app.id == application_id:
                    logger.info(f"Retrieved application: {app.title}")
                    return app
            logger.warning(f"Application not found: {application_id}")
            return None
        except Exception as e:
            logger.error(f"Error retrieving application {application_id}: {e}")
            return None

    @staticmethod
    def update_application_answer(
        application_id: str, question: str, answer: str, author: str
    ) -> GrantAnswer:
        """Update or create an answer for a grant application"""
        try:
            # Find existing answer
            existing_answer = None
            for ans in answers_db:
                if ans.application_id == application_id and ans.question == question:
                    existing_answer = ans
                    break

            if existing_answer:
                # Create new version
                new_answer = GrantAnswer(
                    id=str(uuid.uuid4()),
                    application_id=application_id,
                    question=question,
                    answer=answer,
                    author=author,
                    version=existing_answer.version + 1,
                    created_at=datetime.now(),
                    updated_at=datetime.now(),
                )
            else:
                # Create first answer
                new_answer = GrantAnswer(
                    id=str(uuid.uuid4()),
                    application_id=application_id,
                    question=question,
                    answer=answer,
                    author=author,
                    version=1,
                    created_at=datetime.now(),
                    updated_at=datetime.now(),
                )

            answers_db.append(new_answer)

            # Update application
            for app in applications_db:
                if app.id == application_id:
                    app.answers[question] = answer
                    app.updated_at = datetime.now()
                    break

            logger.info(f"Updated answer for application {application_id}")
            return new_answer
        except Exception as e:
            logger.error(f"Error updating answer: {e}")
            raise

    @staticmethod
    def add_comment(application_id: str, content: str, author: str) -> GrantComment:
        """Add a comment to a grant application"""
        try:
            comment = GrantComment(
                id=str(uuid.uuid4()),
                application_id=application_id,
                author=author,
                content=content,
                created_at=datetime.now(),
            )

            comments_db.append(comment)
            logger.info(f"Added comment to application {application_id}")
            return comment
        except Exception as e:
            logger.error(f"Error adding comment: {e}")
            raise

    @staticmethod
    def get_application_comments(application_id: str) -> List[GrantComment]:
        """Get all comments for an application"""
        try:
            result = [c for c in comments_db if c.application_id == application_id]
            logger.info(
                f"Retrieved {len(result)} comments for application {application_id}"
            )
            return result
        except Exception as e:
            logger.error(
                f"Error retrieving comments for application {application_id}: {e}"
            )
            return []

    @staticmethod
    def get_application_answers(application_id: str) -> List[GrantAnswer]:
        """Get all answers for an application"""
        try:
            result = [a for a in answers_db if a.application_id == application_id]
            logger.info(
                f"Retrieved {len(result)} answers for application {application_id}"
            )
            return result
        except Exception as e:
            logger.error(
                f"Error retrieving answers for application {application_id}: {e}"
            )
            return []

    @staticmethod
    def submit_application(application_id: str) -> bool:
        """Submit a grant application"""
        try:
            for app in applications_db:
                if app.id == application_id:
                    app.status = GrantStatus.SUBMITTED
                    app.submitted_at = datetime.now()
                    app.updated_at = datetime.now()
                    logger.info(f"Submitted application: {app.title}")
                    return True
            logger.warning(f"Application not found for submission: {application_id}")
            return False
        except Exception as e:
            logger.error(f"Error submitting application {application_id}: {e}")
            return False

    def get_performance_metrics(self) -> Dict[str, Any]:
        """Get performance metrics for monitoring"""
        return {
            "total_requests": self._performance_metrics["total_requests"],
            "cache_hits": self._performance_metrics["cache_hits"],
            "cache_misses": self._performance_metrics["cache_misses"],
            "cache_hit_rate": (
                self._performance_metrics["cache_hits"]
                / max(self._performance_metrics["total_requests"], 1)
            ),
            "average_response_time_ms": round(
                self._performance_metrics["average_response_time_ms"], 2
            ),
            "cache_size": len(self._cache),
        }


# Initialize the enhanced service
grant_service = GrantService()
