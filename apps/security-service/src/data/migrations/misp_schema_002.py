"""MISP Schema Artifacts Migration

Revision ID: misp_schema_002
Revises: misp_performance_001
Create Date: 2024-12-28 23:45:00

Migration for MISP database schema artifacts including:
- Database initialization scripts
- Custom data types and enums
- Performance indexes and constraints  
- Triggers for automatic maintenance
- Monitoring views for operational visibility
- Maintenance procedures for database health
"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import ENUM

# revision identifiers
revision = 'misp_schema_002'
down_revision = 'misp_performance_001'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Apply MISP schema artifacts migration"""

    # Enable required PostgreSQL extensions
    op.execute("CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\"")
    op.execute("CREATE EXTENSION IF NOT EXISTS \"pgcrypto\"")

    # Create custom MISP data types
    misp_threat_level = ENUM('1', '2', '3', '4', name='misp_threat_level')
    misp_threat_level.create(op.get_bind())

    misp_analysis_status = ENUM('0', '1', '2', name='misp_analysis_status')
    misp_analysis_status.create(op.get_bind())

    misp_distribution_level = ENUM(
        '0', '1', '2', '3', '4', '5', name='misp_distribution_level')
    misp_distribution_level.create(op.get_bind())

    # Create database functions for triggers
    op.execute("""
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
    """)

    op.execute("""
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
    """)

    op.execute("""
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
    """)

    op.execute("""
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
    """)

    op.execute("""
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
    """)

    # Create database triggers (will be applied after tables exist)
    op.execute("""
        -- Create triggers for automatic maintenance
        -- Note: These are created conditionally since tables may not exist yet
        
        DO $$
        BEGIN
            -- Trigger for attribute count updates
            IF EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'attributes') THEN
                DROP TRIGGER IF EXISTS trigger_update_event_attribute_count ON attributes;
                CREATE TRIGGER trigger_update_event_attribute_count
                    AFTER INSERT OR DELETE ON attributes
                    FOR EACH ROW EXECUTE FUNCTION update_event_attribute_count();
            END IF;
            
            -- Trigger for event timestamp updates on attribute changes
            IF EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'attributes') THEN
                DROP TRIGGER IF EXISTS trigger_update_event_timestamp_on_attribute ON attributes;
                CREATE TRIGGER trigger_update_event_timestamp_on_attribute
                    AFTER INSERT OR UPDATE OR DELETE ON attributes
                    FOR EACH ROW EXECUTE FUNCTION update_event_timestamp();
            END IF;
            
            -- Trigger for correlation cache invalidation
            IF EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'attributes') THEN
                DROP TRIGGER IF EXISTS trigger_invalidate_correlation_cache ON attributes;
                CREATE TRIGGER trigger_invalidate_correlation_cache
                    AFTER INSERT OR UPDATE OR DELETE ON attributes
                    FOR EACH ROW EXECUTE FUNCTION invalidate_correlation_cache();
            END IF;
            
            -- Trigger for object statistics updates
            IF EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'attributes') THEN
                DROP TRIGGER IF EXISTS trigger_update_object_statistics ON attributes;
                CREATE TRIGGER trigger_update_object_statistics
                    AFTER INSERT OR UPDATE OR DELETE ON attributes
                    FOR EACH ROW EXECUTE FUNCTION update_object_statistics();
            END IF;
            
            -- Trigger for correlation consistency
            IF EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'attributes') THEN
                DROP TRIGGER IF EXISTS trigger_maintain_correlation_consistency ON attributes;
                CREATE TRIGGER trigger_maintain_correlation_consistency
                    AFTER UPDATE OR DELETE ON attributes
                    FOR EACH ROW EXECUTE FUNCTION maintain_correlation_consistency();
            END IF;
        END $$;
    """)

    # Create monitoring views
    op.execute("""
        -- Event statistics view
        CREATE OR REPLACE VIEW misp_event_statistics AS
        SELECT 
            DATE(to_timestamp(COALESCE(e.timestamp, 0))) as event_date,
            COUNT(*) as total_events,
            COUNT(*) FILTER (WHERE e.published = true) as published_events,
            COUNT(*) FILTER (WHERE e.analysis = 0) as initial_events,
            COUNT(*) FILTER (WHERE e.analysis = 1) as ongoing_events,
            COUNT(*) FILTER (WHERE e.analysis = 2) as complete_events,
            COALESCE(AVG(e.attribute_count), 0) as avg_attributes_per_event,
            COALESCE(MAX(e.attribute_count), 0) as max_attributes_per_event,
            COUNT(DISTINCT e.org_id) as contributing_orgs,
            COUNT(DISTINCT e.threat_level_id) as threat_levels_used
        FROM events e 
        WHERE COALESCE(e.timestamp, 0) >= EXTRACT(epoch FROM NOW() - interval '30 days')::bigint
        GROUP BY DATE(to_timestamp(COALESCE(e.timestamp, 0)))
        ORDER BY event_date DESC;
    """)

    op.execute("""
        -- Performance metrics view
        CREATE OR REPLACE VIEW misp_performance_metrics AS
        SELECT 
            'events' as table_name,
            COUNT(*) as total_records,
            COUNT(*) FILTER (WHERE COALESCE(timestamp, 0) >= EXTRACT(epoch FROM NOW() - interval '24 hours')::bigint) as records_24h,
            COUNT(*) FILTER (WHERE COALESCE(timestamp, 0) >= EXTRACT(epoch FROM NOW() - interval '7 days')::bigint) as records_7d,
            pg_size_pretty(pg_total_relation_size('events')) as table_size
        FROM events
        UNION ALL
        SELECT 
            'attributes' as table_name,
            COUNT(*) as total_records,
            COUNT(*) FILTER (WHERE COALESCE(timestamp, 0) >= EXTRACT(epoch FROM NOW() - interval '24 hours')::bigint) as records_24h,
            COUNT(*) FILTER (WHERE COALESCE(timestamp, 0) >= EXTRACT(epoch FROM NOW() - interval '7 days')::bigint) as records_7d,
            pg_size_pretty(pg_total_relation_size('attributes')) as table_size
        FROM attributes WHERE deleted = false;
    """)

    op.execute("""
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
    """)

    # Create maintenance procedures
    op.execute("""
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
            IF EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'misp_correlation_cache') THEN
                TRUNCATE TABLE misp_correlation_cache;
            END IF;
            
            FOR current_attr IN attr_cursor LOOP
                -- Check for correlations with this attribute value
                SELECT COUNT(*) INTO correlation_count
                FROM attributes a2
                WHERE a2.value1 = current_attr.value1
                    AND a2.to_ids = true
                    AND a2.deleted = false
                    AND a2.id != current_attr.id;
                
                total_correlations := total_correlations + correlation_count;
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
    """)

    op.execute("""
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
            
            -- Clean up old access logs if table exists
            IF EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'access_logs') THEN
                EXECUTE format('DELETE FROM access_logs WHERE created < %L', cutoff_date);
                GET DIAGNOSTICS deleted_count = ROW_COUNT;
                RETURN QUERY SELECT 'access_logs'::TEXT, deleted_count;
            END IF;
            
            -- Clean up soft-deleted attributes if table exists
            IF EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'attributes') THEN
                EXECUTE format('DELETE FROM attributes WHERE deleted = true AND timestamp < %L', cutoff_timestamp);
                GET DIAGNOSTICS deleted_count = ROW_COUNT;
                RETURN QUERY SELECT 'attributes_permanent'::TEXT, deleted_count;
            END IF;
            
        END;
        $$ LANGUAGE plpgsql;
    """)

    op.execute("""
        -- Procedure to update database statistics
        CREATE OR REPLACE FUNCTION update_misp_statistics()
        RETURNS VOID AS $$
        DECLARE
            table_name TEXT;
        BEGIN
            -- Analyze all MISP tables that exist
            FOR table_name IN 
                SELECT t.table_name 
                FROM information_schema.tables t
                WHERE t.table_schema = 'public' 
                AND t.table_name IN (
                    'events', 'attributes', 'objects', 'organisations', 'users', 
                    'tags', 'attribute_tags', 'event_tags', 'sightings', 'correlations',
                    'taxonomies', 'taxonomy_predicates', 'taxonomy_entries',
                    'galaxies', 'galaxy_clusters', 'sharing_groups', 'sharing_group_orgs',
                    'servers', 'feeds', 'warninglists', 'warninglist_entries',
                    'access_logs', 'auth_keys', 'threads', 'posts', 'workflows'
                )
            LOOP
                EXECUTE format('ANALYZE %I', table_name);
            END LOOP;
            
            RAISE NOTICE 'MISP database statistics updated successfully';
        END;
        $$ LANGUAGE plpgsql;
    """)


def downgrade() -> None:
    """Remove MISP schema artifacts"""

    # Drop maintenance procedures
    op.execute("DROP FUNCTION IF EXISTS update_misp_statistics()")
    op.execute("DROP FUNCTION IF EXISTS cleanup_old_data(INTEGER)")
    op.execute(
        "DROP FUNCTION IF EXISTS rebuild_correlation_cache(INTEGER, INTEGER)")

    # Drop monitoring views
    op.execute("DROP VIEW IF EXISTS misp_system_health")
    op.execute("DROP VIEW IF EXISTS misp_performance_metrics")
    op.execute("DROP VIEW IF EXISTS misp_event_statistics")

    # Drop triggers
    op.execute(
        "DROP TRIGGER IF EXISTS trigger_maintain_correlation_consistency ON attributes")
    op.execute(
        "DROP TRIGGER IF EXISTS trigger_update_object_statistics ON attributes")
    op.execute(
        "DROP TRIGGER IF EXISTS trigger_invalidate_correlation_cache ON attributes")
    op.execute(
        "DROP TRIGGER IF EXISTS trigger_update_event_timestamp_on_attribute ON attributes")
    op.execute(
        "DROP TRIGGER IF EXISTS trigger_update_event_attribute_count ON attributes")

    # Drop trigger functions
    op.execute("DROP FUNCTION IF EXISTS maintain_correlation_consistency()")
    op.execute("DROP FUNCTION IF EXISTS update_object_statistics()")
    op.execute("DROP FUNCTION IF EXISTS invalidate_correlation_cache()")
    op.execute("DROP FUNCTION IF EXISTS update_event_timestamp()")
    op.execute("DROP FUNCTION IF EXISTS update_event_attribute_count()")

    # Drop custom data types
    op.execute("DROP TYPE IF EXISTS misp_distribution_level")
    op.execute("DROP TYPE IF EXISTS misp_analysis_status")
    op.execute("DROP TYPE IF EXISTS misp_threat_level")
