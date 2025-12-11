"""
API endpoints for RAG (Retrieval-Augmented Generation) functionality
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db.session import get_db
from .. import schemas
from ..services import rag_service


router = APIRouter()


@router.post("/textbook/{textbook_id}/query", response_model=schemas.RAGQueryResponse)
async def query_textbook(
    textbook_id: str,
    query_request: schemas.RAGQueryRequest,
    db: Session = Depends(get_db)
):
    """Query the textbook content using RAG"""
    try:
        response = rag_service.query_textbook_content(
            db, textbook_id, query_request.query, query_request.user_id
        )
        if not response:
            raise HTTPException(status_code=404, detail="Textbook not found or RAG index not ready")
        return response
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.post("/rag-index", response_model=schemas.RAGIndexResponse)
async def create_rag_index(
    rag_index_request: schemas.RAGIndexCreate,
    db: Session = Depends(get_db)
):
    """Create a RAG index for a textbook"""
    try:
        rag_index = rag_service.create_rag_index(db, rag_index_request)
        if not rag_index:
            raise HTTPException(status_code=404, detail="Textbook not found")
        return rag_index
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")