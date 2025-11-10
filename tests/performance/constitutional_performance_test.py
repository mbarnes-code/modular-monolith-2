"""
Constitutional Performance Testing Framework
T136 Implementation - Automated performance testing scripts per constitutional requirements

This module provides automated performance validation for:
- Domain-specific performance tiers (Security <1s, Productivity <2s, MTG <3s, Infrastructure <5s)
- UI response time validation (<200ms for executive function support)
- Constitutional compliance monitoring
- Performance regression detection
"""

import asyncio
import json
import statistics
import time
from dataclasses import asdict, dataclass
from enum import Enum
from typing import Dict, List, Optional, Tuple

import httpx
import pytest


class Domain(Enum):
    SECURITY = "security"
    PRODUCTIVITY = "productivity"
    MTG = "mtg"
    INFRASTRUCTURE = "infrastructure"


class ComplianceLevel(Enum):
    PASS = "pass"
    WARNING = "warning"
    FAIL = "fail"


@dataclass
class PerformanceThreshold:
    """Constitutional performance thresholds"""
    domain: Domain
    response_time_ms: int
    p95_threshold_ms: int
    p99_threshold_ms: int
    error_rate_threshold: float = 0.05  # 5% max error rate


@dataclass
class PerformanceResult:
    """Performance test result"""
    domain: Domain
    endpoint: str
    avg_response_time: float
    p95_response_time: float
    p99_response_time: float
    min_response_time: float
    max_response_time: float
    error_rate: float
    total_requests: int
    successful_requests: int
    failed_requests: int
    compliance_level: ComplianceLevel
    timestamp: float


class ConstitutionalPerformanceTester:
    """
    Constitutional performance validation framework

    Validates performance against executive function accommodations:
    - Domain-specific performance tiers
    - UI response time requirements
    - ADHD/autism support thresholds
    """

    # Constitutional performance thresholds
    THRESHOLDS = {
        Domain.SECURITY: PerformanceThreshold(
            domain=Domain.SECURITY,
            response_time_ms=1000,  # <1s
            p95_threshold_ms=800,   # P95 should be well under threshold
            p99_threshold_ms=950    # P99 close to but under threshold
        ),
        Domain.PRODUCTIVITY: PerformanceThreshold(
            domain=Domain.PRODUCTIVITY,
            response_time_ms=2000,  # <2s
            p95_threshold_ms=1600,
            p99_threshold_ms=1900
        ),
        Domain.MTG: PerformanceThreshold(
            domain=Domain.MTG,
            response_time_ms=3000,  # <3s
            p95_threshold_ms=2400,
            p99_threshold_ms=2850
        ),
        Domain.INFRASTRUCTURE: PerformanceThreshold(
            domain=Domain.INFRASTRUCTURE,
            response_time_ms=5000,  # <5s
            p95_threshold_ms=4000,
            p99_threshold_ms=4750
        )
    }

    # UI response time for executive function support
    UI_RESPONSE_THRESHOLD_MS = 200  # <200ms for ADHD/autism accommodations

    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.results: List[PerformanceResult] = []

    async def test_domain_performance(
        self,
        domain: Domain,
        endpoint: str,
        num_requests: int = 100,
        concurrency: int = 10
    ) -> PerformanceResult:
        """
        Test performance for a specific domain endpoint

        Args:
            domain: Domain to test (Security, Productivity, MTG, Infrastructure)
            endpoint: API endpoint to test
            num_requests: Total number of requests to send
            concurrency: Number of concurrent requests

        Returns:
            PerformanceResult with detailed metrics
        """
        print(f"Testing {domain.value} domain endpoint: {endpoint}")

        threshold = self.THRESHOLDS[domain]
        response_times: List[float] = []
        errors = 0

        async with httpx.AsyncClient(timeout=30.0) as client:
            # Create semaphore to limit concurrency
            semaphore = asyncio.Semaphore(concurrency)

            async def make_request() -> float:
                async with semaphore:
                    start_time = time.time()
                    try:
                        response = await client.get(f"{self.base_url}{endpoint}")
                        response.raise_for_status()
                        # Convert to ms
                        return (time.time() - start_time) * 1000
                    except Exception as e:
                        print(f"Request failed: {e}")
                        return -1  # Error marker

            # Execute all requests
            tasks = [make_request() for _ in range(num_requests)]
            results = await asyncio.gather(*tasks)

            # Process results
            for result in results:
                if result > 0:
                    response_times.append(result)
                else:
                    errors += 1

        if not response_times:
            raise ValueError(f"All requests failed for {endpoint}")

        # Calculate metrics
        avg_response = statistics.mean(response_times)
        p95_response = self._percentile(response_times, 95)
        p99_response = self._percentile(response_times, 99)
        min_response = min(response_times)
        max_response = max(response_times)
        error_rate = errors / num_requests

        # Determine compliance level
        compliance = self._determine_compliance(
            avg_response, p95_response, p99_response, error_rate, threshold
        )

        result = PerformanceResult(
            domain=domain,
            endpoint=endpoint,
            avg_response_time=avg_response,
            p95_response_time=p95_response,
            p99_response_time=p99_response,
            min_response_time=min_response,
            max_response_time=max_response,
            error_rate=error_rate,
            total_requests=num_requests,
            successful_requests=len(response_times),
            failed_requests=errors,
            compliance_level=compliance,
            timestamp=time.time()
        )

        self.results.append(result)
        self._print_result(result, threshold)
        return result

    async def test_ui_response_time(
        self,
        ui_endpoints: List[str],
        num_requests: int = 50
    ) -> Dict[str, PerformanceResult]:
        """
        Test UI response times for executive function support

        UI responses must be <200ms for ADHD/autism accommodations

        Args:
            ui_endpoints: List of UI endpoints to test
            num_requests: Number of requests per endpoint

        Returns:
            Dictionary of endpoint -> PerformanceResult
        """
        print("Testing UI response times for executive function support")
        print(
            f"Constitutional requirement: <{self.UI_RESPONSE_THRESHOLD_MS}ms")

        results = {}

        for endpoint in ui_endpoints:
            print(f"\nTesting UI endpoint: {endpoint}")

            response_times = []
            errors = 0

            async with httpx.AsyncClient(timeout=5.0) as client:
                for _ in range(num_requests):
                    start_time = time.time()
                    try:
                        response = await client.get(f"{self.base_url}{endpoint}")
                        response.raise_for_status()
                        response_time_ms = (time.time() - start_time) * 1000
                        response_times.append(response_time_ms)
                    except Exception as e:
                        print(f"UI request failed: {e}")
                        errors += 1

            if response_times:
                avg_response = statistics.mean(response_times)
                p95_response = self._percentile(response_times, 95)
                p99_response = self._percentile(response_times, 99)

                # UI compliance check
                ui_compliant = (
                    avg_response < self.UI_RESPONSE_THRESHOLD_MS and
                    p95_response < self.UI_RESPONSE_THRESHOLD_MS * 1.2  # Allow 20% margin for P95
                )

                compliance = ComplianceLevel.PASS if ui_compliant else ComplianceLevel.FAIL

                result = PerformanceResult(
                    domain=Domain.PRODUCTIVITY,  # UI is part of productivity domain
                    endpoint=endpoint,
                    avg_response_time=avg_response,
                    p95_response_time=p95_response,
                    p99_response_time=p99_response,
                    min_response_time=min(response_times),
                    max_response_time=max(response_times),
                    error_rate=errors / num_requests,
                    total_requests=num_requests,
                    successful_requests=len(response_times),
                    failed_requests=errors,
                    compliance_level=compliance,
                    timestamp=time.time()
                )

                results[endpoint] = result
                print(
                    f"UI Response: {avg_response:.1f}ms avg, {p95_response:.1f}ms P95 - {'✅ PASS' if ui_compliant else '❌ FAIL'}")

        return results

    def _percentile(self, data: List[float], percentile: int) -> float:
        """Calculate percentile value"""
        if not data:
            return 0.0
        sorted_data = sorted(data)
        index = (percentile / 100) * (len(sorted_data) - 1)
        if index == int(index):
            return sorted_data[int(index)]
        else:
            lower = sorted_data[int(index)]
            upper = sorted_data[int(index) + 1]
            return lower + (upper - lower) * (index - int(index))

    def _determine_compliance(
        self,
        avg: float,
        p95: float,
        p99: float,
        error_rate: float,
        threshold: PerformanceThreshold
    ) -> ComplianceLevel:
        """Determine constitutional compliance level"""

        # Critical failure conditions
        if (avg > threshold.response_time_ms or
            p95 > threshold.p95_threshold_ms or
                error_rate > threshold.error_rate_threshold):
            return ComplianceLevel.FAIL

        # Warning conditions (approaching limits)
        if (avg > threshold.response_time_ms * 0.8 or
                p95 > threshold.p95_threshold_ms * 0.8):
            return ComplianceLevel.WARNING

        return ComplianceLevel.PASS

    def _print_result(self, result: PerformanceResult, threshold: PerformanceThreshold):
        """Print formatted test result"""
        status_icon = {
            ComplianceLevel.PASS: "✅",
            ComplianceLevel.WARNING: "⚠️",
            ComplianceLevel.FAIL: "❌"
        }

        print(
            f"\n{status_icon[result.compliance_level]} {result.domain.value.upper()} DOMAIN RESULTS")
        print(f"Endpoint: {result.endpoint}")
        print(
            f"Average Response: {result.avg_response_time:.1f}ms (threshold: {threshold.response_time_ms}ms)")
        print(
            f"P95 Response: {result.p95_response_time:.1f}ms (threshold: {threshold.p95_threshold_ms}ms)")
        print(
            f"P99 Response: {result.p99_response_time:.1f}ms (threshold: {threshold.p99_threshold_ms}ms)")
        print(
            f"Error Rate: {result.error_rate:.2%} (threshold: {threshold.error_rate_threshold:.2%})")
        print(
            f"Requests: {result.successful_requests}/{result.total_requests} successful")
        print(f"Compliance: {result.compliance_level.value.upper()}")

    def generate_report(self, output_file: str = "performance_report.json"):
        """Generate comprehensive performance report"""
        report = {
            "timestamp": time.time(),
            "constitutional_requirements": {
                "ui_response_threshold_ms": self.UI_RESPONSE_THRESHOLD_MS,
                "domain_thresholds": {
                    domain.value: {
                        "response_time_ms": threshold.response_time_ms,
                        "p95_threshold_ms": threshold.p95_threshold_ms,
                        "p99_threshold_ms": threshold.p99_threshold_ms,
                        "error_rate_threshold": threshold.error_rate_threshold
                    }
                    for domain, threshold in self.THRESHOLDS.items()
                }
            },
            "results": [asdict(result) for result in self.results],
            "summary": self._generate_summary()
        }

        with open(output_file, 'w') as f:
            json.dump(report, f, indent=2, default=str)

        print(f"\n📊 Performance report saved to: {output_file}")
        return report

    def _generate_summary(self) -> Dict:
        """Generate performance summary"""
        if not self.results:
            return {"error": "No test results available"}

        total_tests = len(self.results)
        passed_tests = len(
            [r for r in self.results if r.compliance_level == ComplianceLevel.PASS])
        warning_tests = len(
            [r for r in self.results if r.compliance_level == ComplianceLevel.WARNING])
        failed_tests = len(
            [r for r in self.results if r.compliance_level == ComplianceLevel.FAIL])

        domain_summary = {}
        for domain in Domain:
            domain_results = [r for r in self.results if r.domain == domain]
            if domain_results:
                domain_summary[domain.value] = {
                    "total_tests": len(domain_results),
                    "avg_response_time": statistics.mean([r.avg_response_time for r in domain_results]),
                    "compliance_rate": len([r for r in domain_results if r.compliance_level == ComplianceLevel.PASS]) / len(domain_results)
                }

        return {
            "total_tests": total_tests,
            "passed_tests": passed_tests,
            "warning_tests": warning_tests,
            "failed_tests": failed_tests,
            "overall_compliance_rate": passed_tests / total_tests if total_tests > 0 else 0,
            "domain_summary": domain_summary
        }


# Pytest integration for CI/CD pipeline
class TestConstitutionalPerformance:
    """Pytest test class for constitutional performance validation"""

    @pytest.fixture
    def tester(self):
        return ConstitutionalPerformanceTester()

    @pytest.mark.asyncio
    async def test_security_domain_performance(self, tester):
        """Test Security domain <1s requirement"""
        result = await tester.test_domain_performance(
            Domain.SECURITY,
            "/api/security/threat-analysis",
            num_requests=50
        )
        assert result.compliance_level != ComplianceLevel.FAIL, f"Security domain failed: {result.avg_response_time}ms avg"

    @pytest.mark.asyncio
    async def test_productivity_domain_performance(self, tester):
        """Test Productivity domain <2s requirement"""
        result = await tester.test_domain_performance(
            Domain.PRODUCTIVITY,
            "/api/productivity/task-list",
            num_requests=50
        )
        assert result.compliance_level != ComplianceLevel.FAIL, f"Productivity domain failed: {result.avg_response_time}ms avg"

    @pytest.mark.asyncio
    async def test_mtg_domain_performance(self, tester):
        """Test MTG domain <3s requirement"""
        result = await tester.test_domain_performance(
            Domain.MTG,
            "/api/mtg/card-analysis",
            num_requests=30
        )
        assert result.compliance_level != ComplianceLevel.FAIL, f"MTG domain failed: {result.avg_response_time}ms avg"

    @pytest.mark.asyncio
    async def test_infrastructure_domain_performance(self, tester):
        """Test Infrastructure domain <5s requirement"""
        result = await tester.test_domain_performance(
            Domain.INFRASTRUCTURE,
            "/api/infrastructure/system-status",
            num_requests=30
        )
        assert result.compliance_level != ComplianceLevel.FAIL, f"Infrastructure domain failed: {result.avg_response_time}ms avg"

    @pytest.mark.asyncio
    async def test_ui_executive_function_support(self, tester):
        """Test UI response times for executive function support (<200ms)"""
        ui_endpoints = [
            "/",
            "/performance-validation",
            "/api/health"
        ]

        results = await tester.test_ui_response_time(ui_endpoints)

        for endpoint, result in results.items():
            assert result.compliance_level == ComplianceLevel.PASS, \
                f"UI endpoint {endpoint} failed executive function requirement: {result.avg_response_time}ms > 200ms"


# CLI interface for manual testing
async def main():
    """Main CLI interface for performance testing"""
    print("🎯 Constitutional Performance Testing Framework")
    print("Testing executive function accommodations and domain performance tiers\n")

    tester = ConstitutionalPerformanceTester()

    # Test all domains
    test_scenarios = [
        (Domain.SECURITY, "/api/security/threat-analysis"),
        (Domain.PRODUCTIVITY, "/api/productivity/task-list"),
        (Domain.MTG, "/api/mtg/card-analysis"),
        (Domain.INFRASTRUCTURE, "/api/infrastructure/system-status")
    ]

    print("🔍 Testing Domain Performance Tiers...")
    for domain, endpoint in test_scenarios:
        try:
            await tester.test_domain_performance(domain, endpoint, num_requests=20)
        except Exception as e:
            print(f"❌ Failed to test {domain.value}: {e}")

    # Test UI response times
    print("\n🖥️ Testing UI Executive Function Support...")
    ui_endpoints = ["/", "/performance-validation", "/api/health"]
    try:
        await tester.test_ui_response_time(ui_endpoints, num_requests=10)
    except Exception as e:
        print(f"❌ Failed to test UI: {e}")

    # Generate report
    print("\n📊 Generating Performance Report...")
    report = tester.generate_report()

    # Print summary
    summary = report["summary"]
    print(f"\n🎯 CONSTITUTIONAL PERFORMANCE SUMMARY")
    print(f"Total Tests: {summary['total_tests']}")
    print(f"Passed: {summary['passed_tests']} ✅")
    print(f"Warnings: {summary['warning_tests']} ⚠️")
    print(f"Failed: {summary['failed_tests']} ❌")
    print(f"Overall Compliance: {summary['overall_compliance_rate']:.1%}")


if __name__ == "__main__":
    asyncio.run(main())
