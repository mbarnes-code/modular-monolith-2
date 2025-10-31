"""
Workflow Optimization API Endpoints

Performance analysis and optimization for adaptive workflows
based on execution metrics and success patterns.
"""

from typing import List

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from ...data.database import get_db
from ...services.workflow_optimization_service import (
    OptimizationRecommendation, OptimizationResult, PerformanceMetrics,
    WorkflowOptimizationService)

router = APIRouter(prefix="/api/workflow-optimization", tags=["optimization"])


class PerformanceMetricsResponse(BaseModel):
    """Performance metrics response model"""
    workflow_id: str
    execution_count: int
    success_rate: float
    average_execution_time: float
    error_rate: float
    user_satisfaction: float
    automation_efficiency: float
    last_optimization: str | None


class OptimizationRecommendationResponse(BaseModel):
    """Optimization recommendation response model"""
    workflow_id: str
    recommendation_type: str
    description: str
    expected_improvement: float
    priority: str
    implementation_complexity: str
    estimated_time_savings: float


class OptimizationResultResponse(BaseModel):
    """Optimization result response model"""
    workflow_id: str
    optimization_type: str
    success: bool
    improvement_percentage: float
    error_message: str | None


def get_optimization_service(db: Session = Depends(get_db)) -> WorkflowOptimizationService:
    """Get workflow optimization service instance"""
    return WorkflowOptimizationService(db)


@router.get("/metrics/{workflow_id}", response_model=PerformanceMetricsResponse)
async def get_workflow_metrics(
    workflow_id: str,
    days_back: int = 30,
    service: WorkflowOptimizationService = Depends(get_optimization_service)
):
    """Get performance metrics for a specific workflow"""
    try:
        metrics = await service.analyze_workflow_performance(workflow_id, days_back)

        return PerformanceMetricsResponse(
            workflow_id=metrics.workflow_id,
            execution_count=metrics.execution_count,
            success_rate=metrics.success_rate,
            average_execution_time=metrics.average_execution_time,
            error_rate=metrics.error_rate,
            user_satisfaction=metrics.user_satisfaction,
            automation_efficiency=metrics.automation_efficiency,
            last_optimization=metrics.last_optimization.isoformat(
            ) if metrics.last_optimization else None
        )

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error analyzing metrics: {str(e)}")


@router.get("/recommendations/{workflow_id}", response_model=List[OptimizationRecommendationResponse])
async def get_optimization_recommendations(
    workflow_id: str,
    service: WorkflowOptimizationService = Depends(get_optimization_service)
):
    """Get optimization recommendations for a workflow"""
    try:
        recommendations = await service.generate_optimization_recommendations(workflow_id)

        return [
            OptimizationRecommendationResponse(
                workflow_id=rec.workflow_id,
                recommendation_type=rec.recommendation_type,
                description=rec.description,
                expected_improvement=rec.expected_improvement,
                priority=rec.priority,
                implementation_complexity=rec.implementation_complexity,
                estimated_time_savings=rec.estimated_time_savings
            )
            for rec in recommendations
        ]

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error generating recommendations: {str(e)}")


@router.post("/optimize/{workflow_id}", response_model=OptimizationResultResponse)
async def optimize_workflow(
    workflow_id: str,
    optimization_type: str = "auto",
    service: WorkflowOptimizationService = Depends(get_optimization_service)
):
    """
    Optimize a specific workflow

    optimization_type options:
    - auto: Apply best optimizations automatically
    - execution_time: Focus on reducing execution time
    - success_rate: Focus on improving success rate
    - error_handling: Focus on better error handling
    """
    valid_types = ["auto", "execution_time", "success_rate", "error_handling"]

    if optimization_type not in valid_types:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid optimization type. Must be one of: {', '.join(valid_types)}"
        )

    try:
        result = await service.optimize_workflow(workflow_id, optimization_type)

        return OptimizationResultResponse(
            workflow_id=result.workflow_id,
            optimization_type=result.optimization_type,
            success=result.success,
            improvement_percentage=result.improvement_percentage,
            error_message=result.error_message
        )

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error optimizing workflow: {str(e)}")


@router.post("/batch-optimize")
async def batch_optimize_workflows(
    background_tasks: BackgroundTasks,
    min_executions: int = 10,
    max_workflows: int = 10,
    service: WorkflowOptimizationService = Depends(get_optimization_service)
):
    """Batch optimize multiple workflows in the background"""
    if min_executions < 5:
        raise HTTPException(
            status_code=400,
            detail="Minimum executions must be at least 5 for reliable optimization"
        )

    if max_workflows > 50:
        raise HTTPException(
            status_code=400,
            detail="Maximum workflows cannot exceed 50 for batch optimization"
        )

    # Start batch optimization in background
    background_tasks.add_task(
        service.batch_optimize_workflows,
        min_executions,
        max_workflows
    )

    return {
        "message": "Batch optimization started",
        "parameters": {
            "min_executions": min_executions,
            "max_workflows": max_workflows
        },
        "status": "processing"
    }


@router.get("/performance-summary")
async def get_performance_summary(
    service: WorkflowOptimizationService = Depends(get_optimization_service),
    db: Session = Depends(get_db)
):
    """Get overall performance summary for all workflows"""
    from sqlalchemy import func

    from ...data.models.adaptive_workflow import AdaptiveWorkflow

    try:
        # Get active workflows with executions
        active_workflows = db.query(AdaptiveWorkflow)\
            .filter(AdaptiveWorkflow.is_active == True)\
            .filter(func.json_array_length(AdaptiveWorkflow.execution_history) > 0)\
            .all()

        if not active_workflows:
            return {
                "total_workflows": 0,
                "average_success_rate": 0.0,
                "average_execution_time": 0.0,
                "workflows_needing_optimization": 0,
                "optimization_opportunities": []
            }

        # Analyze performance for all workflows
        total_success_rate = 0.0
        total_execution_time = 0.0
        workflows_needing_optimization = 0
        optimization_opportunities = []

        for workflow in active_workflows:
            try:
                metrics = await service.analyze_workflow_performance(str(workflow.id))

                total_success_rate += metrics.success_rate
                total_execution_time += metrics.average_execution_time

                # Check if optimization is needed
                needs_optimization = (
                    metrics.success_rate < 0.8 or
                    metrics.average_execution_time > 20 or
                    metrics.error_rate > 0.2
                )

                if needs_optimization:
                    workflows_needing_optimization += 1

                    # Generate optimization opportunity
                    recommendations = await service.generate_optimization_recommendations(str(workflow.id))
                    if recommendations:
                        top_recommendation = recommendations[0]
                        optimization_opportunities.append({
                            "workflow_id": str(workflow.id),
                            "workflow_name": workflow.name,
                            "current_performance": {
                                "success_rate": metrics.success_rate,
                                "execution_time": metrics.average_execution_time,
                                "error_rate": metrics.error_rate
                            },
                            "top_recommendation": {
                                "type": top_recommendation.recommendation_type,
                                "expected_improvement": top_recommendation.expected_improvement,
                                "priority": top_recommendation.priority
                            }
                        })

            except Exception as e:
                # Skip workflows with analysis errors
                continue

        workflow_count = len(active_workflows)

        return {
            "total_workflows": workflow_count,
            "average_success_rate": total_success_rate / workflow_count if workflow_count > 0 else 0.0,
            "average_execution_time": total_execution_time / workflow_count if workflow_count > 0 else 0.0,
            "workflows_needing_optimization": workflows_needing_optimization,
            # Top 10
            "optimization_opportunities": optimization_opportunities[:10],
            "performance_targets": {
                "target_success_rate": service.TARGET_SUCCESS_RATE,
                "target_execution_time": service.TARGET_EXECUTION_TIME,
                "target_error_rate": service.TARGET_ERROR_RATE
            }
        }

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error generating performance summary: {str(e)}")


@router.get("/health")
async def optimization_health_check(
    service: WorkflowOptimizationService = Depends(get_optimization_service),
    db: Session = Depends(get_db)
):
    """Health check for optimization service"""
    from sqlalchemy import func

    from ...data.models.adaptive_workflow import AdaptiveWorkflow

    try:
        # Count workflows available for optimization
        optimizable_workflows = db.query(func.count(AdaptiveWorkflow.id))\
            .filter(AdaptiveWorkflow.is_active == True)\
            .filter(func.json_array_length(AdaptiveWorkflow.execution_history) >= service.MIN_EXECUTIONS_FOR_OPTIMIZATION)\
            .scalar()

        # Count recently optimized workflows (last 7 days)
        from datetime import datetime, timedelta
        recent_date = datetime.utcnow() - timedelta(days=7)

        recently_optimized = db.query(func.count(AdaptiveWorkflow.id))\
            .filter(AdaptiveWorkflow.last_optimization >= recent_date)\
            .scalar()

        service_healthy = True
        status_message = "Optimization service operational"

        return {
            "healthy": service_healthy,
            "status": status_message,
            "metrics": {
                "optimizable_workflows": optimizable_workflows or 0,
                "recently_optimized": recently_optimized or 0,
                "min_executions_threshold": service.MIN_EXECUTIONS_FOR_OPTIMIZATION,
                "performance_targets": {
                    "success_rate": service.TARGET_SUCCESS_RATE,
                    "execution_time": service.TARGET_EXECUTION_TIME,
                    "error_rate": service.TARGET_ERROR_RATE
                }
            }
        }

    except Exception as e:
        return {
            "healthy": False,
            "status": f"Optimization service error: {str(e)}",
            "metrics": {}
        }
