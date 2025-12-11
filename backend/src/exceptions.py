"""
Custom exception classes for the textbook generation backend
"""


class TextbookGenerationException(Exception):
    """Base exception class for textbook generation errors"""
    def __init__(self, message: str, error_code: str = None):
        self.message = message
        self.error_code = error_code
        super().__init__(self.message)


class TextbookNotFoundException(TextbookGenerationException):
    """Exception raised when a textbook is not found"""
    def __init__(self, textbook_id: str):
        self.textbook_id = textbook_id
        super().__init__(f"Textbook with ID {textbook_id} not found", "TEXTBOOK_NOT_FOUND")


class ChapterNotFoundException(TextbookGenerationException):
    """Exception raised when a chapter is not found"""
    def __init__(self, chapter_id: str):
        self.chapter_id = chapter_id
        super().__init__(f"Chapter with ID {chapter_id} not found", "CHAPTER_NOT_FOUND")


class RAGIndexException(TextbookGenerationException):
    """Exception raised when there's an issue with RAG index"""
    def __init__(self, message: str):
        super().__init__(message, "RAG_INDEX_ERROR")


class ValidationError(TextbookGenerationException):
    """Exception raised when input validation fails"""
    def __init__(self, field: str, message: str):
        self.field = field
        super().__init__(f"Validation error in field '{field}': {message}", "VALIDATION_ERROR")