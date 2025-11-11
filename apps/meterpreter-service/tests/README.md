# Meterpreter Service Tests

This directory contains test files for the Meterpreter service.

## Test Structure

- `integration/` - Integration tests for built payloads
- `unit/` - Unit tests for individual components
- `fixtures/` - Test data and fixtures
- `scripts/` - Test utility scripts

## Running Tests

```bash
# All tests
npx nx test meterpreter-service

# Integration tests only
npx nx test:integration meterpreter-service

# Manual validation
npm run test
```

## Test Requirements

Tests require:
1. Successfully built payloads (`nx build meterpreter-service`)
2. Basic system tools (file, ls, stat)
3. Shell environment (bash/sh)

## Adding Tests

Create new test files in the appropriate subdirectory:

- Integration tests: `integration/test-*.sh`
- Unit tests: `unit/test-*.c` or `unit/test-*.cpp`
- Fixtures: `fixtures/sample-*.bin`

All test scripts should be executable and follow the naming convention `test-*.sh`.

## Test Coverage

Current test coverage includes:
- [ ] Binary payload validation
- [ ] Extension library validation
- [ ] File size and format checks
- [ ] Basic security validation
- [ ] Cross-architecture compatibility

## Future Enhancements

Planned test improvements:
- [ ] Automated unit testing framework
- [ ] Performance benchmarks
- [ ] Memory leak detection
- [ ] Static analysis integration
- [ ] Continuous integration testing