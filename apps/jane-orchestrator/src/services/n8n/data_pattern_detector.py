"""Data Transformation Pattern Recognition for n8n Workflow Automation.

This module analyzes user data transformation workflows to identify repeatable
patterns that can be automated through n8n data processing nodes. It focuses
on detecting common data manipulation, formatting, and processing sequences.
"""

import hashlib
import re
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple, Union


class TransformationType(Enum):
    """Types of data transformations that can be detected."""
    FORMAT_CONVERSION = "format_conversion"  # JSON -> CSV, XML -> JSON, etc.
    DATA_EXTRACTION = "data_extraction"  # Extract fields, regex patterns
    DATA_AGGREGATION = "data_aggregation"  # Sum, count, group by
    DATA_FILTERING = "data_filtering"  # Filter by criteria, remove duplicates
    DATA_ENRICHMENT = "data_enrichment"  # Add external data, lookups
    DATA_VALIDATION = "data_validation"  # Check formats, validate values
    DATA_NORMALIZATION = "data_normalization"  # Clean, standardize formats
    DATA_SPLITTING = "data_splitting"  # Split strings, arrays, objects
    DATA_MERGING = "data_merging"  # Combine multiple sources
    ENCODING_DECODING = "encoding_decoding"  # Base64, URL encoding, etc.


class DataFormat(Enum):
    """Supported data formats for transformation analysis."""
    JSON = "json"
    CSV = "csv"
    XML = "xml"
    YAML = "yaml"
    TEXT = "text"
    BINARY = "binary"
    TABLE = "table"
    KEY_VALUE = "key_value"
    ARRAY = "array"
    NESTED_OBJECT = "nested_object"


@dataclass
class TransformationStep:
    """Represents a single data transformation step."""
    step_id: str
    transformation_type: TransformationType
    input_format: DataFormat
    output_format: DataFormat
    # Specific operation (e.g., "json_to_csv", "extract_emails")
    operation: str
    parameters: Dict[str, Any]  # Operation parameters
    tool_used: str  # Tool that performed transformation
    input_schema: Optional[Dict[str, Any]]  # Input data structure
    output_schema: Optional[Dict[str, Any]]  # Output data structure
    success_rate: float  # Success rate of this transformation
    avg_processing_time_ms: int
    data_volume_handled: int  # Approximate records/items processed


@dataclass
class TransformationPattern:
    """Represents a detected pattern of data transformations."""
    pattern_id: str
    pattern_name: str
    transformation_steps: List[TransformationStep]
    input_formats: Set[DataFormat]
    output_formats: Set[DataFormat]
    data_flow_description: str
    tools_involved: Set[str]
    complexity_score: float  # 0.0 to 1.0
    frequency: int  # How often this pattern occurs
    automation_potential: float  # 0.0 to 1.0
    performance_metrics: Dict[str, Any]
    common_use_cases: List[str]
    error_patterns: List[Dict[str, Any]]  # Common failure modes


@dataclass
class DataTransformationSequence:
    """Represents a sequence of related data transformations."""
    sequence_id: str
    user_id: str
    steps: List[TransformationStep]
    start_time: datetime
    end_time: datetime
    total_processing_time_ms: int
    data_volume_processed: int
    success_rate: float
    context_tags: List[str]
    source_tools: Set[str]
    intermediate_formats: List[DataFormat]
    final_output_format: DataFormat


class DataPatternDetector:
    """Detects data transformation patterns for n8n automation."""

    def __init__(self):
        self.transformation_history = []
        self.format_converters = self._initialize_format_mappings()
        self.operation_signatures = self._initialize_operation_signatures()
        self.schema_cache = {}  # Cache for inferred schemas

    def _initialize_format_mappings(self) -> Dict[str, DataFormat]:
        """Initialize mapping of file extensions and content types to formats."""
        return {
            # File extensions
            '.json': DataFormat.JSON,
            '.csv': DataFormat.CSV,
            '.xml': DataFormat.XML,
            '.yml': DataFormat.YAML,
            '.yaml': DataFormat.YAML,
            '.txt': DataFormat.TEXT,
            '.bin': DataFormat.BINARY,

            # Content types
            'application/json': DataFormat.JSON,
            'text/csv': DataFormat.CSV,
            'application/xml': DataFormat.XML,
            'text/xml': DataFormat.XML,
            'application/yaml': DataFormat.YAML,
            'text/yaml': DataFormat.YAML,
            'text/plain': DataFormat.TEXT,
            'application/octet-stream': DataFormat.BINARY,

            # Data structures
            'dict': DataFormat.NESTED_OBJECT,
            'list': DataFormat.ARRAY,
            'table': DataFormat.TABLE,
            'key_value_pairs': DataFormat.KEY_VALUE
        }

    def _initialize_operation_signatures(self) -> Dict[str, TransformationType]:
        """Initialize mapping of operation patterns to transformation types."""
        return {
            # Format conversion patterns
            r'.*to_json.*|.*json_convert.*': TransformationType.FORMAT_CONVERSION,
            r'.*to_csv.*|.*csv_convert.*': TransformationType.FORMAT_CONVERSION,
            r'.*to_xml.*|.*xml_convert.*': TransformationType.FORMAT_CONVERSION,

            # Extraction patterns
            r'.*extract.*|.*parse.*|.*regex.*': TransformationType.DATA_EXTRACTION,
            r'.*find.*|.*search.*|.*match.*': TransformationType.DATA_EXTRACTION,

            # Aggregation patterns
            r'.*sum.*|.*count.*|.*aggregate.*': TransformationType.DATA_AGGREGATION,
            r'.*group.*|.*pivot.*|.*summarize.*': TransformationType.DATA_AGGREGATION,

            # Filtering patterns
            r'.*filter.*|.*where.*|.*select.*': TransformationType.DATA_FILTERING,
            r'.*remove.*|.*exclude.*|.*dedupe.*': TransformationType.DATA_FILTERING,

            # Enrichment patterns
            r'.*enrich.*|.*lookup.*|.*join.*': TransformationType.DATA_ENRICHMENT,
            r'.*merge.*|.*append.*|.*augment.*': TransformationType.DATA_ENRICHMENT,

            # Validation patterns
            r'.*validate.*|.*verify.*|.*check.*': TransformationType.DATA_VALIDATION,
            r'.*sanitize.*|.*clean.*|.*normalize.*': TransformationType.DATA_NORMALIZATION,

            # Encoding patterns
            r'.*encode.*|.*decode.*|.*base64.*': TransformationType.ENCODING_DECODING,
            r'.*hash.*|.*encrypt.*|.*decrypt.*': TransformationType.ENCODING_DECODING,

            # Splitting patterns
            r'.*split.*|.*divide.*|.*separate.*': TransformationType.DATA_SPLITTING,

            # Merging patterns
            r'.*combine.*|.*concat.*|.*union.*': TransformationType.DATA_MERGING
        }

    def record_transformation(
        self,
        user_id: str,
        tool_name: str,
        operation: str,
        input_data: Any,
        output_data: Any,
        parameters: Dict[str, Any],
        processing_time_ms: int,
        success: bool,
        context_tags: Optional[List[str]] = None
    ) -> TransformationStep:
        """Record a data transformation for pattern analysis."""

        # Infer transformation type and formats
        transformation_type = self._infer_transformation_type(
            operation, parameters)
        input_format = self._infer_data_format(input_data)
        output_format = self._infer_data_format(output_data)

        # Generate schemas
        input_schema = self._infer_schema(input_data)
        output_schema = self._infer_schema(output_data)

        # Create transformation step
        step = TransformationStep(
            step_id=self._generate_step_id(user_id, tool_name, operation),
            transformation_type=transformation_type,
            input_format=input_format,
            output_format=output_format,
            operation=operation,
            parameters=parameters,
            tool_used=tool_name,
            input_schema=input_schema,
            output_schema=output_schema,
            success_rate=1.0 if success else 0.0,
            avg_processing_time_ms=processing_time_ms,
            data_volume_handled=self._estimate_data_volume(input_data)
        )

        self.transformation_history.append({
            'step': step,
            'user_id': user_id,
            'timestamp': datetime.utcnow(),
            'context_tags': context_tags or [],
            'success': success
        })

        return step

    def analyze_transformation_sequences(
        self, user_id: str, time_window: timedelta = timedelta(days=7)
    ) -> List[DataTransformationSequence]:
        """Analyze user's data transformation sequences."""

        # Filter transformations for user and time window
        cutoff_time = datetime.utcnow() - time_window
        user_transformations = [
            record for record in self.transformation_history
            if (record['user_id'] == user_id and
                record['timestamp'] >= cutoff_time)
        ]

        if not user_transformations:
            return []

        # Sort by timestamp
        user_transformations.sort(key=lambda x: x['timestamp'])

        # Group into sequences based on temporal proximity and context
        sequences = self._group_transformations_into_sequences(
            user_transformations
        )

        # Analyze each sequence
        analyzed_sequences = []
        for sequence_steps in sequences:
            sequence = self._create_transformation_sequence(
                user_id, sequence_steps
            )
            if self._is_meaningful_sequence(sequence):
                analyzed_sequences.append(sequence)

        return analyzed_sequences

    def detect_transformation_patterns(
        self, sequences: List[DataTransformationSequence]
    ) -> List[TransformationPattern]:
        """Detect recurring transformation patterns from sequences."""

        patterns = []

        # Group similar sequences
        sequence_groups = self._group_similar_sequences(sequences)

        for group in sequence_groups:
            if len(group) >= 2:  # Minimum frequency for pattern
                pattern = self._extract_transformation_pattern(group)
                if pattern and self._is_viable_pattern(pattern):
                    patterns.append(pattern)

        # Sort by automation potential and frequency
        patterns.sort(
            key=lambda p: (p.automation_potential, p.frequency),
            reverse=True
        )

        return patterns

    def analyze_data_flow_patterns(
        self, sequences: List[DataTransformationSequence]
    ) -> Dict[str, Any]:
        """Analyze common data flow patterns across sequences."""

        # Track format transitions
        format_transitions = Counter()
        transformation_chains = defaultdict(int)
        tool_usage_patterns = defaultdict(int)

        for sequence in sequences:
            # Track format flow
            for i in range(len(sequence.steps) - 1):
                current_output = sequence.steps[i].output_format
                next_input = sequence.steps[i + 1].input_format
                transition = f"{current_output.value}->{next_input.value}"
                format_transitions[transition] += 1

            # Track transformation chains
            chain = "->".join([
                step.transformation_type.value for step in sequence.steps
            ])
            transformation_chains[chain] += 1

            # Track tool patterns
            tool_chain = "->".join([step.tool_used for step in sequence.steps])
            tool_usage_patterns[tool_chain] += 1

        return {
            'format_transitions': dict(format_transitions.most_common(10)),
            'transformation_chains': dict(transformation_chains.most_common(10)),
            'tool_usage_patterns': dict(tool_usage_patterns.most_common(10)),
            'common_formats': self._analyze_format_usage(sequences),
            'processing_performance': self._analyze_processing_performance(
                sequences
            )
        }

    def identify_optimization_opportunities(
        self, patterns: List[TransformationPattern]
    ) -> List[Dict[str, Any]]:
        """Identify opportunities to optimize transformation workflows."""

        opportunities = []

        for pattern in patterns:
            optimizations = []

            # Check for redundant transformations
            redundancy_score = self._detect_redundant_transformations(pattern)
            if redundancy_score > 0.3:
                optimizations.append({
                    'type': 'redundancy_reduction',
                    'description': 'Remove redundant transformation steps',
                    'potential_improvement': f"{redundancy_score * 100:.0f}%"
                })

            # Check for format optimization
            format_optimization = self._suggest_format_optimization(pattern)
            if format_optimization:
                optimizations.append(format_optimization)

            # Check for parallelization opportunities
            parallel_potential = self._assess_parallelization_potential(
                pattern)
            if parallel_potential > 0.4:
                optimizations.append({
                    'type': 'parallelization',
                    'description': 'Process data streams in parallel',
                    'potential_improvement': f"{parallel_potential * 100:.0f}%"
                })

            # Check for caching opportunities
            caching_potential = self._assess_caching_potential(pattern)
            if caching_potential > 0.5:
                optimizations.append({
                    'type': 'caching',
                    'description': 'Cache intermediate transformation results',
                    'potential_improvement': f"{caching_potential * 100:.0f}%"
                })

            if optimizations:
                opportunities.append({
                    'pattern_id': pattern.pattern_id,
                    'pattern_name': pattern.pattern_name,
                    'frequency': pattern.frequency,
                    'current_performance': pattern.performance_metrics,
                    'optimizations': optimizations,
                    'estimated_time_savings': self._estimate_optimization_savings(
                        pattern, optimizations
                    ),
                    'implementation_complexity': self._assess_optimization_complexity(
                        optimizations
                    )
                })

        return opportunities

    def generate_n8n_data_nodes(
        self, pattern: TransformationPattern
    ) -> List[Dict[str, Any]]:
        """Generate n8n data processing nodes for a transformation pattern."""

        nodes = []

        for i, step in enumerate(pattern.transformation_steps):
            node = self._create_n8n_node_for_step(step, i)
            if node:
                nodes.append(node)

        return nodes

    # Private helper methods

    def _infer_transformation_type(
        self, operation: str, parameters: Dict[str, Any]
    ) -> TransformationType:
        """Infer transformation type from operation name and parameters."""

        operation_lower = operation.lower()

        # Check operation signatures
        for pattern, trans_type in self.operation_signatures.items():
            if re.match(pattern, operation_lower):
                return trans_type

        # Check parameters for clues
        if 'format' in parameters or 'output_format' in parameters:
            return TransformationType.FORMAT_CONVERSION
        elif 'filter' in parameters or 'criteria' in parameters:
            return TransformationType.DATA_FILTERING
        elif 'aggregate' in parameters or 'group_by' in parameters:
            return TransformationType.DATA_AGGREGATION

        # Default based on common operation names
        if any(keyword in operation_lower for keyword in
               ['convert', 'transform', 'change']):
            return TransformationType.FORMAT_CONVERSION

        # Fallback to data processing
        return TransformationType.DATA_EXTRACTION

    def _infer_data_format(self, data: Any) -> DataFormat:
        """Infer data format from data content or type."""

        if data is None:
            return DataFormat.TEXT

        # Check if it's a string with format indicators
        if isinstance(data, str):
            data_lower = data.lower().strip()

            if data_lower.startswith('{') and data_lower.endswith('}'):
                return DataFormat.JSON
            elif data_lower.startswith('<') and data_lower.endswith('>'):
                return DataFormat.XML
            elif ',' in data and '\n' in data:
                return DataFormat.CSV
            else:
                return DataFormat.TEXT

        # Check Python data types
        elif isinstance(data, dict):
            return DataFormat.NESTED_OBJECT
        elif isinstance(data, list):
            return DataFormat.ARRAY
        elif isinstance(data, (int, float, bool)):
            return DataFormat.TEXT
        elif isinstance(data, bytes):
            return DataFormat.BINARY

        # Check if it has metadata about format
        if hasattr(data, 'content_type'):
            return self.format_converters.get(
                data.content_type, DataFormat.TEXT
            )
        elif hasattr(data, 'filename'):
            ext = '.' + data.filename.split('.')[-1].lower()
            return self.format_converters.get(ext, DataFormat.TEXT)

        return DataFormat.TEXT

    def _infer_schema(self, data: Any) -> Optional[Dict[str, Any]]:
        """Infer data schema from sample data."""

        if data is None:
            return None

        # Generate schema hash for caching
        schema_hash = hashlib.md5(str(type(data)).encode()).hexdigest()

        if schema_hash in self.schema_cache:
            return self.schema_cache[schema_hash]

        schema = None

        try:
            if isinstance(data, dict):
                schema = {
                    'type': 'object',
                    'properties': {
                        key: {'type': type(value).__name__.lower()}
                        for key, value in data.items()
                    }
                }
            elif isinstance(data, list) and data:
                first_item = data[0]
                if isinstance(first_item, dict):
                    schema = {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'properties': {
                                key: {'type': type(value).__name__.lower()}
                                for key, value in first_item.items()
                            }
                        }
                    }
                else:
                    schema = {
                        'type': 'array',
                        'items': {'type': type(first_item).__name__.lower()}
                    }
            else:
                schema = {'type': type(data).__name__.lower()}

        except Exception:
            schema = {'type': 'unknown'}

        # Cache the schema
        if schema:
            self.schema_cache[schema_hash] = schema

        return schema

    def _estimate_data_volume(self, data: Any) -> int:
        """Estimate data volume (number of records/items)."""

        if isinstance(data, (list, tuple)):
            return len(data)
        elif isinstance(data, dict):
            return len(data)
        elif isinstance(data, str):
            # Estimate based on length and newlines (for CSV-like data)
            if '\n' in data:
                return data.count('\n') + 1
            else:
                return 1
        else:
            return 1

    def _generate_step_id(
        self, user_id: str, tool_name: str, operation: str
    ) -> str:
        """Generate unique step ID."""
        timestamp = datetime.utcnow().isoformat()
        content = f"{user_id}_{tool_name}_{operation}_{timestamp}"
        return hashlib.md5(content.encode()).hexdigest()[:16]

    def _group_transformations_into_sequences(
        self, transformations: List[Dict[str, Any]]
    ) -> List[List[Dict[str, Any]]]:
        """Group transformations into logical sequences."""

        sequences = []
        current_sequence = []
        sequence_timeout = timedelta(minutes=30)  # Max gap between steps

        for transformation in transformations:
            if not current_sequence:
                current_sequence = [transformation]
                continue

            last_transformation = current_sequence[-1]
            time_gap = (transformation['timestamp'] -
                        last_transformation['timestamp'])

            # Check if transformations are related
            if (time_gap <= sequence_timeout and
                    self._transformations_are_related(
                        last_transformation, transformation
                    )):
                current_sequence.append(transformation)
            else:
                # Save current sequence and start new one
                if len(current_sequence) >= 1:
                    sequences.append(current_sequence)
                current_sequence = [transformation]

        # Add final sequence
        if current_sequence:
            sequences.append(current_sequence)

        return sequences

    def _transformations_are_related(
        self, trans1: Dict[str, Any], trans2: Dict[str, Any]
    ) -> bool:
        """Determine if two transformations are related."""

        # Check for shared context tags
        tags1 = set(trans1['context_tags'])
        tags2 = set(trans2['context_tags'])
        if tags1 & tags2:
            return True

        # Check for data format compatibility
        step1 = trans1['step']
        step2 = trans2['step']

        if step1.output_format == step2.input_format:
            return True

        # Check for similar operations
        if step1.transformation_type == step2.transformation_type:
            return True

        # Check for tool continuity
        if step1.tool_used == step2.tool_used:
            return True

        return False

    def _create_transformation_sequence(
        self, user_id: str, transformation_records: List[Dict[str, Any]]
    ) -> DataTransformationSequence:
        """Create a DataTransformationSequence from transformation records."""

        steps = [record['step'] for record in transformation_records]
        timestamps = [record['timestamp'] for record in transformation_records]

        # Calculate metrics
        total_time = sum(step.avg_processing_time_ms for step in steps)
        total_volume = sum(step.data_volume_handled for step in steps)
        success_count = sum(1 for record in transformation_records
                            if record['success'])
        success_rate = success_count / len(transformation_records)

        # Extract context and tools
        all_tags = []
        all_tools = set()
        for record in transformation_records:
            all_tags.extend(record['context_tags'])
            all_tools.add(record['step'].tool_used)

        # Determine intermediate and final formats
        intermediate_formats = []
        for step in steps[:-1]:
            intermediate_formats.append(step.output_format)

        final_format = steps[-1].output_format if steps else DataFormat.TEXT

        return DataTransformationSequence(
            sequence_id=f"seq_{user_id}_{timestamps[0].isoformat()}",
            user_id=user_id,
            steps=steps,
            start_time=timestamps[0],
            end_time=timestamps[-1],
            total_processing_time_ms=total_time,
            data_volume_processed=total_volume,
            success_rate=success_rate,
            context_tags=list(set(all_tags)),
            source_tools=all_tools,
            intermediate_formats=intermediate_formats,
            final_output_format=final_format
        )

    def _is_meaningful_sequence(
        self, sequence: DataTransformationSequence
    ) -> bool:
        """Determine if a sequence is meaningful for pattern analysis."""

        # Must have reasonable success rate
        if sequence.success_rate < 0.7:
            return False

        # Must process reasonable data volume
        if sequence.data_volume_processed < 1:
            return False

        # Must involve meaningful transformation
        if not sequence.steps:
            return False

        # Single-step sequences are less interesting unless complex
        if len(sequence.steps) == 1:
            step = sequence.steps[0]
            if step.transformation_type in [
                TransformationType.DATA_VALIDATION,
                TransformationType.DATA_NORMALIZATION
            ]:
                return False

        return True

    def _group_similar_sequences(
        self, sequences: List[DataTransformationSequence]
    ) -> List[List[DataTransformationSequence]]:
        """Group similar transformation sequences."""

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
        self, seq1: DataTransformationSequence, seq2: DataTransformationSequence
    ) -> bool:
        """Determine if two sequences are similar."""

        # Similar number of steps
        if abs(len(seq1.steps) - len(seq2.steps)) > 1:
            return False

        # Similar transformation types
        types1 = [step.transformation_type for step in seq1.steps]
        types2 = [step.transformation_type for step in seq2.steps]

        if len(types1) == len(types2):
            matches = sum(1 for t1, t2 in zip(types1, types2) if t1 == t2)
            if matches / len(types1) < 0.7:
                return False

        # Similar tools involved
        tools_overlap = len(seq1.source_tools & seq2.source_tools)
        tools_union = len(seq1.source_tools | seq2.source_tools)
        if tools_union > 0 and tools_overlap / tools_union < 0.5:
            return False

        # Similar output format
        if seq1.final_output_format != seq2.final_output_format:
            return False

        return True

    def _extract_transformation_pattern(
        self, group: List[DataTransformationSequence]
    ) -> Optional[TransformationPattern]:
        """Extract a transformation pattern from a group of similar sequences."""

        if not group:
            return None

        # Extract common transformation steps
        common_steps = self._extract_common_steps(group)
        if not common_steps:
            return None

        # Calculate pattern metrics
        all_tools = set()
        all_input_formats = set()
        all_output_formats = set()
        total_frequency = len(group)

        for sequence in group:
            all_tools.update(sequence.source_tools)
            if sequence.steps:
                all_input_formats.add(sequence.steps[0].input_format)
                all_output_formats.add(sequence.final_output_format)

        # Calculate performance metrics
        avg_processing_time = sum(
            seq.total_processing_time_ms for seq in group
        ) / len(group)
        avg_success_rate = sum(seq.success_rate for seq in group) / len(group)

        # Generate pattern description
        step_descriptions = []
        for step in common_steps:
            step_descriptions.append(
                f"{step.transformation_type.value} "
                f"({step.input_format.value}->{step.output_format.value})"
            )
        data_flow_desc = " -> ".join(step_descriptions)

        # Calculate complexity and automation potential
        complexity = self._calculate_pattern_complexity(common_steps)
        automation_potential = self._calculate_automation_potential(
            group, common_steps
        )

        return TransformationPattern(
            pattern_id=f"pattern_{hashlib.md5(data_flow_desc.encode()).hexdigest()[:16]}",
            pattern_name=f"Data transformation: {data_flow_desc}",
            transformation_steps=common_steps,
            input_formats=all_input_formats,
            output_formats=all_output_formats,
            data_flow_description=data_flow_desc,
            tools_involved=all_tools,
            complexity_score=complexity,
            frequency=total_frequency,
            automation_potential=automation_potential,
            performance_metrics={
                'avg_processing_time_ms': avg_processing_time,
                'avg_success_rate': avg_success_rate,
                'avg_data_volume': sum(
                    seq.data_volume_processed for seq in group
                ) / len(group)
            },
            common_use_cases=self._extract_use_cases(group),
            error_patterns=self._analyze_error_patterns(group)
        )

    def _extract_common_steps(
        self, group: List[DataTransformationSequence]
    ) -> List[TransformationStep]:
        """Extract common transformation steps from a group."""

        if not group:
            return []

        # Start with steps from first sequence as template
        template_steps = group[0].steps
        common_steps = []

        for step_idx, template_step in enumerate(template_steps):
            # Check if this step position exists in other sequences
            matching_steps = [template_step]

            for sequence in group[1:]:
                if step_idx < len(sequence.steps):
                    other_step = sequence.steps[step_idx]
                    if (other_step.transformation_type ==
                            template_step.transformation_type):
                        matching_steps.append(other_step)

            # If most sequences have this step, include it
            if len(matching_steps) >= len(group) * 0.7:
                # Create averaged step
                common_step = self._create_averaged_step(matching_steps)
                common_steps.append(common_step)

        return common_steps

    def _create_averaged_step(
        self, steps: List[TransformationStep]
    ) -> TransformationStep:
        """Create an averaged transformation step from multiple steps."""

        template = steps[0]

        # Calculate averages
        avg_success_rate = sum(
            step.success_rate for step in steps) / len(steps)
        avg_processing_time = sum(
            step.avg_processing_time_ms for step in steps
        ) / len(steps)
        avg_data_volume = sum(
            step.data_volume_handled for step in steps
        ) / len(steps)

        return TransformationStep(
            step_id=f"common_{template.step_id}",
            transformation_type=template.transformation_type,
            input_format=template.input_format,
            output_format=template.output_format,
            operation=template.operation,
            parameters=template.parameters.copy(),
            tool_used=template.tool_used,
            input_schema=template.input_schema,
            output_schema=template.output_schema,
            success_rate=avg_success_rate,
            avg_processing_time_ms=int(avg_processing_time),
            data_volume_handled=int(avg_data_volume)
        )

    def _is_viable_pattern(self, pattern: TransformationPattern) -> bool:
        """Determine if a pattern is viable for automation."""

        # Must have reasonable frequency
        if pattern.frequency < 2:
            return False

        # Must have good success rate
        if pattern.performance_metrics.get('avg_success_rate', 0) < 0.8:
            return False

        # Must have reasonable automation potential
        if pattern.automation_potential < 0.5:
            return False

        # Must involve meaningful transformations
        if not pattern.transformation_steps:
            return False

        return True

    def _calculate_pattern_complexity(
        self, steps: List[TransformationStep]
    ) -> float:
        """Calculate complexity score for a pattern."""

        factors = []

        # Number of steps
        step_factor = min(len(steps) / 5.0, 1.0)
        factors.append(step_factor)

        # Variety of transformation types
        unique_types = len(set(step.transformation_type for step in steps))
        type_factor = min(unique_types / 3.0, 1.0)
        factors.append(type_factor)

        # Format diversity
        all_formats = set()
        for step in steps:
            all_formats.add(step.input_format)
            all_formats.add(step.output_format)
        format_factor = min(len(all_formats) / 4.0, 1.0)
        factors.append(format_factor)

        # Processing time complexity
        avg_time = sum(
            step.avg_processing_time_ms for step in steps) / len(steps)
        # 5 seconds = high complexity
        time_factor = min(avg_time / 5000.0, 1.0)
        factors.append(time_factor)

        return sum(factors) / len(factors)

    def _calculate_automation_potential(
        self,
        group: List[DataTransformationSequence],
        steps: List[TransformationStep]
    ) -> float:
        """Calculate automation potential for a pattern."""

        factors = []

        # Frequency factor
        frequency_factor = min(len(group) / 10.0, 1.0)
        factors.append(frequency_factor)

        # Success rate factor
        avg_success = sum(seq.success_rate for seq in group) / len(group)
        factors.append(avg_success)

        # Consistency factor
        consistency = self._calculate_sequence_consistency(group)
        factors.append(consistency)

        # Determinism factor (how predictable are the transformations)
        determinism = self._assess_transformation_determinism(steps)
        factors.append(determinism)

        # Data volume factor (higher volume = more automation value)
        avg_volume = sum(
            seq.data_volume_processed for seq in group) / len(group)
        volume_factor = min(avg_volume / 100.0, 1.0)
        factors.append(volume_factor)

        return sum(factors) / len(factors)

    def _calculate_sequence_consistency(
        self, group: List[DataTransformationSequence]
    ) -> float:
        """Calculate how consistent sequences are in the group."""

        if len(group) <= 1:
            return 1.0

        # Compare step counts
        step_counts = [len(seq.steps) for seq in group]
        step_variance = max(step_counts) - min(step_counts)
        step_consistency = max(0, 1.0 - step_variance / 3.0)

        # Compare transformation types
        reference_types = [step.transformation_type for step in group[0].steps]
        type_matches = 0
        total_comparisons = 0

        for sequence in group[1:]:
            seq_types = [step.transformation_type for step in sequence.steps]
            for i, ref_type in enumerate(reference_types):
                if i < len(seq_types):
                    if ref_type == seq_types[i]:
                        type_matches += 1
                    total_comparisons += 1

        type_consistency = (type_matches / total_comparisons
                            if total_comparisons > 0 else 1.0)

        return (step_consistency + type_consistency) / 2.0

    def _assess_transformation_determinism(
        self, steps: List[TransformationStep]
    ) -> float:
        """Assess how deterministic the transformations are."""

        deterministic_types = {
            TransformationType.FORMAT_CONVERSION,
            TransformationType.DATA_EXTRACTION,
            TransformationType.DATA_NORMALIZATION,
            TransformationType.ENCODING_DECODING,
            TransformationType.DATA_SPLITTING
        }

        probabilistic_types = {
            TransformationType.DATA_ENRICHMENT,
            TransformationType.DATA_VALIDATION,
            TransformationType.DATA_AGGREGATION
        }

        deterministic_count = sum(
            1 for step in steps
            if step.transformation_type in deterministic_types
        )

        probabilistic_count = sum(
            1 for step in steps
            if step.transformation_type in probabilistic_types
        )

        total_steps = len(steps)
        if total_steps == 0:
            return 0.5

        # Higher score for more deterministic transformations
        determinism_score = (
            (deterministic_count * 1.0 + probabilistic_count * 0.7) /
            total_steps
        )

        return min(determinism_score, 1.0)

    # Analysis helper methods

    def _analyze_format_usage(
        self, sequences: List[DataTransformationSequence]
    ) -> Dict[str, Any]:
        """Analyze format usage patterns."""

        input_formats = Counter()
        output_formats = Counter()
        intermediate_formats = Counter()

        for sequence in sequences:
            if sequence.steps:
                input_formats[sequence.steps[0].input_format.value] += 1
                output_formats[sequence.final_output_format.value] += 1

                for fmt in sequence.intermediate_formats:
                    intermediate_formats[fmt.value] += 1

        return {
            'most_common_inputs': dict(input_formats.most_common(5)),
            'most_common_outputs': dict(output_formats.most_common(5)),
            'most_common_intermediates': dict(intermediate_formats.most_common(5))
        }

    def _analyze_processing_performance(
        self, sequences: List[DataTransformationSequence]
    ) -> Dict[str, Any]:
        """Analyze processing performance patterns."""

        processing_times = [seq.total_processing_time_ms for seq in sequences]
        data_volumes = [seq.data_volume_processed for seq in sequences]
        success_rates = [seq.success_rate for seq in sequences]

        return {
            'avg_processing_time_ms': sum(processing_times) / len(processing_times),
            'min_processing_time_ms': min(processing_times),
            'max_processing_time_ms': max(processing_times),
            'avg_data_volume': sum(data_volumes) / len(data_volumes),
            'avg_success_rate': sum(success_rates) / len(success_rates),
            'throughput_items_per_second': self._calculate_throughput(sequences)
        }

    def _calculate_throughput(
        self, sequences: List[DataTransformationSequence]
    ) -> float:
        """Calculate average throughput in items per second."""

        throughputs = []
        for sequence in sequences:
            if sequence.total_processing_time_ms > 0:
                throughput = (
                    sequence.data_volume_processed /
                    (sequence.total_processing_time_ms / 1000.0)
                )
                throughputs.append(throughput)

        return sum(throughputs) / len(throughputs) if throughputs else 0.0

    def _extract_use_cases(
        self, group: List[DataTransformationSequence]
    ) -> List[str]:
        """Extract common use cases from sequence group."""

        use_cases = []

        # Analyze context tags for use cases
        all_tags = []
        for sequence in group:
            all_tags.extend(sequence.context_tags)

        tag_counts = Counter(all_tags)
        common_tags = [tag for tag, count in tag_counts.most_common(3)]

        # Generate use case descriptions based on patterns
        if common_tags:
            use_cases.append(f"Data processing for {', '.join(common_tags)}")

        # Analyze transformation patterns
        step_types = []
        for sequence in group:
            for step in sequence.steps:
                step_types.append(step.transformation_type.value)

        type_counts = Counter(step_types)
        if type_counts:
            most_common_type = type_counts.most_common(1)[0][0]
            use_cases.append(f"Automated {most_common_type.replace('_', ' ')}")

        return use_cases[:3]  # Return top 3 use cases

    def _analyze_error_patterns(
        self, group: List[DataTransformationSequence]
    ) -> List[Dict[str, Any]]:
        """Analyze error patterns in transformation sequences."""

        error_patterns = []

        # Analyze sequences with low success rates
        problematic_sequences = [
            seq for seq in group if seq.success_rate < 0.9
        ]

        if problematic_sequences:
            # Common failure points
            failure_steps = defaultdict(int)
            for sequence in problematic_sequences:
                for step in sequence.steps:
                    if step.success_rate < 0.9:
                        failure_key = f"{step.transformation_type.value}_{step.tool_used}"
                        failure_steps[failure_key] += 1

            if failure_steps:
                most_common_failure = max(
                    failure_steps.items(), key=lambda x: x[1])
                error_patterns.append({
                    'type': 'step_failure',
                    'description': f"Common failure in {most_common_failure[0]}",
                    'frequency': most_common_failure[1],
                    'mitigation': 'Add error handling and retry logic'
                })

        return error_patterns

    # Optimization methods

    def _detect_redundant_transformations(
        self, pattern: TransformationPattern
    ) -> float:
        """Detect redundant transformation steps in a pattern."""

        steps = pattern.transformation_steps
        if len(steps) <= 1:
            return 0.0

        redundancy_score = 0.0

        # Check for consecutive similar transformations
        for i in range(len(steps) - 1):
            current = steps[i]
            next_step = steps[i + 1]

            # Same transformation type
            if current.transformation_type == next_step.transformation_type:
                redundancy_score += 0.3

            # Round-trip format conversion
            if (current.output_format == next_step.input_format and
                    current.input_format == next_step.output_format):
                redundancy_score += 0.5

        return min(redundancy_score, 1.0)

    def _suggest_format_optimization(
        self, pattern: TransformationPattern
    ) -> Optional[Dict[str, Any]]:
        """Suggest format optimizations for a pattern."""

        steps = pattern.transformation_steps
        if len(steps) <= 1:
            return None

        # Find format conversion chains
        format_chain = []
        for step in steps:
            if step.transformation_type == TransformationType.FORMAT_CONVERSION:
                format_chain.append((step.input_format, step.output_format))

        if len(format_chain) >= 2:
            return {
                'type': 'format_optimization',
                'description': 'Optimize format conversion chain',
                'suggestion': 'Convert directly to final format to reduce steps',
                'potential_improvement': f"{len(format_chain) * 20}%"
            }

        return None

    def _assess_parallelization_potential(
        self, pattern: TransformationPattern
    ) -> float:
        """Assess potential for parallelizing transformations."""

        steps = pattern.transformation_steps
        if len(steps) <= 1:
            return 0.0

        # Check for independent transformations
        independent_steps = 0

        for i, step in enumerate(steps):
            # Check if step depends on previous step's output
            has_dependency = False

            if i > 0:
                prev_step = steps[i - 1]
                # Simple heuristic: same input/output format suggests dependency
                if prev_step.output_format == step.input_format:
                    has_dependency = True

            if not has_dependency:
                independent_steps += 1

        # Higher score for more independent steps
        return min(independent_steps / len(steps), 1.0)

    def _assess_caching_potential(self, pattern: TransformationPattern) -> float:
        """Assess potential for caching intermediate results."""

        caching_score = 0.0

        # High-frequency patterns benefit more from caching
        if pattern.frequency >= 5:
            caching_score += 0.4

        # Expensive transformations benefit from caching
        avg_processing_time = pattern.performance_metrics.get(
            'avg_processing_time_ms', 0
        )
        if avg_processing_time > 2000:  # More than 2 seconds
            caching_score += 0.3

        # Large data volumes benefit from caching
        avg_volume = pattern.performance_metrics.get('avg_data_volume', 0)
        if avg_volume > 50:
            caching_score += 0.3

        return min(caching_score, 1.0)

    def _estimate_optimization_savings(
        self, pattern: TransformationPattern, optimizations: List[Dict[str, Any]]
    ) -> Dict[str, float]:
        """Estimate time savings from optimizations."""

        current_time = pattern.performance_metrics.get(
            'avg_processing_time_ms', 1000
        )

        total_improvement = 0.0
        for optimization in optimizations:
            improvement_str = optimization.get('potential_improvement', '0%')
            improvement_pct = float(improvement_str.rstrip('%')) / 100.0
            total_improvement += improvement_pct

        # Cap total improvement at 80%
        total_improvement = min(total_improvement, 0.8)

        time_savings_ms = current_time * total_improvement
        executions_per_month = pattern.frequency * 4  # Estimate monthly

        return {
            'time_savings_per_execution_ms': time_savings_ms,
            'estimated_monthly_executions': executions_per_month,
            'estimated_monthly_savings_ms': time_savings_ms * executions_per_month,
            'estimated_monthly_savings_minutes': (
                time_savings_ms * executions_per_month
            ) / (1000 * 60)
        }

    def _assess_optimization_complexity(
        self, optimizations: List[Dict[str, Any]]
    ) -> str:
        """Assess implementation complexity of optimizations."""

        complexity_scores = {
            'redundancy_reduction': 1,
            'format_optimization': 2,
            'parallelization': 4,
            'caching': 3
        }

        total_complexity = sum(
            complexity_scores.get(opt['type'], 2) for opt in optimizations
        )

        if total_complexity <= 3:
            return 'low'
        elif total_complexity <= 7:
            return 'medium'
        else:
            return 'high'

    def _create_n8n_node_for_step(
        self, step: TransformationStep, index: int
    ) -> Optional[Dict[str, Any]]:
        """Create an n8n node configuration for a transformation step."""

        node_type_mapping = {
            TransformationType.FORMAT_CONVERSION: 'n8n-nodes-base.function',
            TransformationType.DATA_EXTRACTION: 'n8n-nodes-base.jsonExtract',
            TransformationType.DATA_FILTERING: 'n8n-nodes-base.filter',
            TransformationType.DATA_AGGREGATION: 'n8n-nodes-base.aggregate',
            TransformationType.DATA_NORMALIZATION: 'n8n-nodes-base.function',
            TransformationType.ENCODING_DECODING: 'n8n-nodes-base.crypto',
            TransformationType.DATA_SPLITTING: 'n8n-nodes-base.splitInBatches',
            TransformationType.DATA_MERGING: 'n8n-nodes-base.merge'
        }

        node_type = node_type_mapping.get(
            step.transformation_type, 'n8n-nodes-base.function'
        )

        return {
            'id': f'step_{index}_{step.step_id}',
            'type': node_type,
            'name': f'{step.transformation_type.value.title()} Step {index + 1}',
            'parameters': {
                'operation': step.operation,
                'input_format': step.input_format.value,
                'output_format': step.output_format.value,
                **step.parameters
            },
            'position': [200 + index * 250, 200],
            'typeVersion': 1
        }


# Utility functions

def analyze_transformation_workflow(
    user_id: str,
    transformation_history: List[Dict[str, Any]],
    time_window: timedelta = timedelta(days=14)
) -> Dict[str, Any]:
    """High-level function to analyze transformation workflows for a user."""

    detector = DataPatternDetector()

    # Record transformations
    for record in transformation_history:
        detector.record_transformation(
            user_id=user_id,
            tool_name=record['tool'],
            operation=record['operation'],
            input_data=record['input_data'],
            output_data=record['output_data'],
            parameters=record.get('parameters', {}),
            processing_time_ms=record.get('processing_time_ms', 1000),
            success=record.get('success', True),
            context_tags=record.get('context_tags', [])
        )

    # Analyze sequences and patterns
    sequences = detector.analyze_transformation_sequences(user_id, time_window)
    patterns = detector.detect_transformation_patterns(sequences)
    data_flow_analysis = detector.analyze_data_flow_patterns(sequences)
    optimizations = detector.identify_optimization_opportunities(patterns)

    return {
        'sequences_found': len(sequences),
        'patterns_detected': len(patterns),
        'optimization_opportunities': len(optimizations),
        'data_flow_analysis': data_flow_analysis,
        'top_patterns': patterns[:5],  # Top 5 patterns
        'recommended_optimizations': optimizations[:3],  # Top 3 optimizations
        'summary': {
            'most_common_transformations': list(set().union(*[
                [step.transformation_type.value for step in p.transformation_steps]
                for p in patterns[:3]
            ])),
            'most_used_formats': list(data_flow_analysis['common_formats']['most_common_inputs'].keys()),
            'high_automation_potential': len([
                p for p in patterns if p.automation_potential > 0.7
            ])
        }
    }
