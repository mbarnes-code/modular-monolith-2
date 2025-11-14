"""
Code Intelligence Service - AI-Enhanced TypeScript AST Manipulation

This service provides AI-driven code generation, refactoring, and analysis capabilities
using ts-morph-like functionality for the mental prosthetic platform.

Zero Dependencies Promise:
- All existing applications continue working without this service
- Code intelligence is purely additive - enhances capabilities when available
- Graceful degradation ensures applications work even if this service fails
- No breaking changes to existing codebases

Usage Patterns:
1. Optional Enhancement: @with_code_intelligence decorator
2. Direct Integration: CodeIntelligenceService.analyze()
3. Context Manager: async with code_intelligence_context()
"""

import asyncio
import json
import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple, Union

logger = logging.getLogger(__name__)


class CodeDomain(Enum):
    """Code intelligence domains matching the 37-tool platform structure."""
    SECURITY = "security"
    PRODUCTIVITY = "productivity"
    MTG = "mtg"
    INFRASTRUCTURE = "infrastructure"
    CROSS_DOMAIN = "cross-domain"


class CodeIntelligenceType(Enum):
    """Types of code intelligence operations."""
    GENERATION = "generation"
    REFACTORING = "refactoring"
    PATTERN_ANALYSIS = "pattern_analysis"
    AST_MANIPULATION = "ast_manipulation"
    SECURITY_ANALYSIS = "security_analysis"
    ACCESSIBILITY_ENHANCEMENT = "accessibility_enhancement"


@dataclass
class CodePattern:
    """Represents a detected code pattern."""
    id: str
    name: str
    type: str
    domain: CodeDomain
    confidence: float
    locations: List[Dict[str, Any]]
    suggested_improvements: List[str]
    security_implications: Optional[Dict[str, Any]] = None
    accessibility_score: Optional[float] = None
    performance_impact: Optional[Dict[str, Any]] = None


@dataclass
class GenerationRequest:
    """Request for AI-driven code generation."""
    domain: CodeDomain
    intent: str
    context: Dict[str, Any]
    requirements: Dict[str, Any]
    security_level: str = "standard"
    accessibility_requirements: Optional[Dict[str, Any]] = None
    executive_function_accommodations: bool = True


@dataclass
class RefactoringPlan:
    """Plan for AI-guided code refactoring."""
    id: str
    target_files: List[str]
    transformations: List[Dict[str, Any]]
    risk_assessment: Dict[str, Any]
    estimated_impact: Dict[str, Any]
    rollback_plan: Dict[str, Any]


@dataclass
class AccessibilityFeatures:
    """Accessibility features for executive function support."""
    response_time_target: int = 75  # milliseconds for ADHD-friendly UI
    focus_management: Dict[str, Any] = field(default_factory=dict)
    interaction_patterns: Dict[str, Any] = field(default_factory=dict)
    feedback_systems: Dict[str, Any] = field(default_factory=dict)
    cognitive_load_score: Optional[float] = None


class CodeIntelligenceError(Exception):
    """Base exception for code intelligence operations."""
    pass


class AICodeAnalyzer:
    """AI-powered code analysis engine (mock implementation)."""

    async def analyze_patterns(self, code: str, domain: CodeDomain) -> List[CodePattern]:
        """Analyze code for patterns using AI."""
        # Mock AI analysis - in real implementation, this would use AI models
        await asyncio.sleep(0.1)  # Simulate AI processing

        patterns = []

        # Security pattern detection
        if "password" in code.lower() or "api_key" in code.lower():
            patterns.append(CodePattern(
                id=f"security_pattern_{datetime.now().timestamp()}",
                name="Potential Credential Exposure",
                type="security_risk",
                domain=domain,
                confidence=0.85,
                locations=[{"line": 1, "column": 1, "length": 10}],
                suggested_improvements=[
                    "Use environment variables for credentials",
                    "Implement credential rotation",
                    "Add credential encryption"
                ],
                security_implications={
                    "risk_level": "high",
                    "threat_vectors": ["credential_theft", "data_breach"]
                }
            ))

        # Performance pattern detection
        if "setTimeout" in code or "setInterval" in code:
            patterns.append(CodePattern(
                id=f"perf_pattern_{datetime.now().timestamp()}",
                name="Potential Performance Impact",
                type="performance",
                domain=domain,
                confidence=0.7,
                locations=[{"line": 1, "column": 1, "length": 15}],
                suggested_improvements=[
                    "Consider using requestAnimationFrame for UI updates",
                    "Implement debouncing for frequent operations",
                    "Add performance monitoring"
                ],
                performance_impact={
                    "response_time_impact": "+50ms",
                    "memory_impact": "low"
                }
            ))

        # Accessibility pattern detection
        if "onClick" in code and "onKeyDown" not in code:
            patterns.append(CodePattern(
                id=f"a11y_pattern_{datetime.now().timestamp()}",
                name="Missing Keyboard Navigation",
                type="accessibility",
                domain=domain,
                confidence=0.9,
                locations=[{"line": 1, "column": 1, "length": 7}],
                suggested_improvements=[
                    "Add keyboard event handlers",
                    "Implement focus management",
                    "Add ARIA labels"
                ],
                accessibility_score=0.6
            ))

        return patterns

    async def generate_code(self, request: GenerationRequest) -> Dict[str, Any]:
        """Generate code based on AI analysis."""
        await asyncio.sleep(0.2)  # Simulate AI generation

        # Domain-specific generation patterns
        templates = {
            CodeDomain.SECURITY: {
                "class_template": """
class SecureComponent {
    private validateInput(input: string): boolean {
        // AI-generated input validation
        return input.length > 0 && !this.containsSQLInjection(input);
    }
    
    private containsSQLInjection(input: string): boolean {
        const patterns = [/'/, /--/, /;/, /\bUNION\b/i];
        return patterns.some(pattern => pattern.test(input));
    }
}""",
                "features": ["input_validation", "sql_injection_prevention", "audit_logging"]
            },
            CodeDomain.PRODUCTIVITY: {
                "class_template": """
class ProductivityComponent {
    private responseTimeTracker = new PerformanceTracker();
    
    async optimizedOperation(data: any): Promise<any> {
        const start = performance.now();
        try {
            const result = await this.processData(data);
            const duration = performance.now() - start;
            
            // Executive function accommodation - fast feedback
            if (duration > 75) {
                console.warn('Operation exceeded ADHD-friendly threshold');
            }
            
            return result;
        } catch (error) {
            this.responseTimeTracker.recordError(error);
            throw error;
        }
    }
}""",
                "features": ["performance_tracking", "executive_function_support", "error_handling"]
            },
            CodeDomain.MTG: {
                "class_template": """
interface MTGCard {
    name: string;
    manaCost: string;
    type: string;
    abilities: string[];
}

class MTGRulesEngine {
    async resolveInteraction(card1: MTGCard, card2: MTGCard): Promise<InteractionResult> {
        // AI-generated rules resolution
        const interactions = await this.analyzeCardInteractions([card1, card2]);
        return this.applyPriorityRules(interactions);
    }
}""",
                "features": ["type_safety", "rules_engine", "interaction_resolution"]
            }
        }

        template = templates.get(
            request.domain, templates[CodeDomain.SECURITY])

        # Add accessibility accommodations if requested
        accessibility_features = AccessibilityFeatures()
        if request.executive_function_accommodations:
            accessibility_features.response_time_target = 75
            accessibility_features.focus_management = {
                "auto_focus": True,
                "focus_trap": True,
                "escape_handling": True
            }

        return {
            "generated_code": template["class_template"],
            "features": template["features"],
            "accessibility_features": accessibility_features,
            "metadata": {
                "domain": request.domain.value,
                "generation_time": datetime.now().isoformat(),
                "ai_confidence": 0.85,
                "security_level": request.security_level
            }
        }

    async def suggest_refactoring(self, code: str, patterns: List[CodePattern]) -> RefactoringPlan:
        """Generate refactoring suggestions based on detected patterns."""
        await asyncio.sleep(0.15)  # Simulate AI analysis

        transformations = []

        for pattern in patterns:
            if pattern.type == "security_risk":
                transformations.append({
                    "type": "security_enhancement",
                    "description": "Add credential protection",
                    "changes": [
                        {
                            "action": "replace",
                            "target": "hardcoded credentials",
                            "replacement": "environment variable access"
                        }
                    ]
                })
            elif pattern.type == "accessibility":
                transformations.append({
                    "type": "accessibility_improvement",
                    "description": "Add keyboard navigation support",
                    "changes": [
                        {
                            "action": "add",
                            "target": "event handlers",
                            "replacement": "keyboard event handlers with ARIA support"
                        }
                    ]
                })

        return RefactoringPlan(
            id=f"refactor_plan_{datetime.now().timestamp()}",
            target_files=["example.ts"],
            transformations=transformations,
            risk_assessment={
                "overall_risk": "low",
                "breaking_changes": False,
                "rollback_complexity": "simple"
            },
            estimated_impact={
                "security_improvement": "+40%",
                "accessibility_score": "+30%",
                "performance_impact": "neutral"
            },
            rollback_plan={
                "strategy": "git_revert",
                "automated": True,
                "backup_required": False
            }
        )


class CodeIntelligenceService:
    """
    AI-Enhanced Code Intelligence Service

    Provides ts-morph-like capabilities with AI enhancement for:
    - Cross-domain pattern analysis
    - Executive function accommodations
    - Security-first code generation
    - Automated refactoring suggestions
    - Domain-specific optimizations
    """

    def __init__(self):
        self.ai_analyzer = AICodeAnalyzer()
        self.cache = {}
        self.metrics = {
            "patterns_detected": 0,
            "code_generated": 0,
            "refactorings_suggested": 0
        }

    async def analyze_cross_domain_patterns(
        self,
        codebases: Dict[CodeDomain, List[str]]
    ) -> Dict[str, Any]:
        """
        Analyze patterns across security, productivity, MTG, and infrastructure domains.

        This is the core ts-morph enhancement - AI-driven cross-domain pattern detection
        that identifies opportunities for unified architectures and reduced cognitive overhead.
        """
        try:
            all_patterns = {}

            for domain, code_files in codebases.items():
                domain_patterns = []

                for code in code_files:
                    patterns = await self.ai_analyzer.analyze_patterns(code, domain)
                    domain_patterns.extend(patterns)

                all_patterns[domain.value] = domain_patterns
                self.metrics["patterns_detected"] += len(domain_patterns)

            # AI synthesis of cross-domain insights
            cross_domain_insights = await self._synthesize_cross_domain_insights(all_patterns)

            return {
                "domain_patterns": all_patterns,
                "cross_domain_insights": cross_domain_insights,
                "unified_opportunities": await self._identify_unification_opportunities(all_patterns),
                "executive_function_score": self._calculate_cognitive_load_score(all_patterns),
                "metrics": self.metrics.copy()
            }

        except Exception as e:
            logger.error(f"Cross-domain pattern analysis failed: {e}")
            return {"error": str(e), "patterns": {}}

    async def generate_accessible_component(
        self,
        spec: GenerationRequest
    ) -> Dict[str, Any]:
        """
        Generate code with built-in executive function accommodations.

        Implements the ADHD-friendly development tools concept from ts-morph notes.
        """
        try:
            # Ensure executive function accommodations are enabled
            spec.executive_function_accommodations = True
            if not spec.accessibility_requirements:
                spec.accessibility_requirements = {
                    "response_time_target": 75,  # <75ms for ADHD-friendly
                    "focus_management": True,
                    "progress_indicators": True,
                    "predictable_patterns": True
                }

            generated = await self.ai_analyzer.generate_code(spec)
            self.metrics["code_generated"] += 1

            # Add executive function specific enhancements
            enhanced_code = self._add_executive_function_accommodations(
                generated["generated_code"],
                spec.accessibility_requirements
            )

            return {
                **generated,
                "enhanced_code": enhanced_code,
                "executive_function_features": {
                    "response_time_optimized": True,
                    "consistent_patterns": True,
                    "cognitive_load_minimized": True,
                    "focus_management_built_in": True
                }
            }

        except Exception as e:
            logger.error(f"Accessible component generation failed: {e}")
            return {"error": str(e)}

    async def generate_security_first_component(
        self,
        threat_model: Dict[str, Any],
        business_requirements: List[str]
    ) -> Dict[str, Any]:
        """
        Generate code with security controls baked in.

        Implements threat-model driven development from ts-morph notes.
        """
        try:
            # Analyze threat model to determine security requirements
            security_requirements = await self._analyze_threat_model(threat_model)

            # Create generation request with security focus
            request = GenerationRequest(
                domain=CodeDomain.SECURITY,
                intent="secure_component_with_threat_protection",
                context={"threat_model": threat_model},
                requirements={"business": business_requirements},
                security_level="high"
            )

            generated = await self.ai_analyzer.generate_code(request)

            # Add security-specific enhancements
            security_enhanced_code = self._add_security_controls(
                generated["generated_code"],
                security_requirements
            )

            self.metrics["code_generated"] += 1

            return {
                **generated,
                "security_enhanced_code": security_enhanced_code,
                "security_features": security_requirements,
                "threat_coverage": self._calculate_threat_coverage(
                    threat_model,
                    security_requirements
                )
            }

        except Exception as e:
            logger.error(f"Security-first component generation failed: {e}")
            return {"error": str(e)}

    async def generate_mtg_rules_engine(
        self,
        card_specs: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Generate MTG rules engine with type-safe interactions.

        Implements domain-specific language creation from ts-morph notes.
        """
        try:
            # AI analyzes MTG card interactions
            rule_patterns = await self._analyze_mtg_interactions(card_specs)

            request = GenerationRequest(
                domain=CodeDomain.MTG,
                intent="type_safe_rules_engine",
                context={"card_specs": card_specs},
                requirements={"type_safety": True,
                              "interaction_resolution": True}
            )

            generated = await self.ai_analyzer.generate_code(request)

            # Add MTG-specific rule resolution
            rules_engine_code = self._add_mtg_rule_resolution(
                generated["generated_code"],
                rule_patterns
            )

            self.metrics["code_generated"] += 1

            return {
                **generated,
                "rules_engine_code": rules_engine_code,
                "rule_patterns": rule_patterns,
                "interaction_coverage": len(rule_patterns.get("interactions", []))
            }

        except Exception as e:
            logger.error(f"MTG rules engine generation failed: {e}")
            return {"error": str(e)}

    async def suggest_intelligent_refactoring(
        self,
        source_files: List[str]
    ) -> RefactoringPlan:
        """
        AI-guided refactoring with modernization suggestions.

        Implements intelligent code modernization from ts-morph notes.
        """
        try:
            all_patterns = []

            for code in source_files:
                patterns = await self.ai_analyzer.analyze_patterns(code, CodeDomain.CROSS_DOMAIN)
                all_patterns.extend(patterns)

            refactoring_plan = await self.ai_analyzer.suggest_refactoring("".join(source_files), all_patterns)

            # Add AI-specific enhancements
            enhanced_plan = await self._enhance_refactoring_plan(refactoring_plan, all_patterns)

            self.metrics["refactorings_suggested"] += 1

            return enhanced_plan

        except Exception as e:
            logger.error(f"Intelligent refactoring suggestion failed: {e}")
            return RefactoringPlan(
                id="error_plan",
                target_files=[],
                transformations=[],
                risk_assessment={"error": str(e)},
                estimated_impact={},
                rollback_plan={}
            )

    # Private helper methods

    async def _synthesize_cross_domain_insights(self, patterns: Dict[str, List[CodePattern]]) -> Dict[str, Any]:
        """Synthesize insights across multiple domains."""
        await asyncio.sleep(0.1)  # Simulate AI synthesis

        total_patterns = sum(len(p) for p in patterns.values())
        security_patterns = len(patterns.get("security", []))
        accessibility_patterns = sum(1 for domain_patterns in patterns.values()
                                     for p in domain_patterns if p.accessibility_score)

        return {
            "total_patterns_detected": total_patterns,
            "security_attention_needed": security_patterns > 0,
            "accessibility_opportunities": accessibility_patterns,
            "cross_domain_similarities": ["error_handling", "input_validation", "performance_monitoring"],
            "unification_potential": "high" if total_patterns > 5 else "medium"
        }

    async def _identify_unification_opportunities(self, patterns: Dict[str, List[CodePattern]]) -> List[Dict[str, Any]]:
        """Identify opportunities for unified architectures."""
        opportunities = []

        # Look for common patterns across domains
        common_types = set()
        for domain_patterns in patterns.values():
            common_types.update(p.type for p in domain_patterns)

        if len(common_types) > 2:
            opportunities.append({
                "type": "shared_utility_library",
                "description": "Create shared utilities for common patterns",
                "affected_domains": list(patterns.keys()),
                "estimated_effort": "medium",
                "cognitive_load_reduction": "high"
            })

        return opportunities

    def _calculate_cognitive_load_score(self, patterns: Dict[str, List[CodePattern]]) -> float:
        """Calculate cognitive load score for executive function support."""
        total_patterns = sum(len(p) for p in patterns.values())
        accessibility_patterns = sum(1 for domain_patterns in patterns.values()
                                     for p in domain_patterns if p.accessibility_score)

        if total_patterns == 0:
            return 1.0

        # Higher accessibility pattern ratio = lower cognitive load
        accessibility_ratio = accessibility_patterns / total_patterns
        return min(1.0, accessibility_ratio + 0.5)

    def _add_executive_function_accommodations(self, code: str, requirements: Dict[str, Any]) -> str:
        """Add executive function specific code enhancements."""
        accommodations = [
            "// Executive Function Accommodations",
            "const RESPONSE_TIME_TARGET = 75; // milliseconds for ADHD-friendly UI",
            "const performanceTracker = new PerformanceTracker();",
            "",
            "// Auto-focus management for reduced cognitive load",
            "useEffect(() => {",
            "  if (autoFocus && inputRef.current) {",
            "    inputRef.current.focus();",
            "  }",
            "}, []);",
            "",
            "// Consistent interaction patterns",
            "const handleInteraction = useCallback((event) => {",
            "  const start = performance.now();",
            "  // ... interaction logic",
            "  const duration = performance.now() - start;",
            "  if (duration > RESPONSE_TIME_TARGET) {",
            "    console.warn('Interaction exceeded target response time');",
            "  }",
            "}, []);"
        ]

        return "\n".join(accommodations) + "\n\n" + code

    def _add_security_controls(self, code: str, security_requirements: Dict[str, Any]) -> str:
        """Add security controls to generated code."""
        security_additions = [
            "// Security Controls - Threat Model Driven",
            "import { validateInput, sanitizeOutput, auditLog } from '@security/utils';",
            "",
            "const securityMiddleware = {",
            "  validateInput: (input: any) => {",
            "    const validation = validateInput(input);",
            "    if (!validation.isValid) {",
            "      auditLog.warn('Input validation failed', { input, errors: validation.errors });",
            "      throw new SecurityError('Invalid input');",
            "    }",
            "    return validation.sanitized;",
            "  },",
            "  ",
            "  sanitizeOutput: (output: any) => {",
            "    return sanitizeOutput(output, { removeScripts: true, escapeHtml: true });",
            "  }",
            "};"
        ]

        return "\n".join(security_additions) + "\n\n" + code

    def _add_mtg_rule_resolution(self, code: str, rule_patterns: Dict[str, Any]) -> str:
        """Add MTG-specific rule resolution logic."""
        mtg_additions = [
            "// MTG Rules Engine - Type-Safe Interactions",
            "interface CardInteraction {",
            "  priority: number;",
            "  condition: (gameState: GameState) => boolean;",
            "  effect: (gameState: GameState) => GameState;",
            "}",
            "",
            "class InteractionResolver {",
            "  resolveStack(interactions: CardInteraction[]): GameState {",
            "    return interactions",
            "      .sort((a, b) => b.priority - a.priority)",
            "      .reduce((state, interaction) => {",
            "        return interaction.condition(state) ? interaction.effect(state) : state;",
            "      }, this.currentGameState);",
            "  }",
            "}"
        ]

        return "\n".join(mtg_additions) + "\n\n" + code

    async def _analyze_threat_model(self, threat_model: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze threat model and determine required security controls."""
        await asyncio.sleep(0.1)  # Simulate analysis

        return {
            "input_validation": [
                {"type": "sql_injection", "required": True},
                {"type": "xss_prevention", "required": True}
            ],
            "middleware": [
                {"type": "authentication", "required": True},
                {"type": "authorization", "required": True}
            ],
            "monitoring": [
                {"type": "audit_logging", "required": True},
                {"type": "anomaly_detection", "required": False}
            ]
        }

    def _calculate_threat_coverage(self, threat_model: Dict[str, Any], security_requirements: Dict[str, Any]) -> float:
        """Calculate how well the generated code covers the threat model."""
        # Simple coverage calculation - in real implementation this would be more sophisticated
        return 0.85

    async def _analyze_mtg_interactions(self, card_specs: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze MTG card interactions to determine rule patterns."""
        await asyncio.sleep(0.1)  # Simulate analysis

        return {
            "card_types": [
                {"name": "Creature", "properties": [
                    "power", "toughness", "abilities"]},
                {"name": "Instant", "properties": ["effect", "mana_cost"]},
                {"name": "Sorcery", "properties": ["effect", "mana_cost"]}
            ],
            "interactions": [
                {"type": "combat_damage", "priority": 1},
                {"type": "triggered_ability", "priority": 2}
            ]
        }

    async def _enhance_refactoring_plan(self, plan: RefactoringPlan, patterns: List[CodePattern]) -> RefactoringPlan:
        """Enhance refactoring plan with AI insights."""
        # Add accessibility improvements
        accessibility_transformations = []
        for pattern in patterns:
            if pattern.accessibility_score and pattern.accessibility_score < 0.8:
                accessibility_transformations.append({
                    "type": "accessibility_enhancement",
                    "description": f"Improve accessibility for {pattern.name}",
                    "changes": pattern.suggested_improvements
                })

        plan.transformations.extend(accessibility_transformations)
        return plan


# Integration adapters for existing applications

class CodeIntelligenceAdapter:
    """Adapter for integrating code intelligence with existing applications."""

    def __init__(self, service: Optional[CodeIntelligenceService] = None):
        self.service = service or CodeIntelligenceService()
        self.available = service is not None

    async def enhance_n8n_node_generation(self, node_spec: Dict[str, Any]) -> Dict[str, Any]:
        """Enhance n8n node generation with AI intelligence."""
        if not self.available:
            return node_spec  # Graceful degradation

        try:
            # Generate enhanced node with AI recommendations
            generation_request = GenerationRequest(
                domain=CodeDomain.PRODUCTIVITY,
                intent="n8n_node_generation",
                context=node_spec,
                requirements={"workflow_optimization": True}
            )

            enhanced = await self.service.generate_accessible_component(generation_request)

            return {
                **node_spec,
                "ai_enhanced": True,
                "generated_code": enhanced.get("enhanced_code", ""),
                "intelligence_metadata": enhanced.get("metadata", {})
            }

        except Exception as e:
            logger.warning(
                f"Code intelligence enhancement failed, using fallback: {e}")
            return node_spec  # Graceful fallback

    async def enhance_security_tool_integration(self, tool_spec: Dict[str, Any]) -> Dict[str, Any]:
        """Enhance security tool integration with threat analysis."""
        if not self.available:
            return tool_spec

        try:
            threat_model = tool_spec.get("threat_model", {})
            business_requirements = tool_spec.get("requirements", [])

            enhanced = await self.service.generate_security_first_component(
                threat_model, business_requirements
            )

            return {
                **tool_spec,
                "security_enhanced": True,
                "generated_integration": enhanced.get("security_enhanced_code", ""),
                "threat_coverage": enhanced.get("threat_coverage", 0.0)
            }

        except Exception as e:
            logger.warning(f"Security enhancement failed, using fallback: {e}")
            return tool_spec


# Decorator for optional code intelligence enhancement

def with_code_intelligence(intelligence_type: CodeIntelligenceType = CodeIntelligenceType.GENERATION):
    """
    Decorator to optionally enhance functions with code intelligence.

    Usage:
    @with_code_intelligence(CodeIntelligenceType.GENERATION)
    async def generate_component(spec):
        # Original functionality preserved
        return basic_component
    """
    def decorator(func):
        async def wrapper(*args, **kwargs):
            # Always execute original function
            result = await func(*args, **kwargs)

            try:
                # Try to enhance with code intelligence
                adapter = CodeIntelligenceAdapter()
                if adapter.available and intelligence_type == CodeIntelligenceType.GENERATION:
                    if "n8n" in str(func.__name__).lower():
                        result = await adapter.enhance_n8n_node_generation(result)
                    elif "security" in str(func.__name__).lower():
                        result = await adapter.enhance_security_tool_integration(result)

            except Exception as e:
                logger.debug(f"Code intelligence enhancement failed: {e}")
                # Return original result on any failure

            return result

        return wrapper
    return decorator


# Export key components for easy integration

__all__ = [
    "CodeIntelligenceService",
    "CodeIntelligenceAdapter",
    "CodeDomain",
    "CodeIntelligenceType",
    "GenerationRequest",
    "RefactoringPlan",
    "AccessibilityFeatures",
    "with_code_intelligence"
]
