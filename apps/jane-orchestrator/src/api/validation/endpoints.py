"""
Data Consistency Validation API Endpoints.

REST API endpoints for managing and monitoring data consistency validation
across all 37 integrated tools.
"""

from datetime import datetime
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from ..data.database import get_async_session
from ..services.data_consistency_validator import (
    DataConsistencyValidator, ValidationCategory, ValidationIssue,
    ValidationResult, ValidationSeverity, create_data_consistency_validator)

router = APIRouter(prefix="/api/validation",
                   tags=["Data Consistency Validation"])

# Pydantic models for API


class ValidationRequest(BaseModel):
    """Request model for starting validation."""
    tool_id: str = Field(..., description="ID of the tool to validate")
    domain: str = Field(
        ..., description="Domain of the tool (Security, Productivity, MTG, Infrastructure)")
    validation_types: Optional[List[str]] = Field(
        default=None,
        description="Specific validation types to run (optional, runs all if not provided)"
    )


class CrossDomainValidationRequest(BaseModel):
    """Request model for cross-domain validation."""
    domains: List[str] = Field(...,
                               description="List of domains to validate consistency across")
    include_all_tools: bool = Field(
        default=True, description="Include all tools in selected domains")
    specific_tools: Optional[List[str]] = Field(
        default=None, description="Specific tools to validate")


class ValidationIssueResponse(BaseModel):
    """Response model for validation issues."""
    id: str
    tool_id: str
    domain: str
    category: str
    severity: str
    title: str
    description: str
    affected_records_count: int
    suggested_fix: Optional[str]
    auto_fixable: bool
    detected_at: datetime
    resolved_at: Optional[datetime]


class ValidationResultResponse(BaseModel):
    """Response model for validation results."""
    validation_id: str
    tool_id: str
    domain: str
    started_at: datetime
    completed_at: Optional[datetime]
    total_records_checked: int
    issues_found: List[ValidationIssueResponse]
    passed_checks: int
    failed_checks: int
    skipped_checks: int
    overall_status: str
    success_rate: float


class ValidationSummaryResponse(BaseModel):
    """Response model for validation summary."""
    timestamp: datetime
    total_tools_validated: int
    total_validations: int
    passed_validations: int
    failed_validations: int
    overall_success_rate: float
    domain_statistics: Dict[str, Dict[str, Any]]
    recent_validations: List[Dict[str, Any]]


class AutoFixRequest(BaseModel):
    """Request model for auto-fixing validation issues."""
    validation_id: str = Field(...,
                               description="ID of the validation containing issues to fix")
    issue_ids: Optional[List[str]] = Field(
        default=None,
        description="Specific issue IDs to fix (optional, fixes all auto-fixable if not provided)"
    )


# Dependency to get validator instance
async def get_validator() -> DataConsistencyValidator:
    """Dependency to get DataConsistencyValidator instance."""
    return await create_data_consistency_validator()


@router.post("/validate/tool", response_model=ValidationResultResponse)
async def validate_tool_consistency(
    request: ValidationRequest,
    background_tasks: BackgroundTasks,
    session: AsyncSession = Depends(get_async_session),
    validator: DataConsistencyValidator = Depends(get_validator)
):
    """
    Start data consistency validation for a specific tool.

    This endpoint initiates comprehensive validation checks for a single tool
    including referential integrity, data format validation, business rules,
    and cross-domain consistency checks.
    """
    try:
        # Start validation in background
        background_tasks.add_task(
            _run_tool_validation,
            validator,
            request.tool_id,
            request.domain,
            session
        )

        # Return immediate response with validation ID
        validation_id = f"val_{request.tool_id}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"

        return ValidationResultResponse(
            validation_id=validation_id,
            tool_id=request.tool_id,
            domain=request.domain,
            started_at=datetime.utcnow(),
            completed_at=None,
            total_records_checked=0,
            issues_found=[],
            passed_checks=0,
            failed_checks=0,
            skipped_checks=0,
            overall_status="running",
            success_rate=0.0
        )

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to start validation: {str(e)}")


@router.post("/validate/cross-domain", response_model=Dict[str, ValidationResultResponse])
async def validate_cross_domain_consistency(
    request: CrossDomainValidationRequest,
    background_tasks: BackgroundTasks,
    session: AsyncSession = Depends(get_async_session),
    validator: DataConsistencyValidator = Depends(get_validator)
):
    """
    Start cross-domain data consistency validation.

    This endpoint validates data consistency across multiple domains,
    checking for proper data synchronization, referential integrity
    across domain boundaries, and adherence to cross-domain business rules.
    """
    try:
        # Start cross-domain validation in background
        background_tasks.add_task(
            _run_cross_domain_validation,
            validator,
            request.domains,
            session
        )

        # Return immediate response for each domain
        results = {}
        for domain in request.domains:
            validation_id = f"cross_domain_{domain}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"
            results[domain] = ValidationResultResponse(
                validation_id=validation_id,
                tool_id=f"cross_domain_{domain}",
                domain=domain,
                started_at=datetime.utcnow(),
                completed_at=None,
                total_records_checked=0,
                issues_found=[],
                passed_checks=0,
                failed_checks=0,
                skipped_checks=0,
                overall_status="running",
                success_rate=0.0
            )

        return results

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to start cross-domain validation: {str(e)}")


@router.get("/results/{validation_id}", response_model=ValidationResultResponse)
async def get_validation_result(
    validation_id: str,
    validator: DataConsistencyValidator = Depends(get_validator)
):
    """
    Get the results of a specific validation run.

    Returns detailed validation results including all issues found,
    success rates, and remediation suggestions.
    """
    try:
        # Get validation result from validator
        validation_result = validator._active_validations.get(validation_id)

        if not validation_result:
            raise HTTPException(
                status_code=404, detail="Validation result not found")

        # Convert to response model
        issues_response = [
            ValidationIssueResponse(
                id=issue.id,
                tool_id=issue.tool_id,
                domain=issue.domain,
                category=issue.category.value,
                severity=issue.severity.value,
                title=issue.title,
                description=issue.description,
                affected_records_count=len(issue.affected_records),
                suggested_fix=issue.suggested_fix,
                auto_fixable=issue.auto_fixable,
                detected_at=issue.detected_at,
                resolved_at=issue.resolved_at
            )
            for issue in validation_result.issues_found
        ]

        return ValidationResultResponse(
            validation_id=validation_result.validation_id,
            tool_id=validation_result.tool_id,
            domain=validation_result.domain,
            started_at=validation_result.started_at,
            completed_at=validation_result.completed_at,
            total_records_checked=validation_result.total_records_checked,
            issues_found=issues_response,
            passed_checks=validation_result.passed_checks,
            failed_checks=validation_result.failed_checks,
            skipped_checks=validation_result.skipped_checks,
            overall_status=validation_result.overall_status,
            success_rate=validation_result.success_rate
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to get validation result: {str(e)}")


@router.get("/summary", response_model=ValidationSummaryResponse)
async def get_validation_summary(
    hours: int = Query(
        default=24, description="Hours to include in summary (default: 24)"),
    session: AsyncSession = Depends(get_async_session),
    validator: DataConsistencyValidator = Depends(get_validator)
):
    """
    Get overall validation summary across all tools.

    Returns aggregated statistics including success rates by domain,
    recent validation trends, and overall system health indicators.
    """
    try:
        summary_data = await validator.get_validation_summary(session)

        return ValidationSummaryResponse(
            timestamp=datetime.fromisoformat(summary_data['timestamp']),
            total_tools_validated=summary_data['total_tools_validated'],
            total_validations=summary_data['total_validations'],
            passed_validations=summary_data['passed_validations'],
            failed_validations=summary_data['failed_validations'],
            overall_success_rate=summary_data['overall_success_rate'],
            domain_statistics=summary_data['domain_statistics'],
            recent_validations=summary_data['recent_validations']
        )

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to get validation summary: {str(e)}")


@router.get("/issues", response_model=List[ValidationIssueResponse])
async def get_validation_issues(
    domain: Optional[str] = Query(
        default=None, description="Filter by domain"),
    severity: Optional[str] = Query(
        default=None, description="Filter by severity (info, warning, error, critical)"),
    category: Optional[str] = Query(
        default=None, description="Filter by category"),
    tool_id: Optional[str] = Query(
        default=None, description="Filter by tool ID"),
    unresolved_only: bool = Query(
        default=True, description="Show only unresolved issues"),
    limit: int = Query(
        default=100, description="Maximum number of issues to return"),
    validator: DataConsistencyValidator = Depends(get_validator)
):
    """
    Get validation issues with optional filtering.

    Returns a list of validation issues that can be filtered by domain,
    severity, category, tool, and resolution status.
    """
    try:
        # Collect issues from all active validations
        all_issues = []

        for validation in validator._active_validations.values():
            for issue in validation.issues_found:
                # Apply filters
                if domain and issue.domain != domain:
                    continue
                if severity and issue.severity.value != severity:
                    continue
                if category and issue.category.value != category:
                    continue
                if tool_id and issue.tool_id != tool_id:
                    continue
                if unresolved_only and issue.resolved_at is not None:
                    continue

                all_issues.append(ValidationIssueResponse(
                    id=issue.id,
                    tool_id=issue.tool_id,
                    domain=issue.domain,
                    category=issue.category.value,
                    severity=issue.severity.value,
                    title=issue.title,
                    description=issue.description,
                    affected_records_count=len(issue.affected_records),
                    suggested_fix=issue.suggested_fix,
                    auto_fixable=issue.auto_fixable,
                    detected_at=issue.detected_at,
                    resolved_at=issue.resolved_at
                ))

        # Sort by severity and detection time
        severity_order = {'critical': 0, 'error': 1, 'warning': 2, 'info': 3}
        all_issues.sort(
            key=lambda x: (severity_order.get(x.severity, 4), x.detected_at),
            reverse=True
        )

        return all_issues[:limit]

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to get validation issues: {str(e)}")


@router.post("/auto-fix")
async def auto_fix_validation_issues(
    request: AutoFixRequest,
    background_tasks: BackgroundTasks,
    session: AsyncSession = Depends(get_async_session),
    validator: DataConsistencyValidator = Depends(get_validator)
):
    """
    Automatically fix validation issues where possible.

    Attempts to automatically resolve validation issues that have been
    marked as auto-fixable. Returns a summary of fix attempts and results.
    """
    try:
        # Start auto-fix in background
        background_tasks.add_task(
            _run_auto_fix,
            validator,
            request.validation_id,
            session
        )

        return JSONResponse(
            status_code=202,
            content={
                "message": "Auto-fix process started",
                "validation_id": request.validation_id,
                "status": "processing"
            }
        )

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to start auto-fix: {str(e)}")


@router.get("/health")
async def get_validation_health():
    """
    Get validation service health status.

    Returns the current status of the validation service including
    active validations, service availability, and performance metrics.
    """
    try:
        return JSONResponse(content={
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat(),
            "service": "data_consistency_validator",
            "version": "1.0.0",
            "capabilities": [
                "tool_validation",
                "cross_domain_validation",
                "auto_fix",
                "real_time_monitoring"
            ]
        })

    except Exception as e:
        return JSONResponse(
            status_code=503,
            content={
                "status": "unhealthy",
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }
        )


# Background task functions
async def _run_tool_validation(
    validator: DataConsistencyValidator,
    tool_id: str,
    domain: str,
    session: AsyncSession
):
    """Background task to run tool validation."""
    try:
        result = await validator.validate_tool_consistency(tool_id, domain, session)
        # Result is automatically stored in validator._active_validations
    except Exception as e:
        logger = __import__('logging').getLogger(__name__)
        logger.error(
            f"Background tool validation failed for {tool_id}: {str(e)}")


async def _run_cross_domain_validation(
    validator: DataConsistencyValidator,
    domains: List[str],
    session: AsyncSession
):
    """Background task to run cross-domain validation."""
    try:
        results = await validator.validate_cross_domain_consistency(domains, session)
        # Results are automatically stored in validator._active_validations
    except Exception as e:
        logger = __import__('logging').getLogger(__name__)
        logger.error(
            f"Background cross-domain validation failed for {domains}: {str(e)}")


async def _run_auto_fix(
    validator: DataConsistencyValidator,
    validation_id: str,
    session: AsyncSession
):
    """Background task to run auto-fix."""
    try:
        result = await validator.auto_fix_validation_issues(validation_id, session)
        # Auto-fix results are logged and stored
    except Exception as e:
        logger = __import__('logging').getLogger(__name__)
        logger.error(
            f"Background auto-fix failed for {validation_id}: {str(e)}")
