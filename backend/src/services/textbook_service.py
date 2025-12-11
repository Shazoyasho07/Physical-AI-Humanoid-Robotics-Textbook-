"""
Textbook service layer for business logic
"""
from sqlalchemy.orm import Session, joinedload
from .. import models
from ..schemas import TextbookCreate, TextbookUpdate, ChapterCreate, ChapterUpdate


def get_textbook(db: Session, textbook_id: str):
    """Get a textbook by ID"""
    return db.query(models.Textbook).filter(models.Textbook.id == textbook_id).first()


def get_textbook_with_chapters(db: Session, textbook_id: str):
    """Get a textbook with its chapters in a single optimized query"""
    return db.query(models.Textbook).filter(
        models.Textbook.id == textbook_id
    ).options(
        joinedload(models.Textbook.chapters)
    ).first()


def get_textbook_chapters(db: Session, textbook_id: str):
    """Get all chapters for a specific textbook with optimized query"""
    from sqlalchemy.orm import joinedload
    textbook = db.query(models.Textbook).filter(
        models.Textbook.id == textbook_id
    ).options(
        joinedload(models.Textbook.chapters)
    ).first()

    if not textbook:
        return []
    return textbook.chapters


def create_textbook(db: Session, textbook: TextbookCreate):
    """Create a new textbook"""
    db_textbook = models.Textbook(
        title=textbook.title,
        description=textbook.description,
        author_id=textbook.author_id
    )
    db.add(db_textbook)
    db.commit()
    db.refresh(db_textbook)
    return db_textbook


def update_textbook(db: Session, textbook_id: str, textbook_update: TextbookUpdate):
    """Update an existing textbook"""
    db_textbook = get_textbook(db, textbook_id)
    if not db_textbook:
        return None
    
    for key, value in textbook_update.dict(exclude_unset=True).items():
        setattr(db_textbook, key, value)
    
    db.commit()
    db.refresh(db_textbook)
    return db_textbook


def create_chapter(db: Session, chapter: ChapterCreate):
    """Create a new chapter in a textbook"""
    # Verify the textbook exists
    textbook = get_textbook(db, chapter.textbook_id)
    if not textbook:
        return None
    
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
    db_chapter = db.query(models.Chapter).filter(models.Chapter.id == chapter_id).first()
    if not db_chapter:
        return None
    
    for key, value in chapter_update.dict(exclude_unset=True).items():
        setattr(db_chapter, key, value)
    
    db.commit()
    db.refresh(db_chapter)
    return db_chapter