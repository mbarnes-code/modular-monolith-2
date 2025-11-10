"""
MISP Unified Configuration Management

This module provides unified configuration management for MISP integration
as required by T1905c. It integrates tool-specific MISP configurations
with Jane's unified configuration system while preserving all original
MISP configuration patterns and functionality.

Based on analysis Section 10.1 - Configuration Management patterns.
"""

import json
import os
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import yaml
from pydantic import BaseSettings, Field, validator
from pydantic.env_settings import SettingsSourceCallable

logger = __import__('logging').getLogger(__name__)


class MISPUnifiedConfig(BaseSettings):
    """
    Unified configuration management for MISP integration.

    This class integrates MISP's extensive configuration requirements
    with Jane's unified configuration system, preserving all original
    MISP functionality while enabling seamless integration.
    """

    # ===== CORE MISP SETTINGS =====

    # Base configuration
    baseurl: str = Field(
        default="http://localhost:8080",
        description="MISP base URL",
        env="MISP_BASEURL"
    )

    org: str = Field(
        default="Jane Security Platform",
        description="Organization name",
        env="MISP_ORG"
    )

    contact: str = Field(
        default="security@jane.local",
        description="Contact email",
        env="MISP_CONTACT"
    )

    # API and authentication
    api_key: Optional[str] = Field(
        default=None,
        description="MISP API key",
        env="MISP_API_KEY"
    )

    verify_ssl: bool = Field(
        default=True,
        description="Verify SSL certificates",
        env="MISP_VERIFY_SSL"
    )

    timeout: int = Field(
        default=30,
        description="API timeout in seconds",
        env="MISP_TIMEOUT"
    )

    # ===== SECURITY SETTINGS =====

    # Authentication and authorization
    auth_enforced: bool = Field(
        default=True,
        description="Enforce authentication",
        env="MISP_AUTH_ENFORCED"
    )

    require_password_confirmation: bool = Field(
        default=True,
        description="Require password confirmation",
        env="MISP_REQUIRE_PASSWORD_CONFIRMATION"
    )

    advanced_authkeys: bool = Field(
        default=True,
        description="Enable advanced API keys",
        env="MISP_ADVANCED_AUTHKEYS"
    )

    password_policy_length: int = Field(
        default=12,
        description="Minimum password length",
        env="MISP_PASSWORD_POLICY_LENGTH"
    )

    password_policy_complexity: str = Field(
        default=r"/^((?=.*\\d)|(?=.*\\W+))(?![\\n])(?=.*[A-Z])(?=.*[a-z]).*$|.{16,}/",
        description="Password complexity regex",
        env="MISP_PASSWORD_POLICY_COMPLEXITY"
    )

    # Session and security
    authkey_keep_session: bool = Field(
        default=False,
        description="Keep session with API key",
        env="MISP_AUTHKEY_KEEP_SESSION"
    )

    disable_auto_logout: bool = Field(
        default=False,
        description="Disable automatic logout",
        env="MISP_DISABLE_AUTO_LOGOUT"
    )

    # ===== OPERATIONAL SETTINGS =====

    # Background processing
    background_jobs: bool = Field(
        default=True,
        description="Enable background jobs",
        env="MISP_BACKGROUND_JOBS"
    )

    manage_workers: bool = Field(
        default=True,
        description="Manage worker processes",
        env="MISP_MANAGE_WORKERS"
    )

    python_bin: Optional[str] = Field(
        default=None,
        description="Python binary path",
        env="MISP_PYTHON_BIN"
    )

    # Email and notifications
    disable_emailing: bool = Field(
        default=False,
        description="Disable email notifications",
        env="MISP_DISABLE_EMAILING"
    )

    email_subject_tlp_string: str = Field(
        default="tlp:amber",
        description="TLP string for email subjects",
        env="MISP_EMAIL_SUBJECT_TLP_STRING"
    )

    # ===== DISTRIBUTION AND SHARING =====

    default_event_distribution: int = Field(
        default=1,
        description="Default event distribution level",
        env="MISP_DEFAULT_EVENT_DISTRIBUTION"
    )

    default_attribute_distribution: str = Field(
        default="event",
        description="Default attribute distribution",
        env="MISP_DEFAULT_ATTRIBUTE_DISTRIBUTION"
    )

    unpublishedprivate: bool = Field(
        default=False,
        description="Unpublished events are private",
        env="MISP_UNPUBLISHED_PRIVATE"
    )

    # ===== TAGGING AND TAXONOMY =====

    tagging: bool = Field(
        default=True,
        description="Enable tagging",
        env="MISP_TAGGING"
    )

    full_tags_on_event_index: bool = Field(
        default=True,
        description="Show full tags on event index",
        env="MISP_FULL_TAGS_ON_EVENT_INDEX"
    )

    attribute_tagging: bool = Field(
        default=True,
        description="Enable attribute tagging",
        env="MISP_ATTRIBUTE_TAGGING"
    )

    full_tags_on_attribute_index: bool = Field(
        default=True,
        description="Show full tags on attribute index",
        env="MISP_FULL_TAGS_ON_ATTRIBUTE_INDEX"
    )

    # ===== CORRELATION SETTINGS =====

    ssdeep_correlation_threshold: int = Field(
        default=40,
        description="SSDeep correlation threshold",
        env="MISP_SSDEEP_CORRELATION_THRESHOLD"
    )

    max_correlations_per_event: int = Field(
        default=5000,
        description="Maximum correlations per event",
        env="MISP_MAX_CORRELATIONS_PER_EVENT"
    )

    show_correlations_on_index: bool = Field(
        default=True,
        description="Show correlations on index",
        env="MISP_SHOW_CORRELATIONS_ON_INDEX"
    )

    # ===== REDIS CONFIGURATION =====

    redis_host: str = Field(
        default="127.0.0.1",
        description="Redis host",
        env="MISP_REDIS_HOST"
    )

    redis_port: int = Field(
        default=6379,
        description="Redis port",
        env="MISP_REDIS_PORT"
    )

    redis_database: int = Field(
        default=13,
        description="Redis database number",
        env="MISP_REDIS_DATABASE"
    )

    redis_password: str = Field(
        default="",
        description="Redis password",
        env="MISP_REDIS_PASSWORD"
    )

    # ===== EXTERNAL INTEGRATIONS =====

    # CVE and vulnerability integration
    cve_url: str = Field(
        default="https://vulnerability.circl.lu/vuln/",
        description="CVE lookup URL",
        env="MISP_CVE_URL"
    )

    cwe_url: str = Field(
        default="https://vulnerability.circl.lu/cwes/",
        description="CWE lookup URL",
        env="MISP_CWE_URL"
    )

    # STIX integration
    stix_enabled: bool = Field(
        default=True,
        description="Enable STIX support",
        env="MISP_STIX_ENABLED"
    )

    # Feed configuration
    enable_feed_processing: bool = Field(
        default=True,
        description="Enable feed processing",
        env="MISP_ENABLE_FEED_PROCESSING"
    )

    feed_urls: List[str] = Field(
        default_factory=list,
        description="Threat feed URLs",
        env="MISP_FEED_URLS"
    )

    # ===== PERFORMANCE AND LIMITS =====

    # Constitutional compliance (security domain <1s)
    max_response_time_ms: int = Field(
        default=1000,
        description="Maximum response time (constitutional requirement)",
        env="MISP_MAX_RESPONSE_TIME_MS"
    )

    # Event and attribute limits
    default_event_threat_level: str = Field(
        default="4",
        description="Default threat level",
        env="MISP_DEFAULT_EVENT_THREAT_LEVEL"
    )

    proposals_block_attributes: bool = Field(
        default=False,
        description="Proposals block attributes",
        env="MISP_PROPOSALS_BLOCK_ATTRIBUTES"
    )

    # ===== LOGGING AND MONITORING =====

    log_client_ip: bool = Field(
        default=True,
        description="Log client IP addresses",
        env="MISP_LOG_CLIENT_IP"
    )

    log_auth: bool = Field(
        default=True,
        description="Log authentication events",
        env="MISP_LOG_AUTH"
    )

    store_api_access_time: bool = Field(
        default=True,
        description="Store API access times",
        env="MISP_STORE_API_ACCESS_TIME"
    )

    log_paranoid: bool = Field(
        default=False,
        description="Enable paranoid logging",
        env="MISP_LOG_PARANOID"
    )

    # ===== UI AND UX SETTINGS =====

    title_text: str = Field(
        default="Jane MISP Integration",
        description="UI title text",
        env="MISP_TITLE_TEXT"
    )

    language: str = Field(
        default="eng",
        description="Default language",
        env="MISP_LANGUAGE"
    )

    footer_logo: str = Field(
        default="",
        description="Footer logo path",
        env="MISP_FOOTER_LOGO"
    )

    # ===== JANE INTEGRATION SETTINGS =====

    # Unified monolith integration
    use_unified_auth: bool = Field(
        default=True,
        description="Use Jane's unified authentication",
        env="JANE_MISP_USE_UNIFIED_AUTH"
    )

    offline_mode: bool = Field(
        default=False,
        description="Enable offline/airgapped mode",
        env="JANE_MISP_OFFLINE_MODE"
    )

    local_data_path: str = Field(
        default="/tmp/misp_cache",
        description="Local data cache path",
        env="JANE_MISP_LOCAL_DATA_PATH"
    )

    enable_constitutional_monitoring: bool = Field(
        default=True,
        description="Enable constitutional compliance monitoring",
        env="JANE_MISP_CONSTITUTIONAL_MONITORING"
    )

    # Integration with other Jane services
    security_domain_integration: bool = Field(
        default=True,
        description="Enable security domain integration",
        env="JANE_MISP_SECURITY_DOMAIN_INTEGRATION"
    )

    ai_enhancement_enabled: bool = Field(
        default=True,
        description="Enable AI enhancement features",
        env="JANE_MISP_AI_ENHANCEMENT"
    )

    # Custom validators

    @validator('max_response_time_ms')
    def validate_constitutional_compliance(cls, v):
        """Ensure response time meets constitutional requirements."""
        if v > 1000:
            raise ValueError(
                "Security domain response time must be ≤1000ms "
                "per constitutional requirements"
            )
        return v

    @validator('default_event_distribution')
    def validate_distribution_level(cls, v):
        """Validate distribution level."""
        if v not in [0, 1, 2, 3, 4]:
            raise ValueError("Distribution level must be 0-4")
        return v

    @validator('local_data_path')
    def ensure_data_path_exists(cls, v):
        """Ensure data path exists."""
        path = Path(v)
        path.mkdir(parents=True, exist_ok=True)
        return str(path)

    @validator('feed_urls', pre=True)
    def parse_feed_urls(cls, v):
        """Parse feed URLs from string or list."""
        if isinstance(v, str):
            if v.strip():
                return [url.strip() for url in v.split(',') if url.strip()]
            return []
        return v or []

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False

        # Custom settings sources for enhanced configuration loading
        @classmethod
        def customise_sources(
            cls,
            init_settings: SettingsSourceCallable,
            env_settings: SettingsSourceCallable,
            file_secret_settings: SettingsSourceCallable,
        ) -> tuple[SettingsSourceCallable, ...]:
            return (
                init_settings,
                env_settings,
                yaml_config_settings_source,
                json_config_settings_source,
                legacy_misp_config_source,
                file_secret_settings,
            )


def yaml_config_settings_source(settings: BaseSettings) -> Dict[str, Any]:
    """Load configuration from YAML files."""
    config_data = {}

    # Look for YAML config files
    config_paths = [
        Path("config/misp.yaml"),
        Path("config/misp.yml"),
        Path("/etc/jane/misp.yaml"),
        Path("/etc/misp/config.yaml")
    ]

    for config_path in config_paths:
        if config_path.exists():
            try:
                with open(config_path, 'r') as f:
                    yaml_data = yaml.safe_load(f) or {}

                # Flatten nested configuration
                flattened = _flatten_config(yaml_data)
                config_data.update(flattened)

                logger.info(f"Loaded MISP config from {config_path}")
                break

            except Exception as e:
                logger.warning(
                    f"Failed to load YAML config from {config_path}: {e}")

    return config_data


def json_config_settings_source(settings: BaseSettings) -> Dict[str, Any]:
    """Load configuration from JSON files."""
    config_data = {}

    # Look for JSON config files
    config_paths = [
        Path("config/misp.json"),
        Path("/etc/jane/misp.json"),
        Path("/etc/misp/config.json")
    ]

    for config_path in config_paths:
        if config_path.exists():
            try:
                with open(config_path, 'r') as f:
                    json_data = json.load(f)

                # Flatten nested configuration
                flattened = _flatten_config(json_data)
                config_data.update(flattened)

                logger.info(f"Loaded MISP config from {config_path}")
                break

            except Exception as e:
                logger.warning(
                    f"Failed to load JSON config from {config_path}: {e}")

    return config_data


def legacy_misp_config_source(settings: BaseSettings) -> Dict[str, Any]:
    """Load configuration from legacy MISP config files."""
    config_data = {}

    # Look for legacy MISP configuration
    legacy_paths = [
        Path("features/MISP/app/Config/config.default.php"),
        Path("/var/www/MISP/app/Config/config.default.php"),
        Path("/opt/misp/app/Config/config.default.php")
    ]

    for config_path in legacy_paths:
        if config_path.exists():
            try:
                # Parse PHP config file (basic parsing)
                legacy_config = _parse_legacy_misp_config(config_path)
                config_data.update(legacy_config)

                logger.info(f"Loaded legacy MISP config from {config_path}")
                break

            except Exception as e:
                logger.warning(
                    f"Failed to load legacy config from {config_path}: {e}")

    return config_data


def _flatten_config(config: Dict[str, Any], prefix: str = "") -> Dict[str, Any]:
    """Flatten nested configuration dictionary."""
    flattened = {}

    for key, value in config.items():
        new_key = f"{prefix}_{key}" if prefix else key

        if isinstance(value, dict):
            flattened.update(_flatten_config(value, new_key))
        else:
            flattened[new_key.lower()] = value

    return flattened


def _parse_legacy_misp_config(config_path: Path) -> Dict[str, Any]:
    """Parse legacy MISP PHP configuration file."""
    config_data = {}

    try:
        with open(config_path, 'r') as f:
            content = f.read()

        # Basic PHP config parsing - extract key-value pairs
        # This is a simplified parser for common MISP config patterns

        # Extract MISP section
        if "'MISP' => array(" in content:
            misp_section = content.split(
                "'MISP' => array(")[1].split("'Security'")[0]

            # Parse basic key-value pairs
            import re

            # Match patterns like: 'key' => 'value',
            string_pattern = r"'([^']+)'\s*=>\s*'([^']*)',"
            bool_pattern = r"'([^']+)'\s*=>\s*(true|false),"
            int_pattern = r"'([^']+)'\s*=>\s*(\d+),"

            for pattern in [string_pattern, bool_pattern, int_pattern]:
                matches = re.findall(pattern, misp_section)
                for key, value in matches:
                    # Convert to appropriate type
                    if value in ['true', 'false']:
                        config_data[key.lower()] = value == 'true'
                    elif value.isdigit():
                        config_data[key.lower()] = int(value)
                    else:
                        config_data[key.lower()] = value

    except Exception as e:
        logger.warning(f"Legacy config parsing failed: {e}")

    return config_data


class MISPConfigManager:
    """
    Unified configuration manager for MISP integration.

    Provides centralized configuration management with support for
    multiple configuration sources and runtime configuration updates.
    """

    def __init__(self):
        """Initialize configuration manager."""
        self._config = None
        self._config_sources = []
        self._config_cache = {}

    def get_config(self) -> MISPUnifiedConfig:
        """Get unified MISP configuration."""
        if self._config is None:
            self._config = MISPUnifiedConfig()
            self._cache_config()

        return self._config

    def _cache_config(self):
        """Cache configuration for quick access."""
        config = self._config

        self._config_cache = {
            # Core settings
            'baseurl': config.baseurl,
            'api_key': config.api_key,
            'verify_ssl': config.verify_ssl,
            'timeout': config.timeout,

            # Operational settings
            'offline_mode': config.offline_mode,
            'background_jobs': config.background_jobs,
            'max_response_time_ms': config.max_response_time_ms,

            # Integration settings
            'use_unified_auth': config.use_unified_auth,
            'stix_enabled': config.stix_enabled,
            'enable_feed_processing': config.enable_feed_processing,

            # Redis settings
            'redis_host': config.redis_host,
            'redis_port': config.redis_port,
            'redis_database': config.redis_database,
            'redis_password': config.redis_password,

            # Security settings
            'auth_enforced': config.auth_enforced,
            'log_client_ip': config.log_client_ip,
            'log_auth': config.log_auth,
        }

    def get_adapter_config(self) -> Dict[str, Any]:
        """Get configuration dictionary for MISP adapter."""
        if not self._config_cache:
            self.get_config()  # Ensure config is loaded

        return self._config_cache.copy()

    def get_legacy_format(self) -> Dict[str, Any]:
        """Get configuration in legacy MISP format for compatibility."""
        config = self.get_config()

        return {
            'MISP': {
                'baseurl': config.baseurl,
                'org': config.org,
                'contact': config.contact,
                'background_jobs': config.background_jobs,
                'tagging': config.tagging,
                'full_tags_on_event_index': config.full_tags_on_event_index,
                'default_event_distribution': str(config.default_event_distribution),
                'default_attribute_distribution': config.default_attribute_distribution,
                'redis_host': config.redis_host,
                'redis_port': config.redis_port,
                'redis_database': config.redis_database,
                'ssdeep_correlation_threshold': config.ssdeep_correlation_threshold,
                'max_correlations_per_event': config.max_correlations_per_event,
                'log_client_ip': config.log_client_ip,
                'log_auth': config.log_auth,
                'cveurl': config.cve_url,
                'cweurl': config.cwe_url,
                'title_text': config.title_text,
                'language': config.language,
            },
            'Security': {
                'auth_enforced': config.auth_enforced,
                'require_password_confirmation': config.require_password_confirmation,
                'advanced_authkeys': config.advanced_authkeys,
                'password_policy_length': config.password_policy_length,
                'password_policy_complexity': config.password_policy_complexity,
            }
        }

    def reload_config(self):
        """Reload configuration from all sources."""
        self._config = None
        self._config_cache = {}
        return self.get_config()

    def validate_config(self) -> Dict[str, Any]:
        """Validate current configuration."""
        config = self.get_config()
        validation_results = {
            'valid': True,
            'warnings': [],
            'errors': [],
            'constitutional_compliance': True
        }

        # Validate constitutional compliance
        if config.max_response_time_ms > 1000:
            validation_results['valid'] = False
            validation_results['constitutional_compliance'] = False
            validation_results['errors'].append(
                "Response time exceeds constitutional requirement (<1000ms)"
            )

        # Validate required settings
        if not config.baseurl:
            validation_results['warnings'].append("Base URL not configured")

        if not config.api_key and not config.offline_mode:
            validation_results['warnings'].append(
                "API key not configured (required for online mode)"
            )

        # Validate paths
        try:
            Path(config.local_data_path).mkdir(parents=True, exist_ok=True)
        except Exception as e:
            validation_results['errors'].append(f"Invalid data path: {e}")
            validation_results['valid'] = False

        return validation_results


# Global configuration manager instance
_config_manager = None


def get_misp_config_manager() -> MISPConfigManager:
    """Get global MISP configuration manager instance."""
    global _config_manager
    if _config_manager is None:
        _config_manager = MISPConfigManager()
    return _config_manager


def get_misp_config() -> MISPUnifiedConfig:
    """Get MISP unified configuration."""
    return get_misp_config_manager().get_config()


def get_misp_adapter_config() -> Dict[str, Any]:
    """Get configuration for MISP adapter."""
    return get_misp_config_manager().get_adapter_config()


def get_legacy_misp_config() -> Dict[str, Any]:
    """Get configuration in legacy MISP format."""
    return get_misp_config_manager().get_legacy_format()
