# MISP Multi-Target Build System Migration Plan

## Overview
MISP supports multiple deployment targets and build configurations that must be preserved during migration to the modular monolith architecture.

## Current Build Targets Identified

### 1. Web Application (Primary Target)
- **Platform**: Apache + PHP + MySQL/MariaDB stack
- **Target OS**: Ubuntu 22.04, Debian 12/13
- **Configuration**: Standard LAMP stack deployment
- **Entry Point**: Apache web server with mod_php
- **Build Process**: Composer dependencies + PHP configuration

### 2. Debian Package (.deb)
- **Build Script**: `build-deb.sh`
- **Configuration**: `debian/` directory with package metadata
- **Target**: Debian/Ubuntu systems via APT package manager
- **Dependencies**: Defined in `debian/control`
- **Installation**: Automated via `dpkg-buildpackage`

### 3. Container/Docker Deployment
- **Inferred from**: GitHub Actions workflow setup
- **Components**: Redis, MariaDB, Apache containers
- **Orchestration**: Docker Compose configuration
- **Environment**: Containerized microservices architecture

### 4. Development Environment
- **Build Tool**: GitHub Actions + CI/CD pipeline
- **Test Matrix**: PHP 8.1, 8.3 across Ubuntu 22.04
- **Components**: Apache, MariaDB, Redis, Python virtual environment
- **Testing**: PHPUnit, PyMISP, comprehensive integration tests

## Build Configuration Analysis

### PHP Build System
```makefile
# from app/Makefile
check-style:     # PHP CodeSniffer - CakePHP standards
check-cpd:       # PHP Copy/Paste Detector
check-js:        # JavaScript linting (disabled)
check-all-ci:    # Combined CI checks
```

### Composer Dependencies
```json
// from app/composer.json (inferred)
- CakePHP framework core
- PHP extensions: mysql, redis, gd, gnupg, xml, mbstring
- PEAR packages for GPG functionality
- Custom MISP libraries and plugins
```

### Python Virtual Environment
```bash
# from GitHub Actions workflow
python3 -m virtualenv -p python3 ./venv
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### System Dependencies
```bash
# from INSTALL scripts and debian/control
- Apache2 with mod_php
- MariaDB/MySQL server and client
- Redis server
- PHP 8.1/8.3 with extensions
- Python3 with pip and virtualenv
- GPG for cryptographic operations
- Various system utilities (curl, zip, openssl)
```

## Migration Strategy for Modular Monolith

### Target Build Configurations

#### 1. Development Environment
```yaml
# .github/workflows/test.yml (new)
name: MISP Service Adapter Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-22.04
    strategy:
      matrix:
        python-version: [3.11, 3.12]
    steps:
      - uses: actions/checkout@v4
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: ${{ matrix.python-version }}
      - name: Install dependencies
        run: |
          pip install -r libs/service-adapters/security/requirements.txt
          pip install pytest pytest-cov
      - name: Run tests
        run: |
          pytest tests/security/misp/ -v --cov
```

#### 2. Docker Container Build
```dockerfile
# libs/service-adapters/security/misp/Dockerfile
FROM python:3.12-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gpg \
    curl \
    redis-tools \
    && rm -rf /var/lib/apt/lists/*

# Copy MISP adapter code
COPY libs/service-adapters/security/misp/ /app/misp/
COPY libs/shared/ /app/shared/

# Install Python dependencies
RUN pip install -r /app/misp/requirements.txt

# Set up GPG directory
RUN mkdir -p /app/.gnupg && chmod 700 /app/.gnupg

EXPOSE 8000
CMD ["python", "/app/misp/main.py"]
```

#### 3. Production Deployment
```yaml
# docker-compose.misp.yml
version: '3.8'
services:
  misp-adapter:
    build: ./libs/service-adapters/security/misp/
    environment:
      - REDIS_URL=redis://redis:6379/13
      - DATABASE_URL=postgresql://user:pass@db:5432/misp
      - GPG_HOME=/app/.gnupg
    volumes:
      - misp_gpg:/app/.gnupg
      - misp_files:/app/files
    depends_on:
      - redis
      - postgresql
```

### Build System Components to Preserve

#### 1. Quality Assurance Tools
```python
# tools/quality_check.py (migrated from Makefile)
import subprocess
import sys

def check_code_style():
    """Python equivalent of phpcs check"""
    result = subprocess.run(['black', '--check', 'libs/service-adapters/security/'], 
                          capture_output=True)
    return result.returncode == 0

def check_type_hints():
    """Python equivalent of PHP type checking"""
    result = subprocess.run(['mypy', 'libs/service-adapters/security/'], 
                          capture_output=True)
    return result.returncode == 0

def check_duplicate_code():
    """Python equivalent of phpcpd"""
    result = subprocess.run(['pylint', '--disable=all', '--enable=R0801', 
                           'libs/service-adapters/security/'], capture_output=True)
    return result.returncode == 0
```

#### 2. Configuration Management
```python
# libs/service-adapters/security/misp/config.py
import os
from typing import Dict, Any

class MISPConfig:
    """Configuration management for MISP adapter"""
    
    @classmethod
    def get_config(cls) -> Dict[str, Any]:
        return {
            'redis': {
                'host': os.getenv('REDIS_HOST', '127.0.0.1'),
                'port': int(os.getenv('REDIS_PORT', '6379')),
                'database': int(os.getenv('REDIS_DB', '13')),
            },
            'database': {
                'url': os.getenv('DATABASE_URL', 'postgresql://localhost/misp'),
            },
            'gpg': {
                'homedir': os.getenv('GPG_HOME', '/app/.gnupg'),
                'binary': os.getenv('GPG_BINARY', '/usr/bin/gpg'),
            },
            'email': {
                'from_address': os.getenv('MISP_EMAIL', 'admin@misp.local'),
            }
        }
```

#### 3. Test Framework Integration
```python
# tests/security/misp/conftest.py
import pytest
import tempfile
import subprocess

@pytest.fixture
def misp_config():
    """Test configuration for MISP adapter"""
    with tempfile.TemporaryDirectory() as tmpdir:
        config = {
            'redis': {'host': 'localhost', 'port': 6379, 'database': 15},
            'gpg': {'homedir': f'{tmpdir}/.gnupg'},
            'testing': True
        }
        
        # Set up test GPG environment
        subprocess.run(['gpg', '--batch', '--gen-key', '--homedir', 
                       config['gpg']['homedir']], input=TEST_GPG_CONFIG.encode())
        
        yield config
```

### Compatibility Layer Design

#### 1. API Compatibility
```python
# libs/service-adapters/security/misp/compatibility.py
from typing import Dict, Any
from libs.shared.data.json_converter import JSONConverterTool

class MISPCompatibilityLayer:
    """Maintains API compatibility with original MISP"""
    
    @staticmethod
    def convert_event_for_api(event_data: Dict[str, Any]) -> str:
        """Convert event data to MISP API format"""
        return JSONConverterTool.convert(event_data, raw=False)
    
    @staticmethod
    def validate_attribute_format(attribute: Dict[str, Any]) -> bool:
        """Validate attribute matches MISP schema"""
        required_fields = ['type', 'value', 'category']
        return all(field in attribute for field in required_fields)
```

#### 2. Export Format Preservation
```python
# libs/service-adapters/security/misp/export_compatibility.py
from typing import List, Dict, Any

class ExportCompatibility:
    """Preserve all MISP export format compatibility"""
    
    @staticmethod
    def export_stix2(events: List[Dict[str, Any]]) -> str:
        """Export to STIX 2.x format - exact compatibility"""
        # Implementation preserves original STIX export logic
        pass
    
    @staticmethod
    def export_yara(attributes: List[Dict[str, Any]]) -> str:
        """Export to YARA rules - exact compatibility"""
        # Implementation preserves original YARA export logic
        pass
```

## Build Automation Integration

### Makefile Integration
```makefile
# Makefile (root level)
.PHONY: build-misp test-misp lint-misp

build-misp:
	cd libs/service-adapters/security/misp && docker build -t misp-adapter .

test-misp:
	pytest tests/security/misp/ -v --cov=libs/service-adapters/security/misp

lint-misp:
	black --check libs/service-adapters/security/misp/
	mypy libs/service-adapters/security/misp/
	
install-misp-deps:
	pip install -r libs/service-adapters/security/misp/requirements.txt
```

### Package Distribution
```python
# libs/service-adapters/security/misp/setup.py
from setuptools import setup, find_packages

setup(
    name="misp-service-adapter",
    version="2.5.0",
    packages=find_packages(),
    install_requires=[
        "fastapi>=0.104.0",
        "redis>=5.0.1",
        "python-gnupg>=0.5.0",
        "cryptography>=41.0.0",
        "pymisp>=2.5.17",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "mypy>=1.5.0",
        ]
    },
    python_requires=">=3.11",
    entry_points={
        "console_scripts": [
            "misp-adapter=misp_adapter.main:main",
        ],
    },
)
```

## Migration Completion Criteria

### Build System Validation
1. **Development Environment**: All tests pass in Python 3.11/3.12
2. **Docker Build**: Container builds successfully and passes health checks
3. **API Compatibility**: All original MISP API endpoints work identically
4. **Export Formats**: All 25+ export formats produce identical output
5. **Performance**: Build and test times within 20% of original

### Quality Assurance
1. **Code Quality**: Black, mypy, pylint all pass
2. **Test Coverage**: 80%+ coverage on all migrated components
3. **Integration Tests**: Full workflow tests with real MISP data
4. **Security Tests**: GPG operations, encryption validation
5. **Load Tests**: Performance under concurrent load

This migration plan ensures all MISP build targets and deployment scenarios are preserved while modernizing the architecture for the modular monolith.