"""
System-wide Rollback Service for Mental Prosthetic Platform

Provides comprehensive system-wide rollback capabilities as the final fallback option
when tool-specific and domain-specific rollbacks are insufficient. Coordinates rollback
across all 37 integrated tools and 4 domains with minimal service disruption.

Key Features:
- System-wide rollback orchestration across all domains
- Dependency-aware rollback ordering
- Graceful service shutdown and restart
- Data consistency validation during rollback
- Executive function accommodations with clear progress reporting
- Emergency rollback procedures for critical system failures
"""

import asyncio
import json
import logging
from dataclasses import asdict, dataclass
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple

from ......libs.shared.config.state_backup_service import (RestoreStatus,
                                                           get_backup_service)
from ......libs.shared.rollback.consistency_validator import (
    ConsistencyReport, ValidationStatus, get_consistency_validator)
from ......libs.shared.rollback.service_restart_manager import (
    RestartResult, RestartStatus, get_service_restart_manager)
from ......libs.shared.rollback.tool_rollback_service import (
    RollbackResult, RollbackStatus, get_tool_rollback_service)
from ......libs.shared.utils.logging import get_logger

logger = get_logger(__name__)


class SystemRollbackPhase(Enum):
    """Phases of system-wide rollback"""
    INITIALIZATION = "initialization"
    VALIDATION = "validation"
    PREPARATION = "preparation"
    DOMAIN_ROLLBACK = "domain_rollback"
    SERVICE_RESTART = "service_restart"
    CONSISTENCY_CHECK = "consistency_check"
    FINALIZATION = "finalization"
    COMPLETED = "completed"
    FAILED = "failed"


class SystemRollbackStrategy(Enum):
    """System rollback strategies"""
    GRACEFUL = "graceful"        # Normal rollback with user notification
    EMERGENCY = "emergency"      # Fast rollback for critical failures
    MAINTENANCE = "maintenance"  # Planned rollback during maintenance window
    PARTIAL = "partial"         # Rollback specific domains only


@dataclass
class SystemRollbackPlan:
    """System-wide rollback execution plan"""
    rollback_id: str
    strategy: SystemRollbackStrategy
    target_timestamp: datetime
    domains: List[str]
    tools: List[str]
    execution_phases: List[SystemRollbackPhase]
    dependencies: Dict[str, List[str]]
    estimated_duration_minutes: int
    requires_downtime: bool
    user_impact_level: str


@dataclass
class SystemRollbackResult:
    """Result of system-wide rollback operation"""
    rollback_id: str
    status: RollbackStatus
    start_time: datetime
    end_time: Optional[datetime]
    current_phase: SystemRollbackPhase
    completed_phases: List[SystemRollbackPhase]
    domain_results: Dict[str, RollbackResult]
    service_results: Dict[str, RestartResult]
    consistency_report: Optional[ConsistencyReport]
    total_execution_time_seconds: int
    user_impact_summary: Dict[str, Any]
    recovery_actions: List[str]
    next_steps: List[str]


class SystemRollbackService:
    """
    System-wide rollback orchestration service

    Coordinates rollback operations across all 37 integrated tools and 4 domains.
    Provides the final fallback mechanism when individual tool or domain rollbacks
    are insufficient to restore system stability.
    """

    def __init__(self):
        self.tool_rollback_service = get_tool_rollback_service()
        self.service_restart_manager = get_service_restart_manager()
        self.consistency_validator = get_consistency_validator()
        self.backup_service = get_backup_service()

        # Active rollback tracking
        self.active_rollbacks: Dict[str, SystemRollbackResult] = {}

        # Domain service dependencies (rollback order)
        self.domain_dependencies = {
            "infrastructure": [],  # Independent - rollback first
            "security": ["infrastructure"],  # Depends on infrastructure
            "productivity": ["infrastructure"],  # Depends on infrastructure
            "mtg": ["infrastructure"]  # Depends on infrastructure
        }

        # Critical services that require special handling
        self.critical_services = {
            "security": ["misp", "helk", "securityonion"],
            "productivity": ["n8n", "dispatch"],
            "mtg": [],
            "infrastructure": ["kong", "ghostwriter"]
        }

        # Executive function accommodations
        self.progress_update_interval_seconds = 10
        self.user_notification_thresholds = {
            "long_operation_minutes": 5,
            "critical_failure_seconds": 30,
            "user_impact_notification": True
        }

    async def create_rollback_plan(self, target_timestamp: datetime,
                                   strategy: SystemRollbackStrategy = SystemRollbackStrategy.GRACEFUL,
                                   domains: Optional[List[str]] = None,
                                   tools: Optional[List[str]] = None) -> SystemRollbackPlan:
        """
        Create a system-wide rollback execution plan

        Args:
            target_timestamp: Target timestamp to rollback to
            strategy: Rollback strategy (graceful, emergency, maintenance, partial)
            domains: Specific domains to rollback (None = all)
            tools: Specific tools to rollback (None = all)

        Returns:
            Detailed rollback execution plan
        """
        rollback_id = f"system_rollback_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"

        # Determine rollback scope
        target_domains = domains or ["security",
                                     "productivity", "mtg", "infrastructure"]

        # Calculate dependencies and execution order
        ordered_domains = self._calculate_rollback_order(target_domains)

        # Estimate execution phases
        execution_phases = [
            SystemRollbackPhase.INITIALIZATION,
            SystemRollbackPhase.VALIDATION,
            SystemRollbackPhase.PREPARATION,
            SystemRollbackPhase.DOMAIN_ROLLBACK,
            SystemRollbackPhase.SERVICE_RESTART,
            SystemRollbackPhase.CONSISTENCY_CHECK,
            SystemRollbackPhase.FINALIZATION
        ]

        # Estimate duration based on strategy
        base_duration = self._estimate_rollback_duration(target_domains, tools)
        strategy_multiplier = {
            SystemRollbackStrategy.GRACEFUL: 1.2,  # Extra time for notifications
            SystemRollbackStrategy.EMERGENCY: 0.7,  # Skip non-critical steps
            SystemRollbackStrategy.MAINTENANCE: 1.5,  # Extra validation
            SystemRollbackStrategy.PARTIAL: 0.8   # Fewer components
        }
        estimated_duration = int(base_duration * strategy_multiplier[strategy])

        # Determine downtime requirements
        requires_downtime = strategy in [
            SystemRollbackStrategy.EMERGENCY, SystemRollbackStrategy.MAINTENANCE]

        return SystemRollbackPlan(
            rollback_id=rollback_id,
            strategy=strategy,
            target_timestamp=target_timestamp,
            domains=ordered_domains,
            tools=tools or [],
            execution_phases=execution_phases,
            dependencies=self.domain_dependencies,
            estimated_duration_minutes=estimated_duration,
            requires_downtime=requires_downtime,
            user_impact_level=self._calculate_user_impact(
                strategy, target_domains)
        )

    async def execute_system_rollback(self, plan: SystemRollbackPlan) -> SystemRollbackResult:
        """
        Execute system-wide rollback according to plan

        Args:
            plan: Rollback execution plan

        Returns:
            Detailed rollback execution result
        """
        start_time = datetime.utcnow()
        rollback_id = plan.rollback_id

        # Initialize rollback result
        result = SystemRollbackResult(
            rollback_id=rollback_id,
            status=RollbackStatus.IN_PROGRESS,
            start_time=start_time,
            end_time=None,
            current_phase=SystemRollbackPhase.INITIALIZATION,
            completed_phases=[],
            domain_results={},
            service_results={},
            consistency_report=None,
            total_execution_time_seconds=0,
            user_impact_summary={},
            recovery_actions=[],
            next_steps=[]
        )

        # Track active rollback
        self.active_rollbacks[rollback_id] = result

        try:
            logger.info(
                f"Starting system-wide rollback {rollback_id} with strategy {plan.strategy.value}")

            # Phase 1: Initialization
            await self._execute_initialization_phase(plan, result)

            # Phase 2: Validation
            await self._execute_validation_phase(plan, result)

            # Phase 3: Preparation
            await self._execute_preparation_phase(plan, result)

            # Phase 4: Domain Rollback
            await self._execute_domain_rollback_phase(plan, result)

            # Phase 5: Service Restart
            await self._execute_service_restart_phase(plan, result)

            # Phase 6: Consistency Check
            await self._execute_consistency_check_phase(plan, result)

            # Phase 7: Finalization
            await self._execute_finalization_phase(plan, result)

            # Mark as completed
            result.current_phase = SystemRollbackPhase.COMPLETED
            result.status = RollbackStatus.SUCCESS
            result.end_time = datetime.utcnow()
            result.total_execution_time_seconds = int(
                (result.end_time - start_time).total_seconds())

            logger.info(
                f"System-wide rollback {rollback_id} completed successfully in {result.total_execution_time_seconds}s")

        except Exception as e:
            logger.error(f"System-wide rollback {rollback_id} failed: {e}")
            result.current_phase = SystemRollbackPhase.FAILED
            result.status = RollbackStatus.FAILED
            result.end_time = datetime.utcnow()
            result.total_execution_time_seconds = int(
                (result.end_time - start_time).total_seconds())
            result.recovery_actions.append(f"System rollback failed: {str(e)}")
            result.next_steps.extend([
                "Review system logs for detailed error information",
                "Consider manual intervention for critical services",
                "Validate system state before attempting another rollback"
            ])

        return result

    async def _execute_initialization_phase(self, plan: SystemRollbackPlan, result: SystemRollbackResult):
        """Execute initialization phase"""
        result.current_phase = SystemRollbackPhase.INITIALIZATION
        logger.info(f"Rollback {plan.rollback_id}: Initialization phase")

        # Notify users of upcoming rollback
        if plan.strategy != SystemRollbackStrategy.EMERGENCY:
            await self._notify_users_rollback_starting(plan)

        # Create system snapshot before rollback
        await self._create_pre_rollback_snapshot(plan)

        # Lock system for rollback (if required)
        if plan.requires_downtime:
            await self._enable_maintenance_mode()

        result.completed_phases.append(SystemRollbackPhase.INITIALIZATION)

    async def _execute_validation_phase(self, plan: SystemRollbackPlan, result: SystemRollbackResult):
        """Execute validation phase"""
        result.current_phase = SystemRollbackPhase.VALIDATION
        logger.info(f"Rollback {plan.rollback_id}: Validation phase")

        # Validate rollback prerequisites
        validation_errors = []

        # Check backup availability
        for domain in plan.domains:
            domain_tools = self.critical_services.get(domain, [])
            for tool in domain_tools:
                latest_backup = self.backup_service.get_latest_backup(
                    domain, tool)
                if not latest_backup:
                    validation_errors.append(
                        f"No backup available for {domain}/{tool}")
                elif latest_backup.timestamp > plan.target_timestamp:
                    # This is actually good - we have a backup after target time
                    pass

        # Check system resources
        if not await self._check_system_resources():
            validation_errors.append(
                "Insufficient system resources for rollback")

        # Check service dependencies
        if not await self._validate_service_dependencies(plan.domains):
            validation_errors.append("Service dependency validation failed")

        if validation_errors:
            raise Exception(
                f"Rollback validation failed: {'; '.join(validation_errors)}")

        result.completed_phases.append(SystemRollbackPhase.VALIDATION)

    async def _execute_preparation_phase(self, plan: SystemRollbackPlan, result: SystemRollbackResult):
        """Execute preparation phase"""
        result.current_phase = SystemRollbackPhase.PREPARATION
        logger.info(f"Rollback {plan.rollback_id}: Preparation phase")

        # Stop non-critical services to reduce conflicts
        await self._stop_non_critical_services(plan.domains)

        # Clear caches and temporary data
        await self._clear_system_caches()

        # Prepare rollback workspace
        await self._prepare_rollback_workspace(plan.rollback_id)

        result.completed_phases.append(SystemRollbackPhase.PREPARATION)

    async def _execute_domain_rollback_phase(self, plan: SystemRollbackPlan, result: SystemRollbackResult):
        """Execute domain rollback phase"""
        result.current_phase = SystemRollbackPhase.DOMAIN_ROLLBACK
        logger.info(f"Rollback {plan.rollback_id}: Domain rollback phase")

        # Execute domain rollbacks in dependency order
        for domain in plan.domains:
            logger.info(f"Rolling back domain: {domain}")

            try:
                # Get tools for this domain
                domain_tools = plan.tools if plan.tools else self._get_domain_tools(
                    domain)

                # Execute domain-specific rollback
                domain_result = await self.tool_rollback_service.rollback_domain_tools(
                    domain, domain_tools, plan.target_timestamp
                )

                result.domain_results[domain] = domain_result

                if domain_result.status != RollbackStatus.SUCCESS:
                    logger.warning(
                        f"Domain {domain} rollback had issues: {domain_result.status}")
                    if domain in self.critical_services and self.critical_services[domain]:
                        # Critical domain failure
                        raise Exception(
                            f"Critical domain {domain} rollback failed")

            except Exception as e:
                logger.error(f"Domain {domain} rollback failed: {e}")
                result.domain_results[domain] = RollbackResult(
                    rollback_id=f"{plan.rollback_id}_{domain}",
                    tool_name=f"domain_{domain}",
                    status=RollbackStatus.FAILED,
                    start_time=datetime.utcnow(),
                    end_time=datetime.utcnow(),
                    details={"error": str(e)},
                    rollback_actions=[],
                    next_steps=[
                        f"Manual intervention required for domain {domain}"]
                )

                # Continue with other domains unless this is emergency mode
                if plan.strategy == SystemRollbackStrategy.EMERGENCY:
                    raise Exception(
                        f"Emergency rollback failed at domain {domain}: {e}")

        result.completed_phases.append(SystemRollbackPhase.DOMAIN_ROLLBACK)

    async def _execute_service_restart_phase(self, plan: SystemRollbackPlan, result: SystemRollbackResult):
        """Execute service restart phase"""
        result.current_phase = SystemRollbackPhase.SERVICE_RESTART
        logger.info(f"Rollback {plan.rollback_id}: Service restart phase")

        # Restart services in dependency order
        for domain in plan.domains:
            logger.info(f"Restarting services for domain: {domain}")

            try:
                # Get domain services
                domain_services = self._get_domain_services(domain)

                # Restart services for this domain
                for service_name in domain_services:
                    restart_result = await self.service_restart_manager.restart_service(
                        service_name, f"System rollback {plan.rollback_id}"
                    )
                    result.service_results[service_name] = restart_result

                    if restart_result.status != RestartStatus.SUCCESS:
                        logger.warning(
                            f"Service {service_name} restart failed: {restart_result.status}")

                        # Critical service failure handling
                        if service_name in self.critical_services.get(domain, []):
                            result.recovery_actions.append(
                                f"Critical service {service_name} failed to restart")

            except Exception as e:
                logger.error(
                    f"Service restart failed for domain {domain}: {e}")

        result.completed_phases.append(SystemRollbackPhase.SERVICE_RESTART)

    async def _execute_consistency_check_phase(self, plan: SystemRollbackPlan, result: SystemRollbackResult):
        """Execute consistency check phase"""
        result.current_phase = SystemRollbackPhase.CONSISTENCY_CHECK
        logger.info(f"Rollback {plan.rollback_id}: Consistency check phase")

        # Perform comprehensive consistency validation
        consistency_report = await self.consistency_validator.validate_system_consistency(
            domains=plan.domains,
            tools=plan.tools
        )

        result.consistency_report = consistency_report

        # Analyze consistency results
        if consistency_report.overall_status == ValidationStatus.FAILED:
            logger.error(f"Post-rollback consistency validation failed")
            result.recovery_actions.extend([
                "System consistency validation failed after rollback",
                "Manual data consistency review required",
                "Consider additional rollback or manual data repair"
            ])
        elif consistency_report.overall_status == ValidationStatus.WARNING:
            logger.warning(
                f"Post-rollback consistency validation has warnings")
            result.recovery_actions.append(
                "Review consistency warnings and address as needed")

        result.completed_phases.append(SystemRollbackPhase.CONSISTENCY_CHECK)

    async def _execute_finalization_phase(self, plan: SystemRollbackPlan, result: SystemRollbackResult):
        """Execute finalization phase"""
        result.current_phase = SystemRollbackPhase.FINALIZATION
        logger.info(f"Rollback {plan.rollback_id}: Finalization phase")

        # Disable maintenance mode if enabled
        if plan.requires_downtime:
            await self._disable_maintenance_mode()

        # Clean up rollback workspace
        await self._cleanup_rollback_workspace(plan.rollback_id)

        # Generate user impact summary
        result.user_impact_summary = await self._generate_user_impact_summary(plan, result)

        # Generate next steps
        result.next_steps = await self._generate_next_steps(plan, result)

        # Notify users of rollback completion
        await self._notify_users_rollback_complete(plan, result)

        result.completed_phases.append(SystemRollbackPhase.FINALIZATION)

    def _calculate_rollback_order(self, domains: List[str]) -> List[str]:
        """Calculate optimal rollback order based on dependencies"""
        ordered = []
        remaining = set(domains)

        while remaining:
            # Find domains with no remaining dependencies
            ready = []
            for domain in remaining:
                deps = self.domain_dependencies.get(domain, [])
                if not any(dep in remaining for dep in deps):
                    ready.append(domain)

            if not ready:
                # Circular dependency or error - add all remaining
                ready = list(remaining)
                logger.warning(
                    f"Circular dependency detected in domains: {remaining}")

            # Sort ready domains by priority (infrastructure first)
            priority_order = ["infrastructure",
                              "security", "productivity", "mtg"]
            ready.sort(key=lambda d: priority_order.index(d)
                       if d in priority_order else 999)

            ordered.extend(ready)
            remaining -= set(ready)

        return ordered

    def _estimate_rollback_duration(self, domains: List[str], tools: Optional[List[str]]) -> int:
        """Estimate rollback duration in minutes"""
        base_minutes_per_domain = {
            "security": 15,  # Critical security tools take longer
            "productivity": 10,
            "mtg": 5,
            "infrastructure": 20  # Infrastructure is complex
        }

        total_minutes = sum(base_minutes_per_domain.get(domain, 10)
                            for domain in domains)

        # Add overhead for system-wide operations
        system_overhead = 10

        return total_minutes + system_overhead

    def _calculate_user_impact(self, strategy: SystemRollbackStrategy, domains: List[str]) -> str:
        """Calculate user impact level"""
        if strategy == SystemRollbackStrategy.EMERGENCY:
            return "HIGH - Emergency rollback in progress, all services temporarily unavailable"
        elif strategy == SystemRollbackStrategy.MAINTENANCE:
            return "MEDIUM - Planned maintenance rollback, services unavailable during window"
        elif len(domains) >= 3:
            return "MEDIUM - Multiple domains affected, some service interruption expected"
        else:
            return "LOW - Limited domain rollback, minimal service interruption"

    def _get_domain_tools(self, domain: str) -> List[str]:
        """Get list of tools for a domain"""
        domain_tools = {
            "security": [
                "misp", "helk", "securityonion", "maltrail", "yara-x", "cyberchef",
                "nemesis", "apiscout", "blackarch", "brute-ratel", "hexstrike",
                "meterpreter", "onex"
            ],
            "productivity": [
                "n8n", "mealie", "dispatch", "actual-budget", "firecrawl",
                "goose", "it-tools", "inspector"
            ],
            "mtg": [
                "commander-spellbook", "mtg-commander-map", "mtg-scripting-toolkit",
                "card-analysis"
            ],
            "infrastructure": [
                "kong", "ghostwriter", "kasmvnc", "chroma-mcp", "virustotal-mcp",
                "n8n-mcp", "firecrawl-mcp", "malwarebazaar-mcp", "filescopemcp",
                "lscript", "rita", "software-forensic-kit"
            ]
        }
        return domain_tools.get(domain, [])

    def _get_domain_services(self, domain: str) -> List[str]:
        """Get list of services for a domain"""
        # Map domains to their service names
        return [f"{domain}-service"]

    async def _notify_users_rollback_starting(self, plan: SystemRollbackPlan):
        """Notify users that rollback is starting"""
        logger.info(f"Notifying users of rollback start: {plan.rollback_id}")
        # Implementation would send notifications to users

    async def _notify_users_rollback_complete(self, plan: SystemRollbackPlan, result: SystemRollbackResult):
        """Notify users that rollback is complete"""
        logger.info(
            f"Notifying users of rollback completion: {plan.rollback_id}")
        # Implementation would send completion notifications

    async def _create_pre_rollback_snapshot(self, plan: SystemRollbackPlan):
        """Create system snapshot before rollback"""
        logger.info(f"Creating pre-rollback snapshot for {plan.rollback_id}")
        # Implementation would create system snapshot

    async def _enable_maintenance_mode(self):
        """Enable system maintenance mode"""
        logger.info("Enabling maintenance mode")
        # Implementation would enable maintenance mode

    async def _disable_maintenance_mode(self):
        """Disable system maintenance mode"""
        logger.info("Disabling maintenance mode")
        # Implementation would disable maintenance mode

    async def _check_system_resources(self) -> bool:
        """Check if system has adequate resources for rollback"""
        # Implementation would check CPU, memory, disk space
        return True

    async def _validate_service_dependencies(self, domains: List[str]) -> bool:
        """Validate service dependencies are intact"""
        # Implementation would validate service dependencies
        return True

    async def _stop_non_critical_services(self, domains: List[str]):
        """Stop non-critical services to reduce conflicts"""
        logger.info("Stopping non-critical services")
        # Implementation would stop non-critical services

    async def _clear_system_caches(self):
        """Clear system caches and temporary data"""
        logger.info("Clearing system caches")
        # Implementation would clear caches

    async def _prepare_rollback_workspace(self, rollback_id: str):
        """Prepare workspace for rollback operations"""
        logger.info(f"Preparing rollback workspace for {rollback_id}")
        # Implementation would prepare workspace

    async def _cleanup_rollback_workspace(self, rollback_id: str):
        """Clean up rollback workspace"""
        logger.info(f"Cleaning up rollback workspace for {rollback_id}")
        # Implementation would clean up workspace

    async def _generate_user_impact_summary(self, plan: SystemRollbackPlan,
                                            result: SystemRollbackResult) -> Dict[str, Any]:
        """Generate user impact summary"""
        return {
            "rollback_duration_minutes": result.total_execution_time_seconds / 60,
            "affected_domains": plan.domains,
            "service_availability": "restored" if result.status == RollbackStatus.SUCCESS else "degraded",
            "data_consistency": result.consistency_report.overall_status.value if result.consistency_report else "unknown",
            "user_action_required": len(result.recovery_actions) > 0
        }

    async def _generate_next_steps(self, plan: SystemRollbackPlan,
                                   result: SystemRollbackResult) -> List[str]:
        """Generate recommended next steps"""
        steps = []

        if result.status == RollbackStatus.SUCCESS:
            steps.extend([
                "Monitor system stability for the next 24 hours",
                "Validate that all required functionality is working correctly",
                "Review rollback logs for any warnings or issues"
            ])

            if result.consistency_report and result.consistency_report.warning_checks > 0:
                steps.append("Address consistency validation warnings")
        else:
            steps.extend([
                "Review detailed error logs for rollback failure causes",
                "Consider manual intervention for failed components",
                "Validate system state before attempting recovery",
                "Contact system administrator if issues persist"
            ])

        return steps

    def get_active_rollbacks(self) -> Dict[str, SystemRollbackResult]:
        """Get currently active rollback operations"""
        return {k: v for k, v in self.active_rollbacks.items()
                if v.status == RollbackStatus.IN_PROGRESS}

    def get_rollback_status(self, rollback_id: str) -> Optional[SystemRollbackResult]:
        """Get status of specific rollback operation"""
        return self.active_rollbacks.get(rollback_id)


# Global system rollback service instance
_system_rollback_service: Optional[SystemRollbackService] = None


def get_system_rollback_service() -> SystemRollbackService:
    """Get or create the global system rollback service instance"""
    global _system_rollback_service
    if _system_rollback_service is None:
        _system_rollback_service = SystemRollbackService()
    return _system_rollback_service


async def execute_emergency_rollback(target_timestamp: datetime,
                                     domains: Optional[List[str]] = None) -> SystemRollbackResult:
    """Convenience function for emergency system rollback"""
    service = get_system_rollback_service()
    plan = await service.create_rollback_plan(
        target_timestamp=target_timestamp,
        strategy=SystemRollbackStrategy.EMERGENCY,
        domains=domains
    )
    return await service.execute_system_rollback(plan)
