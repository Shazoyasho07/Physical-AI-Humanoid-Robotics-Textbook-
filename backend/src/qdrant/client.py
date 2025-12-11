"""
Qdrant client configuration for the textbook generation backend
"""
from qdrant_client import QdrantClient
from .config import settings


def get_qdrant_client():
    """Create and return a Qdrant client instance"""
    client = QdrantClient(
        url=settings.qdrant_url,
        api_key=settings.qdrant_api_key,
        prefer_grpc=False  # Using HTTP for simplicity, can switch to gRPC for production
    )
    return client


# Create a global client instance
qdrant_client = get_qdrant_client()