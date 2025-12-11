"""
API endpoints for user preferences
"""
import json
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db.session import get_db
from .. import models, schemas
from ..services import user_preference_service


router = APIRouter()


@router.get("/users/{user_id}/textbooks/{textbook_id}/preferences", response_model=schemas.UserPreference)
async def get_user_preferences(
    user_id: str,
    textbook_id: str,
    db: Session = Depends(get_db)
):
    """Get user preferences for a specific textbook"""
    preferences = user_preference_service.get_user_preferences(db, user_id, textbook_id)
    if not preferences:
        raise HTTPException(status_code=404, detail="User preferences not found")
    return preferences


@router.post("/users/{user_id}/textbooks/{textbook_id}/preferences", response_model=schemas.UserPreference)
async def set_user_preferences(
    user_id: str,
    textbook_id: str,
    selected_chapters: list,
    db: Session = Depends(get_db)
):
    """Set user preferences for a specific textbook"""
    preferences = user_preference_service.create_or_update_user_preferences(
        db, user_id, textbook_id, selected_chapters
    )
    return preferences


@router.get("/users/{user_id}/textbooks/{textbook_id}/chapters", response_model=schemas.ChaptersResponse)
async def get_filtered_chapters(
    user_id: str,
    textbook_id: str,
    db: Session = Depends(get_db)
):
    """Get chapters filtered by user preferences"""
    chapters = user_preference_service.get_filtered_chapters(db, textbook_id, user_id)
    if not chapters:
        # If no user ID is provided or no preferences are set, get all chapters
        chapters = user_preference_service.get_filtered_chapters(db, textbook_id)
    return {"chapters": chapters}