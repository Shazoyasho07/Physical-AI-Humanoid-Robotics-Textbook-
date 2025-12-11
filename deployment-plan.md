# Production Deployment Plan: AI-Native Textbook with RAG Chatbot

## Overview
This document outlines the production deployment of the AI-Native Textbook with RAG Chatbot, including both frontend (Docusaurus) and backend (FastAPI) components with appropriate hosting, CI/CD workflows, and monitoring.

## Architecture
- **Frontend**: Docusaurus static site deployed to GitHub Pages
- **Backend**: FastAPI application deployed to Railway
- **Database**: PostgreSQL on Neon
- **Vector Store**: Qdrant Cloud
- **CDN**: GitHub Pages CDN for frontend assets

## Deployment Steps

### Backend Deployment (Railway)

1. **Prepare Backend for Production**
   - Create production-ready requirements.txt
   - Set up environment variables management
   - Configure production database connection
   - Add health checks endpoint
   - Implement proper logging configuration

2. **Railway Setup**
   - Create Railway account and new project
   - Configure the deployment to pull from GitHub
   - Set environment variables (see section below)
   - Configure domain name for the backend API
   - Set up auto-deploy from main branch

3. **Backend Configuration**
   - Health check endpoint: /health
   - Proper error handling and logging
   - Rate limiting for API endpoints
   - Security headers and CORS configuration

### Frontend Deployment (GitHub Pages)

1. **Prepare Frontend for Production**
   - Update API base URL to production backend
   - Build static assets with `npm run build`
   - Ensure proper routing for GitHub Pages
   - Optimize build size and performance

2. **GitHub Pages Setup**
   - Enable GitHub Pages in repository settings
   - Set source to `/docs` folder or `gh-pages` branch
   - Configure custom domain if needed
   - Set up GitHub Actions workflow for CI/CD

3. **Frontend Configuration**
   - Update REACT_APP_API_BASE_URL to production backend
   - Add appropriate meta tags and SEO configuration
   - Include proper error boundaries

## Environment Variables

### Backend (Railway)
```
DATABASE_URL=postgresql+asyncpg://username:password@ep-xxx.us-east-1.aws.neon.tech/textbook_db
QDRANT_URL=https://your-cluster.qdrant.tech
QDRANT_API_KEY=your_qdrant_api_key
LLM_PROVIDER_API_KEY=your_openai_api_key
EMBEDDING_MODEL_NAME=text-embedding-3-small
APP_ENV=production
LOG_LEVEL=INFO
```

### Frontend (GitHub Pages)
```
REACT_APP_API_BASE_URL=https://your-backend-app.railway.app
```

## Health Checks

### Backend Health Checks
- Endpoint: `GET /health`
- Response: `{"status": "healthy", "version": "x.x.x"}`
- Monitoring: Set up uptime monitoring for the health endpoint

### Frontend Health Checks
- Monitor GitHub Pages site availability
- Check that API endpoints are accessible from frontend domain

## Launch Checklist

### Pre-Launch
- [ ] Database schema migration completed
- [ ] Vector database (Qdrant) collection created and tested
- [ ] API keys properly configured and tested
- [ ] Frontend build completes successfully
- [ ] End-to-end functionality tested
- [ ] Performance benchmarks verified
- [ ] Security review completed
- [ ] SSL certificates configured

### Launch Day
- [ ] Deploy backend first
- [ ] Verify backend health and functionality
- [ ] Deploy frontend
- [ ] Update DNS records if using custom domains
- [ ] Monitor for any issues during first hour of operation
- [ ] Verify all API endpoints are working correctly

### Post-Launch
- [ ] Monitor system performance
- [ ] Set up alerts for errors or downtime
- [ ] Gather user feedback
- [ ] Document any issues encountered during deployment
- [ ] Update documentation with production details

## CI/CD Workflows

### Backend Deployment Workflow (Railway)
- Auto-deploy on pushes to main branch
- Run tests before deployment
- Environment: production

### Frontend Deployment Workflow (GitHub Actions)
```yaml
name: Deploy to GitHub Pages
on:
  push:
    branches: [main]
  workflow_dispatch:

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v3
      
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
      
      - name: Install dependencies
        run: npm ci
      
      - name: Build
        run: npm run build
        env:
          REACT_APP_API_BASE_URL: https://your-backend-app.railway.app
      
      - name: Deploy to GitHub Pages
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./build
```

## Monitoring & Maintenance

### Backend Monitoring
- Response time tracking
- Error rate monitoring
- Database connection health
- Qdrant connection status
- API usage metrics

### Frontend Monitoring
- Page load performance
- User interaction tracking
- API call success/failure rates

## Rollback Plan
- Backend: Use Railway's deployment history to revert to a previous version
- Frontend: Maintain previous build in a separate branch for quick rollback

## Security Considerations
- Implement proper authentication for API endpoints
- Secure database connections with SSL
- Validate and sanitize all inputs
- Implement rate limiting to prevent abuse
- Regular security scanning of dependencies