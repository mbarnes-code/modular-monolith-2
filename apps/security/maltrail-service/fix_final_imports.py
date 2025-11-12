#!/usr/bin/env python3
"""
Final import fix script for Maltrail NX reorganization
"""

import os
import re


def fix_remaining_imports(file_path):
    """Fix remaining absolute imports that should be relative"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        original_content = content

        # Determine the directory depth to get to the maltrail package root
        rel_path = file_path.replace(
            '/workspaces/modular-monolith-2/apps/maltrail-service/src/maltrail/', '')
        depth = len(rel_path.split('/')) - 1

        # Create the right number of ../ to get to maltrail package root
        if depth == 0:
            # File is in maltrail root (server.py, sensor.py, __init__.py)
            prefix = "."
        elif depth == 1:
            # File is in core/, plugins/, trails/, thirdparty/
            prefix = ".."
        elif depth == 2:
            # File is in subdirectories like trails/feeds/
            prefix = "../.."
        else:
            # Deeper nesting
            prefix = "../" * depth

        # Fix absolute imports to thirdparty
        content = re.sub(
            r'^from thirdparty', f'from {prefix}.thirdparty', content, flags=re.MULTILINE)
        content = re.sub(r'^import thirdparty',
                         f'from {prefix} import thirdparty', content, flags=re.MULTILINE)

        # Fix absolute imports to core (from files outside core)
        if '/core/' not in file_path:
            content = re.sub(
                r'^from core\.', f'from {prefix}.core.', content, flags=re.MULTILINE)

        # Fix absolute imports to plugins (from files outside plugins)
        if '/plugins/' not in file_path:
            content = re.sub(
                r'^from plugins\.', f'from {prefix}.plugins.', content, flags=re.MULTILINE)

        # Fix absolute imports to trails (from files outside trails)
        if '/trails/' not in file_path:
            content = re.sub(
                r'^from trails\.', f'from {prefix}.trails.', content, flags=re.MULTILINE)

        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Fixed: {file_path}")

    except Exception as e:
        print(f"Error fixing {file_path}: {e}")


def main():
    """Main function to fix all remaining import issues"""
    src_dir = "/workspaces/modular-monolith-2/apps/maltrail-service/src/maltrail"

    # Find all Python files
    python_files = []
    for root, dirs, files in os.walk(src_dir):
        for file in files:
            if file.endswith('.py'):
                python_files.append(os.path.join(root, file))

    print(f"Found {len(python_files)} Python files to check")

    for file_path in python_files:
        fix_remaining_imports(file_path)

    print("Final import fix complete!")


if __name__ == "__main__":
    main()
