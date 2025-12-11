#!/bin/bash
# build-backend.sh - Production build script for backend

# Exit on any error
set -e

echo "Starting backend production build..."

# Navigate to the backend directory
cd backend

# Install dependencies using poetry
echo "Installing dependencies..."
pip install poetry
poetry export -o requirements.txt -f requirements.txt --without-hashes
pip install -r requirements.txt

# Verify the required modules are available
python -c "import fastapi, uvicorn, sqlalchemy, qdrant_client, langchain" || {
    echo "Error: Required packages not installed properly"
    exit 1
}

echo "Backend build process completed."