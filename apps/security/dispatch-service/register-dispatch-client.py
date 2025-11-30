#!/usr/bin/env python3
"""
Register Dispatch Service as OAuth2 Client

This script registers Dispatch with the central authentication service
as an OAuth2/OIDC client to enable SSO integration.
"""

import json
import logging
import os
import sys
from typing import Any, Dict, Optional

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
log = logging.getLogger(__name__)


def register_dispatch_client() -> Optional[Dict[str, Any]]:
    """Register Dispatch as OAuth2 client in central auth service."""

    # Configuration
    auth_service_url = os.getenv(
        'CENTRAL_AUTH_SERVICE_URL', 'http://localhost:3001')
    dispatch_base_url = os.getenv('DISPATCH_BASE_URL', 'http://localhost:8080')
    admin_api_key = os.getenv('CENTRAL_AUTH_ADMIN_API_KEY')

    if not admin_api_key:
        log.error("CENTRAL_AUTH_ADMIN_API_KEY environment variable required")
        return None

    log.info("Registering Dispatch as OAuth2 client...")
    log.info(f"  Auth Service: {auth_service_url}")
    log.info(f"  Dispatch URL: {dispatch_base_url}")

    try:
        import httpx

        # Dispatch OAuth2 client configuration
        client_config = {
            "client_id": "dispatch-service",
            "client_name": "Dispatch Incident Management",
            "client_type": "confidential",
            "grant_types": ["authorization_code", "refresh_token"],
            "response_types": ["code"],
            "redirect_uris": [
                f"{dispatch_base_url}/api/v1/auth/callback",
                f"{dispatch_base_url}/auth/callback",
            ],
            "scopes": ["openid", "profile", "email"],
            "token_endpoint_auth_method": "client_secret_basic",
            "application_metadata": {
                "description": "Dispatch Incident Management and Response Platform",
                "homepage": dispatch_base_url,
                "logo_uri": f"{dispatch_base_url}/static/dispatch/logo.png",
                "policy_uri": f"{dispatch_base_url}/privacy",
                "tos_uri": f"{dispatch_base_url}/terms",
            },
        }

        # Register with central auth service
        with httpx.Client() as client:
            response = client.post(
                f"{auth_service_url}/admin/oauth2/clients",
                json=client_config,
                headers={
                    "X-API-Key": admin_api_key,
                    "Content-Type": "application/json",
                },
                timeout=30,
            )

            if response.status_code == 200 or response.status_code == 201:
                result = response.json()
                client_id = result.get("client_id")
                client_secret = result.get("client_secret")

                log.info("✅ Dispatch OAuth2 client registered successfully!")

                # Output configuration
                print("\n" + "="*60)
                print("📋 DISPATCH CENTRAL AUTH CONFIGURATION")
                print("="*60)
                print()
                print("Add these environment variables to your Dispatch configuration:")
                print()
                print(f"CENTRAL_AUTH_ENABLED=true")
                print(f"CENTRAL_AUTH_SERVICE_URL={auth_service_url}")
                print(f"CENTRAL_AUTH_CLIENT_ID={client_id}")
                print(f"CENTRAL_AUTH_CLIENT_SECRET={client_secret}")
                print(
                    f"DISPATCH_AUTHENTICATION_PROVIDER_SLUG=dispatch-auth-provider-central")
                print()
                print("🔗 OIDC Discovery Endpoint:")
                print(f"{auth_service_url}/oauth2/.well-known/openid_configuration")
                print()

                # Save to .env file
                env_content = f"""
# Dispatch Central Auth Configuration (Generated {import_datetime()})
CENTRAL_AUTH_ENABLED=true
CENTRAL_AUTH_SERVICE_URL={auth_service_url}
CENTRAL_AUTH_CLIENT_ID={client_id}
CENTRAL_AUTH_CLIENT_SECRET={client_secret}
DISPATCH_BASE_URL={dispatch_base_url}
DISPATCH_AUTHENTICATION_PROVIDER_SLUG=dispatch-auth-provider-central
"""

                with open('.env.dispatch-sso', 'w') as f:
                    f.write(env_content.strip())

                print("💾 Configuration saved to .env.dispatch-sso")
                print()

                return {
                    "client_id": client_id,
                    "client_secret": client_secret,
                    "auth_service_url": auth_service_url,
                    "dispatch_url": dispatch_base_url,
                }

            else:
                log.error(
                    f"Failed to register client. Status: {response.status_code}")
                log.error(f"Response: {response.text}")
                return None

    except ImportError:
        log.error("httpx library required. Install with: pip install httpx")
        return None
    except Exception as e:
        log.error(f"Error registering Dispatch client: {str(e)}")
        return None


def import_datetime():
    """Import datetime to avoid issues in f-strings."""
    from datetime import datetime
    return datetime.now().isoformat()


def validate_environment():
    """Validate required environment variables."""
    required_vars = [
        'CENTRAL_AUTH_SERVICE_URL',
        'CENTRAL_AUTH_ADMIN_API_KEY',
        'DISPATCH_BASE_URL',
    ]

    missing = []
    for var in required_vars:
        if not os.getenv(var):
            missing.append(var)

    if missing:
        log.error("Missing required environment variables:")
        for var in missing:
            log.error(f"  {var}")

        print("\nExample usage:")
        print("CENTRAL_AUTH_SERVICE_URL=http://localhost:3001 \\")
        print("CENTRAL_AUTH_ADMIN_API_KEY=your-admin-key \\")
        print("DISPATCH_BASE_URL=http://localhost:8080 \\")
        print("python register-dispatch-client.py")

        return False

    return True


def check_auth_service_health():
    """Check if central auth service is accessible."""
    auth_service_url = os.getenv(
        'CENTRAL_AUTH_SERVICE_URL', 'http://localhost:3001')

    try:
        import httpx
        with httpx.Client() as client:
            response = client.get(f"{auth_service_url}/health", timeout=10)
            if response.status_code == 200:
                log.info("✅ Central auth service is accessible")
                return True
            else:
                log.warning(
                    f"⚠️ Auth service returned status {response.status_code}")
                return False
    except ImportError:
        log.warning("Cannot check auth service health - httpx not available")
        return True
    except Exception as e:
        log.error(f"❌ Cannot reach auth service: {str(e)}")
        return False


def main():
    """Main function."""
    print("🔧 Dispatch Central Auth Registration")
    print("=====================================")
    print()

    # Validate environment
    if not validate_environment():
        sys.exit(1)

    # Check auth service health
    if not check_auth_service_health():
        response = input(
            "Auth service not accessible. Continue anyway? (y/N): ")
        if response.lower() != 'y':
            sys.exit(1)

    # Register client
    result = register_dispatch_client()
    if result:
        print("🎉 Setup completed successfully!")
        print()
        print("Next steps:")
        print("1. Copy the environment variables to your Dispatch .env file")
        print("2. Restart Dispatch service with central auth configuration")
        print("3. Access Dispatch and test SSO login")
        sys.exit(0)
    else:
        print("❌ Registration failed. Check logs above.")
        sys.exit(1)


if __name__ == "__main__":
    main()
