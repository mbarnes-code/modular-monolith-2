"""MISP Query Optimization Patterns

PostgreSQL-specific query optimization patterns based on MISP analysis.
Addresses problematic queries identified in Section 2.3 of MISP analysis.
"""

import hashlib
import json
import logging
from datetime import datetime
from typing import Any, Dict, List, Optional

from redis import Redis
from sqlalchemy import text
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)


class MispQueryOptimizer:
    """
    MISP Query Optimization Patterns for PostgreSQL

    Addresses specific problematic queries identified in MISP analysis:
    1. Full-text search across all attributes (5-30 seconds → <1 second)
    2. Complex event export with relationships (500MB+ memory → streaming)
    3. Cross-MISP correlation queries (30s+ → background async)
    """

    def __init__(self, db_session: Session, redis_client: Redis):
        self.db = db_session
        self.redis = redis_client
        self.search_cache_ttl = 300  # 5 minutes for search results

    def setup_full_text_search_optimization(self):
        """
        Optimize full-text search to achieve <1s performance
        Based on: app/Model/MispAttribute.php restSearch()
        """
        logger.info("Setting up full-text search optimization")

        # Create GIN indexes for full-text search
        search_indexes = [
            # Full-text search on attribute values
            """
            CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_attributes_fulltext_gin
            ON attributes USING gin (
                to_tsvector('english', COALESCE(value1, '') || ' ' || COALESCE(value2, '') || ' ' || COALESCE(comment, ''))
            ) WHERE deleted = false
            """,

            # Event info full-text search
            """
            CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_events_fulltext_gin
            ON events USING gin (to_tsvector('english', info))
            WHERE deleted = false
            """,

            # Combined attribute search with metadata
            """
            CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_attributes_search_compound
            ON attributes USING btree (type, category, to_ids, deleted)
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
                self.db.execute(text(index_sql))
                logger.info("Created full-text search index")
            except Exception as e:
                logger.warning(f"Search index creation failed: {e}")

        self.db.commit()

    def optimized_attribute_search(self,
                                   search_terms: str,
                                   event_ids: List[int] = None,
                                   attribute_types: List[str] = None,
                                   categories: List[str] = None,
                                   tags: List[str] = None,
                                   limit: int = 1000) -> Dict[str, Any]:
        """
        Optimized attribute search using PostgreSQL full-text search
        Replaces slow LIKE queries with GIN index lookups
        """
        cache_key = self._generate_search_cache_key(
            "attr_search", search_terms, event_ids, attribute_types, categories, tags, limit
        )

        # Check cache first
        cached_result = self.redis.get(cache_key)
        if cached_result:
            return json.loads(cached_result)

        # Build optimized search query
        base_query = """
        SELECT a.id, a.event_id, a.type, a.category, a.value1, a.value2, 
               a.comment, a.timestamp, a.to_ids,
               e.info as event_info, e.date as event_date,
               o.name as org_name,
               ts_rank(
                   to_tsvector('english', COALESCE(a.value1, '') || ' ' || COALESCE(a.value2, '') || ' ' || COALESCE(a.comment, '')),
                   plainto_tsquery('english', :search_terms)
               ) as relevance_score
        FROM attributes a
        JOIN events e ON a.event_id = e.id
        JOIN organisations o ON e.org_id = o.id
        WHERE a.deleted = false AND e.deleted = false
        """

        conditions = []
        params = {"search_terms": search_terms, "limit": limit}

        # Full-text search condition
        if search_terms.strip():
            conditions.append("""
                to_tsvector('english', COALESCE(a.value1, '') || ' ' || COALESCE(a.value2, '') || ' ' || COALESCE(a.comment, ''))
                @@ plainto_tsquery('english', :search_terms)
            """)

        # Additional filters
        if event_ids:
            conditions.append("a.event_id = ANY(:event_ids)")
            params["event_ids"] = event_ids

        if attribute_types:
            conditions.append("a.type = ANY(:attr_types)")
            params["attr_types"] = attribute_types

        if categories:
            conditions.append("a.category = ANY(:categories)")
            params["categories"] = categories

        # Tag filtering with exists query
        if tags:
            conditions.append("""
                EXISTS (
                    SELECT 1 FROM attribute_tags at
                    JOIN tags t ON at.tag_id = t.id
                    WHERE at.attribute_id = a.id AND t.name = ANY(:tags)
                )
            """)
            params["tags"] = tags

        if conditions:
            base_query += " AND " + " AND ".join(conditions)

        # Order by relevance for search, timestamp for filters
        if search_terms.strip():
            base_query += " ORDER BY relevance_score DESC, a.timestamp DESC"
        else:
            base_query += " ORDER BY a.timestamp DESC"

        base_query += " LIMIT :limit"

        # Execute optimized query
        start_time = datetime.utcnow()
        results = self.db.execute(text(base_query), params).fetchall()
        query_time = (datetime.utcnow() - start_time).total_seconds()

        search_results = {
            'attributes': [dict(row._mapping) for row in results],
            'count': len(results),
            'query_time_seconds': query_time,
            'search_terms': search_terms
        }

        # Cache results
        self.redis.setex(cache_key, self.search_cache_ttl,
                         json.dumps(search_results, default=str))

        logger.info(
            f"Attribute search completed in {query_time:.3f}s, found {len(results)} results")
        return search_results

    def setup_streaming_export_optimization(self):
        """
        Setup streaming export to handle large events without memory issues
        Based on: app/Model/Event.php fetchEvent() memory intensive operations
        """
        logger.info("Setting up streaming export optimization")

        # Create materialized view for export optimization
        export_view_sql = """
        CREATE MATERIALIZED VIEW IF NOT EXISTS event_export_cache AS
        SELECT 
            e.id as event_id,
            e.uuid, e.info, e.date, e.threat_level_id, e.analysis,
            e.distribution, e.published, e.org_id, e.orgc_id,
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
                    'tags', (
                        SELECT json_agg(t.name)
                        FROM attribute_tags at
                        JOIN tags t ON at.tag_id = t.id
                        WHERE at.attribute_id = a.id
                    )
                )
            ) FILTER (WHERE a.id IS NOT NULL) as attributes,
            json_agg(
                DISTINCT jsonb_build_object(
                    'id', o.id,
                    'name', o.name,
                    'meta_category', o.meta_category,
                    'template_uuid', o.template_uuid,
                    'attributes', (
                        SELECT json_agg(
                            jsonb_build_object(
                                'id', oa.id,
                                'type', oa.type,
                                'value', oa.value1,
                                'object_relation', oa.object_relation
                            )
                        )
                        FROM attributes oa
                        WHERE oa.object_id = o.id AND oa.deleted = false
                    )
                )
            ) FILTER (WHERE o.id IS NOT NULL) as objects
        FROM events e
        LEFT JOIN attributes a ON e.id = a.event_id AND a.deleted = false AND a.object_id IS NULL
        LEFT JOIN objects o ON e.id = o.event_id AND o.deleted = false
        WHERE e.deleted = false
        GROUP BY e.id, e.uuid, e.info, e.date, e.threat_level_id, e.analysis,
                 e.distribution, e.published, e.org_id, e.orgc_id;
        
        CREATE UNIQUE INDEX IF NOT EXISTS idx_event_export_cache_id 
        ON event_export_cache (event_id);
        
        CREATE INDEX IF NOT EXISTS idx_event_export_cache_uuid
        ON event_export_cache (uuid);
        """

        self.db.execute(text(export_view_sql))
        self.db.commit()
        logger.info("Created event export cache materialized view")

    def get_streaming_event_export(self, event_id: int, chunk_size: int = 1000):
        """
        Generator for streaming event export to avoid memory issues
        Yields event data in chunks to prevent 500MB+ memory usage
        """
        # Get basic event info first
        event_query = text("""
            SELECT e.id, e.uuid, e.info, e.date, e.threat_level_id, e.analysis,
                   e.distribution, e.published, e.attribute_count,
                   o.name as org_name, oc.name as orgc_name,
                   tl.name as threat_level_name
            FROM events e
            JOIN organisations o ON e.org_id = o.id
            JOIN organisations oc ON e.orgc_id = oc.id  
            JOIN threat_levels tl ON e.threat_level_id = tl.id
            WHERE e.id = :event_id AND e.deleted = false
        """)

        event = self.db.execute(event_query, {"event_id": event_id}).fetchone()
        if not event:
            return

        # Yield event header
        yield {
            'event_header': dict(event._mapping),
            'chunk_type': 'header'
        }

        # Stream attributes in chunks
        offset = 0
        while True:
            attributes_query = text("""
                SELECT a.id, a.type, a.category, a.value1, a.value2, a.comment,
                       a.to_ids, a.timestamp, a.object_id, a.object_relation,
                       CASE WHEN a.value2 IS NOT NULL 
                            THEN a.value1 || '|' || a.value2 
                            ELSE a.value1 END as value,
                       array_agg(t.name) FILTER (WHERE t.id IS NOT NULL) as tags
                FROM attributes a
                LEFT JOIN attribute_tags at ON a.id = at.attribute_id
                LEFT JOIN tags t ON at.tag_id = t.id
                WHERE a.event_id = :event_id AND a.deleted = false
                GROUP BY a.id, a.type, a.category, a.value1, a.value2, 
                         a.comment, a.to_ids, a.timestamp, a.object_id, a.object_relation
                ORDER BY a.id
                LIMIT :chunk_size OFFSET :offset
            """)

            attributes = self.db.execute(attributes_query, {
                "event_id": event_id,
                "chunk_size": chunk_size,
                "offset": offset
            }).fetchall()

            if not attributes:
                break

            yield {
                'attributes': [dict(attr._mapping) for attr in attributes],
                'chunk_type': 'attributes',
                'chunk_offset': offset,
                'chunk_size': len(attributes)
            }

            offset += chunk_size

        # Stream objects in chunks
        offset = 0
        while True:
            objects_query = text("""
                SELECT o.id, o.name, o.meta_category, o.template_uuid, 
                       o.template_version, o.comment,
                       json_agg(
                           jsonb_build_object(
                               'id', oa.id,
                               'type', oa.type,
                               'value', oa.value1,
                               'object_relation', oa.object_relation,
                               'comment', oa.comment
                           )
                       ) FILTER (WHERE oa.id IS NOT NULL) as object_attributes
                FROM objects o
                LEFT JOIN attributes oa ON o.id = oa.object_id AND oa.deleted = false
                WHERE o.event_id = :event_id AND o.deleted = false
                GROUP BY o.id, o.name, o.meta_category, o.template_uuid, 
                         o.template_version, o.comment
                ORDER BY o.id
                LIMIT :chunk_size OFFSET :offset
            """)

            objects = self.db.execute(objects_query, {
                "event_id": event_id,
                "chunk_size": chunk_size,
                "offset": offset
            }).fetchall()

            if not objects:
                break

            yield {
                'objects': [dict(obj._mapping) for obj in objects],
                'chunk_type': 'objects',
                'chunk_offset': offset,
                'chunk_size': len(objects)
            }

            offset += chunk_size

        # Yield completion marker
        yield {
            'chunk_type': 'complete',
            'total_attributes': event.attribute_count
        }

    def setup_background_correlation_sync(self):
        """
        Setup background correlation sync to handle cross-MISP queries
        Based on: app/Model/Server.php pullEvents() network dependent queries
        """
        logger.info("Setting up background correlation sync optimization")

        # Create sync queue table
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
            max_retries INTEGER DEFAULT 3
        );
        
        CREATE INDEX IF NOT EXISTS idx_sync_queue_status_priority
        ON correlation_sync_queue (status, priority, scheduled_at);
        
        CREATE INDEX IF NOT EXISTS idx_sync_queue_server_event
        ON correlation_sync_queue (source_server_id, event_uuid);
        """

        self.db.execute(text(sync_queue_sql))
        self.db.commit()
        logger.info("Created correlation sync queue table")

    def queue_correlation_sync(self, server_id: int, event_uuid: str, priority: int = 5):
        """Queue correlation sync for background processing"""
        queue_sql = text("""
            INSERT INTO correlation_sync_queue 
            (source_server_id, event_uuid, sync_type, priority, status)
            VALUES (:server_id, :event_uuid, 'correlation', :priority, 'pending')
            ON CONFLICT (source_server_id, event_uuid) 
            DO UPDATE SET 
                priority = GREATEST(correlation_sync_queue.priority, EXCLUDED.priority),
                scheduled_at = NOW(),
                status = 'pending'
            WHERE correlation_sync_queue.status IN ('failed', 'completed')
        """)

        self.db.execute(queue_sql, {
            "server_id": server_id,
            "event_uuid": event_uuid,
            "priority": priority
        })
        self.db.commit()

        logger.info(
            f"Queued correlation sync for event {event_uuid} from server {server_id}")

    def get_next_sync_job(self) -> Optional[Dict[str, Any]]:
        """Get next correlation sync job for background worker"""
        job_query = text("""
            UPDATE correlation_sync_queue 
            SET status = 'processing', started_at = NOW()
            WHERE id = (
                SELECT id FROM correlation_sync_queue
                WHERE status = 'pending' 
                AND scheduled_at <= NOW()
                AND retry_count < max_retries
                ORDER BY priority ASC, created_at ASC
                LIMIT 1
                FOR UPDATE SKIP LOCKED
            )
            RETURNING id, source_server_id, event_uuid, sync_type, priority
        """)

        result = self.db.execute(job_query).fetchone()
        self.db.commit()

        if result:
            return dict(result._mapping)
        return None

    def complete_sync_job(self, job_id: int, success: bool, error_message: str = None):
        """Mark sync job as completed or failed"""
        if success:
            update_sql = text("""
                UPDATE correlation_sync_queue 
                SET status = 'completed', completed_at = NOW()
                WHERE id = :job_id
            """)
            self.db.execute(update_sql, {"job_id": job_id})
        else:
            update_sql = text("""
                UPDATE correlation_sync_queue 
                SET status = CASE WHEN retry_count >= max_retries THEN 'failed' ELSE 'pending' END,
                    retry_count = retry_count + 1,
                    error_message = :error_message,
                    scheduled_at = NOW() + INTERVAL '5 minutes' * retry_count
                WHERE id = :job_id
            """)
            self.db.execute(update_sql, {
                "job_id": job_id,
                "error_message": error_message
            })

        self.db.commit()

    def refresh_export_cache(self, event_id: int = None):
        """Refresh materialized view for export optimization"""
        if event_id:
            # Partial refresh for specific event (PostgreSQL doesn't support this directly)
            # We'll need to implement a custom partial refresh
            logger.info(f"Refreshing export cache for event {event_id}")

            # Delete old cache entry
            self.db.execute(text("""
                DELETE FROM event_export_cache WHERE event_id = :event_id
            """), {"event_id": event_id})

            # Insert updated entry
            insert_sql = text("""
                INSERT INTO event_export_cache 
                SELECT * FROM (
                    SELECT 
                        e.id as event_id,
                        e.uuid, e.info, e.date, e.threat_level_id, e.analysis,
                        e.distribution, e.published, e.org_id, e.orgc_id,
                        json_agg(
                            DISTINCT jsonb_build_object(
                                'id', a.id, 'type', a.type, 'category', a.category, 
                                'value', CASE WHEN a.value2 IS NOT NULL 
                                       THEN a.value1 || '|' || a.value2 
                                       ELSE a.value1 END,
                                'comment', a.comment, 'to_ids', a.to_ids, 'timestamp', a.timestamp
                            )
                        ) FILTER (WHERE a.id IS NOT NULL) as attributes,
                        json_agg(
                            DISTINCT jsonb_build_object(
                                'id', o.id, 'name', o.name, 'meta_category', o.meta_category,
                                'template_uuid', o.template_uuid
                            )
                        ) FILTER (WHERE o.id IS NOT NULL) as objects
                    FROM events e
                    LEFT JOIN attributes a ON e.id = a.event_id AND a.deleted = false AND a.object_id IS NULL
                    LEFT JOIN objects o ON e.id = o.event_id AND o.deleted = false
                    WHERE e.id = :event_id AND e.deleted = false
                    GROUP BY e.id, e.uuid, e.info, e.date, e.threat_level_id, e.analysis,
                             e.distribution, e.published, e.org_id, e.orgc_id
                ) AS new_cache
            """)

            self.db.execute(insert_sql, {"event_id": event_id})
        else:
            # Full refresh
            logger.info("Refreshing complete export cache")
            self.db.execute(
                text("REFRESH MATERIALIZED VIEW event_export_cache"))

        self.db.commit()

    def _generate_search_cache_key(self, operation: str, *args, **kwargs) -> str:
        """Generate cache key for search operations"""
        key_parts = [f"misp:search:{operation}"]

        # Add positional arguments
        for arg in args:
            if arg is not None:
                key_parts.append(str(arg))

        # Add keyword arguments
        for k, v in sorted(kwargs.items()):
            if v is not None:
                if isinstance(v, list):
                    key_parts.append(f"{k}:{'|'.join(map(str, v))}")
                else:
                    key_parts.append(f"{k}:{v}")

        cache_key = ":".join(key_parts)

        # Hash if too long
        if len(cache_key) > 250:
            cache_key = f"misp:search:{operation}:" + \
                hashlib.sha256(cache_key.encode()).hexdigest()

        return cache_key

    def get_query_performance_stats(self) -> Dict[str, Any]:
        """Get query performance statistics"""
        stats_query = text("""
            SELECT 
                calls,
                total_time,
                mean_time,
                query
            FROM pg_stat_statements
            WHERE query LIKE '%attributes%' OR query LIKE '%events%'
            ORDER BY total_time DESC
            LIMIT 10
        """)

        try:
            results = self.db.execute(stats_query).fetchall()
            return {
                'top_queries': [dict(row._mapping) for row in results]
            }
        except Exception as e:
            logger.warning(f"Could not get query stats: {e}")
            return {'top_queries': []}
