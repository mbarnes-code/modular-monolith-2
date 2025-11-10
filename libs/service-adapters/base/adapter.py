"""
Base Service Adapter Framework

Foundation for integrating all 37 mental prosthetic tools with unified
interface, business logic preservation, and executive function support.
"""

import asyncio
import logging
from abc import ABC, abstractmethod
from contextlib import asynccontextmanager
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, Generic, List, Optional, TypeVar

# Type definitions
T = TypeVar('T')
ConfigType = Dict[str, Any]
ResponseType = Dict[str, Any]


class ToolDomain(Enum):
    """Domain classification for the 37 mental prosthetic tools"""
    SECURITY = "security"  # 13 tools
    PRODUCTIVITY = "productivity"  # 8 tools
    MTG = "mtg"  # 4 tools
    INFRASTRUCTURE = "infrastructure"  # 12 tools


class AdaptationStrategy(Enum):
    """Business logic preservation strategies per consolidated analysis"""
    MICROSERVICE = "microservice"  # Category A: Complex algorithms
    MODULAR_INTEGRATION = "modular"  # Category B: Domain logic
    UTILITY_WRAPPER = "utility"  # Category C: Simple utilities


class ExecutiveFunctionLevel(Enum):
    """Executive function accommodation levels"""
    MINIMAL = "minimal"  # Basic functionality
    MODERATE = "moderate"  # Standard accommodations
    COMPREHENSIVE = "comprehensive"  # Full ADHD/autism support


@dataclass
class ToolMetadata:
    """Metadata for each of the 37 tools"""
    tool_id: str
    tool_name: str
    domain: ToolDomain
    version: str
    adaptation_strategy: AdaptationStrategy
    original_framework: str  # e.g., "flask", "fastapi", "node.js", "php"
    database_type: str       # e.g., "postgresql", "sqlite", "mysql"
    port: Optional[int] = None
    config_files: List[str] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)
    executive_function_level: ExecutiveFunctionLevel = ExecutiveFunctionLevel.MODERATE
    performance_target_ms: int = 2000  # Default 2s, varies by domain
    business_logic_preserved: bool = True
    migration_completed: bool = False


@dataclass
class AdapterResponse:
    """Standardized response format for all adapters"""
    success: bool
    data: Any = None
    error: Optional[str] = None
    execution_time_ms: int = 0
    tool_id: str = ""
    accommodations_applied: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)


@dataclass
class ExecutiveFunctionContext:
    """Context for executive function accommodations"""
    user_id: str
    adhd_mode_enabled: bool = False
    focus_assist_enabled: bool = True
    context_switching_warning: bool = True
    ui_response_threshold_ms: int = 200
    session_id: Optional[str] = None
    cognitive_load_score: int = 30  # 0-100
    current_tool: Optional[str] = None
    active_workflows: List[str] = field(default_factory=list)


class BaseServiceAdapter(ABC, Generic[T]):
    """
    Abstract base class for all 37 mental prosthetic tool adapters

    Provides unified interface while preserving business logic from each tool.
    Implements executive function accommodations and performance monitoring.
    """

    def __init__(self,
                 metadata: ToolMetadata,
                 config: ConfigType,
                 logger: Optional[logging.Logger] = None):
        self.metadata = metadata
        self.config = config
        self.logger = logger or logging.getLogger(
            f"adapter.{metadata.tool_id}")
        self._is_initialized = False
        self._startup_time = datetime.utcnow()
        self._request_count = 0
        self._error_count = 0

        # Executive function support
        self._response_times: List[int] = []
        self._max_response_history = 100

    @property
    def tool_id(self) -> str:
        return self.metadata.tool_id

    @property
    def tool_name(self) -> str:
        return self.metadata.tool_name

    @property
    def domain(self) -> ToolDomain:
        return self.metadata.domain

    @property
    def is_initialized(self) -> bool:
        return self._is_initialized

    @property
    def average_response_time_ms(self) -> float:
        if not self._response_times:
            return 0.0
        return sum(self._response_times) / len(self._response_times)

    @abstractmethod
    async def initialize(self) -> bool:
        """
        Initialize the adapter and underlying tool
        Must preserve all original business logic
        """
        pass

    @abstractmethod
    async def health_check(self) -> AdapterResponse:
        """Check if the adapted tool is healthy and responsive"""
        pass

    @abstractmethod
    async def get_capabilities(self) -> List[str]:
        """Return list of capabilities this tool provides"""
        pass

    @abstractmethod
    async def execute_operation(self,
                                operation: str,
                                params: Dict[str, Any],
                                context: ExecutiveFunctionContext) -> AdapterResponse:
        """
        Execute a tool operation with executive function support
        Must preserve original business logic while adding accommodations
        """
        pass

    async def initialize_with_accommodation(self,
                                            context: ExecutiveFunctionContext) -> AdapterResponse:
        """Initialize with executive function accommodations"""
        start_time = datetime.utcnow()

        try:
            # Apply pre-initialization accommodations
            accommodations_applied = []

            if context.adhd_mode_enabled:
                # Reduce startup distractions
                self.logger.setLevel(logging.WARNING)  # Reduce log noise
                accommodations_applied.append("reduced_startup_logging")

            if context.focus_assist_enabled:
                # Prioritize essential initialization only
                accommodations_applied.append("essential_init_only")

            # Execute initialization
            success = await self.initialize()
            self._is_initialized = success

            execution_time = int(
                (datetime.utcnow() - start_time).total_seconds() * 1000)

            # Check performance target
            warnings = []
            if execution_time > self.metadata.performance_target_ms:
                warnings.append(
                    f"Initialization exceeded target ({execution_time}ms > {self.metadata.performance_target_ms}ms)")

            return AdapterResponse(
                success=success,
                execution_time_ms=execution_time,
                tool_id=self.tool_id,
                accommodations_applied=accommodations_applied,
                warnings=warnings
            )

        except Exception as e:
            execution_time = int(
                (datetime.utcnow() - start_time).total_seconds() * 1000)
            self.logger.error(f"Initialization failed for {self.tool_id}: {e}")

            return AdapterResponse(
                success=False,
                error=str(e),
                execution_time_ms=execution_time,
                tool_id=self.tool_id
            )

    async def execute_with_accommodation(self,
                                         operation: str,
                                         params: Dict[str, Any],
                                         context: ExecutiveFunctionContext) -> AdapterResponse:
        """Execute operation with full executive function support"""
        start_time = datetime.utcnow()
        self._request_count += 1

        try:
            # Pre-execution accommodations
            accommodations_applied = []
            modified_params = params.copy()

            # ADHD accommodations
            if context.adhd_mode_enabled:
                # Reduce cognitive load
                if 'limit' not in modified_params and 'page_size' not in modified_params:
                    modified_params['limit'] = 20  # Smaller result sets
                    accommodations_applied.append("reduced_result_set")

                # Add progress indicators for long operations
                if operation in self._get_long_running_operations():
                    modified_params['progress_callback'] = True
                    accommodations_applied.append("progress_indicators")

            # Focus assist accommodations
            if context.focus_assist_enabled:
                # Prioritize essential data only
                if 'fields' not in modified_params:
                    modified_params['fields'] = self._get_essential_fields(
                        operation)
                    accommodations_applied.append("essential_fields_only")

            # Context switching warning
            if context.context_switching_warning and context.current_tool != self.tool_id:
                accommodations_applied.append("context_switch_detected")

            # Execute the operation
            response = await self.execute_operation(operation, modified_params, context)

            # Post-execution processing
            execution_time = int(
                (datetime.utcnow() - start_time).total_seconds() * 1000)
            self._record_response_time(execution_time)

            # Performance validation
            warnings = response.warnings or []

            # Domain-specific performance targets
            domain_targets = {
                ToolDomain.SECURITY: 1000,      # <1s for threat analysis
                ToolDomain.PRODUCTIVITY: 2000,  # <2s for task management
                ToolDomain.MTG: 3000,          # <3s for game analysis
                ToolDomain.INFRASTRUCTURE: 5000  # <5s for system operations
            }

            target_ms = domain_targets.get(self.domain, 2000)
            if execution_time > target_ms:
                warnings.append(
                    f"Response time exceeded domain target ({execution_time}ms > {target_ms}ms)")

            # UI responsiveness check
            if execution_time > context.ui_response_threshold_ms:
                warnings.append(
                    f"UI responsiveness threshold exceeded ({execution_time}ms > {context.ui_response_threshold_ms}ms)")

            # Update response with accommodation info
            response.execution_time_ms = execution_time
            response.accommodations_applied.extend(accommodations_applied)
            response.warnings = warnings

            return response

        except Exception as e:
            self._error_count += 1
            execution_time = int(
                (datetime.utcnow() - start_time).total_seconds() * 1000)

            self.logger.error(
                f"Operation {operation} failed for {self.tool_id}: {e}")

            return AdapterResponse(
                success=False,
                error=f"Executive function accommodated error: {str(e)}",
                execution_time_ms=execution_time,
                tool_id=self.tool_id
            )

    def _record_response_time(self, time_ms: int) -> None:
        """Record response time for performance monitoring"""
        self._response_times.append(time_ms)
        if len(self._response_times) > self._max_response_history:
            self._response_times.pop(0)

    def _get_long_running_operations(self) -> List[str]:
        """Get list of operations that typically take longer to execute"""
        # Override in subclasses for tool-specific long operations
        return ['search', 'analyze', 'generate', 'process', 'scan']

    def _get_essential_fields(self, operation: str) -> List[str]:
        """Get essential fields for focus assist mode"""
        # Override in subclasses for tool-specific essential fields
        return ['id', 'name', 'status', 'created_at']

    async def get_metrics(self) -> Dict[str, Any]:
        """Get adapter performance and usage metrics"""
        uptime_seconds = (datetime.utcnow() -
                          self._startup_time).total_seconds()

        return {
            'tool_id': self.tool_id,
            'tool_name': self.tool_name,
            'domain': self.domain.value,
            'is_initialized': self._is_initialized,
            'uptime_seconds': uptime_seconds,
            'request_count': self._request_count,
            'error_count': self._error_count,
            'error_rate': self._error_count / max(self._request_count, 1),
            'average_response_time_ms': self.average_response_time_ms,
            'business_logic_preserved': self.metadata.business_logic_preserved,
            'migration_completed': self.metadata.migration_completed,
            'performance_target_ms': self.metadata.performance_target_ms
        }

    @asynccontextmanager
    async def managed_operation(self, operation_name: str):
        """Context manager for operation lifecycle management"""
        self.logger.debug(f"Starting operation: {operation_name}")
        start_time = datetime.utcnow()

        try:
            yield
        except Exception as e:
            self.logger.error(f"Operation {operation_name} failed: {e}")
            raise
        finally:
            duration = (datetime.utcnow() - start_time).total_seconds()
            self.logger.debug(
                f"Operation {operation_name} completed in {duration:.3f}s")


class AdapterRegistry:
    """Registry for managing all 37 mental prosthetic tool adapters"""

    def __init__(self):
        self._adapters: Dict[str, BaseServiceAdapter] = {}
        self._adapters_by_domain: Dict[ToolDomain, List[BaseServiceAdapter]] = {
            domain: [] for domain in ToolDomain
        }
        self.logger = logging.getLogger("adapter_registry")

    def register_adapter(self, adapter: BaseServiceAdapter) -> None:
        """Register a tool adapter"""
        tool_id = adapter.tool_id

        if tool_id in self._adapters:
            self.logger.warning(
                f"Adapter {tool_id} already registered, replacing")

        self._adapters[tool_id] = adapter
        self._adapters_by_domain[adapter.domain].append(adapter)

        self.logger.info(
            f"Registered adapter: {tool_id} ({adapter.domain.value})")

    def get_adapter(self, tool_id: str) -> Optional[BaseServiceAdapter]:
        """Get adapter by tool ID"""
        return self._adapters.get(tool_id)

    def get_adapters_by_domain(self, domain: ToolDomain) -> List[BaseServiceAdapter]:
        """Get all adapters for a specific domain"""
        return self._adapters_by_domain.get(domain, [])

    def get_all_adapters(self) -> List[BaseServiceAdapter]:
        """Get all registered adapters"""
        return list(self._adapters.values())

    async def initialize_all(self, context: ExecutiveFunctionContext) -> Dict[str, AdapterResponse]:
        """Initialize all registered adapters with executive function support"""
        results = {}

        # Initialize by domain priority (Security first for threat response)
        domain_priority = [
            ToolDomain.SECURITY,
            ToolDomain.PRODUCTIVITY,
            ToolDomain.INFRASTRUCTURE,
            ToolDomain.MTG
        ]

        for domain in domain_priority:
            adapters = self.get_adapters_by_domain(domain)
            self.logger.info(
                f"Initializing {len(adapters)} {domain.value} adapters")

            # Initialize domain adapters in parallel
            domain_tasks = [
                adapter.initialize_with_accommodation(context)
                for adapter in adapters
            ]

            domain_results = await asyncio.gather(*domain_tasks, return_exceptions=True)

            for adapter, result in zip(adapters, domain_results):
                if isinstance(result, Exception):
                    results[adapter.tool_id] = AdapterResponse(
                        success=False,
                        error=str(result),
                        tool_id=adapter.tool_id
                    )
                else:
                    results[adapter.tool_id] = result

        # Log initialization summary
        successful = sum(1 for r in results.values() if r.success)
        total = len(results)
        self.logger.info(
            f"Adapter initialization complete: {successful}/{total} successful")

        return results

    async def health_check_all(self) -> Dict[str, AdapterResponse]:
        """Health check all adapters"""
        tasks = [
            adapter.health_check()
            for adapter in self._adapters.values()
        ]

        results = await asyncio.gather(*tasks, return_exceptions=True)

        health_status = {}
        for adapter, result in zip(self._adapters.values(), results):
            if isinstance(result, Exception):
                health_status[adapter.tool_id] = AdapterResponse(
                    success=False,
                    error=str(result),
                    tool_id=adapter.tool_id
                )
            else:
                health_status[adapter.tool_id] = result

        return health_status

    def get_registry_metrics(self) -> Dict[str, Any]:
        """Get overall registry metrics"""
        total_adapters = len(self._adapters)
        initialized_adapters = sum(
            1 for a in self._adapters.values() if a.is_initialized)

        domain_counts = {
            domain.value: len(adapters)
            for domain, adapters in self._adapters_by_domain.items()
        }

        return {
            'total_adapters': total_adapters,
            'initialized_adapters': initialized_adapters,
            'initialization_rate': initialized_adapters / max(total_adapters, 1),
            'domain_distribution': domain_counts,
            'target_tool_count': 37,  # Constitutional requirement
            'migration_progress': initialized_adapters / 37
        }


# Global registry instance
adapter_registry = AdapterRegistry()
