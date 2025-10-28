# Mental Prosthetic Platform Test Framework

This directory contains the comprehensive test suite for the Mental Prosthetic Platform, organized by domain and supporting all 37 integrated executive function tools.

## Test Organization Structure

```
tests/
├── security/          # Security domain tests (13 tools)
├── productivity/      # Productivity domain tests (8 tools)  
├── mtg/              # MTG domain tests (4 tools)
├── infrastructure/   # Infrastructure domain tests (12+ tools)
├── integration/      # Cross-domain integration tests
├── performance/      # Performance validation tests
├── e2e/             # End-to-end user workflow tests
├── unit/            # Unit tests for shared components
└── fixtures/        # Test data and fixtures
```

## Domain Test Coverage

### Security Domain (13 tools)
- MISP - Threat intelligence platform
- HELK - Hunting ELK stack  
- SecurityOnion - Network security monitoring
- Maltrail - Malicious activity detection
- YARA-X - Pattern matching engine
- CyberChef - Data transformation toolkit
- Nemesis - Post-exploitation framework
- APIScout - API discovery and analysis
- BlackArch - Penetration testing toolkit
- Brute Ratel C4 - Red team framework
- HexStrike AI - AI-powered security analysis
- Meterpreter - Post-exploitation toolkit
- OneX - Security automation framework

### Productivity Domain (8 tools)
- n8n - Workflow automation
- Mealie - Recipe management
- Dispatch - Incident management
- Actual Budget - Personal finance
- Firecrawl - Web scraping
- Goose - AI coding assistant
- IT-Tools - Developer utilities
- Inspector - Code analysis

### MTG Domain (4 tools)
- Commander Spellbook - Combo database
- MTG Commander Map - Deck visualization
- MTG Scripting Toolkit - Card analysis
- Card Analysis - Statistical analysis

### Infrastructure Domain (12+ tools)
- Kong - API gateway
- Ghostwriter - Report generation
- KasmVNC - Remote desktop
- Chroma MCP - Vector database
- VirusTotal MCP - Malware analysis
- n8n MCP - Workflow integration
- Firecrawl MCP - Web scraping integration
- MalwareBazaar MCP - Malware intelligence
- FileScopeMCP - File analysis
- LScript - Scripting framework
- RITA - Network traffic analysis
- Software Forensic Kit - Digital forensics

## Test Types

### Unit Tests (`unit/`)
- Individual component testing
- Service layer testing
- Utility function testing
- Business logic validation

### Integration Tests (`integration/`)
- Cross-domain data flow
- Service-to-service communication
- API endpoint integration
- Database interaction testing

### Performance Tests (`performance/`)
- Domain-specific performance validation:
  - Security tools: <1s response time
  - Productivity tools: <2s response time
  - MTG tools: <3s response time
  - Infrastructure tools: <5s response time
- UI responsiveness: <200ms (executive function requirement)
- Load testing for 37-tool simultaneous usage

### End-to-End Tests (`e2e/`)
- Complete user workflows
- Cross-tool integration scenarios
- Executive function accommodation validation
- Mobile/PWA functionality testing

## Executive Function Accommodations Testing

All tests validate constitutional requirements for ADHD/autism support:

- **UI Response Time**: <200ms for all interactions
- **Context Switching**: Minimal cognitive load between tools
- **Consistent Patterns**: Unified navigation and interaction patterns
- **WCAG 2.1 AA Compliance**: Accessibility validation
- **Focus Management**: Attention maintenance features

## Test Execution

### Run All Tests
```bash
# Run complete test suite
npm run test:all

# Run tests by domain
npm run test:security
npm run test:productivity
npm run test:mtg
npm run test:infrastructure

# Run by test type
npm run test:unit
npm run test:integration
npm run test:performance
npm run test:e2e
```

### Python Tests
```bash
# Run Python service tests
pytest tests/unit/python/ -v
pytest tests/integration/python/ -v

# Run with coverage
pytest --cov=apps/jane-orchestrator tests/
```

### Performance Validation
```bash
# Domain-specific performance validation
python tests/performance/validate_domain_performance.py
```

## Test Data Management

### Fixtures (`fixtures/`)
- Sample data for all 37 tools
- Executive function test scenarios
- Cross-domain integration datasets
- Performance benchmark data

### Test Databases
- Isolated test databases per domain
- Seed data for consistent testing
- Rollback/cleanup capabilities

## Continuous Integration

Tests are integrated into CI/CD pipeline with:
- Pre-commit testing for changed components
- Full suite execution on pull requests  
- Performance regression detection
- Constitutional compliance validation

## Business Logic Preservation

All tests validate that integrated tools maintain 100% functional compatibility with their original implementations:

- Original test suites migrated and adapted
- Tool-specific behavior validation
- Performance baseline comparisons
- Feature parity verification

## Getting Started

1. **Install Dependencies**
   ```bash
   npm install
   pip install -r requirements-test.txt
   ```

2. **Setup Test Environment**
   ```bash
   npm run test:setup
   ```

3. **Run Basic Validation**
   ```bash
   npm run test:smoke
   ```

4. **Validate Constitutional Compliance**
   ```bash
   npm run test:constitutional
   ```

For detailed test documentation, see individual domain README files.