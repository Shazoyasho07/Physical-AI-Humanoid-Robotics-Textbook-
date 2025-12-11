"""
User preference service layer for business logic
"""
import json
from sqlalchemy.orm import Session
from .. import models
from ..schemas import TextbookResponse


def get_user_preferences(db: Session, user_id: str, textbook_id: str):
    """Get user preferences for a specific textbook"""
    preference = db.query(models.UserPreference).filter(
        models.UserPreference.user_id == user_id,
        models.UserPreference.textbook_id == textbook_id
    ).first()
    
    return preference


def create_or_update_user_preferences(db: Session, user_id: str, textbook_id: str, selected_chapters: list):
    """Create or update user preferences for a specific textbook"""
    # Try to find existing preference
    preference = db.query(models.UserPreference).filter(
        models.UserPreference.user_id == user_id,
        models.UserPreference.textbook_id == textbook_id
    ).first()
    
    if preference:
        # Update existing preference
        preference.selected_chapters = json.dumps(selected_chapters)
    else:
        # Create new preference
        preference = models.UserPreference(
            user_id=user_id,
            textbook_id=textbook_id,
            selected_chapters=json.dumps(selected_chapters)
        )
        db.add(preference)
    
    db.commit()
    db.refresh(preference)
    return preference


def get_selected_chapters(db: Session, user_id: str, textbook_id: str):
    """Get the list of selected chapters for a user and textbook"""
    preference = get_user_preferences(db, user_id, textbook_id)
    if not preference or not preference.selected_chapters:
        return []
    
    try:
        return json.loads(preference.selected_chapters)
    except json.JSONDecodeError:
        return []


def get_filtered_chapters(db: Session, textbook_id: str, user_id: str = None):
    """Get chapters, filtered by user preferences if provided"""
    # Get all chapters for the textbook
    from ..services.textbook_service import get_textbook_chapters
    all_chapters = get_textbook_chapters(db, textbook_id)
    
    if not user_id:
        return all_chapters
    
    # Get user's selected chapters
    selected_chapter_ids = get_selected_chapters(db, user_id, textbook_id)
    
    if not selected_chapter_ids:
        return all_chapters
    
    # Filter chapters based on user preferences
    filtered_chapters = [
        chapter for chapter in all_chapters 
        if chapter.id in selected_chapter_ids
    ]
    
    # Maintain the order specified by the user
    ordered_chapters = []
    for chapter_id in selected_chapter_ids:
        for chapter in all_chapters:
            if chapter.id == chapter_id:
                ordered_chapters.append(chapter)
                break
    
    return ordered_chapters