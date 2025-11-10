"""MISP Database Performance Optimization Module

PostgreSQL-specific performance patterns migrated from MISP MySQL patterns.
Implements correlation caching, query optimization, and index strategies.
"""

import hashlib
import json
import logging
from contextlib import contextmanager
from datetime import datetime, timedelta
from functools import wraps
from typing import Any, Dict, List, Optional, Tuple

from redis import Redis
from sqlalchemy import (Boolean, Column, DateTime, Index, Integer, MetaData,
                        String, Table, Text, and_, asc, create_engine, delete,
                        desc, func, or_, select, text)
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import Session, sessionmaker

logger = logging.getLogger(__name__)


class MispPerformanceOptimizer:
    """
    MISP Performance Optimization Manager for PostgreSQL

    Implements performance patterns from original MISP:
    - Correlation caching (O(n²) → O(n) optimization)
    - Event pagination with covering indexes  
    - Redis caching for taxonomy/galaxy lookups
    - Denormalization patterns for statistics
    """

    def __init__(self, db_session: Session, redis_client: Redis):
        self.db = db_session
        self.redis = redis_client
        self.cache_ttl = {
            'correlation': 3600,      # 1 hour for correlation cache
            'taxonomy': 86400,        # 24 hours for taxonomy lookups
            'galaxy': 86400,          # 24 hours for galaxy data
            'event_stats': 1800,      # 30 minutes for event statistics
            'search_results': 300     # 5 minutes for search results
        }

    # Correlation Optimization Patterns

    def optimize_correlation_queries(self):
        """
        Implement O(n²) → O(n) correlation optimization
        Based on: app/Model/Correlation.php
        """
        logger.info("Setting up correlation optimization indexes")

        # Create correlation value indexes for fast matching
        correlation_indexes = [
            # Fast value lookups for correlation matching
            "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_correlation_values_fast "
            "ON correlation_values USING btree (value_hash)",

            # Attribute correlation compound index
            "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_attr_correlation_compound "
            "ON attributes USING btree (value1, type, category) WHERE deleted = false",

            # Event correlation tracking
            "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_event_correlation_stats "
            "ON events USING btree (correlation_count, published) WHERE deleted = false",

            # Temporal correlation patterns
            "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_attr_temporal_correlation "
            "ON attributes USING btree (timestamp, event_id) WHERE deleted = false",
        ]

        for index_sql in correlation_indexes:
            try:
                self.db.execute(text(index_sql))
                logger.info(f"Created index: {index_sql.split()[-3]}")
            except Exception as e:
                logger.warning(f"Index creation failed: {e}")

        self.db.commit()

    def create_correlation_cache_table(self):
        """Create pre-computed correlation cache table"""
        cache_table_sql = """
        CREATE TABLE IF NOT EXISTS correlation_cache (
            id SERIAL PRIMARY KEY,
            value_hash VARCHAR(64) NOT NULL,
            attribute_ids INTEGER[] NOT NULL,
            correlation_count INTEGER NOT NULL DEFAULT 0,
            last_updated TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
            expires_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() + INTERVAL '1 hour'
        );
        
        CREATE INDEX IF NOT EXISTS idx_correlation_cache_hash 
        ON correlation_cache USING btree (value_hash);
        
        CREATE INDEX IF NOT EXISTS idx_correlation_cache_expires 
        ON correlation_cache USING btree (expires_at);
        """

        self.db.execute(text(cache_table_sql))
        self.db.commit()
        logger.info("Created correlation cache table with indexes")

    def get_cached_correlations(self, value_hash: str) -> Optional[Dict[str, Any]]:
        """
        Get pre-computed correlations from cache
        Implements cache-aside pattern with TTL expiration
        """
        # Check Redis cache first (fastest)
        cache_key = f"misp:correlation:{value_hash}"
        cached_data = self.redis.get(cache_key)

        if cached_data:
            return json.loads(cached_data)

        # Check database correlation cache
        cache_result = self.db.execute(text("""
            SELECT attribute_ids, correlation_count, last_updated
            FROM correlation_cache 
            WHERE value_hash = :hash AND expires_at > NOW()
        """), {"hash": value_hash}).fetchone()

        if cache_result:
            correlation_data = {
                'attribute_ids': cache_result.attribute_ids,
                'count': cache_result.correlation_count,
                'cached_at': cache_result.last_updated.isoformat()
            }

            # Cache in Redis for faster access
            self.redis.setex(
                cache_key,
                self.cache_ttl['correlation'],
                json.dumps(correlation_data)
            )

            return correlation_data

        return None

    def cache_attribute_correlations(self, attribute_id: int, value: str):
        """
        Cache attribute correlations for O(n) lookup performance
        """
        value_hash = hashlib.sha256(value.encode()).hexdigest()

        # Find all correlating attributes
        correlation_query = text("""
            SELECT a.id, a.event_id, a.type, a.category
            FROM attributes a
            WHERE (a.value1 = :value OR CONCAT(a.value1, '|', a.value2) = :value)
            AND a.deleted = false
            AND a.id != :attr_id
            ORDER BY a.timestamp DESC
            LIMIT 1000
        """)

        correlations = self.db.execute(correlation_query, {
            "value": value,
            "attr_id": attribute_id
        }).fetchall()

        if correlations:
            attribute_ids = [c.id for c in correlations]

            # Update correlation cache table
            upsert_sql = """
            INSERT INTO correlation_cache (value_hash, attribute_ids, correlation_count, last_updated, expires_at)
            VALUES (:hash, :ids, :count, NOW(), NOW() + INTERVAL '1 hour')
            ON CONFLICT (value_hash) DO UPDATE SET
                attribute_ids = EXCLUDED.attribute_ids,
                correlation_count = EXCLUDED.correlation_count,
                last_updated = NOW(),
                expires_at = NOW() + INTERVAL '1 hour'
            """

            self.db.execute(text(upsert_sql), {
                "hash": value_hash,
                "ids": attribute_ids,
                "count": len(attribute_ids)
            })

            # Cache in Redis
            cache_data = {
                'attribute_ids': attribute_ids,
                'count': len(attribute_ids),
                'cached_at': datetime.utcnow().isoformat()
            }

            self.redis.setex(
                f"misp:correlation:{value_hash}",
                self.cache_ttl['correlation'],
                json.dumps(cache_data)
            )

            logger.debug(
                f"Cached {len(attribute_ids)} correlations for value hash {value_hash}")

    # Event Pagination Optimization

    def optimize_event_pagination(self):
        """
        Create covering indexes for efficient event pagination
        Based on: app/Model/Event.php fetchEvents()
        """
        logger.info("Setting up event pagination optimization indexes")

        pagination_indexes = [
            # Covering index for event list queries
            "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_events_list_covering "
            "ON events USING btree (published, distribution, date DESC) "
            "INCLUDE (id, uuid, info, threat_level_id, org_id, attribute_count)",

            # Organization-specific event queries
            "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_events_org_date "
            "ON events USING btree (org_id, date DESC, published) "
            "WHERE deleted = false",

            # Distribution-based queries with statistics
            "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_events_distribution_stats "
            "ON events USING btree (distribution, attribute_count DESC, date DESC) "
            "WHERE published = true AND deleted = false",

            # Search optimization index
            "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_events_search_gin "
            "ON events USING gin (to_tsvector('english', info))",
        ]

        for index_sql in pagination_indexes:
            try:
                self.db.execute(text(index_sql))
                logger.info(f"Created pagination index")
            except Exception as e:
                logger.warning(f"Pagination index creation failed: {e}")

        self.db.commit()

    def get_paginated_events(self,
                             page: int = 1,
                             per_page: int = 50,
                             org_id: Optional[int] = None,
                             published_only: bool = False,
                             distribution_levels: List[int] = None) -> Dict[str, Any]:
        """
        Optimized event pagination with strategic LIMIT/OFFSET
        """
        offset = (page - 1) * per_page

        # Build base query with covering index usage
        base_conditions = ["e.deleted = false"]
        params = {"limit": per_page, "offset": offset}

        if org_id:
            base_conditions.append("e.org_id = :org_id")
            params["org_id"] = org_id

        if published_only:
            base_conditions.append("e.published = true")

        if distribution_levels:
            base_conditions.append("e.distribution = ANY(:dist_levels)")
            params["dist_levels"] = distribution_levels

        where_clause = " AND ".join(base_conditions)

        # Use covering index for efficient pagination
        events_query = text(f"""
            SELECT e.id, e.uuid, e.info, e.date, e.threat_level_id, 
                   e.org_id, e.attribute_count, e.published, e.distribution,
                   o.name as org_name, tl.name as threat_level_name
            FROM events e
            JOIN organisations o ON e.org_id = o.id
            JOIN threat_levels tl ON e.threat_level_id = tl.id
            WHERE {where_clause}
            ORDER BY e.date DESC, e.id DESC
            LIMIT :limit OFFSET :offset
        """)

        events = self.db.execute(events_query, params).fetchall()

        # Get total count efficiently
        count_query = text(f"""
            SELECT COUNT(*) as total
            FROM events e 
            WHERE {where_clause}
        """)

        total = self.db.execute(count_query, params).scalar()

        return {
            'events': [dict(event._mapping) for event in events],
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': total,
                'pages': (total + per_page - 1) // per_page
            }
        }

    # Redis Caching Patterns

    def cache_taxonomy_lookups(self):
        """
        Implement 90% database load reduction for taxonomy/galaxy lookups
        Cache-aside pattern with TTL expiration
        """
        logger.info("Caching taxonomy and galaxy data")

        # Cache all taxonomies
        taxonomies_query = text("""
            SELECT t.id, t.namespace, t.description, t.version,
                   json_agg(json_build_object(
                       'id', tp.id, 
                       'value', tp.value, 
                       'description', tp.description
                   )) as predicates
            FROM taxonomies t
            LEFT JOIN taxonomy_predicates tp ON t.id = tp.taxonomy_id
            WHERE t.enabled = true
            GROUP BY t.id, t.namespace, t.description, t.version
        """)

        taxonomies = self.db.execute(taxonomies_query).fetchall()

        for taxonomy in taxonomies:
            cache_key = f"misp:taxonomy:{taxonomy.namespace}"
            taxonomy_data = {
                'id': taxonomy.id,
                'namespace': taxonomy.namespace,
                'description': taxonomy.description,
                'version': taxonomy.version,
                'predicates': taxonomy.predicates
            }

            self.redis.setex(
                cache_key,
                self.cache_ttl['taxonomy'],
                json.dumps(taxonomy_data)
            )

        logger.info(f"Cached {len(taxonomies)} taxonomies")

        # Cache all galaxies
        galaxies_query = text("""
            SELECT g.id, g.name, g.type, g.description, g.version,
                   json_agg(json_build_object(
                       'id', gc.id,
                       'value', gc.value,
                       'description', gc.description,
                       'tag_name', gc.tag_name
                   )) as clusters
            FROM galaxies g
            LEFT JOIN galaxy_clusters gc ON g.id = gc.galaxy_id
            WHERE g.enabled = true AND (gc.deleted = false OR gc.id IS NULL)
            GROUP BY g.id, g.name, g.type, g.description, g.version
        """)

        galaxies = self.db.execute(galaxies_query).fetchall()

        for galaxy in galaxies:
            cache_key = f"misp:galaxy:{galaxy.type}"
            galaxy_data = {
                'id': galaxy.id,
                'name': galaxy.name,
                'type': galaxy.type,
                'description': galaxy.description,
                'version': galaxy.version,
                'clusters': galaxy.clusters
            }

            self.redis.setex(
                cache_key,
                self.cache_ttl['galaxy'],
                json.dumps(galaxy_data)
            )

        logger.info(f"Cached {len(galaxies)} galaxies")

    def get_cached_taxonomy(self, namespace: str) -> Optional[Dict[str, Any]]:
        """Get taxonomy from cache with fallback to database"""
        cache_key = f"misp:taxonomy:{namespace}"
        cached_data = self.redis.get(cache_key)

        if cached_data:
            return json.loads(cached_data)

        # Fallback to database
        taxonomy_query = text("""
            SELECT t.id, t.namespace, t.description, t.version,
                   json_agg(json_build_object(
                       'id', tp.id, 
                       'value', tp.value, 
                       'description', tp.description
                   )) as predicates
            FROM taxonomies t
            LEFT JOIN taxonomy_predicates tp ON t.id = tp.taxonomy_id
            WHERE t.namespace = :namespace AND t.enabled = true
            GROUP BY t.id, t.namespace, t.description, t.version
        """)

        result = self.db.execute(
            taxonomy_query, {"namespace": namespace}).fetchone()

        if result:
            taxonomy_data = {
                'id': result.id,
                'namespace': result.namespace,
                'description': result.description,
                'version': result.version,
                'predicates': result.predicates
            }

            # Cache for future use
            self.redis.setex(
                cache_key,
                self.cache_ttl['taxonomy'],
                json.dumps(taxonomy_data)
            )

            return taxonomy_data

        return None

    # Denormalization Patterns

    def setup_event_statistics_denormalization(self):
        """
        Setup denormalized event statistics to avoid expensive aggregate queries
        Based on: Events table computed columns pattern
        """
        logger.info("Setting up event statistics denormalization")

        # Create event statistics update function
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

        self.db.execute(text(stats_function_sql))
        self.db.commit()
        logger.info("Created event statistics triggers")

    def refresh_all_event_statistics(self):
        """Bulk refresh all event statistics"""
        logger.info("Refreshing all event statistics")

        refresh_sql = """
        UPDATE events SET 
            attribute_count = (
                SELECT COUNT(*) 
                FROM attributes 
                WHERE event_id = events.id AND deleted = false
            ),
            correlation_count = (
                SELECT COUNT(DISTINCT c.attribute_id) 
                FROM correlations c
                JOIN attributes a ON c.attribute_id = a.id
                WHERE a.event_id = events.id AND a.deleted = false
            )
        WHERE deleted = false;
        """

        result = self.db.execute(text(refresh_sql))
        self.db.commit()

        logger.info(f"Updated statistics for {result.rowcount} events")

    # Cache Management

    def invalidate_correlation_cache(self, value: str):
        """Invalidate correlation cache for a specific value"""
        value_hash = hashlib.sha256(value.encode()).hexdigest()

        # Remove from Redis
        self.redis.delete(f"misp:correlation:{value_hash}")

        # Remove from database cache
        self.db.execute(text("""
            DELETE FROM correlation_cache WHERE value_hash = :hash
        """), {"hash": value_hash})

        self.db.commit()

    def cleanup_expired_cache(self):
        """Clean up expired cache entries"""
        # Clean database cache
        self.db.execute(text("""
            DELETE FROM correlation_cache WHERE expires_at < NOW()
        """))

        self.db.commit()
        logger.info("Cleaned up expired correlation cache entries")

    # Performance Monitoring

    def get_performance_metrics(self) -> Dict[str, Any]:
        """Get current performance metrics"""
        metrics = {}

        # Cache hit rates
        cache_stats = self.redis.info('stats')
        if 'keyspace_hits' in cache_stats and 'keyspace_misses' in cache_stats:
            hits = cache_stats['keyspace_hits']
            misses = cache_stats['keyspace_misses']
            hit_rate = hits / (hits + misses) if (hits + misses) > 0 else 0
            metrics['cache_hit_rate'] = hit_rate

        # Database performance
        db_stats = self.db.execute(text("""
            SELECT 
                COUNT(*) as total_events,
                AVG(attribute_count) as avg_attributes_per_event,
                MAX(attribute_count) as max_attributes_per_event
            FROM events WHERE deleted = false
        """)).fetchone()

        metrics.update({
            'total_events': db_stats.total_events,
            'avg_attributes_per_event': float(db_stats.avg_attributes_per_event or 0),
            'max_attributes_per_event': db_stats.max_attributes_per_event
        })

        # Correlation cache performance
        cache_stats = self.db.execute(text("""
            SELECT 
                COUNT(*) as cached_correlations,
                AVG(correlation_count) as avg_correlations_per_value
            FROM correlation_cache WHERE expires_at > NOW()
        """)).fetchone()

        metrics.update({
            'cached_correlations': cache_stats.cached_correlations,
            'avg_correlations_per_value': float(cache_stats.avg_correlations_per_value or 0)
        })

        return metrics


# Decorator for caching expensive operations
def misp_cache(ttl: int = 300, key_prefix: str = "misp"):
    """Decorator for caching MISP operations in Redis"""
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            if not hasattr(self, 'redis'):
                return func(self, *args, **kwargs)

            # Generate cache key from function name and arguments
            key_parts = [key_prefix, func.__name__]
            key_parts.extend(str(arg) for arg in args)
            key_parts.extend(f"{k}:{v}" for k, v in sorted(kwargs.items()))
            cache_key = ":".join(key_parts)

            # Try to get from cache
            cached_result = self.redis.get(cache_key)
            if cached_result:
                return json.loads(cached_result)

            # Execute function and cache result
            result = func(self, *args, **kwargs)
            self.redis.setex(cache_key, ttl, json.dumps(result))

            return result
        return wrapper
    return decorator
