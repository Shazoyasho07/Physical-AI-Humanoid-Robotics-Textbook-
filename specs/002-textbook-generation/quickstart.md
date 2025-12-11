# Quickstart Guide: AI-Native Textbook with RAG Chatbot

## Prerequisites

- Python 3.11 or higher
- Node.js 18 or higher
- Git
- Access to a free-tier Neon PostgreSQL account
- Access to a free-tier Qdrant account
- An API key for your preferred LLM provider (e.g., OpenAI, Anthropic)

## Setup Instructions

### 1. Clone the Repository

```bash
git clone <repository-url>
cd <repository-name>
```

### 2. Backend Setup

```bash
# Navigate to the backend directory
cd backend

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your specific configuration values
```

### 3. Frontend Setup

```bash
# Navigate to the frontend directory
cd frontend

# Install dependencies
npm install

# Set up environment variables
cp .env.example .env
# Edit .env with your specific configuration values
```

### 4. Database Setup

```bash
# In the backend directory with activated virtual environment
cd src

# Run database migrations
python -m scripts.migrate
```

### 5. Vector Database Setup

```bash
# Ensure Qdrant is running (locally or via cloud)
# For local setup:
docker run -d --name qdrant -p 6333:6333 -p 6334:6334 qdrant/qdrant
```

## Running the Application

### 1. Start the Backend Server

```bash
cd backend
source venv/bin/activate  # On Windows: venv\Scripts\activate
python -m src.main
```

### 2. Start the Frontend

```bash
cd frontend
npm start
```

## Adding Textbook Content

1. Navigate to the `docs` directory in your project
2. Add or modify content for each chapter
3. The sidebar navigation will auto-generate based on the chapter structure
4. Run the textbook generation process:
   ```bash
   cd backend
   python -m scripts.generate_textbook
   ```

## Setting up RAG for a Textbook

1. Make sure your textbook content is in the system
2. Create the vector embeddings for RAG:
   ```bash
   cd backend
   python -m scripts.create_rag_index
   ```
3. This will process the textbook content and create the necessary vector database entries

## Testing the RAG Chatbot

1. With the backend running, you can test the API endpoint:
   ```bash
   curl -X POST http://localhost:8000/api/v1/rag/query \
   -H "Content-Type: application/json" \
   -d '{
     "textbook_id": "<your-textbook-id>",
     "query": "Your question about the textbook content"
   }'
   ```

## Configuration

Key environment variables to configure:

- `NEON_DATABASE_URL`: Connection string for your Neon PostgreSQL database
- `QDRANT_URL`: URL for your Qdrant vector database
- `LLM_PROVIDER_API_KEY`: API key for your LLM provider
- `EMBEDDING_MODEL_NAME`: Name of the embedding model to use (e.g., text-embedding-3-small)

## Building for Production

```bash
# Frontend
cd frontend
npm run build

# Backend (create a distribution)
cd backend
python -m pip install pyinstaller
pyinstaller --onefile src/main.py
```

Your textbook application will be available at http://localhost:3000 (frontend) and the API at http://localhost:8000 (backend).