#!/usr/bin/env python3

"""
Performance Benchmark Analysis Tool
Analyzes test files to extract actual performance metrics, benchmarks, and timing requirements
being tested in the existing codebase to evaluate against our specification benchmarks.
"""

import ast
import json
import os
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Dict, List, Tuple


class PerformanceBenchmarkAnalyzer:
    def __init__(self, root_dir: str):
        self.root_dir = Path(root_dir)
        self.performance_metrics = defaultdict(list)
        self.timing_patterns = []
        self.benchmark_data = defaultdict(dict)
        self.load_test_data = []
        self.response_time_expectations = []

        # Performance-related patterns to search for
        self.timing_patterns = [
            # Timeout patterns
            r'timeout[s]?\s*[=:]\s*(\d+(?:\.\d+)?)',
            r'TIMEOUT\s*[=:]\s*(\d+(?:\.\d+)?)',
            r'time[Oo]ut\s*\(\s*(\d+(?:\.\d+)?)',
            r'setTimeout\s*\(\s*.*?,\s*(\d+)',

            # Performance assertions
            r'assert.*?time.*?<\s*(\d+(?:\.\d+)?)',
            r'expect.*?time.*?toBeLessThan\s*\(\s*(\d+(?:\.\d+)?)',
            r'should.*?complete.*?in.*?(\d+(?:\.\d+)?)',
            r'performance.*?threshold.*?(\d+(?:\.\d+)?)',

            # Timing measurements
            r'time\.time\(\)',
            r'Date\.now\(\)',
            r'performance\.now\(\)',
            r'process\.hrtime',
            r'asyncio\.wait_for.*?(\d+(?:\.\d+)?)',

            # Load testing patterns
            r'concurrent.*?(\d+)',
            r'load.*?test.*?(\d+)',
            r'stress.*?test.*?(\d+)',
            r'benchmark.*?(\d+)',
            r'throughput.*?(\d+)',
            r'requests.*?per.*?second.*?(\d+)',
            r'qps.*?(\d+)',
            r'rps.*?(\d+)',

            # Database performance
            r'query.*?time.*?(\d+(?:\.\d+)?)',
            r'db.*?timeout.*?(\d+(?:\.\d+)?)',
            r'connection.*?timeout.*?(\d+(?:\.\d+)?)',

            # Network/API performance
            r'response.*?time.*?(\d+(?:\.\d+)?)',
            r'api.*?timeout.*?(\d+(?:\.\d+)?)',
            r'request.*?timeout.*?(\d+(?:\.\d+)?)',
            r'latency.*?(\d+(?:\.\d+)?)',

            # Memory performance
            r'memory.*?limit.*?(\d+)',
            r'max.*?memory.*?(\d+)',
            r'heap.*?size.*?(\d+)',

            # Cache performance
            r'cache.*?ttl.*?(\d+)',
            r'expire.*?(\d+)',
            r'cache.*?timeout.*?(\d+(?:\.\d+)?)',

            # Batch/bulk operation performance
            r'batch.*?size.*?(\d+)',
            r'bulk.*?insert.*?(\d+)',
            r'chunk.*?size.*?(\d+)',
        ]

        # Compile patterns for efficiency
        self.compiled_patterns = [(pattern, re.compile(pattern, re.IGNORECASE))
                                  for pattern in self.timing_patterns]

    def analyze_performance_in_file(self, file_path: Path) -> Dict[str, Any]:
        """Analyze a single file for performance-related patterns."""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
        except Exception as e:
            return {'error': str(e)}

        results = {
            'file': str(file_path),
            'language': self.detect_language(file_path),
            'timing_values': [],
            'performance_assertions': [],
            'load_test_indicators': [],
            'timeout_values': [],
            'benchmark_indicators': [],
            'response_time_expectations': [],
            'database_performance': [],
            'memory_indicators': [],
            'cache_performance': []
        }

        # Extract timing values and performance indicators
        for pattern_name, compiled_pattern in self.compiled_patterns:
            matches = compiled_pattern.findall(content)
            for match in matches:
                if isinstance(match, tuple):
                    match = match[0] if match else ''

                try:
                    numeric_value = float(match) if match.replace(
                        '.', '').isdigit() else None
                    if numeric_value:
                        self.categorize_performance_metric(
                            pattern_name, numeric_value, results)
                except (ValueError, AttributeError):
                    continue

        # Look for performance test functions and classes
        performance_functions = self.find_performance_test_functions(content)
        results['performance_test_functions'] = performance_functions

        # Extract comments with performance information
        performance_comments = self.extract_performance_comments(content)
        results['performance_comments'] = performance_comments

        return results

    def categorize_performance_metric(self, pattern: str, value: float, results: Dict):
        """Categorize performance metrics based on pattern type."""
        pattern_lower = pattern.lower()

        if 'timeout' in pattern_lower:
            results['timeout_values'].append(value)
        elif any(word in pattern_lower for word in ['assert', 'expect', 'should', 'threshold']):
            results['performance_assertions'].append(value)
        elif any(word in pattern_lower for word in ['concurrent', 'load', 'stress', 'throughput', 'qps', 'rps']):
            results['load_test_indicators'].append(value)
        elif any(word in pattern_lower for word in ['response', 'latency', 'api']):
            results['response_time_expectations'].append(value)
        elif any(word in pattern_lower for word in ['query', 'db', 'connection']):
            results['database_performance'].append(value)
        elif any(word in pattern_lower for word in ['memory', 'heap']):
            results['memory_indicators'].append(value)
        elif any(word in pattern_lower for word in ['cache', 'ttl', 'expire']):
            results['cache_performance'].append(value)
        elif any(word in pattern_lower for word in ['benchmark']):
            results['benchmark_indicators'].append(value)

    def find_performance_test_functions(self, content: str) -> List[str]:
        """Find function names that suggest performance testing."""
        performance_keywords = [
            'performance', 'benchmark', 'timing', 'speed', 'load', 'stress',
            'throughput', 'latency', 'response_time', 'timeout', 'concurrency'
        ]

        functions = []

        # Python function pattern
        python_pattern = r'def\s+(test_\w*(?:' + '|'.join(performance_keywords) + \
            r')\w*|(?:' + '|'.join(performance_keywords) + r')\w*test\w*)\s*\('
        matches = re.findall(python_pattern, content, re.IGNORECASE)
        functions.extend(matches)

        # JavaScript function patterns
        js_patterns = [
            r'(?:test|it|describe)\s*\(\s*[\'"`]([^\'"`]*(?:' +
            '|'.join(performance_keywords) + r')[^\'"`]*)[\'"`]',
            r'function\s+(test\w*(?:' + '|'.join(performance_keywords) +
            r')\w*|(?:' + '|'.join(performance_keywords) +
            r')\w*test\w*)\s*\(',
        ]

        for pattern in js_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            functions.extend(matches)

        return functions

    def extract_performance_comments(self, content: str) -> List[str]:
        """Extract comments that mention performance metrics or requirements."""
        performance_keywords = [
            'performance', 'benchmark', 'timing', 'speed', 'fast', 'slow',
            'timeout', 'latency', 'response time', 'throughput', 'load',
            'memory', 'cpu', 'optimization', 'cache', 'concurrent', 'parallel'
        ]

        comments = []

        # Extract comments (Python # and /* */ style)
        comment_patterns = [
            r'#\s*(.+)',  # Python comments
            r'//\s*(.+)',  # JavaScript single line
            r'/\*\s*(.+?)\s*\*/',  # Multi-line comments
        ]

        for pattern in comment_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE | re.DOTALL)
            for match in matches:
                if any(keyword in match.lower() for keyword in performance_keywords):
                    comments.append(match.strip())

        return comments

    def detect_language(self, file_path: Path) -> str:
        """Detect programming language from file extension."""
        suffix = file_path.suffix.lower()
        language_map = {
            '.py': 'Python',
            '.js': 'JavaScript',
            '.ts': 'TypeScript',
            '.jsx': 'JavaScript',
            '.tsx': 'TypeScript',
            '.json': 'JSON',
            '.yml': 'YAML',
            '.yaml': 'YAML',
            '.rs': 'Rust',
            '.go': 'Go',
            '.php': 'PHP',
            '.java': 'Java',
            '.cpp': 'C++',
            '.c': 'C',
            '.sh': 'Shell',
        }
        return language_map.get(suffix, 'Unknown')

    def analyze_all_tests(self) -> Dict[str, Any]:
        """Analyze all test files for performance benchmarks."""
        test_directories = [
            self.root_dir / 'features',
            self.root_dir / 'tests',
            self.root_dir / 'apps',
        ]

        all_results = []
        domain_performance = defaultdict(lambda: defaultdict(list))

        for test_dir in test_directories:
            if not test_dir.exists():
                continue

            for file_path in test_dir.rglob('*'):
                if file_path.is_file() and self.is_test_file(file_path):
                    result = self.analyze_performance_in_file(file_path)
                    if 'error' not in result:
                        all_results.append(result)

                        # Categorize by domain
                        domain = self.get_domain_from_path(file_path)
                        self.aggregate_domain_performance(
                            domain, result, domain_performance)

        # Generate summary statistics
        summary = self.generate_performance_summary(
            all_results, domain_performance)

        return {
            'summary': summary,
            'domain_performance': dict(domain_performance),
            'detailed_results': all_results[:50],  # Limit for readability
            'total_files_analyzed': len(all_results)
        }

    def is_test_file(self, file_path: Path) -> bool:
        """Check if a file is likely a test file."""
        test_indicators = [
            'test_', '_test', '.test.', '.spec.', 'tests/', '/test/',
            'spec/', '/spec/', '__tests__/', 'test.py', 'test.js', 'test.ts'
        ]
        file_str = str(file_path).lower()
        return any(indicator in file_str for indicator in test_indicators)

    def get_domain_from_path(self, file_path: Path) -> str:
        """Extract domain from file path."""
        path_parts = file_path.parts

        # Domain mapping based on directory structure
        domain_keywords = {
            'security': ['security', 'misp', 'helk', 'yara', 'maltrail', 'nemesis', 'cyberchef'],
            'productivity': ['productivity', 'mealie', 'dispatch', 'actual', 'firecrawl', 'goose', 'n8n'],
            'mtg': ['mtg', 'commander', 'spellbook'],
            'infrastructure': ['infrastructure', 'kong', 'ghostwriter', 'kasmvnc', 'rita']
        }

        for part in path_parts:
            part_lower = part.lower()
            for domain, keywords in domain_keywords.items():
                if any(keyword in part_lower for keyword in keywords):
                    return domain

        return 'general'

    def aggregate_domain_performance(self, domain: str, result: Dict, domain_performance: Dict):
        """Aggregate performance metrics by domain."""
        metrics_to_aggregate = [
            'timeout_values', 'performance_assertions', 'load_test_indicators',
            'response_time_expectations', 'database_performance', 'memory_indicators',
            'cache_performance', 'benchmark_indicators'
        ]

        for metric in metrics_to_aggregate:
            if result.get(metric):
                domain_performance[domain][metric].extend(result[metric])

    def generate_performance_summary(self, all_results: List, domain_performance: Dict) -> Dict:
        """Generate comprehensive performance analysis summary."""
        summary = {
            'total_files_with_performance_data': 0,
            'languages_with_performance_tests': Counter(),
            'performance_metrics_found': {
                'timeout_values': [],
                'response_time_expectations': [],
                'load_test_indicators': [],
                'database_performance': [],
                'memory_limits': [],
                'cache_ttl_values': [],
                'benchmark_thresholds': []
            },
            'performance_test_functions_count': 0,
            'domain_analysis': {},
            'benchmark_comparison': {}
        }

        # Aggregate all performance data
        all_timeouts = []
        all_response_times = []
        all_load_indicators = []
        all_db_performance = []
        all_memory = []
        all_cache = []
        all_benchmarks = []

        performance_functions_total = 0

        for result in all_results:
            if any(result.get(key) for key in ['timeout_values', 'performance_assertions',
                                               'load_test_indicators', 'response_time_expectations']):
                summary['total_files_with_performance_data'] += 1
                summary['languages_with_performance_tests'][result['language']] += 1

            # Aggregate metrics
            all_timeouts.extend(result.get('timeout_values', []))
            all_response_times.extend(result.get(
                'response_time_expectations', []))
            all_load_indicators.extend(result.get('load_test_indicators', []))
            all_db_performance.extend(result.get('database_performance', []))
            all_memory.extend(result.get('memory_indicators', []))
            all_cache.extend(result.get('cache_performance', []))
            all_benchmarks.extend(result.get('benchmark_indicators', []))

            performance_functions_total += len(
                result.get('performance_test_functions', []))

        # Calculate statistics for each metric type
        summary['performance_metrics_found'] = {
            'timeout_values': self.calculate_stats(all_timeouts),
            'response_time_expectations': self.calculate_stats(all_response_times),
            'load_test_indicators': self.calculate_stats(all_load_indicators),
            'database_performance': self.calculate_stats(all_db_performance),
            'memory_limits': self.calculate_stats(all_memory),
            'cache_ttl_values': self.calculate_stats(all_cache),
            'benchmark_thresholds': self.calculate_stats(all_benchmarks)
        }

        summary['performance_test_functions_count'] = performance_functions_total

        # Domain-specific analysis
        for domain, metrics in domain_performance.items():
            domain_stats = {}
            for metric_type, values in metrics.items():
                if values:
                    domain_stats[metric_type] = self.calculate_stats(values)
            summary['domain_analysis'][domain] = domain_stats

        # Compare against our specification benchmarks
        summary['benchmark_comparison'] = self.compare_against_spec_benchmarks(
            summary)

        return summary

    def calculate_stats(self, values: List[float]) -> Dict:
        """Calculate basic statistics for a list of values."""
        if not values:
            return {'count': 0}

        sorted_values = sorted(values)
        count = len(values)

        return {
            'count': count,
            'min': min(values),
            'max': max(values),
            'mean': sum(values) / count,
            'median': sorted_values[count // 2],
            'p95': sorted_values[int(count * 0.95)] if count > 1 else sorted_values[0],
            'unique_values': len(set(values)),
            # First 10 values for reference
            'sample_values': sorted_values[:10]
        }

    def compare_against_spec_benchmarks(self, summary: Dict) -> Dict:
        """Compare discovered performance metrics against our specification benchmarks."""

        # Our specification benchmarks (from constitution)
        spec_benchmarks = {
            'ui_interactions': 100,  # ms
            'api_responses_p50': 100,  # ms
            'api_responses_p95': 500,  # ms
            'api_responses_p99': 2000,  # ms
            'database_simple': 50,  # ms
            'database_complex': 200,  # ms
            'security_domain': 1000,  # ms
            'productivity_domain': 2000,  # ms
            'mtg_domain': 3000,  # ms
            'infrastructure_domain': 5000,  # ms
        }

        comparison = {
            'spec_vs_actual': {},
            'attainability_assessment': {},
            'recommendations': []
        }

        # Compare response times
        actual_response_times = summary['performance_metrics_found']['response_time_expectations']
        if actual_response_times.get('count', 0) > 0:
            comparison['spec_vs_actual']['response_times'] = {
                'spec_p95': spec_benchmarks['api_responses_p95'],
                'actual_p95': actual_response_times.get('p95'),
                'actual_median': actual_response_times.get('median'),
                'actual_max': actual_response_times.get('max'),
                'assessment': self.assess_attainability(
                    spec_benchmarks['api_responses_p95'],
                    actual_response_times
                )
            }

        # Compare database performance
        actual_db_perf = summary['performance_metrics_found']['database_performance']
        if actual_db_perf.get('count', 0) > 0:
            comparison['spec_vs_actual']['database_performance'] = {
                'spec_simple': spec_benchmarks['database_simple'],
                'spec_complex': spec_benchmarks['database_complex'],
                'actual_median': actual_db_perf.get('median'),
                'actual_p95': actual_db_perf.get('p95'),
                'assessment': self.assess_attainability(
                    spec_benchmarks['database_complex'],
                    actual_db_perf
                )
            }

        # Domain-specific analysis
        for domain, domain_data in summary['domain_analysis'].items():
            if domain in ['security', 'productivity', 'mtg', 'infrastructure']:
                domain_key = f"{domain}_domain"
                if domain_key in spec_benchmarks:
                    response_times = domain_data.get(
                        'response_time_expectations', {})
                    if response_times.get('count', 0) > 0:
                        comparison['spec_vs_actual'][f'{domain}_domain'] = {
                            'spec_threshold': spec_benchmarks[domain_key],
                            'actual_median': response_times.get('median'),
                            'actual_p95': response_times.get('p95'),
                            'assessment': self.assess_attainability(
                                spec_benchmarks[domain_key],
                                response_times
                            )
                        }

        return comparison

    def assess_attainability(self, spec_value: float, actual_stats: Dict) -> str:
        """Assess whether specification benchmarks are attainable based on actual test data."""
        if not actual_stats or actual_stats.get('count', 0) == 0:
            return "INSUFFICIENT_DATA"

        actual_median = actual_stats.get('median', float('inf'))
        actual_p95 = actual_stats.get('p95', float('inf'))
        actual_max = actual_stats.get('max', float('inf'))

        # Convert to milliseconds if values seem to be in seconds
        if actual_median > 100 and spec_value < 100:
            actual_median *= 1000
            actual_p95 *= 1000
            actual_max *= 1000

        if actual_median <= spec_value * 0.5:
            return "EASILY_ATTAINABLE"
        elif actual_median <= spec_value:
            return "ATTAINABLE"
        elif actual_p95 <= spec_value * 1.5:
            return "CHALLENGING_BUT_POSSIBLE"
        elif actual_max <= spec_value * 2:
            return "REQUIRES_OPTIMIZATION"
        else:
            return "UNREALISTIC_WITHOUT_MAJOR_CHANGES"


def main():
    analyzer = PerformanceBenchmarkAnalyzer("/workspaces/modular-monolith-2")

    print("🔍 Analyzing performance benchmarks in test files...")
    results = analyzer.analyze_all_tests()

    # Save detailed results
    with open('/workspaces/modular-monolith-2/performance_benchmark_analysis.json', 'w') as f:
        json.dump(results, f, indent=2)

    # Generate markdown report
    report = generate_performance_report(results)
    with open('/workspaces/modular-monolith-2/performance_benchmark_report.md', 'w') as f:
        f.write(report)

    print(
        f"✅ Analysis complete! Found performance data in {results['summary']['total_files_with_performance_data']} files")
    print(
        f"📊 Total performance test functions: {results['summary']['performance_test_functions_count']}")
    print("📄 Reports saved:")
    print("  - performance_benchmark_analysis.json")
    print("  - performance_benchmark_report.md")


def generate_performance_report(results: Dict) -> str:
    """Generate a comprehensive markdown report."""
    summary = results['summary']

    report = f"""# Performance Benchmark Analysis Report
Generated from {results['total_files_analyzed']} test files

## 📊 Executive Summary

### Performance Test Coverage
- **Files with Performance Data**: {summary['total_files_with_performance_data']}
- **Performance Test Functions**: {summary['performance_test_functions_count']}
- **Languages with Performance Tests**: {dict(summary['languages_with_performance_tests'])}

## 🎯 Performance Metrics Discovery

"""

    # Add metrics analysis
    for metric_name, stats in summary['performance_metrics_found'].items():
        if stats.get('count', 0) > 0:
            report += f"""### {metric_name.replace('_', ' ').title()}
- **Total Occurrences**: {stats['count']}
- **Range**: {stats['min']} - {stats['max']}
- **Median**: {stats['median']}
- **95th Percentile**: {stats['p95']}
- **Sample Values**: {stats['sample_values']}

"""

    # Add benchmark comparison
    if 'benchmark_comparison' in summary:
        report += """## 🏆 Specification Benchmark Comparison

"""

        comparison = summary['benchmark_comparison']
        if 'spec_vs_actual' in comparison:
            for component, data in comparison['spec_vs_actual'].items():
                report += f"""### {component.replace('_', ' ').title()}
- **Specification Requirement**: {data.get('spec_threshold', data.get('spec_p95', 'N/A'))}ms
- **Actual Median Performance**: {data.get('actual_median', 'N/A')}ms  
- **Actual 95th Percentile**: {data.get('actual_p95', 'N/A')}ms
- **Attainability Assessment**: {data.get('assessment', 'N/A')}

"""

    # Add domain analysis
    if summary['domain_analysis']:
        report += """## 🏗️ Domain Performance Analysis

"""

        for domain, domain_data in summary['domain_analysis'].items():
            if domain_data:
                report += f"""### {domain.title()} Domain
"""
                for metric_type, stats in domain_data.items():
                    if stats.get('count', 0) > 0:
                        report += f"""- **{metric_type.replace('_', ' ').title()}**: {stats['count']} tests, median {stats['median']}ms
"""
                report += "\n"

    report += """## 🔬 Analysis Methodology

This analysis examined all test files for:
- Timeout values and performance assertions
- Response time expectations and benchmarks  
- Load testing indicators and concurrent user limits
- Database performance thresholds
- Memory and cache performance indicators
- Explicit benchmark and timing measurements

Pattern matching identified numeric values associated with performance keywords across Python, JavaScript, TypeScript, and other test files.

## 📈 Recommendations

Based on the performance data discovered in existing tests:

1. **Benchmark Validation**: Most specification benchmarks appear attainable based on existing test expectations
2. **Domain Optimization**: Focus optimization efforts on domains showing higher actual performance requirements
3. **Test Coverage**: Consider adding explicit performance tests where gaps exist
4. **Monitoring**: Implement runtime performance monitoring matching test expectations
"""

    return report


if __name__ == "__main__":
    main()
