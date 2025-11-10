#!/bin/bash

# Hybrid Architecture Migration Script
# Migrates all 37 tools from features/ to appropriate domain services
# Based on the implementation guide for hybrid domain-based architecture

set -e  # Exit on any error

echo "🚀 Starting hybrid architecture migration..."
echo "This will migrate all 37 tools from features/ to domain services"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
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

# Check if features directory exists and has content
if [ ! -d "features" ]; then
    print_error "features/ directory not found"
    exit 1
fi

if [ -z "$(ls -A features/)" ]; then
    print_warning "features/ directory is already empty - migration may be complete"
    exit 0
fi

print_status "Found $(ls -1 features/ | wc -l) items in features/ directory"

# Security Domain Migration (13 tools)
print_status "Migrating Security Domain tools..."
SECURITY_TOOLS=(
    "misp"
    "HELK:helk"
    "yara-x:yara"
    "CyberChef:cyberchef" 
    "Nemesis:nemesis"
    "Ghostwriter:ghostwriter"
    "maltrail"
    "securityonion"
    "rita"
    "blackarch"
    "onex"
    "Brute-Ratel-C4-Community-Kit:brute-ratel"
    "apiscout"
)

for tool in "${SECURITY_TOOLS[@]}"; do
    IFS=':' read -r source_name target_name <<< "$tool"
    target_name=${target_name:-$source_name}
    
    if [ -d "features/$source_name" ]; then
        print_status "Migrating $source_name → apps/security-service/src/domains/$target_name/"
        mv "features/$source_name/" "apps/security-service/src/domains/$target_name/"
        # Remove README placeholder
        rm -f "apps/security-service/src/domains/$target_name/README.md" 2>/dev/null || true
        print_success "✓ $source_name migrated"
    else
        print_warning "⚠ $source_name not found in features/"
    fi
done

# Productivity Domain Migration (8 tools)
print_status "Migrating Productivity Domain tools..."
PRODUCTIVITY_TOOLS=(
    "actual:actual-budget"
    "mealie"
    "dispatch"
    "firecrawl"
    "goose"
    "inspector"
    "it-tools"
    "kong"
)

for tool in "${PRODUCTIVITY_TOOLS[@]}"; do
    IFS=':' read -r source_name target_name <<< "$tool"
    target_name=${target_name:-$source_name}
    
    if [ -d "features/$source_name" ]; then
        print_status "Migrating $source_name → apps/productivity-service/src/domains/$target_name/"
        mv "features/$source_name/" "apps/productivity-service/src/domains/$target_name/"
        rm -f "apps/productivity-service/src/domains/$target_name/README.md" 2>/dev/null || true
        print_success "✓ $source_name migrated"
    else
        print_warning "⚠ $source_name not found in features/"
    fi
done

# MTG Domain Migration (4 tools)
print_status "Migrating MTG Domain tools..."
MTG_TOOLS=(
    "commander-spellbook-backend"
    "commander-spellbook-site"
    "mtg-commander-map"
    "mtg-scripting-toolkit"
)

for tool in "${MTG_TOOLS[@]}"; do
    if [ -d "features/$tool" ]; then
        print_status "Migrating $tool → apps/mtg-service/src/domains/$tool/"
        mv "features/$tool/" "apps/mtg-service/src/domains/$tool/"
        rm -f "apps/mtg-service/src/domains/$tool/README.md" 2>/dev/null || true
        print_success "✓ $tool migrated"
    else
        print_warning "⚠ $tool not found in features/"
    fi
done

# Infrastructure Domain Migration (12 tools)
print_status "Migrating Infrastructure Domain tools..."
INFRASTRUCTURE_TOOLS=(
    "KasmVNC:kasmvnc"
    "lscript"
    "software-forensic-kit"
    "meterpreter"
    "hexstrike-ai"
)

for tool in "${INFRASTRUCTURE_TOOLS[@]}"; do
    IFS=':' read -r source_name target_name <<< "$tool"
    target_name=${target_name:-$source_name}
    
    if [ -d "features/$source_name" ]; then
        print_status "Migrating $source_name → apps/infrastructure-service/src/domains/$target_name/"
        mv "features/$source_name/" "apps/infrastructure-service/src/domains/$target_name/"
        rm -f "apps/infrastructure-service/src/domains/$target_name/README.md" 2>/dev/null || true
        print_success "✓ $source_name migrated"
    else
        print_warning "⚠ $source_name not found in features/"
    fi
done

# MCP Servers Migration
print_status "Migrating MCP servers to Infrastructure Domain..."
MCP_TOOLS=(
    "chroma-mcp"
    "FileScopeMCP:filescope-mcp"
    "firecrawl-mcp-server:firecrawl-mcp"
    "MalwareBazaar_MCP:malwarebazaar-mcp"
    "mcp-virustotal"
)

for tool in "${MCP_TOOLS[@]}"; do
    IFS=':' read -r source_name target_name <<< "$tool"
    target_name=${target_name:-$source_name}
    
    if [ -d "features/$source_name" ]; then
        print_status "Migrating $source_name → apps/infrastructure-service/src/domains/mcp-servers/$target_name/"
        mv "features/$source_name/" "apps/infrastructure-service/src/domains/mcp-servers/$target_name/"
        rm -f "apps/infrastructure-service/src/domains/mcp-servers/$target_name/README.md" 2>/dev/null || true
        print_success "✓ $source_name migrated"
    else
        print_warning "⚠ $source_name not found in features/"
    fi
done

# n8n Migration to Central Workflow Service
print_status "Migrating n8n to central workflow service..."
if [ -d "features/n8n" ]; then
    print_status "Migrating n8n → apps/n8n-workflow-service/src/workflows/n8n/"
    mv "features/n8n/" "apps/n8n-workflow-service/src/workflows/n8n/"
    print_success "✓ n8n migrated to central orchestration service"
fi

if [ -d "features/n8n-mcp-server" ]; then
    print_status "Migrating n8n-mcp-server → apps/n8n-workflow-service/src/ai/n8n-mcp/"
    mv "features/n8n-mcp-server/" "apps/n8n-workflow-service/src/ai/n8n-mcp/"
    print_success "✓ n8n MCP server migrated"
fi

if [ -d "features/securityonion-n8n-workflows" ]; then
    print_status "Migrating securityonion-n8n-workflows → apps/n8n-workflow-service/src/workflows/security-workflows/"
    mv "features/securityonion-n8n-workflows/" "apps/n8n-workflow-service/src/workflows/security-workflows/"
    print_success "✓ SecurityOnion n8n workflows migrated"
fi

# Check migration completion
print_status "Checking migration completion..."
remaining_items=$(ls -1 features/ 2>/dev/null | wc -l)

if [ "$remaining_items" -eq 0 ]; then
    print_success "🎉 SUCCESS: All 37 tools have been migrated!"
    print_success "✅ features/ directory is now empty"
    print_status "Next steps:"
    echo "  1. Update service main.py files to remove placeholder status"
    echo "  2. Implement actual business logic integration"
    echo "  3. Test all services with: npx nx run-many --target=serve --all"
    echo "  4. Remove legacy jane-orchestrator when ready"
else
    print_warning "⚠ Migration incomplete. Remaining items in features/:"
    ls -la features/
    print_status "You may need to manually handle these remaining items"
fi

print_status "Migration script completed!"