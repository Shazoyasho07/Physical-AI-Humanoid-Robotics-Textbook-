# AI-Native Textbook with RAG Chatbot - Production Deployment

This repository contains a complete AI-Native Textbook system with RAG (Retrieval-Augmented Generation) chatbot functionality. This document provides instructions for deploying the system to production.

## Architecture

The system consists of two main components:
- **Backend**: FastAPI application handling business logic, database operations, and RAG functionality
- **Frontend**: Docusaurus-based textbook interface with RAG chatbot component

## Prerequisites

Before deploying, ensure you have:

- A PostgreSQL database (recommended: Neon)
- A Qdrant vector database (recommended: Qdrant Cloud)
- An LLM provider API key (e.g., OpenAI)
- GitHub account for frontend hosting
- Railway account for backend hosting

## Deployment Steps

### 1. Backend Deployment (Railway)

1. **Prepare Environment Variables**:
   - Create a Neon PostgreSQL database
   - Set up Qdrant Cloud account
   - Obtain your LLM provider API key

2. **Deploy to Railway**:
   - Connect your GitHub repository to Railway
   - Add your environment variables:
     ```
     DATABASE_URL=postgresql+asyncpg://...
     QDRANT_URL=...
     QDRANT_API_KEY=...
     LLM_PROVIDER_API_KEY=...
     EMBEDDING_MODEL_NAME=text-embedding-3-small
     APP_ENV=production
     LOG_LEVEL=INFO
     ```
   - Deploy the application

3. **Verify Backend**:
   - Access the health check endpoint: `GET /health`
   - Verify the API is responding correctly

### 2. Frontend Deployment (GitHub Pages)

1. **Update Configuration**:
   - Modify `frontend/.env.production` to point to your backend API:
     ```
     REACT_APP_API_BASE_URL=https://your-backend-app.railway.app
     ```

2. **Build and Deploy**:
   - The GitHub Actions workflow will automatically build and deploy the frontend to GitHub Pages when changes are pushed to the main branch
   - The workflow is defined in `.github/workflows/deploy-frontend.yml`

### 3. Environment Variables

#### Backend (Railway)
```
DATABASE_URL=postgresql+asyncpg://username:password@ep-xxx.us-east-1.aws.neon.tech/textbook_db
QDRANT_URL=https://your-cluster.qdrant.tech
QDRANT_API_KEY=your_qdrant_api_key
LLM_PROVIDER_API_KEY=your_openai_api_key
EMBEDDING_MODEL_NAME=text-embedding-3-small
APP_ENV=production
LOG_LEVEL=INFO
```

#### Frontend (GitHub Pages via Actions)
```
REACT_APP_API_BASE_URL=https://your-backend-app.railway.app
```

## Health Checks

### Backend Health Check
- Endpoint: `GET /health`
- Expected Response:
  ```json
  {
    "status": "healthy",
    "version": "0.1.0"
  }
  ```

### Frontend Health Check
- Visit the deployed site URL
- Verify the RAG chatbot component loads and connects to the backend

## Monitoring and Maintenance

### Backend Monitoring
- Monitor response times for API endpoints
- Track database connection health
- Monitor Qdrant connection status
- Track API usage metrics

### Frontend Monitoring
- Monitor page load performance
- Track API call success/failure rates
- Monitor user interaction metrics

## Troubleshooting

### Common Issues

1. **Environment Variables Not Loading**
   - Verify all environment variables are correctly set in Railway
   - Check that domain names are correctly configured

2. **Database Connection Issues**
   - Verify PostgreSQL connection string format
   - Check if Neon database is active and accessible

3. **Qdrant Connection Issues**
   - Verify QDRANT_URL and QDRANT_API_KEY are correct
   - Ensure the Qdrant cluster is running

4. **Frontend Cannot Connect to Backend**
   - Verify REACT_APP_API_BASE_URL is set correctly
   - Check CORS settings in the backend

### API Endpoints

- `GET /health`: Backend health check
- `GET /api/v1/textbooks/{id}/chapters`: Get textbook chapters
- `POST /api/v1/textbook/{id}/query`: Query textbook content via RAG
- `GET /usage`: API usage statistics

## Development and Local Testing

For local development, use the provided docker-compose file:

```bash
# Start all services
docker-compose up

# Access the services:
# Backend: http://localhost:8000
# Frontend: http://localhost:3000
# Database: http://localhost:5432
# Qdrant: http://localhost:6333
```

## Security Considerations

- All API endpoints should be secured with appropriate authentication
- Database connections should use SSL
- API keys should be properly secured and rotated regularly
- Implement rate limiting to prevent abuse
- Regular security scanning of dependencies

## Rollback Plan

- Backend: Use Railway's deployment history to revert to a previous version
- Frontend: Maintain previous build in a separate branch for quick rollback

## Support

For issues with the deployment, please check the logs in Railway and GitHub Actions. For system issues, contact the development team.