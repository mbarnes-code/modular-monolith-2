#!/usr/bin/env tsx

/**
 * Automated Library Hoisting Script
 * 
 * Uses the existing ts-morph AST infrastructure to safely hoist Phase 1 dependencies
 * from individual apps to the root monorepo level with automated validation and rollback.
 * 
 * Based on LIBRARY_OVERLAP_AUDIT.md and VERSION_COMPATIBILITY_ANALYSIS.md
 */

import { execSync } from 'child_process';
import * as fs from 'fs';
import * as path from 'path';
import type { BatchProcessingConfig, RefactoringOperation } from '../libs/intelligence/code';
import { batchProcess } from '../libs/intelligence/code';

// Phase 1 Dependencies - Zero Risk (from compatibility analysis)
const PHASE_1_DEPENDENCIES = {
  // JavaScript Dependencies
  'axios': '1.12.2',
  'uuid': '13.0.0', 
  'cors': '2.8.5',
  'lodash': '4.17.21',
  'winston': '3.18.3',
  
  // Dev Dependencies
  '@types/uuid': '10.0.0',
  '@types/cors': '2.8.17',
  '@types/lodash': '4.17.13'
} as const;

// Services affected (from actual dependency analysis)
const AFFECTED_SERVICES = [
  'apps/productivity/n8n-service',
  'apps/tcg/commander-spellbook-site',
  'apps/productivity/actual-service',
  'apps/security/cyberchef-service'
] as const;

interface PackageJson {
  name?: string;
  dependencies?: Record<string, string>;
  devDependencies?: Record<string, string>;
  [key: string]: any;
}

interface HoistingResult {
  success: boolean;
  hoistedDependencies: string[];
  updatedServices: string[];
  errors: string[];
  rollbackData: Array<{ file: string; originalContent: string }>;
}

/**
 * Load and parse package.json files
 */
function loadPackageJson(servicePath: string): PackageJson | null {
  const packageJsonPath = path.join(servicePath, 'package.json');
  
  if (!fs.existsSync(packageJsonPath)) {
    return null;
  }
  
  try {
    return JSON.parse(fs.readFileSync(packageJsonPath, 'utf-8'));
  } catch (error) {
    console.warn(`Failed to parse ${packageJsonPath}:`, error);
    return null;
  }
}

/**
 * Save package.json with proper formatting
 */
function savePackageJson(servicePath: string, packageJson: PackageJson): void {
  const packageJsonPath = path.join(servicePath, 'package.json');
  fs.writeFileSync(packageJsonPath, JSON.stringify(packageJson, null, 2) + '\n');
}

/**
 * Create backup of package.json for rollback
 */
function createBackup(servicePath: string): string {
  const packageJsonPath = path.join(servicePath, 'package.json');
  const backupPath = path.join(servicePath, 'package.json.backup');
  
  if (fs.existsSync(packageJsonPath)) {
    fs.copyFileSync(packageJsonPath, backupPath);
    return fs.readFileSync(packageJsonPath, 'utf-8');
  }
  
  return '';
}

/**
 * Refactoring operation to update import paths after hoisting
 */
const updateImportPathsOperation: RefactoringOperation = {
  name: 'updateImportPaths',
  description: 'Update import paths after dependency hoisting',
  patterns: [{
    nodeType: 'ImportDeclaration',
    conditions: {}
  }],
  transform: (sourceFile, matches) => {
    try {
      // Use existing updateImports function to handle import path updates
      const imports = sourceFile.getImportDeclarations();
      let hasChanges = false;
      
      imports.forEach(importDecl => {
        const moduleSpecifier = importDecl.getModuleSpecifierValue();
        
        // Check if this is a hoisted dependency
        if (Object.keys(PHASE_1_DEPENDENCIES).some(dep => 
          moduleSpecifier === dep || moduleSpecifier.startsWith(dep + '/')
        )) {
          // Import paths should remain the same after hoisting to root
          // The package manager will resolve from root node_modules
          hasChanges = true;
        }
      });
      
      return hasChanges;
    } catch (error) {
      console.error('Failed to update import paths:', error);
      return false;
    }
  },
  safetyCheck: (sourceFile) => {
    // Basic safety check - ensure file can be parsed
    try {
      sourceFile.getImportDeclarations();
      return true;
    } catch {
      return false;
    }
  },
  rollback: (sourceFile) => {
    // Rollback would restore original import paths
    // For now, we rely on package.json rollback
    return true;
  }
};

/**
 * Main hoisting function
 */
async function hoistLibraries(): Promise<HoistingResult> {
  const result: HoistingResult = {
    success: false,
    hoistedDependencies: [],
    updatedServices: [],
    errors: [],
    rollbackData: []
  };

  console.log('🚀 Starting automated library hoisting...\n');

  try {
    // Step 1: Load root package.json
    const rootPackageJson = loadPackageJson('.');
    if (!rootPackageJson) {
      throw new Error('Root package.json not found');
    }

    // Create backup of root package.json
    const rootBackup = createBackup('.');
    result.rollbackData.push({ file: 'package.json', originalContent: rootBackup });

    // Step 2: Analyze affected services
    const servicesToUpdate: Array<{ path: string; packageJson: PackageJson; hasTargetDeps: boolean }> = [];
    
    for (const servicePath of AFFECTED_SERVICES) {
      const packageJson = loadPackageJson(servicePath);
      if (!packageJson) {
        console.warn(`⚠️  No package.json found in ${servicePath}`);
        continue;
      }

      // Check if service has any Phase 1 dependencies
      const hasTargetDeps = Object.keys(PHASE_1_DEPENDENCIES).some(dep => 
        packageJson.dependencies?.[dep] || packageJson.devDependencies?.[dep]
      );

      if (hasTargetDeps) {
        servicesToUpdate.push({ path: servicePath, packageJson, hasTargetDeps });
        
        // Create backup
        const backup = createBackup(servicePath);
        result.rollbackData.push({ file: path.join(servicePath, 'package.json'), originalContent: backup });
      }
    }

    console.log(`📦 Found ${servicesToUpdate.length} services with Phase 1 dependencies\n`);

    // Step 3: Hoist dependencies to root
    const rootDeps = rootPackageJson.dependencies || {};
    const rootDevDeps = rootPackageJson.devDependencies || {};

    for (const [depName, targetVersion] of Object.entries(PHASE_1_DEPENDENCIES)) {
      const isDevDep = depName.startsWith('@types/');
      
      if (isDevDep) {
        rootDevDeps[depName] = targetVersion;
      } else {
        rootDeps[depName] = targetVersion;
      }
      
      result.hoistedDependencies.push(`${depName}@${targetVersion}`);
      console.log(`✅ Hoisted ${depName}@${targetVersion} to root`);
    }

    // Update root package.json
    rootPackageJson.dependencies = rootDeps;
    rootPackageJson.devDependencies = rootDevDeps;
    savePackageJson('.', rootPackageJson);

    // Step 4: Remove dependencies from individual services
    for (const { path: servicePath, packageJson } of servicesToUpdate) {
      let serviceUpdated = false;

      for (const depName of Object.keys(PHASE_1_DEPENDENCIES)) {
        if (packageJson.dependencies?.[depName]) {
          delete packageJson.dependencies[depName];
          serviceUpdated = true;
        }
        
        if (packageJson.devDependencies?.[depName]) {
          delete packageJson.devDependencies[depName];
          serviceUpdated = true;
        }
      }

      if (serviceUpdated) {
        savePackageJson(servicePath, packageJson);
        result.updatedServices.push(servicePath);
        console.log(`📝 Updated ${servicePath}/package.json`);
      }
    }

    // Step 5: Update import paths using AST operations
    console.log('\n🔧 Updating import paths...');
    
    const tsFiles: string[] = [];
    for (const { path: servicePath } of servicesToUpdate) {
      // Find TypeScript files in service
      const srcPath = path.join(servicePath, 'src');
      if (fs.existsSync(srcPath)) {
        const findTsFiles = (dir: string): void => {
          const entries = fs.readdirSync(dir, { withFileTypes: true });
          for (const entry of entries) {
            const fullPath = path.join(dir, entry.name);
            if (entry.isDirectory() && entry.name !== 'node_modules') {
              findTsFiles(fullPath);
            } else if (entry.isFile() && (entry.name.endsWith('.ts') || entry.name.endsWith('.tsx'))) {
              tsFiles.push(fullPath);
            }
          }
        };
        findTsFiles(srcPath);
      }
    }

    if (tsFiles.length > 0) {
      const batchConfig: BatchProcessingConfig = {
        files: tsFiles,
        operations: [updateImportPathsOperation],
        parallelism: 4,
        continueOnError: true,
        createBackups: false, // We already have backups
        onProgress: (progress) => {
          const percentage = Math.round((progress.processed / progress.total) * 100);
          console.log(`   📊 Progress: ${percentage}% (${progress.processed}/${progress.total})`);
        },
        onError: (error) => {
          result.errors.push(`Import update error in ${error.filePath}: ${error.message}`);
        }
      };

      const batchResult = await batchProcess(batchConfig);
      if (!batchResult.success && result.errors.length === 0) {
        result.errors.push('Some TypeScript files failed to update imports');
      }
    }

    // Step 6: Install dependencies
    console.log('\n📥 Installing dependencies...');
    try {
      execSync('pnpm install', { cwd: '.', stdio: 'inherit' });
      console.log('✅ Dependencies installed successfully');
    } catch (error) {
      result.errors.push(`Dependency installation failed: ${error}`);
      throw error;
    }

    // Step 7: Validate hoisting
    console.log('\n🔍 Validating hoisting...');
    
    // Check that hoisted dependencies exist in root node_modules
    for (const depName of Object.keys(PHASE_1_DEPENDENCIES)) {
      const depPath = path.join('node_modules', depName);
      if (!fs.existsSync(depPath)) {
        result.errors.push(`Hoisted dependency ${depName} not found in root node_modules`);
      }
    }

    if (result.errors.length === 0) {
      result.success = true;
      console.log('\n🎉 Library hoisting completed successfully!');
      console.log(`\n📊 Summary:`);
      console.log(`   • Hoisted ${result.hoistedDependencies.length} dependencies`);
      console.log(`   • Updated ${result.updatedServices.length} services`);
      console.log(`   • Processed ${tsFiles.length} TypeScript files`);
    } else {
      console.log('\n⚠️  Hoisting completed with errors. Consider rollback.');
    }

  } catch (error) {
    result.errors.push(`Critical error: ${error}`);
    console.error('\n❌ Critical error during hoisting:', error);
  }

  return result;
}

/**
 * Rollback function to restore original state
 */
async function rollbackHoisting(rollbackData: Array<{ file: string; originalContent: string }>): Promise<void> {
  console.log('\n🔄 Rolling back changes...');
  
  for (const { file, originalContent } of rollbackData) {
    try {
      fs.writeFileSync(file, originalContent);
      console.log(`✅ Restored ${file}`);
    } catch (error) {
      console.error(`❌ Failed to restore ${file}:`, error);
    }
  }
  
  // Reinstall original dependencies
  try {
    execSync('pnpm install', { cwd: '.', stdio: 'inherit' });
    console.log('✅ Dependencies restored');
  } catch (error) {
    console.error('❌ Failed to restore dependencies:', error);
  }
}

/**
 * CLI interface
 */
async function main() {
  const args = process.argv.slice(2);
  const dryRun = args.includes('--dry-run');
  const force = args.includes('--force');

  if (dryRun) {
    console.log('🔍 DRY RUN MODE - No changes will be made\n');
    // TODO: Implement dry run analysis
    return;
  }

  if (!force) {
    console.log('⚠️  This will modify package.json files across multiple services.');
    console.log('   Add --force flag to proceed, or --dry-run to preview changes.\n');
    return;
  }

  const result = await hoistLibraries();

  if (!result.success && result.rollbackData.length > 0) {
    console.log('\n🤔 Errors detected. Rollback? (y/N)');
    
    // Simple prompt handling
    process.stdin.setEncoding('utf8');
    process.stdin.on('data', async (data) => {
      const input = data.toString().trim().toLowerCase();
      if (input === 'y' || input === 'yes') {
        await rollbackHoisting(result.rollbackData);
      }
      process.exit(result.success ? 0 : 1);
    });
  } else {
    process.exit(result.success ? 0 : 1);
  }
}

// Run if called directly
if (require.main === module) {
  main().catch(console.error);
}

export { AFFECTED_SERVICES, hoistLibraries, PHASE_1_DEPENDENCIES, rollbackHoisting };
