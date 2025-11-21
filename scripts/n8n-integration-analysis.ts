#!/usr/bin/env tsx

/**
 * N8N Monorepo Integration Analysis
 * 
 * Analyzes N8N's monorepo structure and creates a comprehensive integration plan
 * for bringing N8N fully into the main Mental Prosthetic Platform monorepo.
 */

import * as fs from 'fs';
import * as path from 'path';

interface N8NPackage {
  name: string;
  path: string;
  dependencies: Record<string, string>;
  devDependencies: Record<string, string>;
  isCore: boolean;
  isScoped: boolean;
  buildOutputs: string[];
}

interface CatalogEntry {
  name: string;
  version: string;
  usedBy: string[];
  catalogType: 'main' | 'frontend' | 'backend';
}

interface IntegrationPlan {
  packages: {
    core: N8NPackage[];
    optional: N8NPackage[];
    conflicting: N8NPackage[];
  };
  catalogs: {
    toMerge: CatalogEntry[];
    conflicts: Array<{ name: string; currentVersion: string; n8nVersion: string }>;
  };
  buildSystem: {
    turboTasks: Record<string, any>;
    nxProjects: string[];
    conflicts: string[];
  };
  migrationSteps: Array<{
    phase: string;
    description: string;
    packages: string[];
    estimatedEffort: 'low' | 'medium' | 'high';
    risks: string[];
  }>;
}

/**
 * Analyze N8N's package structure
 */
function analyzeN8NPackages(): N8NPackage[] {
  const n8nRoot = 'apps/productivity/n8n-service';
  const packagesDir = path.join(n8nRoot, 'src/packages');
  const packages: N8NPackage[] = [];

  if (!fs.existsSync(packagesDir)) {
    console.warn('N8N packages directory not found');
    return packages;
  }

  // Analyze packages in src/packages
  const packageDirs = ['@n8n', 'cli', 'core', 'frontend', 'nodes-base', 'workflow'];
  
  for (const dir of packageDirs) {
    const packagePath = path.join(packagesDir, dir);
    if (!fs.existsSync(packagePath)) continue;

    if (dir === '@n8n') {
      // Handle scoped packages
      const scopedPackages = fs.readdirSync(packagePath, { withFileTypes: true })
        .filter(dirent => dirent.isDirectory())
        .map(dirent => dirent.name);

      for (const scopedPkg of scopedPackages) {
        const scopedPath = path.join(packagePath, scopedPkg);
        const packageJsonPath = path.join(scopedPath, 'package.json');
        
        if (fs.existsSync(packageJsonPath)) {
          const pkg = analyzePackage(packageJsonPath, path.join('src/packages/@n8n', scopedPkg));
          if (pkg) {
            pkg.isScoped = true;
            pkg.isCore = isCore(pkg.name);
            packages.push(pkg);
          }
        }
      }
    } else {
      // Handle regular packages
      const packageJsonPath = path.join(packagePath, 'package.json');
      if (fs.existsSync(packageJsonPath)) {
        const pkg = analyzePackage(packageJsonPath, path.join('src/packages', dir));
        if (pkg) {
          pkg.isScoped = false;
          pkg.isCore = isCore(pkg.name);
          packages.push(pkg);
        }
      }
    }
  }

  return packages;
}

/**
 * Analyze individual package
 */
function analyzePackage(packageJsonPath: string, relativePath: string): N8NPackage | null {
  try {
    const packageJson = JSON.parse(fs.readFileSync(packageJsonPath, 'utf-8'));
    
    return {
      name: packageJson.name || path.basename(relativePath),
      path: relativePath,
      dependencies: packageJson.dependencies || {},
      devDependencies: packageJson.devDependencies || {},
      isCore: false, // Will be set by caller
      isScoped: false, // Will be set by caller
      buildOutputs: getBuildOutputs(packageJson)
    };
  } catch (error) {
    console.warn(`Failed to analyze package ${packageJsonPath}: ${error}`);
    return null;
  }
}

/**
 * Determine if package is core to N8N functionality
 */
function isCore(packageName: string): boolean {
  const corePackages = [
    'n8n-core',
    'n8n-workflow', 
    '@n8n/core',
    '@n8n/workflow',
    'n8n-cli',
    '@n8n/cli',
    '@n8n/nodes-base'
  ];
  
  return corePackages.some(core => packageName.includes(core));
}

/**
 * Extract build outputs from package.json
 */
function getBuildOutputs(packageJson: any): string[] {
  const outputs = ['dist/**'];
  
  if (packageJson.scripts?.build) {
    // Try to infer outputs from build script
    const buildScript = packageJson.scripts.build;
    if (buildScript.includes('--outDir')) {
      const match = buildScript.match(/--outDir\s+([^\s]+)/);
      if (match) outputs.push(`${match[1]}/**`);
    }
  }
  
  return outputs;
}

/**
 * Analyze N8N's catalog system
 */
function analyzeN8NCatalogs(): CatalogEntry[] {
  const n8nRoot = 'apps/productivity/n8n-service';
  const workspaceFile = path.join(n8nRoot, 'pnpm-workspace.yaml');
  const catalogs: CatalogEntry[] = [];

  if (!fs.existsSync(workspaceFile)) {
    return catalogs;
  }

  try {
    const workspaceContent = fs.readFileSync(workspaceFile, 'utf-8');
    
    // Parse YAML manually for catalog entries (simple parsing)
    const lines = workspaceContent.split('\n');
    let inCatalog = false;
    let catalogType: 'main' | 'frontend' | 'backend' = 'main';

    for (const line of lines) {
      if (line.trim().startsWith('catalog:')) {
        inCatalog = true;
        catalogType = 'main';
      } else if (line.trim().startsWith('catalogs:')) {
        inCatalog = false;
      } else if (line.trim().match(/^\s*\w+:$/)) {
        // Frontend/backend catalog
        const match = line.trim().match(/^(\w+):$/);
        if (match && inCatalog) {
          catalogType = match[1] as 'frontend' | 'backend';
        }
      } else if (inCatalog && line.includes(':') && !line.trim().startsWith('#')) {
        const match = line.match(/^\s*'?([^':\s]+)'?:\s*(.+)$/);
        if (match && match[1] && match[2]) {
          catalogs.push({
            name: match[1],
            version: match[2].trim(),
            usedBy: [], // Would need deeper analysis to populate
            catalogType
          });
        }
      }
    }
  } catch (error) {
    console.warn(`Failed to parse N8N workspace file: ${error}`);
  }

  return catalogs;
}

/**
 * Analyze current monorepo catalogs
 */
function analyzeCurrentCatalogs(): CatalogEntry[] {
  const workspaceFile = 'pnpm-workspace.yaml';
  const catalogs: CatalogEntry[] = [];

  if (!fs.existsSync(workspaceFile)) {
    return catalogs;
  }

  // Current monorepo doesn't have catalogs yet, so return empty
  // This would be populated when we implement the catalog system
  return catalogs;
}

/**
 * Create integration plan
 */
function createIntegrationPlan(
  n8nPackages: N8NPackage[],
  n8nCatalogs: CatalogEntry[],
  currentCatalogs: CatalogEntry[]
): IntegrationPlan {
  
  // Categorize packages
  const corePackages = n8nPackages.filter(pkg => pkg.isCore);
  const optionalPackages = n8nPackages.filter(pkg => !pkg.isCore && !hasConflicts(pkg.name));
  const conflictingPackages = n8nPackages.filter(pkg => hasConflicts(pkg.name));

  // Analyze catalog conflicts
  const catalogConflicts = n8nCatalogs
    .filter(n8nCat => currentCatalogs.some(currentCat => currentCat.name === n8nCat.name))
    .map(n8nCat => {
      const currentCat = currentCatalogs.find(c => c.name === n8nCat.name)!;
      return {
        name: n8nCat.name,
        currentVersion: currentCat.version,
        n8nVersion: n8nCat.version
      };
    });

  const catalogsToMerge = n8nCatalogs.filter(n8nCat => 
    !currentCatalogs.some(currentCat => currentCat.name === n8nCat.name)
  );

  // Create migration phases
  const migrationSteps = [
    {
      phase: 'Phase 1: Infrastructure Setup',
      description: 'Add Turbo, implement catalog system, create scoped packages structure',
      packages: [],
      estimatedEffort: 'medium' as const,
      risks: ['Build system conflicts', 'Dependency resolution issues']
    },
    {
      phase: 'Phase 2: Core Package Migration',
      description: 'Migrate essential N8N packages (core, workflow, cli)',
      packages: corePackages.map(pkg => pkg.name),
      estimatedEffort: 'high' as const,
      risks: ['Breaking changes', 'Complex dependency graphs', 'Testing challenges']
    },
    {
      phase: 'Phase 3: Optional Package Migration',
      description: 'Migrate non-essential but valuable packages',
      packages: optionalPackages.map(pkg => pkg.name),
      estimatedEffort: 'medium' as const,
      risks: ['Feature conflicts', 'Maintenance overhead']
    },
    {
      phase: 'Phase 4: Integration & Optimization',
      description: 'Cross-domain integration and workflow orchestration',
      packages: [],
      estimatedEffort: 'high' as const,
      risks: ['Performance impact', 'Complex cross-domain dependencies']
    }
  ];

  return {
    packages: {
      core: corePackages,
      optional: optionalPackages,
      conflicting: conflictingPackages
    },
    catalogs: {
      toMerge: catalogsToMerge,
      conflicts: catalogConflicts
    },
    buildSystem: {
      turboTasks: extractTurboTasks(),
      nxProjects: [], // Would extract from current NX config
      conflicts: [] // Would identify conflicts between Turbo and NX
    },
    migrationSteps
  };
}

/**
 * Check if package has conflicts with existing monorepo
 */
function hasConflicts(packageName: string): boolean {
  // Check for naming conflicts with existing packages
  const existingPackages = [
    'jane-ui',
    'jane-orchestrator',
    'actual-service'
    // Add more as needed
  ];
  
  return existingPackages.some(existing => 
    packageName.toLowerCase().includes(existing.toLowerCase()) ||
    existing.toLowerCase().includes(packageName.toLowerCase())
  );
}

/**
 * Extract Turbo tasks from N8N's turbo.json
 */
function extractTurboTasks(): Record<string, any> {
  const n8nTurboFile = 'apps/productivity/n8n-service/turbo.json';
  
  if (!fs.existsSync(n8nTurboFile)) {
    return {};
  }

  try {
    const turboConfig = JSON.parse(fs.readFileSync(n8nTurboFile, 'utf-8'));
    return turboConfig.tasks || {};
  } catch (error) {
    console.warn(`Failed to parse N8N turbo.json: ${error}`);
    return {};
  }
}

/**
 * Generate migration scripts
 */
function generateMigrationScripts(plan: IntegrationPlan): void {
  const scriptsDir = 'scripts/n8n-migration';
  
  if (!fs.existsSync(scriptsDir)) {
    fs.mkdirSync(scriptsDir, { recursive: true });
  }

  // Generate package extraction script
  const extractScript = `#!/usr/bin/env tsx

/**
 * Extract N8N packages for integration
 * Generated by n8n-integration-analysis.ts
 */

const CORE_PACKAGES = ${JSON.stringify(plan.packages.core.map(p => p.name), null, 2)};
const OPTIONAL_PACKAGES = ${JSON.stringify(plan.packages.optional.map(p => p.name), null, 2)};

// Implementation would go here
console.log('Extracting N8N packages...', CORE_PACKAGES.length, 'core packages');
`;

  fs.writeFileSync(path.join(scriptsDir, 'extract-packages.ts'), extractScript);

  // Generate catalog merge script
  const catalogScript = `#!/usr/bin/env tsx

/**
 * Merge N8N catalog system with main monorepo
 * Generated by n8n-integration-analysis.ts
 */

const CATALOGS_TO_MERGE = ${JSON.stringify(plan.catalogs.toMerge, null, 2)};
const CATALOG_CONFLICTS = ${JSON.stringify(plan.catalogs.conflicts, null, 2)};

// Implementation would go here
console.log('Merging catalogs...', CATALOGS_TO_MERGE.length, 'entries to merge');
`;

  fs.writeFileSync(path.join(scriptsDir, 'merge-catalogs.ts'), catalogScript);

  console.log(`Generated migration scripts in ${scriptsDir}/`);
}

/**
 * Main analysis function
 */
function main() {
  console.log('🔍 N8N Monorepo Integration Analysis\n');
  console.log('=====================================\n');

  console.log('📦 Analyzing N8N packages...');
  const n8nPackages = analyzeN8NPackages();
  console.log(`   Found ${n8nPackages.length} N8N packages`);
  console.log(`   Core packages: ${n8nPackages.filter(p => p.isCore).length}`);
  console.log(`   Scoped packages: ${n8nPackages.filter(p => p.isScoped).length}\n`);

  console.log('📋 Analyzing catalog systems...');
  const n8nCatalogs = analyzeN8NCatalogs();
  const currentCatalogs = analyzeCurrentCatalogs();
  console.log(`   N8N catalog entries: ${n8nCatalogs.length}`);
  console.log(`   Current catalog entries: ${currentCatalogs.length}\n`);

  console.log('🎯 Creating integration plan...');
  const plan = createIntegrationPlan(n8nPackages, n8nCatalogs, currentCatalogs);

  // Display results
  console.log('\n📊 Integration Analysis Results:\n');
  
  console.log('   📦 Package Categories:');
  console.log(`      • Core packages (must migrate): ${plan.packages.core.length}`);
  plan.packages.core.forEach(pkg => console.log(`        - ${pkg.name}`));
  
  console.log(`      • Optional packages: ${plan.packages.optional.length}`);
  plan.packages.optional.slice(0, 5).forEach(pkg => console.log(`        - ${pkg.name}`));
  if (plan.packages.optional.length > 5) {
    console.log(`        ... and ${plan.packages.optional.length - 5} more`);
  }
  
  console.log(`      • Conflicting packages: ${plan.packages.conflicting.length}`);
  plan.packages.conflicting.forEach(pkg => console.log(`        - ${pkg.name} (needs resolution)`));

  console.log('\n   📋 Catalog Analysis:');
  console.log(`      • Catalogs to merge: ${plan.catalogs.toMerge.length}`);
  console.log(`      • Catalog conflicts: ${plan.catalogs.conflicts.length}`);
  plan.catalogs.conflicts.forEach(conflict => 
    console.log(`        - ${conflict.name}: current(${conflict.currentVersion}) vs n8n(${conflict.n8nVersion})`)
  );

  console.log('\n   🗺️ Migration Phases:');
  plan.migrationSteps.forEach((step, index) => {
    console.log(`      ${index + 1}. ${step.phase} (${step.estimatedEffort} effort)`);
    console.log(`         ${step.description}`);
    if (step.packages.length > 0) {
      console.log(`         Packages: ${step.packages.slice(0, 3).join(', ')}${step.packages.length > 3 ? '...' : ''}`);
    }
    console.log(`         Risks: ${step.risks.join(', ')}`);
    console.log('');
  });

  console.log('🛠️ Generating migration scripts...');
  generateMigrationScripts(plan);

  console.log('\n🎯 Recommendations:\n');
  
  if (plan.packages.core.length > 0) {
    console.log('   ✅ N8N has valuable core packages worth integrating');
    console.log('   📈 Expected benefits: Advanced workflow automation, sophisticated build system');
  }
  
  if (plan.catalogs.conflicts.length > 0) {
    console.log('   ⚠️  Catalog conflicts need resolution before migration');
    console.log('   🔍 Review version differences and choose optimal versions');
  }
  
  if (plan.packages.conflicting.length === 0) {
    console.log('   ✅ No major package naming conflicts detected');
  }

  console.log('\n📋 Next Steps:');
  console.log('   1. Review generated migration scripts in scripts/n8n-migration/');
  console.log('   2. Resolve catalog conflicts');
  console.log('   3. Set up Turbo build system');
  console.log('   4. Begin Phase 1: Infrastructure Setup');

  console.log('\n=====================================\n');
}

// Run analysis
if (require.main === module) {
  main();
}

export { analyzeN8NPackages, createIntegrationPlan };
