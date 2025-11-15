# Application Documentation Index

This directory contains documentation extracted from individual applications within the monorepo, organized by domain.

## Directory Structure

```
docs/apps/
├── security/          # Security domain application documentation
├── productivity/      # Productivity domain application documentation
├── tcg/              # Trading Card Game domain application documentation
├── core/             # Core infrastructure application documentation
└── ai/               # AI server documentation
```

## Security Domain

### MISP (Malware Information Sharing Platform)
- **Location**: `security/misp/`
- **Contents**: Complete MISP documentation, API documentation, coding standards, security policies
- **Key Files**:
  - `CONTRIBUTING.md` - Contribution guidelines
  - `CODINGSTYLE.md` - Code style guide
  - `SECURITY.md` - Security policies
  - `ROADMAP.md` - Development roadmap
  - `api-docs/` - API documentation

### Nemesis (Post-Exploitation Framework)
- **Location**: `security/nemesis/`
- **Contents**: Nemesis framework documentation, NX integration guides
- **Key Files**:
  - `NX_README.md` - NX workspace integration
  - `NX_BEST_PRACTICES_README.md` - Best practices for NX usage

### YARA-X (Rule Engine)
- **Location**: `security/yara-x/`
- **Contents**: YARA-X documentation and NX integration

### KasmVNC (Remote Desktop)
- **Location**: `security/kasmvnc/`
- **Contents**: KasmVNC documentation, building guides, debugging guides
- **Key Files**:
  - `BUILDING.md` - Build instructions
  - `DEBUGGING.md` - Debugging guide
  - `ACKNOWLEDGEMENTS.md` - Credits and acknowledgements

### APIScout
- **Location**: `security/apiscout/`
- **Contents**: API Scout tool documentation

### Meterpreter
- **Location**: `security/meterpreter/`
- **Contents**: Meterpreter payload documentation

### HELK (Hunting ELK Stack)
- **Location**: `security/helk/`
- **Contents**: HELK stack documentation and assets

### BlackArch
- **Location**: `security/blackarch/`
- **Contents**: BlackArch Linux tools documentation

### Dispatch (Incident Management)
- **Location**: `security/dispatch/`
- **Contents**: Dispatch incident management documentation
- **Subdirectories**:
  - `confluence-plugin/` - Atlassian Confluence plugin docs
  - `google-plugin/` - Google integration plugin docs
- **Key Files**:
  - `MIGRATION_SUMMARY.md` - Migration notes

### Maltrail (Malware Detection)
- **Location**: `security/maltrail/`
- **Contents**: Maltrail documentation, reorganization status, security policies

### CyberChef
- **Location**: `security/cyberchef/`
- **Contents**: CyberChef documentation, security policies, code of conduct

### Ghostwriter
- **Location**: `security/ghostwriter/`
- **Contents**: Penetration testing reporting tool documentation

### HexStrike
- **Location**: `security/hexstrike/`
- **Contents**: AI-powered security tools documentation

### Software Forensic Kit
- **Location**: `security/software-forensic-kit/`
- **Contents**: Digital forensics tools documentation, NX integration guides

### Security Service
- **Location**: `security/security-service/`
- **Contents**: Security domain aggregation service documentation

## Productivity Domain

### Mealie (Recipe Management)
- **Location**: `productivity/mealie/`
- **Contents**: Complete Mealie documentation site (MkDocs)
- **Key Directories**:
  - `docs/` - Full documentation site
  - `docs/contributors/` - Contributor guides
  - `docs/news/` - News and updates

### Goose (AI Coding Assistant)
- **Location**: `productivity/goose/`
- **Contents**: Goose AI coding assistant documentation

### Onex (Exploitation Toolkit)
- **Location**: `productivity/onex/`
- **Contents**: Security exploitation toolkit documentation

### n8n (Workflow Automation)
- **Location**: `productivity/n8n/`
- **Contents**: n8n workflow automation documentation
- **Subdirectories**:
  - `eslint-plugin/` - ESLint plugin for community nodes
  - `i18n/` - Internationalization documentation
  - `playwright/` - Playwright testing documentation

## TCG Domain

### Commander Spellbook
- **Location**: `tcg/commander-spellbook/`
- **Contents**: MTG Commander Spellbook documentation
- **Subdirectories**:
  - `backend/` - Backend API documentation
  - `frontend/` - Frontend development documentation

## Notes

- **Original Locations**: Documentation has been copied (not moved) from original locations to preserve source integrity
- **README Files**: Individual service README.md files remain in their original locations within `apps/`
- **Node Modules**: Documentation from `node_modules/` has been excluded
- **Source Reference**: Each documentation folder corresponds to a service in `apps/<domain>/<service-name>/`

## Maintenance

When adding new services or updating documentation:

1. Keep service-specific README.md in the service directory (`apps/<domain>/<service>/README.md`)
2. Extract detailed documentation (guides, tutorials, API docs) to `docs/apps/<domain>/<service>/`
3. Update this index to reflect new documentation locations
4. Ensure documentation references use relative paths where possible

## Related Documentation

- **Root Documentation**: `/docs/` - Project-wide documentation
- **Specifications**: `/specs/` - Technical specifications
- **Base Skeleton**: `/docs/base skeleton version docs/` - Base architecture documentation
