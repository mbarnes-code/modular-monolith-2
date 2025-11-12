"""
Intelligence Service Adapters

Provides optional integration adapters for existing applications to easily
connect with intelligence services without modifying core business logic.

These adapters follow the principle: applications work perfectly without them.
"""

import asyncio
import functools
from contextlib import contextmanager
from datetime import datetime
from typing import Any, Callable, Dict, List, Optional, TypeVar

from ..shared.interfaces import (IntelligenceContext, IntelligenceInsight,
                                 IntelligenceRequest, IntelligenceType,
                                 intelligence_registry)

T = TypeVar('T')


class IntelligenceAdapter:
    """
    Base adapter for integrating intelligence services with applications

    Provides graceful degradation - if intelligence services are not available,
    applications continue working normally.
    """

    def __init__(
        self,
        app_name: str,
        domain: str,
        enabled: bool = True
    ):
        self.app_name = app_name
        self.domain = domain
        self.enabled = enabled
        self._cache: Dict[str, Any] = {}

    def create_context(
        self,
        user_id: str,
        tool_name: Optional[str] = None,
        session_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> IntelligenceContext:
        """Create intelligence context for requests"""
        return IntelligenceContext(
            user_id=user_id,
            domain=self.domain,
            tool_name=tool_name or self.app_name,
            session_id=session_id,
            timestamp=datetime.now(),
            metadata=metadata or {}
        )

    async def get_insights(
        self,
        user_id: str,
        data: Dict[str, Any],
        intelligence_types: Optional[List[IntelligenceType]] = None,
        session_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> List[IntelligenceInsight]:
        """
        Get intelligence insights for user data

        Returns empty list if intelligence services are not available.
        """
        if not self.enabled:
            return []

        try:
            context = self.create_context(
                user_id=user_id,
                session_id=session_id,
                metadata=metadata
            )

            request = IntelligenceRequest(
                request_id=f"{self.app_name}_{datetime.now().timestamp()}",
                intelligence_type=IntelligenceType.PATTERN_DETECTION,
                context=context,
                data=data
            )

            all_insights = []

            # If specific types requested, get those
            if intelligence_types:
                for intel_type in intelligence_types:
                    service = intelligence_registry.get_service(intel_type)
                    is_available = intelligence_registry.is_service_available(
                        intel_type
                    )
                    if service and is_available:
                        request.intelligence_type = intel_type
                        insights = await service.analyze(request)
                        all_insights.extend(insights)
            else:
                # Get insights from all available services
                insights_by_type = (
                    await intelligence_registry.get_all_insights(request)
                )
                for insights in insights_by_type.values():
                    all_insights.extend(insights)

            return all_insights

        except Exception as e:
            # Log error but don't fail the application
            print(f"Intelligence service error in {self.app_name}: {e}")
            return []

    def record_activity(
        self,
        user_id: str,
        activity_data: Dict[str, Any],
        session_id: Optional[str] = None
    ) -> None:
        """
        Record user activity for pattern analysis

        Fire-and-forget operation that doesn't affect application flow.
        """
        if not self.enabled:
            return

        try:
            # Create background task to record activity
            asyncio.create_task(
                self._background_record_activity(
                    user_id, activity_data, session_id
                )
            )
        except Exception:
            # Silently fail - recording shouldn't affect main application
            pass

    async def _background_record_activity(
        self,
        user_id: str,
        activity_data: Dict[str, Any],
        session_id: Optional[str] = None
    ) -> None:
        """Background task for recording activity"""
        try:
            context = self.create_context(
                user_id=user_id,
                session_id=session_id
            )

            request = IntelligenceRequest(
                request_id=f"activity_{datetime.now().timestamp()}",
                intelligence_type=IntelligenceType.PATTERN_DETECTION,
                context=context,
                data=activity_data
            )

            # Send to pattern detection service if available
            pattern_service = intelligence_registry.get_service(
                IntelligenceType.PATTERN_DETECTION
            )
            if pattern_service:
                await pattern_service.analyze(request)

        except Exception:
            # Silently fail
            pass


class SecurityIntelligenceAdapter(IntelligenceAdapter):
    """Adapter specifically for security applications"""

    def __init__(self, app_name: str, enabled: bool = True):
        super().__init__(app_name, "security", enabled)

    async def assess_threat(
        self,
        user_id: str,
        activity: Dict[str, Any],
        session_id: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Assess threat level of an activity

        Returns None if security intelligence is not available.
        """
        insights = await self.get_insights(
            user_id=user_id,
            data=activity,
            intelligence_types=[IntelligenceType.SECURITY_ANALYSIS],
            session_id=session_id
        )

        if not insights:
            return None

        # Return highest threat level found
        max_threat_insight = max(
            insights,
            key=lambda x: x.data.get('threat_level', 0)
        )

        return {
            'threat_level': max_threat_insight.data.get('threat_level', 0),
            'threat_description': max_threat_insight.description,
            'recommendations': max_threat_insight.recommendations,
            'confidence': max_threat_insight.confidence.value
        }


class ProductivityIntelligenceAdapter(IntelligenceAdapter):
    """Adapter specifically for productivity applications"""

    def __init__(self, app_name: str, enabled: bool = True):
        super().__init__(app_name, "productivity", enabled)

    async def get_productivity_insights(
        self,
        user_id: str,
        workflow_data: Dict[str, Any],
        session_id: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Get productivity optimization insights

        Returns empty list if productivity intelligence is not available.
        """
        insights = await self.get_insights(
            user_id=user_id,
            data=workflow_data,
            intelligence_types=[IntelligenceType.PRODUCTIVITY_OPTIMIZATION],
            session_id=session_id
        )

        return [
            {
                'title': insight.title,
                'description': insight.description,
                'recommendations': insight.recommendations,
                'confidence': insight.confidence.value,
                'data': insight.data
            }
            for insight in insights
        ]

    async def track_productivity_metrics(
        self,
        user_id: str,
        metrics: Dict[str, Any],
        session_id: Optional[str] = None
    ) -> None:
        """Track productivity metrics for analysis"""
        self.record_activity(user_id, metrics, session_id)


def with_intelligence(
    adapter: IntelligenceAdapter,
    intelligence_types: Optional[List[IntelligenceType]] = None
):
    """
    Decorator to add intelligence analysis to application functions

    Usage:
    @with_intelligence(my_adapter, [IntelligenceType.PATTERN_DETECTION])
    def my_function(user_id: str, data: dict):
        # Original function logic
        result = process_data(data)
        return result

    The decorated function will:
    1. Execute original logic normally
    2. Optionally analyze data for insights (if services available)
    3. Return original result + optional insights
    """
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs):
            # Execute original function
            result = await func(*args, **kwargs)

            # Try to add intelligence insights
            try:
                # Extract user_id and data from function arguments
                user_id = None
                data = {}

                # Look for user_id in kwargs or args
                if 'user_id' in kwargs:
                    user_id = kwargs['user_id']
                elif len(args) > 0:
                    # Assume first argument might be user_id if it's a string
                    if isinstance(args[0], str):
                        user_id = args[0]

                # Look for data in kwargs
                if 'data' in kwargs:
                    data = kwargs['data']
                elif len(args) > 1:
                    # Assume second argument might be data if it's a dict
                    if isinstance(args[1], dict):
                        data = args[1]

                if user_id and adapter.enabled:
                    insights = await adapter.get_insights(
                        user_id=user_id,
                        data=data,
                        intelligence_types=intelligence_types
                    )

                    # If result is a dict, add insights
                    if isinstance(result, dict):
                        result['intelligence_insights'] = insights
                    # If result is a tuple, add insights as additional element
                    elif isinstance(result, tuple):
                        result = (*result, insights)

            except Exception:
                # Intelligence failure shouldn't affect main function
                pass

            return result

        @functools.wraps(func)
        def sync_wrapper(*args, **kwargs):
            # For synchronous functions, just execute normally
            return func(*args, **kwargs)

        # Return appropriate wrapper based on function type
        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper

    return decorator


@contextmanager
def intelligence_session(
    adapter: IntelligenceAdapter,
    user_id: str,
    session_name: str = "default"
):
    """
    Context manager for intelligence-aware application sessions

    Usage:
    with intelligence_session(adapter, user_id, "analysis_session"):
        # All activities in this block are tracked for pattern analysis
        result1 = process_data(data1)
        result2 = analyze_results(result1)
    """
    session_id = f"{session_name}_{datetime.now().timestamp()}"

    try:
        # Session start activity
        adapter.record_activity(
            user_id=user_id,
            activity_data={
                'session_event': 'start',
                'session_name': session_name,
                'timestamp': datetime.now().isoformat()
            },
            session_id=session_id
        )

        yield session_id

    finally:
        # Session end activity
        adapter.record_activity(
            user_id=user_id,
            activity_data={
                'session_event': 'end',
                'session_name': session_name,
                'timestamp': datetime.now().isoformat()
            },
            session_id=session_id
        )


# Pre-configured adapters for common application types
def create_security_adapter(app_name: str) -> SecurityIntelligenceAdapter:
    """Create a security intelligence adapter"""
    return SecurityIntelligenceAdapter(app_name)


def create_productivity_adapter(app_name: str) -> ProductivityIntelligenceAdapter:
    """Create a productivity intelligence adapter"""
    return ProductivityIntelligenceAdapter(app_name)


def create_general_adapter(
    app_name: str,
    domain: str = "general"
) -> IntelligenceAdapter:
    """Create a general intelligence adapter"""
    return IntelligenceAdapter(app_name, domain)
