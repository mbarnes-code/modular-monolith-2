"""
Domain-Specific Performance Monitoring for Mental Prosthetic Platform

Monitors performance across all 37 tools with domain-specific targets:
- Security: <1s (threat analysis criticality)
- Productivity: <2s (task management workflows)  
- MTG: <3s (game analysis complexity)
- Infrastructure: <5s (system operations tolerance)
- UI Interactions: <200ms (executive function support)
"""

import asyncio
import logging
import time
from collections import defaultdict, deque
from contextlib import asynccontextmanager
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Callable, Dict, List, Optional

logger = logging.getLogger(__name__)


class PerformanceTier(Enum):
    """Performance tiers based on domain requirements."""
    SECURITY = "security"           # <1s for threat analysis
    PRODUCTIVITY = "productivity"   # <2s for task management
    MTG = "mtg"                    # <3s for game analysis
    INFRASTRUCTURE = "infrastructure"  # <5s for system operations
    UI_INTERACTION = "ui"          # <200ms for executive function


@dataclass
class PerformanceMetric:
    """Individual performance measurement."""
    operation: str
    tier: PerformanceTier
    duration_ms: int
    timestamp: datetime
    success: bool
    tool_id: str
    user_id: Optional[str] = None
    context: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TierMetrics:
    """Aggregated metrics for a performance tier."""
    tier: PerformanceTier
    target_ms: int
    count: int
    avg_duration_ms: float
    p95_duration_ms: float
    p99_duration_ms: float
    violation_count: int
    violation_rate: float
    success_rate: float


class PerformanceMonitor:
    """Monitor domain-specific performance across all mental prosthetic tools."""

    def __init__(self, history_size: int = 10000):
        self.history_size = history_size
        self.metrics: deque = deque(maxlen=history_size)
        self.tier_targets = {
            PerformanceTier.SECURITY: 1000,      # 1s
            PerformanceTier.PRODUCTIVITY: 2000,  # 2s
            PerformanceTier.MTG: 3000,          # 3s
            PerformanceTier.INFRASTRUCTURE: 5000,  # 5s
            PerformanceTier.UI_INTERACTION: 200  # 200ms
        }

        # Real-time violation tracking
        self.active_violations: Dict[str,
                                     List[PerformanceMetric]] = defaultdict(list)
        self.violation_callbacks: List[Callable] = []

        # Executive function monitoring
        self.ui_violation_threshold = 5  # Alert after 5 UI violations
        self.context_switch_penalty_ms = 50  # Additional latency for context switches

    def start_measurement(self, operation: str, tier: PerformanceTier,
                          tool_id: str, user_id: str = None,
                          context: Dict[str, Any] = None) -> 'PerformanceMeasurement':
        """Start a performance measurement for an operation."""
        return PerformanceMeasurement(
            monitor=self,
            operation=operation,
            tier=tier,
            tool_id=tool_id,
            user_id=user_id,
            context=context or {}
        )

    def record_metric(self, metric: PerformanceMetric) -> None:
        """Record a performance metric."""
        self.metrics.append(metric)

        # Check for violations
        target_ms = self.tier_targets[metric.tier]
        if metric.duration_ms > target_ms:
            self._handle_violation(metric, target_ms)

        # Executive function specific monitoring
        if metric.tier == PerformanceTier.UI_INTERACTION:
            self._monitor_ui_responsiveness(metric)

    def _handle_violation(self, metric: PerformanceMetric, target_ms: int) -> None:
        """Handle performance violations."""
        violation_key = f"{metric.tier.value}:{metric.tool_id}"
        self.active_violations[violation_key].append(metric)

        # Clean old violations (keep last hour)
        cutoff_time = datetime.utcnow() - timedelta(hours=1)
        self.active_violations[violation_key] = [
            v for v in self.active_violations[violation_key]
            if v.timestamp > cutoff_time
        ]

        # Log violation
        severity = self._get_violation_severity(metric.duration_ms, target_ms)
        logger.log(
            logging.WARNING if severity == "warning" else logging.ERROR,
            f"Performance violation: {metric.operation} in {metric.tool_id} "
            f"took {metric.duration_ms}ms (target: {target_ms}ms, tier: {metric.tier.value})"
        )

        # Notify callbacks
        for callback in self.violation_callbacks:
            try:
                callback(metric, target_ms, severity)
            except Exception as e:
                logger.error(f"Violation callback failed: {e}")

    def _monitor_ui_responsiveness(self, metric: PerformanceMetric) -> None:
        """Special monitoring for UI responsiveness (executive function support)."""
        if metric.duration_ms > self.tier_targets[PerformanceTier.UI_INTERACTION]:
            # Check for frequent UI violations
            ui_violations = self.active_violations.get("ui:all", [])
            recent_violations = [
                v for v in ui_violations
                if v.timestamp > datetime.utcnow() - timedelta(minutes=5)
            ]

            if len(recent_violations) >= self.ui_violation_threshold:
                logger.critical(
                    f"Frequent UI responsiveness violations detected: "
                    f"{len(recent_violations)} violations in 5 minutes. "
                    f"Executive function support may be compromised."
                )

    def _get_violation_severity(self, actual_ms: int, target_ms: int) -> str:
        """Determine violation severity based on how much target was exceeded."""
        ratio = actual_ms / target_ms
        if ratio >= 3.0:
            return "critical"
        elif ratio >= 2.0:
            return "error"
        else:
            return "warning"

    def get_tier_metrics(self, tier: PerformanceTier,
                         time_window: timedelta = None) -> TierMetrics:
        """Get aggregated metrics for a performance tier."""
        if time_window is None:
            time_window = timedelta(hours=1)

        cutoff_time = datetime.utcnow() - time_window
        tier_metrics = [
            m for m in self.metrics
            if m.tier == tier and m.timestamp > cutoff_time
        ]

        if not tier_metrics:
            return TierMetrics(
                tier=tier,
                target_ms=self.tier_targets[tier],
                count=0,
                avg_duration_ms=0,
                p95_duration_ms=0,
                p99_duration_ms=0,
                violation_count=0,
                violation_rate=0,
                success_rate=0
            )

        durations = [m.duration_ms for m in tier_metrics]
        durations.sort()

        target_ms = self.tier_targets[tier]
        violations = [m for m in tier_metrics if m.duration_ms > target_ms]
        successes = [m for m in tier_metrics if m.success]

        return TierMetrics(
            tier=tier,
            target_ms=target_ms,
            count=len(tier_metrics),
            avg_duration_ms=sum(durations) / len(durations),
            p95_duration_ms=durations[int(len(durations) * 0.95)],
            p99_duration_ms=durations[int(len(durations) * 0.99)],
            violation_count=len(violations),
            violation_rate=len(violations) / len(tier_metrics),
            success_rate=len(successes) / len(tier_metrics)
        )

    def get_tool_metrics(self, tool_id: str,
                         time_window: timedelta = None) -> Dict[str, Any]:
        """Get performance metrics for a specific tool."""
        if time_window is None:
            time_window = timedelta(hours=1)

        cutoff_time = datetime.utcnow() - time_window
        tool_metrics = [
            m for m in self.metrics
            if m.tool_id == tool_id and m.timestamp > cutoff_time
        ]

        if not tool_metrics:
            return {
                "tool_id": tool_id,
                "count": 0,
                "avg_duration_ms": 0,
                "violations": 0,
                "success_rate": 0
            }

        durations = [m.duration_ms for m in tool_metrics]
        successes = [m for m in tool_metrics if m.success]

        # Get tier-specific violations
        tier_violations = {}
        for tier in PerformanceTier:
            tier_tool_metrics = [m for m in tool_metrics if m.tier == tier]
            target_ms = self.tier_targets[tier]
            violations = [
                m for m in tier_tool_metrics if m.duration_ms > target_ms]
            tier_violations[tier.value] = len(violations)

        return {
            "tool_id": tool_id,
            "count": len(tool_metrics),
            "avg_duration_ms": sum(durations) / len(durations),
            "violations_by_tier": tier_violations,
            "total_violations": sum(tier_violations.values()),
            "success_rate": len(successes) / len(tool_metrics)
        }

    def get_executive_function_health(self) -> Dict[str, Any]:
        """Get executive function specific health metrics."""
        ui_metrics = self.get_tier_metrics(PerformanceTier.UI_INTERACTION)

        # Recent context switches (estimated from rapid tool changes)
        recent_metrics = [
            m for m in self.metrics
            if m.timestamp > datetime.utcnow() - timedelta(minutes=10)
        ]

        # Detect potential context switches
        context_switches = 0
        last_tool = None
        for metric in sorted(recent_metrics, key=lambda x: x.timestamp):
            if last_tool and last_tool != metric.tool_id:
                context_switches += 1
            last_tool = metric.tool_id

        return {
            "ui_responsiveness": {
                "target_ms": ui_metrics.target_ms,
                "avg_duration_ms": ui_metrics.avg_duration_ms,
                "violation_rate": ui_metrics.violation_rate,
                "compliance": ui_metrics.violation_rate < 0.05  # <5% violations acceptable
            },
            "context_switching": {
                "switches_per_10min": context_switches,
                # Rough estimate
                "estimated_cognitive_load": min(100, context_switches * 5)
            },
            "overall_ef_health": self._calculate_ef_health_score()
        }

    def _calculate_ef_health_score(self) -> float:
        """Calculate overall executive function health score (0-100)."""
        ui_metrics = self.get_tier_metrics(PerformanceTier.UI_INTERACTION)

        # UI responsiveness score (60% weight)
        ui_score = max(0, 100 - (ui_metrics.violation_rate * 200))

        # Overall performance score (40% weight)
        all_tiers_score = 0
        for tier in [PerformanceTier.SECURITY, PerformanceTier.PRODUCTIVITY,
                     PerformanceTier.MTG, PerformanceTier.INFRASTRUCTURE]:
            tier_metrics = self.get_tier_metrics(tier)
            tier_score = max(0, 100 - (tier_metrics.violation_rate * 100))
            all_tiers_score += tier_score
        all_tiers_score /= 4  # Average across tiers

        return (ui_score * 0.6 + all_tiers_score * 0.4)

    def add_violation_callback(self, callback: Callable) -> None:
        """Add callback to be notified of performance violations."""
        self.violation_callbacks.append(callback)

    def get_dashboard_data(self) -> Dict[str, Any]:
        """Get comprehensive performance data for monitoring dashboard."""
        tier_data = {}
        for tier in PerformanceTier:
            tier_data[tier.value] = self.get_tier_metrics(tier).__dict__

        return {
            "timestamp": datetime.utcnow().isoformat(),
            "tier_metrics": tier_data,
            "executive_function": self.get_executive_function_health(),
            "active_violations": {
                k: len(v) for k, v in self.active_violations.items()
            },
            "total_measurements": len(self.metrics)
        }


class PerformanceMeasurement:
    """Context manager for measuring operation performance."""

    def __init__(self, monitor: PerformanceMonitor, operation: str,
                 tier: PerformanceTier, tool_id: str, user_id: str = None,
                 context: Dict[str, Any] = None):
        self.monitor = monitor
        self.operation = operation
        self.tier = tier
        self.tool_id = tool_id
        self.user_id = user_id
        self.context = context or {}
        self.start_time = None
        self.success = True

    def __enter__(self) -> 'PerformanceMeasurement':
        self.start_time = time.perf_counter()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.start_time is None:
            return

        duration_ms = int((time.perf_counter() - self.start_time) * 1000)

        # Check for context switching penalty
        if self.context.get("context_switch", False):
            duration_ms += self.monitor.context_switch_penalty_ms

        # Record failure if exception occurred
        if exc_type is not None:
            self.success = False

        metric = PerformanceMetric(
            operation=self.operation,
            tier=self.tier,
            duration_ms=duration_ms,
            timestamp=datetime.utcnow(),
            success=self.success,
            tool_id=self.tool_id,
            user_id=self.user_id,
            context=self.context
        )

        self.monitor.record_metric(metric)

    @asynccontextmanager
    async def async_context(self):
        """Async context manager version."""
        self.start_time = time.perf_counter()
        try:
            yield self
        except Exception as e:
            self.success = False
            raise
        finally:
            if self.start_time is not None:
                duration_ms = int(
                    (time.perf_counter() - self.start_time) * 1000)

                if self.context.get("context_switch", False):
                    duration_ms += self.monitor.context_switch_penalty_ms

                metric = PerformanceMetric(
                    operation=self.operation,
                    tier=self.tier,
                    duration_ms=duration_ms,
                    timestamp=datetime.utcnow(),
                    success=self.success,
                    tool_id=self.tool_id,
                    user_id=self.user_id,
                    context=self.context
                )

                self.monitor.record_metric(metric)


# Global performance monitor instance
performance_monitor = PerformanceMonitor()


# Convenience functions for common measurement patterns
def measure_security_operation(operation: str, tool_id: str, user_id: str = None):
    """Measure a security domain operation (<1s target)."""
    return performance_monitor.start_measurement(
        operation, PerformanceTier.SECURITY, tool_id, user_id
    )


def measure_productivity_operation(operation: str, tool_id: str, user_id: str = None):
    """Measure a productivity domain operation (<2s target)."""
    return performance_monitor.start_measurement(
        operation, PerformanceTier.PRODUCTIVITY, tool_id, user_id
    )


def measure_mtg_operation(operation: str, tool_id: str, user_id: str = None):
    """Measure an MTG domain operation (<3s target)."""
    return performance_monitor.start_measurement(
        operation, PerformanceTier.MTG, tool_id, user_id
    )


def measure_infrastructure_operation(operation: str, tool_id: str, user_id: str = None):
    """Measure an infrastructure domain operation (<5s target)."""
    return performance_monitor.start_measurement(
        operation, PerformanceTier.INFRASTRUCTURE, tool_id, user_id
    )


def measure_ui_interaction(operation: str, tool_id: str, user_id: str = None):
    """Measure a UI interaction (<200ms target for executive function support)."""
    return performance_monitor.start_measurement(
        operation, PerformanceTier.UI_INTERACTION, tool_id, user_id
    )


# Example violation callback for alerting
def log_critical_violations(metric: PerformanceMetric, target_ms: int, severity: str):
    """Example callback for handling critical performance violations."""
    if severity == "critical":
        logger.critical(
            f"CRITICAL PERFORMANCE VIOLATION: {metric.operation} in {metric.tool_id} "
            f"took {metric.duration_ms}ms (target: {target_ms}ms). "
            f"Executive function support may be severely impacted."
        )


# Register default violation callback
performance_monitor.add_violation_callback(log_critical_violations)
