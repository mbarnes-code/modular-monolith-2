# Performance Testing Framework

This directory contains automated performance testing scripts for constitutional compliance validation.

## Constitutional Requirements

### Domain Performance Tiers
- **Security Domain**: <1s response time (threat analysis criticality)
- **Productivity Domain**: <2s response time (task management workflows)  
- **MTG Domain**: <3s response time (game analysis complexity)
- **Infrastructure Domain**: <5s response time (system operations tolerance)

### Executive Function Support
- **UI Response Time**: <200ms (ADHD/autism accommodations)
- **Context Switching**: 95% reduction target
- **WCAG Compliance**: AA level accessibility

## Usage

### Quick Test
```bash
make test-performance
```

### Domain-Specific Testing
```bash
python3 run_performance_tests.py
```

### CI/CD Integration
```bash
make ci-performance
```

## Test Scripts

- `run_performance_tests.py` - Main performance testing script
- `constitutional_performance_test.py` - Comprehensive test framework
- `test_constitutional_performance.py` - Simplified test runner

## Reports

Performance test results are saved to:
- `performance_test_results.json`
- `performance_report.json`

## Dependencies

```bash
make install-deps
```

Required packages:
- httpx (async HTTP client)
- pytest (testing framework)
- pytest-asyncio (async test support)