# Documentation Map

This document provides a comprehensive map of all documentation locations within the monorepo.

## Root-Level Documentation

### Project Documentation
- **README.md** - Main project overview and quick start guide
- **CONTRIBUTING.md** - Contribution guidelines
- **SECURITY.md** - Security policies and reporting
- **SETUP.md** - Detailed setup instructions
- **CLAUDE.md** - Claude AI assistant guidelines
- **PNPM_MIGRATION.md** - PNPM migration guide
- **MAKEFILE_UPDATES.md** - Makefile usage and updates

### Documentation Directories

#### `/docs/`
Project-wide documentation and guides

- **automation notes/** - Automation and workflow documentation
- **base skeleton version docs/** - Base architecture documentation
- **MISP integration docs/** - MISP integration guides
- **NX migration notes/** - NX workspace migration documentation
- **apps/** - Application-specific documentation (organized by domain)

#### `/specs/`
Technical specifications and implementation plans

- **spec.md** - Main specification document
- **plan.md** - Project plan
- **tasks.md** - Task tracking
- **migration-strategy.md** - Migration strategy
- **001-mental-prosthetic-platform/** - Platform specifications
- Additional specification directories (002-xxx, 003-xxx, etc.)

## Application Documentation

All application-specific documentation has been centralized in `/docs/apps/` organized by domain:

### Security Domain (`/docs/apps/security/`)

| Application | Documentation Location | Key Contents |
|------------|----------------------|--------------|
| MISP | `security/misp/` | API docs, coding standards, security policies, roadmap |
| Nemesis | `security/nemesis/` | Framework docs, NX integration guides |
| YARA-X | `security/yara-x/` | Rule engine documentation |
| KasmVNC | `security/kasmvnc/` | Building guides, debugging, RFB protocol specs |
| APIScout | `security/apiscout/` | API analysis tool documentation |
| Meterpreter | `security/meterpreter/` | Payload documentation |
| HELK | `security/helk/` | Hunting ELK stack documentation |
| BlackArch | `security/blackarch/` | Linux security tools documentation |
| Dispatch | `security/dispatch/` | Incident management, plugin documentation |
| Maltrail | `security/maltrail/` | Malware detection documentation |
| CyberChef | `security/cyberchef/` | Data operations tool documentation |
| Ghostwriter | `security/ghostwriter/` | Penetration testing reporting |
| HexStrike | `security/hexstrike/` | AI-powered security tools |
| Software Forensic Kit | `security/software-forensic-kit/` | Digital forensics documentation |
| Security Service | `security/security-service/` | Domain aggregation service |

### Productivity Domain (`/docs/apps/productivity/`)

| Application | Documentation Location | Key Contents |
|------------|----------------------|--------------|
| Mealie | `productivity/mealie/` | Complete MkDocs site, contributor guides |
| Goose | `productivity/goose/` | AI coding assistant documentation |
| Onex | `productivity/onex/` | Exploitation toolkit documentation |
| n8n | `productivity/n8n/` | Workflow automation, ESLint plugin, i18n, testing |

### TCG Domain (`/docs/apps/tcg/`)

| Application | Documentation Location | Key Contents |
|------------|----------------------|--------------|
| Commander Spellbook | `tcg/commander-spellbook/` | Backend API docs, frontend development guides |

## Service README Files

Each service maintains its own README.md in its application directory:

### Security Services
- `/apps/security/misp-service/README.md`
- `/apps/security/nemesis-service/README.md`
- `/apps/security/yara-x-service/README.md`
- `/apps/security/kasmvnc-service/README.md`
- `/apps/security/cyberchef-service/README.md`
- `/apps/security/dispatch-service/README.md`
- `/apps/security/ghostwriter-service/README.md`
- `/apps/security/helk-service/README.md`
- `/apps/security/maltrail-service/README.md`
- And more...

### Productivity Services
- `/apps/productivity/mealie-service/README.md`
- `/apps/productivity/n8n-service/README.md`
- `/apps/productivity/actual-service/README.md`
- `/apps/productivity/firecrawl-service/README.md`
- `/apps/productivity/goose-service/README.md`
- `/apps/productivity/inspector-service/README.md`
- And more...

### TCG Services
- `/apps/tcg/commander-spellbook-backend/README.md`
- `/apps/tcg/commander-spellbook-site/README.md`
- `/apps/tcg/mtg-service/README.md`
- And more...

### Core Services
- `/apps/core/jane-ui/README.md`
- `/apps/core/jane-orchestrator/README.md`
- `/apps/core/infrastructure-service/README.md`

### AI Services
- `/apps/ai/cyber-llm-server/README.md`
- `/apps/ai/mtg-llm-server/README.md`
- `/apps/ai/infrastructure-llm-server/README.md`

## Library Documentation

Libraries maintain their documentation within their respective directories:

- `/libs/shared/` - Shared utilities and types
- `/libs/ui/` - UI component library
- `/libs/service-adapters/` - Service integration adapters
- `/libs/firecrawl-core/` - Firecrawl core functionality
- `/libs/mtg-scripting-toolkit/` - MTG scripting utilities
- And more...

## Development Documentation

### Scripts
- `/scripts/` - Build and utility scripts (many have inline documentation)

### Infrastructure
- `/infrastructure/docker/` - Docker configurations
- `/infrastructure/kubernetes/` - Kubernetes manifests
- `/infrastructure/terraform/` - Terraform IaC

## Finding Documentation

### By Topic

**Getting Started**
- Start with: `/README.md`
- Setup: `/SETUP.md` or quick scripts: `setup-codespace.sh`, `quick-setup.sh`

**Contributing**
- Guide: `/CONTRIBUTING.md`
- Code standards: Service-specific CODINGSTYLE.md in `/docs/apps/`

**Security**
- Policies: `/SECURITY.md`
- Service-specific: `/docs/apps/security/<service>/SECURITY.md`

**Architecture**
- Specifications: `/specs/`
- Base architecture: `/docs/base skeleton version docs/`

**Service Usage**
- Individual service READMEs in `/apps/<domain>/<service>/README.md`
- Detailed docs in `/docs/apps/<domain>/<service>/`

### By Format

**Markdown Files**
- Scattered throughout the repository
- Primary locations: `/docs/`, `/specs/`, service directories

**MkDocs Sites**
- Mealie: `/docs/apps/productivity/mealie/docs/` (mkdocs.yml)

**API Documentation**
- MISP API: `/docs/apps/security/misp/api-docs/`
- OpenAPI specs: Various service directories

## Documentation Maintenance Guidelines

1. **Service READMEs**: Keep in service root (`/apps/<domain>/<service>/README.md`)
2. **Detailed Docs**: Extract to `/docs/apps/<domain>/<service>/`
3. **Project Docs**: Keep in `/docs/` root
4. **Specifications**: Keep in `/specs/`
5. **Update This Map**: When adding new documentation locations

## Quick Reference Commands

```bash
# Find all markdown files
find . -name "*.md" -not -path "*/node_modules/*" -not -path "*/.venv/*"

# Find documentation directories
find . -type d -name "docs" -not -path "*/node_modules/*"

# Search documentation content
grep -r "search term" docs/ --include="*.md"
```

## Notes

- Documentation has been **copied** (not moved) to preserve source integrity
- Original documentation remains in service directories for backwards compatibility
- `node_modules/` documentation has been excluded from centralization
- API documentation and generated docs remain in their original locations
