"""
API endpoints for textbook management
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db.session import get_db
from .. import models, schemas
from ..services import textbook_service


router = APIRouter()


@router.get("/textbooks/{textbook_id}", response_model=schemas.TextbookResponse)
async def get_textbook(textbook_id: str, db: Session = Depends(get_db)):
    """Get a specific textbook by ID"""
    textbook = textbook_service.get_textbook(db, textbook_id)
    if not textbook:
        raise HTTPException(status_code=404, detail="Textbook not found")
    return textbook


@router.get("/textbooks/{textbook_id}/chapters", response_model=schemas.ChaptersResponse)
async def get_textbook_chapters(textbook_id: str, db: Session = Depends(get_db)):
    """Get all chapters for a specific textbook"""
    chapters = textbook_service.get_textbook_chapters(db, textbook_id)
    if not chapters:
        raise HTTPException(status_code=404, detail="Textbook not found or has no chapters")
    return {"chapters": chapters}