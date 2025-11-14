#!/usr/bin/env python3
"""
Workflow Analysis Script

Analyzes all collected workflows to extract patterns, triggers, and capabilities
for integration planning.
"""

import json
import os
from collections import Counter, defaultdict
from pathlib import Path

import yaml


def analyze_workflows():
    """Analyze all collected workflows and generate insights."""

    base_dir = Path(
        "/workspaces/modular-monolith-2/.github/workflows-collection")

    # Storage for analysis
    workflows = []
    triggers = Counter()
    jobs = Counter()
    actions_used = Counter()
    patterns = defaultdict(list)

    # Find all workflow files
    yml_files = list(base_dir.rglob("*.yml"))

    print(f"🔍 Analyzing {len(yml_files)} workflow files...")

    for yml_file in yml_files:
        try:
            with open(yml_file, 'r', encoding='utf-8') as f:
                content = yaml.safe_load(f)

            if not content or not isinstance(content, dict):
                continue

            # Extract workflow info
            workflow_info = {
                'path': str(yml_file.relative_to(base_dir)),
                'name': content.get('name', yml_file.name),
                'triggers': list(content.get('on', {}).keys()) if content.get('on') else [],
                'jobs': list(content.get('jobs', {}).keys()),
                'job_count': len(content.get('jobs', {}))
            }

            workflows.append(workflow_info)

            # Count triggers
            for trigger in workflow_info['triggers']:
                triggers[trigger] += 1

            # Count jobs
            for job in workflow_info['jobs']:
                jobs[job] += 1

            # Analyze job patterns
            for job_name, job_config in content.get('jobs', {}).items():
                if isinstance(job_config, dict) and 'steps' in job_config:
                    for step in job_config['steps']:
                        if 'uses' in step:
                            action = step['uses'].split(
                                '@')[0]  # Remove version
                            actions_used[action] += 1

            # Pattern detection
            if 'docker' in workflow_info['name'].lower():
                patterns['docker_builds'].append(yml_file)
            if 'test' in workflow_info['name'].lower():
                patterns['testing'].append(yml_file)
            if 'release' in workflow_info['name'].lower():
                patterns['releases'].append(yml_file)
            if 'ci' in workflow_info['name'].lower():
                patterns['ci_cd'].append(yml_file)
            if 'security' in workflow_info['name'].lower() or 'codeql' in workflow_info['name'].lower():
                patterns['security'].append(yml_file)

        except Exception as e:
            print(f"⚠️  Error processing {yml_file}: {e}")
            continue

    # Generate analysis report
    report = {
        'total_workflows': len(workflows),
        'top_triggers': dict(triggers.most_common(10)),
        'top_jobs': dict(jobs.most_common(10)),
        'top_actions': dict(actions_used.most_common(15)),
        'patterns': {k: len(v) for k, v in patterns.items()},
        'domain_breakdown': analyze_domains(workflows)
    }

    return report, workflows, patterns


def analyze_domains(workflows):
    """Analyze workflow distribution by domain."""
    domains = defaultdict(int)

    for workflow in workflows:
        path = workflow['path']
        if '/productivity/' in path:
            domains['productivity'] += 1
        elif '/security/' in path:
            domains['security'] += 1
        elif '/tcg/' in path or 'mtg' in path.lower():
            domains['tcg'] += 1
        elif '/ai/' in path or 'claude' in workflow['name'].lower():
            domains['ai'] += 1
        else:
            domains['infrastructure'] += 1

    return dict(domains)


def generate_integration_recommendations(patterns):
    """Generate recommendations for workflow integration."""

    recommendations = []

    if len(patterns['ci_cd']) > 5:
        recommendations.append({
            'type': 'consolidation',
            'title': 'Standardize CI/CD Pipeline',
            'description': f'Found {len(patterns["ci_cd"])} CI workflows that could use a common template',
            'files': [str(p.name) for p in patterns['ci_cd'][:5]]
        })

    if len(patterns['testing']) > 10:
        recommendations.append({
            'type': 'optimization',
            'title': 'Unified Testing Framework',
            'description': f'Found {len(patterns["testing"])} test workflows that could share common patterns',
            'files': [str(p.name) for p in patterns['testing'][:5]]
        })

    if len(patterns['docker_builds']) > 3:
        recommendations.append({
            'type': 'efficiency',
            'title': 'Container Build Optimization',
            'description': f'Found {len(patterns["docker_builds"])} Docker workflows that could use shared build templates',
            'files': [str(p.name) for p in patterns['docker_builds'][:5]]
        })

    return recommendations


if __name__ == "__main__":
    print("🚀 Workflow Collection Analysis")
    print("=" * 50)

    report, workflows, patterns = analyze_workflows()
    recommendations = generate_integration_recommendations(patterns)

    print(f"\n📊 Analysis Results:")
    print(f"   Total Workflows: {report['total_workflows']}")
    print(f"   Domain Breakdown: {report['domain_breakdown']}")
    print(f"   Pattern Distribution: {report['patterns']}")

    print(f"\n🔥 Most Common Triggers:")
    for trigger, count in report['top_triggers'].items():
        print(f"   {trigger}: {count} workflows")

    print(f"\n⚙️  Most Common Actions:")
    for action, count in list(report['top_actions'].items())[:5]:
        print(f"   {action}: {count} uses")

    print(f"\n💡 Integration Recommendations:")
    for rec in recommendations:
        print(f"   🎯 {rec['title']}: {rec['description']}")

    # Save detailed analysis
    output_file = "/workspaces/modular-monolith-2/.github/workflows-collection/analysis.json"
    with open(output_file, 'w') as f:
        json.dump({
            'report': report,
            'workflows': workflows,
            'recommendations': recommendations
        }, f, indent=2)

    print(f"\n✅ Detailed analysis saved to: analysis.json")
    print(f"🎊 Ready for workflow integration planning!")
