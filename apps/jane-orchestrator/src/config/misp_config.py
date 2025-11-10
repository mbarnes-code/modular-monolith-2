"""
MISP Configuration Management

This module provides configuration management for MISP integration
within the unified monolith stack as required by T1885a.

Integrates MISP-specific settings with the Jane orchestrator configuration
system while preserving original MISP configuration patterns.
"""

import os
from pathlib import Path
from typing import Any, Dict, Optional

from pydantic import BaseSettings, Field, validator


class MISPConfig(BaseSettings):
    """
    MISP configuration settings for unified monolith integration.

    This class preserves MISP's original configuration structure while
    integrating with Jane's unified configuration system.
    """

    # Core MISP settings
    misp_url: str = Field(
        default="http://localhost:8080",
        description="MISP instance URL"
    )

    api_key: Optional[str] = Field(
        default=None,
        description="MISP API key for authentication"
    )

    verify_ssl: bool = Field(
        default=True,
        description="Verify SSL certificates for MISP connections"
    )

    timeout: int = Field(
        default=30,
        description="Request timeout in seconds"
    )

    # Operational mode settings
    offline_mode: bool = Field(
        default=False,
        description="Enable offline/airgapped operation mode"
    )

    local_data_path: str = Field(
        default="/tmp/misp_cache",
        description="Local cache directory for offline operations"
    )

    # Performance settings (Constitutional compliance)
    max_response_time_ms: int = Field(
        default=1000,
        description="Maximum response time for security domain (<1s requirement)"
    )

    # Redis configuration (inherited from unified stack)
    redis_host: str = Field(
        default="127.0.0.1",
        description="Redis host for caching"
    )

    redis_port: int = Field(
        default=6379,
        description="Redis port"
    )

    redis_database: int = Field(
        default=13,
        description="Redis database number (MISP default)"
    )

    redis_password: str = Field(
        default="",
        description="Redis password"
    )

    # External integration settings
    stix_enabled: bool = Field(
        default=True,
        description="Enable STIX format support"
    )

    cve_lookup_enabled: bool = Field(
        default=True,
        description="Enable CVE vulnerability lookups"
    )

    cve_url: str = Field(
        default="https://vulnerability.circl.lu/vuln/",
        description="CVE lookup service URL"
    )

    # Organization settings (preserved from MISP config)
    org_name: str = Field(
        default="Jane Security Platform",
        description="Organization name"
    )

    contact_email: str = Field(
        default="security@jane.local",
        description="Contact email address"
    )

    # Distribution and sharing settings
    default_event_distribution: int = Field(
        default=1,
        description="Default event distribution level"
    )

    default_attribute_distribution: str = Field(
        default="event",
        description="Default attribute distribution setting"
    )

    # Correlation settings
    ssdeep_correlation_threshold: int = Field(
        default=40,
        description="SSDeep correlation threshold"
    )

    max_correlations_per_event: int = Field(
        default=5000,
        description="Maximum correlations per event"
    )

    # Background processing
    background_jobs: bool = Field(
        default=True,
        description="Enable background job processing"
    )

    # Tagging and taxonomy settings
    tagging_enabled: bool = Field(
        default=True,
        description="Enable event and attribute tagging"
    )

    full_tags_on_event_index: bool = Field(
        default=True,
        description="Show full tags on event index"
    )

    # Security settings
    require_password_confirmation: bool = Field(
        default=True,
        description="Require password confirmation for sensitive operations"
    )

    auth_enforced: bool = Field(
        default=True,
        description="Enforce authentication"
    )

    # Integration with Jane's unified auth
    use_unified_auth: bool = Field(
        default=True,
        description="Use Jane's unified authentication system"
    )

    # Logging and monitoring
    log_client_ip: bool = Field(
        default=True,
        description="Log client IP addresses"
    )

    log_auth: bool = Field(
        default=True,
        description="Log authentication events"
    )

    store_api_access_time: bool = Field(
        default=True,
        description="Store API access timestamps"
    )

    # Feed and sync settings
    enable_feed_processing: bool = Field(
        default=True,
        description="Enable automatic feed processing"
    )

    feed_cache_timeout: int = Field(
        default=3600,
        description="Feed cache timeout in seconds"
    )

    @validator('local_data_path')
    def validate_data_path(cls, v):
        """Ensure data path exists and is writable."""
        path = Path(v)
        path.mkdir(parents=True, exist_ok=True)
        return str(path)

    @validator('max_response_time_ms')
    def validate_response_time(cls, v):
        """Ensure response time meets constitutional requirements."""
        if v > 1000:
            raise ValueError(
                "Security domain response time must be <1000ms "
                "per constitutional requirements"
            )
        return v

    class Config:
        env_prefix = "MISP_"
        case_sensitive = False

        # Environment variable mapping
        fields = {
            'misp_url': {'env': 'MISP_BASEURL'},
            'api_key': {'env': 'MISP_API_KEY'},
            'org_name': {'env': 'MISP_ORG'},
            'contact_email': {'env': 'MISP_CONTACT'},
        }


def get_misp_config() -> MISPConfig:
    """Get MISP configuration instance."""
    return MISPConfig()


def create_misp_adapter_config() -> Dict[str, Any]:
    """Create configuration dictionary for MISP adapter."""
    config = get_misp_config()

    return {
        'misp_url': config.misp_url,
        'api_key': config.api_key,
        'verify_ssl': config.verify_ssl,
        'timeout': config.timeout,
        'offline_mode': config.offline_mode,
        'local_data_path': config.local_data_path,
        'max_response_time_ms': config.max_response_time_ms,
        'redis_host': config.redis_host,
        'redis_port': config.redis_port,
        'redis_database': config.redis_database,
        'redis_password': config.redis_password,
        'stix_enabled': config.stix_enabled,
        'cve_lookup_enabled': config.cve_lookup_enabled,
        'cve_url': config.cve_url,
        'ssdeep_correlation_threshold': config.ssdeep_correlation_threshold,
        'max_correlations_per_event': config.max_correlations_per_event,
        'background_jobs': config.background_jobs,
        'tagging_enabled': config.tagging_enabled,
        'use_unified_auth': config.use_unified_auth,
        'log_client_ip': config.log_client_ip,
        'log_auth': config.log_auth,
        'enable_feed_processing': config.enable_feed_processing,
        'feed_cache_timeout': config.feed_cache_timeout,
    }


def get_legacy_misp_config_format() -> Dict[str, Any]:
    """
    Generate legacy MISP configuration format for compatibility.

    This maintains compatibility with existing MISP configuration
    while integrating with the unified monolith stack.
    """
    config = get_misp_config()

    return {
        'MISP': {
            'baseurl': config.misp_url,
            'org': config.org_name,
            'contact': config.contact_email,
            'email': config.contact_email,
            'background_jobs': config.background_jobs,
            'tagging': config.tagging_enabled,
            'full_tags_on_event_index': config.full_tags_on_event_index,
            'default_event_distribution': str(config.default_event_distribution),
            'default_attribute_distribution': config.default_attribute_distribution,
            'redis_host': config.redis_host,
            'redis_port': config.redis_port,
            'redis_database': config.redis_database,
            'redis_password': config.redis_password,
            'ssdeep_correlation_threshold': config.ssdeep_correlation_threshold,
            'max_correlations_per_event': config.max_correlations_per_event,
            'log_client_ip': config.log_client_ip,
            'log_auth': config.log_auth,
            'store_api_access_time': config.store_api_access_time,
        },
        'Security': {
            'require_password_confirmation': config.require_password_confirmation,
            'auth_enforced': config.auth_enforced,
        }
    }
