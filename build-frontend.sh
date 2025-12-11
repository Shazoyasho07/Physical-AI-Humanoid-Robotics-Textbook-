#!/bin/bash
# build-frontend.sh - Production build script for frontend

# Exit on any error
set -e

echo "Starting frontend production build..."

# Navigate to the frontend directory
cd frontend

# Install dependencies
echo "Installing dependencies..."
npm ci --production=false

# Build the application
echo "Building application..."
npm run build

# Verify the build completed successfully
if [ -d "build" ]; then
    echo "Build completed successfully!"
    echo "Build output is in the 'build' directory"
    ls -la build/
else
    echo "Build failed - no build directory created"
    exit 1
fi

echo "Frontend build process completed."