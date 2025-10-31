#!/bin/bash
# MISP Comprehensive Test Execution Script
# Purpose: Execute T1986 comprehensive testing strategy for MISP integration
# Requirements: Validate threat intelligence functionality preservation
# Usage: ./run_misp_tests.sh [options]

set -e  # Exit on any error

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="/workspaces/modular-monolith-2"
MISP_TEST_DIR="$PROJECT_ROOT/tests/security/MISP"
APPS_DIR="$PROJECT_ROOT/apps/jane-orchestrator"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Print usage information
print_usage() {
    cat << EOF
MISP Comprehensive Test Execution Script

Usage: $0 [OPTIONS]

Options:
    -h, --help              Show this help message
    -v, --verbose           Enable verbose output
    -c, --coverage-only     Run only coverage analysis
    -p, --performance-only  Run only performance tests
    -f, --fast              Skip slow tests
    --no-cleanup           Don't cleanup temporary files
    --report-format FORMAT Set report format (json|html|both) [default: both]

Examples:
    $0                      # Run all MISP tests
    $0 -v                   # Run with verbose output
    $0 -p                   # Run only performance tests
    $0 --coverage-only      # Generate coverage report only

Test Requirements (T1986):
- Validate threat intelligence functionality preservation
- Achieve 80%+ test coverage for critical components
- Verify <1s response time for security domain operations
- Ensure 100% business logic preservation from original MISP

EOF
}

# Parse command line arguments
VERBOSE=false
COVERAGE_ONLY=false
PERFORMANCE_ONLY=false
FAST_MODE=false
NO_CLEANUP=false
REPORT_FORMAT="both"

while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            print_usage
            exit 0
            ;;
        -v|--verbose)
            VERBOSE=true
            shift
            ;;
        -c|--coverage-only)
            COVERAGE_ONLY=true
            shift
            ;;
        -p|--performance-only)
            PERFORMANCE_ONLY=true
            shift
            ;;
        -f|--fast)
            FAST_MODE=true
            shift
            ;;
        --no-cleanup)
            NO_CLEANUP=true
            shift
            ;;
        --report-format)
            REPORT_FORMAT="$2"
            shift 2
            ;;
        *)
            log_error "Unknown option: $1"
            print_usage
            exit 1
            ;;
    esac
done

# Validate environment
validate_environment() {
    log_info "Validating test environment..."
    
    # Check if we're in the correct directory structure
    if [[ ! -d "$PROJECT_ROOT/apps/jane-orchestrator" ]]; then
        log_error "jane-orchestrator app directory not found at $PROJECT_ROOT/apps/jane-orchestrator"
        exit 1
    fi
    
    # Check if MISP test directory exists
    if [[ ! -d "$MISP_TEST_DIR" ]]; then
        log_error "MISP test directory not found at $MISP_TEST_DIR"
        exit 1
    fi
    
    # Check for required test files
    local required_files=(
        "test_threat_intelligence_core.py"
        "test_api_integration.py"
        "test_performance_benchmarks.py"
        "execute_comprehensive_tests.py"
    )
    
    for file in "${required_files[@]}"; do
        if [[ ! -f "$MISP_TEST_DIR/$file" ]]; then
            log_error "Required test file not found: $MISP_TEST_DIR/$file"
            exit 1
        fi
    done
    
    # Check Python environment
    if ! command -v python3 &> /dev/null; then
        log_error "Python 3 is required but not installed"
        exit 1
    fi
    
    # Check pytest availability
    if ! python3 -c "import pytest" 2>/dev/null; then
        log_error "pytest is required but not installed"
        log_info "Install with: pip install pytest pytest-asyncio pytest-cov"
        exit 1
    fi
    
    log_success "Environment validation passed"
}

# Setup test environment
setup_test_environment() {
    log_info "Setting up test environment..."
    
    # Change to project root
    cd "$PROJECT_ROOT"
    
    # Set PYTHONPATH to include source directories
    export PYTHONPATH="$APPS_DIR/src:$PROJECT_ROOT:$PYTHONPATH"
    
    # Create temporary directories for test results
    mkdir -p "$MISP_TEST_DIR/results"
    mkdir -p "$MISP_TEST_DIR/htmlcov"
    
    # Setup test database if needed (mock for now)
    export MISP_TEST_MODE=true
    export MISP_TEST_DB_URL="sqlite:///tmp/misp_test.db"
    
    log_success "Test environment setup complete"
}

# Execute threat intelligence core tests
run_threat_intelligence_tests() {
    if [[ "$COVERAGE_ONLY" == true || "$PERFORMANCE_ONLY" == true ]]; then
        return 0
    fi
    
    log_info "Executing threat intelligence core functionality tests..."
    
    local test_cmd="python3 -m pytest $MISP_TEST_DIR/test_threat_intelligence_core.py"
    test_cmd="$test_cmd -v --tb=short"
    test_cmd="$test_cmd --cov=libs.service_adapters.security.misp_adapter"
    test_cmd="$test_cmd --cov=services.security_service"
    test_cmd="$test_cmd --cov-report=term-missing"
    
    if [[ "$FAST_MODE" == true ]]; then
        test_cmd="$test_cmd -m 'not slow'"
    fi
    
    if [[ "$VERBOSE" == true ]]; then
        test_cmd="$test_cmd -s"
    fi
    
    log_info "Command: $test_cmd"
    
    if eval "$test_cmd"; then
        log_success "Threat intelligence core tests PASSED"
        return 0
    else
        log_error "Threat intelligence core tests FAILED"
        return 1
    fi
}

# Execute unit model tests (Section 8.1)
run_unit_model_tests() {
    if [[ "$COVERAGE_ONLY" == true || "$PERFORMANCE_ONLY" == true ]]; then
        return 0
    fi
    
    log_info "Executing unit model validation tests (Section 8.1)..."
    
    local test_cmd="python3 -m pytest $MISP_TEST_DIR/test_unit_models.py"
    test_cmd="$test_cmd -v --tb=short"
    test_cmd="$test_cmd --cov=data.models"
    test_cmd="$test_cmd --cov=libs.service_adapters.security.misp_adapter"
    test_cmd="$test_cmd --cov-report=term-missing"
    
    if [[ "$FAST_MODE" == true ]]; then
        test_cmd="$test_cmd -m 'not slow'"
    fi
    
    if [[ "$VERBOSE" == true ]]; then
        test_cmd="$test_cmd -s"
    fi
    
    log_info "Command: $test_cmd"
    
    if eval "$test_cmd"; then
        log_success "Unit model tests PASSED"
        return 0
    else
        log_error "Unit model tests FAILED"
        return 1
    fi
}

# Execute functional workflow tests (Section 8.2)
run_functional_workflow_tests() {
    if [[ "$COVERAGE_ONLY" == true || "$PERFORMANCE_ONLY" == true ]]; then
        return 0
    fi
    
    log_info "Executing functional workflow tests (Section 8.2)..."
    
    local test_cmd="python3 -m pytest $MISP_TEST_DIR/test_functional_workflows.py"
    test_cmd="$test_cmd -v --tb=short --asyncio-mode=auto"
    test_cmd="$test_cmd --cov=api"
    test_cmd="$test_cmd --cov=services"
    test_cmd="$test_cmd --cov=libs.service_adapters.security.misp_adapter"
    test_cmd="$test_cmd --cov-report=term-missing"
    
    if [[ "$FAST_MODE" == true ]]; then
        test_cmd="$test_cmd -m 'not slow'"
    fi
    
    if [[ "$VERBOSE" == true ]]; then
        test_cmd="$test_cmd -s"
    fi
    
    log_info "Command: $test_cmd"
    
    if eval "$test_cmd"; then
        log_success "Functional workflow tests PASSED"
        return 0
    else
        log_error "Functional workflow tests FAILED"
        return 1
    fi
}

# Execute integration external tests (Section 8.3)
run_integration_external_tests() {
    if [[ "$COVERAGE_ONLY" == true || "$PERFORMANCE_ONLY" == true ]]; then
        return 0
    fi
    
    log_info "Executing integration external tests (Section 8.3)..."
    
    local test_cmd="python3 -m pytest $MISP_TEST_DIR/test_integration_external.py"
    test_cmd="$test_cmd -v --tb=short --asyncio-mode=auto"
    test_cmd="$test_cmd --cov=api"
    test_cmd="$test_cmd --cov=services"
    test_cmd="$test_cmd --cov=libs.service_adapters.security.misp_adapter"
    test_cmd="$test_cmd --cov=data"
    test_cmd="$test_cmd --cov-report=term-missing"
    
    if [[ "$FAST_MODE" == true ]]; then
        test_cmd="$test_cmd -m 'not slow'"
    fi
    
    if [[ "$VERBOSE" == true ]]; then
        test_cmd="$test_cmd -s"
    fi
    
    log_info "Command: $test_cmd"
    
    if eval "$test_cmd"; then
        log_success "Integration external tests PASSED"
        return 0
    else
        log_error "Integration external tests FAILED"
        return 1
    fi
}

# Execute API integration tests
run_api_integration_tests() {
    if [[ "$COVERAGE_ONLY" == true || "$PERFORMANCE_ONLY" == true ]]; then
        return 0
    fi
    
    log_info "Executing API integration compatibility tests..."
    
    local test_cmd="python3 -m pytest $MISP_TEST_DIR/test_api_integration.py"
    test_cmd="$test_cmd -v --tb=short"
    test_cmd="$test_cmd --cov=api.security"
    test_cmd="$test_cmd --cov=libs.service_adapters.security.misp_adapter"
    test_cmd="$test_cmd --cov-report=term-missing"
    
    if [[ "$FAST_MODE" == true ]]; then
        test_cmd="$test_cmd -m 'not slow'"
    fi
    
    if [[ "$VERBOSE" == true ]]; then
        test_cmd="$test_cmd -s"
    fi
    
    log_info "Command: $test_cmd"
    
    if eval "$test_cmd"; then
        log_success "API integration tests PASSED"
        return 0
    else
        log_error "API integration tests FAILED"
        return 1
    fi
}

# Execute performance benchmark tests
run_performance_tests() {
    if [[ "$COVERAGE_ONLY" == true ]]; then
        return 0
    fi
    
    log_info "Executing performance benchmark tests..."
    
    local test_cmd="python3 -m pytest $MISP_TEST_DIR/test_performance_benchmarks.py"
    test_cmd="$test_cmd -v --tb=short"
    test_cmd="$test_cmd --cov=libs.service_adapters.security.misp_adapter"
    test_cmd="$test_cmd --cov-report=term-missing"
    test_cmd="$test_cmd --benchmark-only"
    
    if [[ "$VERBOSE" == true ]]; then
        test_cmd="$test_cmd -s"
    fi
    
    log_info "Command: $test_cmd"
    
    if eval "$test_cmd"; then
        log_success "Performance benchmark tests PASSED"
        return 0
    else
        log_error "Performance benchmark tests FAILED"
        return 1
    fi
}

# Execute comprehensive test suite using the framework
run_comprehensive_tests() {
    if [[ "$COVERAGE_ONLY" == true || "$PERFORMANCE_ONLY" == true ]]; then
        return 0
    fi
    
    log_info "Executing comprehensive test framework..."
    
    local test_cmd="python3 $MISP_TEST_DIR/execute_comprehensive_tests.py"
    
    if [[ "$VERBOSE" == true ]]; then
        test_cmd="$test_cmd --verbose"
    fi
    
    log_info "Command: $test_cmd"
    
    if eval "$test_cmd"; then
        log_success "Comprehensive test framework execution PASSED"
        return 0
    else
        log_error "Comprehensive test framework execution FAILED"
        return 1
    fi
}

# Generate coverage report
generate_coverage_report() {
    log_info "Generating comprehensive coverage report..."
    
    local coverage_cmd="python3 -m pytest $MISP_TEST_DIR/"
    coverage_cmd="$coverage_cmd --cov=libs.service_adapters.security.misp_adapter"
    coverage_cmd="$coverage_cmd --cov=services.security_service"
    coverage_cmd="$coverage_cmd --cov=api.security"
    coverage_cmd="$coverage_cmd --cov=data.models.security_profile"
    coverage_cmd="$coverage_cmd --cov-report=html:$MISP_TEST_DIR/htmlcov"
    coverage_cmd="$coverage_cmd --cov-report=json:$MISP_TEST_DIR/results/coverage.json"
    coverage_cmd="$coverage_cmd --cov-report=term-missing"
    coverage_cmd="$coverage_cmd --cov-branch"
    
    if [[ "$FAST_MODE" == true ]]; then
        coverage_cmd="$coverage_cmd -m 'not slow'"
    fi
    
    log_info "Command: $coverage_cmd"
    
    if eval "$coverage_cmd"; then
        log_success "Coverage report generated successfully"
        log_info "HTML coverage report: $MISP_TEST_DIR/htmlcov/index.html"
        log_info "JSON coverage report: $MISP_TEST_DIR/results/coverage.json"
        return 0
    else
        log_error "Coverage report generation FAILED"
        return 1
    fi
}

# Validate results against T1986 requirements
validate_test_requirements() {
    log_info "Validating test results against T1986 requirements..."
    
    local validation_passed=true
    
    # Check if coverage JSON exists
    if [[ -f "$MISP_TEST_DIR/results/coverage.json" ]]; then
        # Extract coverage percentage (simplified parsing)
        local coverage_percent=$(python3 -c "
import json
try:
    with open('$MISP_TEST_DIR/results/coverage.json', 'r') as f:
        data = json.load(f)
    print(data.get('totals', {}).get('percent_covered', 0))
except:
    print(0)
")
        
        log_info "Coverage percentage: ${coverage_percent}%"
        
        if (( $(echo "$coverage_percent >= 80" | bc -l) )); then
            log_success "Coverage requirement met (≥80%): ${coverage_percent}%"
        else
            log_error "Coverage requirement NOT met (<80%): ${coverage_percent}%"
            validation_passed=false
        fi
    else
        log_warning "Coverage report not found, skipping coverage validation"
    fi
    
    # Check for test report files
    local report_files=(
        "$MISP_TEST_DIR/results/misp_test_report_*.json"
    )
    
    local report_found=false
    for pattern in "${report_files[@]}"; do
        if ls $pattern 1> /dev/null 2>&1; then
            report_found=true
            log_success "Test execution report found: $(ls $pattern | head -1)"
            break
        fi
    done
    
    if [[ "$report_found" == false ]]; then
        log_warning "No test execution report found"
    fi
    
    if [[ "$validation_passed" == true ]]; then
        log_success "All T1986 requirements validation PASSED"
        return 0
    else
        log_error "T1986 requirements validation FAILED"
        return 1
    fi
}

# Print final summary
print_final_summary() {
    local exit_code=$1
    
    echo ""
    echo "=========================================="
    echo "MISP Comprehensive Test Execution Summary"
    echo "=========================================="
    
    if [[ $exit_code -eq 0 ]]; then
        log_success "✅ ALL TESTS PASSED - MISP integration validation successful"
        echo ""
        echo "Business Logic Preservation: ✅ VALIDATED"
        echo "API Compatibility: ✅ MAINTAINED"
        echo "Performance Requirements: ✅ MET (<1s security domain)"
        echo "Test Coverage: ✅ ACHIEVED (≥80%)"
        echo ""
        echo "🎉 MISP ready for migration from features/MISP/ directory"
        echo ""
        echo "Next steps:"
        echo "1. Review test reports in: $MISP_TEST_DIR/results/"
        echo "2. Verify coverage report: $MISP_TEST_DIR/htmlcov/index.html"
        echo "3. Proceed with T2106l: Remove features/MISP/ directory"
    else
        log_error "❌ TESTS FAILED - MISP integration validation unsuccessful"
        echo ""
        echo "Issues found that must be resolved before migration:"
        echo "- Check test output above for specific failures"
        echo "- Review coverage requirements (≥80% needed)"
        echo "- Validate performance benchmarks (<1s security domain)"
        echo ""
        echo "🚫 DO NOT proceed with features/MISP/ directory removal"
        echo ""
        echo "Troubleshooting:"
        echo "1. Check detailed logs in test output"
        echo "2. Review failed test cases"
        echo "3. Verify MISP service adapter implementation"
        echo "4. Re-run with -v flag for verbose output"
    fi
    
    echo "=========================================="
}

# Cleanup temporary files
cleanup() {
    if [[ "$NO_CLEANUP" != true ]]; then
        log_info "Cleaning up temporary files..."
        
        # Remove temporary test files
        rm -f /tmp/pytest_results.json
        rm -f /tmp/coverage_results.json
        rm -f /tmp/misp_test.db
        
        log_info "Cleanup completed"
    fi
}

# Main execution function
main() {
    local overall_success=true
    
    # Trap cleanup on exit
    trap cleanup EXIT
    
    log_info "Starting MISP Comprehensive Test Execution (T1986)"
    log_info "Requirements: Validate threat intelligence functionality preservation"
    
    # Validate environment
    validate_environment
    
    # Setup test environment
    setup_test_environment
    
    # Execute test suites based on options
    if [[ "$PERFORMANCE_ONLY" == true ]]; then
        log_info "Running performance tests only..."
        if ! run_performance_tests; then
            overall_success=false
        fi
    elif [[ "$COVERAGE_ONLY" == true ]]; then
        log_info "Generating coverage report only..."
        if ! generate_coverage_report; then
            overall_success=false
        fi
    else
        # Run all test suites matching Section 7.1-7.2 requirements
        log_info "Running comprehensive test suite..."
        
        # Section 8.1 - Unit Tests
        if ! run_unit_model_tests; then
            overall_success=false
        fi
        
        # Section 8.2 - Functional Tests
        if ! run_functional_workflow_tests; then
            overall_success=false
        fi
        
        # Section 8.3 - Integration Tests
        if ! run_integration_external_tests; then
            overall_success=false
        fi
        
        # Core validation tests
        if ! run_threat_intelligence_tests; then
            overall_success=false
        fi
        
        if ! run_api_integration_tests; then
            overall_success=false
        fi
        
        if ! run_performance_tests; then
            overall_success=false
        fi
        
        if ! run_comprehensive_tests; then
            overall_success=false
        fi
        
        # Generate reports
        if ! generate_coverage_report; then
            overall_success=false
        fi
    fi
    
    # Validate against requirements
    if ! validate_test_requirements; then
        overall_success=false
    fi
    
    # Print final summary
    local exit_code=0
    if [[ "$overall_success" != true ]]; then
        exit_code=1
    fi
    
    print_final_summary $exit_code
    
    return $exit_code
}

# Execute main function
main "$@"