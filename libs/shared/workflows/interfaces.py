"""
Workflow Orchestration Abstraction - Core Interfaces

Provides unified interface for workflow engines (n8n, Temporal, Dapr).
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Callable, Dict, List, Optional
from uuid import uuid4


class WorkflowStatus(Enum):
    """Workflow execution status"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    TIMEOUT = "timeout"


class ActivityStatus(Enum):
    """Activity execution status"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    RETRYING = "retrying"


@dataclass
class WorkflowDefinition:
    """
    Workflow definition containing activities and dependencies.

    Attributes:
        workflow_id: Unique workflow identifier
        name: Human-readable workflow name
        description: Workflow purpose description
        activities: List of activity definitions
        timeout_seconds: Maximum execution time
        retry_policy: Retry configuration
        metadata: Additional workflow metadata
    """
    workflow_id: str
    name: str
    description: str = ""
    activities: List[Dict[str, Any]] = field(default_factory=list)
    timeout_seconds: int = 300
    retry_policy: Optional[Dict[str, Any]] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class WorkflowExecution:
    """
    Workflow execution instance.

    Attributes:
        execution_id: Unique execution identifier
        workflow_id: Associated workflow definition ID
        status: Current execution status
        input_data: Workflow input parameters
        output_data: Workflow execution results
        started_at: Execution start time
        completed_at: Execution completion time
        error_message: Error details if failed
        activity_executions: List of activity execution records
    """
    execution_id: str = field(default_factory=lambda: str(uuid4()))
    workflow_id: str = ""
    status: WorkflowStatus = WorkflowStatus.PENDING
    input_data: Dict[str, Any] = field(default_factory=dict)
    output_data: Optional[Dict[str, Any]] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    error_message: Optional[str] = None
    activity_executions: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class ActivityDefinition:
    """
    Activity (task) definition within a workflow.

    Attributes:
        activity_id: Unique activity identifier
        name: Activity name
        handler: Function/service to execute
        input_mapping: Input parameter mapping
        output_mapping: Output result mapping
        retry_policy: Activity-specific retry configuration
        timeout_seconds: Activity execution timeout
        dependencies: List of prerequisite activity IDs
    """
    activity_id: str
    name: str
    handler: Any  # Function, service endpoint, or task name
    input_mapping: Dict[str, str] = field(default_factory=dict)
    output_mapping: Dict[str, str] = field(default_factory=dict)
    retry_policy: Optional[Dict[str, Any]] = None
    timeout_seconds: int = 60
    dependencies: List[str] = field(default_factory=list)


class IWorkflowEngine(ABC):
    """
    Abstract interface for workflow orchestration engines.

    Supports:
    - Workflow definition and registration
    - Workflow execution (sync/async)
    - Activity orchestration
    - State persistence
    - Error handling and retries
    """

    @abstractmethod
    async def start(self) -> None:
        """
        Initialize workflow engine connection.

        Raises:
            ConnectionError: If connection cannot be established
        """
        pass

    @abstractmethod
    async def stop(self) -> None:
        """Gracefully shutdown workflow engine"""
        pass

    @abstractmethod
    async def register_workflow(
        self,
        definition: WorkflowDefinition,
    ) -> str:
        """
        Register a workflow definition.

        Args:
            definition: Workflow definition to register

        Returns:
            Workflow ID

        Raises:
            WorkflowError: If registration fails
        """
        pass

    @abstractmethod
    async def execute_workflow(
        self,
        workflow_id: str,
        input_data: Dict[str, Any],
        wait_for_completion: bool = False,
        timeout_seconds: Optional[int] = None,
    ) -> WorkflowExecution:
        """
        Execute a workflow.

        Args:
            workflow_id: ID of workflow to execute
            input_data: Input parameters for workflow
            wait_for_completion: Block until workflow completes
            timeout_seconds: Override default workflow timeout

        Returns:
            Workflow execution instance

        Raises:
            WorkflowError: If execution fails to start
            TimeoutError: If execution exceeds timeout
        """
        pass

    @abstractmethod
    async def get_execution_status(
        self,
        execution_id: str,
    ) -> WorkflowExecution:
        """
        Get workflow execution status.

        Args:
            execution_id: Execution instance ID

        Returns:
            Current execution state
        """
        pass

    @abstractmethod
    async def cancel_execution(
        self,
        execution_id: str,
    ) -> None:
        """
        Cancel a running workflow execution.

        Args:
            execution_id: Execution instance ID
        """
        pass

    @abstractmethod
    async def list_executions(
        self,
        workflow_id: Optional[str] = None,
        status: Optional[WorkflowStatus] = None,
        limit: int = 100,
    ) -> List[WorkflowExecution]:
        """
        List workflow executions.

        Args:
            workflow_id: Filter by workflow ID
            status: Filter by execution status
            limit: Maximum number of results

        Returns:
            List of workflow executions
        """
        pass

    @abstractmethod
    async def register_activity(
        self,
        definition: ActivityDefinition,
    ) -> str:
        """
        Register an activity handler.

        Args:
            definition: Activity definition

        Returns:
            Activity ID
        """
        pass

    @abstractmethod
    async def health_check(self) -> bool:
        """
        Check workflow engine health.

        Returns:
            True if healthy, False otherwise
        """
        pass


class IWorkflowEngineFactory(ABC):
    """Factory interface for creating workflow engine instances"""

    @staticmethod
    @abstractmethod
    def create(
        engine_type: str,
        config: Dict[str, Any],
    ) -> IWorkflowEngine:
        """
        Create a workflow engine adapter instance.

        Args:
            engine_type: Type of engine (n8n, temporal, dapr)
            config: Engine-specific configuration

        Returns:
            Configured workflow engine instance

        Raises:
            ValueError: If engine_type is unknown
            ConfigurationError: If config is invalid
        """
        pass


class WorkflowError(Exception):
    """Base exception for workflow errors"""
    pass


class WorkflowExecutionError(WorkflowError):
    """Error during workflow execution"""
    pass


class ActivityError(WorkflowError):
    """Error during activity execution"""
    pass
