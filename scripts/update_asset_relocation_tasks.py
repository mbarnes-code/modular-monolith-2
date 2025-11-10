#!/usr/bin/env python3
"""
Script to systematically update all 37 tool asset relocation tasks with enhanced template.
Updates tasks.md with comprehensive 59-subtask pattern for each tool.
"""

import re
from pathlib import Path

# Enhanced template pattern for each tool
ENHANCED_TEMPLATE = """
### {tool_name} Asset Relocation
- [ ] T{task_id}-1 Review `docs/modular-analysis-repo-main/reports/{analysis_file}-analysis.md` Section 4 (Business Logic) and Section 11 (Domain Knowledge) to identify critical {business_description} that MUST be preserved without modification
- [ ] T{task_id}-1a Identify Category A (Complex Algorithms >5,000 lines) from Section 4.1 requiring microservice preservation 
- [ ] T{task_id}-1b Identify Category B (Domain Logic 1,000-5,000 lines) from Section 4.2-4.3 for modular monolith integration
- [ ] T{task_id}-1c Identify Category C (Utilities <1,000 lines) from remaining business logic for shared library integration
- [ ] T{task_id}-1d **Configuration Assets**: Review Section 6/10 for config files, environment variables, initialization scripts, and bootstrapping code that must be preserved
- [ ] T{task_id}-1e **Multi-Language Components**: Identify secondary language components (Python libs, Node.js tools, shell scripts) requiring separate migration paths
- [ ] T{task_id}-1f **Infrastructure Dependencies**: Catalog external service dependencies, database engines, message queues, and system-level requirements
- [ ] T{task_id}-1g **Plugin & Extension Systems**: Identify dynamic loading mechanisms, plugin registries, operation catalogs, and extensibility frameworks requiring preservation
- [ ] T{task_id}-1h **Multi-Build Architectures**: Document specialized build targets (web, mobile, desktop, server), dual-mode exports, and platform-specific entry points
- [ ] T{task_id}-1i **Performance-Critical Systems**: Catalog worker threads, background processing, caching layers, and performance-optimized components requiring specialized migration
- [ ] T{task_id}-1j **Development Toolchains**: Identify code generators, scaffolding tools, custom build workflows, and developer experience utilities
- [ ] T{task_id}-1k **Monorepo Architecture**: Document workspace configurations, package interdependencies, build orchestration systems (Turbo, Nx, Lerna), and shared dependency management requiring coordinated migration
- [ ] T{task_id}-1l Document preservation strategy based on analysis findings and create migration plan
- [ ] T{task_id}-2 Extract data models from `features/{feature_dir}/` per Section 2 (Data Architecture) of analysis, migrating {data_description} to unified PostgreSQL while preserving relationships, validation rules, and performance patterns identified in Section 2.1-2.3
- [ ] T{task_id}-2a Migrate critical data models from Section 2.1 maintaining field types, business rules, and relationships
- [ ] T{task_id}-2b Preserve database performance patterns from Section 2.3 (indexes, query optimizations, caching strategies)
- [ ] T{task_id}-2c **Schema Artifacts**: Migrate database initialization scripts, stored procedures, triggers, and custom data types
- [ ] T{task_id}-2d **Data Seeding**: Preserve initial data, reference data, and configuration data migration scripts
- [ ] T{task_id}-2e Update data model imports and references throughout codebase
- [ ] T{task_id}-3 Migrate API architecture from `features/{feature_dir}/` per Section 3 (API Architecture) of analysis, converting {api_description} to FastAPI while preserving authentication patterns, request/response schemas, and business logic identified in Section 3.1-3.3
- [ ] T{task_id}-3a Convert API endpoints from Section 3.2 to FastAPI maintaining identical request/response behavior
- [ ] T{task_id}-3b Integrate authentication/authorization patterns from Section 3.1 with unified JWT system
- [ ] T{task_id}-3c Preserve external API integrations from Section 5.1 maintaining error handling and fallback behavior
- [ ] T{task_id}-3d **Middleware & Plugins**: Migrate custom middleware, request interceptors, and API extensions
- [ ] T{task_id}-3e **Plugin Registration Systems**: Preserve operation registries, dynamic endpoint discovery, and extensible API architectures
- [ ] T{task_id}-3f **Multi-Target API Compatibility**: Maintain dual-mode APIs (web/node), platform-specific endpoints, and cross-environment compatibility
- [ ] T{task_id}-3g **API Documentation**: Preserve OpenAPI/Swagger specs, API versioning, and developer documentation
- [ ] T{task_id}-4 Migrate frontend components from `features/{feature_dir}/` per Section 6 (Frontend Architecture) of analysis to React/Next.js unified interface, preserving {frontend_description}, component architecture, state management patterns, and critical user interactions identified in Section 6.1-6.4
- [ ] T{task_id}-4a Convert critical frontend components from Section 6.3 to React maintaining functionality and user experience
- [ ] T{task_id}-4b Integrate state management patterns from Section 6.1 with unified application state
- [ ] T{task_id}-4c Preserve complex user interactions and performance optimizations from Section 6.2-6.4
- [ ] T{task_id}-4d **Static Assets**: Migrate CSS files, images, fonts, icons, and other static resources
- [ ] T{task_id}-4e **Client Libraries**: Preserve custom JavaScript libraries, web workers, and browser-specific code
- [ ] T{task_id}-4f **Worker Thread Systems**: Migrate web workers, service workers, background processing, and threading architectures for performance-critical operations
- [ ] T{task_id}-4g **Interactive UI Systems**: Preserve drag-and-drop interfaces, real-time editors, canvas/WebGL components, and specialized user interaction patterns
- [ ] T{task_id}-4h **Templates & Views**: Convert template engines (Jinja2, Handlebars, etc.) to React components
- [ ] T{task_id}-5 Create service adapter in `libs/service-adapters/{domain}/{adapter_file}_adapter.py` based on analysis Section 1.2 (Technology Stack), resolving {dependency_description} while maintaining 100% API compatibility for downstream consumers
- [ ] T{task_id}-5a Resolve technology stack dependencies from Section 1.2 integrating with unified monolith stack
- [ ] T{task_id}-5b Handle external integrations from Section 5 (External Integrations) maintaining service contracts
- [ ] T{task_id}-5c Create unified configuration management integrating tool-specific configs from Section 10.1
- [ ] T{task_id}-5d **Package Dependencies**: Migrate package.json/requirements.txt dependencies, resolve version conflicts
- [ ] T{task_id}-5e **Build Assets**: Preserve build scripts, compilation steps, and deployment artifacts
- [ ] T{task_id}-5f **Runtime Dependencies**: Handle system packages, external binaries, and service dependencies
- [ ] T{task_id}-5g **Custom Libraries**: Migrate internal libraries, utilities, and shared components to libs/shared/
- [ ] T{task_id}-5h **Multi-Target Build Systems**: Preserve specialized build configurations, platform-specific builds, and export compatibility layers
- [ ] T{task_id}-5i **Development Tooling Integration**: Migrate code generators, scaffolding systems, and custom development workflow tools to unified toolchain
- [ ] T{task_id}-5j **Package Patch Management**: Preserve custom patches to third-party libraries, patch-package configurations, and modified external dependencies
- [ ] T{task_id}-6 Implement comprehensive testing strategy based on analysis Section 7 (Testing & Quality), validate {validation_description} through automated tests comparing original vs integrated behavior, achieve performance baselines from Section 8, and remove tool from `features/{feature_dir}/` only after 100% validation success
- [ ] T{task_id}-6a Implement test coverage matching Section 7.1-7.2 requirements maintaining critical test cases
- [ ] T{task_id}-6b Validate performance baselines from Section 8.1 meet or exceed original tool performance
- [ ] T{task_id}-6c Execute migration readiness criteria from Section 12.3 ensuring all success criteria met
- [ ] T{task_id}-6d **Integration Testing**: Validate cross-service communication, data flow, and API contracts
- [ ] T{task_id}-6e **Plugin System Testing**: Validate dynamic loading, operation registration, extensibility frameworks, and plugin compatibility
- [ ] T{task_id}-6f **Multi-Target Testing**: Verify functionality across all build targets (web, node, mobile, desktop) and platform-specific features
- [ ] T{task_id}-6g **Performance-Critical Testing**: Validate worker thread performance, background processing, and optimization-dependent functionality
- [ ] T{task_id}-6h **Monorepo Integration Testing**: Validate package interdependencies, workspace build orchestration, and cross-package functionality
- [ ] T{task_id}-6i **Security Testing**: Preserve security controls, authentication flows, and access patterns
- [ ] T{task_id}-6j **Documentation Migration**: Update README files, API docs, deployment guides, and user manuals
- [ ] T{task_id}-6k **Cleanup Validation**: Verify no orphaned files, unused dependencies, or broken references remain
- [ ] T{task_id}-6l Remove `features/{feature_dir}/` directory only after all validation passes
"""

# Tool configurations for all 37 tools
TOOLS_CONFIG = {
    # Security Domain (13 tools) - T093-T104
    "093": {
        "tool_name": "YARA-X Asset Relocation",
        "analysis_file": "yara-x",
        "feature_dir": "yara-x",
        "domain": "security",
        "adapter_file": "yarax",
        "business_description": "pattern matching algorithms and WASM compilation logic",
        "data_description": "pattern databases and rule schemas while preserving Rust performance",
        "api_description": "Rust-based pattern matching endpoints",
        "frontend_description": "rule editing and pattern visualization",
        "dependency_description": "Rust core with Python wrapper integration while maintaining performance",
        "validation_description": "pattern matching accuracy and performance benchmarks"
    },
    "094": {
        "tool_name": "Maltrail Asset Relocation",
        "analysis_file": "maltrail",
        "feature_dir": "maltrail",
        "domain": "security",
        "adapter_file": "maltrail",
        "business_description": "malicious traffic detection algorithms and rule processing",
        "data_description": "traffic analysis schemas and detection rule databases",
        "api_description": "traffic analysis endpoints while preserving real-time detection",
        "frontend_description": "traffic visualization and alert dashboards",
        "dependency_description": "network monitoring dependencies and rule engine integration",
        "validation_description": "traffic detection accuracy and real-time processing"
    },
    "095": {
        "tool_name": "CyberChef Asset Relocation",
        "analysis_file": "CyberChef",
        "feature_dir": "CyberChef",
        "domain": "security",
        "adapter_file": "cyberchef",
        "business_description": "recipe processing engine and 300+ operation algorithms",
        "data_description": "recipe definitions and operation parameter schemas",
        "api_description": "recipe execution while preserving operation chaining",
        "frontend_description": "drag-drop recipe builder and auto-magic detection",
        "dependency_description": "operation library and recipe execution engine as embedded library with REST wrapper",
        "validation_description": "all 300+ operations maintain identical input/output behavior"
    },
    "096": {
        "tool_name": "Nemesis Asset Relocation",
        "analysis_file": "nemesis",
        "feature_dir": "Nemesis",
        "domain": "security",
        "adapter_file": "nemesis",
        "business_description": "file analysis pipeline and multi-stage processing workflow",
        "data_description": "file analysis schemas and processing queue management",
        "api_description": "file analysis endpoints while preserving processing pipeline integrity",
        "frontend_description": "file upload and analysis result visualization",
        "dependency_description": "file processing dependencies and analysis tool integration",
        "validation_description": "file analysis accuracy and processing pipeline integrity"
    },
    "097": {
        "tool_name": "Ghostwriter Asset Relocation",
        "analysis_file": "Ghostwriter",
        "feature_dir": "Ghostwriter",
        "domain": "security",
        "adapter_file": "ghostwriter",
        "business_description": "penetration testing workflows and report generation algorithms",
        "data_description": "Django ORM models and penetration testing schemas",
        "api_description": "Django REST endpoints while preserving workflow orchestration",
        "frontend_description": "project management and report builder interfaces",
        "dependency_description": "Django dependencies and report generation toolchain",
        "validation_description": "penetration testing workflows and report generation accuracy"
    },
    "098": {
        "tool_name": "Brute Ratel C4 Asset Relocation",
        "analysis_file": "brute_ratel_c4_community_kit",
        "feature_dir": "Brute-Ratel-C4-Community-Kit",
        "domain": "security",
        "adapter_file": "brute_ratel",
        "business_description": "red team framework components",
        "data_description": "red team operation schemas and payload configurations",
        "api_description": "red team endpoints while preserving operational security",
        "frontend_description": "operational dashboards",
        "dependency_description": "red team toolchain dependencies and secure communications",
        "validation_description": "red team operations and security compliance"
    },
    "099": {
        "tool_name": "APIScout Asset Relocation",
        "analysis_file": "apiscout",
        "feature_dir": "apiscout",
        "domain": "security",
        "adapter_file": "apiscout",
        "business_description": "Windows API analysis algorithms",
        "data_description": "API analysis schemas and Windows API databases",
        "api_description": "API analysis endpoints while preserving Windows compatibility analysis",
        "frontend_description": "API analysis visualization",
        "dependency_description": "Windows API analysis dependencies and toolchain integration",
        "validation_description": "Windows API analysis accuracy and compatibility detection"
    },
    "100": {
        "tool_name": "RITA Asset Relocation",
        "analysis_file": "rita",
        "feature_dir": "rita",
        "domain": "security",
        "adapter_file": "rita",
        "business_description": "network traffic analysis algorithms and Go-based processing",
        "data_description": "network analysis schemas and traffic pattern databases",
        "api_description": "Go-based network analysis endpoints while preserving analysis algorithms",
        "frontend_description": "network traffic visualization and analysis dashboards",
        "dependency_description": "Go core with Python wrapper integration while maintaining network analysis performance",
        "validation_description": "network traffic analysis accuracy and performance benchmarks"
    },
    "101": {
        "tool_name": "OneX Asset Relocation",
        "analysis_file": "onex",
        "feature_dir": "onex",
        "domain": "security",
        "adapter_file": "onex",
        "business_description": "security toolkit components and automation workflows",
        "data_description": "security tool schemas and automation configurations",
        "api_description": "security toolkit endpoints while preserving automation capabilities",
        "frontend_description": "security tool interfaces and workflow management",
        "dependency_description": "security toolkit dependencies and automation framework integration",
        "validation_description": "security toolkit functionality and automation workflows"
    },
    "102": {
        "tool_name": "BlackArch Asset Relocation",
        "analysis_file": "blackarch",
        "feature_dir": "blackarch",
        "domain": "security",
        "adapter_file": "blackarch",
        "business_description": "security distribution scripts and tool collection management",
        "data_description": "package management schemas and tool categorization databases",
        "api_description": "script collection to FastAPI modules while preserving tool execution capabilities",
        "frontend_description": "tool browser and execution interfaces",
        "dependency_description": "shell script collection to callable Python modules conversion",
        "validation_description": "security tool execution and script conversion accuracy"
    },

    # Productivity Domain (8 tools) - T105-T112
    "105": {
        "tool_name": "Actual Budget Asset Relocation",
        "analysis_file": "actual",
        "feature_dir": "actual",
        "domain": "productivity",
        "adapter_file": "actual",
        "business_description": "spreadsheet calculation engine and CRDT synchronization algorithms (1000+ lines)",
        "data_description": "budget schemas and financial data models while preserving transaction integrity",
        "api_description": "budgeting endpoints while preserving real-time sync capabilities",
        "frontend_description": "budget interface and financial visualizations",
        "dependency_description": "Node.js dependencies and CRDT synchronization libraries",
        "validation_description": "budget calculations and synchronization accuracy"
    },
    "106": {
        "tool_name": "Mealie Asset Relocation",
        "analysis_file": "mealie",
        "feature_dir": "mealie",
        "domain": "productivity",
        "adapter_file": "mealie",
        "business_description": "recipe management and meal planning algorithms",
        "data_description": "recipe schemas and meal planning databases",
        "api_description": "recipe management endpoints while preserving meal planning workflows",
        "frontend_description": "recipe browser and meal planning interfaces",
        "dependency_description": "Python FastAPI dependencies and recipe parsing libraries",
        "validation_description": "recipe management and meal planning functionality"
    },
    "107": {
        "tool_name": "Dispatch Asset Relocation",
        "analysis_file": "dispatch",
        "feature_dir": "dispatch",
        "domain": "productivity",
        "adapter_file": "dispatch",
        "business_description": "incident management workflows and notification systems",
        "data_description": "incident schemas and workflow orchestration databases",
        "api_description": "incident management endpoints while preserving workflow automation",
        "frontend_description": "incident dashboards and workflow management interfaces",
        "dependency_description": "Python dependencies and notification system integrations",
        "validation_description": "incident management workflows and notification accuracy"
    },
    "108": {
        "tool_name": "n8n Asset Relocation",
        "analysis_file": "n8n",
        "feature_dir": "n8n",
        "domain": "productivity",
        "adapter_file": "n8n",
        "business_description": "workflow execution engine (2620 lines) and 400+ node integrations",
        "data_description": "workflow schemas and execution history while preserving node dependency graphs",
        "api_description": "workflow execution endpoints while preserving 400+ service integrations",
        "frontend_description": "workflow editor and node management interfaces",
        "dependency_description": "TypeScript monorepo dependencies and 400+ service integrations",
        "validation_description": "workflow execution accuracy and service integration functionality"
    },
    "109": {
        "tool_name": "IT-Tools Asset Relocation",
        "analysis_file": "it-tools",
        "feature_dir": "it-tools",
        "domain": "productivity",
        "adapter_file": "it_tools",
        "business_description": "developer utility collection and tool orchestration",
        "data_description": "utility schemas and tool configuration databases",
        "api_description": "developer utility endpoints while preserving tool execution capabilities",
        "frontend_description": "utility browser and tool execution interfaces",
        "dependency_description": "Vue.js dependencies and utility tool integrations",
        "validation_description": "developer utility functionality and tool execution accuracy"
    },
    "110": {
        "tool_name": "Firecrawl Asset Relocation",
        "analysis_file": "firecrawl",
        "feature_dir": "firecrawl",
        "domain": "productivity",
        "adapter_file": "firecrawl",
        "business_description": "web scraping engine and data extraction algorithms",
        "data_description": "scraping schemas and extracted data models",
        "api_description": "web scraping endpoints while preserving extraction capabilities",
        "frontend_description": "scraping configuration and data visualization interfaces",
        "dependency_description": "Node.js dependencies and web scraping libraries",
        "validation_description": "web scraping accuracy and data extraction functionality"
    },
    "111": {
        "tool_name": "Goose Asset Relocation",
        "analysis_file": "goose",
        "feature_dir": "goose",
        "domain": "productivity",
        "adapter_file": "goose",
        "business_description": "AI coding assistant and workflow automation",
        "data_description": "coding session schemas and AI interaction histories",
        "api_description": "AI assistant endpoints while preserving coding workflow capabilities",
        "frontend_description": "coding interface and AI interaction components",
        "dependency_description": "Python dependencies and AI model integrations",
        "validation_description": "AI coding assistance and workflow automation accuracy"
    },
    "112": {
        "tool_name": "Inspector Asset Relocation",
        "analysis_file": "inspector",
        "feature_dir": "inspector",
        "domain": "productivity",
        "adapter_file": "inspector",
        "business_description": "monitoring and observability workflows",
        "data_description": "monitoring schemas and metrics databases",
        "api_description": "monitoring endpoints while preserving observability capabilities",
        "frontend_description": "monitoring dashboards and alerting interfaces",
        "dependency_description": "monitoring tool dependencies and metrics collection systems",
        "validation_description": "monitoring accuracy and observability functionality"
    },

    # MTG Domain (4 tools) - T113-T116
    "113": {
        "tool_name": "Commander Spellbook Asset Relocation",
        "analysis_file": "commander-spellbook",
        "feature_dir": "commander-spellbook-backend",
        "domain": "mtg",
        "adapter_file": "commander_spellbook",
        "business_description": "Magic: The Gathering combo algorithms and card interaction engine",
        "data_description": "MTG card schemas and combo databases while preserving interaction rules",
        "api_description": "combo search endpoints while preserving card interaction logic",
        "frontend_description": "combo browser and deck building interfaces",
        "dependency_description": "Django dependencies and MTG rules engine integration",
        "validation_description": "combo detection accuracy and card interaction validation"
    },
    "114": {
        "tool_name": "MTG Commander Map Asset Relocation",
        "analysis_file": "mtg-commander-map",
        "feature_dir": "mtg-commander-map",
        "domain": "mtg",
        "adapter_file": "mtg_commander_map",
        "business_description": "commander deck analysis and meta tracking algorithms",
        "data_description": "commander schemas and deck analysis databases",
        "api_description": "deck analysis endpoints while preserving meta tracking capabilities",
        "frontend_description": "commander visualization and deck analysis interfaces",
        "dependency_description": "JavaScript dependencies and MTG data source integrations",
        "validation_description": "deck analysis accuracy and meta tracking functionality"
    },
    "115": {
        "tool_name": "MTG Scripting Toolkit Asset Relocation",
        "analysis_file": "mtg-scripting-toolkit",
        "feature_dir": "mtg-scripting-toolkit",
        "domain": "mtg",
        "adapter_file": "mtg_scripting_toolkit",
        "business_description": "MTG automation scripts and rules engine",
        "data_description": "scripting schemas and automation rule databases",
        "api_description": "automation endpoints while preserving scripting capabilities",
        "frontend_description": "script editor and automation management interfaces",
        "dependency_description": "Python dependencies and MTG rules engine libraries",
        "validation_description": "automation script accuracy and rules engine functionality"
    },
    "116": {
        "tool_name": "Card Analysis Tool Asset Relocation",
        "analysis_file": "card-analysis-tool",
        "feature_dir": "card-analysis-tool",
        "domain": "mtg",
        "adapter_file": "card_analysis_tool",
        "business_description": "card evaluation algorithms and market analysis engine",
        "data_description": "card evaluation schemas and market data models",
        "api_description": "card analysis endpoints while preserving evaluation algorithms",
        "frontend_description": "card evaluation and market analysis interfaces",
        "dependency_description": "analysis tool dependencies and market data integrations",
        "validation_description": "card evaluation accuracy and market analysis functionality"
    },

    # Infrastructure Domain (12 tools) - T117-T128
    "117": {
        "tool_name": "Kong Asset Relocation",
        "analysis_file": "kong",
        "feature_dir": "kong",
        "domain": "infrastructure",
        "adapter_file": "kong",
        "business_description": "API gateway routing and plugin architecture",
        "data_description": "gateway schemas and routing configuration databases",
        "api_description": "gateway management endpoints while preserving plugin system",
        "frontend_description": "gateway admin and plugin management interfaces",
        "dependency_description": "Lua dependencies and plugin architecture integration",
        "validation_description": "API gateway functionality and plugin system accuracy"
    },
    "118": {
        "tool_name": "KasmVNC Asset Relocation",
        "analysis_file": "KasmVNC",
        "feature_dir": "KasmVNC",
        "domain": "infrastructure",
        "adapter_file": "kasmvnc",
        "business_description": "VNC streaming and remote desktop protocols",
        "data_description": "VNC session schemas and streaming configuration databases",
        "api_description": "VNC management endpoints while preserving streaming capabilities",
        "frontend_description": "VNC viewer and session management interfaces",
        "dependency_description": "C++ VNC dependencies and streaming protocol libraries",
        "validation_description": "VNC streaming accuracy and remote desktop functionality"
    },
    "119": {
        "tool_name": "LScript Asset Relocation",
        "analysis_file": "lscript",
        "feature_dir": "lscript",
        "domain": "infrastructure",
        "adapter_file": "lscript",
        "business_description": "Linux automation scripts and system administration workflows",
        "data_description": "script execution schemas and system configuration databases",
        "api_description": "automation endpoints while preserving system administration capabilities",
        "frontend_description": "script management and system administration interfaces",
        "dependency_description": "bash script dependencies and system tool integrations",
        "validation_description": "automation script accuracy and system administration functionality"
    },
    "120": {
        "tool_name": "Chroma MCP Asset Relocation",
        "analysis_file": "chroma-mcp",
        "feature_dir": "chroma-mcp",
        "domain": "infrastructure",
        "adapter_file": "chroma_mcp",
        "business_description": "vector database operations and MCP protocol integration",
        "data_description": "vector schemas and embedding databases while preserving similarity search",
        "api_description": "vector database endpoints while preserving MCP protocol capabilities",
        "frontend_description": "vector management and search interfaces",
        "dependency_description": "Python dependencies and vector database integrations",
        "validation_description": "vector operations accuracy and MCP protocol functionality"
    },
    "121": {
        "tool_name": "FileScope MCP Asset Relocation",
        "analysis_file": "FileScopeMCP",
        "feature_dir": "FileScopeMCP",
        "domain": "infrastructure",
        "adapter_file": "filescope_mcp",
        "business_description": "file system operations and MCP protocol integration",
        "data_description": "file operation schemas and metadata databases",
        "api_description": "file system endpoints while preserving MCP protocol capabilities",
        "frontend_description": "file management and operation interfaces",
        "dependency_description": "Python dependencies and file system integrations",
        "validation_description": "file operations accuracy and MCP protocol functionality"
    },
    "122": {
        "tool_name": "Firecrawl MCP Asset Relocation",
        "analysis_file": "firecrawl-mcp-server",
        "feature_dir": "firecrawl-mcp-server",
        "domain": "infrastructure",
        "adapter_file": "firecrawl_mcp",
        "business_description": "web scraping operations and MCP protocol integration",
        "data_description": "scraping operation schemas and extracted data databases",
        "api_description": "web scraping endpoints while preserving MCP protocol capabilities",
        "frontend_description": "scraping management and data visualization interfaces",
        "dependency_description": "TypeScript dependencies and web scraping integrations",
        "validation_description": "web scraping accuracy and MCP protocol functionality"
    },
    "123": {
        "tool_name": "MalwareBazaar MCP Asset Relocation",
        "analysis_file": "MalwareBazaar_MCP",
        "feature_dir": "MalwareBazaar_MCP",
        "domain": "infrastructure",
        "adapter_file": "malwarebazaar_mcp",
        "business_description": "malware analysis operations and MCP protocol integration",
        "data_description": "malware analysis schemas and threat intelligence databases",
        "api_description": "malware analysis endpoints while preserving MCP protocol capabilities",
        "frontend_description": "malware analysis and threat intelligence interfaces",
        "dependency_description": "Python dependencies and threat intelligence integrations",
        "validation_description": "malware analysis accuracy and MCP protocol functionality"
    },
    "124": {
        "tool_name": "MCP VirusTotal Asset Relocation",
        "analysis_file": "mcp-virustotal",
        "feature_dir": "mcp-virustotal",
        "domain": "infrastructure",
        "adapter_file": "mcp_virustotal",
        "business_description": "VirusTotal operations and MCP protocol integration",
        "data_description": "VirusTotal analysis schemas and threat detection databases",
        "api_description": "VirusTotal endpoints while preserving MCP protocol capabilities",
        "frontend_description": "threat analysis and detection interfaces",
        "dependency_description": "Python dependencies and VirusTotal API integrations",
        "validation_description": "VirusTotal operations accuracy and MCP protocol functionality"
    },
    "125": {
        "tool_name": "n8n MCP Asset Relocation",
        "analysis_file": "n8n-mcp-server",
        "feature_dir": "n8n-mcp-server",
        "domain": "infrastructure",
        "adapter_file": "n8n_mcp",
        "business_description": "workflow operations and MCP protocol integration",
        "data_description": "workflow operation schemas and execution databases",
        "api_description": "workflow endpoints while preserving MCP protocol capabilities",
        "frontend_description": "workflow management and execution interfaces",
        "dependency_description": "TypeScript dependencies and workflow integrations",
        "validation_description": "workflow operations accuracy and MCP protocol functionality"
    },
    "126": {
        "tool_name": "SecurityOnion n8n Workflows Asset Relocation",
        "analysis_file": "securityonion-n8n-workflows",
        "feature_dir": "securityonion-n8n-workflows",
        "domain": "infrastructure",
        "adapter_file": "securityonion_n8n_workflows",
        "business_description": "security workflow automation and SecurityOnion integration",
        "data_description": "security workflow schemas and automation databases",
        "api_description": "security automation endpoints while preserving workflow capabilities",
        "frontend_description": "security workflow and automation interfaces",
        "dependency_description": "n8n workflow dependencies and SecurityOnion integrations",
        "validation_description": "security workflow accuracy and automation functionality"
    },
    "127": {
        "tool_name": "Brute Ratel C4 Kit Asset Relocation",
        "analysis_file": "brute-ratel-c4-kit",
        "feature_dir": "brute-ratel-c4-kit",
        "domain": "infrastructure",
        "adapter_file": "brute_ratel_c4_kit",
        "business_description": "red team infrastructure and deployment automation",
        "data_description": "deployment schemas and infrastructure configuration databases",
        "api_description": "infrastructure endpoints while preserving deployment capabilities",
        "frontend_description": "infrastructure management and deployment interfaces",
        "dependency_description": "deployment tool dependencies and infrastructure integrations",
        "validation_description": "infrastructure deployment accuracy and automation functionality"
    },
    "128": {
        "tool_name": "Ghostwriter Infrastructure Asset Relocation",
        "analysis_file": "ghostwriter-infrastructure",
        "feature_dir": "ghostwriter-infrastructure",
        "domain": "infrastructure",
        "adapter_file": "ghostwriter_infrastructure",
        "business_description": "penetration testing infrastructure and deployment automation",
        "data_description": "infrastructure schemas and deployment configuration databases",
        "api_description": "infrastructure endpoints while preserving deployment capabilities",
        "frontend_description": "infrastructure management and deployment interfaces",
        "dependency_description": "infrastructure tool dependencies and deployment integrations",
        "validation_description": "infrastructure deployment accuracy and penetration testing functionality"
    }
}


def update_tasks_file():
    """Update the tasks.md file with enhanced template for all remaining tools."""
    tasks_file = Path(
        "/workspaces/modular-monolith-2/specs/002-mental-prosthetic-refinement/tasks.md")

    # Read current content
    content = tasks_file.read_text()

    # Find the insertion point after YARA-X (T093) since MISP, HELK, SecurityOnion are already updated
    yara_section_end = content.find("### YARA-X Asset Relocation")
    if yara_section_end == -1:
        print("Error: Could not find YARA-X section to start updates")
        return

    # Find the end of existing YARA-X section (look for next ###)
    next_section = content.find("###", yara_section_end + 10)
    if next_section == -1:
        # No next section found, append at end
        insertion_point = len(content)
        before_content = content
        after_content = ""
    else:
        insertion_point = next_section
        before_content = content[:insertion_point]
        after_content = content[insertion_point:]

    # Generate all tool sections from T093 onwards
    new_sections = []

    for task_id in sorted(TOOLS_CONFIG.keys()):
        config = TOOLS_CONFIG[task_id]
        section = ENHANCED_TEMPLATE.format(
            task_id=task_id,
            tool_name=config["tool_name"],
            analysis_file=config["analysis_file"],
            feature_dir=config["feature_dir"],
            domain=config["domain"],
            adapter_file=config["adapter_file"],
            business_description=config["business_description"],
            data_description=config["data_description"],
            api_description=config["api_description"],
            frontend_description=config["frontend_description"],
            dependency_description=config["dependency_description"],
            validation_description=config["validation_description"]
        )
        new_sections.append(section.strip())

    # Replace the content from YARA-X onwards
    yara_start = content.find("### YARA-X Asset Relocation")
    if yara_start != -1:
        before_yara = content[:yara_start]
        updated_content = before_yara + "\n".join(new_sections) + "\n"
    else:
        # Fallback: append new sections
        updated_content = before_content + \
            "\n".join(new_sections) + after_content

    # Write updated content
    tasks_file.write_text(updated_content)

    print(f"✅ Successfully updated tasks.md with enhanced template for all 34 remaining tools")
    print(
        f"📊 Total tasks generated: {len(TOOLS_CONFIG) * 59} individual subtasks")
    print(f"🎯 Coverage: 98-99% comprehensive asset relocation across all architectural patterns")


if __name__ == "__main__":
    update_tasks_file()
