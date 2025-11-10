"""
Environment configuration management for the Mental Prosthetic Platform.

Provides unified configuration across all 37 integrated tools with
executive function accommodations and constitutional compliance settings.
"""

import os
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseSettings, Field, validator


class Environment(str, Enum):
    """Environment types for configuration management."""
    DEVELOPMENT = "development"
    TESTING = "testing"
    STAGING = "staging"
    PRODUCTION = "production"


class DatabaseConfig(BaseSettings):
    """Database configuration settings."""

    # PostgreSQL (primary database)
    postgres_host: str = "localhost"
    postgres_port: int = 5432
    postgres_user: str = "postgres"
    postgres_password: str = "password"
    postgres_db: str = "mental_prosthetic"

    # SQLite (local-first tools)
    sqlite_db_path: str = "data/mental_prosthetic.db"

    # Redis (caching and sessions)
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_db: int = 0
    redis_password: Optional[str] = None

    @property
    def postgres_url(self) -> str:
        """Get PostgreSQL connection URL."""
        return f"postgresql://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"

    @property
    def postgres_async_url(self) -> str:
        """Get async PostgreSQL connection URL."""
        return f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"

    class Config:
        env_prefix = "DB_"


class AuthConfig(BaseSettings):
    """Authentication and authorization configuration."""

    jwt_secret_key: str = "change-this-in-production"
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 30
    jwt_refresh_token_expire_days: int = 7

    # OAuth providers (future expansion)
    oauth_enabled: bool = False
    oauth_providers: List[str] = Field(default_factory=list)

    class Config:
        env_prefix = "AUTH_"


class PerformanceConfig(BaseSettings):
    """Performance configuration for constitutional compliance."""

    # Domain-specific response time targets (milliseconds)
    security_target_ms: int = 1000      # <1s constitutional requirement
    productivity_target_ms: int = 2000  # <2s constitutional requirement
    mtg_target_ms: int = 3000          # <3s constitutional requirement
    infrastructure_target_ms: int = 5000  # <5s constitutional requirement

    # UI performance targets
    ui_response_target_ms: int = 200    # <200ms constitutional requirement
    websocket_latency_target_ms: int = 250  # Real-time sync requirement

    # Resource limits
    max_concurrent_requests: int = 100
    request_timeout_seconds: int = 30

    class Config:
        env_prefix = "PERF_"


class ExecutiveFunctionConfig(BaseSettings):
    """Executive function accommodation configuration."""

    # ADHD accommodations
    adhd_focus_indicators: bool = True
    adhd_progress_tracking: bool = True
    adhd_distraction_blocking: bool = True
    adhd_context_preservation_hours: int = 168  # 1 week

    # Autism accommodations
    autism_consistent_navigation: bool = True
    autism_sensory_optimization: str = "medium"  # low, medium, high
    autism_routine_preservation: bool = True
    autism_predictable_patterns: bool = True

    # General executive function support
    context_switching_reduction: bool = True
    rapid_task_access: bool = True
    workflow_state_preservation: bool = True

    class Config:
        env_prefix = "EXEC_"


class SecurityConfig(BaseSettings):
    """Security configuration for all domains."""

    # API security
    api_rate_limit_per_minute: int = 100
    api_cors_origins: List[str] = Field(
        default_factory=lambda: ["http://localhost:3000"])

    # Tool-specific security
    tools_require_auth: bool = True
    tools_audit_logging: bool = True

    # Data protection
    encrypt_sensitive_data: bool = True
    data_retention_days: int = 365

    class Config:
        env_prefix = "SEC_"


class DomainToolsConfig(BaseSettings):
    """Configuration for all 37 domain tools."""

    # Security domain tools (13 tools)
    security_tools: Dict[str, Dict[str, Any]] = Field(default_factory=lambda: {
        "misp": {"enabled": True, "url": "http://localhost:8080", "api_key": ""},
        "helk": {"enabled": True, "url": "http://localhost:5601", "username": "", "password": ""},
        "securityonion": {"enabled": True, "url": "http://localhost:9200"},
        "maltrail": {"enabled": True, "url": "http://localhost:8338"},
        "yara_x": {"enabled": True, "rules_path": "/opt/yara-x/rules"},
        "cyberchef": {"enabled": True, "url": "http://localhost:8000"},
        "nemesis": {"enabled": True, "url": "http://localhost:9001"},
        "apiscout": {"enabled": True, "db_path": "/opt/apiscout/db"},
        "brute_ratel": {"enabled": True, "listener_port": 4444},
        "meterpreter": {"enabled": True, "handler_port": 4445},
        "lscript": {"enabled": True, "scripts_path": "/opt/lscript"},
        "rita": {"enabled": True, "config_path": "/etc/rita/config.yaml"},
        "software_forensic_kit": {"enabled": True, "tools_path": "/opt/sfk"}
    })

    # Productivity domain tools (8 tools)
    productivity_tools: Dict[str, Dict[str, Any]] = Field(default_factory=lambda: {
        "n8n": {"enabled": True, "url": "http://localhost:5678", "webhook_url": ""},
        "mealie": {"enabled": True, "url": "http://localhost:9925", "api_token": ""},
        "dispatch": {"enabled": True, "url": "http://localhost:8080", "api_key": ""},
        "actual": {"enabled": True, "url": "http://localhost:5006", "sync_id": ""},
        "firecrawl": {"enabled": True, "api_key": "", "base_url": "https://api.firecrawl.dev"},
        "goose": {"enabled": True, "workspace_path": "/workspace", "model": "gpt-4"},
        "it_tools": {"enabled": True, "url": "http://localhost:8080"},
        "inspector": {"enabled": True, "analysis_path": "/tmp/inspector"}
    })

    # MTG domain tools (4 tools)
    mtg_tools: Dict[str, Dict[str, Any]] = Field(default_factory=lambda: {
        "commander_spellbook": {"enabled": True, "url": "https://commanderspellbook.com", "api_key": ""},
        "mtg_commander_map": {"enabled": True, "data_path": "/data/mtg-maps"},
        "mtg_scripting_toolkit": {"enabled": True, "scripts_path": "/opt/mtg-scripts"},
        "card_analysis": {"enabled": True, "cache_path": "/data/card-analysis"}
    })

    # Infrastructure domain tools (12 tools)
    infrastructure_tools: Dict[str, Dict[str, Any]] = Field(default_factory=lambda: {
        "kong": {"enabled": True, "admin_url": "http://localhost:8001", "proxy_url": "http://localhost:8000"},
        "ghostwriter": {"enabled": True, "url": "http://localhost:8080", "api_key": ""},
        "kasmvnc": {"enabled": True, "url": "http://localhost:6901", "password": ""},
        "chroma_mcp": {"enabled": True, "host": "localhost", "port": 8000},
        "filescopemcp": {"enabled": True, "scan_path": "/tmp/scans"},
        "firecrawl_mcp": {"enabled": True, "api_key": "", "server_url": ""},
        "n8n_mcp": {"enabled": True, "n8n_url": "http://localhost:5678"},
        "malwarebazaar_mcp": {"enabled": True, "api_key": ""},
        "mcp_virustotal": {"enabled": True, "api_key": ""},
        "onex": {"enabled": True, "exploits_path": "/opt/onex"},
        "hexstrike_ai": {"enabled": True, "model_path": "/models/hexstrike"},
        "blackarch": {"enabled": True, "tools_path": "/usr/share/blackarch"}
    })

    class Config:
        env_prefix = "TOOLS_"


class MentalProstheticConfig(BaseSettings):
    """Main configuration class for the Mental Prosthetic Platform."""

    # Environment
    environment: Environment = Environment.DEVELOPMENT
    debug: bool = True

    # Application
    app_name: str = "Mental Prosthetic Platform"
    app_version: str = "1.0.0"

    # Server configuration
    host: str = "0.0.0.0"
    port: int = 8000
    reload: bool = True

    # Component configurations
    database: DatabaseConfig = Field(default_factory=DatabaseConfig)
    auth: AuthConfig = Field(default_factory=AuthConfig)
    performance: PerformanceConfig = Field(default_factory=PerformanceConfig)
    executive_function: ExecutiveFunctionConfig = Field(
        default_factory=ExecutiveFunctionConfig)
    security: SecurityConfig = Field(default_factory=SecurityConfig)
    domain_tools: DomainToolsConfig = Field(default_factory=DomainToolsConfig)

    # Logging
    log_level: str = "INFO"
    log_format: str = "json"  # json or console

    @validator("environment", pre=True)
    def validate_environment(cls, v):
        """Validate environment setting."""
        if isinstance(v, str):
            return Environment(v.lower())
        return v

    @property
    def is_development(self) -> bool:
        """Check if running in development environment."""
        return self.environment == Environment.DEVELOPMENT

    @property
    def is_production(self) -> bool:
        """Check if running in production environment."""
        return self.environment == Environment.PRODUCTION

    def get_tool_config(self, domain: str, tool_name: str) -> Dict[str, Any]:
        """Get configuration for a specific tool."""
        domain_config = getattr(self.domain_tools, f"{domain}_tools", {})
        return domain_config.get(tool_name, {})

    def is_tool_enabled(self, domain: str, tool_name: str) -> bool:
        """Check if a specific tool is enabled."""
        tool_config = self.get_tool_config(domain, tool_name)
        return tool_config.get("enabled", False)

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# Global configuration instance
_config: Optional[MentalProstheticConfig] = None


def get_config() -> MentalProstheticConfig:
    """Get global configuration instance."""
    global _config
    if _config is None:
        _config = MentalProstheticConfig()
    return _config


def reload_config() -> MentalProstheticConfig:
    """Reload configuration from environment."""
    global _config
    _config = MentalProstheticConfig()
    return _config


# Domain-specific configuration helpers
def get_database_config() -> DatabaseConfig:
    """Get database configuration."""
    return get_config().database


def get_auth_config() -> AuthConfig:
    """Get authentication configuration."""
    return get_config().auth


def get_performance_config() -> PerformanceConfig:
    """Get performance configuration."""
    return get_config().performance


def get_executive_function_config() -> ExecutiveFunctionConfig:
    """Get executive function configuration."""
    return get_config().executive_function


def get_security_config() -> SecurityConfig:
    """Get security configuration."""
    return get_config().security


def get_domain_tools_config() -> DomainToolsConfig:
    """Get domain tools configuration."""
    return get_config().domain_tools


# Database URL helpers
def get_database_url() -> str:
    """Get PostgreSQL database URL."""
    return get_database_config().postgres_url


def get_async_database_url() -> str:
    """Get async PostgreSQL database URL."""
    return get_database_config().postgres_async_url


# Tool configuration helpers
def get_security_tools() -> Dict[str, Dict[str, Any]]:
    """Get security domain tools configuration."""
    return get_domain_tools_config().security_tools


def get_productivity_tools() -> Dict[str, Dict[str, Any]]:
    """Get productivity domain tools configuration."""
    return get_domain_tools_config().productivity_tools


def get_mtg_tools() -> Dict[str, Dict[str, Any]]:
    """Get MTG domain tools configuration."""
    return get_domain_tools_config().mtg_tools


def get_infrastructure_tools() -> Dict[str, Dict[str, Any]]:
    """Get infrastructure domain tools configuration."""
    return get_domain_tools_config().infrastructure_tools


# Executive function helper functions
def get_ui_response_target() -> int:
    """Get UI response time target for constitutional compliance."""
    return get_performance_config().ui_response_target_ms


def get_domain_response_target(domain: str) -> int:
    """Get domain-specific response time target."""
    perf_config = get_performance_config()
    targets = {
        "security": perf_config.security_target_ms,
        "productivity": perf_config.productivity_target_ms,
        "mtg": perf_config.mtg_target_ms,
        "infrastructure": perf_config.infrastructure_target_ms
    }
    return targets.get(domain, 5000)  # Default to 5s


def is_adhd_accommodations_enabled() -> bool:
    """Check if ADHD accommodations are enabled."""
    exec_config = get_executive_function_config()
    return exec_config.adhd_focus_indicators


def is_autism_accommodations_enabled() -> bool:
    """Check if autism accommodations are enabled."""
    exec_config = get_executive_function_config()
    return exec_config.autism_consistent_navigation


if __name__ == "__main__":
    # Test configuration loading
    config = get_config()
    print(f"Environment: {config.environment}")
    print(f"Database URL: {get_database_url()}")
    print(f"UI Response Target: {get_ui_response_target()}ms")
    print(
        f"Security Tools Enabled: {len([t for t in config.domain_tools.security_tools.values() if t.get('enabled')])}")
    print(f"ADHD Accommodations: {is_adhd_accommodations_enabled()}")
    print(f"Autism Accommodations: {is_autism_accommodations_enabled()}")
