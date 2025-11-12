"""
WorkflowValidationService for testing generated workflows.

This service validates generated n8n workflows using historical data
and performance testing to ensure they work correctly.
"""

import asyncio
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List

from sqlalchemy.orm import Session

from ..data.models.adaptive_workflow import AdaptiveWorkflow
from ..data.models.user_request import UserRequest
from .base_service import BaseService


@dataclass
class ValidationResult:
    """Result of workflow validation."""
    is_valid: bool
    success_rate: float
    execution_time: float
    errors: List[str]
    warnings: List[str]
    test_count: int


class WorkflowValidationService(BaseService):
    """
    Service for validating generated n8n workflows.

    Tests workflows against historical data and validates
    their correctness before deployment.
    """

    def __init__(self, db_session: Session):
        super().__init__(db_session)
        self.min_test_scenarios = 5
        self.max_execution_time = 300  # 5 minutes
        self.min_success_rate = 0.85  # 85%

    async def validate_workflow(
        self,
        adaptive_workflow: AdaptiveWorkflow
    ) -> ValidationResult:
        """
        Comprehensive validation of a generated workflow.

        Args:
            adaptive_workflow: The workflow to validate

        Returns:
            ValidationResult with validation outcome
        """
        validation_result = ValidationResult(
            is_valid=False,
            success_rate=0.0,
            execution_time=0.0,
            errors=[],
            warnings=[],
            test_count=0
        )

        try:
            # Step 1: Static validation
            static_validation = self._validate_workflow_structure(
                adaptive_workflow.workflow_definition
            )
            validation_result.errors.extend(static_validation["errors"])
            validation_result.warnings.extend(static_validation["warnings"])

            if not static_validation["is_valid"]:
                return validation_result

            # Step 2: Generate test scenarios
            test_scenarios = await self._generate_test_scenarios(
                adaptive_workflow
            )

            if len(test_scenarios) < self.min_test_scenarios:
                validation_result.warnings.append(
                    f"Only {len(test_scenarios)} test scenarios generated "
                    f"(minimum {self.min_test_scenarios} recommended)"
                )

            # Step 3: Execute test scenarios
            test_results = await self._execute_test_scenarios(
                adaptive_workflow, test_scenarios
            )

            # Step 4: Analyze results
            validation_result = self._analyze_test_results(
                test_results, validation_result
            )

            # Step 5: Final validation
            validation_result.is_valid = self._determine_final_validity(
                validation_result
            )

            return validation_result

        except Exception as e:
            validation_result.errors.append(f"Validation failed: {str(e)}")
            return validation_result

    def _validate_workflow_structure(
        self,
        workflow_definition: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Validate the basic structure of the workflow."""
        result = {
            "is_valid": True,
            "errors": [],
            "warnings": []
        }

        # Check required fields
        required_fields = ["name", "nodes", "connections"]
        for field in required_fields:
            if field not in workflow_definition:
                result["errors"].append(f"Missing required field: {field}")
                result["is_valid"] = False

        nodes = workflow_definition.get("nodes", [])

        # Validate nodes
        if not nodes:
            result["errors"].append("Workflow must contain at least one node")
            result["is_valid"] = False
            return result

        # Check for trigger node
        trigger_types = [
            "n8n-nodes-base.scheduleTrigger",
            "n8n-nodes-base.manualTrigger",
            "n8n-nodes-base.webhook"
        ]

        has_trigger = any(
            node.get("type") in trigger_types for node in nodes
        )

        if not has_trigger:
            result["errors"].append("Workflow must have a trigger node")
            result["is_valid"] = False

        # Validate node structure
        for i, node in enumerate(nodes):
            node_errors = self._validate_node_structure(node, i)
            result["errors"].extend(node_errors)
            if node_errors:
                result["is_valid"] = False

        # Validate connections
        connections = workflow_definition.get("connections", {})
        connection_errors = self._validate_connections(nodes, connections)
        result["errors"].extend(connection_errors)
        if connection_errors:
            result["is_valid"] = False

        return result

    def _validate_node_structure(
        self,
        node: Dict[str, Any],
        index: int
    ) -> List[str]:
        """Validate individual node structure."""
        errors = []

        required_node_fields = ["id", "name", "type", "position"]
        for field in required_node_fields:
            if field not in node:
                errors.append(
                    f"Node {index}: Missing required field '{field}'")

        # Validate position
        position = node.get("position")
        if position and (
            not isinstance(position, list) or
            len(position) != 2 or
            not all(isinstance(x, (int, float)) for x in position)
        ):
            errors.append(f"Node {index}: Invalid position format")

        # Validate node type
        node_type = node.get("type")
        if node_type and not isinstance(node_type, str):
            errors.append(f"Node {index}: Invalid node type")

        return errors

    def _validate_connections(
        self,
        nodes: List[Dict[str, Any]],
        connections: Dict[str, Any]
    ) -> List[str]:
        """Validate workflow connections."""
        errors = []

        node_names = {node.get("name") for node in nodes}
        node_ids = {node.get("id") for node in nodes}

        for node_id, node_connections in connections.items():
            if node_id not in node_ids:
                errors.append(f"Connection from unknown node ID: {node_id}")
                continue

            if "main" in node_connections:
                for connection_list in node_connections["main"]:
                    if not isinstance(connection_list, list):
                        errors.append(
                            f"Invalid connection format for node {node_id}")
                        continue

                    for connection in connection_list:
                        target_node = connection.get("node")
                        if target_node not in node_names:
                            errors.append(
                                f"Connection to unknown node: {target_node}"
                            )

        return errors

    async def _generate_test_scenarios(
        self,
        adaptive_workflow: AdaptiveWorkflow
    ) -> List[Dict[str, Any]]:
        """Generate test scenarios from historical data."""
        # Get historical requests that match the pattern
        pattern_requests = self.db_session.query(UserRequest).filter(
            UserRequest.pattern_hash == adaptive_workflow.source_pattern_hash,
            UserRequest.execution_success.is_(True)
        ).limit(20).all()

        test_scenarios = []

        for request in pattern_requests:
            scenario = {
                "id": f"test_{request.id}",
                "name": f"Historical Request {request.request_id[:8]}",
                "input_data": {
                    "user_input": request.user_input,
                    "tools_used": request.tools_used,
                    "domain_context": request.domain_context,
                    "user_context": request.user_context
                },
                "expected_output": {
                    "tools_executed": request.tools_used,
                    "success": request.execution_success,
                    "actions_count": len(request.actions_taken or [])
                },
                "timeout": min(
                    (request.execution_duration or 30) * 2,
                    self.max_execution_time
                )
            }
            test_scenarios.append(scenario)

        # Add synthetic test scenarios if we don't have enough historical data
        if len(test_scenarios) < self.min_test_scenarios:
            synthetic_scenarios = self._generate_synthetic_scenarios(
                adaptive_workflow
            )
            test_scenarios.extend(synthetic_scenarios)

        return test_scenarios[:20]  # Limit to 20 scenarios

    def _generate_synthetic_scenarios(
        self,
        adaptive_workflow: AdaptiveWorkflow
    ) -> List[Dict[str, Any]]:
        """Generate synthetic test scenarios."""
        synthetic_scenarios = []

        # Generate basic scenarios based on workflow configuration
        tools = [
            node.get("name", "").replace(" Action", "")
            for node in adaptive_workflow.node_configuration
            if "Action" in node.get("name", "")
        ]

        for i in range(3):  # Generate 3 synthetic scenarios
            scenario = {
                "id": f"synthetic_{i}",
                "name": f"Synthetic Test {i + 1}",
                "input_data": {
                    "user_input": f"Execute workflow with tools: {', '.join(tools)}",
                    "tools_used": tools,
                    "domain_context": adaptive_workflow.category,
                    "user_context": {"test": True}
                },
                "expected_output": {
                    "tools_executed": tools,
                    "success": True,
                    "actions_count": len(tools)
                },
                "timeout": 60
            }
            synthetic_scenarios.append(scenario)

        return synthetic_scenarios

    async def _execute_test_scenarios(
        self,
        adaptive_workflow: AdaptiveWorkflow,
        test_scenarios: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Execute test scenarios against the workflow."""
        test_results = []

        for scenario in test_scenarios:
            result = await self._execute_single_test(
                adaptive_workflow, scenario
            )
            test_results.append(result)

        return test_results

    async def _execute_single_test(
        self,
        adaptive_workflow: AdaptiveWorkflow,
        scenario: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute a single test scenario."""
        start_time = datetime.utcnow()

        try:
            # Simulate workflow execution
            # In a real implementation, this would call the n8n API
            execution_result = await self._simulate_workflow_execution(
                adaptive_workflow, scenario
            )

            end_time = datetime.utcnow()
            execution_time = (end_time - start_time).total_seconds()

            # Compare with expected output
            success = self._compare_results(
                execution_result, scenario["expected_output"]
            )

            return {
                "scenario_id": scenario["id"],
                "success": success,
                "execution_time": execution_time,
                "result": execution_result,
                "error": None
            }

        except Exception as e:
            end_time = datetime.utcnow()
            execution_time = (end_time - start_time).total_seconds()

            return {
                "scenario_id": scenario["id"],
                "success": False,
                "execution_time": execution_time,
                "result": None,
                "error": str(e)
            }

    async def _simulate_workflow_execution(
        self,
        adaptive_workflow: AdaptiveWorkflow,
        scenario: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Simulate workflow execution for testing."""
        # This is a simplified simulation
        # In production, this would integrate with actual n8n execution

        await asyncio.sleep(0.1)  # Simulate processing time

        tools_used = scenario["input_data"].get("tools_used", [])

        return {
            "tools_executed": tools_used,
            "success": True,
            "actions_count": len(tools_used),
            "execution_data": {
                "workflow_id": adaptive_workflow.workflow_id,
                "timestamp": datetime.utcnow().isoformat()
            }
        }

    def _compare_results(
        self,
        actual: Dict[str, Any],
        expected: Dict[str, Any]
    ) -> bool:
        """Compare actual results with expected results."""
        # Check success status
        if actual.get("success") != expected.get("success"):
            return False

        # Check tools executed
        actual_tools = set(actual.get("tools_executed", []))
        expected_tools = set(expected.get("tools_executed", []))

        if actual_tools != expected_tools:
            return False

        # Check action count (allow some variance)
        actual_actions = actual.get("actions_count", 0)
        expected_actions = expected.get("actions_count", 0)

        if abs(actual_actions - expected_actions) > 2:
            return False

        return True

    def _analyze_test_results(
        self,
        test_results: List[Dict[str, Any]],
        validation_result: ValidationResult
    ) -> ValidationResult:
        """Analyze test execution results."""
        if not test_results:
            validation_result.errors.append("No test results to analyze")
            return validation_result

        # Calculate metrics
        successful_tests = sum(1 for r in test_results if r["success"])
        validation_result.test_count = len(test_results)
        validation_result.success_rate = successful_tests / len(test_results)

        # Calculate average execution time
        execution_times = [r["execution_time"] for r in test_results]
        validation_result.execution_time = sum(
            execution_times) / len(execution_times)

        # Analyze failures
        failed_tests = [r for r in test_results if not r["success"]]
        for failed_test in failed_tests:
            error_msg = failed_test.get("error", "Unknown error")
            validation_result.errors.append(
                f"Test {failed_test['scenario_id']} failed: {error_msg}"
            )

        # Performance warnings
        if validation_result.execution_time > 60:
            validation_result.warnings.append(
                f"Average execution time ({validation_result.execution_time:.1f}s) "
                "is longer than recommended (60s)"
            )

        return validation_result

    def _determine_final_validity(
        self,
        validation_result: ValidationResult
    ) -> bool:
        """Determine if workflow is valid based on all criteria."""
        # Must have no critical errors
        if validation_result.errors:
            return False

        # Must meet minimum success rate
        if validation_result.success_rate < self.min_success_rate:
            return False

        # Must have been tested
        if validation_result.test_count == 0:
            return False

        # Must not exceed maximum execution time
        if validation_result.execution_time > self.max_execution_time:
            return False

        return True

    def get_validation_report(
        self,
        validation_result: ValidationResult
    ) -> Dict[str, Any]:
        """Generate a comprehensive validation report."""
        return {
            "is_valid": validation_result.is_valid,
            "summary": {
                "success_rate": f"{validation_result.success_rate:.1%}",
                "test_count": validation_result.test_count,
                "average_execution_time": f"{validation_result.execution_time:.2f}s",
                "error_count": len(validation_result.errors),
                "warning_count": len(validation_result.warnings)
            },
            "criteria": {
                "min_success_rate": f"{self.min_success_rate:.1%}",
                "max_execution_time": f"{self.max_execution_time}s",
                "min_test_scenarios": self.min_test_scenarios
            },
            "errors": validation_result.errors,
            "warnings": validation_result.warnings,
            "recommendation": (
                "Workflow is ready for deployment" if validation_result.is_valid
                else "Workflow needs improvements before deployment"
            )
        }
