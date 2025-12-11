"""
Integration tests for API endpoints
"""
import pytest
from fastapi.testclient import TestClient
from src.main import app
from unittest.mock import patch, MagicMock


client = TestClient(app)


class TestTextbookAPI:
    @patch('src.services.textbook_service.get_textbook_chapters')
    def test_get_textbook_chapters_success(self, mock_get_chapters):
        """Test getting textbook chapters API endpoint"""
        # Arrange
        mock_chapters = [
            {
                "id": "test-chapter-id",
                "title": "Test Chapter",
                "content": "Test content",
                "chapter_number": 1,
                "textbook_id": "test-textbook-id",
                "created_at": "2023-01-01T00:00:00",
                "updated_at": "2023-01-01T00:00:00"
            }
        ]
        mock_get_chapters.return_value = mock_chapters

        # Act
        response = client.get("/api/v1/textbooks/test-textbook-id/chapters")

        # Assert
        assert response.status_code == 200
        assert response.json() == {"chapters": mock_chapters}


class TestRAGAPI:
    @patch('src.services.rag_service.query_textbook_content')
    def test_query_textbook_success(self, mock_query_content):
        """Test querying textbook content via API"""
        # Arrange
        mock_response = MagicMock()
        mock_response.query = "test query"
        mock_response.response = "test response"
        mock_response.sources = []
        mock_response.confidence = 0.9
        mock_query_content.return_value = mock_response

        # Act
        response = client.post(
            "/api/v1/textbook/test-textbook-id/query",
            json={"query": "test query"}
        )

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["query"] == "test query"
        assert data["response"] == "test response"
        assert data["confidence"] == 0.9


class TestHealthCheck:
    def test_health_check(self):
        """Test health check endpoint"""
        # Act
        response = client.get("/health")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "version" in data