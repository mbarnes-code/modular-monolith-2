#!/usr/bin/env python3
"""
Comprehensive file type enumeration script for the features directory.
Analyzes all files by extension and categorizes them by type and purpose.
"""

import json
import os
import sys
from collections import Counter, defaultdict
from pathlib import Path


def get_file_category(extension):
    """Categorize file extensions by type and purpose."""
    categories = {
        # Programming Languages
        'javascript': ['.js', '.mjs', '.cjs', '.jsx'],
        'typescript': ['.ts', '.tsx', '.d.ts'],
        'python': ['.py', '.pyx', '.pyi', '.pyw'],
        'rust': ['.rs'],
        'go': ['.go'],
        'c_cpp': ['.c', '.cpp', '.cc', '.cxx', '.h', '.hpp', '.hxx'],
        'shell': ['.sh', '.bash', '.zsh', '.fish'],
        'lua': ['.lua'],
        'php': ['.php', '.phtml'],
        'ruby': ['.rb'],
        'java': ['.java'],
        'csharp': ['.cs'],
        'kotlin': ['.kt'],
        'scala': ['.scala'],
        'clojure': ['.clj', '.cljs'],
        'assembly': ['.s', '.S', '.asm'],

        # Web Technologies
        'html': ['.html', '.htm'],
        'css': ['.css', '.scss', '.sass', '.less'],
        'vue': ['.vue'],
        'svelte': ['.svelte'],
        'jsx_components': ['.jsx', '.tsx'],

        # Configuration Files
        'json_config': ['.json'],
        'yaml_config': ['.yml', '.yaml'],
        'toml_config': ['.toml'],
        'ini_config': ['.ini', '.cfg', '.conf'],
        'xml_config': ['.xml'],
        'env_config': ['.env'],

        # Package Management
        'node_deps': ['package.json', 'package-lock.json', 'yarn.lock', 'pnpm-lock.yaml', '.nvmrc', '.yarnrc.yml'],
        'python_deps': ['requirements.txt', 'pyproject.toml', 'setup.py', 'setup.cfg', 'Pipfile', 'Pipfile.lock', 'poetry.lock', 'conda.yaml', 'environment.yml'],
        'rust_deps': ['Cargo.toml', 'Cargo.lock'],
        'go_deps': ['go.mod', 'go.sum'],
        'php_deps': ['composer.json', 'composer.lock'],
        'ruby_deps': ['Gemfile', 'Gemfile.lock'],
        'java_deps': ['pom.xml', 'build.gradle', 'gradle.properties'],

        # Build Systems
        'docker': ['Dockerfile', 'docker-compose.yml', 'docker-compose.yaml', '.dockerignore'],
        'make': ['Makefile', 'makefile', 'GNUmakefile'],
        'cmake': ['CMakeLists.txt', 'cmake'],
        'autotools': ['configure.ac', 'configure.in', 'Makefile.am', 'Makefile.in'],
        'bazel': ['BUILD', 'WORKSPACE', 'BUILD.bazel', 'WORKSPACE.bazel'],
        'ninja': ['build.ninja'],

        # CI/CD
        'github_actions': ['.github'],
        'gitlab_ci': ['.gitlab-ci.yml'],
        'travis': ['.travis.yml'],
        'jenkins': ['Jenkinsfile'],
        'circleci': ['.circleci'],
        'azure_pipelines': ['azure-pipelines.yml'],

        # Quality Assurance
        'linting': ['.eslintrc', '.eslintrc.js', '.eslintrc.json', '.eslintrc.yml', '.prettierrc', '.prettierrc.js', '.prettierrc.json', '.flake8', '.pylintrc', 'tox.ini', '.bandit'],
        'formatting': ['.editorconfig', '.clang-format', 'rustfmt.toml'],
        'git_config': ['.gitignore', '.gitattributes', '.gitmodules'],
        'pre_commit': ['.pre-commit-config.yaml', '.pre-commit-hooks.yaml'],

        # Testing
        'test_config': ['jest.config.js', 'jest.config.json', 'vitest.config.js', 'playwright.config.js', 'cypress.config.js', 'pytest.ini', '.coveragerc', 'karma.conf.js'],
        'test_files': ['.test.', '.spec.', '_test.', 'test_', 'spec_'],

        # Documentation
        'markdown': ['.md', '.markdown', '.mdx'],
        'rst': ['.rst'],
        'asciidoc': ['.adoc', '.asciidoc'],
        'tex': ['.tex', '.latex'],

        # Data Files
        'databases': ['.db', '.sqlite', '.sqlite3', '.sql'],
        'csv_data': ['.csv', '.tsv'],
        'json_data': ['.json', '.jsonl', '.ndjson'],
        'xml_data': ['.xml', '.xsd', '.xsl'],
        'binary_data': ['.bin', '.dat', '.dump'],

        # Images
        'raster_images': ['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp', '.tiff', '.tga'],
        'vector_images': ['.svg', '.eps', '.ai'],
        'icons': ['.ico', '.icns'],

        # Media
        'audio': ['.mp3', '.wav', '.flac', '.ogg', '.aac', '.m4a'],
        'video': ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv'],

        # Archives
        'archives': ['.zip', '.tar', '.gz', '.bz2', '.xz', '.7z', '.rar'],
        'packages': ['.deb', '.rpm', '.msi', '.dmg', '.pkg'],

        # Fonts
        'fonts': ['.ttf', '.otf', '.woff', '.woff2', '.eot'],

        # Security
        'certificates': ['.pem', '.crt', '.key', '.p12', '.pfx'],
        'keys': ['.pub', '.priv', '.gpg'],

        # Logs
        'logs': ['.log', '.out', '.err'],

        # Temporary/Cache
        'temp_cache': ['.tmp', '.temp', '.cache', '.swp', '.bak', '~'],

        # IDE/Editor
        'vscode': ['.vscode'],
        'idea': ['.idea'],
        'eclipse': ['.project', '.classpath'],

        # License/Legal
        'legal': ['LICENSE', 'COPYING', 'COPYRIGHT', 'NOTICE'],

        # Readme/Info
        'readme': ['README', 'readme'],
        'changelog': ['CHANGELOG', 'HISTORY', 'NEWS'],

        # Other
        'patches': ['.patch', '.diff'],
        'executables': ['.exe', '.msi', '.app', '.deb', '.rpm'],
        'libraries': ['.so', '.dll', '.dylib', '.a', '.lib'],
    }

    ext_lower = extension.lower()

    # Check exact matches first
    for category, extensions in categories.items():
        if ext_lower in [e.lower() for e in extensions]:
            return category

    # Check partial matches for test files
    for category, patterns in categories.items():
        if category == 'test_files':
            for pattern in patterns:
                if pattern in ext_lower:
                    return category

    return 'other'


def analyze_features_directory(features_path):
    """Analyze all files in the features directory."""
    results = {
        'total_files': 0,
        'by_extension': Counter(),
        'by_category': Counter(),
        'by_directory': defaultdict(lambda: {
            'total': 0,
            'extensions': Counter(),
            'categories': Counter()
        }),
        'config_files': {
            'package_management': Counter(),
            'build_systems': Counter(),
            'ci_cd': Counter(),
            'quality_assurance': Counter(),
            'testing': Counter()
        },
        'programming_languages': Counter(),
        'top_extensions': Counter(),
        'empty_files': [],
        'large_files': [],
        'duplicate_names': defaultdict(list)
    }

    features_path = Path(features_path)
    file_names = defaultdict(int)

    print(f"Analyzing directory: {features_path}")

    for root, dirs, files in os.walk(features_path):
        # Skip hidden directories and common ignore patterns
        dirs[:] = [d for d in dirs if not d.startswith(
            '.') and d not in ['__pycache__', 'node_modules', 'target', 'build', 'dist']]

        rel_root = Path(root).relative_to(features_path)
        dir_name = str(rel_root).split(
            '/')[0] if str(rel_root) != '.' else 'root'

        for file in files:
            if file.startswith('.'):
                continue

            file_path = Path(root) / file

            try:
                file_size = file_path.stat().st_size

                # Track file statistics
                results['total_files'] += 1

                # Get extension
                if '.' in file:
                    extension = '.' + file.split('.')[-1].lower()
                else:
                    extension = '[no_extension]'

                # Special handling for common config files
                if file in ['Dockerfile', 'Makefile', 'makefile', 'Jenkinsfile']:
                    extension = file.lower()
                elif file.endswith('.lock'):
                    extension = file.lower()
                elif 'requirements' in file.lower() and file.endswith('.txt'):
                    extension = 'requirements.txt'
                elif file == 'package.json':
                    extension = 'package.json'
                elif file.startswith('.'):
                    extension = file.lower()

                results['by_extension'][extension] += 1
                results['top_extensions'][extension] += 1

                # Categorize file
                category = get_file_category(extension)
                results['by_category'][category] += 1

                # Update directory stats
                results['by_directory'][dir_name]['total'] += 1
                results['by_directory'][dir_name]['extensions'][extension] += 1
                results['by_directory'][dir_name]['categories'][category] += 1

                # Track configuration files
                if category in ['node_deps', 'python_deps', 'rust_deps', 'go_deps', 'php_deps', 'ruby_deps', 'java_deps']:
                    results['config_files']['package_management'][extension] += 1
                elif category in ['docker', 'make', 'cmake', 'autotools', 'bazel']:
                    results['config_files']['build_systems'][extension] += 1
                elif category in ['github_actions', 'gitlab_ci', 'travis', 'jenkins', 'circleci']:
                    results['config_files']['ci_cd'][extension] += 1
                elif category in ['linting', 'formatting', 'git_config', 'pre_commit']:
                    results['config_files']['quality_assurance'][extension] += 1
                elif category in ['test_config', 'test_files']:
                    results['config_files']['testing'][extension] += 1

                # Track programming languages
                if category in ['javascript', 'typescript', 'python', 'rust', 'go', 'c_cpp', 'lua', 'php', 'ruby', 'java']:
                    results['programming_languages'][category] += 1

                # Track empty files
                if file_size == 0:
                    results['empty_files'].append(
                        str(file_path.relative_to(features_path)))

                # Track large files (>10MB)
                if file_size > 10 * 1024 * 1024:
                    results['large_files'].append(
                        (str(file_path.relative_to(features_path)), file_size))

                # Track duplicate names
                file_names[file] += 1
                if file_names[file] > 1:
                    results['duplicate_names'][file].append(
                        str(file_path.relative_to(features_path)))

            except (OSError, IOError) as e:
                print(f"Error processing {file_path}: {e}")
                continue

    return results


def format_results_for_markdown(results):
    """Format analysis results for markdown output."""
    md_content = []

    md_content.append("## Comprehensive File Type Analysis")
    md_content.append("")
    md_content.append(f"**Total Files Analyzed**: {results['total_files']:,}")
    md_content.append("")

    # Top file extensions
    md_content.append("### Top 20 File Extensions")
    md_content.append("")
    md_content.append("| Extension | Count | Percentage |")
    md_content.append("|-----------|-------|------------|")

    top_20_extensions = results['top_extensions'].most_common(20)
    for ext, count in top_20_extensions:
        percentage = (count / results['total_files']) * 100
        md_content.append(f"| {ext} | {count:,} | {percentage:.2f}% |")

    md_content.append("")

    # File categories
    md_content.append("### File Categories")
    md_content.append("")
    md_content.append("| Category | Count | Percentage |")
    md_content.append("|----------|-------|------------|")

    sorted_categories = sorted(
        results['by_category'].items(), key=lambda x: x[1], reverse=True)
    for category, count in sorted_categories:
        percentage = (count / results['total_files']) * 100
        md_content.append(
            f"| {category.replace('_', ' ').title()} | {count:,} | {percentage:.2f}% |")

    md_content.append("")

    # Programming languages breakdown
    md_content.append("### Programming Languages Distribution")
    md_content.append("")
    if results['programming_languages']:
        total_prog_files = sum(results['programming_languages'].values())
        md_content.append("| Language | Files | Percentage of Code Files |")
        md_content.append("|----------|-------|-------------------------|")

        sorted_langs = sorted(
            results['programming_languages'].items(), key=lambda x: x[1], reverse=True)
        for lang, count in sorted_langs:
            percentage = (count / total_prog_files) * 100
            md_content.append(
                f"| {lang.replace('_', '/').title()} | {count:,} | {percentage:.2f}% |")
    else:
        md_content.append("No programming language files detected.")

    md_content.append("")

    # Configuration files breakdown
    md_content.append("### Configuration Files Detailed Breakdown")
    md_content.append("")

    for config_type, files in results['config_files'].items():
        if files:
            md_content.append(f"#### {config_type.replace('_', ' ').title()}")
            md_content.append("")
            total_config = sum(files.values())
            md_content.append(f"**Total**: {total_config:,} files")
            md_content.append("")

            sorted_files = sorted(
                files.items(), key=lambda x: x[1], reverse=True)
            for file_type, count in sorted_files:
                md_content.append(f"- **{file_type}**: {count:,} files")
            md_content.append("")

    # Top directories by file count
    md_content.append("### Top Directories by File Count")
    md_content.append("")
    md_content.append(
        "| Directory | Total Files | Top Extension | Top Category |")
    md_content.append(
        "|-----------|-------------|---------------|--------------|")

    sorted_dirs = sorted(results['by_directory'].items(
    ), key=lambda x: x[1]['total'], reverse=True)
    for dir_name, dir_stats in sorted_dirs[:15]:
        top_ext = dir_stats['extensions'].most_common(
            1)[0] if dir_stats['extensions'] else ('[none]', 0)
        top_cat = dir_stats['categories'].most_common(
            1)[0] if dir_stats['categories'] else ('[none]', 0)
        md_content.append(
            f"| {dir_name} | {dir_stats['total']:,} | {top_ext[0]} ({top_ext[1]}) | {top_cat[0].replace('_', ' ').title()} ({top_cat[1]}) |")

    md_content.append("")

    # Large files
    if results['large_files']:
        md_content.append("### Large Files (>10MB)")
        md_content.append("")
        md_content.append("| File Path | Size (MB) |")
        md_content.append("|-----------|-----------|")

        sorted_large = sorted(
            results['large_files'], key=lambda x: x[1], reverse=True)
        for file_path, size in sorted_large[:10]:
            size_mb = size / (1024 * 1024)
            md_content.append(f"| {file_path} | {size_mb:.2f} |")
        md_content.append("")

    # Empty files
    if results['empty_files']:
        md_content.append("### Empty Files")
        md_content.append("")
        md_content.append(f"**Count**: {len(results['empty_files'])} files")
        md_content.append("")
        if len(results['empty_files']) <= 20:
            for empty_file in results['empty_files']:
                md_content.append(f"- {empty_file}")
        else:
            md_content.append(
                "(Too many empty files to list - showing count only)")
        md_content.append("")

    # File extension analysis by directory
    md_content.append("### File Extension Distribution by Directory")
    md_content.append("")

    for dir_name, dir_stats in sorted_dirs[:10]:
        if dir_stats['total'] > 100:  # Only show directories with significant file counts
            md_content.append(
                f"#### {dir_name} ({dir_stats['total']:,} files)")
            md_content.append("")

            top_extensions = dir_stats['extensions'].most_common(10)
            for ext, count in top_extensions:
                percentage = (count / dir_stats['total']) * 100
                md_content.append(
                    f"- **{ext}**: {count:,} files ({percentage:.1f}%)")
            md_content.append("")

    return "\n".join(md_content)


def main():
    """Main execution function."""
    if len(sys.argv) > 1:
        features_path = sys.argv[1]
    else:
        features_path = "/workspaces/modular-monolith-2/features"

    if not os.path.exists(features_path):
        print(f"Error: Directory {features_path} does not exist")
        sys.exit(1)

    print("Starting comprehensive file type analysis...")
    results = analyze_features_directory(features_path)

    print(f"Analysis complete! Found {results['total_files']:,} files")
    print(f"Unique extensions: {len(results['by_extension'])}")
    print(f"File categories: {len(results['by_category'])}")

    # Generate markdown output
    markdown_content = format_results_for_markdown(results)

    # Save results to JSON for potential future use
    json_results = {
        'total_files': results['total_files'],
        'by_extension': dict(results['by_extension']),
        'by_category': dict(results['by_category']),
        'programming_languages': dict(results['programming_languages']),
        'config_files': {k: dict(v) for k, v in results['config_files'].items()},
        'large_files_count': len(results['large_files']),
        'empty_files_count': len(results['empty_files'])
    }

    with open('file_analysis_results.json', 'w') as f:
        json.dump(json_results, f, indent=2)

    print("\nMarkdown content generated!")
    print("JSON results saved to file_analysis_results.json")
    print("\n" + "="*50)
    print(markdown_content)

    return markdown_content


if __name__ == "__main__":
    main()
