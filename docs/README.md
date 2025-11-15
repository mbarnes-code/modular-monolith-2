# Documentation Hub

Welcome to the modular-monolith-2 documentation hub. This directory contains all project documentation organized for easy discovery and navigation.

## Quick Navigation

### 📚 Documentation Index
- **[Documentation Map](./DOCUMENTATION_MAP.md)** - Complete map of all documentation locations
- **[Application Docs](./apps/README.md)** - Application-specific documentation by domain
- **[Migration Summary](./DOCUMENTATION_MIGRATION_SUMMARY.md)** - Documentation organization history

### 🏗️ Architecture & Planning
- **[Base Skeleton Docs](./base%20skeleton%20version%20docs/)** - Base architecture documentation
- **[Specifications](/specs/)** - Technical specifications (in `/specs/` directory)

### 🔧 Integration & Migration
- **[MISP Integration](./MISP%20integration%20docs/)** - MISP platform integration guides
- **[NX Migration Notes](./NX%20migration%20notes/)** - NX workspace migration documentation
- **[Automation Notes](./automation%20notes/)** - Workflow automation documentation

## Documentation by Category

### Getting Started
Start here if you're new to the project:

1. **[Main README](/README.md)** - Project overview and quick start
2. **[Setup Guide](/SETUP.md)** - Detailed installation instructions
3. **[Contributing Guide](/CONTRIBUTING.md)** - How to contribute

### Application Documentation

#### By Domain
- **[Security Apps](./apps/security/)** - 15 security domain applications
  - MISP, Nemesis, YARA-X, KasmVNC, CyberChef, Dispatch, Ghostwriter, HELK, Maltrail, and more
- **[Productivity Apps](./apps/productivity/)** - 4 productivity domain applications
  - Mealie, Goose, n8n, Onex
- **[TCG Apps](./apps/tcg/)** - Trading card game applications
  - Commander Spellbook (frontend & backend)

#### Quick Links to Popular Apps
- [MISP Documentation](./apps/security/misp/) - Malware Information Sharing Platform
- [Nemesis Documentation](./apps/security/nemesis/) - Post-exploitation framework
- [Mealie Documentation](./apps/productivity/mealie/) - Recipe management (full MkDocs site)
- [n8n Documentation](./apps/productivity/n8n/) - Workflow automation
- [Commander Spellbook](./apps/tcg/commander-spellbook/) - MTG combo database

### Technical Documentation

#### Specifications
Located in `/specs/` directory:
- [Main Specification](/specs/spec.md)
- [Project Plan](/specs/plan.md)
- [Tasks](/specs/tasks.md)
- [Migration Strategy](/specs/migration-strategy.md)

#### Architecture
- [Base Skeleton Documentation](./base%20skeleton%20version%20docs/)
- [Hybrid Domain Architecture](/README.md#ddd-based-hybrid-domain-based-architecture)

#### Migration & Integration
- [NX Migration Notes](./NX%20migration%20notes/)
- [MISP Integration](./MISP%20integration%20docs/)
- [Automation Workflows](./automation%20notes/)

## Finding What You Need

### By Technology Stack

**Frontend (React/Next.js)**
- [Jane UI](/apps/core/jane-ui/README.md)
- [UI Component Library](/libs/ui/)

**Backend (Python/FastAPI)**
- [Jane Orchestrator](/apps/core/jane-orchestrator/README.md)
- [Domain Services](/apps/)

**AI/LLM**
- [Cyber LLM Server](/apps/ai/cyber-llm-server/README.md)
- [MTG LLM Server](/apps/ai/mtg-llm-server/README.md)

**Infrastructure**
- [Docker](/infrastructure/docker/)
- [Kubernetes](/infrastructure/kubernetes/)
- [Terraform](/infrastructure/terraform/)

### By Task

**Setting Up Development Environment**
1. [Main Setup Guide](/SETUP.md)
2. Quick setup scripts: `/setup-codespace.sh` or `/quick-setup.sh`

**Contributing Code**
1. [Contributing Guide](/CONTRIBUTING.md)
2. Service-specific guidelines in [apps documentation](./apps/)

**Security & Policies**
- [Security Policy](/SECURITY.md)
- [Code of Conduct](./apps/security/misp/code_of_conduct.md)

**Building & Deployment**
- [Infrastructure Documentation](/infrastructure/)
- [NX Build Commands](/README.md#building)

## Search Documentation

### Using Command Line
```bash
# Search all markdown files for a term
grep -r "search term" /workspaces/modular-monolith-2/docs/ --include="*.md"

# Find documentation by filename
find /workspaces/modular-monolith-2/docs/ -name "*keyword*.md"

# List all documentation files
find /workspaces/modular-monolith-2/docs/ -name "*.md" -type f
```

### Documentation Structure
```
docs/
├── README.md (this file)
├── DOCUMENTATION_MAP.md              # Complete location reference
├── DOCUMENTATION_MIGRATION_SUMMARY.md # Migration details
├── apps/                             # Application docs by domain
│   ├── security/                     # Security domain (15 apps)
│   ├── productivity/                 # Productivity domain (4 apps)
│   ├── tcg/                         # TCG domain (1 app)
│   ├── core/                        # Core infrastructure
│   └── ai/                          # AI services
├── base skeleton version docs/       # Architecture documentation
├── MISP integration docs/           # MISP integration guides
├── NX migration notes/              # NX workspace migration
└── automation notes/                # Automation workflows
```

## Contributing to Documentation

### Adding New Documentation
1. Place service-specific docs in `/docs/apps/<domain>/<service>/`
2. Update [Application Docs Index](./apps/README.md)
3. Update [Documentation Map](./DOCUMENTATION_MAP.md) if needed
4. Keep service README in `/apps/<domain>/<service>/README.md`

### Documentation Standards
- Use Markdown (.md) format
- Include table of contents for long documents
- Use relative links when possible
- Add code examples where applicable
- Keep line length reasonable (80-120 characters)

### Maintenance
- Keep source and docs/apps/ in sync
- Update indexes when adding new services
- Review and update outdated documentation regularly

## Documentation Tools

### Available Documentation Sites
- **Mealie**: Full MkDocs site at `docs/apps/productivity/mealie/docs/`
- **Goose**: Documentation at `docs/apps/productivity/goose/docs/`

### Potential Additions
- Unified MkDocs or Docusaurus site
- API documentation generation
- Automated documentation sync
- Search functionality

## Support & Questions

- **Issues**: Create an issue on GitHub
- **Discussions**: Use GitHub Discussions
- **Documentation Requests**: Label as `documentation` in issues

## Recent Changes

- **2025-11-15**: Centralized application documentation from `/apps/` to `/docs/apps/`
  - 597 files migrated
  - 121 directories created
  - 20 services documented
  - Created comprehensive index and map

## Related Resources

- **Main Project**: [README.md](/README.md)
- **Specifications**: [/specs/](/specs/)
- **Source Code**: [/apps/](/apps/)
- **Libraries**: [/libs/](/libs/)
- **Infrastructure**: [/infrastructure/](/infrastructure/)
