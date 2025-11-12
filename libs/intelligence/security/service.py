"""
Security Intelligence Service

Provides security analysis, threat detection, and risk assessment
capabilities across all security tools and domains.

This service is OPTIONAL and security applications work perfectly without it.
"""

import re
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional

from ..shared.interfaces import (IntelligenceContext, IntelligenceInsight,
                                 IntelligenceRequest, IntelligenceType,
                                 SecurityIntelligenceInterface)
from ..shared.utils import (calculate_confidence, create_insight,
                            default_cache, default_metrics, with_caching,
                            with_metrics, with_timeout)


class ThreatLevel:
    """Threat levels for security analysis"""
    VERY_LOW = 1
    LOW = 2
    MEDIUM = 3
    HIGH = 4
    CRITICAL = 5


class SecurityIntelligenceService(SecurityIntelligenceInterface):
    """
    Advanced security intelligence service

    Provides threat assessment, anomaly detection, and security insights
    across all security tools in the platform.
    """

    def __init__(self, name: str = "security_intelligence"):
        self.name = name
        self.threat_patterns = self._load_threat_patterns()
        self.security_baselines = {}
        self.user_behaviors = {}

    def _load_threat_patterns(self) -> List[Dict[str, Any]]:
        """Load security threat patterns for analysis"""
        return [
            {
                'id': 'suspicious_commands',
                'pattern': r'(rm -rf|dd if=|curl.*bash|wget.*sh)',
                'threat_level': ThreatLevel.CRITICAL,
                'category': 'command_injection',
                'description': 'Potentially dangerous command execution'
            },
            {
                'id': 'credential_access',
                'pattern': r'(passwd|shadow|ssh.*key|\.env)',
                'threat_level': ThreatLevel.HIGH,
                'category': 'credential_access',
                'description': 'Potential credential harvesting attempt'
            },
            {
                'id': 'network_scanning',
                'pattern': r'(nmap|masscan|nc -l|netcat)',
                'threat_level': ThreatLevel.MEDIUM,
                'category': 'reconnaissance',
                'description': 'Network scanning or port listening'
            },
            {
                'id': 'persistence_attempt',
                'pattern': r'(crontab|systemctl|service.*enable)',
                'threat_level': ThreatLevel.HIGH,
                'category': 'persistence',
                'description': 'Attempt to establish persistence'
            },
            {
                'id': 'data_exfiltration',
                'pattern': r'(curl.*POST|wget.*data|scp.*\*)',
                'threat_level': ThreatLevel.HIGH,
                'category': 'exfiltration',
                'description': 'Potential data exfiltration attempt'
            }
        ]

    @with_timeout(timeout_seconds=10.0)
    @with_metrics(default_metrics, "security_intelligence")
    @with_caching(default_cache, "security_intelligence")
    async def analyze(
        self,
        request: IntelligenceRequest
    ) -> List[IntelligenceInsight]:
        """Analyze security aspects of user data"""
        context = request.context
        data = request.data

        insights = []

        # Threat assessment
        threat_insights = await self.assess_threat_level(data, context)
        insights.extend(threat_insights)

        # Anomaly detection
        anomaly_insights = await self.detect_anomalies([data], context)
        insights.extend(anomaly_insights)

        # Security posture analysis
        posture_insights = await self._analyze_security_posture(
            data, context
        )
        insights.extend(posture_insights)

        return insights

    async def get_cached_insights(
        self,
        context: IntelligenceContext,
        intelligence_type: Optional[IntelligenceType] = None
    ) -> List[IntelligenceInsight]:
        """Get cached security insights"""
        return []

    async def health_check(self) -> Dict[str, Any]:
        """Check security intelligence service health"""
        return {
            "service": self.name,
            "status": "healthy",
            "metrics": {
                "threat_patterns_loaded": len(self.threat_patterns),
                "users_monitored": len(self.user_behaviors),
                "baselines_established": len(self.security_baselines)
            },
            "timestamp": datetime.now().isoformat()
        }

    def get_service_info(self) -> Dict[str, Any]:
        """Get security intelligence service information"""
        return {
            "name": self.name,
            "type": IntelligenceType.SECURITY_ANALYSIS.value,
            "description": "Security threat analysis and anomaly detection",
            "capabilities": [
                "threat_level_assessment",
                "anomaly_detection",
                "security_posture_analysis",
                "behavioral_baseline_monitoring",
                "pattern_based_threat_detection"
            ],
            "threat_categories": [
                "command_injection",
                "credential_access",
                "reconnaissance",
                "persistence",
                "exfiltration",
                "privilege_escalation"
            ]
        }

    async def assess_threat_level(
        self,
        activity: Dict[str, Any],
        context: IntelligenceContext
    ) -> List[IntelligenceInsight]:
        """Assess threat level of an activity"""
        insights = []

        # Extract activity content for analysis
        content = self._extract_content_for_analysis(activity)
        if not content:
            return insights

        # Check against known threat patterns
        detected_threats = []
        for pattern_def in self.threat_patterns:
            if re.search(pattern_def['pattern'], content, re.IGNORECASE):
                detected_threats.append(pattern_def)

        # Create insights for detected threats
        for threat in detected_threats:
            confidence = calculate_confidence(
                pattern_frequency=10,  # Pattern is well-established
                data_quality=0.9,     # High quality pattern matching
                temporal_consistency=0.8,  # Consistent threat indicators
                user_feedback=0.5     # No feedback yet
            )

            insight = create_insight(
                insight_id=f"threat_{uuid.uuid4().hex[:8]}",
                title=f"Security Threat Detected: {threat['category']}",
                description=(
                    f"{threat['description']}. "
                    f"Threat level: "
                    f"{self._get_threat_level_name(threat['threat_level'])}. "
                    f"Immediate review recommended."
                ),
                intelligence_type=IntelligenceType.SECURITY_ANALYSIS,
                context=context,
                confidence=confidence,
                recommendations=self._get_threat_recommendations(threat),
                data={
                    'threat_id': threat['id'],
                    'threat_level': threat['threat_level'],
                    'category': threat['category'],
                    'matched_pattern': threat['pattern'],
                    'detection_timestamp': datetime.now().isoformat(),
                    'requires_immediate_attention': (
                        threat['threat_level'] >= ThreatLevel.HIGH
                    )
                },
                source_service=self.name
            )
            insights.append(insight)

        return insights

    async def detect_anomalies(
        self,
        activities: List[Dict[str, Any]],
        context: IntelligenceContext
    ) -> List[IntelligenceInsight]:
        """Detect security anomalies in activities"""
        insights = []

        if len(activities) < 2:
            return insights

        # Establish or update user behavioral baseline
        await self._update_user_baseline(context.user_id, activities)

        # Check for anomalies against baseline
        baseline = self.user_behaviors.get(context.user_id, {})
        if not baseline:
            return insights

        anomalies = await self._detect_behavioral_anomalies(
            activities, baseline, context
        )
        insights.extend(anomalies)

        return insights

    def _extract_content_for_analysis(
        self, activity: Dict[str, Any]
    ) -> Optional[str]:
        """Extract content from activity for security analysis"""
        content_fields = [
            'command', 'query', 'input', 'content', 'text', 'data',
            'parameters', 'args', 'payload', 'request_body'
        ]

        content_parts = []
        for field in content_fields:
            if field in activity and activity[field]:
                value = activity[field]
                if isinstance(value, str):
                    content_parts.append(value)
                elif isinstance(value, (list, dict)):
                    content_parts.append(str(value))

        return ' '.join(content_parts) if content_parts else None

    def _get_threat_level_name(self, level: int) -> str:
        """Convert threat level number to name"""
        level_names = {
            ThreatLevel.VERY_LOW: "Very Low",
            ThreatLevel.LOW: "Low",
            ThreatLevel.MEDIUM: "Medium",
            ThreatLevel.HIGH: "High",
            ThreatLevel.CRITICAL: "Critical"
        }
        return level_names.get(level, "Unknown")

    def _get_threat_recommendations(
        self, threat: Dict[str, Any]
    ) -> List[str]:
        """Get recommendations based on threat type"""
        base_recommendations = [
            "Review activity logs immediately",
            "Verify user authorization for this action",
            "Check for additional suspicious activities"
        ]

        category_recommendations = {
            'command_injection': [
                "Implement input sanitization",
                "Use parameterized commands",
                "Enable command auditing"
            ],
            'credential_access': [
                "Rotate affected credentials immediately",
                "Enable multi-factor authentication",
                "Monitor for credential misuse"
            ],
            'reconnaissance': [
                "Block suspicious network activity",
                "Monitor for follow-up attacks",
                "Review network security policies"
            ],
            'persistence': [
                "Remove unauthorized persistence mechanisms",
                "Audit system configuration changes",
                "Implement change monitoring"
            ],
            'exfiltration': [
                "Block data transfer if ongoing",
                "Audit data access logs",
                "Implement data loss prevention"
            ]
        }

        category = threat.get('category', '')
        specific_recommendations = category_recommendations.get(category, [])

        return base_recommendations + specific_recommendations

    async def _analyze_security_posture(
        self,
        data: Dict[str, Any],
        context: IntelligenceContext
    ) -> List[IntelligenceInsight]:
        """Analyze overall security posture"""
        insights = []

        # Check for security best practices
        posture_issues = await self._check_security_practices(data, context)

        for issue in posture_issues:
            confidence = calculate_confidence(
                pattern_frequency=5,
                data_quality=0.7,
                temporal_consistency=0.6,
                user_feedback=0.5
            )

            insight = create_insight(
                insight_id=f"posture_{uuid.uuid4().hex[:8]}",
                title=f"Security Posture: {issue['title']}",
                description=issue['description'],
                intelligence_type=IntelligenceType.SECURITY_ANALYSIS,
                context=context,
                confidence=confidence,
                recommendations=issue['recommendations'],
                data={
                    'posture_category': issue['category'],
                    'severity': issue['severity'],
                    'improvement_potential': True
                },
                source_service=self.name
            )
            insights.append(insight)

        return insights

    async def _update_user_baseline(
        self,
        user_id: str,
        activities: List[Dict[str, Any]]
    ) -> None:
        """Update user behavioral baseline"""
        if user_id not in self.user_behaviors:
            self.user_behaviors[user_id] = {
                'activity_count': 0,
                'common_tools': set(),
                'typical_hours': set(),
                'command_patterns': [],
                'last_updated': datetime.now()
            }

        baseline = self.user_behaviors[user_id]

        for activity in activities:
            baseline['activity_count'] += 1

            # Track tool usage
            tool = activity.get('tool_name')
            if tool:
                baseline['common_tools'].add(tool)

            # Track timing patterns
            timestamp = activity.get('timestamp')
            if timestamp:
                try:
                    dt = datetime.fromisoformat(timestamp)
                    baseline['typical_hours'].add(dt.hour)
                except ValueError:
                    pass

            # Track command patterns (simplified)
            content = self._extract_content_for_analysis(activity)
            if content:
                # Keep only recent command patterns (last 100)
                baseline['command_patterns'].append(content[:100])
                if len(baseline['command_patterns']) > 100:
                    baseline['command_patterns'] = (
                        baseline['command_patterns'][-100:]
                    )

        baseline['last_updated'] = datetime.now()

    async def _detect_behavioral_anomalies(
        self,
        activities: List[Dict[str, Any]],
        baseline: Dict[str, Any],
        context: IntelligenceContext
    ) -> List[IntelligenceInsight]:
        """Detect anomalies compared to user baseline"""
        insights = []

        for activity in activities:
            anomalies = []

            # Check for unusual tool usage
            tool = activity.get('tool_name')
            if tool and tool not in baseline.get('common_tools', set()):
                anomalies.append({
                    'type': 'unusual_tool',
                    'description': f'Unusual tool usage: {tool}',
                    'severity': 'low'
                })

            # Check for unusual timing
            timestamp = activity.get('timestamp')
            if timestamp:
                try:
                    dt = datetime.fromisoformat(timestamp)
                    if dt.hour not in baseline.get('typical_hours', set()):
                        anomalies.append({
                            'type': 'unusual_timing',
                            'description': f'Activity at unusual hour: {dt.hour:02d}:00',
                            'severity': 'medium'
                        })
                except ValueError:
                    pass

            # Create insights for anomalies
            for anomaly in anomalies:
                confidence = calculate_confidence(
                    pattern_frequency=3,
                    data_quality=0.6,
                    temporal_consistency=0.5,
                    user_feedback=0.5
                )

                insight = create_insight(
                    insight_id=f"anomaly_{uuid.uuid4().hex[:8]}",
                    title=f"Behavioral Anomaly: {anomaly['type']}",
                    description=anomaly['description'],
                    intelligence_type=IntelligenceType.SECURITY_ANALYSIS,
                    context=context,
                    confidence=confidence,
                    recommendations=[
                        "Review activity for legitimacy",
                        "Verify user identity",
                        "Monitor for additional anomalies"
                    ],
                    data={
                        'anomaly_type': anomaly['type'],
                        'severity': anomaly['severity'],
                        'baseline_deviation': True
                    },
                    source_service=self.name
                )
                insights.append(insight)

        return insights

    async def _check_security_practices(
        self,
        data: Dict[str, Any],
        context: IntelligenceContext
    ) -> List[Dict[str, Any]]:
        """Check for security best practices"""
        issues = []

        # Check for weak authentication patterns
        content = self._extract_content_for_analysis(data)
        if content and re.search(r'password.*=.*["\'].*["\']', content, re.IGNORECASE):
            issues.append({
                'title': 'Potential Password in Clear Text',
                'description': 'Detected potential password in configuration or command',
                'category': 'credential_security',
                'severity': 'high',
                'recommendations': [
                    'Use environment variables for sensitive data',
                    'Implement secret management system',
                    'Avoid hardcoded credentials'
                ]
            })

        # Check for insecure network practices
        if content and re.search(r'http://.*\.(com|org|net)', content):
            issues.append({
                'title': 'Insecure HTTP Usage',
                'description': 'Detected HTTP usage instead of HTTPS',
                'category': 'network_security',
                'severity': 'medium',
                'recommendations': [
                    'Use HTTPS for all external communications',
                    'Implement certificate validation',
                    'Consider using VPN for sensitive operations'
                ]
            })

        return issues
