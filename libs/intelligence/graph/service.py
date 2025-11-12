"""
Graph Analysis Intelligence Service

Enhanced graph analysis capabilities based on real business logic patterns from:
- HELK: Attack path analysis and threat correlation
- Commander Spellbook: Combo dependency graphs and rule validation
- Actual Budget: Dependency graph processing for calculations
- Kong: Request routing and service dependency mapping
- n8n: Workflow dependency analysis and execution optimization

Provides optional graph intelligence that applications can use for:
- Attack path detection and security analysis
- Dependency resolution and cycle detection  
- Relationship mapping and traversal optimization
- Multi-source correlation and pattern analysis
"""

import json
from collections import defaultdict, deque
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List

from ..shared.interfaces import (ConfidenceLevel, IntelligenceInsight,
                                 IntelligenceRequest,
                                 IntelligenceServiceInterface)
from ..shared.utils import IntelligenceCache, with_caching


class GraphType(Enum):
    """Types of graphs that can be analyzed"""
    DEPENDENCY = "dependency"
    ATTACK_PATH = "attack_path"
    WORKFLOW = "workflow"
    CORRELATION = "correlation"
    ROUTING = "routing"


@dataclass
class GraphNode:
    """Represents a node in the intelligence graph"""
    id: str
    type: str
    properties: Dict[str, Any]
    metadata: Dict[str, Any]


@dataclass
class GraphEdge:
    """Represents an edge in the intelligence graph"""
    source: str
    target: str
    type: str
    weight: float
    properties: Dict[str, Any]


@dataclass
class GraphAnalysisResult:
    """Result of graph analysis operations"""
    paths: List[List[str]]
    cycles: List[List[str]]
    critical_nodes: List[str]
    communities: List[List[str]]
    metrics: Dict[str, float]


class GraphAnalysisIntelligenceService(IntelligenceServiceInterface):
    """
    Advanced graph analysis service for relationship discovery and path analysis.

    Based on real business logic patterns:
    - HELK attack path detection (GraphFrames analysis)
    - Commander Spellbook combo dependency resolution  
    - Actual Budget calculation dependency graphs
    - n8n workflow execution optimization
    - Kong service routing analysis
    """

    def __init__(self):
        self.cache = IntelligenceCache(max_size=1000, ttl_seconds=3600)
        self._graphs: Dict[str, Dict[str, Any]] = {}
        self._analysis_cache: Dict[str, GraphAnalysisResult] = {}

    async def analyze(
        self, request: IntelligenceRequest
    ) -> List[IntelligenceInsight]:
        """Analyze graph structures and relationships"""
        try:
            graph_data = request.data.get('graph', {})
            analysis_type = request.data.get('analysis_type', 'full')
            graph_type = GraphType(
                request.data.get('graph_type', 'dependency'))

            # Build graph from input data
            graph_id = await self._build_graph(graph_data, graph_type)

            # Perform requested analysis
            insights = []

            if analysis_type in ['full', 'paths']:
                path_insights = await self._analyze_paths(graph_id, graph_type)
                insights.extend(path_insights)

            if analysis_type in ['full', 'cycles']:
                cycle_insights = await self._detect_cycles(graph_id)
                insights.extend(cycle_insights)

            if analysis_type in ['full', 'critical']:
                critical_insights = await self._find_critical_nodes(graph_id)
                insights.extend(critical_insights)

            if analysis_type in ['full', 'communities']:
                community_insights = await self._detect_communities(graph_id)
                insights.extend(community_insights)

            return insights

        except Exception as e:
            return [IntelligenceInsight(
                type="graph_analysis_error",
                confidence=ConfidenceLevel.LOW,
                summary=f"Graph analysis failed: {str(e)}",
                details={"error": str(e), "analysis_type": analysis_type},
                recommendations=[
                    "Verify graph data format",
                    "Check for data completeness",
                    "Ensure valid node and edge relationships"
                ],
                metadata={"service": "graph_analysis", "error": True}
            )]

    async def _build_graph(
        self, graph_data: Dict[str, Any], graph_type: GraphType
    ) -> str:
        """Build internal graph representation from input data"""
        graph_id = f"graph_{hash(json.dumps(graph_data, sort_keys=True))}"

        if graph_id in self._graphs:
            return graph_id

        nodes = {}
        edges = defaultdict(list)

        # Process nodes
        for node_data in graph_data.get('nodes', []):
            node = GraphNode(
                id=node_data['id'],
                type=node_data.get('type', 'default'),
                properties=node_data.get('properties', {}),
                metadata=node_data.get('metadata', {})
            )
            nodes[node.id] = node

        # Process edges
        for edge_data in graph_data.get('edges', []):
            edge = GraphEdge(
                source=edge_data['source'],
                target=edge_data['target'],
                type=edge_data.get('type', 'default'),
                weight=edge_data.get('weight', 1.0),
                properties=edge_data.get('properties', {})
            )
            edges[edge.source].append(edge)

        self._graphs[graph_id] = {
            'nodes': nodes,
            'edges': edges,
            'type': graph_type,
            'metadata': graph_data.get('metadata', {})
        }

        return graph_id

    async def _analyze_paths(
        self, graph_id: str, graph_type: GraphType
    ) -> List[IntelligenceInsight]:
        """
        Analyze paths through the graph - based on HELK attack path analysis
        """
        graph = self._graphs[graph_id]
        insights = []

        if graph_type == GraphType.ATTACK_PATH:
            # Security-focused path analysis
            attack_paths = await self._find_attack_paths(graph_id)
            for path in attack_paths:
                risk_score = self._calculate_path_risk(path, graph)

                insights.append(IntelligenceInsight(
                    type="attack_path_detected",
                    confidence=ConfidenceLevel.HIGH if risk_score > 0.7 else ConfidenceLevel.MEDIUM,
                    summary=f"Potential attack path: {' -> '.join(path)}",
                    details={
                        "path": path,
                        "risk_score": risk_score,
                        "path_length": len(path),
                        "critical_nodes": self._identify_critical_path_nodes(path, graph)
                    },
                    recommendations=[
                        "Strengthen security controls along this path",
                        "Monitor these nodes for suspicious activity",
                        "Consider network segmentation to break the path"
                    ],
                    metadata={"service": "graph_analysis",
                              "analysis": "attack_path"}
                ))

        elif graph_type == GraphType.DEPENDENCY:
            # Dependency analysis like Commander Spellbook or Actual Budget
            critical_paths = await self._find_critical_dependency_paths(graph_id)
            for path in critical_paths:
                insights.append(IntelligenceInsight(
                    type="critical_dependency_path",
                    confidence=ConfidenceLevel.HIGH,
                    summary="Critical dependency chain detected",
                    details={
                        "path": path,
                        "dependency_depth": len(path),
                        "affected_components": self._count_affected_components(path, graph)
                    },
                    recommendations=[
                        "Consider dependency optimization",
                        "Add caching for expensive calculations",
                        "Parallelize independent operations"
                    ],
                    metadata={"service": "graph_analysis",
                              "analysis": "dependency"}
                ))

        return insights

    @with_caching(prefix="cycle_detection")
    async def _detect_cycles(self, graph_id: str) -> List[IntelligenceInsight]:
        """
        Detect cycles in the graph - critical for dependency resolution
        """
        graph = self._graphs[graph_id]
        cycles = self._find_cycles_dfs(graph)
        insights = []

        for cycle in cycles:
            severity = "high" if len(cycle) <= 3 else "medium"

            insights.append(IntelligenceInsight(
                type="dependency_cycle_detected",
                confidence=ConfidenceLevel.HIGH,
                summary=f"Dependency cycle detected: {' -> '.join(cycle + [cycle[0]])}",
                details={
                    "cycle": cycle,
                    "cycle_length": len(cycle),
                    "severity": severity,
                    "involved_types": [graph['nodes'][node_id].type for node_id in cycle]
                },
                recommendations=[
                    "Break the cycle by removing one dependency",
                    "Restructure components to eliminate circular references",
                    "Add lazy loading to break tight coupling"
                ],
                metadata={"service": "graph_analysis",
                          "analysis": "cycle_detection"}
            ))

        return insights

    async def _find_critical_nodes(self, graph_id: str) -> List[IntelligenceInsight]:
        """
        Find nodes that are critical to graph connectivity - high centrality
        """
        graph = self._graphs[graph_id]
        centrality_scores = self._calculate_betweenness_centrality(graph)

        # Top 10% most critical nodes
        sorted_nodes = sorted(
            centrality_scores.items(),
            key=lambda x: x[1],
            reverse=True
        )
        critical_threshold = 0.1  # Top 10%
        critical_count = max(1, int(len(sorted_nodes) * critical_threshold))
        critical_nodes = sorted_nodes[:critical_count]

        insights = []
        for node_id, centrality in critical_nodes:
            node = graph['nodes'][node_id]

            insights.append(IntelligenceInsight(
                type="critical_node_identified",
                confidence=ConfidenceLevel.HIGH,
                summary=f"Critical node identified: {node_id}",
                details={
                    "node_id": node_id,
                    "node_type": node.type,
                    "centrality_score": centrality,
                    "properties": node.properties,
                    "connection_count": len(graph['edges'].get(node_id, []))
                },
                recommendations=[
                    "Monitor this node for performance issues",
                    "Implement redundancy for critical functionality",
                    "Add extra logging and alerting",
                    "Consider load balancing if applicable"
                ],
                metadata={"service": "graph_analysis",
                          "analysis": "centrality"}
            ))

        return insights

    async def _detect_communities(self, graph_id: str) -> List[IntelligenceInsight]:
        """
        Detect communities/clusters in the graph structure
        """
        graph = self._graphs[graph_id]
        communities = self._find_communities_simple(graph)

        insights = []
        for i, community in enumerate(communities):
            if len(community) >= 3:  # Only report significant communities

                # Analyze community characteristics
                types = [graph['nodes'][node_id].type for node_id in community]
                type_distribution = {}
                for t in types:
                    type_distribution[t] = type_distribution.get(t, 0) + 1

                insights.append(IntelligenceInsight(
                    type="graph_community_detected",
                    confidence=ConfidenceLevel.MEDIUM,
                    summary=f"Graph community detected with {len(community)} nodes",
                    details={
                        "community_id": i,
                        "nodes": community,
                        "size": len(community),
                        "type_distribution": type_distribution,
                        "density": self._calculate_community_density(community, graph)
                    },
                    recommendations=[
                        "Consider grouping related functionality",
                        "Optimize internal communication within community",
                        "Evaluate if community should be a separate module"
                    ],
                    metadata={"service": "graph_analysis",
                              "analysis": "community"}
                ))

        return insights

    # Helper methods for graph algorithms

    def _find_cycles_dfs(self, graph: Dict[str, Any]) -> List[List[str]]:
        """Find cycles using depth-first search"""
        cycles = []
        visited = set()
        rec_stack = set()

        def dfs(node_id: str, path: List[str]):
            if node_id in rec_stack:
                # Found a cycle
                cycle_start = path.index(node_id)
                cycle = path[cycle_start:]
                cycles.append(cycle)
                return

            if node_id in visited:
                return

            visited.add(node_id)
            rec_stack.add(node_id)

            for edge in graph['edges'].get(node_id, []):
                dfs(edge.target, path + [edge.target])

            rec_stack.remove(node_id)

        for node_id in graph['nodes']:
            if node_id not in visited:
                dfs(node_id, [node_id])

        return cycles

    def _calculate_betweenness_centrality(
        self, graph: Dict[str, Any]
    ) -> Dict[str, float]:
        """Calculate betweenness centrality for all nodes"""
        centrality = {node_id: 0.0 for node_id in graph['nodes']}

        # Simplified betweenness centrality calculation
        # In production, use NetworkX or similar optimized implementation
        for source in graph['nodes']:
            for target in graph['nodes']:
                if source != target:
                    paths = self._find_shortest_paths(source, target, graph)
                    if paths:
                        for path in paths:
                            for node in path[1:-1]:  # Exclude source and target
                                centrality[node] += 1.0 / len(paths)

        # Normalize
        n = len(graph['nodes'])
        if n > 2:
            normalizer = 2.0 / ((n - 1) * (n - 2))
            for node in centrality:
                centrality[node] *= normalizer

        return centrality

    def _find_shortest_paths(
        self, source: str, target: str, graph: Dict[str, Any]
    ) -> List[List[str]]:
        """Find all shortest paths between source and target"""
        # BFS to find shortest paths
        queue = deque([(source, [source])])
        visited_distances = {source: 0}
        paths = []
        min_distance = None

        while queue:
            node, path = queue.popleft()

            if node == target:
                if min_distance is None:
                    min_distance = len(path) - 1
                if len(path) - 1 == min_distance:
                    paths.append(path)
                continue

            current_distance = len(path) - 1

            for edge in graph['edges'].get(node, []):
                next_node = edge.target
                next_distance = current_distance + 1

                if (next_node not in visited_distances or
                        visited_distances[next_node] >= next_distance):
                    visited_distances[next_node] = next_distance
                    queue.append((next_node, path + [next_node]))

        return paths

    async def _find_attack_paths(self, graph_id: str) -> List[List[str]]:
        """Find potential attack paths - based on HELK patterns"""
        graph = self._graphs[graph_id]
        attack_paths = []

        # Look for paths from external nodes to high-value targets
        external_nodes = [
            node_id for node_id, node in graph['nodes'].items()
            if node.type in ['external', 'internet', 'untrusted']
        ]

        target_nodes = [
            node_id for node_id, node in graph['nodes'].items()
            if node.type in ['critical', 'admin', 'database', 'server']
        ]

        for external in external_nodes:
            for target in target_nodes:
                paths = self._find_shortest_paths(external, target, graph)
                attack_paths.extend(paths[:3])  # Limit to top 3 shortest paths

        return attack_paths

    async def _find_critical_dependency_paths(
        self, graph_id: str
    ) -> List[List[str]]:
        """Find critical dependency chains"""
        graph = self._graphs[graph_id]
        critical_paths = []

        # Find long dependency chains
        for node_id in graph['nodes']:
            paths = self._get_dependency_chain(node_id, graph)
            for path in paths:
                if len(path) > 5:  # Chains longer than 5 are potentially problematic
                    critical_paths.append(path)

        return critical_paths

    def _get_dependency_chain(
        self, start_node: str, graph: Dict[str, Any]
    ) -> List[List[str]]:
        """Get dependency chain starting from a node"""
        chains = []
        visited = set()

        def dfs_chain(node: str, path: List[str]):
            if node in visited:
                return

            visited.add(node)
            current_path = path + [node]

            dependencies = graph['edges'].get(node, [])
            if not dependencies:
                chains.append(current_path)
            else:
                for edge in dependencies:
                    dfs_chain(edge.target, current_path)

        dfs_chain(start_node, [])
        return chains

    def _calculate_path_risk(
        self, path: List[str], graph: Dict[str, Any]
    ) -> float:
        """Calculate risk score for an attack path"""
        risk_score = 0.0

        for node_id in path:
            node = graph['nodes'][node_id]

            # Higher risk for certain node types
            if node.type in ['admin', 'critical', 'database']:
                risk_score += 0.3
            elif node.type in ['server', 'workstation']:
                risk_score += 0.2
            else:
                risk_score += 0.1

            # Factor in node properties
            if node.properties.get('exposed', False):
                risk_score += 0.2
            if node.properties.get('unpatched', False):
                risk_score += 0.15

        # Normalize by path length
        return min(1.0, risk_score / len(path))

    def _identify_critical_path_nodes(
        self, path: List[str], graph: Dict[str, Any]
    ) -> List[str]:
        """Identify the most critical nodes in a path"""
        critical = []
        for node_id in path:
            node = graph['nodes'][node_id]
            if (node.type in ['admin', 'critical', 'database'] or
                    node.properties.get('exposed', False)):
                critical.append(node_id)
        return critical

    def _count_affected_components(
        self, path: List[str], graph: Dict[str, Any]
    ) -> int:
        """Count how many components would be affected by this dependency"""
        # Simplified - count downstream dependencies
        affected = set(path)

        for node_id in path:
            # Add all nodes that depend on this path
            for other_node, edges in graph['edges'].items():
                for edge in edges:
                    if edge.target in path:
                        affected.add(other_node)

        return len(affected)

    def _find_communities_simple(
        self, graph: Dict[str, Any]
    ) -> List[List[str]]:
        """Simple community detection using connected components"""
        communities = []
        visited = set()

        def dfs_component(node: str, component: List[str]):
            if node in visited:
                return

            visited.add(node)
            component.append(node)

            # Follow both incoming and outgoing edges
            for edge in graph['edges'].get(node, []):
                dfs_component(edge.target, component)

            # Follow incoming edges
            for source_node, edges in graph['edges'].items():
                for edge in edges:
                    if edge.target == node:
                        dfs_component(source_node, component)

        for node_id in graph['nodes']:
            if node_id not in visited:
                component = []
                dfs_component(node_id, component)
                if component:
                    communities.append(component)

        return communities

    def _calculate_community_density(
        self, community: List[str], graph: Dict[str, Any]
    ) -> float:
        """Calculate density of connections within a community"""
        if len(community) < 2:
            return 0.0

        internal_edges = 0
        max_possible_edges = len(community) * (len(community) - 1)

        for node in community:
            for edge in graph['edges'].get(node, []):
                if edge.target in community:
                    internal_edges += 1

        return internal_edges / max_possible_edges if max_possible_edges > 0 else 0.0
