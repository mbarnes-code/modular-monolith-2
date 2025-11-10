"""n8n Workflow API Integration for Automatic Workflow Creation."""

from typing import List, Dict, Any, Optional
from datetime import datetime
import httpx
from dataclasses import dataclass
from enum import Enum


class WorkflowStatus(Enum):
    """Status of n8n workflows."""
    ACTIVE = "active"
    INACTIVE = "inactive"
    ERROR = "error"
    TESTING = "testing"


@dataclass
class N8nWorkflow:
    """Represents an n8n workflow with full metadata."""
    id: Optional[str]
    name: str
    active: bool
    nodes: List[Dict[str, Any]]
    connections: Dict[str, Any]
    settings: Dict[str, Any]
    static_data: Optional[Dict[str, Any]] = None
    tags: List[str] = None
    version_id: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


@dataclass
class N8nWorkflowExecution:
    """Represents an n8n workflow execution."""
    id: str
    workflow_id: str
    status: str
    started_at: datetime
    finished_at: Optional[datetime]
    mode: str
    data: Dict[str, Any]


class N8nAPIError(Exception):
    """Custom exception for n8n API errors."""
    
    def __init__(self, message: str, status_code: Optional[int] = None,
                 response_data: Optional[Dict[str, Any]] = None):
        self.message = message
        self.status_code = status_code
        self.response_data = response_data
        super().__init__(self.message)


class N8nAPIClient:
    """Client for interacting with n8n REST API."""
    
    def __init__(self, base_url: str, api_key: Optional[str] = None):
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.session = None
        self._auth_headers = {}
        
        if api_key:
            self._auth_headers['X-N8N-API-KEY'] = api_key
    
    async def __aenter__(self):
        """Async context manager entry."""
        self.session = httpx.AsyncClient(
            timeout=httpx.Timeout(30.0),
            headers=self._auth_headers
        )
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        if self.session:
            await self.session.aclose()
    
    async def create_workflow(self, workflow: N8nWorkflow) -> N8nWorkflow:
        """Create a new workflow in n8n."""
        workflow_data = {
            "name": workflow.name,
            "active": workflow.active,
            "nodes": workflow.nodes,
            "connections": workflow.connections,
            "settings": workflow.settings,
            "staticData": workflow.static_data,
            "tags": workflow.tags or []
        }
        
        try:
            response = await self.session.post(
                f"{self.base_url}/api/v1/workflows",
                json=workflow_data
            )
            response.raise_for_status()
            
            result = response.json()
            return self._parse_workflow_response(result)
            
        except httpx.HTTPStatusError as e:
            raise N8nAPIError(
                f"Failed to create workflow: {e.response.text}",
                e.response.status_code
            )
    
    async def get_workflow(self, workflow_id: str) -> N8nWorkflow:
        """Get a workflow by ID."""
        try:
            response = await self.session.get(
                f"{self.base_url}/api/v1/workflows/{workflow_id}"
            )
            response.raise_for_status()
            
            result = response.json()
            return self._parse_workflow_response(result)
            
        except httpx.HTTPStatusError as e:
            raise N8nAPIError(
                f"Failed to get workflow: {e.response.text}",
                e.response.status_code
            )
    
    async def list_workflows(self) -> List[N8nWorkflow]:
        """List all workflows."""
        try:
            response = await self.session.get(
                f"{self.base_url}/api/v1/workflows"
            )
            response.raise_for_status()
            
            result = response.json()
            return [self._parse_workflow_response(wf) for wf in result['data']]
            
        except httpx.HTTPStatusError as e:
            raise N8nAPIError(
                f"Failed to list workflows: {e.response.text}",
                e.response.status_code
            )
    
    async def activate_workflow(self, workflow_id: str) -> N8nWorkflow:
        """Activate a workflow."""
        try:
            response = await self.session.patch(
                f"{self.base_url}/api/v1/workflows/{workflow_id}",
                json={"active": True}
            )
            response.raise_for_status()
            
            result = response.json()
            return self._parse_workflow_response(result)
            
        except httpx.HTTPStatusError as e:
            raise N8nAPIError(
                f"Failed to activate workflow: {e.response.text}",
                e.response.status_code
            )
    
    async def deactivate_workflow(self, workflow_id: str) -> N8nWorkflow:
        """Deactivate a workflow."""
        try:
            response = await self.session.patch(
                f"{self.base_url}/api/v1/workflows/{workflow_id}",
                json={"active": False}
            )
            response.raise_for_status()
            
            result = response.json()
            return self._parse_workflow_response(result)
            
        except httpx.HTTPStatusError as e:
            raise N8nAPIError(
                f"Failed to deactivate workflow: {e.response.text}",
                e.response.status_code
            )
    
    async def delete_workflow(self, workflow_id: str) -> bool:
        """Delete a workflow by ID."""
        try:
            response = await self.session.delete(
                f"{self.base_url}/api/v1/workflows/{workflow_id}"
            )
            response.raise_for_status()
            return True
            
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                return False
            raise N8nAPIError(
                f"Failed to delete workflow: {e.response.text}",
                e.response.status_code
            )
    
    async def execute_workflow(self, workflow_id: str) -> str:
        """Execute a workflow manually and return execution ID."""
        try:
            response = await self.session.post(
                f"{self.base_url}/api/v1/workflows/{workflow_id}/execute"
            )
            response.raise_for_status()
            
            result = response.json()
            return result['data']['executionId']
            
        except httpx.HTTPStatusError as e:
            raise N8nAPIError(
                f"Failed to execute workflow: {e.response.text}",
                e.response.status_code
            )
    
    async def test_workflow(self, workflow: N8nWorkflow) -> Dict[str, Any]:
        """Test a workflow without saving it."""
        workflow_data = {
            "workflowData": {
                "name": workflow.name,
                "nodes": workflow.nodes,
                "connections": workflow.connections,
                "settings": workflow.settings
            }
        }
        
        try:
            response = await self.session.post(
                f"{self.base_url}/api/v1/workflows/test",
                json=workflow_data
            )
            response.raise_for_status()
            
            return response.json()
            
        except httpx.HTTPStatusError as e:
            raise N8nAPIError(
                f"Failed to test workflow: {e.response.text}",
                e.response.status_code
            )
    
    def _parse_workflow_response(self, data: Dict[str, Any]) -> N8nWorkflow:
        """Parse n8n API workflow response into N8nWorkflow object."""
        return N8nWorkflow(
            id=data.get('id'),
            name=data['name'],
            active=data.get('active', False),
            nodes=data.get('nodes', []),
            connections=data.get('connections', {}),
            settings=data.get('settings', {}),
            static_data=data.get('staticData'),
            tags=data.get('tags', []),
            version_id=data.get('versionId'),
            created_at=self._parse_datetime(data.get('createdAt')),
            updated_at=self._parse_datetime(data.get('updatedAt'))
        )
    
    def _parse_datetime(self, date_str: Optional[str]) -> Optional[datetime]:
        """Parse ISO datetime string."""
        if not date_str:
            return None
        try:
            return datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        except (ValueError, AttributeError):
            return None


class WorkflowDeploymentManager:
    """Manages deployment of generated workflows to n8n."""
    
    def __init__(self, n8n_client: N8nAPIClient):
        self.n8n_client = n8n_client
        self.deployment_history = []
    
    async def deploy_workflow(
        self, generated_workflow: Any, test_first: bool = True
    ) -> Dict[str, Any]:
        """Deploy a generated workflow to n8n with optional testing."""
        deployment_result = {
            "workflow_id": None,
            "status": "failed",
            "test_results": None,
            "errors": [],
            "deployed_at": datetime.utcnow()
        }
        
        try:
            # Convert generated workflow to n8n format
            n8n_workflow = self._convert_to_n8n_workflow(generated_workflow)
            
            # Test workflow first if requested
            if test_first:
                test_results = await self.n8n_client.test_workflow(n8n_workflow)
                deployment_result["test_results"] = test_results
                
                if self._has_test_errors(test_results):
                    deployment_result["errors"].append("Workflow test failed")
                    deployment_result["status"] = "test_failed"
                    return deployment_result
            
            # Deploy the workflow
            deployed_workflow = await self.n8n_client.create_workflow(
                n8n_workflow
            )
            deployment_result["workflow_id"] = deployed_workflow.id
            deployment_result["status"] = "deployed"
            
            # Record deployment
            self.deployment_history.append({
                "pattern_id": getattr(generated_workflow, 'pattern_id', None),
                "workflow_id": deployed_workflow.id,
                "deployed_at": deployment_result["deployed_at"],
                "status": "success"
            })
            
        except N8nAPIError as e:
            deployment_result["errors"].append(f"n8n API error: {e.message}")
        except Exception as e:
            deployment_result["errors"].append(f"Deployment error: {str(e)}")
        
        return deployment_result
    
    def _convert_to_n8n_workflow(self, generated_workflow: Any) -> N8nWorkflow:
        """Convert a generated workflow to n8n format."""
        return N8nWorkflow(
            id=None,  # Will be assigned by n8n
            name=generated_workflow.name,
            active=False,  # Start inactive for safety
            nodes=generated_workflow.nodes,
            connections=generated_workflow.connections,
            settings=getattr(generated_workflow, 'settings', {
                "executionOrder": "v1"
            }),
            tags=["auto-generated", "pattern-based"]
        )
    
    def _has_test_errors(self, test_results: Dict[str, Any]) -> bool:
        """Check if test results contain errors."""
        if not test_results:
            return True
        
        # Check for execution errors
        if test_results.get('status') == 'error':
            return True
        
        # Check for node errors
        data = test_results.get('data', {})
        if isinstance(data, dict):
            for node_data in data.values():
                if isinstance(node_data, list):
                    for execution in node_data:
                        if execution.get('error'):
                            return True
        
        return False
    
    async def get_deployment_status(self, pattern_id: str) -> Dict[str, Any]:
        """Get deployment status for a specific pattern."""
        deployments = [
            d for d in self.deployment_history
            if d.get("pattern_id") == pattern_id
        ]
        
        if not deployments:
            return {"status": "not_deployed", "deployments": []}
        
        latest_deployment = max(deployments, key=lambda x: x["deployed_at"])
        
        # Check current status in n8n
        try:
            workflow = await self.n8n_client.get_workflow(
                latest_deployment["workflow_id"]
            )
            current_status = "active" if workflow.active else "inactive"
        except N8nAPIError:
            current_status = "not_found"
        
        return {
            "status": current_status,
            "latest_deployment": latest_deployment,
            "total_deployments": len(deployments),
            "deployments": deployments
        }