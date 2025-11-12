"""
PatternDetectionService for analyzing user request patterns.

This service analyzes user interactions to identify recurring patterns
that can be automated through n8n workflow generation.
"""

import hashlib
from collections import defaultdict
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

from sqlalchemy import desc
from sqlalchemy.orm import Session

from ..data.models.user_request import UserRequest
from ..data.models.workflow_pattern import WorkflowPattern
from .base_service import BaseService


class PatternDetectionService(BaseService):
    """
    Service for detecting user behavior patterns for workflow automation.

    Analyzes user requests to identify recurring patterns that meet
    the constitutional requirement of 3+ occurrences within 7 days.
    """

    def __init__(self, db_session: Session):
        super().__init__(db_session)
        self.min_pattern_occurrences = 3  # Constitutional requirement
        self.pattern_detection_window_days = 7
        self.confidence_threshold = 0.7

    def analyze_user_patterns(
        self,
        user_id: str,
        lookback_days: int = 30
    ) -> List[WorkflowPattern]:
        """
        Analyze user requests to detect automation patterns.

        Args:
            user_id: User to analyze patterns for
            lookback_days: How many days back to analyze

        Returns:
            List of detected patterns meeting criteria
        """
        # Get recent user requests
        cutoff_date = datetime.utcnow() - timedelta(days=lookback_days)
        requests = self.db_session.query(UserRequest).filter(
            UserRequest.user_id == user_id,
            UserRequest.request_timestamp >= cutoff_date,
            UserRequest.execution_success,
            UserRequest.tools_used.isnot(None)
        ).order_by(desc(UserRequest.request_timestamp)).all()

        if len(requests) < self.min_pattern_occurrences:
            return []

        # Group requests by potential patterns
        pattern_groups = self._group_requests_by_similarity(requests)

        # Analyze each group for pattern detection
        detected_patterns = []
        for pattern_features, grouped_requests in pattern_groups.items():
            if len(grouped_requests) >= self.min_pattern_occurrences:
                pattern = self._create_pattern_from_requests(
                    pattern_features, grouped_requests, user_id
                )
                if pattern:
                    detected_patterns.append(pattern)

        return detected_patterns

    def _group_requests_by_similarity(
        self,
        requests: List[UserRequest]
    ) -> Dict[str, List[UserRequest]]:
        """Group requests by similarity for pattern detection."""
        pattern_groups = defaultdict(list)

        for request in requests:
            # Extract pattern features
            features = self._extract_pattern_features(request)
            pattern_key = self._generate_pattern_key(features)
            pattern_groups[pattern_key].append(request)

        return dict(pattern_groups)

    def _extract_pattern_features(self, request: UserRequest) -> Dict[str, Any]:
        """Extract features from a request for pattern matching."""
        tools_used = sorted(request.tools_used or [])

        return {
            "intent_category": request.intent_category,
            "tools_used": tools_used,
            "tool_count": len(tools_used),
            "domain_context": request.domain_context,
            "execution_duration_bucket": self._bucket_duration(
                request.execution_duration or 0
            ),
            "action_count_bucket": self._bucket_action_count(
                len(request.actions_taken or [])
            )
        }

    def _generate_pattern_key(self, features: Dict[str, Any]) -> str:
        """Generate a consistent key for pattern grouping."""
        # Create a normalized representation for hashing
        key_parts = [
            features.get("intent_category", "unknown"),
            "|".join(features.get("tools_used", [])),
            str(features.get("tool_count", 0)),
            features.get("domain_context", "unknown"),
            str(features.get("execution_duration_bucket", 0)),
            str(features.get("action_count_bucket", 0))
        ]

        key_string = "::".join(key_parts)
        return hashlib.md5(key_string.encode()).hexdigest()[:16]

    def _bucket_duration(self, duration: float) -> int:
        """Bucket execution duration for pattern matching."""
        if duration < 10:
            return 1  # Fast
        elif duration < 60:
            return 2  # Medium
        elif duration < 300:
            return 3  # Slow
        else:
            return 4  # Very slow

    def _bucket_action_count(self, count: int) -> int:
        """Bucket action count for pattern matching."""
        if count <= 1:
            return 1  # Simple
        elif count <= 5:
            return 2  # Medium
        elif count <= 10:
            return 3  # Complex
        else:
            return 4  # Very complex

    def _create_pattern_from_requests(
        self,
        pattern_key: str,
        requests: List[UserRequest],
        user_id: str
    ) -> Optional[WorkflowPattern]:
        """Create a WorkflowPattern from grouped requests."""
        if not requests:
            return None

        # Check if pattern already exists
        existing_pattern = self.db_session.query(WorkflowPattern).filter(
            WorkflowPattern.pattern_hash == pattern_key,
            WorkflowPattern.user_id == user_id
        ).first()

        if existing_pattern:
            # Update existing pattern
            existing_pattern.update_occurrence()
            existing_pattern.calculate_confidence()
            return existing_pattern

        # Analyze requests to extract pattern details
        first_request = requests[0]
        pattern_analysis = self._analyze_pattern_details(requests)

        # Create new pattern
        pattern = WorkflowPattern(
            pattern_hash=pattern_key,
            pattern_name=self._generate_pattern_name(first_request, requests),
            description=self._generate_pattern_description(requests),
            category=first_request.domain_context or "general",
            complexity_score=self._calculate_complexity_score(requests),
            trigger_sequence=pattern_analysis["trigger_sequence"],
            tool_sequence=pattern_analysis["tool_sequence"],
            data_flow=pattern_analysis["data_flow"],
            timing_pattern=pattern_analysis["timing_pattern"],
            occurrence_count=len(requests),
            first_detected=requests[-1].request_timestamp,
            last_seen=requests[0].request_timestamp,
            user_id=user_id
        )

        pattern.calculate_confidence()

        # Associate requests with pattern
        for request in requests:
            request.set_pattern_association(
                pattern_key, pattern.confidence_score)

        self.db_session.add(pattern)
        return pattern

    def _generate_pattern_name(
        self,
        first_request: UserRequest,
        requests: List[UserRequest]
    ) -> str:
        """Generate a descriptive name for the pattern."""
        tools = first_request.tools_used or []
        domain = first_request.domain_context or "General"

        if len(tools) == 1:
            return f"{domain} - {tools[0]} Operation"
        elif len(tools) <= 3:
            return f"{domain} - {' + '.join(tools[:3])} Workflow"
        else:
            return f"{domain} - Multi-tool Workflow ({len(tools)} tools)"

    def _generate_pattern_description(self, requests: List[UserRequest]) -> str:
        """Generate a description for the pattern."""
        tools = set()
        intents = set()

        for request in requests:
            if request.tools_used:
                tools.update(request.tools_used)
            if request.intent_category:
                intents.add(request.intent_category)

        tool_list = ", ".join(sorted(tools)[:5])
        intent_list = ", ".join(sorted(intents)[:3])

        return (
            f"Recurring pattern involving {tool_list}. "
            f"Common intents: {intent_list}. "
            f"Detected {len(requests)} times."
        )

    def _calculate_complexity_score(self, requests: List[UserRequest]) -> int:
        """Calculate complexity score (1-10) for the pattern."""
        avg_tools = sum(
            len(r.tools_used or []) for r in requests
        ) / len(requests)
        avg_actions = sum(
            len(r.actions_taken or []) for r in requests
        ) / len(requests)
        avg_duration = sum(
            r.execution_duration or 0 for r in requests
        ) / len(requests)

        # Calculate complexity based on multiple factors
        complexity = 1

        # Tool count factor (0-3 points)
        if avg_tools >= 5:
            complexity += 3
        elif avg_tools >= 3:
            complexity += 2
        elif avg_tools >= 2:
            complexity += 1

        # Action count factor (0-3 points)
        if avg_actions >= 10:
            complexity += 3
        elif avg_actions >= 5:
            complexity += 2
        elif avg_actions >= 3:
            complexity += 1

        # Duration factor (0-2 points)
        if avg_duration >= 300:  # 5+ minutes
            complexity += 2
        elif avg_duration >= 60:  # 1+ minute
            complexity += 1

        # Data flow complexity (0-2 points)
        has_data_transformation = any(
            len(r.actions_taken or []) > 2 for r in requests
        )
        if has_data_transformation:
            complexity += 1

        return min(complexity, 10)

    def _analyze_pattern_details(
        self,
        requests: List[UserRequest]
    ) -> Dict[str, Any]:
        """Analyze requests to extract detailed pattern information."""
        # Extract common trigger sequence
        trigger_sequence = self._extract_trigger_sequence(requests)

        # Extract tool sequence
        tool_sequence = self._extract_tool_sequence(requests)

        # Extract data flow patterns
        data_flow = self._extract_data_flow_pattern(requests)

        # Extract timing patterns
        timing_pattern = self._extract_timing_pattern(requests)

        return {
            "trigger_sequence": trigger_sequence,
            "tool_sequence": tool_sequence,
            "data_flow": data_flow,
            "timing_pattern": timing_pattern
        }

    def _extract_trigger_sequence(
        self,
        requests: List[UserRequest]
    ) -> Dict[str, Any]:
        """Extract common trigger patterns from requests."""
        # Analyze what triggers these requests
        triggers = []
        for request in requests:
            trigger = {
                "intent": request.intent_category,
                "context": request.domain_context,
                "has_previous": bool(request.previous_request_id)
            }
            triggers.append(trigger)

        return {
            "common_intent": max(
                set(r.intent_category for r in requests if r.intent_category),
                key=lambda x: sum(
                    1 for r in requests if r.intent_category == x
                ),
                default="unknown"
            ),
            "common_context": max(
                set(r.domain_context for r in requests if r.domain_context),
                key=lambda x: sum(
                    1 for r in requests if r.domain_context == x
                ),
                default="general"
            ),
            "is_chained": sum(
                1 for r in requests if r.previous_request_id
            ) > len(requests) * 0.5
        }

    def _extract_tool_sequence(
        self,
        requests: List[UserRequest]
    ) -> List[str]:
        """Extract common tool usage sequence."""
        # Find the most common tool sequence
        tool_sequences = [r.tools_used or [] for r in requests]

        if not tool_sequences:
            return []

        # Find longest common sequence
        common_tools = set(tool_sequences[0])
        for seq in tool_sequences[1:]:
            common_tools &= set(seq)

        return sorted(list(common_tools))

    def _extract_data_flow_pattern(
        self,
        requests: List[UserRequest]
    ) -> Dict[str, Any]:
        """Extract data flow patterns from requests."""
        return {
            "has_data_transformation": any(
                len(r.actions_taken or []) > 2 for r in requests
            ),
            "multi_tool_data_flow": any(
                len(r.tools_used or []) > 1 for r in requests
            ),
            "average_actions": sum(
                len(r.actions_taken or []) for r in requests
            ) / len(requests)
        }

    def _extract_timing_pattern(
        self,
        requests: List[UserRequest]
    ) -> Dict[str, Any]:
        """Extract timing patterns from requests."""
        timestamps = [
            r.request_timestamp for r in requests if r.request_timestamp]

        if len(timestamps) < 2:
            return {"has_timing_pattern": False}

        # Calculate intervals between requests
        timestamps.sort()
        intervals = [
            (timestamps[i] - timestamps[i-1]).total_seconds() / 3600  # hours
            for i in range(1, len(timestamps))
        ]

        avg_interval = sum(intervals) / len(intervals)

        return {
            "has_timing_pattern": True,
            "average_interval_hours": avg_interval,
            "is_regular": all(
                abs(interval - avg_interval) < avg_interval * 0.3
                for interval in intervals
            ),
            "suggested_schedule": self._suggest_schedule(avg_interval)
        }

    def _suggest_schedule(self, avg_interval_hours: float) -> str:
        """Suggest a schedule based on average interval."""
        if avg_interval_hours < 1:
            return "every_30_minutes"
        elif avg_interval_hours < 6:
            return "hourly"
        elif avg_interval_hours < 36:
            return "daily"
        elif avg_interval_hours < 200:
            return "weekly"
        else:
            return "monthly"

    def get_patterns_ready_for_automation(
        self,
        user_id: str
    ) -> List[WorkflowPattern]:
        """Get patterns that are ready for n8n workflow generation."""
        return self.db_session.query(WorkflowPattern).filter(
            WorkflowPattern.user_id == user_id,
            WorkflowPattern.occurrence_count >= self.min_pattern_occurrences,
            WorkflowPattern.confidence_score >= self.confidence_threshold,
            WorkflowPattern.workflow_generated == False
        ).order_by(desc(WorkflowPattern.occurrence_count)).all()

    def update_pattern_feedback(
        self,
        pattern_id: str,
        user_feedback: Dict[str, Any]
    ) -> bool:
        """Update pattern with user feedback."""
        pattern = self.db_session.query(WorkflowPattern).filter(
            WorkflowPattern.id == pattern_id
        ).first()

        if not pattern:
            return False

        # Update user feedback
        if "rating" in user_feedback:
            pattern.user_feedback_score = float(user_feedback["rating"])

        if "validated" in user_feedback:
            pattern.is_validated = bool(user_feedback["validated"])

        # Recalculate confidence
        pattern.calculate_confidence()

        return True
