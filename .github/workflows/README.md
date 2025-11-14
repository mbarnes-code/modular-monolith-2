# Automated Refactoring Workflow

This GitHub Actions workflow (`refactor.yml`) provides automated refactoring capabilities using the enhanced TypeScript AST tools generalized from the n8n CLI.

## 🚀 How to Use

### 1. **Trigger the Workflow**

Go to the **Actions** tab in GitHub and select **"Automated Refactoring"**, then click **"Run workflow"**.

### 2. **Configure Options**

- **Refactor Type**: Choose what to refactor
  - `logging` - Extract logging into shared library ✅ **READY**  
  - `imports` - Organize imports (coming soon)
  - `unused-code` - Remove dead code (coming soon)
  - `type-annotations` - Add TypeScript types (coming soon)

- **Dry Run**: 
  - `true` - Analyze only, no changes made (RECOMMENDED for first run)
  - `false` - Actually perform the refactoring

- **Target Scope**:
  - `affected` - Only files changed since last commit (RECOMMENDED)
  - `all` - Entire codebase
  - `apps-only` - Only application code
  - `libs-only` - Only library code

- **Create PR**: 
  - `true` - Automatically create a pull request (RECOMMENDED)
  - `false` - Apply changes directly to current branch

## 🧪 **Recommended First Run**

```
Refactor Type: logging
Dry Run: true
Target Scope: affected  
Create PR: true
```

This will analyze your code and show you what would be changed without making any actual modifications.

## ✅ **For Real Execution**

Once you're satisfied with the dry run results:

```
Refactor Type: logging
Dry Run: false
Target Scope: affected
Create PR: true
```

## 🛡️ **Safety Features**

- **Pre-flight Validation**: Checks if tools are available and patterns exist
- **Post-refactoring Testing**: Runs lints and tests to ensure no breakage
- **Automatic Rollback**: If anything fails, no changes are applied
- **Pull Request Review**: Changes go through normal PR review process
- **Complete Audit Trail**: Every change is tracked and documented

## 📊 **What Gets Generated**

### Logging Refactoring Output:
- **Shared Library**: `libs/shared/logging/` with complete logging infrastructure
- **Updated Imports**: All files automatically updated to use new shared logger
- **Executive Function Accommodations**: ADHD-friendly patterns built in
- **Domain-Specific Loggers**: Performance-optimized for each domain

### Example Changes:

**Before:**
```typescript
console.log('Processing request...');
console.error('Failed:', error);
```

**After:**
```typescript
import { logger } from '@shared/logging';

logger.info('Processing request...');
logger.error('Failed:', error);
```

## 🎯 **Expected Results**

The workflow will:

1. **Scan** your codebase for logging patterns
2. **Generate** a comprehensive shared logging library
3. **Refactor** all detected logging calls automatically  
4. **Validate** that nothing is broken
5. **Create PR** for your review (if enabled)

## 🔧 **Technical Details**

### Tools Used:
- **TypeScript AST Tools**: `libs/intelligence/code/` (2,000+ lines)
- **ts-morph**: Safe AST manipulation library
- **Enhanced from n8n CLI**: Proven, battle-tested patterns
- **Executive Function Support**: ADHD-friendly design patterns

### Performance:
- **Parallel processing** for large codebases
- **Incremental analysis** (only affected files when possible)
- **Batch operations** for efficiency
- **Error isolation** (one file failure doesn't break others)

## 🆘 **Troubleshooting**

### Workflow Fails at Pre-flight:
- Check that `libs/intelligence/code/logging-refactor.ts` exists
- Verify Node.js and npm dependencies are installed

### No Patterns Found:
- Your codebase may already be optimized!
- Try changing scope to `all` to scan entire codebase

### Post-refactoring Tests Fail:
- The workflow automatically rolls back changes
- Check the logs to see which tests failed
- May indicate edge cases that need manual attention

### Created PR has Issues:
- Review the generated code in the PR
- Complete rollback is available if needed
- Provide feedback to improve the tools

## 🎊 **Success Indicators**

✅ **Successful Run Shows:**
- Number of files processed
- Number of patterns refactored  
- All tests pass
- PR created for review
- Zero breaking changes

## 💡 **Tips**

- **Start with dry run** to see what will be changed
- **Use `affected` scope** for faster processing
- **Review the PR carefully** before merging
- **Executive function benefits** are built into the generated code
- **Complete rollback** is always available if needed

---

🤖 **This workflow uses the Enhanced TypeScript AST Tools**  
Generalized from n8n CLI with AI-driven improvements  
Zero Dependencies Promise: Maintained