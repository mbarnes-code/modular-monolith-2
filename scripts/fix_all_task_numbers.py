#!/usr/bin/env python3
"""Comprehensively fix all task numbering in tasks.md to be sequential."""

import re
from pathlib import Path
from typing import Dict, List, Tuple


def fix_task_numbering(file_path: Path):
    """Fix all task numbering issues in tasks.md."""

    with open(file_path, 'r') as f:
        lines = f.readlines()

    # Track all task definitions and references
    task_pattern = r'^- \[ \] T(\d{3})\b'
    reference_pattern = r'\bT(\d{3})\b'

    # First pass: identify all task definitions with their line numbers
    task_definitions = []
    for i, line in enumerate(lines):
        match = re.match(task_pattern, line)
        if match:
            old_num = match.group(1)
            task_definitions.append((i, old_num))

    print(f"Found {len(task_definitions)} task definitions")

    # Create mapping from old to new task numbers
    old_to_new = {}
    for new_idx, (line_idx, old_num) in enumerate(task_definitions, start=1):
        new_num = f"{new_idx:03d}"
        old_to_new[old_num] = new_num

    # Second pass: replace all task numbers (both definitions and references)
    # Use temporary placeholders to avoid conflicts
    for i, line in enumerate(lines):
        # Replace task numbers with temporary placeholders
        for old_num, new_num in old_to_new.items():
            # Replace task definitions
            lines[i] = re.sub(
                rf'^(- \[ \] )T{old_num}\b',
                rf'\1TEMP{new_num}',
                lines[i]
            )
            # Replace task references in text
            lines[i] = re.sub(
                rf'\bT{old_num}\b',
                f'TEMP{new_num}',
                lines[i]
            )

    # Third pass: convert temporary placeholders to final numbers
    for i, line in enumerate(lines):
        lines[i] = re.sub(r'TEMP(\d{3})', r'T\1', lines[i])

    # Write back
    with open(file_path, 'w') as f:
        f.writelines(lines)

    print(f"\n✅ Renumbered {len(old_to_new)} unique task numbers")
    print(f"Task range: T001-T{len(task_definitions):03d}")

    # Show sample mappings
    print("\nSample mappings:")
    for old, new in list(old_to_new.items())[:20]:
        print(f"  T{old} → T{new}")

    if len(old_to_new) > 20:
        print(f"  ... ({len(old_to_new) - 20} more)")

    # Verify no duplicates remain
    verify_no_duplicates(file_path)


def verify_no_duplicates(file_path: Path):
    """Verify there are no duplicate task numbers."""
    with open(file_path, 'r') as f:
        content = f.read()

    task_pattern = r'^- \[ \] T(\d{3})'
    tasks = re.findall(task_pattern, content, re.MULTILINE)

    duplicates = [t for t in set(tasks) if tasks.count(t) > 1]

    if duplicates:
        print(
            f"\n⚠️  WARNING: Found {len(duplicates)} duplicate task numbers:")
        for dup in sorted(duplicates):
            print(f"  T{dup} appears {tasks.count(dup)} times")
        return False
    else:
        print(f"\n✅ Verification passed: No duplicate task numbers found")
        print(f"   Total unique tasks: {len(set(tasks))}")
        return True


if __name__ == '__main__':
    tasks_file = Path(
        '/workspaces/modular-monolith-2/specs/003-brownfield-integration/tasks.md')
    print(f"Processing: {tasks_file}")
    fix_task_numbering(tasks_file)
