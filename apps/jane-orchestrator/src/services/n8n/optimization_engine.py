"""Workflow Optimization Recommendations Engine for n8n Automation.

This module provides comprehensive workflow improvement suggestions based on
performance analysis, best practices, and optimization opportunities across
all aspects of n8n workflow automation.
"""

import statistics
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple


class OptimizationType(Enum):
    """Types of optimizations that can be recommended."""
    PERFORMANCE = "performance"  # Speed and efficiency improvements
    RELIABILITY = "reliability"  # Error handling and resilience
    RESOURCE = "resource"  # CPU, memory, storage optimization
    MAINTAINABILITY = "maintainability"  # Code quality and structure
    SCALABILITY = "scalability"  # Handling increased load
    COST = "cost"  # Reducing operational costs
    SECURITY = "security"  # Security enhancements
    USER_EXPERIENCE = "user_experience"  # UX improvements
    DATA_QUALITY = "data_quality"  # Data validation and integrity
    MONITORING = "monitoring"  # Observability and alerting


class OptimizationPriority(Enum):
    """Priority levels for optimization recommendations."""
    CRITICAL = "critical"  # Must fix immediately
    HIGH = "high"  # Should fix soon
    MEDIUM = "medium"  # Moderate importance
    LOW = "low"  # Nice to have
    INFORMATIONAL = "informational"  # For awareness


class OptimizationComplexity(Enum):
    """Implementation complexity for optimizations."""
    TRIVIAL = "trivial"  # < 1 hour
    SIMPLE = "simple"  # 1-4 hours
    MODERATE = "moderate"  # 1-3 days
    COMPLEX = "complex"  # 1-2 weeks
    MAJOR = "major"  # > 2 weeks


@dataclass
class OptimizationRecommendation:
    """Represents a single optimization recommendation."""
    recommendation_id: str
    title: str
    description: str
    optimization_type: OptimizationType
    priority: OptimizationPriority
    complexity: OptimizationComplexity
    impact_score: float  # 0.0 to 1.0
    confidence: float  # 0.0 to 1.0
    estimated_savings: Dict[str, Any]  # Time, cost, resource savings
    implementation_steps: List[str]
    before_state: Dict[str, Any]  # Current state description
    after_state: Dict[str, Any]  # Expected state after optimization
    metrics_to_track: List[str]  # KPIs to monitor improvement
    risks: List[str]  # Potential risks of implementation
    dependencies: List[str]  # Other recommendations this depends on


@dataclass
class WorkflowMetrics:
    """Performance and quality metrics for a workflow."""
    workflow_id: str
    execution_count: int
    success_rate: float
    avg_execution_time_ms: float
    median_execution_time_ms: float
    p95_execution_time_ms: float
    error_rate: float
    retry_rate: float
    resource_usage: Dict[str, float]  # CPU, memory, network usage
    data_volume_processed: int
    cost_per_execution: float
    user_satisfaction_score: float  # 0.0 to 1.0
    last_updated: datetime


@dataclass
class OptimizationContext:
    """Context information for optimization analysis."""
    user_id: str
    workflow_count: int
    total_executions: int
    average_workflow_complexity: float
    primary_use_cases: List[str]
    tools_used: Set[str]
    business_requirements: Dict[str, Any]
    performance_targets: Dict[str, float]
    budget_constraints: Dict[str, float]
    technical_constraints: List[str]


class OptimizationEngine:
    """Comprehensive workflow optimization recommendations engine."""

    def __init__(self):
        self.workflow_metrics = {}
        self.optimization_rules = self._initialize_optimization_rules()
        self.best_practices = self._initialize_best_practices()
        self.performance_benchmarks = self._initialize_benchmarks()
        self.cost_models = self._initialize_cost_models()

    def _initialize_optimization_rules(self) -> Dict[str, Dict[str, Any]]:
        """Initialize optimization rules and thresholds."""
        return {
            'performance': {
                'slow_execution_threshold_ms': 10000,  # 10 seconds
                'high_p95_threshold_ms': 30000,  # 30 seconds
                'memory_usage_threshold_mb': 512,
                'cpu_usage_threshold_percent': 80,
                'network_timeout_threshold_ms': 5000
            },
            'reliability': {
                'min_success_rate': 0.95,  # 95%
                'max_error_rate': 0.05,  # 5%
                'max_retry_rate': 0.10,  # 10%
                'min_uptime_sla': 0.999  # 99.9%
            },
            'resource': {
                'max_memory_per_workflow_mb': 1024,
                'max_cpu_per_workflow_percent': 50,
                'max_storage_per_workflow_gb': 10,
                'max_concurrent_executions': 100
            },
            'cost': {
                'max_cost_per_execution': 0.10,  # $0.10
                'max_monthly_cost_per_workflow': 50.0,  # $50
                'cost_efficiency_threshold': 0.80  # 80% efficiency
            },
            'scalability': {
                'max_workflow_complexity_score': 0.8,
                'min_parallel_processing_ratio': 0.3,
                'max_sequential_dependencies': 10
            }
        }

    def _initialize_best_practices(self) -> Dict[str, List[Dict[str, Any]]]:
        """Initialize best practice recommendations."""
        return {
            'error_handling': [
                {
                    'practice': 'Add error handling nodes',
                    'description': 'Include error handling for all external API calls',
                    'benefit': 'Improved reliability and user experience'
                },
                {
                    'practice': 'Implement retry logic',
                    'description': 'Add retry mechanisms for transient failures',
                    'benefit': 'Higher success rates and resilience'
                }
            ],
            'data_validation': [
                {
                    'practice': 'Validate input data',
                    'description': 'Check data formats and required fields',
                    'benefit': 'Prevent downstream errors and data corruption'
                },
                {
                    'practice': 'Sanitize outputs',
                    'description': 'Clean and format output data consistently',
                    'benefit': 'Improved data quality and reliability'
                }
            ],
            'monitoring': [
                {
                    'practice': 'Add logging nodes',
                    'description': 'Log important workflow events and decisions',
                    'benefit': 'Better debugging and audit trails'
                },
                {
                    'practice': 'Set up alerts',
                    'description': 'Configure alerts for failures and anomalies',
                    'benefit': 'Faster incident response and resolution'
                }
            ],
            'performance': [
                {
                    'practice': 'Use parallel execution',
                    'description': 'Execute independent tasks in parallel',
                    'benefit': 'Reduced execution time and better resource utilization'
                },
                {
                    'practice': 'Implement caching',
                    'description': 'Cache frequently accessed data and API responses',
                    'benefit': 'Faster execution and reduced API costs'
                }
            ]
        }

    def _initialize_benchmarks(self) -> Dict[str, Dict[str, float]]:
        """Initialize performance benchmarks."""
        return {
            'execution_time': {
                'excellent': 1000,  # < 1 second
                'good': 5000,      # < 5 seconds
                'acceptable': 15000,  # < 15 seconds
                'poor': 30000      # > 30 seconds
            },
            'success_rate': {
                'excellent': 0.99,   # > 99%
                'good': 0.95,        # > 95%
                'acceptable': 0.90,  # > 90%
                'poor': 0.85         # < 85%
            },
            'resource_efficiency': {
                'excellent': 0.9,    # > 90%
                'good': 0.8,         # > 80%
                'acceptable': 0.7,   # > 70%
                'poor': 0.6          # < 60%
            }
        }

    def _initialize_cost_models(self) -> Dict[str, Dict[str, float]]:
        """Initialize cost models for different resources."""
        return {
            'compute': {
                'cpu_hour_cost': 0.10,        # $0.10 per CPU hour
                'memory_gb_hour_cost': 0.02,  # $0.02 per GB hour
                'storage_gb_month_cost': 0.05  # $0.05 per GB month
            },
            'api_calls': {
                'internal_call_cost': 0.0001,  # $0.0001 per call
                'external_call_cost': 0.01,   # $0.01 per call
                'premium_api_cost': 0.10      # $0.10 per call
            },
            'data_transfer': {
                'internal_transfer_gb_cost': 0.0,  # Free
                'external_transfer_gb_cost': 0.05  # $0.05 per GB
            }
        }

    def record_workflow_metrics(
        self,
        workflow_id: str,
        execution_time_ms: float,
        success: bool,
        error_details: Optional[Dict[str, Any]] = None,
        resource_usage: Optional[Dict[str, float]] = None,
        data_volume: int = 0,
        cost: float = 0.0,
        user_feedback: Optional[float] = None
    ) -> None:
        """Record workflow execution metrics for analysis."""

        if workflow_id not in self.workflow_metrics:
            self.workflow_metrics[workflow_id] = WorkflowMetrics(
                workflow_id=workflow_id,
                execution_count=0,
                success_rate=0.0,
                avg_execution_time_ms=0.0,
                median_execution_time_ms=0.0,
                p95_execution_time_ms=0.0,
                error_rate=0.0,
                retry_rate=0.0,
                resource_usage={},
                data_volume_processed=0,
                cost_per_execution=0.0,
                user_satisfaction_score=0.0,
                last_updated=datetime.utcnow()
            )

        metrics = self.workflow_metrics[workflow_id]

        # Update execution metrics
        metrics.execution_count += 1

        # Update success rate
        prev_successes = metrics.success_rate * (metrics.execution_count - 1)
        new_successes = prev_successes + (1 if success else 0)
        metrics.success_rate = new_successes / metrics.execution_count

        # Update execution time metrics
        if not hasattr(metrics, '_execution_times'):
            metrics._execution_times = []
        metrics._execution_times.append(execution_time_ms)

        # Keep only recent execution times (last 1000)
        if len(metrics._execution_times) > 1000:
            metrics._execution_times = metrics._execution_times[-1000:]

        metrics.avg_execution_time_ms = statistics.mean(
            metrics._execution_times)
        metrics.median_execution_time_ms = statistics.median(
            metrics._execution_times)
        if len(metrics._execution_times) >= 20:
            metrics.p95_execution_time_ms = statistics.quantiles(
                metrics._execution_times, n=20
            )[18]  # 95th percentile

        # Update error rate
        if not success:
            prev_errors = metrics.error_rate * (metrics.execution_count - 1)
            metrics.error_rate = (prev_errors + 1) / metrics.execution_count

        # Update resource usage
        if resource_usage:
            for resource, usage in resource_usage.items():
                if resource not in metrics.resource_usage:
                    metrics.resource_usage[resource] = 0.0
                # Running average
                prev_avg = metrics.resource_usage[resource]
                metrics.resource_usage[resource] = (
                    (prev_avg * (metrics.execution_count - 1) + usage) /
                    metrics.execution_count
                )

        # Update other metrics
        metrics.data_volume_processed += data_volume
        if cost > 0:
            prev_cost_total = metrics.cost_per_execution * \
                (metrics.execution_count - 1)
            metrics.cost_per_execution = (
                prev_cost_total + cost) / metrics.execution_count

        if user_feedback is not None:
            if metrics.user_satisfaction_score == 0.0:
                metrics.user_satisfaction_score = user_feedback
            else:
                # Running average of user feedback
                metrics.user_satisfaction_score = (
                    (metrics.user_satisfaction_score * 0.8) + (user_feedback * 0.2)
                )

        metrics.last_updated = datetime.utcnow()

    def analyze_workflow_performance(
        self, workflow_id: str
    ) -> Dict[str, Any]:
        """Analyze performance metrics for a specific workflow."""

        if workflow_id not in self.workflow_metrics:
            return {'error': 'No metrics available for workflow'}

        metrics = self.workflow_metrics[workflow_id]

        # Performance scoring
        perf_scores = {}
        benchmarks = self.performance_benchmarks

        # Execution time score
        avg_time = metrics.avg_execution_time_ms
        if avg_time <= benchmarks['execution_time']['excellent']:
            perf_scores['execution_time'] = 'excellent'
        elif avg_time <= benchmarks['execution_time']['good']:
            perf_scores['execution_time'] = 'good'
        elif avg_time <= benchmarks['execution_time']['acceptable']:
            perf_scores['execution_time'] = 'acceptable'
        else:
            perf_scores['execution_time'] = 'poor'

        # Success rate score
        success_rate = metrics.success_rate
        if success_rate >= benchmarks['success_rate']['excellent']:
            perf_scores['success_rate'] = 'excellent'
        elif success_rate >= benchmarks['success_rate']['good']:
            perf_scores['success_rate'] = 'good'
        elif success_rate >= benchmarks['success_rate']['acceptable']:
            perf_scores['success_rate'] = 'acceptable'
        else:
            perf_scores['success_rate'] = 'poor'

        # Resource efficiency score
        cpu_usage = metrics.resource_usage.get('cpu_percent', 0)
        memory_usage = metrics.resource_usage.get('memory_mb', 0)
        efficiency = 1.0 - min(cpu_usage / 100.0, 1.0) * \
            0.5 - min(memory_usage / 1024.0, 1.0) * 0.5

        if efficiency >= benchmarks['resource_efficiency']['excellent']:
            perf_scores['resource_efficiency'] = 'excellent'
        elif efficiency >= benchmarks['resource_efficiency']['good']:
            perf_scores['resource_efficiency'] = 'good'
        elif efficiency >= benchmarks['resource_efficiency']['acceptable']:
            perf_scores['resource_efficiency'] = 'acceptable'
        else:
            perf_scores['resource_efficiency'] = 'poor'

        return {
            'workflow_id': workflow_id,
            'performance_scores': perf_scores,
            'metrics_summary': {
                'execution_count': metrics.execution_count,
                'success_rate': metrics.success_rate,
                'avg_execution_time_ms': metrics.avg_execution_time_ms,
                'p95_execution_time_ms': metrics.p95_execution_time_ms,
                'error_rate': metrics.error_rate,
                'cost_per_execution': metrics.cost_per_execution,
                'user_satisfaction': metrics.user_satisfaction_score
            },
            'trends': self._analyze_performance_trends(workflow_id),
            'bottlenecks': self._identify_bottlenecks(workflow_id)
        }

    def generate_optimization_recommendations(
        self,
        workflow_id: str,
        context: Optional[OptimizationContext] = None
    ) -> List[OptimizationRecommendation]:
        """Generate comprehensive optimization recommendations."""

        if workflow_id not in self.workflow_metrics:
            return []

        recommendations = []
        metrics = self.workflow_metrics[workflow_id]

        # Performance optimizations
        recommendations.extend(
            self._generate_performance_recommendations(metrics))

        # Reliability optimizations
        recommendations.extend(
            self._generate_reliability_recommendations(metrics))

        # Resource optimizations
        recommendations.extend(
            self._generate_resource_recommendations(metrics))

        # Cost optimizations
        recommendations.extend(self._generate_cost_recommendations(metrics))

        # Scalability optimizations
        recommendations.extend(
            self._generate_scalability_recommendations(metrics))

        # Security optimizations
        recommendations.extend(
            self._generate_security_recommendations(metrics))

        # Maintainability optimizations
        recommendations.extend(
            self._generate_maintainability_recommendations(metrics))

        # Filter and prioritize recommendations
        recommendations = self._prioritize_recommendations(
            recommendations, context)

        return recommendations

    def generate_comparative_analysis(
        self, workflow_ids: List[str]
    ) -> Dict[str, Any]:
        """Generate comparative analysis across multiple workflows."""

        if not workflow_ids:
            return {}

        # Filter workflows with available metrics
        available_workflows = [
            wf_id for wf_id in workflow_ids
            if wf_id in self.workflow_metrics
        ]

        if not available_workflows:
            return {'error': 'No metrics available for specified workflows'}

        # Collect metrics for comparison
        comparison_data = {}
        for wf_id in available_workflows:
            metrics = self.workflow_metrics[wf_id]
            comparison_data[wf_id] = {
                'success_rate': metrics.success_rate,
                'avg_execution_time': metrics.avg_execution_time_ms,
                'cost_per_execution': metrics.cost_per_execution,
                'user_satisfaction': metrics.user_satisfaction_score,
                'execution_count': metrics.execution_count
            }

        # Find best and worst performers
        best_performers = {}
        worst_performers = {}

        for metric in ['success_rate', 'user_satisfaction']:
            best_performers[metric] = max(
                comparison_data.items(),
                key=lambda x: x[1][metric]
            )
            worst_performers[metric] = min(
                comparison_data.items(),
                key=lambda x: x[1][metric]
            )

        for metric in ['avg_execution_time', 'cost_per_execution']:
            best_performers[metric] = min(
                comparison_data.items(),
                key=lambda x: x[1][metric]
            )
            worst_performers[metric] = max(
                comparison_data.items(),
                key=lambda x: x[1][metric]
            )

        # Calculate averages
        averages = {}
        for metric in ['success_rate', 'avg_execution_time', 'cost_per_execution', 'user_satisfaction']:
            values = [data[metric] for data in comparison_data.values()]
            averages[metric] = sum(values) / len(values)

        return {
            'workflows_analyzed': len(available_workflows),
            'comparison_data': comparison_data,
            'best_performers': best_performers,
            'worst_performers': worst_performers,
            'averages': averages,
            'improvement_opportunities': self._identify_improvement_opportunities(
                comparison_data
            )
        }

    def suggest_workflow_consolidation(
        self, workflow_ids: List[str]
    ) -> List[Dict[str, Any]]:
        """Suggest opportunities to consolidate similar workflows."""

        consolidation_opportunities = []

        # Group workflows by similarity (simplified logic)
        workflow_groups = self._group_similar_workflows(workflow_ids)

        for group in workflow_groups:
            if len(group) >= 2:  # At least 2 workflows to consolidate
                # Calculate potential savings
                total_executions = sum(
                    self.workflow_metrics[wf_id].execution_count
                    for wf_id in group
                    if wf_id in self.workflow_metrics
                )

                avg_cost = sum(
                    self.workflow_metrics[wf_id].cost_per_execution
                    for wf_id in group
                    if wf_id in self.workflow_metrics
                ) / len(group)

                potential_savings = avg_cost * total_executions * 0.3  # 30% savings estimate

                consolidation_opportunities.append({
                    'workflow_group': group,
                    'consolidation_type': 'merge_similar_workflows',
                    'potential_monthly_savings': potential_savings,
                    'implementation_effort': 'moderate',
                    'risk_level': 'low',
                    'description': f'Consolidate {len(group)} similar workflows into a single optimized workflow'
                })

        return consolidation_opportunities

    def generate_capacity_planning_recommendations(
        self, workflow_ids: List[str], growth_projection: float = 1.5
    ) -> Dict[str, Any]:
        """Generate capacity planning recommendations."""

        current_capacity = {}
        projected_capacity = {}

        for wf_id in workflow_ids:
            if wf_id not in self.workflow_metrics:
                continue

            metrics = self.workflow_metrics[wf_id]

            # Current resource usage
            current_cpu = metrics.resource_usage.get('cpu_percent', 0)
            current_memory = metrics.resource_usage.get('memory_mb', 0)
            current_executions = metrics.execution_count

            # Projected usage
            projected_cpu = current_cpu * growth_projection
            projected_memory = current_memory * growth_projection
            projected_executions = current_executions * growth_projection

            current_capacity[wf_id] = {
                'cpu_percent': current_cpu,
                'memory_mb': current_memory,
                'executions_per_month': current_executions
            }

            projected_capacity[wf_id] = {
                'cpu_percent': projected_cpu,
                'memory_mb': projected_memory,
                'executions_per_month': projected_executions
            }

        # Identify capacity constraints
        constraints = []
        for wf_id, projected in projected_capacity.items():
            if projected['cpu_percent'] > 80:
                constraints.append({
                    'workflow_id': wf_id,
                    'resource': 'cpu',
                    'current_usage': current_capacity[wf_id]['cpu_percent'],
                    'projected_usage': projected['cpu_percent'],
                    'recommendation': 'Scale up CPU resources or optimize CPU usage'
                })

            if projected['memory_mb'] > 1024:
                constraints.append({
                    'workflow_id': wf_id,
                    'resource': 'memory',
                    'current_usage': current_capacity[wf_id]['memory_mb'],
                    'projected_usage': projected['memory_mb'],
                    'recommendation': 'Scale up memory or optimize memory usage'
                })

        return {
            'growth_projection_factor': growth_projection,
            'current_capacity': current_capacity,
            'projected_capacity': projected_capacity,
            'capacity_constraints': constraints,
            'scaling_recommendations': self._generate_scaling_recommendations(constraints)
        }

    # Private helper methods for generating recommendations

    def _generate_performance_recommendations(
        self, metrics: WorkflowMetrics
    ) -> List[OptimizationRecommendation]:
        """Generate performance optimization recommendations."""

        recommendations = []
        rules = self.optimization_rules['performance']

        # Slow execution recommendation
        if metrics.avg_execution_time_ms > rules['slow_execution_threshold_ms']:
            time_savings = metrics.avg_execution_time_ms - \
                rules['slow_execution_threshold_ms']

            recommendations.append(OptimizationRecommendation(
                recommendation_id=f"perf_slow_{metrics.workflow_id}",
                title="Optimize slow workflow execution",
                description=f"Workflow execution time ({metrics.avg_execution_time_ms:.0f}ms) exceeds recommended threshold ({rules['slow_execution_threshold_ms']}ms)",
                optimization_type=OptimizationType.PERFORMANCE,
                priority=OptimizationPriority.HIGH,
                complexity=OptimizationComplexity.MODERATE,
                impact_score=min(
                    time_savings / rules['slow_execution_threshold_ms'], 1.0),
                confidence=0.8,
                estimated_savings={
                    'time_per_execution_ms': time_savings,
                    'monthly_time_savings_hours': (time_savings * metrics.execution_count) / (1000 * 60 * 60)
                },
                implementation_steps=[
                    "Profile workflow execution to identify bottlenecks",
                    "Optimize slow database queries or API calls",
                    "Implement parallel processing where possible",
                    "Add caching for frequently accessed data",
                    "Consider asynchronous processing for non-critical tasks"
                ],
                before_state={
                    'avg_execution_time_ms': metrics.avg_execution_time_ms},
                after_state={
                    'target_execution_time_ms': rules['slow_execution_threshold_ms']},
                metrics_to_track=['avg_execution_time_ms',
                                  'p95_execution_time_ms'],
                risks=['Potential complexity increase',
                       'Need for thorough testing'],
                dependencies=[]
            ))

        # High P95 latency recommendation
        if metrics.p95_execution_time_ms > rules['high_p95_threshold_ms']:
            recommendations.append(OptimizationRecommendation(
                recommendation_id=f"perf_p95_{metrics.workflow_id}",
                title="Reduce P95 execution latency",
                description=f"95th percentile execution time ({metrics.p95_execution_time_ms:.0f}ms) indicates performance inconsistency",
                optimization_type=OptimizationType.PERFORMANCE,
                priority=OptimizationPriority.MEDIUM,
                complexity=OptimizationComplexity.MODERATE,
                impact_score=0.6,
                confidence=0.7,
                estimated_savings={
                    'improved_user_experience': 'Reduced latency variance',
                    'better_sla_compliance': '95% of executions under target time'
                },
                implementation_steps=[
                    "Identify outlier executions causing high P95",
                    "Add timeout controls for external API calls",
                    "Implement circuit breakers for unreliable dependencies",
                    "Optimize resource allocation during peak loads"
                ],
                before_state={
                    'p95_execution_time_ms': metrics.p95_execution_time_ms},
                after_state={
                    'target_p95_time_ms': rules['high_p95_threshold_ms']},
                metrics_to_track=['p95_execution_time_ms',
                                  'execution_time_variance'],
                risks=['Potential timeout-related errors'],
                dependencies=[]
            ))

        return recommendations

    def _generate_reliability_recommendations(
        self, metrics: WorkflowMetrics
    ) -> List[OptimizationRecommendation]:
        """Generate reliability optimization recommendations."""

        recommendations = []
        rules = self.optimization_rules['reliability']

        # Low success rate recommendation
        if metrics.success_rate < rules['min_success_rate']:
            improvement_needed = rules['min_success_rate'] - \
                metrics.success_rate

            recommendations.append(OptimizationRecommendation(
                recommendation_id=f"rel_success_{metrics.workflow_id}",
                title="Improve workflow success rate",
                description=f"Success rate ({metrics.success_rate:.1%}) is below target ({rules['min_success_rate']:.1%})",
                optimization_type=OptimizationType.RELIABILITY,
                priority=OptimizationPriority.HIGH,
                complexity=OptimizationComplexity.MODERATE,
                impact_score=improvement_needed / rules['min_success_rate'],
                confidence=0.9,
                estimated_savings={
                    'success_rate_improvement': f"{improvement_needed:.1%}",
                    'reduced_manual_intervention': "Fewer failed executions to handle manually"
                },
                implementation_steps=[
                    "Analyze common failure patterns",
                    "Add comprehensive error handling",
                    "Implement retry logic with exponential backoff",
                    "Add input validation and sanitization",
                    "Set up monitoring and alerting for failures"
                ],
                before_state={'success_rate': metrics.success_rate},
                after_state={'target_success_rate': rules['min_success_rate']},
                metrics_to_track=['success_rate', 'error_rate', 'retry_rate'],
                risks=['Increased complexity', 'Potential for retry storms'],
                dependencies=[]
            ))

        # High error rate recommendation
        if metrics.error_rate > rules['max_error_rate']:
            recommendations.append(OptimizationRecommendation(
                recommendation_id=f"rel_errors_{metrics.workflow_id}",
                title="Reduce workflow error rate",
                description=f"Error rate ({metrics.error_rate:.1%}) exceeds acceptable threshold ({rules['max_error_rate']:.1%})",
                optimization_type=OptimizationType.RELIABILITY,
                priority=OptimizationPriority.HIGH,
                complexity=OptimizationComplexity.SIMPLE,
                impact_score=0.7,
                confidence=0.8,
                estimated_savings={
                    'error_reduction': f"{metrics.error_rate - rules['max_error_rate']:.1%}",
                    'operational_overhead_reduction': "Less time spent on error investigation"
                },
                implementation_steps=[
                    "Implement structured error logging",
                    "Add error categorization and handling",
                    "Create error recovery procedures",
                    "Set up automated error notifications"
                ],
                before_state={'error_rate': metrics.error_rate},
                after_state={'target_error_rate': rules['max_error_rate']},
                metrics_to_track=['error_rate',
                                  'error_categories', 'recovery_success_rate'],
                risks=['False positive alerts',
                       'Over-engineering error handling'],
                dependencies=[]
            ))

        return recommendations

    def _generate_resource_recommendations(
        self, metrics: WorkflowMetrics
    ) -> List[OptimizationRecommendation]:
        """Generate resource optimization recommendations."""

        recommendations = []
        rules = self.optimization_rules['resource']

        # High memory usage recommendation
        memory_usage = metrics.resource_usage.get('memory_mb', 0)
        if memory_usage > rules['max_memory_per_workflow_mb']:
            recommendations.append(OptimizationRecommendation(
                recommendation_id=f"res_memory_{metrics.workflow_id}",
                title="Optimize memory usage",
                description=f"Memory usage ({memory_usage:.0f}MB) exceeds recommended limit ({rules['max_memory_per_workflow_mb']}MB)",
                optimization_type=OptimizationType.RESOURCE,
                priority=OptimizationPriority.MEDIUM,
                complexity=OptimizationComplexity.MODERATE,
                impact_score=0.6,
                confidence=0.7,
                estimated_savings={
                    'memory_reduction_mb': memory_usage - rules['max_memory_per_workflow_mb'],
                    'cost_savings_monthly': (memory_usage - rules['max_memory_per_workflow_mb']) *
                    self.cost_models['compute']['memory_gb_hour_cost'] *
                    24 * 30 / 1024
                },
                implementation_steps=[
                    "Profile memory usage patterns",
                    "Optimize data structures and algorithms",
                    "Implement streaming processing for large datasets",
                    "Add memory cleanup routines",
                    "Consider memory-efficient data formats"
                ],
                before_state={'memory_usage_mb': memory_usage},
                after_state={
                    'target_memory_mb': rules['max_memory_per_workflow_mb']},
                metrics_to_track=['memory_usage_mb', 'memory_peak_mb'],
                risks=['Potential performance trade-offs',
                       'Increased code complexity'],
                dependencies=[]
            ))

        # High CPU usage recommendation
        cpu_usage = metrics.resource_usage.get('cpu_percent', 0)
        if cpu_usage > rules['max_cpu_per_workflow_percent']:
            recommendations.append(OptimizationRecommendation(
                recommendation_id=f"res_cpu_{metrics.workflow_id}",
                title="Optimize CPU utilization",
                description=f"CPU usage ({cpu_usage:.1f}%) is high and may impact other workflows",
                optimization_type=OptimizationType.RESOURCE,
                priority=OptimizationPriority.MEDIUM,
                complexity=OptimizationComplexity.MODERATE,
                impact_score=0.5,
                confidence=0.6,
                estimated_savings={
                    'cpu_reduction_percent': cpu_usage - rules['max_cpu_per_workflow_percent'],
                    'improved_system_responsiveness': 'Better performance for other workflows'
                },
                implementation_steps=[
                    "Profile CPU usage hotspots",
                    "Optimize computational algorithms",
                    "Implement task prioritization",
                    "Consider offloading CPU-intensive tasks",
                    "Add CPU usage monitoring and throttling"
                ],
                before_state={'cpu_usage_percent': cpu_usage},
                after_state={
                    'target_cpu_percent': rules['max_cpu_per_workflow_percent']},
                metrics_to_track=['cpu_usage_percent', 'cpu_wait_time'],
                risks=['Potential processing delays',
                       'Complexity in throttling logic'],
                dependencies=[]
            ))

        return recommendations

    def _generate_cost_recommendations(
        self, metrics: WorkflowMetrics
    ) -> List[OptimizationRecommendation]:
        """Generate cost optimization recommendations."""

        recommendations = []
        rules = self.optimization_rules['cost']

        # High cost per execution
        if metrics.cost_per_execution > rules['max_cost_per_execution']:
            cost_reduction = metrics.cost_per_execution - \
                rules['max_cost_per_execution']
            monthly_savings = cost_reduction * metrics.execution_count

            recommendations.append(OptimizationRecommendation(
                recommendation_id=f"cost_exec_{metrics.workflow_id}",
                title="Reduce execution costs",
                description=f"Cost per execution (${metrics.cost_per_execution:.3f}) exceeds budget target (${rules['max_cost_per_execution']:.3f})",
                optimization_type=OptimizationType.COST,
                priority=OptimizationPriority.HIGH,
                complexity=OptimizationComplexity.MODERATE,
                impact_score=cost_reduction / rules['max_cost_per_execution'],
                confidence=0.8,
                estimated_savings={
                    'cost_reduction_per_execution': cost_reduction,
                    'monthly_cost_savings': monthly_savings,
                    'annual_cost_savings': monthly_savings * 12
                },
                implementation_steps=[
                    "Analyze cost breakdown by workflow component",
                    "Optimize API usage and reduce unnecessary calls",
                    "Implement result caching to avoid redundant processing",
                    "Negotiate better rates with service providers",
                    "Consider alternative service providers or architectures"
                ],
                before_state={
                    'cost_per_execution': metrics.cost_per_execution},
                after_state={
                    'target_cost_per_execution': rules['max_cost_per_execution']},
                metrics_to_track=['cost_per_execution', 'monthly_total_cost'],
                risks=['Potential service quality trade-offs',
                       'Migration complexity'],
                dependencies=[]
            ))

        return recommendations

    def _generate_scalability_recommendations(
        self, metrics: WorkflowMetrics
    ) -> List[OptimizationRecommendation]:
        """Generate scalability optimization recommendations."""

        recommendations = []

        # If execution count is growing, suggest scalability improvements
        if metrics.execution_count > 100:  # Threshold for scalability concerns
            recommendations.append(OptimizationRecommendation(
                recommendation_id=f"scale_prep_{metrics.workflow_id}",
                title="Prepare for scale",
                description="High execution volume indicates need for scalability optimizations",
                optimization_type=OptimizationType.SCALABILITY,
                priority=OptimizationPriority.MEDIUM,
                complexity=OptimizationComplexity.COMPLEX,
                impact_score=0.6,
                confidence=0.7,
                estimated_savings={
                    'future_performance_protection': 'Maintain performance as volume grows',
                    'reduced_scaling_pain': 'Proactive preparation for growth'
                },
                implementation_steps=[
                    "Implement horizontal scaling capabilities",
                    "Add load balancing and distribution logic",
                    "Optimize database queries for scale",
                    "Implement connection pooling",
                    "Add performance monitoring and auto-scaling triggers"
                ],
                before_state={'execution_count': metrics.execution_count},
                after_state={'scale_ready': True},
                metrics_to_track=[
                    'throughput', 'concurrent_executions', 'resource_utilization'],
                risks=['Increased architectural complexity',
                       'Higher operational overhead'],
                dependencies=[]
            ))

        return recommendations

    def _generate_security_recommendations(
        self, metrics: WorkflowMetrics
    ) -> List[OptimizationRecommendation]:
        """Generate security optimization recommendations."""

        recommendations = []

        # Generic security recommendations based on execution volume
        if metrics.execution_count > 50:  # Workflows with significant usage
            recommendations.append(OptimizationRecommendation(
                recommendation_id=f"sec_audit_{metrics.workflow_id}",
                title="Security audit and hardening",
                description="High-usage workflow should undergo security review",
                optimization_type=OptimizationType.SECURITY,
                priority=OptimizationPriority.MEDIUM,
                complexity=OptimizationComplexity.SIMPLE,
                impact_score=0.4,
                confidence=0.6,
                estimated_savings={
                    'risk_reduction': 'Lower security incident probability',
                    'compliance_improvement': 'Better adherence to security standards'
                },
                implementation_steps=[
                    "Conduct security audit of workflow logic",
                    "Implement input validation and sanitization",
                    "Add authentication and authorization checks",
                    "Encrypt sensitive data in transit and at rest",
                    "Set up security monitoring and logging"
                ],
                before_state={'security_review_status': 'pending'},
                after_state={'security_review_status': 'completed'},
                metrics_to_track=['security_incidents', 'compliance_score'],
                risks=['Development overhead', 'Potential performance impact'],
                dependencies=[]
            ))

        return recommendations

    def _generate_maintainability_recommendations(
        self, metrics: WorkflowMetrics
    ) -> List[OptimizationRecommendation]:
        """Generate maintainability optimization recommendations."""

        recommendations = []

        # For complex or frequently-executed workflows
        if metrics.execution_count > 20:
            recommendations.append(OptimizationRecommendation(
                recommendation_id=f"maint_doc_{metrics.workflow_id}",
                title="Improve documentation and maintainability",
                description="Frequently-used workflow should have comprehensive documentation",
                optimization_type=OptimizationType.MAINTAINABILITY,
                priority=OptimizationPriority.LOW,
                complexity=OptimizationComplexity.SIMPLE,
                impact_score=0.3,
                confidence=0.8,
                estimated_savings={
                    'reduced_maintenance_time': 'Faster troubleshooting and updates',
                    'improved_team_productivity': 'Easier onboarding and knowledge sharing'
                },
                implementation_steps=[
                    "Add comprehensive workflow documentation",
                    "Include inline comments for complex logic",
                    "Create troubleshooting guides",
                    "Document dependencies and configuration",
                    "Set up automated documentation generation"
                ],
                before_state={'documentation_status': 'incomplete'},
                after_state={'documentation_status': 'comprehensive'},
                metrics_to_track=[
                    'documentation_coverage', 'maintenance_time'],
                risks=['Documentation maintenance overhead'],
                dependencies=[]
            ))

        return recommendations

    def _prioritize_recommendations(
        self,
        recommendations: List[OptimizationRecommendation],
        context: Optional[OptimizationContext] = None
    ) -> List[OptimizationRecommendation]:
        """Prioritize and filter recommendations based on context."""

        # Calculate priority scores
        for rec in recommendations:
            score = 0.0

            # Base priority score
            priority_scores = {
                OptimizationPriority.CRITICAL: 10.0,
                OptimizationPriority.HIGH: 7.0,
                OptimizationPriority.MEDIUM: 5.0,
                OptimizationPriority.LOW: 3.0,
                OptimizationPriority.INFORMATIONAL: 1.0
            }
            score += priority_scores[rec.priority]

            # Impact score
            score += rec.impact_score * 5.0

            # Confidence score
            score += rec.confidence * 3.0

            # Complexity penalty
            complexity_penalties = {
                OptimizationComplexity.TRIVIAL: 0.0,
                OptimizationComplexity.SIMPLE: -0.5,
                OptimizationComplexity.MODERATE: -1.0,
                OptimizationComplexity.COMPLEX: -2.0,
                OptimizationComplexity.MAJOR: -3.0
            }
            score += complexity_penalties[rec.complexity]

            rec._priority_score = score

        # Sort by priority score
        recommendations.sort(key=lambda r: r._priority_score, reverse=True)

        return recommendations

    # Analysis helper methods

    def _analyze_performance_trends(self, workflow_id: str) -> Dict[str, Any]:
        """Analyze performance trends for a workflow."""

        # Simplified trend analysis
        metrics = self.workflow_metrics[workflow_id]

        trends = {
            'execution_time_trend': 'stable',  # Could be 'improving', 'degrading', 'stable'
            'success_rate_trend': 'stable',
            'cost_trend': 'stable',
            'volume_trend': 'growing' if metrics.execution_count > 50 else 'stable'
        }

        return trends

    def _identify_bottlenecks(self, workflow_id: str) -> List[Dict[str, Any]]:
        """Identify performance bottlenecks in a workflow."""

        metrics = self.workflow_metrics[workflow_id]
        bottlenecks = []

        # High execution time bottleneck
        if metrics.avg_execution_time_ms > 10000:
            bottlenecks.append({
                'type': 'execution_time',
                'severity': 'high',
                'description': 'Long average execution time indicates processing bottleneck',
                'metric_value': metrics.avg_execution_time_ms,
                'threshold': 10000
            })

        # High memory usage bottleneck
        memory_usage = metrics.resource_usage.get('memory_mb', 0)
        if memory_usage > 512:
            bottlenecks.append({
                'type': 'memory_usage',
                'severity': 'medium',
                'description': 'High memory usage may limit concurrent executions',
                'metric_value': memory_usage,
                'threshold': 512
            })

        return bottlenecks

    def _identify_improvement_opportunities(
        self, comparison_data: Dict[str, Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Identify improvement opportunities from comparative analysis."""

        opportunities = []

        # Find workflows that could learn from best performers
        success_rates = {wf_id: data['success_rate']
                         for wf_id, data in comparison_data.items()}
        best_success_rate = max(success_rates.values())

        for wf_id, success_rate in success_rates.items():
            if success_rate < best_success_rate - 0.1:  # 10% gap
                opportunities.append({
                    'workflow_id': wf_id,
                    'improvement_type': 'success_rate',
                    'current_value': success_rate,
                    'target_value': best_success_rate,
                    'gap': best_success_rate - success_rate,
                    'suggestion': 'Analyze best-performing workflow patterns and apply similar optimizations'
                })

        return opportunities

    def _group_similar_workflows(self, workflow_ids: List[str]) -> List[List[str]]:
        """Group similar workflows for consolidation analysis."""

        # Simplified grouping logic - in practice, this would analyze workflow structures
        # For now, just return individual workflows
        return [[wf_id] for wf_id in workflow_ids if wf_id in self.workflow_metrics]

    def _generate_scaling_recommendations(
        self, constraints: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Generate scaling recommendations based on capacity constraints."""

        recommendations = []

        for constraint in constraints:
            if constraint['resource'] == 'cpu':
                recommendations.append({
                    'type': 'horizontal_scaling',
                    'description': 'Add more compute instances to distribute CPU load',
                    'estimated_cost_increase': '20-30%',
                    'implementation_effort': 'moderate'
                })
            elif constraint['resource'] == 'memory':
                recommendations.append({
                    'type': 'vertical_scaling',
                    'description': 'Upgrade to instances with more memory',
                    'estimated_cost_increase': '15-25%',
                    'implementation_effort': 'simple'
                })

        return recommendations


# Utility functions

def analyze_workflow_optimization_opportunities(
    workflow_metrics: Dict[str, Dict[str, Any]],
    context: Optional[OptimizationContext] = None
) -> Dict[str, Any]:
    """High-level function to analyze optimization opportunities across workflows."""

    engine = OptimizationEngine()

    # Record metrics for all workflows
    for workflow_id, metrics_data in workflow_metrics.items():
        engine.record_workflow_metrics(
            workflow_id=workflow_id,
            execution_time_ms=metrics_data.get('execution_time_ms', 1000),
            success=metrics_data.get('success', True),
            resource_usage=metrics_data.get('resource_usage', {}),
            data_volume=metrics_data.get('data_volume', 0),
            cost=metrics_data.get('cost', 0.0),
            user_feedback=metrics_data.get('user_feedback')
        )

    # Generate comprehensive analysis
    workflow_ids = list(workflow_metrics.keys())
    all_recommendations = []

    for workflow_id in workflow_ids:
        recommendations = engine.generate_optimization_recommendations(
            workflow_id, context)
        all_recommendations.extend(recommendations)

    # Comparative analysis
    comparative_analysis = engine.generate_comparative_analysis(workflow_ids)

    # Consolidation opportunities
    consolidation_opportunities = engine.suggest_workflow_consolidation(
        workflow_ids)

    # Capacity planning
    capacity_planning = engine.generate_capacity_planning_recommendations(
        workflow_ids)

    return {
        'total_workflows_analyzed': len(workflow_ids),
        'total_recommendations': len(all_recommendations),
        'recommendations_by_type': Counter([r.optimization_type.value for r in all_recommendations]),
        'recommendations_by_priority': Counter([r.priority.value for r in all_recommendations]),
        # Top 10 recommendations
        'top_recommendations': all_recommendations[:10],
        'comparative_analysis': comparative_analysis,
        'consolidation_opportunities': consolidation_opportunities,
        'capacity_planning': capacity_planning,
        'summary': {
            'critical_issues': len([r for r in all_recommendations if r.priority == OptimizationPriority.CRITICAL]),
            'high_impact_opportunities': len([r for r in all_recommendations if r.impact_score > 0.7]),
            'estimated_monthly_savings': sum([
                r.estimated_savings.get('monthly_cost_savings', 0)
                for r in all_recommendations
            ]),
            'quick_wins': len([r for r in all_recommendations
                               if r.complexity == OptimizationComplexity.TRIVIAL and r.impact_score > 0.5])
        }
    }
