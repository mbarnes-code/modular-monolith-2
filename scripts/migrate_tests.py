#!/usr/bin/env python3
"""
Test Migration Script: Move tests from features/ to tests/ with domain classification
Purpose: Discover current tool capabilities through existing test analysis
"""

import os
import shutil
import subprocess
from pathlib import Path
from typing import Dict, List, Tuple

# Domain classifications based on current architecture
DOMAIN_MAPPING = {
    # Security Domain (13 tools)
    'MISP': 'security',
    'HELK': 'security', 
    'CyberChef': 'security',
    'yara-x': 'security',
    'Nemesis': 'security',
    'Ghostwriter': 'security',
    'maltrail': 'security',
    'securityonion': 'security',
    'rita': 'security',
    'blackarch': 'security',
    'onex': 'security',
    'Brute-Ratel-C4-Community-Kit': 'security',
    'apiscout': 'security',
    
    # Productivity Domain (8 tools)
    'actual': 'productivity',
    'mealie': 'productivity',
    'dispatch': 'productivity', 
    'firecrawl': 'productivity',
    'goose': 'productivity',
    'inspector': 'productivity',
    'it-tools': 'productivity',
    'kong': 'productivity',  # Could be infrastructure
    
    # MTG Domain (4 tools)
    'commander-spellbook-backend': 'mtg',
    'commander-spellbook-site': 'mtg',
    'mtg-commander-map': 'mtg',
    'mtg-scripting-toolkit': 'mtg',
    
    # Infrastructure Domain (12 tools)
    'KasmVNC': 'infrastructure',
    'lscript': 'infrastructure',
    'software-forensic-kit': 'infrastructure',
    'meterpreter': 'infrastructure',
    'chroma-mcp': 'infrastructure',
    'FileScopeMCP': 'infrastructure',
    'firecrawl-mcp-server': 'infrastructure',
    'MalwareBazaar_MCP': 'infrastructure',
    'mcp-virustotal': 'infrastructure',
    'n8n-mcp-server': 'infrastructure',
    'hexstrike-ai': 'infrastructure',
    'n8n': 'infrastructure',  # Central orchestration
}

def find_test_directories(features_dir: Path) -> List[Tuple[Path, str, str]]:
    """Find all test directories and classify by domain"""
    test_dirs = []
    
    for feature_dir in features_dir.iterdir():
        if not feature_dir.is_dir():
            continue
            
        feature_name = feature_dir.name
        domain = DOMAIN_MAPPING.get(feature_name, 'unknown')
        
        # Find test directories within this feature
        for root, dirs, files in os.walk(feature_dir):
            for dir_name in dirs:
                if 'test' in dir_name.lower():
                    test_path = Path(root) / dir_name
                    test_dirs.append((test_path, feature_name, domain))
    
    return test_dirs

def analyze_test_content(test_dir: Path) -> Dict[str, any]:
    """Analyze test directory to understand tool capabilities"""
    analysis = {
        'test_files': [],
        'test_types': set(),
        'frameworks': set(),
        'performance_tests': [],
        'integration_tests': [],
        'capabilities': set()
    }
    
    for root, dirs, files in os.walk(test_dir):
        for file in files:
            file_path = Path(root) / file
            
            # Categorize test files
            if any(ext in file.lower() for ext in ['.py', '.js', '.ts', '.php', '.rb', '.go', '.rs']):
                analysis['test_files'].append(str(file_path))
                
                # Try to read first few lines to identify frameworks/capabilities
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read(1000)  # Read first 1000 chars
                        
                        # Identify test frameworks
                        if 'pytest' in content or 'import pytest' in content:
                            analysis['frameworks'].add('pytest')
                        if 'unittest' in content or 'import unittest' in content:
                            analysis['frameworks'].add('unittest')
                        if 'jest' in content or 'describe(' in content:
                            analysis['frameworks'].add('jest')
                        if 'phpunit' in content.lower():
                            analysis['frameworks'].add('phpunit')
                        if 'cargo test' in content or '#[test]' in content:
                            analysis['frameworks'].add('cargo_test')
                            
                        # Identify test types
                        if 'performance' in content.lower() or 'benchmark' in content.lower():
                            analysis['performance_tests'].append(str(file_path))
                        if 'integration' in content.lower() or 'api' in content.lower():
                            analysis['integration_tests'].append(str(file_path))
                            
                        # Extract potential capabilities (simple heuristic)
                        for line in content.split('\n')[:20]:  # First 20 lines
                            if 'def test_' in line or 'it(' in line or 'test(' in line:
                                capability = line.strip().replace('def test_', '').replace('it(', '').split('(')[0]
                                analysis['capabilities'].add(capability)
                                
                except Exception:
                    pass  # Skip files we can't read
    
    return analysis

def migrate_tests():
    """Main migration function"""
    workspace_root = Path('/workspaces/modular-monolith-2')
    features_dir = workspace_root / 'features'
    tests_dir = workspace_root / 'tests'
    
    # Create domain test directories
    for domain in ['security', 'productivity', 'mtg', 'infrastructure', 'integration']:
        (tests_dir / domain).mkdir(parents=True, exist_ok=True)
    
    # Find and analyze all test directories
    test_dirs = find_test_directories(features_dir)
    
    migration_report = {
        'migrated_tools': {},
        'domain_stats': {domain: {'tools': 0, 'test_dirs': 0, 'test_files': 0} 
                        for domain in ['security', 'productivity', 'mtg', 'infrastructure', 'unknown']},
        'capabilities_by_domain': {domain: set() for domain in ['security', 'productivity', 'mtg', 'infrastructure', 'unknown']},
        'frameworks_by_domain': {domain: set() for domain in ['security', 'productivity', 'mtg', 'infrastructure', 'unknown']},
        'performance_test_count': 0,
        'integration_test_count': 0
    }
    
    print(f"Found {len(test_dirs)} test directories across {len(set(t[1] for t in test_dirs))} tools")
    
    for test_path, feature_name, domain in test_dirs:
        print(f"Analyzing {feature_name} ({domain}): {test_path}")
        
        # Analyze test content
        analysis = analyze_test_content(test_path)
        
        # Update migration report
        if feature_name not in migration_report['migrated_tools']:
            migration_report['migrated_tools'][feature_name] = {
                'domain': domain,
                'test_directories': [],
                'analysis': {
                    'total_test_files': 0,
                    'frameworks': set(),
                    'capabilities': set(),
                    'performance_tests': 0,
                    'integration_tests': 0
                }
            }
        
        migration_report['migrated_tools'][feature_name]['test_directories'].append(str(test_path))
        tool_analysis = migration_report['migrated_tools'][feature_name]['analysis']
        tool_analysis['total_test_files'] += len(analysis['test_files'])
        tool_analysis['frameworks'].update(analysis['frameworks'])
        tool_analysis['capabilities'].update(analysis['capabilities'])
        tool_analysis['performance_tests'] += len(analysis['performance_tests'])
        tool_analysis['integration_tests'] += len(analysis['integration_tests'])
        
        # Update domain stats
        migration_report['domain_stats'][domain]['test_dirs'] += 1
        migration_report['domain_stats'][domain]['test_files'] += len(analysis['test_files'])
        migration_report['capabilities_by_domain'][domain].update(analysis['capabilities'])
        migration_report['frameworks_by_domain'][domain].update(analysis['frameworks'])
        migration_report['performance_test_count'] += len(analysis['performance_tests'])
        migration_report['integration_test_count'] += len(analysis['integration_tests'])
        
        # Create target directory
        target_dir = tests_dir / domain / feature_name / test_path.name
        target_dir.parent.mkdir(parents=True, exist_ok=True)
        
        # Copy test directory (don't move, preserve originals)
        if not target_dir.exists():
            shutil.copytree(test_path, target_dir)
            print(f"  Copied to: {target_dir}")
        else:
            print(f"  Already exists: {target_dir}")
    
    # Count tools per domain
    for tool_name, tool_info in migration_report['migrated_tools'].items():
        domain = tool_info['domain']
        migration_report['domain_stats'][domain]['tools'] += 1
    
    # Generate analysis report
    report_path = tests_dir / 'migration_analysis.md'
    with open(report_path, 'w') as f:
        f.write("# Test Migration Analysis Report\n\n")
        f.write(f"**Generated**: {os.popen('date').read().strip()}\n")
        f.write(f"**Purpose**: Analyze existing tool capabilities through test discovery\n\n")
        
        f.write("## Domain Statistics\n\n")
        for domain, stats in migration_report['domain_stats'].items():
            if stats['tools'] > 0:
                f.write(f"### {domain.title()} Domain\n")
                f.write(f"- **Tools**: {stats['tools']}\n")
                f.write(f"- **Test Directories**: {stats['test_dirs']}\n") 
                f.write(f"- **Test Files**: {stats['test_files']}\n")
                f.write(f"- **Frameworks**: {', '.join(migration_report['frameworks_by_domain'][domain])}\n")
                f.write(f"- **Capabilities**: {len(migration_report['capabilities_by_domain'][domain])} discovered\n\n")
        
        f.write("## Tool Analysis\n\n")
        for tool_name, tool_info in sorted(migration_report['migrated_tools'].items()):
            analysis = tool_info['analysis']
            f.write(f"### {tool_name} ({tool_info['domain']})\n")
            f.write(f"- **Test Files**: {analysis['total_test_files']}\n")
            f.write(f"- **Frameworks**: {', '.join(analysis['frameworks'])}\n")
            f.write(f"- **Performance Tests**: {analysis['performance_tests']}\n")
            f.write(f"- **Integration Tests**: {analysis['integration_tests']}\n")
            if analysis['capabilities']:
                f.write(f"- **Capabilities**: {', '.join(list(analysis['capabilities'])[:10])}...\n")
            f.write("\n")
        
        f.write("## Constitutional Compliance Assessment\n\n")
        f.write(f"- **Total Performance Tests**: {migration_report['performance_test_count']}\n")
        f.write(f"- **Total Integration Tests**: {migration_report['integration_test_count']}\n")
        f.write("- **Performance Validation**: Requires analysis of discovered performance tests\n")
        f.write("- **Business Logic Preservation**: Requires comparison with original implementations\n\n")
        
        f.write("## Next Steps\n\n")
        f.write("1. **Performance Baseline**: Run existing performance tests to establish baselines\n")
        f.write("2. **Capability Mapping**: Map discovered capabilities to constitutional requirements\n")
        f.write("3. **Integration Strategy**: Use integration tests as migration validation\n")
        f.write("4. **Business Logic Analysis**: Compare test expectations with integrated implementations\n")
    
    print(f"\nMigration complete! Analysis report: {report_path}")
    return migration_report

if __name__ == '__main__':
    migrate_tests()
