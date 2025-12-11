# Data Model: AI-Native Textbook with RAG Chatbot

## Entities

### Textbook
- **id**: UUID (primary key)
- **title**: string (e.g., "Physical AI & Humanoid Robotics — Essentials")
- **description**: text
- **version**: string
- **created_at**: timestamp
- **updated_at**: timestamp
- **author_id**: UUID (foreign key to User)

### Chapter
- **id**: UUID (primary key)
- **title**: string (e.g., "Introduction to Physical AI", "Basics of Humanoid Robotics", etc.)
- **content**: text (markdown format)
- **chapter_number**: integer
- **textbook_id**: UUID (foreign key to Textbook)
- **created_at**: timestamp
- **updated_at**: timestamp

### User
- **id**: UUID (primary key)
- **email**: string (unique)
- **name**: string
- **user_type**: enum ( educator, student )
- **created_at**: timestamp
- **updated_at**: timestamp

### UserPreference
- **id**: UUID (primary key)
- **user_id**: UUID (foreign key to User)
- **textbook_id**: UUID (foreign key to Textbook)
- **selected_chapters**: array of UUIDs (references to Chapter.id)
- **language_preference**: string (default: "en")
- **created_at**: timestamp
- **updated_at**: timestamp

### RAGIndex
- **id**: UUID (primary key)
- **textbook_id**: UUID (foreign key to Textbook)
- **qdrant_collection_id**: string (identifier in Qdrant)
- **status**: enum (processing, ready, failed)
- **embedding_model**: string (name of the model used)
- **created_at**: timestamp
- **updated_at**: timestamp

## Relationships

- Textbook (1) → Chapter (many): A textbook contains multiple chapters
- User (1) → UserPreference (many): A user can have preferences for multiple textbooks
- Textbook (1) → UserPreference (many): A textbook can have preferences from multiple users
- Textbook (1) → RAGIndex (1): A textbook has one associated RAG index

## Validation Rules

- Textbook title must be between 5-100 characters
- Chapter content must be valid markdown format
- Chapter numbers within a textbook must be unique and sequential
- User email must be valid and unique
- A textbook must have at least 1 chapter and no more than 100 chapters
- The RAGIndex status must be one of the defined values

## State Transitions

- RAGIndex can transition from 'processing' to either 'ready' or 'failed'
- Textbook can have version updates that update the 'updated_at' timestamp