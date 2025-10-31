"""
Real-time Pattern Detection Monitoring Service

Monitors user requests in real-time and validates patterns meet constitutional
3+ occurrence requirement within 7-day window for automation.
"""

import asyncio
import logging
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Set

from sqlalchemy import and_, func
from sqlalchemy.orm import Session

from ..data.models.user_request import UserRequest
from ..data.models.workflow_pattern import WorkflowPattern
from .pattern_detection_service import PatternDetectionService

logger = logging.getLogger(__name__)


@dataclass
class PatternAlert:
    """Alert for pattern that meets automation threshold"""
    pattern_id: str
    pattern_signature: str
    occurrence_count: int
    confidence_score: float
    automation_value: float
    first_seen: datetime
    last_seen: datetime
    requests: List[str]
    recommendation: str


@dataclass
class MonitoringStats:
    """Real-time monitoring statistics"""
    active_patterns: int
    qualified_patterns: int
    pending_patterns: int
    total_requests_analyzed: int
    monitoring_uptime: timedelta
    last_pattern_detected: Optional[datetime]


class PatternMonitoringService:
    """
    Real-time pattern detection monitoring service

    Constitutional Requirements:
    - Pattern must occur 3+ times within 7-day window
    - Real-time analysis of incoming user requests
    - Threshold validation for automation readiness
    """

    def __init__(self, db: Session, pattern_service: PatternDetectionService):
        self.db = db
        self.pattern_service = pattern_service
        self.monitoring_active = False
        self.monitoring_start_time: Optional[datetime] = None
        self.request_buffer: List[UserRequest] = []
        self.pattern_cache: Dict[str, WorkflowPattern] = {}
        self.alert_callbacks: List[callable] = []

        # Constitutional thresholds
        self.MIN_OCCURRENCES = 3
        self.TIME_WINDOW_DAYS = 7
        self.BUFFER_SIZE = 100
        self.ANALYSIS_INTERVAL = 30  # seconds

    async def start_monitoring(self) -> None:
        """Start real-time pattern monitoring"""
        if self.monitoring_active:
            logger.warning("Pattern monitoring already active")
            return

        self.monitoring_active = True
        self.monitoring_start_time = datetime.utcnow()

        logger.info(
            f"Starting real-time pattern monitoring with {self.MIN_OCCURRENCES}+ occurrences in {self.TIME_WINDOW_DAYS} days")

        # Start monitoring tasks
        await asyncio.gather(
            self._monitor_requests(),
            self._analyze_patterns(),
            self._cleanup_patterns()
        )

    async def stop_monitoring(self) -> None:
        """Stop pattern monitoring"""
        self.monitoring_active = False
        logger.info("Pattern monitoring stopped")

    def add_alert_callback(self, callback: callable) -> None:
        """Add callback for pattern alerts"""
        self.alert_callbacks.append(callback)

    async def process_user_request(self, request: UserRequest) -> None:
        """Process new user request for pattern detection"""
        if not self.monitoring_active:
            return

        # Add to buffer for batch processing
        self.request_buffer.append(request)

        # Process buffer if full
        if len(self.request_buffer) >= self.BUFFER_SIZE:
            await self._process_request_buffer()

    async def _monitor_requests(self) -> None:
        """Monitor incoming user requests"""
        while self.monitoring_active:
            try:
                # Get recent requests not yet analyzed
                cutoff_time = datetime.utcnow() - timedelta(minutes=5)

                recent_requests = self.db.query(UserRequest)\
                    .filter(UserRequest.created_at >= cutoff_time)\
                    .filter(UserRequest.pattern_analyzed == False)\
                    .all()

                for request in recent_requests:
                    await self.process_user_request(request)
                    request.pattern_analyzed = True

                self.db.commit()

                await asyncio.sleep(self.ANALYSIS_INTERVAL)

            except Exception as e:
                logger.error(f"Error in request monitoring: {e}")
                await asyncio.sleep(5)

    async def _analyze_patterns(self) -> None:
        """Analyze patterns for threshold validation"""
        while self.monitoring_active:
            try:
                await self._validate_pattern_thresholds()
                await asyncio.sleep(self.ANALYSIS_INTERVAL * 2)

            except Exception as e:
                logger.error(f"Error in pattern analysis: {e}")
                await asyncio.sleep(10)

    async def _cleanup_patterns(self) -> None:
        """Clean up old patterns outside time window"""
        while self.monitoring_active:
            try:
                cutoff_time = datetime.utcnow() - timedelta(days=self.TIME_WINDOW_DAYS)

                # Archive old patterns
                old_patterns = self.db.query(WorkflowPattern)\
                    .filter(WorkflowPattern.last_occurrence < cutoff_time)\
                    .filter(WorkflowPattern.is_active == True)\
                    .all()

                for pattern in old_patterns:
                    if pattern.occurrence_count < self.MIN_OCCURRENCES:
                        pattern.is_active = False
                        logger.info(
                            f"Archived pattern {pattern.pattern_hash} - insufficient occurrences")

                self.db.commit()

                # Sleep for 1 hour between cleanups
                await asyncio.sleep(3600)

            except Exception as e:
                logger.error(f"Error in pattern cleanup: {e}")
                await asyncio.sleep(300)  # 5 minute delay on error

    async def _process_request_buffer(self) -> None:
        """Process buffered requests for pattern detection"""
        if not self.request_buffer:
            return

        requests_to_process = self.request_buffer.copy()
        self.request_buffer.clear()

        try:
            # Analyze patterns in batch
            patterns = await self.pattern_service.analyze_patterns(requests_to_process)

            for pattern in patterns:
                await self._update_pattern_monitoring(pattern)

        except Exception as e:
            logger.error(f"Error processing request buffer: {e}")

    async def _update_pattern_monitoring(self, pattern: WorkflowPattern) -> None:
        """Update pattern monitoring and check thresholds"""
        pattern_key = pattern.pattern_hash

        # Update cache
        self.pattern_cache[pattern_key] = pattern

        # Check if pattern meets constitutional requirements
        if await self._meets_automation_threshold(pattern):
            alert = await self._create_pattern_alert(pattern)
            await self._notify_pattern_alert(alert)

    async def _meets_automation_threshold(self, pattern: WorkflowPattern) -> bool:
        """
        Validate pattern meets constitutional 3+ occurrence threshold
        within 7-day window
        """
        time_window = datetime.utcnow() - timedelta(days=self.TIME_WINDOW_DAYS)

        # Count occurrences within time window
        recent_count = self.db.query(func.count(UserRequest.id))\
            .filter(UserRequest.pattern_hash == pattern.pattern_hash)\
            .filter(UserRequest.created_at >= time_window)\
            .scalar()

        # Constitutional validation
        meets_occurrence_threshold = recent_count >= self.MIN_OCCURRENCES
        meets_confidence_threshold = pattern.confidence_score >= 0.8
        has_automation_value = pattern.automation_value > 0.5

        if meets_occurrence_threshold and meets_confidence_threshold and has_automation_value:
            logger.info(
                f"Pattern {pattern.pattern_hash} meets automation threshold: "
                f"{recent_count} occurrences, {pattern.confidence_score:.2f} confidence, "
                f"{pattern.automation_value:.2f} value"
            )
            return True

        return False

    async def _create_pattern_alert(self, pattern: WorkflowPattern) -> PatternAlert:
        """Create pattern alert for qualified automation"""
        time_window = datetime.utcnow() - timedelta(days=self.TIME_WINDOW_DAYS)

        # Get related requests
        related_requests = self.db.query(UserRequest)\
            .filter(UserRequest.pattern_hash == pattern.pattern_hash)\
            .filter(UserRequest.created_at >= time_window)\
            .order_by(UserRequest.created_at.asc())\
            .all()

        first_seen = related_requests[0].created_at if related_requests else pattern.first_occurrence
        last_seen = related_requests[-1].created_at if related_requests else pattern.last_occurrence

        # Generate recommendation
        recommendation = self._generate_automation_recommendation(
            pattern, len(related_requests))

        return PatternAlert(
            pattern_id=str(pattern.id),
            pattern_signature=pattern.pattern_signature,
            occurrence_count=len(related_requests),
            confidence_score=pattern.confidence_score,
            automation_value=pattern.automation_value,
            first_seen=first_seen,
            last_seen=last_seen,
            requests=[str(req.id) for req in related_requests],
            recommendation=recommendation
        )

    def _generate_automation_recommendation(self, pattern: WorkflowPattern, occurrence_count: int) -> str:
        """Generate automation recommendation based on pattern analysis"""
        if occurrence_count >= 10:
            priority = "HIGH"
        elif occurrence_count >= 5:
            priority = "MEDIUM"
        else:
            priority = "LOW"

        time_saved = occurrence_count * pattern.automation_value * \
            5  # Estimate 5 minutes per task

        return (
            f"{priority} PRIORITY: Pattern detected {occurrence_count} times. "
            f"Automation could save ~{time_saved:.0f} minutes. "
            f"Confidence: {pattern.confidence_score:.0%}. "
            f"Recommend creating workflow for this pattern."
        )

    async def _notify_pattern_alert(self, alert: PatternAlert) -> None:
        """Notify subscribers of pattern alert"""
        logger.info(
            f"Pattern alert: {alert.pattern_signature} - {alert.recommendation}")

        # Store alert in database
        pattern = self.db.query(WorkflowPattern)\
            .filter(WorkflowPattern.id == alert.pattern_id)\
            .first()

        if pattern:
            pattern.automation_ready = True
            pattern.automation_priority = alert.occurrence_count * alert.confidence_score
            self.db.commit()

        # Notify callbacks
        for callback in self.alert_callbacks:
            try:
                await callback(alert)
            except Exception as e:
                logger.error(f"Error in alert callback: {e}")

    async def get_monitoring_stats(self) -> MonitoringStats:
        """Get current monitoring statistics"""
        if not self.monitoring_active:
            return MonitoringStats(
                active_patterns=0,
                qualified_patterns=0,
                pending_patterns=0,
                total_requests_analyzed=0,
                monitoring_uptime=timedelta(0),
                last_pattern_detected=None
            )

        time_window = datetime.utcnow() - timedelta(days=self.TIME_WINDOW_DAYS)

        # Count patterns by status
        active_patterns = self.db.query(func.count(WorkflowPattern.id))\
            .filter(WorkflowPattern.is_active == True)\
            .scalar()

        qualified_patterns = self.db.query(func.count(WorkflowPattern.id))\
            .filter(WorkflowPattern.automation_ready == True)\
            .filter(WorkflowPattern.last_occurrence >= time_window)\
            .scalar()

        pending_patterns = self.db.query(func.count(WorkflowPattern.id))\
            .filter(WorkflowPattern.automation_ready == False)\
            .filter(WorkflowPattern.is_active == True)\
            .filter(WorkflowPattern.occurrence_count < self.MIN_OCCURRENCES)\
            .scalar()

        # Count analyzed requests
        total_requests = self.db.query(func.count(UserRequest.id))\
            .filter(UserRequest.pattern_analyzed == True)\
            .scalar()

        # Get last pattern detection
        last_pattern = self.db.query(WorkflowPattern)\
            .filter(WorkflowPattern.created_at >= time_window)\
            .order_by(WorkflowPattern.created_at.desc())\
            .first()

        uptime = timedelta(0)
        if self.monitoring_start_time:
            uptime = datetime.utcnow() - self.monitoring_start_time

        return MonitoringStats(
            active_patterns=active_patterns or 0,
            qualified_patterns=qualified_patterns or 0,
            pending_patterns=pending_patterns or 0,
            total_requests_analyzed=total_requests or 0,
            monitoring_uptime=uptime,
            last_pattern_detected=last_pattern.created_at if last_pattern else None
        )

    async def get_qualified_patterns(self) -> List[WorkflowPattern]:
        """Get patterns that meet automation threshold"""
        time_window = datetime.utcnow() - timedelta(days=self.TIME_WINDOW_DAYS)

        return self.db.query(WorkflowPattern)\
            .filter(WorkflowPattern.automation_ready == True)\
            .filter(WorkflowPattern.last_occurrence >= time_window)\
            .filter(WorkflowPattern.occurrence_count >= self.MIN_OCCURRENCES)\
            .order_by(WorkflowPattern.automation_priority.desc())\
            .all()

    async def validate_pattern_threshold(self, pattern_id: str) -> bool:
        """Validate specific pattern meets threshold requirements"""
        pattern = self.db.query(WorkflowPattern)\
            .filter(WorkflowPattern.id == pattern_id)\
            .first()

        if not pattern:
            return False

        return await self._meets_automation_threshold(pattern)
