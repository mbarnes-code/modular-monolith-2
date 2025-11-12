"""
Performance Validation API Endpoints

Provides REST API access to domain performance validation system.
Supports constitutional compliance monitoring and validation orchestration.
"""

from datetime import datetime
from typing import Any, Dict, List, Optional

from apps.jane_orchestrator.src.data.models.performance_metrics import \
    DomainType
from apps.jane_orchestrator.src.services.performance.validation_service import \
    PerformanceValidationService
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from libs.shared.data.database import get_db_session
from libs.shared.logging import get_logger
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

logger = get_logger(__name__)

# Create router
performance_router = APIRouter(
    prefix="/api/performance",
    tags=["performance", "validation", "constitutional"]
)


# Request/Response Models
class ValidationRequest(BaseModel):
    """Request model for domain validation"""
    domains: Optional[List[str]] = Field(
        default=None,
        description="Specific domains to validate (default: all)"
    )
    parallel: bool = Field(
        default=True,
        description="Whether to run validations in parallel"
    )
    test_tools: Optional[List[str]] = Field(
        default=None,
        description="Specific tools to test (domain-specific)"
    )
    triggered_by_user: Optional[str] = Field(
        default=None,
        description="User who triggered the validation"
    )


class ValidationResponse(BaseModel):
    """Response model for validation results"""
    validation_id: str
    status: str
    domains_tested: int
    domains_passed: int
    domains_failed: int
    total_violations: int
    total_warnings: int
    constitutional_compliance: bool
    started_at: str
    completed_at: Optional[str]
    domain_details: Dict[str, Any]
    recommendations: List[Dict[str, Any]]


class MetricsQuery(BaseModel):
    """Query model for performance metrics"""
    domain: Optional[str] = None
    tool_name: Optional[str] = None
    metric_type: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    limit: int = Field(default=100, le=1000)
    violations_only: bool = False


# API Endpoints

@performance_router.post("/validate", response_model=ValidationResponse)
async def validate_domains(
    request: ValidationRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db_session)
):
    """
    Trigger domain performance validation

    Validates constitutional performance requirements across specified domains.
    Runs validation in background and returns immediate response with tracking ID.
    """
    try:
        service = PerformanceValidationService(db)

        # Parse domains
        domains = None
        if request.domains:
            try:
                domains = [DomainType(domain) for domain in request.domains]
            except ValueError as e:
                raise HTTPException(
                    status_code=400,
                    detail=f"Invalid domain: {e}"
                )

        # Start validation
        if request.parallel:
            validation_results = await service.validate_all_domains(
                triggered_by="api",
                triggered_by_user=request.triggered_by_user,
                domains=domains,
                parallel=True
            )
        else:
            validation_results = await service.validate_all_domains(
                triggered_by="api",
                triggered_by_user=request.triggered_by_user,
                domains=domains,
                parallel=False
            )

        # Generate summary
        summary = service.get_validation_summary(validation_results)

        # Create response
        response = ValidationResponse(
            validation_id=f"validation_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}",
            status=summary["overall_status"],
            domains_tested=summary["domains_tested"],
            domains_passed=summary["domains_passed"],
            domains_failed=summary["domains_failed"],
            total_violations=summary["total_violations"],
            total_warnings=summary["total_warnings"],
            constitutional_compliance=summary["constitutional_compliance"],
            started_at=summary["timestamp"],
            completed_at=summary["timestamp"],
            domain_details=summary["domain_details"],
            recommendations=summary["recommendations"]
        )

        logger.info(
            f"Domain validation completed: {response.status} "
            f"({response.domains_passed}/{response.domains_tested} passed)"
        )

        return response

    except Exception as e:
        logger.error(f"Domain validation failed: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Validation failed: {str(e)}"
        )


@performance_router.post("/validate/{domain}")
async def validate_single_domain(
    domain: str,
    test_tools: Optional[List[str]] = None,
    triggered_by_user: Optional[str] = None,
    db: Session = Depends(get_db_session)
):
    """
    Validate a single domain

    Validates performance requirements for a specific domain with optional
    tool filtering.
    """
    try:
        # Parse domain
        try:
            domain_enum = DomainType(domain)
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid domain: {domain}. Valid domains: {[d.value for d in DomainType]}"
            )

        service = PerformanceValidationService(db)
        validation = await service.validate_single_domain(
            domain=domain_enum,
            triggered_by="api",
            triggered_by_user=triggered_by_user,
            test_tools=test_tools
        )

        return {
            "domain": domain,
            "validation_run_id": validation.validation_run_id,
            "status": validation.status,
            "violations_found": validation.violations_found,
            "warnings_found": validation.warnings_found,
            "tools_tested": validation.tools_tested,
            "pass_rate": validation.pass_rate,
            "duration_ms": validation.duration_ms,
            "summary": validation.summary,
            "recommendations": validation.recommendations,
            "constitutional_compliant": validation.violations_found == 0
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Single domain validation failed: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Validation failed: {str(e)}"
        )


@performance_router.get("/status")
async def get_validation_status(db: Session = Depends(get_db_session)):
    """
    Get current performance validation status

    Returns overview of recent validation results and system health.
    """
    try:
        # This would query recent validation runs from database
        # For now, returning mock status

        return {
            "system_status": "healthy",
            "last_validation": datetime.utcnow().isoformat(),
            "constitutional_compliance": {
                "security": {"threshold_ms": 1000, "status": "compliant"},
                "productivity": {"threshold_ms": 2000, "status": "compliant"},
                "mtg": {"threshold_ms": 3000, "status": "compliant"},
                "infrastructure": {"threshold_ms": 5000, "status": "compliant"}
            },
            "monitoring_active": True,
            "alerts_count": 0
        }

    except Exception as e:
        logger.error(f"Status check failed: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Status check failed: {str(e)}"
        )


@performance_router.get("/metrics")
async def get_performance_metrics(
    query: MetricsQuery = Depends(),
    db: Session = Depends(get_db_session)
):
    """
    Query performance metrics

    Retrieves performance metrics with filtering and pagination.
    """
    try:
        # This would query PerformanceMetrics from database
        # For now, returning mock metrics

        return {
            "metrics": [],
            "total_count": 0,
            "query_parameters": query.dict(),
            "constitutional_thresholds": {
                "security": 1000,
                "productivity": 2000,
                "mtg": 3000,
                "infrastructure": 5000,
                "ui_response": 200
            }
        }

    except Exception as e:
        logger.error(f"Metrics query failed: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Metrics query failed: {str(e)}"
        )


@performance_router.get("/thresholds")
async def get_performance_thresholds(db: Session = Depends(get_db_session)):
    """
    Get constitutional performance thresholds

    Returns the current constitutional performance requirements for all domains.
    """
    try:
        return {
            "constitutional_thresholds": {
                "security": {
                    "response_time_ms": 1000,
                    "description": "Threat analysis criticality requirement"
                },
                "productivity": {
                    "response_time_ms": 2000,
                    "description": "Task management workflow requirement"
                },
                "mtg": {
                    "response_time_ms": 3000,
                    "description": "Game analysis complexity tolerance"
                },
                "infrastructure": {
                    "response_time_ms": 5000,
                    "description": "System operations tolerance"
                }
            },
            "universal_thresholds": {
                "ui_response_ms": 200,
                "api_latency_p95_ms": 500,
                "websocket_latency_ms": 250
            },
            "last_updated": datetime.utcnow().isoformat()
        }

    except Exception as e:
        logger.error(f"Thresholds query failed: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Thresholds query failed: {str(e)}"
        )


@performance_router.get("/health")
async def health_check():
    """
    Performance validation service health check

    Returns basic health status for monitoring systems.
    """
    return {
        "status": "healthy",
        "service": "performance_validation",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0"
    }
