"""
Service Restart Manager for Mental Prosthetic Platform

Provides controlled restart capabilities for individual domain services
across all 37 mental prosthetic tools with graceful shutdown, state
preservation, and dependency management.
"""

import asyncio
import json
import logging
import os
import signal
import subprocess
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

import psutil

logger = logging.getLogger(__name__)


class ServiceStatus(Enum):
    """Status of domain services."""
    RUNNING = "running"
    STOPPED = "stopped"
    STARTING = "starting"
    STOPPING = "stopping"
    FAILED = "failed"
    UNKNOWN = "unknown"


class RestartStrategy(Enum):
    """Strategies for service restart."""
    GRACEFUL = "graceful"      # Graceful shutdown then restart
    IMMEDIATE = "immediate"    # Kill and restart immediately
    ROLLING = "rolling"        # Rolling restart with health checks
    DEPENDENCY_AWARE = "dependency_aware"  # Restart with dependency order


@dataclass
class ServiceInfo:
    """Information about a domain service."""
    service_id: str
    service_name: str
    domain: str
    pid: Optional[int] = None
    port: Optional[int] = None
    status: ServiceStatus = ServiceStatus.UNKNOWN
    health_check_url: Optional[str] = None
    dependencies: List[str] = field(default_factory=list)
    dependents: List[str] = field(default_factory=list)
    restart_command: Optional[str] = None
    working_directory: Optional[str] = None
    environment_vars: Dict[str, str] = field(default_factory=dict)


@dataclass
class RestartOperation:
    """Represents a service restart operation."""
    operation_id: str
    service_id: str
    strategy: RestartStrategy
    started_at: datetime
    completed_at: Optional[datetime] = None
    status: ServiceStatus = ServiceStatus.STARTING
    error_message: Optional[str] = None
    pre_restart_checks: List[str] = field(default_factory=list)
    post_restart_checks: List[str] = field(default_factory=list)
    affected_services: List[str] = field(default_factory=list)


class ServiceRestartManager:
    """Manages restart operations for domain services."""

    def __init__(self, config_dir: str = "/etc/mental-prosthetic/services"):
        self.config_dir = Path(config_dir)
        self.services: Dict[str, ServiceInfo] = {}
        self.restart_history: List[RestartOperation] = []

        # Load service configurations
        self._load_service_configurations()

        # Service dependency graph
        self.dependency_graph = self._build_dependency_graph()

    def _load_service_configurations(self):
        """Load service configurations from config directory."""
        # Default service configurations for Mental Prosthetic Platform
        default_services = {
            # Core orchestration services
            "jane-orchestrator": {
                "service_name": "Jane Orchestrator",
                "domain": "orchestration",
                "port": 8000,
                "health_check_url": "http://localhost:8000/health",
                "restart_command": "uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000",
                "working_directory": "/workspaces/modular-monolith-2/apps/jane-orchestrator",
                "dependencies": ["postgres", "redis"]
            },
            "jane-ui": {
                "service_name": "Jane UI",
                "domain": "frontend",
                "port": 3000,
                "health_check_url": "http://localhost:3000",
                "restart_command": "npx nx serve jane-ui",
                "working_directory": "/workspaces/modular-monolith-2",
                "dependencies": ["jane-orchestrator"]
            },

            # Domain services
            "security-service": {
                "service_name": "Security Domain Service",
                "domain": "security",
                "port": 8001,
                "health_check_url": "http://localhost:8001/health",
                "restart_command": "python -m uvicorn src.main:app --reload --port 8001",
                "working_directory": "/workspaces/modular-monolith-2/apps/security-service",
                "dependencies": ["postgres", "redis"]
            },
            "productivity-service": {
                "service_name": "Productivity Domain Service",
                "domain": "productivity",
                "port": 8002,
                "health_check_url": "http://localhost:8002/health",
                "restart_command": "python -m uvicorn src.main:app --reload --port 8002",
                "working_directory": "/workspaces/modular-monolith-2/apps/productivity-service",
                "dependencies": ["postgres", "redis"]
            },
            "mtg-service": {
                "service_name": "MTG Domain Service",
                "domain": "mtg",
                "port": 8003,
                "health_check_url": "http://localhost:8003/health",
                "restart_command": "python -m uvicorn src.main:app --reload --port 8003",
                "working_directory": "/workspaces/modular-monolith-2/apps/mtg-service",
                "dependencies": ["postgres", "redis"]
            },
            "infrastructure-service": {
                "service_name": "Infrastructure Domain Service",
                "domain": "infrastructure",
                "port": 8004,
                "health_check_url": "http://localhost:8004/health",
                "restart_command": "python -m uvicorn src.main:app --reload --port 8004",
                "working_directory": "/workspaces/modular-monolith-2/apps/infrastructure-service",
                "dependencies": ["postgres", "redis"]
            },

            # AI services
            "cyber-llm-server": {
                "service_name": "Cyber LLM Server",
                "domain": "ai",
                "port": 8010,
                "health_check_url": "http://localhost:8010/health",
                "restart_command": "python -m uvicorn src.main:app --reload --port 8010",
                "working_directory": "/workspaces/modular-monolith-2/apps/cyber-llm-server",
                "dependencies": ["postgres"]
            },
            "mtg-llm-server": {
                "service_name": "MTG LLM Server",
                "domain": "ai",
                "port": 8011,
                "health_check_url": "http://localhost:8011/health",
                "restart_command": "python -m uvicorn src.main:app --reload --port 8011",
                "working_directory": "/workspaces/modular-monolith-2/apps/mtg-llm-server",
                "dependencies": ["postgres"]
            },

            # Infrastructure services
            "postgres": {
                "service_name": "PostgreSQL Database",
                "domain": "database",
                "port": 5432,
                "health_check_url": None,
                "restart_command": "sudo systemctl restart postgresql",
                "working_directory": None,
                "dependencies": []
            },
            "redis": {
                "service_name": "Redis Cache",
                "domain": "cache",
                "port": 6379,
                "health_check_url": None,
                "restart_command": "sudo systemctl restart redis",
                "working_directory": None,
                "dependencies": []
            }
        }

        # Create ServiceInfo objects
        for service_id, config in default_services.items():
            service_info = ServiceInfo(
                service_id=service_id,
                service_name=config["service_name"],
                domain=config["domain"],
                port=config.get("port"),
                health_check_url=config.get("health_check_url"),
                dependencies=config.get("dependencies", []),
                restart_command=config.get("restart_command"),
                working_directory=config.get("working_directory")
            )
            self.services[service_id] = service_info

        logger.info(f"Loaded {len(self.services)} service configurations")

    def _build_dependency_graph(self) -> Dict[str, Set[str]]:
        """Build service dependency graph."""
        graph = {}

        for service_id, service in self.services.items():
            graph[service_id] = set(service.dependencies)

            # Build reverse dependencies (dependents)
            for dep in service.dependencies:
                if dep in self.services:
                    self.services[dep].dependents.append(service_id)

        return graph

    async def get_service_status(self, service_id: str) -> ServiceStatus:
        """Get current status of a service."""
        if service_id not in self.services:
            return ServiceStatus.UNKNOWN

        service = self.services[service_id]

        try:
            # Check if process is running by port
            if service.port:
                for conn in psutil.net_connections():
                    if conn.laddr.port == service.port and conn.status == 'LISTEN':
                        service.pid = conn.pid
                        service.status = ServiceStatus.RUNNING
                        return ServiceStatus.RUNNING

            # Check health endpoint if available
            if service.health_check_url:
                try:
                    import aiohttp
                    async with aiohttp.ClientSession() as session:
                        async with session.get(service.health_check_url, timeout=5) as resp:
                            if resp.status == 200:
                                service.status = ServiceStatus.RUNNING
                                return ServiceStatus.RUNNING
                except:
                    pass

            service.status = ServiceStatus.STOPPED
            return ServiceStatus.STOPPED

        except Exception as e:
            logger.error(f"Error checking status for {service_id}: {e}")
            service.status = ServiceStatus.UNKNOWN
            return ServiceStatus.UNKNOWN

    async def restart_service(self, service_id: str,
                              strategy: RestartStrategy = RestartStrategy.GRACEFUL) -> RestartOperation:
        """Restart a specific service."""
        operation_id = f"restart_{service_id}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"

        operation = RestartOperation(
            operation_id=operation_id,
            service_id=service_id,
            strategy=strategy,
            started_at=datetime.utcnow()
        )

        try:
            if service_id not in self.services:
                operation.status = ServiceStatus.FAILED
                operation.error_message = f"Service {service_id} not found"
                return operation

            service = self.services[service_id]

            # Pre-restart checks
            operation.pre_restart_checks.append("service_exists")

            # Get current status
            current_status = await self.get_service_status(service_id)
            operation.pre_restart_checks.append(
                f"current_status_{current_status.value}")

            # Stop service if running
            if current_status == ServiceStatus.RUNNING:
                await self._stop_service(service, strategy)
                operation.pre_restart_checks.append("service_stopped")

            # Wait a moment for cleanup
            await asyncio.sleep(2)

            # Start service
            await self._start_service(service)
            operation.post_restart_checks.append("service_started")

            # Verify service is running
            await asyncio.sleep(3)  # Give service time to start
            new_status = await self.get_service_status(service_id)

            if new_status == ServiceStatus.RUNNING:
                operation.status = ServiceStatus.RUNNING
                operation.post_restart_checks.append("health_check_passed")
            else:
                operation.status = ServiceStatus.FAILED
                operation.error_message = f"Service failed to start properly: {new_status.value}"

            operation.completed_at = datetime.utcnow()

        except Exception as e:
            operation.status = ServiceStatus.FAILED
            operation.error_message = str(e)
            operation.completed_at = datetime.utcnow()
            logger.error(f"Service restart failed for {service_id}: {e}")

        self.restart_history.append(operation)
        return operation

    async def _stop_service(self, service: ServiceInfo, strategy: RestartStrategy):
        """Stop a service gracefully or forcefully."""
        if service.pid:
            try:
                process = psutil.Process(service.pid)

                if strategy == RestartStrategy.GRACEFUL:
                    # Send SIGTERM for graceful shutdown
                    process.terminate()

                    # Wait up to 10 seconds for graceful shutdown
                    try:
                        process.wait(timeout=10)
                    except psutil.TimeoutExpired:
                        # Force kill if graceful shutdown failed
                        process.kill()

                elif strategy == RestartStrategy.IMMEDIATE:
                    # Force kill immediately
                    process.kill()

                logger.info(
                    f"Stopped service {service.service_id} (PID: {service.pid})")
                service.pid = None

            except psutil.NoSuchProcess:
                # Process already stopped
                service.pid = None
            except Exception as e:
                logger.error(
                    f"Error stopping service {service.service_id}: {e}")
                raise

    async def _start_service(self, service: ServiceInfo):
        """Start a service."""
        if not service.restart_command:
            raise ValueError(
                f"No restart command configured for {service.service_id}")

        try:
            # Set working directory and environment
            cwd = service.working_directory
            env = os.environ.copy()
            env.update(service.environment_vars)

            # Start the service
            process = subprocess.Popen(
                service.restart_command,
                shell=True,
                cwd=cwd,
                env=env,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )

            service.pid = process.pid
            logger.info(
                f"Started service {service.service_id} (PID: {service.pid})")

        except Exception as e:
            logger.error(f"Error starting service {service.service_id}: {e}")
            raise

    async def restart_domain(self, domain: str,
                             strategy: RestartStrategy = RestartStrategy.DEPENDENCY_AWARE) -> Dict[str, RestartOperation]:
        """Restart all services in a domain."""
        domain_services = [
            service_id for service_id, service in self.services.items()
            if service.domain == domain
        ]

        results = {}

        if strategy == RestartStrategy.DEPENDENCY_AWARE:
            # Restart in dependency order
            for service_id in self._get_restart_order(domain_services):
                results[service_id] = await self.restart_service(service_id, RestartStrategy.GRACEFUL)
        else:
            # Restart all services in parallel
            tasks = [
                self.restart_service(service_id, strategy)
                for service_id in domain_services
            ]
            restart_results = await asyncio.gather(*tasks)

            for service_id, result in zip(domain_services, restart_results):
                results[service_id] = result

        return results

    def _get_restart_order(self, service_ids: List[str]) -> List[str]:
        """Get optimal restart order considering dependencies."""
        # Simple topological sort for restart order
        ordered = []
        remaining = set(service_ids)

        while remaining:
            # Find services with no dependencies in remaining set
            ready = [
                sid for sid in remaining
                if not (set(self.services[sid].dependencies) & remaining)
            ]

            if not ready:
                # Circular dependency or external dependency
                ready = [remaining.pop()]

            for service_id in ready:
                ordered.append(service_id)
                remaining.discard(service_id)

        return ordered

    async def get_system_health(self) -> Dict[str, Any]:
        """Get overall system health status."""
        health_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "services": {},
            "domains": {},
            "overall_health": "healthy"
        }

        # Check all services
        failed_services = 0
        for service_id, service in self.services.items():
            status = await self.get_service_status(service_id)
            health_data["services"][service_id] = {
                "status": status.value,
                "name": service.service_name,
                "domain": service.domain,
                "port": service.port
            }

            if status in [ServiceStatus.FAILED, ServiceStatus.STOPPED]:
                failed_services += 1

        # Aggregate by domain
        domain_health = {}
        for service_id, service_data in health_data["services"].items():
            domain = service_data["domain"]
            if domain not in domain_health:
                domain_health[domain] = {
                    "running": 0, "total": 0, "services": []}

            domain_health[domain]["total"] += 1
            domain_health[domain]["services"].append(service_id)

            if service_data["status"] == "running":
                domain_health[domain]["running"] += 1

        # Calculate domain health percentages
        for domain, data in domain_health.items():
            data["health_percentage"] = (data["running"] / data["total"]) * 100

        health_data["domains"] = domain_health

        # Overall health
        total_services = len(self.services)
        if failed_services == 0:
            health_data["overall_health"] = "healthy"
        elif failed_services < total_services * 0.3:
            health_data["overall_health"] = "degraded"
        else:
            health_data["overall_health"] = "critical"

        return health_data

    def get_restart_history(self, service_id: str = None, limit: int = 50) -> List[RestartOperation]:
        """Get restart operation history."""
        history = self.restart_history

        if service_id:
            history = [op for op in history if op.service_id == service_id]

        return sorted(history, key=lambda op: op.started_at, reverse=True)[:limit]


# Global service restart manager
service_restart_manager = ServiceRestartManager()


# Convenience functions
async def restart_service(service_id: str, strategy: RestartStrategy = RestartStrategy.GRACEFUL) -> RestartOperation:
    """Restart a specific service."""
    return await service_restart_manager.restart_service(service_id, strategy)


async def restart_domain(domain: str, strategy: RestartStrategy = RestartStrategy.DEPENDENCY_AWARE) -> Dict[str, RestartOperation]:
    """Restart all services in a domain."""
    return await service_restart_manager.restart_domain(domain, strategy)


async def get_system_health() -> Dict[str, Any]:
    """Get overall system health."""
    return await service_restart_manager.get_system_health()


# Example usage
async def example_usage():
    """Example of how to use the service restart manager."""
    # Check system health
    health = await get_system_health()
    print(f"System health: {health['overall_health']}")

    # Restart a specific service
    result = await restart_service("jane-orchestrator", RestartStrategy.GRACEFUL)
    print(f"Restart result: {result.status.value}")

    # Restart entire security domain
    domain_results = await restart_domain("security", RestartStrategy.DEPENDENCY_AWARE)
    print(f"Domain restart completed: {len(domain_results)} services")


if __name__ == "__main__":
    asyncio.run(example_usage())
