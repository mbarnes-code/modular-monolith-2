"""
Intelligence Service Utilities

Common utilities and helper functions used across all intelligence services.
Provides caching, metrics, error handling, and other shared functionality.
"""

import asyncio
import functools
import hashlib
import json
import time
from datetime import datetime, timedelta
from typing import Any, Callable, Dict, List, Optional, TypeVar

from .interfaces import (ConfidenceLevel, IntelligenceContext,
                         IntelligenceInsight)

T = TypeVar('T')


class IntelligenceCache:
    """Simple in-memory cache for intelligence insights"""

    def __init__(self, max_size: int = 1000, ttl_seconds: int = 3600):
        self.max_size = max_size
        self.ttl_seconds = ttl_seconds
        self._cache: Dict[str, Dict[str, Any]] = {}
        self._access_times: Dict[str, float] = {}

    def _generate_key(
        self,
        context: IntelligenceContext,
        data_hash: str,
        service_name: str
    ) -> str:
        """Generate cache key from context and data"""
        key_data = {
            'user_id': context.user_id,
            'domain': context.domain,
            'tool_name': context.tool_name,
            'data_hash': data_hash,
            'service': service_name
        }
        key_str = json.dumps(key_data, sort_keys=True)
        return hashlib.md5(key_str.encode()).hexdigest()

    def get(
        self,
        context: IntelligenceContext,
        data_hash: str,
        service_name: str
    ) -> Optional[List[IntelligenceInsight]]:
        """Get cached insights"""
        key = self._generate_key(context, data_hash, service_name)

        if key not in self._cache:
            return None

        # Check TTL
        cache_entry = self._cache[key]
        if time.time() - cache_entry['timestamp'] > self.ttl_seconds:
            self._evict(key)
            return None

        # Update access time
        self._access_times[key] = time.time()
        return cache_entry['insights']

    def set(
        self,
        context: IntelligenceContext,
        data_hash: str,
        service_name: str,
        insights: List[IntelligenceInsight]
    ) -> None:
        """Cache insights"""
        key = self._generate_key(context, data_hash, service_name)

        # Evict if at max capacity
        if len(self._cache) >= self.max_size:
            self._evict_lru()

        self._cache[key] = {
            'insights': insights,
            'timestamp': time.time()
        }
        self._access_times[key] = time.time()

    def _evict(self, key: str) -> None:
        """Evict specific key"""
        self._cache.pop(key, None)
        self._access_times.pop(key, None)

    def _evict_lru(self) -> None:
        """Evict least recently used item"""
        if not self._access_times:
            return

        lru_key = min(self._access_times, key=self._access_times.get)
        self._evict(lru_key)


class IntelligenceMetrics:
    """Metrics collection for intelligence services"""

    def __init__(self):
        self.metrics: Dict[str, Any] = {
            'total_requests': 0,
            'successful_requests': 0,
            'failed_requests': 0,
            'average_response_time': 0.0,
            'cache_hits': 0,
            'cache_misses': 0,
            'insights_generated': 0,
            'service_health': {}
        }

    def record_request(
        self,
        service_name: str,
        success: bool,
        response_time: float,
        insights_count: int = 0
    ) -> None:
        """Record a service request"""
        self.metrics['total_requests'] += 1

        if success:
            self.metrics['successful_requests'] += 1
            self.metrics['insights_generated'] += insights_count
        else:
            self.metrics['failed_requests'] += 1

        # Update average response time
        total_requests = self.metrics['total_requests']
        current_avg = self.metrics['average_response_time']
        self.metrics['average_response_time'] = (
            (current_avg * (total_requests - 1) + response_time) /
            total_requests
        )

        # Update service-specific metrics
        if service_name not in self.metrics['service_health']:
            self.metrics['service_health'][service_name] = {
                'requests': 0,
                'failures': 0,
                'avg_response_time': 0.0
            }

        service_metrics = self.metrics['service_health'][service_name]
        service_metrics['requests'] += 1
        if not success:
            service_metrics['failures'] += 1

        # Update service average response time
        service_requests = service_metrics['requests']
        service_avg = service_metrics['avg_response_time']
        service_metrics['avg_response_time'] = (
            (service_avg * (service_requests - 1) + response_time) /
            service_requests
        )

    def record_cache_hit(self) -> None:
        """Record cache hit"""
        self.metrics['cache_hits'] += 1

    def record_cache_miss(self) -> None:
        """Record cache miss"""
        self.metrics['cache_misses'] += 1

    def get_cache_hit_rate(self) -> float:
        """Get cache hit rate"""
        total = self.metrics['cache_hits'] + self.metrics['cache_misses']
        if total == 0:
            return 0.0
        return self.metrics['cache_hits'] / total

    def get_success_rate(self) -> float:
        """Get overall success rate"""
        total = self.metrics['total_requests']
        if total == 0:
            return 0.0
        return self.metrics['successful_requests'] / total


def hash_data(data: Any) -> str:
    """Generate hash for data objects"""
    data_str = json.dumps(data, sort_keys=True, default=str)
    return hashlib.sha256(data_str.encode()).hexdigest()[:16]


def with_caching(
    cache: IntelligenceCache,
    service_name: str,
    ttl_seconds: Optional[int] = None
):
    """Decorator to add caching to intelligence service methods"""
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @functools.wraps(func)
        async def wrapper(*args, **kwargs) -> T:
            # Extract context and request data
            context = None

            # Look for IntelligenceContext in args/kwargs
            for arg in args:
                if hasattr(arg, '__dict__') and hasattr(arg, 'user_id'):
                    context = arg
                    break

            if context is None:
                # No context found, can't cache
                return await func(*args, **kwargs)

            # Hash the input data for cache key
            data_hash = hash_data({'args': args[1:], 'kwargs': kwargs})

            # Try to get from cache
            cached_result = cache.get(context, data_hash, service_name)
            if cached_result is not None:
                return cached_result

            # Execute function and cache result
            result = await func(*args, **kwargs)
            if isinstance(result, list) and all(
                isinstance(item, IntelligenceInsight) for item in result
            ):
                cache.set(context, data_hash, service_name, result)

            return result

        return wrapper
    return decorator


def with_metrics(metrics: IntelligenceMetrics, service_name: str):
    """Decorator to add metrics collection to intelligence service methods"""
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @functools.wraps(func)
        async def wrapper(*args, **kwargs) -> T:
            start_time = time.time()
            success = False
            insights_count = 0

            try:
                result = await func(*args, **kwargs)
                success = True

                # Count insights if result is a list of IntelligenceInsight
                if isinstance(result, list):
                    insights_count = len([
                        item for item in result
                        if isinstance(item, IntelligenceInsight)
                    ])

                return result

            except Exception as e:
                success = False
                raise e

            finally:
                response_time = time.time() - start_time
                metrics.record_request(
                    service_name,
                    success,
                    response_time,
                    insights_count
                )

        return wrapper
    return decorator


def with_timeout(timeout_seconds: float = 30.0):
    """Decorator to add timeout to intelligence service methods"""
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @functools.wraps(func)
        async def wrapper(*args, **kwargs) -> T:
            return await asyncio.wait_for(
                func(*args, **kwargs),
                timeout=timeout_seconds
            )
        return wrapper
    return decorator


def calculate_confidence(
    pattern_frequency: int,
    data_quality: float,
    temporal_consistency: float,
    user_feedback: float = 0.5
) -> ConfidenceLevel:
    """
    Calculate confidence level for intelligence insights

    Args:
        pattern_frequency: How often the pattern occurs (1-10)
        data_quality: Quality of input data (0.0-1.0)
        temporal_consistency: Consistency over time (0.0-1.0)
        user_feedback: User feedback score (0.0-1.0)

    Returns:
        Calculated confidence level
    """
    # Normalize pattern frequency to 0-1 scale
    freq_score = min(pattern_frequency / 10.0, 1.0)

    # Weighted average of factors
    confidence_score = (
        freq_score * 0.3 +
        data_quality * 0.3 +
        temporal_consistency * 0.25 +
        user_feedback * 0.15
    )

    if confidence_score >= 0.85:
        return ConfidenceLevel.VERY_HIGH
    elif confidence_score >= 0.65:
        return ConfidenceLevel.HIGH
    elif confidence_score >= 0.45:
        return ConfidenceLevel.MEDIUM
    elif confidence_score >= 0.25:
        return ConfidenceLevel.LOW
    else:
        return ConfidenceLevel.VERY_LOW


def create_insight(
    insight_id: str,
    title: str,
    description: str,
    intelligence_type,  # IntelligenceType (avoiding circular import)
    context: IntelligenceContext,
    confidence: ConfidenceLevel,
    recommendations: List[str],
    data: Dict[str, Any],
    expires_in_hours: int = 24,
    source_service: Optional[str] = None
) -> IntelligenceInsight:
    """Helper to create IntelligenceInsight objects"""
    expires_at = datetime.now() + timedelta(hours=expires_in_hours)

    return IntelligenceInsight(
        id=insight_id,
        type=intelligence_type,
        title=title,
        description=description,
        confidence=confidence,
        recommendations=recommendations,
        data=data,
        context=context,
        timestamp=datetime.now(),
        expires_at=expires_at,
        source_service=source_service
    )


def filter_insights_by_confidence(
    insights: List[IntelligenceInsight],
    min_confidence: ConfidenceLevel = ConfidenceLevel.MEDIUM
) -> List[IntelligenceInsight]:
    """Filter insights by minimum confidence level"""
    return [
        insight for insight in insights
        if insight.confidence.value >= min_confidence.value
    ]


def merge_similar_insights(
    insights: List[IntelligenceInsight],
    similarity_threshold: float = 0.8
) -> List[IntelligenceInsight]:
    """
    Merge similar insights to reduce duplication

    This is a simple implementation that could be enhanced with
    more sophisticated similarity detection algorithms.
    """
    if not insights:
        return insights

    merged = []
    used_indices = set()

    for i, insight in enumerate(insights):
        if i in used_indices:
            continue

        similar_insights = [insight]
        used_indices.add(i)

        # Find similar insights
        for j, other_insight in enumerate(insights[i+1:], i+1):
            if j in used_indices:
                continue

            # Simple similarity check based on title and type
            if (insight.type == other_insight.type and
                    _calculate_text_similarity(
                        insight.title, other_insight.title
                    ) >= similarity_threshold):
                similar_insights.append(other_insight)
                used_indices.add(j)

        # Merge similar insights
        if len(similar_insights) > 1:
            merged_insight = _merge_insights(similar_insights)
            merged.append(merged_insight)
        else:
            merged.append(insight)

    return merged


def _calculate_text_similarity(text1: str, text2: str) -> float:
    """Calculate similarity between two text strings"""
    # Simple Jaccard similarity
    words1 = set(text1.lower().split())
    words2 = set(text2.lower().split())

    intersection = words1.intersection(words2)
    union = words1.union(words2)

    if not union:
        return 0.0

    return len(intersection) / len(union)


def _merge_insights(insights: List[IntelligenceInsight]) -> IntelligenceInsight:
    """Merge multiple similar insights into one"""
    # Use the highest confidence insight as base
    base_insight = max(insights, key=lambda x: x.confidence.value)

    # Combine recommendations
    all_recommendations = []
    for insight in insights:
        all_recommendations.extend(insight.recommendations)
    unique_recommendations = list(set(all_recommendations))

    # Combine data
    merged_data = base_insight.data.copy()
    merged_data['merged_from_count'] = len(insights)
    merged_data['merged_sources'] = [
        insight.source_service for insight in insights
        if insight.source_service
    ]

    # Update title to indicate merging
    merged_title = f"{base_insight.title} (and {len(insights)-1} similar)"

    return IntelligenceInsight(
        id=base_insight.id,
        type=base_insight.type,
        title=merged_title,
        description=base_insight.description,
        confidence=base_insight.confidence,
        recommendations=unique_recommendations,
        data=merged_data,
        context=base_insight.context,
        timestamp=base_insight.timestamp,
        expires_at=base_insight.expires_at,
        source_service=base_insight.source_service
    )


# Global instances
default_cache = IntelligenceCache()
default_metrics = IntelligenceMetrics()
