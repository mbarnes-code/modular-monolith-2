#!/usr/bin/env python3
"""
Script to update imports in Maltrail files to use new package structure
"""

import glob
import os
import re


def update_imports_in_file(file_path):
    """Update imports from 'core.' to '.core.' in a Python file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Update imports
        # from core.module -> from .core.module
        content = re.sub(r'^from core\.', 'from .core.',
                         content, flags=re.MULTILINE)

        # import core.module -> from . import core (this is more complex, handle case by case)
        # For now, let's focus on the 'from' imports which are most common

        # from plugins.module -> from .plugins.module
        content = re.sub(r'^from plugins\.', 'from .plugins.',
                         content, flags=re.MULTILINE)

        # from trails.module -> from .trails.module
        content = re.sub(r'^from trails\.', 'from .trails.',
                         content, flags=re.MULTILINE)

        # from thirdparty.module -> from .thirdparty.module
        content = re.sub(r'^from thirdparty\.',
                         'from .thirdparty.', content, flags=re.MULTILINE)

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"Updated: {file_path}")

    except Exception as e:
        print(f"Error updating {file_path}: {e}")


def main():
    """Main function to update all Python files in the maltrail package"""
    src_dir = "/workspaces/modular-monolith-2/apps/maltrail-service/src/maltrail"

    # Find all Python files
    python_files = []
    for root, dirs, files in os.walk(src_dir):
        for file in files:
            if file.endswith('.py'):
                python_files.append(os.path.join(root, file))

    print(f"Found {len(python_files)} Python files to update")

    for file_path in python_files:
        update_imports_in_file(file_path)

    print("Import update complete!")


if __name__ == "__main__":
    main()
