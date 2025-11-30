#!/usr/bin/env python3
"""
Test Dispatch Central Auth Integration

This script tests the central authentication integration
with Dispatch to ensure everything is working correctly.
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


def test_auth_plugin():
    """Test the central auth provider plugin."""
    log.info("Testing central auth provider plugin...")

    try:
        # Import the plugin
        from src.services.plugins.dispatch_central_auth.plugin import \
            CentralAuthProviderPlugin

        # Create plugin instance
        plugin = CentralAuthProviderPlugin()

        # Test health check
        health = plugin.health_check()
        log.info(f"Plugin health: {health}")

        if health.get("status") == "error":
            log.error("Plugin health check failed")
            return False

        log.info("✅ Auth plugin test passed")
        return True

    except Exception as e:
        log.error(f"❌ Auth plugin test failed: {str(e)}")
        return False


def test_middleware():
    """Test the central auth middleware."""
    log.info("Testing central auth middleware...")

    try:
        # Import middleware
        from src.services.plugins.dispatch_central_auth.middleware import \
            CentralAuthMiddleware

        # Create mock app
        class MockApp:
            def __init__(self):
                self.middleware_stack = []

        app = MockApp()

        # Create middleware instance
        middleware = CentralAuthMiddleware(app)

        # Test health check
        health = middleware.health_check()
        log.info(f"Middleware health: {health}")

        log.info("✅ Middleware test passed")
        return True

    except Exception as e:
        log.error(f"❌ Middleware test failed: {str(e)}")
        return False


def test_configuration():
    """Test configuration loading."""
    log.info("Testing configuration...")

    try:
        # Import config
        from src.services.plugins.dispatch_central_auth.config import (
            CENTRAL_AUTH_ENABLED, CENTRAL_AUTH_PROVIDER_SLUG,
            CENTRAL_AUTH_SERVICE_URL)

        log.info(f"Central auth enabled: {CENTRAL_AUTH_ENABLED}")
        log.info(f"Auth service URL: {CENTRAL_AUTH_SERVICE_URL}")
        log.info(f"Provider slug: {CENTRAL_AUTH_PROVIDER_SLUG}")

        log.info("✅ Configuration test passed")
        return True

    except Exception as e:
        log.error(f"❌ Configuration test failed: {str(e)}")
        return False


def test_integration():
    """Test integration components."""
    log.info("Testing integration components...")

    try:
        # Import integration
        from src.services.plugins.dispatch_central_auth.integration import (
            initialize_central_auth_integration, patch_dispatch_config)

        # Test config patching (should handle missing modules gracefully)
        config_result = patch_dispatch_config()
        log.info(f"Config patch result: {config_result}")

        log.info("✅ Integration test passed")
        return True

    except Exception as e:
        log.error(f"❌ Integration test failed: {str(e)}")
        return False


def test_client_registration():
    """Test OAuth2 client registration (if auth service available)."""
    log.info("Testing OAuth2 client registration...")

    auth_service_url = os.getenv(
        'CENTRAL_AUTH_SERVICE_URL', 'http://localhost:3001')

    try:
        import httpx

        # Test if auth service is accessible
        with httpx.Client() as client:
            response = client.get(f"{auth_service_url}/health", timeout=5)

            if response.status_code == 200:
                log.info("✅ Central auth service is accessible")

                # Test OIDC discovery endpoint
                discovery_response = client.get(
                    f"{auth_service_url}/oauth2/.well-known/openid_configuration",
                    timeout=5
                )

                if discovery_response.status_code == 200:
                    discovery = discovery_response.json()
                    log.info(f"OIDC issuer: {discovery.get('issuer')}")
                    log.info("✅ OIDC discovery test passed")
                else:
                    log.warning("⚠️ OIDC discovery endpoint not available")

                return True
            else:
                log.warning(
                    f"⚠️ Auth service returned status {response.status_code}")
                return False

    except ImportError:
        log.warning("⚠️ httpx not available, skipping auth service test")
        return True
    except Exception as e:
        log.warning(f"⚠️ Cannot reach auth service: {str(e)}")
        return False


def test_environment():
    """Test environment configuration."""
    log.info("Testing environment configuration...")

    # Check critical environment variables
    required_vars = [
        'CENTRAL_AUTH_ENABLED',
        'CENTRAL_AUTH_SERVICE_URL',
    ]

    optional_vars = [
        'CENTRAL_AUTH_CLIENT_ID',
        'CENTRAL_AUTH_CLIENT_SECRET',
        'REDIS_HOST',
        'REDIS_PORT',
    ]

    # Check required variables
    missing_required = []
    for var in required_vars:
        value = os.getenv(var)
        if value:
            log.info(f"✓ {var}={value}")
        else:
            missing_required.append(var)
            log.warning(f"✗ {var} not set")

    # Check optional variables
    for var in optional_vars:
        value = os.getenv(var)
        if value:
            log.info(f"✓ {var}={value}")
        else:
            log.info(f"- {var} not set (optional)")

    if missing_required:
        log.error(
            f"Missing required environment variables: {missing_required}")
        return False

    log.info("✅ Environment test passed")
    return True


def run_all_tests():
    """Run all integration tests."""
    print("🧪 Dispatch Central Auth Integration Tests")
    print("==========================================")
    print()

    tests = [
        ("Environment Configuration", test_environment),
        ("Configuration Loading", test_configuration),
        ("Auth Plugin", test_auth_plugin),
        ("Auth Middleware", test_middleware),
        ("Integration Components", test_integration),
        ("Client Registration", test_client_registration),
    ]

    results = {}

    for test_name, test_func in tests:
        print(f"Running {test_name}...")
        try:
            result = test_func()
            results[test_name] = result
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"  {status}")
        except Exception as e:
            results[test_name] = False
            print(f"  ❌ ERROR: {str(e)}")
        print()

    # Summary
    passed = sum(1 for r in results.values() if r)
    total = len(results)

    print("📊 Test Results Summary")
    print("======================")
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {test_name}: {status}")

    print()
    print(f"Tests passed: {passed}/{total}")

    if passed == total:
        print("🎉 All tests passed! Central auth integration is ready.")
        return True
    else:
        print("⚠️ Some tests failed. Check configuration and dependencies.")
        return False


def main():
    """Main function."""
    # Set test environment if not configured
    if not os.getenv('CENTRAL_AUTH_ENABLED'):
        os.environ['CENTRAL_AUTH_ENABLED'] = 'true'
        os.environ['CENTRAL_AUTH_SERVICE_URL'] = 'http://localhost:3001'
        os.environ['CENTRAL_AUTH_CLIENT_ID'] = 'dispatch-service'
        print("Using default test configuration...")
        print()

    success = run_all_tests()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
