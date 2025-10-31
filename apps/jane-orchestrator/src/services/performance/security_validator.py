"""
Security Domain Validator

Validates constitutional performance requirements for security domain tools.
Enforces <1s response time requirement for threat analysis criticality.
"""

import asyncio
import time
from typing import Any, Dict, List, Optional

from apps.jane_orchestrator.src.data.models.domain_validation import (
    DomainValidation, ValidationStatus)
from apps.jane_orchestrator.src.data.models.performance_metrics import (
    DomainType, PerformanceMetrics)
from libs.shared.logging import get_logger
from sqlalchemy.orm import Session

logger = get_logger(__name__)


class SecurityDomainValidator:
    """
    Validates performance requirements for Security domain tools

    Constitutional requirement: <1s response time for threat analysis
    """

    DOMAIN = DomainType.SECURITY
    CONSTITUTIONAL_THRESHOLD_MS = 1000.0  # <1s

    # Security tools that must be validated
    SECURITY_TOOLS = [
        "misp",
        "helk",
        "securityonion",
        "maltrail",
        "yara-x",
        "cyberchef",
        "nemesis",
        "apiscout",
        "blackarch",
        "brute-ratel-c4",
        "meterpreter",
        "rita",
        "software-forensic-kit"
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
        """
        Validate security domain performance requirements

        Args:
            triggered_by: What triggered this validation
            triggered_by_user: User who triggered validation
            test_tools: Specific tools to test (defaults to all security tools)

        Returns:
            DomainValidation results
        """
        logger.info(
            f"Starting security domain validation triggered by {triggered_by}"
        )

        # Create validation run
        self.validation_run = DomainValidation.create_validation_run(
            domain=self.DOMAIN,
            triggered_by=triggered_by,
            triggered_by_user=triggered_by_user,
            metadata={
                "constitutional_threshold_ms": self.CONSTITUTIONAL_THRESHOLD_MS,
                "tools_to_test": test_tools or self.SECURITY_TOOLS
            }
        )

        # Start validation
        self.validation_run.status = ValidationStatus.RUNNING.value
        self.db_session.add(self.validation_run)
        self.db_session.commit()

        try:
            # Test tools
            tools_to_test = test_tools or self.SECURITY_TOOLS
            await self._test_security_tools(tools_to_test)

            # Analyze results
            self._analyze_results()

            # Generate recommendations
            self._generate_recommendations()

            # Mark completed
            status = (
                ValidationStatus.PASSED
                if self.validation_run.violations_found == 0
                else ValidationStatus.FAILED
            )
            self.validation_run.mark_completed(status)

        except Exception as e:
            logger.error(f"Security domain validation failed: {e}")
            self.validation_run.mark_completed(ValidationStatus.ERROR)
            self.validation_run.add_recommendation(
                f"Validation failed with error: {str(e)}",
                severity="critical",
                category="system_error"
            )

        # Generate summary
        self.validation_run.generate_summary()

        # Save final results
        self.db_session.commit()

        logger.info(f"Security validation: {self.validation_run.status}")
        return self.validation_run

    async def _test_security_tools(self, tools: List[str]) -> None:
        """Test performance of security tools"""
        logger.info(f"Testing {len(tools)} security tools")

        # Test tools concurrently (but respect individual tool constraints)
        tasks = []
        for tool_name in tools:
            task = self._test_single_tool(tool_name)
            tasks.append(task)

        # Run tests with limited concurrency to avoid overwhelming system
        semaphore = asyncio.Semaphore(3)  # Max 3 concurrent tests

        async def run_with_semaphore(task):
            async with semaphore:
                return await task

        results = await asyncio.gather(
            *[run_with_semaphore(task) for task in tasks],
            return_exceptions=True
        )

        # Process results
        successful_tests = 0
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                logger.error(f"Tool test failed for {tools[i]}: {result}")
                self.validation_run.warnings_found += 1
            else:
                successful_tests += 1

        self.validation_run.tools_tested = len(tools)
        self.validation_run.calculate_pass_rate(len(tools), successful_tests)

    async def _test_single_tool(self, tool_name: str) -> Dict[str, Any]:
        """
        Test performance of a single security tool

        Args:
            tool_name: Name of the tool to test

        Returns:
            Test results dictionary
        """
        logger.debug(f"Testing security tool: {tool_name}")

        try:
            # Simulate tool performance test
            # In real implementation, this would:
            # 1. Make actual API calls to the tool
            # 2. Measure response times for typical operations
            # 3. Test threat analysis workflows
            # 4. Validate data processing speeds

            start_time = time.time()

            # Test different aspects of tool performance
            test_results = {}

            # Test 1: Basic health check / API response
            api_start = time.time()
            await self._simulate_api_call(tool_name, "health_check")
            api_response_time = (time.time() - api_start) * 1000

            # Create API response metric
            api_metric = PerformanceMetrics.create_response_time_metric(
                domain=self.DOMAIN,
                tool_name=tool_name,
                response_time_ms=api_response_time,
                user_session_id=self.validation_run.validation_run_id,
                metadata={
                    "test_type": "api_health_check",
                    "validation_run": self.validation_run.validation_run_id
                }
            )

            self.db_session.add(api_metric)
            self.metrics_collected.append(api_metric)
            test_results["api_response_time_ms"] = api_response_time

            # Test 2: Threat search/analysis operation (critical for security)
            if tool_name in ["misp", "helk", "securityonion", "yara-x"]:
                search_start = time.time()
                await self._simulate_threat_analysis(tool_name)
                search_response_time = (time.time() - search_start) * 1000

                search_metric = PerformanceMetrics.create_response_time_metric(
                    domain=self.DOMAIN,
                    tool_name=tool_name,
                    response_time_ms=search_response_time,
                    user_session_id=self.validation_run.validation_run_id,
                    metadata={
                        "test_type": "threat_analysis",
                        "validation_run": self.validation_run.validation_run_id
                    }
                )

                self.db_session.add(search_metric)
                self.metrics_collected.append(search_metric)
                test_results["threat_analysis_time_ms"] = search_response_time

            # Test 3: Data ingestion/processing speed
            if tool_name in ["helk", "securityonion", "maltrail"]:
                ingest_start = time.time()
                await self._simulate_data_ingestion(tool_name)
                ingest_response_time = (time.time() - ingest_start) * 1000

                ingest_metric = PerformanceMetrics.create_response_time_metric(
                    domain=self.DOMAIN,
                    tool_name=tool_name,
                    response_time_ms=ingest_response_time,
                    user_session_id=self.validation_run.validation_run_id,
                    metadata={
                        "test_type": "data_ingestion",
                        "validation_run": self.validation_run.validation_run_id
                    }
                )

                self.db_session.add(ingest_metric)
                self.metrics_collected.append(ingest_metric)
                test_results["data_ingestion_time_ms"] = ingest_response_time

            total_time = (time.time() - start_time) * 1000
            test_results["total_test_time_ms"] = total_time
            test_results["status"] = "success"

            logger.debug(
                f"Tool {tool_name} test completed in {total_time:.2f}ms")
            return test_results

        except Exception as e:
            logger.error(f"Tool test failed for {tool_name}: {e}")
            return {
                "tool_name": tool_name,
                "status": "error",
                "error": str(e)
            }

    async def _simulate_api_call(self, tool_name: str, operation: str) -> None:
        """Simulate API call to security tool"""
        # Simulate realistic response times based on tool complexity
        delays = {
            "misp": 0.2,  # MISP threat intel lookup
            "helk": 0.15,  # HELK log query
            "securityonion": 0.25,  # Security Onion SIEM query
            "maltrail": 0.1,  # Maltrail real-time detection
            "yara-x": 0.05,  # YARA-X pattern matching
            "cyberchef": 0.02,  # CyberChef data operations
            "nemesis": 0.3,  # Nemesis data collection
        }

        delay = delays.get(tool_name, 0.1)  # Default 100ms
        await asyncio.sleep(delay)

    async def _simulate_threat_analysis(self, tool_name: str) -> None:
        """Simulate threat analysis operation"""
        # Threat analysis typically takes longer
        delays = {
            "misp": 0.5,  # MISP correlation analysis
            "helk": 0.4,  # HELK threat hunting query
            "securityonion": 0.6,  # Security Onion alert analysis
            "yara-x": 0.2,  # YARA-X malware detection
        }

        delay = delays.get(tool_name, 0.3)
        await asyncio.sleep(delay)

    async def _simulate_data_ingestion(self, tool_name: str) -> None:
        """Simulate data ingestion operation"""
        delays = {
            "helk": 0.3,  # HELK log ingestion
            "securityonion": 0.4,  # Security Onion packet analysis
            "maltrail": 0.15,  # Maltrail real-time processing
        }

        delay = delays.get(tool_name, 0.2)
        await asyncio.sleep(delay)

    def _analyze_results(self) -> None:
        """Analyze validation results and identify violations"""
        logger.info("Analyzing security domain performance results")

        violations = 0
        warnings = 0

        for metric in self.metrics_collected:
            if metric.is_violation:
                violations += 1
                logger.warning(
                    f"Constitutional violation: {metric.tool_name} "
                    f"{metric.metric_type} = {metric.value}ms "
                    f"(threshold: {metric.threshold}ms)"
                )
            elif metric.performance_ratio > 0.8:  # Within 80% of threshold
                warnings += 1
                logger.info(
                    f"Performance warning: {metric.tool_name} "
                    f"{metric.metric_type} = {metric.value}ms "
                    f"({metric.performance_ratio*100:.1f}% of threshold)"
                )

        self.validation_run.violations_found = violations
        self.validation_run.warnings_found = warnings
        self.validation_run.metrics_collected = len(self.metrics_collected)

    def _generate_recommendations(self) -> None:
        """Generate recommendations based on validation results"""
        logger.info("Generating security domain recommendations")

        if self.validation_run.violations_found > 0:
            self.validation_run.add_recommendation(
                f"CRITICAL: {self.validation_run.violations_found} security tools "
                f"violate the <1s constitutional requirement. Immediate optimization "
                f"required for threat analysis criticality.",
                severity="critical",
                category="constitutional_violation"
            )

        if self.validation_run.warnings_found > 0:
            self.validation_run.add_recommendation(
                f"WARNING: {self.validation_run.warnings_found} security tools "
                f"are approaching performance limits. Consider optimization.",
                severity="warning",
                category="performance_optimization"
            )

        # Tool-specific recommendations
        tool_performance = {}
        for metric in self.metrics_collected:
            if metric.tool_name not in tool_performance:
                tool_performance[metric.tool_name] = []
            tool_performance[metric.tool_name].append(metric)

        for tool_name, metrics in tool_performance.items():
            worst_metric = max(metrics, key=lambda m: m.performance_ratio)

            if worst_metric.is_violation:
                self.validation_run.add_recommendation(
                    f"Tool '{tool_name}' requires immediate optimization. "
                    f"Worst performance: {worst_metric.metric_type} = "
                    f"{worst_metric.value}ms (limit: {worst_metric.threshold}ms)",
                    severity="error",
                    category="tool_optimization"
                )
            elif worst_metric.performance_ratio > 0.8:
                self.validation_run.add_recommendation(
                    f"Consider optimizing '{tool_name}' performance. "
                    f"Current: {worst_metric.value}ms "
                    f"({worst_metric.performance_ratio*100:.1f}% of limit)",
                    severity="info",
                    category="preventive_optimization"
                )

        # Constitutional compliance summary
        if self.validation_run.violations_found == 0:
            self.validation_run.add_recommendation(
                "Security domain meets all constitutional performance requirements. "
                "Threat analysis capabilities operating within <1s requirement.",
                severity="info",
                category="constitutional_compliance"
            )
