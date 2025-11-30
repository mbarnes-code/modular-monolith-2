"""
Dispatch Central Auth Plugin Package

This package provides integration between Dispatch and the central
authentication service through custom authentication providers.
"""

from .plugin import CentralAuthProviderPlugin, get_auth_provider_plugin

__version__ = "1.0.0"
__title__ = "dispatch-central-auth"
__description__ = "Central authentication service integration for Dispatch"
__author__ = "Modular Monolith Team"

__all__ = [
    "CentralAuthProviderPlugin",
    "get_auth_provider_plugin",
]
