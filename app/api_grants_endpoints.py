# ---------------------
# FastAPI Endpoints (FIXED VERSION)
# ---------------------

from fastapi import APIRouter, HTTPException
from datetime import datetime
from .grants import (
    grant_service,
    GrantCategory,
    logger
)

router = APIRouter()


@router.get("/api/grants")
async def get_grants():
    """Get all grants with proper data source validation"""
    try:
        grants_data = grant_service.get_all_grants()
        # Add data_source field to each grant for frontend validation
        grants_with_source = []
        for grant in grants_data:
            grant_dict = grant.dict()  # ✅ FIXED - with parentheses
            grant_dict["data_source"] = "api"  # ✅ CRITICAL FIX
            grants_with_source.append(grant_dict)
        
        logger.info(f"Retrieved {len(grants_with_source)} grants from API")
        return {"grants": grants_with_source, "total": len(grants_with_source)}
    except Exception as e:
        logger.error(f"Error in get_grants endpoint: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve grants: {str(e)}")

@router.get("/api/grants/{grant_id}")
async def get_grant_by_id(grant_id: str):
    """Get specific grant by ID"""
    try:
        grant = grant_service.get_grant_by_id(grant_id)
        if grant is None:
            raise HTTPException(status_code=404, detail="Grant not found")
        
        grant_dict = grant.dict()  # ✅ FIXED - with parentheses
        grant_dict["data_source"] = "api"  # ✅ Add data source
        return grant_dict
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in get_grant_by_id endpoint: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve grant: {str(e)}")

@router.post("/api/grants/search")
async def search_grants(search_filters: dict):
    """Search grants with filters"""
    try:
        keywords = search_filters.get("keywords")
        category = search_filters.get("category")
        min_amount = search_filters.get("min_amount")
        max_amount = search_filters.get("max_amount")
        deadline_before = search_filters.get("deadline_before")
        
        # Convert deadline_before string to datetime if provided
        if deadline_before and isinstance(deadline_before, str):
            try:
                deadline_before = datetime.fromisoformat(deadline_before.replace('Z', '+00:00'))
            except ValueError:
                raise HTTPException(status_code=400, detail="Invalid deadline format")
        
        # Convert category string to enum if provided
        if category and isinstance(category, str):
            try:
                category = GrantCategory(category)
            except ValueError:
                raise HTTPException(status_code=400, detail="Invalid category")
        
        results = grant_service.search_grants(
            keywords=keywords,
            category=category,
            min_amount=min_amount,
            max_amount=max_amount,
            deadline_before=deadline_before
        )
        
        # Add data_source to each result
        grants_with_source = []
        for grant in results:
            grant_dict = grant.dict()  # ✅ FIXED - with parentheses
            grant_dict["data_source"] = "api"  # ✅ Add data source
            grants_with_source.append(grant_dict)
        
        return {
            "grants": grants_with_source,
            "total_results": len(grants_with_source),
            "filters_applied": search_filters
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in search_grants endpoint: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to search grants: {str(e)}")

@router.post("/api/grants/recommendations")
async def get_recommendations(user_profile: dict):
    """Get AI-powered grant recommendations"""
    try:
        if not user_profile:
            raise HTTPException(status_code=400, detail="User profile is required")
        
        recommendations = grant_service.get_recommended_grants(user_profile)
        
        # Add data_source to each recommendation
        recommendations_with_source = []
        for grant in recommendations:
            grant_dict = grant.dict()  # ✅ FIXED - with parentheses
            grant_dict["data_source"] = "api"  # ✅ Add data source
            recommendations_with_source.append(grant_dict)
        
        return {
            "recommendations": recommendations_with_source,
            "total_recommendations": len(recommendations_with_source)
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in get_recommendations endpoint: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get recommendations: {str(e)}")

@router.get("/api/grants/categories")
async def get_categories():
    """Get all available grant categories"""
    try:
        categories = [category.value for category in GrantCategory]
        return {"categories": categories, "total": len(categories)}
    except Exception as e:
        logger.error(f"Error in get_categories endpoint: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve categories: {str(e)}")

@router.get("/api/grant-applications")
async def get_applications():
    """Get all grant applications (placeholder for now)"""
    try:
        # For now, return empty list since applications_db is empty
        return {
            "applications": [],
            "total_applications": 0
        }
    except Exception as e:
        logger.error(f"Error in get_applications endpoint: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve applications: {str(e)}")

@router.post("/api/grant-applications")
async def create_application(application_data: dict):
    """Create a new grant application"""
    try:
        grant_id = application_data.get("grant_id")
        title = application_data.get("title")
        assigned_to = application_data.get("assigned_to")
        collaborators = application_data.get("collaborators", [])
        
        if not all([grant_id, title, assigned_to]):
            raise HTTPException(status_code=400, detail="Missing required fields")
        
        application = grant_service.create_application(
            grant_id=grant_id,
            title=title,
            assigned_to=assigned_to,
            collaborators=collaborators
        )
        
        return application.dict()  # ✅ FIXED - with parentheses
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in create_application endpoint: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to create application: {str(e)}")

@router.post("/api/grant-applications/{application_id}/answers")
async def update_application_answer(application_id: str, answer_data: dict):
    """Update or create an answer for a grant application"""
    try:
        question = answer_data.get("question")
        answer = answer_data.get("answer")
        author = answer_data.get("author")
        
        if not all([question, answer, author]):
            raise HTTPException(status_code=400, detail="Missing required fields")
        
        result = grant_service.update_application_answer(
            application_id=application_id,
            question=question,
            answer=answer,
            author=author
        )
        
        return result.dict()  # ✅ FIXED - with parentheses
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in update_application_answer endpoint: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to update answer: {str(e)}")

@router.post("/api/grant-applications/{application_id}/comments")
async def add_application_comment(application_id: str, comment_data: dict):
    """Add a comment to a grant application"""
    try:
        content = comment_data.get("content")
        author = comment_data.get("author")
        
        if not all([content, author]):
            raise HTTPException(status_code=400, detail="Missing required fields")
        
        comment = grant_service.add_comment(
            application_id=application_id,
            content=content,
            author=author
        )
        
        return comment.dict()  # ✅ FIXED - with parentheses
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in add_application_comment endpoint: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to add comment: {str(e)}")

@router.post("/api/grant-applications/{application_id}/submit")
async def submit_application(application_id: str):
    """Submit a grant application"""
    try:
        success = grant_service.submit_application(application_id)
        if not success:
            raise HTTPException(status_code=404, detail="Application not found")
        
        return {"message": "Application submitted successfully", "application_id": application_id}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in submit_application endpoint: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to submit application: {str(e)}")