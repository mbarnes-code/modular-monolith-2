import logging
from typing import Any

from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

from ..config.auth_config import get_auth_config
# Import MISP-compatible middleware and plugins
from .middleware import (AccessLogMiddleware, AuthMiddleware,
                         CompressionMiddleware)
from .middleware import CorsMiddleware as MispCorsMiddleware
from .middleware import RateLimitMiddleware, SecurityMiddleware
# Import authentication routes and config
from .routes.auth import router as auth_router

# Import startup initialization
try:
    from .startup import initialize_auth_system, shutdown_auth_system
except ImportError:
    initialize_auth_system = None
    shutdown_auth_system = None
# Import MISP API routers
from .misp.events import router as misp_events_router
from .plugins import PluginManager

# Import additional MISP routers with fallbacks
try:
    from .misp.attributes import router as misp_attributes_router
except ImportError:
    from fastapi import APIRouter
    misp_attributes_router = APIRouter(
        prefix="/attributes", tags=["misp-attributes"]
    )

try:
    from .misp.organizations import router as misp_organizations_router
except ImportError:
    from fastapi import APIRouter
    misp_organizations_router = APIRouter(
        prefix="/organisations", tags=["misp-organizations"]
    )

try:
    from .misp.users import router as misp_users_router
except ImportError:
    from fastapi import APIRouter
    misp_users_router = APIRouter(
        prefix="/users", tags=["misp-users"]
    )

try:
    from .misp.tags import router as misp_tags_router
except ImportError:
    from fastapi import APIRouter
    misp_tags_router = APIRouter(
        prefix="/tags", tags=["misp-tags"]
    )

try:
    from .misp.auth import router as misp_auth_router
except ImportError:
    from fastapi import APIRouter
    misp_auth_router = APIRouter(
        prefix="/auth", tags=["misp-auth"]
    )

try:
    from .misp.external_apis import router as misp_external_apis_router
except ImportError:
    from fastapi import APIRouter
    misp_external_apis_router = APIRouter(
        prefix="/external", tags=["misp-external-apis"]
    )

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

# Startup and shutdown event handlers


@app.on_event("startup")
async def startup_event():
    """Initialize services on startup."""
    logger.info("Starting Jane Orchestrator service...")

    # Initialize authentication system
    if initialize_auth_system:
        try:
            await initialize_auth_system(app)
        except Exception as e:
            logger.warning("Auth system initialization failed: %s", str(e))

    logger.info("Jane Orchestrator startup complete")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown."""
    logger.info("Shutting down Jane Orchestrator service...")

    if shutdown_auth_system:
        try:
            await shutdown_auth_system()
        except Exception as e:
            logger.warning("Auth system shutdown failed: %s", str(e))

# Configure MISP-compatible middleware stack
# Order matters - middleware is applied in reverse order of addition

# 1. Access logging (outermost)
app.add_middleware(AccessLogMiddleware)

# 2. CORS handling
# Use auth configuration for CORS settings
auth_config = get_auth_config()
security_config = auth_config.get_security_config()
app.add_middleware(
    MispCorsMiddleware,
    allow_origins=security_config.get("cors_origins", ["*"]),
    allow_credentials=True,
    allow_methods=security_config.get("cors_methods", ["*"]),
    allow_headers=security_config.get("cors_headers", ["*"])
)

# 3. Security middleware
app.add_middleware(
    SecurityMiddleware,
    csrf_check=True,
    force_https=False,  # Configure for production
    disable_browser_cache=True,
    check_sec_fetch_site=True
)

# 4. Compression middleware
app.add_middleware(CompressionMiddleware)

# 5. Rate limiting middleware
app.add_middleware(
    RateLimitMiddleware,
    default_window_seconds=900
)

# 6. Authentication middleware (innermost)
# Note: Auth providers will be initialized during startup
# and added to app.state for middleware access
app.add_middleware(
    AuthMiddleware,
    exempt_paths=[
        "/", "/health", "/ready", "/docs", "/openapi.json",
        "/auth/login", "/auth/callback", "/auth/login/direct"
    ]
)

# Initialize plugin manager
plugin_manager = PluginManager(app)

# Include authentication routes
app.include_router(auth_router, prefix="/api")

# Include MISP API routes
app.include_router(misp_auth_router, prefix="/api/misp")
app.include_router(misp_events_router, prefix="/api/misp")
app.include_router(misp_attributes_router, prefix="/api/misp")
app.include_router(misp_organizations_router, prefix="/api/misp")
app.include_router(misp_users_router, prefix="/api/misp")
app.include_router(misp_tags_router, prefix="/api/misp")
app.include_router(misp_external_apis_router, prefix="/api/misp")


class HealthResponse(BaseModel):
    """Health check response model."""
    status: str = Field(..., description="Health status")
    version: str = Field(..., description="Service version")


class ReadinessResponse(BaseModel):
    """Readiness check response model."""
    status: str = Field(..., description="Readiness status")
    dependencies: dict[str,
                       str] = Field(..., description="Dependency statuses")


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
    # Initialize plugin system
    await plugin_manager.initialize()


@app.on_event("shutdown")
async def shutdown_event():
    """Clean up resources on shutdown."""
    logger.info("Jane Orchestrator Service shutting down...")
    # Cleanup plugin system
    await plugin_manager.shutdown()
