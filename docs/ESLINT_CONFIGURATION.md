# ESLint Configuration Strategy

## Overview

This workspace uses a comprehensive root-level `.eslintrc.json` file that serves as the baseline configuration for all applications and libraries. The configuration consolidates common patterns and best practices found across the workspace.

## Root Configuration (/.eslintrc.json)

The root ESLint configuration provides:

### Core Features
- **TypeScript Support**: Full TypeScript parsing and rules
- **React Support**: React and React Hooks rules for JSX applications
- **Import Management**: Organized import ordering and duplicate detection
- **Accessibility**: Basic a11y rules for frontend applications
- **Multi-Environment**: Browser, Node.js, and Jest globals
- **NX Integration**: Dependency checking for JSON files

### Rule Categories

#### TypeScript Rules
- `@typescript-eslint/no-explicit-any`: Warn on `any` usage
- `@typescript-eslint/no-unused-vars`: Error on unused variables (with ignore patterns for `_` prefixed)
- `@typescript-eslint/prefer-const`: Enforce const over let when possible
- `@typescript-eslint/no-non-null-assertion`: Warn on non-null assertions

#### General JavaScript Rules
- `no-console`: Warn on console usage (overridden per project as needed)
- `no-debugger`: Error on debugger statements
- `prefer-const`: Enforce const usage
- `no-var`: Error on var usage
- `curly`: Require braces for all control statements
- `eqeqeq`: Require strict equality

#### Import Rules
- `import/order`: Alphabetical ordering with group separation
- `import/no-duplicates`: Prevent duplicate imports
- `import/no-unresolved`: Error on unresolved imports

#### React Rules (when applicable)
- Modern React 17+ settings (no need for React import)
- React Hooks rules for proper hook usage
- Disabled prop-types (using TypeScript instead)

#### Accessibility Rules
- Basic ARIA and semantic HTML validation
- Alt text and role requirements

### File-Specific Overrides

The configuration includes targeted overrides for:

1. **TypeScript Files** (*.ts, *.tsx)
   - Enhanced TypeScript-specific rules

2. **JavaScript Files** (*.js, *.jsx)
   - Relaxed TypeScript rules
   - Allow CommonJS patterns

3. **Test Files** (*.test.*, *.spec.*, test/, tests/, __tests__/)
   - Allow `any` types
   - Allow unused variables
   - Allow console statements
   - Allow debugger statements

4. **Configuration Files** (*.config.*, etc.)
   - Allow require() usage
   - Allow console statements
   - Allow unresolved imports

5. **Next.js Files** (pages/, app/, next.config.*)
   - Extend Next.js core web vitals
   - Disable specific Next.js rules as needed

6. **Backend/Node.js Files** (server/, api/, backend/, services/)
   - Allow console statements
   - Node.js-specific environment

## Project-Specific Configurations

Each app/library extends from the root configuration and adds minimal overrides:

### Standard Extension Pattern
```json
{
  "extends": ["../../.eslintrc.json"],
  "ignorePatterns": ["!**/*"],
  "rules": {
    // Project-specific overrides only
  }
}
```

### Common Overrides by Project Type

#### Frontend Applications (React/Next.js)
```json
{
  "extends": ["../../.eslintrc.json"],
  "ignorePatterns": ["!**/*"],
  "rules": {
    "no-console": "warn"  // Allow console for development
  }
}
```

#### Backend Services
```json
{
  "extends": ["../../.eslintrc.json"],
  "ignorePatterns": ["!**/*"],
  "rules": {
    "no-console": "off"  // Allow console logging
  }
}
```

#### Security Services (Stricter Rules)
```json
{
  "extends": ["../../.eslintrc.json"],
  "ignorePatterns": ["!**/*"],
  "rules": {
    "@typescript-eslint/no-explicit-any": "error",  // Stricter than root
    "@typescript-eslint/no-unused-vars": "error",
    "no-console": "off"
  }
}
```

#### Libraries
```json
{
  "extends": ["../../.eslintrc.json"],
  "ignorePatterns": ["!**/*"]
  // Usually no additional rules needed
}
```

## Migration Status

The following configurations have been updated to use the new baseline:

### Updated Configurations
- ✅ `apps/core/jane-ui/.eslintrc.json` - Next.js app with console warnings
- ✅ `apps/productivity/mealie-service/.eslintrc.json` - Service with console allowed
- ✅ `apps/security/helk-service/.eslintrc.json` - Security service with strict rules
- ✅ `apps/productivity/inspector-service/.eslintrc.json` - Standard service
- ✅ `apps/productivity/n8n-service/.eslintrc.json` - Service with console allowed
- ✅ `libs/firecrawl-ui/.eslintrc.json` - Standard library
- ✅ `features/firecrawl-mcp-server/.eslintrc.json` - MCP server with relaxed rules
- ✅ `features/n8n-mcp-server/.eslintrc.json` - MCP server with relaxed rules

### Legacy Configurations (Still Need Migration)
These configurations have their own complete rulesets and should be updated to extend from root:

- `features/it-tools/.eslintrc.cjs` - Vue/Vite project with custom rules
- `apps/security/kasmvnc-service/src/kasmweb/.eslintrc` - Legacy JavaScript rules
- `apps/security/dispatch-service/src/services/static/dispatch/.eslintrc.js` - Vue.js with custom rules

## Usage Instructions

### For New Projects
1. Create minimal `.eslintrc.json` extending from root:
```json
{
  "extends": ["../../.eslintrc.json"],
  "ignorePatterns": ["!**/*"]
}
```

2. Add project-specific rule overrides only if needed
3. Test with: `npx eslint src --ext .ts,.tsx,.js,.jsx`

### For Existing Projects
1. Compare current rules with root configuration
2. Remove duplicate rules that match root defaults
3. Keep only project-specific overrides
4. Test to ensure no regressions

### ESLint v9 Compatibility Note
This workspace currently uses ESLint v9, which prefers flat configuration format (`eslint.config.js`). However, due to compatibility issues with the existing NX setup and various plugins, we're maintaining the legacy `.eslintrc.json` format with the `ESLINT_USE_FLAT_CONFIG=false` environment variable when needed.

To use the configuration:
```bash
# For legacy mode (current setup)
ESLINT_USE_FLAT_CONFIG=false npx eslint src --ext .ts,.tsx,.js,.jsx

# Or add to package.json scripts:
"lint": "ESLINT_USE_FLAT_CONFIG=false eslint src --ext .ts,.tsx,.js,.jsx --max-warnings=0"
```

## Benefits Achieved

1. **Consistency**: All projects now follow the same baseline rules
2. **Maintainability**: Rules are defined once in the root configuration
3. **Flexibility**: Projects can override rules as needed for their specific requirements
4. **Performance**: Reduced configuration overhead and faster linting
5. **Best Practices**: Incorporates TypeScript, React, and accessibility best practices

## Future Improvements

1. **Flat Config Migration**: When NX and plugins fully support ESLint v9 flat config
2. **Additional Plugins**: Consider adding more specialized rules (security, performance)
3. **CI Integration**: Enforce consistent linting across all projects in CI/CD
4. **IDE Integration**: Ensure consistent experience across different IDEs

## Troubleshooting

### Common Issues

1. **"Cannot extend from ../../.eslintrc.json"**
   - Ensure the relative path is correct for your project structure
   - Verify the root `.eslintrc.json` file exists

2. **"Plugin not found"**
   - Install missing plugins: `npm install --save-dev <plugin-name>`
   - Check that all required plugins are listed in root `package.json`

3. **TypeScript parsing errors**
   - Ensure `@typescript-eslint/parser` and `@typescript-eslint/eslint-plugin` are installed
   - Check that your `tsconfig.json` is properly configured

4. **React rules not working**
   - Verify `eslint-plugin-react` and `eslint-plugin-react-hooks` are installed
   - Ensure React version is detected properly in settings

### Debug Commands

```bash
# Check which config is being used
ESLINT_USE_FLAT_CONFIG=false npx eslint --debug src

# Print effective configuration for a file
ESLINT_USE_FLAT_CONFIG=false npx eslint --print-config src/index.ts

# Lint with verbose output
ESLINT_USE_FLAT_CONFIG=false npx eslint src --format=verbose
```