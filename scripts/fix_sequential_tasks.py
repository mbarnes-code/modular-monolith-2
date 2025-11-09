#!/usr/bin/env python3
"""Fix task numbering to be completely sequential from T001 to T254."""

import re
from pathlib import Path


def fix_sequential_numbering(file_path: Path):
    """Make all task numbers sequential."""

    with open(file_path, 'r') as f:
        lines = f.readlines()

    # Find all task definitions in order
    task_pattern = r'^- \[ \] T(\d{3})\b'

    # First pass: create ordered list of (line_index, old_task_num)
    task_locations = []
    for i, line in enumerate(lines):
        match = re.match(task_pattern, line)
        if match:
            old_num = match.group(1)
            task_locations.append((i, old_num))

    print(f"Found {len(task_locations)} task definitions")

    # Create old_num -> new_num mapping based on order of appearance
    old_to_new = {}
    for seq_num, (line_idx, old_num) in enumerate(task_locations, start=1):
        new_num = f"{seq_num:03d}"
        if old_num not in old_to_new:
            old_to_new[old_num] = new_num

    print(f"Created {len(old_to_new)} unique mappings")

    # Show which numbers are being changed
    changes = [(old, new) for old, new in old_to_new.items() if old != new]
    if changes:
        print(f"\nChanging {len(changes)} task numbers:")
        for old, new in changes[:10]:
            print(f"  T{old} → T{new}")
        if len(changes) > 10:
            print(f"  ... and {len(changes) - 10} more")

    # Replace in reverse order of task number to avoid conflicts
    # Sort by old number descending
    sorted_mappings = sorted(
        old_to_new.items(), key=lambda x: int(x[0]), reverse=True)

    # Convert entire file to string for easier replacement
    content = ''.join(lines)

    # Replace with temporary markers first
    for old_num, new_num in sorted_mappings:
        # Replace task definitions
        content = re.sub(
            rf'(^- \[ \] )T{old_num}\b',
            rf'\1TEMP{new_num}',
            content,
            flags=re.MULTILINE
        )
        # Replace references in text (but not in TEMP markers)
        content = re.sub(
            rf'(?<!TEMP)\bT{old_num}\b',
            f'TEMP{new_num}',
            content
        )

    # Convert TEMP markers to final T numbers
    content = re.sub(r'TEMP(\d{3})', r'T\1', content)

    # Write back
    with open(file_path, 'w') as f:
        f.write(content)

    print(f"\n✅ Task numbering fixed!")
    print(f"   Task range: T001-T{len(task_locations):03d}")

    # Verify
    verify_sequential(file_path)


def verify_sequential(file_path: Path):
    """Verify tasks are numbered sequentially without duplicates."""
    with open(file_path, 'r') as f:
        content = f.read()

    task_pattern = r'^- \[ \] T(\d{3})'
    tasks = re.findall(task_pattern, content, re.MULTILINE)

    # Check for duplicates
    seen = set()
    duplicates = []
    for task in tasks:
        if task in seen:
            duplicates.append(task)
        seen.add(task)

    if duplicates:
        print(f"\n⚠️  Found {len(duplicates)} duplicate task definitions:")
        for dup in sorted(set(duplicates)):
            count = tasks.count(dup)
            print(f"  T{dup} appears {count} times")
        return False

    # Check for sequential numbering
    task_nums = [int(t) for t in tasks]
    expected = list(range(1, len(task_nums) + 1))

    if task_nums == expected:
        print(f"\n✅ Verification passed:")
        print(
            f"   {len(tasks)} tasks numbered sequentially from T001 to T{len(tasks):03d}")
        print(f"   No duplicates found")
        return True
    else:
        missing = set(expected) - set(task_nums)
        extra = set(task_nums) - set(expected)
        print(f"\n⚠️  Task numbering is not sequential:")
        if missing:
            print(f"   Missing: {sorted(missing)}")
        if extra:
            print(f"   Extra: {sorted(extra)}")
        return False


if __name__ == '__main__':
    tasks_file = Path(
        '/workspaces/modular-monolith-2/specs/003-brownfield-integration/tasks.md')
    print(f"Processing: {tasks_file}\n")
    fix_sequential_numbering(tasks_file)
