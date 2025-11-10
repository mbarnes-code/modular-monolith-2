"""
Pattern Monitoring API Endpoints

Real-time pattern detection monitoring with constitutional 3+ occurrence
threshold validation within 7-day window.
"""

from datetime import datetime, timedelta
from typing import List

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from ...data.database import get_db
from ...services.pattern_detection_service import PatternDetectionService
from ...services.pattern_monitoring_service import (MonitoringStats,
                                                    PatternAlert,
                                                    PatternMonitoringService)

router = APIRouter(prefix="/api/pattern-monitoring",
                   tags=["pattern-monitoring"])


class PatternAlertResponse(BaseModel):
    """Pattern alert response model"""
    pattern_id: str
    pattern_signature: str
    occurrence_count: int
    confidence_score: float
    automation_value: float
    first_seen: datetime
    last_seen: datetime
    requests: List[str]
    recommendation: str


class MonitoringStatsResponse(BaseModel):
    """Monitoring statistics response model"""
    active_patterns: int
    qualified_patterns: int
    pending_patterns: int
    total_requests_analyzed: int
    monitoring_uptime_seconds: int
    last_pattern_detected: datetime | None


class MonitoringStatusResponse(BaseModel):
    """Monitoring status response model"""
    is_active: bool
    uptime_seconds: int
    patterns_detected_today: int
    automation_alerts_sent: int


# Global monitoring service instance
monitoring_service: PatternMonitoringService | None = None


def get_monitoring_service(db: Session = Depends(get_db)) -> PatternMonitoringService:
    """Get pattern monitoring service instance"""
    global monitoring_service

    if monitoring_service is None:
        pattern_service = PatternDetectionService(db)
        monitoring_service = PatternMonitoringService(db, pattern_service)

    return monitoring_service


@router.post("/start")
async def start_monitoring(
    background_tasks: BackgroundTasks,
    service: PatternMonitoringService = Depends(get_monitoring_service)
):
    """Start real-time pattern monitoring"""
    if service.monitoring_active:
        raise HTTPException(
            status_code=400,
            detail="Pattern monitoring is already active"
        )

    # Start monitoring in background
    background_tasks.add_task(service.start_monitoring)

    return {
        "message": "Pattern monitoring started",
        "min_occurrences": service.MIN_OCCURRENCES,
        "time_window_days": service.TIME_WINDOW_DAYS
    }


@router.post("/stop")
async def stop_monitoring(
    service: PatternMonitoringService = Depends(get_monitoring_service)
):
    """Stop pattern monitoring"""
    if not service.monitoring_active:
        raise HTTPException(
            status_code=400,
            detail="Pattern monitoring is not active"
        )

    await service.stop_monitoring()

    return {"message": "Pattern monitoring stopped"}


@router.get("/status", response_model=MonitoringStatusResponse)
async def get_monitoring_status(
    service: PatternMonitoringService = Depends(get_monitoring_service)
):
    """Get current monitoring status"""
    stats = await service.get_monitoring_stats()

    uptime_seconds = int(stats.monitoring_uptime.total_seconds())

    # Count patterns detected today
    today = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    patterns_today = len([
        p for p in service.pattern_cache.values()
        if p.created_at >= today
    ])

    return MonitoringStatusResponse(
        is_active=service.monitoring_active,
        uptime_seconds=uptime_seconds,
        patterns_detected_today=patterns_today,
        automation_alerts_sent=len(service.alert_callbacks)
    )


@router.get("/stats", response_model=MonitoringStatsResponse)
async def get_monitoring_stats(
    service: PatternMonitoringService = Depends(get_monitoring_service)
):
    """Get detailed monitoring statistics"""
    stats = await service.get_monitoring_stats()

    return MonitoringStatsResponse(
        active_patterns=stats.active_patterns,
        qualified_patterns=stats.qualified_patterns,
        pending_patterns=stats.pending_patterns,
        total_requests_analyzed=stats.total_requests_analyzed,
        monitoring_uptime_seconds=int(stats.monitoring_uptime.total_seconds()),
        last_pattern_detected=stats.last_pattern_detected
    )


@router.get("/qualified-patterns")
async def get_qualified_patterns(
    service: PatternMonitoringService = Depends(get_monitoring_service)
):
    """Get patterns that meet automation threshold (3+ occurrences in 7 days)"""
    patterns = await service.get_qualified_patterns()

    return {
        "patterns": [
            {
                "id": str(pattern.id),
                "pattern_signature": pattern.pattern_signature,
                "occurrence_count": pattern.occurrence_count,
                "confidence_score": pattern.confidence_score,
                "automation_value": pattern.automation_value,
                "automation_priority": pattern.automation_priority,
                "first_occurrence": pattern.first_occurrence,
                "last_occurrence": pattern.last_occurrence,
                "automation_ready": pattern.automation_ready
            }
            for pattern in patterns
        ],
        "total_count": len(patterns),
        "constitutional_requirements": {
            "min_occurrences": service.MIN_OCCURRENCES,
            "time_window_days": service.TIME_WINDOW_DAYS,
            "description": f"Patterns must occur {service.MIN_OCCURRENCES}+ times within {service.TIME_WINDOW_DAYS} days"
        }
    }


@router.get("/pattern/{pattern_id}/validate")
async def validate_pattern_threshold(
    pattern_id: str,
    service: PatternMonitoringService = Depends(get_monitoring_service)
):
    """Validate specific pattern meets constitutional threshold requirements"""
    is_valid = await service.validate_pattern_threshold(pattern_id)

    if not is_valid:
        return {
            "valid": False,
            "message": f"Pattern does not meet constitutional requirements of {service.MIN_OCCURRENCES}+ occurrences in {service.TIME_WINDOW_DAYS} days",
            "requirements": {
                "min_occurrences": service.MIN_OCCURRENCES,
                "time_window_days": service.TIME_WINDOW_DAYS
            }
        }

    return {
        "valid": True,
        "message": "Pattern meets automation threshold requirements",
        "requirements": {
            "min_occurrences": service.MIN_OCCURRENCES,
            "time_window_days": service.TIME_WINDOW_DAYS
        }
    }


@router.get("/alerts/recent")
async def get_recent_alerts(
    hours: int = 24,
    service: PatternMonitoringService = Depends(get_monitoring_service),
    db: Session = Depends(get_db)
):
    """Get recent pattern alerts that met automation threshold"""
    from ...data.models.workflow_pattern import WorkflowPattern

    cutoff_time = datetime.utcnow() - timedelta(hours=hours)

    # Get recently qualified patterns
    recent_qualified = db.query(WorkflowPattern)\
        .filter(WorkflowPattern.automation_ready == True)\
        .filter(WorkflowPattern.updated_at >= cutoff_time)\
        .order_by(WorkflowPattern.automation_priority.desc())\
        .limit(20)\
        .all()

    alerts = []
    for pattern in recent_qualified:
        # Count recent occurrences
        recent_count = db.query(pattern.__class__)\
            .filter(pattern.__class__.pattern_hash == pattern.pattern_hash)\
            .filter(pattern.__class__.last_occurrence >= cutoff_time)\
            .count()

        alerts.append({
            "pattern_id": str(pattern.id),
            "pattern_signature": pattern.pattern_signature,
            "occurrence_count": recent_count,
            "confidence_score": pattern.confidence_score,
            "automation_value": pattern.automation_value,
            "automation_priority": pattern.automation_priority,
            "qualified_at": pattern.updated_at,
            "recommendation": f"Pattern qualified for automation with {recent_count} occurrences"
        })

    return {
        "alerts": alerts,
        "total_count": len(alerts),
        "time_window_hours": hours,
        "constitutional_note": f"All patterns meet {service.MIN_OCCURRENCES}+ occurrence requirement"
    }


@router.post("/thresholds/update")
async def update_monitoring_thresholds(
    min_occurrences: int = 3,
    time_window_days: int = 7,
    service: PatternMonitoringService = Depends(get_monitoring_service)
):
    """
    Update monitoring thresholds (must maintain constitutional minimums)

    Constitutional requirements enforce minimum values to prevent over-automation
    """
    # Enforce constitutional minimums
    if min_occurrences < 3:
        raise HTTPException(
            status_code=400,
            detail="Constitutional requirement: minimum 3 occurrences required for automation"
        )

    if time_window_days < 7:
        raise HTTPException(
            status_code=400,
            detail="Constitutional requirement: minimum 7-day window required for pattern validation"
        )

    service.MIN_OCCURRENCES = min_occurrences
    service.TIME_WINDOW_DAYS = time_window_days

    return {
        "message": "Monitoring thresholds updated",
        "min_occurrences": service.MIN_OCCURRENCES,
        "time_window_days": service.TIME_WINDOW_DAYS,
        "constitutional_note": "Thresholds enforce minimum requirements to prevent over-automation"
    }


@router.get("/health")
async def monitoring_health_check(
    service: PatternMonitoringService = Depends(get_monitoring_service)
):
    """Health check for pattern monitoring service"""
    stats = await service.get_monitoring_stats()

    # Determine health status
    is_healthy = (
        service.monitoring_active and
        stats.monitoring_uptime.total_seconds() > 60 and  # Running for at least 1 minute
        len(service.request_buffer) < service.BUFFER_SIZE *
        0.9  # Buffer not overwhelmed
    )

    return {
        "healthy": is_healthy,
        "monitoring_active": service.monitoring_active,
        "uptime_seconds": int(stats.monitoring_uptime.total_seconds()),
        "buffer_utilization": f"{len(service.request_buffer)}/{service.BUFFER_SIZE}",
        "constitutional_compliance": {
            "min_occurrences": service.MIN_OCCURRENCES >= 3,
            "time_window": service.TIME_WINDOW_DAYS >= 7,
            "status": "Constitutional requirements enforced"
        }
    }
