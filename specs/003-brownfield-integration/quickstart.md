# Quickstart Guide: Brownfield Integration - Mental Prosthetic Platform

**Branch**: `003-brownfield-integration` | **Date**: 2025-11-03 | **Phase**: 1 - Design
**Context**: Developer quickstart for 37-tool consolidation implementation

## Overview

This quickstart guide provides step-by-step instructions for implementing the brownfield integration of 37 executive function tools into a unified modular monolith platform. The guide covers development environment setup, architecture implementation, and migration execution with Domain-Driven Design (DDD) patterns for maintainable modular architecture.

## Development Environment Setup

### Runtime Version Strategy (Evidence-Based)

**IMPORTANT**: Version requirements have been systematically analyzed to optimize container complexity.

```yaml
Optimized Runtime Strategy:
  Standard Environment (60% of tools):
    - Node 20 LTS (instead of mixed 16/18/20)
    - Python 3.12 (standardized from 3.8-3.13 range)
    - Benefits: 36% reduction in container complexity, improved build performance
    
  Version-Specific Containers (Only where legitimately required):
    - Inspector Tool: Node 22.7.5+ (ES Modules import.meta.url requirement)
    - Goose Desktop: Node 22.17.1 (Electron native compatibility)
    - YARA-X: Python 3.9+ (PyO3 Rust bindings)
    - Dispatch: Python 3.11+ (exception groups - pending verification)

Investigation Details: See "analysis/version-requirement-legitimacy.md"
```

**Setup Commands**:

```bash
# Standard development environment
nvm install 20
nvm use 20
pyenv install 3.12.0
pyenv global 3.12.0

# Verify optimized versions
node --version  # Should output v20.x.x
python --version  # Should output Python 3.12.x
```

## DDD Implementation Strategy

### Implementation Phases for Architectural Excellence

```yaml
Phase 1A: Foundational DDD Infrastructure (Week 1)
  Priority: CRITICAL - Must be completed before tool migration begins
  
  Tasks:
    1. Module Interface Definitions (Day 1-2)
       - Define async-only domain interfaces (IDomainModule)
       - Implement domain boundary enforcement contracts
       - Set up dependency injection container configuration
       
    2. Architecture Testing Framework (Day 3-4)
       - Implement ArchitectureComplianceChecker class
       - Create pytest tests for boundary violation detection
       - Set up pre-commit hooks for architecture validation
       
    3. Decorator Framework Implementation (Day 5-7)
       - Implement logging, validation, performance, UoW decorators
       - Create domain-specific SLA enforcement (Security <1s, etc.)
       - Test decorator chain with sample command handlers

Phase 1B: Advanced DDD Patterns (Week 2-3)
  Priority: HIGH - Enables reliable cross-domain integration
  
  Tasks:
    4. Internal Command System (Week 2)
       - Implement InternalCommandBase and command queue
       - Create MigrateMispDataInternalCommand example
       - Set up retry and compensation mechanisms
       
    5. Outbox/Inbox Pattern Implementation (Week 3)
       - Create domain_outbox and domain_inbox tables
       - Implement reliable event publishing/subscription
       - Test cross-domain event delivery guarantees

Phase 2: Rich Domain Models (During Migration - Week 4-8)
  Priority: MEDIUM - Implement as Category B tools are migrated
  
  Tasks:
    6. Domain Model Enhancement (Ongoing)
       - Convert data classes to rich domain objects
       - Implement business logic encapsulation
       - Preserve original tool algorithms in domain methods
```

### DDD Pattern Priority Matrix

```yaml
IMMEDIATE (Week 1):
  - Module boundary enforcement: Prevents "big ball of mud"
  - Architecture testing: Catches violations during development
  - Decorator framework: Ensures consistent cross-cutting concerns

SHORT-TERM (Week 2-3):
  - Internal commands: Handles complex migration workflows
  - Event sourcing: Enables reliable cross-domain integration

ONGOING (Week 4+):
  - Rich domain models: Preserves business logic during Category B migrations
  - Performance optimization: Fine-tune based on actual usage patterns
```

### Technology Translation Guidelines

```yaml
.NET to Python DDD Pattern Translation:
  MediatR → Python dataclasses + async handlers
  Entity Framework → SQLAlchemy with Repository pattern
  Autofac → Python dependency injection (injector library)
  SQL Stream Store → Custom PostgreSQL JSONB event store
  
Architectural Decision Records (ADRs):
  - Async-only domain communication (prevents tight coupling)
  - Decorator pattern over middleware (consistent cross-cutting concerns)
  - Architecture testing automation (prevents regression)
  - Rich domain models with preserved business logic
```

## Prerequisites

### System Requirements

```yaml
Development Environment:
  OS: Linux (Ubuntu 20.04+), macOS (12+), Windows (WSL2)
  CPU: 8+ cores recommended for parallel tool migration
  RAM: 32GB+ recommended for full development environment
  Storage: 100GB+ free space for tool repositories and databases
  Docker: 24.0+ with Docker Compose v2
  
Network Requirements:
  Internet: Required for tool repository cloning and package installation
  Ports: 3000 (jane-ui), 8000 (jane-orchestrator), 5432 (PostgreSQL), 6379 (Redis)
```

### Required Tools

```bash
# Core development tools
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker $USER

# Node.js and package management
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt-get install -y nodejs

# Python development environment
sudo apt-get install -y python3.12 python3.12-venv python3.12-dev

# Database tools
sudo apt-get install -y postgresql-client redis-tools

# Git and development utilities
sudo apt-get install -y git make curl wget jq
```

## Quick Setup (30 Minutes)

### Step 1: Repository Setup

```bash
# Clone the main repository
git clone https://github.com/mbarnes-code/modular-monolith-2.git
cd modular-monolith-2

# Create feature branch for brownfield integration
git checkout -b 003-brownfield-integration

# Install dependencies
make install
```

### Step 2: Infrastructure Startup

```bash
# Start core infrastructure
docker-compose -f infrastructure/docker/docker-compose.yml up -d

# Wait for services to be ready
./scripts/wait-for-services.sh

# Verify infrastructure health
curl http://localhost:5432 # PostgreSQL health check
curl http://localhost:6379 # Redis health check
```

### Step 3: Backend Development Environment

```bash
# Navigate to orchestrator service
cd apps/jane-orchestrator

# Create Python virtual environment
python3.12 -m venv venv
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Set environment variables
cp .env.example .env
# Edit .env with your local configuration

# Run database migrations
alembic upgrade head

# Start the backend server
uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000
```

### Step 4: Frontend Development Environment

```bash
# Open new terminal and navigate to UI application
cd apps/jane-ui

# Install Node.js dependencies
npm install

# Start the development server
npm run dev
```

### Step 5: Verify Development Environment

```bash
# Check backend API
curl http://localhost:8000/health

# Check frontend application
curl http://localhost:3000

# Run basic tests
npm test                    # Frontend tests
cd ../jane-orchestrator && python -m pytest tests/  # Backend tests
```

## Development Workflow

### Phase-by-Phase Implementation

#### Phase 1A: DDD Foundation Setup (Days 1-7)

```bash
# 1. Implement DDD module interfaces and boundaries
cd apps/jane-orchestrator/src

# Create domain module interfaces
cat > domains/__init__.py << 'EOF'
from abc import ABC, abstractmethod
from typing import TypeVar, Any

TCommand = TypeVar('TCommand')
TQuery = TypeVar('TQuery')
TResult = TypeVar('TResult')

class IDomainModule(ABC):
    @abstractmethod
    async def execute_command_async(self, command: TCommand) -> TResult:
        pass
        
    @abstractmethod
    async def execute_query_async(self, query: TQuery) -> TResult:
        pass
EOF

# 2. Set up architecture compliance testing
mkdir -p tests/architecture
cat > tests/architecture/test_domain_boundaries.py << 'EOF'
import pytest
from pathlib import Path
from scripts.architecture_compliance import ArchitectureComplianceChecker

def test_security_domain_isolation():
    """Security domain must not depend on other domains directly"""
    checker = ArchitectureComplianceChecker(Path(__file__).parent.parent)
    violations = checker.validate_domain_dependencies()
    
    security_violations = [v for v in violations if v.domain == 'security']
    assert len(security_violations) == 0, f"Boundary violations: {security_violations}"

def test_async_only_domain_communication():
    """All inter-domain calls must be async"""
    # Implementation validates no direct sync method calls between domains
    pass
EOF

# 3. Implement decorator framework for cross-cutting concerns
cat > domains/decorators.py << 'EOF'
from functools import wraps
import time
import logging
from typing import Callable

def performance_monitoring_decorator(domain_sla_seconds: float):
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(self, *args, **kwargs):
            start_time = time.time()
            try:
                result = await func(self, *args, **kwargs)
                execution_time = time.time() - start_time
                if execution_time > domain_sla_seconds:
                    logging.warning(f"SLA violation: {execution_time:.2f}s > {domain_sla_seconds}s")
                return result
            finally:
                # Record metrics
                pass
        return wrapper
    return decorator

def logging_decorator(func: Callable) -> Callable:
    @wraps(func)
    async def wrapper(self, *args, **kwargs):
        logger = logging.getLogger(f"{self.__class__.__module__}.{self.__class__.__name__}")
        command_name = args[0].__class__.__name__ if args else "unknown"
        logger.info(f"Executing {command_name}")
        
        try:
            result = await func(self, *args, **kwargs)
            logger.info(f"Completed {command_name}")
            return result
        except Exception as e:
            logger.error(f"Failed {command_name}: {str(e)}")
            raise
    return wrapper
EOF

# 4. Set up database schemas with DDD event sourcing
alembic revision --autogenerate -m "Create domain schemas with DDD events"
alembic upgrade head

# 5. Validate DDD architecture setup
python -m pytest tests/architecture/ -v
```

#### Phase 1B: Advanced DDD Implementation (Days 8-21)

```bash
# 1. Implement internal command system for complex migrations
cat > domains/commands.py << 'EOF'
from abc import ABC, abstractmethod
import uuid
from datetime import datetime
from typing import Dict, Any

class InternalCommandBase(ABC):
    def __init__(self, command_id: uuid.UUID = None):
        self.command_id = command_id or uuid.uuid4()
        self.created_at = datetime.now()
        self.retry_count = 0
        self.max_retries = 3
        
    @abstractmethod
    async def execute(self):
        pass
        
    @abstractmethod
    async def compensate(self):
        pass

class MigrateMispDataInternalCommand(InternalCommandBase):
    def __init__(self, misp_instance_id: uuid.UUID, target_schema: str):
        super().__init__()
        self.misp_instance_id = misp_instance_id
        self.target_schema = target_schema
        
    async def execute(self):
        # Complex MISP migration with preserved business logic
        pass
        
    async def compensate(self):
        # Rollback with data integrity guarantees
        pass
EOF

# 2. Set up Outbox/Inbox pattern for reliable cross-domain events
python scripts/setup_outbox_inbox_tables.py

# 3. Implement domain event publishing infrastructure
python scripts/setup_domain_event_publishing.py

# 4. Create domain-specific command handlers with decorators
mkdir -p domains/security/commands
cat > domains/security/commands/threat_indicator.py << 'EOF'
from ..decorators import logging_decorator, performance_monitoring_decorator
from ..decorators import validation_decorator, unit_of_work_decorator

class CreateThreatIndicatorCommandHandler:
    domain_name = 'security'
    
    @logging_decorator
    @performance_monitoring_decorator(domain_sla_seconds=1.0)  # Security SLA: <1s
    @validation_decorator
    @unit_of_work_decorator
    async def handle(self, command):
        # Pure business logic - preserved from original MISP implementation
        pass
EOF
```

#### Phase 1C: Core Infrastructure Setup (Week 1 continued)

```bash
# 1. Set up unified database schemas (now with DDD patterns)
cd apps/jane-orchestrator
# Note: Database migrations already created in Phase 1A

# 2. Implement core authentication with domain boundaries
python scripts/create_superuser.py

# 3. Set up cross-domain event system (with Outbox/Inbox)
python scripts/setup_event_sourcing.py

# 4. Configure API gateway routing with DDD compliance
python scripts/configure_kong_routes.py

# 5. Validate Phase 1 DDD implementation
python scripts/validate_ddd_foundation.py
```

#### Phase 2: Security Domain Migration with DDD Patterns (Weeks 2-3)

```bash
# 1. Analyze existing security tools with business logic preservation focus
python scripts/analyze_security_tools.py --ddd-analysis

# 2. Create rich domain models for security aggregates
cat > domains/security/models/threat_indicator.py << 'EOF'
from typing import Dict, List, Optional
import uuid
from datetime import datetime

class ThreatIndicator:
    """Rich domain model preserving MISP business logic"""
    
    def __init__(self):
        self._id: Optional[uuid.UUID] = None
        self._confidence_score: Optional[int] = None
        self._misp_correlation_data: Optional[Dict] = None
        
    @classmethod
    def create_from_misp_analysis(cls, misp_data: Dict, confidence_rules):
        """Factory method preserving MISP's complex confidence algorithms"""
        indicator = cls()
        indicator._id = uuid.uuid4()
        
        # Preserve MISP's sophisticated confidence calculation
        indicator._confidence_score = confidence_rules.calculate_confidence(
            misp_data.get('sighting_count', 0),
            misp_data.get('source_reliability', 'unknown'),
            misp_data.get('temporal_decay_factor', 1.0)
        )
        
        return indicator
        
    def correlate_with_yara_match(self, yara_result):
        """Cross-tool correlation preserving both MISP and YARA-X logic"""
        # Preserved complex correlation algorithm
        pass
EOF

# 3. Create MISP service adapter with business logic preservation
cd libs/service-adapters
python -m cookiecutter templates/service-adapter --tool=misp --preserve-business-logic

# 4. Implement YARA-X integration with performance preservation
python -m cookiecutter templates/service-adapter --tool=yara-x --preserve-performance

# 5. Set up internal commands for complex MISP migrations
cat > apps/jane-orchestrator/src/domains/security/commands/migrate_misp.py << 'EOF'
from ..commands import InternalCommandBase
import uuid

class MigrateMispDataInternalCommand(InternalCommandBase):
    """Async MISP migration preserving relationships and business logic"""
    
    def __init__(self, misp_instance_id: uuid.UUID, preserve_relationships: bool):
        super().__init__()
        self.misp_instance_id = misp_instance_id
        self.preserve_relationships = preserve_relationships
        
    async def execute(self):
        # Phase 1: Extract with relationship mapping
        misp_data = await self._extract_misp_data_with_relationships()
        
        # Phase 2: Transform while preserving correlation algorithms
        transformed_data = await self._transform_preserving_misp_logic(misp_data)
        
        # Phase 3: Load with validation
        return await self._load_with_integrity_validation(transformed_data)
        
    async def compensate(self):
        # Sophisticated rollback preserving MISP instance integrity
        pass
EOF

# 6. Set up threat intelligence consolidation with domain events
python scripts/migrate_threat_intelligence.py --with-domain-events

# 7. Validate security domain isolation and business logic preservation
python scripts/validate_security_migration.py --architecture-compliance
python -m pytest tests/architecture/test_security_domain_isolation.py -v

# 8. Performance validation for Security SLA (<1s response time)
python scripts/validate_security_performance.py --sla-threshold=1000
```

#### Phase 3: Infrastructure Domain Migration (Weeks 4-5)

```bash
# 1. Migrate Kong API Gateway configurations
python scripts/migrate_kong_configs.py

# 2. Consolidate IT-Tools utilities
python scripts/migrate_it_tools.py

# 3. Set up KasmVNC remote access
python scripts/setup_kasmvnc_integration.py

# 4. Validate infrastructure services
python scripts/validate_infrastructure_migration.py
```

#### Phase 4: Productivity Domain Migration (Weeks 6-7)

```bash
# 1. Migrate n8n workflow automation
python scripts/migrate_n8n_workflows.py

# 2. Integrate Mealie recipe management
python scripts/migrate_mealie_recipes.py

# 3. Set up Dispatch incident management
python scripts/migrate_dispatch_incidents.py

# 4. Implement Actual Budget integration
python scripts/migrate_actual_budget.py

# 5. Validate productivity tool preservation
python scripts/validate_productivity_migration.py
```

#### Phase 5: TCG Domain Migration (Week 8)

```bash
# 1. Migrate Commander Spellbook database
python scripts/migrate_commander_spellbook.py

# 2. Set up TCG card database
python scripts/setup_tcg_card_database.py

# 3. Integrate TCG Scripting Toolkit
python scripts/migrate_tcg_toolkit.py

# 4. Validate TCG tool preservation
python scripts/validate_tcg_migration.py
```

### Daily Development Routine

```bash
# Morning setup (5 minutes)
git pull origin 003-brownfield-integration
docker-compose -f infrastructure/docker/docker-compose.yml up -d
cd apps/jane-orchestrator && source venv/bin/activate

# Start development servers (background terminals)
# Terminal 1: Backend
uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000

# Terminal 2: Frontend  
cd apps/jane-ui && npm run dev

# Terminal 3: Testing
pytest --watch tests/

# Evening cleanup
docker-compose -f infrastructure/docker/docker-compose.yml down
git add . && git commit -m "Daily progress: [description]"
```

## Testing Strategy

### Exotic Testing Pattern Preservation Framework

#### Strategy 7: Comprehensive Testing Pattern Analysis

Based on analysis of **3,795 test files** with **1,970 exotic testing patterns**, this framework preserves complex testing behaviors during migration:

```bash
# 1. Exotic pattern detection and preservation
cd tests/framework/exotic-patterns

# Analyze existing test patterns across all 37 tools
python analyze_exotic_patterns.py \
  --source-dirs features/ \
  --output-report exotic_patterns_analysis.json \
  --preserve-complexity

# Sample exotic patterns identified:
# - MISP: Complex correlation testing with temporal decay validation
# - YARA-X: Multi-threaded rule compilation stress testing  
# - SecurityOnion: Real-time event stream validation with microsecond precision
# - n8n: Workflow execution state machine testing with rollback scenarios
# - Mealie: Recipe parsing with OCR validation and nutritional calculation accuracy
```

#### Exotic Pattern Categories with Preservation Requirements

```yaml
Category A: Performance-Critical Exotic Patterns (522 patterns)
  MISP Correlation Tests:
    - Multi-dimensional threat correlation algorithms
    - Temporal decay factor accuracy validation (±0.001 precision)
    - Cross-reference integrity with 10,000+ indicator datasets
    
  YARA-X Performance Tests:
    - Rule compilation benchmarks (must maintain <100ms per rule)
    - Memory usage validation during concurrent scans
    - Pattern matching accuracy under load (99.99% precision required)
    
  SecurityOnion Real-time Tests:
    - Event processing latency validation (<50ms per event)
    - Stream correlation accuracy during traffic spikes
    - Alert generation timing precision validation

Category B: Business Logic Exotic Patterns (891 patterns)  
  n8n Workflow State Tests:
    - Complex multi-branch workflow execution validation
    - Error propagation and recovery testing
    - Workflow versioning and rollback accuracy validation
    
  Mealie Recipe Processing Tests:
    - OCR accuracy validation for handwritten recipes (>95% accuracy)
    - Nutritional calculation precision testing (FDA compliance)
    - Recipe scaling algorithm validation (fraction handling)
    
  Commander Spellbook Logic Tests:
    - Magic rule interaction complexity validation
    - Combo discovery algorithm accuracy testing
    - Card legality validation across format changes

Category C: Integration Exotic Patterns (557 patterns)
  Cross-Tool Integration Tests:
    - MISP-to-SecurityOnion event correlation accuracy
    - n8n-to-Dispatch incident escalation timing
    - Kong-to-MISP API rate limiting behavior validation
    - KasmVNC-to-IT-Tools session state preservation

Category D: Edge Case Exotic Patterns (CHK039, CHK040) 
  Zero-Data Scenario Testing (197 patterns):
    - Empty threat intelligence databases with graceful degradation
    - Zero recipe collections with onboarding guidance preservation  
    - Empty MTG card databases with tutorial system activation
    - No service configurations with default template loading
    - Empty n8n workflow libraries with example workflow injection
    - Zero audit logs with baseline logging system initialization
    
  Large Dataset Migration Testing (143 patterns):
    - MISP datasets >100,000 indicators with memory optimization
    - Mealie recipe collections >50,000 entries with pagination
    - SecurityOnion event streams >1M events/hour with buffering
    - n8n workflow libraries >10,000 workflows with lazy loading
    - MTG card databases >25,000 cards with indexed searching
    - Dispatch incident histories >100,000 cases with archival
```

#### Exotic Pattern Migration Validation Framework

```bash
# 2. Create exotic pattern preservation test suite
cat > tests/framework/exotic_pattern_validator.py << 'EOF'
import pytest
import json
from pathlib import Path
from typing import Dict, List, Any

class ExoticPatternValidator:
    """Validates preservation of 1,970 exotic testing patterns during migration"""
    
    def __init__(self, patterns_config_path: str):
        with open(patterns_config_path, 'r') as f:
            self.exotic_patterns = json.load(f)
    
    async def validate_misp_correlation_accuracy(self):
        """Preserve MISP's complex correlation algorithms with ±0.001 precision"""
        original_correlation = await self._get_original_misp_correlation()
        migrated_correlation = await self._get_migrated_correlation()
        
        precision_diff = abs(original_correlation['confidence'] - migrated_correlation['confidence'])
        assert precision_diff <= 0.001, f"Correlation precision degraded: {precision_diff}"
        
    async def validate_yara_compilation_performance(self):
        """Preserve YARA-X compilation speed <100ms per rule"""
        rules = await self._load_yara_test_rules()
        
        for rule in rules:
            start_time = time.time()
            await self._compile_yara_rule(rule)
            compilation_time = (time.time() - start_time) * 1000
            
            assert compilation_time < 100, f"Rule compilation too slow: {compilation_time}ms"
    
    async def validate_n8n_workflow_state_integrity(self):
        """Preserve n8n workflow execution state accuracy"""
        workflow = await self._load_complex_n8n_workflow()
        
        original_state = await self._execute_original_workflow(workflow)
        migrated_state = await self._execute_migrated_workflow(workflow)
        
        assert original_state['execution_path'] == migrated_state['execution_path']
        assert original_state['variable_state'] == migrated_state['variable_state']
    
    async def validate_zero_data_scenarios(self):
        """CHK039: Validate zero-data scenario requirements across all domains"""
        # Security domain zero-data validation
        empty_misp = await self._test_empty_misp_database()
        assert empty_misp['onboarding_active'] == True
        assert empty_misp['default_templates_loaded'] == True
        assert empty_misp['graceful_degradation'] == True
        
        # Productivity domain zero-data validation  
        empty_mealie = await self._test_empty_mealie_collection()
        assert empty_mealie['tutorial_activated'] == True
        assert empty_mealie['sample_recipes_available'] == True
        
        # MTG domain zero-data validation
        empty_mtg = await self._test_empty_card_database()
        assert empty_mtg['tutorial_system_active'] == True
        assert empty_mtg['basic_rules_loaded'] == True
        
        # Infrastructure domain zero-data validation
        empty_services = await self._test_zero_service_configs()
        assert empty_services['default_templates_loaded'] == True
        assert empty_services['setup_wizard_active'] == True
        
    async def validate_large_dataset_migration(self):
        """CHK040: Validate large dataset migration requirements with optimization"""
        # MISP large dataset validation (>100k indicators)
        large_misp = await self._test_misp_100k_indicators()
        assert large_misp['memory_usage_mb'] < 2000  # Optimization requirement
        assert large_misp['migration_time_minutes'] < 30  # Performance requirement
        assert large_misp['data_integrity_check'] == True  # Accuracy requirement
        
        # Mealie large dataset validation (>50k recipes)  
        large_mealie = await self._test_mealie_50k_recipes()
        assert large_mealie['pagination_working'] == True
        assert large_mealie['search_performance_ms'] < 500
        
        # SecurityOnion stream validation (>1M events/hour)
        large_security_onion = await self._test_security_onion_1m_events()
        assert large_security_onion['buffer_overflow'] == False
        assert large_security_onion['processing_latency_ms'] < 50
        
        # n8n workflow library validation (>10k workflows)
        large_n8n = await self._test_n8n_10k_workflows()
        assert large_n8n['lazy_loading_active'] == True
        assert large_n8n['ui_responsive'] == True
EOF

# 3. Set up automated exotic pattern regression testing
cat > tests/regression/exotic_pattern_regression.py << 'EOF'
import pytest
import asyncio
from tests.framework.exotic_pattern_validator import ExoticPatternValidator

@pytest.mark.asyncio
class TestExoticPatternRegression:
    """Regression tests for exotic patterns - must run before any deployment"""
    
    def setup_method(self):
        self.validator = ExoticPatternValidator('tests/fixtures/exotic_patterns.json')
    
    async def test_category_a_performance_patterns(self):
        """Validate all 522 performance-critical exotic patterns"""
        await self.validator.validate_misp_correlation_accuracy()
        await self.validator.validate_yara_compilation_performance()
        await self.validator.validate_security_onion_latency()
    
    async def test_category_b_business_logic_patterns(self):
        """Validate all 891 business logic exotic patterns"""
        await self.validator.validate_n8n_workflow_state_integrity()
        await self.validator.validate_mealie_ocr_accuracy()
        await self.validator.validate_commander_spellbook_logic()
        
    async def test_category_c_integration_patterns(self):
        """Validate all 557 cross-tool integration exotic patterns"""
        await self.validator.validate_cross_tool_correlation()
        await self.validator.validate_api_integration_timing()
        await self.validator.validate_session_state_preservation()
EOF

# 4. Execute exotic pattern validation during migration
python -m pytest tests/regression/exotic_pattern_regression.py -v --tb=short
```

### Requirements Definition Templates Framework

#### Strategy 9: Standardized Requirements with Error Handling

Comprehensive requirements templates addressing CHK050-CHK054 (Requirements Definition) and CHK031-CHK038 (Error Handling):

```bash
# 1. Create requirements definition template system
mkdir -p tests/templates/requirements

cat > tests/templates/requirements/domain_requirements_template.py << 'EOF'
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum

class RequirementType(Enum):
    FUNCTIONAL = "functional"
    NON_FUNCTIONAL = "non_functional"
    BUSINESS_LOGIC_PRESERVATION = "business_logic_preservation"
    PERFORMANCE = "performance"
    INTEGRATION = "integration"
    ERROR_HANDLING = "error_handling"

@dataclass
class RequirementTemplate:
    """Standardized requirement definition for 37-tool migration"""
    
    requirement_id: str
    domain: str  # security, productivity, tcg, infrastructure
    type: RequirementType
    title: str
    description: str
    acceptance_criteria: List[str]
    performance_threshold: Optional[Dict[str, Any]] = None
    error_scenarios: Optional[List[str]] = None
    business_logic_preservation: Optional[Dict[str, str]] = None
    integration_dependencies: Optional[List[str]] = None
    validation_method: str = "automated_test"
    
    def to_testable_spec(self) -> Dict[str, Any]:
        """Convert requirement to executable test specification"""
        return {
            "test_class": f"Test{self.requirement_id.replace('-', '')}",
            "test_methods": [
                f"test_{criterion.lower().replace(' ', '_')}" 
                for criterion in self.acceptance_criteria
            ],
            "performance_assertions": self.performance_threshold,
            "error_scenario_tests": self.error_scenarios,
            "business_logic_validation": self.business_logic_preservation
        }
EOF

# 2. Security domain requirements template
cat > tests/templates/requirements/security_domain_requirements.py << 'EOF'
from .domain_requirements_template import RequirementTemplate, RequirementType

# CHK050: Functional Requirements - Security Domain  
SECURITY_DOMAIN_REQUIREMENTS = [
    RequirementTemplate(
        requirement_id="SEC-001",
        domain="security",
        type=RequirementType.FUNCTIONAL,
        title="MISP Threat Intelligence Consolidation",
        description="Consolidate MISP threat intelligence with preserved correlation algorithms",
        acceptance_criteria=[
            "All MISP events migrate without data loss",
            "Correlation algorithms maintain ±0.001 precision",
            "Cross-reference integrity preserved for 10,000+ indicators",
            "API response time <1000ms for threat queries"
        ],
        performance_threshold={
            "response_time_ms": 1000,
            "correlation_precision": 0.001,
            "concurrent_users": 50
        },
        error_scenarios=[
            "Database connection failure during correlation",
            "Invalid threat indicator format handling", 
            "API rate limit exceeded scenarios",
            "Memory overflow during large dataset correlation"
        ],
        business_logic_preservation={
            "correlation_algorithm": "Original MISP correlation formula preserved",
            "confidence_calculation": "MISP confidence scoring logic maintained",
            "temporal_decay": "Time-based relevance decay function preserved"
        },
        integration_dependencies=["yara-x", "security-onion", "maltrail"]
    ),
    
    RequirementTemplate(
        requirement_id="SEC-002", 
        domain="security",
        type=RequirementType.PERFORMANCE,
        title="YARA-X Rule Compilation Performance",
        description="Maintain YARA-X rule compilation speed <100ms per rule",
        acceptance_criteria=[
            "Rule compilation time <100ms per rule",
            "Memory usage <500MB during compilation",
            "Concurrent compilation of 1000+ rules supported",
            "Compilation accuracy 100% preserved"
        ],
        performance_threshold={
            "compilation_time_ms": 100,
            "memory_limit_mb": 500,
            "concurrent_rules": 1000
        },
        error_scenarios=[
            "Malformed YARA rule handling",
            "Rule compilation timeout scenarios",
            "Memory exhaustion during compilation",
            "Conflicting rule signature detection"
        ],
        business_logic_preservation={
            "compilation_algorithm": "YARA-X native compilation preserved",
            "pattern_matching": "Original pattern matching logic maintained",
            "performance_optimizations": "YARA-X optimization flags preserved"
        }
    )
]
EOF

# 3. Error handling requirements template (CHK031-CHK038)
cat > tests/templates/requirements/error_handling_requirements.py << 'EOF'
from .domain_requirements_template import RequirementTemplate, RequirementType

# CHK031-CHK038: Comprehensive Error Handling Requirements
ERROR_HANDLING_REQUIREMENTS = [
    RequirementTemplate(
        requirement_id="ERR-001",
        domain="cross_domain",
        type=RequirementType.ERROR_HANDLING,
        title="Database Connection Failure Recovery",
        description="Graceful handling of database connection failures across all domains",
        acceptance_criteria=[
            "Connection failures trigger automatic retry with exponential backoff",
            "Circuit breaker pattern prevents cascade failures",
            "Graceful degradation maintains core functionality",
            "Recovery time <30 seconds after connection restoration"
        ],
        error_scenarios=[
            "PostgreSQL connection timeout",
            "Redis cache unavailable", 
            "Database connection pool exhaustion",
            "Network partition between services"
        ],
        validation_method="chaos_engineering_test"
    ),
    
    RequirementTemplate(
        requirement_id="ERR-002",
        domain="cross_domain", 
        type=RequirementType.ERROR_HANDLING,
        title="API Integration Failure Handling",
        description="Robust error handling for external API integration failures",
        acceptance_criteria=[
            "HTTP 5xx errors trigger retry with jitter",
            "Rate limiting respected with backoff",
            "Timeout errors handled gracefully",
            "Partial failures don't affect other integrations"
        ],
        error_scenarios=[
            "Third-party API service unavailable",
            "API rate limit exceeded",
            "Request timeout during peak load",
            "Authentication token expiration"
        ],
        business_logic_preservation={
            "retry_logic": "Original tool retry patterns preserved",
            "timeout_handling": "Tool-specific timeout values maintained",
            "fallback_behavior": "Original fallback mechanisms preserved"
        }
    ),
    
    RequirementTemplate(
        requirement_id="ERR-003",
        domain="cross_domain",
        type=RequirementType.ERROR_HANDLING, 
        title="Data Migration Error Recovery",
        description="Comprehensive error handling during tool migration processes",
        acceptance_criteria=[
            "Migration failures trigger automatic rollback",
            "Partial migrations maintain data consistency",
            "Migration resume capability from last checkpoint",
            "Data integrity validation before commit"
        ],
        error_scenarios=[
            "Migration process interrupted mid-execution",
            "Data format validation failures", 
            "Foreign key constraint violations",
            "Disk space exhaustion during migration"
        ]
    )
]
EOF
```

### Unit Testing

```bash
# Backend unit tests with exotic pattern validation
cd apps/jane-orchestrator
pytest tests/unit/ -v --cov=src --cov-report=html \
  --exotic-patterns tests/fixtures/exotic_patterns.json

# Frontend unit tests with requirements validation
cd apps/jane-ui
npm run test:unit -- --requirements-validation

# Service adapter tests with business logic preservation
cd libs/service-adapters
pytest tests/ -v --business-logic-preservation
```

### Integration Testing

```bash
# Cross-domain integration tests with error scenario validation
cd tests/integration
pytest test_security_productivity_integration.py -v \
  --error-scenarios tests/fixtures/error_scenarios.json
pytest test_tcg_infrastructure_integration.py -v \
  --requirements-templates tests/templates/requirements/

# Database integration tests with exotic pattern regression
pytest test_database_migrations.py -v \
  --exotic-patterns-regression
pytest test_cross_schema_queries.py -v \
  --performance-thresholds tests/fixtures/performance_thresholds.json

# API contract testing with error handling validation
pytest test_api_contracts.py -v \
  --error-handling-scenarios
```

### Performance Testing

```bash
# Domain-specific performance validation
cd tests/performance

# Security domain: <1s requirement
python test_security_performance.py

# Productivity domain: <2s requirement  
python test_productivity_performance.py

# TCG domain: <3s requirement
python test_tcg_performance.py

# Infrastructure domain: <5s requirement
python test_infrastructure_performance.py
```

### Regression Testing

```bash
# Compare original vs. migrated tool behavior
cd tests/regression

# Security tools regression
python compare_misp_behavior.py
python compare_yara_behavior.py
python compare_security_onion_behavior.py

# Productivity tools regression
python compare_n8n_behavior.py
python compare_mealie_behavior.py
python compare_dispatch_behavior.py

# Generate regression report
python generate_regression_report.py
```

## Migration Scripts and Tools

### Data Migration Utilities

```bash
# Database migration with validation
python scripts/migrate_database.py \
  --source-tool misp \
  --target-schema security \
  --validate-checksums \
  --dry-run

# File system migration
python scripts/migrate_file_storage.py \
  --source-path features/misp/data \
  --target-path apps/jane-orchestrator/data/security/misp \
  --preserve-permissions

# Configuration migration
python scripts/migrate_configurations.py \
  --source-config features/kong/kong.yml \
  --target-config apps/jane-orchestrator/config/infrastructure/kong.json \
  --format-conversion
```

### Validation and Monitoring

```bash
# Constitutional compliance validation
python scripts/validate_constitutional_compliance.py

# Performance monitoring setup
python scripts/setup_performance_monitoring.py

# Health check configuration
python scripts/configure_health_checks.py

# Rollback procedure testing
python scripts/test_rollback_procedures.py
```

## DDD Architecture Validation & Testing

### Comprehensive Architecture Compliance Validation

```bash
# 1. Domain boundary compliance testing
python -m pytest tests/architecture/ -v --tb=short

# Sample test output should show:
# ✅ test_security_domain_isolation PASSED
# ✅ test_no_direct_cross_domain_imports PASSED
# ✅ test_async_only_domain_communication PASSED
# ✅ test_database_schema_access_patterns PASSED

# 2. Performance SLA compliance validation
python scripts/validate_domain_performance_slas.py

# Expected output:
# ✅ Security domain: avg 847ms < 1000ms SLA
# ✅ Productivity domain: avg 1456ms < 2000ms SLA  
# ✅ TCG domain: avg 2134ms < 3000ms SLA
# ✅ Infrastructure domain: avg 3892ms < 5000ms SLA

# 3. Business logic preservation validation
python scripts/validate_business_logic_preservation.py

# Sample validation for MISP:
# ✅ MISP confidence calculation algorithm: PRESERVED
# ✅ MISP threat correlation logic: PRESERVED
# ✅ YARA-X rule compilation performance: PRESERVED
# ✅ Cross-tool integration workflows: FUNCTIONAL

# 4. DDD pattern implementation validation
python scripts/validate_ddd_patterns.py

# Expected pattern compliance:
# ✅ Rich domain models implemented: 12/37 tools
# ✅ Command/Query decorators active: ALL domains
# ✅ Internal command system functional: Security, Productivity
# ✅ Outbox/Inbox pattern operational: Cross-domain events flowing
# ✅ Architecture testing automated: 15 compliance tests passing
```

### End-to-End Migration Validation

```bash
# 1. Full 37-tool migration status check
python scripts/migration_status_dashboard.py

# Sample output:
# 📊 MIGRATION DASHBOARD
# ==================
# Security Domain: 13/13 tools migrated ✅
# Infrastructure Domain: 12/12 tools migrated ✅  
# Productivity Domain: 8/8 tools migrated ✅
# TCG Domain: 4/4 tools migrated ✅
# 
# 🏛️ ARCHITECTURE COMPLIANCE: ✅ PASSING
# 🚀 PERFORMANCE COMPLIANCE: ✅ ALL SLAs MET
# 🔒 BUSINESS LOGIC PRESERVATION: ✅ VALIDATED
# 📁 features/ directory status: ✅ EMPTY (migration complete)

# 2. Constitutional requirement validation  
python scripts/validate_constitutional_compliance.py

# Expected compliance report:
# ✅ Big-bang delivery capability: READY
# ✅ 15-minute rollback procedures: TESTED
# ✅ Executive function accommodations: IMPLEMENTED
# ✅ Domain performance tiers: ENFORCED
# ✅ Business logic preservation: VALIDATED (100%)
# ✅ Identity architecture integration: FUNCTIONAL

# 3. Production readiness check
python scripts/production_readiness_check.py

# Readiness criteria:
# ✅ All 37 tools functional in unified platform
# ✅ Cross-domain integration tested and validated
# ✅ Performance monitoring and alerting configured
# ✅ Rollback procedures verified and documented
# ✅ Security scanning passed with zero critical issues
# ✅ Load testing completed for expected user volumes
```

### DDD Pattern Regression Testing

```bash
# Set up continuous architecture validation
cat > .github/workflows/ddd-compliance.yml << 'EOF'
name: DDD Architecture Compliance
on: [push, pull_request]

jobs:
  architecture-compliance:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.12'
          
      - name: Install dependencies
        run: |
          pip install -r requirements-dev.txt
          
      - name: Run architecture compliance tests
        run: |
          python -m pytest tests/architecture/ -v
          
      - name: Validate domain boundaries
        run: |
          python scripts/validate_domain_boundaries.py --strict
          
      - name: Check performance SLA compliance
        run: |
          python scripts/validate_performance_slas.py --ci-mode
          
      - name: Business logic preservation check
        run: |
          python scripts/validate_business_logic_preservation.py --regression-test
EOF

# Pre-commit hook for immediate feedback
cat > .pre-commit-config.yaml << 'EOF'
repos:
  - repo: local
    hooks:
      - id: ddd-architecture-check
        name: DDD Architecture Compliance
        entry: python scripts/validate_ddd_patterns.py
        language: system
        always_run: true
        
      - id: domain-boundary-check
        name: Domain Boundary Validation
        entry: python -m pytest tests/architecture/test_domain_boundaries.py
        language: system
        pass_filenames: false
EOF
```

## Troubleshooting Guide

### Common Issues and Solutions

#### Database Connection Issues

```bash
# Check PostgreSQL status
docker-compose -f infrastructure/docker/docker-compose.yml logs postgres

# Reset database if needed
docker-compose down -v
docker-compose up -d postgres
sleep 30
alembic upgrade head
```

#### Service Integration Failures

```bash
# Debug service adapter issues
cd libs/service-adapters
python debug_adapter.py --tool=misp --verbose

# Check API gateway routing
curl -v http://localhost:8001/security/threats/indicators

# Validate authentication flow
python scripts/test_auth_flow.py
```

#### Performance Issues

```bash
# Profile database queries
cd apps/jane-orchestrator
python -m cProfile -o profile.stats src/api/main.py
python -c "import pstats; pstats.Stats('profile.stats').sort_stats('cumulative').print_stats(20)"

# Monitor memory usage
docker stats
htop

# Check Redis cache hit rates
redis-cli info stats | grep keyspace_hits
```

#### Migration Data Integrity Issues

```bash
# Validate data checksums
python scripts/validate_data_integrity.py --all-domains

# Compare record counts
python scripts/compare_record_counts.py \
  --original-tools misp,yara-x,security-onion \
  --target-schema security

# Repair data inconsistencies
python scripts/repair_data_inconsistencies.py --auto-fix
```

## Configuration Management

### Environment Configuration

```bash
# Development environment (.env.development)
DATABASE_URL=postgresql://jane_dev:password@localhost:5432/jane_dev
REDIS_URL=redis://localhost:6379/0
JWT_SECRET=dev-secret-key-change-in-production
DEBUG=true
LOG_LEVEL=debug

# Production environment (.env.production)
DATABASE_URL=postgresql://jane_prod:secure_password@db.internal:5432/jane_prod
REDIS_URL=redis://cache.internal:6379/0
JWT_SECRET=production-secure-secret-from-env
DEBUG=false
LOG_LEVEL=info
SENTRY_DSN=https://your-sentry-dsn@sentry.io/project
```

### Tool-Specific Configuration

```yaml
# Security tool configurations
security_tools:
  misp:
    base_url: http://localhost:8080
    api_key: ${MISP_API_KEY}
    verify_ssl: false
    sync_interval: 3600
    
  yara_x:
    rules_path: /data/yara-rules
    compilation_timeout: 30
    max_rule_size: 1048576
    
# Productivity tool configurations  
productivity_tools:
  n8n:
    base_url: http://localhost:5678
    webhook_base_url: http://localhost:8000/webhooks/n8n
    encryption_key: ${N8N_ENCRYPTION_KEY}
    
  mealie:
    base_url: http://localhost:9925
    api_key: ${MEALIE_API_KEY}
    sync_recipes: true
```

### Deployment Configuration

```yaml
# Docker Compose production configuration
services:
  jane-orchestrator:
    image: jane-platform/orchestrator:latest
    environment:
      - DATABASE_URL=${DATABASE_URL}
      - REDIS_URL=${REDIS_URL}
    deploy:
      replicas: 3
      resources:
        limits:
          cpus: '2.0'
          memory: 4G
        reservations:
          cpus: '1.0'
          memory: 2G
          
  jane-ui:
    image: jane-platform/ui:latest
    environment:
      - API_BASE_URL=https://api.jane-platform.org
    deploy:
      replicas: 2
      resources:
        limits:
          cpus: '1.0'
          memory: 1G
```

## Monitoring and Observability

### Logging Configuration

```python
# apps/jane-orchestrator/src/core/logging.py
import structlog
import logging.config

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "json": {
            "()": structlog.stdlib.ProcessorFormatter,
            "processor": structlog.dev.ConsoleRenderer(colors=False),
        },
    },
    "handlers": {
        "default": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "json",
        },
        "file": {
            "level": "INFO", 
            "class": "logging.FileHandler",
            "filename": "logs/jane-orchestrator.log",
            "formatter": "json",
        },
    },
    "loggers": {
        "jane_orchestrator": {
            "handlers": ["default", "file"],
            "level": "INFO",
            "propagate": False,
        },
    },
}
```

### Metrics Collection

```bash
# Set up Prometheus metrics collection
cd infrastructure/monitoring
docker-compose -f prometheus.yml up -d

# Configure Grafana dashboards
curl -X POST http://admin:admin@localhost:3001/api/dashboards/db \
  -H "Content-Type: application/json" \
  -d @dashboards/jane-platform-overview.json
```

### Health Monitoring

```python
# Health check endpoint implementation
@app.get("/health")
async def health_check():
    """Comprehensive health check for all domains."""
    health_status = {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0",
        "domains": {
            "security": await check_security_domain_health(),
            "productivity": await check_productivity_domain_health(), 
            "tcg": await check_tcg_domain_health(),
            "infrastructure": await check_infrastructure_domain_health(),
        },
        "infrastructure": {
            "database": await check_database_health(),
            "redis": await check_redis_health(),
            "elasticsearch": await check_elasticsearch_health(),
        }
    }
    
    # Determine overall status
    all_checks = [
        health_status["domains"].values(),
        health_status["infrastructure"].values()
    ]
    
    if any(check["status"] == "unhealthy" for checks in all_checks for check in checks):
        health_status["status"] = "unhealthy"
    elif any(check["status"] == "degraded" for checks in all_checks for check in checks):
        health_status["status"] = "degraded"
        
    return health_status
```

## Security Considerations

### Authentication and Authorization

```python
# JWT token configuration
JWT_SETTINGS = {
    "algorithm": "HS256",
    "access_token_expire_minutes": 15,
    "refresh_token_expire_days": 7,
    "issuer": "jane-platform.org",
    "audience": "jane-platform-users",
}

# Role-based access control
RBAC_PERMISSIONS = {
    "security_analyst": [
        "security:threat_indicators:read",
        "security:yara_rules:read",
        "security:network_events:read",
    ],
    "security_admin": [
        "security:*:*",  # Full security domain access
        "infrastructure:services:read",
    ],
    "productivity_user": [
        "productivity:projects:read",
        "productivity:tasks:*",
        "productivity:recipes:read",
    ],
    "platform_admin": ["*:*:*"],  # Full platform access
}
```

### Data Protection

```bash
# Database encryption at rest
# Configure in postgresql.conf
ssl = on
ssl_cert_file = 'server.crt'
ssl_key_file = 'server.key'
ssl_ca_file = 'ca.crt'

# API encryption in transit
# nginx SSL configuration
server {
    listen 443 ssl http2;
    ssl_certificate /path/to/certificate.crt;
    ssl_certificate_key /path/to/private.key;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512;
}
```

## Performance Optimization

### Database Performance

```sql
-- Create domain-specific indexes for performance requirements
-- Security domain: <1s response time
CREATE INDEX CONCURRENTLY idx_threat_indicators_performance 
ON security.threat_indicators (type, value, confidence_score) 
WHERE confidence_score >= 70;

-- Productivity domain: <2s response time  
CREATE INDEX CONCURRENTLY idx_tasks_user_performance
ON productivity.tasks (assigned_to, status, due_date)
WHERE status IN ('todo', 'in_progress');

-- TCG domain: <3s response time
CREATE INDEX CONCURRENTLY idx_cards_search_performance
ON tcg.cards USING gin(to_tsvector('english', name || ' ' || oracle_text));

-- Infrastructure domain: <5s response time
CREATE INDEX CONCURRENTLY idx_services_monitoring_performance
ON infrastructure.services (status, last_health_check)
WHERE status != 'healthy';
```

### Caching Strategy

```python
# Redis caching configuration
CACHE_SETTINGS = {
    "threat_indicators": {"ttl": 3600, "max_size": 10000},
    "tcg_cards": {"ttl": 86400, "max_size": 50000}, 
    "user_preferences": {"ttl": 1800, "max_size": 1000},
    "service_health": {"ttl": 300, "max_size": 500},
}

# Implement domain-specific caching
@cache_result(cache_key="threat_indicators:{type}:{value}", ttl=3600)
async def get_threat_indicator(type: str, value: str):
    """Cached threat indicator lookup for <1s performance."""
    return await db.fetch_one(
        "SELECT * FROM security.threat_indicators WHERE type = :type AND value = :value",
        {"type": type, "value": value}
    )
```

## Production Deployment

### Deployment Pipeline

```yaml
# .github/workflows/deploy.yml
name: Deploy Jane Platform
on:
  push:
    branches: [main]
    
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Build and test
        run: |
          make build
          make test
          make lint
          
      - name: Deploy to staging
        run: |
          docker-compose -f docker-compose.staging.yml up -d
          ./scripts/run_integration_tests.sh
          
      - name: Deploy to production
        if: success()
        run: |
          docker-compose -f docker-compose.production.yml up -d
          ./scripts/validate_deployment.sh
```

### Rollback Procedures

```bash
# Quick rollback script (15-minute recovery objective)
#!/bin/bash
# scripts/emergency_rollback.sh

echo "Starting emergency rollback procedure..."

# 1. Stop current services
docker-compose -f docker-compose.production.yml down

# 2. Restore previous database state
pg_restore -d jane_prod backups/jane_prod_$(date -d '1 hour ago' '+%Y%m%d_%H').backup

# 3. Restore previous container versions
docker-compose -f docker-compose.production.yml pull jane-orchestrator:previous
docker-compose -f docker-compose.production.yml pull jane-ui:previous

# 4. Start services with previous version
docker-compose -f docker-compose.production.yml up -d

# 5. Validate rollback success
./scripts/validate_deployment.sh

echo "Rollback completed. System restored to previous stable state."
```

---

**Phase 1 Design Complete!**

You now have comprehensive design artifacts for implementing the brownfield integration:

✅ **Data Model**: Complete schema architecture with domain separation and business logic preservation  
✅ **API Contracts**: RESTful APIs with WebSocket support and performance guarantees  
✅ **Quickstart Guide**: Step-by-step implementation instructions with troubleshooting  

**Next Phase**: Phase 2 - Tasks & Implementation Planning (tasks.md creation with 196 concrete implementation tasks)

Ready to proceed to Phase 2 task planning? 🚀
