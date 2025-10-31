# MISP Development Tooling Migration Plan

## Overview
MISP contains extensive development tooling for code generation, documentation creation, and development workflow automation that must be preserved and integrated into the modular monolith toolchain.

## Current Development Tools Identified

### 1. Code Generation Tools

#### Type/Category Generator (`gen_misp_types_categories.py`)
- **Function**: Generates MISP attribute types and categories from PHP source
- **Outputs**: Updates multiple repositories (PyMISP, misp-book, misp-website, misp-rfc)
- **Usage**: Maintains consistency across MISP ecosystem documentation
- **Migration Priority**: High - Critical for data model consistency

#### Configuration Generator (`misp-config`)
- **Function**: Perl script for MISP configuration management
- **Features**: Dumps/applies configuration via CakePHP console
- **Usage**: System administration and deployment automation
- **Migration Priority**: Medium - Replaced by unified config management

### 2. Documentation Generators

#### Changelog Generator (`gen_misp_changelog.py`)
- **Function**: Sanitizes gitchangelog output for documentation
- **Output**: Clean changelog for releases
- **Usage**: Release management and documentation
- **Migration Priority**: Low - Standard git tools available

#### Install Documentation Generator (`gen_misp_install_docs.sh`)
- **Function**: Generates installation documentation
- **Integration**: Multi-repository documentation updates
- **Usage**: Maintains installation guides across platforms
- **Migration Priority**: Medium - Documentation automation

### 3. Development Workflow Tools

#### PR Testing Script (`testPR.sh`)
- **Function**: Automated PR testing with backup/restore
- **Features**: Branch switching, git management, backup creation
- **Usage**: Development team PR validation workflow
- **Migration Priority**: High - Critical development workflow

#### Update Script (`exp_misp_update_via_github.sh`)
- **Function**: MISP instance updates via Git
- **Features**: Automated deployment from GitHub releases
- **Usage**: Production deployment automation
- **Migration Priority**: High - Deployment automation

### 4. Utility Tools

#### Flag Downloader (`get-flags.py`)
- **Function**: Downloads country flags for UI
- **Usage**: Asset management for web interface
- **Migration Priority**: Low - Static asset management

#### Certificate Tool (`get-misp-automation-client-cert.py`)
- **Function**: Generates client certificates for API access
- **Usage**: Security and authentication setup
- **Migration Priority**: Medium - Security tooling

## Migration Strategy

### Phase 1: Core Code Generation (Week 1)

#### Python Type Generator Migration
```python
# tools/generate_misp_types.py (migrated from gen_misp_types_categories.py)
"""
MISP Type and Category Generator for Modular Monolith
Migrated from tools/gen_misp_types_categories.py
"""

import json
import subprocess
from pathlib import Path
from typing import Dict, Any, List

class MISPTypeGenerator:
    """Generate MISP types and categories for service adapters."""
    
    def __init__(self, misp_source_path: Path):
        self.misp_source_path = misp_source_path
        self.output_path = Path("libs/service-adapters/security/misp/data/")
    
    def extract_php_definitions(self) -> tuple[Dict[str, Any], Dict[str, Any]]:
        """Extract category and type definitions from PHP source."""
        # Read MISP attribute model
        model_file = self.misp_source_path / "app/Model/MispAttribute.php"
        
        # Extract PHP arrays and convert to JSON via PHP CLI
        # (Preserves original logic but updates output location)
        pass
    
    def generate_python_constants(self, categories: Dict, types: Dict) -> None:
        """Generate Python constants file for service adapter."""
        output_file = self.output_path / "misp_constants.py"
        
        with open(output_file, 'w') as f:
            f.write('"""MISP Attribute Types and Categories"""\n\n')
            f.write(f'CATEGORIES = {json.dumps(list(categories.keys()), indent=2)}\n\n')
            f.write(f'TYPES = {json.dumps(list(types.keys()), indent=2)}\n\n')
            f.write('CATEGORY_TYPE_MAPPINGS = {\n')
            for cat, data in categories.items():
                f.write(f'    "{cat}": {json.dumps(data["types"])},\n')
            f.write('}\n')
    
    def generate_json_schema(self, categories: Dict, types: Dict) -> None:
        """Generate JSON schema for API validation."""
        schema = {
            "categories": list(categories.keys()),
            "types": list(types.keys()),
            "mappings": {cat: data["types"] for cat, data in categories.items()}
        }
        
        output_file = self.output_path / "misp_schema.json"
        with open(output_file, 'w') as f:
            json.dump(schema, f, indent=2)
```

#### Configuration Generator Migration
```python
# tools/misp_config_generator.py (migrated from misp-config)
"""
MISP Configuration Generator for FastAPI Service Adapter
Migrated from tools/misp-config (Perl)
"""

import json
import yaml
from pathlib import Path
from typing import Dict, Any

class MISPConfigGenerator:
    """Generate configuration files for MISP service adapter."""
    
    def __init__(self):
        self.config_template = {
            "database": {
                "url": "${DATABASE_URL}",
                "pool_size": 10,
                "echo": False
            },
            "redis": {
                "host": "${REDIS_HOST:-localhost}",
                "port": "${REDIS_PORT:-6379}",
                "database": "${REDIS_DB:-13}"
            },
            "gpg": {
                "homedir": "${GPG_HOME:-/app/.gnupg}",
                "binary": "${GPG_BINARY:-/usr/bin/gpg}"
            },
            "security": {
                "secret_key": "${SECRET_KEY}",
                "api_auth_enabled": True
            }
        }
    
    def generate_development_config(self) -> None:
        """Generate development configuration."""
        config = self.config_template.copy()
        config["debug"] = True
        config["database"]["echo"] = True
        
        output_path = Path("libs/service-adapters/security/misp/config/")
        output_path.mkdir(parents=True, exist_ok=True)
        
        with open(output_path / "development.yaml", 'w') as f:
            yaml.dump(config, f, default_flow_style=False)
    
    def generate_production_config(self) -> None:
        """Generate production configuration template."""
        config = self.config_template.copy()
        config["debug"] = False
        config["logging"] = {"level": "INFO"}
        
        output_path = Path("libs/service-adapters/security/misp/config/")
        with open(output_path / "production.yaml", 'w') as f:
            yaml.dump(config, f, default_flow_style=False)
```

### Phase 2: Development Workflow Integration (Week 2)

#### PR Testing Automation
```python
# tools/test_service_adapter.py (migrated from testPR.sh)
"""
Service Adapter Testing Tool
Migrated from tools/testPR.sh
"""

import subprocess
import tempfile
import shutil
from pathlib import Path
from typing import Optional

class ServiceAdapterTester:
    """Test service adapter changes with backup/restore capability."""
    
    def __init__(self, adapter_path: Path):
        self.adapter_path = adapter_path
        self.backup_path: Optional[Path] = None
    
    def create_backup(self) -> None:
        """Create backup of current adapter state."""
        self.backup_path = Path(tempfile.mkdtemp(prefix="misp_adapter_backup_"))
        shutil.copytree(self.adapter_path, self.backup_path / "adapter")
        print(f"Backup created at: {self.backup_path}")
    
    def restore_backup(self) -> None:
        """Restore from backup."""
        if self.backup_path and self.backup_path.exists():
            shutil.rmtree(self.adapter_path)
            shutil.copytree(self.backup_path / "adapter", self.adapter_path)
            shutil.rmtree(self.backup_path)
            print("Backup restored successfully")
    
    def test_pr_branch(self, pr_number: int) -> bool:
        """Test a specific PR branch."""
        try:
            # Switch to PR branch
            subprocess.run([
                "git", "fetch", "origin", f"pull/{pr_number}/head:PR_{pr_number}"
            ], cwd=self.adapter_path, check=True)
            
            subprocess.run([
                "git", "checkout", f"PR_{pr_number}"
            ], cwd=self.adapter_path, check=True)
            
            # Run tests
            result = subprocess.run([
                "pytest", "tests/security/misp/", "-v"
            ], cwd=Path.cwd())
            
            return result.returncode == 0
            
        except subprocess.CalledProcessError:
            return False
    
    def cleanup_pr_branch(self, pr_number: int) -> None:
        """Clean up PR testing branch."""
        subprocess.run([
            "git", "checkout", "main"
        ], cwd=self.adapter_path)
        
        subprocess.run([
            "git", "branch", "-D", f"PR_{pr_number}"
        ], cwd=self.adapter_path)
```

### Phase 3: Unified Toolchain Integration (Week 3)

#### Makefile Integration
```makefile
# Makefile (root level) - MISP development tools integration
.PHONY: misp-generate-types misp-test-pr misp-config-dev misp-config-prod

# MISP Type Generation
misp-generate-types:
	python tools/generate_misp_types.py --source features/MISP/ --output libs/service-adapters/security/misp/data/

# MISP Configuration Generation  
misp-config-dev:
	python tools/misp_config_generator.py --environment development

misp-config-prod:
	python tools/misp_config_generator.py --environment production

# MISP PR Testing
misp-test-pr:
	@read -p "Enter PR number: " pr; \
	python tools/test_service_adapter.py --pr $$pr --adapter libs/service-adapters/security/misp/

# MISP Service Adapter Development
misp-dev-setup:
	pip install -r libs/service-adapters/security/misp/requirements-dev.txt
	python tools/misp_config_generator.py --environment development
	python tools/generate_misp_types.py --source features/MISP/

# MISP Documentation Generation
misp-docs:
	cd libs/service-adapters/security/misp && python -m pdoc --html --output-dir docs/ misp_adapter/
```

#### NX Workspace Integration
```json
// nx.json - MISP development tools integration
{
  "projects": {
    "misp-service-adapter": {
      "root": "libs/service-adapters/security/misp",
      "sourceRoot": "libs/service-adapters/security/misp/src",
      "projectType": "library",
      "targets": {
        "generate-types": {
          "executor": "@nrwl/workspace:run-commands",
          "options": {
            "command": "python tools/generate_misp_types.py --source features/MISP/"
          }
        },
        "test": {
          "executor": "@nrwl/workspace:run-commands",
          "options": {
            "command": "pytest tests/security/misp/ -v --cov"
          }
        },
        "lint": {
          "executor": "@nrwl/workspace:run-commands",
          "options": {
            "commands": [
              "black --check libs/service-adapters/security/misp/",
              "mypy libs/service-adapters/security/misp/"
            ]
          }
        }
      }
    }
  }
}
```

### Phase 4: Documentation and Release Tools (Week 4)

#### Documentation Generator
```python
# tools/generate_docs.py
"""
Documentation Generator for MISP Service Adapter
"""

import subprocess
from pathlib import Path

class DocumentationGenerator:
    """Generate comprehensive documentation for MISP adapter."""
    
    def __init__(self, adapter_path: Path):
        self.adapter_path = adapter_path
        self.docs_path = adapter_path / "docs"
    
    def generate_api_docs(self) -> None:
        """Generate API documentation from FastAPI app."""
        subprocess.run([
            "python", "-m", "pdoc", 
            "--html", "--output-dir", str(self.docs_path),
            str(self.adapter_path / "src")
        ])
    
    def generate_migration_docs(self) -> None:
        """Generate migration documentation."""
        # Create migration guide from PHP to Python
        pass
    
    def generate_compatibility_matrix(self) -> None:
        """Generate MISP API compatibility matrix."""
        # Document which MISP API endpoints are supported
        pass
```

## Tool Integration Directory Structure

```
tools/
├── misp/
│   ├── generate_types.py          # Type/category generation
│   ├── config_generator.py        # Configuration management
│   ├── test_service_adapter.py    # PR testing automation
│   ├── documentation_generator.py # Documentation automation
│   └── migration_validator.py     # Migration validation
├── shared/
│   ├── git_utils.py               # Git workflow utilities
│   ├── backup_restore.py          # Backup/restore functionality
│   └── config_templates.py        # Configuration templates
└── unified/
    ├── pre_commit_hooks.py        # Pre-commit validation
    ├── release_automation.py      # Release workflow
    └── quality_gates.py           # Quality assurance automation
```

## Integration with Existing Toolchain

### GitHub Actions Integration
```yaml
# .github/workflows/misp-tools.yml
name: MISP Development Tools
on:
  push:
    paths: ['libs/service-adapters/security/misp/**']
  pull_request:
    paths: ['libs/service-adapters/security/misp/**']

jobs:
  generate-types:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.12'
      - name: Generate MISP Types
        run: python tools/misp/generate_types.py --validate
      - name: Check for changes
        run: git diff --exit-code || (echo "Types need regeneration" && exit 1)
  
  test-adapter:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Test Service Adapter
        run: make misp-test
```

### Pre-commit Hooks
```python
# tools/unified/pre_commit_hooks.py
"""Pre-commit hooks for MISP development."""

def validate_misp_types():
    """Ensure MISP types are up to date."""
    pass

def validate_config_consistency():
    """Ensure configuration files are consistent."""
    pass

def run_misp_tests():
    """Run MISP service adapter tests."""
    pass
```

## Migration Completion Criteria

### Tooling Functionality
1. **Type Generation**: Python equivalent produces identical output to PHP version
2. **Configuration Management**: YAML/JSON configs replace PHP config management
3. **PR Testing**: Automated testing with backup/restore functionality
4. **Documentation**: Automated docs generation for service adapter

### Integration Success
1. **Makefile**: All MISP tools accessible via unified Makefile
2. **NX Workspace**: MISP tools integrated with monorepo workflow
3. **GitHub Actions**: Automated validation in CI/CD pipeline
4. **Pre-commit**: Quality gates prevent broken code commits

### Quality Assurance
1. **Test Coverage**: 90%+ coverage on development tools
2. **Documentation**: Comprehensive migration guides and API docs
3. **Compatibility**: 100% functional equivalence with original tools
4. **Performance**: Tool execution time within 20% of original

This migration plan ensures all MISP development tooling is preserved while integrating seamlessly with the modular monolith development workflow.