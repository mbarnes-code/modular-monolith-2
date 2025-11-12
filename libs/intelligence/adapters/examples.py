"""
Example Integration Adapters

Shows how existing applications can integrate intelligence services
with minimal code changes and zero dependencies.
"""

from datetime import datetime
from typing import Any, Dict, List

from ..shared.interfaces import IntelligenceType
from .base import (ProductivityIntelligenceAdapter,
                   SecurityIntelligenceAdapter, intelligence_session,
                   with_intelligence)


# Example 1: CyberChef Integration
class CyberChefIntelligenceAdapter(SecurityIntelligenceAdapter):
    """Intelligence adapter for CyberChef operations"""

    def __init__(self):
        super().__init__("cyberchef")

    async def analyze_recipe(
        self,
        user_id: str,
        recipe_data: Dict[str, Any],
        input_data: str,
        output_data: str
    ) -> Dict[str, Any]:
        """
        Analyze CyberChef recipe for security insights

        Example usage in CyberChef:
        adapter = CyberChefIntelligenceAdapter()
        analysis = await adapter.analyze_recipe(
            user_id="user123",
            recipe_data={"operations": ["To Base64", "AES Decrypt"]},
            input_data=input_text,
            output_data=result_text
        )
        """
        activity = {
            'recipe': recipe_data,
            'input_data': input_data[:1000],  # Limit for analysis
            'output_data': output_data[:1000],
            'operation_type': 'data_transformation',
            'timestamp': datetime.now().isoformat()
        }

        # Check for potential security threats in input/output
        threat_assessment = await self.assess_threat(
            user_id=user_id,
            activity=activity
        )

        # Record activity for pattern analysis
        self.record_activity(user_id, activity)

        return {
            'recipe_analysis': {
                'complexity_score': len(recipe_data.get('operations', [])),
                'potential_automation': (
                    len(recipe_data.get('operations', [])) >= 3
                )
            },
            'security_analysis': threat_assessment,
            'suggestions': [
                'Save frequently used recipes as templates',
                'Consider automating multi-step operations',
                'Review input data for sensitive information'
            ] if not threat_assessment else [
                'Review this operation for security implications',
                'Verify data sources and destinations',
                'Consider additional security controls'
            ]
        }


# Example 2: Mealie Integration
class MealieIntelligenceAdapter(ProductivityIntelligenceAdapter):
    """Intelligence adapter for Mealie recipe management"""

    def __init__(self):
        super().__init__("mealie")

    async def analyze_cooking_patterns(
        self,
        user_id: str,
        recipe_usage: List[Dict[str, Any]],
        shopping_lists: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Analyze cooking patterns and meal planning efficiency

        Example usage in Mealie:
        adapter = MealieIntelligenceAdapter()
        insights = await adapter.analyze_cooking_patterns(
            user_id="user123",
            recipe_usage=[...],
            shopping_lists=[...]
        )
        """
        activity = {
            'recipe_count': len(recipe_usage),
            'shopping_list_count': len(shopping_lists),
            'activity_type': 'meal_planning',
            'timestamp': datetime.now().isoformat()
        }

        insights = await self.get_productivity_insights(
            user_id=user_id,
            workflow_data=activity
        )

        # Track productivity metrics
        await self.track_productivity_metrics(
            user_id=user_id,
            metrics={
                'recipes_used_this_week': len(recipe_usage),
                'meal_planning_efficiency': (
                    self._calculate_planning_efficiency(
                        recipe_usage, shopping_lists
                    )
                )
            }
        )

        return {
            'cooking_insights': insights,
            'recommendations': self._get_cooking_recommendations(
                recipe_usage, shopping_lists
            )
        }

    def _calculate_planning_efficiency(
        self,
        recipes: List[Dict[str, Any]],
        shopping_lists: List[Dict[str, Any]]
    ) -> float:
        """Calculate meal planning efficiency score"""
        if not recipes:
            return 0.0

        # Simple efficiency calculation based on recipe reuse
        unique_ingredients = set()
        total_ingredients = 0

        for recipe in recipes:
            ingredients = recipe.get('ingredients', [])
            total_ingredients += len(ingredients)
            unique_ingredients.update(ingredients)

        if total_ingredients == 0:
            return 0.0

        return len(unique_ingredients) / total_ingredients

    def _get_cooking_recommendations(
        self,
        recipes: List[Dict[str, Any]],
        shopping_lists: List[Dict[str, Any]]
    ) -> List[str]:
        """Generate cooking recommendations"""
        recommendations = []

        if len(recipes) > 10:
            recommendations.append("Consider meal prepping to save time")

        if len(shopping_lists) > 2:
            recommendations.append(
                "Consolidate shopping lists to reduce trips"
            )

        return recommendations or ["Keep tracking your cooking patterns!"]


# Example 3: n8n Workflow Integration
class N8nIntelligenceAdapter(ProductivityIntelligenceAdapter):
    """Intelligence adapter for n8n workflow automation"""

    def __init__(self):
        super().__init__("n8n")

    async def analyze_workflow_efficiency(
        self,
        user_id: str,
        workflow_data: Dict[str, Any],
        execution_history: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Analyze n8n workflow efficiency and suggest optimizations

        Example usage in n8n:
        adapter = N8nIntelligenceAdapter()
        analysis = await adapter.analyze_workflow_efficiency(
            user_id="user123",
            workflow_data=workflow,
            execution_history=recent_runs
        )
        """
        activity = {
            'workflow_id': workflow_data.get('id'),
            'node_count': len(workflow_data.get('nodes', [])),
            'execution_count': len(execution_history),
            'avg_execution_time': self._calculate_avg_execution_time(
                execution_history
            ),
            'success_rate': self._calculate_success_rate(execution_history),
            'activity_type': 'workflow_management'
        }

        insights = await self.get_productivity_insights(
            user_id=user_id,
            workflow_data=activity
        )

        return {
            'workflow_insights': insights,
            'optimization_suggestions': self._get_workflow_optimizations(
                workflow_data, execution_history
            ),
            'performance_metrics': {
                'efficiency_score': self._calculate_efficiency_score(activity),
                'automation_potential': activity['node_count'] >= 5
            }
        }

    def _calculate_avg_execution_time(
        self,
        executions: List[Dict[str, Any]]
    ) -> float:
        """Calculate average execution time"""
        if not executions:
            return 0.0

        times = [e.get('execution_time', 0) for e in executions]
        return sum(times) / len(times)

    def _calculate_success_rate(
        self,
        executions: List[Dict[str, Any]]
    ) -> float:
        """Calculate workflow success rate"""
        if not executions:
            return 0.0

        successes = sum(1 for e in executions if e.get('success', False))
        return successes / len(executions)

    def _calculate_efficiency_score(self, activity: Dict[str, Any]) -> float:
        """Calculate overall workflow efficiency score"""
        success_rate = activity.get('success_rate', 0)
        node_count = activity.get('node_count', 0)

        # Efficiency decreases with complexity, increases with success
        base_score = success_rate
        complexity_penalty = max(0, (node_count - 10) * 0.05)

        return max(0, base_score - complexity_penalty)

    def _get_workflow_optimizations(
        self,
        workflow: Dict[str, Any],
        executions: List[Dict[str, Any]]
    ) -> List[str]:
        """Generate workflow optimization suggestions"""
        suggestions = []

        node_count = len(workflow.get('nodes', []))
        if node_count > 15:
            suggestions.append(
                "Consider breaking complex workflow into smaller parts"
            )

        if executions:
            avg_time = self._calculate_avg_execution_time(executions)
            if avg_time > 300:  # 5 minutes
                suggestions.append("Optimize slow-running nodes")

        return suggestions or ["Workflow looks efficient!"]


# Example 4: Decorator-based Integration
@with_intelligence(
    SecurityIntelligenceAdapter("misp"),
    [IntelligenceType.SECURITY_ANALYSIS]
)
async def process_misp_event(user_id: str, event_data: Dict[str, Any]):
    """
    Example MISP event processing with intelligence analysis

    The decorator automatically adds security intelligence without
    changing the core function logic.
    """
    # Original MISP processing logic
    processed_event = {
        'event_id': event_data['id'],
        'threat_level': event_data.get('threat_level_id', 1),
        'processed_at': datetime.now().isoformat(),
        'indicators': event_data.get('attributes', [])
    }

    # Core business logic remains unchanged
    return processed_event
    # Intelligence insights automatically added to result


# Example 5: Session-based Integration
async def analyze_security_session_example(user_id: str):
    """
    Example of session-based intelligence tracking
    """
    adapter = SecurityIntelligenceAdapter("security-analysis")

    with intelligence_session(adapter, user_id, "threat_analysis"):
        # All activities in this session are tracked together

        # Analyze some suspicious files
        file_results = await analyze_suspicious_files(user_id, ["file1.exe"])

        # Check network connections
        network_results = await analyze_network_connections(
            user_id, ["192.168.1.100"]
        )

        # Generate threat report
        threat_report = compile_threat_report(file_results, network_results)

        return threat_report


async def analyze_suspicious_files(
    user_id: str, files: List[str]
) -> Dict[str, Any]:
    """Placeholder for file analysis"""
    return {'analyzed_files': files, 'threats_found': 0}


async def analyze_network_connections(
    user_id: str, ips: List[str]
) -> Dict[str, Any]:
    """Placeholder for network analysis"""
    return {'analyzed_ips': ips, 'suspicious_connections': 0}


def compile_threat_report(
    file_results: Dict[str, Any], network_results: Dict[str, Any]
) -> Dict[str, Any]:
    """Placeholder for report compilation"""
    return {
        'report_type': 'threat_analysis',
        'file_analysis': file_results,
        'network_analysis': network_results,
        'overall_threat_level': 'low'
    }
