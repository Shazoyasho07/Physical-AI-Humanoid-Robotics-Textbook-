"""
Database models and schema for the textbook generation backend
"""
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, ForeignKey, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import event
from datetime import datetime
import enum
import uuid
import re

Base = declarative_base()

class UserTypeEnum(enum.Enum):
    educator = "educator"
    student = "student"

class RAGIndexStatusEnum(enum.Enum):
    processing = "processing"
    ready = "ready"
    failed = "failed"

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    user_type = Column(Enum(UserTypeEnum), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def validate(self):
        """Validate user data"""
        if not re.match(r"[^@]+@[^@]+\.[^@]+", self.email):
            raise ValueError("Invalid email format")

        if not self.name or len(self.name.strip()) == 0:
            raise ValueError("Name is required")

        return True

class Textbook(Base):
    __tablename__ = "textbooks"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String, nullable=False)
    description = Column(Text)
    version = Column(String, default="1.0.0")
    author_id = Column(String, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship
    chapters = relationship("Chapter", back_populates="textbook", cascade="all, delete-orphan")
    rag_index = relationship("RAGIndex", back_populates="textbook", uselist=False, cascade="all, delete-orphan")
    user_preferences = relationship("UserPreference", back_populates="textbook")

    def validate(self):
        """Validate textbook data"""
        if not self.title or len(self.title.strip()) < 5 or len(self.title.strip()) > 100:
            raise ValueError("Title must be between 5-100 characters")

        return True

class Chapter(Base):
    __tablename__ = "chapters"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)  # Markdown format
    chapter_number = Column(Integer, nullable=False)
    textbook_id = Column(String, ForeignKey("textbooks.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship
    textbook = relationship("Textbook", back_populates="chapters")

    def validate(self):
        """Validate chapter data"""
        if not self.title or len(self.title.strip()) == 0:
            raise ValueError("Chapter title is required")

        if not self.content or len(self.content.strip()) == 0:
            raise ValueError("Chapter content is required")

        if self.chapter_number < 1:
            raise ValueError("Chapter number must be greater than 0")

        # Check if content is valid markdown format (basic check)
        if not isinstance(self.content, str):
            raise ValueError("Chapter content must be a string")

        return True

class UserPreference(Base):
    __tablename__ = "user_preferences"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    textbook_id = Column(String, ForeignKey("textbooks.id"), nullable=False)
    selected_chapters = Column(Text)  # JSON string of chapter IDs
    language_preference = Column(String, default="en")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User")
    textbook = relationship("Textbook", back_populates="user_preferences")

class RAGIndex(Base):
    __tablename__ = "rag_indices"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    textbook_id = Column(String, ForeignKey("textbooks.id"), nullable=False, unique=True)
    qdrant_collection_id = Column(String, nullable=False)
    status = Column(Enum(RAGIndexStatusEnum), default=RAGIndexStatusEnum.processing)
    embedding_model = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship
    textbook = relationship("Textbook", back_populates="rag_index")

    def validate(self):
        """Validate RAG index data"""
        if self.status not in RAGIndexStatusEnum:
            raise ValueError("Invalid RAG index status")

        return True

# Validation events for models
@event.listens_for(Textbook, 'before_insert')
@event.listens_for(Textbook, 'before_update')
def validate_textbook(mapper, connection, target):
    target.validate()

@event.listens_for(Chapter, 'before_insert')
@event.listens_for(Chapter, 'before_update')
def validate_chapter(mapper, connection, target):
    target.validate()

@event.listens_for(User, 'before_insert')
@event.listens_for(User, 'before_update')
def validate_user(mapper, connection, target):
    target.validate()

@event.listens_for(RAGIndex, 'before_insert')
@event.listens_for(RAGIndex, 'before_update')
def validate_rag_index(mapper, connection, target):
    target.validate()