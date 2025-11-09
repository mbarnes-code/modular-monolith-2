#!/usr/bin/env python3
"""Renumber tasks in Phase 4 onwards in tasks.md after Phase 3 handoff protocol changes."""

import re
from pathlib import Path


def renumber_phase4_tasks(file_path: Path, phase4_start: int = 314):
    """Renumber all tasks in Phase 4 and beyond starting from specified number."""

    with open(file_path, 'r') as f:
        content = f.read()

    # Find Phase 4 start
    phase4_match = re.search(r'^## Phase 4:', content, re.MULTILINE)
    if not phase4_match:
        print("Could not find Phase 4 start")
        return

    phase4_pos = phase4_match.start()
    before_phase4 = content[:phase4_pos]
    phase4_onwards = content[phase4_pos:]

    # Find all task numbers in Phase 4 onwards
    task_pattern = r'- \[ \] T(\d{3})'
    tasks_found = re.findall(task_pattern, phase4_onwards)

    print(f"Found {len(tasks_found)} tasks in Phase 4 onwards")
    print(f"Current range: T{min(tasks_found)}-T{max(tasks_found)}")
    print(
        f"Target range: T{phase4_start:03d}-T{phase4_start + len(tasks_found) - 1:03d}")

    # Create mapping of old to new task numbers
    unique_tasks = []
    seen = set()
    for task in re.finditer(task_pattern, phase4_onwards):
        task_num = task.group(1)
        if task_num not in seen:
            unique_tasks.append(task_num)
            seen.add(task_num)

    mapping = {}
    for i, old_num in enumerate(sorted(set(tasks_found), key=int)):
        new_num = phase4_start + i
        mapping[old_num] = f"{new_num:03d}"

    # Apply replacements in reverse order to avoid conflicts
    for old_num in sorted(mapping.keys(), key=int, reverse=True):
        new_num = mapping[old_num]
        # Replace with temporary marker first
        phase4_onwards = re.sub(
            rf'\b T{old_num}\b',
            f' TEMP{new_num}',
            phase4_onwards
        )

    # Convert temporary markers to final numbers
    phase4_onwards = re.sub(r'TEMP(\d{3})', r'T\1', phase4_onwards)

    # Write back
    new_content = before_phase4 + phase4_onwards
    with open(file_path, 'w') as f:
        f.write(new_content)

    print(f"✅ Renumbered {len(mapping)} unique task numbers in Phase 4+")
    print("Sample mappings:")
    for old, new in list(mapping.items())[:10]:
        print(f"  T{old} → T{new}")


if __name__ == '__main__':
    tasks_file = Path(
        '/workspaces/modular-monolith-2/specs/003-brownfield-integration/tasks.md')
    renumber_phase4_tasks(tasks_file, phase4_start=314)
