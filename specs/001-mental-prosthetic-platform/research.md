# Research: Mental Prosthetic Platform

**Date**: 2025-10-18  
**Purpose**: Resolve technical clarifications and establish integration strategy

## Analysis Documentation Review

### Project Inventory from Features Directory

Based on features/ directory scan, the following 37 projects need integration:

**Security Domain** (13 projects):
- Brute-Ratel-C4-Community-Kit, HELK, MISP, Nemesis, apiscout, blackarch, hexstrike-ai, lscript, maltrail, meterpreter, onex, rita, securityonion, software-forensic-kit, yara-x

**Productivity Domain** (8 projects):
- actual, dispatch, firecrawl, goose, mealie, n8n, inspector, it-tools

**MTG Domain** (3 projects):
- commander-spellbook-backend, commander-spellbook-site, mtg-commander-map, mtg-scripting-toolkit

**Infrastructure/Integration** (13 projects):
- CyberChef, FileScopeMCP, Ghostwriter, KasmVNC, kong, chroma-mcp, firecrawl-mcp-server, MalwareBazaar_MCP, mcp-virustotal, n8n-mcp-server, securityonion-n8n-workflows

## Research Findings

### Decision: Vector Database for LLM Embeddings
**Chosen**: Chroma DB (already available in chroma-mcp project)
**Rationale**: Chroma is lightweight, Python-native, and already present in the features/ directory as chroma-mcp. It integrates well with vLLM servers and supports the vector operations needed for AI context management.
**Alternatives considered**: Pinecone (cloud-based, not suitable for local deployment), Weaviate (more complex setup), FAISS (lower-level, requires more custom code)

### Decision: Integration Strategy Based on Analysis Documentation
**Chosen**: Domain-based incremental integration with dependency analysis
**Rationale**: After reviewing the consolidated analysis documents, projects fall into clear domain boundaries (security, productivity, MTG, infrastructure). The modular-analysis-repo-main contains technical debt analysis and business logic analysis that indicates shared dependencies and integration complexity.
**Alternatives considered**: All-at-once migration (too risky), project-by-project (ignores domain synergies), technology-stack-based (breaks functional boundaries)

### Decision: MCP (Model Context Protocol) Integration Pattern
**Chosen**: Unified MCP server within jane-orchestrator
**Rationale**: Multiple projects use MCP pattern (chroma-mcp, firecrawl-mcp-server, MalwareBazaar_MCP, mcp-virustotal, n8n-mcp-server). Consolidating into a single MCP implementation within the orchestrator reduces complexity while maintaining protocol benefits.
**Alternatives considered**: Multiple MCP servers (increased complexity), no MCP (loses existing integration benefits), external MCP proxy (additional infrastructure)

### Decision: Service Adapter Architecture
**Chosen**: Domain-specific service adapters in libs/service-adapters/
**Rationale**: This preserves business logic from each project while providing unified interfaces. Each adapter handles the specific integration patterns for its domain (REST APIs, database connections, file processing, etc.).
**Alternatives considered**: Direct integration (loses modularity), wrapper services (violates no-wrapper requirement), microservices (contrary to modular monolith goal)

### Decision: Progressive Web App (PWA) Support
**Chosen**: Next.js PWA capabilities for offline support
**Rationale**: Executive function support needs to work during connectivity issues. PWA provides offline capabilities while maintaining the web-based approach.
**Alternatives considered**: Native mobile app (future phase), desktop app (Electron - too resource-heavy), web-only (no offline support)

### Decision: Authentication and Session Management
**Chosen**: JWT with refresh tokens, unified session across all tools
**Rationale**: Supports the requirement for single sign-on across all integrated tools. JWT allows for stateless authentication across the distributed services within the monolith.
**Alternatives considered**: Session cookies (doesn't scale across services), OAuth only (too complex for single-user), no authentication (insecure for remote access)

## Integration Sequence

Based on analysis documentation and dependency mapping:

1. **Foundation Phase**: Core infrastructure and shared libraries
2. **Productivity Phase**: Start with high-impact, low-complexity tools (actual, mealie, n8n)
3. **Security Phase**: Integrate security tools with established patterns
4. **MTG Phase**: Add MTG-specific tools
5. **Infrastructure Phase**: Finalize MCP integrations and advanced tools
6. **AI Enhancement Phase**: Complete LLM integration across all domains

## Technical Decisions

### Database Schema Strategy
- PostgreSQL as primary database with domain-specific schemas
- Chroma DB for vector embeddings and AI context
- Synology NAS integration for automated backups

### API Design Patterns
- OpenAPI specifications for all service adapters
- WebSocket connections for real-time AI communication
- REST APIs for standard CRUD operations
- GraphQL consideration for complex data relationships (deferred to implementation)

### Error Handling and Recovery
- Circuit breaker pattern for service adapters
- Graceful degradation with clear status indicators
- Automated recovery workflows using health checks and service restart policies