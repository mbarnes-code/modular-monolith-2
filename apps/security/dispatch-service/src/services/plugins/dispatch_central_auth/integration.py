"""
Dispatch Configuration Patch for Central Auth Integration

This module patches Dispatch's configuration to enable central
authentication service integration.
"""

import logging
from typing import Any, Dict

log = logging.getLogger(__name__)


def patch_dispatch_config():
    """
    Patch Dispatch configuration to include central auth settings.

    This function should be called during Dispatch startup to enable
    central authentication service integration.
    """
    try:
        # Import configuration modules
        from dispatch import config

        from .config import (CENTRAL_AUTH_ENABLED, CENTRAL_AUTH_PROVIDER_SLUG,
                             CENTRAL_AUTH_SERVICE_URL)

        # Only patch if central auth is enabled
        if not CENTRAL_AUTH_ENABLED:
            log.info("Central auth disabled, skipping configuration patch")
            return False

        # Patch authentication provider slug
        original_slug = getattr(
            config, 'DISPATCH_AUTHENTICATION_PROVIDER_SLUG', None)
        config.DISPATCH_AUTHENTICATION_PROVIDER_SLUG = CENTRAL_AUTH_PROVIDER_SLUG

        log.info("Patched Dispatch auth provider: %s -> %s",
                 original_slug, CENTRAL_AUTH_PROVIDER_SLUG)

        # Add central auth service URL to config
        config.CENTRAL_AUTH_SERVICE_URL = CENTRAL_AUTH_SERVICE_URL

        log.info("Central auth configuration patched successfully")
        return True

    except ImportError as e:
        log.error("Failed to patch Dispatch config - missing modules: %s", str(e))
        return False
    except Exception as e:
        log.error("Failed to patch Dispatch config: %s", str(e))
        return False


def register_central_auth_plugin():
    """
    Register central auth plugin with Dispatch's plugin system.

    This function registers the CentralAuthProviderPlugin so it can be
    discovered and used by Dispatch's authentication system.
    """
    try:
        from dispatch.plugin import service as plugin_service
        from dispatch.plugin.models import Plugin, PluginInstance
        from dispatch.project import service as project_service

        from .config import CENTRAL_AUTH_PROVIDER_SLUG
        from .plugin import CentralAuthProviderPlugin

        # Create plugin instance
        auth_plugin = CentralAuthProviderPlugin()

        # Register with plugin service (this is usually done through DB)
        log.info("Registering central auth plugin: %s",
                 CENTRAL_AUTH_PROVIDER_SLUG)

        # Note: In a real implementation, you would register this through
        # Dispatch's plugin management system, likely via database entries
        # This is a simplified registration for demonstration

        return auth_plugin

    except ImportError as e:
        log.error("Failed to register plugin - missing modules: %s", str(e))
        return None
    except Exception as e:
        log.error("Failed to register central auth plugin: %s", str(e))
        return None


def initialize_central_auth_integration():
    """
    Initialize complete central auth integration with Dispatch.

    This is the main entry point for enabling central authentication
    in a Dispatch instance.
    """
    log.info("Initializing central auth integration...")

    # Step 1: Patch configuration
    config_success = patch_dispatch_config()
    if not config_success:
        log.warning(
            "Configuration patch failed, central auth may not work properly")

    # Step 2: Register plugin
    plugin = register_central_auth_plugin()
    if not plugin:
        log.error("Plugin registration failed, central auth unavailable")
        return False

    # Step 3: Health check
    health = plugin.health_check()
    log.info("Central auth health check: %s", health)

    if health.get("status") == "healthy":
        log.info("✅ Central auth integration initialized successfully")
        return True
    else:
        log.warning("⚠️ Central auth integration initialized with warnings: %s",
                    health.get("message"))
        return True


def setup_central_auth_middleware(app):
    """
    Setup central auth middleware for a FastAPI/Starlette app.

    This adds the central auth middleware to the application middleware stack.
    """
    try:
        from .config import CENTRAL_AUTH_ENABLED
        from .middleware import CentralAuthMiddleware

        if not CENTRAL_AUTH_ENABLED:
            log.info("Central auth disabled, skipping middleware setup")
            return

        # Add central auth middleware
        app.add_middleware(CentralAuthMiddleware)

        log.info("Central auth middleware added to application")

    except Exception as e:
        log.error("Failed to setup central auth middleware: %s", str(e))


# Environment setup function for easy integration
def setup_central_auth(app=None):
    """
    Complete setup function for central auth integration.

    Args:
        app: FastAPI/Starlette application instance (optional)

    Returns:
        Boolean indicating success
    """
    success = initialize_central_auth_integration()

    if app and success:
        setup_central_auth_middleware(app)

    return success
