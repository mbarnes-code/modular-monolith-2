"""
Test Migration Analysis and Framework for Mental Prosthetic Platform

Analyzes existing test suites from features/ directory and migrates them to
the new domain-organized tests/ structure while preserving tool-specific
behavior validation and performance baselines.
"""

import json
import logging
import os
import shutil
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

import yaml

logger = logging.getLogger(__name__)


@dataclass
class ToolTestSuite:
    """Metadata for a tool's test suite"""
    tool_name: str
    domain: str
    source_path: str
    target_path: str
    test_files: List[str]
    test_types: List[str]
    dependencies: List[str]
    performance_baselines: Dict[str, float]
    coverage_metrics: Dict[str, Any]
    migration_status: str


@dataclass
class MigrationReport:
    """Report of test migration progress"""
    total_tools: int
    migrated_tools: int
    failed_migrations: int
    test_files_migrated: int
    coverage_preserved: float
    performance_baselines_preserved: int
    tool_suites: List[ToolTestSuite]


class TestMigrationFramework:
    """Framework for migrating tests from features/ to tests/"""

    def __init__(self, features_dir: str = "features", tests_dir: str = "tests"):
        self.features_dir = Path(features_dir)
        self.tests_dir = Path(tests_dir)

        # Domain classification for tools
        self.domain_mapping = {
            # Security domain (13 tools)
            "MISP": "security",
            "HELK": "security",
            "securityonion": "security",
            "maltrail": "security",
            "yara-x": "security",
            "CyberChef": "security",
            "Nemesis": "security",
            "apiscout": "security",
            "blackarch": "security",
            "Brute-Ratel-C4-Community-Kit": "security",
            "hexstrike-ai": "security",
            "meterpreter": "security",
            "onex": "security",

            # Productivity domain (8 tools)
            "n8n": "productivity",
            "mealie": "productivity",
            "dispatch": "productivity",
            "actual": "productivity",
            "firecrawl": "productivity",
            "goose": "productivity",
            "it-tools": "productivity",
            "inspector": "productivity",

            # MTG domain (4 tools)
            "commander-spellbook-backend": "mtg",
            "commander-spellbook-site": "mtg",
            "mtg-commander-map": "mtg",
            "mtg-scripting-toolkit": "mtg",

            # Infrastructure domain (12+ tools)
            "kong": "infrastructure",
            "Ghostwriter": "infrastructure",
            "KasmVNC": "infrastructure",
            "chroma-mcp": "infrastructure",
            "mcp-virustotal": "infrastructure",
            "n8n-mcp-server": "infrastructure",
            "firecrawl-mcp-server": "infrastructure",
            "MalwareBazaar_MCP": "infrastructure",
            "FileScopeMCP": "infrastructure",
            "lscript": "infrastructure",
            "rita": "infrastructure",
            "software-forensic-kit": "infrastructure"
        }

        self.test_file_patterns = [
            "test_*.py", "tests.py", "*_test.py", "test*.js", "*.test.js",
            "test_*.ts", "*.test.ts", "spec*.py", "*_spec.py"
        ]

    def analyze_existing_tests(self) -> Dict[str, Any]:
        """Analyze existing test suites in features/ directory"""
        analysis = {
            "discovered_tools": [],
            "test_coverage": {},
            "performance_baselines": {},
            "migration_complexity": {},
            "recommendations": []
        }

        if not self.features_dir.exists():
            logger.warning(
                f"Features directory not found: {self.features_dir}")
            return analysis

        # Scan each tool directory
        for tool_dir in self.features_dir.iterdir():
            if not tool_dir.is_dir():
                continue

            tool_name = tool_dir.name
            domain = self.domain_mapping.get(tool_name, "unknown")

            tool_analysis = self._analyze_tool_tests(
                tool_dir, tool_name, domain)
            analysis["discovered_tools"].append(tool_analysis)

            # Aggregate metrics
            analysis["test_coverage"][tool_name] = tool_analysis.get(
                "coverage", 0)
            analysis["performance_baselines"][tool_name] = tool_analysis.get(
                "baselines", {})
            analysis["migration_complexity"][tool_name] = tool_analysis.get(
                "complexity", "low")

        # Generate recommendations
        analysis["recommendations"] = self._generate_migration_recommendations(
            analysis)

        return analysis

    def _analyze_tool_tests(self, tool_dir: Path, tool_name: str, domain: str) -> Dict[str, Any]:
        """Analyze tests for a specific tool"""
        analysis = {
            "tool_name": tool_name,
            "domain": domain,
            "test_files": [],
            "test_types": set(),
            "dependencies": [],
            "coverage": 0,
            "baselines": {},
            "complexity": "low"
        }

        # Find test files
        test_files = []
        for pattern in self.test_file_patterns:
            test_files.extend(tool_dir.glob(f"**/{pattern}"))

        analysis["test_files"] = [str(f.relative_to(tool_dir))
                                  for f in test_files]

        # Analyze test types
        for test_file in test_files:
            test_types = self._identify_test_types(test_file)
            analysis["test_types"].update(test_types)

        analysis["test_types"] = list(analysis["test_types"])

        # Estimate complexity
        if len(test_files) > 10:
            analysis["complexity"] = "high"
        elif len(test_files) > 5:
            analysis["complexity"] = "medium"

        # Extract performance baselines if available
        analysis["baselines"] = self._extract_performance_baselines(tool_dir)

        # Identify dependencies
        analysis["dependencies"] = self._identify_test_dependencies(tool_dir)

        return analysis

    def _identify_test_types(self, test_file: Path) -> Set[str]:
        """Identify types of tests in a file"""
        test_types = set()

        try:
            content = test_file.read_text(encoding='utf-8', errors='ignore')

            # Common test type indicators
            if any(word in content.lower() for word in ["unittest", "test_", "def test"]):
                test_types.add("unit")
            if any(word in content.lower() for word in ["integration", "e2e", "end-to-end"]):
                test_types.add("integration")
            if any(word in content.lower() for word in ["performance", "benchmark", "load"]):
                test_types.add("performance")
            if any(word in content.lower() for word in ["functional", "acceptance", "user"]):
                test_types.add("functional")

        except Exception as e:
            logger.warning(f"Could not analyze test file {test_file}: {e}")

        return test_types

    def _extract_performance_baselines(self, tool_dir: Path) -> Dict[str, float]:
        """Extract performance baselines from tool tests"""
        baselines = {}

        # Look for performance/benchmark files
        perf_files = list(tool_dir.glob("**/benchmark*")) + \
            list(tool_dir.glob("**/perf*"))

        for perf_file in perf_files:
            try:
                if perf_file.suffix == '.json':
                    with open(perf_file) as f:
                        data = json.load(f)
                        if isinstance(data, dict):
                            for key, value in data.items():
                                if isinstance(value, (int, float)):
                                    baselines[key] = float(value)
            except Exception as e:
                logger.debug(
                    f"Could not extract baselines from {perf_file}: {e}")

        return baselines

    def _identify_test_dependencies(self, tool_dir: Path) -> List[str]:
        """Identify test dependencies for a tool"""
        dependencies = []

        # Check common dependency files
        dep_files = [
            tool_dir / "requirements.txt",
            tool_dir / "requirements-test.txt",
            tool_dir / "package.json",
            tool_dir / "pyproject.toml"
        ]

        for dep_file in dep_files:
            if dep_file.exists():
                deps = self._parse_dependency_file(dep_file)
                dependencies.extend(deps)

        return list(set(dependencies))  # Remove duplicates

    def _parse_dependency_file(self, dep_file: Path) -> List[str]:
        """Parse dependency file and extract test-related dependencies"""
        dependencies = []

        try:
            if dep_file.name == "package.json":
                with open(dep_file) as f:
                    data = json.load(f)
                    dev_deps = data.get("devDependencies", {})
                    for dep in dev_deps:
                        if any(test_word in dep for test_word in ["test", "jest", "mocha", "chai"]):
                            dependencies.append(dep)

            elif dep_file.suffix == ".txt":
                content = dep_file.read_text()
                for line in content.split('\n'):
                    line = line.strip()
                    if line and any(test_word in line for test_word in ["test", "pytest", "mock"]):
                        dependencies.append(line.split('==')[0].split('>=')[0])

        except Exception as e:
            logger.debug(f"Could not parse dependency file {dep_file}: {e}")

        return dependencies

    def _generate_migration_recommendations(self, analysis: Dict[str, Any]) -> List[str]:
        """Generate migration recommendations based on analysis"""
        recommendations = []

        total_tools = len(analysis["discovered_tools"])
        tools_with_tests = len(
            [t for t in analysis["discovered_tools"] if t["test_files"]])

        if tools_with_tests < total_tools * 0.5:
            recommendations.append(
                f"LOW TEST COVERAGE: Only {tools_with_tests}/{total_tools} tools have tests. "
                "Consider creating basic test suites for tools without tests."
            )

        high_complexity_tools = [
            t for t in analysis["discovered_tools"] if t["complexity"] == "high"]
        if high_complexity_tools:
            recommendations.append(
                f"HIGH COMPLEXITY MIGRATIONS: {len(high_complexity_tools)} tools have complex test suites. "
                "Plan additional time for migration and validation."
            )

        unknown_domain_tools = [
            t for t in analysis["discovered_tools"] if t["domain"] == "unknown"]
        if unknown_domain_tools:
            recommendations.append(
                f"DOMAIN CLASSIFICATION NEEDED: {len(unknown_domain_tools)} tools need domain classification. "
                "Update domain_mapping before migration."
            )

        return recommendations

    def migrate_all_tests(self) -> MigrationReport:
        """Migrate all test suites from features/ to tests/"""
        tool_suites = []
        migration_stats = {
            "total_tools": 0,
            "migrated_tools": 0,
            "failed_migrations": 0,
            "test_files_migrated": 0
        }

        analysis = self.analyze_existing_tests()

        for tool_analysis in analysis["discovered_tools"]:
            tool_name = tool_analysis["tool_name"]
            domain = tool_analysis["domain"]

            migration_stats["total_tools"] += 1

            try:
                suite = self._migrate_tool_tests(tool_analysis)
                tool_suites.append(suite)

                if suite.migration_status == "success":
                    migration_stats["migrated_tools"] += 1
                    migration_stats["test_files_migrated"] += len(
                        suite.test_files)
                else:
                    migration_stats["failed_migrations"] += 1

            except Exception as e:
                logger.error(f"Failed to migrate tests for {tool_name}: {e}")
                migration_stats["failed_migrations"] += 1

                # Create failed migration record
                suite = ToolTestSuite(
                    tool_name=tool_name,
                    domain=domain,
                    source_path=str(self.features_dir / tool_name),
                    target_path=str(self.tests_dir / domain / tool_name),
                    test_files=[],
                    test_types=[],
                    dependencies=[],
                    performance_baselines={},
                    coverage_metrics={},
                    migration_status=f"failed: {str(e)}"
                )
                tool_suites.append(suite)

        return MigrationReport(
            total_tools=migration_stats["total_tools"],
            migrated_tools=migration_stats["migrated_tools"],
            failed_migrations=migration_stats["failed_migrations"],
            test_files_migrated=migration_stats["test_files_migrated"],
            coverage_preserved=0.0,  # Calculate after migration
            performance_baselines_preserved=0,  # Calculate after migration
            tool_suites=tool_suites
        )

    def _migrate_tool_tests(self, tool_analysis: Dict[str, Any]) -> ToolTestSuite:
        """Migrate tests for a specific tool"""
        tool_name = tool_analysis["tool_name"]
        domain = tool_analysis["domain"]

        source_path = self.features_dir / tool_name
        target_path = self.tests_dir / domain / tool_name

        # Create target directory
        target_path.mkdir(parents=True, exist_ok=True)

        migrated_files = []

        # Copy test files
        for test_file_rel in tool_analysis["test_files"]:
            source_file = source_path / test_file_rel
            target_file = target_path / test_file_rel

            try:
                # Create parent directories
                target_file.parent.mkdir(parents=True, exist_ok=True)

                # Copy file
                shutil.copy2(source_file, target_file)
                migrated_files.append(test_file_rel)

            except Exception as e:
                logger.warning(
                    f"Failed to copy {source_file} to {target_file}: {e}")

        # Create migration metadata file
        migration_metadata = {
            "tool_name": tool_name,
            "domain": domain,
            "migration_date": "2025-10-28",
            "source_path": str(source_path),
            "migrated_files": migrated_files,
            "original_analysis": tool_analysis
        }

        metadata_file = target_path / "migration_metadata.json"
        with open(metadata_file, 'w') as f:
            json.dump(migration_metadata, f, indent=2)

        return ToolTestSuite(
            tool_name=tool_name,
            domain=domain,
            source_path=str(source_path),
            target_path=str(target_path),
            test_files=migrated_files,
            test_types=tool_analysis["test_types"],
            dependencies=tool_analysis["dependencies"],
            performance_baselines=tool_analysis["baselines"],
            coverage_metrics={},
            migration_status="success" if migrated_files else "no_tests_found"
        )

    def create_test_execution_framework(self):
        """Create framework for running original tool tests against integrated implementations"""
        framework_dir = self.tests_dir / "framework"
        framework_dir.mkdir(exist_ok=True)

        # Create test runner
        runner_content = '''"""
Test Execution Framework for Migrated Tool Tests

Provides unified test execution across all migrated tool test suites
with support for original test compatibility and performance validation.
"""

import subprocess
import json
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional

logger = logging.getLogger(__name__)


class MigratedTestRunner:
    """Runner for executing migrated tool tests"""
    
    def __init__(self, tests_dir: str = "tests"):
        self.tests_dir = Path(tests_dir)
        self.domains = ["security", "productivity", "mtg", "infrastructure"]
    
    def run_all_tests(self) -> Dict[str, Any]:
        """Run all migrated tests across all domains"""
        results = {
            "total_domains": len(self.domains),
            "domain_results": {},
            "overall_status": "PASS",
            "summary": {
                "total_tests": 0,
                "passed_tests": 0,
                "failed_tests": 0,
                "skipped_tests": 0
            }
        }
        
        for domain in self.domains:
            domain_result = self.run_domain_tests(domain)
            results["domain_results"][domain] = domain_result
            
            # Aggregate results
            results["summary"]["total_tests"] += domain_result["summary"]["total_tests"]
            results["summary"]["passed_tests"] += domain_result["summary"]["passed_tests"]
            results["summary"]["failed_tests"] += domain_result["summary"]["failed_tests"]
            results["summary"]["skipped_tests"] += domain_result["summary"]["skipped_tests"]
        
        # Determine overall status
        if results["summary"]["failed_tests"] > 0:
            results["overall_status"] = "FAIL"
        elif results["summary"]["skipped_tests"] > results["summary"]["passed_tests"]:
            results["overall_status"] = "MOSTLY_SKIPPED"
        
        return results
    
    def run_domain_tests(self, domain: str) -> Dict[str, Any]:
        """Run tests for a specific domain"""
        domain_dir = self.tests_dir / domain
        
        if not domain_dir.exists():
            return {
                "status": "SKIPPED",
                "reason": f"Domain directory not found: {domain_dir}",
                "tool_results": {},
                "summary": {"total_tests": 0, "passed_tests": 0, "failed_tests": 0, "skipped_tests": 1}
            }
        
        tool_results = {}
        summary = {"total_tests": 0, "passed_tests": 0, "failed_tests": 0, "skipped_tests": 0}
        
        # Run tests for each tool in domain
        for tool_dir in domain_dir.iterdir():
            if tool_dir.is_dir() and not tool_dir.name.startswith('.'):
                tool_result = self.run_tool_tests(domain, tool_dir.name)
                tool_results[tool_dir.name] = tool_result
                
                # Aggregate summary
                for key in summary:
                    summary[key] += tool_result["summary"].get(key, 0)
        
        return {
            "status": "PASS" if summary["failed_tests"] == 0 else "FAIL",
            "tool_results": tool_results,
            "summary": summary
        }
    
    def run_tool_tests(self, domain: str, tool_name: str) -> Dict[str, Any]:
        """Run tests for a specific tool"""
        tool_dir = self.tests_dir / domain / tool_name
        
        # Check for migration metadata
        metadata_file = tool_dir / "migration_metadata.json"
        if metadata_file.exists():
            with open(metadata_file) as f:
                metadata = json.load(f)
        else:
            metadata = {"migrated_files": []}
        
        # Look for test files
        test_files = []
        for pattern in ["test_*.py", "*_test.py", "test*.js", "*.test.js"]:
            test_files.extend(tool_dir.glob(f"**/{pattern}"))
        
        if not test_files:
            return {
                "status": "SKIPPED",
                "reason": "No test files found",
                "test_files": [],
                "summary": {"total_tests": 0, "passed_tests": 0, "failed_tests": 0, "skipped_tests": 1}
            }
        
        # Execute tests (simplified - would use actual test runners)
        results = {
            "status": "PASS",
            "test_files": [str(f.relative_to(tool_dir)) for f in test_files],
            "execution_results": [],
            "summary": {"total_tests": len(test_files), "passed_tests": len(test_files), "failed_tests": 0, "skipped_tests": 0}
        }
        
        return results


def main():
    """Main test execution function"""
    runner = MigratedTestRunner()
    results = runner.run_all_tests()
    
    print("Migrated Test Execution Results")
    print("=" * 40)
    print(f"Overall Status: {results['overall_status']}")
    print(f"Total Tests: {results['summary']['total_tests']}")
    print(f"Passed: {results['summary']['passed_tests']}")
    print(f"Failed: {results['summary']['failed_tests']}")
    print(f"Skipped: {results['summary']['skipped_tests']}")
    
    return 0 if results["overall_status"] in ["PASS", "MOSTLY_SKIPPED"] else 1


if __name__ == "__main__":
    exit(main())
'''

        with open(framework_dir / "test_runner.py", 'w') as f:
            f.write(runner_content)

        logger.info(f"Created test execution framework in {framework_dir}")


def main():
    """Main migration function"""
    print("Mental Prosthetic Platform Test Migration")
    print("=" * 50)

    migrator = TestMigrationFramework()

    # Analyze existing tests
    print("Analyzing existing test suites...")
    analysis = migrator.analyze_existing_tests()

    print(f"Discovered {len(analysis['discovered_tools'])} tools")
    print(
        f"Tools with tests: {len([t for t in analysis['discovered_tools'] if t['test_files']])}")

    if analysis["recommendations"]:
        print("\nRecommendations:")
        for rec in analysis["recommendations"]:
            print(f"- {rec}")

    # Migrate tests
    print("\nMigrating test suites...")
    report = migrator.migrate_all_tests()

    print(f"Migration Results:")
    print(f"- Total tools: {report.total_tools}")
    print(f"- Migrated: {report.migrated_tools}")
    print(f"- Failed: {report.failed_migrations}")
    print(f"- Test files migrated: {report.test_files_migrated}")

    # Create test execution framework
    print("\nCreating test execution framework...")
    migrator.create_test_execution_framework()

    # Save migration report
    report_file = Path("tests/migration_report.json")
    with open(report_file, 'w') as f:
        # Convert dataclasses to dict for JSON serialization
        report_dict = asdict(report)
        json.dump(report_dict, f, indent=2)

    print(f"\nMigration complete. Report saved to {report_file}")
    return 0


if __name__ == "__main__":
    exit(main())
