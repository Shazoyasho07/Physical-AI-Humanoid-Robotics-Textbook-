"""
Main FastAPI application with API routing structure
"""
import hashlib
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from .api import textbook, rag, user_preferences
from .logging_config import setup_logging
from .monitoring.api_monitor import check_api_limits, get_api_usage_stats


def get_api_key_hash(request: Request) -> str:
    """Extract and hash the API key from the request"""
    api_key = request.headers.get("Authorization", "").replace("Bearer ", "")
    if api_key:
        return hashlib.md5(api_key.encode()).hexdigest()
    return "anonymous"


def create_app():
    """Create and configure the FastAPI application"""
    # Set up logging
    setup_logging()

    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        description="Backend API for AI-Native Textbook with RAG Chatbot",
        contact={
            "name": "Textbook Generation Team",
            "email": settings.admin_email,
        },
        license_info={
            "name": "MIT License",
            "url": "https://opensource.org/licenses/MIT",
        },
    )

    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # In production, replace with specific origins
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # API rate limiting middleware
    @app.middleware("http")
    async def api_rate_limiting(request: Request, call_next):
        # Skip rate limiting for health checks and root endpoint
        if request.url.path in ["/", "/health"]:
            response = await call_next(request)
            return response

        # Get API key hash and check limits
        api_key_hash = get_api_key_hash(request)
        if not check_api_limits(api_key_hash):
            from fastapi.responses import JSONResponse
            return JSONResponse(
                status_code=429,
                content={"detail": "Rate limit exceeded"}
            )

        response = await call_next(request)
        return response

    # Include API routers
    app.include_router(textbook.router, prefix="/api/v1", tags=["textbook"])
    app.include_router(rag.router, prefix="/api/v1", tags=["rag"])
    app.include_router(user_preferences.router, prefix="/api/v1", tags=["user-preferences"])

    @app.get("/")
    async def root():
        return {"message": "Welcome to the Textbook Generation Backend API"}

    @app.get("/health")
    async def health_check():
        return {"status": "healthy", "version": settings.app_version}

    @app.get("/usage")
    async def usage_check(request: Request):
        api_key_hash = get_api_key_hash(request)
        stats = get_api_usage_stats(api_key_hash)
        return stats

    return app


app = create_app()