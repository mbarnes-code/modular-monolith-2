"""
Validation framework for service adapters.

Ensures business logic preservation and proper integration of all 37
mental prosthetic tools with executive function accommodations.
"""

import logging
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Callable, Dict, List, Optional

from .adapter import BaseServiceAdapter, ExecutiveFunctionContext, ToolMetadata

logger = logging.getLogger(__name__)


@dataclass
class AdapterValidationResult:
    """Result of adapter validation process."""
    adapter_id: str
    passed: bool
    business_logic_preserved: bool
    executive_function_compliant: bool
    performance_compliant: bool
    errors: List[str]
    warnings: List[str]
    metrics: Dict[str, Any]
    validation_timestamp: datetime


class AdapterValidator:
    """Validates service adapters for compliance and quality."""

    def __init__(self):
        self.validation_rules: List[Callable] = []
        self.performance_thresholds = {
            "security": 1000,      # 1s for security domain
            "productivity": 2000,  # 2s for productivity domain
            "mtg": 3000,          # 3s for MTG domain
            "infrastructure": 5000  # 5s for infrastructure domain
        }

    async def validate_adapter_implementation(
        self,
        adapter: BaseServiceAdapter
    ) -> AdapterValidationResult:
        """Comprehensive validation of adapter implementation."""
        start_time = datetime.utcnow()
        errors = []
        warnings = []
        metrics = {}

        # 1. Basic implementation validation
        basic_check = await self._validate_basic_implementation(adapter)
        if not basic_check["passed"]:
            errors.extend(basic_check["errors"])

        # 2. Business logic preservation check
        business_logic_check = await self._validate_business_logic_preservation(adapter)
        business_logic_preserved = business_logic_check["preserved"]
        if not business_logic_preserved:
            errors.extend(business_logic_check["errors"])

        # 3. Executive function compliance
        exec_func_check = await self._validate_executive_function_compliance(adapter)
        executive_function_compliant = exec_func_check["compliant"]
        if not executive_function_compliant:
            warnings.extend(exec_func_check["warnings"])

        # 4. Performance validation
        perf_check = await self._validate_performance_compliance(adapter)
        performance_compliant = perf_check["compliant"]
        if not performance_compliant:
            warnings.extend(perf_check["warnings"])

        # Compile metrics
        metrics.update({
            "validation_duration_ms": int(
                (datetime.utcnow() - start_time).total_seconds() * 1000
            ),
            "business_logic_score": business_logic_check.get("score", 0),
            "performance_score": perf_check.get("score", 0),
            "executive_function_score": exec_func_check.get("score", 0)
        })

        # Determine overall pass/fail
        passed = (
            len(errors) == 0 and
            business_logic_preserved and
            executive_function_compliant and
            performance_compliant
        )

        return AdapterValidationResult(
            adapter_id=adapter.tool_id,
            passed=passed,
            business_logic_preserved=business_logic_preserved,
            executive_function_compliant=executive_function_compliant,
            performance_compliant=performance_compliant,
            errors=errors,
            warnings=warnings,
            metrics=metrics,
            validation_timestamp=datetime.utcnow()
        )

    async def _validate_basic_implementation(
        self,
        adapter: BaseServiceAdapter
    ) -> Dict[str, Any]:
        """Validate basic adapter implementation requirements."""
        errors = []

        # Check required methods
        required_methods = ["initialize", "health_check",
                            "get_capabilities", "execute_operation"]
        for method_name in required_methods:
            if not hasattr(adapter, method_name):
                errors.append(f"Missing required method: {method_name}")
            elif not callable(getattr(adapter, method_name)):
                errors.append(f"Method {method_name} is not callable")

        # Check metadata
        if not adapter.metadata:
            errors.append("Adapter missing metadata")
        elif not isinstance(adapter.metadata, ToolMetadata):
            errors.append("Invalid metadata type")

        # Check configuration
        if not adapter.config:
            errors.append("Adapter missing configuration")

        return {
            "passed": len(errors) == 0,
            "errors": errors
        }

    async def _validate_business_logic_preservation(
        self,
        adapter: BaseServiceAdapter
    ) -> Dict[str, Any]:
        """Validate that original business logic is preserved."""
        errors = []
        score = 100  # Start with perfect score

        # Check if adapter claims business logic preservation
        if not adapter.metadata.business_logic_preserved:
            errors.append("Adapter does not claim business logic preservation")
            score -= 50

        # Check for essential capabilities
        try:
            capabilities = await adapter.get_capabilities()
            if not capabilities:
                errors.append(
                    "No capabilities reported - business logic may be missing")
                score -= 30
            elif len(capabilities) < 3:
                errors.append(
                    "Limited capabilities - incomplete business logic preservation")
                score -= 20
        except Exception as e:
            errors.append(f"Failed to get capabilities: {e}")
            score -= 40

        # Check adaptation strategy alignment
        strategy = adapter.metadata.adaptation_strategy
        if strategy.value == "microservice":
            # Microservices should preserve complex algorithms
            if "algorithm" not in str(capabilities).lower():
                errors.append(
                    "Microservice strategy but no algorithmic capabilities detected")
                score -= 15

        return {
            "preserved": len(errors) == 0 and score >= 70,
            "errors": errors,
            "score": max(0, score)
        }

    async def _validate_executive_function_compliance(
        self,
        adapter: BaseServiceAdapter
    ) -> Dict[str, Any]:
        """Validate executive function accommodations."""
        warnings = []
        score = 100

        # Check executive function support level
        ef_level = adapter.metadata.executive_function_level
        if ef_level.value == "minimal":
            warnings.append(
                "Minimal executive function support - may not meet user needs")
            score -= 30

        # Test accommodation methods
        test_context = ExecutiveFunctionContext(
            user_id="test_user",
            adhd_mode_enabled=True,
            focus_assist_enabled=True
        )

        try:
            # Test initialization with accommodations
            init_response = await adapter.initialize_with_accommodation(test_context)
            if not init_response.accommodations_applied:
                warnings.append(
                    "No accommodations applied during initialization")
                score -= 20
        except Exception as e:
            warnings.append(f"Failed accommodation test: {e}")
            score -= 40

        return {
            "compliant": score >= 70,
            "warnings": warnings,
            "score": max(0, score)
        }

    async def _validate_performance_compliance(
        self,
        adapter: BaseServiceAdapter
    ) -> Dict[str, Any]:
        """Validate performance requirements."""
        warnings = []
        score = 100

        domain = adapter.domain.value
        target_ms = self.performance_thresholds.get(domain, 2000)

        # Check configured performance target
        if adapter.metadata.performance_target_ms > target_ms:
            warnings.append(
                f"Performance target ({adapter.metadata.performance_target_ms}ms) "
                f"exceeds domain requirement ({target_ms}ms)"
            )
            score -= 30

        # Test actual performance if adapter is initialized
        if adapter.is_initialized:
            try:
                # Simple health check performance test
                start_time = datetime.utcnow()
                health_response = await adapter.health_check()
                duration_ms = int(
                    (datetime.utcnow() - start_time).total_seconds() * 1000
                )

                if duration_ms > target_ms:
                    warnings.append(
                        f"Health check exceeded domain target: {duration_ms}ms > {target_ms}ms"
                    )
                    score -= 25

                if not health_response.success:
                    warnings.append("Health check failed")
                    score -= 20

            except Exception as e:
                warnings.append(f"Performance test failed: {e}")
                score -= 40

        return {
            "compliant": score >= 70,
            "warnings": warnings,
            "score": max(0, score)
        }


async def validate_adapter_implementation(adapter: BaseServiceAdapter) -> AdapterValidationResult:
    """Standalone function to validate a single adapter."""
    validator = AdapterValidator()
    return await validator.validate_adapter_implementation(adapter)


async def validate_business_logic_preservation(adapter: BaseServiceAdapter) -> bool:
    """Quick check for business logic preservation."""
    validator = AdapterValidator()
    result = await validator._validate_business_logic_preservation(adapter)
    return result["preserved"]
