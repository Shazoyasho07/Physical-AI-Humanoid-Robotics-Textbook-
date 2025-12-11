"""
Logging configuration for the textbook generation backend
"""
import logging
import sys
from .config import settings


def setup_logging():
    """Configure logging for the application"""
    # Set the logging level based on configuration
    log_level = getattr(logging, settings.log_level.upper(), logging.INFO)
    
    # Configure root logger
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout),  # Log to stdout
            # In production, you might also want to log to a file
        ]
    )
    
    # Set lower log levels for specific libraries if needed
    logging.getLogger("uvicorn").setLevel(log_level)
    logging.getLogger("sqlalchemy").setLevel(logging.WARNING)  # Reduce SQLAlchemy noise


# Set up logging when the module is imported
setup_logging()


def get_logger(name: str) -> logging.Logger:
    """Get a logger with the specified name"""
    return logging.getLogger(name)