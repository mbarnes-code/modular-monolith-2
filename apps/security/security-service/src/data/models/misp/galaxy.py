"""MISP Galaxy Models

Galaxy taxonomy system for threat intelligence classification.
Migrated from CakePHP Galaxy.php and related models.
"""

from sqlalchemy import (Boolean, Column, ForeignKey, Index, Integer, String,
                        Text)
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import relationship

from . import DeletedMixin, MispBaseModel, TimestampMixin, UUIDMixin


class Galaxy(MispBaseModel, UUIDMixin, TimestampMixin, DeletedMixin):
    """MISP Galaxy - Threat intelligence taxonomy"""
    __tablename__ = 'galaxies'

    # Core galaxy fields
    name = Column(String(255), nullable=False, index=True)
    type = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    version = Column(String(255), nullable=False, index=True)

    # Icon and namespace
    icon = Column(String(255), nullable=True)
    namespace = Column(String(255), nullable=False, index=True)

    # Enabled flag
    enabled = Column(Boolean, nullable=False, default=True, index=True)

    # JSON metadata
    galaxy_meta = Column(JSONB, nullable=True)

    # Relationships
    galaxy_clusters = relationship(
        "GalaxyCluster",
        back_populates="galaxy",
        cascade="all, delete-orphan"
    )

    __table_args__ = (
        Index('idx_galaxies_name', 'name'),
        Index('idx_galaxies_type', 'type'),
        Index('idx_galaxies_version', 'version'),
        Index('idx_galaxies_namespace', 'namespace'),
        Index('idx_galaxies_enabled', 'enabled'),
    )

    def __repr__(self):
        return f"<Galaxy(id={self.id}, name='{self.name}', type='{self.type}')>"


class GalaxyCluster(MispBaseModel, UUIDMixin, TimestampMixin, DeletedMixin):
    """MISP Galaxy Cluster - Specific threat intelligence items"""
    __tablename__ = 'galaxy_clusters'

    # Galaxy relationship
    galaxy_id = Column(Integer, ForeignKey('galaxies.id'),
                       nullable=False, index=True)

    # Core cluster fields
    type = Column(String(255), nullable=False, index=True)
    value = Column(String(255), nullable=False, index=True)
    tag_name = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    source = Column(String(255), nullable=True)

    # Authors and references
    authors = Column(Text, nullable=True)
    references = Column(Text, nullable=True)

    # Versioning and publication
    version = Column(String(255), nullable=True)
    published = Column(Boolean, nullable=False, default=False, index=True)

    # Distribution and sharing
    distribution = Column(Integer, nullable=False, default=0, index=True)
    sharing_group_id = Column(Integer, ForeignKey('sharing_groups.id'),
                              nullable=True, index=True)

    # Organisation context
    org_id = Column(Integer, ForeignKey('organisations.id'),
                    nullable=False, index=True)
    orgc_id = Column(Integer, ForeignKey('organisations.id'),
                     nullable=False, index=True)

    # JSON metadata
    cluster_meta = Column(JSONB, nullable=True)

    # Relationships
    galaxy = relationship("Galaxy", back_populates="galaxy_clusters")
    org = relationship("Organisation", foreign_keys=[org_id])
    orgc = relationship("Organisation", foreign_keys=[orgc_id])
    sharing_group = relationship("SharingGroup")

    # Cluster elements
    galaxy_elements = relationship(
        "GalaxyElement",
        back_populates="galaxy_cluster",
        cascade="all, delete-orphan"
    )

    # Cluster relations (outgoing)
    cluster_relations_source = relationship(
        "GalaxyClusterRelation",
        foreign_keys="GalaxyClusterRelation.galaxy_cluster_id",
        back_populates="source_cluster",
        cascade="all, delete-orphan"
    )

    # Cluster relations (incoming)
    cluster_relations_target = relationship(
        "GalaxyClusterRelation",
        foreign_keys="GalaxyClusterRelation.referenced_galaxy_cluster_id",
        back_populates="target_cluster"
    )

    __table_args__ = (
        Index('idx_galaxy_clusters_galaxy_id', 'galaxy_id'),
        Index('idx_galaxy_clusters_type', 'type'),
        Index('idx_galaxy_clusters_value', 'value'),
        Index('idx_galaxy_clusters_tag_name', 'tag_name'),
        Index('idx_galaxy_clusters_published', 'published'),
        Index('idx_galaxy_clusters_distribution', 'distribution'),
        Index('idx_galaxy_clusters_org_id', 'org_id'),
        Index('idx_galaxy_clusters_orgc_id', 'orgc_id'),
    )

    def __repr__(self):
        return (f"<GalaxyCluster(id={self.id}, "
                f"value='{self.value}', type='{self.type}')>")


class GalaxyElement(MispBaseModel, TimestampMixin):
    """MISP Galaxy Element - Key-value metadata for clusters"""
    __tablename__ = 'galaxy_elements'

    # Cluster relationship
    galaxy_cluster_id = Column(Integer, ForeignKey('galaxy_clusters.id'),
                               nullable=False, index=True)

    # Element data
    key = Column(String(255), nullable=False, index=True)
    value = Column(Text, nullable=False)

    # Relationships
    galaxy_cluster = relationship("GalaxyCluster",
                                  back_populates="galaxy_elements")

    __table_args__ = (
        Index('idx_galaxy_elements_cluster_id', 'galaxy_cluster_id'),
        Index('idx_galaxy_elements_key', 'key'),
        Index('idx_galaxy_elements_cluster_key', 'galaxy_cluster_id', 'key'),
    )

    def __repr__(self):
        return (f"<GalaxyElement(id={self.id}, "
                f"key='{self.key}', value='{self.value[:50]}...')>")


class GalaxyClusterRelation(MispBaseModel, UUIDMixin, TimestampMixin,
                            DeletedMixin):
    """MISP Galaxy Cluster Relation - Relationships between clusters"""
    __tablename__ = 'galaxy_cluster_relations'

    # Source and target clusters
    galaxy_cluster_id = Column(Integer, ForeignKey('galaxy_clusters.id'),
                               nullable=False, index=True)
    referenced_galaxy_cluster_id = Column(
        Integer, ForeignKey('galaxy_clusters.id'),
        nullable=False, index=True
    )

    # Relation metadata
    referenced_galaxy_cluster_uuid = Column(UUID(as_uuid=True),
                                            nullable=False, index=True)
    referenced_galaxy_cluster_type = Column(String(255),
                                            nullable=False, index=True)
    referenced_galaxy_cluster_value = Column(String(255),
                                             nullable=False, index=True)

    # Distribution and sharing
    distribution = Column(Integer, nullable=False, default=0, index=True)
    sharing_group_id = Column(Integer, ForeignKey('sharing_groups.id'),
                              nullable=True, index=True)

    # Default relation flag
    default = Column(Boolean, nullable=False, default=False, index=True)

    # JSON tags
    tags = Column(JSONB, nullable=True)

    # Relationships
    source_cluster = relationship(
        "GalaxyCluster",
        foreign_keys=[galaxy_cluster_id],
        back_populates="cluster_relations_source"
    )
    target_cluster = relationship(
        "GalaxyCluster",
        foreign_keys=[referenced_galaxy_cluster_id],
        back_populates="cluster_relations_target"
    )
    sharing_group = relationship("SharingGroup")

    __table_args__ = (
        Index('idx_galaxy_cluster_relations_source', 'galaxy_cluster_id'),
        Index('idx_galaxy_cluster_relations_target',
              'referenced_galaxy_cluster_id'),
        Index('idx_galaxy_cluster_relations_uuid',
              'referenced_galaxy_cluster_uuid'),
        Index('idx_galaxy_cluster_relations_default', 'default'),
    )

    def __repr__(self):
        return (f"<GalaxyClusterRelation(id={self.id}, "
                f"source={self.galaxy_cluster_id}, "
                f"target={self.referenced_galaxy_cluster_id})>")
