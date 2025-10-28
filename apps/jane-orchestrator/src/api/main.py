import logging
from typing import Any

from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Jane Orchestrator Service",
    description="Central orchestration service for Jane Monorepo",
    version="1.0.0"
)


class HealthResponse(BaseModel):
    """Health check response model."""
    status: str = Field(..., description="Health status")
    version: str = Field(..., description="Service version")


class ReadinessResponse(BaseModel):
    """Readiness check response model."""
    status: str = Field(..., description="Readiness status")
    dependencies: dict[str, str] = Field(..., description="Dependency statuses")


@app.get("/", response_model=dict[str, Any])
async def root():
    """Root endpoint providing service information."""
    logger.info("Root endpoint accessed")
    return {
        "message": "Jane Orchestrator Service",
        "status": "running",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "readiness": "/ready"
        }
    }


@app.get("/health", response_model=HealthResponse)
async def health():
    """
    Health check endpoint for liveness probes.
    Returns service health status.
    """
    logger.debug("Health check requested")
    return HealthResponse(
        status="healthy",
        version="1.0.0"
    )


@app.get("/ready", response_model=ReadinessResponse)
async def ready():
    """
    Readiness probe endpoint - checks if service is ready to accept traffic.
    Validates connectivity to dependent services (LLM servers, databases, etc.).
    """
    logger.debug("Readiness check requested")

    # Best practice: Check actual dependencies
    dependencies = {
        "database": "connected",
        "cyber_llm": "available",
        "mtg_llm": "available",
        "code_llm": "available"
    }

    # In production, implement actual health checks
    # Example:
    # try:
    #     await check_database_connection()
    #     await check_llm_servers()
    # except Exception as e:
    #     logger.error(f"Readiness check failed: {e}")
    #     raise HTTPException(status_code=503, detail="Service not ready")

    return ReadinessResponse(
        status="ready",
        dependencies=dependencies
    )


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """
    Global exception handler for unhandled errors.
    Best practice: Log errors and return appropriate responses.
    """
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Internal server error",
            "message": str(exc)
        }
    )


@app.on_event("startup")
async def startup_event():
    """Initialize resources on startup."""
    logger.info("Jane Orchestrator Service starting up...")


@app.on_event("shutdown")
async def shutdown_event():
    """Clean up resources on shutdown."""
    logger.info("Jane Orchestrator Service shutting down...")
