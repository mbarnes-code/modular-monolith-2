"""
MISP Build Integration Service

Integrates MISP build assets and deployment processes into Jane's unified
service architecture with constitutional compliance.
"""

import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict

from ..base_service import BaseService
from .misp_build_assets import misp_build_manager
from .misp_build_deployment import misp_deployment_manager

logger = logging.getLogger(__name__)


class MISPBuildIntegrationService(BaseService):
    """
    Service for managing MISP build and deployment integration.

    Provides:
    - Build asset preservation
    - Deployment process orchestration
    - Constitutional compliance monitoring
    - Jane platform integration
    """

    def __init__(self):
        super().__init__()
        self.build_manager = misp_build_manager
        self.deployment_manager = misp_deployment_manager
        self.service_name = "misp_build_integration"

    async def preserve_build_assets(self) -> Dict[str, Any]:
        """
        Preserve MISP build assets with constitutional compliance.

        Returns:
            Dict containing build asset preservation results
        """
        operation_start = datetime.now()

        try:
            logger.info("Starting MISP build assets preservation...")

            # Execute build asset preservation
            result = self.build_manager.preserve_build_scripts()

            # Constitutional compliance monitoring
            operation_time = (
                datetime.now() - operation_start
            ).total_seconds()

            if operation_time > 1.0:
                logger.warning(
                    f"Build asset preservation took {operation_time:.2f}s "
                    "- exceeds security domain <1s requirement"
                )

            # Add service metadata
            result["service_info"] = {
                "service_name": self.service_name,
                "operation": "preserve_build_assets",
                "operation_time_seconds": operation_time,
                "constitutional_compliance": operation_time <= 1.0
            }

            logger.info(
                f"MISP build assets preservation completed "
                f"in {operation_time:.3f}s"
            )

            return result

        except Exception as e:
            logger.error(f"Build assets preservation failed: {e}")
            return {
                "status": "error",
                "error": str(e),
                "service_info": {
                    "service_name": self.service_name,
                    "operation": "preserve_build_assets"
                },
                "timestamp": datetime.now().isoformat()
            }

    async def execute_build_deployment(
        self,
        target_platform: str = "ubuntu-24.04",
        deployment_type: str = "development"
    ) -> Dict[str, Any]:
        """
        Execute MISP build deployment process.

        Args:
            target_platform: Target deployment platform
            deployment_type: Type of deployment

        Returns:
            Dict containing deployment execution results
        """
        operation_start = datetime.now()

        try:
            logger.info(
                f"Starting MISP build deployment for {target_platform} "
                f"({deployment_type})..."
            )

            # Execute build deployment
            result = await self.deployment_manager.execute_build_process(
                target_platform, deployment_type
            )

            # Add service metadata
            operation_time = (
                datetime.now() - operation_start
            ).total_seconds()

            result["service_info"] = {
                "service_name": self.service_name,
                "operation": "execute_build_deployment",
                "operation_time_seconds": operation_time,
                "target_platform": target_platform,
                "deployment_type": deployment_type
            }

            logger.info(
                f"MISP build deployment completed for {target_platform} "
                f"in {operation_time:.2f}s"
            )

            return result

        except Exception as e:
            logger.error(f"Build deployment failed: {e}")
            return {
                "status": "error",
                "error": str(e),
                "service_info": {
                    "service_name": self.service_name,
                    "operation": "execute_build_deployment",
                    "target_platform": target_platform,
                    "deployment_type": deployment_type
                },
                "timestamp": datetime.now().isoformat()
            }

    async def get_build_status(self) -> Dict[str, Any]:
        """
        Get current MISP build status and capabilities.

        Returns:
            Dict containing build status information
        """
        try:
            # Check build assets status
            build_artifacts_path = self.build_manager.build_artifacts_path
            artifacts_exist = build_artifacts_path.exists()

            # Count preserved assets
            asset_counts = {}
            if artifacts_exist:
                for asset_type in ["debian", "installation", "configuration",
                                   "docker", "services"]:
                    asset_dir = build_artifacts_path / asset_type
                    if asset_dir.exists():
                        asset_counts[asset_type] = len(
                            list(asset_dir.rglob("*")))
                    else:
                        asset_counts[asset_type] = 0

            # Check deployment artifacts
            deployment_artifacts_path = (
                self.deployment_manager.deployment_artifacts_path
            )
            deployments_exist = deployment_artifacts_path.exists()

            deployment_counts = {}
            if deployments_exist:
                for platform_dir in deployment_artifacts_path.iterdir():
                    if platform_dir.is_dir():
                        deployment_counts[platform_dir.name] = len(
                            list(platform_dir.rglob("*"))
                        )

            return {
                "status": "success",
                "build_assets": {
                    "preserved": artifacts_exist,
                    "assets_path": str(build_artifacts_path),
                    "asset_counts": asset_counts
                },
                "deployment_artifacts": {
                    "available": deployments_exist,
                    "artifacts_path": str(deployment_artifacts_path),
                    "deployment_counts": deployment_counts
                },
                "capabilities": {
                    "supported_platforms": [
                        "ubuntu-24.04", "ubuntu-22.04",
                        "debian-12", "debian-13",
                        "rhel-8", "docker", "kubernetes"
                    ],
                    "deployment_types": [
                        "development", "staging", "production"
                    ],
                    "jane_integration": True,
                    "constitutional_compliance": True
                },
                "service_info": {
                    "service_name": self.service_name,
                    "operation": "get_build_status"
                },
                "timestamp": datetime.now().isoformat()
            }

        except Exception as e:
            logger.error(f"Failed to get build status: {e}")
            return {
                "status": "error",
                "error": str(e),
                "service_info": {
                    "service_name": self.service_name,
                    "operation": "get_build_status"
                },
                "timestamp": datetime.now().isoformat()
            }

    async def validate_build_environment(self) -> Dict[str, Any]:
        """
        Validate build environment for MISP deployment.

        Returns:
            Dict containing environment validation results
        """
        try:
            validation_results = {
                "docker_available": False,
                "bash_available": False,
                "python_available": False,
                "misp_source_available": False,
                "build_dependencies": []
            }

            # Check Docker availability
            try:
                import subprocess
                result = subprocess.run(
                    ["docker", "--version"],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                validation_results["docker_available"] = result.returncode == 0
                if result.returncode == 0:
                    validation_results["docker_version"] = result.stdout.strip(
                    )
            except (subprocess.SubprocessError, FileNotFoundError):
                validation_results["docker_available"] = False

            # Check Bash availability
            try:
                result = subprocess.run(
                    ["bash", "--version"],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                validation_results["bash_available"] = result.returncode == 0
            except (subprocess.SubprocessError, FileNotFoundError):
                validation_results["bash_available"] = False

            # Check Python availability
            try:
                result = subprocess.run(
                    ["python3", "--version"],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                validation_results["python_available"] = result.returncode == 0
                if result.returncode == 0:
                    validation_results["python_version"] = result.stdout.strip(
                    )
            except (subprocess.SubprocessError, FileNotFoundError):
                validation_results["python_available"] = False

            # Check MISP source availability
            misp_source_path = self.build_manager.misp_source_path
            validation_results["misp_source_available"] = misp_source_path.exists(
            )
            if misp_source_path.exists():
                validation_results["misp_source_path"] = str(misp_source_path)

            # Determine overall validation status
            critical_deps = [
                validation_results["bash_available"],
                validation_results["python_available"],
                validation_results["misp_source_available"]
            ]

            overall_status = "valid" if all(critical_deps) else "invalid"

            return {
                "status": "success",
                "validation_status": overall_status,
                "environment": validation_results,
                "recommendations": self._generate_environment_recommendations(
                    validation_results
                ),
                "service_info": {
                    "service_name": self.service_name,
                    "operation": "validate_build_environment"
                },
                "timestamp": datetime.now().isoformat()
            }

        except Exception as e:
            logger.error(f"Build environment validation failed: {e}")
            return {
                "status": "error",
                "error": str(e),
                "service_info": {
                    "service_name": self.service_name,
                    "operation": "validate_build_environment"
                },
                "timestamp": datetime.now().isoformat()
            }

    def _generate_environment_recommendations(
        self, validation_results: Dict[str, Any]
    ) -> list:
        """Generate environment setup recommendations."""
        recommendations = []

        if not validation_results["docker_available"]:
            recommendations.append({
                "component": "Docker",
                "issue": "Docker not available",
                "solution": "Install Docker for container-based deployments",
                "priority": "medium"
            })

        if not validation_results["bash_available"]:
            recommendations.append({
                "component": "Bash",
                "issue": "Bash shell not available",
                "solution": "Install Bash shell for script execution",
                "priority": "high"
            })

        if not validation_results["python_available"]:
            recommendations.append({
                "component": "Python",
                "issue": "Python 3 not available",
                "solution": "Install Python 3 for build scripts",
                "priority": "high"
            })

        if not validation_results["misp_source_available"]:
            recommendations.append({
                "component": "MISP Source",
                "issue": "MISP source code not found",
                "solution": "Ensure MISP source is available in features/MISP",
                "priority": "critical"
            })

        return recommendations


# Service instance
misp_build_integration_service = MISPBuildIntegrationService()
