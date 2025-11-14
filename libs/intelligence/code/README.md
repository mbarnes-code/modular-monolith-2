# TypeScript Code Intelligence Library

Enhanced TypeScript AST manipulation and code intelligence tools, generalized from the n8n Node CLI for universal TypeScript project support.

## Features

### 🎯 **Core Capabilities**
- **Project-agnostic AST operations** - Works with any TypeScript project
- **Type-safe property updates** - Modify classes, interfaces, and objects safely
- **Intelligent code generation** - AI-enhanced code creation with context awareness
- **Batch processing** - Process multiple files efficiently with rollback capabilities
- **Cross-file refactoring** - Safely modify related code across multiple files

### 🧠 **Executive Function Accommodations**
- **ADHD-friendly patterns** - Reduces cognitive load with consistent structures
- **Progressive disclosure** - Break complex operations into manageable steps
- **Consistent naming enforcement** - Automatic code style consistency
- **Complexity analysis** - Identifies overly complex code patterns

### 🔒 **Security-First Development**
- **Security pattern detection** - Identifies potential vulnerabilities
- **Secure coding suggestions** - Recommends security best practices
- **Input validation patterns** - Helps implement proper validation
- **Authentication handling** - Specialized auth system manipulation

### 🔄 **Cross-Domain Intelligence**
- **Multi-domain support** - Security, Productivity, MTG, Infrastructure
- **Pattern sharing** - Reuse successful patterns across domains
- **Context-aware operations** - Understands different project types
- **Integration helpers** - Smooth connections between different tools

## Installation

```bash
npm install @modular-monolith/code-intelligence
```

## Quick Start

### Basic AST Operations

```typescript
import { loadSourceFile, updateStringProperty, updateClassDeclaration } from '@modular-monolith/code-intelligence';

// Load and modify a TypeScript file
const sourceFile = loadSourceFile('./src/MyClass.ts');

// Update a class
const classDecl = sourceFile.getClass('MyClass');
updateClassDeclaration({
  sourceFile,
  className: 'MyClass',
  updates: {
    name: 'EnhancedClass',
    properties: { version: '2.0.0' },
    methods: [{ 
      name: 'newMethod', 
      body: 'return "enhanced";',
      returnType: 'string' 
    }]
  }
});

// Save changes
await sourceFile.save();
```

### React Component Generation

```typescript
import { updateReactComponent } from '@modular-monolith/code-intelligence';

// Enhance a React component with accessibility and type safety
const component = updateReactComponent({
  componentPath: './src/UserProfile.tsx',
  componentName: 'UserProfile',
  props: {
    userId: 'string',
    onEdit: '() => void',
    disabled: 'boolean'
  },
  accessibility: {
    ariaLabel: 'User profile editor',
    role: 'main',
    keyboardNavigation: true
  }
});
```

### API Service Configuration

```typescript
import { updateApiServiceClass } from '@modular-monolith/code-intelligence';

// Update an API service class
const service = updateApiServiceClass({
  servicePath: './src/services/GitHubService.ts',
  className: 'GitHubService',
  baseUrl: 'https://api.github.com',
  apiConfig: {
    displayName: 'GitHub API Service',
    description: 'Enhanced GitHub integration',
    version: '2.0.0',
    authentication: 'oauth2'
  }
});
```

### Executive Function Accommodations

```typescript
import { applyExecutiveFunctionAccommodations } from '@modular-monolith/code-intelligence';

// Apply ADHD-friendly code patterns
const enhanced = applyExecutiveFunctionAccommodations({
  filePath: './src/ComplexClass.ts',
  accommodations: {
    maxFunctionComplexity: 10,
    maxParameterCount: 4,
    enforceConsistentNaming: true,
    enhanceReadability: true
  }
});
```

### Security Best Practices

```typescript
import { applySecurityBestPractices } from '@modular-monolith/code-intelligence';

// Apply security enhancements
const secured = applySecurityBestPractices({
  filePath: './src/AuthService.ts',
  securityLevel: 'strict'
});
```

### Batch Processing

```typescript
import { batchProcess } from '@modular-monolith/code-intelligence';

// Process multiple files efficiently
const result = await batchProcess({
  files: ['./src/**/*.ts'],
  operations: [
    (sourceFile) => {
      // Add consistent error handling
      sourceFile.getClasses().forEach(cls => {
        cls.getMethods().forEach(method => {
          // Add try-catch blocks where missing
        });
      });
    }
  ],
  parallelism: 4
});

console.log(`Processed ${result.processed} files with ${result.errors.length} errors`);
```

### Code Analysis

```typescript
import { analyzeCodePatterns } from '@modular-monolith/code-intelligence';

// Analyze code quality and get AI-enhanced suggestions
const sourceFile = loadSourceFile('./src/MyClass.ts');
const analysis = analyzeCodePatterns(sourceFile);

console.log(`Complexity: ${analysis.complexity}`);
console.log(`Security Score: ${analysis.securityScore}`);
console.log(`Executive Function Score: ${analysis.executiveFunctionScore}`);
console.log(`Accessibility Score: ${analysis.accessibilityScore}`);
```

### Template-Based Code Generation

```typescript
import { generateFromTemplate } from '@modular-monolith/code-intelligence';

const template = {
  name: 'fastapi-endpoint',
  category: 'service',
  template: `
@router.{{method}}("{{path}}")
async def {{functionName}}({{parameters}}):
    """{{description}}"""
    try:
        # Implementation here
        return {"success": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
`,
  variables: {
    method: { type: 'string', required: true },
    path: { type: 'string', required: true },
    functionName: { type: 'string', required: true },
    description: { type: 'string', required: true }
  },
  fileExtension: 'py'
};

const result = generateFromTemplate({
  template,
  variables: {
    method: 'post',
    path: '/users',
    functionName: 'create_user',
    description: 'Create a new user account'
  },
  outputPath: './src/endpoints/users.py'
});
```

## Advanced Usage

### Custom Refactoring Operations

```typescript
import { batchRefactor, RefactoringOperation } from '@modular-monolith/code-intelligence';

// Define custom refactoring operations
const modernizeOperation: RefactoringOperation = {
  name: 'modernize-syntax',
  description: 'Update to modern TypeScript syntax',
  patterns: [
    { nodeType: 'FunctionDeclaration' }
  ],
  transform: (sourceFile, matches) => {
    // Convert function declarations to arrow functions where appropriate
    return true;
  },
  safetyCheck: (sourceFile) => {
    // Ensure the transformation is safe
    return true;
  }
};

// Apply refactoring with rollback capability
const { success, rollbackPlan } = await batchRefactor({
  files: ['./src/**/*.ts'],
  operations: [modernizeOperation]
});
```

### AI-Enhanced Code Generation

```typescript
import { generateCodeWithAI } from '@modular-monolith/code-intelligence';

// Generate code using AI assistance
const aiConfig = {
  enableSuggestions: true,
  enableAutoFix: true,
  modelPreferences: {
    codeGeneration: 'claude-3-5-sonnet',
    analysis: 'claude-3-5-sonnet'
  },
  contextWindowSize: 8000,
  maxTokens: 2000,
  temperature: 0.3
};

const generatedCode = await generateCodeWithAI({
  template: reactComponentTemplate,
  variables: { componentName: 'DataTable', features: ['sorting', 'filtering'] },
  aiConfig
});
```

### Cross-Domain Pattern Analysis

```typescript
import { applyCrossDomainPatterns } from '@modular-monolith/code-intelligence';

// Apply patterns that work across multiple domains
const enhanced = applyCrossDomainPatterns({
  filePath: './src/SecurityService.ts',
  targetDomains: ['security', 'productivity'],
  patterns: ['error-handling', 'logging', 'validation']
});
```

## Configuration

### Project Configuration

```typescript
import type { ProjectConfig } from '@modular-monolith/code-intelligence';

const config: ProjectConfig = {
  tsConfigPath: './tsconfig.json',
  skipDependencies: true,
  useInMemory: false,
  compilerOptions: {
    target: 'ES2020',
    module: 'ESNext',
    strict: true
  },
  includePatterns: ['src/**/*.ts', 'src/**/*.tsx'],
  excludePatterns: ['**/*.test.ts', 'dist/**/*']
};
```

### Security Configuration

```typescript
import type { SecurityAnalysisConfig } from '@modular-monolith/code-intelligence';

const securityConfig: SecurityAnalysisConfig = {
  enableVulnerabilityScanning: true,
  severityThreshold: 'medium',
  rules: [
    {
      id: 'no-hardcoded-secrets',
      name: 'No Hardcoded Secrets',
      pattern: /password.*=.*["'].*["']/,
      severity: 'high',
      category: 'data-leak'
    }
  ]
};
```

### Executive Function Configuration

```typescript
import type { ExecutiveFunctionConfig } from '@modular-monolith/code-intelligence';

const efConfig: ExecutiveFunctionConfig = {
  maxComplexityPerFunction: 10,
  maxParametersPerFunction: 5,
  maxMethodsPerClass: 10,
  enforceNamingConventions: true,
  requireFunctionDocs: true,
  maxNestingDepth: 4,
  enforceSingleResponsibility: true
};
```

## Integration with Mental Prosthetic Platform

This library is designed as part of the 37-tool Mental Prosthetic Platform, providing code intelligence across:

- **Security Domain** (13 tools): MISP, HELK, SecurityOnion, Maltrail, etc.
- **Productivity Domain** (8 tools): n8n, Mealie, Dispatch, Actual Budget, etc.
- **MTG Domain** (4 tools): Commander Spellbook, MTG Commander Map, etc.
- **Infrastructure Domain** (12 tools): Kong, Ghostwriter, KasmVNC, etc.

### Zero Dependencies Promise

- ✅ All existing applications continue working without this service
- ✅ Code intelligence is purely additive - enhances capabilities when available
- ✅ Graceful degradation ensures applications work even if this service fails
- ✅ No breaking changes to existing codebases

### Executive Function Accommodations

- **UI Response Times**: <200ms for enhanced ADHD-friendly responsiveness
- **Consistent Patterns**: Unified interface design across all integrated tools
- **Cognitive Load Reduction**: Break complex operations into manageable steps
- **WCAG 2.1 AA Compliance**: Enhanced focus indicators and accessibility

## API Reference

### Core Functions

#### `loadSourceFile(path: string, config?: ProjectConfig): SourceFile`
Load a single TypeScript source file for manipulation.

#### `updateStringProperty(options: UpdateStringPropertyOptions): boolean`
Update string properties in objects or classes with type safety.

#### `updateClassDeclaration(options: UpdateClassOptions): ClassDeclaration | null`
Comprehensively update class declarations with new properties, methods, and inheritance.

#### `analyzeCodePatterns(sourceFile: SourceFile): CodeAnalysisResult`
Analyze code for quality metrics, security issues, and improvement opportunities.

#### `batchProcess(config: BatchProcessingConfig): Promise<BatchProcessingResult>`
Process multiple files efficiently with parallel execution and error handling.

### Domain Operations

#### `updateApiServiceClass(options: ApiServiceOptions): SourceFile`
Update API service classes with configuration, endpoints, and authentication.

#### `updateReactComponent(options: ReactComponentOptions): SourceFile`
Enhance React components with props, hooks, and accessibility features.

#### `applyExecutiveFunctionAccommodations(options: AccommodationOptions): SourceFile`
Apply ADHD-friendly code patterns automatically.

#### `applySecurityBestPractices(options: SecurityOptions): SourceFile`
Apply security enhancements and vulnerability fixes.

### Advanced Operations

#### `batchRefactor(options: BatchRefactorOptions): Promise<RefactorResult>`
Apply multiple refactoring operations with rollback capabilities.

#### `generateFromTemplate(options: TemplateOptions): GenerationResult`
Generate code from templates with variable substitution.

#### `generateCodeWithAI(options: AIGenerationOptions): Promise<string>`
Use AI to generate context-aware code.

## Contributing

We welcome contributions! Please see our [Contributing Guide](../../CONTRIBUTING.md) for details.

### Development Setup

```bash
# Install dependencies
npm install

# Run tests
npm test

# Run tests with coverage
npm run test:coverage

# Build the library
npm run build

# Lint and format
npm run lint:fix
npm run format
```

## License

MIT License - see [LICENSE](../../../LICENSE) for details.

## Related Projects

- [n8n Node CLI](https://github.com/n8n-io/n8n/tree/master/packages/@n8n/node-cli) - Original inspiration
- [ts-morph](https://github.com/dsherret/ts-morph) - Core AST manipulation library
- [Mental Prosthetic Platform](../../README.md) - Parent project

## Support

- 📖 [Documentation](./docs/)
- 🐛 [Issue Tracker](https://github.com/mbarnes-code/modular-monolith-2/issues)
- 💬 [Discussions](https://github.com/mbarnes-code/modular-monolith-2/discussions)
- 📧 [Email Support](mailto:support@mentalprosthetic.dev)