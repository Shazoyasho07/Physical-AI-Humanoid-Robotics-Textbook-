# Railway Deployment Configuration

This configuration file outlines the setup for deploying the backend to Railway.

## Railway Configuration

### 1. Railway.json Configuration
Create a `railway.json` file at the root of the backend:

```json
{
  "projectId": "",
  "name": "textbook-generation-backend",
  "region": "us-east1",
  "deployments": {
    "autoDeploy": true,
    "redployOnPush": true,
    "numDaysToKeep": 30
  },
  "build": {
    "builder": "NIXPACKS",
    "nixpacksPlan": {
      "phases": {
        "setup": {
          "nixPkgs": ["python311", "pip", "gcc", "g++", "cmake", "pkg-config"]
        },
        "install": {
          "cmd": [
            "pip install poetry",
            "poetry export -o requirements.txt -f requirements.txt --without-hashes",
            "pip install -r requirements.txt"
          ]
        },
        "build": {
          "cmd": [
            "echo 'Build complete'"
          ]
        },
        "start": {
          "cmd": [
            "cd backend && uvicorn src.main:app --host 0.0.0.0 --port $PORT"
          ]
        }
      },
      "variables": {
        "PYTHONPATH": "/app/backend/src"
      }
    }
  },
  "env": {
    "DATABASE_URL": {
      "description": "PostgreSQL database URL",
      "required": true
    },
    "QDRANT_URL": {
      "description": "Qdrant vector database URL",
      "required": true
    },
    "QDRANT_API_KEY": {
      "description": "Qdrant API key",
      "required": true
    },
    "LLM_PROVIDER_API_KEY": {
      "description": "OpenAI or other LLM provider API key",
      "required": true
    },
    "EMBEDDING_MODEL_NAME": {
      "description": "Embedding model name",
      "default": "text-embedding-3-small"
    },
    "APP_ENV": {
      "description": "Application environment",
      "default": "production"
    },
    "LOG_LEVEL": {
      "description": "Logging level",
      "default": "INFO"
    }
  }
}
```

### 2. Dockerfile for Railway (Alternative approach)
If using Docker instead of nixpacks, create a Dockerfile:

```Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/src ./src

EXPOSE 8000

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 3. Railway Environment Variables
Required environment variables for deployment:

- DATABASE_URL: PostgreSQL connection string
- QDRANT_URL: Qdrant service URL
- QDRANT_API_KEY: Qdrant access key
- LLM_PROVIDER_API_KEY: OpenAI or other LLM provider API key
- EMBEDDING_MODEL_NAME: Name of the embedding model (default: text-embedding-3-small)
- APP_ENV: Environment (production, staging, etc.)
- LOG_LEVEL: Logging level (INFO, DEBUG, etc.)
```