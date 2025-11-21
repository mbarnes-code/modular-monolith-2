# Automated Library Hoisting 🚀

This directory contains automated scripts for safely hoisting duplicate dependencies from individual services to the root monorepo level, leveraging the existing ts-morph AST infrastructure.

## 📋 Overview

Based on the **Library Overlap Audit** and **Version Compatibility Analysis**, these scripts automatically:

1. **Hoist Phase 1 dependencies** (zero-risk) to the root `package.json`
2. **Remove duplicates** from individual service `package.json` files  
3. **Update import paths** using AST manipulation (if needed)
4. **Validate changes** with comprehensive safety checks
5. **Provide rollback** capabilities if issues are detected

## 🎯 Phase 1 Dependencies (Zero Risk)

The following dependencies are automatically hoisted:

### JavaScript Dependencies
- `axios`: 1.12.2 (security fix from 0.21.4)
- `uuid`: 13.0.0 (latest stable)
- `cors`: 2.8.5 (latest stable) 
- `lodash`: 4.17.21 (maintained version)
- `winston`: 3.18.3 (latest stable)

### TypeScript Dev Dependencies
- `@types/uuid`: 10.0.0
- `@types/cors`: 2.8.17
- `@types/lodash`: 4.17.13

## 🏗️ Affected Services

The following services contain Phase 1 dependencies and will be updated:

- `apps/jane-orchestrator` (FastAPI service)
- `apps/actual-service` (Budget management)
- `apps/cyberchef-service` (Security tools)
- `apps/firecrawl-service` (Web scraping)
- `apps/goose-service` (AI assistant)
- `apps/inspector-service` (Development tools)
- `apps/nemesis-service` (Security framework)
- `apps/maltrail-service` (Threat detection)

## 🛠️ Scripts

### `validate-hoisting.ts`
**Purpose**: Validates environment prerequisites before hoisting
**Usage**: `npm run validate-hoisting` or `make validate-hoisting`

**Checks**:
- ✅ Root `package.json` exists
- ✅ AST utilities are available and functional
- ✅ Target services exist with `package.json` files
- ✅ `pnpm` package manager is available
- ✅ NX workspace configuration is valid
- ✅ TypeScript configuration exists
- ✅ Intelligence code library is available

**Output**: Comprehensive validation report with recommendations

### `hoist-libraries.ts`
**Purpose**: Performs automated library hoisting with safety checks
**Usage**: `npm run hoist-libraries` or `make hoist-libraries`

**Features**:
- 🔍 **Safety-first**: Comprehensive validation before changes
- 🔄 **Rollback capability**: Automatic backup and restore on errors
- ⚡ **AST-powered**: Uses ts-morph for precise import path updates
- 🔧 **Parallel processing**: Efficient handling of multiple services
- 📊 **Progress tracking**: Real-time progress with executive function support
- 🎯 **Targeted updates**: Only modifies services with overlapping dependencies

## 🚀 Quick Start

### Option 1: Makefile Commands (Recommended)

```bash
# 1. Validate environment
make validate-hoisting

# 2. Preview changes (dry run)
make hoist-libraries-preview

# 3. Execute hoisting
make hoist-libraries
```

### Option 2: npm scripts

```bash
# 1. Validate environment  
npm run validate-hoisting

# 2. Preview changes
npm run hoist-libraries:preview

# 3. Execute hoisting
npm run hoist-libraries
```

### Option 3: Direct execution

```bash
# Validation
npx tsx scripts/validate-hoisting.ts

# Dry run
npx tsx scripts/hoist-libraries.ts --dry-run

# Execute with force
npx tsx scripts/hoist-libraries.ts --force
```

## 📊 Expected Results

### Before Hoisting
```
apps/actual-service/package.json:
  "axios": "0.21.4",
  "uuid": "11.1.0"

apps/goose-service/package.json:
  "axios": "1.12.2", 
  "winston": "3.14.2"

apps/inspector-service/package.json:
  "lodash": "4.17.21",
  "cors": "2.8.4"
```

### After Hoisting  
```
package.json: (root)
  "axios": "1.12.2",
  "uuid": "13.0.0", 
  "winston": "3.18.3",
  "lodash": "4.17.21",
  "cors": "2.8.5"

apps/*/package.json:
  // Phase 1 dependencies removed
  // Import statements unchanged (resolved from root)
```

## 🔧 Technical Implementation

### AST Infrastructure Integration

The hoisting scripts leverage the existing **ts-morph AST utilities** from `/libs/intelligence/code/`:

```typescript
// Uses existing AST operations
import { batchProcess, updateImports } from '../libs/intelligence/code';
import type { RefactoringOperation, BatchProcessingConfig } from '../libs/intelligence/code';

// Applies tested refactoring operations
const updateImportPathsOperation: RefactoringOperation = {
  name: 'updateImportPaths',
  transform: (sourceFile, matches) => { /* AST manipulation */ },
  safetyCheck: (sourceFile) => { /* Validation */ },
  rollback: (sourceFile) => { /* Restoration */ }
};
```

### Safety Features

1. **Pre-flight validation**: Environment and dependency checks
2. **Backup creation**: Automatic `package.json.backup` files
3. **Incremental processing**: Service-by-service with error isolation
4. **Rollback automation**: One-command restoration on failure
5. **Import validation**: AST-powered import path verification
6. **Dependency verification**: Post-install validation

### Executive Function Accommodations

- **Progress indicators**: Real-time status with percentage completion
- **Clear messaging**: Unambiguous success/error states
- **Automated validation**: Reduces cognitive load of manual checks
- **One-command execution**: Minimal steps to complete task
- **Rollback simplicity**: Single command to undo all changes

## 🔄 Rollback Process

If issues are detected during or after hoisting:

### Automatic Rollback (during execution)
```bash
# Errors detected. Rollback? (y/N)
y
✅ Restored package.json
✅ Restored apps/actual-service/package.json  
✅ Dependencies restored
```

### Manual Rollback (post-execution)
```bash
# Restore from backups
find . -name "package.json.backup" -exec sh -c 'mv "$1" "${1%.backup}"' _ {} \;

# Reinstall original dependencies
pnpm install
```

## 📈 Success Metrics

**Expected improvements after hoisting**:

- ✅ **37% reduction** in duplicate dependencies across services
- ✅ **Standardized versions** eliminate compatibility issues  
- ✅ **Security improvements** via axios 0.21.4 → 1.12.2 upgrade
- ✅ **Faster installs** due to reduced dependency tree depth
- ✅ **Simplified maintenance** with centralized dependency management

## 🚨 Troubleshooting

### Common Issues

**Issue**: `AST utilities not available`
**Solution**: Build the intelligence library first
```bash
nx build intelligence-code
```

**Issue**: `pnpm not found`  
**Solution**: Install pnpm package manager
```bash
npm install -g pnpm
```

**Issue**: `Service package.json not found`
**Solution**: Verify service paths in `AFFECTED_SERVICES` array

**Issue**: `Import resolution failed`
**Solution**: Run `pnpm install` to update dependency resolution

### Debug Mode

Add environment variable for detailed logging:
```bash
DEBUG=hoist-libraries npm run hoist-libraries
```

## 🔮 Next Steps

After successful Phase 1 hoisting, consider:

1. **Phase 2**: Medium-risk dependencies (requires testing)
   - Express 4.x → 5.x migration
   - Pydantic validation updates
   
2. **Phase 3**: High-impact dependencies (requires significant testing)
   - Major framework upgrades
   - Breaking API changes

3. **Continuous monitoring**: Set up dependency update automation
   - Dependabot configuration  
   - Automated compatibility testing
   - Regular overlap audits

## 📚 Related Documentation

- [Library Overlap Audit](../docs/LIBRARY_OVERLAP_AUDIT.md) - Initial analysis
- [Version Compatibility Analysis](../docs/VERSION_COMPATIBILITY_ANALYSIS.md) - Risk assessment  
- [AST Intelligence Library](../libs/intelligence/code/README.md) - Technical foundation
- [Constitutional Guidelines](../.github/copilot-instructions.md) - Development principles

---

*Generated by the Mental Prosthetic Platform Team*  
*Last updated: November 19, 2025*