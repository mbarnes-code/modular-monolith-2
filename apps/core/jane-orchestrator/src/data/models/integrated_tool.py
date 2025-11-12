"""
Integrated Tool model for managing 37 executive function tools.

Constitutional Requirements:
- Complete inventory of all 37 tools across 4 domains
- Tool status and health monitoring
- Integration status tracking
- Performance baseline preservation
"""

from datetime import datetime
from typing import Dict, Any, List, Optional
from sqlalchemy import (
    Column, Integer, String, DateTime, JSON, Boolean, Text, ForeignKey
)
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class IntegratedTool(Base):
    """
    Integrated tool registry for 37 executive function tools.
    
    Constitutional inventory:
    - Security Domain: 13 tools
    - Productivity Domain: 8 tools
    - MTG Domain: 4 tools
    - Infrastructure Domain: 12 tools
    """
    
    __tablename__ = "integrated_tools"
    
    # Primary identification
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False, index=True)
    display_name = Column(String(150), nullable=False)
    
    # Domain relationship
    domain_id = Column(Integer, ForeignKey("domains.id"), nullable=False)
    domain_name = Column(String(50), nullable=False, index=True)
    
    # Tool metadata
    description = Column(Text, nullable=True)
    version = Column(String(50), nullable=True)
    homepage_url = Column(String(500), nullable=True)
    documentation_url = Column(String(500), nullable=True)
    
    # Visual representation
    icon = Column(String(50), nullable=True)
    color = Column(String(20), nullable=True)
    screenshot_url = Column(String(500), nullable=True)
    
    # Technical details
    technology_stack = Column(JSON, default=lambda: {})  # Tech stack
    original_location = Column(String(500), nullable=True)  # Original path
    integration_type = Column(String(50), nullable=False)  # adapter, embedded
    
    # Integration status
    integration_status = Column(String(50), default="not_started")  # status
    migration_phase = Column(String(50), nullable=True)  # phase
    business_logic_preserved = Column(Boolean, default=False)
    
    # Performance and health
    health_status = Column(String(50), default="unknown")  # health status
    last_health_check = Column(DateTime(timezone=True), nullable=True)
    performance_baseline = Column(JSON, default=lambda: {})  # Baseline metrics
    current_performance = Column(JSON, default=lambda: {})   # Current metrics
    
    # Configuration
    config_schema = Column(JSON, default=lambda: {})    # Configuration schema
    default_config = Column(JSON, default=lambda: {})   # Default configuration
    runtime_config = Column(JSON, default=lambda: {})   # Runtime config
    
    # Features and capabilities
    features = Column(JSON, default=lambda: {})         # Features
    dependencies = Column(JSON, default=lambda: {})     # Tool dependencies
    api_endpoints = Column(JSON, default=lambda: {})    # API endpoints
    
    # Usage and analytics
    usage_stats = Column(JSON, default=lambda: {})      # Usage statistics
    user_preferences = Column(JSON, default=lambda: {})  # User preferences
    
    # Executive function support
    cognitive_load = Column(String(20), default="medium")  # low/medium/high
    adhd_friendly = Column(Boolean, default=False)
    autism_friendly = Column(Boolean, default=False)
    accessibility_features = Column(JSON, default=lambda: {})
    
    # Status and metadata
    is_active = Column(Boolean, default=True)
    is_favorite = Column(Boolean, default=False)
    sort_order = Column(Integer, default=0)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )
    
    @classmethod
    def get_constitutional_tool_count(cls) -> Dict[str, int]:
        """Get constitutional 37-tool count by domain."""
        return {
            "security": 13,
            "productivity": 8,
            "mtg": 4,
            "infrastructure": 12,
            "total": 37
        }
    
    def is_healthy(self) -> bool:
        """Check if tool is currently healthy."""
        return self.health_status == "healthy"
    
    def is_integration_complete(self) -> bool:
        """Check if tool integration is complete."""
        return (
            self.integration_status == "completed" and
            self.business_logic_preserved
        )
    
    def get_performance_score(self) -> Optional[float]:
        """Get current performance score compared to baseline."""
        if not self.performance_baseline or not self.current_performance:
            return None
        
        baseline_time = self.performance_baseline.get("avg_response_time_ms")
        current_time = self.current_performance.get("avg_response_time_ms")
        
        if not baseline_time or not current_time:
            return None
        
        # Score: 1.0 = same as baseline, >1.0 = worse, <1.0 = better
        return current_time / baseline_time
    
    def supports_executive_function(self) -> bool:
        """Check if tool supports executive function accommodations."""
        return self.adhd_friendly or self.autism_friendly
    
    def get_cognitive_load_score(self) -> int:
        """Get cognitive load score (1-10 scale)."""
        load_map = {"low": 3, "medium": 6, "high": 9}
        return load_map.get(self.cognitive_load, 6)
    
    def get_api_endpoints(self) -> List[str]:
        """Get list of available API endpoints."""
        if not self.api_endpoints:
            return []
        return list(self.api_endpoints.keys())
    
    def get_dependencies(self) -> List[str]:
        """Get list of tool dependencies."""
        if not self.dependencies:
            return []
        return self.dependencies.get("tools", [])
    
    def get_technology_stack(self) -> Dict[str, Any]:
        """Get technology stack information."""
        return self.technology_stack or {}
    
    def get_features(self) -> Dict[str, Any]:
        """Get feature flags and capabilities."""
        return self.features or {}
    
    def update_health_status(
        self, status: str, details: Optional[Dict[str, Any]] = None
    ) -> None:
        """Update tool health status."""
        self.health_status = status
        self.last_health_check = datetime.utcnow()
    
    def record_performance(self, metrics: Dict[str, Any]) -> None:
        """Record current performance metrics."""
        self.current_performance = {
            **metrics,
            "recorded_at": datetime.utcnow().isoformat()
        }
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert tool to dictionary for JSON serialization."""
        return {
            "id": self.id,
            "name": self.name,
            "display_name": self.display_name,
            "domain_name": self.domain_name,
            "description": self.description,
            "version": self.version,
            "icon": self.icon,
            "color": self.color,
            "technology_stack": self.get_technology_stack(),
            "integration_status": self.integration_status,
            "integration_type": self.integration_type,
            "business_logic_preserved": self.business_logic_preserved,
            "health_status": self.health_status,
            "is_healthy": self.is_healthy(),
            "integration_complete": self.is_integration_complete(),
            "performance_score": self.get_performance_score(),
            "cognitive_load": self.cognitive_load,
            "cognitive_load_score": self.get_cognitive_load_score(),
            "executive_function_support": self.supports_executive_function(),
            "adhd_friendly": self.adhd_friendly,
            "autism_friendly": self.autism_friendly,
            "features": self.get_features(),
            "api_endpoints": self.get_api_endpoints(),
            "dependencies": self.get_dependencies(),
            "is_active": self.is_active,
            "is_favorite": self.is_favorite,
            "sort_order": self.sort_order
        }
    
    def __repr__(self) -> str:
        return (
            f"<IntegratedTool(id={self.id}, name='{self.name}', "
            f"domain='{self.domain_name}', "
            f"status='{self.integration_status}')>"
        )