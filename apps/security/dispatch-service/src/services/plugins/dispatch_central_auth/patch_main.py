"""
Dispatch Application Integration Patch

This module patches Dispatch's main application to integrate
the central authentication service during startup.
"""

import logging
from typing import Optional

log = logging.getLogger(__name__)


def patch_dispatch_main():
    """
    Patch Dispatch's main application startup to integrate central auth.

    This function should be called early in Dispatch's startup process
    to enable central authentication integration.
    """
    try:
        # Import Dispatch's main application components
        from dispatch.main import app
        from dispatch.plugins.dispatch_central_auth.config import \
            CENTRAL_AUTH_ENABLED
        from dispatch.plugins.dispatch_central_auth.integration import \
            setup_central_auth

        if not CENTRAL_AUTH_ENABLED:
            log.info("Central auth disabled, skipping integration")
            return False

        log.info("Integrating central auth with Dispatch application...")

        # Setup central auth integration
        success = setup_central_auth(app)

        if success:
            log.info("✅ Central auth integration completed")
        else:
            log.warning("⚠️ Central auth integration completed with warnings")

        return success

    except ImportError as e:
        log.error("Cannot patch Dispatch main - missing modules: %s", str(e))
        return False
    except Exception as e:
        log.error("Failed to patch Dispatch main: %s", str(e))
        return False


def add_central_auth_routes(app):
    """
    Add central auth-specific routes to Dispatch application.

    This adds routes for OAuth2 callbacks and auth service integration.
    """
    try:
        from dispatch.plugins.dispatch_central_auth.config import (
            CENTRAL_AUTH_CLIENT_ID, CENTRAL_AUTH_SERVICE_URL)
        from fastapi import APIRouter, Request, Response
        from fastapi.responses import RedirectResponse

        # Create auth router
        auth_router = APIRouter(prefix="/auth", tags=["central-auth"])

        @auth_router.get("/login")
        async def central_auth_login(request: Request):
            """Redirect to central auth service for login."""
            redirect_uri = str(request.url_for("central_auth_callback"))

            # Build OAuth2 authorization URL
            auth_url = (
                f"{CENTRAL_AUTH_SERVICE_URL}/oauth2/authorize"
                f"?response_type=code"
                f"&client_id={CENTRAL_AUTH_CLIENT_ID}"
                f"&redirect_uri={redirect_uri}"
                f"&scope=openid+profile+email"
                f"&state=dispatch_login"
            )

            return RedirectResponse(url=auth_url)

        @auth_router.get("/callback")
        async def central_auth_callback(
            request: Request,
            code: str,
            state: str = None
        ):
            """Handle OAuth2 callback from central auth service."""
            # This would typically exchange the code for tokens
            # and create a session. For now, redirect to main app.

            log.info("OAuth2 callback received: code=%s, state=%s", code, state)

            # TODO: Implement token exchange and session creation

            # Redirect to main Dispatch UI
            return RedirectResponse(url="/")

        @auth_router.post("/logout")
        async def central_auth_logout(request: Request):
            """Logout from central auth service."""
            # Clear local session and redirect to central auth logout
            logout_url = f"{CENTRAL_AUTH_SERVICE_URL}/auth/logout"
            return RedirectResponse(url=logout_url)

        # Add health check route
        @auth_router.get("/health")
        async def central_auth_health():
            """Health check for central auth integration."""
            try:
                from dispatch.plugins.dispatch_central_auth.plugin import \
                    CentralAuthProviderPlugin
                plugin = CentralAuthProviderPlugin()
                return plugin.health_check()
            except Exception as e:
                return {
                    "status": "error",
                    "message": f"Health check failed: {str(e)}"
                }

        # Include auth router in main app
        app.include_router(auth_router)

        log.info("Central auth routes added to application")

    except Exception as e:
        log.error("Failed to add central auth routes: %s", str(e))


def create_dispatch_startup_hook():
    """
    Create a startup hook that can be called from Dispatch's main.py

    Returns a function that can be registered as a startup event handler.
    """

    async def central_auth_startup():
        """Startup hook for central auth integration."""
        log.info("🚀 Initializing Dispatch with central auth integration...")

        try:
            # Patch main application
            success = patch_dispatch_main()

            if success:
                log.info("🔗 Central auth integration initialized successfully")
            else:
                log.warning("⚠️ Central auth integration failed or disabled")

        except Exception as e:
            log.error("❌ Central auth startup hook failed: %s", str(e))

    return central_auth_startup


# Easy integration function for Dispatch main.py
def integrate_central_auth_with_dispatch(app):
    """
    Main integration function to be called from Dispatch's main.py

    This function should be called during Dispatch application setup
    to enable central authentication integration.

    Args:
        app: FastAPI application instance

    Returns:
        Boolean indicating success
    """
    try:
        from dispatch.plugins.dispatch_central_auth.config import \
            CENTRAL_AUTH_ENABLED

        if not CENTRAL_AUTH_ENABLED:
            log.info("Central auth disabled in configuration")
            return True

        log.info("Integrating central auth with Dispatch...")

        # Setup central auth
        success = setup_central_auth(app)

        # Add auth routes
        add_central_auth_routes(app)

        # Add startup hook
        startup_hook = create_dispatch_startup_hook()
        app.add_event_handler("startup", startup_hook)

        log.info("Central auth integration setup completed")
        return success

    except Exception as e:
        log.error("Failed to integrate central auth: %s", str(e))
        return False
