# Research: AI-Native Textbook with RAG Chatbot

## Decision: Technology Stack
- **Rationale**: Selected Python with FastAPI for the backend due to strong support for AI/RAG applications, LangChain for RAG implementation, Qdrant for vector storage, and Docusaurus for the textbook frontend. These technologies align with the requirements for a free-tier, efficient implementation.
- **Alternatives considered**: 
  - Node.js/JavaScript stack for full-stack consistency
  - Different vector databases like Pinecone or Weaviate
  - Alternative static site generators like Gatsby or Next.js
  - Different RAG frameworks like Haystack or LlamaIndex

## Decision: Textbook Generation Approach
- **Rationale**: Using Docusaurus with its built-in sidebar generation capabilities provides automatic navigation for the 6 textbook chapters. Docusaurus is well-suited for documentation-style content, which matches the textbook format.
- **Alternatives considered**:
  - Custom React-based solution
  - Static site generators like Jekyll or Hugo
  - Custom-built solution with different frameworks

## Decision: RAG Implementation
- **Rationale**: LangChain provides a comprehensive framework for building RAG systems with good integration options for various LLMs and vector databases. Qdrant was selected as it provides a good free-tier option with efficient similarity search capabilities.
- **Alternatives considered**:
  - Haystack framework
  - LlamaIndex
  - Custom RAG implementation from scratch
  - Different vector databases (Pinecone, Weaviate, Chroma)

## Decision: Free-tier Architecture
- **Rationale**: Selected Neon for PostgreSQL hosting and Qdrant for vector storage based on their free-tier availability and capabilities. Both meet the performance requirements while staying within budget constraints.
- **Alternatives considered**:
  - PostgreSQL on alternative providers (Supabase, PlanetScale)
  - Free-tier options on major cloud providers
  - Different database solutions for metadata storage

## Decision: Performance Optimization
- **Rationale**: Implementation will focus on efficient embeddings generation and caching to stay within free-tier limits while meeting the 3-second response time requirement for the RAG chatbot.
- **Alternatives considered**:
  - More complex caching strategies
  - Different embedding models for better performance
  - Pre-computed embeddings vs. on-demand generation