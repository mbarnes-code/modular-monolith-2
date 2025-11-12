"""
Productivity Service - Domain Service for Productivity Tools
Part of the hybrid domain-based architecture for Mental Prosthetic Platform

This service manages 8 productivity tools:
- Actual Budget (Personal finance management)
- Mealie (Recipe management)
- Dispatch (Incident management)
- Firecrawl (Web scraping service)
- Goose (AI coding assistant)
- Inspector (Code inspection tools)
- IT-Tools (IT utility tools)
- Kong (API Gateway - if productivity-focused)

Performance Target: <2s response time for task management workflows
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Productivity Service API",
    description="Domain service for productivity tools and task management",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {
        "service": "Productivity Service",
        "status": "running",
        "domain": "productivity",
        "tools_count": 8,
        "performance_target": "<2s response time"
    }


@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "productivity-service"}


@app.get("/tools")
def list_productivity_tools():
    """List all productivity tools available in this domain service"""
    return {
        "tools": [
            {"name": "Actual Budget", "status": "pending_migration",
                "description": "Personal finance management"},
            {"name": "Mealie", "status": "pending_migration",
                "description": "Recipe management"},
            {"name": "Dispatch", "status": "pending_migration",
                "description": "Incident management"},
            {"name": "Firecrawl", "status": "pending_migration",
                "description": "Web scraping service"},
            {"name": "Goose", "status": "pending_migration",
                "description": "AI coding assistant"},
            {"name": "Inspector", "status": "pending_migration",
                "description": "Code inspection tools"},
            {"name": "IT-Tools", "status": "pending_migration",
                "description": "IT utility tools"},
            {"name": "Kong", "status": "pending_migration",
                "description": "API Gateway (if productivity-focused)"}
        ]
    }

# TODO: Remove this placeholder once migration begins
# This file will be replaced with proper FastAPI implementation during tool migration
