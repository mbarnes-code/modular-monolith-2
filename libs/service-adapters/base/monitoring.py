"""
Performance monitoring and metrics for service adapters.

Tracks domain-specific performance, executive function compliance,
and overall system health across all 37 mental prosthetic tools.
"""

import logging
from collections import defaultdict, deque
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


@dataclass
class DomainMetrics:
    """Metrics for a specific tool domain."""
    domain: str
    tool_count: int
    active_tools: int
    average_response_time_ms: float
    p95_response_time_ms: float
    error_rate: float
    requests_per_minute: float
    target_response_time_ms: int
    compliance_rate: float


@dataclass
class ExecutiveFunctionMetrics:
    """Metrics for executive function accommodations."""
    ui_response_violations: int = 0
    context_switches: int = 0
    focus_assists_applied: int = 0
    adhd_accommodations_applied: int = 0
    cognitive_load_warnings: int = 0
    accommodation_success_rate: float = 0.0


class PerformanceMonitor:
    """Monitor performance across all service adapters."""

    def __init__(self, history_size: int = 1000):
        self.history_size = history_size
        self.response_times: Dict[str, deque] = defaultdict(
            lambda: deque(maxlen=history_size)
        )
        self.error_counts: Dict[str, int] = defaultdict(int)
        self.request_counts: Dict[str, int] = defaultdict(int)
        self.last_request_time: Dict[str, datetime] = {}

        # Executive function metrics
        self.executive_function_metrics = ExecutiveFunctionMetrics()

        # Domain configuration
        self.domain_targets = {
            "security": 1000,      # 1s for security domain
            "productivity": 2000,  # 2s for productivity domain
            "mtg": 3000,           # 3s for MTG domain
            "infrastructure": 5000  # 5s for infrastructure domain
        }

        self.ui_response_threshold = 200  # 200ms for UI responsiveness

    def record_request(self, tool_id: str, response_time_ms: int,
                       success: bool = True, domain: str = "unknown"):
        """Record a request and its performance metrics."""
        self.request_counts[tool_id] += 1
        self.response_times[tool_id].append(response_time_ms)
        self.last_request_time[tool_id] = datetime.utcnow()

        if not success:
            self.error_counts[tool_id] += 1

        # Check domain performance compliance
        target = self.domain_targets.get(domain, 2000)
        if response_time_ms > target:
            logger.warning(
                f"Performance violation: {tool_id} ({response_time_ms}ms > {target}ms)"
            )

        # Check UI responsiveness
        if response_time_ms > self.ui_response_threshold:
            self.executive_function_metrics.ui_response_violations += 1

    def record_executive_function_event(self, event_type: str, tool_id: str = None):
        """Record executive function accommodation events."""
        if event_type == "context_switch":
            self.executive_function_metrics.context_switches += 1
        elif event_type == "focus_assist":
            self.executive_function_metrics.focus_assists_applied += 1
        elif event_type == "adhd_accommodation":
            self.executive_function_metrics.adhd_accommodations_applied += 1
        elif event_type == "cognitive_load_warning":
            self.executive_function_metrics.cognitive_load_warnings += 1

    def get_tool_metrics(self, tool_id: str) -> Dict[str, Any]:
        """Get performance metrics for a specific tool."""
        response_times = list(self.response_times[tool_id])
        request_count = self.request_counts[tool_id]
        error_count = self.error_counts[tool_id]

        if not response_times:
            return {
                "tool_id": tool_id,
                "request_count": 0,
                "average_response_time_ms": 0,
                "p95_response_time_ms": 0,
                "error_rate": 0,
                "last_request": None
            }

        avg_response = sum(response_times) / len(response_times)
        p95_response = sorted(response_times)[int(len(response_times) * 0.95)]
        error_rate = error_count / max(request_count, 1)

        return {
            "tool_id": tool_id,
            "request_count": request_count,
            "average_response_time_ms": round(avg_response, 2),
            "p95_response_time_ms": p95_response,
            "error_rate": round(error_rate, 4),
            "last_request": self.last_request_time.get(tool_id)
        }

    def get_domain_metrics(self, domain: str, tool_ids: List[str]) -> DomainMetrics:
        """Get aggregated metrics for a domain."""
        active_tools = 0
        total_requests = 0
        total_errors = 0
        all_response_times = []

        for tool_id in tool_ids:
            tool_metrics = self.get_tool_metrics(tool_id)
            if tool_metrics["request_count"] > 0:
                active_tools += 1
                total_requests += tool_metrics["request_count"]
                total_errors += self.error_counts[tool_id]
                all_response_times.extend(list(self.response_times[tool_id]))

        if not all_response_times:
            avg_response = 0
            p95_response = 0
        else:
            avg_response = sum(all_response_times) / len(all_response_times)
            p95_response = sorted(all_response_times)[
                int(len(all_response_times) * 0.95)]

        error_rate = total_errors / max(total_requests, 1)
        target_ms = self.domain_targets.get(domain, 2000)

        # Calculate compliance rate (requests meeting target)
        compliant_requests = sum(
            1 for rt in all_response_times if rt <= target_ms)
        compliance_rate = compliant_requests / max(len(all_response_times), 1)

        # Calculate requests per minute
        now = datetime.utcnow()
        recent_requests = 0
        for tool_id in tool_ids:
            last_request = self.last_request_time.get(tool_id)
            if last_request and (now - last_request) < timedelta(minutes=1):
                recent_requests += self.request_counts[tool_id]

        return DomainMetrics(
            domain=domain,
            tool_count=len(tool_ids),
            active_tools=active_tools,
            average_response_time_ms=round(avg_response, 2),
            p95_response_time_ms=p95_response,
            error_rate=round(error_rate, 4),
            requests_per_minute=recent_requests,
            target_response_time_ms=target_ms,
            compliance_rate=round(compliance_rate, 4)
        )

    def get_executive_function_metrics(self) -> ExecutiveFunctionMetrics:
        """Get executive function accommodation metrics."""
        # Calculate accommodation success rate
        total_accommodations = (
            self.executive_function_metrics.focus_assists_applied +
            self.executive_function_metrics.adhd_accommodations_applied
        )

        if total_accommodations > 0:
            # Success = accommodations that didn't result in violations
            successful_accommodations = total_accommodations - (
                self.executive_function_metrics.ui_response_violations +
                self.executive_function_metrics.cognitive_load_warnings
            )
            success_rate = max(0, successful_accommodations) / \
                total_accommodations
        else:
            success_rate = 1.0  # No accommodations needed = perfect success

        metrics = ExecutiveFunctionMetrics(
            ui_response_violations=self.executive_function_metrics.ui_response_violations,
            context_switches=self.executive_function_metrics.context_switches,
            focus_assists_applied=self.executive_function_metrics.focus_assists_applied,
            adhd_accommodations_applied=self.executive_function_metrics.adhd_accommodations_applied,
            cognitive_load_warnings=self.executive_function_metrics.cognitive_load_warnings,
            accommodation_success_rate=round(success_rate, 4)
        )

        return metrics

    def get_system_health_score(self) -> float:
        """Calculate overall system health score (0-100)."""
        if not self.request_counts:
            return 100.0  # No requests = perfect health

        # Factor 1: Error rates (40% weight)
        total_requests = sum(self.request_counts.values())
        total_errors = sum(self.error_counts.values())
        error_rate = total_errors / total_requests
        error_score = max(0, 100 - (error_rate * 1000))  # 10% error = 0 points

        # Factor 2: Response time compliance (40% weight)
        all_response_times = []
        for times in self.response_times.values():
            all_response_times.extend(list(times))

        if all_response_times:
            avg_response = sum(all_response_times) / len(all_response_times)
            # Normalize against 2s target (default)
            response_score = max(0, 100 - (avg_response / 20))
        else:
            response_score = 100

        # Factor 3: Executive function compliance (20% weight)
        ef_metrics = self.get_executive_function_metrics()
        ef_score = ef_metrics.accommodation_success_rate * 100

        # Weighted average
        health_score = (
            error_score * 0.4 +
            response_score * 0.4 +
            ef_score * 0.2
        )

        return round(health_score, 2)

    def reset_metrics(self, tool_id: str = None):
        """Reset metrics for a specific tool or all tools."""
        if tool_id:
            self.response_times[tool_id].clear()
            self.error_counts[tool_id] = 0
            self.request_counts[tool_id] = 0
            if tool_id in self.last_request_time:
                del self.last_request_time[tool_id]
        else:
            self.response_times.clear()
            self.error_counts.clear()
            self.request_counts.clear()
            self.last_request_time.clear()
            self.executive_function_metrics = ExecutiveFunctionMetrics()


# Global performance monitor instance
performance_monitor = PerformanceMonitor()
