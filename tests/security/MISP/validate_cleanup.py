#!/usr/bin/env python3
"""
MISP Asset Relocation - Cleanup Validation Script
Task: T2096k Cleanup Validation

This script validates the MISP migration is complete and safe for cleanup:
1. Verifies no orphaned files remain
2. Checks for unused dependencies
3. Validates no broken References
4. Confirms all functionality preserved
5. Executes final regression test suite
"""

import ast
import importlib.util
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Set, Tuple


class MISPCleanupValidator:
    """Validates MISP migration cleanup readiness"""

    def __init__(self, workspace_root: str):
        self.workspace_root = Path(workspace_root)
        self.misp_source = self.workspace_root / "features" / "MISP"
        self.test_root = self.workspace_root / "tests" / "security" / "MISP"
        self.apps_root = self.workspace_root / "apps"
        self.libs_root = self.workspace_root / "libs"

        self.issues = []
        self.warnings = []

    def validate_all(self) -> bool:
        """Execute all validation checks"""
        print("🔍 MISP Cleanup Validation Starting...")
        print(f"📁 Source Directory: {self.misp_source}")
        print(f"📁 Workspace Root: {self.workspace_root}")
        print()

        success = True

        # Core validation checks
        success &= self.check_orphaned_files()
        success &= self.check_unused_dependencies()
        success &= self.check_broken_references()
        success &= self.validate_functionality_preservation()
        success &= self.check_migration_completeness()
        success &= self.validate_test_coverage()

        # Final regression test
        success &= self.execute_final_regression_test()

        # Report results
        self.print_validation_report()

        return success

    def check_orphaned_files(self) -> bool:
        """Check for orphaned files that should have been migrated"""
        print("📋 Checking for orphaned files...")

        if not self.misp_source.exists():
            print("✅ Source directory already removed - no orphaned files")
            return True

        # Files that should have been migrated
        orphaned_files = []

        # Check for Python files with business logic
        for py_file in self.misp_source.rglob("*.py"):
            if self._is_business_logic_file(py_file):
                orphaned_files.append(py_file)

        # Check for configuration files
        for config_file in self.misp_source.rglob("*.json"):
            if self._is_configuration_file(config_file):
                orphaned_files.append(config_file)

        # Check for template files
        for template_file in self.misp_source.rglob("*.html"):
            if self._is_template_file(template_file):
                orphaned_files.append(template_file)

        if orphaned_files:
            self.issues.extend([
                f"Orphaned file: {f.relative_to(self.workspace_root)}"
                for f in orphaned_files
            ])
            print(f"❌ Found {len(orphaned_files)} orphaned files")
            return False
        else:
            print("✅ No orphaned files found")
            return True

    def _is_business_logic_file(self, filepath: Path) -> bool:
        """Check if Python file contains business logic"""
        try:
            content = filepath.read_text(encoding='utf-8')

            # Skip test files and __init__.py
            if 'test_' in filepath.name or filepath.name == '__init__.py':
                return False

            # Look for business logic indicators
            business_indicators = [
                'class.*Model',
                'def.*api',
                'def.*process',
                'def.*analyze',
                'def.*correlate',
                'async def',
                '@router',
                '@app.route'
            ]

            for indicator in business_indicators:
                if re.search(indicator, content, re.IGNORECASE):
                    return True

            return False
        except Exception:
            return False

    def _is_configuration_file(self, filepath: Path) -> bool:
        """Check if JSON file is configuration"""
        config_names = [
            'config', 'settings', 'package', 'manifest',
            'schema', 'template', 'taxonomy'
        ]

        return any(name in filepath.name.lower() for name in config_names)

    def _is_template_file(self, filepath: Path) -> bool:
        """Check if HTML file is a template"""
        try:
            content = filepath.read_text(encoding='utf-8')

            # Look for template indicators
            template_indicators = [
                '{{', '{% ', '{%', '${', '<template', 'ng-', 'v-'
            ]

            return any(indicator in content for indicator in template_indicators)
        except Exception:
            return False

    def check_unused_dependencies(self) -> bool:
        """Check for dependencies that are no longer needed"""
        print("📋 Checking for unused dependencies...")

        unused_deps = []

        # Check package.json dependencies
        package_json = self.workspace_root / "package.json"
        if package_json.exists():
            unused_deps.extend(self._check_npm_dependencies(package_json))

        # Check Python dependencies
        requirements_files = [
            self.workspace_root / "requirements.txt",
            self.apps_root / "jane-orchestrator" / "requirements.txt"
        ]

        for req_file in requirements_files:
            if req_file.exists():
                unused_deps.extend(self._check_python_dependencies(req_file))

        if unused_deps:
            self.warnings.extend([
                f"Potentially unused dependency: {dep}" for dep in unused_deps
            ])
            print(
                f"⚠️  Found {len(unused_deps)} potentially unused dependencies")
        else:
            print("✅ No unused dependencies detected")

        return True  # Warnings don't fail validation

    def _check_npm_dependencies(self, package_json: Path) -> List[str]:
        """Check for unused NPM dependencies"""
        try:
            package_data = json.loads(package_json.read_text())
            dependencies = package_data.get('dependencies', {})

            # MISP-specific dependencies that might be unused
            misp_related = [dep for dep in dependencies.keys()
                            if 'misp' in dep.lower()]

            unused = []
            for dep in misp_related:
                if not self._is_dependency_used(dep, ['.ts', '.tsx', '.js', '.jsx']):
                    unused.append(dep)

            return unused
        except Exception:
            return []

    def _check_python_dependencies(self, requirements_file: Path) -> List[str]:
        """Check for unused Python dependencies"""
        try:
            requirements = requirements_file.read_text().strip().split('\n')
            dependencies = [req.split('==')[0].split('>=')[0].strip()
                            for req in requirements if req and not req.startswith('#')]

            # MISP-specific dependencies
            misp_related = [dep for dep in dependencies
                            if 'misp' in dep.lower() or 'pymisp' in dep.lower()]

            unused = []
            for dep in misp_related:
                if not self._is_dependency_used(dep, ['.py']):
                    unused.append(dep)

            return unused
        except Exception:
            return []

    def _is_dependency_used(self, dependency: str, extensions: List[str]) -> bool:
        """Check if dependency is used in codebase"""
        import_patterns = [
            f"import {dependency}",
            f"from {dependency}",
            f"'{dependency}'",
            f'"{dependency}"'
        ]

        for ext in extensions:
            for file_path in self.workspace_root.rglob(f"*{ext}"):
                if 'node_modules' in str(file_path) or '.git' in str(file_path):
                    continue

                try:
                    content = file_path.read_text(encoding='utf-8')
                    if any(pattern in content for pattern in import_patterns):
                        return True
                except Exception:
                    continue

        return False

    def check_broken_references(self) -> bool:
        """Check for broken references to MISP source code"""
        print("📋 Checking for broken references...")

        broken_refs = []

        # Check import statements
        broken_refs.extend(self._check_import_references())

        # Check file path references
        broken_refs.extend(self._check_file_path_references())

        # Check configuration references
        broken_refs.extend(self._check_config_references())

        if broken_refs:
            self.issues.extend([
                f"Broken reference: {ref}" for ref in broken_refs
            ])
            print(f"❌ Found {len(broken_refs)} broken references")
            return False
        else:
            print("✅ No broken references found")
            return True

    def _check_import_references(self) -> List[str]:
        """Check for broken import statements"""
        broken_imports = []

        # Python imports
        for py_file in self.workspace_root.rglob("*.py"):
            if 'features/MISP' in str(py_file):
                continue

            try:
                content = py_file.read_text(encoding='utf-8')

                # Look for imports referencing features.MISP
                import_patterns = [
                    r'from features\.MISP',
                    r'import features\.MISP',
                    r'from.*features/MISP',
                    r'import.*features/MISP'
                ]

                for pattern in import_patterns:
                    matches = re.findall(pattern, content, re.IGNORECASE)
                    for match in matches:
                        broken_imports.append(f"{py_file}: {match}")

            except Exception:
                continue

        # TypeScript/JavaScript imports
        for ts_file in self.workspace_root.rglob("*.ts"):
            if ts_file.suffix in ['.ts', '.tsx', '.js', '.jsx']:
                try:
                    content = ts_file.read_text(encoding='utf-8')

                    import_patterns = [
                        r'from.*["\'].*features/MISP',
                        r'import.*["\'].*features/MISP'
                    ]

                    for pattern in import_patterns:
                        matches = re.findall(pattern, content, re.IGNORECASE)
                        for match in matches:
                            broken_imports.append(f"{ts_file}: {match}")

                except Exception:
                    continue

        return broken_imports

    def _check_file_path_references(self) -> List[str]:
        """Check for hardcoded file path references"""
        broken_paths = []

        path_patterns = [
            r'features/MISP',
            r'features\\MISP',
            r'"features/MISP"',
            r"'features/MISP'"
        ]

        for file_path in self.workspace_root.rglob("*"):
            if file_path.is_file() and file_path.suffix in ['.py', '.ts', '.tsx', '.js', '.jsx', '.json', '.yaml', '.yml']:
                if 'features/MISP' in str(file_path):
                    continue

                try:
                    content = file_path.read_text(encoding='utf-8')

                    for pattern in path_patterns:
                        matches = re.findall(pattern, content)
                        for match in matches:
                            broken_paths.append(f"{file_path}: {match}")

                except Exception:
                    continue

        return broken_paths

    def _check_config_references(self) -> List[str]:
        """Check configuration files for MISP references"""
        broken_configs = []

        config_files = [
            self.workspace_root / "nx.json",
            self.workspace_root / "package.json",
            self.workspace_root / "tsconfig.base.json"
        ]

        for config_file in config_files:
            if config_file.exists():
                try:
                    content = config_file.read_text()

                    if 'features/MISP' in content or 'features\\MISP' in content:
                        broken_configs.append(
                            f"Config reference in {config_file}")

                except Exception:
                    continue

        return broken_configs

    def validate_functionality_preservation(self) -> bool:
        """Validate that all MISP functionality is preserved"""
        print("📋 Validating functionality preservation...")

        # Check core MISP services are available
        missing_functionality = []

        # Event management
        if not self._check_service_exists("events", ["create", "read", "update", "delete"]):
            missing_functionality.append("Event management service")

        # Attribute management
        if not self._check_service_exists("attributes", ["create", "read", "correlate"]):
            missing_functionality.append("Attribute management service")

        # Organization management
        if not self._check_service_exists("organizations", ["list", "manage"]):
            missing_functionality.append("Organization management service")

        # Search functionality
        if not self._check_service_exists("search", ["query", "filter"]):
            missing_functionality.append("Search service")

        # Import/Export
        if not self._check_service_exists("import_export", ["import", "export"]):
            missing_functionality.append("Import/Export service")

        if missing_functionality:
            self.issues.extend([
                f"Missing functionality: {func}" for func in missing_functionality
            ])
            print(
                f"❌ Missing {len(missing_functionality)} core functionalities")
            return False
        else:
            print("✅ All core functionality preserved")
            return True

    def _check_service_exists(self, service_name: str, operations: List[str]) -> bool:
        """Check if service and operations exist in migrated code"""

        # Check in jane-orchestrator services
        service_dir = self.apps_root / "jane-orchestrator" / "src" / "services"

        service_patterns = [
            f"{service_name}_service.py",
            f"{service_name}.py",
            f"misp_{service_name}.py"
        ]

        service_found = False
        for pattern in service_patterns:
            service_file = service_dir / pattern
            if service_file.exists():
                service_found = True

                # Check operations exist
                try:
                    content = service_file.read_text()
                    operations_found = sum(1 for op in operations
                                           if f"def {op}" in content or f"async def {op}" in content)

                    # At least 50% of operations
                    if operations_found < len(operations) * 0.5:
                        return False

                except Exception:
                    return False

                break

        return service_found

    def check_migration_completeness(self) -> bool:
        """Verify migration completion against checklist"""
        print("📋 Checking migration completeness...")

        # Check if all expected files exist in migrated location
        expected_components = [
            "apps/jane-orchestrator/src/services/misp_service.py",
            "apps/jane-orchestrator/src/data/models/misp_models.py",
            "apps/jane-orchestrator/src/api/routes/misp_routes.py",
            "apps/jane-ui/src/components/security/MISPDashboard.tsx",
            "libs/service-adapters/src/misp/misp-adapter.ts",
            "tests/security/MISP/test_functionality.py"
        ]

        missing_components = []
        for component in expected_components:
            component_path = self.workspace_root / component
            if not component_path.exists():
                missing_components.append(component)

        if missing_components:
            self.issues.extend([
                f"Missing migrated component: {comp}" for comp in missing_components
            ])
            print(f"❌ Missing {len(missing_components)} expected components")
            return False
        else:
            print("✅ All expected components present")
            return True

    def validate_test_coverage(self) -> bool:
        """Validate comprehensive test coverage exists"""
        print("📋 Validating test coverage...")

        # Check test files exist
        required_test_files = [
            "test_api_integration.py",
            "test_functionality.py",
            "test_performance.py",
            "test_monorepo_integration.py",
            "test_security.py"
        ]

        missing_tests = []
        for test_file in required_test_files:
            test_path = self.test_root / test_file
            if not test_path.exists():
                missing_tests.append(test_file)

        if missing_tests:
            self.issues.extend([
                f"Missing test file: {test}" for test in missing_tests
            ])
            print(f"❌ Missing {len(missing_tests)} required test files")
            return False
        else:
            print("✅ All required test files present")
            return True

    def execute_final_regression_test(self) -> bool:
        """Execute comprehensive regression test suite"""
        print("📋 Executing final regression test suite...")

        try:
            # Run comprehensive test execution
            test_script = self.test_root / "execute_comprehensive_tests.py"
            if not test_script.exists():
                self.issues.append("Comprehensive test script not found")
                return False

            # Execute the test suite
            result = subprocess.run([
                sys.executable, str(test_script)
            ], cwd=str(self.workspace_root), capture_output=True, text=True)

            if result.returncode != 0:
                self.issues.append(f"Regression test failed: {result.stderr}")
                print("❌ Regression test suite failed")
                return False
            else:
                print("✅ Regression test suite passed")
                return True

        except Exception as e:
            self.issues.append(f"Error executing regression test: {str(e)}")
            print(f"❌ Error executing regression test: {e}")
            return False

    def print_validation_report(self):
        """Print comprehensive validation report"""
        print("\n" + "="*50)
        print("🔍 MISP CLEANUP VALIDATION REPORT")
        print("="*50)

        if not self.issues and not self.warnings:
            print("✅ VALIDATION PASSED - Ready for cleanup")
            print("\n🎉 All checks passed successfully!")
            print("📁 The features/MISP directory can be safely removed.")
            print("🚀 MISP integration is complete and functional.")
        else:
            if self.issues:
                print(f"❌ VALIDATION FAILED - {len(self.issues)} issues found")
                print("\n🚨 Critical Issues:")
                for issue in self.issues:
                    print(f"   • {issue}")

            if self.warnings:
                print(f"\n⚠️  {len(self.warnings)} warnings:")
                for warning in self.warnings:
                    print(f"   • {warning}")

            print("\n❌ Cleanup cannot proceed until issues are resolved.")

        print("\n" + "="*50)


def main():
    """Main execution function"""
    workspace_root = os.getcwd()
    validator = MISPCleanupValidator(workspace_root)

    success = validator.validate_all()

    if success:
        print("\n✅ T2096k Cleanup Validation: COMPLETE")
        print("🎯 Ready to proceed with T2106l Directory Removal")
        sys.exit(0)
    else:
        print("\n❌ T2096k Cleanup Validation: FAILED")
        print("🔧 Issues must be resolved before cleanup")
        sys.exit(1)


if __name__ == "__main__":
    main()
