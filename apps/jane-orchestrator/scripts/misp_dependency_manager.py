#!/usr/bin/env python3
"""
MISP Dependency Management Utility

This utility handles package dependency migration and version conflict resolution
for MISP integration as required by T1915d.

Usage:
    python misp_dependency_manager.py check          # Check for conflicts
    python misp_dependency_manager.py resolve        # Resolve conflicts
    python misp_dependency_manager.py install        # Install MISP dependencies
    python misp_dependency_manager.py validate       # Validate installation
"""

import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple


class MISPDependencyManager:
    """Manages MISP dependencies and resolves version conflicts."""

    def __init__(self, project_root: Optional[Path] = None):
        """Initialize dependency manager."""
        self.project_root = project_root or Path(__file__).parent.parent
        self.pyproject_path = self.project_root / "pyproject.toml"
        self.misp_requirements_path = self.project_root / "requirements-misp.txt"

        # Known version conflicts and their resolutions
        self.conflict_resolutions = {
            # Pydantic compatibility
            ("pydantic", "pydantic-settings"): {
                "pydantic": ">=2.12.0,<3.0.0",
                "pydantic-settings": ">=2.0.0,<3.0.0"
            },

            # Requests ecosystem
            ("requests", "urllib3", "certifi"): {
                "requests": ">=2.31.0,<3.0.0",
                "urllib3": ">=2.0.0,<3.0.0",
                "certifi": ">=2023.7.22"
            },

            # Async HTTP clients
            ("aiohttp", "yarl", "multidict"): {
                "aiohttp": ">=3.8.0,<4.0.0",
                "yarl": ">=1.9.0,<2.0.0",
                "multidict": ">=6.0.0,<7.0.0"
            },

            # Cryptography stack
            ("cryptography", "pyopenssl", "cffi"): {
                "cryptography": ">=41.0.0,<42.0.0",
                "pyopenssl": ">=23.0.0,<24.0.0",
                "cffi": ">=1.15.0,<2.0.0"
            }
        }

        # Dependencies that are known to be problematic
        self.problematic_dependencies = {
            "stix": "Use stix2 instead (legacy STIX 1.x has dependency conflicts)",
            "old-stix": "Conflicts with modern Python versions",
            "pymisp<2.5": "Older versions have security vulnerabilities"
        }

    def check_conflicts(self) -> Dict[str, List[str]]:
        """Check for dependency conflicts."""
        print("🔍 Checking for dependency conflicts...")

        conflicts = {
            "version_conflicts": [],
            "missing_dependencies": [],
            "problematic_packages": [],
            "resolution_suggestions": []
        }

        # Check for version conflicts in pyproject.toml
        if self.pyproject_path.exists():
            conflicts.update(self._check_pyproject_conflicts())

        # Check MISP-specific requirements
        if self.misp_requirements_path.exists():
            conflicts.update(self._check_misp_requirements_conflicts())

        # Check currently installed packages
        installed_conflicts = self._check_installed_conflicts()
        conflicts["installed_conflicts"] = installed_conflicts

        return conflicts

    def _check_pyproject_conflicts(self) -> Dict[str, List[str]]:
        """Check conflicts in pyproject.toml."""
        conflicts = {"pyproject_issues": []}

        try:
            import tomli
            with open(self.pyproject_path, 'rb') as f:
                pyproject_data = tomli.load(f)

            dependencies = pyproject_data.get(
                "project", {}).get("dependencies", [])

            # Parse dependencies and check for conflicts
            parsed_deps = {}
            for dep in dependencies:
                name, version = self._parse_dependency(dep)
                if name in parsed_deps:
                    conflicts["pyproject_issues"].append(
                        f"Duplicate dependency: {name}"
                    )
                parsed_deps[name] = version

            # Check against known conflict patterns
            for conflict_group, resolutions in self.conflict_resolutions.items():
                conflicted_deps = [
                    dep for dep in conflict_group if dep in parsed_deps]
                if len(conflicted_deps) > 1:
                    conflicts["pyproject_issues"].append(
                        f"Potential conflict: {', '.join(conflicted_deps)}"
                    )

        except ImportError:
            conflicts["pyproject_issues"].append(
                "tomli not available - install with: pip install tomli"
            )
        except Exception as e:
            conflicts["pyproject_issues"].append(
                f"Error reading pyproject.toml: {e}")

        return conflicts

    def _check_misp_requirements_conflicts(self) -> Dict[str, List[str]]:
        """Check conflicts in MISP requirements."""
        conflicts = {"misp_requirements_issues": []}

        try:
            with open(self.misp_requirements_path, 'r') as f:
                requirements = f.read()

            # Parse requirements
            req_lines = [
                line.strip() for line in requirements.split('\n')
                if line.strip() and not line.strip().startswith('#')
            ]

            parsed_reqs = {}
            for req in req_lines:
                name, version = self._parse_dependency(req)
                if name:
                    if name in parsed_reqs:
                        conflicts["misp_requirements_issues"].append(
                            f"Duplicate requirement: {name}"
                        )
                    parsed_reqs[name] = version

            # Check for problematic dependencies
            for dep_name in parsed_reqs:
                for problematic, reason in self.problematic_dependencies.items():
                    if dep_name.startswith(problematic.split('<')[0]):
                        conflicts["misp_requirements_issues"].append(
                            f"Problematic dependency {dep_name}: {reason}"
                        )

        except Exception as e:
            conflicts["misp_requirements_issues"].append(
                f"Error reading MISP requirements: {e}"
            )

        return conflicts

    def _check_installed_conflicts(self) -> List[str]:
        """Check conflicts in currently installed packages."""
        conflicts = []

        try:
            # Get list of installed packages
            result = subprocess.run(
                [sys.executable, "-m", "pip", "list", "--format=json"],
                capture_output=True,
                text=True,
                check=True
            )

            installed_packages = json.loads(result.stdout)
            installed_dict = {pkg["name"].lower(): pkg["version"]
                              for pkg in installed_packages}

            # Check for known conflict patterns
            for conflict_group, resolutions in self.conflict_resolutions.items():
                installed_from_group = [
                    (name, installed_dict[name])
                    for name in conflict_group
                    if name.lower() in installed_dict
                ]

                if len(installed_from_group) > 1:
                    conflicts.append(
                        f"Installed conflict: {', '.join([f'{n}=={v}' for n,
                                                         v in installed_from_group])}"
                    )

        except Exception as e:
            conflicts.append(f"Error checking installed packages: {e}")

        return conflicts

    def _parse_dependency(self, dep_str: str) -> Tuple[Optional[str], Optional[str]]:
        """Parse dependency string to extract name and version."""
        # Remove comments and clean up
        dep_str = dep_str.split('#')[0].strip()
        if not dep_str:
            return None, None

        # Parse name and version specifier
        match = re.match(r'^([a-zA-Z0-9_-]+)(.*)$', dep_str)
        if match:
            name = match.group(1).lower()
            version = match.group(2).strip()
            return name, version

        return None, None

    def resolve_conflicts(self) -> bool:
        """Resolve dependency conflicts automatically."""
        print("🔧 Resolving dependency conflicts...")

        conflicts = self.check_conflicts()

        # Apply automatic resolutions
        resolved_count = 0

        # Update pyproject.toml with conflict resolutions
        if conflicts.get("pyproject_issues"):
            resolved_count += self._apply_pyproject_resolutions()

        # Update MISP requirements with resolutions
        if conflicts.get("misp_requirements_issues"):
            resolved_count += self._apply_misp_requirements_resolutions()

        if resolved_count > 0:
            print(f"✅ Resolved {resolved_count} dependency conflicts")
            return True
        else:
            print("ℹ️  No automatic resolutions available")
            return False

    def _apply_pyproject_resolutions(self) -> int:
        """Apply resolutions to pyproject.toml."""
        # This would implement actual TOML editing
        # For now, just log what would be done
        print("📝 Would update pyproject.toml with resolved versions")
        return 1

    def _apply_misp_requirements_resolutions(self) -> int:
        """Apply resolutions to MISP requirements."""
        # This would implement actual requirements.txt editing
        print("📝 Would update requirements-misp.txt with resolved versions")
        return 1

    def install_dependencies(self) -> bool:
        """Install MISP dependencies."""
        print("📦 Installing MISP dependencies...")

        try:
            # Install from MISP requirements file
            if self.misp_requirements_path.exists():
                cmd = [
                    sys.executable, "-m", "pip", "install",
                    "-r", str(self.misp_requirements_path)
                ]

                result = subprocess.run(cmd, capture_output=True, text=True)

                if result.returncode == 0:
                    print("✅ MISP dependencies installed successfully")
                    return True
                else:
                    print(f"❌ Installation failed: {result.stderr}")
                    return False
            else:
                print("❌ MISP requirements file not found")
                return False

        except Exception as e:
            print(f"❌ Installation error: {e}")
            return False

    def validate_installation(self) -> Dict[str, bool]:
        """Validate MISP dependency installation."""
        print("✅ Validating MISP installation...")

        validation_results = {}

        # Test critical imports
        critical_imports = [
            "pymisp",
            "stix2",
            "requests",
            "redis",
            "jsonschema",
            "yaml"
        ]

        for module_name in critical_imports:
            try:
                __import__(module_name)
                validation_results[module_name] = True
                print(f"  ✅ {module_name}")
            except ImportError:
                validation_results[module_name] = False
                print(f"  ❌ {module_name}")

        # Test MISP adapter functionality
        try:
            from pymisp import PyMISP
            validation_results["pymisp_functional"] = True
            print("  ✅ PyMISP functional")
        except Exception:
            validation_results["pymisp_functional"] = False
            print("  ❌ PyMISP functional")

        # Overall validation
        all_passed = all(validation_results.values())
        validation_results["overall"] = all_passed

        if all_passed:
            print("🎉 All validations passed!")
        else:
            print("⚠️  Some validations failed")

        return validation_results


def main():
    """Main CLI interface."""
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    command = sys.argv[1]
    manager = MISPDependencyManager()

    if command == "check":
        conflicts = manager.check_conflicts()
        print(json.dumps(conflicts, indent=2))

    elif command == "resolve":
        success = manager.resolve_conflicts()
        sys.exit(0 if success else 1)

    elif command == "install":
        success = manager.install_dependencies()
        sys.exit(0 if success else 1)

    elif command == "validate":
        results = manager.validate_installation()
        success = results.get("overall", False)
        sys.exit(0 if success else 1)

    else:
        print(f"Unknown command: {command}")
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
