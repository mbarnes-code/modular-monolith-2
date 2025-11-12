"""
API endpoints for adaptive workflow management.

This module provides REST endpoints for managing n8n adaptive workflows,
including pattern detection, workflow generation, and validation.
"""

from datetime import datetime
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from ...data.database import get_db
from ...data.models.adaptive_workflow import AdaptiveWorkflow
from ...data.models.workflow_pattern import WorkflowPattern
from ...services.pattern_detection_service import PatternDetectionService
from ...services.workflow_generation_service import WorkflowGenerationService
from ...services.workflow_validation_service import WorkflowValidationService

router = APIRouter(prefix="/adaptive-workflows", tags=["adaptive-workflows"])


# Pydantic models for API requests/responses
class PatternAnalysisRequest(BaseModel):
    """Request model for pattern analysis."""
    user_id: str
    lookback_days: int = Field(default=30, ge=1, le=365)
    force_reanalysis: bool = False


class PatternResponse(BaseModel):
    """Response model for workflow patterns."""
    id: str
    pattern_hash: str
    pattern_name: str
    description: str
    category: str
    occurrence_count: int
    confidence_score: float
    is_ready_for_automation: bool
    tool_sequence: List[str]
    created_at: str
    last_seen: str


class WorkflowGenerationRequest(BaseModel):
    """Request model for workflow generation."""
    pattern_id: str
    workflow_name: Optional[str] = None
    auto_activate: bool = False


class AdaptiveWorkflowResponse(BaseModel):
    """Response model for adaptive workflows."""
    id: str
    workflow_id: str
    workflow_name: str
    description: str
    category: str
    is_active: bool
    is_validated: bool
    generation_confidence: float
    total_executions: int
    success_rate: float
    efficiency_score: float
    created_at: str


class ValidationRequest(BaseModel):
    """Request model for workflow validation."""
    workflow_id: str
    test_historical_data: bool = True
    max_test_scenarios: int = Field(default=10, ge=1, le=50)


class ValidationResponse(BaseModel):
    """Response model for validation results."""
    is_valid: bool
    success_rate: float
    test_count: int
    average_execution_time: float
    errors: List[str]
    warnings: List[str]
    recommendation: str


@router.post("/analyze-patterns", response_model=List[PatternResponse])
async def analyze_user_patterns(
    request: PatternAnalysisRequest,
    db: Session = Depends(get_db)
) -> List[Dict[str, Any]]:
    """
    Analyze user behavior patterns for workflow automation opportunities.

    This endpoint analyzes user request history to identify recurring patterns
    that meet the constitutional requirement of 3+ occurrences.
    """
    try:
        pattern_service = PatternDetectionService(db)

        # Analyze patterns
        detected_patterns = pattern_service.analyze_user_patterns(
            user_id=request.user_id,
            lookback_days=request.lookback_days
        )

        # Convert to response format
        pattern_responses = []
        for pattern in detected_patterns:
            response = PatternResponse(
                id=pattern.id,
                pattern_hash=pattern.pattern_hash,
                pattern_name=pattern.pattern_name,
                description=pattern.description or "",
                category=pattern.category,
                occurrence_count=pattern.occurrence_count,
                confidence_score=pattern.confidence_score,
                is_ready_for_automation=pattern.is_ready_for_automation(),
                tool_sequence=pattern.tool_sequence or [],
                created_at=pattern.created_at.isoformat(),
                last_seen=pattern.last_seen.isoformat() if pattern.last_seen else ""
            )
            pattern_responses.append(response)

        # Commit any new patterns found
        db.commit()

        return [response.dict() for response in pattern_responses]

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Failed to analyze patterns: {str(e)}"
        )


@router.get("/patterns/ready", response_model=List[PatternResponse])
async def get_patterns_ready_for_automation(
    user_id: str,
    db: Session = Depends(get_db)
) -> List[Dict[str, Any]]:
    """Get patterns that are ready for n8n workflow generation."""
    try:
        pattern_service = PatternDetectionService(db)

        ready_patterns = pattern_service.get_patterns_ready_for_automation(
            user_id)

        pattern_responses = []
        for pattern in ready_patterns:
            response = PatternResponse(
                id=pattern.id,
                pattern_hash=pattern.pattern_hash,
                pattern_name=pattern.pattern_name,
                description=pattern.description or "",
                category=pattern.category,
                occurrence_count=pattern.occurrence_count,
                confidence_score=pattern.confidence_score,
                is_ready_for_automation=pattern.is_ready_for_automation(),
                tool_sequence=pattern.tool_sequence or [],
                created_at=pattern.created_at.isoformat(),
                last_seen=pattern.last_seen.isoformat() if pattern.last_seen else ""
            )
            pattern_responses.append(response)

        return [response.dict() for response in pattern_responses]

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get ready patterns: {str(e)}"
        )


@router.post("/generate", response_model=AdaptiveWorkflowResponse)
async def generate_workflow_from_pattern(
    request: WorkflowGenerationRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Generate an n8n workflow from a detected pattern.

    Creates a new adaptive workflow that can be validated and deployed.
    """
    try:
        # Get the pattern
        pattern = db.query(WorkflowPattern).filter(
            WorkflowPattern.id == request.pattern_id
        ).first()

        if not pattern:
            raise HTTPException(
                status_code=404,
                detail="Pattern not found"
            )

        if not pattern.is_ready_for_automation():
            raise HTTPException(
                status_code=400,
                detail="Pattern is not ready for automation"
            )

        # Generate workflow
        generation_service = WorkflowGenerationService(db)
        adaptive_workflow = generation_service.generate_workflow_from_pattern(
            pattern)

        if not adaptive_workflow:
            raise HTTPException(
                status_code=500,
                detail="Failed to generate workflow"
            )

        # Override workflow name if provided
        if request.workflow_name:
            adaptive_workflow.workflow_name = request.workflow_name

        # Set active status
        adaptive_workflow.is_active = request.auto_activate

        db.commit()

        # Schedule validation in background if requested
        if not request.auto_activate:
            background_tasks.add_task(
                validate_workflow_background,
                adaptive_workflow.id,
                db
            )

        # Create response
        response = AdaptiveWorkflowResponse(
            id=adaptive_workflow.id,
            workflow_id=adaptive_workflow.workflow_id,
            workflow_name=adaptive_workflow.workflow_name,
            description=adaptive_workflow.description or "",
            category=adaptive_workflow.category,
            is_active=adaptive_workflow.is_active,
            is_validated=adaptive_workflow.is_validated,
            generation_confidence=adaptive_workflow.generation_confidence,
            total_executions=adaptive_workflow.total_executions,
            success_rate=adaptive_workflow.calculate_success_rate(),
            efficiency_score=adaptive_workflow.efficiency_score,
            created_at=adaptive_workflow.created_at.isoformat()
        )

        return response.dict()

    except HTTPException:
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate workflow: {str(e)}"
        )


@router.post("/validate", response_model=ValidationResponse)
async def validate_workflow(
    request: ValidationRequest,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Validate a generated workflow using historical data.

    Tests the workflow against historical scenarios to ensure correctness.
    """
    try:
        # Get the workflow
        workflow = db.query(AdaptiveWorkflow).filter(
            AdaptiveWorkflow.workflow_id == request.workflow_id
        ).first()

        if not workflow:
            raise HTTPException(
                status_code=404,
                detail="Workflow not found"
            )

        # Validate workflow
        validation_service = WorkflowValidationService(db)
        validation_result = await validation_service.validate_workflow(workflow)

        # Update workflow validation status
        workflow.is_validated = validation_result.is_valid
        db.commit()

        # Create response
        response = ValidationResponse(
            is_valid=validation_result.is_valid,
            success_rate=validation_result.success_rate,
            test_count=validation_result.test_count,
            average_execution_time=validation_result.execution_time,
            errors=validation_result.errors,
            warnings=validation_result.warnings,
            recommendation=(
                "Workflow is ready for deployment" if validation_result.is_valid
                else "Workflow needs improvements before deployment"
            )
        )

        return response.dict()

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to validate workflow: {str(e)}"
        )


@router.get("/workflows", response_model=List[AdaptiveWorkflowResponse])
async def get_adaptive_workflows(
    user_id: str,
    category: Optional[str] = None,
    is_active: Optional[bool] = None,
    is_validated: Optional[bool] = None,
    limit: int = Field(default=50, ge=1, le=200),
    db: Session = Depends(get_db)
) -> List[Dict[str, Any]]:
    """Get adaptive workflows with optional filtering."""
    try:
        query = db.query(AdaptiveWorkflow).filter(
            AdaptiveWorkflow.user_id == user_id
        )

        # Apply filters
        if category:
            query = query.filter(AdaptiveWorkflow.category == category)
        if is_active is not None:
            query = query.filter(AdaptiveWorkflow.is_active == is_active)
        if is_validated is not None:
            query = query.filter(AdaptiveWorkflow.is_validated == is_validated)

        workflows = query.limit(limit).all()

        # Convert to response format
        workflow_responses = []
        for workflow in workflows:
            response = AdaptiveWorkflowResponse(
                id=workflow.id,
                workflow_id=workflow.workflow_id,
                workflow_name=workflow.workflow_name,
                description=workflow.description or "",
                category=workflow.category,
                is_active=workflow.is_active,
                is_validated=workflow.is_validated,
                generation_confidence=workflow.generation_confidence,
                total_executions=workflow.total_executions,
                success_rate=workflow.calculate_success_rate(),
                efficiency_score=workflow.efficiency_score,
                created_at=workflow.created_at.isoformat()
            )
            workflow_responses.append(response)

        return [response.dict() for response in workflow_responses]

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get workflows: {str(e)}"
        )


@router.put("/workflows/{workflow_id}/activate")
async def activate_workflow(
    workflow_id: str,
    db: Session = Depends(get_db)
) -> Dict[str, str]:
    """Activate a validated workflow for automatic execution."""
    try:
        workflow = db.query(AdaptiveWorkflow).filter(
            AdaptiveWorkflow.workflow_id == workflow_id
        ).first()

        if not workflow:
            raise HTTPException(
                status_code=404,
                detail="Workflow not found"
            )

        if not workflow.is_validated:
            raise HTTPException(
                status_code=400,
                detail="Workflow must be validated before activation"
            )

        workflow.is_active = True
        db.commit()

        return {"message": "Workflow activated successfully"}

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Failed to activate workflow: {str(e)}"
        )


@router.put("/workflows/{workflow_id}/deactivate")
async def deactivate_workflow(
    workflow_id: str,
    db: Session = Depends(get_db)
) -> Dict[str, str]:
    """Deactivate a workflow to stop automatic execution."""
    try:
        workflow = db.query(AdaptiveWorkflow).filter(
            AdaptiveWorkflow.workflow_id == workflow_id
        ).first()

        if not workflow:
            raise HTTPException(
                status_code=404,
                detail="Workflow not found"
            )

        workflow.deactivate()
        db.commit()

        return {"message": "Workflow deactivated successfully"}

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Failed to deactivate workflow: {str(e)}"
        )


@router.get("/workflows/{workflow_id}/export")
async def export_workflow_for_n8n(
    workflow_id: str,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Export workflow in n8n-compatible format."""
    try:
        workflow = db.query(AdaptiveWorkflow).filter(
            AdaptiveWorkflow.workflow_id == workflow_id
        ).first()

        if not workflow:
            raise HTTPException(
                status_code=404,
                detail="Workflow not found"
            )

        generation_service = WorkflowGenerationService(db)
        n8n_workflow = generation_service.export_workflow_for_n8n(workflow)

        return n8n_workflow

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to export workflow: {str(e)}"
        )


@router.delete("/workflows/{workflow_id}")
async def delete_workflow(
    workflow_id: str,
    db: Session = Depends(get_db)
) -> Dict[str, str]:
    """Delete an adaptive workflow."""
    try:
        workflow = db.query(AdaptiveWorkflow).filter(
            AdaptiveWorkflow.workflow_id == workflow_id
        ).first()

        if not workflow:
            raise HTTPException(
                status_code=404,
                detail="Workflow not found"
            )

        # Deactivate first if active
        if workflow.is_active:
            workflow.deactivate()

        db.delete(workflow)
        db.commit()

        return {"message": "Workflow deleted successfully"}

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Failed to delete workflow: {str(e)}"
        )


# Background task functions
async def validate_workflow_background(
    workflow_id: str,
    db: Session
) -> None:
    """Background task to validate workflow."""
    try:
        workflow = db.query(AdaptiveWorkflow).filter(
            AdaptiveWorkflow.id == workflow_id
        ).first()

        if workflow:
            validation_service = WorkflowValidationService(db)
            validation_result = await validation_service.validate_workflow(workflow)

            workflow.is_validated = validation_result.is_valid
            db.commit()

    except Exception as e:
        # Log error but don't raise in background task
        print(f"Background validation failed: {e}")
        db.rollback()
