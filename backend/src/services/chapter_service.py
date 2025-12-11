"""
Chapter service layer for business logic
"""
from sqlalchemy.orm import Session
from .. import models
from ..schemas import ChapterCreate, ChapterUpdate


def get_chapter(db: Session, chapter_id: str):
    """Get a chapter by ID"""
    return db.query(models.Chapter).filter(models.Chapter.id == chapter_id).first()


def get_chapter_by_number(db: Session, textbook_id: str, chapter_number: int):
    """Get a chapter by textbook ID and chapter number"""
    return db.query(models.Chapter).filter(
        models.Chapter.textbook_id == textbook_id,
        models.Chapter.chapter_number == chapter_number
    ).first()


def create_chapter(db: Session, chapter: ChapterCreate):
    """Create a new chapter in a textbook"""
    # Verify the textbook exists
    textbook = db.query(models.Textbook).filter(models.Textbook.id == chapter.textbook_id).first()
    if not textbook:
        return None
    
    # Check if a chapter with this number already exists in the textbook
    existing_chapter = get_chapter_by_number(db, chapter.textbook_id, chapter.chapter_number)
    if existing_chapter:
        return None  # Or raise an exception, depending on requirements
    
    db_chapter = models.Chapter(
        title=chapter.title,
        content=chapter.content,
        chapter_number=chapter.chapter_number,
        textbook_id=chapter.textbook_id
    )
    
    db.add(db_chapter)
    db.commit()
    db.refresh(db_chapter)
    return db_chapter


def update_chapter(db: Session, chapter_id: str, chapter_update: ChapterUpdate):
    """Update an existing chapter"""
    db_chapter = get_chapter(db, chapter_id)
    if not db_chapter:
        return None
    
    for key, value in chapter_update.dict(exclude_unset=True).items():
        setattr(db_chapter, key, value)
    
    db.commit()
    db.refresh(db_chapter)
    return db_chapter


def delete_chapter(db: Session, chapter_id: str):
    """Delete a chapter by ID"""
    db_chapter = get_chapter(db, chapter_id)
    if not db_chapter:
        return False
    
    db.delete(db_chapter)
    db.commit()
    return True