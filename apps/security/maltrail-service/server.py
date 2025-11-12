#!/usr/bin/env python3
"""
Maltrail Server Entry Point

This script provides the main entry point for running the Maltrail server
following NX best practices.
"""

import os
import sys
from pathlib import Path

# Add the src directory to Python path for imports
current_dir = Path(__file__).parent
src_dir = current_dir / "src"
sys.path.insert(0, str(src_dir))

# Change to the source directory so relative paths work correctly
os.chdir(src_dir / "maltrail")

if __name__ == "__main__":
    # Import and run the original server main function directly
    from maltrail.server import main
    main()
