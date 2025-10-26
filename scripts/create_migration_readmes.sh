#!/bin/bash

# Script to generate README files for all 37 tool migration directories
# This creates placeholder instructions for each tool migration

echo "Creating migration README files for all 37 tools..."

# Security Domain Tools (13 tools)
declare -A SECURITY_TOOLS=(
    ["helk"]="HELK:Hunting ELK Stack for threat hunting and log analysis"
    ["yara"]="YARA-X:Pattern matching engine for malware detection"
    ["cyberchef"]="CyberChef:Data operations and analysis toolkit"
    ["nemesis"]="Nemesis:Post-exploitation framework for red team operations"
    ["ghostwriter"]="Ghostwriter:Penetration testing reporting and documentation"
    ["maltrail"]="Maltrail:Malicious traffic detection system"
    ["securityonion"]="SecurityOnion:Network security monitoring platform"
    ["rita"]="RITA:Real Intelligence Threat Analytics for network analysis"
    ["blackarch"]="BlackArch:Collection of penetration testing tools"
    ["onex"]="OneX:Security exploitation toolkit and framework"
    ["brute-ratel"]="Brute Ratel C4:Red team C2 framework and toolkit"
    ["apiscout"]="ApiScout:API reconnaissance and discovery tool"
)

# Productivity Domain Tools (8 tools)  
declare -A PRODUCTIVITY_TOOLS=(
    ["actual-budget"]="Actual Budget:Personal finance management with CRDT sync"
    ["mealie"]="Mealie:Recipe management and meal planning system"
    ["dispatch"]="Dispatch:Incident management and response coordination"
    ["firecrawl"]="Firecrawl:Web scraping and content extraction service"
    ["goose"]="Goose:AI-powered coding assistant and development tool"
    ["inspector"]="Inspector:Code inspection and analysis toolkit"
    ["it-tools"]="IT-Tools:Collection of 80+ IT utility tools"
    ["kong"]="Kong:API Gateway for microservices (if productivity-focused)"
)

# MTG Domain Tools (4 tools)
declare -A MTG_TOOLS=(
    ["commander-spellbook-backend"]="Commander Spellbook Backend:Django API for MTG combo database"
    ["commander-spellbook-site"]="Commander Spellbook Site:Vue.js frontend for combo search"
    ["mtg-commander-map"]="MTG Commander Map:Commander deck mapping and analysis"
    ["mtg-scripting-toolkit"]="MTG Scripting Toolkit:Automation scripts for MTG workflows"
)

# Infrastructure Domain Tools (12 tools)
declare -A INFRASTRUCTURE_TOOLS=(
    ["kasmvnc"]="KasmVNC:Remote desktop solution with web interface"
    ["lscript"]="LScript:Linux scripting tools and automation utilities"
    ["software-forensic-kit"]="Software Forensic Kit:Digital forensics analysis tools"
    ["meterpreter"]="Meterpreter:Penetration testing payload framework"
    ["hexstrike-ai"]="HexStrike AI:AI-powered security analysis tools"
    ["mcp-servers/chroma-mcp"]="Chroma MCP:Vector database MCP server integration"
    ["mcp-servers/filescope-mcp"]="FileScopeMCP:File analysis MCP server"
    ["mcp-servers/firecrawl-mcp"]="Firecrawl MCP:Web scraping MCP server integration"
    ["mcp-servers/malwarebazaar-mcp"]="MalwareBazaar MCP:Malware analysis MCP server"
    ["mcp-servers/mcp-virustotal"]="VirusTotal MCP:VirusTotal integration MCP server"
)

# Function to create README for a tool
create_tool_readme() {
    local service=$1
    local tool_dir=$2
    local tool_info=$3
    local performance_target=$4
    
    IFS=':' read -r tool_name tool_description <<< "$tool_info"
    
    cat > "apps/${service}/src/domains/${tool_dir}/README.md" << EOF
# ${tool_name} Integration Directory

This directory will contain the ${tool_name} integration.

## Migration Instructions

When migrating from \`features/${tool_dir}/\`, move the following:

### Core Components
- **Application Code**: Move main application files and business logic
- **Configuration**: Move config files to \`../services/${tool_dir}_config.py\`
- **Database Schema**: Migrate database models to \`../data/models/\`
- **API Integration**: Create FastAPI endpoints in \`../api/${tool_dir}_api.py\`

### Description
${tool_description}

### Integration Points
- **${service^} Service API**: Expose operations via FastAPI endpoints
- **Database**: Convert schemas to PostgreSQL models
- **Authentication**: Integrate with unified JWT authentication
- **n8n Integration**: Create workflow nodes for automation

### Performance Requirements
- Response time: ${performance_target}
- Support for concurrent operations
- Caching for frequently accessed data

## TODO: Delete this README when migration is complete

This placeholder will be replaced with actual integration code during the migration process.
EOF
}

# Create READMEs for Security Tools
for tool_dir in "${!SECURITY_TOOLS[@]}"; do
    create_tool_readme "security-service" "$tool_dir" "${SECURITY_TOOLS[$tool_dir]}" "<1s for threat analysis"
done

# Create READMEs for Productivity Tools
for tool_dir in "${!PRODUCTIVITY_TOOLS[@]}"; do
    create_tool_readme "productivity-service" "$tool_dir" "${PRODUCTIVITY_TOOLS[$tool_dir]}" "<2s for task management"
done

# Create READMEs for MTG Tools
for tool_dir in "${!MTG_TOOLS[@]}"; do
    create_tool_readme "mtg-service" "$tool_dir" "${MTG_TOOLS[$tool_dir]}" "<3s for game analysis"
done

# Create READMEs for Infrastructure Tools
for tool_dir in "${!INFRASTRUCTURE_TOOLS[@]}"; do
    create_tool_readme "infrastructure-service" "$tool_dir" "${INFRASTRUCTURE_TOOLS[$tool_dir]}" "<5s for system operations"
done

echo "✅ Created migration README files for all 37 tools"
echo "📁 Each tool directory now contains migration instructions"
echo "🔄 These READMEs should be deleted when actual migration begins"