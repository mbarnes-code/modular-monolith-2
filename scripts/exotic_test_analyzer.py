#!/usr/bin/env python3
"""
Deep Dive Analysis: Exotic Testing Patterns and Complex Business Logic
Focuses on the most sophisticated testing scenarios found in the 3,795+ test files
"""

import os
import re
from collections import defaultdict
from pathlib import Path


class ExoticTestAnalyzer:
    def __init__(self, test_dir="/workspaces/modular-monolith-2/tests"):
        self.test_dir = Path(test_dir)
        self.exotic_examples = defaultdict(list)
        self.complex_scenarios = []

    def find_exotic_patterns(self):
        """Find specific examples of exotic testing patterns"""

        print("🔬 Deep diving into exotic testing patterns...")

        # Define exotic patterns to search for
        exotic_patterns = {
            "async_testing": [
                r"async def test_",
                r"@pytest\.mark\.asyncio",
                r"await.*test",
                r"asyncio\.run"
            ],
            "parametrized_testing": [
                r"@pytest\.mark\.parametrize",
                r"@pytest\.fixture\(params=",
                r"pytest\.param"
            ],
            "monkey_patching": [
                r"monkeypatch\.",
                r"@patch\(",
                r"mock\.patch",
                r"Mock\(\)",
                r"MagicMock"
            ],
            "database_testing": [
                r"@pytest\.mark\.django_db",
                r"TransactionTestCase",
                r"rollback",
                r"database\.atomic",
                r"transaction\.on_commit"
            ],
            "integration_testing": [
                r"TestClient",
                r"api_client",
                r"requests\.(get|post|put|delete)",
                r"subprocess\.run",
                r"docker"
            ],
            "performance_testing": [
                r"@pytest\.mark\.benchmark",
                r"timeit",
                r"time\.time",
                r"performance",
                r"load.*test"
            ],
            "security_testing": [
                r"csrf",
                r"xss",
                r"sql.*injection",
                r"authentication",
                r"authorization",
                r"permission"
            ],
            "state_machine_testing": [
                r"state.*machine",
                r"workflow",
                r"transition",
                r"FSM",
                r"state.*change"
            ],
            "event_driven_testing": [
                r"event.*driven",
                r"publish.*subscribe",
                r"message.*queue",
                r"webhook",
                r"callback"
            ],
            "ui_testing": [
                r"render\(",
                r"screen\.",
                r"fireEvent",
                r"@testing-library",
                r"enzyme",
                r"cypress",
                r"playwright"
            ]
        }

        # Search through test files
        for root, dirs, files in os.walk(self.test_dir):
            for file in files:
                if not (file.endswith('.py') or file.endswith('.js') or file.endswith('.ts')):
                    continue

                file_path = Path(root) / file
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()

                    # Check for each exotic pattern
                    for pattern_name, patterns in exotic_patterns.items():
                        for pattern in patterns:
                            matches = re.finditer(
                                pattern, content, re.IGNORECASE | re.MULTILINE)
                            for match in matches:
                                # Get context around match
                                lines = content.split('\n')
                                match_line = content[:match.start()].count(
                                    '\n')

                                # Extract 3 lines of context
                                start_line = max(0, match_line - 1)
                                end_line = min(len(lines), match_line + 2)
                                context = '\n'.join(lines[start_line:end_line])

                                self.exotic_examples[pattern_name].append({
                                    "file": str(file_path.relative_to(self.test_dir)),
                                    "pattern": pattern,
                                    "context": context.strip(),
                                    "line": match_line + 1
                                })

                                # Stop after finding a few examples per pattern per file
                                if len([ex for ex in self.exotic_examples[pattern_name]
                                       if ex["file"] == str(file_path.relative_to(self.test_dir))]) >= 2:
                                    break

                except Exception as e:
                    continue

        self._analyze_complex_scenarios()
        return self.exotic_examples

    def _analyze_complex_scenarios(self):
        """Identify the most complex testing scenarios"""

        # Look for files with multiple exotic patterns
        file_pattern_count = defaultdict(set)

        for pattern_name, examples in self.exotic_examples.items():
            for example in examples:
                file_pattern_count[example["file"]].add(pattern_name)

        # Find files with high complexity (multiple exotic patterns)
        for file_path, patterns in file_pattern_count.items():
            if len(patterns) >= 3:  # Files with 3+ exotic patterns
                self.complex_scenarios.append({
                    "file": file_path,
                    "pattern_count": len(patterns),
                    "patterns": list(patterns),
                    "complexity_score": len(patterns) * 2 + len([p for p in patterns if p in ["async_testing", "state_machine_testing", "event_driven_testing"]])
                })

        # Sort by complexity
        self.complex_scenarios.sort(
            key=lambda x: x["complexity_score"], reverse=True)

    def analyze_business_logic_complexity(self):
        """Analyze the complexity of business logic being tested"""

        print("🧠 Analyzing business logic complexity...")

        business_logic_patterns = {
            "multi_step_workflows": [
                r"step.*\d+",
                r"workflow.*step",
                r"process.*flow",
                r"sequence.*test"
            ],
            "state_transitions": [
                r"state.*from.*to",
                r"transition.*state",
                r"change.*status",
                r"pending.*complete"
            ],
            "complex_algorithms": [
                r"algorithm",
                r"search.*sort",
                r"graph.*traversal",
                r"optimization",
                r"complexity.*O\("
            ],
            "data_consistency": [
                r"consistency",
                r"integrity",
                r"constraint.*violation",
                r"referential.*integrity"
            ],
            "concurrency_control": [
                r"race.*condition",
                r"deadlock",
                r"lock.*contention",
                r"concurrent.*access",
                r"thread.*safe"
            ],
            "business_rule_validation": [
                r"business.*rule",
                r"validation.*rule",
                r"constraint.*check",
                r"policy.*enforcement"
            ]
        }

        business_examples = defaultdict(list)

        for root, dirs, files in os.walk(self.test_dir):
            for file in files:
                if not (file.endswith('.py') or file.endswith('.js') or file.endswith('.ts')):
                    continue

                file_path = Path(root) / file
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()

                    for pattern_name, patterns in business_logic_patterns.items():
                        for pattern in patterns:
                            if re.search(pattern, content, re.IGNORECASE):
                                # Extract function names containing this pattern
                                function_matches = re.finditer(
                                    rf'def (test_[^(]*{pattern.replace(".*", ".*?")}[^(]*)\(',
                                    content, re.IGNORECASE
                                )

                                for match in function_matches:
                                    business_examples[pattern_name].append({
                                        "file": str(file_path.relative_to(self.test_dir)),
                                        "function": match.group(1),
                                        "pattern": pattern
                                    })

                except Exception:
                    continue

        return business_examples

    def generate_exotic_patterns_report(self):
        """Generate detailed report on exotic testing patterns"""

        report = []
        report.append("# Exotic Testing Patterns Analysis")
        report.append("=" * 50)

        # Summary statistics
        total_exotic_examples = sum(len(examples)
                                    for examples in self.exotic_examples.values())
        report.append(f"\n## 📊 Exotic Pattern Statistics")
        report.append(
            f"- **Total Exotic Pattern Instances**: {total_exotic_examples:,}")
        report.append(
            f"- **Unique Pattern Types**: {len(self.exotic_examples)}")
        report.append(
            f"- **Highly Complex Files**: {len(self.complex_scenarios)} (3+ exotic patterns)")

        # Most complex scenarios
        report.append(f"\n## 🚀 Most Complex Testing Scenarios")
        for i, scenario in enumerate(self.complex_scenarios[:10], 1):
            report.append(f"{i}. **{scenario['file']}**")
            report.append(
                f"   - Complexity Score: {scenario['complexity_score']}")
            report.append(f"   - Patterns: {', '.join(scenario['patterns'])}")

        # Detailed pattern analysis
        report.append(f"\n## 🔬 Exotic Pattern Deep Dive")

        for pattern_name, examples in sorted(self.exotic_examples.items(),
                                             key=lambda x: len(x[1]), reverse=True):
            if not examples:
                continue

            report.append(f"\n### {pattern_name.replace('_', ' ').title()}")
            report.append(f"**Occurrences**: {len(examples)}")

            # Show top examples
            unique_files = set(ex["file"] for ex in examples[:5])
            report.append(f"**Example Files**:")
            for file in list(unique_files)[:3]:
                report.append(f"- `{file}`")

            # Show example code
            if examples:
                report.append(f"**Example Code**:")
                report.append(f"```python")
                report.append(
                    f"# From: {examples[0]['file']} (line {examples[0]['line']})")
                report.append(examples[0]['context'])
                report.append(f"```")

        return '\n'.join(report)


def main():
    analyzer = ExoticTestAnalyzer()

    # Find exotic patterns
    exotic_examples = analyzer.find_exotic_patterns()

    # Analyze business logic complexity
    business_examples = analyzer.analyze_business_logic_complexity()

    # Generate report
    report = analyzer.generate_exotic_patterns_report()

    # Add business logic analysis to report
    report += "\n\n" + "=" * 50
    report += "\n# Business Logic Complexity Analysis\n"
    report += f"## 🧠 Complex Business Logic Patterns\n"

    for pattern_name, examples in sorted(business_examples.items(),
                                         key=lambda x: len(x[1]), reverse=True):
        if examples:
            report += f"\n### {pattern_name.replace('_', ' ').title()}\n"
            report += f"**Occurrences**: {len(examples)}\n"
            report += f"**Example Functions**:\n"
            for example in examples[:3]:
                report += f"- `{example['function']}` in `{example['file']}`\n"

    # Save report
    with open('/workspaces/modular-monolith-2/exotic_test_patterns_report.md', 'w') as f:
        f.write(report)

    print(report[:2000] + "..." if len(report) > 2000 else report)
    print(f"\n📁 Detailed report saved: exotic_test_patterns_report.md")


if __name__ == "__main__":
    main()
