"""Conditional Logic Flow Analysis for n8n Workflow Automation.

This module detects decision trees and conditional workflows in user behavior 
patterns to automate them through n8n IF/Switch nodes and conditional routing.
"""

import re
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Set


class ConditionType(Enum):
    """Types of conditions that can be detected in workflows."""
    BOOLEAN = "boolean"  # Simple true/false conditions
    COMPARISON = "comparison"  # Value comparisons (>, <, ==, etc.)
    RANGE = "range"  # Value within range
    PATTERN_MATCH = "pattern_match"  # Regex or string pattern matching
    LIST_CONTAINS = "list_contains"  # Item in list/array
    THRESHOLD = "threshold"  # Value above/below threshold
    STATUS_CHECK = "status_check"  # Status or state conditions
    DATA_PRESENCE = "data_presence"  # Data exists or is null
    TIME_BASED = "time_based"  # Time/date conditions
    MULTI_CRITERIA = "multi_criteria"  # Multiple conditions combined


class LogicOperator(Enum):
    """Logical operators for combining conditions."""
    AND = "and"
    OR = "or"
    NOT = "not"
    XOR = "xor"


class ActionType(Enum):
    """Types of actions taken based on conditions."""
    ROUTE_TO_TOOL = "route_to_tool"  # Route to different tool
    SKIP_STEP = "skip_step"  # Skip certain steps
    REPEAT_ACTION = "repeat_action"  # Repeat an action
    TERMINATE_FLOW = "terminate_flow"  # Stop the workflow
    TRANSFORM_DATA = "transform_data"  # Apply data transformation
    SEND_NOTIFICATION = "send_notification"  # Send alert/notification
    LOG_EVENT = "log_event"  # Log for audit/debugging
    SET_VARIABLE = "set_variable"  # Set workflow variable


@dataclass
class Condition:
    """Represents a single condition in a decision flow."""
    condition_id: str
    condition_type: ConditionType
    field_name: str  # Data field being evaluated
    operator: str  # Comparison operator (==, >, <, contains, etc.)
    value: Any  # Value to compare against
    description: str  # Human-readable description
    confidence: float  # Confidence in condition detection (0.0-1.0)


@dataclass
class ConditionalAction:
    """Represents an action taken when conditions are met."""
    action_id: str
    action_type: ActionType
    target: str  # Target tool, step, or resource
    parameters: Dict[str, Any]  # Action parameters
    description: str


@dataclass
class DecisionNode:
    """Represents a decision point in a conditional workflow."""
    node_id: str
    conditions: List[Condition]
    logic_operator: LogicOperator  # How to combine conditions
    true_action: ConditionalAction  # Action if conditions are true
    false_action: Optional[ConditionalAction]  # Action if conditions are false
    frequency: int  # How often this decision pattern occurs
    success_rate: float  # Success rate of this decision logic


@dataclass
class ConditionalFlow:
    """Represents a complete conditional workflow pattern."""
    flow_id: str
    flow_name: str
    decision_nodes: List[DecisionNode]
    entry_conditions: List[Condition]  # Conditions to enter the flow
    flow_description: str
    tools_involved: Set[str]
    complexity_score: float  # 0.0 to 1.0
    automation_potential: float  # 0.0 to 1.0
    frequency: int
    performance_metrics: Dict[str, Any]


@dataclass
class UserDecision:
    """Represents a user decision captured from interaction history."""
    decision_id: str
    user_id: str
    timestamp: datetime
    context_data: Dict[str, Any]  # Data available at decision time
    decision_taken: str  # What the user chose to do
    outcome: str  # Result of the decision
    success: bool  # Whether the decision was successful
    tool_context: str  # Which tool the decision was made in
    prior_actions: List[str]  # Previous actions leading to decision


class LogicFlowAnalyzer:
    """Analyzes user behavior to detect conditional logic patterns."""

    def __init__(self):
        self.decision_history = []
        self.condition_patterns = self._initialize_condition_patterns()
        self.action_patterns = self._initialize_action_patterns()
        # Max time between related decisions
        self.decision_timeout = timedelta(minutes=15)

    def _initialize_condition_patterns(self) -> Dict[str, ConditionType]:
        """Initialize patterns that indicate different condition types."""
        return {
            # Boolean patterns
            r'.*is.*true|.*is.*false|.*enabled|.*disabled': ConditionType.BOOLEAN,
            r'.*active|.*inactive|.*on|.*off': ConditionType.BOOLEAN,

            # Comparison patterns
            r'.*greater.*than|.*less.*than|.*equal.*to': ConditionType.COMPARISON,
            r'.*above|.*below|.*exceeds|.*under': ConditionType.COMPARISON,

            # Range patterns
            r'.*between|.*range|.*within': ConditionType.RANGE,

            # Pattern matching
            r'.*matches|.*contains|.*starts.*with|.*ends.*with': ConditionType.PATTERN_MATCH,
            r'.*regex|.*pattern|.*format': ConditionType.PATTERN_MATCH,

            # List operations
            r'.*in.*list|.*exists.*in|.*member.*of': ConditionType.LIST_CONTAINS,

            # Threshold patterns
            r'.*threshold|.*limit|.*maximum|.*minimum': ConditionType.THRESHOLD,

            # Status patterns
            r'.*status|.*state|.*condition': ConditionType.STATUS_CHECK,

            # Data presence
            r'.*exists|.*null|.*empty|.*missing': ConditionType.DATA_PRESENCE,

            # Time-based
            r'.*before|.*after|.*during|.*time': ConditionType.TIME_BASED,
            r'.*date|.*hour|.*day|.*week': ConditionType.TIME_BASED
        }

    def _initialize_action_patterns(self) -> Dict[str, ActionType]:
        """Initialize patterns that indicate different action types."""
        return {
            # Routing patterns
            r'.*route.*to|.*send.*to|.*forward.*to': ActionType.ROUTE_TO_TOOL,
            r'.*use.*tool|.*switch.*to|.*redirect': ActionType.ROUTE_TO_TOOL,

            # Skip patterns
            r'.*skip|.*bypass|.*ignore': ActionType.SKIP_STEP,

            # Repeat patterns
            r'.*repeat|.*retry|.*again|.*loop': ActionType.REPEAT_ACTION,

            # Terminate patterns
            r'.*stop|.*end|.*terminate|.*cancel': ActionType.TERMINATE_FLOW,
            r'.*abort|.*halt|.*exit': ActionType.TERMINATE_FLOW,

            # Transform patterns
            r'.*transform|.*convert|.*modify': ActionType.TRANSFORM_DATA,
            r'.*format|.*process|.*clean': ActionType.TRANSFORM_DATA,

            # Notification patterns
            r'.*notify|.*alert|.*warn|.*inform': ActionType.SEND_NOTIFICATION,
            r'.*email|.*message|.*send': ActionType.SEND_NOTIFICATION,

            # Logging patterns
            r'.*log|.*record|.*track|.*audit': ActionType.LOG_EVENT,

            # Variable patterns
            r'.*set|.*assign|.*store|.*save': ActionType.SET_VARIABLE
        }

    def record_user_decision(
        self,
        user_id: str,
        context_data: Dict[str, Any],
        decision_taken: str,
        outcome: str,
        success: bool,
        tool_context: str,
        prior_actions: Optional[List[str]] = None
    ) -> UserDecision:
        """Record a user decision for analysis."""

        decision = UserDecision(
            decision_id=f"{user_id}_{datetime.utcnow().isoformat()}",
            user_id=user_id,
            timestamp=datetime.utcnow(),
            context_data=context_data,
            decision_taken=decision_taken,
            outcome=outcome,
            success=success,
            tool_context=tool_context,
            prior_actions=prior_actions or []
        )

        self.decision_history.append(decision)
        return decision

    def analyze_decision_patterns(
        self, user_id: str, time_window: timedelta = timedelta(days=14)
    ) -> List[DecisionNode]:
        """Analyze user decisions to identify conditional patterns."""

        # Filter decisions for user and time window
        cutoff_time = datetime.utcnow() - time_window
        user_decisions = [
            decision for decision in self.decision_history
            if (decision.user_id == user_id and
                decision.timestamp >= cutoff_time)
        ]

        if not user_decisions:
            return []

        # Group decisions by context similarity
        decision_groups = self._group_similar_decisions(user_decisions)

        # Extract decision nodes from groups
        decision_nodes = []
        for group in decision_groups:
            node = self._extract_decision_node(group)
            if node and self._is_meaningful_decision_node(node):
                decision_nodes.append(node)

        return decision_nodes

    def detect_conditional_flows(
        self, decision_nodes: List[DecisionNode]
    ) -> List[ConditionalFlow]:
        """Detect complete conditional flows from decision nodes."""

        flows = []

        # Group related decision nodes into flows
        flow_groups = self._group_nodes_into_flows(decision_nodes)

        for group in flow_groups:
            flow = self._create_conditional_flow(group)
            if flow and self._is_viable_flow(flow):
                flows.append(flow)

        # Sort by automation potential and frequency
        flows.sort(
            key=lambda f: (f.automation_potential, f.frequency),
            reverse=True
        )

        return flows

    def analyze_decision_context(
        self, decisions: List[UserDecision]
    ) -> Dict[str, Any]:
        """Analyze the context and triggers for user decisions."""

        context_analysis = {
            'common_trigger_fields': self._analyze_trigger_fields(decisions),
            'decision_timing_patterns': self._analyze_timing_patterns(decisions),
            'success_factors': self._analyze_success_factors(decisions),
            'tool_transition_patterns': self._analyze_tool_transitions(decisions),
            'data_dependency_patterns': self._analyze_data_dependencies(decisions)
        }

        return context_analysis

    def generate_n8n_conditional_nodes(
        self, flow: ConditionalFlow
    ) -> List[Dict[str, Any]]:
        """Generate n8n IF/Switch nodes for a conditional flow."""

        nodes = []

        for i, decision_node in enumerate(flow.decision_nodes):
            # Create IF or Switch node based on complexity
            if len(decision_node.conditions) == 1:
                node = self._create_n8n_if_node(decision_node, i)
            else:
                node = self._create_n8n_switch_node(decision_node, i)

            if node:
                nodes.append(node)

        return nodes

    def suggest_flow_optimizations(
        self, flow: ConditionalFlow
    ) -> List[Dict[str, Any]]:
        """Suggest optimizations for conditional flows."""

        optimizations = []

        # Check for redundant conditions
        redundancy = self._detect_redundant_conditions(flow)
        if redundancy:
            optimizations.append(redundancy)

        # Check for condition reordering opportunities
        reordering = self._suggest_condition_reordering(flow)
        if reordering:
            optimizations.append(reordering)

        # Check for parallel evaluation opportunities
        parallelization = self._assess_parallel_evaluation(flow)
        if parallelization:
            optimizations.append(parallelization)

        # Check for caching opportunities
        caching = self._suggest_condition_caching(flow)
        if caching:
            optimizations.append(caching)

        return optimizations

    # Private helper methods

    def _group_similar_decisions(
        self, decisions: List[UserDecision]
    ) -> List[List[UserDecision]]:
        """Group decisions with similar context or patterns."""

        groups = []
        used_decisions = set()

        for i, decision in enumerate(decisions):
            if i in used_decisions:
                continue

            group = [decision]
            used_decisions.add(i)

            # Find similar decisions
            for j, other_decision in enumerate(decisions[i+1:], i+1):
                if j in used_decisions:
                    continue

                if self._decisions_are_similar(decision, other_decision):
                    group.append(other_decision)
                    used_decisions.add(j)

            if len(group) >= 2:  # Only include groups with multiple decisions
                groups.append(group)

        return groups

    def _decisions_are_similar(
        self, decision1: UserDecision, decision2: UserDecision
    ) -> bool:
        """Determine if two decisions are similar enough to group."""

        # Similar tool context
        if decision1.tool_context != decision2.tool_context:
            return False

        # Similar decision type (based on decision text)
        if not self._have_similar_decision_text(
            decision1.decision_taken, decision2.decision_taken
        ):
            return False

        # Similar context data structure
        if not self._have_similar_context_structure(
            decision1.context_data, decision2.context_data
        ):
            return False

        # Similar outcomes
        if decision1.success != decision2.success:
            return False

        return True

    def _have_similar_decision_text(self, text1: str, text2: str) -> bool:
        """Check if two decision descriptions are similar."""

        # Extract key action words
        words1 = set(re.findall(r'\b\w+\b', text1.lower()))
        words2 = set(re.findall(r'\b\w+\b', text2.lower()))

        # Calculate similarity
        intersection = words1 & words2
        union = words1 | words2

        if not union:
            return False

        similarity = len(intersection) / len(union)
        return similarity >= 0.4  # 40% word overlap

    def _have_similar_context_structure(
        self, context1: Dict[str, Any], context2: Dict[str, Any]
    ) -> bool:
        """Check if two context dictionaries have similar structure."""

        keys1 = set(context1.keys())
        keys2 = set(context2.keys())

        # Check for key overlap
        intersection = keys1 & keys2
        union = keys1 | keys2

        if not union:
            return True  # Both empty

        key_similarity = len(intersection) / len(union)
        return key_similarity >= 0.6  # 60% key overlap

    def _extract_decision_node(
        self, decision_group: List[UserDecision]
    ) -> Optional[DecisionNode]:
        """Extract a decision node pattern from a group of similar decisions."""

        if not decision_group:
            return None

        # Analyze conditions from context data
        conditions = self._extract_conditions_from_group(decision_group)
        if not conditions:
            return None

        # Determine logic operator
        logic_operator = self._infer_logic_operator(decision_group)

        # Extract actions
        true_action = self._extract_true_action(decision_group)
        false_action = self._extract_false_action(decision_group)

        # Calculate metrics
        frequency = len(decision_group)
        success_count = sum(1 for d in decision_group if d.success)
        success_rate = success_count / len(decision_group)

        return DecisionNode(
            node_id=f"node_{decision_group[0].user_id}_{len(conditions)}",
            conditions=conditions,
            logic_operator=logic_operator,
            true_action=true_action,
            false_action=false_action,
            frequency=frequency,
            success_rate=success_rate
        )

    def _extract_conditions_from_group(
        self, decision_group: List[UserDecision]
    ) -> List[Condition]:
        """Extract common conditions from a group of decisions."""

        conditions = []

        # Analyze context data to find decision factors
        common_fields = self._find_common_context_fields(decision_group)

        for field_name in common_fields:
            condition = self._create_condition_for_field(
                field_name, decision_group
            )
            if condition:
                conditions.append(condition)

        return conditions

    def _find_common_context_fields(
        self, decisions: List[UserDecision]
    ) -> Set[str]:
        """Find context fields that appear in most decisions."""

        field_counts = Counter()

        for decision in decisions:
            for field in decision.context_data.keys():
                field_counts[field] += 1

        # Return fields that appear in at least 70% of decisions
        threshold = len(decisions) * 0.7
        common_fields = {
            field for field, count in field_counts.items()
            if count >= threshold
        }

        return common_fields

    def _create_condition_for_field(
        self, field_name: str, decisions: List[UserDecision]
    ) -> Optional[Condition]:
        """Create a condition based on field analysis across decisions."""

        # Extract field values and associated decisions
        field_values = []
        successful_decisions = []

        for decision in decisions:
            if field_name in decision.context_data:
                field_values.append(decision.context_data[field_name])
                if decision.success:
                    successful_decisions.append(decision)

        if not field_values:
            return None

        # Analyze value patterns to determine condition type and operator
        condition_type = self._infer_condition_type(field_name, field_values)
        operator, value = self._infer_condition_operator_and_value(
            field_values, successful_decisions
        )

        if not operator:
            return None

        # Calculate confidence based on pattern consistency
        confidence = self._calculate_condition_confidence(
            field_values, operator, value
        )

        return Condition(
            condition_id=f"cond_{field_name}_{hash(str(value)) % 10000}",
            condition_type=condition_type,
            field_name=field_name,
            operator=operator,
            value=value,
            description=f"{field_name} {operator} {value}",
            confidence=confidence
        )

    def _infer_condition_type(
        self, field_name: str, values: List[Any]
    ) -> ConditionType:
        """Infer condition type from field name and values."""

        field_lower = field_name.lower()

        # Check field name patterns
        for pattern, condition_type in self.condition_patterns.items():
            if re.search(pattern, field_lower):
                return condition_type

        # Check value types
        if all(isinstance(v, bool) for v in values):
            return ConditionType.BOOLEAN
        elif all(isinstance(v, (int, float)) for v in values):
            return ConditionType.COMPARISON
        elif all(isinstance(v, str) for v in values):
            if any(pattern in v.lower() for v in values
                   for pattern in ['match', 'contains', 'pattern']):
                return ConditionType.PATTERN_MATCH
            else:
                return ConditionType.STATUS_CHECK
        elif all(isinstance(v, list) for v in values):
            return ConditionType.LIST_CONTAINS

        return ConditionType.COMPARISON  # Default

    def _infer_condition_operator_and_value(
        self, field_values: List[Any], successful_decisions: List[UserDecision]
    ) -> tuple[Optional[str], Any]:
        """Infer the operator and threshold value for a condition."""

        if not field_values:
            return None, None

        # Analyze successful vs unsuccessful decisions
        successful_values = []
        for decision in successful_decisions:
            if hasattr(decision, 'context_data'):
                for value in decision.context_data.values():
                    if value in field_values:
                        successful_values.append(value)

        # Handle different value types
        if all(isinstance(v, bool) for v in field_values):
            # Boolean condition
            most_successful = Counter(successful_values).most_common(1)
            if most_successful:
                return "==", most_successful[0][0]
            return "==", True

        elif all(isinstance(v, (int, float)) for v in field_values):
            # Numeric condition
            if successful_values:
                avg_successful = sum(successful_values) / \
                    len(successful_values)
                avg_all = sum(field_values) / len(field_values)

                if avg_successful > avg_all:
                    return ">", avg_all
                else:
                    return "<", avg_all
            else:
                # Use median as threshold
                sorted_values = sorted(field_values)
                median = sorted_values[len(sorted_values) // 2]
                return ">", median

        elif all(isinstance(v, str) for v in field_values):
            # String condition
            most_common = Counter(successful_values).most_common(1)
            if most_common:
                return "==", most_common[0][0]
            else:
                return "contains", ""

        elif all(isinstance(v, list) for v in field_values):
            # List condition
            return "length >", 0

        return None, None

    def _calculate_condition_confidence(
        self, field_values: List[Any], operator: str, value: Any
    ) -> float:
        """Calculate confidence in a condition based on value consistency."""

        if not field_values:
            return 0.0

        # Test how many values satisfy the condition
        satisfying_count = 0

        for field_value in field_values:
            try:
                if operator == "==":
                    if field_value == value:
                        satisfying_count += 1
                elif operator == ">":
                    if isinstance(field_value, (int, float)) and field_value > value:
                        satisfying_count += 1
                elif operator == "<":
                    if isinstance(field_value, (int, float)) and field_value < value:
                        satisfying_count += 1
                elif operator == "contains":
                    if isinstance(field_value, str) and str(value) in field_value:
                        satisfying_count += 1
                elif operator == "length >":
                    if hasattr(field_value, '__len__') and len(field_value) > value:
                        satisfying_count += 1
            except (TypeError, AttributeError):
                continue

        # Confidence is the percentage of values that satisfy the condition
        confidence = satisfying_count / len(field_values)

        # Boost confidence if it's either very high or very low (clear pattern)
        if confidence >= 0.8 or confidence <= 0.2:
            confidence = min(confidence + 0.1, 1.0)

        return confidence

    def _infer_logic_operator(
        self, decision_group: List[UserDecision]
    ) -> LogicOperator:
        """Infer how multiple conditions should be combined."""

        # Analyze decision text for logic keywords
        all_text = " ".join([
            d.decision_taken.lower() for d in decision_group
        ])

        if " and " in all_text or " & " in all_text:
            return LogicOperator.AND
        elif " or " in all_text or " | " in all_text:
            return LogicOperator.OR
        elif " not " in all_text or "!" in all_text:
            return LogicOperator.NOT
        else:
            # Default to AND for multiple conditions
            return LogicOperator.AND

    def _extract_true_action(
        self, decision_group: List[UserDecision]
    ) -> ConditionalAction:
        """Extract the action taken when conditions are true."""

        # Analyze successful decisions
        successful_decisions = [d for d in decision_group if d.success]
        if not successful_decisions:
            successful_decisions = decision_group

        # Find most common action
        actions = [d.decision_taken for d in successful_decisions]
        most_common_action = Counter(actions).most_common(1)[0][0]

        # Infer action type
        action_type = self._infer_action_type(most_common_action)

        # Extract target from action
        target = self._extract_action_target(most_common_action)

        return ConditionalAction(
            action_id=f"action_true_{hash(most_common_action) % 10000}",
            action_type=action_type,
            target=target,
            parameters=self._extract_action_parameters(successful_decisions),
            description=most_common_action
        )

    def _extract_false_action(
        self, decision_group: List[UserDecision]
    ) -> Optional[ConditionalAction]:
        """Extract the action taken when conditions are false."""

        # Look for unsuccessful decisions or alternative actions
        unsuccessful_decisions = [d for d in decision_group if not d.success]

        if not unsuccessful_decisions:
            return None

        # Find alternative action pattern
        actions = [d.decision_taken for d in unsuccessful_decisions]
        if not actions:
            return None

        most_common_action = Counter(actions).most_common(1)[0][0]
        action_type = self._infer_action_type(most_common_action)
        target = self._extract_action_target(most_common_action)

        return ConditionalAction(
            action_id=f"action_false_{hash(most_common_action) % 10000}",
            action_type=action_type,
            target=target,
            parameters=self._extract_action_parameters(unsuccessful_decisions),
            description=most_common_action
        )

    def _infer_action_type(self, action_text: str) -> ActionType:
        """Infer action type from action description."""

        action_lower = action_text.lower()

        # Check action patterns
        for pattern, action_type in self.action_patterns.items():
            if re.search(pattern, action_lower):
                return action_type

        # Default to route if no pattern matches
        return ActionType.ROUTE_TO_TOOL

    def _extract_action_target(self, action_text: str) -> str:
        """Extract the target of an action from its description."""

        # Look for tool names or common targets
        words = action_text.lower().split()

        # Common tool patterns
        tool_keywords = [
            'misp', 'helk', 'cyberchef', 'dispatch', 'n8n',
            'kong', 'ghostwriter', 'yara', 'nemesis'
        ]

        for word in words:
            if word in tool_keywords:
                return word

        # Look for generic targets
        target_patterns = [
            r'to\s+(\w+)', r'using\s+(\w+)', r'with\s+(\w+)'
        ]

        for pattern in target_patterns:
            match = re.search(pattern, action_text.lower())
            if match:
                return match.group(1)

        return "unknown"

    def _extract_action_parameters(
        self, decisions: List[UserDecision]
    ) -> Dict[str, Any]:
        """Extract common parameters from decision context."""

        params = {}

        # Find common context keys and values
        all_context = {}
        for decision in decisions:
            for key, value in decision.context_data.items():
                if key not in all_context:
                    all_context[key] = []
                all_context[key].append(value)

        # Include parameters that have consistent values
        for key, values in all_context.items():
            if len(set(str(v) for v in values)) == 1:  # All same value
                params[key] = values[0]
            elif len(values) >= 2:  # Multiple values - use most common
                most_common = Counter(str(v) for v in values).most_common(1)
                if most_common[0][1] > 1:  # Appears more than once
                    params[key] = most_common[0][0]

        return params

    def _is_meaningful_decision_node(self, node: DecisionNode) -> bool:
        """Determine if a decision node is meaningful for automation."""

        # Must have at least one condition
        if not node.conditions:
            return False

        # Must have reasonable frequency
        if node.frequency < 2:
            return False

        # Must have reasonable success rate
        if node.success_rate < 0.6:
            return False

        # Must have confident conditions
        avg_confidence = sum(
            c.confidence for c in node.conditions) / len(node.conditions)
        if avg_confidence < 0.5:
            return False

        return True

    def _group_nodes_into_flows(
        self, nodes: List[DecisionNode]
    ) -> List[List[DecisionNode]]:
        """Group related decision nodes into complete flows."""

        # Simple grouping - in practice, this would analyze node relationships
        # For now, treat each node as a potential flow
        return [[node] for node in nodes]

    def _create_conditional_flow(
        self, node_group: List[DecisionNode]
    ) -> Optional[ConditionalFlow]:
        """Create a conditional flow from a group of nodes."""

        if not node_group:
            return None

        # Extract flow characteristics
        all_tools = set()
        total_frequency = 0
        all_conditions = []

        for node in node_group:
            if node.true_action:
                all_tools.add(node.true_action.target)
            if node.false_action:
                all_tools.add(node.false_action.target)
            total_frequency += node.frequency
            all_conditions.extend(node.conditions)

        # Calculate complexity
        complexity = min(len(all_conditions) / 5.0, 1.0)

        # Calculate automation potential
        avg_success_rate = sum(
            n.success_rate for n in node_group) / len(node_group)
        avg_confidence = sum(
            c.confidence for c in all_conditions) / len(all_conditions)
        automation_potential = (avg_success_rate + avg_confidence) / 2.0

        # Generate flow description
        condition_descriptions = [c.description for c in all_conditions[:3]]
        flow_description = f"Conditional flow based on: {', '.join(condition_descriptions)}"

        return ConditionalFlow(
            flow_id=f"flow_{hash(flow_description) % 10000}",
            flow_name=f"Conditional workflow ({len(node_group)} nodes)",
            decision_nodes=node_group,
            entry_conditions=all_conditions[:2],  # First 2 as entry conditions
            flow_description=flow_description,
            tools_involved=all_tools,
            complexity_score=complexity,
            automation_potential=automation_potential,
            frequency=total_frequency,
            performance_metrics={
                'avg_success_rate': avg_success_rate,
                'avg_confidence': avg_confidence,
                'total_conditions': len(all_conditions)
            }
        )

    def _is_viable_flow(self, flow: ConditionalFlow) -> bool:
        """Determine if a flow is viable for automation."""

        # Must have reasonable automation potential
        if flow.automation_potential < 0.6:
            return False

        # Must have meaningful frequency
        if flow.frequency < 3:
            return False

        # Must involve at least one tool
        if not flow.tools_involved:
            return False

        return True

    # Analysis methods

    def _analyze_trigger_fields(
        self, decisions: List[UserDecision]
    ) -> Dict[str, int]:
        """Analyze which context fields most often trigger decisions."""

        field_counts = Counter()

        for decision in decisions:
            for field in decision.context_data.keys():
                field_counts[field] += 1

        return dict(field_counts.most_common(10))

    def _analyze_timing_patterns(
        self, decisions: List[UserDecision]
    ) -> Dict[str, Any]:
        """Analyze timing patterns in decisions."""

        if len(decisions) < 2:
            return {}

        # Calculate time intervals between decisions
        intervals = []
        for i in range(1, len(decisions)):
            interval = decisions[i].timestamp - decisions[i-1].timestamp
            intervals.append(interval.total_seconds())

        avg_interval = sum(intervals) / len(intervals)

        return {
            'avg_interval_seconds': avg_interval,
            'min_interval_seconds': min(intervals),
            'max_interval_seconds': max(intervals),
            'decision_frequency_per_hour': 3600 / avg_interval if avg_interval > 0 else 0
        }

    def _analyze_success_factors(
        self, decisions: List[UserDecision]
    ) -> Dict[str, Any]:
        """Analyze factors that contribute to decision success."""

        successful = [d for d in decisions if d.success]
        unsuccessful = [d for d in decisions if not d.success]

        if not successful:
            return {}

        # Find context fields that correlate with success
        success_factors = {}

        # Analyze all context fields
        all_fields = set()
        for decision in decisions:
            all_fields.update(decision.context_data.keys())

        for field in all_fields:
            successful_values = []
            unsuccessful_values = []

            for decision in successful:
                if field in decision.context_data:
                    successful_values.append(decision.context_data[field])

            for decision in unsuccessful:
                if field in decision.context_data:
                    unsuccessful_values.append(decision.context_data[field])

            if successful_values:
                success_factors[field] = {
                    'appears_in_successful': len(successful_values),
                    'appears_in_unsuccessful': len(unsuccessful_values),
                    'success_correlation': len(successful_values) / len(successful)
                }

        return success_factors

    def _analyze_tool_transitions(
        self, decisions: List[UserDecision]
    ) -> Dict[str, int]:
        """Analyze patterns in tool transitions based on decisions."""

        transitions = Counter()

        for i in range(1, len(decisions)):
            prev_tool = decisions[i-1].tool_context
            curr_tool = decisions[i].tool_context

            if prev_tool != curr_tool:
                transition = f"{prev_tool} -> {curr_tool}"
                transitions[transition] += 1

        return dict(transitions.most_common(10))

    def _analyze_data_dependencies(
        self, decisions: List[UserDecision]
    ) -> List[Dict[str, Any]]:
        """Analyze data dependencies in decision sequences."""

        dependencies = []

        for i in range(1, len(decisions)):
            prev_decision = decisions[i-1]
            curr_decision = decisions[i]

            # Check for data overlap between consecutive decisions
            prev_data = set(str(v)
                            for v in prev_decision.context_data.values())
            curr_data = set(str(v)
                            for v in curr_decision.context_data.values())

            overlap = prev_data & curr_data
            if overlap:
                dependencies.append({
                    'from_decision': prev_decision.decision_id,
                    'to_decision': curr_decision.decision_id,
                    'shared_data': list(overlap),
                    'dependency_strength': len(overlap) / len(prev_data | curr_data)
                })

        return dependencies

    # n8n node generation methods

    def _create_n8n_if_node(
        self, decision_node: DecisionNode, index: int
    ) -> Dict[str, Any]:
        """Create an n8n IF node for a simple decision."""

        condition = decision_node.conditions[0]  # Single condition

        return {
            'id': f'if_node_{index}_{decision_node.node_id}',
            'type': 'n8n-nodes-base.if',
            'name': f'Decision: {condition.description}',
            'parameters': {
                'conditions': {
                    'options': {
                        'caseSensitive': True,
                        'leftValue': f"={{{{ $json.{condition.field_name} }}}}",
                        'operation': self._convert_operator_to_n8n(condition.operator),
                        'rightValue': condition.value
                    }
                }
            },
            'position': [200 + index * 300, 200],
            'typeVersion': 1
        }

    def _create_n8n_switch_node(
        self, decision_node: DecisionNode, index: int
    ) -> Dict[str, Any]:
        """Create an n8n Switch node for complex decisions."""

        rules = []
        for i, condition in enumerate(decision_node.conditions):
            rules.append({
                'name': f'Rule {i+1}',
                'value': f"={{{{ $json.{condition.field_name} }}}}",
                'operation': self._convert_operator_to_n8n(condition.operator),
                'value2': condition.value
            })

        return {
            'id': f'switch_node_{index}_{decision_node.node_id}',
            'type': 'n8n-nodes-base.switch',
            'name': f'Multi-condition Decision ({len(decision_node.conditions)} rules)',
            'parameters': {
                'rules': {
                    'rules': rules
                },
                'fallbackOutput': 3  # Default output if no rules match
            },
            'position': [200 + index * 300, 200],
            'typeVersion': 1
        }

    def _convert_operator_to_n8n(self, operator: str) -> str:
        """Convert custom operators to n8n operator format."""

        operator_mapping = {
            '==': 'equal',
            '!=': 'notEqual',
            '>': 'larger',
            '<': 'smaller',
            '>=': 'largerEqual',
            '<=': 'smallerEqual',
            'contains': 'contains',
            'starts_with': 'startsWith',
            'ends_with': 'endsWith',
            'regex': 'regex',
            'length >': 'larger'  # For array/string length
        }

        return operator_mapping.get(operator, 'equal')

    # Optimization methods

    def _detect_redundant_conditions(
        self, flow: ConditionalFlow
    ) -> Optional[Dict[str, Any]]:
        """Detect redundant conditions in a flow."""

        all_conditions = []
        for node in flow.decision_nodes:
            all_conditions.extend(node.conditions)

        # Find duplicate conditions
        condition_signatures = []
        for condition in all_conditions:
            signature = f"{condition.field_name}_{condition.operator}_{condition.value}"
            condition_signatures.append(signature)

        duplicates = [sig for sig, count in Counter(condition_signatures).items()
                      if count > 1]

        if duplicates:
            return {
                'type': 'redundant_conditions',
                'description': f'Found {len(duplicates)} redundant conditions',
                'redundant_conditions': duplicates,
                'potential_improvement': f'{len(duplicates) * 15}%'
            }

        return None

    def _suggest_condition_reordering(
        self, flow: ConditionalFlow
    ) -> Optional[Dict[str, Any]]:
        """Suggest reordering conditions for better performance."""

        # Analyze condition confidence and evaluation cost
        condition_scores = []

        for node in flow.decision_nodes:
            for condition in node.conditions:
                # Higher confidence and simpler conditions should be evaluated first
                score = condition.confidence

                # Boost score for simple conditions
                if condition.condition_type in [
                    ConditionType.BOOLEAN,
                    ConditionType.COMPARISON
                ]:
                    score += 0.2

                condition_scores.append((condition, score))

        # Sort by score (higher first)
        condition_scores.sort(key=lambda x: x[1], reverse=True)

        # Check if reordering would help
        current_order = [
            c for node in flow.decision_nodes for c in node.conditions]
        optimal_order = [item[0] for item in condition_scores]

        if current_order != optimal_order:
            return {
                'type': 'condition_reordering',
                'description': 'Reorder conditions for better performance',
                'suggested_order': [c.description for c in optimal_order],
                'potential_improvement': '20%'
            }

        return None

    def _assess_parallel_evaluation(
        self, flow: ConditionalFlow
    ) -> Optional[Dict[str, Any]]:
        """Assess opportunities for parallel condition evaluation."""

        independent_conditions = 0
        total_conditions = 0

        for node in flow.decision_nodes:
            total_conditions += len(node.conditions)

            # Simple heuristic: conditions on different fields can be parallel
            fields = set(c.field_name for c in node.conditions)
            if len(fields) > 1:
                independent_conditions += len(fields) - 1

        if independent_conditions > 0:
            parallel_potential = independent_conditions / total_conditions

            return {
                'type': 'parallel_evaluation',
                'description': 'Evaluate independent conditions in parallel',
                'parallel_conditions': independent_conditions,
                'potential_improvement': f'{parallel_potential * 30:.0f}%'
            }

        return None

    def _suggest_condition_caching(
        self, flow: ConditionalFlow
    ) -> Optional[Dict[str, Any]]:
        """Suggest caching for expensive condition evaluations."""

        expensive_conditions = []

        for node in flow.decision_nodes:
            for condition in node.conditions:
                # Consider expensive condition types
                if condition.condition_type in [
                    ConditionType.PATTERN_MATCH,
                    ConditionType.MULTI_CRITERIA
                ]:
                    expensive_conditions.append(condition)

        if expensive_conditions:
            return {
                'type': 'condition_caching',
                'description': 'Cache results of expensive condition evaluations',
                'cacheable_conditions': len(expensive_conditions),
                'potential_improvement': f'{len(expensive_conditions) * 25}%'
            }

        return None


# Utility functions

def analyze_user_decision_patterns(
    user_id: str,
    decision_history: List[Dict[str, Any]],
    time_window: timedelta = timedelta(days=21)
) -> Dict[str, Any]:
    """High-level function to analyze decision patterns for a user."""

    analyzer = LogicFlowAnalyzer()

    # Record decisions
    for record in decision_history:
        analyzer.record_user_decision(
            user_id=user_id,
            context_data=record['context_data'],
            decision_taken=record['decision_taken'],
            outcome=record['outcome'],
            success=record.get('success', True),
            tool_context=record['tool_context'],
            prior_actions=record.get('prior_actions', [])
        )

    # Analyze patterns
    decision_nodes = analyzer.analyze_decision_patterns(user_id, time_window)
    conditional_flows = analyzer.detect_conditional_flows(decision_nodes)
    context_analysis = analyzer.analyze_decision_context(
        analyzer.decision_history
    )

    return {
        'decision_nodes_found': len(decision_nodes),
        'conditional_flows_detected': len(conditional_flows),
        'context_analysis': context_analysis,
        'top_flows': conditional_flows[:3],  # Top 3 flows
        'optimization_opportunities': sum(
            len(analyzer.suggest_flow_optimizations(flow))
            for flow in conditional_flows
        ),
        'summary': {
            'most_common_conditions': list(set().union(*[
                [c.field_name for c in node.conditions]
                for node in decision_nodes[:3]
            ])),
            'high_automation_potential': len([
                f for f in conditional_flows if f.automation_potential > 0.7
            ]),
            'total_decision_frequency': sum(f.frequency for f in conditional_flows)
        }
    }
