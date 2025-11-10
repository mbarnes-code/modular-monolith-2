#!/usr/bin/env python3
"""
Performance Testing Script - T136
Constitutional performance validation
"""

import asyncio
import json
import time

import httpx


async def test_domain_performance(domain, endpoint, threshold_ms):
    """Test domain performance against constitutional requirements"""
    print(f"Testing {domain} domain: {endpoint} (<{threshold_ms}ms)")

    response_times = []
    base_url = "http://localhost:8000"

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            for i in range(10):
                start_time = time.time()
                try:
                    response = await client.get(f"{base_url}{endpoint}")
                    response_time_ms = (time.time() - start_time) * 1000
                    response_times.append(response_time_ms)
                except Exception:
                    print(f"  Request {i+1} failed")

        if response_times:
            avg_time = sum(response_times) / len(response_times)
            max_time = max(response_times)
            status = "✅ PASS" if avg_time < threshold_ms else "❌ FAIL"

            print(f"  Average: {avg_time:.1f}ms")
            print(f"  Max: {max_time:.1f}ms")
            print(f"  Status: {status}")

            return {
                "domain": domain,
                "endpoint": endpoint,
                "avg_response_time": avg_time,
                "max_response_time": max_time,
                "threshold": threshold_ms,
                "compliant": avg_time < threshold_ms
            }
    except Exception as e:
        print(f"  Error testing {domain}: {e}")

    return None


async def test_ui_performance():
    """Test UI response times for executive function support"""
    print("Testing UI performance (<200ms)")

    ui_endpoints = ["/", "/api/health"]
    results = []

    for endpoint in ui_endpoints:
        result = await test_domain_performance("UI", endpoint, 200)
        if result:
            results.append(result)

    return results


async def main():
    """Main performance testing function"""
    print("🎯 Constitutional Performance Testing")
    print("=" * 50)

    results = []

    # Domain performance tests
    domain_tests = [
        ("Security", "/api/security/status", 1000),      # <1s
        ("Productivity", "/api/productivity/tasks", 2000),  # <2s
        ("MTG", "/api/mtg/cards", 3000),                 # <3s
        ("Infrastructure", "/api/infrastructure/health", 5000)  # <5s
    ]

    for domain, endpoint, threshold in domain_tests:
        result = await test_domain_performance(domain, endpoint, threshold)
        if result:
            results.append(result)
        print()

    # UI performance tests
    ui_results = await test_ui_performance()
    results.extend(ui_results)

    # Generate report
    report = {
        "timestamp": time.time(),
        "constitutional_requirements": {
            "security_threshold_ms": 1000,
            "productivity_threshold_ms": 2000,
            "mtg_threshold_ms": 3000,
            "infrastructure_threshold_ms": 5000,
            "ui_threshold_ms": 200
        },
        "results": results,
        "summary": {
            "total_tests": len(results),
            "compliant_tests": len([r for r in results if r.get("compliant", False)]),
            "compliance_rate": len([r for r in results if r.get("compliant", False)]) / len(results) if results else 0
        }
    }

    # Save report
    with open("performance_test_results.json", "w") as f:
        json.dump(report, f, indent=2)

    print("📊 SUMMARY")
    print(f"Total tests: {report['summary']['total_tests']}")
    print(f"Compliant: {report['summary']['compliant_tests']}")
    print(f"Compliance rate: {report['summary']['compliance_rate']:.1%}")
    print("Report saved: performance_test_results.json")


if __name__ == "__main__":
    asyncio.run(main())
