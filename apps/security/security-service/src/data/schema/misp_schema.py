"""MISP Database Schema Definitions

Schema artifacts migrated from MISP PostgreSQL structure.
Preserves all table definitions, indexes, and constraints while integrating 
with unified PostgreSQL architecture.
"""

from typing import Optional

from apps.security_service.src.data.models.misp import MispBaseModel
from sqlalchemy import (BigInteger, Boolean, Column, DateTime, ForeignKey,
                        Index, Integer, SmallInteger, String, Text, func, text)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base


class MispSchemaArtifacts:
    """MISP schema artifacts and database initialization utilities"""

    @staticmethod
    def get_initialization_sql() -> str:
        """Get PostgreSQL initialization SQL for MISP schema"""
        return """
        -- MISP Database Initialization Script
        -- Migrated from features/MISP/INSTALL/POSTGRESQL-structure.sql
        
        SET statement_timeout = 0;
        SET lock_timeout = 0;
        SET idle_in_transaction_session_timeout = 0;
        SET client_encoding = 'UTF8';
        SET standard_conforming_strings = on;
        SET check_function_bodies = false;
        SET client_min_messages = warning;
        SET row_security = off;
        SET default_tablespace = '';
        SET default_with_oids = false;
        
        -- Enable required extensions
        CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
        CREATE EXTENSION IF NOT EXISTS "pgcrypto";
        
        -- Custom data types for MISP
        DO $$ BEGIN
            CREATE TYPE misp_threat_level AS ENUM ('1', '2', '3', '4');
        EXCEPTION
            WHEN duplicate_object THEN null;
        END $$;
        
        DO $$ BEGIN
            CREATE TYPE misp_analysis_status AS ENUM ('0', '1', '2');
        EXCEPTION
            WHEN duplicate_object THEN null;
        END $$;
        
        DO $$ BEGIN
            CREATE TYPE misp_distribution_level AS ENUM ('0', '1', '2', '3', '4', '5');
        EXCEPTION
            WHEN duplicate_object THEN null;
        END $$;
        """

    @staticmethod
    def get_performance_indexes() -> str:
        """Get critical performance indexes for MISP data"""
        return """
        -- MISP Performance Indexes (migrated and optimized)
        -- Based on original PostgreSQL schema with performance enhancements
        
        -- Attributes performance indexes
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_attributes_event_id 
            ON attributes (event_id);
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_attributes_object_id 
            ON attributes (object_id) WHERE object_id != 0;
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_attributes_category 
            ON attributes (category);
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_attributes_type 
            ON attributes (type);
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_attributes_value1_hash 
            ON attributes USING hash (sha256(value1::bytea));
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_attributes_uuid 
            ON attributes (uuid);
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_attributes_timestamp 
            ON attributes (timestamp DESC);
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_attributes_to_ids 
            ON attributes (to_ids) WHERE to_ids = true;
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_attributes_deleted 
            ON attributes (deleted) WHERE deleted = false;
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_attributes_distribution 
            ON attributes (distribution);
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_attributes_sharing_group_id 
            ON attributes (sharing_group_id) WHERE sharing_group_id != 0;
        
        -- Full-text search index for attributes
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_attributes_fulltext 
            ON attributes USING gin (
                to_tsvector('english', 
                    COALESCE(value1, '') || ' ' || 
                    COALESCE(value2, '') || ' ' || 
                    COALESCE(comment, '')
                )
            );
        
        -- Events performance indexes  
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_events_org_id 
            ON events (org_id);
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_events_orgc_id 
            ON events (orgc_id);
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_events_user_id 
            ON events (user_id);
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_events_date 
            ON events (date DESC);
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_events_threat_level_id 
            ON events (threat_level_id);
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_events_published 
            ON events (published);
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_events_uuid 
            ON events (uuid);
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_events_timestamp 
            ON events (timestamp DESC);
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_events_distribution 
            ON events (distribution);
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_events_sharing_group_id 
            ON events (sharing_group_id) WHERE sharing_group_id != 0;
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_events_analysis 
            ON events (analysis);
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_events_attribute_count 
            ON events (attribute_count) WHERE attribute_count > 0;
        
        -- Event pagination index (covering index for performance)
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_events_pagination 
            ON events (date DESC, id DESC) 
            INCLUDE (info, threat_level_id, analysis, published, attribute_count);
        
        -- Full-text search index for events
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_events_fulltext 
            ON events USING gin (
                to_tsvector('english', COALESCE(info, ''))
            );
        
        -- Objects performance indexes
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_objects_event_id 
            ON objects (event_id);
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_objects_template_uuid 
            ON objects (template_uuid);
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_objects_template_version 
            ON objects (template_version);
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_objects_name 
            ON objects (name);
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_objects_uuid 
            ON objects (uuid);
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_objects_timestamp 
            ON objects (timestamp DESC);
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_objects_distribution 
            ON objects (distribution);
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_objects_sharing_group_id 
            ON objects (sharing_group_id) WHERE sharing_group_id != 0;
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_objects_deleted 
            ON objects (deleted) WHERE deleted = false;
        
        -- Organizations performance indexes
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_organisations_name 
            ON organisations (name);
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_organisations_uuid 
            ON organisations (uuid);
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_organisations_local 
            ON organisations (local);
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_organisations_nationality 
            ON organisations (nationality);
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_organisations_sector 
            ON organisations (sector);
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_organisations_type 
            ON organisations (type);
        
        -- Users performance indexes
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_users_email 
            ON users (email);
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_users_org_id 
            ON users (org_id);
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_users_server_id 
            ON users (server_id);
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_users_role_id 
            ON users (role_id);
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_users_authkey 
            ON users (authkey);
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_users_disabled 
            ON users (disabled) WHERE disabled = false;
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_users_terms_accepted 
            ON users (terms_accepted) WHERE terms_accepted = true;
        
        -- Tags performance indexes
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_tags_name 
            ON tags (name);
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_tags_colour 
            ON tags (colour);
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_tags_org_id 
            ON tags (org_id);
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_tags_user_id 
            ON tags (user_id);
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_tags_exportable 
            ON tags (exportable);
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_tags_hide_tag 
            ON tags (hide_tag) WHERE hide_tag = false;
        
        -- Tag relationships indexes
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_attribute_tags_attribute_id 
            ON attribute_tags (attribute_id);
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_attribute_tags_tag_id 
            ON attribute_tags (tag_id);
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_attribute_tags_event_id 
            ON attribute_tags (event_id);
        
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_event_tags_event_id 
            ON event_tags (event_id);
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_event_tags_tag_id 
            ON event_tags (tag_id);
        
        -- Sightings performance indexes
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_sightings_attribute_id 
            ON sightings (attribute_id);
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_sightings_org_id 
            ON sightings (org_id);
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_sightings_event_id 
            ON sightings (event_id);
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_sightings_date_sighting 
            ON sightings (date_sighting DESC);
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_sightings_type 
            ON sightings (type);
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_sightings_source 
            ON sightings (source);
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_sightings_uuid 
            ON sightings (uuid);
        
        -- Taxonomies performance indexes
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_taxonomies_namespace 
            ON taxonomies (namespace);
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_taxonomies_enabled 
            ON taxonomies (enabled) WHERE enabled = true;
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_taxonomies_version 
            ON taxonomies (version);
        
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_taxonomy_predicates_taxonomy_id 
            ON taxonomy_predicates (taxonomy_id);
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_taxonomy_predicates_value 
            ON taxonomy_predicates (value);
        
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_taxonomy_entries_taxonomy_predicate_id 
            ON taxonomy_entries (taxonomy_predicate_id);
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_taxonomy_entries_value 
            ON taxonomy_entries (value);
        
        -- Galaxies performance indexes
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_galaxies_uuid 
            ON galaxies (uuid);
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_galaxies_name 
            ON galaxies (name);
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_galaxies_type 
            ON galaxies (type);
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_galaxies_namespace 
            ON galaxies (namespace);
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_galaxies_enabled 
            ON galaxies (enabled) WHERE enabled = true;
        
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_galaxy_clusters_galaxy_id 
            ON galaxy_clusters (galaxy_id);
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_galaxy_clusters_uuid 
            ON galaxy_clusters (uuid);
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_galaxy_clusters_type 
            ON galaxy_clusters (type);
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_galaxy_clusters_value 
            ON galaxy_clusters (value);
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_galaxy_clusters_tag_name 
            ON galaxy_clusters (tag_name);
        
        -- Sharing groups performance indexes
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_sharing_groups_uuid 
            ON sharing_groups (uuid);
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_sharing_groups_name 
            ON sharing_groups (name);
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_sharing_groups_org_id 
            ON sharing_groups (org_id);
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_sharing_groups_active 
            ON sharing_groups (active) WHERE active = true;
        
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_sharing_group_orgs_sharing_group_id 
            ON sharing_group_orgs (sharing_group_id);
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_sharing_group_orgs_org_id 
            ON sharing_group_orgs (org_id);
        
        -- Correlations performance indexes (critical for MISP performance)
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_correlations_value 
            ON correlations USING hash (value);
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_correlations_1_value 
            ON correlations (value, 1_attribute_id);
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_correlations_1_event_id 
            ON correlations (1_event_id);
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_correlations_1_object_id 
            ON correlations (1_object_id) WHERE 1_object_id != 0;
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_correlations_event_id 
            ON correlations (event_id);
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_correlations_attribute_id 
            ON correlations (attribute_id);
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_correlations_object_id 
            ON correlations (object_id) WHERE object_id != 0;
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_correlations_org_id 
            ON correlations (org_id);
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_correlations_distribution 
            ON correlations (distribution);
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_correlations_private 
            ON correlations (private) WHERE private = false;
        
        -- Servers performance indexes (for federation)
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_servers_url 
            ON servers (url);
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_servers_org_id 
            ON servers (org_id);
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_servers_push 
            ON servers (push) WHERE push = true;
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_servers_pull 
            ON servers (pull) WHERE pull = true;
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_servers_lastpushedid 
            ON servers (lastpushedid);
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_servers_lastpulledid 
            ON servers (lastpulledid);
        
        -- Feeds performance indexes
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_feeds_provider 
            ON feeds (provider);
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_feeds_name 
            ON feeds (name);
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_feeds_enabled 
            ON feeds (enabled) WHERE enabled = true;
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_feeds_caching_enabled 
            ON feeds (caching_enabled) WHERE caching_enabled = true;
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_feeds_source_format 
            ON feeds (source_format);
        
        -- Warninglists performance indexes
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_warninglists_name 
            ON warninglists (name);
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_warninglists_type 
            ON warninglists (type);
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_warninglists_enabled 
            ON warninglists (enabled) WHERE enabled = true;
        
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_warninglist_entries_warninglist_id 
            ON warninglist_entries (warninglist_id);
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_warninglist_entries_value 
            ON warninglist_entries USING hash (value);
        
        -- Access logs performance indexes (for monitoring)
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_access_logs_created 
            ON access_logs (created DESC);
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_access_logs_user_id 
            ON access_logs (user_id);
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_access_logs_org_id 
            ON access_logs (org_id);
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_access_logs_authkey_id 
            ON access_logs (authkey_id) WHERE authkey_id IS NOT NULL;
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_access_logs_ip 
            ON access_logs (ip);
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_access_logs_request_type 
            ON access_logs (request_type);
        
        -- Workflows performance indexes (MISP workflow system)
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_workflows_name 
            ON workflows (name);
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_workflows_uuid 
            ON workflows (uuid);
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_workflows_enabled 
            ON workflows (enabled) WHERE enabled = true;
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_workflows_trigger_id 
            ON workflows (trigger_id);
        
        -- Authkeys performance indexes
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_auth_keys_authkey 
            ON auth_keys (authkey_start, authkey_end);
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_auth_keys_user_id 
            ON auth_keys (user_id);
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_auth_keys_expiration 
            ON auth_keys (expiration) WHERE expiration IS NOT NULL;
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_auth_keys_allowed_ips 
            ON auth_keys USING gin (allowed_ips) WHERE allowed_ips IS NOT NULL;
        
        -- Threads performance indexes (discussion system)
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_threads_event_id 
            ON threads (event_id);
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_threads_org_id 
            ON threads (org_id);
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_threads_user_id 
            ON threads (user_id);
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_threads_sharing_group_id 
            ON threads (sharing_group_id) WHERE sharing_group_id != 0;
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_threads_date_created 
            ON threads (date_created DESC);
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_threads_date_modified 
            ON threads (date_modified DESC);
        
        -- Posts performance indexes (discussion posts)
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_posts_thread_id 
            ON posts (thread_id);
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_posts_user_id 
            ON posts (user_id);
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_posts_date_created 
            ON posts (date_created DESC);
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_posts_date_modified 
            ON posts (date_modified DESC);
        """

    @staticmethod
    def get_constraints_and_triggers() -> str:
        """Get foreign key constraints and database triggers"""
        return """
        -- MISP Foreign Key Constraints
        -- Preserving referential integrity from original schema
        
        -- Events constraints
        ALTER TABLE events 
            ADD CONSTRAINT fk_events_org_id 
            FOREIGN KEY (org_id) REFERENCES organisations(id) ON DELETE CASCADE;
        
        ALTER TABLE events 
            ADD CONSTRAINT fk_events_orgc_id 
            FOREIGN KEY (orgc_id) REFERENCES organisations(id) ON DELETE CASCADE;
        
        ALTER TABLE events 
            ADD CONSTRAINT fk_events_user_id 
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE;
        
        ALTER TABLE events 
            ADD CONSTRAINT fk_events_threat_level_id 
            FOREIGN KEY (threat_level_id) REFERENCES threat_levels(id) ON DELETE SET NULL;
        
        ALTER TABLE events 
            ADD CONSTRAINT fk_events_sharing_group_id 
            FOREIGN KEY (sharing_group_id) REFERENCES sharing_groups(id) ON DELETE SET NULL;
        
        -- Attributes constraints
        ALTER TABLE attributes 
            ADD CONSTRAINT fk_attributes_event_id 
            FOREIGN KEY (event_id) REFERENCES events(id) ON DELETE CASCADE;
        
        ALTER TABLE attributes 
            ADD CONSTRAINT fk_attributes_object_id 
            FOREIGN KEY (object_id) REFERENCES objects(id) ON DELETE CASCADE;
        
        ALTER TABLE attributes 
            ADD CONSTRAINT fk_attributes_sharing_group_id 
            FOREIGN KEY (sharing_group_id) REFERENCES sharing_groups(id) ON DELETE SET NULL;
        
        -- Objects constraints
        ALTER TABLE objects 
            ADD CONSTRAINT fk_objects_event_id 
            FOREIGN KEY (event_id) REFERENCES events(id) ON DELETE CASCADE;
        
        ALTER TABLE objects 
            ADD CONSTRAINT fk_objects_sharing_group_id 
            FOREIGN KEY (sharing_group_id) REFERENCES sharing_groups(id) ON DELETE SET NULL;
        
        -- Users constraints
        ALTER TABLE users 
            ADD CONSTRAINT fk_users_org_id 
            FOREIGN KEY (org_id) REFERENCES organisations(id) ON DELETE CASCADE;
        
        ALTER TABLE users 
            ADD CONSTRAINT fk_users_server_id 
            FOREIGN KEY (server_id) REFERENCES servers(id) ON DELETE SET NULL;
        
        ALTER TABLE users 
            ADD CONSTRAINT fk_users_role_id 
            FOREIGN KEY (role_id) REFERENCES roles(id) ON DELETE SET NULL;
        
        -- Tag relationship constraints
        ALTER TABLE attribute_tags 
            ADD CONSTRAINT fk_attribute_tags_attribute_id 
            FOREIGN KEY (attribute_id) REFERENCES attributes(id) ON DELETE CASCADE;
        
        ALTER TABLE attribute_tags 
            ADD CONSTRAINT fk_attribute_tags_tag_id 
            FOREIGN KEY (tag_id) REFERENCES tags(id) ON DELETE CASCADE;
        
        ALTER TABLE attribute_tags 
            ADD CONSTRAINT fk_attribute_tags_event_id 
            FOREIGN KEY (event_id) REFERENCES events(id) ON DELETE CASCADE;
        
        ALTER TABLE event_tags 
            ADD CONSTRAINT fk_event_tags_event_id 
            FOREIGN KEY (event_id) REFERENCES events(id) ON DELETE CASCADE;
        
        ALTER TABLE event_tags 
            ADD CONSTRAINT fk_event_tags_tag_id 
            FOREIGN KEY (tag_id) REFERENCES tags(id) ON DELETE CASCADE;
        
        -- Sightings constraints
        ALTER TABLE sightings 
            ADD CONSTRAINT fk_sightings_attribute_id 
            FOREIGN KEY (attribute_id) REFERENCES attributes(id) ON DELETE CASCADE;
        
        ALTER TABLE sightings 
            ADD CONSTRAINT fk_sightings_event_id 
            FOREIGN KEY (event_id) REFERENCES events(id) ON DELETE CASCADE;
        
        ALTER TABLE sightings 
            ADD CONSTRAINT fk_sightings_org_id 
            FOREIGN KEY (org_id) REFERENCES organisations(id) ON DELETE CASCADE;
        
        -- Taxonomy constraints
        ALTER TABLE taxonomy_predicates 
            ADD CONSTRAINT fk_taxonomy_predicates_taxonomy_id 
            FOREIGN KEY (taxonomy_id) REFERENCES taxonomies(id) ON DELETE CASCADE;
        
        ALTER TABLE taxonomy_entries 
            ADD CONSTRAINT fk_taxonomy_entries_taxonomy_predicate_id 
            FOREIGN KEY (taxonomy_predicate_id) REFERENCES taxonomy_predicates(id) ON DELETE CASCADE;
        
        -- Galaxy constraints
        ALTER TABLE galaxy_clusters 
            ADD CONSTRAINT fk_galaxy_clusters_galaxy_id 
            FOREIGN KEY (galaxy_id) REFERENCES galaxies(id) ON DELETE CASCADE;
        
        -- Sharing group constraints
        ALTER TABLE sharing_groups 
            ADD CONSTRAINT fk_sharing_groups_org_id 
            FOREIGN KEY (org_id) REFERENCES organisations(id) ON DELETE CASCADE;
        
        ALTER TABLE sharing_group_orgs 
            ADD CONSTRAINT fk_sharing_group_orgs_sharing_group_id 
            FOREIGN KEY (sharing_group_id) REFERENCES sharing_groups(id) ON DELETE CASCADE;
        
        ALTER TABLE sharing_group_orgs 
            ADD CONSTRAINT fk_sharing_group_orgs_org_id 
            FOREIGN KEY (org_id) REFERENCES organisations(id) ON DELETE CASCADE;
        
        -- Correlation constraints
        ALTER TABLE correlations 
            ADD CONSTRAINT fk_correlations_event_id 
            FOREIGN KEY (event_id) REFERENCES events(id) ON DELETE CASCADE;
        
        ALTER TABLE correlations 
            ADD CONSTRAINT fk_correlations_attribute_id 
            FOREIGN KEY (attribute_id) REFERENCES attributes(id) ON DELETE CASCADE;
        
        ALTER TABLE correlations 
            ADD CONSTRAINT fk_correlations_object_id 
            FOREIGN KEY (object_id) REFERENCES objects(id) ON DELETE CASCADE;
        
        ALTER TABLE correlations 
            ADD CONSTRAINT fk_correlations_org_id 
            FOREIGN KEY (org_id) REFERENCES organisations(id) ON DELETE CASCADE;
        
        -- Server constraints
        ALTER TABLE servers 
            ADD CONSTRAINT fk_servers_org_id 
            FOREIGN KEY (org_id) REFERENCES organisations(id) ON DELETE CASCADE;
        
        -- Warninglist constraints
        ALTER TABLE warninglist_entries 
            ADD CONSTRAINT fk_warninglist_entries_warninglist_id 
            FOREIGN KEY (warninglist_id) REFERENCES warninglists(id) ON DELETE CASCADE;
        
        -- Access log constraints
        ALTER TABLE access_logs 
            ADD CONSTRAINT fk_access_logs_user_id 
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE;
        
        ALTER TABLE access_logs 
            ADD CONSTRAINT fk_access_logs_org_id 
            FOREIGN KEY (org_id) REFERENCES organisations(id) ON DELETE CASCADE;
        
        ALTER TABLE access_logs 
            ADD CONSTRAINT fk_access_logs_authkey_id 
            FOREIGN KEY (authkey_id) REFERENCES auth_keys(id) ON DELETE SET NULL;
        
        -- Thread constraints
        ALTER TABLE threads 
            ADD CONSTRAINT fk_threads_event_id 
            FOREIGN KEY (event_id) REFERENCES events(id) ON DELETE CASCADE;
        
        ALTER TABLE threads 
            ADD CONSTRAINT fk_threads_org_id 
            FOREIGN KEY (org_id) REFERENCES organisations(id) ON DELETE CASCADE;
        
        ALTER TABLE threads 
            ADD CONSTRAINT fk_threads_user_id 
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE;
        
        ALTER TABLE threads 
            ADD CONSTRAINT fk_threads_sharing_group_id 
            FOREIGN KEY (sharing_group_id) REFERENCES sharing_groups(id) ON DELETE SET NULL;
        
        -- Post constraints
        ALTER TABLE posts 
            ADD CONSTRAINT fk_posts_thread_id 
            FOREIGN KEY (thread_id) REFERENCES threads(id) ON DELETE CASCADE;
        
        ALTER TABLE posts 
            ADD CONSTRAINT fk_posts_user_id 
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE;
        
        -- Auth key constraints
        ALTER TABLE auth_keys 
            ADD CONSTRAINT fk_auth_keys_user_id 
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE;
        
        -- MISP Database Triggers
        -- Automatic cache invalidation and statistics updates
        
        -- Function to update event attribute count
        CREATE OR REPLACE FUNCTION update_event_attribute_count()
        RETURNS TRIGGER AS $$
        BEGIN
            IF TG_OP = 'INSERT' THEN
                UPDATE events 
                SET attribute_count = attribute_count + 1 
                WHERE id = NEW.event_id;
                RETURN NEW;
            ELSIF TG_OP = 'DELETE' THEN
                UPDATE events 
                SET attribute_count = attribute_count - 1 
                WHERE id = OLD.event_id AND attribute_count > 0;
                RETURN OLD;
            END IF;
            RETURN NULL;
        END;
        $$ LANGUAGE plpgsql;
        
        -- Trigger for attribute count updates
        DROP TRIGGER IF EXISTS trigger_update_event_attribute_count ON attributes;
        CREATE TRIGGER trigger_update_event_attribute_count
            AFTER INSERT OR DELETE ON attributes
            FOR EACH ROW EXECUTE FUNCTION update_event_attribute_count();
        
        -- Function to update event timestamps
        CREATE OR REPLACE FUNCTION update_event_timestamp()
        RETURNS TRIGGER AS $$
        BEGIN
            UPDATE events 
            SET timestamp = EXTRACT(epoch FROM NOW())::bigint
            WHERE id = NEW.event_id;
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;
        
        -- Trigger for event timestamp updates on attribute changes
        DROP TRIGGER IF EXISTS trigger_update_event_timestamp_on_attribute ON attributes;
        CREATE TRIGGER trigger_update_event_timestamp_on_attribute
            AFTER INSERT OR UPDATE OR DELETE ON attributes
            FOR EACH ROW EXECUTE FUNCTION update_event_timestamp();
        
        -- Function to invalidate correlation cache
        CREATE OR REPLACE FUNCTION invalidate_correlation_cache()
        RETURNS TRIGGER AS $$
        BEGIN
            -- Notify correlation cache invalidation
            PERFORM pg_notify('correlation_cache_invalidate', 
                json_build_object(
                    'event_id', COALESCE(NEW.event_id, OLD.event_id),
                    'attribute_id', COALESCE(NEW.id, OLD.id),
                    'value_hash', COALESCE(
                        encode(sha256(NEW.value1::bytea), 'hex'),
                        encode(sha256(OLD.value1::bytea), 'hex')
                    )
                )::text
            );
            RETURN COALESCE(NEW, OLD);
        END;
        $$ LANGUAGE plpgsql;
        
        -- Trigger for correlation cache invalidation
        DROP TRIGGER IF EXISTS trigger_invalidate_correlation_cache ON attributes;
        CREATE TRIGGER trigger_invalidate_correlation_cache
            AFTER INSERT OR UPDATE OR DELETE ON attributes
            FOR EACH ROW EXECUTE FUNCTION invalidate_correlation_cache();
        
        -- Function to update object statistics
        CREATE OR REPLACE FUNCTION update_object_statistics()
        RETURNS TRIGGER AS $$
        BEGIN
            IF TG_OP = 'INSERT' THEN
                UPDATE objects 
                SET attribute_count = (
                    SELECT COUNT(*) FROM attributes 
                    WHERE object_id = NEW.object_id AND deleted = false
                )
                WHERE id = NEW.object_id;
                RETURN NEW;
            ELSIF TG_OP = 'DELETE' THEN
                UPDATE objects 
                SET attribute_count = (
                    SELECT COUNT(*) FROM attributes 
                    WHERE object_id = OLD.object_id AND deleted = false
                )
                WHERE id = OLD.object_id;
                RETURN OLD;
            ELSIF TG_OP = 'UPDATE' THEN
                -- Update both old and new objects if object_id changed
                IF OLD.object_id != NEW.object_id THEN
                    UPDATE objects 
                    SET attribute_count = (
                        SELECT COUNT(*) FROM attributes 
                        WHERE object_id = OLD.object_id AND deleted = false
                    )
                    WHERE id = OLD.object_id;
                    
                    UPDATE objects 
                    SET attribute_count = (
                        SELECT COUNT(*) FROM attributes 
                        WHERE object_id = NEW.object_id AND deleted = false
                    )
                    WHERE id = NEW.object_id;
                ELSE
                    -- Update current object
                    UPDATE objects 
                    SET attribute_count = (
                        SELECT COUNT(*) FROM attributes 
                        WHERE object_id = NEW.object_id AND deleted = false
                    )
                    WHERE id = NEW.object_id;
                END IF;
                RETURN NEW;
            END IF;
            RETURN NULL;
        END;
        $$ LANGUAGE plpgsql;
        
        -- Trigger for object statistics updates
        DROP TRIGGER IF EXISTS trigger_update_object_statistics ON attributes;
        CREATE TRIGGER trigger_update_object_statistics
            AFTER INSERT OR UPDATE OR DELETE ON attributes
            FOR EACH ROW EXECUTE FUNCTION update_object_statistics();
        
        -- Function to maintain correlation consistency
        CREATE OR REPLACE FUNCTION maintain_correlation_consistency()
        RETURNS TRIGGER AS $$
        BEGIN
            IF TG_OP = 'DELETE' THEN
                -- Clean up correlations when attribute is deleted
                DELETE FROM correlations 
                WHERE attribute_id = OLD.id OR 1_attribute_id = OLD.id;
                RETURN OLD;
            ELSIF TG_OP = 'UPDATE' THEN
                -- Update correlations if attribute value changed
                IF OLD.value1 != NEW.value1 OR OLD.to_ids != NEW.to_ids THEN
                    DELETE FROM correlations 
                    WHERE attribute_id = NEW.id OR 1_attribute_id = NEW.id;
                    
                    -- Notify correlation rebuild needed
                    PERFORM pg_notify('correlation_rebuild', 
                        json_build_object(
                            'attribute_id', NEW.id,
                            'value_hash', encode(sha256(NEW.value1::bytea), 'hex')
                        )::text
                    );
                END IF;
                RETURN NEW;
            END IF;
            RETURN NULL;
        END;
        $$ LANGUAGE plpgsql;
        
        -- Trigger for correlation consistency
        DROP TRIGGER IF EXISTS trigger_maintain_correlation_consistency ON attributes;
        CREATE TRIGGER trigger_maintain_correlation_consistency
            AFTER UPDATE OR DELETE ON attributes
            FOR EACH ROW EXECUTE FUNCTION maintain_correlation_consistency();
        """

    @staticmethod
    def get_monitoring_views() -> str:
        """Get monitoring views for MISP performance tracking"""
        return """
        -- MISP Performance Monitoring Views
        -- Real-time monitoring and analytics for MISP operations
        
        -- Event statistics view
        CREATE OR REPLACE VIEW misp_event_statistics AS
        SELECT 
            DATE(to_timestamp(e.timestamp)) as event_date,
            COUNT(*) as total_events,
            COUNT(*) FILTER (WHERE e.published = true) as published_events,
            COUNT(*) FILTER (WHERE e.analysis = 0) as initial_events,
            COUNT(*) FILTER (WHERE e.analysis = 1) as ongoing_events,
            COUNT(*) FILTER (WHERE e.analysis = 2) as complete_events,
            AVG(e.attribute_count) as avg_attributes_per_event,
            MAX(e.attribute_count) as max_attributes_per_event,
            COUNT(DISTINCT e.org_id) as contributing_orgs,
            COUNT(DISTINCT e.threat_level_id) as threat_levels_used
        FROM events e 
        WHERE e.timestamp >= EXTRACT(epoch FROM NOW() - interval '30 days')::bigint
        GROUP BY DATE(to_timestamp(e.timestamp))
        ORDER BY event_date DESC;
        
        -- Attribute type distribution view
        CREATE OR REPLACE VIEW misp_attribute_distribution AS
        SELECT 
            a.type,
            a.category,
            COUNT(*) as total_count,
            COUNT(*) FILTER (WHERE a.to_ids = true) as indicators_count,
            COUNT(DISTINCT a.event_id) as unique_events,
            COUNT(DISTINCT s.id) as sightings_count,
            AVG(CASE WHEN s.id IS NOT NULL THEN 1 ELSE 0 END) as avg_sightings_ratio
        FROM attributes a 
        LEFT JOIN sightings s ON a.id = s.attribute_id
        WHERE a.deleted = false 
            AND a.timestamp >= EXTRACT(epoch FROM NOW() - interval '30 days')::bigint
        GROUP BY a.type, a.category
        ORDER BY total_count DESC;
        
        -- Organization activity view
        CREATE OR REPLACE VIEW misp_org_activity AS
        SELECT 
            o.name as org_name,
            o.nationality,
            o.sector,
            COUNT(DISTINCT e.id) as events_created,
            COUNT(DISTINCT a.id) as attributes_created,
            COUNT(DISTINCT u.id) as active_users,
            MAX(e.timestamp) as last_event_timestamp,
            COUNT(DISTINCT e.id) FILTER (WHERE e.published = true) as published_events,
            AVG(e.attribute_count) as avg_attributes_per_event
        FROM organisations o
        LEFT JOIN events e ON o.id = e.org_id 
            AND e.timestamp >= EXTRACT(epoch FROM NOW() - interval '30 days')::bigint
        LEFT JOIN attributes a ON e.id = a.event_id AND a.deleted = false
        LEFT JOIN users u ON o.id = u.org_id AND u.disabled = false
        GROUP BY o.id, o.name, o.nationality, o.sector
        ORDER BY events_created DESC;
        
        -- Correlation performance view
        CREATE OR REPLACE VIEW misp_correlation_statistics AS
        SELECT 
            DATE(to_timestamp(c.event_id::bigint)) as correlation_date,
            COUNT(*) as total_correlations,
            COUNT(DISTINCT c.value) as unique_values,
            COUNT(DISTINCT c.event_id) as correlated_events,
            COUNT(DISTINCT c.org_id) as contributing_orgs,
            AVG(subq.correlation_count) as avg_correlations_per_value
        FROM correlations c
        JOIN (
            SELECT value, COUNT(*) as correlation_count
            FROM correlations 
            GROUP BY value
        ) subq ON c.value = subq.value
        WHERE c.private = false
        GROUP BY DATE(to_timestamp(c.event_id::bigint))
        ORDER BY correlation_date DESC;
        
        -- Tag usage statistics view
        CREATE OR REPLACE VIEW misp_tag_statistics AS
        SELECT 
            t.name as tag_name,
            t.colour as tag_colour,
            COUNT(DISTINCT et.event_id) as event_usage,
            COUNT(DISTINCT at.attribute_id) as attribute_usage,
            COUNT(DISTINCT et.event_id) + COUNT(DISTINCT at.attribute_id) as total_usage,
            COUNT(DISTINCT COALESCE(e.org_id, a.event_id)) as unique_contexts
        FROM tags t
        LEFT JOIN event_tags et ON t.id = et.tag_id
        LEFT JOIN attribute_tags at ON t.id = at.tag_id
        LEFT JOIN events e ON et.event_id = e.id
        LEFT JOIN attributes a ON at.attribute_id = a.id AND a.deleted = false
        WHERE t.hide_tag = false
        GROUP BY t.id, t.name, t.colour
        HAVING COUNT(DISTINCT et.event_id) + COUNT(DISTINCT at.attribute_id) > 0
        ORDER BY total_usage DESC;
        
        -- Sightings activity view
        CREATE OR REPLACE VIEW misp_sightings_activity AS
        SELECT 
            DATE(s.date_sighting) as sighting_date,
            s.type as sighting_type,
            COUNT(*) as total_sightings,
            COUNT(DISTINCT s.attribute_id) as unique_attributes,
            COUNT(DISTINCT s.event_id) as unique_events,
            COUNT(DISTINCT s.org_id) as contributing_orgs,
            AVG(CASE WHEN s.type = 0 THEN 1 ELSE 0 END) as positive_ratio,
            AVG(CASE WHEN s.type = 1 THEN 1 ELSE 0 END) as false_positive_ratio
        FROM sightings s
        WHERE s.date_sighting >= CURRENT_DATE - interval '30 days'
        GROUP BY DATE(s.date_sighting), s.type
        ORDER BY sighting_date DESC, sighting_type;
        
        -- Performance metrics view
        CREATE OR REPLACE VIEW misp_performance_metrics AS
        SELECT 
            'events' as table_name,
            COUNT(*) as total_records,
            COUNT(*) FILTER (WHERE timestamp >= EXTRACT(epoch FROM NOW() - interval '24 hours')::bigint) as records_24h,
            COUNT(*) FILTER (WHERE timestamp >= EXTRACT(epoch FROM NOW() - interval '7 days')::bigint) as records_7d,
            pg_size_pretty(pg_total_relation_size('events')) as table_size
        FROM events
        UNION ALL
        SELECT 
            'attributes' as table_name,
            COUNT(*) as total_records,
            COUNT(*) FILTER (WHERE timestamp >= EXTRACT(epoch FROM NOW() - interval '24 hours')::bigint) as records_24h,
            COUNT(*) FILTER (WHERE timestamp >= EXTRACT(epoch FROM NOW() - interval '7 days')::bigint) as records_7d,
            pg_size_pretty(pg_total_relation_size('attributes')) as table_size
        FROM attributes WHERE deleted = false
        UNION ALL
        SELECT 
            'correlations' as table_name,
            COUNT(*) as total_records,
            0 as records_24h,  -- Correlations don't have timestamps
            0 as records_7d,
            pg_size_pretty(pg_total_relation_size('correlations')) as table_size
        FROM correlations
        UNION ALL
        SELECT 
            'sightings' as table_name,
            COUNT(*) as total_records,
            COUNT(*) FILTER (WHERE date_sighting >= CURRENT_DATE - interval '24 hours') as records_24h,
            COUNT(*) FILTER (WHERE date_sighting >= CURRENT_DATE - interval '7 days') as records_7d,
            pg_size_pretty(pg_total_relation_size('sightings')) as table_size
        FROM sightings;
        
        -- System health view
        CREATE OR REPLACE VIEW misp_system_health AS
        SELECT 
            'Database Size' as metric,
            pg_size_pretty(pg_database_size(current_database())) as value,
            'info' as status
        UNION ALL
        SELECT 
            'Active Connections' as metric,
            COUNT(*)::text as value,
            CASE 
                WHEN COUNT(*) > 80 THEN 'warning'
                WHEN COUNT(*) > 100 THEN 'critical'
                ELSE 'ok'
            END as status
        FROM pg_stat_activity 
        WHERE state = 'active'
        UNION ALL
        SELECT 
            'Events Last 24h' as metric,
            COUNT(*)::text as value,
            CASE 
                WHEN COUNT(*) = 0 THEN 'warning'
                ELSE 'ok'
            END as status
        FROM events 
        WHERE timestamp >= EXTRACT(epoch FROM NOW() - interval '24 hours')::bigint
        UNION ALL
        SELECT 
            'Cache Hit Ratio' as metric,
            ROUND(
                CASE 
                    WHEN blks_hit + blks_read = 0 THEN 0
                    ELSE (blks_hit::float / (blks_hit + blks_read)) * 100
                END, 2
            )::text || '%' as value,
            CASE 
                WHEN (blks_hit::float / NULLIF(blks_hit + blks_read, 0)) < 0.9 THEN 'warning'
                WHEN (blks_hit::float / NULLIF(blks_hit + blks_read, 0)) < 0.8 THEN 'critical'
                ELSE 'ok'
            END as status
        FROM pg_stat_database 
        WHERE datname = current_database();
        """

    @staticmethod
    def get_maintenance_procedures() -> str:
        """Get database maintenance procedures"""
        return """
        -- MISP Database Maintenance Procedures
        -- Automated maintenance for optimal performance
        
        -- Procedure to rebuild correlation cache
        CREATE OR REPLACE FUNCTION rebuild_correlation_cache(
            batch_size INTEGER DEFAULT 1000,
            max_correlations INTEGER DEFAULT 100000
        )
        RETURNS TABLE(processed_attributes INTEGER, correlations_created INTEGER) AS $$
        DECLARE
            attr_cursor CURSOR FOR 
                SELECT id, event_id, value1, to_ids, deleted 
                FROM attributes 
                WHERE to_ids = true AND deleted = false
                ORDER BY id;
            
            current_attr RECORD;
            batch_count INTEGER := 0;
            total_processed INTEGER := 0;
            total_correlations INTEGER := 0;
            correlation_count INTEGER;
        BEGIN
            -- Clear existing correlation cache
            TRUNCATE TABLE misp_correlation_cache;
            
            FOR current_attr IN attr_cursor LOOP
                -- Check for correlations with this attribute value
                SELECT COUNT(*) INTO correlation_count
                FROM attributes a2
                WHERE a2.value1 = current_attr.value1
                    AND a2.to_ids = true
                    AND a2.deleted = false
                    AND a2.id != current_attr.id;
                
                -- Only cache if there are correlations
                IF correlation_count > 0 THEN
                    INSERT INTO misp_correlation_cache (
                        value_hash,
                        attribute_ids,
                        correlation_count,
                        last_seen
                    )
                    VALUES (
                        encode(sha256(current_attr.value1::bytea), 'hex'),
                        ARRAY(
                            SELECT a3.id
                            FROM attributes a3
                            WHERE a3.value1 = current_attr.value1
                                AND a3.to_ids = true
                                AND a3.deleted = false
                            ORDER BY a3.timestamp DESC
                            LIMIT 100  -- Limit per correlation
                        ),
                        correlation_count,
                        NOW()
                    )
                    ON CONFLICT (value_hash) DO UPDATE SET
                        attribute_ids = EXCLUDED.attribute_ids,
                        correlation_count = EXCLUDED.correlation_count,
                        last_seen = EXCLUDED.last_seen;
                    
                    total_correlations := total_correlations + correlation_count;
                END IF;
                
                total_processed := total_processed + 1;
                batch_count := batch_count + 1;
                
                -- Process in batches
                IF batch_count >= batch_size THEN
                    COMMIT;
                    batch_count := 0;
                    
                    -- Break if we've hit the correlation limit
                    IF total_correlations >= max_correlations THEN
                        EXIT;
                    END IF;
                END IF;
            END LOOP;
            
            RETURN QUERY SELECT total_processed, total_correlations;
        END;
        $$ LANGUAGE plpgsql;
        
        -- Procedure to clean up old data
        CREATE OR REPLACE FUNCTION cleanup_old_data(
            days_to_keep INTEGER DEFAULT 365
        )
        RETURNS TABLE(
            table_name TEXT,
            records_deleted INTEGER
        ) AS $$
        DECLARE
            cutoff_timestamp BIGINT;
            cutoff_date DATE;
            deleted_count INTEGER;
        BEGIN
            cutoff_timestamp := EXTRACT(epoch FROM NOW() - (days_to_keep || ' days')::interval)::bigint;
            cutoff_date := CURRENT_DATE - (days_to_keep || ' days')::interval;
            
            -- Clean up old access logs
            DELETE FROM access_logs WHERE created < cutoff_date;
            GET DIAGNOSTICS deleted_count = ROW_COUNT;
            RETURN QUERY SELECT 'access_logs'::TEXT, deleted_count;
            
            -- Clean up old sightings (keep recent ones)
            DELETE FROM sightings WHERE date_sighting < cutoff_date;
            GET DIAGNOSTICS deleted_count = ROW_COUNT;
            RETURN QUERY SELECT 'sightings'::TEXT, deleted_count;
            
            -- Clean up soft-deleted attributes (permanently remove after retention period)
            DELETE FROM attributes 
            WHERE deleted = true 
                AND timestamp < cutoff_timestamp;
            GET DIAGNOSTICS deleted_count = ROW_COUNT;
            RETURN QUERY SELECT 'attributes_permanent'::TEXT, deleted_count;
            
            -- Clean up orphaned correlations
            DELETE FROM correlations c
            WHERE NOT EXISTS (
                SELECT 1 FROM attributes a 
                WHERE a.id = c.attribute_id AND a.deleted = false
            );
            GET DIAGNOSTICS deleted_count = ROW_COUNT;
            RETURN QUERY SELECT 'correlations_orphaned'::TEXT, deleted_count;
            
            -- Clean up correlation cache older than 7 days
            DELETE FROM misp_correlation_cache 
            WHERE last_seen < NOW() - interval '7 days';
            GET DIAGNOSTICS deleted_count = ROW_COUNT;
            RETURN QUERY SELECT 'correlation_cache_old'::TEXT, deleted_count;
        END;
        $$ LANGUAGE plpgsql;
        
        -- Procedure to update database statistics
        CREATE OR REPLACE FUNCTION update_misp_statistics()
        RETURNS VOID AS $$
        BEGIN
            -- Analyze all MISP tables for query planner
            ANALYZE events;
            ANALYZE attributes;
            ANALYZE objects;
            ANALYZE organisations;
            ANALYZE users;
            ANALYZE tags;
            ANALYZE attribute_tags;
            ANALYZE event_tags;
            ANALYZE sightings;
            ANALYZE correlations;
            ANALYZE taxonomies;
            ANALYZE taxonomy_predicates;
            ANALYZE taxonomy_entries;
            ANALYZE galaxies;
            ANALYZE galaxy_clusters;
            ANALYZE sharing_groups;
            ANALYZE sharing_group_orgs;
            ANALYZE servers;
            ANALYZE feeds;
            ANALYZE warninglists;
            ANALYZE warninglist_entries;
            ANALYZE access_logs;
            ANALYZE auth_keys;
            ANALYZE threads;
            ANALYZE posts;
            ANALYZE workflows;
            
            -- Update correlation cache statistics
            ANALYZE misp_correlation_cache;
            
            RAISE NOTICE 'MISP database statistics updated successfully';
        END;
        $$ LANGUAGE plpgsql;
        
        -- Procedure to vacuum and reindex critical tables
        CREATE OR REPLACE FUNCTION maintain_misp_tables()
        RETURNS VOID AS $$
        BEGIN
            -- Vacuum critical tables (non-blocking)
            VACUUM (ANALYZE) events;
            VACUUM (ANALYZE) attributes;
            VACUUM (ANALYZE) correlations;
            VACUUM (ANALYZE) sightings;
            VACUUM (ANALYZE) access_logs;
            
            -- Reindex critical indexes if fragmentation is high
            REINDEX INDEX CONCURRENTLY idx_attributes_value1_hash;
            REINDEX INDEX CONCURRENTLY idx_attributes_fulltext;
            REINDEX INDEX CONCURRENTLY idx_events_pagination;
            REINDEX INDEX CONCURRENTLY idx_correlations_value;
            
            RAISE NOTICE 'MISP table maintenance completed successfully';
        END;
        $$ LANGUAGE plpgsql;
        """


class MispDatabaseInitializer:
    """Database initialization and schema management for MISP"""

    def __init__(self, database_url: str):
        """Initialize with database connection"""
        from sqlalchemy import create_engine
        from sqlalchemy.orm import sessionmaker

        self.engine = create_engine(database_url)
        self.Session = sessionmaker(bind=self.engine)

    def initialize_schema(self) -> None:
        """Initialize complete MISP schema with all artifacts"""
        with self.engine.connect() as conn:
            # Run initialization SQL
            conn.execute(text(MispSchemaArtifacts.get_initialization_sql()))
            conn.commit()

            # Create all tables using SQLAlchemy models
            MispBaseModel.metadata.create_all(self.engine)

            # Add performance indexes
            conn.execute(text(MispSchemaArtifacts.get_performance_indexes()))
            conn.commit()

            # Add constraints and triggers
            conn.execute(
                text(MispSchemaArtifacts.get_constraints_and_triggers()))
            conn.commit()

            # Create monitoring views
            conn.execute(text(MispSchemaArtifacts.get_monitoring_views()))
            conn.commit()

            # Add maintenance procedures
            conn.execute(
                text(MispSchemaArtifacts.get_maintenance_procedures()))
            conn.commit()

    def get_schema_validation_query(self) -> str:
        """Get query to validate schema is properly initialized"""
        return """
        SELECT 
            COUNT(*) FILTER (WHERE table_type = 'BASE TABLE') as table_count,
            COUNT(*) FILTER (WHERE table_type = 'VIEW') as view_count,
            (SELECT COUNT(*) FROM pg_indexes WHERE schemaname = 'public') as index_count,
            (SELECT COUNT(*) FROM pg_trigger) as trigger_count,
            (SELECT COUNT(*) FROM pg_proc WHERE pronamespace = 
                (SELECT oid FROM pg_namespace WHERE nspname = 'public')) as function_count
        FROM information_schema.tables 
        WHERE table_schema = 'public' AND table_name LIKE '%misp%' OR table_name IN (
            'events', 'attributes', 'objects', 'organisations', 'users', 
            'tags', 'sightings', 'correlations', 'taxonomies', 'galaxies'
        );
        """

    def seed_initial_data(self) -> None:
        """Seed database with initial MISP data"""
        with self.Session() as session:
            from apps.security_service.src.data.models.misp import (
                AdminSetting, Role, ThreatLevel)

            # Create default threat levels
            threat_levels = [
                ThreatLevel(id=1, name="High", description="High threat level",
                            form_description="High"),
                ThreatLevel(id=2, name="Medium", description="Medium threat level",
                            form_description="Medium"),
                ThreatLevel(id=3, name="Low", description="Low threat level",
                            form_description="Low"),
                ThreatLevel(id=4, name="Undefined", description="Undefined threat level",
                            form_description="Undefined")
            ]

            for tl in threat_levels:
                existing = session.query(
                    ThreatLevel).filter_by(id=tl.id).first()
                if not existing:
                    session.add(tl)

            # Create default roles
            roles = [
                Role(id=1, name="admin", created=func.now(), modified=func.now(),
                     perm_add=True, perm_modify=True, perm_publish=True,
                     perm_delegate=True, perm_sync=True, perm_admin=True,
                     perm_audit=True, perm_auth=True, default_role=False),
                Role(id=2, name="Org Admin", created=func.now(), modified=func.now(),
                     perm_add=True, perm_modify=True, perm_publish=True,
                     perm_delegate=True, perm_sync=True, perm_admin=False,
                     perm_audit=True, perm_auth=True, default_role=False),
                Role(id=3, name="User", created=func.now(), modified=func.now(),
                     perm_add=True, perm_modify=True, perm_publish=False,
                     perm_delegate=False, perm_sync=False, perm_admin=False,
                     perm_audit=False, perm_auth=False, default_role=True)
            ]

            for role in roles:
                existing = session.query(Role).filter_by(id=role.id).first()
                if not existing:
                    session.add(role)

            # Create initial admin settings
            admin_settings = [
                AdminSetting(setting="MISP.baseurl",
                             value="https://localhost"),
                AdminSetting(setting="MISP.live", value="true"),
                AdminSetting(setting="MISP.language", value="eng"),
                AdminSetting(
                    setting="MISP.default_event_distribution", value="0"),
                AdminSetting(
                    setting="MISP.default_attribute_distribution", value="5"),
                AdminSetting(setting="MISP.redis_host", value="127.0.0.1"),
                AdminSetting(setting="MISP.redis_port", value="6379"),
                AdminSetting(setting="MISP.redis_password", value=""),
                AdminSetting(setting="MISP.redis_database", value="13"),
                AdminSetting(setting="db_version", value="11")
            ]

            for setting in admin_settings:
                existing = session.query(AdminSetting).filter_by(
                    setting=setting.setting
                ).first()
                if not existing:
                    session.add(setting)

            session.commit()
