"""
Unit tests for the RAG service
"""
import pytest
from unittest.mock import MagicMock, patch, mock_open
from sqlalchemy.orm import Session
from src.services import rag_service
from src import models, schemas


class TestRAGService:
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
            content="This is test content for the chapter",
            chapter_number=1,
            textbook_id="test-textbook-id"
        )
        
        # Create a mock RAG index request
        self.rag_index_request = schemas.RAGIndexCreate(
            textbook_id="test-textbook-id",
            embedding_model="text-embedding-3-small"
        )

    def test_chunk_text_small_text(self):
        """Test chunking text that is smaller than the chunk size"""
        # Arrange
        text = "Small text"
        expected_chunks = ["Small text"]

        # Act
        result = rag_service.chunk_text(text, max_chunk_size=100)

        # Assert
        assert result == expected_chunks

    def test_chunk_text_large_text(self):
        """Test chunking text that needs to be split"""
        # Arrange
        text = "First paragraph.\n\nSecond paragraph.\n\nThird paragraph."
        expected_chunks = [
            "First paragraph.",
            "Second paragraph.",
            "Third paragraph."
        ]

        # Act
        result = rag_service.chunk_text(text, max_chunk_size=20)  # Small size to force chunking

        # Assert
        assert result == expected_chunks

    @patch('src.services.rag_service.db')
    def test_process_textbook_for_rag_success(self, mock_db_session):
        """Test processing textbook for RAG successfully"""
        # Arrange
        mock_db_session.query.return_value.filter.return_value.first.return_value = self.mock_textbook
        self.mock_textbook.chapters = [self.mock_chapter]
        
        # Mock the Qdrant client and related imports
        with patch('src.services.rag_service.qdrant_client'), \
             patch('src.services.rag_service.Qdrant'), \
             patch('src.services.rag_service.OpenAIEmbeddings'):
            
            # Act & Assert (should not raise an exception)
            try:
                result = rag_service.process_textbook_for_rag(mock_db_session, "test-textbook-id")
                assert result is True
            except Exception as e:
                pytest.fail(f"process_textbook_for_rag raised {e} unexpectedly!")

    @patch('src.services.rag_service.get_cached_result', return_value=None)
    @patch('src.services.rag_service.cache_result')
    def test_query_textbook_content_not_cached(self, mock_cache_result, mock_get_cached_result):
        """Test querying textbook content when not cached"""
        # Arrange
        mock_db_query = MagicMock()
        mock_db_query.filter.return_value.first.return_value = MagicMock(
            status=models.RAGIndexStatusEnum.ready,
            qdrant_collection_id="test-collection"
        )
        self.mock_db.query.return_value = mock_db_query
        
        # Mock the Qdrant similarity search
        mock_qdrant = MagicMock()
        mock_doc = MagicMock()
        mock_doc.metadata = {
            "chapter_id": "test-chapter-id",
            "chapter_title": "Test Chapter",
            "chapter_number": 1
        }
        mock_qdrant.similarity_search_with_score.return_value = [(mock_doc, 0.9)]
        
        with patch('src.services.rag_service.Qdrant', return_value=mock_qdrant), \
             patch('src.services.rag_service.OpenAIEmbeddings'):
            
            # Act
            result = rag_service.query_textbook_content(
                self.mock_db, 
                "test-textbook-id", 
                "test query"
            )
            
            # Assert
            assert result is not None
            assert result.query == "test query"
            assert len(result.sources) == 1
            assert result.sources[0].chapter_id == "test-chapter-id"
            mock_cache_result.assert_called_once()