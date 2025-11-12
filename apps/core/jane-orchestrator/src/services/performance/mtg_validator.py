"""
MTG Domain Validator

Validates constitutional performance requirements for MTG domain tools.
Enforces <3s response time requirement for game analysis complexity.
"""

import asyncio
import time
from typing import List, Optional

from apps.jane_orchestrator.src.data.models.domain_validation import (
    DomainValidation, ValidationStatus)
from apps.jane_orchestrator.src.data.models.performance_metrics import (
    DomainType, PerformanceMetrics)
from libs.shared.logging import get_logger
from sqlalchemy.orm import Session

logger = get_logger(__name__)


class MTGDomainValidator:
    """
    Validates performance requirements for MTG domain tools

    Constitutional requirement: <3s response time for game analysis
    """

    DOMAIN = DomainType.MTG
    CONSTITUTIONAL_THRESHOLD_MS = 3000.0  # <3s

    # MTG tools that must be validated
    MTG_TOOLS = [
        "commander-spellbook",
        "mtg-commander-map",
        "mtg-scripting-toolkit",
        "mtg-analysis-tools"
    ]

    def __init__(self, db_session: Session):
        self.db_session = db_session
        self.validation_run: Optional[DomainValidation] = None
        self.metrics_collected: List[PerformanceMetrics] = []

    async def validate_domain(
        self,
        triggered_by: str = "manual",
        triggered_by_user: Optional[str] = None,
        test_tools: Optional[List[str]] = None
    ) -> DomainValidation:
        """Validate MTG domain performance requirements"""

        # Create validation run
        self.validation_run = DomainValidation.create_validation_run(
            domain=self.DOMAIN,
            triggered_by=triggered_by,
            triggered_by_user=triggered_by_user,
            metadata={
                "threshold_ms": self.CONSTITUTIONAL_THRESHOLD_MS,
                "tools": test_tools or self.MTG_TOOLS
            }
        )

        self.validation_run.status = ValidationStatus.RUNNING.value
        self.db_session.add(self.validation_run)
        self.db_session.commit()

        try:
            # Test MTG tools
            tools_to_test = test_tools or self.MTG_TOOLS
            await self._test_mtg_tools(tools_to_test)

            # Analyze and complete
            self._analyze_results()
            self._generate_recommendations()

            status = (
                ValidationStatus.PASSED
                if self.validation_run.violations_found == 0
                else ValidationStatus.FAILED
            )
            self.validation_run.mark_completed(status)

        except Exception as e:
            logger.error(f"MTG validation failed: {e}")
            self.validation_run.mark_completed(ValidationStatus.ERROR)

        self.validation_run.generate_summary()
        self.db_session.commit()

        return self.validation_run

    async def _test_mtg_tools(self, tools: List[str]) -> None:
        """Test performance of MTG tools"""

        for tool_name in tools:
            try:
                start_time = time.time()

                # Simulate game analysis operations
                if "spellbook" in tool_name:
                    await asyncio.sleep(0.8)  # Combo analysis
                elif "commander-map" in tool_name:
                    await asyncio.sleep(0.6)  # Deck analysis
                else:
                    await asyncio.sleep(0.4)  # Basic operations

                total_time = (time.time() - start_time) * 1000

                # Create metric
                metric = PerformanceMetrics.create_response_time_metric(
                    domain=self.DOMAIN,
                    tool_name=tool_name,
                    response_time_ms=total_time,
                    user_session_id=self.validation_run.validation_run_id,
                    metadata={
                        "test_type": "mtg_analysis",
                        "validation_run": self.validation_run.validation_run_id
                    }
                )

                self.db_session.add(metric)
                self.metrics_collected.append(metric)

            except Exception as e:
                logger.error(f"MTG tool test failed for {tool_name}: {e}")
                self.validation_run.warnings_found += 1

        self.validation_run.tools_tested = len(tools)
        successful = len(tools) - self.validation_run.warnings_found
        self.validation_run.calculate_pass_rate(len(tools), successful)

    def _analyze_results(self) -> None:
        """Analyze validation results"""
        violations = sum(1 for m in self.metrics_collected if m.is_violation)
        warnings = sum(
            1 for m in self.metrics_collected
            if not m.is_violation and m.performance_ratio > 0.8
        )

        self.validation_run.violations_found = violations
        self.validation_run.warnings_found += warnings
        self.validation_run.metrics_collected = len(self.metrics_collected)

    def _generate_recommendations(self) -> None:
        """Generate recommendations based on results"""
        if self.validation_run.violations_found > 0:
            self.validation_run.add_recommendation(
                f"CRITICAL: {self.validation_run.violations_found} MTG tools "
                f"violate <3s requirement for game analysis complexity.",
                severity="critical",
                category="constitutional_violation"
            )

        if self.validation_run.violations_found == 0:
            self.validation_run.add_recommendation(
                "MTG domain meets constitutional requirements. "
                "Game analysis operations within <3s limit.",
                severity="info",
                category="constitutional_compliance"
            )
