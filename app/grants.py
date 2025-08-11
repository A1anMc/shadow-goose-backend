import json
import uuid
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from pydantic import BaseModel
from enum import Enum

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
    id: str
    title: str
    description: str
    amount: float
    deadline: datetime
    category: GrantCategory
    eligibility: List[str]
    requirements: List[str]
    contact_info: Dict[str, str]
    website: str
    source: str
    success_score: float = 0.0
    created_at: datetime
    updated_at: datetime

class GrantApplication(BaseModel):
    id: str
    grant_id: str
    title: str
    status: GrantStatus
    priority: GrantPriority
    assigned_to: str
    collaborators: List[str]
    answers: Dict[str, str]
    documents: List[str]
    budget: float
    timeline: str
    impact_statement: str
    created_at: datetime
    updated_at: datetime
    submitted_at: Optional[datetime] = None

class GrantAnswer(BaseModel):
    id: str
    application_id: str
    question: str
    answer: str
    author: str
    version: int
    created_at: datetime
    updated_at: datetime

class GrantComment(BaseModel):
    id: str
    application_id: str
    author: str
    content: str
    created_at: datetime

# In-memory storage (will be replaced with database)
grants_db = []
applications_db = []
answers_db = []
comments_db = []

# Sample grants data
SAMPLE_GRANTS = [
    {
        "id": "grant_001",
        "title": "Victorian Creative Industries Grant",
        "description": "Supporting creative projects that contribute to Victoria's cultural landscape",
        "amount": 50000,
        "deadline": datetime.now() + timedelta(days=30),
        "category": GrantCategory.ARTS_CULTURE,
        "eligibility": ["Non-profit organizations", "Creative businesses", "Individual artists"],
        "requirements": ["Project proposal", "Budget breakdown", "Timeline", "Impact assessment"],
        "contact_info": {"email": "grants@creative.vic.gov.au", "phone": "03 8683 3100"},
        "website": "https://creative.vic.gov.au/grants",
        "source": "Creative Victoria",
        "success_score": 0.85,
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    },
    {
        "id": "grant_002",
        "title": "Community Impact Fund",
        "description": "Supporting community projects that create positive social impact",
        "amount": 25000,
        "deadline": datetime.now() + timedelta(days=45),
        "category": GrantCategory.COMMUNITY,
        "eligibility": ["Community organizations", "Social enterprises", "Non-profits"],
        "requirements": ["Community consultation", "Impact measurement plan", "Partnership details"],
        "contact_info": {"email": "impact@community.gov.au", "phone": "03 9208 3333"},
        "website": "https://community.gov.au/impact-fund",
        "source": "Department of Communities",
        "success_score": 0.92,
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    },
    {
        "id": "grant_003",
        "title": "Youth Innovation Grant",
        "description": "Supporting innovative projects led by young people",
        "amount": 15000,
        "deadline": datetime.now() + timedelta(days=60),
        "category": GrantCategory.YOUTH,
        "eligibility": ["Youth-led organizations", "Young entrepreneurs", "Youth groups"],
        "requirements": ["Youth leadership", "Innovation component", "Community benefit"],
        "contact_info": {"email": "youth@innovation.gov.au", "phone": "03 9208 4444"},
        "website": "https://youth.gov.au/innovation-grant",
        "source": "Youth Affairs Victoria",
        "success_score": 0.78,
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    }
]

# Initialize sample data
for grant_data in SAMPLE_GRANTS:
    grants_db.append(Grant(**grant_data))

class GrantService:
    @staticmethod
    def get_all_grants() -> List[Grant]:
        """Get all available grants"""
        return grants_db
    
    @staticmethod
    def get_grant_by_id(grant_id: str) -> Optional[Grant]:
        """Get a specific grant by ID"""
        for grant in grants_db:
            if grant.id == grant_id:
                return grant
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
        results = grants_db.copy()
        
        if category:
            results = [g for g in results if g.category == category]
        
        if min_amount:
            results = [g for g in results if g.amount >= min_amount]
        
        if max_amount:
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
        return results
    
    @staticmethod
    def get_recommended_grants(user_profile: Dict) -> List[Grant]:
        """Get AI-recommended grants based on user profile"""
        # Simple recommendation algorithm (can be enhanced with ML)
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
        return [grant for grant, score in recommendations[:10]]
    
    @staticmethod
    def create_application(
        grant_id: str,
        title: str,
        assigned_to: str,
        collaborators: List[str] = None
    ) -> GrantApplication:
        """Create a new grant application"""
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
        return application
    
    @staticmethod
    def get_applications_by_user(user_id: str) -> List[GrantApplication]:
        """Get all applications for a user (assigned or collaborating)"""
        return [
            app for app in applications_db 
            if app.assigned_to == user_id or user_id in app.collaborators
        ]
    
    @staticmethod
    def get_application_by_id(application_id: str) -> Optional[GrantApplication]:
        """Get a specific application by ID"""
        for app in applications_db:
            if app.id == application_id:
                return app
        return None
    
    @staticmethod
    def update_application_answer(
        application_id: str,
        question: str,
        answer: str,
        author: str
    ) -> GrantAnswer:
        """Update or create an answer for a grant application"""
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
        
        return new_answer
    
    @staticmethod
    def add_comment(
        application_id: str,
        content: str,
        author: str
    ) -> GrantComment:
        """Add a comment to a grant application"""
        comment = GrantComment(
            id=str(uuid.uuid4()),
            application_id=application_id,
            author=author,
            content=content,
            created_at=datetime.now()
        )
        
        comments_db.append(comment)
        return comment
    
    @staticmethod
    def get_application_comments(application_id: str) -> List[GrantComment]:
        """Get all comments for an application"""
        return [c for c in comments_db if c.application_id == application_id]
    
    @staticmethod
    def get_application_answers(application_id: str) -> List[GrantAnswer]:
        """Get all answers for an application"""
        return [a for a in answers_db if a.application_id == application_id]
    
    @staticmethod
    def submit_application(application_id: str) -> bool:
        """Submit a grant application"""
        for app in applications_db:
            if app.id == application_id:
                app.status = GrantStatus.SUBMITTED
                app.submitted_at = datetime.now()
                app.updated_at = datetime.now()
                return True
        return False

# Global grant service instance
grant_service = GrantService() 