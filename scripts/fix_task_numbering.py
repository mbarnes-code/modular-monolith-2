#!/usr/bin/env python3
"""
Script to fix task numbering in tasks.md file.
This will renumber all tasks sequentially from T001 onwards.
"""

import re


def fix_task_numbering(file_path):
    """Read the file and renumber all tasks sequentially."""

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Split content into lines
    lines = content.split('\n')

    # Track current task number
    current_task_num = 1

    # Process each line
    for i, line in enumerate(lines):
        # Check if this line is a task - handle all variants
        match = re.match(r'^- \[ \] T(\d+[-a-z]*)', line)
        if match:
            old_task_id = match.group(1)
            # Replace with new sequential number
            new_task_id = f"{current_task_num:03d}"
            # Use a more comprehensive regex to catch all variants
            new_line = re.sub(r'^- \[ \] T\d+[-a-z]*',
                              f'- [ ] T{new_task_id}', line)
            lines[i] = new_line
            print(f"Renamed T{old_task_id} -> T{new_task_id}")
            current_task_num += 1

    # Rejoin content
    new_content = '\n'.join(lines)

    # Write back to file
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print(f"\nCompleted renumbering. Total tasks: {current_task_num - 1}")

    return current_task_num - 1


if __name__ == "__main__":
    file_path = "/workspaces/modular-monolith-2/specs/002-mental-prosthetic-refinement/tasks.md"
    total_tasks = fix_task_numbering(file_path)
    print(f"Successfully renumbered {total_tasks} tasks in {file_path}")
