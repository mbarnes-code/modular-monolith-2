#!/usr/bin/env python3
"""
MISP Comprehensive Test Execution Framework

Purpose: Execute all MISP validation tests and report results
Requirements: T1986 comprehensive testing strategy implementation
Coverage: All test suites with detailed reporting and validation

Test execution includes:
- Threat intelligence core functionality tests
- API integration compatibility tests  
- Performance benchmark validation
- Business logic preservation verification
"""

import json
import logging
import os
import subprocess
import sys
import time
from pathlib import Path
from typing import Any, Dict, List

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Test suite configuration matching Section 7.1-7.2 requirements
TEST_SUITES = {
    'unit_models': {
        'file': 'test_unit_models.py',
        'description': 'Unit tests for MISP model validation and business logic',
        'timeout': 180,  # 3 minutes
        'required_coverage': 85.0,
        'requirement': 'Section 8.1 Unit Tests'
    },
    'functional_workflows': {
        'file': 'test_functional_workflows.py',
        'description': 'Functional tests for MISP component integration and workflows',
        'timeout': 300,  # 5 minutes
        'required_coverage': 80.0,
        'requirement': 'Section 8.2 Functional Tests'
    },
    'integration_external': {
        'file': 'test_integration_external.py',
        'description': 'Integration tests for external system integration and data flow',
        'timeout': 360,  # 6 minutes
        'required_coverage': 75.0,
        'requirement': 'Section 8.3 Integration Tests'
    },
    'plugin_system': {
        'file': 'test_plugin_system.py',
        'description': 'Plugin system tests for dynamic loading and extensibility',
        'timeout': 240,  # 4 minutes
        'required_coverage': 80.0,
        'requirement': 'T2036e Plugin System Testing'
    },
    'multi_target': {
        'file': 'test_multi_target.py',
        'description': 'Multi-target deployment testing (T2046f)',
        'timeout': 300,
        'coverage_required': 85
    },
    'performance_critical': {
        'file': 'test_performance_critical.py',
        'description': 'Performance-critical systems testing (T2056g)',
        'timeout': 600,  # Extended timeout for performance tests
        'coverage_required': 80
    },
    'monorepo_integration': {
        'file': 'test_monorepo_integration.py',
        'description': 'Monorepo integration testing (T2066h)',
        'timeout': 300,
        'coverage_required': 75
    },
    'security': {
        'file': 'test_security.py',
        'description': 'Security controls and authentication testing (T2076i)',
        'timeout': 400,
        'coverage_required': 85
    },
    'threat_intelligence_core': {
        'file': 'test_threat_intelligence_core.py',
        'description': 'Critical threat intelligence algorithms validation',
        'timeout': 300,  # 5 minutes
        'required_coverage': 80.0,
        'requirement': 'Core validation from misp-analysis.md'
    },
    'api_integration': {
        'file': 'test_api_integration.py',
        'description': 'MISP API compatibility validation',
        'timeout': 180,  # 3 minutes
        'required_coverage': 85.0,
        'requirement': 'API compatibility validation'
    },
    'performance_benchmarks': {
        'file': 'test_performance_benchmarks.py',
        'description': 'Performance requirement validation',
        'timeout': 600,  # 10 minutes
        'required_coverage': 70.0,
        'requirement': '<1s security domain response time'
    }
}

# Performance thresholds
PERFORMANCE_THRESHOLDS = {
    'event_creation': 1.0,  # seconds
    'event_search': 1.0,    # seconds
    'correlation_finding': 1.0,  # seconds
    'api_response': 1.0,    # seconds
    'memory_usage': 100,    # MB increase
    'cpu_usage': 80.0       # percent average
}


class MISPTestExecutor:
    """Comprehensive test execution and validation framework"""

    def __init__(self, test_dir: str):
        self.test_dir = Path(test_dir)
        self.results = {}
        self.overall_success = True

    def run_all_tests(self) -> Dict[str, Any]:
        """Execute all MISP test suites and return comprehensive results"""
        logger.info("Starting MISP comprehensive test execution")

        start_time = time.time()

        # Execute each test suite
        for suite_name, suite_config in TEST_SUITES.items():
            logger.info(f"Executing test suite: {suite_name}")
            suite_result = self.run_test_suite(suite_name, suite_config)
            self.results[suite_name] = suite_result

            if not suite_result['success']:
                self.overall_success = False
                logger.error(f"Test suite {suite_name} FAILED")
            else:
                logger.info(f"Test suite {suite_name} PASSED")

        # Generate comprehensive report
        total_time = time.time() - start_time
        final_report = self.generate_final_report(total_time)

        # Validate against business logic preservation requirements
        preservation_validation = self.validate_business_logic_preservation()
        final_report['business_logic_preservation'] = preservation_validation

        return final_report

    def run_test_suite(self, suite_name: str, suite_config: Dict) -> Dict[str, Any]:
        """Execute individual test suite with coverage and performance tracking"""
        test_file = self.test_dir / suite_config['file']

        if not test_file.exists():
            return {
                'success': False,
                'error': f"Test file {test_file} not found",
                'coverage': 0.0,
                'execution_time': 0.0,
                'test_count': 0,
                'passed': 0,
                'failed': 0
            }

        # Prepare pytest command with coverage
        cmd = [
            sys.executable, '-m', 'pytest',
            str(test_file),
            '-v',
            '--tb=short',
            '--json-report',
            '--json-report-file=/tmp/pytest_results.json',
            f'--cov=libs.service_adapters.security.misp_adapter',
            f'--cov=services.security_service',
            '--cov-report=json:/tmp/coverage_results.json',
            '--cov-report=term-missing',
            f'--timeout={suite_config["timeout"]}'
        ]

        try:
            start_time = time.time()
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=suite_config['timeout']
            )
            execution_time = time.time() - start_time

            # Parse pytest results
            pytest_results = self.parse_pytest_results(
                '/tmp/pytest_results.json')
            coverage_results = self.parse_coverage_results(
                '/tmp/coverage_results.json')

            return {
                'success': result.returncode == 0,
                'execution_time': execution_time,
                'coverage': coverage_results.get('total_coverage', 0.0),
                'test_count': pytest_results.get('total', 0),
                'passed': pytest_results.get('passed', 0),
                'failed': pytest_results.get('failed', 0),
                'skipped': pytest_results.get('skipped', 0),
                'stdout': result.stdout,
                'stderr': result.stderr,
                'coverage_meets_requirement': coverage_results.get('total_coverage', 0.0) >= suite_config['required_coverage'],
                'detailed_coverage': coverage_results.get('files', {}),
                'test_details': pytest_results.get('tests', [])
            }

        except subprocess.TimeoutExpired:
            return {
                'success': False,
                'error': f"Test suite timed out after {suite_config['timeout']} seconds",
                'execution_time': suite_config['timeout'],
                'coverage': 0.0,
                'test_count': 0,
                'passed': 0,
                'failed': 0
            }
        except Exception as e:
            return {
                'success': False,
                'error': f"Test execution failed: {str(e)}",
                'execution_time': 0.0,
                'coverage': 0.0,
                'test_count': 0,
                'passed': 0,
                'failed': 0
            }

    def parse_pytest_results(self, results_file: str) -> Dict[str, Any]:
        """Parse pytest JSON results"""
        try:
            if os.path.exists(results_file):
                with open(results_file, 'r') as f:
                    data = json.load(f)
                return {
                    'total': data.get('summary', {}).get('total', 0),
                    'passed': data.get('summary', {}).get('passed', 0),
                    'failed': data.get('summary', {}).get('failed', 0),
                    'skipped': data.get('summary', {}).get('skipped', 0),
                    'tests': data.get('tests', [])
                }
        except Exception as e:
            logger.warning(f"Failed to parse pytest results: {e}")

        return {'total': 0, 'passed': 0, 'failed': 0, 'skipped': 0, 'tests': []}

    def parse_coverage_results(self, coverage_file: str) -> Dict[str, Any]:
        """Parse coverage JSON results"""
        try:
            if os.path.exists(coverage_file):
                with open(coverage_file, 'r') as f:
                    data = json.load(f)

                total_coverage = data.get('totals', {}).get(
                    'percent_covered', 0.0)
                files_coverage = {}

                for filename, file_data in data.get('files', {}).items():
                    files_coverage[filename] = {
                        'coverage': file_data.get('summary', {}).get('percent_covered', 0.0),
                        'missing_lines': file_data.get('missing_lines', []),
                        'statements': file_data.get('summary', {}).get('num_statements', 0)
                    }

                return {
                    'total_coverage': total_coverage,
                    'files': files_coverage
                }
        except Exception as e:
            logger.warning(f"Failed to parse coverage results: {e}")

        return {'total_coverage': 0.0, 'files': {}}

    def validate_business_logic_preservation(self) -> Dict[str, Any]:
        """Validate 100% business logic preservation requirement"""
        validation_results = {
            'overall_preservation': True,
            'critical_algorithms_preserved': True,
            'api_compatibility_maintained': True,
            'performance_requirements_met': True,
            'validation_details': {}
        }

        # Check threat intelligence core preservation
        if 'threat_intelligence_core' in self.results:
            core_result = self.results['threat_intelligence_core']
            if not core_result['success'] or core_result['failed'] > 0:
                validation_results['critical_algorithms_preserved'] = False
                validation_results['overall_preservation'] = False
                validation_results['validation_details']['core_algorithms'] = (
                    "Critical threat intelligence algorithms failed validation"
                )

        # Check API compatibility preservation
        if 'api_integration' in self.results:
            api_result = self.results['api_integration']
            if not api_result['success'] or api_result['failed'] > 0:
                validation_results['api_compatibility_maintained'] = False
                validation_results['overall_preservation'] = False
                validation_results['validation_details']['api_compatibility'] = (
                    "API compatibility validation failed"
                )

        # Check performance requirements
        if 'performance_benchmarks' in self.results:
            perf_result = self.results['performance_benchmarks']
            if not perf_result['success'] or perf_result['failed'] > 0:
                validation_results['performance_requirements_met'] = False
                validation_results['overall_preservation'] = False
                validation_results['validation_details']['performance'] = (
                    "Performance requirements not met"
                )

        return validation_results

    def generate_final_report(self, total_execution_time: float) -> Dict[str, Any]:
        """Generate comprehensive test execution report"""
        total_tests = sum(result.get('test_count', 0)
                          for result in self.results.values())
        total_passed = sum(result.get('passed', 0)
                           for result in self.results.values())
        total_failed = sum(result.get('failed', 0)
                           for result in self.results.values())
        total_skipped = sum(result.get('skipped', 0)
                            for result in self.results.values())

        # Calculate overall coverage
        coverage_weights = {'threat_intelligence_core': 0.5,
                            'api_integration': 0.3, 'performance_benchmarks': 0.2}
        weighted_coverage = sum(
            self.results.get(suite, {}).get('coverage', 0.0) * weight
            for suite, weight in coverage_weights.items()
        )

        return {
            'execution_summary': {
                'overall_success': self.overall_success,
                'total_execution_time': total_execution_time,
                'total_tests': total_tests,
                'total_passed': total_passed,
                'total_failed': total_failed,
                'total_skipped': total_skipped,
                'success_rate': (total_passed / total_tests * 100) if total_tests > 0 else 0.0,
                'overall_coverage': weighted_coverage
            },
            'suite_results': self.results,
            'validation_status': {
                'meets_80_percent_coverage': weighted_coverage >= 80.0,
                'all_critical_tests_passed': total_failed == 0,
                'performance_requirements_met': self.results.get('performance_benchmarks', {}).get('success', False),
                'ready_for_migration': self.overall_success and weighted_coverage >= 80.0
            },
            'recommendations': self.generate_recommendations()
        }

    def generate_recommendations(self) -> List[str]:
        """Generate actionable recommendations based on test results"""
        recommendations = []

        # Coverage recommendations
        for suite_name, result in self.results.items():
            if result.get('coverage', 0.0) < TEST_SUITES[suite_name]['required_coverage']:
                recommendations.append(
                    f"Increase test coverage for {suite_name} "
                    f"(current: {result.get('coverage', 0.0):.1f}%, "
                    f"required: {TEST_SUITES[suite_name]['required_coverage']}%)"
                )

        # Performance recommendations
        if 'performance_benchmarks' in self.results:
            perf_result = self.results['performance_benchmarks']
            if not perf_result['success']:
                recommendations.append(
                    "Review performance bottlenecks and optimize critical algorithms"
                )

        # Overall recommendations
        if not self.overall_success:
            recommendations.append(
                "Address failing tests before proceeding with MISP migration"
            )

        if not recommendations:
            recommendations.append(
                "All tests passed! MISP integration ready for production migration."
            )

        return recommendations

    def save_report(self, report: Dict[str, Any], output_file: str):
        """Save comprehensive report to file"""
        try:
            with open(output_file, 'w') as f:
                json.dump(report, f, indent=2, default=str)
            logger.info(f"Test report saved to {output_file}")
        except Exception as e:
            logger.error(f"Failed to save report: {e}")

    def print_summary(self, report: Dict[str, Any]):
        """Print test execution summary to console"""
        summary = report['execution_summary']
        validation = report['validation_status']

        print("\n" + "="*80)
        print("MISP COMPREHENSIVE TEST EXECUTION SUMMARY")
        print("="*80)

        print(
            f"Overall Success: {'✅ PASS' if summary['overall_success'] else '❌ FAIL'}")
        print(f"Total Tests: {summary['total_tests']}")
        print(
            f"Passed: {summary['total_passed']} | Failed: {summary['total_failed']} | Skipped: {summary['total_skipped']}")
        print(f"Success Rate: {summary['success_rate']:.1f}%")
        print(f"Overall Coverage: {summary['overall_coverage']:.1f}%")
        print(f"Execution Time: {summary['total_execution_time']:.1f}s")

        print("\nValidation Status:")
        print(
            f"  80%+ Coverage: {'✅' if validation['meets_80_percent_coverage'] else '❌'}")
        print(
            f"  All Critical Tests: {'✅' if validation['all_critical_tests_passed'] else '❌'}")
        print(
            f"  Performance Requirements: {'✅' if validation['performance_requirements_met'] else '❌'}")
        print(
            f"  Ready for Migration: {'✅' if validation['ready_for_migration'] else '❌'}")

        print("\nRecommendations:")
        for rec in report['recommendations']:
            print(f"  • {rec}")

        print("="*80)


def main():
    """Main execution function"""
    # Setup test directory
    test_dir = "/workspaces/modular-monolith-2/tests/security/MISP"

    # Initialize executor
    executor = MISPTestExecutor(test_dir)

    try:
        # Run comprehensive test suite
        report = executor.run_all_tests()

        # Save report
        report_file = f"{test_dir}/misp_test_report_{int(time.time())}.json"
        executor.save_report(report, report_file)

        # Print summary
        executor.print_summary(report)

        # Exit with appropriate code
        exit_code = 0 if report['execution_summary']['overall_success'] else 1
        sys.exit(exit_code)

    except Exception as e:
        logger.error(f"Test execution failed: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
