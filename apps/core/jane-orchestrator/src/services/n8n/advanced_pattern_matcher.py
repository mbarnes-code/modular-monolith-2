"""Advanced Pattern Matching Algorithms for n8n Adaptive Workflow System.

Implements sophisticated pattern matching with confidence scoring,
temporal analysis, and cross-domain recognition for 95% accuracy target.
"""

import numpy as np
from typing import List, Dict, Any, Tuple, Optional, Set
from dataclasses import dataclass
from datetime import datetime, timedelta
from collections import defaultdict, Counter
from enum import Enum


class PatternType(Enum):
    """Types of patterns that can be detected."""
    SEQUENCE = "sequence"
    PARALLEL = "parallel"
    CYCLICAL = "cyclical"
    CROSS_DOMAIN = "cross_domain"
    TEMPORAL = "temporal"


class DomainType(Enum):
    """Domain classification for cross-domain analysis."""
    SECURITY = "security"
    PRODUCTIVITY = "productivity"
    MTG = "mtg"
    INFRASTRUCTURE = "infrastructure"


@dataclass
class PatternMatch:
    """Represents a matched pattern with confidence metrics."""
    pattern_id: str
    pattern_type: PatternType
    confidence_score: float  # 0.0 to 1.0
    support_count: int  # Number of occurrences
    temporal_strength: float  # Temporal consistency
    domain_coverage: Set[DomainType]  # Domains involved
    tools_involved: List[str]
    sequence_length: int
    avg_time_between_steps: Optional[timedelta]
    last_occurrence: datetime
    prediction_accuracy: Optional[float] = None


class AdvancedPatternMatcher:
    """Advanced pattern matching with ML-inspired algorithms."""
    
    def __init__(self, min_confidence: float = 0.7, min_support: int = 3):
        self.min_confidence = min_confidence
        self.min_support = min_support
        self.domain_tools = self._initialize_domain_mapping()
        self.confidence_weights = {
            'frequency': 0.25,
            'temporal_consistency': 0.20,
            'sequence_stability': 0.20,
            'domain_coherence': 0.15,
            'prediction_accuracy': 0.20
        }
    
    def _initialize_domain_mapping(self) -> Dict[DomainType, Set[str]]:
        """Initialize mapping of tools to domains."""
        return {
            DomainType.SECURITY: {
                'misp', 'helk', 'securityonion', 'maltrail', 'yara-x',
                'cyberchef', 'nemesis', 'apiscout', 'rita', 'blackarch'
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
                'workflow-automation', 'chroma-mcp', 'filescopemcp'
            }
        }
    
    def find_advanced_patterns(
        self, interaction_sequences: List[Any]
    ) -> List[PatternMatch]:
        """Find patterns using advanced matching algorithms."""
        patterns = []
        
        # Sequential pattern mining
        patterns.extend(
            self._mine_sequential_patterns(interaction_sequences)
        )
        
        # Parallel pattern detection
        patterns.extend(
            self._detect_parallel_patterns(interaction_sequences)
        )
        
        # Cross-domain pattern analysis
        patterns.extend(
            self._analyze_cross_domain_patterns(interaction_sequences)
        )
        
        # Temporal pattern extraction
        patterns.extend(
            self._extract_temporal_patterns(interaction_sequences)
        )
        
        # Filter by confidence and support thresholds
        qualified_patterns = [
            p for p in patterns
            if (p.confidence_score >= self.min_confidence and
                p.support_count >= self.min_support)
        ]
        
        # Sort by confidence score
        qualified_patterns.sort(
            key=lambda x: x.confidence_score, reverse=True
        )
        
        return qualified_patterns
    
    def _mine_sequential_patterns(
        self, sequences: List[Any]
    ) -> List[PatternMatch]:
        """Mine sequential patterns using modified Apriori algorithm."""
        patterns = []
        
        # Extract tool sequences
        tool_sequences = []
        for seq in sequences:
            tools = [
                interaction.tool_name for interaction in seq.interactions
            ]
            if len(tools) >= 2:
                tool_sequences.append(tools)
        
        if not tool_sequences:
            return patterns
        
        # Find frequent subsequences
        frequent_sequences = self._find_frequent_subsequences(tool_sequences)
        
        for seq, support in frequent_sequences.items():
            if len(seq) < 2:
                continue
                
            # Calculate confidence metrics
            confidence = self._calculate_sequence_confidence(
                seq, tool_sequences
            )
            temporal_strength = self._calculate_temporal_strength(
                seq, sequences
            )
            domain_coverage = self._get_domain_coverage(list(seq))
            
            # Calculate average time between steps
            avg_time = self._calculate_avg_sequence_time(seq, sequences)
            
            pattern = PatternMatch(
                pattern_id=f"seq_{hash(seq)}",
                pattern_type=PatternType.SEQUENCE,
                confidence_score=confidence,
                support_count=support,
                temporal_strength=temporal_strength,
                domain_coverage=domain_coverage,
                tools_involved=list(seq),
                sequence_length=len(seq),
                avg_time_between_steps=avg_time,
                last_occurrence=self._get_last_occurrence(seq, sequences)
            )
            
            patterns.append(pattern)
        
        return patterns
    
    def _detect_parallel_patterns(
        self, sequences: List[Any]
    ) -> List[PatternMatch]:
        """Detect patterns of parallel tool usage."""
        patterns = []
        parallel_groups = defaultdict(int)
        
        # Group interactions by time windows
        time_window = timedelta(minutes=5)
        
        for seq in sequences:
            interactions = seq.interactions
            for i, interaction in enumerate(interactions):
                concurrent_tools = {interaction.tool_name}
                
                # Find tools used concurrently
                for j, other in enumerate(interactions):
                    if i != j:
                        time_diff = abs(
                            (interaction.timestamp - 
                             other.timestamp).total_seconds()
                        )
                        if time_diff <= time_window.total_seconds():
                            concurrent_tools.add(other.tool_name)
                
                if len(concurrent_tools) >= 2:
                    group_key = tuple(sorted(concurrent_tools))
                    parallel_groups[group_key] += 1
        
        # Convert to pattern matches
        for tools, count in parallel_groups.items():
            if count >= self.min_support:
                confidence = self._calculate_parallel_confidence(
                    tools, sequences
                )
                domain_coverage = self._get_domain_coverage(list(tools))
                
                pattern = PatternMatch(
                    pattern_id=f"par_{hash(tools)}",
                    pattern_type=PatternType.PARALLEL,
                    confidence_score=confidence,
                    support_count=count,
                    temporal_strength=0.8,
                    domain_coverage=domain_coverage,
                    tools_involved=list(tools),
                    sequence_length=len(tools),
                    avg_time_between_steps=timedelta(seconds=0),
                    last_occurrence=datetime.utcnow()
                )
                
                patterns.append(pattern)
        
        return patterns
    
    def _analyze_cross_domain_patterns(
        self, sequences: List[Any]
    ) -> List[PatternMatch]:
        """Analyze patterns that span multiple domains."""
        patterns = []
        cross_domain_sequences = []
        
        # Find sequences that span multiple domains
        for seq in sequences:
            domains_in_sequence = set()
            tools_in_sequence = []
            
            for interaction in seq.interactions:
                tool = interaction.tool_name
                tools_in_sequence.append(tool)
                domain = self._get_tool_domain(tool)
                if domain:
                    domains_in_sequence.add(domain)
            
            if len(domains_in_sequence) >= 2:
                cross_domain_sequences.append({
                    'tools': tools_in_sequence,
                    'domains': domains_in_sequence,
                    'sequence': seq
                })
        
        # Group similar cross-domain patterns
        pattern_groups = defaultdict(list)
        for cd_seq in cross_domain_sequences:
            domain_sequence = [
                self._get_tool_domain(tool) for tool in cd_seq['tools']
            ]
            domain_transitions = [
                (domain_sequence[i], domain_sequence[i+1])
                for i in range(len(domain_sequence)-1)
                if domain_sequence[i] != domain_sequence[i+1]
            ]
            
            if domain_transitions:
                pattern_key = tuple(domain_transitions)
                pattern_groups[pattern_key].append(cd_seq)
        
        # Convert to pattern matches
        for transitions, group in pattern_groups.items():
            if len(group) >= self.min_support:
                confidence = self._calculate_cross_domain_confidence(
                    transitions, group
                )
                
                all_tools = set()
                all_domains = set()
                for cd_seq in group:
                    all_tools.update(cd_seq['tools'])
                    all_domains.update(cd_seq['domains'])
                
                pattern = PatternMatch(
                    pattern_id=f"cross_{hash(transitions)}",
                    pattern_type=PatternType.CROSS_DOMAIN,
                    confidence_score=confidence,
                    support_count=len(group),
                    temporal_strength=0.6,
                    domain_coverage=all_domains,
                    tools_involved=list(all_tools),
                    sequence_length=len(all_tools),
                    avg_time_between_steps=self._calculate_cross_domain_avg_time(
                        group
                    ),
                    last_occurrence=max(
                        cd_seq['sequence'].start_time for cd_seq in group
                    )
                )
                
                patterns.append(pattern)
        
        return patterns
    
    def _extract_temporal_patterns(
        self, sequences: List[Any]
    ) -> List[PatternMatch]:
        """Extract time-based patterns."""
        patterns = []
        
        # Group interactions by hour of day
        hourly_patterns = defaultdict(list)
        for seq in sequences:
            for interaction in seq.interactions:
                hour = interaction.timestamp.hour
                hourly_patterns[hour].append(interaction.tool_name)
        
        # Find frequently used tools at specific times
        for hour, tools in hourly_patterns.items():
            tool_counts = Counter(tools)
            frequent_tools = [
                tool for tool, count in tool_counts.items()
                if count >= self.min_support
            ]
            
            if frequent_tools:
                confidence = self._calculate_temporal_confidence(
                    hour, frequent_tools, sequences
                )
                
                if confidence >= self.min_confidence:
                    domain_coverage = self._get_domain_coverage(frequent_tools)
                    
                    pattern = PatternMatch(
                        pattern_id=f"temp_hour_{hour}_{hash(tuple(frequent_tools))}",
                        pattern_type=PatternType.TEMPORAL,
                        confidence_score=confidence,
                        support_count=sum(tool_counts.values()),
                        temporal_strength=0.95,
                        domain_coverage=domain_coverage,
                        tools_involved=frequent_tools,
                        sequence_length=len(frequent_tools),
                        avg_time_between_steps=timedelta(hours=1),
                        last_occurrence=datetime.utcnow()
                    )
                    
                    patterns.append(pattern)
        
        return patterns
    
    def calculate_pattern_confidence(self, pattern: PatternMatch) -> float:
        """Calculate comprehensive confidence score for a pattern."""
        scores = {}
        
        # Frequency score (normalized support)
        max_possible_support = 100
        scores['frequency'] = min(
            pattern.support_count / max_possible_support, 1.0
        )
        
        # Temporal consistency score
        scores['temporal_consistency'] = pattern.temporal_strength
        
        # Sequence stability
        scores['sequence_stability'] = self._calculate_sequence_stability(
            pattern
        )
        
        # Domain coherence
        scores['domain_coherence'] = self._calculate_domain_coherence(pattern)
        
        # Prediction accuracy
        scores['prediction_accuracy'] = (
            pattern.prediction_accuracy if pattern.prediction_accuracy 
            is not None else 0.5
        )
        
        # Weighted sum
        weighted_score = sum(
            scores[metric] * weight
            for metric, weight in self.confidence_weights.items()
        )
        
        return min(weighted_score, 1.0)
    
    # Helper methods
    
    def _find_frequent_subsequences(
        self, sequences: List[List[str]]
    ) -> Dict[Tuple[str, ...], int]:
        """Find frequent subsequences using sliding window."""
        subsequence_counts = defaultdict(int)
        
        for sequence in sequences:
            for length in range(2, len(sequence) + 1):
                for i in range(len(sequence) - length + 1):
                    subseq = tuple(sequence[i:i + length])
                    subsequence_counts[subseq] += 1
        
        return {
            subseq: count for subseq, count in subsequence_counts.items()
            if count >= self.min_support
        }
    
    def _calculate_sequence_confidence(
        self, sequence: Tuple[str, ...], all_sequences: List[List[str]]
    ) -> float:
        """Calculate confidence for a sequential pattern."""
        full_matches = 0
        prefix_matches = 0
        
        for seq in all_sequences:
            seq_str = ' '.join(seq)
            pattern_str = ' '.join(sequence)
            
            if pattern_str in seq_str:
                full_matches += 1
            
            prefix_str = ' '.join(sequence[:-1])
            if prefix_str in seq_str:
                prefix_matches += 1
        
        return full_matches / prefix_matches if prefix_matches > 0 else 0.0
    
    def _calculate_temporal_strength(
        self, sequence: Tuple[str, ...], sequences: List[Any]
    ) -> float:
        """Calculate temporal strength of a pattern."""
        time_intervals = []
        
        for seq in sequences:
            tools = [
                interaction.tool_name for interaction in seq.interactions
            ]
            timestamps = [
                interaction.timestamp for interaction in seq.interactions
            ]
            
            for i in range(len(tools) - len(sequence) + 1):
                if tuple(tools[i:i + len(sequence)]) == sequence:
                    for j in range(len(sequence) - 1):
                        interval = (
                            timestamps[i + j + 1] - timestamps[i + j]
                        ).total_seconds()
                        time_intervals.append(interval)
        
        if not time_intervals:
            return 0.0
        
        mean_interval = np.mean(time_intervals)
        std_interval = np.std(time_intervals)
        
        if mean_interval == 0:
            return 1.0
        
        cv = std_interval / mean_interval
        return max(0.0, 1.0 - min(cv, 1.0))
    
    def _get_domain_coverage(self, tools: List[str]) -> Set[DomainType]:
        """Get domain coverage for a list of tools."""
        domains = set()
        for tool in tools:
            domain = self._get_tool_domain(tool)
            if domain:
                domains.add(domain)
        return domains
    
    def _get_tool_domain(self, tool_name: str) -> Optional[DomainType]:
        """Get the domain for a specific tool."""
        for domain, tools in self.domain_tools.items():
            if tool_name.lower() in tools:
                return domain
        return None
    
    def _calculate_avg_sequence_time(
        self, sequence: Tuple[str, ...], sequences: List[Any]
    ) -> Optional[timedelta]:
        """Calculate average time between sequence steps."""
        intervals = []
        
        for seq in sequences:
            tools = [
                interaction.tool_name for interaction in seq.interactions
            ]
            timestamps = [
                interaction.timestamp for interaction in seq.interactions
            ]
            
            for i in range(len(tools) - len(sequence) + 1):
                if tuple(tools[i:i + len(sequence)]) == sequence:
                    total_time = (
                        timestamps[i + len(sequence) - 1] - timestamps[i]
                    )
                    if len(sequence) > 1:
                        avg_step_time = total_time / (len(sequence) - 1)
                    else:
                        avg_step_time = timedelta(0)
                    intervals.append(avg_step_time.total_seconds())
        
        if not intervals:
            return None
        
        avg_seconds = np.mean(intervals)
        return timedelta(seconds=avg_seconds)
    
    def _get_last_occurrence(
        self, sequence: Tuple[str, ...], sequences: List[Any]
    ) -> datetime:
        """Get the timestamp of the last occurrence of a pattern."""
        last_time = datetime.min
        
        for seq in sequences:
            tools = [
                interaction.tool_name for interaction in seq.interactions
            ]
            timestamps = [
                interaction.timestamp for interaction in seq.interactions
            ]
            
            for i in range(len(tools) - len(sequence) + 1):
                if tuple(tools[i:i + len(sequence)]) == sequence:
                    end_time = timestamps[i + len(sequence) - 1]
                    if end_time > last_time:
                        last_time = end_time
        
        return last_time if last_time != datetime.min else datetime.utcnow()
    
    def _calculate_parallel_confidence(
        self, tools: Tuple[str, ...], sequences: List[Any]
    ) -> float:
        """Calculate confidence for parallel tool usage pattern."""
        together_count = 0
        separate_count = 0
        time_window = timedelta(minutes=5)
        
        for seq in sequences:
            interactions = seq.interactions
            tool_times = {
                interaction.tool_name: interaction.timestamp
                for interaction in interactions
            }
            
            tools_in_seq = set(tool_times.keys())
            pattern_tools = set(tools)
            
            if pattern_tools.issubset(tools_in_seq):
                timestamps = [tool_times[tool] for tool in tools]
                time_span = max(timestamps) - min(timestamps)
                
                if time_span <= time_window:
                    together_count += 1
                else:
                    separate_count += 1
        
        total_occurrences = together_count + separate_count
        return (
            together_count / total_occurrences 
            if total_occurrences > 0 else 0.0
        )
    
    def _calculate_cross_domain_confidence(
        self, transitions: Tuple, group: List[Dict]
    ) -> float:
        """Calculate confidence for cross-domain patterns."""
        transition_consistency = len(group) / (len(group) + 1)
        
        all_domains = set()
        for cd_seq in group:
            all_domains.update(cd_seq['domains'])
        
        domain_diversity_bonus = min(len(all_domains) / 4, 0.2)
        
        return min(transition_consistency + domain_diversity_bonus, 1.0)
    
    def _calculate_cross_domain_avg_time(self, group: List[Dict]) -> timedelta:
        """Calculate average time for cross-domain transitions."""
        all_durations = []
        
        for cd_seq in group:
            seq = cd_seq['sequence']
            if hasattr(seq, 'end_time') and hasattr(seq, 'start_time'):
                duration = seq.end_time - seq.start_time
                all_durations.append(duration.total_seconds())
        
        if not all_durations:
            return timedelta(minutes=30)
        
        avg_seconds = np.mean(all_durations)
        return timedelta(seconds=avg_seconds)
    
    def _calculate_temporal_confidence(
        self, hour: int, tools: List[str], sequences: List[Any]
    ) -> float:
        """Calculate confidence for temporal patterns."""
        hour_usage = 0
        other_hour_usage = 0
        
        for seq in sequences:
            for interaction in seq.interactions:
                if interaction.tool_name in tools:
                    if interaction.timestamp.hour == hour:
                        hour_usage += 1
                    else:
                        other_hour_usage += 1
        
        total_usage = hour_usage + other_hour_usage
        return hour_usage / total_usage if total_usage > 0 else 0.0
    
    def _calculate_sequence_stability(self, pattern: PatternMatch) -> float:
        """Calculate sequence stability score."""
        stability_scores = {
            PatternType.SEQUENCE: 0.8,
            PatternType.PARALLEL: 0.7,
            PatternType.CROSS_DOMAIN: 0.6,
            PatternType.TEMPORAL: 0.85
        }
        
        return stability_scores.get(pattern.pattern_type, 0.7)
    
    def _calculate_domain_coherence(self, pattern: PatternMatch) -> float:
        """Calculate domain coherence score."""
        num_domains = len(pattern.domain_coverage)
        
        if num_domains == 1:
            return 1.0
        elif num_domains == 2:
            return 0.8
        elif num_domains == 3:
            return 0.6
        else:
            return 0.4