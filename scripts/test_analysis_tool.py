#!/usr/bin/env python3
"""
Comprehensive Test Analysis Tool for 3,795+ Test Files
Analyzes test patterns, business logic, and exotic testing scenarios
"""

import ast
import json
import os
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path


class TestAnalyzer:
    def __init__(self, test_dir="/workspaces/modular-monolith-2/tests"):
        self.test_dir = Path(test_dir)
        self.results = {
            "frameworks": Counter(),
            "test_patterns": Counter(),
            "business_logic_patterns": Counter(),
            "exotic_patterns": Counter(),
            "domains": defaultdict(lambda: {"files": 0, "tests": 0, "patterns": Counter()}),
            "file_stats": {
                "total_files": 0,
                "total_test_functions": 0,
                "by_language": Counter(),
                "by_framework": Counter()
            },
            "critical_patterns": [],
            "complex_scenarios": []
        }

    def analyze_python_test(self, file_path):
        """Analyze Python test files for patterns and business logic"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

            # Parse AST for detailed analysis
            try:
                tree = ast.parse(content)
                return self._analyze_python_ast(tree, file_path, content)
            except SyntaxError:
                # Fall back to regex analysis for problematic files
                return self._analyze_python_regex(content, file_path)

        except Exception as e:
            return {"error": str(e), "file": str(file_path)}

    def _analyze_python_ast(self, tree, file_path, content):
        """Detailed AST analysis of Python test files"""
        analysis = {
            "framework": None,
            "test_functions": [],
            "imports": [],
            "assertions": [],
            "business_logic": [],
            "exotic_patterns": []
        }

        # Extract imports
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    analysis["imports"].append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    analysis["imports"].append(node.module)

        # Identify framework
        if any("pytest" in imp for imp in analysis["imports"]):
            analysis["framework"] = "pytest"
        elif any("unittest" in imp for imp in analysis["imports"]):
            analysis["framework"] = "unittest"
        elif any("django.test" in imp for imp in analysis["imports"]):
            analysis["framework"] = "django"

        # Extract test functions and analyze patterns
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name.startswith('test_'):
                test_info = {
                    "name": node.name,
                    "line": node.lineno,
                    "business_logic": self._extract_business_logic_from_name(node.name),
                    "complexity": self._estimate_complexity(node)
                }
                analysis["test_functions"].append(test_info)

                # Look for exotic patterns
                exotic = self._detect_exotic_patterns(node, content)
                if exotic:
                    analysis["exotic_patterns"].extend(exotic)

        return analysis

    def _analyze_python_regex(self, content, file_path):
        """Regex-based analysis for files that can't be parsed"""
        analysis = {
            "framework": None,
            "test_functions": [],
            "business_logic": [],
            "exotic_patterns": []
        }

        # Framework detection
        if re.search(r'import pytest|from pytest', content):
            analysis["framework"] = "pytest"
        elif re.search(r'import unittest|from unittest', content):
            analysis["framework"] = "unittest"
        elif re.search(r'from django\.test', content):
            analysis["framework"] = "django"

        # Extract test function names
        test_functions = re.findall(r'def (test_\w+)', content)
        for func_name in test_functions:
            analysis["test_functions"].append({
                "name": func_name,
                "business_logic": self._extract_business_logic_from_name(func_name)
            })

        # Look for exotic patterns using regex
        exotic_patterns = []

        # API testing patterns
        if re.search(r'TestClient|api_client|requests\.(get|post|put|delete)', content):
            exotic_patterns.append("api_testing")

        # Database testing
        if re.search(r'@pytest\.mark\.django_db|TransactionTestCase|rollback', content):
            exotic_patterns.append("database_transactions")

        # Async testing
        if re.search(r'async def test_|@pytest\.mark\.asyncio|await ', content):
            exotic_patterns.append("async_testing")

        # Mock/patch patterns
        if re.search(r'@patch|@mock|Mock\(|MagicMock', content):
            exotic_patterns.append("mocking_framework")

        # Performance testing
        if re.search(r'@pytest\.mark\.performance|benchmark|time\.time|timeit', content):
            exotic_patterns.append("performance_testing")

        analysis["exotic_patterns"] = exotic_patterns
        return analysis

    def analyze_javascript_test(self, file_path):
        """Analyze JavaScript/TypeScript test files"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

            analysis = {
                "framework": None,
                "test_functions": [],
                "business_logic": [],
                "exotic_patterns": []
            }

            # Framework detection
            if re.search(r'from ["\']vitest["\']|import.*vitest', content):
                analysis["framework"] = "vitest"
            elif re.search(r'describe\(|it\(|test\(', content):
                if 'jest' in content.lower():
                    analysis["framework"] = "jest"
                else:
                    analysis["framework"] = "mocha/jasmine"

            # Extract test cases
            test_patterns = re.findall(
                r'(?:test|it)\s*\(\s*["\']([^"\']+)["\']', content)
            describe_patterns = re.findall(
                r'describe\s*\(\s*["\']([^"\']+)["\']', content)

            for test_name in test_patterns:
                analysis["test_functions"].append({
                    "name": test_name,
                    "type": "test",
                    "business_logic": self._extract_business_logic_from_description(test_name)
                })

            for desc_name in describe_patterns:
                analysis["test_functions"].append({
                    "name": desc_name,
                    "type": "describe",
                    "business_logic": self._extract_business_logic_from_description(desc_name)
                })

            # Exotic patterns for JS/TS
            exotic_patterns = []
            if re.search(r'async.*expect|await.*expect', content):
                exotic_patterns.append("async_testing")
            if re.search(r'mock|jest\.fn|vi\.fn|sinon', content):
                exotic_patterns.append("mocking_framework")
            if re.search(r'render\(|screen\.|fireEvent', content):
                exotic_patterns.append("ui_testing")
            if re.search(r'cy\.|browser\.|page\.', content):
                exotic_patterns.append("e2e_testing")

            analysis["exotic_patterns"] = exotic_patterns
            return analysis

        except Exception as e:
            return {"error": str(e), "file": str(file_path)}

    def _extract_business_logic_from_name(self, test_name):
        """Extract business logic concepts from test function names"""
        business_concepts = []

        # Common business logic patterns
        patterns = {
            "authentication": r"auth|login|logout|token|credential|password",
            "authorization": r"permission|role|access|admin|user|group",
            "data_validation": r"valid|invalid|format|schema|constraint",
            "crud_operations": r"create|read|update|delete|insert|select|modify",
            "api_operations": r"get|post|put|delete|patch|endpoint|route",
            "business_rules": r"rule|policy|workflow|process|business",
            "integration": r"sync|integrate|connect|external|third_party",
            "performance": r"performance|speed|load|stress|benchmark",
            "security": r"security|encrypt|decrypt|hash|secure|vulnerability",
            "error_handling": r"error|exception|fail|timeout|retry"
        }

        test_name_lower = test_name.lower()
        for concept, pattern in patterns.items():
            if re.search(pattern, test_name_lower):
                business_concepts.append(concept)

        return business_concepts

    def _extract_business_logic_from_description(self, description):
        """Extract business logic from test descriptions"""
        return self._extract_business_logic_from_name(description)

    def _estimate_complexity(self, node):
        """Estimate test complexity based on AST structure"""
        complexity = 0
        for child in ast.walk(node):
            if isinstance(child, (ast.If, ast.For, ast.While, ast.Try)):
                complexity += 1
            elif isinstance(child, ast.FunctionDef) and child != node:
                complexity += 2  # Nested functions are complex
        return complexity

    def _detect_exotic_patterns(self, node, content):
        """Detect exotic testing patterns in AST"""
        patterns = []

        # Look for specific exotic patterns in the function
        func_text = content.split('\n')[node.lineno-1:node.end_lineno]
        func_content = '\n'.join(func_text)

        if re.search(r'@pytest\.mark\.(parametrize|fixture)', func_content):
            patterns.append("parametrized_testing")
        if re.search(r'monkeypatch|mock|patch', func_content):
            patterns.append("monkey_patching")
        if re.search(r'async|await', func_content):
            patterns.append("async_testing")
        if re.search(r'subprocess|multiprocessing', func_content):
            patterns.append("process_testing")

        return patterns

    def analyze_all_tests(self):
        """Analyze all test files in the directory"""
        print("🔍 Analyzing 3,795+ test files...")

        for root, dirs, files in os.walk(self.test_dir):
            for file in files:
                file_path = Path(root) / file

                # Determine domain from path
                rel_path = file_path.relative_to(self.test_dir)
                domain = str(rel_path).split(
                    '/')[0] if '/' in str(rel_path) else 'root'

                self.results["file_stats"]["total_files"] += 1
                self.results["domains"][domain]["files"] += 1

                # Analyze based on file extension
                if file.endswith('.py'):
                    self.results["file_stats"]["by_language"]["Python"] += 1
                    analysis = self.analyze_python_test(file_path)
                elif file.endswith(('.js', '.ts')):
                    self.results["file_stats"]["by_language"]["JavaScript/TypeScript"] += 1
                    analysis = self.analyze_javascript_test(file_path)
                else:
                    continue

                if "error" not in analysis:
                    self._process_analysis_results(analysis, domain)

        self._generate_insights()
        return self.results

    def _process_analysis_results(self, analysis, domain):
        """Process analysis results and update counters"""
        if analysis.get("framework"):
            self.results["frameworks"][analysis["framework"]] += 1
            self.results["file_stats"]["by_framework"][analysis["framework"]] += 1

        # Count test functions
        test_count = len(analysis.get("test_functions", []))
        self.results["file_stats"]["total_test_functions"] += test_count
        self.results["domains"][domain]["tests"] += test_count

        # Process business logic patterns
        for test_func in analysis.get("test_functions", []):
            for logic in test_func.get("business_logic", []):
                self.results["business_logic_patterns"][logic] += 1
                self.results["domains"][domain]["patterns"][logic] += 1

        # Process exotic patterns
        for pattern in analysis.get("exotic_patterns", []):
            self.results["exotic_patterns"][pattern] += 1

    def _generate_insights(self):
        """Generate insights about testing patterns"""
        # Identify most critical patterns
        critical_threshold = 50  # Patterns appearing in 50+ tests
        for pattern, count in self.results["business_logic_patterns"].items():
            if count >= critical_threshold:
                self.results["critical_patterns"].append({
                    "pattern": pattern,
                    "count": count,
                    "criticality": "HIGH" if count > 100 else "MEDIUM"
                })

        # Identify complex scenarios
        exotic_threshold = 10
        for pattern, count in self.results["exotic_patterns"].items():
            if count >= exotic_threshold:
                self.results["complex_scenarios"].append({
                    "pattern": pattern,
                    "count": count,
                    "complexity": "HIGH" if count > 30 else "MEDIUM"
                })

    def generate_report(self):
        """Generate comprehensive analysis report"""
        report = []
        report.append("# Test Analysis Report: 3,795+ Test Files")
        report.append("=" * 50)

        # File statistics
        stats = self.results["file_stats"]
        report.append(f"\n## 📊 File Statistics")
        report.append(f"- **Total Test Files**: {stats['total_files']:,}")
        report.append(
            f"- **Total Test Functions**: {stats['total_test_functions']:,}")
        report.append(f"- **Languages**: {dict(stats['by_language'])}")
        report.append(f"- **Frameworks**: {dict(stats['by_framework'])}")

        # Domain breakdown
        report.append(f"\n## 🏗️ Domain Analysis")
        for domain, data in sorted(self.results["domains"].items(), key=lambda x: x[1]["tests"], reverse=True):
            if data["tests"] > 0:
                report.append(
                    f"- **{domain.title()}**: {data['files']} files, {data['tests']} tests")

        # Critical business logic patterns
        report.append(f"\n## 🎯 Critical Business Logic Patterns")
        for pattern_info in sorted(self.results["critical_patterns"], key=lambda x: x["count"], reverse=True):
            report.append(
                f"- **{pattern_info['pattern'].replace('_', ' ').title()}**: {pattern_info['count']:,} tests ({pattern_info['criticality']})")

        # Exotic testing patterns
        report.append(f"\n## 🚀 Exotic/Complex Testing Patterns")
        for pattern_info in sorted(self.results["complex_scenarios"], key=lambda x: x["count"], reverse=True):
            report.append(
                f"- **{pattern_info['pattern'].replace('_', ' ').title()}**: {pattern_info['count']:,} occurrences ({pattern_info['complexity']})")

        # Framework distribution
        report.append(f"\n## 🛠️ Testing Framework Distribution")
        for framework, count in self.results["frameworks"].most_common():
            percentage = (count / stats["total_files"]) * 100
            report.append(
                f"- **{framework}**: {count:,} files ({percentage:.1f}%)")

        # Business logic insights
        report.append(f"\n## 💼 Business Logic Coverage")
        total_business_tests = sum(
            self.results["business_logic_patterns"].values())
        for pattern, count in self.results["business_logic_patterns"].most_common(15):
            percentage = (count / total_business_tests) * 100
            report.append(
                f"- **{pattern.replace('_', ' ').title()}**: {count:,} tests ({percentage:.1f}%)")

        return '\n'.join(report)


def main():
    analyzer = TestAnalyzer()
    results = analyzer.analyze_all_tests()

    # Generate and save report
    report = analyzer.generate_report()

    # Save results
    with open('/workspaces/modular-monolith-2/test_analysis_report.md', 'w') as f:
        f.write(report)

    with open('/workspaces/modular-monolith-2/test_analysis_data.json', 'w') as f:
        # Convert Counter objects to regular dicts for JSON serialization
        json_results = {}
        for key, value in results.items():
            if isinstance(value, Counter):
                json_results[key] = dict(value)
            elif isinstance(value, defaultdict):
                json_results[key] = dict(value)
            else:
                json_results[key] = value
        json.dump(json_results, f, indent=2, default=str)

    print(report)
    print(f"\n📁 Reports saved:")
    print(f"   - Markdown: test_analysis_report.md")
    print(f"   - JSON Data: test_analysis_data.json")


if __name__ == "__main__":
    main()
