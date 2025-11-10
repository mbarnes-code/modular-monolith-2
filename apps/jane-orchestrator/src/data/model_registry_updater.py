"""
Database Model Registry Update

Updates the main database configuration to include MISP models
and ensures proper imports throughout the codebase.
"""

import logging
from pathlib import Path
from typing import List

logger = logging.getLogger(__name__)


class DatabaseModelRegistryUpdater:
    """
    Updates database model registry to include MISP models.

    Ensures:
    - MISP models are registered with SQLAlchemy
    - Proper imports are available throughout codebase
    - Migration scripts can access all models
    - Services can import MISP models correctly
    """

    def __init__(self):
        self.root_dir = Path(__file__).parent.parent.parent.parent.parent
        self.models_dir = self.root_dir / "apps/jane-orchestrator/src/data/models"

    def update_all_imports(self) -> None:
        """Update all model imports and registrations."""
        logger.info("Updating database model imports for MISP integration...")

        try:
            self._create_main_models_init()
            self._create_database_config_update()
            self._create_migration_import_helper()
            self._create_service_import_helper()

            logger.info("Database model imports updated successfully")

        except Exception as e:
            logger.error("Failed to update model imports: %s", e)
            raise

    def _create_main_models_init(self) -> None:
        """Create or update main models __init__.py file."""
        logger.info("Creating main models __init__.py...")

        models_init_content = '''"""
Jane Orchestrator Data Models

Unified import for all data models including MISP threat intelligence
data structures and other domain models.
"""

# Import MISP models
from .misp import (
    # Base
    Base as MISPBase,
    # Core models
    AdminSetting,
    Role,
    Organization,
    User,
    Server,
    Tag,
    Event,
    Attribute,
    Object,
    SharingGroup,
    # Reference data models  
    Taxonomy,
    TaxonomyPredicate,
    TaxonomyEntry,
    Galaxy,
    GalaxyCluster,
    GalaxyElement,
    GalaxyClusterRelation,
    Warninglist,
    WarninglistEntry,
    WarninglistType,
    # Model collections
    CORE_MODELS as MISP_CORE_MODELS,
    REFERENCE_MODELS as MISP_REFERENCE_MODELS,
    ALL_MODELS as MISP_ALL_MODELS
)

# Domain-specific model imports will be added here as they are created
# from .security import SecurityModels
# from .productivity import ProductivityModels
# from .mtg import MTGModels
# from .infrastructure import InfrastructureModels

# Export all models for unified access
__all__ = [
    # MISP Base
    "MISPBase",
    
    # MISP Core Models
    "AdminSetting",
    "Role", 
    "Organization",
    "User",
    "Server",
    "Tag",
    "Event", 
    "Attribute",
    "Object",
    "SharingGroup",
    
    # MISP Reference Models
    "Taxonomy",
    "TaxonomyPredicate",
    "TaxonomyEntry",
    "Galaxy",
    "GalaxyCluster", 
    "GalaxyElement",
    "GalaxyClusterRelation",
    "Warninglist",
    "WarninglistEntry",
    "WarninglistType",
    
    # Model Collections
    "MISP_CORE_MODELS",
    "MISP_REFERENCE_MODELS", 
    "MISP_ALL_MODELS"
]

# Database base classes for different domains
DATABASE_BASES = {
    "misp": MISPBase,
    # Additional bases will be added as domains are implemented
}

# All models registry for migrations and utilities
ALL_DOMAIN_MODELS = {
    "misp": MISP_ALL_MODELS,
    # Additional domain models will be added here
}
'''

        models_init_file = self.models_dir / "__init__.py"
        with open(models_init_file, 'w', encoding='utf-8') as f:
            f.write(models_init_content)

        logger.info(f"Created models __init__.py: {models_init_file}")

    def _create_database_config_update(self) -> None:
        """Create database configuration with MISP models."""
        logger.info("Creating database configuration update...")

        db_config_content = '''"""
Database Configuration with MISP Models

Enhanced database configuration that includes MISP models
and supports multi-domain model registration.
"""

import logging
from typing import Dict, List, Type

from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from .models import (
    DATABASE_BASES, ALL_DOMAIN_MODELS,
    MISP_ALL_MODELS, MISPBase
)

logger = logging.getLogger(__name__)


class DatabaseManager:
    """
    Enhanced database manager with multi-domain model support.
    
    Handles:
    - MISP threat intelligence models
    - Domain-specific model registration  
    - Migration support for all model types
    - Service-level model access
    """
    
    def __init__(self, database_url: str):
        self.database_url = database_url
        self.engines = {}
        self.sessions = {}
        self.metadata_registry = {}
        
        # Initialize database engines and sessions
        self._initialize_engines()
        self._register_all_models()
        
    def _initialize_engines(self) -> None:
        """Initialize database engines for all domains."""
        logger.info("Initializing database engines...")
        
        # Main async engine for the application
        self.async_engine = create_async_engine(
            self.database_url,
            echo=False,
            future=True
        )
        
        # Sync engine for migrations and utilities
        sync_url = self.database_url.replace("+asyncpg", "")
        self.sync_engine = create_engine(sync_url, echo=False)
        
        # Session factories
        self.AsyncSessionLocal = sessionmaker(
            self.async_engine,
            class_=AsyncSession,
            expire_on_commit=False
        )
        
        self.SyncSessionLocal = sessionmaker(
            bind=self.sync_engine,
            expire_on_commit=False
        )
        
        logger.info("Database engines initialized")
        
    def _register_all_models(self) -> None:
        """Register all domain models with their respective bases."""
        logger.info("Registering all domain models...")
        
        for domain, base_class in DATABASE_BASES.items():
            logger.info(f"Registering {domain} models...")
            
            # Create metadata registry for this domain
            metadata = MetaData()
            self.metadata_registry[domain] = metadata
            
            # Bind metadata to base class
            base_class.metadata = metadata
            
            # Log model registration
            models = ALL_DOMAIN_MODELS.get(domain, [])
            logger.info(f"Registered {len(models)} models for {domain} domain")
            
        logger.info("All domain models registered successfully")
        
    async def create_all_tables(self) -> None:
        """Create all tables for all domains."""
        logger.info("Creating all database tables...")
        
        async with self.async_engine.begin() as conn:
            # Create MISP tables
            await conn.run_sync(MISPBase.metadata.create_all)
            
            # Additional domain tables will be created here
            
        logger.info("All database tables created")
        
    async def get_async_session(self) -> AsyncSession:
        """Get async database session."""
        return self.AsyncSessionLocal()
        
    def get_sync_session(self):
        """Get sync database session."""
        return self.SyncSessionLocal()
        
    def get_models_for_domain(self, domain: str) -> List[Type]:
        """Get all models for a specific domain."""
        return ALL_DOMAIN_MODELS.get(domain, [])
        
    def get_base_for_domain(self, domain: str) -> Type:
        """Get base class for a specific domain.""" 
        return DATABASE_BASES.get(domain)
        
    async def validate_models(self) -> Dict[str, bool]:
        """Validate all registered models."""
        logger.info("Validating database models...")
        
        validation_results = {}
        
        for domain, models in ALL_DOMAIN_MODELS.items():
            try:
                # Basic model validation
                base_class = DATABASE_BASES[domain]
                validation_results[domain] = len(models) > 0 and base_class is not None
                logger.info(f"{domain} models validation: {'PASS' if validation_results[domain] else 'FAIL'}")
                
            except Exception as e:
                logger.error(f"Model validation failed for {domain}: {e}")
                validation_results[domain] = False
                
        return validation_results


# Global database manager instance
database_manager = None


def get_database_manager(database_url: str) -> DatabaseManager:
    """Get or create database manager instance."""
    global database_manager
    
    if database_manager is None:
        database_manager = DatabaseManager(database_url)
        
    return database_manager


async def get_db_session() -> AsyncSession:
    """Get database session for dependency injection."""
    if database_manager is None:
        raise RuntimeError("Database manager not initialized")
        
    return await database_manager.get_async_session()
'''

        db_config_file = self.models_dir.parent / "database_config.py"
        with open(db_config_file, 'w', encoding='utf-8') as f:
            f.write(db_config_content)

        logger.info(f"Created database configuration: {db_config_file}")

    def _create_migration_import_helper(self) -> None:
        """Create migration import helper for database operations."""
        logger.info("Creating migration import helper...")

        migration_helper_content = '''"""
Migration Import Helper

Provides unified access to all models for database migrations,
specifically supporting MISP model migrations and schema updates.
"""

from typing import Dict, List, Type

# Import all MISP models for migration operations
from ..models.misp import (
    Base as MISPBase,
    AdminSetting, Role, Organization, User, Server, Tag,
    Event, Attribute, Object, SharingGroup,
    Taxonomy, TaxonomyPredicate, TaxonomyEntry,
    Galaxy, GalaxyCluster, GalaxyElement, GalaxyClusterRelation,  
    Warninglist, WarninglistEntry, WarninglistType,
    ALL_MODELS as MISP_ALL_MODELS
)

# Model registry for migration operations
MIGRATION_MODEL_REGISTRY = {
    "misp": {
        "base": MISPBase,
        "models": MISP_ALL_MODELS,
        "core_models": [
            AdminSetting, Role, Organization, User, Server, Tag,
            Event, Attribute, Object, SharingGroup
        ],
        "reference_models": [
            Taxonomy, TaxonomyPredicate, TaxonomyEntry,
            Galaxy, GalaxyCluster, GalaxyElement, GalaxyClusterRelation,
            Warninglist, WarninglistEntry, WarninglistType
        ]
    }
}

# Migration execution order for dependencies
MIGRATION_ORDER = {
    "misp": [
        # Core infrastructure first
        [AdminSetting, Role, Organization],
        # User management
        [User, Server], 
        # Content structure
        [Tag, SharingGroup],
        # Events and attributes
        [Event, Attribute, Object],
        # Reference data
        [Taxonomy, TaxonomyPredicate, TaxonomyEntry],
        [Galaxy, GalaxyCluster, GalaxyElement, GalaxyClusterRelation],
        [Warninglist, WarninglistEntry, WarninglistType]
    ]
}


def get_models_for_migration(domain: str) -> List[Type]:
    """Get models for migration in dependency order."""
    domain_info = MIGRATION_MODEL_REGISTRY.get(domain, {})
    return domain_info.get("models", [])


def get_migration_order(domain: str) -> List[List[Type]]:
    """Get models in migration dependency order."""
    return MIGRATION_ORDER.get(domain, [])
    
    
def get_base_for_migration(domain: str) -> Type:
    """Get base class for migration operations."""
    domain_info = MIGRATION_MODEL_REGISTRY.get(domain, {})
    return domain_info.get("base")
'''

        migration_helper_file = self.models_dir.parent / "migrations" / "import_helper.py"
        migration_helper_file.parent.mkdir(parents=True, exist_ok=True)

        with open(migration_helper_file, 'w', encoding='utf-8') as f:
            f.write(migration_helper_content)

        logger.info(
            f"Created migration import helper: {migration_helper_file}")

    def _create_service_import_helper(self) -> None:
        """Create service import helper for easy model access."""
        logger.info("Creating service import helper...")

        service_helper_content = '''"""
Service Import Helper

Provides convenient imports for services to access MISP models
and other domain models without complex import paths.
"""

# MISP model imports for services
from ..models.misp import (
    # Core models for threat intelligence
    AdminSetting, Role, Organization, User, Server, Tag,
    Event, Attribute, Object, SharingGroup,
    
    # Reference data models
    Taxonomy, TaxonomyPredicate, TaxonomyEntry,
    Galaxy, GalaxyCluster, GalaxyElement, GalaxyClusterRelation,
    Warninglist, WarninglistEntry, WarninglistType
)

# Commonly used model groups
ADMIN_MODELS = [AdminSetting, Role, Organization, User]
THREAT_INTEL_MODELS = [Event, Attribute, Object, Tag, SharingGroup]
REFERENCE_DATA_MODELS = [
    Taxonomy, TaxonomyPredicate, TaxonomyEntry,
    Galaxy, GalaxyCluster, GalaxyElement, GalaxyClusterRelation,
    Warninglist, WarninglistEntry, WarninglistType
]

# Service-friendly model registry
SERVICE_MODEL_REGISTRY = {
    "admin": ADMIN_MODELS,
    "threat_intel": THREAT_INTEL_MODELS,
    "reference": REFERENCE_DATA_MODELS
}


def get_models_for_service(service_type: str):
    """Get models commonly used by service type."""
    return SERVICE_MODEL_REGISTRY.get(service_type, [])
'''

        service_helper_file = self.models_dir.parent / "services" / "model_imports.py"
        service_helper_file.parent.mkdir(parents=True, exist_ok=True)

        with open(service_helper_file, 'w', encoding='utf-8') as f:
            f.write(service_helper_content)

        logger.info(f"Created service import helper: {service_helper_file}")


def update_database_model_imports() -> None:
    """Entry point for updating database model imports."""
    updater = DatabaseModelRegistryUpdater()
    updater.update_all_imports()


if __name__ == "__main__":
    update_database_model_imports()
