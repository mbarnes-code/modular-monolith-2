"""
MISP Models Package

Unified import for all MISP data models preserving the original
MISP threat intelligence data structures.
"""

# Import core models
from .core_models import (AdminSetting, Attribute, Base, Event, Object,
                          Organization, Role, Server, SharingGroup, Tag, User)
# Import reference data models
from .reference_models import (Galaxy, GalaxyCluster, GalaxyClusterRelation,
                               GalaxyElement, Taxonomy, TaxonomyEntry,
                               TaxonomyPredicate, Warninglist,
                               WarninglistEntry, WarninglistType)

# Export all models for easy importing
__all__ = [
    # Base
    "Base",

    # Core models
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

    # Reference data models
    "Taxonomy",
    "TaxonomyPredicate",
    "TaxonomyEntry",
    "Galaxy",
    "GalaxyCluster",
    "GalaxyElement",
    "GalaxyClusterRelation",
    "Warninglist",
    "WarninglistEntry",
    "WarninglistType"
]

# Model categories for selective imports
CORE_MODELS = [
    AdminSetting, Role, Organization, User, Server,
    Tag, Event, Attribute, Object, SharingGroup
]

REFERENCE_MODELS = [
    Taxonomy, TaxonomyPredicate, TaxonomyEntry,
    Galaxy, GalaxyCluster, GalaxyElement, GalaxyClusterRelation,
    Warninglist, WarninglistEntry, WarninglistType
]

ALL_MODELS = CORE_MODELS + REFERENCE_MODELS
