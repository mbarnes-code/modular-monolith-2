"""
Dispatch Service - Incident Management and Orchestration Platform
Part of the hybrid domain-based architecture for Mental Prosthetic Platform

This service provides integration with Netflix's Dispatch incident management
platform with full business logic preservation.

Performance Target: <2s response time for incident management workflows
Architecture: Service adapter pattern with business logic preservation
"""

import logging
import warnings
from contextlib import asynccontextmanager
from typing import Any, Dict

from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
# from slowapi import _rate_limit_exceeded_handler
# from slowapi.errors import RateLimitExceeded
from starlette.middleware.gzip import GZipMiddleware

# Filter out Pydantic migration warnings
warnings.filterwarnings("ignore", message=".*has been moved to.*")

# Configure basic logging for now
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

# TODO: Enable when dependencies are resolved
# from .logging import configure_logging
# configure_logging()

# Configure extensions (Sentry, etc.) - TODO: Enable later
# from .extensions import configure_extensions
# configure_extensions()

# Import after logging is configured (disabled for now)
# from .api.api import api_router
# from .api.rate_limiter import limiter

log = logging.getLogger(__name__)


async def not_found(request, exc):
    """Custom 404 handler."""
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": [{"msg": "Not Found."}]}
    )


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan management."""
    log.info("Starting Dispatch Service...")
    
    # Startup logic here if needed
    # e.g., initialize database connections, load plugins, etc.
    
    yield
    
    # Shutdown logic here if needed
    log.info("Shutting down Dispatch Service...")


# Create the main FastAPI application
app = FastAPI(
    title="Dispatch Service API",
    description="Netflix Dispatch incident management integration service",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan
)

# Add exception handlers after app creation
app.add_exception_handler(404, not_found)

# Configure rate limiting (disabled for now)
# app.state.limiter = limiter
# app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Add middleware
app.add_middleware(GZipMiddleware, minimum_size=1000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the main API router (will be enabled when imports are fixed)
# app.include_router(api_router, prefix="/api/v1")


@app.get("/")
async def read_root() -> Dict[str, Any]:
    """Service information endpoint."""
    return {
        "service": "Dispatch Service",
        "status": "running",
        "version": "1.0.0",
        "description": "Netflix Dispatch incident management integration",
        "domain": "incident-management",
        "performance_target": "<2s response time",
        "api_docs": "/docs",
        "api_prefix": "/api/v1",
        "features": [
            "incident_management",
            "case_management",
            "task_orchestration",
            "communication_workflows",
            "post_incident_analysis",
            "tool_integration",
            "cost_tracking",
            "participant_management",
            "document_management",
            "search_and_analytics"
        ]
    }


@app.get("/health")
async def health_check() -> Dict[str, str]:
    """Health check endpoint for monitoring."""
    return {
        "status": "healthy",
        "service": "dispatch-service",
        "version": "1.0.0"
    }


# Legacy compatibility endpoints (placeholders for now)
@app.get("/api/v1/")
async def api_root():
    """API root endpoint."""
    return {
        "message": "Dispatch API v1",
        "docs": "/docs",
        "version": "1.0.0"
    }


@app.get("/incidents")
async def list_incidents() -> Dict[str, Any]:
    """List all incidents (placeholder - will be moved to API router)."""
    return {
        "incidents": [],
        "total": 0,
        "message": "Integration in progress"
    }


@app.post("/incidents")
async def create_incident(incident_data: Dict[str, Any]) -> Dict[str, Any]:
    """Create a new incident (placeholder - will be moved to API router)."""
    log.info(f"Incident creation requested: {incident_data}")
    return {
        "id": "placeholder-incident-id",
        "status": "created",
        "message": "Integration in progress"
    }


@app.get("/incidents/{incident_id}")
async def get_incident(incident_id: str) -> Dict[str, Any]:
    """Get incident details by ID (placeholder - moved to API router)."""
    return {
        "id": incident_id,
        "status": "placeholder",
        "message": "Integration in progress"
    }


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler for better error responses."""
    log.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error",
            "service": "dispatch-service"
        }
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8013,
        reload=True,
        log_level="info"
    )
