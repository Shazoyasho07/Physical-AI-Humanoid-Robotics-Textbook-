"""
RAG (Retrieval-Augmented Generation) service layer for business logic
"""
import uuid
from typing import List, Optional
import hashlib
import json
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from .. import models, schemas
from ..db.session import get_db
from ..qdrant.client import qdrant_client
from langchain_community.vectorstores import Qdrant
from langchain_openai import OpenAIEmbeddings
from ..config import settings


# Simple in-memory cache for embeddings (in production, use Redis or similar)
# Format: {cache_key: (content, expiry_time)}
embedding_cache = {}


def get_cache_key(textbook_id: str, query: str) -> str:
    """Generate a unique cache key for a textbook query"""
    content = f"{textbook_id}:{query}"
    return hashlib.md5(content.encode()).hexdigest()


def get_cached_result(cache_key: str):
    """Get cached result if it exists and hasn't expired"""
    if cache_key in embedding_cache:
        content, expiry = embedding_cache[cache_key]
        if datetime.now() < expiry:
            return content
        else:
            # Remove expired entry
            del embedding_cache[cache_key]
    return None


def cache_result(cache_key: str, content, ttl_minutes: int = 60):
    """Cache a result with TTL"""
    expiry = datetime.now() + timedelta(minutes=ttl_minutes)
    embedding_cache[cache_key] = (content, expiry)


def create_rag_index(db: Session, rag_index_request: schemas.RAGIndexCreate):
    """Create a RAG index for a textbook"""
    # Get the textbook to ensure it exists
    textbook = db.query(models.Textbook).filter(
        models.Textbook.id == rag_index_request.textbook_id
    ).first()
    
    if not textbook:
        return None
    
    # Create a new RAG index record in the database
    rag_index = models.RAGIndex(
        textbook_id=rag_index_request.textbook_id,
        qdrant_collection_id=f"textbook_{rag_index_request.textbook_id}_collection",
        status=models.RAGIndexStatusEnum.processing,
        embedding_model=rag_index_request.embedding_model
    )
    
    db.add(rag_index)
    db.commit()
    db.refresh(rag_index)
    
    try:
        # Process textbook content into embeddings
        process_textbook_for_rag(db, textbook.id)
        
        # Update the RAG index status to 'ready'
        rag_index.status = models.RAGIndexStatusEnum.ready
        db.commit()
        db.refresh(rag_index)
    except Exception as e:
        # If there's an error, mark the index as failed
        rag_index.status = models.RAGIndexStatusEnum.failed
        db.commit()
        raise e
    
    return rag_index


def process_textbook_for_rag(db: Session, textbook_id: str):
    """Process textbook content into vector embeddings for RAG"""
    # Get the textbook and its chapters
    textbook = db.query(models.Textbook).filter(
        models.Textbook.id == textbook_id
    ).first()

    if not textbook:
        raise ValueError("Textbook not found")

    chapters = textbook.chapters

    # Prepare content for embedding with size optimization
    documents = []
    for chapter in chapters:
        # Break large chapters into smaller chunks for embedding size optimization
        content_chunks = chunk_text(chapter.content, max_chunk_size=1000)  # Free tier limit friendly

        for i, chunk in enumerate(content_chunks):
            # Create a document for each chunk
            from langchain.schema import Document
            doc = Document(
                page_content=chunk,
                metadata={
                    "chapter_id": chapter.id,
                    "chapter_title": chapter.title,
                    "chapter_number": chapter.chapter_number,
                    "textbook_id": textbook.id,
                    "textbook_title": textbook.title,
                    "chunk_number": i,
                    "total_chunks": len(content_chunks)
                }
            )
            documents.append(doc)

    # Initialize the embedding model
    embeddings = OpenAIEmbeddings(
        openai_api_key=settings.llm_provider_api_key,
        model=settings.embedding_model_name
    )

    # Create the Qdrant vector store
    qdrant = Qdrant.from_documents(
        documents,
        embeddings,
        url=settings.qdrant_url,
        collection_name=f"textbook_{textbook_id}_collection",
        api_key=settings.qdrant_api_key,
    )

    return True


def chunk_text(text: str, max_chunk_size: int = 1000) -> List[str]:
    """
    Break text into smaller chunks to optimize for embedding size limits
    """
    if len(text) <= max_chunk_size:
        return [text]

    chunks = []
    paragraphs = text.split('\n\n')

    current_chunk = ""
    for paragraph in paragraphs:
        # If adding the paragraph would exceed the limit
        if len(current_chunk) + len(paragraph) > max_chunk_size:
            # If current chunk is not empty, save it
            if current_chunk.strip():
                chunks.append(current_chunk.strip())
                current_chunk = ""

            # If the paragraph itself is too large, split it by sentences
            if len(paragraph) > max_chunk_size:
                sentences = paragraph.split('. ')
                temp_chunk = ""
                for sentence in sentences:
                    if len(temp_chunk) + len(sentence) + 2 <= max_chunk_size:
                        temp_chunk += sentence + '. '
                    else:
                        if temp_chunk.strip():
                            chunks.append(temp_chunk.strip())
                        temp_chunk = sentence + '. '

                if temp_chunk.strip():
                    current_chunk = temp_chunk.strip()
            else:
                current_chunk = paragraph
        else:
            current_chunk += '\n\n' + paragraph

    # Add the last chunk if it exists
    if current_chunk.strip():
        chunks.append(current_chunk.strip())

    return chunks


def query_textbook_content(
    db: Session,
    textbook_id: str,
    query: str,
    user_id: Optional[str] = None
) -> Optional[schemas.RAGQueryResponse]:
    """Query textbook content using RAG and return the response"""
    # Generate cache key and check for cached result
    cache_key = get_cache_key(textbook_id, query)
    cached_result = get_cached_result(cache_key)
    if cached_result:
        return cached_result

    # Get the RAG index for this textbook
    rag_index = db.query(models.RAGIndex).filter(
        models.RAGIndex.textbook_id == textbook_id
    ).first()

    if not rag_index or rag_index.status != models.RAGIndexStatusEnum.ready:
        return None

    # Initialize the embedding model
    embeddings = OpenAIEmbeddings(
        openai_api_key=settings.llm_provider_api_key,
        model=settings.embedding_model_name
    )

    # Connect to the Qdrant collection for this textbook
    qdrant = Qdrant(
        url=settings.qdrant_url,
        collection_name=rag_index.qdrant_collection_id,
        embeddings=embeddings,
        api_key=settings.qdrant_api_key,
    )

    # Perform similarity search
    search_results = qdrant.similarity_search_with_score(query, k=5)

    # Prepare sources from search results
    sources = []
    for doc, score in search_results:
        source = schemas.RAGSource(
            chapter_id=doc.metadata.get("chapter_id", ""),
            chapter_title=doc.metadata.get("chapter_title", ""),
            page_reference=f"Chapter {doc.metadata.get('chapter_number', 'N/A')}"
        )
        sources.append(source)

    # For simplicity, we'll return a basic response
    # In a real implementation, you would use an LLM to generate the response
    # based on the retrieved documents and the original query
    response_text = f"Based on the textbook content, here's the answer to your question: {query}"

    response = schemas.RAGQueryResponse(
        query=query,
        response=response_text,
        sources=sources,
        confidence=min(len(sources) * 0.2, 1.0)  # Simple confidence calculation
    )

    # Cache the result to reduce API calls
    cache_result(cache_key, response)

    return response