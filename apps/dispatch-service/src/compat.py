"""
Compatibility layer for Dispatch imports during migration.

This module provides import compatibility for existing Dispatch modules
while we transition to the new shared library structure.
"""

import logging

log = logging.getLogger(__name__)

# Try to import from shared libraries first, fall back to local imports
try:
    # These will be available once the shared libraries are properly set up
    from dispatch_core.enums import *  # noqa: F403, F401
    from dispatch_core.exceptions import *  # noqa: F403, F401
    from dispatch_core.types import *  # noqa: F403, F401
    from dispatch_core.utils import *  # noqa: F403, F401
    log.info("Using dispatch_core shared library")
except ImportError:
    log.warning("dispatch_core not available, using local fallbacks")

try:
    from dispatch_database import *  # noqa: F403, F401
    log.info("Using dispatch_database shared library")
except ImportError:
    log.warning("dispatch_database not available, using local fallbacks")

# Create compatibility imports for the old dispatch.* structure
# This allows existing code to work while we migrate
try:
    # Import from the actual location in the database library
    import os
    import sys

    # Add the database library to Python path for import compatibility
    db_lib_path = os.path.join(
        os.path.dirname(__file__),
        "..", "..", "..", "libs", "dispatch-database", "src"
    )
    if os.path.exists(db_lib_path):
        sys.path.insert(0, os.path.abspath(db_lib_path))
        log.info(f"Added database library path: {db_lib_path}")

except Exception as e:
    log.warning(f"Could not set up compatibility imports: {e}")

# Re-export common items that other modules expect
__all__ = [
    "log",
]
