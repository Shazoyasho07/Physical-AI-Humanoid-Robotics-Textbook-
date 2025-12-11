#!/usr/bin/env python3
"""
Health check script for AI-Native Textbook with RAG Chatbot
This script verifies the health of both backend and frontend components
"""

import requests
import sys
import os
from urllib.parse import urljoin
import json


def check_backend_health(backend_url):
    """
    Check the health of the backend service
    """
    try:
        health_url = urljoin(backend_url, "/health")
        response = requests.get(health_url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "healthy":
                print(f"[SUCCESS] Backend is healthy: {data}")
                return True
            else:
                print(f"[WARNING] Backend is unhealthy: {data}")
                return False
        else:
            print(f"[ERROR] Backend health check failed with status {response.status_code}")
            return False
    except Exception as e:
        print(f"[ERROR] Error checking backend health: {str(e)}")
        return False


def check_textbook_api(backend_url):
    """
    Check if the textbook API is accessible
    """
    try:
        # Check if we can access textbooks (without specific ID, should return an error that's expected)
        textbooks_url = urljoin(backend_url, "/api/v1/textbooks/some-id/chapters")
        response = requests.get(textbooks_url, timeout=10)
        
        # We expect a 404 or 422 for an invalid textbook ID, but not a connection error
        if response.status_code in [404, 422]:
            print("[SUCCESS] Textbook API is accessible")
            return True
        elif response.status_code == 200:
            print("[SUCCESS] Textbook API is accessible (returned 200)")
            return True
        else:
            print(f"[WARNING] Textbook API returned unexpected status: {response.status_code}")
            return True  # Still consider as accessible since it responded
    except Exception as e:
        print(f"[ERROR] Error checking textbook API: {str(e)}")
        return False


def check_rag_api(backend_url):
    """
    Check if the RAG API is accessible
    """
    try:
        # Try to access the RAG endpoint with a simple query (expecting a 404 for invalid textbook ID)
        rag_url = urljoin(backend_url, "/api/v1/textbook/some-id/query")
        response = requests.post(
            rag_url,
            json={"query": "test"},
            timeout=10
        )
        
        # We expect a 404 for invalid textbook ID or possibly 422 for validation error, but not connection error
        if response.status_code in [404, 422, 400]:
            print("[SUCCESS] RAG API is accessible")
            return True
        elif response.status_code == 200:
            print("[SUCCESS] RAG API is accessible (returned 200)")
            return True
        else:
            print(f"[WARNING] RAG API returned unexpected status: {response.status_code}")
            return True  # Still consider as accessible since it responded
    except Exception as e:
        print(f"[ERROR] Error checking RAG API: {str(e)}")
        return False


def check_api_usage(backend_url):
    """
    Check if the API usage endpoint is accessible
    """
    try:
        usage_url = urljoin(backend_url, "/usage")
        response = requests.get(usage_url, timeout=10)
        
        if response.status_code in [200, 401, 403]:  # 401/403 are expected without proper auth
            print("[SUCCESS] API usage endpoint is accessible")
            return True
        else:
            print(f"[WARNING] API usage endpoint returned unexpected status: {response.status_code}")
            return True
    except Exception as e:
        print(f"[ERROR] Error checking API usage endpoint: {str(e)}")
        return False


def check_frontend(backend_url):
    """
    Check if frontend would be able to access backend (by checking API accessibility)
    """
    print("[INFO] Frontend health check: verifying API accessibility from frontend perspective")
    return (
        check_textbook_api(backend_url) and
        check_rag_api(backend_url) and
        check_api_usage(backend_url)
    )


def main():
    # Get backend URL from environment or use default
    backend_url = os.environ.get("BACKEND_URL", "http://localhost:8000")
    print(f"[INFO] Checking health of system with backend URL: {backend_url}")

    # Run all checks
    backend_healthy = check_backend_health(backend_url)
    if not backend_healthy:
        print("[ERROR] Backend is not healthy, stopping checks")
        sys.exit(1)

    api_healthy = (
        check_textbook_api(backend_url) and
        check_rag_api(backend_url) and
        check_api_usage(backend_url)
    )

    frontend_healthy = check_frontend(backend_url)

    # Overall health
    overall_healthy = backend_healthy and api_healthy and frontend_healthy

    if overall_healthy:
        print("\n[SUCCESS] All systems are healthy!")
        sys.exit(0)
    else:
        print("\n[ERROR] Some systems are not healthy!")
        sys.exit(1)


if __name__ == "__main__":
    main()