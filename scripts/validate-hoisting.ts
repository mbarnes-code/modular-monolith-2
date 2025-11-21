#!/usr/bin/env tsx

/**
 * Library Hoisting Validation Script
 * 
 * Validates the environment and dependencies before running the automated hoisting
 */

import * as fs from 'fs';
import * as path from 'path';

// Import types to verify AST utilities are available

interface ValidationResult {
  success: boolean;
  checks: Array<{ name: string; passed: boolean; message: string }>;
  errors: string[];
  warnings: string[];
}

/**
 * Validate prerequisites for library hoisting
 */
async function validateHoistingPrerequisites(): Promise<ValidationResult> {
  const result: ValidationResult = {
    success: false,
    checks: [],
    errors: [],
    warnings: []
  };

  console.log('🔍 Validating hoisting prerequisites...\n');

  // Check 1: Root package.json exists
  const rootPackageJsonExists = fs.existsSync('package.json');
  result.checks.push({
    name: 'Root package.json exists',
    passed: rootPackageJsonExists,
    message: rootPackageJsonExists ? 'Found root package.json' : 'Root package.json not found'
  });

  if (!rootPackageJsonExists) {
    result.errors.push('Root package.json is required for hoisting');
  }

  // Check 2: AST utilities are available
  let astUtilsAvailable = false;
  try {
    await import('../libs/intelligence/code');
    astUtilsAvailable = true;
  } catch (error) {
    result.errors.push(`AST utilities not available: ${error}`);
  }

  result.checks.push({
    name: 'AST utilities available',
    passed: astUtilsAvailable,
    message: astUtilsAvailable ? 'AST utilities loaded successfully' : 'AST utilities not found'
  });

  // Check 3: Target services exist
  const targetServices = [
    'apps/productivity/n8n-service',
    'apps/tcg/commander-spellbook-site',
    'apps/productivity/actual-service',
    'apps/security/cyberchef-service'
  ];

  let servicesFound = 0;
  for (const servicePath of targetServices) {
    const serviceExists = fs.existsSync(servicePath);
    const packageJsonExists = fs.existsSync(path.join(servicePath, 'package.json'));
    
    if (serviceExists && packageJsonExists) {
      servicesFound++;
    } else if (serviceExists) {
      result.warnings.push(`Service ${servicePath} exists but has no package.json`);
    } else {
      result.warnings.push(`Service ${servicePath} not found`);
    }
  }

  result.checks.push({
    name: `Target services found (${servicesFound}/${targetServices.length})`,
    passed: servicesFound > 0,
    message: `Found ${servicesFound} services with package.json files`
  });

  // Check 4: pnpm is available
  let pnpmAvailable = false;
  try {
    const { execSync } = await import('child_process');
    execSync('pnpm --version', { stdio: 'ignore' });
    pnpmAvailable = true;
  } catch {
    result.errors.push('pnpm is required but not available');
  }

  result.checks.push({
    name: 'pnpm available',
    passed: pnpmAvailable,
    message: pnpmAvailable ? 'pnpm is available' : 'pnpm not found'
  });

  // Check 5: NX workspace
  const nxJsonExists = fs.existsSync('nx.json');
  result.checks.push({
    name: 'NX workspace',
    passed: nxJsonExists,
    message: nxJsonExists ? 'NX workspace detected' : 'Not an NX workspace'
  });

  if (!nxJsonExists) {
    result.warnings.push('This doesn\'t appear to be an NX workspace');
  }

  // Check 6: TypeScript configuration
  const tsConfigExists = fs.existsSync('tsconfig.json') || fs.existsSync('tsconfig.base.json');
  result.checks.push({
    name: 'TypeScript configuration',
    passed: tsConfigExists,
    message: tsConfigExists ? 'TypeScript configuration found' : 'No TypeScript configuration'
  });

  // Check 7: Intelligence code library is built
  const intelligenceLibBuilt = fs.existsSync('libs/intelligence/code/dist') || 
                              fs.existsSync('libs/intelligence/code/index.ts');
  result.checks.push({
    name: 'Intelligence code library',
    passed: intelligenceLibBuilt,
    message: intelligenceLibBuilt ? 'Intelligence library available' : 'Intelligence library not built'
  });

  if (!intelligenceLibBuilt) {
    result.warnings.push('Consider building the intelligence code library first: nx build intelligence-code');
  }

  // Summary
  const passedChecks = result.checks.filter(c => c.passed).length;
  const totalChecks = result.checks.length;
  result.success = result.errors.length === 0 && passedChecks >= totalChecks * 0.8; // 80% pass rate

  return result;
}

/**
 * Analyze current dependency overlap
 */
function analyzeDependencyOverlap(): { [dep: string]: string[] } {
  const overlaps: { [dep: string]: string[] } = {};
  
  const targetDeps = ['axios', 'uuid', 'cors', 'lodash', 'winston'];
  const servicePaths = [
    'apps/productivity/n8n-service',
    'apps/tcg/commander-spellbook-site', 
    'apps/productivity/actual-service',
    'apps/security/cyberchef-service'
  ];

  for (const servicePath of servicePaths) {
    const packageJsonPath = path.join(servicePath, 'package.json');
    if (!fs.existsSync(packageJsonPath)) continue;

    try {
      const packageJson = JSON.parse(fs.readFileSync(packageJsonPath, 'utf-8'));
      const allDeps = { ...packageJson.dependencies, ...packageJson.devDependencies };

      for (const dep of targetDeps) {
        if (allDeps[dep]) {
          if (!overlaps[dep]) overlaps[dep] = [];
          overlaps[dep].push(`${servicePath} (${allDeps[dep]})`);
        }
      }
    } catch (error) {
      console.warn(`Failed to analyze ${packageJsonPath}: ${error}`);
    }
  }

  return overlaps;
}

/**
 * Main validation function
 */
async function main() {
  console.log('📋 Library Hoisting Validation\n');
  console.log('==============================\n');

  const result = await validateHoistingPrerequisites();

  // Display check results
  console.log('✅ Prerequisites Check:\n');
  for (const check of result.checks) {
    const icon = check.passed ? '✅' : '❌';
    console.log(`   ${icon} ${check.name}: ${check.message}`);
  }

  // Display warnings
  if (result.warnings.length > 0) {
    console.log('\n⚠️  Warnings:\n');
    for (const warning of result.warnings) {
      console.log(`   • ${warning}`);
    }
  }

  // Display errors
  if (result.errors.length > 0) {
    console.log('\n❌ Errors:\n');
    for (const error of result.errors) {
      console.log(`   • ${error}`);
    }
  }

  // Analyze current overlaps
  console.log('\n📊 Current Dependency Overlaps:\n');
  const overlaps = analyzeDependencyOverlap();
  
  if (Object.keys(overlaps).length === 0) {
    console.log('   No overlapping dependencies found.');
  } else {
    for (const [dep, services] of Object.entries(overlaps)) {
      console.log(`   📦 ${dep}:`);
      for (const service of services) {
        console.log(`      • ${service}`);
      }
      console.log('');
    }
  }

  // Final recommendation
  console.log('\n🎯 Recommendation:\n');
  
  if (result.success) {
    console.log('   ✅ Environment is ready for automated library hoisting!');
    console.log('   Run: make hoist-libraries-preview');
    console.log('   Then: make hoist-libraries');
  } else {
    console.log('   ❌ Please resolve the errors above before proceeding.');
    console.log('   Consider running: npm install && nx build intelligence-code');
  }

  console.log('\n==============================\n');

  process.exit(result.success ? 0 : 1);
}

// Run validation
if (require.main === module) {
  main().catch(console.error);
}

export { analyzeDependencyOverlap, validateHoistingPrerequisites };
