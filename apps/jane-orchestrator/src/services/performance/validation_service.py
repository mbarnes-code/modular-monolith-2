"""
Performance Validation Service

Orchestrates domain-specific performance validation across all 4 domains.
Coordinates Security, Productivity, MTG, and Infrastructure validators.
"""

import asyncio
from datetime import datetime
from typing import Any, Dict, List, Optional

from apps.jane_orchestrator.src.data.models.domain_validation import \
    DomainValidation
from apps.jane_orchestrator.src.data.models.performance_metrics import \
    DomainType
from libs.shared.logging import get_logger
from sqlalchemy.orm import Session

from .infrastructure_validator import InfrastructureDomainValidator
from .mtg_validator import MTGDomainValidator
from .productivity_validator import ProductivityDomainValidator
from .security_validator import SecurityDomainValidator

logger = get_logger(__name__)


class PerformanceValidationService:
    """
    Orchestrates performance validation across all domains

    Ensures constitutional compliance:
    - Security: <1s response time
    - Productivity: <2s response time
    - MTG: <3s response time
    - Infrastructure: <5s response time
    """

    def __init__(self, db_session: Session):
        self.db_session = db_session

        # Initialize domain validators
        self.validators = {
            DomainType.SECURITY: SecurityDomainValidator(db_session),
            DomainType.PRODUCTIVITY: ProductivityDomainValidator(db_session),
            DomainType.MTG: MTGDomainValidator(db_session),
            DomainType.INFRASTRUCTURE: InfrastructureDomainValidator(
                db_session
            )
        }

    async def validate_all_domains(
        self,
        triggered_by: str = "manual",
        triggered_by_user: Optional[str] = None,
        domains: Optional[List[DomainType]] = None,
        parallel: bool = True
    ) -> Dict[str, DomainValidation]:
        """
        Validate performance across all or specified domains

        Args:
            triggered_by: What triggered this validation
            triggered_by_user: User who triggered validation
            domains: Specific domains to validate (default: all)
            parallel: Whether to run validations in parallel

        Returns:
            Dictionary mapping domain names to validation results
        """
        domains_to_validate = domains or list(DomainType)

        logger.info(
            f"Starting performance validation for {len(domains_to_validate)} "
            f"domains (parallel={parallel})"
        )

        if parallel:
            return await self._validate_domains_parallel(
                domains_to_validate, triggered_by, triggered_by_user
            )
        else:
            return await self._validate_domains_sequential(
                domains_to_validate, triggered_by, triggered_by_user
            )

    async def _validate_domains_parallel(
        self,
        domains: List[DomainType],
        triggered_by: str,
        triggered_by_user: Optional[str]
    ) -> Dict[str, DomainValidation]:
        """Validate domains in parallel for faster results"""

        # Create validation tasks
        tasks = {}
        for domain in domains:
            validator = self.validators[domain]
            task = validator.validate_domain(
                triggered_by=triggered_by,
                triggered_by_user=triggered_by_user
            )
            tasks[domain.value] = task

        # Run all validations concurrently
        results = await asyncio.gather(
            *tasks.values(),
            return_exceptions=True
        )

        # Process results
        validation_results = {}
        for i, domain in enumerate(domains):
            result = results[i]
            if isinstance(result, Exception):
                logger.error(f"Validation failed for {domain.value}: {result}")
                validation_results[domain.value] = None
            else:
                validation_results[domain.value] = result

        return validation_results

    async def _validate_domains_sequential(
        self,
        domains: List[DomainType],
        triggered_by: str,
        triggered_by_user: Optional[str]
    ) -> Dict[str, DomainValidation]:
        """Validate domains sequentially (safer for resource constraints)"""

        validation_results = {}

        for domain in domains:
            try:
                validator = self.validators[domain]
                result = await validator.validate_domain(
                    triggered_by=triggered_by,
                    triggered_by_user=triggered_by_user
                )
                validation_results[domain.value] = result

            except Exception as e:
                logger.error(f"Validation failed for {domain.value}: {e}")
                validation_results[domain.value] = None

        return validation_results

    async def validate_single_domain(
        self,
        domain: DomainType,
        triggered_by: str = "manual",
        triggered_by_user: Optional[str] = None,
        test_tools: Optional[List[str]] = None
    ) -> DomainValidation:
        """
        Validate a single domain with optional tool filtering

        Args:
            domain: Domain to validate
            triggered_by: What triggered this validation
            triggered_by_user: User who triggered validation
            test_tools: Specific tools to test (domain-specific)

        Returns:
            Validation results for the domain
        """
        logger.info(f"Starting single domain validation: {domain.value}")

        validator = self.validators[domain]
        return await validator.validate_domain(
            triggered_by=triggered_by,
            triggered_by_user=triggered_by_user,
            test_tools=test_tools
        )

    def get_validation_summary(
        self,
        validation_results: Dict[str, DomainValidation]
    ) -> Dict[str, Any]:
        """
        Generate overall validation summary across domains

        Args:
            validation_results: Results from validate_all_domains

        Returns:
            Summary statistics and recommendations
        """
        summary = {
            "timestamp": datetime.utcnow().isoformat(),
            "domains_tested": len(validation_results),
            "domains_passed": 0,
            "domains_failed": 0,
            "domains_error": 0,
            "total_violations": 0,
            "total_warnings": 0,
            "total_tools_tested": 0,
            "total_metrics_collected": 0,
            "constitutional_compliance": True,
            "domain_details": {},
            "overall_status": "UNKNOWN",
            "recommendations": []
        }

        for domain_name, validation in validation_results.items():
            if validation is None:
                summary["domains_error"] += 1
                continue

            # Count status
            if validation.is_passed:
                summary["domains_passed"] += 1
            elif validation.is_failed:
                summary["domains_failed"] += 1
            else:
                summary["domains_error"] += 1

            # Aggregate metrics
            summary["total_violations"] += validation.violations_found
            summary["total_warnings"] += validation.warnings_found
            summary["total_tools_tested"] += validation.tools_tested
            summary["total_metrics_collected"] += validation.metrics_collected

            # Track constitutional compliance
            if validation.violations_found > 0:
                summary["constitutional_compliance"] = False

            # Store domain details
            summary["domain_details"][domain_name] = {
                "status": validation.status,
                "violations": validation.violations_found,
                "warnings": validation.warnings_found,
                "tools_tested": validation.tools_tested,
                "pass_rate": validation.pass_rate,
                "duration_ms": validation.duration_ms
            }

        # Determine overall status
        if summary["domains_error"] > 0:
            summary["overall_status"] = "ERROR"
        elif summary["total_violations"] > 0:
            summary["overall_status"] = "FAILED"
        elif summary["domains_failed"] > 0:
            summary["overall_status"] = "FAILED"
        elif summary["domains_passed"] == summary["domains_tested"]:
            summary["overall_status"] = "PASSED"
        else:
            summary["overall_status"] = "PARTIAL"

        # Generate overall recommendations
        self._generate_overall_recommendations(summary)

        return summary

    def _generate_overall_recommendations(
        self,
        summary: Dict[str, Any]
    ) -> None:
        """Generate recommendations based on overall validation results"""

        if summary["constitutional_compliance"]:
            summary["recommendations"].append({
                "severity": "info",
                "category": "constitutional_compliance",
                "message": (
                    "All domains meet constitutional performance requirements. "
                    "Platform operates within specified thresholds."
                )
            })
        else:
            summary["recommendations"].append({
                "severity": "critical",
                "category": "constitutional_violation",
                "message": (
                    f"CRITICAL: {summary['total_violations']} constitutional "
                    f"violations found across domains. Immediate optimization "
                    f"required."
                )
            })

        if summary["total_warnings"] > 0:
            summary["recommendations"].append({
                "severity": "warning",
                "category": "performance_optimization",
                "message": (
                    f"WARNING: {summary['total_warnings']} performance warnings "
                    f"detected. Consider proactive optimization."
                )
            })

        # Domain-specific recommendations
        failed_domains = [
            name for name, details in summary["domain_details"].items()
            if details["violations"] > 0
        ]

        if failed_domains:
            summary["recommendations"].append({
                "severity": "error",
                "category": "domain_optimization",
                "message": (
                    f"Domains requiring immediate attention: "
                    f"{', '.join(failed_domains)}"
                )
            })
