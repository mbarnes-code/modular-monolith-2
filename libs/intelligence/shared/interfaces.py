"""
Abstract Intelligence Service Interfaces

Defines the core interfaces that all intelligence services must implement.
These interfaces ensure consistent behavior across all intelligence services
while maintaining flexibility for domain-specific implementations.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional


class IntelligenceType(Enum):
    """Types of intelligence analysis"""
    PATTERN_DETECTION = "pattern_detection"
    BEHAVIOR_ANALYSIS = "behavior_analysis"
    SECURITY_ANALYSIS = "security_analysis"
    PRODUCTIVITY_OPTIMIZATION = "productivity_optimization"
    DATA_INTELLIGENCE = "data_intelligence"
    INFRASTRUCTURE_MONITORING = "infrastructure_monitoring"
    KNOWLEDGE_MAPPING = "knowledge_mapping"
    RECOMMENDATION = "recommendation"
    ANOMALY_DETECTION = "anomaly_detection"
    PERFORMANCE_ANALYSIS = "performance_analysis"


class AnalysisStatus(Enum):
    """Status of intelligence analysis"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CACHED = "cached"


class ConfidenceLevel(Enum):
    """Confidence levels for intelligence insights"""
    VERY_LOW = 0.1
    LOW = 0.3
    MEDIUM = 0.5
    HIGH = 0.7
    VERY_HIGH = 0.9


@dataclass
class IntelligenceContext:
    """Context information for intelligence analysis"""
    user_id: str
    domain: str
    tool_name: Optional[str] = None
    session_id: Optional[str] = None
    timestamp: Optional[datetime] = None
    metadata: Optional[Dict[str, Any]] = None


@dataclass
class IntelligenceInsight:
    """A single intelligence insight"""
    id: str
    type: IntelligenceType
    title: str
    description: str
    confidence: ConfidenceLevel
    recommendations: List[str]
    data: Dict[str, Any]
    context: IntelligenceContext
    timestamp: datetime
    expires_at: Optional[datetime] = None
    source_service: Optional[str] = None


@dataclass
class IntelligenceRequest:
    """Request for intelligence analysis"""
    request_id: str
    intelligence_type: IntelligenceType
    context: IntelligenceContext
    data: Dict[str, Any]
    options: Optional[Dict[str, Any]] = None
    priority: int = 5  # 1=highest, 10=lowest


class IntelligenceServiceInterface(ABC):
    """Abstract base class for all intelligence services"""

    @abstractmethod
    async def analyze(
        self,
        request: IntelligenceRequest
    ) -> List[IntelligenceInsight]:
        """
        Perform intelligence analysis on the provided data

        Args:
            request: The intelligence analysis request

        Returns:
            List of intelligence insights
        """
        pass

    @abstractmethod
    async def get_cached_insights(
        self,
        context: IntelligenceContext,
        intelligence_type: Optional[IntelligenceType] = None
    ) -> List[IntelligenceInsight]:
        """Get cached insights for the given context"""
        pass

    @abstractmethod
    async def health_check(self) -> Dict[str, Any]:
        """Check service health and status"""
        pass

    @abstractmethod
    def get_service_info(self) -> Dict[str, Any]:
        """Get service information and capabilities"""
        pass


class PatternIntelligenceInterface(IntelligenceServiceInterface):
    """Interface for pattern-based intelligence services"""

    @abstractmethod
    async def detect_patterns(
        self,
        user_interactions: List[Dict[str, Any]],
        context: IntelligenceContext,
        lookback_days: int = 30
    ) -> List[IntelligenceInsight]:
        """Detect patterns in user interactions"""
        pass

    @abstractmethod
    async def predict_next_action(
        self,
        current_session: Dict[str, Any],
        context: IntelligenceContext
    ) -> List[IntelligenceInsight]:
        """Predict likely next actions based on patterns"""
        pass


class SecurityIntelligenceInterface(IntelligenceServiceInterface):
    """Interface for security intelligence services"""

    @abstractmethod
    async def assess_threat_level(
        self,
        activity: Dict[str, Any],
        context: IntelligenceContext
    ) -> List[IntelligenceInsight]:
        """Assess threat level of an activity"""
        pass

    @abstractmethod
    async def detect_anomalies(
        self,
        activities: List[Dict[str, Any]],
        context: IntelligenceContext
    ) -> List[IntelligenceInsight]:
        """Detect security anomalies"""
        pass


class ProductivityIntelligenceInterface(IntelligenceServiceInterface):
    """Interface for productivity intelligence services"""

    @abstractmethod
    async def analyze_efficiency(
        self,
        workflows: List[Dict[str, Any]],
        context: IntelligenceContext
    ) -> List[IntelligenceInsight]:
        """Analyze workflow efficiency"""
        pass

    @abstractmethod
    async def suggest_optimizations(
        self,
        current_workflow: Dict[str, Any],
        context: IntelligenceContext
    ) -> List[IntelligenceInsight]:
        """Suggest workflow optimizations"""
        pass


class DataIntelligenceInterface(IntelligenceServiceInterface):
    """Interface for data intelligence services"""

    @abstractmethod
    async def analyze_data_flow(
        self,
        data_operations: List[Dict[str, Any]],
        context: IntelligenceContext
    ) -> List[IntelligenceInsight]:
        """Analyze data flow patterns"""
        pass

    @abstractmethod
    async def detect_data_quality_issues(
        self,
        data_samples: List[Dict[str, Any]],
        context: IntelligenceContext
    ) -> List[IntelligenceInsight]:
        """Detect data quality issues"""
        pass


class IntelligenceServiceRegistry:
    """Registry for managing intelligence services"""

    def __init__(self):
        self._services: Dict[
            IntelligenceType, IntelligenceServiceInterface
        ] = {}
        self._service_health: Dict[IntelligenceType, bool] = {}

    def register_service(
        self,
        intelligence_type: IntelligenceType,
        service: IntelligenceServiceInterface
    ) -> None:
        """Register an intelligence service"""
        self._services[intelligence_type] = service
        self._service_health[intelligence_type] = True

    def get_service(
        self,
        intelligence_type: IntelligenceType
    ) -> Optional[IntelligenceServiceInterface]:
        """Get a registered intelligence service"""
        return self._services.get(intelligence_type)

    def is_service_available(
        self, intelligence_type: IntelligenceType
    ) -> bool:
        """Check if a service is available and healthy"""
        return (
            intelligence_type in self._services and
            self._service_health.get(intelligence_type, False)
        )

    async def get_all_insights(
        self,
        request: IntelligenceRequest
    ) -> Dict[IntelligenceType, List[IntelligenceInsight]]:
        """Get insights from all available services"""
        insights = {}

        for intelligence_type, service in self._services.items():
            if self.is_service_available(intelligence_type):
                try:
                    request.intelligence_type = intelligence_type
                    service_insights = await service.analyze(request)
                    insights[intelligence_type] = service_insights
                except Exception as e:
                    # Log error but don't fail entire operation
                    print(f"Intelligence service {intelligence_type} "
                          f"failed: {e}")
                    self._service_health[intelligence_type] = False

        return insights


# Global service registry instance
intelligence_registry = IntelligenceServiceRegistry()
