"""
Productivity Intelligence Service

Analyzes workflow efficiency, task management patterns, and provides
productivity optimization recommendations across all productivity tools.

This service is OPTIONAL and productivity applications work perfectly
without it.
"""

import uuid
from collections import defaultdict
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

from ..shared.interfaces import (IntelligenceContext, IntelligenceInsight,
                                 IntelligenceRequest, IntelligenceType,
                                 ProductivityIntelligenceInterface)
from ..shared.utils import (calculate_confidence, create_insight,
                            default_cache, default_metrics, with_caching,
                            with_metrics, with_timeout)


class ProductivityIntelligenceService(ProductivityIntelligenceInterface):
    """
    Advanced productivity analysis service

    Analyzes workflow efficiency, identifies bottlenecks, and suggests
    optimizations to improve productivity across all tools.
    """

    def __init__(self, name: str = "productivity_intelligence"):
        self.name = name
        self.efficiency_thresholds = {
            'task_completion_rate': 0.8,  # 80% completion rate expected
            'context_switch_frequency': 5,  # Max 5 switches per hour
            'focus_session_duration': 25,  # Minimum 25 minutes focused work
            'workflow_automation_potential': 0.7  # 70% automation score
        }
        self.user_productivity_profiles = {}

    @with_timeout(timeout_seconds=15.0)
    @with_metrics(default_metrics, "productivity_intelligence")
    @with_caching(default_cache, "productivity_intelligence")
    async def analyze(
        self,
        request: IntelligenceRequest
    ) -> List[IntelligenceInsight]:
        """Analyze productivity aspects of user data"""
        context = request.context
        data = request.data

        insights = []

        # Update user productivity profile
        await self._update_productivity_profile(context.user_id, data)

        # Analyze workflow efficiency
        efficiency_insights = await self.analyze_efficiency([data], context)
        insights.extend(efficiency_insights)

        # Suggest optimizations
        optimization_insights = await self.suggest_optimizations(data, context)
        insights.extend(optimization_insights)

        # Analyze focus patterns
        focus_insights = await self._analyze_focus_patterns(data, context)
        insights.extend(focus_insights)

        return insights

    async def get_cached_insights(
        self,
        context: IntelligenceContext,
        intelligence_type: Optional[IntelligenceType] = None
    ) -> List[IntelligenceInsight]:
        """Get cached productivity insights"""
        return []

    async def health_check(self) -> Dict[str, Any]:
        """Check productivity intelligence service health"""
        return {
            "service": self.name,
            "status": "healthy",
            "metrics": {
                "users_tracked": len(self.user_productivity_profiles),
                "efficiency_thresholds": self.efficiency_thresholds,
                "analysis_categories": [
                    "workflow_efficiency",
                    "task_management",
                    "focus_patterns",
                    "automation_opportunities"
                ]
            },
            "timestamp": datetime.now().isoformat()
        }

    def get_service_info(self) -> Dict[str, Any]:
        """Get productivity intelligence service information"""
        return {
            "name": self.name,
            "type": IntelligenceType.PRODUCTIVITY_OPTIMIZATION.value,
            "description": "Productivity analysis and workflow optimization",
            "capabilities": [
                "workflow_efficiency_analysis",
                "task_completion_tracking",
                "focus_pattern_detection",
                "automation_opportunity_identification",
                "productivity_metric_calculation",
                "burnout_risk_assessment"
            ],
            "optimization_areas": [
                "task_management",
                "time_allocation",
                "tool_usage_efficiency",
                "workflow_automation",
                "focus_optimization",
                "work_life_balance"
            ]
        }

    async def analyze_efficiency(
        self,
        workflows: List[Dict[str, Any]],
        context: IntelligenceContext
    ) -> List[IntelligenceInsight]:
        """Analyze workflow efficiency"""
        insights = []

        if not workflows:
            return insights

        user_profile = self.user_productivity_profiles.get(
            context.user_id, {}
        )

        # Analyze task completion patterns
        completion_insights = await self._analyze_task_completion(
            workflows, context, user_profile
        )
        insights.extend(completion_insights)

        # Analyze time usage efficiency
        time_insights = await self._analyze_time_efficiency(
            workflows, context, user_profile
        )
        insights.extend(time_insights)

        # Analyze tool switching patterns
        switching_insights = await self._analyze_context_switching(
            workflows, context, user_profile
        )
        insights.extend(switching_insights)

        return insights

    async def suggest_optimizations(
        self,
        current_workflow: Dict[str, Any],
        context: IntelligenceContext
    ) -> List[IntelligenceInsight]:
        """Suggest workflow optimizations"""
        insights = []

        user_profile = self.user_productivity_profiles.get(
            context.user_id, {}
        )

        # Suggest automation opportunities
        automation_suggestions = await self._suggest_automation(
            current_workflow, context, user_profile
        )
        insights.extend(automation_suggestions)

        # Suggest focus improvements
        focus_suggestions = await self._suggest_focus_improvements(
            current_workflow, context, user_profile
        )
        insights.extend(focus_suggestions)

        # Suggest tool optimizations
        tool_suggestions = await self._suggest_tool_optimizations(
            current_workflow, context, user_profile
        )
        insights.extend(tool_suggestions)

        return insights

    async def _update_productivity_profile(
        self,
        user_id: str,
        data: Dict[str, Any]
    ) -> None:
        """Update user productivity profile with new data"""
        if user_id not in self.user_productivity_profiles:
            self.user_productivity_profiles[user_id] = {
                'total_tasks': 0,
                'completed_tasks': 0,
                'total_work_time': 0,
                'focus_sessions': [],
                'tool_usage': defaultdict(int),
                'productivity_trends': [],
                'last_updated': datetime.now()
            }

        profile = self.user_productivity_profiles[user_id]

        # Update task metrics
        if 'task_status' in data:
            profile['total_tasks'] += 1
            if data.get('task_status') == 'completed':
                profile['completed_tasks'] += 1

        # Update work time
        work_duration = data.get('work_duration_minutes', 0)
        profile['total_work_time'] += work_duration

        # Update focus sessions
        if work_duration >= self.efficiency_thresholds['focus_session_duration']:
            profile['focus_sessions'].append({
                'duration': work_duration,
                'timestamp': datetime.now().isoformat(),
                'tool': data.get('tool_name'),
                'domain': data.get('domain')
            })

            # Keep only recent focus sessions
            cutoff = datetime.now() - timedelta(days=30)
            profile['focus_sessions'] = [
                session for session in profile['focus_sessions']
                if datetime.fromisoformat(session['timestamp']) > cutoff
            ]

        # Update tool usage
        tool_name = data.get('tool_name')
        if tool_name:
            profile['tool_usage'][tool_name] += 1

        profile['last_updated'] = datetime.now()

    async def _analyze_task_completion(
        self,
        workflows: List[Dict[str, Any]],
        context: IntelligenceContext,
        user_profile: Dict[str, Any]
    ) -> List[IntelligenceInsight]:
        """Analyze task completion patterns"""
        insights = []

        if not user_profile or user_profile.get('total_tasks', 0) < 5:
            return insights

        completion_rate = (
            user_profile.get('completed_tasks', 0) /
            user_profile.get('total_tasks', 1)
        )

        threshold = self.efficiency_thresholds['task_completion_rate']

        if completion_rate < threshold:
            confidence = calculate_confidence(
                pattern_frequency=8,
                data_quality=0.8,
                temporal_consistency=0.7,
                user_feedback=0.5
            )

            insight = create_insight(
                insight_id=f"completion_{uuid.uuid4().hex[:8]}",
                title="Low Task Completion Rate",
                description=(
                    f"Your task completion rate is {completion_rate:.1%}, "
                    f"which is below the recommended {threshold:.0%}. "
                    f"Consider reviewing your task management approach."
                ),
                intelligence_type=IntelligenceType.PRODUCTIVITY_OPTIMIZATION,
                context=context,
                confidence=confidence,
                recommendations=[
                    "Break large tasks into smaller, manageable chunks",
                    "Set realistic deadlines and priorities",
                    "Review and eliminate task blockers",
                    "Consider time-boxing techniques (Pomodoro, etc.)",
                    "Delegate or eliminate low-priority tasks"
                ],
                data={
                    'completion_rate': completion_rate,
                    'total_tasks': user_profile.get('total_tasks'),
                    'completed_tasks': user_profile.get('completed_tasks'),
                    'improvement_needed': True
                },
                source_service=self.name
            )
            insights.append(insight)

        return insights

    async def _analyze_time_efficiency(
        self,
        workflows: List[Dict[str, Any]],
        context: IntelligenceContext,
        user_profile: Dict[str, Any]
    ) -> List[IntelligenceInsight]:
        """Analyze time usage efficiency"""
        insights = []

        focus_sessions = user_profile.get('focus_sessions', [])
        if len(focus_sessions) < 3:
            return insights

        # Calculate average focus session duration
        avg_focus_duration = sum(
            session['duration'] for session in focus_sessions
        ) / len(focus_sessions)

        min_threshold = self.efficiency_thresholds['focus_session_duration']

        if avg_focus_duration < min_threshold * 1.5:  # 37.5 minutes
            confidence = calculate_confidence(
                pattern_frequency=len(focus_sessions),
                data_quality=0.7,
                temporal_consistency=0.6,
                user_feedback=0.5
            )

            insight = create_insight(
                insight_id=f"focus_{uuid.uuid4().hex[:8]}",
                title="Short Focus Sessions Detected",
                description=(
                    f"Your average focus session is {avg_focus_duration:.1f} "
                    f"minutes. Longer focus periods could improve productivity."
                ),
                intelligence_type=IntelligenceType.PRODUCTIVITY_OPTIMIZATION,
                context=context,
                confidence=confidence,
                recommendations=[
                    "Try the Pomodoro technique (25 min work + 5 min break)",
                    "Eliminate distractions during work sessions",
                    "Use focus apps or website blockers",
                    "Schedule specific times for checking messages",
                    "Set up a dedicated workspace"
                ],
                data={
                    'avg_focus_duration': avg_focus_duration,
                    'focus_sessions_count': len(focus_sessions),
                    'recommended_minimum': min_threshold * 1.5
                },
                source_service=self.name
            )
            insights.append(insight)

        return insights

    async def _analyze_context_switching(
        self,
        workflows: List[Dict[str, Any]],
        context: IntelligenceContext,
        user_profile: Dict[str, Any]
    ) -> List[IntelligenceInsight]:
        """Analyze context switching patterns"""
        insights = []

        # Analyze tool switching frequency
        tool_usage = user_profile.get('tool_usage', {})
        if len(tool_usage) > self.efficiency_thresholds['context_switch_frequency']:
            confidence = calculate_confidence(
                pattern_frequency=len(tool_usage),
                data_quality=0.6,
                temporal_consistency=0.5,
                user_feedback=0.5
            )

            insight = create_insight(
                insight_id=f"switching_{uuid.uuid4().hex[:8]}",
                title="High Context Switching Detected",
                description=(
                    f"You're using {len(tool_usage)} different tools regularly, "
                    f"which may cause productivity loss due to context switching."
                ),
                intelligence_type=IntelligenceType.PRODUCTIVITY_OPTIMIZATION,
                context=context,
                confidence=confidence,
                recommendations=[
                    "Consolidate similar tools where possible",
                    "Batch similar tasks to reduce tool switching",
                    "Use integrated workflow platforms",
                    "Schedule specific times for different tool usage",
                    "Consider workflow automation tools"
                ],
                data={
                    'tools_count': len(tool_usage),
                    'most_used_tools': dict(
                        sorted(
                            tool_usage.items(),
                            key=lambda x: x[1],
                            reverse=True
                        )[:5]
                    ),
                    'optimization_potential': True
                },
                source_service=self.name
            )
            insights.append(insight)

        return insights

    async def _analyze_focus_patterns(
        self,
        data: Dict[str, Any],
        context: IntelligenceContext
    ) -> List[IntelligenceInsight]:
        """Analyze focus and attention patterns"""
        insights = []

        user_profile = self.user_productivity_profiles.get(
            context.user_id, {}
        )
        focus_sessions = user_profile.get('focus_sessions', [])

        if len(focus_sessions) >= 5:
            # Analyze focus session timing patterns
            session_hours = []
            for session in focus_sessions[-10:]:  # Last 10 sessions
                try:
                    dt = datetime.fromisoformat(session['timestamp'])
                    session_hours.append(dt.hour)
                except ValueError:
                    continue

            if session_hours:
                # Find most productive hours
                hour_counts = defaultdict(int)
                for hour in session_hours:
                    hour_counts[hour] += 1

                if hour_counts:
                    peak_hour = max(hour_counts.items(), key=lambda x: x[1])

                    confidence = calculate_confidence(
                        pattern_frequency=peak_hour[1],
                        data_quality=0.7,
                        temporal_consistency=0.8,
                        user_feedback=0.5
                    )

                    insight = create_insight(
                        insight_id=f"peak_focus_{uuid.uuid4().hex[:8]}",
                        title=f"Peak Focus Time: {peak_hour[0]:02d}:00",
                        description=(
                            f"You have {peak_hour[1]} focus sessions around "
                            f"{peak_hour[0]:02d}:00. This appears to be your "
                            f"most productive time."
                        ),
                        intelligence_type=IntelligenceType.PRODUCTIVITY_OPTIMIZATION,
                        context=context,
                        confidence=confidence,
                        recommendations=[
                            f"Schedule important tasks around {peak_hour[0]:02d}:00",
                            "Block calendar time during peak focus hours",
                            "Avoid meetings during high-productivity periods",
                            "Use this time for complex, creative work",
                            "Protect this time from interruptions"
                        ],
                        data={
                            'peak_hour': peak_hour[0],
                            'focus_sessions_at_peak': peak_hour[1],
                            'hour_distribution': dict(hour_counts)
                        },
                        source_service=self.name
                    )
                    insights.append(insight)

        return insights

    async def _suggest_automation(
        self,
        workflow: Dict[str, Any],
        context: IntelligenceContext,
        user_profile: Dict[str, Any]
    ) -> List[IntelligenceInsight]:
        """Suggest automation opportunities"""
        insights = []

        # Check for repetitive tasks
        tool_usage = user_profile.get('tool_usage', {})
        repetitive_tools = {
            tool: count for tool, count in tool_usage.items()
            if count >= 10  # Used at least 10 times
        }

        if repetitive_tools:
            confidence = calculate_confidence(
                pattern_frequency=max(repetitive_tools.values()),
                data_quality=0.7,
                temporal_consistency=0.6,
                user_feedback=0.5
            )

            top_tool = max(repetitive_tools.items(), key=lambda x: x[1])

            insight = create_insight(
                insight_id=f"automation_{uuid.uuid4().hex[:8]}",
                title=f"Automation Opportunity: {top_tool[0]}",
                description=(
                    f"You've used {top_tool[0]} {top_tool[1]} times. "
                    f"Consider automating repetitive workflows with this tool."
                ),
                intelligence_type=IntelligenceType.PRODUCTIVITY_OPTIMIZATION,
                context=context,
                confidence=confidence,
                recommendations=[
                    f"Set up automated workflows for {top_tool[0]}",
                    "Use scripting or workflow tools (n8n, Zapier)",
                    "Create templates for common tasks",
                    "Set up triggers and scheduled actions",
                    "Document your automation for team sharing"
                ],
                data={
                    'tool_name': top_tool[0],
                    'usage_count': top_tool[1],
                    'automation_potential_high': True,
                    'repetitive_tools': repetitive_tools
                },
                source_service=self.name
            )
            insights.append(insight)

        return insights

    async def _suggest_focus_improvements(
        self,
        workflow: Dict[str, Any],
        context: IntelligenceContext,
        user_profile: Dict[str, Any]
    ) -> List[IntelligenceInsight]:
        """Suggest focus and attention improvements"""
        # This would analyze interruption patterns, attention spans, etc.
        return []

    async def _suggest_tool_optimizations(
        self,
        workflow: Dict[str, Any],
        context: IntelligenceContext,
        user_profile: Dict[str, Any]
    ) -> List[IntelligenceInsight]:
        """Suggest tool usage optimizations"""
        # This would analyze tool efficiency, integration opportunities, etc.
        return []
