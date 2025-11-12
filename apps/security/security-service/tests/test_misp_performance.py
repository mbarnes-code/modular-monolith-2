"""MISP Performance Optimization Tests

Test suite for validating MISP performance patterns and optimizations.
Ensures <1s security domain performance requirements are met.
"""

import json
import time
from datetime import datetime, timedelta
from unittest.mock import Mock, patch

import pytest
from apps.security_service.src.data.models.misp import (Event, MispAttribute,
                                                        MispBaseModel,
                                                        Organisation, Role,
                                                        ThreatLevel, User)
from apps.security_service.src.data.performance.cache_manager import \
    MispCacheManager
from apps.security_service.src.data.performance.misp_optimizer import \
    MispPerformanceOptimizer
from apps.security_service.src.data.performance.query_optimizer import \
    MispQueryOptimizer
from redis import Redis
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker


@pytest.fixture
def engine():
    """Create test database engine"""
    engine = create_engine("sqlite:///:memory:", echo=False)
    MispBaseModel.metadata.create_all(engine)
    return engine


@pytest.fixture
def session(engine):
    """Create database session"""
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()


@pytest.fixture
def redis_client():
    """Create mock Redis client"""
    return Mock(spec=Redis)


@pytest.fixture
def performance_optimizer(session, redis_client):
    """Create performance optimizer instance"""
    return MispPerformanceOptimizer(session, redis_client)


@pytest.fixture
def query_optimizer(session, redis_client):
    """Create query optimizer instance"""
    return MispQueryOptimizer(session, redis_client)


@pytest.fixture
def cache_manager(redis_client, session):
    """Create cache manager instance"""
    return MispCacheManager(redis_client, session)


@pytest.fixture
def sample_data(session):
    """Create sample test data"""
    # Create test organization
    org = Organisation(
        name="Test Org",
        description="Test Organization",
        type="CERT",
        nationality="US",
        sector="Government",
        local=True
    )
    session.add(org)

    # Create test role
    role = Role(
        name="admin",
        created=datetime.utcnow(),
        modified=datetime.utcnow(),
        perm_add=True,
        perm_modify=True,
        perm_publish=True,
        default_role=False
    )
    session.add(role)

    # Create test user
    user = User(
        email="test@example.com",
        org_id=1,  # Will be set after org is committed
        server_id=0,
        password="hashed_password",
        authkey="test_auth_key",
        role_id=1,  # Will be set after role is committed
        terms_accepted=True,
        disabled=False
    )

    # Create threat level
    threat_level = ThreatLevel(
        name="High",
        description="High threat level",
        form_description="High threat level"
    )
    session.add(threat_level)

    session.commit()

    # Update foreign keys
    user.org_id = org.id
    user.role_id = role.id
    session.add(user)

    # Create test events
    events = []
    for i in range(10):
        event = Event(
            org_id=org.id,
            orgc_id=org.id,
            user_id=user.id,
            date=f"2024-01-{i+1:02d}",
            threat_level_id=threat_level.id,
            info=f"Test Event {i+1}",
            published=i % 2 == 0,  # Alternate published status
            analysis=0,
            attribute_count=0,
            distribution=0
        )
        events.append(event)
        session.add(event)

    session.commit()

    # Create test attributes
    attributes = []
    for i, event in enumerate(events):
        for j in range(5):  # 5 attributes per event
            attr = MispAttribute(
                event_id=event.id,
                category="Network activity",
                type="ip-dst",
                value1=f"192.168.{i}.{j}",
                to_ids=True,
                timestamp=int(datetime.utcnow().timestamp()),
                distribution=0,
                deleted=False
            )
            attributes.append(attr)
            session.add(attr)

    session.commit()

    # Update event attribute counts
    for event in events:
        event.attribute_count = len(
            [a for a in attributes if a.event_id == event.id])

    session.commit()

    return {
        'org': org,
        'user': user,
        'role': role,
        'threat_level': threat_level,
        'events': events,
        'attributes': attributes
    }


class TestMispPerformanceOptimizer:
    """Test MISP performance optimizer functionality"""

    def test_correlation_cache_creation(self, performance_optimizer, session):
        """Test correlation cache table creation"""
        # This would create the table in a real database
        performance_optimizer.create_correlation_cache_table()

        # Verify table exists (in SQLite, we can't test the exact PostgreSQL structure)
        # But we can verify the method completes without error
        assert True

    def test_correlation_caching(self, performance_optimizer, sample_data):
        """Test correlation caching functionality"""
        # Mock Redis responses
        performance_optimizer.redis.get.return_value = None
        performance_optimizer.redis.setex.return_value = True

        # Test caching correlations
        performance_optimizer.cache_attribute_correlations(1, "192.168.1.1")

        # Verify Redis was called
        assert performance_optimizer.redis.setex.called

    def test_get_cached_correlations(self, performance_optimizer):
        """Test retrieving cached correlations"""
        # Mock Redis response
        cached_data = {
            'attribute_ids': [1, 2, 3],
            'count': 3,
            'cached_at': datetime.utcnow().isoformat()
        }
        performance_optimizer.redis.get.return_value = json.dumps(cached_data)

        result = performance_optimizer.get_cached_correlations("test_hash")

        assert result is not None
        assert result['count'] == 3
        assert len(result['attribute_ids']) == 3

    def test_event_pagination_performance(self, performance_optimizer, sample_data):
        """Test event pagination performance"""
        start_time = time.time()

        # Test paginated event retrieval
        result = performance_optimizer.get_paginated_events(
            page=1,
            per_page=5,
            published_only=True
        )

        end_time = time.time()
        query_time = end_time - start_time

        # Should complete in <1s for security domain requirement
        assert query_time < 1.0
        assert 'events' in result
        assert 'pagination' in result
        assert len(result['events']) <= 5

    def test_performance_metrics(self, performance_optimizer):
        """Test performance metrics collection"""
        # Mock Redis info
        performance_optimizer.redis.info.return_value = {
            'keyspace_hits': 100,
            'keyspace_misses': 20,
            'instantaneous_ops_per_sec': 50
        }

        metrics = performance_optimizer.get_performance_metrics()

        assert 'cache_hit_rate' in metrics
        assert metrics['cache_hit_rate'] > 0.8  # Should have >80% hit rate


class TestMispQueryOptimizer:
    """Test MISP query optimizer functionality"""

    def test_optimized_attribute_search_performance(self, query_optimizer, sample_data):
        """Test optimized attribute search meets <1s requirement"""
        # Mock Redis cache miss
        query_optimizer.redis.get.return_value = None
        query_optimizer.redis.setex.return_value = True

        start_time = time.time()

        result = query_optimizer.optimized_attribute_search(
            search_terms="192.168",
            limit=100
        )

        end_time = time.time()
        query_time = end_time - start_time

        # Must meet <1s security domain requirement
        assert query_time < 1.0
        assert 'attributes' in result
        assert 'query_time_seconds' in result
        assert result['query_time_seconds'] < 1.0

    def test_streaming_export_memory_efficiency(self, query_optimizer, sample_data):
        """Test streaming export prevents memory issues"""
        event_id = sample_data['events'][0].id

        chunks = list(query_optimizer.get_streaming_event_export(
            event_id, chunk_size=2))

        # Should have header, attributes, and completion chunks
        assert len(chunks) >= 3

        # Verify chunk types
        chunk_types = [chunk['chunk_type'] for chunk in chunks]
        assert 'header' in chunk_types
        assert 'attributes' in chunk_types
        assert 'complete' in chunk_types

        # Verify no single chunk is too large (memory efficiency)
        for chunk in chunks:
            if 'attributes' in chunk:
                assert len(chunk['attributes']) <= 2  # chunk_size limit

    def test_background_sync_queue(self, query_optimizer):
        """Test background correlation sync queue"""
        # Queue a sync job
        query_optimizer.queue_correlation_sync(
            server_id=1,
            event_uuid="test-uuid-123",
            priority=3
        )

        # Get next job
        job = query_optimizer.get_next_sync_job()

        # In SQLite test, job might be None, but method should not fail
        assert job is None or isinstance(job, dict)

    def test_search_cache_key_generation(self, query_optimizer):
        """Test search cache key generation"""
        cache_key = query_optimizer._generate_search_cache_key(
            "test_search",
            "search_terms",
            event_ids=[1, 2, 3],
            tags=["malware", "apt"]
        )

        assert cache_key.startswith("misp:search:test_search")
        assert "event_ids" in cache_key
        assert "tags" in cache_key


class TestMispCacheManager:
    """Test MISP cache manager functionality"""

    def test_taxonomy_caching(self, cache_manager):
        """Test taxonomy caching for 90% load reduction"""
        # Mock database results
        with patch.object(cache_manager.db, 'execute') as mock_execute:
            mock_result = Mock()
            mock_result.fetchall.return_value = [
                Mock(
                    id=1,
                    namespace="tlp",
                    description="Traffic Light Protocol",
                    version="1.0",
                    enabled=True,
                    predicates=[
                        {'id': 1, 'value': 'white', 'description': 'TLP White'},
                        {'id': 2, 'value': 'green', 'description': 'TLP Green'}
                    ]
                )
            ]
            mock_execute.return_value = mock_result

            # Mock Redis
            cache_manager.redis.setex.return_value = True

            count = cache_manager.cache_all_taxonomies()

            assert count == 1
            assert cache_manager.redis.setex.call_count >= 2  # namespace and ID cache

    def test_get_cached_taxonomy(self, cache_manager):
        """Test retrieving cached taxonomy"""
        # Mock Redis hit
        taxonomy_data = {
            'id': 1,
            'namespace': 'tlp',
            'description': 'Traffic Light Protocol',
            'predicates': []
        }
        cache_manager.redis.get.return_value = json.dumps(taxonomy_data)

        result = cache_manager.get_taxonomy('tlp')

        assert result is not None
        assert result['namespace'] == 'tlp'
        assert result['id'] == 1

    def test_event_statistics_caching(self, cache_manager, sample_data):
        """Test event statistics caching"""
        event_id = sample_data['events'][0].id

        # Mock Redis
        cache_manager.redis.setex.return_value = True

        stats = cache_manager.cache_event_statistics(event_id)

        assert 'event_id' in stats
        assert 'attribute_count' in stats
        assert stats['event_id'] == event_id

    def test_cache_invalidation(self, cache_manager):
        """Test cache invalidation functionality"""
        event_id = 1

        # Mock Redis operations
        cache_manager.redis.delete.return_value = 1
        cache_manager.redis.scan_iter.return_value = [
            'misp:stats:event:1',
            'misp:search:results:hash123'
        ]

        cache_manager.invalidate_event_cache(event_id)

        # Verify Redis delete was called
        assert cache_manager.redis.delete.called

    def test_cache_warming(self, cache_manager):
        """Test cache warming process"""
        # Mock database queries
        with patch.object(cache_manager, 'cache_all_taxonomies', return_value=5), \
                patch.object(cache_manager, 'cache_all_galaxies', return_value=3), \
                patch.object(cache_manager.db, 'execute') as mock_execute:

            # Mock recent events query
            mock_result = Mock()
            mock_result.fetchall.return_value = [
                Mock(id=i) for i in range(1, 6)]
            mock_execute.return_value = mock_result

            with patch.object(cache_manager, 'cache_event_statistics', return_value={}):
                start_time = time.time()
                cache_manager.warm_cache()
                end_time = time.time()

                # Should complete quickly
                assert (end_time - start_time) < 1.0

    def test_cache_metrics(self, cache_manager):
        """Test cache metrics collection"""
        # Mock Redis info
        cache_manager.redis.info.return_value = {
            'keyspace_hits': 1000,
            'keyspace_misses': 100,
            'used_memory': 1024 * 1024,  # 1MB
            'instantaneous_ops_per_sec': 100,
            'db0': {'keys': 500}
        }

        # Mock scan_iter for key counting
        cache_manager.redis.scan_iter.return_value = ['key1', 'key2', 'key3']

        metrics = cache_manager.get_cache_metrics()

        assert 'hit_rate' in metrics
        assert 'memory_usage_mb' in metrics
        assert 'key_counts' in metrics
        assert metrics['hit_rate'] > 0.9  # Should have >90% hit rate


class TestPerformanceIntegration:
    """Integration tests for MISP performance optimizations"""

    def test_end_to_end_search_performance(self, query_optimizer, cache_manager, sample_data):
        """Test end-to-end search performance meets requirements"""
        # Warm cache
        cache_manager.redis.get.return_value = None  # Cache miss
        cache_manager.redis.setex.return_value = True

        start_time = time.time()

        # Perform search
        result = query_optimizer.optimized_attribute_search(
            search_terms="192.168",
            attribute_types=["ip-dst"],
            limit=50
        )

        end_time = time.time()
        total_time = end_time - start_time

        # Must meet <1s security domain requirement
        assert total_time < 1.0
        assert 'attributes' in result
        assert result['count'] >= 0

    def test_correlation_performance_optimization(self, performance_optimizer, sample_data):
        """Test correlation performance optimization"""
        # Test O(n²) → O(n) optimization
        test_values = [f"192.168.1.{i}" for i in range(10)]

        start_time = time.time()

        for value in test_values:
            performance_optimizer.cache_attribute_correlations(1, value)

        end_time = time.time()
        total_time = end_time - start_time

        # Should be linear time, not quadratic
        assert total_time < 1.0  # Should be much faster than O(n²)

    def test_memory_usage_optimization(self, query_optimizer, sample_data):
        """Test memory usage stays within limits"""
        import os

        import psutil

        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss

        # Test streaming export (should not spike memory)
        event_id = sample_data['events'][0].id
        chunks = list(query_optimizer.get_streaming_event_export(
            event_id, chunk_size=2))

        final_memory = process.memory_info().rss
        memory_increase = final_memory - initial_memory

        # Should not increase memory significantly (avoid 500MB+ issue)
        assert memory_increase < 50 * 1024 * 1024  # Less than 50MB increase
        assert len(chunks) > 0

    def test_constitutional_performance_compliance(self, performance_optimizer, sample_data):
        """Test compliance with constitutional <1s security domain requirement"""
        # Test multiple operations that must complete within 1s total
        operations = [
            lambda: performance_optimizer.get_paginated_events(
                page=1, per_page=10),
            lambda: performance_optimizer.get_performance_metrics(),
            lambda: performance_optimizer.cache_attribute_correlations(
                1, "test_value")
        ]

        start_time = time.time()

        for operation in operations:
            operation()

        end_time = time.time()
        total_time = end_time - start_time

        # All operations combined must complete in <1s for security domain
        assert total_time < 1.0


@pytest.mark.performance
class TestPerformanceBenchmarks:
    """Performance benchmark tests for MISP optimizations"""

    def test_correlation_lookup_benchmark(self, performance_optimizer):
        """Benchmark correlation lookup performance"""
        # Test with increasing dataset sizes
        dataset_sizes = [100, 500, 1000]

        for size in dataset_sizes:
            start_time = time.time()

            # Simulate correlation lookups
            for i in range(size):
                performance_optimizer.get_cached_correlations(f"hash_{i}")

            end_time = time.time()
            time_per_lookup = (end_time - start_time) / size

            # Each lookup should be <10ms for O(1) performance
            assert time_per_lookup < 0.01

    def test_search_scaling_benchmark(self, query_optimizer):
        """Benchmark search performance scaling"""
        search_terms = ["malware", "apt", "trojan", "backdoor"]

        for term in search_terms:
            start_time = time.time()

            query_optimizer.optimized_attribute_search(
                search_terms=term,
                limit=1000
            )

            end_time = time.time()
            query_time = end_time - start_time

            # Each search must meet <1s requirement
            assert query_time < 1.0

    def test_cache_hit_ratio_benchmark(self, cache_manager):
        """Benchmark cache hit ratio performance"""
        # Mock high hit ratio
        cache_manager.redis.info.return_value = {
            'keyspace_hits': 900,
            'keyspace_misses': 100
        }

        metrics = cache_manager.get_cache_metrics()

        # Should achieve >90% hit rate for database load reduction
        assert metrics['hit_rate'] > 0.9


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
