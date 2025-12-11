"""
Database session management for the textbook generation backend
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

# Create the database engine
engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,  # Verify connections are alive
    pool_recycle=300,    # Recycle connections after 5 minutes
)

# Create a configured "SessionLocal" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a Base class for declarative models
Base = declarative_base()

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()