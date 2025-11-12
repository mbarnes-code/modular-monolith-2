"""
MISP Reference Data Models

SQLAlchemy models for MISP taxonomies, galaxies, warninglists,
and other reference data structures.
"""

from datetime import datetime
from uuid import uuid4

from sqlalchemy import (JSON, UUID, Boolean, Column, DateTime, ForeignKey,
                        Integer, String, Text)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .core_models import Base


class Taxonomy(Base):
    """
    MISP taxonomies for structured classification.

    Preserves MISP's taxonomy system for standardized threat classification.
    """
    __tablename__ = "taxonomies"

    id = Column(Integer, primary_key=True)
    namespace = Column(String(255), nullable=False, unique=True)
    description = Column(Text, nullable=False)
    version = Column(Integer, nullable=False)
    enabled = Column(Boolean, default=False)
    exclusive = Column(Boolean, default=False)
    required = Column(Boolean, default=False)
    highlighted = Column(Boolean, default=False)
    numerical_value = Column(Integer)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    # Relationships
    predicates = relationship("TaxonomyPredicate", back_populates="taxonomy")

    def __repr__(self) -> str:
        return f"<Taxonomy(namespace='{self.namespace}', version={self.version})>"


class TaxonomyPredicate(Base):
    """
    MISP taxonomy predicates - taxonomy classification terms.

    Preserves MISP's hierarchical taxonomy structure.
    """
    __tablename__ = "taxonomy_predicates"

    id = Column(Integer, primary_key=True)
    taxonomy_id = Column(Integer, ForeignKey("taxonomies.id"), nullable=False)
    value = Column(Text, nullable=False)
    expanded = Column(Text)
    colour = Column(String(7))
    description = Column(Text)
    exclusive = Column(Boolean, default=False)
    numerical_value = Column(Integer)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    # Relationships
    taxonomy = relationship("Taxonomy", back_populates="predicates")
    entries = relationship("TaxonomyEntry", back_populates="predicate")

    def __repr__(self) -> str:
        return f"<TaxonomyPredicate(value='{self.value}', taxonomy_id={self.taxonomy_id})>"


class TaxonomyEntry(Base):
    """
    MISP taxonomy entries - specific taxonomy values.

    Preserves MISP's detailed taxonomy entry system.
    """
    __tablename__ = "taxonomy_entries"

    id = Column(Integer, primary_key=True)
    taxonomy_predicate_id = Column(Integer, ForeignKey(
        "taxonomy_predicates.id"), nullable=False)
    value = Column(Text, nullable=False)
    expanded = Column(Text)
    colour = Column(String(7))
    description = Column(Text)
    numerical_value = Column(Integer)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    # Relationships
    predicate = relationship("TaxonomyPredicate", back_populates="entries")

    def __repr__(self) -> str:
        return f"<TaxonomyEntry(value='{self.value}', predicate_id={self.taxonomy_predicate_id})>"


class Galaxy(Base):
    """
    MISP galaxies - threat intelligence knowledge base.

    Preserves MISP's galaxy system for threat actor and technique clustering.
    """
    __tablename__ = "galaxies"

    id = Column(Integer, primary_key=True)
    uuid = Column(UUID(as_uuid=True), nullable=False,
                  unique=True, default=uuid4)
    name = Column(String(255), nullable=False)
    type = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    version = Column(String(255), nullable=False)
    icon = Column(String(255), default="")
    namespace = Column(String(255), default="misp")
    enabled = Column(Boolean, default=True)
    local_only = Column(Boolean, default=False)
    kill_chain_order = Column(JSON)
    orgc_id = Column(Integer, ForeignKey("organizations.id"))
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    # Relationships
    creator_org = relationship("Organization")
    clusters = relationship("GalaxyCluster", back_populates="galaxy")

    def __repr__(self) -> str:
        return f"<Galaxy(name='{self.name}', type='{self.type}')>"


class GalaxyCluster(Base):
    """
    MISP galaxy clusters - specific threat intelligence entities.

    Preserves MISP's galaxy cluster system for detailed threat intelligence.
    """
    __tablename__ = "galaxy_clusters"

    id = Column(Integer, primary_key=True)
    uuid = Column(UUID(as_uuid=True), nullable=False,
                  unique=True, default=uuid4)
    collection_uuid = Column(UUID(as_uuid=True), nullable=False)
    type = Column(String(255), nullable=False)
    value = Column(Text, nullable=False)
    tag_name = Column(String(255), nullable=False)
    description = Column(Text, default="")
    galaxy_id = Column(Integer, ForeignKey("galaxies.id"), nullable=False)
    source = Column(String(255), default="")
    authors = Column(JSON, default=list)
    version = Column(Integer, default=0)
    distribution = Column(Integer, default=0)
    sharing_group_id = Column(Integer, ForeignKey("sharing_groups.id"))
    org_id = Column(Integer, ForeignKey("organizations.id"), nullable=False)
    orgc_id = Column(Integer, ForeignKey("organizations.id"), nullable=False)
    extends_uuid = Column(UUID(as_uuid=True))
    extends_version = Column(Integer, default=0)
    published = Column(Boolean, default=False)
    deleted = Column(Boolean, default=False)
    locked = Column(Boolean, default=False)
    default = Column(Boolean, default=False)
    local_only = Column(Boolean, default=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    # Relationships
    galaxy = relationship("Galaxy", back_populates="clusters")
    sharing_group = relationship("SharingGroup")
    organization = relationship("Organization", foreign_keys=[org_id])
    creator_org = relationship("Organization", foreign_keys=[orgc_id])
    elements = relationship("GalaxyElement", back_populates="cluster")
    relations = relationship("GalaxyClusterRelation",
                             foreign_keys="GalaxyClusterRelation.galaxy_cluster_id",
                             back_populates="source_cluster")

    def __repr__(self) -> str:
        return f"<GalaxyCluster(value='{self.value}', type='{self.type}')>"


class GalaxyElement(Base):
    """
    MISP galaxy elements - cluster metadata and relationships.

    Preserves MISP's galaxy element system for cluster metadata.
    """
    __tablename__ = "galaxy_elements"

    id = Column(Integer, primary_key=True)
    galaxy_cluster_id = Column(Integer, ForeignKey(
        "galaxy_clusters.id"), nullable=False)
    key = Column(String(255), nullable=False)
    value = Column(Text, nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    # Relationships
    cluster = relationship("GalaxyCluster", back_populates="elements")

    def __repr__(self) -> str:
        return f"<GalaxyElement(key='{self.key}', cluster_id={self.galaxy_cluster_id})>"


class GalaxyClusterRelation(Base):
    """
    MISP galaxy cluster relations - relationships between clusters.

    Preserves MISP's galaxy cluster relationship system.
    """
    __tablename__ = "galaxy_cluster_relations"

    id = Column(Integer, primary_key=True)
    galaxy_cluster_id = Column(Integer, ForeignKey(
        "galaxy_clusters.id"), nullable=False)
    referenced_galaxy_cluster_id = Column(
        Integer, ForeignKey("galaxy_clusters.id"), nullable=False)
    referenced_galaxy_cluster_uuid = Column(UUID(as_uuid=True), nullable=False)
    referenced_galaxy_cluster_type = Column(String(255), nullable=False)
    referenced_galaxy_cluster_value = Column(Text, nullable=False)
    galaxy_cluster_uuid = Column(UUID(as_uuid=True), nullable=False)
    relation_type = Column(String(255), nullable=False)
    tags = Column(JSON, default=list)
    distribution = Column(Integer, default=0)
    sharing_group_id = Column(Integer, ForeignKey("sharing_groups.id"))
    default = Column(Boolean, default=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    # Relationships
    source_cluster = relationship("GalaxyCluster",
                                  foreign_keys=[galaxy_cluster_id],
                                  back_populates="relations")
    target_cluster = relationship("GalaxyCluster",
                                  foreign_keys=[referenced_galaxy_cluster_id])
    sharing_group = relationship("SharingGroup")

    def __repr__(self) -> str:
        return f"<GalaxyClusterRelation(type='{self.relation_type}', source={self.galaxy_cluster_id})>"


class Warninglist(Base):
    """
    MISP warninglists - false positive prevention.

    Preserves MISP's warninglist system for filtering false positives.
    """
    __tablename__ = "warninglists"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, unique=True)
    type = Column(String(255), default="string")
    description = Column(Text, nullable=False)
    version = Column(Integer, default=1)
    enabled = Column(Boolean, default=False)
    default = Column(Boolean, default=False)
    category = Column(String(255), default="")
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    # Relationships
    entries = relationship("WarninglistEntry", back_populates="warninglist")
    types = relationship("WarninglistType", back_populates="warninglist")

    def __repr__(self) -> str:
        return f"<Warninglist(name='{self.name}', version={self.version})>"


class WarninglistEntry(Base):
    """
    MISP warninglist entries - specific values to filter.

    Preserves MISP's warninglist entry system.
    """
    __tablename__ = "warninglist_entries"

    id = Column(Integer, primary_key=True)
    value = Column(Text, nullable=False)
    warninglist_id = Column(Integer, ForeignKey(
        "warninglists.id"), nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    # Relationships
    warninglist = relationship("Warninglist", back_populates="entries")

    def __repr__(self) -> str:
        return f"<WarninglistEntry(value='{self.value}', warninglist_id={self.warninglist_id})>"


class WarninglistType(Base):
    """
    MISP warninglist types - attribute types for warninglist application.

    Preserves MISP's warninglist type system.
    """
    __tablename__ = "warninglist_types"

    id = Column(Integer, primary_key=True)
    type = Column(String(255), nullable=False)
    warninglist_id = Column(Integer, ForeignKey(
        "warninglists.id"), nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    # Relationships
    warninglist = relationship("Warninglist", back_populates="types")

    def __repr__(self) -> str:
        return f"<WarninglistType(type='{self.type}', warninglist_id={self.warninglist_id})>"


# Export all reference data models
__all__ = [
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
