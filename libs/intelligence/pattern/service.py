"""
Pattern Detection Intelligence Service

Analyzes user interactions and workflow patterns to identify automation
opportunities, efficiency improvements, and behavioral insights.

This service is OPTIONAL and applications work perfectly without it.
"""

import uuid
from collections import defaultdict
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

from ..shared.interfaces import (IntelligenceContext, IntelligenceInsight,
                                 IntelligenceRequest, IntelligenceType,
                                 PatternIntelligenceInterface)
from ..shared.utils import (calculate_confidence, create_insight,
                            default_cache, default_metrics, with_caching,
                            with_metrics, with_timeout)


class PatternDetectionService(PatternIntelligenceInterface):
    """
    Advanced pattern detection service for user workflow analysis

    Identifies recurring patterns in user behavior and suggests optimizations.
    Builds on the existing pattern detection from jane-orchestrator but
    provides cross-domain intelligence.
    """

    def __init__(self, name: str = "pattern_detection"):
        self.name = name
        self.min_pattern_occurrences = 3
        self.pattern_confidence_threshold = 0.6
        self.lookback_window_days = 30

        # In-memory pattern storage (in production, use persistent storage)
        self.interaction_history: Dict[
            str, List[Dict[str, Any]]
        ] = defaultdict(list)
        self.detected_patterns: Dict[
            str, List[Dict[str, Any]]
        ] = defaultdict(list)

    @with_timeout(timeout_seconds=15.0)
    @with_metrics(default_metrics, "pattern_detection")
    @with_caching(default_cache, "pattern_detection")
    async def analyze(
        self,
        request: IntelligenceRequest
    ) -> List[IntelligenceInsight]:
        """Analyze patterns in user data"""
        context = request.context
        data = request.data

        insights = []

        # Record the interaction
        await self._record_interaction(context, data)

        # Detect workflow patterns
        workflow_patterns = await self._detect_workflow_patterns(context)
        insights.extend(workflow_patterns)

        # Detect temporal patterns
        temporal_patterns = await self._detect_temporal_patterns(context)
        insights.extend(temporal_patterns)

        # Detect efficiency opportunities
        efficiency_insights = await self._detect_efficiency_opportunities(
            context
        )
        insights.extend(efficiency_insights)

        return insights

    async def get_cached_insights(
        self,
        context: IntelligenceContext,
        intelligence_type: Optional[IntelligenceType] = None
    ) -> List[IntelligenceInsight]:
        """Get cached pattern insights"""
        # This would normally query a persistent cache
        return []

    async def health_check(self) -> Dict[str, Any]:
        """Check service health"""
        return {
            "service": self.name,
            "status": "healthy",
            "metrics": {
                "total_users": len(self.interaction_history),
                "total_interactions": sum(
                    len(interactions)
                    for interactions in self.interaction_history.values()
                ),
                "detected_patterns": sum(
                    len(patterns)
                    for patterns in self.detected_patterns.values()
                )
            },
            "timestamp": datetime.now().isoformat()
        }

    def get_service_info(self) -> Dict[str, Any]:
        """Get service information"""
        return {
            "name": self.name,
            "type": IntelligenceType.PATTERN_DETECTION.value,
            "description": "Detects user workflow and behavioral patterns",
            "capabilities": [
                "workflow_pattern_detection",
                "temporal_pattern_analysis",
                "efficiency_optimization",
                "automation_suggestions",
                "cross_tool_analysis"
            ],
            "min_data_points": self.min_pattern_occurrences,
            "confidence_threshold": self.pattern_confidence_threshold
        }

    async def detect_patterns(
        self,
        user_interactions: List[Dict[str, Any]],
        context: IntelligenceContext,
        lookback_days: int = 30
    ) -> List[IntelligenceInsight]:
        """Detect patterns in user interactions"""
        insights = []

        # Store interactions for analysis
        self.interaction_history[context.user_id].extend(user_interactions)

        # Analyze sequential patterns
        sequential_patterns = await self._analyze_sequential_patterns(
            user_interactions, context
        )
        insights.extend(sequential_patterns)

        # Analyze tool usage patterns
        tool_patterns = await self._analyze_tool_usage_patterns(
            user_interactions, context
        )
        insights.extend(tool_patterns)

        # Analyze data flow patterns
        data_flow_patterns = await self._analyze_data_flow_patterns(
            user_interactions, context
        )
        insights.extend(data_flow_patterns)

        return insights

    async def predict_next_action(
        self,
        current_session: Dict[str, Any],
        context: IntelligenceContext
    ) -> List[IntelligenceInsight]:
        """Predict likely next actions based on patterns"""
        insights = []

        user_history = self.interaction_history.get(context.user_id, [])
        if len(user_history) < self.min_pattern_occurrences:
            return insights

        # Find similar historical sessions
        similar_sessions = await self._find_similar_sessions(
            current_session, user_history
        )

        if similar_sessions:
            predictions = await self._generate_predictions(
                similar_sessions, context
            )
            insights.extend(predictions)

        return insights

    async def _record_interaction(
        self,
        context: IntelligenceContext,
        data: Dict[str, Any]
    ) -> None:
        """Record user interaction for pattern analysis"""
        interaction = {
            'timestamp': datetime.now().isoformat(),
            'user_id': context.user_id,
            'domain': context.domain,
            'tool_name': context.tool_name,
            'session_id': context.session_id,
            'data': data,
            'metadata': context.metadata or {}
        }

        self.interaction_history[context.user_id].append(interaction)

        # Keep only recent interactions (memory management)
        cutoff = datetime.now() - timedelta(days=self.lookback_window_days)
        self.interaction_history[context.user_id] = [
            interaction
            for interaction in self.interaction_history[context.user_id]
            if datetime.fromisoformat(interaction['timestamp']) > cutoff
        ]

    async def _detect_workflow_patterns(
        self,
        context: IntelligenceContext
    ) -> List[IntelligenceInsight]:
        """Detect recurring workflow patterns"""
        insights = []
        user_interactions = self.interaction_history.get(context.user_id, [])

        if len(user_interactions) < self.min_pattern_occurrences:
            return insights

        # Group interactions by session
        sessions = defaultdict(list)
        for interaction in user_interactions:
            session_id = interaction.get('session_id', 'unknown')
            sessions[session_id].append(interaction)

        # Find recurring tool sequences
        tool_sequences = []
        for session_interactions in sessions.values():
            tools = [
                i.get('tool_name') for i in session_interactions
                if i.get('tool_name')
            ]
            if len(tools) > 1:
                tool_sequences.append(tools)

        # Detect common sequences
        sequence_counts = defaultdict(int)
        for sequence in tool_sequences:
            # Generate subsequences of length 2-5
            for length in range(2, min(len(sequence) + 1, 6)):
                for i in range(len(sequence) - length + 1):
                    subseq = tuple(sequence[i:i+length])
                    sequence_counts[subseq] += 1

        # Create insights for frequent sequences
        for sequence, count in sequence_counts.items():
            if count >= self.min_pattern_occurrences:
                confidence = calculate_confidence(
                    pattern_frequency=count,
                    data_quality=0.8,  # Assuming good data quality
                    temporal_consistency=0.7,  # Medium consistency
                    user_feedback=0.5  # No feedback yet
                )

                if confidence.value >= self.pattern_confidence_threshold:
                    insight = create_insight(
                        insight_id=f"workflow_{uuid.uuid4().hex[:8]}",
                        title=f"Recurring Workflow: {' → '.join(sequence)}",
                        description=(
                            f"You've used this tool sequence {count} times. "
                            f"Consider creating an automated workflow."
                        ),
                        intelligence_type=IntelligenceType.PATTERN_DETECTION,
                        context=context,
                        confidence=confidence,
                        recommendations=[
                            f"Create automation for: {' → '.join(sequence)}",
                            "Consider workflow optimization",
                            "Set up triggers for this sequence"
                        ],
                        data={
                            'pattern_type': 'workflow_sequence',
                            'sequence': list(sequence),
                            'frequency': count,
                            'automation_potential': True
                        },
                        source_service=self.name
                    )
                    insights.append(insight)

        return insights

    async def _detect_temporal_patterns(
        self,
        context: IntelligenceContext
    ) -> List[IntelligenceInsight]:
        """Detect time-based patterns in user behavior"""
        insights = []
        user_interactions = self.interaction_history.get(context.user_id, [])

        if len(user_interactions) < self.min_pattern_occurrences:
            return insights

        # Analyze by hour of day
        hourly_usage = defaultdict(list)
        for interaction in user_interactions:
            timestamp = datetime.fromisoformat(interaction['timestamp'])
            hour = timestamp.hour
            hourly_usage[hour].append(interaction)

        # Find peak usage hours
        peak_hours = []
        avg_hourly_count = len(user_interactions) / 24

        for hour, interactions in hourly_usage.items():
            if len(interactions) > avg_hourly_count * 1.5:  # 50% above average
                peak_hours.append((hour, len(interactions)))

        if peak_hours:
            peak_hours.sort(key=lambda x: x[1], reverse=True)
            top_hour, count = peak_hours[0]

            confidence = calculate_confidence(
                pattern_frequency=min(count, 10),
                data_quality=0.9,
                temporal_consistency=0.8,
                user_feedback=0.5
            )

            if confidence.value >= self.pattern_confidence_threshold:
                insight = create_insight(
                    insight_id=f"temporal_{uuid.uuid4().hex[:8]}",
                    title=f"Peak Activity at {top_hour:02d}:00",
                    description=(
                        f"You're most active around {top_hour:02d}:00 "
                        f"({count} activities). Consider scheduling "
                        f"important tasks during this time."
                    ),
                    intelligence_type=IntelligenceType.PATTERN_DETECTION,
                    context=context,
                    confidence=confidence,
                    recommendations=[
                        f"Schedule key tasks around {top_hour:02d}:00",
                        "Set up automated reminders for peak hours",
                        "Batch similar activities during high-energy time"
                    ],
                    data={
                        'pattern_type': 'temporal_peak',
                        'peak_hour': top_hour,
                        'activity_count': count,
                        'peak_hours_all': peak_hours[:3]  # Top 3 hours
                    },
                    source_service=self.name
                )
                insights.append(insight)

        return insights

    async def _detect_efficiency_opportunities(
        self,
        context: IntelligenceContext
    ) -> List[IntelligenceInsight]:
        """Detect opportunities for workflow efficiency improvements"""
        insights = []
        user_interactions = self.interaction_history.get(context.user_id, [])

        if len(user_interactions) < self.min_pattern_occurrences:
            return insights

        # Analyze tool switching patterns
        tool_switches = []
        prev_tool = None

        sorted_interactions = sorted(
            user_interactions, key=lambda x: x['timestamp']
        )
        for interaction in sorted_interactions:
            current_tool = interaction.get('tool_name')
            if prev_tool and current_tool and prev_tool != current_tool:
                tool_switches.append((prev_tool, current_tool))
            prev_tool = current_tool

        # Find frequent tool switches that might indicate inefficiency
        switch_counts = defaultdict(int)
        for switch in tool_switches:
            switch_counts[switch] += 1

        for (from_tool, to_tool), count in switch_counts.items():
            if count >= self.min_pattern_occurrences:
                confidence = calculate_confidence(
                    pattern_frequency=count,
                    data_quality=0.7,
                    temporal_consistency=0.6,
                    user_feedback=0.5
                )

                if confidence.value >= self.pattern_confidence_threshold:
                    insight = create_insight(
                        insight_id=f"efficiency_{uuid.uuid4().hex[:8]}",
                        title=f"Frequent Tool Switch: {from_tool} → {to_tool}",
                        description=(
                            f"You switch from {from_tool} to {to_tool} "
                            f"{count} times. Consider integrating these tools "
                            f"or batching similar tasks."
                        ),
                        intelligence_type=IntelligenceType.PATTERN_DETECTION,
                        context=context,
                        confidence=confidence,
                        recommendations=[
                            f"Look for integration between {from_tool} "
                            f"and {to_tool}",
                            "Batch similar tasks to reduce context switching",
                            "Consider workflow tools that combine these "
                            "functions"
                        ],
                        data={
                            'pattern_type': 'tool_switching',
                            'from_tool': from_tool,
                            'to_tool': to_tool,
                            'switch_count': count,
                            'optimization_potential': True
                        },
                        source_service=self.name
                    )
                    insights.append(insight)

        return insights

    async def _analyze_sequential_patterns(
        self,
        interactions: List[Dict[str, Any]],
        context: IntelligenceContext
    ) -> List[IntelligenceInsight]:
        """Analyze sequential patterns in interactions"""
        # Implementation would use sophisticated sequence mining algorithms
        # For now, return empty list
        return []

    async def _analyze_tool_usage_patterns(
        self,
        interactions: List[Dict[str, Any]],
        context: IntelligenceContext
    ) -> List[IntelligenceInsight]:
        """Analyze tool usage patterns"""
        # Implementation would analyze tool usage frequency, combinations, etc.
        return []

    async def _analyze_data_flow_patterns(
        self,
        interactions: List[Dict[str, Any]],
        context: IntelligenceContext
    ) -> List[IntelligenceInsight]:
        """Analyze data flow patterns between tools"""
        # Implementation would track data transformations and flows
        return []

    async def _find_similar_sessions(
        self,
        current_session: Dict[str, Any],
        user_history: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Find historically similar sessions"""
        # Implementation would use similarity algorithms
        return []

    async def _generate_predictions(
        self,
        similar_sessions: List[Dict[str, Any]],
        context: IntelligenceContext
    ) -> List[IntelligenceInsight]:
        """Generate predictions based on similar sessions"""
        # Implementation would predict next likely actions
        return []
