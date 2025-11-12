#!/usr/bin/env python3
"""
Script to fix the double core imports in Maltrail files
"""

import os
import re


def fix_double_core_imports(file_path):
    """Fix imports from '.core.core.' to '.core.' and similar issues"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        original_content = content

        # Fix double core imports: .core.core. -> .core.
        content = re.sub(r'\.core\.core\.', '.core.', content)

        # Fix double plugins imports: .plugins.plugins. -> .plugins.
        content = re.sub(r'\.plugins\.plugins\.', '.plugins.', content)

        # Fix double trails imports: .trails.trails. -> .trails.
        content = re.sub(r'\.trails\.trails\.', '.trails.', content)

        # Fix double thirdparty imports: .thirdparty.thirdparty. -> .thirdparty.
        content = re.sub(r'\.thirdparty\.thirdparty\.',
                         '.thirdparty.', content)

        # For files within core/ directory, imports to sibling modules should not have .core.
        if '/core/' in file_path:
            # from .core.module -> from .module (within core directory)
            content = re.sub(r'^from \.core\.', 'from .',
                             content, flags=re.MULTILINE)

        # For files within plugins/ directory
        if '/plugins/' in file_path:
            # from .plugins.module -> from .module (within plugins directory)
            content = re.sub(r'^from \.plugins\.', 'from .',
                             content, flags=re.MULTILINE)

        # For files within trails/ directory
        if '/trails/' in file_path:
            # from .trails.module -> from .module (within trails directory)
            content = re.sub(r'^from \.trails\.', 'from .',
                             content, flags=re.MULTILINE)

        # For files within thirdparty/ directory
        if '/thirdparty/' in file_path:
            # from .thirdparty.module -> from .module (within thirdparty directory)
            content = re.sub(r'^from \.thirdparty\.', 'from .',
                             content, flags=re.MULTILINE)

        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Fixed: {file_path}")

    except Exception as e:
        print(f"Error fixing {file_path}: {e}")


def main():
    """Main function to fix all Python files in the maltrail package"""
    src_dir = "/workspaces/modular-monolith-2/apps/maltrail-service/src/maltrail"

    # Find all Python files
    python_files = []
    for root, dirs, files in os.walk(src_dir):
        for file in files:
            if file.endswith('.py'):
                python_files.append(os.path.join(root, file))

    print(f"Found {len(python_files)} Python files to check")

    for file_path in python_files:
        fix_double_core_imports(file_path)

    print("Import fix complete!")


if __name__ == "__main__":
    main()
