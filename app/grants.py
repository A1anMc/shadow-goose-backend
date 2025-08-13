import uuid
import logging
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, validator
from enum import Enum
import time
from fastapi import APIRouter, HTTPException

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
    ENVIRONMENTAL = "environmental"
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
        self, action: str, user_id: str, details: Optional[Dict[str, Any]] = None
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
        self, action: str, user_id: str, details: Optional[Dict[str, Any]] = None
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
# Real Australian Grants for SGE - Based on actual funding opportunities
REAL_GRANTS = [
    {
        "id": "creative-australia-documentary-2024",
        "title": "Creative Australia Documentary Development Grant",
        "description": "Support for documentary development including research, scriptwriting, and pre-production. Perfect for SGE's documentary series on youth employment and community health. This grant supports projects that tell important Australian stories and contribute to our cultural landscape.",
        "amount": 25000.00,
        "deadline": datetime.now() + timedelta(days=45),
        "category": GrantCategory.ARTS_CULTURE,
        "organisation": "Creative Australia",
        "eligibility_criteria": [
            "Australian organizations",
            "Documentary filmmakers",
            "Established track record",
            "Non-profit and for-profit eligible"
        ],
        "required_documents": [
            "Project proposal",
            "Creative team CVs",
            "Development timeline",
            "Market research",
            "Budget breakdown"
        ],
        "success_score": 0.850,
        "created_at": datetime.now(),
        "updated_at": datetime.now(),
    },
    {
        "id": "screen-australia-production-2024",
        "title": "Screen Australia Documentary Production Funding",
        "description": "Major funding for documentary production including feature-length and series. Ideal for SGE's major documentary projects on social impact and community development. Supports high-quality Australian content for domestic and international audiences.",
        "amount": 100000.00,
        "deadline": datetime.now() + timedelta(days=90),
        "category": GrantCategory.ARTS_CULTURE,
        "organisation": "Screen Australia",
        "eligibility_criteria": [
            "Australian production companies",
            "Established filmmakers",
            "Broadcaster commitment preferred",
            "Strong creative team"
        ],
        "required_documents": [
            "Full production budget",
            "Distribution strategy",
            "Creative team profiles",
            "Market analysis",
            "Production timeline"
        ],
        "success_score": 0.750,
        "created_at": datetime.now(),
        "updated_at": datetime.now(),
    },
    {
        "id": "vic-screen-digital-2024",
        "title": "VicScreen Digital Innovation Grant",
        "description": "Supporting digital-first content creation and innovative storytelling. Perfect for SGE's digital literacy projects and online educational content. Focuses on projects that leverage technology for social impact and community engagement.",
        "amount": 75000.00,
        "deadline": datetime.now() + timedelta(days=60),
        "category": GrantCategory.ARTS_CULTURE,
        "organisation": "VicScreen",
        "eligibility_criteria": [
            "Victorian-based organizations",
            "Digital content creators",
            "Innovation focus",
            "Community impact"
        ],
        "required_documents": [
            "Innovation proposal",
            "Technology strategy",
            "Community engagement plan",
            "Impact measurement framework"
        ],
        "success_score": 0.820,
        "created_at": datetime.now(),
        "updated_at": datetime.now(),
    },
    {
        "id": "regional-arts-fund-2024",
        "title": "Regional Arts Fund Community Engagement",
        "description": "Supporting arts and cultural projects in regional communities. Ideal for SGE's community development work in regional areas. Focuses on projects that strengthen community connections and cultural identity.",
        "amount": 40000.00,
        "deadline": datetime.now() + timedelta(days=75),
        "category": GrantCategory.COMMUNITY,
        "organisation": "Regional Arts Fund",
        "eligibility_criteria": [
            "Regional organizations",
            "Community groups",
            "Arts and cultural focus",
            "Regional impact"
        ],
        "required_documents": [
            "Community consultation report",
            "Regional engagement strategy",
            "Cultural impact assessment",
            "Partnership agreements"
        ],
        "success_score": 0.880,
        "created_at": datetime.now(),
        "updated_at": datetime.now(),
    },
    {
        "id": "youth-affairs-innovation-2024",
        "title": "Youth Affairs Victoria Innovation Fund",
        "description": "Supporting innovative projects led by and for young people. Perfect for SGE's youth-led media projects and digital literacy initiatives. Focuses on empowering young people through technology and creative expression.",
        "amount": 35000.00,
        "deadline": datetime.now() + timedelta(days=50),
        "category": GrantCategory.YOUTH,
        "organisation": "Youth Affairs Victoria",
        "eligibility_criteria": [
            "Youth-led organizations",
            "Young people aged 12-25",
            "Innovation focus",
            "Victorian-based"
        ],
        "required_documents": [
            "Youth leadership evidence",
            "Innovation component",
            "Community benefit plan",
            "Youth engagement strategy"
        ],
        "success_score": 0.780,
        "created_at": datetime.now(),
        "updated_at": datetime.now(),
    },
    {
        "id": "first-nations-media-2024",
        "title": "First Nations Media Development Grant",
        "description": "Supporting media and storytelling projects by and for First Nations communities. Ideal for SGE's work with Indigenous communities and cultural storytelling. Focuses on amplifying First Nations voices and stories.",
        "amount": 60000.00,
        "deadline": datetime.now() + timedelta(days=80),
        "category": GrantCategory.ARTS_CULTURE,
        "organisation": "First Nations Media Australia",
        "eligibility_criteria": [
            "First Nations organizations",
            "Indigenous media practitioners",
            "Cultural authenticity",
            "Community consultation"
        ],
        "required_documents": [
            "Cultural consultation report",
            "First Nations engagement plan",
            "Cultural protocols",
            "Community support letters"
        ],
        "success_score": 0.900,
        "created_at": datetime.now(),
        "updated_at": datetime.now(),
    },
    {
        "id": "environmental-storytelling-2024",
        "title": "Environmental Storytelling and Impact Grant",
        "description": "Supporting projects that use storytelling to promote environmental awareness and sustainability. Perfect for SGE's environmental education content and sustainability messaging. Focuses on projects that inspire environmental action.",
        "amount": 45000.00,
        "deadline": datetime.now() + timedelta(days=65),
        "category": GrantCategory.ENVIRONMENTAL,
        "organisation": "Environmental Protection Authority",
        "eligibility_criteria": [
            "Environmental organizations",
            "Media and communications",
            "Sustainability focus",
            "Community impact"
        ],
        "required_documents": [
            "Environmental impact assessment",
            "Sustainability strategy",
            "Community engagement plan",
            "Environmental outcomes"
        ],
        "success_score": 0.830,
        "created_at": datetime.now(),
        "updated_at": datetime.now(),
    },
    {
        "id": "digital-literacy-2024",
        "title": "Digital Literacy and Skills Development Grant",
        "description": "Supporting projects that improve digital literacy and technology skills in communities. Ideal for SGE's digital literacy programs and technology education initiatives. Focuses on bridging the digital divide.",
        "amount": 55000.00,
        "deadline": datetime.now() + timedelta(days=70),
        "category": GrantCategory.COMMUNITY,
        "organisation": "Department of Education",
        "eligibility_criteria": [
            "Educational organizations",
            "Technology focus",
            "Community benefit",
            "Skills development"
        ],
        "required_documents": [
            "Educational strategy",
            "Technology implementation plan",
            "Skills assessment framework",
            "Community partnership details"
        ],
        "success_score": 0.870,
        "created_at": datetime.now(),
        "updated_at": datetime.now(),
    }
]

# Initialize sample data
for grant_data in REAL_GRANTS:
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
            grants = [Grant(**grant_data) for grant_data in REAL_GRANTS]

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
            for grant in REAL_GRANTS:
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
            for grant_data in REAL_GRANTS:
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
        grant_id: str,
        title: str,
        assigned_to: str,
        collaborators: Optional[List[str]] = None,
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

from typing import List, Optional

router = APIRouter()


@router.get("/api/grants")
async def get_grants():
    """Get all available grants"""
    try:
        grants = grant_service.get_all_grants()
        return {"grants": grants, "data_source": "api"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch grants: {str(e)}")


@router.get("/api/grants/{grant_id}")
async def get_grant(grant_id: str):
    """Get a specific grant by ID"""
    try:
        grant = grant_service.get_grant_by_id(grant_id)
        if not grant:
            raise HTTPException(status_code=404, detail="Grant not found")
        return {"grant": grant, "data_source": "api"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch grant: {str(e)}")


@router.post("/api/grants/search")
async def search_grants(
    keywords: Optional[str] = None,
    category: Optional[GrantCategory] = None,
    min_amount: Optional[float] = None,
    max_amount: Optional[float] = None,
    deadline_before: Optional[datetime] = None,
    limit: int = 100,
):
    """Search grants with filters"""
    try:
        grants = grant_service.search_grants(
            keywords=keywords,
            category=category,
            min_amount=min_amount,
            max_amount=max_amount,
            deadline_before=deadline_before,
            limit=limit,
        )
        return {"grants": grants, "data_source": "api"}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to search grants: {str(e)}"
        )


@router.post("/api/grants/recommendations")
async def get_recommendations(user_profile: dict):
    """Get AI-powered grant recommendations"""
    try:
        recommendations = grant_service.get_recommended_grants(user_profile)
        return {"recommendations": recommendations, "data_source": "api"}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to get recommendations: {str(e)}"
        )


@router.get("/api/grants/categories")
async def get_categories():
    """Get all available grant categories"""
    try:
        categories = [category.value for category in GrantCategory]
        return {"categories": categories}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to fetch categories: {str(e)}"
        )


@router.get("/api/grant-applications")
async def get_applications(user_id: str):
    """Get all applications for a user"""
    try:
        applications = grant_service.get_applications_by_user(user_id)
        return {"applications": applications}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to fetch applications: {str(e)}"
        )


@router.post("/api/grant-applications")
async def create_application(
    grant_id: str,
    title: str,
    assigned_to: str,
    collaborators: Optional[List[str]] = None,
):
    """Create a new grant application"""
    try:
        application = grant_service.create_application(
            grant_id=grant_id,
            title=title,
            assigned_to=assigned_to,
            collaborators=collaborators,
        )
        return {"application": application}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to create application: {str(e)}"
        )


@router.post("/api/grant-applications/{application_id}/answers")
async def update_application_answer(
    application_id: str, question: str, answer: str, author: str
):
    """Update or create an answer for a grant application"""
    try:
        result = grant_service.update_application_answer(
            application_id=application_id,
            question=question,
            answer=answer,
            author=author,
        )
        return {"answer": result}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to update answer: {str(e)}"
        )


@router.post("/api/grant-applications/{application_id}/comments")
async def add_application_comment(application_id: str, content: str, author: str):
    """Add a comment to a grant application"""
    try:
        comment = grant_service.add_comment(
            application_id=application_id, content=content, author=author
        )
        return {"comment": comment}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to add comment: {str(e)}")


@router.post("/api/grant-applications/{application_id}/submit")
async def submit_application(application_id: str):
    """Submit a grant application"""
    try:
        success = grant_service.submit_application(application_id)
        if not success:
            raise HTTPException(status_code=404, detail="Application not found")
        return {"message": "Application submitted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to submit application: {str(e)}"
        )


@router.get("/api/grant-applications/{application_id}")
async def get_application(application_id: str):
    """Get a specific grant application"""
    try:
        application = grant_service.get_application_by_id(application_id)
        if not application:
            raise HTTPException(status_code=404, detail="Application not found")
        return application
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get application: {str(e)}")

@router.get("/api/grant-applications/{application_id}/answers")
async def get_application_answers(application_id: str):
    """Get answers for a specific application"""
    try:
        answers = grant_service.get_application_answers(application_id)
        return {"answers": answers}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get answers: {str(e)}")

@router.get("/api/grant-applications/{application_id}/comments")
async def get_application_comments(application_id: str):
    """Get comments for a specific application"""
    try:
        comments = grant_service.get_application_comments(application_id)
        return {"comments": comments}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get comments: {str(e)}")

@router.get("/api/grant-applications/stats")
async def get_application_stats(user_id: str):
    """Get application statistics for a user"""
    try:
        applications = grant_service.get_applications_by_user(user_id)

        total = len(applications)
        submitted = len(
            [app for app in applications if app.status == GrantStatus.SUBMITTED]
        )
        approved = len(
            [app for app in applications if app.status == GrantStatus.APPROVED]
        )
        rejected = len(
            [app for app in applications if app.status == GrantStatus.REJECTED]
        )
        draft = len([app for app in applications if app.status == GrantStatus.DRAFT])

        success_rate = (approved / total * 100) if total > 0 else 0

        return {
            "total_applications": total,
            "submitted": submitted,
            "approved": approved,
            "rejected": rejected,
            "draft": draft,
            "success_rate": round(success_rate, 2),
        }
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to get statistics: {str(e)}"
        )
