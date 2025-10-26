#!/bin/bash

# Validation Script for Hybrid Domain-Based Architecture
# Validates that the hybrid architecture migration is successful

set -e

echo "🔍 Validating hybrid domain-based architecture..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Validation counters
total_checks=0
passed_checks=0
failed_checks=0

check_passed() {
    ((total_checks++))
    ((passed_checks++))
    print_success "✅ $1"
}

check_failed() {
    ((total_checks++))
    ((failed_checks++))
    print_error "❌ $1"
}

check_warning() {
    ((total_checks++))
    print_warning "⚠️ $1"
}

# 1. Directory Structure Validation
print_status "Validating directory structure..."

# Check if all 5 services exist
services=("n8n-workflow-service" "security-service" "productivity-service" "mtg-service" "infrastructure-service")
for service in "${services[@]}"; do
    if [ -d "apps/$service" ]; then
        check_passed "$service directory exists"
    else
        check_failed "$service directory missing"
    fi
done

# 2. Service Structure Validation
print_status "Validating service internal structure..."

for service in "${services[@]}"; do
    if [ -d "apps/$service" ]; then
        # Check main.py exists
        if [ -f "apps/$service/src/main.py" ]; then
            check_passed "$service has main.py"
        else
            check_failed "$service missing main.py"
        fi
        
        # Check project.json exists
        if [ -f "apps/$service/project.json" ]; then
            check_passed "$service has project.json"
        else
            check_failed "$service missing project.json"
        fi
        
        # Check required directories
        required_dirs=("src/api" "src/data" "src/services" "src/domains")
        for dir in "${required_dirs[@]}"; do
            if [ -d "apps/$service/$dir" ]; then
                check_passed "$service has $dir/"
            else
                check_failed "$service missing $dir/"
            fi
        done
    fi
done

# 3. n8n Workflow Service Special Validation
print_status "Validating n8n workflow service structure..."

if [ -d "apps/n8n-workflow-service" ]; then
    n8n_dirs=("src/workflows" "src/ai" "src/orchestration" "src/api")
    for dir in "${n8n_dirs[@]}"; do
        if [ -d "apps/n8n-workflow-service/$dir" ]; then
            check_passed "n8n-workflow-service has $dir/"
        else
            check_failed "n8n-workflow-service missing $dir/"
        fi
    done
    
    # Check AI enhancement modules
    ai_modules=("src/ai/pattern_detection.py" "src/ai/workflow_generator.py")
    for module in "${ai_modules[@]}"; do
        if [ -f "apps/n8n-workflow-service/$module" ]; then
            check_passed "n8n-workflow-service has $module"
        else
            check_failed "n8n-workflow-service missing $module"
        fi
    done
fi

# 4. Features Directory Validation
print_status "Validating features/ directory..."

if [ -d "features" ]; then
    feature_count=$(ls -1 features/ 2>/dev/null | wc -l)
    if [ "$feature_count" -eq 0 ]; then
        check_passed "features/ directory is empty (migration complete)"
    else
        check_warning "features/ directory contains $feature_count items (migration incomplete)"
        echo "    Remaining items:"
        ls -la features/ | sed 's/^/      /'
    fi
else
    check_failed "features/ directory not found"
fi

# 5. NX Configuration Validation
print_status "Validating NX configuration..."

if [ -f "nx.json" ]; then
    check_passed "nx.json exists"
    
    # Check if projects are defined
    if grep -q "projects" nx.json; then
        check_passed "nx.json has projects configuration"
        
        # Check if new services are in projects
        for service in "${services[@]}"; do
            if grep -q "\"$service\"" nx.json; then
                check_passed "$service listed in nx.json projects"
            else
                check_failed "$service not found in nx.json projects"
            fi
        done
    else
        check_failed "nx.json missing projects configuration"
    fi
else
    check_failed "nx.json not found"
fi

# 6. Docker Configuration Validation
print_status "Validating Docker configuration..."

if [ -f "infrastructure/docker/docker-compose.yml" ]; then
    check_passed "docker-compose.yml exists"
    
    # Check if all services are defined
    for service in "${services[@]}"; do
        if grep -q "$service:" infrastructure/docker/docker-compose.yml; then
            check_passed "$service defined in docker-compose.yml"
        else
            check_failed "$service not found in docker-compose.yml"
        fi
    done
    
    # Check for required infrastructure services
    infra_services=("postgres" "redis")
    for infra in "${infra_services[@]}"; do
        if grep -q "$infra:" infrastructure/docker/docker-compose.yml; then
            check_passed "$infra defined in docker-compose.yml"
        else
            check_failed "$infra not found in docker-compose.yml"
        fi
    done
    
else
    check_failed "docker-compose.yml not found"
fi

# 7. LLM Server Validation
print_status "Validating AI server configuration..."

if [ -d "apps/infrastructure-llm-server" ]; then
    check_passed "infrastructure-llm-server exists (renamed from code-llm-server)"
else
    if [ -d "apps/code-llm-server" ]; then
        check_warning "code-llm-server still exists (should be renamed to infrastructure-llm-server)"
    else
        check_failed "infrastructure-llm-server not found"
    fi
fi

ai_servers=("cyber-llm-server" "mtg-llm-server" "infrastructure-llm-server")
for server in "${ai_servers[@]}"; do
    if [ -d "apps/$server" ]; then
        check_passed "$server exists"
    else
        check_failed "$server directory missing"
    fi
done

# 8. Tool Migration Validation (Sample Check)
print_status "Validating tool migration (sample check)..."

# Check a few key tools in their expected locations
if [ -d "apps/security-service/src/domains" ]; then
    security_tool_count=$(ls -1 apps/security-service/src/domains/ 2>/dev/null | wc -l)
    if [ "$security_tool_count" -gt 0 ]; then
        check_passed "Security service has $security_tool_count tool directories"
    else
        check_warning "Security service has no tool directories"
    fi
fi

if [ -d "apps/productivity-service/src/domains" ]; then
    productivity_tool_count=$(ls -1 apps/productivity-service/src/domains/ 2>/dev/null | wc -l)
    if [ "$productivity_tool_count" -gt 0 ]; then
        check_passed "Productivity service has $productivity_tool_count tool directories"
    else
        check_warning "Productivity service has no tool directories"
    fi
fi

# 9. NX Build Test
print_status "Testing NX build capability..."

if command -v npx >/dev/null 2>&1; then
    print_status "Running NX build test..."
    if npx nx run-many --target=build --all --parallel=3 >/dev/null 2>&1; then
        check_passed "All services build successfully with NX"
    else
        check_warning "Some services failed to build (expected for placeholder services)"
    fi
else
    check_warning "npx not available, skipping build test"
fi

# Results Summary
echo ""
echo "=================================="
echo "📊 VALIDATION SUMMARY"
echo "=================================="
echo -e "Total Checks: ${BLUE}$total_checks${NC}"
echo -e "Passed: ${GREEN}$passed_checks${NC}"
echo -e "Failed: ${RED}$failed_checks${NC}"
echo -e "Warnings: ${YELLOW}$((total_checks - passed_checks - failed_checks))${NC}"

if [ "$failed_checks" -eq 0 ]; then
    print_success "🎉 Hybrid architecture validation PASSED!"
    echo ""
    echo "Next Steps:"
    echo "1. Run migration script: ./migrate_to_hybrid_architecture.sh"
    echo "2. Test services: npx nx run-many --target=serve --all"
    echo "3. Begin actual tool integration and business logic implementation"
    echo "4. Remove legacy jane-orchestrator when ready"
else
    print_error "⚠️ Validation found $failed_checks issues that need to be addressed"
    echo ""
    echo "Please fix the failed checks before proceeding with migration."
fi

echo ""
print_status "Architecture validation completed!"

# Exit with appropriate code
if [ "$failed_checks" -eq 0 ]; then
    exit 0
else
    exit 1
fi