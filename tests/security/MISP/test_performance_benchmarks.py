#!/usr/bin/env python3
"""
MISP Performance Benchmark Tests

Purpose: Validate MISP performance meets security domain requirements
Requirements: Section 8.1 (Performance) from misp-analysis.md
Coverage: Response times, throughput, resource usage validation

Performance targets: <1s security domain response time
"""

from services.security_service import SecurityToolsService
from libs.service_adapters.security.misp_adapter import MISPAdapter
import asyncio
import concurrent.futures
import statistics
# Import MISP components for performance testing
import sys
import time
from typing import Dict, List

import psutil
import pytest

sys.path.append('/workspaces/modular-monolith-2/apps/jane-orchestrator/src')


class TestMISPPerformance:
    """Performance benchmark tests for MISP integration"""

    @pytest.fixture
    async def misp_adapter(self):
        """Initialize MISP adapter for performance testing"""
        adapter = MISPAdapter()
        await adapter.initialize()
        return adapter

    @pytest.fixture
    def performance_data(self):
        """Sample data for performance testing"""
        return {
            'events': [
                {
                    'info': f'Performance Test Event {i}',
                    'distribution': 0,
                    'threat_level_id': 2,
                    'analysis': 2,
                    'attributes': [
                        {
                            'category': 'Network activity',
                            'type': 'domain',
                            'value': f'test{i}.malicious.com',
                            'to_ids': True
                        }
                    ]
                }
                for i in range(100)
            ]
        }

    @pytest.mark.asyncio
    async def test_event_creation_performance(self, misp_adapter, performance_data):
        """
        Test: Event creation meets <1s performance requirement
        Coverage: Event creation workflow performance
        Requirement: Security domain <1s response time
        """
        creation_times = []

        for event_data in performance_data['events'][:10]:  # Test 10 events
            start_time = time.time()
            await misp_adapter.create_event(event_data)
            creation_time = time.time() - start_time
            creation_times.append(creation_time)

        # Performance validation
        avg_time = statistics.mean(creation_times)
        p95_time = statistics.quantiles(creation_times, n=20)[
            18]  # 95th percentile
        max_time = max(creation_times)

        assert avg_time < 0.5, f"Average creation time {avg_time:.3f}s exceeds 0.5s"
        assert p95_time < 1.0, f"95th percentile time {p95_time:.3f}s exceeds 1s"
        assert max_time < 1.0, f"Maximum creation time {max_time:.3f}s exceeds 1s"

    @pytest.mark.asyncio
    async def test_search_performance(self, misp_adapter):
        """
        Test: Event search meets performance requirements
        Coverage: Search algorithm performance validation
        Requirement: <1s search response time
        """
        search_queries = [
            {'value': 'malicious.com', 'type': 'domain'},
            {'category': 'Network activity', 'type': 'ip-src'},
            {'tags': ['tlp:white'], 'eventinfo': 'APT'},
            {'from': '2024-01-01', 'to': '2024-12-31'},
            {'value': '192.168.1.1', 'type': 'ip-src'}
        ]

        search_times = []

        for query in search_queries:
            start_time = time.time()
            await misp_adapter.search_events(**query)
            search_time = time.time() - start_time
            search_times.append(search_time)

        # Performance validation
        avg_time = statistics.mean(search_times)
        max_time = max(search_times)

        assert avg_time < 0.5, f"Average search time {avg_time:.3f}s exceeds 0.5s"
        assert max_time < 1.0, f"Maximum search time {max_time:.3f}s exceeds 1s"

    @pytest.mark.asyncio
    async def test_correlation_performance(self, misp_adapter, performance_data):
        """
        Test: Correlation finding meets performance requirements
        Coverage: Correlation algorithm performance (critical 8,733 lines)
        Requirement: <1s correlation response time
        """
        # Create some test events first
        event_uuids = []
        for event_data in performance_data['events'][:5]:
            event = await misp_adapter.create_event(event_data)
            event_uuids.append(event['uuid'])

        correlation_times = []

        for event_uuid in event_uuids:
            start_time = time.time()
            await misp_adapter.find_correlations(event_uuid)
            correlation_time = time.time() - start_time
            correlation_times.append(correlation_time)

        # Performance validation
        avg_time = statistics.mean(correlation_times)
        max_time = max(correlation_times)

        assert avg_time < 0.5, f"Average correlation time {avg_time:.3f}s exceeds 0.5s"
        assert max_time < 1.0, f"Maximum correlation time {max_time:.3f}s exceeds 1s"

    @pytest.mark.asyncio
    async def test_concurrent_operations_performance(self, misp_adapter):
        """
        Test: Concurrent operations maintain performance
        Coverage: Multi-user concurrent access performance
        Requirement: Performance under load
        """
        async def create_event_task(event_id: int):
            event_data = {
                'info': f'Concurrent Test Event {event_id}',
                'distribution': 0,
                'threat_level_id': 2,
                'analysis': 2,
                'attributes': [
                    {
                        'category': 'Network activity',
                        'type': 'domain',
                        'value': f'concurrent{event_id}.test.com',
                        'to_ids': True
                    }
                ]
            }
            start_time = time.time()
            await misp_adapter.create_event(event_data)
            return time.time() - start_time

        # Run 10 concurrent event creations
        tasks = [create_event_task(i) for i in range(10)]

        start_total = time.time()
        execution_times = await asyncio.gather(*tasks)
        total_time = time.time() - start_total

        # Performance validation
        avg_time = statistics.mean(execution_times)
        max_time = max(execution_times)

        assert total_time < 5.0, f"Total concurrent time {total_time:.3f}s exceeds 5s"
        assert avg_time < 1.0, f"Average concurrent time {avg_time:.3f}s exceeds 1s"
        assert max_time < 2.0, f"Maximum concurrent time {max_time:.3f}s exceeds 2s"

    @pytest.mark.asyncio
    async def test_memory_usage_performance(self, misp_adapter, performance_data):
        """
        Test: Memory usage remains within acceptable limits
        Coverage: Memory efficiency during bulk operations
        Requirement: Resource utilization constraints
        """
        process = psutil.Process()
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB

        # Perform memory-intensive operations
        for event_data in performance_data['events'][:20]:
            await misp_adapter.create_event(event_data)

        # Search operations
        for i in range(10):
            await misp_adapter.search_events(value=f'test{i}.malicious.com')

        final_memory = process.memory_info().rss / 1024 / 1024  # MB
        memory_increase = final_memory - initial_memory

        # Memory validation (allow up to 100MB increase)
        assert memory_increase < 100, (
            f"Memory increase {memory_increase:.1f}MB exceeds 100MB limit"
        )

    @pytest.mark.asyncio
    async def test_bulk_operations_performance(self, misp_adapter, performance_data):
        """
        Test: Bulk operations performance optimization
        Coverage: Batch processing performance
        Requirement: Efficient bulk data handling
        """
        # Test bulk event creation
        start_time = time.time()
        await misp_adapter.bulk_create_events(performance_data['events'][:50])
        bulk_time = time.time() - start_time

        # Calculate per-event time for bulk operation
        per_event_time = bulk_time / 50

        assert bulk_time < 30.0, f"Bulk creation {bulk_time:.3f}s exceeds 30s limit"
        assert per_event_time < 0.6, (
            f"Per-event bulk time {per_event_time:.3f}s exceeds 0.6s"
        )

    @pytest.mark.asyncio
    async def test_database_query_performance(self, misp_adapter):
        """
        Test: Database query optimization performance
        Coverage: Database interaction efficiency
        Requirement: Optimized database access patterns
        """
        query_performance_tests = [
            {
                'name': 'event_list',
                'operation': lambda: misp_adapter.get_events(limit=100),
                'max_time': 0.5
            },
            {
                'name': 'attribute_search',
                'operation': lambda: misp_adapter.search_attributes(
                    category='Network activity'
                ),
                'max_time': 0.5
            },
            {
                'name': 'organization_list',
                'operation': lambda: misp_adapter.get_organisations(),
                'max_time': 0.3
            },
            {
                'name': 'user_list',
                'operation': lambda: misp_adapter.get_users(),
                'max_time': 0.3
            }
        ]

        for test in query_performance_tests:
            start_time = time.time()
            await test['operation']()
            query_time = time.time() - start_time

            assert query_time < test['max_time'], (
                f"Query {test['name']} took {query_time:.3f}s, "
                f"exceeds {test['max_time']}s limit"
            )

    @pytest.mark.asyncio
    async def test_api_response_time_distribution(self, misp_adapter):
        """
        Test: API response time distribution analysis
        Coverage: Response time consistency validation
        Requirement: Consistent performance characteristics
        """
        operations = [
            ('create_event', lambda: misp_adapter.create_event({
                'info': 'API Performance Test',
                'distribution': 0,
                'threat_level_id': 2,
                'analysis': 2
            })),
            ('search_events', lambda: misp_adapter.search_events(
                value='test.com', type='domain'
            )),
            ('get_organisations', lambda: misp_adapter.get_organisations()),
            ('get_taxonomies', lambda: misp_adapter.get_taxonomies())
        ]

        performance_results = {}

        for op_name, operation in operations:
            times = []
            for _ in range(10):  # 10 samples per operation
                start_time = time.time()
                await operation()
                execution_time = time.time() - start_time
                times.append(execution_time)

            performance_results[op_name] = {
                'mean': statistics.mean(times),
                'median': statistics.median(times),
                'stdev': statistics.stdev(times) if len(times) > 1 else 0,
                'min': min(times),
                'max': max(times),
                'p95': statistics.quantiles(times, n=20)[18] if len(times) >= 20 else max(times)
            }

        # Validate performance consistency
        for op_name, stats in performance_results.items():
            assert stats['mean'] < 1.0, (
                f"{op_name} mean time {stats['mean']:.3f}s exceeds 1s"
            )
            assert stats['p95'] < 1.5, (
                f"{op_name} 95th percentile {stats['p95']:.3f}s exceeds 1.5s"
            )
            assert stats['stdev'] < 0.5, (
                f"{op_name} standard deviation {stats['stdev']:.3f}s too high"
            )

    def test_cpu_usage_monitoring(self, misp_adapter):
        """
        Test: CPU usage during intensive operations
        Coverage: CPU efficiency validation
        Requirement: Resource utilization monitoring
        """
        import queue
        import threading

        cpu_usage_queue = queue.Queue()

        def monitor_cpu():
            for _ in range(20):  # Monitor for ~2 seconds
                cpu_usage_queue.put(psutil.cpu_percent(interval=0.1))

        # Start CPU monitoring
        monitor_thread = threading.Thread(target=monitor_cpu)
        monitor_thread.start()

        # Perform CPU-intensive operations
        asyncio.run(self._cpu_intensive_operations(misp_adapter))

        monitor_thread.join()

        # Collect CPU usage data
        cpu_readings = []
        while not cpu_usage_queue.empty():
            cpu_readings.append(cpu_usage_queue.get())

        if cpu_readings:
            avg_cpu = statistics.mean(cpu_readings)
            max_cpu = max(cpu_readings)

            # CPU usage validation (allow up to 80% average, 95% peak)
            assert avg_cpu < 80.0, f"Average CPU {avg_cpu:.1f}% exceeds 80%"
            assert max_cpu < 95.0, f"Peak CPU {max_cpu:.1f}% exceeds 95%"

    async def _cpu_intensive_operations(self, misp_adapter):
        """Helper method for CPU-intensive test operations"""
        # Create multiple events concurrently
        tasks = []
        for i in range(5):
            event_data = {
                'info': f'CPU Test Event {i}',
                'distribution': 0,
                'threat_level_id': 2,
                'analysis': 2,
                'attributes': [
                    {
                        'category': 'Network activity',
                        'type': 'domain',
                        'value': f'cpu_test_{i}.com',
                        'to_ids': True
                    }
                ]
            }
            tasks.append(misp_adapter.create_event(event_data))

        await asyncio.gather(*tasks)

        # Perform correlation operations
        for i in range(5):
            await misp_adapter.search_events(value=f'cpu_test_{i}.com')


if __name__ == '__main__':
    # Run performance benchmark tests
    pytest.main([
        __file__,
        '-v',
        '--tb=short',
        '--benchmark-only'
    ])
