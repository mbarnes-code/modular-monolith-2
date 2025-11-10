#!/usr/bin/env python3
"""
Simple MISP Cleanup Validation
Execute the cleanup validation for MISP Asset Relocation
"""

from tests.security.MISP.validate_cleanup import MISPCleanupValidator
import os
import sys

sys.path.append('/workspaces/modular-monolith-2')

# Import and run the validation


def main():
    workspace_root = '/workspaces/modular-monolith-2'
    validator = MISPCleanupValidator(workspace_root)

    print("🔍 Starting MISP Cleanup Validation...")
    success = validator.validate_all()

    if success:
        print("\n✅ T2096k Cleanup Validation: COMPLETE")
        print("🎯 Ready to proceed with T2106l Directory Removal")
        return 0
    else:
        print("\n❌ T2096k Cleanup Validation: FAILED")
        print("🔧 Issues must be resolved before cleanup")
        return 1


if __name__ == "__main__":
    result = main()
    print(f"Exit code: {result}")
