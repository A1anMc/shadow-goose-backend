import json
import uuid
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from pydantic import BaseModel, Field, validator
from enum import Enum

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

class Grant(BaseModel):
    id: str = Field(..., description="Unique grant identifier")
    title: str = Field(..., description="Grant title")
    description: str = Field(..., description="Grant description")
    amount: float = Field(..., gt=0, description="Grant amount in AUD")
    deadline: datetime = Field(..., description="Application deadline")
    category: GrantCategory = Field(..., description="Grant category")
    eligibility: List[str] = Field(default_factory=list, description="Eligibility criteria")
    requirements: List[str] = Field(default_factory=list, description="Application requirements")
    contact_info: Dict[str, str] = Field(..., description="Contact information")
    website: str = Field(..., description="Grant website URL")
    source: str = Field(..., description="Grant source organisation")
    success_score: float = Field(default=0.0, ge=0.0, le=1.0, description="AI success probability score")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Creation timestamp")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="Last update timestamp")

    @validator('amount')
    def validate_amount(cls, v):
        if v <= 0:
            raise ValueError('Grant amount must be positive')
        return round(v, 2)  # Ensure precision to 2 decimal places

    @validator('success_score')
    def validate_success_score(cls, v):
        if not 0.0 <= v <= 1.0:
            raise ValueError('Success score must be between 0.0 and 1.0')
        return round(v, 3)  # Ensure precision to 3 decimal places

    def format_amount_aud(self) -> str:
        """Format amount in Australian Dollar format"""
        try:
            return f"AUD ${self.amount:,.2f}"
        except Exception as e:
            logger.error(f"Error formatting amount {self.amount}: {e}")
            return f"AUD ${self.amount:.2f}"

    def format_deadline_uk(self) -> str:
        """Format deadline in UK date format"""
        try:
            return self.deadline.strftime("%d/%m/%Y")
        except Exception as e:
            logger.error(f"Error formatting deadline {self.deadline}: {e}")
            return "Invalid date"

class GrantApplication(BaseModel):
    id: str = Field(..., description="Unique application identifier")
    grant_id: str = Field(..., description="Associated grant ID")
    title: str = Field(..., description="Application title")
    status: GrantStatus = Field(default=GrantStatus.DRAFT, description="Application status")
    priority: GrantPriority = Field(default=GrantPriority.MEDIUM, description="Application priority")
    assigned_to: str = Field(..., description="Primary assignee")
    collaborators: List[str] = Field(default_factory=list, description="Team collaborators")
    answers: Dict[str, str] = Field(default_factory=dict, description="Application answers")
    documents: List[str] = Field(default_factory=list, description="Attached documents")
    budget: float = Field(default=0.0, ge=0.0, description="Project budget in AUD")
    timeline: str = Field(default="", description="Project timeline")
    impact_statement: str = Field(default="", description="Impact statement")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Creation timestamp")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="Last update timestamp")
    submitted_at: Optional[datetime] = Field(default=None, description="Submission timestamp")

    @validator('budget')
    def validate_budget(cls, v):
        if v < 0:
            raise ValueError('Budget cannot be negative')
        return round(v, 2)  # Ensure precision to 2 decimal places

    def format_budget_aud(self) -> str:
        """Format budget in Australian Dollar format"""
        try:
            return f"AUD ${self.budget:,.2f}"
        except Exception as e:
            logger.error(f"Error formatting budget {self.budget}: {e}")
            return f"AUD ${self.budget:.2f}"

class GrantAnswer(BaseModel):
    id: str = Field(..., description="Unique answer identifier")
    application_id: str = Field(..., description="Associated application ID")
    question: str = Field(..., description="Question text")
    answer: str = Field(..., description="Answer text")
    author: str = Field(..., description="Answer author")
    version: int = Field(..., ge=1, description="Answer version number")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Creation timestamp")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="Last update timestamp")

class GrantComment(BaseModel):
    id: str = Field(..., description="Unique comment identifier")
    application_id: str = Field(..., description="Associated application ID")
    author: str = Field(..., description="Comment author")
    content: str = Field(..., description="Comment content")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Creation timestamp")

# In-memory storage for testing (will be replaced with database)
grants_db: List[Grant] = []
applications_db: List[GrantApplication] = []
answers_db: List[GrantAnswer] = []
comments_db: List[GrantComment] = []

# Sample grants data with proper AUD amounts
SAMPLE_GRANTS = [
    {
        "id": "grant_001",
        "title": "Victorian Creative Industries Grant",
        "description": "Supporting creative projects that contribute to Victoria's cultural landscape",
        "amount": 50000.00,
        "deadline": datetime.now() + timedelta(days=30),
        "category": GrantCategory.ARTS_CULTURE,
        "eligibility": ["Non-profit organisations", "Creative businesses", "Individual artists"],
        "requirements": ["Project proposal", "Budget breakdown", "Timeline", "Impact assessment"],
        "contact_info": {"email": "grants@creative.vic.gov.au", "phone": "03 8683 3100"},
        "website": "https://creative.vic.gov.au/grants",
        "source": "Creative Victoria",
        "success_score": 0.850,
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    },
    {
        "id": "grant_002",
        "title": "Community Impact Fund",
        "description": "Supporting community projects that create positive social impact",
        "amount": 25000.00,
        "deadline": datetime.now() + timedelta(days=45),
        "category": GrantCategory.COMMUNITY,
        "eligibility": ["Community organisations", "Social enterprises", "Non-profits"],
        "requirements": ["Community consultation", "Impact measurement plan", "Partnership details"],
        "contact_info": {"email": "impact@community.gov.au", "phone": "03 9208 3333"},
        "website": "https://community.gov.au/impact-fund",
        "source": "Department of Communities",
        "success_score": 0.920,
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    },
    {
        "id": "grant_003",
        "title": "Youth Innovation Grant",
        "description": "Supporting innovative projects led by young people",
        "amount": 15000.00,
        "deadline": datetime.now() + timedelta(days=60),
        "category": GrantCategory.YOUTH,
        "eligibility": ["Youth-led organisations", "Young entrepreneurs", "Youth groups"],
        "requirements": ["Youth leadership", "Innovation component", "Community benefit"],
        "contact_info": {"email": "youth@innovation.gov.au", "phone": "03 9208 4444"},
        "website": "https://youth.gov.au/innovation-grant",
        "source": "Youth Affairs Victoria",
        "success_score": 0.780,
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    }
]

# Initialize sample data
for grant_data in SAMPLE_GRANTS:
    try:
        grants_db.append(Grant(**grant_data))
        logger.info(f"Initialised grant: {grant_data['title']}")
    except Exception as e:
        logger.error(f"Error initialising grant {grant_data['title']}: {e}")

class GrantService:
    @staticmethod
    def get_all_grants() -> List[Grant]:
        """Get all available grants"""
        try:
            logger.info(f"Retrieved {len(grants_db)} grants")
            return grants_db
        except Exception as e:
            logger.error(f"Error retrieving grants: {e}")
            return []
    
    @staticmethod
    def get_grant_by_id(grant_id: str) -> Optional[Grant]:
        """Get a specific grant by ID"""
        try:
            for grant in grants_db:
                if grant.id == grant_id:
                    logger.info(f"Retrieved grant: {grant.title}")
                    return grant
            logger.warning(f"Grant not found: {grant_id}")
            return None
        except Exception as e:
            logger.error(f"Error retrieving grant {grant_id}: {e}")
            return None
    
    @staticmethod
    def search_grants(
        category: Optional[GrantCategory] = None,
        min_amount: Optional[float] = None,
        max_amount: Optional[float] = None,
        deadline_before: Optional[datetime] = None,
        keywords: Optional[str] = None
    ) -> List[Grant]:
        """Search grants with filters"""
        try:
            results = grants_db.copy()
            
            if category:
                results = [g for g in results if g.category == category]
            
            if min_amount is not None:
                results = [g for g in results if g.amount >= min_amount]
            
            if max_amount is not None:
                results = [g for g in results if g.amount <= max_amount]
            
            if deadline_before:
                results = [g for g in results if g.deadline <= deadline_before]
            
            if keywords:
                keywords_lower = keywords.lower()
                results = [g for g in results if 
                          keywords_lower in g.title.lower() or 
                          keywords_lower in g.description.lower()]
            
            # Sort by success score (highest first)
            results.sort(key=lambda x: x.success_score, reverse=True)
            
            logger.info(f"Grant search returned {len(results)} results")
            return results
        except Exception as e:
            logger.error(f"Error searching grants: {e}")
            return []
    
    @staticmethod
    def get_recommended_grants(user_profile: Dict) -> List[Grant]:
        """Get AI-recommended grants based on user profile"""
        try:
            recommendations = []
            
            for grant in grants_db:
                score = 0.0
                
                # Category preference
                if user_profile.get("preferred_categories") and grant.category in user_profile["preferred_categories"]:
                    score += 0.3
                
                # Amount range
                if user_profile.get("min_amount") and grant.amount >= user_profile["min_amount"]:
                    score += 0.2
                if user_profile.get("max_amount") and grant.amount <= user_profile["max_amount"]:
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
        collaborators: List[str] = None
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
                updated_at=datetime.now()
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
                app for app in applications_db 
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
        application_id: str,
        question: str,
        answer: str,
        author: str
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
                    updated_at=datetime.now()
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
                    updated_at=datetime.now()
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
    def add_comment(
        application_id: str,
        content: str,
        author: str
    ) -> GrantComment:
        """Add a comment to a grant application"""
        try:
            comment = GrantComment(
                id=str(uuid.uuid4()),
                application_id=application_id,
                author=author,
                content=content,
                created_at=datetime.now()
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
            logger.info(f"Retrieved {len(result)} comments for application {application_id}")
            return result
        except Exception as e:
            logger.error(f"Error retrieving comments for application {application_id}: {e}")
            return []
    
    @staticmethod
    def get_application_answers(application_id: str) -> List[GrantAnswer]:
        """Get all answers for an application"""
        try:
            result = [a for a in answers_db if a.application_id == application_id]
            logger.info(f"Retrieved {len(result)} answers for application {application_id}")
            return result
        except Exception as e:
            logger.error(f"Error retrieving answers for application {application_id}: {e}")
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

# Global grant service instance
grant_service = GrantService() 