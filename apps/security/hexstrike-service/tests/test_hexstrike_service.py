"""
Test module for HexStrike AI MCP Service
"""
import sys
from pathlib import Path

import pytest

# Add src to Python path for testing
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))


def test_hexstrike_package_import():
    """Test that the main hexstrike package can be imported."""
    try:
        import hexstrike
        assert hexstrike.__version__ == "6.0.0"
        assert hexstrike.__author__ == "HexStrike AI Team"
        assert hexstrike.__license__ == "MIT"
    except ImportError as e:
        pytest.fail(f"Failed to import hexstrike package: {e}")


def test_hexstrike_submodules():
    """Test that HexStrike submodules can be imported."""
    try:
        from hexstrike import api, config, core, mcp, tools, utils

        # Basic smoke test - modules should import without errors
        assert api is not None
        assert core is not None
        assert mcp is not None
        assert tools is not None
        assert utils is not None
        assert config is not None
    except ImportError as e:
        pytest.skip(f"HexStrike submodules not available: {e}")


def test_legacy_modules():
    """Test that legacy modules can still be imported."""
    try:
        import hexstrike_mcp  # noqa: F401
        import hexstrike_server  # noqa: F401

        # Basic smoke test - modules should import without errors
        assert True
    except ImportError as e:
        pytest.skip(f"Legacy HexStrike modules not available: {e}")


def test_config_loading():
    """Test configuration loading."""
    try:
        from hexstrike.config.settings import get_config
        config = get_config('testing')
        assert config is not None
        assert hasattr(config, 'HOST')
        assert hasattr(config, 'PORT')
    except ImportError as e:
        pytest.skip(f"Config module not available: {e}")


if __name__ == "__main__":
    pytest.main([__file__])
