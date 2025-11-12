"""
Combinatorial Intelligence Service

Enhanced combinatorial analysis capabilities based on business logic patterns from:
- Commander Spellbook: Combo variant generation with exponential complexity (O(C^N))
- Actual Budget: Spreadsheet dependency resolution with cycle detection
- n8n: Workflow dependency graph analysis and optimization
- YARA-X: Pattern combination and atom extraction optimization
- Kong: Route combination and priority resolution

Provides optional combinatorial intelligence that applications can use for:
- Complex rule validation and variant generation
- Dependency resolution with cycle detection
- Optimization of combinatorial search spaces
- Pattern combination and matching strategies
"""

import hashlib
import itertools
import json
import time
from collections import defaultdict, deque
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple

from ..shared.interfaces import (ConfidenceLevel, IntelligenceInsight,
                                 IntelligenceRequest,
                                 IntelligenceServiceInterface)
from ..shared.utils import IntelligenceCache


class CombinatorialMode(Enum):
    """Types of combinatorial analysis"""
    VARIANT_GENERATION = "variant_generation"
    DEPENDENCY_RESOLUTION = "dependency_resolution"
    OPTIMIZATION = "optimization"
    PATTERN_COMBINATION = "pattern_combination"
    CONSTRAINT_SATISFACTION = "constraint_satisfaction"


@dataclass
class CombinatorialRule:
    """Represents a combinatorial rule or constraint"""
    id: str
    rule_type: str
    conditions: Dict[str, Any]
    constraints: Dict[str, Any]
    priority: int
    metadata: Dict[str, Any]


@dataclass
class CombinatorialVariant:
    """Represents a generated variant or solution"""
    id: str
    components: List[str]
    properties: Dict[str, Any]
    validity_score: float
    constraints_satisfied: List[str]
    metadata: Dict[str, Any]


@dataclass
class DependencyNode:
    """Represents a node in dependency analysis"""
    id: str
    dependencies: List[str]
    properties: Dict[str, Any]
    resolved: bool


class CombinatorialIntelligenceService(IntelligenceServiceInterface):
    """
    Advanced combinatorial analysis service for complex rule systems.

    Based on real business logic patterns:
    - Commander Spellbook variant generation (exponential complexity handling)
    - Actual Budget dependency graph resolution
    - n8n workflow optimization algorithms
    - YARA-X pattern combination strategies
    - Kong route priority and matching optimization
    """

    def __init__(self):
        self.cache = IntelligenceCache(max_size=5000, ttl_seconds=3600)

        # Combinatorial state management
        self._rules: Dict[str, CombinatorialRule] = {}
        self._variants_cache: Dict[str, List[CombinatorialVariant]] = {}
        self._dependency_cache: Dict[str, Dict[str, DependencyNode]] = {}

        # Performance tracking
        self._generation_stats = {
            'total_variants_generated': 0,
            'max_complexity_handled': 0,
            'avg_generation_time': 0.0,
            'optimization_ratio': 0.0
        }

    async def analyze(
        self, request: IntelligenceRequest
    ) -> List[IntelligenceInsight]:
        """Perform combinatorial analysis"""
        try:
            mode = CombinatorialMode(
                request.data.get('mode', 'variant_generation')
            )

            insights = []

            if mode == CombinatorialMode.VARIANT_GENERATION:
                insights.extend(await self._perform_variant_generation(request))

            elif mode == CombinatorialMode.DEPENDENCY_RESOLUTION:
                insights.extend(await self._perform_dependency_analysis(request))

            elif mode == CombinatorialMode.OPTIMIZATION:
                insights.extend(await self._perform_optimization_analysis(request))

            elif mode == CombinatorialMode.PATTERN_COMBINATION:
                insights.extend(await self._perform_pattern_combination(request))

            elif mode == CombinatorialMode.CONSTRAINT_SATISFACTION:
                insights.extend(await self._perform_constraint_satisfaction(request))

            return insights

        except Exception as e:
            return [IntelligenceInsight(
                type="combinatorial_analysis_error",
                confidence=ConfidenceLevel.LOW,
                summary=f"Combinatorial analysis failed: {str(e)}",
                details={"error": str(e), "mode": request.data.get('mode')},
                recommendations=[
                    "Reduce complexity of input data",
                    "Check rule validation syntax",
                    "Consider breaking problem into smaller parts"
                ],
                metadata={"service": "combinatorial_analysis", "error": True}
            )]

    async def _perform_variant_generation(
        self, request: IntelligenceRequest
    ) -> List[IntelligenceInsight]:
        """
        Generate variants from rules - based on Commander Spellbook patterns
        """
        insights = []

        # Load rules and components
        rules = request.data.get('rules', [])
        components = request.data.get('components', [])
        max_variants = request.data.get('max_variants', 1000)
        allow_duplicates = request.data.get('allow_duplicates', False)

        # Load rules into internal format
        for rule_data in rules:
            rule = CombinatorialRule(
                id=rule_data['id'],
                rule_type=rule_data.get('type', 'combination'),
                conditions=rule_data.get('conditions', {}),
                constraints=rule_data.get('constraints', {}),
                priority=rule_data.get('priority', 0),
                metadata=rule_data.get('metadata', {})
            )
            self._rules[rule.id] = rule

        # Generate variants using combinatorial algorithms
        try:
            variants = await self._generate_variants(
                components, list(self._rules.values()
                                 ), max_variants, allow_duplicates
            )

            # Analyze generation results
            if variants:
                complexity_score = self._calculate_complexity(
                    components, rules)
                optimization_ratio = len(variants) / min(max_variants,
                                                         self._theoretical_max_combinations(components))

                insights.append(IntelligenceInsight(
                    type="variant_generation_complete",
                    confidence=ConfidenceLevel.HIGH,
                    summary=f"Generated {len(variants)} valid variants",
                    details={
                        "variant_count": len(variants),
                        "components_used": len(components),
                        "rules_applied": len(rules),
                        "complexity_score": complexity_score,
                        "optimization_ratio": optimization_ratio,
                        "top_variants": [
                            self._variant_to_dict(v) for v in variants[:5]
                        ]
                    },
                    recommendations=self._get_variant_recommendations(
                        variants, complexity_score
                    ),
                    metadata={"service": "combinatorial_analysis",
                              "analysis": "variants"}
                ))

                # Detect interesting patterns in variants
                patterns = await self._analyze_variant_patterns(variants)
                for pattern in patterns:
                    insights.append(IntelligenceInsight(
                        type="variant_pattern_detected",
                        confidence=ConfidenceLevel.MEDIUM,
                        summary=f"Pattern detected: {pattern['type']}",
                        details=pattern,
                        recommendations=[
                            "Consider optimizing rules based on this pattern",
                            "Evaluate if pattern indicates missing constraints"
                        ],
                        metadata={"service": "combinatorial_analysis",
                                  "analysis": "patterns"}
                    ))

        except Exception as e:
            insights.append(IntelligenceInsight(
                type="variant_generation_failed",
                confidence=ConfidenceLevel.HIGH,
                summary=f"Variant generation failed due to complexity: {str(e)}",
                details={
                    "error": str(e),
                    "component_count": len(components),
                    "rule_count": len(rules),
                    "estimated_complexity": self._calculate_complexity(components, rules)
                },
                recommendations=[
                    "Reduce number of components",
                    "Add more restrictive constraints",
                    "Use iterative generation approach",
                    "Consider parallel processing"
                ],
                metadata={"service": "combinatorial_analysis", "error": True}
            ))

        return insights

    async def _perform_dependency_analysis(
        self, request: IntelligenceRequest
    ) -> List[IntelligenceInsight]:
        """
        Dependency resolution analysis - based on Actual Budget patterns
        """
        insights = []

        dependencies = request.data.get('dependencies', [])

        # Build dependency graph
        dep_graph = {}
        for dep_data in dependencies:
            node = DependencyNode(
                id=dep_data['id'],
                dependencies=dep_data.get('depends_on', []),
                properties=dep_data.get('properties', {}),
                resolved=False
            )
            dep_graph[node.id] = node

        # Detect cycles
        cycles = self._detect_dependency_cycles(dep_graph)
        if cycles:
            for cycle in cycles:
                insights.append(IntelligenceInsight(
                    type="dependency_cycle_detected",
                    confidence=ConfidenceLevel.HIGH,
                    summary=f"Circular dependency: {' -> '.join(cycle + [cycle[0]])}",
                    details={
                        "cycle": cycle,
                        "cycle_length": len(cycle),
                        "affected_nodes": self._get_affected_by_cycle(cycle, dep_graph)
                    },
                    recommendations=[
                        "Break circular dependency by removing one link",
                        "Introduce lazy loading or caching",
                        "Restructure dependencies to eliminate cycle"
                    ],
                    metadata={"service": "combinatorial_analysis",
                              "analysis": "cycles"}
                ))

        # Find optimal resolution order
        try:
            resolution_order = await self._calculate_optimal_resolution_order(dep_graph)

            insights.append(IntelligenceInsight(
                type="dependency_resolution_order",
                confidence=ConfidenceLevel.HIGH,
                summary="Optimal resolution order determined",
                details={
                    "resolution_order": resolution_order,
                    "total_nodes": len(dep_graph),
                    "parallelizable_groups": self._find_parallelizable_groups(
                        resolution_order, dep_graph
                    ),
                    "critical_path_length": self._calculate_critical_path_length(dep_graph)
                },
                recommendations=[
                    "Process dependencies in the suggested order",
                    "Parallelize independent groups where possible",
                    "Cache results of expensive calculations"
                ],
                metadata={"service": "combinatorial_analysis",
                          "analysis": "resolution"}
            ))

        except Exception as e:
            insights.append(IntelligenceInsight(
                type="dependency_resolution_failed",
                confidence=ConfidenceLevel.HIGH,
                summary=f"Cannot resolve dependencies: {str(e)}",
                details={
                    "error": str(e),
                    "cycles_detected": len(cycles),
                    "total_dependencies": len(dep_graph)
                },
                recommendations=[
                    "Remove circular dependencies first",
                    "Simplify dependency structure",
                    "Consider breaking large components into smaller ones"
                ],
                metadata={"service": "combinatorial_analysis", "error": True}
            ))

        return insights

    async def _perform_optimization_analysis(
        self, request: IntelligenceRequest
    ) -> List[IntelligenceInsight]:
        """
        Combinatorial optimization analysis
        """
        insights = []

        optimization_type = request.data.get('optimization_type', 'minimize')
        objective_function = request.data.get('objective', {})
        constraints = request.data.get('constraints', [])
        variables = request.data.get('variables', [])

        # Analyze optimization problem complexity
        problem_size = len(variables)
        constraint_count = len(constraints)
        complexity_estimate = self._estimate_optimization_complexity(
            problem_size, constraint_count, optimization_type
        )

        # Suggest optimization strategies
        strategies = await self._suggest_optimization_strategies(
            complexity_estimate, objective_function, constraints
        )

        insights.append(IntelligenceInsight(
            type="optimization_analysis",
            confidence=ConfidenceLevel.MEDIUM,
            summary=f"Optimization problem analyzed ({optimization_type})",
            details={
                "problem_size": problem_size,
                "constraint_count": constraint_count,
                "complexity_estimate": complexity_estimate,
                "optimization_type": optimization_type,
                "suggested_strategies": strategies
            },
            recommendations=self._get_optimization_recommendations(
                complexity_estimate, strategies
            ),
            metadata={"service": "combinatorial_analysis",
                      "analysis": "optimization"}
        ))

        return insights

    async def _perform_pattern_combination(
        self, request: IntelligenceRequest
    ) -> List[IntelligenceInsight]:
        """
        Pattern combination analysis - based on YARA-X patterns
        """
        insights = []

        patterns = request.data.get('patterns', [])
        combination_rules = request.data.get('combination_rules', [])

        # Generate pattern combinations
        combinations = await self._generate_pattern_combinations(
            patterns, combination_rules
        )

        # Analyze combination effectiveness
        for combo in combinations:
            effectiveness = self._calculate_pattern_effectiveness(combo)

            if effectiveness > 0.7:  # High effectiveness threshold
                insights.append(IntelligenceInsight(
                    type="effective_pattern_combination",
                    confidence=ConfidenceLevel.HIGH,
                    summary="Highly effective pattern combination found",
                    details={
                        "combination_id": combo['id'],
                        "patterns": combo['patterns'],
                        "effectiveness_score": effectiveness,
                        "coverage": combo.get('coverage', 0.0),
                        "specificity": combo.get('specificity', 0.0)
                    },
                    recommendations=[
                        "Use this pattern combination for improved detection",
                        "Monitor false positive rates",
                        "Consider adding to standard pattern library"
                    ],
                    metadata={"service": "combinatorial_analysis",
                              "analysis": "patterns"}
                ))

        return insights

    async def _perform_constraint_satisfaction(
        self, request: IntelligenceRequest
    ) -> List[IntelligenceInsight]:
        """
        Constraint satisfaction problem analysis
        """
        insights = []

        variables = request.data.get('variables', [])
        domains = request.data.get('domains', {})
        constraints = request.data.get('constraints', [])

        # Analyze constraint satisfaction problem
        csp_analysis = await self._analyze_csp(variables, domains, constraints)

        insights.append(IntelligenceInsight(
            type="constraint_satisfaction_analysis",
            confidence=ConfidenceLevel.MEDIUM,
            summary="CSP analysis complete",
            details=csp_analysis,
            recommendations=self._get_csp_recommendations(csp_analysis),
            metadata={"service": "combinatorial_analysis", "analysis": "csp"}
        ))

        return insights

    # Variant generation methods (based on Commander Spellbook)

    async def _generate_variants(
        self,
        components: List[Dict[str, Any]],
        rules: List[CombinatorialRule],
        max_variants: int,
        allow_duplicates: bool
    ) -> List[CombinatorialVariant]:
        """Generate variants using combinatorial algorithms"""
        variants = []
        seen_combinations = set()

        # Determine component requirements from rules
        requirements = self._extract_requirements(rules)

        # Generate combinations within complexity limits
        for combination_size in range(1, min(len(components) + 1, 10)):
            if len(variants) >= max_variants:
                break

            for combo in itertools.combinations(components, combination_size):
                if len(variants) >= max_variants:
                    break

                # Create variant from combination
                variant = await self._create_variant_from_combination(
                    combo, rules, requirements
                )

                if variant and variant.validity_score > 0.5:
                    combo_hash = self._hash_combination(combo)

                    if allow_duplicates or combo_hash not in seen_combinations:
                        variants.append(variant)
                        seen_combinations.add(combo_hash)

        # Sort by validity score
        variants.sort(key=lambda v: v.validity_score, reverse=True)

        return variants[:max_variants]

    async def _create_variant_from_combination(
        self,
        combination: Tuple[Dict[str, Any], ...],
        rules: List[CombinatorialRule],
        requirements: Dict[str, Any]
    ) -> Optional[CombinatorialVariant]:
        """Create a variant from a component combination"""

        # Validate combination against rules
        validity_score = 0.0
        satisfied_constraints = []

        for rule in rules:
            if self._combination_satisfies_rule(combination, rule):
                validity_score += rule.priority / 100.0
                satisfied_constraints.append(rule.id)

        if validity_score <= 0:
            return None

        # Create variant
        component_ids = [comp.get('id', str(i))
                         for i, comp in enumerate(combination)]
        variant_id = hashlib.md5(
            json.dumps(component_ids, sort_keys=True).encode()
        ).hexdigest()[:8]

        return CombinatorialVariant(
            id=variant_id,
            components=component_ids,
            properties=self._calculate_variant_properties(combination),
            validity_score=min(1.0, validity_score),
            constraints_satisfied=satisfied_constraints,
            metadata={
                'combination_size': len(combination),
                'generation_timestamp': time.time()
            }
        )

    def _combination_satisfies_rule(
        self,
        combination: Tuple[Dict[str, Any], ...],
        rule: CombinatorialRule
    ) -> bool:
        """Check if combination satisfies a specific rule"""

        conditions = rule.conditions
        constraints = rule.constraints

        # Check basic conditions
        if 'min_components' in conditions:
            if len(combination) < conditions['min_components']:
                return False

        if 'max_components' in conditions:
            if len(combination) > conditions['max_components']:
                return False

        # Check component type requirements
        if 'required_types' in conditions:
            component_types = [comp.get('type', 'unknown')
                               for comp in combination]
            for required_type in conditions['required_types']:
                if required_type not in component_types:
                    return False

        # Check constraints
        if 'mutually_exclusive' in constraints:
            exclusive_pairs = constraints['mutually_exclusive']
            component_ids = [comp.get('id') for comp in combination]

            for pair in exclusive_pairs:
                if all(comp_id in component_ids for comp_id in pair):
                    return False

        return True

    def _calculate_variant_properties(
        self, combination: Tuple[Dict[str, Any], ...]
    ) -> Dict[str, Any]:
        """Calculate aggregate properties for a variant"""
        properties = {}

        # Aggregate numerical properties
        numerical_props = defaultdict(list)
        for comp in combination:
            for key, value in comp.get('properties', {}).items():
                if isinstance(value, (int, float)):
                    numerical_props[key].append(value)

        for prop_name, values in numerical_props.items():
            properties[f"{prop_name}_sum"] = sum(values)
            properties[f"{prop_name}_avg"] = sum(values) / len(values)
            properties[f"{prop_name}_max"] = max(values)
            properties[f"{prop_name}_min"] = min(values)

        # Collect categorical properties
        categorical_props = defaultdict(set)
        for comp in combination:
            for key, value in comp.get('properties', {}).items():
                if isinstance(value, str):
                    categorical_props[key].add(value)

        for prop_name, values in categorical_props.items():
            properties[f"{prop_name}_set"] = list(values)
            properties[f"{prop_name}_count"] = len(values)

        return properties

    # Dependency analysis methods (based on Actual Budget)

    def _detect_dependency_cycles(
        self, dep_graph: Dict[str, DependencyNode]
    ) -> List[List[str]]:
        """Detect cycles in dependency graph using DFS"""
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

            node = dep_graph.get(node_id)
            if node:
                for dep_id in node.dependencies:
                    if dep_id in dep_graph:
                        dfs(dep_id, path + [dep_id])

            rec_stack.remove(node_id)

        for node_id in dep_graph:
            if node_id not in visited:
                dfs(node_id, [node_id])

        return cycles

    async def _calculate_optimal_resolution_order(
        self, dep_graph: Dict[str, DependencyNode]
    ) -> List[str]:
        """Calculate optimal dependency resolution order using topological sort"""

        # Kahn's algorithm for topological sorting
        in_degree = {node_id: 0 for node_id in dep_graph}

        # Calculate in-degrees
        for node in dep_graph.values():
            for dep_id in node.dependencies:
                if dep_id in in_degree:
                    in_degree[dep_id] += 1

        # Queue of nodes with no dependencies
        queue = deque(
            [node_id for node_id, degree in in_degree.items() if degree == 0])
        resolution_order = []

        while queue:
            node_id = queue.popleft()
            resolution_order.append(node_id)

            # Update in-degrees of dependent nodes
            node = dep_graph.get(node_id)
            if node:
                for dep_id in node.dependencies:
                    if dep_id in in_degree:
                        in_degree[dep_id] -= 1
                        if in_degree[dep_id] == 0:
                            queue.append(dep_id)

        if len(resolution_order) != len(dep_graph):
            raise ValueError("Circular dependencies prevent resolution")

        return resolution_order

    # Helper methods

    def _calculate_complexity(
        self, components: List[Dict[str, Any]], rules: List[Dict[str, Any]]
    ) -> float:
        """Calculate problem complexity score"""
        component_count = len(components)
        rule_count = len(rules)

        # Base complexity from combinatorial explosion
        base_complexity = min(10.0, component_count ** 2 / 100.0)

        # Rule complexity factor
        rule_complexity = min(5.0, rule_count / 10.0)

        return base_complexity + rule_complexity

    def _theoretical_max_combinations(self, components: List[Dict[str, Any]]) -> int:
        """Calculate theoretical maximum number of combinations"""
        n = len(components)
        return 2 ** n - 1  # All non-empty subsets

    def _hash_combination(self, combination: Tuple[Dict[str, Any], ...]) -> str:
        """Create hash for combination to detect duplicates"""
        component_ids = [comp.get('id', str(hash(str(comp))))
                         for comp in combination]
        return hashlib.md5(
            json.dumps(sorted(component_ids)).encode()
        ).hexdigest()

    def _variant_to_dict(self, variant: CombinatorialVariant) -> Dict[str, Any]:
        """Convert variant to dictionary for serialization"""
        return {
            'id': variant.id,
            'components': variant.components,
            'validity_score': variant.validity_score,
            'constraints_satisfied': variant.constraints_satisfied,
            'properties': variant.properties
        }

    def _extract_requirements(self, rules: List[CombinatorialRule]) -> Dict[str, Any]:
        """Extract requirements from rules"""
        requirements = {
            'min_components': 1,
            'max_components': float('inf'),
            'required_types': set(),
            'forbidden_combinations': []
        }

        for rule in rules:
            conditions = rule.conditions

            if 'min_components' in conditions:
                requirements['min_components'] = max(
                    requirements['min_components'],
                    conditions['min_components']
                )

            if 'max_components' in conditions:
                requirements['max_components'] = min(
                    requirements['max_components'],
                    conditions['max_components']
                )

            if 'required_types' in conditions:
                requirements['required_types'].update(
                    conditions['required_types'])

        requirements['required_types'] = list(requirements['required_types'])
        return requirements

    def _get_variant_recommendations(
        self, variants: List[CombinatorialVariant], complexity_score: float
    ) -> List[str]:
        """Get recommendations based on variant generation results"""
        recommendations = []

        if complexity_score > 7.0:
            recommendations.extend([
                "Consider reducing problem complexity",
                "Add more restrictive constraints",
                "Use iterative generation approach"
            ])

        if len(variants) == 0:
            recommendations.extend([
                "Rules may be too restrictive",
                "Check component compatibility",
                "Review constraint definitions"
            ])

        if variants:
            avg_score = sum(v.validity_score for v in variants) / len(variants)
            if avg_score < 0.6:
                recommendations.append(
                    "Consider adjusting rule weights and priorities")

        return recommendations

    async def _analyze_variant_patterns(
        self, variants: List[CombinatorialVariant]
    ) -> List[Dict[str, Any]]:
        """Analyze patterns in generated variants"""
        patterns = []

        # Component usage frequency
        component_usage = defaultdict(int)
        for variant in variants:
            for comp_id in variant.components:
                component_usage[comp_id] += 1

        # Find highly used components
        total_variants = len(variants)
        highly_used = [
            comp_id for comp_id, count in component_usage.items()
            if count / total_variants > 0.8
        ]

        if highly_used:
            patterns.append({
                'type': 'highly_used_components',
                'components': highly_used,
                'usage_rate': max(component_usage[comp_id] / total_variants
                                  for comp_id in highly_used),
                'description': 'Components that appear in most valid variants'
            })

        return patterns
