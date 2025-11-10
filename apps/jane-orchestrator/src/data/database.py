"""
Database configuration and base model for Jane Orchestrator.

This module provides the SQLAlchemy base configuration and session management
for all data models across the 37-tool integration platform.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Create the declarative base for all models
Base = declarative_base()

# Database configuration will be handled by FastAPI dependency injection
# This module provides the base class for all models
