"""
Real-Time Analysis Intelligence Service

Enhanced real-time processing capabilities based on business logic patterns from:
- Maltrail: Multi-protocol traffic analysis with 400K+ indicators (O(1) lookups)
- Kong: High-performance request routing with sub-millisecond latency
- HELK: Real-time event correlation across multiple data sources
- n8n: Workflow execution with real-time dependency processing
- Actual Budget: Real-time spreadsheet calculations with change propagation

Provides optional real-time intelligence that applications can use for:
- High-throughput pattern matching and detection
- Real-time correlation across multiple data streams
- Performance monitoring and bottleneck detection
- Streaming analysis with minimal latency
"""

import hashlib
import json
import re
import time
from collections import defaultdict, deque
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List

from ..shared.interfaces import (ConfidenceLevel, IntelligenceInsight,
                                 IntelligenceRequest,
                                 IntelligenceServiceInterface)
from ..shared.utils import IntelligenceCache


class AnalysisMode(Enum):
    """Types of real-time analysis"""
    PATTERN_MATCHING = "pattern_matching"
    CORRELATION = "correlation"
    PERFORMANCE = "performance"
    THREAT_DETECTION = "threat_detection"
    WORKFLOW_MONITORING = "workflow_monitoring"


@dataclass
class RealTimeEvent:
    """Represents a real-time event for analysis"""
    timestamp: float
    event_type: str
    source: str
    data: Dict[str, Any]
    metadata: Dict[str, Any]


@dataclass
class PatternRule:
    """Pattern rule for real-time matching"""
    id: str
    pattern: str
    rule_type: str  # regex, exact, contains, etc.
    severity: str
    action: str
    metadata: Dict[str, Any]


@dataclass
class PerformanceMetric:
    """Performance tracking metric"""
    name: str
    value: float
    timestamp: float
    threshold: float
    status: str  # normal, warning, critical


class RealTimeAnalysisIntelligenceService(IntelligenceServiceInterface):
    """
    High-performance real-time analysis service.

    Based on real business logic patterns:
    - Maltrail traffic analysis engine (O(1) pattern lookups)
    - Kong request routing optimization
    - HELK multi-source event correlation
    - n8n workflow execution monitoring
    - Actual Budget real-time calculation propagation
    """

    def __init__(self):
        self.cache = IntelligenceCache(max_size=10000, ttl_seconds=300)

        # Pattern matching infrastructure (based on Maltrail design)
        self._pattern_rules: Dict[str, PatternRule] = {}
        self._compiled_patterns: Dict[str, re.Pattern] = {}
        self._exact_patterns: Dict[str, PatternRule] = {}  # O(1) lookups

        # Real-time event processing
        self._event_buffer: deque = deque(maxlen=10000)
        self._correlation_windows: Dict[str,
                                        List[RealTimeEvent]] = defaultdict(list)

        # Performance monitoring (based on Kong patterns)
        self._performance_metrics: Dict[str, PerformanceMetric] = {}
        self._latency_samples: Dict[str, deque] = defaultdict(
            lambda: deque(maxlen=1000))

        # Streaming processing state
        self._processing_stats = {
            'events_processed': 0,
            'patterns_matched': 0,
            'correlations_found': 0,
            'avg_processing_time': 0.0
        }

    async def analyze(
        self, request: IntelligenceRequest
    ) -> List[IntelligenceInsight]:
        """Perform real-time analysis on streaming data"""
        start_time = time.time()

        try:
            analysis_mode = AnalysisMode(
                request.data.get('mode', 'pattern_matching')
            )

            insights = []

            if analysis_mode == AnalysisMode.PATTERN_MATCHING:
                insights.extend(await self._perform_pattern_analysis(request))

            elif analysis_mode == AnalysisMode.CORRELATION:
                insights.extend(await self._perform_correlation_analysis(request))

            elif analysis_mode == AnalysisMode.PERFORMANCE:
                insights.extend(await self._perform_performance_analysis(request))

            elif analysis_mode == AnalysisMode.THREAT_DETECTION:
                insights.extend(await self._perform_threat_analysis(request))

            elif analysis_mode == AnalysisMode.WORKFLOW_MONITORING:
                insights.extend(await self._perform_workflow_analysis(request))

            # Update processing statistics
            processing_time = time.time() - start_time
            self._update_processing_stats(processing_time)

            return insights

        except Exception as e:
            return [IntelligenceInsight(
                type="realtime_analysis_error",
                confidence=ConfidenceLevel.LOW,
                summary=f"Real-time analysis failed: {str(e)}",
                details={"error": str(
                    e), "processing_time": time.time() - start_time},
                recommendations=[
                    "Check input data format",
                    "Verify pattern rules are valid",
                    "Monitor system resources"
                ],
                metadata={"service": "realtime_analysis", "error": True}
            )]

    async def _perform_pattern_analysis(
        self, request: IntelligenceRequest
    ) -> List[IntelligenceInsight]:
        """
        High-performance pattern matching based on Maltrail design
        """
        insights = []
        events = request.data.get('events', [])

        # Load pattern rules if provided
        if 'pattern_rules' in request.data:
            await self._load_pattern_rules(request.data['pattern_rules'])

        # Process each event with O(1) and O(log n) lookups
        for event_data in events:
            event = RealTimeEvent(
                timestamp=event_data.get('timestamp', time.time()),
                event_type=event_data.get('type', 'unknown'),
                source=event_data.get('source', 'unknown'),
                data=event_data.get('data', {}),
                metadata=event_data.get('metadata', {})
            )

            matches = await self._match_patterns(event)
            for match in matches:
                severity = match.get('severity', 'medium')
                confidence = self._calculate_pattern_confidence(match)

                insights.append(IntelligenceInsight(
                    type="pattern_match_detected",
                    confidence=confidence,
                    summary=f"Pattern matched: {match['rule_id']}",
                    details={
                        "rule_id": match['rule_id'],
                        "pattern": match['pattern'],
                        "matched_data": match['matched_data'],
                        "event_source": event.source,
                        "severity": severity,
                        "timestamp": event.timestamp
                    },
                    recommendations=self._get_pattern_recommendations(match),
                    metadata={"service": "realtime_analysis",
                              "analysis": "pattern"}
                ))

        return insights

    async def _perform_correlation_analysis(
        self, request: IntelligenceRequest
    ) -> List[IntelligenceInsight]:
        """
        Multi-source event correlation based on HELK patterns
        """
        insights = []
        events = request.data.get('events', [])
        correlation_window = request.data.get('correlation_window_seconds', 60)

        # Add events to correlation buffer
        for event_data in events:
            event = RealTimeEvent(
                timestamp=event_data.get('timestamp', time.time()),
                event_type=event_data.get('type', 'unknown'),
                source=event_data.get('source', 'unknown'),
                data=event_data.get('data', {}),
                metadata=event_data.get('metadata', {})
            )

            self._add_event_to_correlation(event, correlation_window)

        # Find correlations across different sources
        correlations = await self._find_event_correlations(correlation_window)

        for correlation in correlations:
            confidence = self._calculate_correlation_confidence(correlation)

            insights.append(IntelligenceInsight(
                type="event_correlation_detected",
                confidence=confidence,
                summary=f"Correlated events across {len(correlation['sources'])} sources",
                details={
                    "correlation_id": correlation['id'],
                    "event_count": len(correlation['events']),
                    "sources": correlation['sources'],
                    "time_span": correlation['time_span'],
                    "correlation_strength": correlation['strength'],
                    "patterns": correlation['patterns']
                },
                recommendations=[
                    "Investigate potential coordinated activity",
                    "Review security logs for related events",
                    "Consider automated response if appropriate"
                ],
                metadata={"service": "realtime_analysis",
                          "analysis": "correlation"}
            ))

        return insights

    async def _perform_performance_analysis(
        self, request: IntelligenceRequest
    ) -> List[IntelligenceInsight]:
        """
        Performance monitoring based on Kong and routing patterns
        """
        insights = []
        metrics = request.data.get('metrics', [])

        for metric_data in metrics:
            metric = PerformanceMetric(
                name=metric_data['name'],
                value=metric_data['value'],
                timestamp=metric_data.get('timestamp', time.time()),
                threshold=metric_data.get('threshold', 1000),
                status='normal'
            )

            # Update metric history and detect anomalies
            await self._update_performance_metric(metric)
            anomalies = await self._detect_performance_anomalies(metric)

            for anomaly in anomalies:
                confidence = ConfidenceLevel.HIGH if anomaly[
                    'severity'] == 'critical' else ConfidenceLevel.MEDIUM

                insights.append(IntelligenceInsight(
                    type="performance_anomaly_detected",
                    confidence=confidence,
                    summary=f"Performance anomaly in {metric.name}",
                    details={
                        "metric_name": metric.name,
                        "current_value": metric.value,
                        "threshold": metric.threshold,
                        "severity": anomaly['severity'],
                        "trend": anomaly['trend'],
                        "duration": anomaly.get('duration', 0)
                    },
                    recommendations=[
                        "Scale resources if performance is degraded",
                        "Check for resource bottlenecks",
                        "Review system logs for errors",
                        "Consider load balancing adjustments"
                    ],
                    metadata={"service": "realtime_analysis",
                              "analysis": "performance"}
                ))

        return insights

    async def _perform_threat_analysis(
        self, request: IntelligenceRequest
    ) -> List[IntelligenceInsight]:
        """
        Security threat analysis combining multiple detection methods
        """
        insights = []
        events = request.data.get('events', [])
        threat_indicators = request.data.get('threat_indicators', [])

        # Load threat indicators for fast lookup
        threat_lookup = {}
        for indicator in threat_indicators:
            key = indicator.get('value', '').lower()
            threat_lookup[key] = indicator

        # Analyze events for threat indicators
        for event_data in events:
            event = RealTimeEvent(
                timestamp=event_data.get('timestamp', time.time()),
                event_type=event_data.get('type', 'unknown'),
                source=event_data.get('source', 'unknown'),
                data=event_data.get('data', {}),
                metadata=event_data.get('metadata', {})
            )

            threats = await self._detect_threats_in_event(event, threat_lookup)

            for threat in threats:
                severity = threat.get('severity', 'medium')
                confidence = self._calculate_threat_confidence(threat)

                insights.append(IntelligenceInsight(
                    type="threat_detected",
                    confidence=confidence,
                    summary=f"Threat indicator detected: {threat['type']}",
                    details={
                        "threat_type": threat['type'],
                        "indicator_value": threat['indicator'],
                        "event_source": event.source,
                        "severity": severity,
                        "context": threat.get('context', {}),
                        "timestamp": event.timestamp
                    },
                    recommendations=[
                        "Block malicious indicator if confirmed",
                        "Investigate source of threat activity",
                        "Review related network traffic",
                        "Update threat intelligence feeds"
                    ],
                    metadata={"service": "realtime_analysis",
                              "analysis": "threat"}
                ))

        return insights

    async def _perform_workflow_analysis(
        self, request: IntelligenceRequest
    ) -> List[IntelligenceInsight]:
        """
        Workflow monitoring based on n8n execution patterns
        """
        insights = []
        workflow_events = request.data.get('workflow_events', [])

        # Track workflow execution state
        workflow_states = defaultdict(dict)

        for event_data in workflow_events:
            workflow_id = event_data.get('workflow_id')
            execution_id = event_data.get('execution_id')
            node_id = event_data.get('node_id')
            status = event_data.get('status')
            timestamp = event_data.get('timestamp', time.time())

            if workflow_id and execution_id:
                key = f"{workflow_id}:{execution_id}"
                if key not in workflow_states:
                    workflow_states[key] = {
                        'workflow_id': workflow_id,
                        'execution_id': execution_id,
                        'start_time': timestamp,
                        'nodes': {},
                        'status': 'running'
                    }

                if node_id:
                    workflow_states[key]['nodes'][node_id] = {
                        'status': status,
                        'timestamp': timestamp,
                        'duration': event_data.get('duration', 0)
                    }

        # Analyze workflow performance and issues
        for state in workflow_states.values():
            analysis = await self._analyze_workflow_execution(state)

            if analysis.get('issues'):
                for issue in analysis['issues']:
                    confidence = self._calculate_workflow_confidence(issue)

                    insights.append(IntelligenceInsight(
                        type="workflow_issue_detected",
                        confidence=confidence,
                        summary=f"Workflow issue: {issue['type']}",
                        details={
                            "workflow_id": state['workflow_id'],
                            "execution_id": state['execution_id'],
                            "issue_type": issue['type'],
                            "affected_nodes": issue.get('nodes', []),
                            "duration": issue.get('duration', 0),
                            "severity": issue.get('severity', 'medium')
                        },
                        recommendations=[
                            "Review workflow configuration",
                            "Check node dependencies and timeouts",
                            "Monitor resource usage during execution",
                            "Consider workflow optimization"
                        ],
                        metadata={"service": "realtime_analysis",
                                  "analysis": "workflow"}
                    ))

        return insights

    # Helper methods for pattern matching (based on Maltrail design)

    async def _load_pattern_rules(self, rules: List[Dict[str, Any]]):
        """Load and compile pattern rules for fast matching"""
        for rule_data in rules:
            rule = PatternRule(
                id=rule_data['id'],
                pattern=rule_data['pattern'],
                rule_type=rule_data.get('type', 'regex'),
                severity=rule_data.get('severity', 'medium'),
                action=rule_data.get('action', 'alert'),
                metadata=rule_data.get('metadata', {})
            )

            self._pattern_rules[rule.id] = rule

            if rule.rule_type == 'exact':
                # O(1) exact lookups
                self._exact_patterns[rule.pattern.lower()] = rule
            elif rule.rule_type == 'regex':
                # Compiled regex patterns
                try:
                    compiled = re.compile(rule.pattern, re.IGNORECASE)
                    self._compiled_patterns[rule.id] = compiled
                except re.error:
                    # Skip invalid patterns
                    pass

    async def _match_patterns(self, event: RealTimeEvent) -> List[Dict[str, Any]]:
        """Fast pattern matching against event data"""
        matches = []

        # Convert event data to searchable text
        searchable_text = json.dumps(event.data).lower()

        # O(1) exact pattern lookups
        for pattern_text, rule in self._exact_patterns.items():
            if pattern_text in searchable_text:
                matches.append({
                    'rule_id': rule.id,
                    'pattern': rule.pattern,
                    'matched_data': pattern_text,
                    'severity': rule.severity,
                    'action': rule.action
                })

        # Regex pattern matching
        for rule_id, compiled_pattern in self._compiled_patterns.items():
            rule = self._pattern_rules[rule_id]
            match = compiled_pattern.search(searchable_text)
            if match:
                matches.append({
                    'rule_id': rule.id,
                    'pattern': rule.pattern,
                    'matched_data': match.group(0),
                    'severity': rule.severity,
                    'action': rule.action
                })

        return matches

    def _calculate_pattern_confidence(self, match: Dict[str, Any]) -> ConfidenceLevel:
        """Calculate confidence level for pattern matches"""
        severity = match.get('severity', 'medium')
        pattern_type = match.get('type', 'regex')

        if severity == 'critical' and pattern_type == 'exact':
            return ConfidenceLevel.HIGH
        elif severity in ['high', 'critical']:
            return ConfidenceLevel.HIGH
        elif severity == 'medium':
            return ConfidenceLevel.MEDIUM
        else:
            return ConfidenceLevel.LOW

    def _get_pattern_recommendations(self, match: Dict[str, Any]) -> List[str]:
        """Get recommendations based on pattern match"""
        action = match.get('action', 'alert')
        severity = match.get('severity', 'medium')

        recommendations = []

        if action == 'block':
            recommendations.append("Consider blocking this pattern")
        elif action == 'quarantine':
            recommendations.append("Quarantine affected resources")

        if severity in ['high', 'critical']:
            recommendations.extend([
                "Investigate immediately",
                "Alert security team",
                "Document for incident response"
            ])
        else:
            recommendations.extend([
                "Monitor for additional occurrences",
                "Review context for false positives"
            ])

        return recommendations

    # Correlation analysis methods

    def _add_event_to_correlation(self, event: RealTimeEvent, window_seconds: int):
        """Add event to correlation analysis buffer"""
        self._event_buffer.append(event)

        # Clean up old events outside correlation window
        current_time = time.time()
        cutoff_time = current_time - window_seconds

        while (self._event_buffer and
               self._event_buffer[0].timestamp < cutoff_time):
            self._event_buffer.popleft()

    async def _find_event_correlations(self, window_seconds: int) -> List[Dict[str, Any]]:
        """Find correlations between events in the time window"""
        correlations = []
        current_time = time.time()

        # Group events by correlation keys
        correlation_groups = defaultdict(list)

        for event in self._event_buffer:
            if current_time - event.timestamp <= window_seconds:
                # Create correlation keys based on event properties
                keys = self._generate_correlation_keys(event)
                for key in keys:
                    correlation_groups[key].append(event)

        # Find significant correlations
        for key, events in correlation_groups.items():
            if len(events) >= 2:  # At least 2 events to correlate
                sources = set(event.source for event in events)
                if len(sources) > 1:  # Cross-source correlation

                    time_span = max(event.timestamp for event in events) - \
                        min(event.timestamp for event in events)

                    correlation = {
                        'id': hashlib.md5(key.encode()).hexdigest()[:8],
                        'key': key,
                        'events': [self._event_to_dict(e) for e in events],
                        'sources': list(sources),
                        'time_span': time_span,
                        'strength': self._calculate_correlation_strength(events),
                        'patterns': self._identify_correlation_patterns(events)
                    }
                    correlations.append(correlation)

        return correlations

    def _generate_correlation_keys(self, event: RealTimeEvent) -> List[str]:
        """Generate correlation keys for an event"""
        keys = []

        # Common correlation patterns
        data = event.data

        # IP address correlations
        if 'ip' in data:
            keys.append(f"ip:{data['ip']}")

        # User correlations
        if 'user' in data:
            keys.append(f"user:{data['user']}")

        # Process correlations
        if 'process' in data:
            keys.append(f"process:{data['process']}")

        # File correlations
        if 'file' in data:
            keys.append(f"file:{data['file']}")

        # Custom correlation based on event type
        if event.event_type:
            keys.append(f"type:{event.event_type}")

        return keys

    def _calculate_correlation_strength(self, events: List[RealTimeEvent]) -> float:
        """Calculate strength of correlation between events"""
        if len(events) < 2:
            return 0.0

        # Factor in time clustering, source diversity, data similarity
        time_span = max(event.timestamp for event in events) - \
            min(event.timestamp for event in events)

        # Closer in time = stronger correlation
        time_factor = max(0.1, 1.0 / (1.0 + time_span))

        # More sources = stronger correlation
        source_count = len(set(event.source for event in events))
        source_factor = min(1.0, source_count / 3.0)

        # Event count factor
        count_factor = min(1.0, len(events) / 10.0)

        return time_factor * source_factor * count_factor

    def _identify_correlation_patterns(self, events: List[RealTimeEvent]) -> List[str]:
        """Identify patterns in correlated events"""
        patterns = []

        # Common data elements
        common_data_keys = set()
        if events:
            common_data_keys = set(events[0].data.keys())
            for event in events[1:]:
                common_data_keys.intersection_update(event.data.keys())

        if common_data_keys:
            patterns.append(f"common_data_fields:{','.join(common_data_keys)}")

        # Time patterns
        timestamps = [event.timestamp for event in events]
        if len(timestamps) > 2:
            intervals = [timestamps[i+1] - timestamps[i]
                         for i in range(len(timestamps)-1)]
            avg_interval = sum(intervals) / len(intervals)
            if all(abs(interval - avg_interval) < 1.0 for interval in intervals):
                patterns.append("regular_intervals")

        return patterns

    def _calculate_correlation_confidence(self, correlation: Dict[str, Any]) -> ConfidenceLevel:
        """Calculate confidence in correlation"""
        strength = correlation.get('strength', 0.0)
        event_count = len(correlation.get('events', []))
        source_count = len(correlation.get('sources', []))

        if strength > 0.8 and event_count > 5 and source_count > 2:
            return ConfidenceLevel.HIGH
        elif strength > 0.5 and event_count > 3:
            return ConfidenceLevel.MEDIUM
        else:
            return ConfidenceLevel.LOW

    # Performance monitoring methods

    async def _update_performance_metric(self, metric: PerformanceMetric):
        """Update performance metric history"""
        self._performance_metrics[metric.name] = metric
        self._latency_samples[metric.name].append({
            'timestamp': metric.timestamp,
            'value': metric.value
        })

    async def _detect_performance_anomalies(self, metric: PerformanceMetric) -> List[Dict[str, Any]]:
        """Detect performance anomalies"""
        anomalies = []
        samples = self._latency_samples[metric.name]

        if len(samples) < 10:  # Need enough samples for analysis
            return anomalies

        # Calculate statistics
        values = [sample['value'] for sample in samples]
        avg = sum(values) / len(values)
        std_dev = (sum((x - avg) ** 2 for x in values) / len(values)) ** 0.5

        # Threshold-based detection
        if metric.value > metric.threshold:
            severity = 'critical' if metric.value > metric.threshold * 2 else 'warning'
            anomalies.append({
                'type': 'threshold_exceeded',
                'severity': severity,
                'threshold': metric.threshold,
                'value': metric.value
            })

        # Statistical anomaly detection
        if abs(metric.value - avg) > 2 * std_dev:
            anomalies.append({
                'type': 'statistical_outlier',
                'severity': 'warning',
                'deviation': abs(metric.value - avg) / std_dev,
                'average': avg
            })

        # Trend analysis
        if len(samples) >= 5:
            recent_values = values[-5:]
            if all(recent_values[i] > recent_values[i-1] for i in range(1, len(recent_values))):
                anomalies.append({
                    'type': 'increasing_trend',
                    'severity': 'warning',
                    'trend': 'increasing'
                })

        return anomalies

    # Threat analysis methods

    async def _detect_threats_in_event(
        self, event: RealTimeEvent, threat_lookup: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Detect threats in event data"""
        threats = []

        # Check event data against threat indicators
        for key, value in event.data.items():
            if isinstance(value, str):
                value_lower = value.lower()
                if value_lower in threat_lookup:
                    indicator = threat_lookup[value_lower]
                    threats.append({
                        'type': indicator.get('type', 'unknown'),
                        'indicator': value,
                        'severity': indicator.get('severity', 'medium'),
                        'context': {'field': key, 'event_type': event.event_type}
                    })

        return threats

    def _calculate_threat_confidence(self, threat: Dict[str, Any]) -> ConfidenceLevel:
        """Calculate confidence in threat detection"""
        severity = threat.get('severity', 'medium')
        threat_type = threat.get('type', 'unknown')

        if severity == 'critical':
            return ConfidenceLevel.HIGH
        elif severity == 'high' or threat_type in ['malware', 'c2']:
            return ConfidenceLevel.HIGH
        elif severity == 'medium':
            return ConfidenceLevel.MEDIUM
        else:
            return ConfidenceLevel.LOW

    # Workflow analysis methods

    async def _analyze_workflow_execution(self, workflow_state: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze workflow execution for issues"""
        analysis = {'issues': []}

        nodes = workflow_state.get('nodes', {})
        start_time = workflow_state.get('start_time', 0)
        current_time = time.time()
        total_duration = current_time - start_time

        # Check for failed nodes
        failed_nodes = [
            node_id for node_id, node_data in nodes.items()
            if node_data.get('status') == 'failed'
        ]

        if failed_nodes:
            analysis['issues'].append({
                'type': 'node_failures',
                'nodes': failed_nodes,
                'severity': 'high'
            })

        # Check for long-running workflows
        if total_duration > 300:  # 5 minutes
            analysis['issues'].append({
                'type': 'long_execution',
                'duration': total_duration,
                'severity': 'medium'
            })

        # Check for hanging nodes
        hanging_nodes = []
        for node_id, node_data in nodes.items():
            if (node_data.get('status') == 'running' and
                    current_time - node_data.get('timestamp', current_time) > 120):
                hanging_nodes.append(node_id)

        if hanging_nodes:
            analysis['issues'].append({
                'type': 'hanging_nodes',
                'nodes': hanging_nodes,
                'severity': 'medium'
            })

        return analysis

    def _calculate_workflow_confidence(self, issue: Dict[str, Any]) -> ConfidenceLevel:
        """Calculate confidence in workflow issue detection"""
        issue_type = issue.get('type', 'unknown')
        severity = issue.get('severity', 'medium')

        if issue_type == 'node_failures':
            return ConfidenceLevel.HIGH
        elif severity == 'high':
            return ConfidenceLevel.HIGH
        elif severity == 'medium':
            return ConfidenceLevel.MEDIUM
        else:
            return ConfidenceLevel.LOW

    # Utility methods

    def _event_to_dict(self, event: RealTimeEvent) -> Dict[str, Any]:
        """Convert event to dictionary for serialization"""
        return {
            'timestamp': event.timestamp,
            'event_type': event.event_type,
            'source': event.source,
            'data': event.data,
            'metadata': event.metadata
        }

    def _update_processing_stats(self, processing_time: float):
        """Update processing statistics"""
        self._processing_stats['events_processed'] += 1

        # Update rolling average
        current_avg = self._processing_stats['avg_processing_time']
        count = self._processing_stats['events_processed']

        new_avg = ((current_avg * (count - 1)) + processing_time) / count
        self._processing_stats['avg_processing_time'] = new_avg

    async def get_processing_stats(self) -> Dict[str, Any]:
        """Get current processing statistics"""
        return self._processing_stats.copy()

    async def reset_stats(self):
        """Reset processing statistics"""
        self._processing_stats = {
            'events_processed': 0,
            'patterns_matched': 0,
            'correlations_found': 0,
            'avg_processing_time': 0.0
        }
