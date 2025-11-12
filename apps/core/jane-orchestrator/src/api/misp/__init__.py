"""
MISP API Endpoints

FastAPI implementation of MISP threat intelligence API endpoints.
Migrated from features/MISP/app/Controller/ CakePHP controllers.
"""

from .events import router as events_router

# Import attributes router
try:
    from .attributes import router as attributes_router
except ImportError:
    # Create placeholder if import fails
    from fastapi import APIRouter
    attributes_router = APIRouter(
        prefix="/attributes", tags=["misp-attributes"])

# Placeholder routers for future implementation
from fastapi import APIRouter

organizations_router = APIRouter(
    prefix="/organizations", tags=["misp-organizations"])
servers_router = APIRouter(prefix="/servers", tags=["misp-servers"])
auth_router = APIRouter(prefix="/auth", tags=["misp-auth"])

__all__ = [
    "events_router",
    "attributes_router",
    "organizations_router",
    "servers_router",
    "auth_router"
]
