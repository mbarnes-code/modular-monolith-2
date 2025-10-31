"""Cross-Tool Interaction Sequence Detection for n8n Workflow Automation.

This module analyzes user interactions across the 37 integrated tools to detect
sequences that can be automated through n8n workflows, focusing on cross-domain
patterns and tool transition logic.
"""

from collections import defaultdict, deque
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple


class InteractionType(Enum):
    """Types of tool interactions that can be detected."""
    DATA_IMPORT = "data_import"
    DATA_EXPORT = "data_export"
    DATA_TRANSFORM = "data_transform"
    QUERY_EXECUTION = "query_execution"
    REPORT_GENERATION = "report_generation"
    CONFIGURATION_CHANGE = "configuration_change"
    ANALYSIS_REQUEST = "analysis_request"
    WORKFLOW_EXECUTION = "workflow_execution"


class DomainType(Enum):
    """Domain classification for cross-domain analysis."""
    SECURITY = "security"
    PRODUCTIVITY = "productivity"
    MTG = "mtg"
    INFRASTRUCTURE = "infrastructure"


@dataclass
class ToolInteraction:
    """Represents a single interaction with an integrated tool."""
    interaction_id: str
    user_id: str
    tool_name: str
    domain: DomainType
    interaction_type: InteractionType
    timestamp: datetime
    data_payload: Dict[str, Any]
    output_data: Optional[Dict[str, Any]]
    success: bool
    duration_ms: int
    context_tags: List[str]  # Tags that help identify related interactions


@dataclass
class InteractionSequence:
    """Represents a sequence of related tool interactions."""
    sequence_id: str
    user_id: str
    interactions: List[ToolInteraction]
    start_time: datetime
    end_time: datetime
    total_duration_ms: int
    domains_involved: Set[DomainType]
    tools_involved: Set[str]
    data_flow_chain: List[Tuple[str, str]]  # (source_tool, target_tool)
    success_rate: float
    complexity_score: float


@dataclass
class CrossToolPattern:
    """Represents a detected pattern of cross-tool interactions."""
    pattern_id: str
    pattern_name: str
    tool_sequence: List[str]
    domain_transitions: List[Tuple[DomainType, DomainType]]
    interaction_types: List[InteractionType]
    data_dependencies: List[Dict[str, Any]]  # Data flow requirements
    timing_constraints: Dict[str, timedelta]  # Max time between steps
    success_criteria: Dict[str, Any]
    frequency: int  # How often this pattern occurs
    automation_potential: float  # 0.0 to 1.0


class InteractionAnalyzer:
    """Analyzes cross-tool interaction sequences for automation."""

    def __init__(self):
        self.domain_tools = self._initialize_domain_mapping()
        self.interaction_buffer = deque(maxlen=1000)  # Recent interactions
        self.sequence_timeout = timedelta(hours=2)  # Max time for sequence
        self.min_sequence_length = 2
        self.max_sequence_length = 10

    def _initialize_domain_mapping(self) -> Dict[DomainType, Set[str]]:
        """Initialize mapping of tools to domains."""
        return {
            DomainType.SECURITY: {
                'misp', 'helk', 'securityonion', 'maltrail', 'yara-x',
                'cyberchef', 'nemesis', 'apiscout', 'rita', 'blackarch',
                'meterpreter', 'lscript', 'onex'
            },
            DomainType.PRODUCTIVITY: {
                'n8n', 'mealie', 'dispatch', 'actual', 'firecrawl',
                'goose', 'it-tools', 'inspector'
            },
            DomainType.MTG: {
                'commander-spellbook', 'mtg-commander-map',
                'mtg-scripting-toolkit', 'card-analysis'
            },
            DomainType.INFRASTRUCTURE: {
                'kong', 'ghostwriter', 'kasmvnc', 'mcp-servers',
                'workflow-automation', 'chroma-mcp', 'filescopemcp',
                'malwarebazaar-mcp', 'mcp-virustotal', 'n8n-mcp-server'
            }
        }

    def record_interaction(self, interaction: ToolInteraction) -> None:
        """Record a new tool interaction for sequence analysis."""
        # Classify the tool domain if not already set
        if not interaction.domain:
            interaction.domain = self._classify_tool_domain(
                interaction.tool_name
            )

        # Add to interaction buffer
        self.interaction_buffer.append(interaction)

        # Trigger sequence detection for real-time analysis
        self._detect_active_sequences(interaction.user_id)

    def analyze_interaction_sequences(
        self, user_id: str, time_window: timedelta = timedelta(days=30)
    ) -> List[InteractionSequence]:
        """Analyze user interactions to identify meaningful sequences."""
        # Get user interactions within time window
        cutoff_time = datetime.utcnow() - time_window
        user_interactions = [
            interaction for interaction in self.interaction_buffer
            if (interaction.user_id == user_id and
                interaction.timestamp >= cutoff_time)
        ]

        if not user_interactions:
            return []

        # Sort by timestamp
        user_interactions.sort(key=lambda x: x.timestamp)

        # Group interactions into sequences
        sequences = self._group_interactions_into_sequences(user_interactions)

        # Analyze each sequence for cross-tool patterns
        analyzed_sequences = []
        for sequence in sequences:
            if self._is_meaningful_sequence(sequence):
                sequence.data_flow_chain = self._analyze_data_flow(sequence)
                sequence.complexity_score = self._calculate_complexity_score(
                    sequence
                )
                analyzed_sequences.append(sequence)

        return analyzed_sequences

    def detect_cross_tool_patterns(
        self, sequences: List[InteractionSequence]
    ) -> List[CrossToolPattern]:
        """Detect recurring cross-tool patterns from interaction sequences."""
        patterns = []

        # Group sequences by similar characteristics
        sequence_groups = self._group_similar_sequences(sequences)

        for group in sequence_groups:
            if len(group) >= 3:  # Minimum frequency for pattern recognition
                pattern = self._extract_pattern_from_group(group)
                if pattern and self._is_automatable_pattern(pattern):
                    patterns.append(pattern)

        # Sort patterns by automation potential and frequency
        patterns.sort(
            key=lambda p: (p.automation_potential, p.frequency),
            reverse=True
        )

        return patterns

    def analyze_domain_transitions(
        self, sequences: List[InteractionSequence]
    ) -> Dict[str, Any]:
        """Analyze patterns in domain transitions across sequences."""
        transition_counts = defaultdict(int)
        transition_timings = defaultdict(list)
        domain_efficiency = defaultdict(list)

        for sequence in sequences:
            interactions = sequence.interactions

            # Track domain transitions
            for i in range(len(interactions) - 1):
                current_domain = interactions[i].domain
                next_domain = interactions[i + 1].domain

                if current_domain != next_domain:
                    transition_key = (
                        f"{current_domain.value}->{next_domain.value}"
                    )
                    transition_counts[transition_key] += 1

                    # Calculate transition timing
                    transition_time = (
                        interactions[i + 1].timestamp -
                        interactions[i].timestamp
                    )
                    transition_timings[transition_key].append(
                        transition_time.total_seconds()
                    )

            # Track domain efficiency (success rate and duration)
            domain_stats = defaultdict(list)
            for interaction in interactions:
                domain_stats[interaction.domain.value].append({
                    'success': interaction.success,
                    'duration': interaction.duration_ms
                })

            for domain, stats in domain_stats.items():
                success_rate = sum(
                    1 for s in stats if s['success']) / len(stats)
                avg_duration = sum(s['duration'] for s in stats) / len(stats)
                domain_efficiency[domain].append({
                    'success_rate': success_rate,
                    'avg_duration': avg_duration
                })

        return {
            'transition_frequencies': dict(transition_counts),
            'transition_timings': {
                k: {
                    'avg_seconds': sum(v) / len(v) if v else 0,
                    'min_seconds': min(v) if v else 0,
                    'max_seconds': max(v) if v else 0
                }
                for k, v in transition_timings.items()
            },
            'domain_efficiency': {
                domain: {
                    'avg_success_rate': sum(
                        e['success_rate'] for e in efficiency
                    ) / len(efficiency) if efficiency else 0,
                    'avg_duration_ms': sum(
                        e['avg_duration'] for e in efficiency
                    ) / len(efficiency) if efficiency else 0
                }
                for domain, efficiency in domain_efficiency.items()
            }
        }

    def identify_automation_opportunities(
        self, patterns: List[CrossToolPattern]
    ) -> List[Dict[str, Any]]:
        """Identify specific automation opportunities from detected patterns."""
        opportunities = []

        for pattern in patterns:
            if pattern.automation_potential >= 0.7:  # High automation potential
                opportunity = {
                    'pattern_id': pattern.pattern_id,
                    'pattern_name': pattern.pattern_name,
                    'automation_type': self._determine_automation_type(pattern),
                    'estimated_time_savings': self._estimate_time_savings(pattern),
                    'implementation_complexity': self._assess_implementation_complexity(pattern),
                    'required_integrations': self._identify_required_integrations(pattern),
                    'success_probability': self._calculate_success_probability(pattern),
                    'user_impact': self._assess_user_impact(pattern),
                    'n8n_workflow_template': self._generate_n8n_template_outline(pattern)
                }
                opportunities.append(opportunity)

        return opportunities

    def _detect_active_sequences(self, user_id: str) -> None:
        """Detect if the user is currently in an active interaction sequence."""
        recent_interactions = [
            interaction for interaction in self.interaction_buffer
            if (interaction.user_id == user_id and
                datetime.utcnow() - interaction.timestamp <= timedelta(minutes=30))
        ]

        if len(recent_interactions) >= 2:
            # Check if this might be part of a recurring pattern
            sequence = InteractionSequence(
                sequence_id=f"active_{user_id}_{datetime.utcnow().isoformat()}",
                user_id=user_id,
                interactions=recent_interactions,
                start_time=recent_interactions[0].timestamp,
                end_time=recent_interactions[-1].timestamp,
                total_duration_ms=int(
                    (recent_interactions[-1].timestamp -
                     recent_interactions[0].timestamp).total_seconds() * 1000
                ),
                domains_involved=set(i.domain for i in recent_interactions),
                tools_involved=set(i.tool_name for i in recent_interactions),
                data_flow_chain=[],
                success_rate=sum(
                    1 for i in recent_interactions if i.success) / len(recent_interactions),
                complexity_score=0.0
            )

            # Could trigger real-time workflow suggestions here
            if self._is_meaningful_sequence(sequence):
                # Log potential automation opportunity
                pass

    def _classify_tool_domain(self, tool_name: str) -> DomainType:
        """Classify a tool into its appropriate domain."""
        tool_lower = tool_name.lower()

        for domain, tools in self.domain_tools.items():
            if any(tool in tool_lower for tool in tools):
                return domain

        # Default to infrastructure if unknown
        return DomainType.INFRASTRUCTURE

    def _group_interactions_into_sequences(
        self, interactions: List[ToolInteraction]
    ) -> List[InteractionSequence]:
        """Group interactions into logical sequences based on timing and context."""
        sequences = []
        current_sequence = []

        for interaction in interactions:
            if not current_sequence:
                current_sequence = [interaction]
                continue

            # Check if this interaction belongs to the current sequence
            last_interaction = current_sequence[-1]
            time_gap = interaction.timestamp - last_interaction.timestamp

            # Group criteria: time gap, context tags, data dependencies
            if (time_gap <= self.sequence_timeout and
                    self._interactions_are_related(last_interaction, interaction)):
                current_sequence.append(interaction)
            else:
                # Finalize current sequence and start new one
                if len(current_sequence) >= self.min_sequence_length:
                    sequences.append(self._create_sequence_from_interactions(
                        current_sequence
                    ))
                current_sequence = [interaction]

        # Add final sequence
        if len(current_sequence) >= self.min_sequence_length:
            sequences.append(self._create_sequence_from_interactions(
                current_sequence
            ))

        return sequences

    def _interactions_are_related(
        self, interaction1: ToolInteraction, interaction2: ToolInteraction
    ) -> bool:
        """Determine if two interactions are related and should be in same sequence."""
        # Check for shared context tags
        shared_tags = set(interaction1.context_tags) & set(
            interaction2.context_tags)
        if shared_tags:
            return True

        # Check for data dependencies
        if (interaction1.output_data and interaction2.data_payload and
                self._has_data_dependency(interaction1.output_data, interaction2.data_payload)):
            return True

        # Check for domain continuity or logical transitions
        domain_transitions = [
            # Security -> Task management
            (DomainType.SECURITY, DomainType.PRODUCTIVITY),
            # Tasks -> Infrastructure
            (DomainType.PRODUCTIVITY, DomainType.INFRASTRUCTURE),
            # Security -> Infrastructure
            (DomainType.SECURITY, DomainType.INFRASTRUCTURE),
            (DomainType.MTG, DomainType.PRODUCTIVITY),  # MTG -> Productivity
        ]

        transition = (interaction1.domain, interaction2.domain)
        if transition in domain_transitions or interaction1.domain == interaction2.domain:
            return True

        return False

    def _has_data_dependency(
        self, output_data: Dict[str, Any], input_data: Dict[str, Any]
    ) -> bool:
        """Check if input data depends on output data from previous interaction."""
        # Simple heuristic: check for matching data types or IDs
        if not output_data or not input_data:
            return False

        # Check for ID references
        output_ids = set()
        input_refs = set()

        def extract_ids(data, id_set):
            if isinstance(data, dict):
                for key, value in data.items():
                    if 'id' in key.lower() and isinstance(value, (str, int)):
                        id_set.add(str(value))
                    elif isinstance(value, dict):
                        extract_ids(value, id_set)
                    elif isinstance(value, list):
                        for item in value:
                            if isinstance(item, dict):
                                extract_ids(item, id_set)

        extract_ids(output_data, output_ids)
        extract_ids(input_data, input_refs)

        return bool(output_ids & input_refs)

    def _create_sequence_from_interactions(
        self, interactions: List[ToolInteraction]
    ) -> InteractionSequence:
        """Create an InteractionSequence from a list of interactions."""
        return InteractionSequence(
            sequence_id=f"seq_{interactions[0].user_id}_{interactions[0].timestamp.isoformat()}",
            user_id=interactions[0].user_id,
            interactions=interactions,
            start_time=interactions[0].timestamp,
            end_time=interactions[-1].timestamp,
            total_duration_ms=int(
                (interactions[-1].timestamp -
                 interactions[0].timestamp).total_seconds() * 1000
            ),
            domains_involved=set(i.domain for i in interactions),
            tools_involved=set(i.tool_name for i in interactions),
            data_flow_chain=[],
            success_rate=sum(
                1 for i in interactions if i.success) / len(interactions),
            complexity_score=0.0
        )

    def _is_meaningful_sequence(self, sequence: InteractionSequence) -> bool:
        """Determine if a sequence is meaningful for automation analysis."""
        # Must involve multiple tools
        if len(sequence.tools_involved) < 2:
            return False

        # Must have reasonable success rate
        if sequence.success_rate < 0.7:
            return False

        # Must not be too short or too long
        if not (self.min_sequence_length <= len(sequence.interactions) <= self.max_sequence_length):
            return False

        # Must have some cross-domain activity or repeated tool usage
        if len(sequence.domains_involved) < 2 and len(sequence.tools_involved) < 3:
            return False

        return True

    def _analyze_data_flow(
        self, sequence: InteractionSequence
    ) -> List[Tuple[str, str]]:
        """Analyze data flow between tools in a sequence."""
        data_flow = []

        for i in range(len(sequence.interactions) - 1):
            current = sequence.interactions[i]
            next_interaction = sequence.interactions[i + 1]

            # Check if data flows from current to next
            if (current.output_data and next_interaction.data_payload and
                    self._has_data_dependency(current.output_data, next_interaction.data_payload)):
                data_flow.append(
                    (current.tool_name, next_interaction.tool_name))

        return data_flow

    def _calculate_complexity_score(self, sequence: InteractionSequence) -> float:
        """Calculate complexity score for a sequence (0.0 to 1.0)."""
        factors = []

        # Number of tools involved
        tool_factor = min(len(sequence.tools_involved) / 5.0, 1.0)
        factors.append(tool_factor)

        # Number of domains involved
        domain_factor = min(len(sequence.domains_involved) / 4.0, 1.0)
        factors.append(domain_factor)

        # Data flow complexity
        data_flow_factor = min(len(sequence.data_flow_chain) / 3.0, 1.0)
        factors.append(data_flow_factor)

        # Duration complexity
        duration_hours = sequence.total_duration_ms / (1000 * 60 * 60)
        # 2 hours = max complexity
        duration_factor = min(duration_hours / 2.0, 1.0)
        factors.append(duration_factor)

        return sum(factors) / len(factors)

    def _group_similar_sequences(
        self, sequences: List[InteractionSequence]
    ) -> List[List[InteractionSequence]]:
        """Group similar sequences for pattern detection."""
        groups = []
        used_sequences = set()

        for i, sequence in enumerate(sequences):
            if i in used_sequences:
                continue

            group = [sequence]
            used_sequences.add(i)

            # Find similar sequences
            for j, other_sequence in enumerate(sequences[i+1:], i+1):
                if j in used_sequences:
                    continue

                if self._sequences_are_similar(sequence, other_sequence):
                    group.append(other_sequence)
                    used_sequences.add(j)

            groups.append(group)

        return groups

    def _sequences_are_similar(
        self, seq1: InteractionSequence, seq2: InteractionSequence
    ) -> bool:
        """Determine if two sequences are similar enough to be grouped."""
        # Similar tool usage
        tools_overlap = len(seq1.tools_involved & seq2.tools_involved)
        tools_similarity = tools_overlap / \
            len(seq1.tools_involved | seq2.tools_involved)

        if tools_similarity < 0.6:
            return False

        # Similar domain involvement
        domains_overlap = len(seq1.domains_involved & seq2.domains_involved)
        if domains_overlap == 0:
            return False

        # Similar sequence length
        length_ratio = min(len(seq1.interactions), len(
            seq2.interactions)) / max(len(seq1.interactions), len(seq2.interactions))
        if length_ratio < 0.7:
            return False

        return True

    def _extract_pattern_from_group(
        self, group: List[InteractionSequence]
    ) -> Optional[CrossToolPattern]:
        """Extract a common pattern from a group of similar sequences."""
        if not group:
            return None

        # Find common tools and domains
        common_tools = set(group[0].tools_involved)
        common_domains = set(group[0].domains_involved)

        for sequence in group[1:]:
            common_tools &= sequence.tools_involved
            common_domains &= sequence.domains_involved

        if not common_tools:
            return None

        # Extract common tool sequence
        tool_sequence = self._extract_common_tool_sequence(group)

        # Extract domain transitions
        domain_transitions = self._extract_common_domain_transitions(group)

        # Calculate automation potential
        automation_potential = self._calculate_automation_potential(group)

        return CrossToolPattern(
            pattern_id=f"pattern_{hash(tuple(sorted(common_tools)))}",
            pattern_name=f"Cross-tool pattern: {', '.join(sorted(common_tools))}",
            tool_sequence=tool_sequence,
            domain_transitions=domain_transitions,
            interaction_types=self._extract_common_interaction_types(group),
            data_dependencies=self._extract_data_dependencies(group),
            timing_constraints=self._extract_timing_constraints(group),
            success_criteria=self._extract_success_criteria(group),
            frequency=len(group),
            automation_potential=automation_potential
        )

    def _is_automatable_pattern(self, pattern: CrossToolPattern) -> bool:
        """Determine if a pattern is suitable for automation."""
        # Must have reasonable frequency
        if pattern.frequency < 3:
            return False

        # Must have high automation potential
        if pattern.automation_potential < 0.6:
            return False

        # Must involve meaningful tool sequence
        if len(pattern.tool_sequence) < 2:
            return False

        return True

    # Helper methods for pattern extraction

    def _extract_common_tool_sequence(
        self, group: List[InteractionSequence]
    ) -> List[str]:
        """Extract the most common tool sequence from a group."""
        # Simplified: return tools from first sequence as template
        if group:
            return [i.tool_name for i in group[0].interactions]
        return []

    def _extract_common_domain_transitions(
        self, group: List[InteractionSequence]
    ) -> List[Tuple[DomainType, DomainType]]:
        """Extract common domain transitions from a group."""
        transitions = []
        for sequence in group:
            seq_transitions = []
            for i in range(len(sequence.interactions) - 1):
                current_domain = sequence.interactions[i].domain
                next_domain = sequence.interactions[i + 1].domain
                if current_domain != next_domain:
                    seq_transitions.append((current_domain, next_domain))
            transitions.extend(seq_transitions)

        # Return most common transitions
        from collections import Counter
        common_transitions = Counter(transitions).most_common(3)
        return [transition for transition, count in common_transitions]

    def _extract_common_interaction_types(
        self, group: List[InteractionSequence]
    ) -> List[InteractionType]:
        """Extract common interaction types from a group."""
        all_types = []
        for sequence in group:
            all_types.extend(
                [i.interaction_type for i in sequence.interactions])

        from collections import Counter
        common_types = Counter(all_types).most_common(5)
        return [interaction_type for interaction_type, count in common_types]

    def _extract_data_dependencies(
        self, group: List[InteractionSequence]
    ) -> List[Dict[str, Any]]:
        """Extract data dependencies from a group of sequences."""
        # Simplified implementation
        return [{"type": "data_flow", "description": "Requires data flow analysis"}]

    def _extract_timing_constraints(
        self, group: List[InteractionSequence]
    ) -> Dict[str, timedelta]:
        """Extract timing constraints from a group of sequences."""
        # Calculate average durations between steps
        durations = []
        for sequence in group:
            if len(sequence.interactions) > 1:
                total_duration = sequence.total_duration_ms / 1000  # seconds
                avg_step_duration = total_duration / \
                    (len(sequence.interactions) - 1)
                durations.append(avg_step_duration)

        if durations:
            avg_duration = sum(durations) / len(durations)
            return {"max_step_duration": timedelta(seconds=avg_duration * 2)}

        return {"max_step_duration": timedelta(minutes=30)}

    def _extract_success_criteria(self, group: List[InteractionSequence]) -> Dict[str, Any]:
        """Extract success criteria from a group of sequences."""
        avg_success_rate = sum(seq.success_rate for seq in group) / len(group)
        return {
            "min_success_rate": max(0.8, avg_success_rate - 0.1),
            "required_tools": len(group[0].tools_involved)
        }

    def _calculate_automation_potential(
        self, group: List[InteractionSequence]
    ) -> float:
        """Calculate automation potential for a group of sequences."""
        factors = []

        # Frequency factor
        frequency_factor = min(len(group) / 10.0, 1.0)
        factors.append(frequency_factor)

        # Success rate factor
        avg_success = sum(seq.success_rate for seq in group) / len(group)
        factors.append(avg_success)

        # Consistency factor (how similar are the sequences)
        tools_consistency = self._calculate_tools_consistency(group)
        factors.append(tools_consistency)

        # Complexity factor (not too simple, not too complex)
        avg_complexity = sum(
            seq.complexity_score for seq in group) / len(group)
        # Best at 0.5 complexity
        complexity_factor = 1.0 - abs(0.5 - avg_complexity)
        factors.append(complexity_factor)

        return sum(factors) / len(factors)

    def _calculate_tools_consistency(self, group: List[InteractionSequence]) -> float:
        """Calculate how consistent tool usage is across sequences."""
        if not group:
            return 0.0

        # Get tool usage patterns
        all_tool_sets = [seq.tools_involved for seq in group]
        reference_tools = all_tool_sets[0]

        consistencies = []
        for tool_set in all_tool_sets[1:]:
            overlap = len(reference_tools & tool_set)
            union = len(reference_tools | tool_set)
            consistency = overlap / union if union > 0 else 0
            consistencies.append(consistency)

        return sum(consistencies) / len(consistencies) if consistencies else 1.0

    # Automation opportunity assessment methods

    def _determine_automation_type(self, pattern: CrossToolPattern) -> str:
        """Determine the type of automation suitable for this pattern."""
        if len(pattern.domain_transitions) > 2:
            return "complex_cross_domain"
        elif len(pattern.tool_sequence) > 5:
            return "multi_step_workflow"
        elif len(pattern.data_dependencies) > 0:
            return "data_driven_automation"
        else:
            return "simple_sequence"

    def _estimate_time_savings(self, pattern: CrossToolPattern) -> Dict[str, float]:
        """Estimate time savings from automating this pattern."""
        # Simplified estimation based on tool count and frequency
        manual_time_minutes = len(pattern.tool_sequence) * 5  # 5 min per tool
        automation_time_minutes = 2  # 2 min to trigger automation
        savings_per_execution = manual_time_minutes - automation_time_minutes

        monthly_executions = pattern.frequency * 2  # Estimate growth
        monthly_savings = savings_per_execution * monthly_executions

        return {
            "savings_per_execution_minutes": savings_per_execution,
            "estimated_monthly_executions": monthly_executions,
            "estimated_monthly_savings_minutes": monthly_savings,
            "estimated_monthly_savings_hours": monthly_savings / 60
        }

    def _assess_implementation_complexity(self, pattern: CrossToolPattern) -> str:
        """Assess the complexity of implementing automation for this pattern."""
        complexity_score = 0

        # Domain complexity
        complexity_score += len(pattern.domain_transitions) * 2

        # Tool integration complexity
        complexity_score += len(pattern.tool_sequence)

        # Data dependency complexity
        complexity_score += len(pattern.data_dependencies) * 3

        if complexity_score <= 5:
            return "low"
        elif complexity_score <= 15:
            return "medium"
        else:
            return "high"

    def _identify_required_integrations(
        self, pattern: CrossToolPattern
    ) -> List[Dict[str, str]]:
        """Identify integrations required for automation."""
        integrations = []

        for tool in pattern.tool_sequence:
            domain = self._classify_tool_domain(tool)
            integrations.append({
                "tool": tool,
                "domain": domain.value,
                "integration_type": "service_adapter",
                "priority": "high" if tool in pattern.tool_sequence[:3] else "medium"
            })

        return integrations

    def _calculate_success_probability(self, pattern: CrossToolPattern) -> float:
        """Calculate probability of successful automation implementation."""
        factors = []

        # Pattern frequency (more frequent = higher success probability)
        frequency_factor = min(pattern.frequency / 20.0, 1.0)
        factors.append(frequency_factor)

        # Automation potential
        factors.append(pattern.automation_potential)

        # Implementation complexity (lower complexity = higher success)
        complexity = self._assess_implementation_complexity(pattern)
        complexity_factor = {"low": 0.9,
                             "medium": 0.7, "high": 0.4}[complexity]
        factors.append(complexity_factor)

        # Tool maturity (assume established tools have better APIs)
        maturity_factor = 0.8  # Average maturity
        factors.append(maturity_factor)

        return sum(factors) / len(factors)

    def _assess_user_impact(self, pattern: CrossToolPattern) -> Dict[str, Any]:
        """Assess the impact on users from automating this pattern."""
        return {
            "user_effort_reduction": f"{len(pattern.tool_sequence) * 15}%",
            "context_switching_reduction": f"{len(pattern.domain_transitions) * 25}%",
            "error_reduction_potential": "30%",  # Conservative estimate
            "consistency_improvement": "high" if pattern.frequency > 5 else "medium"
        }

    def _generate_n8n_template_outline(
        self, pattern: CrossToolPattern
    ) -> Dict[str, Any]:
        """Generate an outline for n8n workflow template."""
        nodes = []
        connections = []

        # Create trigger node
        nodes.append({
            "id": "trigger",
            "type": "n8n-nodes-base.manualTrigger",
            "name": f"Trigger: {pattern.pattern_name}",
            "parameters": {}
        })

        # Create nodes for each tool in sequence
        for i, tool in enumerate(pattern.tool_sequence):
            domain = self._classify_tool_domain(tool)
            node_id = f"{tool}_node_{i}"

            nodes.append({
                "id": node_id,
                "type": f"custom.{domain.value}.{tool}",
                "name": f"{tool.title()} Action",
                "parameters": {
                    "operation": "execute",
                    "domain": domain.value
                }
            })

            # Create connection from previous node
            prev_id = "trigger" if i == 0 else f"{pattern.tool_sequence[i-1]}_node_{i-1}"
            connections.append({
                "source": prev_id,
                "target": node_id,
                "type": "main"
            })

        return {
            "name": f"Auto-generated: {pattern.pattern_name}",
            "description": f"Automated workflow for {len(pattern.tool_sequence)} tool sequence",
            "nodes": nodes,
            "connections": connections,
            "settings": {
                "executionOrder": "v1",
                "saveManualExecutions": True,
                "callerPolicy": "workflowsFromSameOwner"
            }
        }


# Utility functions for interaction analysis

def create_tool_interaction(
    user_id: str,
    tool_name: str,
    interaction_type: InteractionType,
    data_payload: Dict[str, Any],
    output_data: Optional[Dict[str, Any]] = None,
    success: bool = True,
    duration_ms: int = 1000,
    context_tags: Optional[List[str]] = None
) -> ToolInteraction:
    """Helper function to create a ToolInteraction object."""
    return ToolInteraction(
        interaction_id=f"{user_id}_{tool_name}_{datetime.utcnow().isoformat()}",
        user_id=user_id,
        tool_name=tool_name,
        domain=DomainType.INFRASTRUCTURE,  # Will be classified automatically
        interaction_type=interaction_type,
        timestamp=datetime.utcnow(),
        data_payload=data_payload,
        output_data=output_data,
        success=success,
        duration_ms=duration_ms,
        context_tags=context_tags or []
    )


def analyze_user_workflow_patterns(
    user_id: str,
    interaction_history: List[ToolInteraction]
) -> Dict[str, Any]:
    """High-level function to analyze workflow patterns for a user."""
    analyzer = InteractionAnalyzer()

    # Record all interactions
    for interaction in interaction_history:
        analyzer.record_interaction(interaction)

    # Analyze sequences
    sequences = analyzer.analyze_interaction_sequences(user_id)

    # Detect patterns
    patterns = analyzer.detect_cross_tool_patterns(sequences)

    # Analyze domain transitions
    domain_analysis = analyzer.analyze_domain_transitions(sequences)

    # Identify automation opportunities
    opportunities = analyzer.identify_automation_opportunities(patterns)

    return {
        'sequences_detected': len(sequences),
        'patterns_found': len(patterns),
        'automation_opportunities': len(opportunities),
        'domain_analysis': domain_analysis,
        'top_opportunities': opportunities[:5],  # Top 5 opportunities
        'summary': {
            'most_common_tools': list(set().union(*[p.tool_sequence for p in patterns[:3]])),
            'cross_domain_frequency': len([p for p in patterns if len(p.domain_transitions) > 0]),
            'high_potential_automations': len([o for o in opportunities if o['success_probability'] > 0.8])
        }
    }
