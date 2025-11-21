#!/usr/bin/env tsx

/**
 * N8N Integration Phase 1: Infrastructure Setup
 * 
 * Sets up the infrastructure needed to integrate N8N's monorepo patterns:
 * 1. Turbo build system integration
 * 2. pnpm catalog system implementation  
 * 3. Scoped package structure creation
 * 4. Enhanced dependency management
 */

import { execSync } from 'child_process';
import * as fs from 'fs';
import * as path from 'path';

interface SetupResult {
  success: boolean;
  steps: Array<{ 
    name: string; 
    completed: boolean; 
    message: string; 
    details?: string[] 
  }>;
  errors: string[];
  nextSteps: string[];
}

/**
 * Setup Turbo build system integration with NX
 */
async function setupTurboBuildSystem(): Promise<{ success: boolean; message: string; details?: string[] }> {
  console.log('🏗️  Setting up Turbo build system...');
  
  try {
    // Check if turbo is already installed
    let turboInstalled = false;
    try {
      execSync('npx turbo --version', { stdio: 'ignore' });
      turboInstalled = true;
    } catch {
      // Turbo not installed
    }

    const details: string[] = [];

    // Install Turbo if not present
    if (!turboInstalled) {
      console.log('   Installing Turbo...');
      execSync('pnpm add -D turbo@latest', { stdio: 'inherit' });
      details.push('Installed Turbo build system');
    } else {
      details.push('Turbo already installed');
    }

    // Create turbo.json configuration
    const turboConfig = {
      "$schema": "https://turbo.build/schema.json",
      "globalEnv": [
        "NODE_ENV", 
        "CI", 
        "PYTHON_ENV",
        "DATABASE_URL",
        "REDIS_URL",
        "OPENAI_API_KEY",
        "ANTHROPIC_API_KEY"
      ],
      "tasks": {
        "build": {
          "dependsOn": ["^build"],
          "outputs": ["dist/**", "build/**", "__pycache__/**", ".next/**"]
        },
        "dev": {
          "cache": false,
          "persistent": true,
          "env": ["DATABASE_URL", "REDIS_URL"]
        },
        "test": {
          "dependsOn": ["^build", "build"],
          "outputs": ["coverage/**", "test-results/**", "*.xml", "junit.xml"]
        },
        "lint": {
          "dependsOn": ["^build"]
        },
        "typecheck": {
          "dependsOn": ["^typecheck", "^build"]
        },
        "format": {
          "cache": false
        },
        // Domain-specific tasks from N8N pattern
        "test:security": {
          "dependsOn": ["build"],
          "outputs": ["security-test-results/**"],
          "env": ["SECURITY_TEST_ENV"]
        },
        "test:ai": {
          "dependsOn": ["build"],
          "env": ["OPENAI_API_KEY", "ANTHROPIC_API_KEY"],
          "outputs": ["ai-test-results/**"]
        },
        "test:e2e": {
          "dependsOn": ["build"],
          "cache": false,
          "outputs": ["e2e-test-results/**", "playwright-report/**"]
        },
        // N8N-style workflow tasks
        "build:workflows": {
          "dependsOn": ["^build"],
          "outputs": ["workflow-dist/**"]
        },
        "dev:workflows": {
          "cache": false,
          "persistent": true,
          "dependsOn": ["^build"]
        }
      }
    };

    const turboJsonPath = 'turbo.json';
    if (!fs.existsSync(turboJsonPath)) {
      fs.writeFileSync(turboJsonPath, JSON.stringify(turboConfig, null, 2));
      details.push('Created turbo.json configuration');
    } else {
      details.push('turbo.json already exists, skipped creation');
    }

    // Update package.json scripts to use Turbo
    const packageJsonPath = 'package.json';
    const packageJson = JSON.parse(fs.readFileSync(packageJsonPath, 'utf-8'));
    
    // Add Turbo scripts while preserving NX scripts
    const turboScripts = {
      "turbo:build": "turbo run build",
      "turbo:dev": "turbo run dev --parallel",
      "turbo:test": "turbo run test",
      "turbo:lint": "turbo run lint",
      "turbo:typecheck": "turbo run typecheck"
    };

    let scriptsUpdated = false;
    for (const [key, value] of Object.entries(turboScripts)) {
      if (!packageJson.scripts[key]) {
        packageJson.scripts[key] = value;
        scriptsUpdated = true;
      }
    }

    if (scriptsUpdated) {
      fs.writeFileSync(packageJsonPath, JSON.stringify(packageJson, null, 2));
      details.push('Added Turbo scripts to package.json');
    }

    return { 
      success: true, 
      message: 'Turbo build system setup completed',
      details
    };

  } catch (error) {
    return { 
      success: false, 
      message: `Failed to setup Turbo: ${error}` 
    };
  }
}

/**
 * Setup pnpm catalog system
 */
async function setupPnpmCatalogSystem(): Promise<{ success: boolean; message: string; details?: string[] }> {
  console.log('📦 Setting up pnpm catalog system...');
  
  try {
    const details: string[] = [];
    const workspaceFile = 'pnpm-workspace.yaml';
    
    // Read current workspace configuration
    let workspaceContent = '';
    if (fs.existsSync(workspaceFile)) {
      workspaceContent = fs.readFileSync(workspaceFile, 'utf-8');
      details.push('Read existing pnpm-workspace.yaml');
    }

    // Create enhanced workspace configuration with catalog system
    const enhancedWorkspace = `packages:
  # Apps - all application services
  - 'apps/*'
  - 'apps/ai/*'
  - 'apps/core/*'
  - 'apps/productivity/*'
  - 'apps/security/*'
  - 'apps/tcg/*'
  
  # Support nested packages (N8N pattern)
  - 'apps/*/packages/*'
  - 'apps/*/*/packages/*'
  
  # Libraries - shared code and utilities
  - 'libs/*'
  - 'libs/@mental-prosthetic/*'
  
  # Tools and scripts
  - 'tools/*'
  
  # Special nested packages (converted from yarn)
  - 'apps/productivity/mealie-service/apps/mealie-web'
  - 'apps/productivity/mealie-service/apps/mealie-api/tests/e2e'
  
  # Exclude nested workspaces to avoid conflicts
  - '!apps/productivity/actual-service/actual-budget'
  - '!**/node_modules'
  - '!**/dist'
  - '!**/build'

# Centralized dependency catalog (N8N pattern)
catalog:
  # Core JavaScript/TypeScript dependencies
  typescript: ^5.5.0
  '@types/node': ^20.0.0
  
  # HTTP and networking
  axios: 1.12.2
  fastify: ^5.2.0
  express: ^4.21.1
  cors: 2.8.5
  
  # Utilities
  lodash: 4.17.21
  uuid: 13.0.0
  
  # Logging and monitoring
  winston: 3.18.3
  pino: ^9.5.0
  
  # Date and time
  date-fns: 2.30.0
  luxon: 3.4.4
  
  # Validation and parsing
  zod: 3.25.67
  joi: ^17.13.3
  
  # Authentication and security
  jsonwebtoken: 9.0.2
  bcrypt: ^5.1.0
  
  # Database
  prisma: ^6.1.0
  '@prisma/client': ^6.1.0
  
  # Testing
  jest: ^29.0.0
  vitest: ^3.1.3
  '@vitest/coverage-v8': 3.2.4
  playwright: ^1.49.0
  
  # Build tools
  turbo: ^2.5.4
  esbuild: ^0.25.0
  vite: ^6.0.0
  webpack: ^5.96.1
  
  # Development tools
  eslint: ^9.35.0
  prettier: ^3.6.2
  tsx: ^4.20.6

# Domain-specific catalogs (N8N frontend pattern)
catalogs:
  security:
    # Security-specific dependencies
    '@misp/api': ^2.4.0
    yara: ^4.5.0
    node-clamav: ^0.8.0
    helmet: ^8.0.0
    rate-limiter-flexible: ^5.0.3
    
  productivity:
    # Productivity tool dependencies
    '@actual/api': ^24.12.0
    '@n8n/workflow': ^1.116.0
    bull: ^4.16.4
    agenda: ^5.0.0
    
  mtg:
    # MTG-specific dependencies
    scryfall-client: ^0.24.8
    mtgsdk: ^1.5.1
    '@mtg/rules-engine': ^1.0.0
    
  ai:
    # AI and ML dependencies
    '@langchain/core': 0.3.68
    '@langchain/openai': 0.6.7
    '@langchain/anthropic': 0.3.26
    openai: ^4.0.0
    '@anthropic-ai/sdk': ^0.29.0
    chromadb: ^1.9.2
    
  frontend:
    # Frontend-specific dependencies
    react: ^19.1.0
    '@types/react': ^19.1.8
    next: ^15.5.2
    vue: ^3.5.13
    '@vue/test-utils': ^2.4.6
    tailwindcss: ^3.4.14
`;

    // Write enhanced workspace file
    fs.writeFileSync(workspaceFile, enhancedWorkspace);
    details.push('Created enhanced pnpm-workspace.yaml with catalog system');

    // Verify pnpm supports catalogs
    try {
      execSync('pnpm --version', { stdio: 'ignore' });
      const pnpmVersion = execSync('pnpm --version', { encoding: 'utf-8' }).trim();
      if (parseFloat(pnpmVersion) >= 8.0) {
        details.push(`pnpm ${pnpmVersion} supports catalog system`);
      } else {
        details.push(`pnpm ${pnpmVersion} might not fully support catalogs, consider upgrading`);
      }
    } catch (error) {
      details.push('Could not verify pnpm version');
    }

    return {
      success: true,
      message: 'pnpm catalog system setup completed',
      details
    };

  } catch (error) {
    return {
      success: false,
      message: `Failed to setup pnpm catalog system: ${error}`
    };
  }
}

/**
 * Create scoped package structure
 */
async function createScopedPackageStructure(): Promise<{ success: boolean; message: string; details?: string[] }> {
  console.log('🏗️  Creating scoped package structure...');
  
  try {
    const details: string[] = [];
    
    // Create @mental-prosthetic scoped packages structure (following N8N's @n8n pattern)
    const scopedPackages = [
      'libs/@mental-prosthetic/core',
      'libs/@mental-prosthetic/security-api', 
      'libs/@mental-prosthetic/productivity-api',
      'libs/@mental-prosthetic/mtg-api',
      'libs/@mental-prosthetic/ai-common',
      'libs/@mental-prosthetic/ui-components',
      'libs/@mental-prosthetic/testing-utils',
      'libs/@mental-prosthetic/workflow-engine',
      'libs/@mental-prosthetic/auth-common'
    ];

    for (const packagePath of scopedPackages) {
      if (!fs.existsSync(packagePath)) {
        fs.mkdirSync(packagePath, { recursive: true });
        
        // Create basic package.json for each scoped package
        const packageName = `@mental-prosthetic/${path.basename(packagePath)}`;
        const basePackageJson = {
          name: packageName,
          version: "0.1.0",
          private: true,
          description: `Mental Prosthetic Platform - ${path.basename(packagePath)} package`,
          main: "dist/index.js",
          types: "dist/index.d.ts",
          scripts: {
            build: "tsc",
            dev: "tsc --watch",
            clean: "rimraf dist",
            typecheck: "tsc --noEmit"
          },
          dependencies: {},
          devDependencies: {
            typescript: "catalog:",
            "@types/node": "catalog:",
            rimraf: "catalog:"
          }
        };

        const packageJsonPath = path.join(packagePath, 'package.json');
        fs.writeFileSync(packageJsonPath, JSON.stringify(basePackageJson, null, 2));
        
        // Create basic TypeScript config
        const tsConfig = {
          extends: "../../../tsconfig.base.json",
          compilerOptions: {
            outDir: "./dist",
            rootDir: "./src"
          },
          include: ["src/**/*"],
          exclude: ["node_modules", "dist"]
        };
        
        const tsConfigPath = path.join(packagePath, 'tsconfig.json');
        fs.writeFileSync(tsConfigPath, JSON.stringify(tsConfig, null, 2));
        
        // Create src directory and index file
        const srcDir = path.join(packagePath, 'src');
        fs.mkdirSync(srcDir, { recursive: true });
        
        const indexContent = `/**
 * ${packageName}
 * 
 * Mental Prosthetic Platform - ${path.basename(packagePath)} package
 */

export * from './types';

// Package-specific exports will be added here
`;
        
        fs.writeFileSync(path.join(srcDir, 'index.ts'), indexContent);
        
        // Create types file
        const typesContent = `/**
 * Type definitions for ${packageName}
 */

// Package-specific types will be defined here
export interface ${path.basename(packagePath).replace(/-./g, (match) => match[1].toUpperCase())}Config {
  // Configuration interface
}
`;
        
        fs.writeFileSync(path.join(srcDir, 'types.ts'), typesContent);
        
        details.push(`Created ${packageName} package structure`);
      } else {
        details.push(`${packagePath} already exists, skipped`);
      }
    }

    // Create nested package structure for apps (N8N pattern)
    const appPackageAreas = [
      'apps/core/packages',
      'apps/security/packages', 
      'apps/productivity/packages',
      'apps/ai/packages'
    ];

    for (const packageArea of appPackageAreas) {
      if (!fs.existsSync(packageArea)) {
        fs.mkdirSync(packageArea, { recursive: true });
        
        // Create README explaining the structure
        const readmeContent = `# ${path.basename(path.dirname(packageArea))} Packages

This directory contains domain-specific packages following the N8N monorepo pattern.

## Structure

Each package in this directory should be a focused, reusable module that:

1. Has a clear, single responsibility
2. Follows the Mental Prosthetic Platform's constitutional principles
3. Provides executive function accommodations
4. Maintains high code quality standards

## Creating New Packages

To create a new package:

1. Create a new directory with a descriptive name
2. Add package.json with appropriate dependencies using catalog system
3. Follow TypeScript and testing standards
4. Document public APIs comprehensively

## Examples

\`\`\`
${packageArea}/
├── auth-middleware/     # Authentication middleware
├── api-gateway/         # API gateway utilities
├── websocket-server/    # WebSocket server components
└── event-processing/    # Event processing utilities
\`\`\`
`;
        
        fs.writeFileSync(path.join(packageArea, 'README.md'), readmeContent);
        details.push(`Created ${packageArea} with documentation`);
      }
    }

    return {
      success: true,
      message: 'Scoped package structure created successfully',
      details
    };

  } catch (error) {
    return {
      success: false,
      message: `Failed to create scoped package structure: ${error}`
    };
  }
}

/**
 * Update NX configuration for hybrid system
 */
async function updateNXConfiguration(): Promise<{ success: boolean; message: string; details?: string[] }> {
  console.log('⚙️  Updating NX configuration for hybrid build system...');
  
  try {
    const details: string[] = [];
    const nxJsonPath = 'nx.json';
    
    if (fs.existsSync(nxJsonPath)) {
      const nxConfig = JSON.parse(fs.readFileSync(nxJsonPath, 'utf-8'));
      
      // Add support for scoped packages and Turbo integration
      nxConfig.workspaceLayout = {
        ...nxConfig.workspaceLayout,
        appsDir: 'apps',
        libsDir: 'libs'
      };

      // Add default project configuration for scoped packages
      nxConfig.generators = {
        ...nxConfig.generators,
        '@nx/typescript:library': {
          buildable: true,
          publishable: false,
          importPath: '@mental-prosthetic/{name}'
        }
      };

      // Update target defaults to work with Turbo
      nxConfig.targetDefaults = {
        ...nxConfig.targetDefaults,
        build: {
          cache: true,
          dependsOn: ['^build'],
          inputs: ['production', '^production'],
          outputs: ['{workspaceRoot}/dist/{projectName}', '{projectRoot}/dist']
        },
        test: {
          cache: true,
          inputs: ['default', '^production', '{workspaceRoot}/jest.preset.js'],
          outputs: ['{workspaceRoot}/coverage/{projectName}']
        },
        lint: {
          cache: true,
          inputs: ['default', '{workspaceRoot}/.eslintrc.json', '{workspaceRoot}/.eslintignore']
        }
      };

      fs.writeFileSync(nxJsonPath, JSON.stringify(nxConfig, null, 2));
      details.push('Updated nx.json for hybrid build system');
    } else {
      details.push('nx.json not found, skipped NX configuration update');
    }

    return {
      success: true,
      message: 'NX configuration updated for hybrid system',
      details
    };

  } catch (error) {
    return {
      success: false,
      message: `Failed to update NX configuration: ${error}`
    };
  }
}

/**
 * Create initial workflow engine structure (N8N integration preparation)
 */
async function createWorkflowEngineStructure(): Promise<{ success: boolean; message: string; details?: string[] }> {
  console.log('🔄 Creating workflow engine structure...');
  
  try {
    const details: string[] = [];
    const workflowEngineDir = 'libs/@mental-prosthetic/workflow-engine/src';
    
    if (fs.existsSync(workflowEngineDir)) {
      // Create core workflow engine files
      const coreFiles = [
        {
          name: 'workflow.ts',
          content: `/**
 * Core workflow definitions
 * Inspired by N8N's workflow engine
 */

export interface WorkflowNode {
  id: string;
  type: string;
  parameters: Record<string, any>;
  position: { x: number; y: number };
}

export interface WorkflowConnection {
  source: string;
  target: string;
  sourcePort?: string;
  targetPort?: string;
}

export interface Workflow {
  id: string;
  name: string;
  description?: string;
  nodes: WorkflowNode[];
  connections: WorkflowConnection[];
  settings: WorkflowSettings;
}

export interface WorkflowSettings {
  executionOrder: 'v0' | 'v1';
  saveManualExecutions: boolean;
  callerPolicy: 'workflowsFromSameOwner' | 'workflowsFromAList' | 'any';
  timezone: string;
}
`
        },
        {
          name: 'executor.ts',
          content: `/**
 * Workflow execution engine
 * Core execution logic for Mental Prosthetic workflows
 */

import type { Workflow, WorkflowNode } from './workflow';

export interface ExecutionContext {
  workflowId: string;
  userId?: string;
  domain: 'security' | 'productivity' | 'mtg' | 'infrastructure';
  environment: 'development' | 'staging' | 'production';
}

export interface ExecutionResult {
  success: boolean;
  executionId: string;
  startTime: Date;
  endTime: Date;
  nodeResults: Record<string, any>;
  error?: string;
}

export class WorkflowExecutor {
  async execute(workflow: Workflow, context: ExecutionContext): Promise<ExecutionResult> {
    // Implementation will integrate with existing services
    // following the Mental Prosthetic Platform's patterns
    
    return {
      success: true,
      executionId: \`exec_\${Date.now()}\`,
      startTime: new Date(),
      endTime: new Date(),
      nodeResults: {}
    };
  }
}
`
        },
        {
          name: 'nodes/index.ts',
          content: `/**
 * Node type definitions for Mental Prosthetic Platform workflows
 * Inspired by N8N's node system
 */

export * from './security-nodes';
export * from './productivity-nodes';
export * from './mtg-nodes';
export * from './core-nodes';
`
        },
        {
          name: 'nodes/core-nodes.ts',
          content: `/**
 * Core workflow nodes
 */

export const CORE_NODES = {
  START: 'mp.core.start',
  END: 'mp.core.end',
  CONDITION: 'mp.core.condition',
  LOOP: 'mp.core.loop',
  HTTP_REQUEST: 'mp.core.httpRequest',
  WEBHOOK: 'mp.core.webhook'
} as const;
`
        }
      ];

      for (const file of coreFiles) {
        const filePath = path.join(workflowEngineDir, file.name);
        const fileDir = path.dirname(filePath);
        
        if (!fs.existsSync(fileDir)) {
          fs.mkdirSync(fileDir, { recursive: true });
        }
        
        fs.writeFileSync(filePath, file.content);
        details.push(`Created ${file.name}`);
      }

      details.push('Workflow engine structure created with N8N-inspired architecture');
    } else {
      details.push('Workflow engine directory not found, skipped structure creation');
    }

    return {
      success: true,
      message: 'Workflow engine structure created',
      details
    };

  } catch (error) {
    return {
      success: false,
      message: `Failed to create workflow engine structure: ${error}`
    };
  }
}

/**
 * Main setup function
 */
async function main(): Promise<SetupResult> {
  console.log('🚀 N8N Integration Phase 1: Infrastructure Setup\n');
  console.log('================================================\n');

  const result: SetupResult = {
    success: false,
    steps: [],
    errors: [],
    nextSteps: []
  };

  // Step 1: Setup Turbo build system
  const turboResult = await setupTurboBuildSystem();
  result.steps.push({
    name: 'Setup Turbo Build System',
    completed: turboResult.success,
    message: turboResult.message,
    details: turboResult.details
  });
  if (!turboResult.success) {
    result.errors.push(turboResult.message);
  }

  // Step 2: Setup pnpm catalog system
  const catalogResult = await setupPnpmCatalogSystem();
  result.steps.push({
    name: 'Setup pnpm Catalog System',
    completed: catalogResult.success,
    message: catalogResult.message,
    details: catalogResult.details
  });
  if (!catalogResult.success) {
    result.errors.push(catalogResult.message);
  }

  // Step 3: Create scoped package structure
  const scopedResult = await createScopedPackageStructure();
  result.steps.push({
    name: 'Create Scoped Package Structure',
    completed: scopedResult.success,
    message: scopedResult.message,
    details: scopedResult.details
  });
  if (!scopedResult.success) {
    result.errors.push(scopedResult.message);
  }

  // Step 4: Update NX configuration
  const nxResult = await updateNXConfiguration();
  result.steps.push({
    name: 'Update NX Configuration',
    completed: nxResult.success,
    message: nxResult.message,
    details: nxResult.details
  });
  if (!nxResult.success) {
    result.errors.push(nxResult.message);
  }

  // Step 5: Create workflow engine structure
  const workflowResult = await createWorkflowEngineStructure();
  result.steps.push({
    name: 'Create Workflow Engine Structure',
    completed: workflowResult.success,
    message: workflowResult.message,
    details: workflowResult.details
  });
  if (!workflowResult.success) {
    result.errors.push(workflowResult.message);
  }

  // Determine overall success
  result.success = result.errors.length === 0;

  // Display results
  console.log('\n📊 Infrastructure Setup Results:\n');
  
  result.steps.forEach((step, index) => {
    const icon = step.completed ? '✅' : '❌';
    console.log(`${index + 1}. ${icon} ${step.name}`);
    console.log(`   ${step.message}`);
    
    if (step.details && step.details.length > 0) {
      step.details.forEach(detail => {
        console.log(`      • ${detail}`);
      });
    }
    console.log('');
  });

  if (result.success) {
    console.log('🎉 Phase 1 Infrastructure Setup completed successfully!\n');
    
    result.nextSteps = [
      'Run `pnpm install` to update dependencies with catalog system',
      'Test Turbo build system: `pnpm turbo:build`',
      'Review created scoped packages and customize as needed',
      'Run `make analyze-n8n-integration` to proceed to Phase 2',
      'Begin extracting N8N core packages for integration'
    ];
    
    console.log('🎯 Next Steps:');
    result.nextSteps.forEach((step, index) => {
      console.log(`   ${index + 1}. ${step}`);
    });
    
  } else {
    console.log('⚠️  Phase 1 completed with errors. Please resolve issues before proceeding.\n');
    
    console.log('❌ Errors encountered:');
    result.errors.forEach((error, index) => {
      console.log(`   ${index + 1}. ${error}`);
    });
  }

  console.log('\n================================================\n');
  
  return result;
}

// Run setup
if (require.main === module) {
  main()
    .then(result => {
      process.exit(result.success ? 0 : 1);
    })
    .catch(error => {
      console.error('Failed to run infrastructure setup:', error);
      process.exit(1);
    });
}

export { main as setupN8NInfrastructure };
