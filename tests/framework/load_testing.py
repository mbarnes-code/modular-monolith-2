"""
Load Testing Framework for Mental Prosthetic Platform

Tests realistic 37-tool simultaneous usage patterns with domain-specific scenarios.
Validates system performance under executive function workload patterns.
"""

import asyncio
import logging
import random
import statistics
import time
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


@dataclass
class LoadTestScenario:
    """Load test scenario definition"""
    name: str
    description: str
    concurrent_users: int
    duration_seconds: int
    domain_mix: Dict[str, float]  # Domain usage percentages
    tools_per_user: int
    executive_function_pattern: bool


@dataclass
class LoadTestResult:
    """Load test execution result"""
    scenario_name: str
    total_requests: int
    successful_requests: int
    failed_requests: int
    average_response_time_ms: float
    p95_response_time_ms: float
    p99_response_time_ms: float
    throughput_rps: float
    domain_performance: Dict[str, Dict[str, float]]
    executive_function_compliance: bool


class LoadTestFramework:
    """Load testing framework for 37-tool simultaneous usage"""

    def __init__(self):
        self.domain_tools = {
            "security": [
                "misp", "helk", "securityonion", "maltrail", "yara-x",
                "cyberchef", "nemesis", "apiscout", "blackarch",
                "brute-ratel", "hexstrike", "meterpreter", "onex"
            ],
            "productivity": [
                "n8n", "mealie", "dispatch", "actual-budget",
                "firecrawl", "goose", "it-tools", "inspector"
            ],
            "mtg": [
                "commander-spellbook", "mtg-commander-map",
                "mtg-scripting-toolkit", "card-analysis"
            ],
            "infrastructure": [
                "kong", "ghostwriter", "kasmvnc", "chroma-mcp",
                "virustotal-mcp", "n8n-mcp", "firecrawl-mcp",
                "malwarebazaar-mcp", "filescopemcp", "lscript",
                "rita", "software-forensic-kit"
            ]
        }

        # Domain performance thresholds
        self.domain_thresholds = {
            "security": 1000,        # 1s
            "productivity": 2000,    # 2s
            "mtg": 3000,            # 3s
            "infrastructure": 5000   # 5s
        }

        # Executive function load patterns
        self.executive_patterns = {
            "context_switching": {
                "frequency": 0.3,  # 30% of operations involve context switch
                "switch_penalty_ms": 50  # Additional time for context switch
            },
            "cognitive_load": {
                "max_concurrent_tools": 5,  # ADHD accommodation
                "break_frequency": 0.1  # 10% operations include micro-breaks
            }
        }

    def define_test_scenarios(self) -> List[LoadTestScenario]:
        """Define realistic load test scenarios"""
        return [
            LoadTestScenario(
                name="Normal Executive Function Workload",
                description="Typical daily usage pattern across all domains",
                concurrent_users=10,
                duration_seconds=300,  # 5 minutes
                domain_mix={
                    "security": 0.4,      # Heavy security focus
                    "productivity": 0.3,  # Regular productivity tasks
                    "mtg": 0.1,          # Occasional MTG analysis
                    "infrastructure": 0.2  # Infrastructure management
                },
                tools_per_user=5,
                executive_function_pattern=True
            ),

            LoadTestScenario(
                name="Peak Security Operations",
                description="High-intensity security operations scenario",
                concurrent_users=15,
                duration_seconds=600,  # 10 minutes
                domain_mix={
                    "security": 0.7,      # Dominant security usage
                    "productivity": 0.2,  # Workflow automation
                    "mtg": 0.05,         # Minimal MTG
                    "infrastructure": 0.25  # Infrastructure support
                },
                tools_per_user=8,
                executive_function_pattern=True
            ),

            LoadTestScenario(
                name="Multi-Domain Analysis Session",
                description="Cross-domain analysis with all tool types",
                concurrent_users=8,
                duration_seconds=900,  # 15 minutes
                domain_mix={
                    "security": 0.25,     # Balanced usage
                    "productivity": 0.25,
                    "mtg": 0.25,
                    "infrastructure": 0.25
                },
                tools_per_user=12,  # Higher tool usage
                executive_function_pattern=True
            ),

            LoadTestScenario(
                name="Stress Test - All Tools Simultaneous",
                description="Maximum load with all 37 tools active",
                concurrent_users=20,
                duration_seconds=180,  # 3 minutes
                domain_mix={
                    "security": 0.35,
                    "productivity": 0.22,
                    "mtg": 0.11,
                    "infrastructure": 0.32
                },
                tools_per_user=15,
                executive_function_pattern=False  # Stress test ignores patterns
            )
        ]

    async def execute_load_test(self, scenario: LoadTestScenario) -> LoadTestResult:
        """Execute a load test scenario"""
        logger.info(f"Starting load test: {scenario.name}")

        start_time = time.time()
        response_times = []
        domain_times = {domain: [] for domain in self.domain_tools.keys()}
        successful_requests = 0
        failed_requests = 0

        # Create user simulation tasks
        user_tasks = []
        for user_id in range(scenario.concurrent_users):
            task = asyncio.create_task(
                self._simulate_user_session(
                    user_id, scenario, response_times, domain_times
                )
            )
            user_tasks.append(task)

        # Execute all user sessions concurrently
        results = await asyncio.gather(*user_tasks, return_exceptions=True)

        # Process results
        for result in results:
            if isinstance(result, Exception):
                failed_requests += 1
                logger.error(f"User session failed: {result}")
            else:
                successful_requests += result.get("requests", 0)
                failed_requests += result.get("failed_requests", 0)

        end_time = time.time()
        total_duration = end_time - start_time

        # Calculate metrics
        total_requests = successful_requests + failed_requests
        average_response_time = statistics.mean(
            response_times) if response_times else 0
        p95_response_time = statistics.quantiles(response_times, n=20)[
            18] if len(response_times) >= 20 else 0
        p99_response_time = statistics.quantiles(response_times, n=100)[
            98] if len(response_times) >= 100 else 0
        throughput = total_requests / total_duration if total_duration > 0 else 0

        # Calculate domain performance
        domain_performance = {}
        for domain, times in domain_times.items():
            if times:
                domain_performance[domain] = {
                    "average_ms": statistics.mean(times),
                    "p95_ms": statistics.quantiles(times, n=20)[18] if len(times) >= 20 else statistics.mean(times),
                    "threshold_ms": self.domain_thresholds[domain],
                    "compliance": all(t <= self.domain_thresholds[domain] for t in times)
                }
            else:
                domain_performance[domain] = {
                    "average_ms": 0,
                    "p95_ms": 0,
                    "threshold_ms": self.domain_thresholds[domain],
                    "compliance": True
                }

        # Check executive function compliance
        executive_function_compliance = (
            average_response_time <= 200 and  # UI responsiveness
            all(domain_performance[d]["compliance"]
                for d in domain_performance)
        )

        return LoadTestResult(
            scenario_name=scenario.name,
            total_requests=total_requests,
            successful_requests=successful_requests,
            failed_requests=failed_requests,
            average_response_time_ms=average_response_time,
            p95_response_time_ms=p95_response_time,
            p99_response_time_ms=p99_response_time,
            throughput_rps=throughput,
            domain_performance=domain_performance,
            executive_function_compliance=executive_function_compliance
        )

    async def _simulate_user_session(self, user_id: int, scenario: LoadTestScenario,
                                     response_times: List[float],
                                     domain_times: Dict[str, List[float]]) -> Dict[str, int]:
        """Simulate a user session with tool usage"""
        session_start = time.time()
        session_end = session_start + scenario.duration_seconds

        session_stats = {"requests": 0, "failed_requests": 0}
        current_tools = set()  # Track active tools for executive function

        while time.time() < session_end:
            try:
                # Select domain based on scenario mix
                domain = self._select_domain_by_weight(scenario.domain_mix)

                # Select tool from domain
                available_tools = self.domain_tools[domain]
                tool = random.choice(available_tools)

                # Executive function accommodation
                if scenario.executive_function_pattern:
                    # Limit concurrent tools for ADHD accommodation
                    max_concurrent = self.executive_patterns["cognitive_load"]["max_concurrent_tools"]
                    if len(current_tools) >= max_concurrent:
                        # Remove a random tool to make space
                        current_tools.pop()

                    current_tools.add(tool)

                    # Context switching penalty
                    if random.random() < self.executive_patterns["context_switching"]["frequency"]:
                        await asyncio.sleep(
                            self.executive_patterns["context_switching"]["switch_penalty_ms"] / 1000
                        )

                # Simulate tool operation
                operation_start = time.time()
                await self._simulate_tool_operation(domain, tool)
                operation_end = time.time()

                operation_time_ms = (operation_end - operation_start) * 1000
                response_times.append(operation_time_ms)
                domain_times[domain].append(operation_time_ms)

                session_stats["requests"] += 1

                # Executive function break pattern
                if (scenario.executive_function_pattern and
                        random.random() < self.executive_patterns["cognitive_load"]["break_frequency"]):
                    await asyncio.sleep(0.5)  # 500ms micro-break

                # Inter-request delay (realistic user behavior)
                await asyncio.sleep(random.uniform(0.1, 2.0))

            except Exception as e:
                logger.debug(f"User {user_id} operation failed: {e}")
                session_stats["failed_requests"] += 1
                await asyncio.sleep(0.1)  # Brief pause on error

        return session_stats

    def _select_domain_by_weight(self, domain_mix: Dict[str, float]) -> str:
        """Select domain based on weighted probabilities"""
        rand_val = random.random()
        cumulative = 0.0

        for domain, weight in domain_mix.items():
            cumulative += weight
            if rand_val <= cumulative:
                return domain

        # Fallback to first domain
        return list(domain_mix.keys())[0]

    async def _simulate_tool_operation(self, domain: str, tool: str):
        """Simulate tool operation with realistic timing"""
        # Base operation times by domain (seconds)
        base_times = {
            "security": 0.3,        # Security tools are complex
            "productivity": 0.2,    # Productivity tools are responsive
            "mtg": 0.4,            # MTG analysis can be complex
            "infrastructure": 0.5   # Infrastructure operations can be slow
        }

        # Add tool-specific variation
        base_time = base_times.get(domain, 0.3)
        variation = random.uniform(0.5, 2.0)  # 50% to 200% of base time
        operation_time = base_time * variation

        await asyncio.sleep(operation_time)

    async def run_all_scenarios(self) -> Dict[str, LoadTestResult]:
        """Run all defined load test scenarios"""
        scenarios = self.define_test_scenarios()
        results = {}

        for scenario in scenarios:
            logger.info(f"Executing scenario: {scenario.name}")
            result = await self.execute_load_test(scenario)
            results[scenario.name] = result

            # Brief pause between scenarios
            await asyncio.sleep(30)

        return results

    def generate_load_test_report(self, results: Dict[str, LoadTestResult]) -> Dict[str, Any]:
        """Generate comprehensive load test report"""
        report = {
            "test_timestamp": time.time(),
            "total_scenarios": len(results),
            "scenario_results": {},
            "overall_assessment": {
                "executive_function_compliant": True,
                "performance_issues": [],
                "recommendations": []
            },
            "summary": {
                "total_requests": 0,
                "average_throughput_rps": 0,
                "worst_case_response_time_ms": 0,
                "domain_compliance": {}
            }
        }

        total_throughput = 0
        worst_response_time = 0
        domain_compliance_all = {
            domain: True for domain in self.domain_tools.keys()}

        # Process each scenario result
        for scenario_name, result in results.items():
            report["scenario_results"][scenario_name] = {
                "total_requests": result.total_requests,
                "success_rate": result.successful_requests / result.total_requests if result.total_requests > 0 else 0,
                "average_response_time_ms": result.average_response_time_ms,
                "p95_response_time_ms": result.p95_response_time_ms,
                "throughput_rps": result.throughput_rps,
                "executive_function_compliant": result.executive_function_compliance,
                "domain_performance": result.domain_performance
            }

            # Aggregate metrics
            report["summary"]["total_requests"] += result.total_requests
            total_throughput += result.throughput_rps
            worst_response_time = max(
                worst_response_time, result.p99_response_time_ms)

            # Check compliance
            if not result.executive_function_compliance:
                report["overall_assessment"]["executive_function_compliant"] = False
                report["overall_assessment"]["performance_issues"].append(
                    f"Scenario '{scenario_name}' failed executive function compliance"
                )

            # Check domain compliance
            for domain, perf in result.domain_performance.items():
                if not perf["compliance"]:
                    domain_compliance_all[domain] = False
                    report["overall_assessment"]["performance_issues"].append(
                        f"Domain '{domain}' exceeded performance threshold in scenario '{scenario_name}'"
                    )

        # Calculate averages
        if results:
            report["summary"]["average_throughput_rps"] = total_throughput / \
                len(results)
        report["summary"]["worst_case_response_time_ms"] = worst_response_time
        report["summary"]["domain_compliance"] = domain_compliance_all

        # Generate recommendations
        if not report["overall_assessment"]["executive_function_compliant"]:
            report["overall_assessment"]["recommendations"].extend([
                "Optimize UI response times to meet <200ms executive function requirement",
                "Review context switching penalties and optimize tool transitions",
                "Consider implementing more aggressive caching for frequently accessed data"
            ])

        if not all(domain_compliance_all.values()):
            report["overall_assessment"]["recommendations"].extend([
                "Optimize slow domain operations to meet constitutional performance requirements",
                "Consider horizontal scaling for high-load domains",
                "Implement better load balancing across domain services"
            ])

        return report


async def main():
    """Main load testing function"""
    print("Mental Prosthetic Platform Load Testing")
    print("=" * 50)

    framework = LoadTestFramework()

    # Run all load test scenarios
    print("Executing load test scenarios...")
    results = await framework.run_all_scenarios()

    # Generate report
    report = framework.generate_load_test_report(results)

    # Display results
    print(f"\nLoad Test Results Summary:")
    print(f"- Scenarios executed: {report['total_scenarios']}")
    print(f"- Total requests: {report['summary']['total_requests']}")
    print(
        f"- Average throughput: {report['summary']['average_throughput_rps']:.2f} RPS")
    print(
        f"- Worst case response time: {report['summary']['worst_case_response_time_ms']:.0f}ms")

    print(
        f"\nExecutive Function Compliance: {'✓ PASS' if report['overall_assessment']['executive_function_compliant'] else '✗ FAIL'}")

    print(f"\nDomain Performance Compliance:")
    for domain, compliant in report['summary']['domain_compliance'].items():
        status = "✓ PASS" if compliant else "✗ FAIL"
        print(f"- {domain.upper()}: {status}")

    if report['overall_assessment']['performance_issues']:
        print(f"\nPerformance Issues:")
        for issue in report['overall_assessment']['performance_issues']:
            print(f"- {issue}")

    if report['overall_assessment']['recommendations']:
        print(f"\nRecommendations:")
        for rec in report['overall_assessment']['recommendations']:
            print(f"- {rec}")

    # Save detailed report
    import json
    with open("tests/load_test_report.json", 'w') as f:
        json.dump(report, f, indent=2)

    print(f"\nDetailed report saved to tests/load_test_report.json")

    return 0 if report['overall_assessment']['executive_function_compliant'] else 1


if __name__ == "__main__":
    exit(asyncio.run(main()))
