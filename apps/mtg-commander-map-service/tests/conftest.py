"""
Pytest configuration for MTG Commander Map Service
"""
import os
import sys
import pytest

# Add src directory to Python path for imports
PROJECT_ROOT = os.path.dirname(__file__)
SRC_DIR = os.path.join(PROJECT_ROOT, '..', 'src')
sys.path.insert(0, SRC_DIR)


@pytest.fixture(scope="session")
def project_root():
    """Return the project root directory."""
    return os.path.dirname(PROJECT_ROOT)


@pytest.fixture(scope="session")
def src_dir():
    """Return the src directory."""
    return SRC_DIR
