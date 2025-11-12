"""
User Feedback Integration for Workflow Accuracy Improvement

This module processes user feedback on auto-generated workflows to improve
the pattern detection and workflow generation accuracy over time.

Constitutional Requirements:
- Improve workflow generation accuracy through user feedback learning
- Support executive function by reducing false positives in suggestions
- Maintain <200ms UI feedback response times
"""

import logging
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Dict, List, Optional

from apps.jane_orchestrator.src.data.models.adaptive_workflow import \
    AdaptiveWorkflow
from apps.jane_orchestrator.src.data.models.workflow_pattern import \
    WorkflowPattern
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)


class FeedbackType(Enum):
    """Types of feedback users can provide on workflows"""
    APPROVE = "approve"
    REJECT = "reject"
    MODIFY = "modify"
    REPORT_ISSUE = "report_issue"


class WorkflowQuality(Enum):
    """Quality assessment of generated workflows"""
    EXCELLENT = "excellent"
    GOOD = "good"
    FAIR = "fair"
    POOR = "poor"


@dataclass
class FeedbackData:
    """Structure for user feedback on workflows"""
    workflow_id: str
    feedback_type: FeedbackType
    quality_rating: Optional[WorkflowQuality]
    accuracy_score: Optional[float]  # 0.0 to 1.0
    user_comments: Optional[str]
    suggested_improvements: Optional[Dict[str, Any]]
    execution_success: bool = True
    response_time_ms: Optional[int] = None


@dataclass
class AccuracyMetrics:
    """Metrics for workflow generation accuracy"""
    total_generated: int
    approved_count: int
    rejected_count: int
    modified_count: int
    accuracy_rate: float
    user_satisfaction: float
    avg_quality_score: float
    improvement_trend: float


class FeedbackProcessor:
    """
    Processes user feedback to improve workflow generation accuracy

    Key Features:
    - Collects and analyzes user feedback on generated workflows
    - Updates pattern detection weights based on success/failure rates
    - Learns from user modifications to improve future suggestions
    - Tracks accuracy metrics and improvement trends
    - Provides recommendations for pattern refinement
    """

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session
        # Minimum feedback items before adjusting weights
        self.min_feedback_threshold = 5
        self.accuracy_target = 0.85  # Target accuracy rate (85%)

    async def process_feedback(
        self,
        feedback: FeedbackData,
        user_id: str
    ) -> Dict[str, Any]:
        """
        Process user feedback on a generated workflow

        Args:
            feedback: User feedback data
            user_id: ID of user providing feedback

        Returns:
            Processing results and updated metrics
        """
        start_time = datetime.now()

        try:
            # Store feedback in database
            await self._store_feedback(feedback, user_id)

            # Update pattern weights based on feedback
            pattern_updates = await self._update_pattern_weights(feedback)

            # Learn from user modifications
            if feedback.feedback_type == FeedbackType.MODIFY:
                await self._learn_from_modifications(feedback)

            # Update accuracy metrics
            metrics = await self._update_accuracy_metrics(feedback.workflow_id)

            # Check if pattern needs refinement
            refinement_needed = await self._check_pattern_refinement(
                feedback.workflow_id
            )

            processing_time = (
                (datetime.now() - start_time).total_seconds() * 1000
            )

            # Constitutional compliance: <200ms response time
            if processing_time > 200:
                logger.warning(
                    f"Feedback processing took {processing_time}ms - "
                    "exceeds 200ms target"
                )

            return {
                "success": True,
                "processing_time_ms": processing_time,
                "pattern_updates": pattern_updates,
                "accuracy_metrics": metrics,
                "refinement_needed": refinement_needed,
                "feedback_id": f"fb_{int(datetime.now().timestamp())}"
            }

        except Exception as e:
            logger.error(f"Error processing feedback: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "processing_time_ms": (
                    (datetime.now() - start_time).total_seconds() * 1000
                )
            }

    async def _store_feedback(
        self, feedback: FeedbackData, user_id: str
    ) -> None:
        """Store feedback data in database"""
        try:
            # Update the adaptive workflow with feedback
            stmt = update(AdaptiveWorkflow).where(
                AdaptiveWorkflow.id == feedback.workflow_id
            ).values(
                feedback_type=feedback.feedback_type.value,
                quality_rating=(
                    feedback.quality_rating.value
                    if feedback.quality_rating else None
                ),
                accuracy_score=feedback.accuracy_score,
                user_comments=feedback.user_comments,
                execution_success=feedback.execution_success,
                feedback_timestamp=datetime.now(),
                user_id=user_id
            )

            await self.db_session.execute(stmt)
            await self.db_session.commit()

        except Exception as e:
            await self.db_session.rollback()
            logger.error(f"Error storing feedback: {str(e)}")
            raise

    async def _update_pattern_weights(
        self, feedback: FeedbackData
    ) -> Dict[str, float]:
        """Update pattern detection weights based on feedback"""
        try:
            # Get the workflow and its associated pattern
            workflow_stmt = select(AdaptiveWorkflow).where(
                AdaptiveWorkflow.id == feedback.workflow_id
            )
            workflow_result = await self.db_session.execute(workflow_stmt)
            workflow = workflow_result.scalar_one_or_none()

            if not workflow or not workflow.pattern_id:
                return {}

            # Get current pattern
            pattern_stmt = select(WorkflowPattern).where(
                WorkflowPattern.id == workflow.pattern_id
            )
            pattern_result = await self.db_session.execute(pattern_stmt)
            pattern = pattern_result.scalar_one_or_none()

            if not pattern:
                return {}

            # Calculate weight adjustment based on feedback
            weight_adjustment = self._calculate_weight_adjustment(feedback)

            # Update pattern confidence based on feedback
            new_confidence = max(
                0.1, min(1.0, pattern.confidence + weight_adjustment)
            )

            update_stmt = update(WorkflowPattern).where(
                WorkflowPattern.id == pattern.id
            ).values(
                confidence=new_confidence,
                last_updated=datetime.now()
            )

            await self.db_session.execute(update_stmt)
            await self.db_session.commit()

            return {
                "pattern_id": pattern.id,
                "old_confidence": pattern.confidence,
                "new_confidence": new_confidence,
                "adjustment": weight_adjustment
            }

        except Exception as e:
            await self.db_session.rollback()
            logger.error(f"Error updating pattern weights: {str(e)}")
            return {}

    def _calculate_weight_adjustment(self, feedback: FeedbackData) -> float:
        """Calculate how much to adjust pattern weight based on feedback"""
        base_adjustment = 0.05  # Base adjustment amount

        if feedback.feedback_type == FeedbackType.APPROVE:
            adjustment = base_adjustment
        elif feedback.feedback_type == FeedbackType.REJECT:
            adjustment = -base_adjustment * 2  # Penalize more for rejections
        elif feedback.feedback_type == FeedbackType.MODIFY:
            adjustment = base_adjustment * 0.5  # Smaller positive adjustment
        else:  # REPORT_ISSUE
            adjustment = -base_adjustment

        # Adjust based on accuracy score if provided
        if feedback.accuracy_score is not None:
            # -1 to 1 range
            accuracy_multiplier = (feedback.accuracy_score - 0.5) * 2
            adjustment *= accuracy_multiplier

        # Adjust based on quality rating
        if feedback.quality_rating:
            quality_multipliers = {
                WorkflowQuality.EXCELLENT: 1.5,
                WorkflowQuality.GOOD: 1.0,
                WorkflowQuality.FAIR: 0.5,
                WorkflowQuality.POOR: -0.5
            }
            adjustment *= quality_multipliers[feedback.quality_rating]

        return adjustment

    async def _learn_from_modifications(self, feedback: FeedbackData) -> None:
        """Learn from user modifications to improve future suggestions"""
        if not feedback.suggested_improvements:
            return

        try:
            # Extract common modification patterns
            modifications = feedback.suggested_improvements

            # This could be expanded to create new patterns or update
            # existing ones
            # based on the types of modifications users commonly make
            logger.info(f"Learning from modifications: {modifications}")

            # TODO: Implement machine learning component to identify
            # common modification patterns and incorporate them into
            # future workflow generation

        except Exception as e:
            logger.error(f"Error learning from modifications: {str(e)}")

    async def _update_accuracy_metrics(
        self, workflow_id: str
    ) -> AccuracyMetrics:
        """Update and return current accuracy metrics"""
        try:
            # Get all workflows with feedback in the last 30 days
            thirty_days_ago = datetime.now() - timedelta(days=30)

            stmt = select(AdaptiveWorkflow).where(
                AdaptiveWorkflow.feedback_timestamp >= thirty_days_ago,
                AdaptiveWorkflow.feedback_type.isnot(None)
            )

            result = await self.db_session.execute(stmt)
            workflows = result.scalars().all()

            if not workflows:
                return AccuracyMetrics(0, 0, 0, 0, 0.0, 0.0, 0.0, 0.0)

            # Calculate metrics
            total_generated = len(workflows)
            approved_count = sum(
                1 for w in workflows if w.feedback_type == "approve"
            )
            rejected_count = sum(
                1 for w in workflows if w.feedback_type == "reject"
            )
            modified_count = sum(
                1 for w in workflows if w.feedback_type == "modify"
            )

            accuracy_rate = (
                (approved_count + modified_count * 0.5) / total_generated
            )

            # Calculate average quality score
            quality_scores = []
            quality_map = {"excellent": 4, "good": 3, "fair": 2, "poor": 1}

            for workflow in workflows:
                if workflow.quality_rating:
                    quality_scores.append(
                        quality_map.get(workflow.quality_rating, 2)
                    )

            avg_quality_score = (
                sum(quality_scores) / len(quality_scores)
                if quality_scores else 2.0
            )
            user_satisfaction = avg_quality_score / 4.0  # Normalize to 0-1

            # Calculate improvement trend (compare with previous period)
            improvement_trend = await self._calculate_improvement_trend()

            return AccuracyMetrics(
                total_generated=total_generated,
                approved_count=approved_count,
                rejected_count=rejected_count,
                modified_count=modified_count,
                accuracy_rate=accuracy_rate,
                user_satisfaction=user_satisfaction,
                avg_quality_score=avg_quality_score,
                improvement_trend=improvement_trend
            )

        except Exception as e:
            logger.error(f"Error updating accuracy metrics: {str(e)}")
            return AccuracyMetrics(0, 0, 0, 0, 0.0, 0.0, 0.0, 0.0)

    async def _calculate_improvement_trend(self) -> float:
        """Calculate the improvement trend over time"""
        try:
            # Compare accuracy in last 15 days vs previous 15 days
            now = datetime.now()
            mid_point = now - timedelta(days=15)
            thirty_days_ago = now - timedelta(days=30)

            # Recent period accuracy
            recent_stmt = select(AdaptiveWorkflow).where(
                AdaptiveWorkflow.feedback_timestamp >= mid_point,
                AdaptiveWorkflow.feedback_type.isnot(None)
            )
            recent_result = await self.db_session.execute(recent_stmt)
            recent_workflows = recent_result.scalars().all()

            # Previous period accuracy
            previous_stmt = select(AdaptiveWorkflow).where(
                AdaptiveWorkflow.feedback_timestamp >= thirty_days_ago,
                AdaptiveWorkflow.feedback_timestamp < mid_point,
                AdaptiveWorkflow.feedback_type.isnot(None)
            )
            previous_result = await self.db_session.execute(previous_stmt)
            previous_workflows = previous_result.scalars().all()

            if not recent_workflows or not previous_workflows:
                return 0.0

            # Calculate accuracy for each period
            recent_accuracy = self._calculate_period_accuracy(recent_workflows)
            previous_accuracy = self._calculate_period_accuracy(
                previous_workflows
            )

            # Return improvement trend (-1 to 1)
            if previous_accuracy == 0:
                return 0.0

            return (recent_accuracy - previous_accuracy) / previous_accuracy

        except Exception as e:
            logger.error(f"Error calculating improvement trend: {str(e)}")
            return 0.0

    def _calculate_period_accuracy(
        self, workflows: List[AdaptiveWorkflow]
    ) -> float:
        """Calculate accuracy for a specific period"""
        if not workflows:
            return 0.0

        approved = sum(1 for w in workflows if w.feedback_type == "approve")
        modified = sum(1 for w in workflows if w.feedback_type == "modify")
        total = len(workflows)

        return (approved + modified * 0.5) / total

    async def _check_pattern_refinement(self, workflow_id: str) -> bool:
        """Check if pattern needs refinement based on feedback patterns"""
        try:
            # Get the workflow and its pattern
            workflow_stmt = select(AdaptiveWorkflow).where(
                AdaptiveWorkflow.id == workflow_id
            )
            workflow_result = await self.db_session.execute(workflow_stmt)
            workflow = workflow_result.scalar_one_or_none()

            if not workflow or not workflow.pattern_id:
                return False

            # Check recent feedback for this pattern
            recent_feedback_stmt = select(AdaptiveWorkflow).where(
                AdaptiveWorkflow.pattern_id == workflow.pattern_id,
                AdaptiveWorkflow.feedback_timestamp >= (
                    datetime.now() - timedelta(days=7)
                ),
                AdaptiveWorkflow.feedback_type.isnot(None)
            )

            result = await self.db_session.execute(recent_feedback_stmt)
            recent_workflows = result.scalars().all()

            if len(recent_workflows) < self.min_feedback_threshold:
                return False

            # Calculate recent accuracy
            recent_accuracy = self._calculate_period_accuracy(recent_workflows)

            # Pattern needs refinement if accuracy is below target
            return recent_accuracy < self.accuracy_target

        except Exception as e:
            logger.error(f"Error checking pattern refinement: {str(e)}")
            return False

    async def get_feedback_summary(
        self,
        pattern_id: Optional[str] = None,
        days: int = 30
    ) -> Dict[str, Any]:
        """Get summary of feedback for analysis"""
        try:
            cutoff_date = datetime.now() - timedelta(days=days)

            stmt = select(AdaptiveWorkflow).where(
                AdaptiveWorkflow.feedback_timestamp >= cutoff_date,
                AdaptiveWorkflow.feedback_type.isnot(None)
            )

            if pattern_id:
                stmt = stmt.where(AdaptiveWorkflow.pattern_id == pattern_id)

            result = await self.db_session.execute(stmt)
            workflows = result.scalars().all()

            if not workflows:
                return {"message": "No feedback data available"}

            # Generate summary statistics
            feedback_counts = {}
            quality_counts = {}

            for workflow in workflows:
                feedback_counts[workflow.feedback_type] = (
                    feedback_counts.get(workflow.feedback_type, 0) + 1
                )
                if workflow.quality_rating:
                    quality_counts[workflow.quality_rating] = (
                        quality_counts.get(workflow.quality_rating, 0) + 1
                    )

            metrics = await self._update_accuracy_metrics(workflows[0].id)

            return {
                "period_days": days,
                "total_feedback": len(workflows),
                "feedback_breakdown": feedback_counts,
                "quality_breakdown": quality_counts,
                "accuracy_metrics": metrics,
                "pattern_id": pattern_id
            }

        except Exception as e:
            logger.error(f"Error getting feedback summary: {str(e)}")
            return {"error": str(e)}

    async def get_improvement_recommendations(self) -> List[Dict[str, Any]]:
        """Get recommendations for improving workflow generation accuracy"""
        try:
            recommendations = []

            # Get current metrics
            # Will calculate overall metrics
            metrics = await self._update_accuracy_metrics("dummy_id")

            # Accuracy-based recommendations
            if metrics.accuracy_rate < self.accuracy_target:
                recommendations.append({
                    "type": "accuracy_improvement",
                    "priority": "high",
                    "message": f"Current accuracy ({metrics.accuracy_rate:.2%}) is below target ({self.accuracy_target:.2%})",
                    "suggestion": "Review rejected workflows and refine pattern detection algorithms"
                })

            # Quality-based recommendations
            if metrics.avg_quality_score < 3.0:  # Less than "good"
                recommendations.append({
                    "type": "quality_improvement",
                    "priority": "medium",
                    "message": f"Average quality score ({metrics.avg_quality_score:.1f}/4.0) could be improved",
                    "suggestion": "Analyze user modifications to identify common improvement patterns"
                })

            # Trend-based recommendations
            if metrics.improvement_trend < -0.1:  # Declining by more than 10%
                recommendations.append({
                    "type": "declining_performance",
                    "priority": "high",
                    "message": f"Performance declining by {abs(metrics.improvement_trend):.1%}",
                    "suggestion": "Investigate recent pattern changes and user behavior shifts"
                })

            return recommendations

        except Exception as e:
            logger.error(
                f"Error getting improvement recommendations: {str(e)}"
            )
            return [{"type": "error", "message": str(e)}]
