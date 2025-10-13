# Migration Notes - Monorepo Restructure

This document outlines the changes made to restructure the Jane monorepo according to the new requirements.

## Version Updates

### TypeScript
- **Previous**: 5.7.3
- **Current**: 5.8.3

### Python Packages
- **FastAPI**: 0.115.12 → 0.115.0
- **Pydantic**: 2.10.6 → 2.0.0
- **Django**: Added at 4.2.0
- **SQLAlchemy**: Added at 2.0.0

### Additional Requirements Documented
- **Rust**: 1.70+ (for specific integrations)
- **Java**: 17 LTS (for specific integrations)

## Application Renames

### Before → After
- `apps/orchestrator/` → `apps/jane-orchestrator/`
- `apps/ui/` → `apps/jane-ui/`
- `apps/llm-server-1/` → `apps/cyber-llm-server/`
- `apps/llm-server-2/` → `apps/mtg-llm-server/`
- `apps/llm-server-3/` → `apps/code-llm-server/`

## New App Structure

### jane-orchestrator
```
apps/jane-orchestrator/
├── src/
│   ├── api/          # API layer with main.py
│   ├── core/         # Core business logic
│   └── db/           # Database layer
├── tests/            # Unit tests
├── Dockerfile        # Container configuration
├── pyproject.toml    # Python project config
├── requirements.txt  # Dependencies
└── project.json      # NX configuration
```

### jane-ui
```
apps/jane-ui/
├── src/
│   ├── app/          # Next.js 15 app directory
│   ├── components/   # React components
│   └── lib/          # Utility libraries
├── public/           # Static assets
├── next.config.js
├── package.json
├── tsconfig.json
└── project.json
```

### LLM Servers (cyber, mtg, code)
```
apps/[name]-llm-server/
├── src/
│   └── server.py     # FastAPI vLLM application
├── models/           # Model configurations
├── Dockerfile        # Container configuration
├── requirements.txt  # Dependencies
├── README.md         # Documentation
└── project.json      # NX configuration
```

## New Libraries

### libs/shared/config/
Configuration management utilities for the monorepo.

### libs/service-adapters/
13 service adapter integrations:
- commander-spellbook
- misp
- nemesis
- dispatch
- ghostwriter
- n8n
- scryfall
- actual-budget
- mealie
- firecrawl
- helk
- goose
- kasmvnc

Each with:
- `src/client.py` - API client
- `src/models.py` - Data models
- `tests/` - Unit tests
- `README.md` - Documentation

### libs/ui/
Expanded UI component libraries:

#### core/
- Button
- Input
- Card
- Modal
- Table

#### domain-security/
- ThreatIndicator
- SeverityBadge
- IOCDisplay
- IncidentCard

#### domain-mtg/
- ComboCard
- ManaSymbol
- ColorIdentityBadge

#### domain-finance/ (New)
- BudgetChart
- TransactionList

#### theme/ (New)
- colors.ts
- typography.ts
- tailwind.config.js

## New Project Subdirectories

### projects/security/
11 security tool integrations:
- misp
- nemesis
- yara-x
- hexstrike-ai
- dispatch
- ghostwriter
- helk
- rita
- blackarch
- onex
- software-forensic-kit

### projects/mtg/
3 MTG-related projects:
- commander-spellbook-backend
- commander-spellbook-frontend
- mtg-scripting-toolkit

### projects/productivity/
4 productivity tools:
- n8n
- actual-budget
- mealie
- firecrawl

### projects/dev-tools/ (New)
3 developer tools:
- goose
- inspector
- it-tools

### projects/infrastructure/ (New)
1 infrastructure integration:
- kasmvnc

Each subdirectory includes README.md with integration notes.

## Port Allocation

| Service | Port | Description |
|---------|------|-------------|
| Jane UI | 3000 | Next.js frontend application |
| Jane Orchestrator | 8000 | Main FastAPI orchestrator service |
| Cyber LLM Server | 8001 | Cybersecurity LLM server (vLLM) |
| MTG LLM Server | 8002 | Magic: The Gathering LLM server (vLLM) |
| Code LLM Server | 8003 | Code generation LLM server (vLLM) |

## NX Project Count

- **Applications**: 5
- **Libraries**: 9 (was 7)
- **Total Projects**: 14

## Updated Commands

### Running Applications
```bash
# UI
npx nx serve jane-ui

# Orchestrator
npx nx serve jane-orchestrator

# LLM Servers
npx nx serve cyber-llm-server
npx nx serve mtg-llm-server
npx nx serve code-llm-server
```

### Installing Dependencies
```bash
# Node.js
npm install

# Python
pip install -r apps/jane-orchestrator/requirements.txt
pip install -r apps/cyber-llm-server/requirements.txt
pip install -r apps/mtg-llm-server/requirements.txt
pip install -r apps/code-llm-server/requirements.txt
```

## Breaking Changes

1. **Application names** have changed - update any scripts or CI/CD pipelines
2. **Python package versions** have been pinned to older versions - may require dependency updates
3. **Directory structure** has changed for apps - update any imports or references
4. **NX commands** now use new project names

## Migration Checklist

- [ ] Update CI/CD pipelines with new project names
- [ ] Update Docker Compose files with new app names
- [ ] Update Kubernetes manifests with new service names
- [ ] Update any scripts that reference old app directories
- [ ] Update environment variables if needed
- [ ] Test all applications after dependency changes
- [ ] Verify all NX targets work correctly
- [ ] Update team documentation

## Files Modified

- `package.json` - TypeScript version updated
- `README.md` - Complete structure and commands updated
- `STRUCTURE.md` - Directory tree and project details updated
- All `apps/*/requirements.txt` - Python package versions updated
- All `apps/*/project.json` - NX configurations updated with new names
- Created 14 new UI components
- Created 13 service adapter integrations
- Created 26 project README files

## Next Steps

1. Run `npm install` to install updated TypeScript version
2. Run `npm audit` to check for security vulnerabilities
3. Test each application to ensure it works with new versions
4. Update any external documentation or wikis
5. Notify team members of the changes
