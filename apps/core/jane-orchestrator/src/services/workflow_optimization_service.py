"""
Workflow Performance Optimization Service

Analyzes workflow execution metrics and automatically optimizes
workflows based on performance data and success patterns.
"""

import logging
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple

from sqlalchemy import and_, desc, func
from sqlalchemy.orm import Session

from ..data.models.adaptive_workflow import AdaptiveWorkflow
from ..data.models.user_request import UserRequest
from ..data.models.workflow_pattern import WorkflowPattern

logger = logging.getLogger(__name__)


@dataclass
class PerformanceMetrics:
    """Workflow performance metrics"""
    workflow_id: str
    execution_count: int
    success_rate: float
    average_execution_time: float
    error_rate: float
    user_satisfaction: float
    automation_efficiency: float
    last_optimization: Optional[datetime]


@dataclass
class OptimizationRecommendation:
    """Workflow optimization recommendation"""
    workflow_id: str
    recommendation_type: str
    description: str
    expected_improvement: float
    priority: str
    implementation_complexity: str
    estimated_time_savings: float


@dataclass
class OptimizationResult:
    """Result of workflow optimization"""
    workflow_id: str
    optimization_type: str
    success: bool
    before_metrics: PerformanceMetrics
    after_metrics: Optional[PerformanceMetrics]
    improvement_percentage: float
    error_message: Optional[str]


class WorkflowOptimizationService:
    """
    Service for analyzing and optimizing workflow performance

    Optimization Strategies:
    - Node sequence optimization based on success patterns
    - Timeout adjustments based on execution time analysis
    - Error handling improvements based on failure patterns
    - Resource allocation optimization
    - Conditional logic optimization
    """

    def __init__(self, db: Session):
        self.db = db

        # Optimization thresholds
        self.MIN_EXECUTIONS_FOR_OPTIMIZATION = 10
        self.MIN_SUCCESS_RATE_THRESHOLD = 0.7
        self.HIGH_EXECUTION_TIME_THRESHOLD = 30.0  # seconds
        self.ERROR_RATE_THRESHOLD = 0.2

        # Performance targets
        self.TARGET_SUCCESS_RATE = 0.95
        self.TARGET_EXECUTION_TIME = 10.0  # seconds
        self.TARGET_ERROR_RATE = 0.05

    async def analyze_workflow_performance(
        self,
        workflow_id: str,
        days_back: int = 30
    ) -> PerformanceMetrics:
        """Analyze performance metrics for a specific workflow"""
        cutoff_date = datetime.utcnow() - timedelta(days=days_back)

        workflow = self.db.query(AdaptiveWorkflow)\
            .filter(AdaptiveWorkflow.id == workflow_id)\
            .first()

        if not workflow:
            raise ValueError(f"Workflow {workflow_id} not found")

        # Calculate metrics from execution history
        execution_count = len(workflow.execution_history)

        if execution_count == 0:
            return PerformanceMetrics(
                workflow_id=workflow_id,
                execution_count=0,
                success_rate=0.0,
                average_execution_time=0.0,
                error_rate=0.0,
                user_satisfaction=0.0,
                automation_efficiency=0.0,
                last_optimization=workflow.last_optimization
            )

        # Recent executions for analysis
        recent_executions = [
            exec_data for exec_data in workflow.execution_history
            if datetime.fromisoformat(exec_data.get('timestamp', '1970-01-01')) >= cutoff_date
        ]

        if not recent_executions:
            # Last 10 executions
            recent_executions = workflow.execution_history[-10:]

        # Calculate performance metrics
        successful_executions = [
            exec_data for exec_data in recent_executions
            if exec_data.get('success', False)
        ]

        success_rate = len(successful_executions) / len(recent_executions)

        execution_times = [
            float(exec_data.get('execution_time', 0))
            for exec_data in recent_executions
            if exec_data.get('execution_time')
        ]

        average_execution_time = sum(
            execution_times) / len(execution_times) if execution_times else 0.0
        error_rate = 1.0 - success_rate

        # Calculate user satisfaction based on success rate and execution time
        user_satisfaction = self._calculate_user_satisfaction(
            success_rate, average_execution_time)

        # Calculate automation efficiency
        automation_efficiency = self._calculate_automation_efficiency(
            workflow, success_rate, average_execution_time
        )

        return PerformanceMetrics(
            workflow_id=workflow_id,
            execution_count=len(recent_executions),
            success_rate=success_rate,
            average_execution_time=average_execution_time,
            error_rate=error_rate,
            user_satisfaction=user_satisfaction,
            automation_efficiency=automation_efficiency,
            last_optimization=workflow.last_optimization
        )

    async def generate_optimization_recommendations(
        self,
        workflow_id: str
    ) -> List[OptimizationRecommendation]:
        """Generate optimization recommendations based on performance analysis"""
        metrics = await self.analyze_workflow_performance(workflow_id)
        recommendations = []

        if metrics.execution_count < self.MIN_EXECUTIONS_FOR_OPTIMIZATION:
            return recommendations  # Not enough data for optimization

        # Success rate optimization
        if metrics.success_rate < self.MIN_SUCCESS_RATE_THRESHOLD:
            recommendations.append(
                self._create_success_rate_recommendation(workflow_id, metrics)
            )

        # Execution time optimization
        if metrics.average_execution_time > self.HIGH_EXECUTION_TIME_THRESHOLD:
            recommendations.append(
                self._create_execution_time_recommendation(
                    workflow_id, metrics)
            )

        # Error handling optimization
        if metrics.error_rate > self.ERROR_RATE_THRESHOLD:
            recommendations.append(
                self._create_error_handling_recommendation(
                    workflow_id, metrics)
            )

        # Node sequence optimization
        sequence_rec = await self._analyze_node_sequence_optimization(workflow_id, metrics)
        if sequence_rec:
            recommendations.append(sequence_rec)

        # Resource optimization
        resource_rec = await self._analyze_resource_optimization(workflow_id, metrics)
        if resource_rec:
            recommendations.append(resource_rec)

        return sorted(recommendations, key=lambda x: self._get_priority_score(x.priority), reverse=True)

    async def optimize_workflow(
        self,
        workflow_id: str,
        optimization_type: str = "auto"
    ) -> OptimizationResult:
        """Apply optimization to workflow based on performance analysis"""
        before_metrics = await self.analyze_workflow_performance(workflow_id)

        workflow = self.db.query(AdaptiveWorkflow)\
            .filter(AdaptiveWorkflow.id == workflow_id)\
            .first()

        if not workflow:
            return OptimizationResult(
                workflow_id=workflow_id,
                optimization_type=optimization_type,
                success=False,
                before_metrics=before_metrics,
                after_metrics=None,
                improvement_percentage=0.0,
                error_message="Workflow not found"
            )

        try:
            # Apply optimization based on type
            if optimization_type == "auto":
                success = await self._apply_auto_optimization(workflow, before_metrics)
            elif optimization_type == "execution_time":
                success = await self._optimize_execution_time(workflow, before_metrics)
            elif optimization_type == "success_rate":
                success = await self._optimize_success_rate(workflow, before_metrics)
            elif optimization_type == "error_handling":
                success = await self._optimize_error_handling(workflow, before_metrics)
            else:
                raise ValueError(
                    f"Unknown optimization type: {optimization_type}")

            if not success:
                return OptimizationResult(
                    workflow_id=workflow_id,
                    optimization_type=optimization_type,
                    success=False,
                    before_metrics=before_metrics,
                    after_metrics=None,
                    improvement_percentage=0.0,
                    error_message="Optimization failed to apply"
                )

            # Update workflow
            workflow.last_optimization = datetime.utcnow()
            workflow.optimization_count = (
                workflow.optimization_count or 0) + 1
            self.db.commit()

            # Calculate improvement (simulated for immediate response)
            improvement = self._estimate_improvement(
                before_metrics, optimization_type)

            return OptimizationResult(
                workflow_id=workflow_id,
                optimization_type=optimization_type,
                success=True,
                before_metrics=before_metrics,
                after_metrics=None,  # Would be measured after execution
                improvement_percentage=improvement,
                error_message=None
            )

        except Exception as e:
            logger.error(f"Error optimizing workflow {workflow_id}: {e}")
            return OptimizationResult(
                workflow_id=workflow_id,
                optimization_type=optimization_type,
                success=False,
                before_metrics=before_metrics,
                after_metrics=None,
                improvement_percentage=0.0,
                error_message=str(e)
            )

    async def batch_optimize_workflows(
        self,
        min_executions: int = 10,
        max_workflows: int = 10
    ) -> List[OptimizationResult]:
        """Batch optimize workflows that meet criteria"""
        # Find workflows that need optimization
        workflows_needing_optimization = self.db.query(AdaptiveWorkflow)\
            .filter(AdaptiveWorkflow.is_active == True)\
            .filter(func.json_array_length(AdaptiveWorkflow.execution_history) >= min_executions)\
            .order_by(desc(AdaptiveWorkflow.created_at))\
            .limit(max_workflows)\
            .all()

        results = []
        for workflow in workflows_needing_optimization:
            try:
                metrics = await self.analyze_workflow_performance(str(workflow.id))

                # Check if optimization is needed
                needs_optimization = (
                    metrics.success_rate < self.TARGET_SUCCESS_RATE or
                    metrics.average_execution_time > self.TARGET_EXECUTION_TIME or
                    metrics.error_rate > self.TARGET_ERROR_RATE
                )

                if needs_optimization:
                    result = await self.optimize_workflow(str(workflow.id), "auto")
                    results.append(result)

            except Exception as e:
                logger.error(
                    f"Error in batch optimization for workflow {workflow.id}: {e}")

        return results

    def _calculate_user_satisfaction(self, success_rate: float, execution_time: float) -> float:
        """Calculate user satisfaction score based on performance metrics"""
        # Weighted formula: 70% success rate, 30% execution time performance
        success_component = success_rate * 0.7

        # Execution time component (inverse relationship)
        # 60 seconds as max acceptable
        time_performance = max(0, 1 - (execution_time / 60))
        time_component = time_performance * 0.3

        return min(1.0, success_component + time_component)

    def _calculate_automation_efficiency(
        self,
        workflow: AdaptiveWorkflow,
        success_rate: float,
        execution_time: float
    ) -> float:
        """Calculate automation efficiency based on time savings and reliability"""
        # Estimate manual time savings
        pattern = self.db.query(WorkflowPattern)\
            .filter(WorkflowPattern.id == workflow.pattern_id)\
            .first()

        if not pattern:
            return 0.0

        # Estimated manual time vs automated time
        manual_time_estimate = pattern.automation_value * \
            300  # 5 minutes per automation value point
        time_savings_ratio = max(
            0, (manual_time_estimate - execution_time) / manual_time_estimate)

        # Efficiency = (time savings * success rate)
        return min(1.0, time_savings_ratio * success_rate)

    def _create_success_rate_recommendation(
        self,
        workflow_id: str,
        metrics: PerformanceMetrics
    ) -> OptimizationRecommendation:
        """Create recommendation to improve success rate"""
        expected_improvement = (
            self.TARGET_SUCCESS_RATE - metrics.success_rate) * 100

        return OptimizationRecommendation(
            workflow_id=workflow_id,
            recommendation_type="success_rate",
            description=f"Improve error handling and add retry logic. Current success rate: {metrics.success_rate:.1%}",
            expected_improvement=expected_improvement,
            priority="HIGH" if metrics.success_rate < 0.5 else "MEDIUM",
            implementation_complexity="MEDIUM",
            estimated_time_savings=expected_improvement *
            0.1  # 10% time per 1% success improvement
        )

    def _create_execution_time_recommendation(
        self,
        workflow_id: str,
        metrics: PerformanceMetrics
    ) -> OptimizationRecommendation:
        """Create recommendation to improve execution time"""
        time_reduction = metrics.average_execution_time - self.TARGET_EXECUTION_TIME
        expected_improvement = (
            time_reduction / metrics.average_execution_time) * 100

        return OptimizationRecommendation(
            workflow_id=workflow_id,
            recommendation_type="execution_time",
            description=f"Optimize node sequence and reduce timeouts. Current time: {metrics.average_execution_time:.1f}s",
            expected_improvement=expected_improvement,
            priority="HIGH" if metrics.average_execution_time > 60 else "MEDIUM",
            implementation_complexity="LOW",
            estimated_time_savings=time_reduction
        )

    def _create_error_handling_recommendation(
        self,
        workflow_id: str,
        metrics: PerformanceMetrics
    ) -> OptimizationRecommendation:
        """Create recommendation to improve error handling"""
        return OptimizationRecommendation(
            workflow_id=workflow_id,
            recommendation_type="error_handling",
            description=f"Add comprehensive error handling and fallback mechanisms. Error rate: {metrics.error_rate:.1%}",
            expected_improvement=(metrics.error_rate -
                                  self.TARGET_ERROR_RATE) * 100,
            priority="HIGH",
            implementation_complexity="MEDIUM",
            # 15 minutes saved per 1% error reduction
            estimated_time_savings=metrics.error_rate * 15
        )

    async def _analyze_node_sequence_optimization(
        self,
        workflow_id: str,
        metrics: PerformanceMetrics
    ) -> Optional[OptimizationRecommendation]:
        """Analyze if node sequence can be optimized"""
        workflow = self.db.query(AdaptiveWorkflow)\
            .filter(AdaptiveWorkflow.id == workflow_id)\
            .first()

        if not workflow or not workflow.n8n_workflow_data:
            return None

        # Analyze node dependencies and execution patterns
        nodes = workflow.n8n_workflow_data.get('nodes', [])

        if len(nodes) > 5:  # Only optimize complex workflows
            return OptimizationRecommendation(
                workflow_id=workflow_id,
                recommendation_type="node_sequence",
                description=f"Optimize node execution order for {len(nodes)} nodes to reduce dependencies",
                expected_improvement=15.0,  # 15% improvement estimate
                priority="MEDIUM",
                implementation_complexity="HIGH",
                estimated_time_savings=metrics.average_execution_time * 0.15
            )

        return None

    async def _analyze_resource_optimization(
        self,
        workflow_id: str,
        metrics: PerformanceMetrics
    ) -> Optional[OptimizationRecommendation]:
        """Analyze resource usage optimization opportunities"""
        if metrics.average_execution_time > 20:
            return OptimizationRecommendation(
                workflow_id=workflow_id,
                recommendation_type="resource_optimization",
                description="Optimize resource allocation and parallel processing",
                expected_improvement=20.0,
                priority="MEDIUM",
                implementation_complexity="HIGH",
                estimated_time_savings=metrics.average_execution_time * 0.2
            )

        return None

    async def _apply_auto_optimization(
        self,
        workflow: AdaptiveWorkflow,
        metrics: PerformanceMetrics
    ) -> bool:
        """Apply automatic optimization based on metrics"""
        optimizations_applied = []

        # Apply low-complexity optimizations first
        if metrics.average_execution_time > self.HIGH_EXECUTION_TIME_THRESHOLD:
            if await self._optimize_execution_time(workflow, metrics):
                optimizations_applied.append("execution_time")

        if metrics.error_rate > self.ERROR_RATE_THRESHOLD:
            if await self._optimize_error_handling(workflow, metrics):
                optimizations_applied.append("error_handling")

        if metrics.success_rate < self.MIN_SUCCESS_RATE_THRESHOLD:
            if await self._optimize_success_rate(workflow, metrics):
                optimizations_applied.append("success_rate")

        return len(optimizations_applied) > 0

    async def _optimize_execution_time(
        self,
        workflow: AdaptiveWorkflow,
        metrics: PerformanceMetrics
    ) -> bool:
        """Optimize workflow execution time"""
        try:
            if workflow.n8n_workflow_data:
                # Reduce timeouts in nodes
                nodes = workflow.n8n_workflow_data.get('nodes', [])
                for node in nodes:
                    if 'parameters' in node and 'timeout' in node['parameters']:
                        current_timeout = node['parameters']['timeout']
                        if current_timeout > 10000:  # Reduce if > 10 seconds
                            node['parameters']['timeout'] = min(
                                current_timeout, 10000)

                # Add parallel execution hints
                workflow.n8n_workflow_data['optimizations'] = workflow.n8n_workflow_data.get(
                    'optimizations', {})
                workflow.n8n_workflow_data['optimizations']['execution_time_optimized'] = True
                workflow.n8n_workflow_data['optimizations']['optimization_date'] = datetime.utcnow(
                ).isoformat()

            return True

        except Exception as e:
            logger.error(f"Error optimizing execution time: {e}")
            return False

    async def _optimize_success_rate(
        self,
        workflow: AdaptiveWorkflow,
        metrics: PerformanceMetrics
    ) -> bool:
        """Optimize workflow success rate"""
        try:
            if workflow.n8n_workflow_data:
                # Add retry logic to nodes
                nodes = workflow.n8n_workflow_data.get('nodes', [])
                for node in nodes:
                    if node.get('type') not in ['n8n-nodes-base.start', 'n8n-nodes-base.webhook']:
                        node['retryOnFail'] = True
                        node['maxTries'] = 3
                        node['waitBetweenTries'] = 1000

                workflow.n8n_workflow_data['optimizations'] = workflow.n8n_workflow_data.get(
                    'optimizations', {})
                workflow.n8n_workflow_data['optimizations']['success_rate_optimized'] = True

            return True

        except Exception as e:
            logger.error(f"Error optimizing success rate: {e}")
            return False

    async def _optimize_error_handling(
        self,
        workflow: AdaptiveWorkflow,
        metrics: PerformanceMetrics
    ) -> bool:
        """Optimize workflow error handling"""
        try:
            if workflow.n8n_workflow_data:
                # Add error handling nodes
                nodes = workflow.n8n_workflow_data.get('nodes', [])

                # Add global error handler if not present
                has_error_handler = any(
                    node.get('type') == 'n8n-nodes-base.errorTrigger'
                    for node in nodes
                )

                if not has_error_handler:
                    error_node = {
                        'id': f'error_handler_{len(nodes)}',
                        'name': 'Error Handler',
                        'type': 'n8n-nodes-base.set',
                        'position': [400, 300],
                        'parameters': {
                            'values': {
                                'string': [
                                    {
                                        'name': 'error_handled',
                                        'value': 'true'
                                    }
                                ]
                            }
                        }
                    }
                    nodes.append(error_node)

                workflow.n8n_workflow_data['optimizations'] = workflow.n8n_workflow_data.get(
                    'optimizations', {})
                workflow.n8n_workflow_data['optimizations']['error_handling_optimized'] = True

            return True

        except Exception as e:
            logger.error(f"Error optimizing error handling: {e}")
            return False

    def _estimate_improvement(self, metrics: PerformanceMetrics, optimization_type: str) -> float:
        """Estimate improvement percentage based on optimization type"""
        if optimization_type == "execution_time":
            if metrics.average_execution_time > self.HIGH_EXECUTION_TIME_THRESHOLD:
                return min(50.0, (metrics.average_execution_time - self.TARGET_EXECUTION_TIME) / metrics.average_execution_time * 100)

        elif optimization_type == "success_rate":
            if metrics.success_rate < self.TARGET_SUCCESS_RATE:
                return (self.TARGET_SUCCESS_RATE - metrics.success_rate) * 100

        elif optimization_type == "error_handling":
            if metrics.error_rate > self.TARGET_ERROR_RATE:
                return (metrics.error_rate - self.TARGET_ERROR_RATE) * 100

        elif optimization_type == "auto":
            # Combined improvement estimate
            improvements = []
            if metrics.average_execution_time > self.TARGET_EXECUTION_TIME:
                improvements.append(20.0)
            if metrics.success_rate < self.TARGET_SUCCESS_RATE:
                improvements.append(15.0)
            if metrics.error_rate > self.TARGET_ERROR_RATE:
                improvements.append(25.0)

            return max(improvements) if improvements else 0.0

        return 0.0

    def _get_priority_score(self, priority: str) -> int:
        """Convert priority string to numeric score"""
        priority_scores = {
            "HIGH": 3,
            "MEDIUM": 2,
            "LOW": 1
        }
        return priority_scores.get(priority, 0)
