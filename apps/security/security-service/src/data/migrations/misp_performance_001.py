"""MISP Performance Migration Script

Database migration to implement MISP performance patterns in PostgreSQL.
Creates indexes, materialized views, and optimization structures.
"""

import logging

import sqlalchemy as sa
from alembic import op
from sqlalchemy import text

logger = logging.getLogger(__name__)

# Revision identifiers
revision = 'misp_performance_001'
down_revision = 'misp_models_001'
branch_labels = None
depends_on = None


def upgrade():
    """Apply MISP performance optimizations"""
    logger.info("Applying MISP performance optimizations")

    # Get database connection
    conn = op.get_bind()

    # 1. Correlation Optimization Indexes
    logger.info("Creating correlation optimization indexes")

    correlation_indexes = [
        # Fast value lookups for correlation matching
        """
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_correlation_values_fast 
        ON attributes USING btree (
            sha256(COALESCE(value1, '') || '|' || COALESCE(value2, ''))
        ) WHERE deleted = false
        """,

        # Attribute correlation compound index
        """
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_attr_correlation_compound 
        ON attributes USING btree (value1, type, category) 
        WHERE deleted = false
        """,

        # Event correlation tracking
        """
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_event_correlation_stats 
        ON events USING btree (correlation_count, published) 
        WHERE deleted = false
        """,

        # Temporal correlation patterns
        """
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_attr_temporal_correlation 
        ON attributes USING btree (timestamp, event_id) 
        WHERE deleted = false
        """,
    ]

    for index_sql in correlation_indexes:
        try:
            conn.execute(text(index_sql))
            logger.info("Created correlation index")
        except Exception as e:
            logger.warning(f"Correlation index creation failed: {e}")

    # 2. Event Pagination Optimization
    logger.info("Creating event pagination indexes")

    pagination_indexes = [
        # Covering index for event list queries
        """
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_events_list_covering 
        ON events USING btree (published, distribution, date DESC) 
        INCLUDE (id, uuid, info, threat_level_id, org_id, attribute_count)
        WHERE deleted = false
        """,

        # Organization-specific event queries
        """
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_events_org_date 
        ON events USING btree (org_id, date DESC, published) 
        WHERE deleted = false
        """,

        # Distribution-based queries with statistics
        """
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_events_distribution_stats 
        ON events USING btree (distribution, attribute_count DESC, date DESC) 
        WHERE published = true AND deleted = false
        """,
    ]

    for index_sql in pagination_indexes:
        try:
            conn.execute(text(index_sql))
            logger.info("Created pagination index")
        except Exception as e:
            logger.warning(f"Pagination index creation failed: {e}")

    # 3. Full-Text Search Optimization
    logger.info("Creating full-text search indexes")

    # Enable pg_trgm extension for fuzzy search
    try:
        conn.execute(text("CREATE EXTENSION IF NOT EXISTS pg_trgm"))
        logger.info("Enabled pg_trgm extension")
    except Exception as e:
        logger.warning(f"Could not enable pg_trgm: {e}")

    search_indexes = [
        # Full-text search on attribute values
        """
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_attributes_fulltext_gin
        ON attributes USING gin (
            to_tsvector('english', 
                COALESCE(value1, '') || ' ' || 
                COALESCE(value2, '') || ' ' || 
                COALESCE(comment, '')
            )
        ) WHERE deleted = false
        """,

        # Event info full-text search
        """
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_events_fulltext_gin
        ON events USING gin (to_tsvector('english', info))
        WHERE deleted = false
        """,

        # Trigram search for fuzzy matching
        """
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_attributes_trigram_gin
        ON attributes USING gin (value1 gin_trgm_ops)
        WHERE deleted = false
        """,

        # Tag-based search optimization
        """
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_tags_search_gin
        ON tags USING gin (to_tsvector('english', name))
        """,
    ]

    for index_sql in search_indexes:
        try:
            conn.execute(text(index_sql))
            logger.info("Created search index")
        except Exception as e:
            logger.warning(f"Search index creation failed: {e}")

    # 4. Correlation Cache Table
    logger.info("Creating correlation cache table")

    correlation_cache_sql = """
    CREATE TABLE IF NOT EXISTS correlation_cache (
        id SERIAL PRIMARY KEY,
        value_hash VARCHAR(64) NOT NULL UNIQUE,
        attribute_ids INTEGER[] NOT NULL,
        correlation_count INTEGER NOT NULL DEFAULT 0,
        last_updated TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
        expires_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() + INTERVAL '1 hour'
    );
    
    CREATE INDEX IF NOT EXISTS idx_correlation_cache_hash 
    ON correlation_cache USING btree (value_hash);
    
    CREATE INDEX IF NOT EXISTS idx_correlation_cache_expires 
    ON correlation_cache USING btree (expires_at);
    
    -- Cleanup trigger for expired entries
    CREATE OR REPLACE FUNCTION cleanup_correlation_cache()
    RETURNS TRIGGER AS $$
    BEGIN
        DELETE FROM correlation_cache WHERE expires_at < NOW() - INTERVAL '1 hour';
        RETURN NULL;
    END;
    $$ LANGUAGE plpgsql;
    
    DROP TRIGGER IF EXISTS trigger_cleanup_correlation_cache ON correlation_cache;
    CREATE TRIGGER trigger_cleanup_correlation_cache
        AFTER INSERT ON correlation_cache
        FOR EACH STATEMENT EXECUTE FUNCTION cleanup_correlation_cache();
    """

    conn.execute(text(correlation_cache_sql))
    logger.info("Created correlation cache table")

    # 5. Event Statistics Denormalization
    logger.info("Setting up event statistics denormalization")

    stats_function_sql = """
    CREATE OR REPLACE FUNCTION update_event_statistics()
    RETURNS TRIGGER AS $$
    BEGIN
        IF TG_OP = 'INSERT' OR TG_OP = 'UPDATE' THEN
            -- Update attribute count
            UPDATE events SET 
                attribute_count = (
                    SELECT COUNT(*) 
                    FROM attributes 
                    WHERE event_id = NEW.event_id AND deleted = false
                )
            WHERE id = NEW.event_id;
            
            RETURN NEW;
        ELSIF TG_OP = 'DELETE' THEN
            -- Update attribute count after deletion
            UPDATE events SET 
                attribute_count = (
                    SELECT COUNT(*) 
                    FROM attributes 
                    WHERE event_id = OLD.event_id AND deleted = false
                )
            WHERE id = OLD.event_id;
            
            RETURN OLD;
        END IF;
        
        RETURN NULL;
    END;
    $$ LANGUAGE plpgsql;
    
    -- Create triggers for automatic statistics updates
    DROP TRIGGER IF EXISTS trigger_update_event_stats ON attributes;
    CREATE TRIGGER trigger_update_event_stats
        AFTER INSERT OR UPDATE OR DELETE ON attributes
        FOR EACH ROW EXECUTE FUNCTION update_event_statistics();
    """

    conn.execute(text(stats_function_sql))
    logger.info("Created event statistics triggers")

    # 6. Export Optimization Materialized View
    logger.info("Creating export optimization materialized view")

    export_view_sql = """
    CREATE MATERIALIZED VIEW IF NOT EXISTS event_export_cache AS
    SELECT 
        e.id as event_id,
        e.uuid, e.info, e.date, e.threat_level_id, e.analysis,
        e.distribution, e.published, e.org_id, e.orgc_id,
        e.attribute_count, e.created, e.modified,
        json_agg(
            DISTINCT jsonb_build_object(
                'id', a.id,
                'type', a.type,
                'category', a.category, 
                'value', CASE WHEN a.value2 IS NOT NULL 
                       THEN a.value1 || '|' || a.value2 
                       ELSE a.value1 END,
                'comment', a.comment,
                'to_ids', a.to_ids,
                'timestamp', a.timestamp,
                'object_id', a.object_id,
                'object_relation', a.object_relation
            )
        ) FILTER (WHERE a.id IS NOT NULL) as attributes,
        json_agg(
            DISTINCT jsonb_build_object(
                'id', o.id,
                'name', o.name,
                'meta_category', o.meta_category,
                'template_uuid', o.template_uuid,
                'template_version', o.template_version,
                'comment', o.comment
            )
        ) FILTER (WHERE o.id IS NOT NULL) as objects
    FROM events e
    LEFT JOIN attributes a ON e.id = a.event_id AND a.deleted = false
    LEFT JOIN objects o ON e.id = o.event_id AND o.deleted = false
    WHERE e.deleted = false
    GROUP BY e.id, e.uuid, e.info, e.date, e.threat_level_id, e.analysis,
             e.distribution, e.published, e.org_id, e.orgc_id,
             e.attribute_count, e.created, e.modified;
    
    CREATE UNIQUE INDEX IF NOT EXISTS idx_event_export_cache_id 
    ON event_export_cache (event_id);
    
    CREATE INDEX IF NOT EXISTS idx_event_export_cache_uuid
    ON event_export_cache (uuid);
    
    CREATE INDEX IF NOT EXISTS idx_event_export_cache_published
    ON event_export_cache (published, date DESC);
    """

    conn.execute(text(export_view_sql))
    logger.info("Created event export cache materialized view")

    # 7. Background Sync Queue
    logger.info("Creating background sync queue")

    sync_queue_sql = """
    CREATE TABLE IF NOT EXISTS correlation_sync_queue (
        id SERIAL PRIMARY KEY,
        source_server_id INTEGER NOT NULL,
        event_uuid VARCHAR(36) NOT NULL,
        sync_type VARCHAR(50) NOT NULL DEFAULT 'correlation',
        priority INTEGER NOT NULL DEFAULT 5,
        status VARCHAR(20) NOT NULL DEFAULT 'pending',
        created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
        scheduled_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
        started_at TIMESTAMP WITH TIME ZONE,
        completed_at TIMESTAMP WITH TIME ZONE,
        error_message TEXT,
        retry_count INTEGER DEFAULT 0,
        max_retries INTEGER DEFAULT 3,
        
        CONSTRAINT unique_server_event UNIQUE (source_server_id, event_uuid)
    );
    
    CREATE INDEX IF NOT EXISTS idx_sync_queue_status_priority
    ON correlation_sync_queue (status, priority, scheduled_at)
    WHERE status = 'pending';
    
    CREATE INDEX IF NOT EXISTS idx_sync_queue_processing
    ON correlation_sync_queue (status, started_at)
    WHERE status = 'processing';
    """

    conn.execute(text(sync_queue_sql))
    logger.info("Created background sync queue")

    # 8. Performance Monitoring Views
    logger.info("Creating performance monitoring views")

    monitoring_views_sql = """
    -- Query performance statistics view
    CREATE OR REPLACE VIEW misp_query_performance AS
    SELECT 
        query,
        calls,
        total_time,
        mean_time,
        min_time,
        max_time,
        rows,
        100.0 * calls / SUM(calls) OVER() AS percentage_calls,
        100.0 * total_time / SUM(total_time) OVER() AS percentage_time
    FROM pg_stat_statements
    WHERE query LIKE '%attributes%' OR query LIKE '%events%' 
       OR query LIKE '%correlations%'
    ORDER BY total_time DESC;
    
    -- Index usage statistics view
    CREATE OR REPLACE VIEW misp_index_usage AS
    SELECT 
        schemaname,
        tablename,
        indexname,
        idx_tup_read,
        idx_tup_fetch,
        idx_scan,
        CASE WHEN idx_scan > 0 
             THEN idx_tup_read::float / idx_scan 
             ELSE 0 END AS avg_tuples_per_scan
    FROM pg_stat_user_indexes
    WHERE schemaname = 'public'
    AND (tablename = 'events' OR tablename = 'attributes' 
         OR tablename = 'correlations')
    ORDER BY idx_scan DESC;
    
    -- Cache hit ratio view
    CREATE OR REPLACE VIEW misp_cache_hit_ratio AS
    SELECT 
        'Database Buffers' as cache_type,
        ROUND(
            100.0 * SUM(heap_blks_hit) / 
            NULLIF(SUM(heap_blks_hit + heap_blks_read), 0), 2
        ) as hit_ratio_percent
    FROM pg_statio_user_tables
    WHERE schemaname = 'public'
    AND (tablename = 'events' OR tablename = 'attributes');
    """

    try:
        conn.execute(text(monitoring_views_sql))
        logger.info("Created performance monitoring views")
    except Exception as e:
        logger.warning(f"Could not create monitoring views: {e}")

    # 9. Refresh Event Statistics
    logger.info("Refreshing event statistics")

    refresh_stats_sql = """
    UPDATE events SET 
        attribute_count = (
            SELECT COUNT(*) 
            FROM attributes 
            WHERE event_id = events.id AND deleted = false
        )
    WHERE deleted = false
    AND attribute_count != (
        SELECT COUNT(*) 
        FROM attributes 
        WHERE event_id = events.id AND deleted = false
    );
    """

    result = conn.execute(text(refresh_stats_sql))
    logger.info(f"Updated statistics for events")

    # 10. Create Performance Configuration
    logger.info("Applying PostgreSQL performance configuration")

    # These are recommendations that should be applied to postgresql.conf
    perf_recommendations = {
        'shared_buffers': '25% of RAM',
        'effective_cache_size': '75% of RAM',
        'work_mem': '4MB-8MB per connection',
        'maintenance_work_mem': '256MB-1GB',
        'checkpoint_timeout': '15min',
        'max_wal_size': '4GB',
        'random_page_cost': '1.1',  # SSD optimization
        'effective_io_concurrency': '200'  # SSD optimization
    }

    logger.info("Performance optimization migration completed successfully")
    logger.info("Recommendations for postgresql.conf:")
    for setting, value in perf_recommendations.items():
        logger.info(f"  {setting} = {value}")


def downgrade():
    """Remove MISP performance optimizations"""
    logger.info("Removing MISP performance optimizations")

    conn = op.get_bind()

    # Drop indexes
    indexes_to_drop = [
        'idx_correlation_values_fast',
        'idx_attr_correlation_compound',
        'idx_event_correlation_stats',
        'idx_attr_temporal_correlation',
        'idx_events_list_covering',
        'idx_events_org_date',
        'idx_events_distribution_stats',
        'idx_attributes_fulltext_gin',
        'idx_events_fulltext_gin',
        'idx_attributes_trigram_gin',
        'idx_tags_search_gin',
        'idx_correlation_cache_hash',
        'idx_correlation_cache_expires',
        'idx_event_export_cache_id',
        'idx_event_export_cache_uuid',
        'idx_event_export_cache_published',
        'idx_sync_queue_status_priority',
        'idx_sync_queue_processing'
    ]

    for index_name in indexes_to_drop:
        try:
            conn.execute(
                text(f"DROP INDEX CONCURRENTLY IF EXISTS {index_name}"))
            logger.info(f"Dropped index {index_name}")
        except Exception as e:
            logger.warning(f"Could not drop index {index_name}: {e}")

    # Drop tables
    tables_to_drop = [
        'correlation_cache',
        'correlation_sync_queue'
    ]

    for table_name in tables_to_drop:
        try:
            conn.execute(text(f"DROP TABLE IF EXISTS {table_name} CASCADE"))
            logger.info(f"Dropped table {table_name}")
        except Exception as e:
            logger.warning(f"Could not drop table {table_name}: {e}")

    # Drop materialized views
    try:
        conn.execute(
            text("DROP MATERIALIZED VIEW IF EXISTS event_export_cache"))
        logger.info("Dropped event export cache materialized view")
    except Exception as e:
        logger.warning(f"Could not drop materialized view: {e}")

    # Drop functions and triggers
    try:
        conn.execute(
            text("DROP TRIGGER IF EXISTS trigger_update_event_stats ON attributes"))
        conn.execute(text("DROP FUNCTION IF EXISTS update_event_statistics()"))
        conn.execute(text(
            "DROP TRIGGER IF EXISTS trigger_cleanup_correlation_cache ON correlation_cache"))
        conn.execute(
            text("DROP FUNCTION IF EXISTS cleanup_correlation_cache()"))
        logger.info("Dropped functions and triggers")
    except Exception as e:
        logger.warning(f"Could not drop functions/triggers: {e}")

    # Drop views
    views_to_drop = [
        'misp_query_performance',
        'misp_index_usage',
        'misp_cache_hit_ratio'
    ]

    for view_name in views_to_drop:
        try:
            conn.execute(text(f"DROP VIEW IF EXISTS {view_name}"))
            logger.info(f"Dropped view {view_name}")
        except Exception as e:
            logger.warning(f"Could not drop view {view_name}: {e}")

    logger.info("Performance optimization rollback completed")
