"""
Configuration settings for HexStrike service.
"""
import os
from typing import Any, Dict


class Config:
    """Base configuration class."""

    # Server settings
    HOST = os.getenv('HEXSTRIKE_HOST', '0.0.0.0')
    PORT = int(os.getenv('HEXSTRIKE_PORT', '8000'))
    DEBUG = os.getenv('HEXSTRIKE_DEBUG', 'false').lower() == 'true'

    # Logging settings
    LOG_LEVEL = os.getenv('HEXSTRIKE_LOG_LEVEL', 'INFO')
    LOG_FILE = os.getenv('HEXSTRIKE_LOG_FILE', 'hexstrike.log')

    # MCP settings
    MCP_HOST = os.getenv('HEXSTRIKE_MCP_HOST', 'localhost')
    MCP_PORT = int(os.getenv('HEXSTRIKE_MCP_PORT', '8001'))

    # Tool configuration
    TOOLS_TIMEOUT = int(os.getenv('HEXSTRIKE_TOOLS_TIMEOUT', '300'))
    MAX_WORKERS = int(os.getenv('HEXSTRIKE_MAX_WORKERS', '4'))

    @classmethod
    def get_config(cls) -> Dict[str, Any]:
        """Get all configuration as a dictionary."""
        return {
            'host': cls.HOST,
            'port': cls.PORT,
            'debug': cls.DEBUG,
            'log_level': cls.LOG_LEVEL,
            'log_file': cls.LOG_FILE,
            'mcp_host': cls.MCP_HOST,
            'mcp_port': cls.MCP_PORT,
            'tools_timeout': cls.TOOLS_TIMEOUT,
            'max_workers': cls.MAX_WORKERS,
        }


class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    LOG_LEVEL = 'DEBUG'


class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    LOG_LEVEL = 'WARNING'


class TestingConfig(Config):
    """Testing configuration."""
    DEBUG = True
    LOG_LEVEL = 'DEBUG'
    PORT = 8888  # Use different port for testing


# Configuration mapping
config_map = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig,
}


def get_config(env: str | None = None) -> Config:
    """Get configuration for the specified environment."""
    env = env or os.getenv('HEXSTRIKE_ENV', 'default')
    return config_map.get(env, DevelopmentConfig)
