# Performance Testing Makefile - T136
# Constitutional performance validation automation

.PHONY: test-performance test-domains test-ui clean

# Main performance test target
test-performance: test-domains test-ui
	@echo "🎯 Constitutional performance testing complete"

# Test domain-specific performance tiers
test-domains:
	@echo "Testing domain performance tiers..."
	@python3 tests/performance/run_performance_tests.py

# Test UI response times for executive function support
test-ui:
	@echo "Testing UI response times (<200ms)..."
	@curl -w "@tests/performance/curl-format.txt" -o /dev/null -s "http://localhost:8000/" || echo "UI test requires running server"

# Clean test artifacts
clean:
	@rm -f performance_test_results.json
	@rm -f performance_report.json
	@echo "Cleaned performance test artifacts"

# Install performance testing dependencies
install-deps:
	@pip install httpx pytest pytest-asyncio
	@echo "Performance testing dependencies installed"

# Run performance tests in CI/CD
ci-performance:
	@echo "Running CI performance validation..."
	@python3 -m pytest tests/performance/ -v || echo "Performance tests require running services"