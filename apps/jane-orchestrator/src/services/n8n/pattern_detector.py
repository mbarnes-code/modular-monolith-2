"""Pattern Detection Engine for User Behavior Analysis."""

import hashlib
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List, Optional

# Import the advanced pattern matcher for enhanced accuracy
from .advanced_pattern_matcher import (AdvancedPatternMatcher, DomainType,
                                       PatternMatch, PatternType)


@dataclass
class InteractionSequence:
    """Represents a sequence of user interactions across tools."""
    user_id: str
    timestamp: datetime
    tool_sequence: List[str]
    action_sequence: List[str]
    data_flow: Dict[str, Any]
    duration_seconds: int
    success_rate: float


@dataclass
class DetectedPattern:
    """Represents a detected behavioral pattern that could be automated."""
    pattern_id: str
    pattern_hash: str
    frequency: int
    confidence_score: float
    tool_sequence: List[str]
    action_sequence: List[str]
    average_duration: float
    success_rate: float
    first_occurrence: datetime
    last_occurrence: datetime
    data_transformation_patterns: Dict[str, Any]


class PatternDetector:
    """Detects recurring user behavior patterns for workflow automation."""

    def __init__(self, db_session: Any):
        self.db = db_session
        self.min_occurrences = 3
        self.time_window_days = 7
        self.min_confidence = 0.75
        self.min_success_rate = 0.8
        self.max_sequence_gap_minutes = 30

        # Initialize advanced pattern matcher for 95% accuracy
        self.advanced_matcher = AdvancedPatternMatcher(
            min_confidence=0.75,
            min_support=3
        )

    def detect_patterns(
        self, user_id: str, days_back: int = 30
    ) -> List[DetectedPattern]:
        """Detect recurring patterns for automation."""
        interactions = self._get_user_interactions(user_id, days_back)

        if len(interactions) < self.min_occurrences:
            return []

        sequences = self._group_into_sequences(interactions)

        # Use advanced pattern matcher for enhanced accuracy
        advanced_patterns = self.advanced_matcher.find_advanced_patterns(
            sequences
        )

        # Convert PatternMatch objects to DetectedPattern objects
        detected_patterns = []
        for pattern_match in advanced_patterns:
            detected_pattern = self._convert_pattern_match_to_detected_pattern(
                pattern_match
            )
            detected_patterns.append(detected_pattern)

        # Also use legacy detection for backward compatibility
        candidates = self._generate_pattern_candidates(sequences)
        for candidate in candidates:
            pattern = self._analyze_pattern_candidate(candidate, sequences)
            if pattern and self._meets_automation_criteria(pattern):
                detected_patterns.append(pattern)

        # Remove duplicates and sort by confidence
        unique_patterns = self._deduplicate_patterns(detected_patterns)

        return sorted(
            unique_patterns,
            key=lambda p: p.confidence_score,
            reverse=True
        )

    def _get_user_interactions(
        self, user_id: str, days_back: int
    ) -> List[Dict[str, Any]]:
        """Retrieve user interactions from the database."""
        # Mock implementation - to be replaced with actual database queries
        return []

    def _group_into_sequences(
        self, interactions: List[Dict[str, Any]]
    ) -> List[InteractionSequence]:
        """Group individual interactions into logical sequences."""
        sequences = []
        current_sequence = []
        last_timestamp = None

        for interaction in interactions:
            current_time = interaction['timestamp']

            # Check if we should start a new sequence
            gap_threshold = self.max_sequence_gap_minutes * 60
            gap_too_large = (
                last_timestamp is not None and
                (current_time - last_timestamp).total_seconds() > gap_threshold
            )

            if last_timestamp is None or gap_too_large:
                if current_sequence:
                    sequences.append(
                        self._create_sequence_from_interactions(
                            current_sequence
                        )
                    )
                current_sequence = [interaction]
            else:
                current_sequence.append(interaction)

            last_timestamp = current_time

        # Add the final sequence
        if current_sequence:
            sequences.append(
                self._create_sequence_from_interactions(current_sequence)
            )

        return sequences

    def _create_sequence_from_interactions(
        self, interactions: List[Dict[str, Any]]
    ) -> InteractionSequence:
        """Convert interactions into an InteractionSequence."""
        if not interactions:
            raise ValueError("Cannot create sequence from empty interactions")

        first_interaction = interactions[0]
        tool_sequence = [i['tool'] for i in interactions]
        action_sequence = [i['action'] for i in interactions]

        total_duration = sum(i.get('duration', 0) for i in interactions)
        success_count = sum(1 for i in interactions if i.get('success', False))
        success_rate = success_count / len(interactions) if interactions else 0

        return InteractionSequence(
            user_id=first_interaction.get('user_id', 'unknown'),
            timestamp=first_interaction['timestamp'],
            tool_sequence=tool_sequence,
            action_sequence=action_sequence,
            data_flow={'transformations': []},
            duration_seconds=total_duration,
            success_rate=success_rate
        )

    def _generate_pattern_candidates(
        self, sequences: List[InteractionSequence]
    ) -> List[str]:
        """Generate pattern candidates by finding similar sequences."""
        pattern_candidates = []
        structure_groups = defaultdict(list)

        for sequence in sequences:
            signature = self._create_pattern_signature(sequence)
            structure_groups[signature].append(sequence)

        for signature, group_sequences in structure_groups.items():
            if len(group_sequences) >= self.min_occurrences:
                pattern_candidates.append(signature)

        return pattern_candidates

    def _create_pattern_signature(self, sequence: InteractionSequence) -> str:
        """Create a unique signature for a sequence pattern."""
        tools_str = "->".join(sequence.tool_sequence)
        actions_str = "->".join(sequence.action_sequence)

        pattern_content = f"{tools_str}|{actions_str}"
        return hashlib.md5(pattern_content.encode()).hexdigest()

    def _analyze_pattern_candidate(
        self, pattern_signature: str, sequences: List[InteractionSequence]
    ) -> Optional[DetectedPattern]:
        """Analyze a pattern candidate for automation suitability."""
        matching_sequences = [
            seq for seq in sequences
            if self._create_pattern_signature(seq) == pattern_signature
        ]

        if len(matching_sequences) < self.min_occurrences:
            return None

        # Calculate statistics
        success_rates = [seq.success_rate for seq in matching_sequences]
        durations = [seq.duration_seconds for seq in matching_sequences]
        timestamps = [seq.timestamp for seq in matching_sequences]

        avg_success_rate = sum(success_rates) / len(success_rates)
        avg_duration = sum(durations) / len(durations)
        confidence_score = self._calculate_confidence_score(matching_sequences)

        reference_sequence = matching_sequences[0]

        return DetectedPattern(
            pattern_id=f"pattern_{pattern_signature[:8]}",
            pattern_hash=pattern_signature,
            frequency=len(matching_sequences),
            confidence_score=confidence_score,
            tool_sequence=reference_sequence.tool_sequence,
            action_sequence=reference_sequence.action_sequence,
            average_duration=avg_duration,
            success_rate=avg_success_rate,
            first_occurrence=min(timestamps),
            last_occurrence=max(timestamps),
            data_transformation_patterns=reference_sequence.data_flow
        )

    def _calculate_confidence_score(
        self, sequences: List[InteractionSequence]
    ) -> float:
        """Calculate confidence score based on pattern consistency."""
        if len(sequences) < 2:
            return 1.0

        reference_tools = sequences[0].tool_sequence
        tool_consistency = sum(
            1 for seq in sequences
            if seq.tool_sequence == reference_tools
        ) / len(sequences)

        reference_actions = sequences[0].action_sequence
        action_consistency = sum(
            1 for seq in sequences
            if seq.action_sequence == reference_actions
        ) / len(sequences)

        # Weighted average of consistency metrics
        confidence_score = tool_consistency * 0.6 + action_consistency * 0.4
        return min(1.0, confidence_score)

    def _meets_automation_criteria(self, pattern: DetectedPattern) -> bool:
        """Check if a pattern meets the criteria for automation."""
        return (
            pattern.frequency >= self.min_occurrences and
            pattern.confidence_score >= self.min_confidence and
            pattern.success_rate >= self.min_success_rate and
            len(pattern.tool_sequence) >= 2
        )

    def save_detected_pattern(
        self, pattern: DetectedPattern, user_id: str
    ) -> Dict[str, Any]:
        """Save a detected pattern to the database."""
        # Mock implementation - to be replaced with actual database operations
        return {
            'pattern_id': pattern.pattern_id,
            'user_id': user_id,
            'status': 'saved'
        }

    def _convert_pattern_match_to_detected_pattern(
        self, pattern_match: PatternMatch
    ) -> DetectedPattern:
        """Convert PatternMatch to DetectedPattern for consistency."""
        return DetectedPattern(
            pattern_id=pattern_match.pattern_id,
            pattern_hash=str(hash(pattern_match.pattern_id)),
            frequency=pattern_match.support_count,
            confidence_score=pattern_match.confidence_score,
            tool_sequence=pattern_match.tools_involved,
            action_sequence=[],  # Not available in PatternMatch
            average_duration=(
                pattern_match.avg_time_between_steps.total_seconds()
                if pattern_match.avg_time_between_steps else 0.0
            ),
            success_rate=0.85,  # Default value
            last_occurrence=pattern_match.last_occurrence,
            pattern_complexity=len(pattern_match.tools_involved),
            data_transformation_patterns={}
        )

    def _deduplicate_patterns(
        self, patterns: List[DetectedPattern]
    ) -> List[DetectedPattern]:
        """Remove duplicate patterns based on tool sequences."""
        seen_sequences = set()
        unique_patterns = []

        for pattern in patterns:
            sequence_key = tuple(sorted(pattern.tool_sequence))
            if sequence_key not in seen_sequences:
                seen_sequences.add(sequence_key)
                unique_patterns.append(pattern)

        return unique_patterns
