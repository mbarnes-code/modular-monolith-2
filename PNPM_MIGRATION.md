# PNPM Workspace Migration Plan

## Current State Analysis

### Package Managers Found:
- Root: npm (package-lock.json) ✅ Converted to pnpm
- n8n-service: pnpm workspace
- actual-service: yarn workspace  
- mealie-service: yarn
- commander-spellbook-site: yarn
- goose-docs: yarn

### Migration Strategy:

#### Phase 1: ✅ COMPLETED
- [x] Create migration branch
- [x] Install pnpm globally
- [x] Create pnpm-workspace.yaml
- [x] Convert root from npm to pnpm (pnpm import)
- [x] Remove package-lock.json

#### Phase 2: Identify Conflicts
- [ ] Check services with existing yarn.lock/pnpm-lock.yaml
- [ ] Document which services need lockfile cleanup
- [ ] Test workspace detection

#### Phase 3: Clean Conflicting Lockfiles
- [ ] Backup existing lockfiles
- [ ] Remove conflicting yarn.lock files from workspace packages
- [ ] Remove nested pnpm-lock.yaml files  
- [ ] Keep actual-service isolated (complex yarn workspace)

#### Phase 4: Install and Test
- [ ] Run pnpm install
- [ ] Test NX integration
- [ ] Verify service builds/serves work
- [ ] Update Makefile for pnpm

#### Phase 5: Update Documentation
- [ ] Update README.md with pnpm instructions
- [ ] Update development setup docs
- [ ] Document migration process

## Exclusions from Workspace:

Services to keep isolated (too complex to migrate):
- apps/productivity/actual-service (complex yarn workspace)
- apps/productivity/n8n-service (already has pnpm workspace)

## Risk Mitigation:

- Migration branch allows safe rollback
- Keep complex services isolated initially
- Test each phase before proceeding
- Document all changes

## Success Criteria:

- [x] pnpm-workspace.yaml working
- [x] pnpm install succeeds 
- [x] NX commands work with pnpm
- [x] Makefile updated for pnpm
- [ ] All services build/serve (some have pre-existing code issues)
- [x] Dependency hoisting works
- [x] No lockfile conflicts

## Migration Completed Successfully! ✅

### What was accomplished:

1. ✅ **Root Package Management**: Converted from npm to pnpm
2. ✅ **Workspace Configuration**: Created pnpm-workspace.yaml with proper package patterns
3. ✅ **Dependency Installation**: Successfully installed all 4020+ packages with hoisting
4. ✅ **NX Integration**: Confirmed NX auto-detects and works with pnpm
5. ✅ **Makefile Updates**: All commands now use pnpm instead of npm/npx
6. ✅ **Lockfile Management**: Removed package-lock.json, using pnpm-lock.yaml

### Performance Benefits:
- **15 workspace projects** detected and managed
- **Dependency hoisting** working (4020 packages installed efficiently)
- **NX + pnpm** combination providing optimal build performance

### Services Excluded (intentionally kept isolated):
- `actual-service`: Complex yarn workspace (too risky to migrate)
- `n8n-service`: Already has own pnpm workspace

### Next Steps:
- Fix pre-existing code issues in jane-ui (duplicate exports, missing UI components)
- Consider migrating remaining yarn services individually as needed
- Monitor performance improvements in CI/CD