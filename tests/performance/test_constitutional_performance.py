#!/usr/bin/env python3
"""
Constitutional Performance Testing - T136
Automated performance testing per constitutional requirements
"""

import asyncio
import json
import statistics
import time
from dataclasses import dataclass
from enum import Enum
from typing import Dict, List

import httpx


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
class PerformanceResult:
    """Performance test result"""
    domain: str
    endpoint: str
    avg_response_time: float
    p95_response_time: float
    error_rate: float
    compliance_level: str
    timestamp: float


class PerformanceTester:
    """Constitutional performance validation"""

    THRESHOLDS = {
        Domain.SECURITY: 1000,      # <1s
        Domain.PRODUCTIVITY: 2000,  # <2s
        Domain.MTG: 3000,          # <3s
        Domain.INFRASTRUCTURE: 5000  # <5s
    }

    UI_THRESHOLD_MS = 200  # <200ms for executive function support

    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.results: List[PerformanceResult] = []

    async def test_domain(self, domain: Domain, endpoint: str,
                          num_requests: int = 50) -> PerformanceResult:
        """Test domain performance against constitutional requirements"""
        print(f"Testing {domain.value} domain: {endpoint}")

        response_times: List[float] = []
        errors = 0

        async with httpx.AsyncClient(timeout=30.0) as client:
            for _ in range(num_requests):
                start_time = time.time()
                try:
                    response = await client.get(f"{self.base_url}{endpoint}")
                    response.raise_for_status()
                    response_time_ms = (time.time() - start_time) * 1000
                    response_times.append(response_time_ms)
                except Exception:
                    errors += 1

        if not response_times:
            raise ValueError(f"All requests failed for {endpoint}")

        # Calculate metrics
        avg_response = statistics.mean(response_times)
        p95_response = self._percentile(response_times, 95)
        error_rate = errors / num_requests

        # Check compliance
        threshold = self.THRESHOLDS[domain]
        compliance = self._check_compliance(avg_response, threshold)

        result = PerformanceResult(
            domain=domain.value,
            endpoint=endpoint,
            avg_response_time=avg_response,
            p95_response_time=p95_response,
            error_rate=error_rate,
            compliance_level=compliance.value,
            timestamp=time.time()
        )

        self.results.append(result)
        self._print_result(result, threshold)
        return result

    async def test_ui_response(self, endpoints: List[str]) -> Dict[str, float]:
        """Test UI response times for executive function support"""
        print("Testing UI response times (<200ms requirement)")

        results = {}

        async with httpx.AsyncClient(timeout=5.0) as client:
            for endpoint in endpoints:
                response_times = []

                for _ in range(20):
                    start_time = time.time()
                    try:
                        response = await client.get(f"{self.base_url}{endpoint}")
                        response.raise_for_status()
                        response_time_ms = (time.time() - start_time) * 1000
                        response_times.append(response_time_ms)
                    except Exception:
                        pass

                if response_times:
                    avg_response = statistics.mean(response_times)
                    results[endpoint] = avg_response
                    status = "✅ PASS" if avg_response < self.UI_THRESHOLD_MS else "❌ FAIL"
                    print(f"{endpoint}: {avg_response:.1f}ms - {status}")

        return results

    def _percentile(self, data: List[float], percentile: int) -> float:
        """Calculate percentile"""
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

    def _check_compliance(self, avg_time: float, threshold: int) -> ComplianceLevel:
        """Check constitutional compliance"""
        if avg_time > threshold:
            return ComplianceLevel.FAIL
        elif avg_time > threshold * 0.8:  # Warning at 80%
            return ComplianceLevel.WARNING
        else:
            return ComplianceLevel.PASS

    def _print_result(self, result: PerformanceResult, threshold: int):
        """Print test result"""
        status_icons = {
            "pass": "✅",
            "warning": "⚠️",
            "fail": "❌"
        }

        icon = status_icons.get(result.compliance_level, "?")
        print(f"{icon} {result.domain.upper()} DOMAIN")
        print(f"  Average: {result.avg_response_time:.1f}ms "
              f"(threshold: {threshold}ms)")
        print(f"  P95: {result.p95_response_time:.1f}ms")
        print(f"  Error Rate: {result.error_rate:.2%}")
        print(f"  Compliance: {result.compliance_level.upper()}")

    def generate_report(self, filename: str = "performance_report.json"):
        """Generate performance report"""
        report = {
            "timestamp": time.time(),
            "constitutional_requirements": {
                "ui_threshold_ms": self.UI_THRESHOLD_MS,
                "domain_thresholds": {
                    domain.value: threshold
                    for domain, threshold in self.THRESHOLDS.items()
                }
            },
            "results": [
                {
                    "domain": r.domain,
                    "endpoint": r.endpoint,
                    "avg_response_time": r.avg_response_time,
                    "p95_response_time": r.p95_response_time,
                    "error_rate": r.error_rate,
                    "compliance_level": r.compliance_level,
                    "timestamp": r.timestamp
                }
                for r in self.results
            ],
            "summary": self._get_summary()
        }

        with open(filename, 'w') as f:
            json.dump(report, f, indent=2)

        print(f"📊 Report saved: {filename}")
        return report

    def _get_summary(self) -> Dict:
        """Generate summary statistics"""
        if not self.results:
            return {"total_tests": 0}

        total = len(self.results)
        passed = len([r for r in self.results if r.compliance_level == "pass"])
        warnings = len(
            [r for r in self.results if r.compliance_level == "warning"])
        failed = len([r for r in self.results if r.compliance_level == "fail"])

        return {
            "total_tests": total,
            "passed": passed,
            "warnings": warnings,
            "failed": failed,
            "compliance_rate": passed / total if total > 0 else 0
        }


async def main():
    """Main performance testing CLI"""
    print("🎯 Constitutional Performance Testing")
    print("Testing executive function accommodations\n")

    tester = PerformanceTester()

    # Test domain performance
    domains_to_test = [
        (Domain.SECURITY, "/api/security/status"),
        (Domain.PRODUCTIVITY, "/api/productivity/tasks"),
        (Domain.MTG, "/api/mtg/cards"),
        (Domain.INFRASTRUCTURE, "/api/infrastructure/health")
    ]

    for domain, endpoint in domains_to_test:
        try:
            await tester.test_domain(domain, endpoint)
        except Exception as e:
            print(f"❌ Failed to test {domain.value}: {e}")

    # Test UI response times
    ui_endpoints = ["/", "/api/health"]
    try:
        await tester.test_ui_response(ui_endpoints)
    except Exception as e:
        print(f"❌ Failed to test UI: {e}")

    # Generate report
    report = tester.generate_report()

    # Print summary
    summary = report["summary"]
    print(f"\n🎯 SUMMARY")
    print(f"Tests: {summary.get('total_tests', 0)}")
    print(f"Passed: {summary.get('passed', 0)} ✅")
    print(f"Warnings: {summary.get('warnings', 0)} ⚠️")
    print(f"Failed: {summary.get('failed', 0)} ❌")
    print(f"Compliance: {summary.get('compliance_rate', 0):.1%}")


if __name__ == "__main__":
    asyncio.run(main())
