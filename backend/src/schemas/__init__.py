"""
Pydantic schemas for request/response validation
"""
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import uuid


# Textbook schemas
class TextbookBase(BaseModel):
    title: str
    description: Optional[str] = None


class TextbookCreate(TextbookBase):
    author_id: str


class TextbookUpdate(TextbookBase):
    pass


class TextbookResponse(TextbookBase):
    id: str
    author_id: str
    version: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Chapter schemas
class ChapterBase(BaseModel):
    title: str
    content: str
    chapter_number: int


class ChapterCreate(ChapterBase):
    textbook_id: str


class ChapterUpdate(ChapterBase):
    pass


class ChapterResponse(ChapterBase):
    id: str
    textbook_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ChaptersResponse(BaseModel):
    chapters: List[ChapterResponse]


# User schemas
class UserBase(BaseModel):
    email: str
    name: str


class UserCreate(UserBase):
    user_type: str


class UserResponse(UserBase):
    id: str
    user_type: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# RAG Query schemas
class RAGQueryRequest(BaseModel):
    query: str
    user_id: Optional[str] = None


class RAGSource(BaseModel):
    chapter_id: str
    chapter_title: str
    page_reference: str


class RAGQueryResponse(BaseModel):
    query: str
    response: str
    sources: List[RAGSource]
    confidence: float


# RAG Index schemas
class RAGIndexCreate(BaseModel):
    textbook_id: str
    embedding_model: str


class RAGIndexResponse(BaseModel):
    id: str
    textbook_id: str
    qdrant_collection_id: str
    status: str
    embedding_model: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True