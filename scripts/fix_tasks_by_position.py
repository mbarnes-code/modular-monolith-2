#!/usr/bin/env python3
"""Fix task numbering by assigning sequential numbers based on position in file."""

import re
from pathlib import Path


def fix_by_position(file_path: Path):
    """Renumber tasks sequentially based on their position in the file."""

    with open(file_path, 'r') as f:
        lines = f.readlines()

    task_pattern = r'^(- \[ \] )T\d{3}\b'

    # Find all task definition lines and assign new sequential numbers
    new_task_num = 1
    task_map = {}  # line_index -> (old_task, new_task)

    for i, line in enumerate(lines):
        match = re.match(task_pattern, line)
        if match:
            old_match = re.search(r'T(\d{3})', line)
            if old_match:
                old_num = old_match.group(1)
                new_num = f"{new_task_num:03d}"
                task_map[i] = (old_num, new_num)
                new_task_num += 1

    print(f"Found {len(task_map)} task definitions")
    print(f"Will renumber T001-T{new_task_num-1:03d}")

    # Phase 1: Replace task definitions with temporary markers
    for line_idx, (old_num, new_num) in task_map.items():
        lines[line_idx] = re.sub(
            r'^(- \[ \] )T\d{3}\b',
            rf'\1TEMP{new_num}',
            lines[line_idx]
        )

    # Phase 2: Build mapping of all old numbers that appeared to their first new number
    old_to_new_global = {}
    for line_idx, (old_num, new_num) in task_map.items():
        if old_num not in old_to_new_global:
            old_to_new_global[old_num] = new_num

    print(f"\nGlobal mappings for references:")
    sample = list(old_to_new_global.items())[:15]
    for old, new in sample:
        print(f"  T{old} → T{new}")
    if len(old_to_new_global) > 15:
        print(f"  ... and {len(old_to_new_global) - 15} more")

    # Phase 3: Replace references in text (excluding TEMP markers)
    # Sort by old number descending to avoid partial replacements
    sorted_refs = sorted(old_to_new_global.items(),
                         key=lambda x: int(x[0]), reverse=True)

    for i, line in enumerate(lines):
        for old_num, new_num in sorted_refs:
            # Replace T### references but not TEMP### markers
            lines[i] = re.sub(
                rf'(?<!TEMP)\bT{old_num}\b',
                f'TEMPREF{new_num}',
                lines[i]
            )

    # Phase 4: Convert all TEMP markers to final T numbers
    for i, line in enumerate(lines):
        lines[i] = re.sub(r'TEMP(REF)?(\d{3})', r'T\2', lines[i])

    # Write back
    with open(file_path, 'w') as f:
        f.writelines(lines)

    print(f"\n✅ Task numbering fixed!")
    print(f"   Renumbered {len(task_map)} task definitions sequentially")

    # Verify
    verify_result(file_path)


def verify_result(file_path: Path):
    """Verify the result."""
    with open(file_path, 'r') as f:
        content = f.read()

    task_pattern = r'^- \[ \] T(\d{3})'
    tasks = re.findall(task_pattern, content, re.MULTILINE)

    # Check for duplicates
    duplicates = {}
    for task in set(tasks):
        count = tasks.count(task)
        if count > 1:
            duplicates[task] = count

    if duplicates:
        print(
            f"\n⚠️  WARNING: Found {len(duplicates)} duplicate task definitions:")
        for task, count in sorted(duplicates.items())[:10]:
            print(f"  T{task} appears {count} times")
        if len(duplicates) > 10:
            print(f"  ... and {len(duplicates) - 10} more duplicates")
        return False

    # Check sequential
    task_nums = [int(t) for t in tasks]
    expected = list(range(1, len(tasks) + 1))

    if task_nums == expected:
        print(f"\n✅ Verification PASSED:")
        print(f"   {len(tasks)} tasks numbered sequentially")
        print(f"   Range: T001-T{len(tasks):03d}")
        print(f"   No duplicates found")
        return True
    else:
        gaps = [i for i in expected if i not in task_nums]
        print(f"\n⚠️  Task sequence has gaps:")
        print(f"   Missing: {gaps[:20]}")
        return False


if __name__ == '__main__':
    tasks_file = Path(
        '/workspaces/modular-monolith-2/specs/003-brownfield-integration/tasks.md')
    print(f"Processing: {tasks_file}\n")
    fix_by_position(tasks_file)
