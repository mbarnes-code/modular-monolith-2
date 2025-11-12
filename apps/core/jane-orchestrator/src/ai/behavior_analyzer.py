"""AI Behavior Analysis for Cross-Tool Interaction Patterns."""

from typing import List, Dict, Any, Optional
from datetime import datetime
from dataclasses import dataclass
from enum import Enum
import numpy as np
from collections import defaultdict, Counter


class InteractionType(Enum):
    """Types of interactions between tools."""
    SEQUENTIAL = "sequential"
    PARALLEL = "parallel"
    CONDITIONAL = "conditional"
    LOOP = "loop"
    BRANCHING = "branching"


class AnalysisInsight(Enum):
    """Types of insights that can be discovered."""
    EFFICIENCY_OPPORTUNITY = "efficiency_opportunity"
    BOTTLENECK = "bottleneck"
    REDUNDANCY = "redundancy"
    MISSING_AUTOMATION = "missing_automation"
    OPTIMIZATION_POTENTIAL = "optimization_potential"


@dataclass
class CrossToolInteraction:
    """Represents an interaction between multiple tools."""
    interaction_id: str
    user_id: str
    timestamp: datetime
    tools_involved: List[str]
    interaction_type: InteractionType
    data_flow: Dict[str, Any]
    duration_seconds: int
    success_rate: float
    context: Dict[str, Any]


@dataclass
class BehaviorPattern:
    """Represents a discovered behavioral pattern."""
    pattern_id: str
    pattern_type: str
    frequency: int
    tools_involved: List[str]
    typical_duration: float
    success_rate: float
    context_conditions: List[str]
    insights: List[AnalysisInsight]
    confidence_score: float


@dataclass
class AIInsight:
    """Represents an AI-generated insight about user behavior."""
    insight_id: str
    insight_type: AnalysisInsight
    description: str
    affected_tools: List[str]
    potential_improvement: str
    estimated_impact: float
    confidence: float
    evidence: Dict[str, Any]
    recommendations: List[str]


class BehaviorAnalyzer:
    """AI-powered analysis of cross-tool interaction patterns."""
    
    def __init__(self, ai_client: Optional[Any] = None):
        self.ai_client = ai_client
        self.pattern_cache = {}
        self.analysis_history = []
        self.min_pattern_frequency = 3
        self.analysis_window_days = 30
    
    async def analyze_user_behavior(
        self, user_id: str, interactions: List[CrossToolInteraction]
    ) -> List[AIInsight]:
        """Perform comprehensive AI analysis of user behavior patterns."""
        if not interactions:
            return []
        
        # Analyze temporal patterns
        temporal_patterns = self._analyze_temporal_patterns(interactions)
        
        # Analyze tool dependencies
        dependency_patterns = self._analyze_tool_dependencies(interactions)
        
        # Analyze efficiency patterns
        efficiency_patterns = self._analyze_efficiency_patterns(interactions)
        
        # Generate insights
        insights = []
        
        for pattern_type, patterns in [
            ("temporal", temporal_patterns),
            ("dependency", dependency_patterns),
            ("efficiency", efficiency_patterns)
        ]:
            pattern_insights = await self._generate_insights_for_patterns(
                pattern_type, patterns, user_id
            )
            insights.extend(pattern_insights)
        
        return self._rank_insights_by_impact(insights)[:10]
    
    def _analyze_temporal_patterns(
        self, interactions: List[CrossToolInteraction]
    ) -> Dict[str, List[BehaviorPattern]]:
        """Analyze when and how users interact with tools over time."""
        temporal_patterns = {
            "daily_routines": [],
            "weekly_patterns": [],
            "session_patterns": []
        }
        
        # Group by daily usage
        daily_groups = self._group_by_time_period(interactions, "daily")
        
        for day, day_interactions in daily_groups.items():
            if len(day_interactions) >= self.min_pattern_frequency:
                pattern = self._extract_routine_pattern(
                    day_interactions, "daily"
                )
                if pattern:
                    temporal_patterns["daily_routines"].append(pattern)
        
        return temporal_patterns
    
    def _analyze_tool_dependencies(
        self, interactions: List[CrossToolInteraction]
    ) -> Dict[str, List[BehaviorPattern]]:
        """Analyze dependencies and relationships between tools."""
        dependency_patterns = {
            "sequential_dependencies": [],
            "tool_clusters": []
        }
        
        # Find sequential patterns
        sequential_patterns = self._find_sequential_patterns(interactions)
        dependency_patterns["sequential_dependencies"] = sequential_patterns
        
        # Find tool clusters
        cluster_patterns = self._find_tool_clusters(interactions)
        dependency_patterns["tool_clusters"] = cluster_patterns
        
        return dependency_patterns
    
    def _analyze_efficiency_patterns(
        self, interactions: List[CrossToolInteraction]
    ) -> Dict[str, List[BehaviorPattern]]:
        """Analyze efficiency and optimization opportunities."""
        efficiency_patterns = {
            "bottlenecks": [],
            "redundancies": []
        }
        
        # Find bottlenecks
        bottlenecks = self._find_bottleneck_patterns(interactions)
        efficiency_patterns["bottlenecks"] = bottlenecks
        
        # Find redundancies
        redundancies = self._find_redundancy_patterns(interactions)
        efficiency_patterns["redundancies"] = redundancies
        
        return efficiency_patterns
    
    def _group_by_time_period(
        self, interactions: List[CrossToolInteraction], period: str
    ) -> Dict[str, List[CrossToolInteraction]]:
        """Group interactions by time period."""
        groups = defaultdict(list)
        
        for interaction in interactions:
            if period == "daily":
                key = interaction.timestamp.strftime("%Y-%m-%d")
            else:
                key = interaction.timestamp.strftime("%Y-W%U")
            
            groups[key].append(interaction)
        
        return dict(groups)
    
    def _extract_routine_pattern(
        self, interactions: List[CrossToolInteraction], period_type: str
    ) -> Optional[BehaviorPattern]:
        """Extract routine patterns from time-grouped interactions."""
        if not interactions:
            return None
        
        # Analyze tools used
        tool_counts = Counter()
        total_duration = 0
        success_count = 0
        
        for interaction in interactions:
            for tool in interaction.tools_involved:
                tool_counts[tool] += 1
            total_duration += interaction.duration_seconds
            if interaction.success_rate > 0.8:
                success_count += 1
        
        most_common_tools = [tool for tool, _ in tool_counts.most_common(5)]
        avg_duration = total_duration / len(interactions)
        success_rate = success_count / len(interactions)
        
        # Determine insights
        insights = []
        if len(most_common_tools) > 3:
            insights.append(AnalysisInsight.OPTIMIZATION_POTENTIAL)
        if avg_duration > 300:  # More than 5 minutes average
            insights.append(AnalysisInsight.EFFICIENCY_OPPORTUNITY)
        
        return BehaviorPattern(
            pattern_id=f"{period_type}_routine_{hash(tuple(most_common_tools))}",
            pattern_type=f"{period_type}_routine",
            frequency=len(interactions),
            tools_involved=most_common_tools,
            typical_duration=avg_duration,
            success_rate=success_rate,
            context_conditions=[f"{period_type}_usage"],
            insights=insights,
            confidence_score=min(1.0, len(interactions) / 10.0)
        )
    
    def _find_sequential_patterns(
        self, interactions: List[CrossToolInteraction]
    ) -> List[BehaviorPattern]:
        """Find patterns of sequential tool usage."""
        sequential_patterns = []
        
        # Sort interactions by time
        sorted_interactions = sorted(interactions, key=lambda x: x.timestamp)
        
        # Group into sequences based on time gaps
        sequences = []
        current_sequence = []
        max_gap_minutes = 30
        
        for interaction in sorted_interactions:
            if current_sequence:
                time_gap = (
                    interaction.timestamp - current_sequence[-1].timestamp
                ).total_seconds()
                
                if time_gap > max_gap_minutes * 60:
                    if len(current_sequence) >= 2:
                        sequences.append(current_sequence)
                    current_sequence = [interaction]
                else:
                    current_sequence.append(interaction)
            else:
                current_sequence.append(interaction)
        
        if len(current_sequence) >= 2:
            sequences.append(current_sequence)
        
        # Analyze sequences for patterns
        sequence_patterns = defaultdict(list)
        for sequence in sequences:
            tool_names = []
            for interaction in sequence:
                tool_names.extend(interaction.tools_involved)
            
            pattern_key = " -> ".join(tool_names[:5])
            sequence_patterns[pattern_key].append(sequence)
        
        # Convert to BehaviorPattern objects
        for pattern_key, pattern_sequences in sequence_patterns.items():
            if len(pattern_sequences) >= self.min_pattern_frequency:
                avg_duration = np.mean([
                    sum(i.duration_seconds for i in seq)
                    for seq in pattern_sequences
                ])
                avg_success_rate = np.mean([
                    np.mean([i.success_rate for i in seq])
                    for seq in pattern_sequences
                ])
                
                tools_involved = list(set(
                    tool for seq in pattern_sequences
                    for interaction in seq
                    for tool in interaction.tools_involved
                ))
                
                sequential_patterns.append(BehaviorPattern(
                    pattern_id=f"sequential_{hash(pattern_key)}",
                    pattern_type="sequential_workflow",
                    frequency=len(pattern_sequences),
                    tools_involved=tools_involved,
                    typical_duration=avg_duration,
                    success_rate=avg_success_rate,
                    context_conditions=["sequential_tool_usage"],
                    insights=[AnalysisInsight.MISSING_AUTOMATION],
                    confidence_score=min(1.0, len(pattern_sequences) / 5.0)
                ))
        
        return sequential_patterns
    
    def _find_tool_clusters(
        self, interactions: List[CrossToolInteraction]
    ) -> List[BehaviorPattern]:
        """Find clusters of tools that are frequently used together."""
        tool_pairs = Counter()
        
        for interaction in interactions:
            tools = interaction.tools_involved
            if len(tools) > 1:
                for i in range(len(tools)):
                    for j in range(i + 1, len(tools)):
                        pair = tuple(sorted([tools[i], tools[j]]))
                        tool_pairs[pair] += 1
        
        clusters = []
        min_co_occurrence = 3
        
        for (tool1, tool2), count in tool_pairs.items():
            if count >= min_co_occurrence:
                cluster_interactions = [
                    interaction for interaction in interactions
                    if (tool1 in interaction.tools_involved and
                        tool2 in interaction.tools_involved)
                ]
                
                avg_duration = np.mean([
                    i.duration_seconds for i in cluster_interactions
                ])
                avg_success_rate = np.mean([
                    i.success_rate for i in cluster_interactions
                ])
                
                clusters.append(BehaviorPattern(
                    pattern_id=f"cluster_{hash((tool1, tool2))}",
                    pattern_type="tool_cluster",
                    frequency=count,
                    tools_involved=[tool1, tool2],
                    typical_duration=avg_duration,
                    success_rate=avg_success_rate,
                    context_conditions=["simultaneous_usage"],
                    insights=[AnalysisInsight.OPTIMIZATION_POTENTIAL],
                    confidence_score=min(1.0, count / 10.0)
                ))
        
        return clusters
    
    def _find_bottleneck_patterns(
        self, interactions: List[CrossToolInteraction]
    ) -> List[BehaviorPattern]:
        """Find bottleneck patterns where tools take unusually long."""
        tool_durations = defaultdict(list)
        
        for interaction in interactions:
            for tool in interaction.tools_involved:
                tool_durations[tool].append(interaction.duration_seconds)
        
        bottlenecks = []
        overall_durations = [
            d for durations_list in tool_durations.values()
            for d in durations_list
        ]
        overall_mean = np.mean(overall_durations) if overall_durations else 0
        overall_std = np.std(overall_durations) if overall_durations else 0
        
        for tool, durations in tool_durations.items():
            if len(durations) >= 3:
                mean_duration = np.mean(durations)
                
                # Identify bottleneck if significantly above average
                if mean_duration > overall_mean + 2 * overall_std:
                    bottlenecks.append(BehaviorPattern(
                        pattern_id=f"bottleneck_{tool}",
                        pattern_type="bottleneck",
                        frequency=len(durations),
                        tools_involved=[tool],
                        typical_duration=mean_duration,
                        success_rate=1.0,
                        context_conditions=["slow_performance"],
                        insights=[AnalysisInsight.BOTTLENECK],
                        confidence_score=min(1.0, len(durations) / 10.0)
                    ))
        
        return bottlenecks
    
    def _find_redundancy_patterns(
        self, interactions: List[CrossToolInteraction]
    ) -> List[BehaviorPattern]:
        """Find patterns of redundant or repetitive actions."""
        similar_groups = defaultdict(list)
        
        for interaction in interactions:
            similarity_key = (
                tuple(sorted(interaction.tools_involved)),
                interaction.interaction_type
            )
            similar_groups[similarity_key].append(interaction)
        
        redundancy_patterns = []
        for similarity_key, similar_interactions in similar_groups.items():
            if len(similar_interactions) >= 5:  # High repetition threshold
                avg_duration = np.mean([
                    i.duration_seconds for i in similar_interactions
                ])
                avg_success_rate = np.mean([
                    i.success_rate for i in similar_interactions
                ])
                
                redundancy_patterns.append(BehaviorPattern(
                    pattern_id=f"redundancy_{hash(similarity_key)}",
                    pattern_type="redundancy",
                    frequency=len(similar_interactions),
                    tools_involved=list(similarity_key[0]),
                    typical_duration=avg_duration,
                    success_rate=avg_success_rate,
                    context_conditions=["repetitive_actions"],
                    insights=[AnalysisInsight.REDUNDANCY],
                    confidence_score=min(1.0, len(similar_interactions) / 10.0)
                ))
        
        return redundancy_patterns
    
    async def _generate_insights_for_patterns(
        self, pattern_type: str, patterns: Dict[str, List[BehaviorPattern]],
        user_id: str
    ) -> List[AIInsight]:
        """Generate AI insights for discovered patterns."""
        insights = []
        
        for pattern_subtype, pattern_list in patterns.items():
            for pattern in pattern_list:
                insight = await self._generate_single_insight(
                    pattern, pattern_type, pattern_subtype, user_id
                )
                if insight:
                    insights.append(insight)
        
        return insights
    
    async def _generate_single_insight(
        self, pattern: BehaviorPattern, pattern_type: str,
        pattern_subtype: str, user_id: str
    ) -> Optional[AIInsight]:
        """Generate a single AI insight for a behavior pattern."""
        insight_templates = {
            ("temporal", "daily_routines"): {
                "description": (
                    f"Daily routine with {len(pattern.tools_involved)} tools, "
                    f"{pattern.frequency} occurrences"
                ),
                "improvement": "Create automated workflow for this routine",
                "impact": pattern.frequency * 60
            },
            ("dependency", "sequential_dependencies"): {
                "description": (
                    f"Sequential workflow across {len(pattern.tools_involved)} tools"
                ),
                "improvement": "Automate this sequential workflow with n8n",
                "impact": pattern.typical_duration * 0.7
            },
            ("efficiency", "bottlenecks"): {
                "description": (
                    f"Performance bottleneck in {pattern.tools_involved[0]}"
                ),
                "improvement": "Optimize tool configuration or find alternatives",
                "impact": pattern.typical_duration * 0.5
            }
        }
        
        template_key = (pattern_type, pattern_subtype)
        template = insight_templates.get(template_key)
        
        if not template:
            return None
        
        # Generate recommendations
        recommendations = []
        for insight_type in pattern.insights:
            if insight_type == AnalysisInsight.MISSING_AUTOMATION:
                recommendations.append("Create automated workflow")
            elif insight_type == AnalysisInsight.BOTTLENECK:
                recommendations.append("Investigate performance issues")
            elif insight_type == AnalysisInsight.REDUNDANCY:
                recommendations.append("Eliminate redundant steps")
            elif insight_type == AnalysisInsight.OPTIMIZATION_POTENTIAL:
                recommendations.append("Review and optimize process")
        
        primary_insight = (
            pattern.insights[0] if pattern.insights
            else AnalysisInsight.OPTIMIZATION_POTENTIAL
        )
        
        return AIInsight(
            insight_id=f"insight_{pattern.pattern_id}",
            insight_type=primary_insight,
            description=template["description"],
            affected_tools=pattern.tools_involved,
            potential_improvement=template["improvement"],
            estimated_impact=template["impact"],
            confidence=pattern.confidence_score,
            evidence={
                "pattern_frequency": pattern.frequency,
                "typical_duration": pattern.typical_duration,
                "success_rate": pattern.success_rate,
                "context_conditions": pattern.context_conditions
            },
            recommendations=recommendations
        )
    
    def _rank_insights_by_impact(self, insights: List[AIInsight]) -> List[AIInsight]:
        """Rank insights by potential impact and confidence."""
        def impact_score(insight: AIInsight) -> float:
            return insight.estimated_impact * insight.confidence
        
        return sorted(insights, key=impact_score, reverse=True)
    
    def get_behavior_summary(
        self, user_id: str, insights: List[AIInsight]
    ) -> Dict[str, Any]:
        """Generate a summary of user behavior analysis."""
        if not insights:
            return {
                "status": "no_insights",
                "summary": "No behavioral patterns found"
            }
        
        # Categorize insights
        insight_categories = defaultdict(list)
        total_impact = 0
        
        for insight in insights:
            insight_categories[insight.insight_type.value].append(insight)
            total_impact += insight.estimated_impact
        
        # Find most impactful tools
        tool_impact = defaultdict(float)
        for insight in insights:
            for tool in insight.affected_tools:
                tool_impact[tool] += insight.estimated_impact
        
        top_tools = sorted(
            tool_impact.items(), key=lambda x: x[1], reverse=True
        )[:5]
        
        return {
            "status": "analysis_complete",
            "total_insights": len(insights),
            "total_estimated_impact": total_impact,
            "insight_categories": dict(insight_categories),
            "top_impactful_tools": top_tools,
            "summary": (
                f"Found {len(insights)} optimization opportunities "
                f"with estimated {total_impact:.0f}s time savings"
            ),
            "recommendations": [
                insight.recommendations[0] for insight in insights[:3]
                if insight.recommendations
            ]
        }