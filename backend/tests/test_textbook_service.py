"""
Unit tests for the textbook service
"""
import pytest
from unittest.mock import MagicMock, patch
from sqlalchemy.orm import Session
from src.services import textbook_service
from src import models


class TestTextbookService:
    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.mock_db = MagicMock(spec=Session)
        
        # Create a mock textbook
        self.mock_textbook = models.Textbook(
            id="test-textbook-id",
            title="Test Textbook",
            description="A test textbook",
            author_id="test-author-id"
        )
        
        # Create a mock chapter
        self.mock_chapter = models.Chapter(
            id="test-chapter-id",
            title="Test Chapter",
            content="This is test content",
            chapter_number=1,
            textbook_id="test-textbook-id"
        )

    @patch('src.services.textbook_service.get_textbook')
    def test_get_textbook_chapters_success(self, mock_get_textbook):
        """Test getting textbook chapters successfully"""
        # Arrange
        mock_get_textbook.return_value = self.mock_textbook
        self.mock_textbook.chapters = [self.mock_chapter]
        
        # Act
        result = textbook_service.get_textbook_chapters(self.mock_db, "test-textbook-id")
        
        # Assert
        assert result == [self.mock_chapter]
        mock_get_textbook.assert_called_once_with(self.mock_db, "test-textbook-id")

    @patch('src.services.textbook_service.get_textbook')
    def test_get_textbook_chapters_textbook_not_found(self, mock_get_textbook):
        """Test getting chapters when textbook doesn't exist"""
        # Arrange
        mock_get_textbook.return_value = None
        
        # Act
        result = textbook_service.get_textbook_chapters(self.mock_db, "nonexistent-textbook-id")
        
        # Assert
        assert result == []

    def test_create_chapter_success(self):
        """Test creating a chapter successfully"""
        # Arrange
        from src.schemas import ChapterCreate
        chapter_create = ChapterCreate(
            title="New Chapter",
            content="New chapter content",
            chapter_number=2,
            textbook_id="test-textbook-id"
        )
        
        # Mock the textbook query
        mock_textbook_query = MagicMock()
        mock_textbook_query.filter.return_value.first.return_value = self.mock_textbook
        with patch.object(self.mock_db, 'query', return_value=mock_textbook_query):
            # Act
            result = textbook_service.create_chapter(self.mock_db, chapter_create)
        
        # Assert
        assert result is not None
        assert result.title == "New Chapter"
        assert result.textbook_id == "test-textbook-id"
        self.mock_db.add.assert_called()
        self.mock_db.commit.assert_called()
        self.mock_db.refresh.assert_called()

    def test_create_chapter_textbook_not_found(self):
        """Test creating a chapter when textbook doesn't exist"""
        # Arrange
        from src.schemas import ChapterCreate
        chapter_create = ChapterCreate(
            title="New Chapter",
            content="New chapter content",
            chapter_number=2,
            textbook_id="nonexistent-textbook-id"
        )
        
        # Mock the textbook query to return None
        mock_textbook_query = MagicMock()
        mock_textbook_query.filter.return_value.first.return_value = None
        with patch.object(self.mock_db, 'query', return_value=mock_textbook_query):
            # Act
            result = textbook_service.create_chapter(self.mock_db, chapter_create)
        
        # Assert
        assert result is None