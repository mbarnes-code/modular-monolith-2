#!/usr/bin/env python3
"""Generate comprehensive verification report for task numbering."""

import re
from collections import defaultdict
from pathlib import Path


def generate_verification_report(file_path: Path):
    """Generate detailed verification report."""

    with open(file_path, 'r') as f:
        content = f.read()
        lines = content.splitlines()

    print("=" * 80)
    print("TASK NUMBERING VERIFICATION REPORT")
    print("=" * 80)

    # 1. Check sequential task definitions
    task_pattern = r'^- \[ \] T(\d{3})'
    tasks = re.findall(task_pattern, content, re.MULTILINE)

    print(f"\n1. TASK DEFINITIONS:")
    print(f"   Total tasks found: {len(tasks)}")
    print(f"   Range: T{min(tasks)}-T{max(tasks)}")

    # Check for duplicates
    duplicates = [t for t in set(tasks) if tasks.count(t) > 1]
    if duplicates:
        print(
            f"   ⚠️  DUPLICATES: {len(duplicates)} task numbers appear multiple times")
        for dup in sorted(duplicates)[:5]:
            print(f"      T{dup} appears {tasks.count(dup)} times")
    else:
        print(f"   ✅ No duplicate task definitions")

    # Check for gaps
    task_nums = [int(t) for t in tasks]
    expected = set(range(1, len(tasks) + 1))
    actual = set(task_nums)
    gaps = expected - actual
    if gaps:
        print(f"   ⚠️  GAPS: {len(gaps)} missing task numbers")
        print(f"      Missing: {sorted(list(gaps))[:10]}")
    else:
        print(f"   ✅ No gaps in sequence")

    # 2. Check task references
    print(f"\n2. TASK REFERENCES:")
    ref_pattern = r'\bT(\d{3})\b'
    all_refs = re.findall(ref_pattern, content)
    ref_count = defaultdict(int)
    for ref in all_refs:
        ref_count[ref] += 1

    # Find references to non-existent tasks
    valid_tasks = set(tasks)
    invalid_refs = {ref for ref in ref_count.keys() if ref not in valid_tasks}

    if invalid_refs:
        print(
            f"   ⚠️  INVALID REFERENCES: {len(invalid_refs)} references to non-existent tasks")
        for ref in sorted(invalid_refs)[:10]:
            print(
                f"      T{ref} (referenced {ref_count[ref]} times but not defined)")
    else:
        print(f"   ✅ All task references point to defined tasks")

    # 3. Check handoff protocol tasks
    print(f"\n3. HANDOFF PROTOCOL TASKS:")
    handoff_pattern = r'- \[ \] T(\d{3}) \[P\] \[HANDOFF\]'
    handoff_tasks = re.findall(handoff_pattern, content, re.MULTILINE)
    print(f"   Total handoff tasks: {len(handoff_tasks)}")

    if handoff_tasks:
        print(f"   Range: T{min(handoff_tasks)}-T{max(handoff_tasks)}")

        # Check handoff task continuity
        handoff_nums = sorted([int(t) for t in handoff_tasks])
        if handoff_nums == list(range(handoff_nums[0], handoff_nums[-1] + 1)):
            print(f"   ✅ Handoff tasks are continuous")
        else:
            print(f"   ⚠️  Handoff tasks have gaps")

    # 4. Check phase organization
    print(f"\n4. PHASE ORGANIZATION:")
    phase_pattern = r'^## Phase (\d+):'
    phases = re.findall(phase_pattern, content, re.MULTILINE)
    print(f"   Total phases: {len(phases)}")
    print(f"   Phase numbers: {', '.join(phases)}")

    # 5. Validation tests references
    print(f"\n5. VALIDATION TEST REFERENCES:")
    validation_pattern = r'\(T(\d{3})\)[^)]*validation'
    validation_refs = re.findall(validation_pattern, content, re.IGNORECASE)
    print(f"   Validation references found: {len(validation_refs)}")

    # Check if referenced tests exist
    missing_validation = [
        ref for ref in validation_refs if ref not in valid_tasks]
    if missing_validation:
        print(
            f"   ⚠️  References to non-existent validation tasks: {missing_validation[:5]}")
    else:
        print(f"   ✅ All validation references are valid")

    # 6. Summary
    print(f"\n" + "=" * 80)
    print("SUMMARY:")
    issues = []
    if duplicates:
        issues.append(f"- {len(duplicates)} duplicate task definitions")
    if gaps:
        issues.append(f"- {len(gaps)} gaps in task sequence")
    if invalid_refs:
        issues.append(f"- {len(invalid_refs)} invalid task references")
    if missing_validation:
        issues.append(
            f"- {len(missing_validation)} broken validation references")

    if not issues:
        print("✅ ALL CHECKS PASSED")
        print(
            f"   - {len(tasks)} tasks numbered sequentially from T001-T{len(tasks):03d}")
        print(f"   - No duplicates, gaps, or invalid references")
        print(f"   - {len(handoff_tasks)} handoff tasks properly organized")
    else:
        print("⚠️  ISSUES FOUND:")
        for issue in issues:
            print(f"   {issue}")

    print("=" * 80)


if __name__ == '__main__':
    tasks_file = Path(
        '/workspaces/modular-monolith-2/specs/003-brownfield-integration/tasks.md')
    generate_verification_report(tasks_file)
