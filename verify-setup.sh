#!/bin/bash
# Verification script for modular-monolith-2 environment
# Run this to check if your development environment is properly configured

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_check() {
    if eval "$2"; then
        echo -e "✅ ${GREEN}$1${NC}"
        return 0
    else
        echo -e "❌ ${RED}$1${NC}"
        return 1
    fi
}

print_header() {
    echo -e "\n${BLUE}$1${NC}"
    echo "================================================"
}

echo "🔍 Environment Verification for Modular Monolith"
echo "================================================"

# Check system requirements
print_header "System Requirements"
print_check "Node.js 20+" "node --version | grep -q '^v2[0-9]'"
print_check "Python 3.12+" "python --version | grep -q 'Python 3.1[2-9]'"
print_check "npm installed" "command -v npm >/dev/null"
print_check "pip installed" "command -v pip >/dev/null"

# Check modern tools
print_header "Modern Development Tools"
print_check "UV installed" "command -v uv >/dev/null"
print_check "specify-cli installed" "command -v specify >/dev/null || command -v ~/.local/bin/specify >/dev/null"

# Check project setup
print_header "Project Configuration"
print_check "NX workspace configured" "npx nx --version >/dev/null 2>&1"
print_check "Node modules installed" "[ -d node_modules ] && [ -f node_modules/.package-lock.json ] || [ -f package-lock.json ]"
print_check "Python deps for orchestrator" "python -c 'import fastapi, uvicorn' >/dev/null 2>&1"
print_check "Python deps for LLM servers" "python -c 'import vllm' >/dev/null 2>&1"

# Check project structure
print_header "Project Structure"
print_check "Apps directory exists" "[ -d apps ]"
print_check "Jane UI app exists" "[ -d apps/jane-ui ]"
print_check "Jane Orchestrator exists" "[ -d apps/jane-orchestrator ]"
print_check "LLM servers exist" "[ -d apps/cyber-llm-server ] && [ -d apps/mtg-llm-server ] && [ -d apps/code-llm-server ]"

# Check optional tools
print_header "Optional Tools"
print_check "Docker installed" "command -v docker >/dev/null"
print_check "Docker Compose installed" "command -v docker-compose >/dev/null"
print_check "kubectl installed" "command -v kubectl >/dev/null"

# Check environment files
print_header "Environment Configuration"
print_check "Orchestrator .env exists" "[ -f apps/jane-orchestrator/.env ]"
print_check "UI .env exists" "[ -f apps/jane-ui/.env ]"

# Test basic functionality
print_header "Functionality Tests"
print_check "NX can list projects" "npx nx show projects >/dev/null 2>&1"
print_check "Can import FastAPI" "python -c 'import fastapi' >/dev/null 2>&1"
print_check "React types available" "[ -d node_modules/@types/react ]"

echo ""
echo "🎯 Summary"
echo "================================================"

# Count successful checks
TOTAL_CHECKS=17
PASSED_CHECKS=$(bash -c '
total=0
node --version | grep -q "^v2[0-9]" && ((total++))
python --version | grep -q "Python 3.1[2-9]" && ((total++))
command -v npm >/dev/null && ((total++))
command -v pip >/dev/null && ((total++))
command -v uv >/dev/null && ((total++))
(command -v specify >/dev/null || command -v ~/.local/bin/specify >/dev/null) && ((total++))
npx nx --version >/dev/null 2>&1 && ((total++))
([ -d node_modules ] && ([ -f node_modules/.package-lock.json ] || [ -f package-lock.json ])) && ((total++))
python -c "import fastapi, uvicorn" >/dev/null 2>&1 && ((total++))
python -c "import vllm" >/dev/null 2>&1 && ((total++))
[ -d apps ] && ((total++))
[ -d apps/jane-ui ] && ((total++))
[ -d apps/jane-orchestrator ] && ((total++))
([ -d apps/cyber-llm-server ] && [ -d apps/mtg-llm-server ] && [ -d apps/code-llm-server ]) && ((total++))
[ -f apps/jane-orchestrator/.env ] && ((total++))
[ -f apps/jane-ui/.env ] && ((total++))
npx nx show projects >/dev/null 2>&1 && ((total++))
echo $total
')

if [ "$PASSED_CHECKS" -eq "$TOTAL_CHECKS" ]; then
    echo -e "🎉 ${GREEN}Perfect! All checks passed ($PASSED_CHECKS/$TOTAL_CHECKS)${NC}"
    echo -e "🚀 ${GREEN}Your environment is ready for development!${NC}"
elif [ "$PASSED_CHECKS" -ge 12 ]; then
    echo -e "✅ ${GREEN}Good! Most checks passed ($PASSED_CHECKS/$TOTAL_CHECKS)${NC}"
    echo -e "⚠️  Some optional features may not be available."
else
    echo -e "⚠️  ${RED}Some issues found ($PASSED_CHECKS/$TOTAL_CHECKS checks passed)${NC}"
    echo -e "🔧 Consider running: ./setup-codespace.sh"
fi

echo ""
echo "Ready-to-use commands:"
echo "  npx nx serve jane-ui          # Start UI (http://localhost:3000)"
echo "  npx nx serve jane-orchestrator # Start API (http://localhost:8000)"
echo "  make build                    # Build all projects"
echo "  ./setup-codespace.sh          # Re-run full setup if needed"