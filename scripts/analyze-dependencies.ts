#!/usr/bin/env tsx

/**
 * Dependency Analysis Script
 * 
 * Analyzes actual dependencies across the monorepo to identify real overlap opportunities
 */

import * as fs from 'fs';
import * as path from 'path';

interface DependencyInfo {
  version: string;
  services: string[];
  isDev: boolean;
}

interface PackageJson {
  name?: string;
  dependencies?: Record<string, string>;
  devDependencies?: Record<string, string>;
}

/**
 * Recursively find all package.json files in the workspace
 */
function findPackageJsonFiles(dir: string, exclude: string[] = []): string[] {
  const packageJsonFiles: string[] = [];
  
  function traverse(currentDir: string) {
    if (exclude.some(pattern => currentDir.includes(pattern))) {
      return;
    }

    try {
      const entries = fs.readdirSync(currentDir, { withFileTypes: true });
      
      for (const entry of entries) {
        const fullPath = path.join(currentDir, entry.name);
        
        if (entry.isDirectory() && 
            entry.name !== 'node_modules' && 
            entry.name !== '.git' && 
            entry.name !== 'dist' && 
            entry.name !== 'build') {
          traverse(fullPath);
        } else if (entry.isFile() && entry.name === 'package.json') {
          packageJsonFiles.push(fullPath);
        }
      }
    } catch (error) {
      console.warn(`Could not read directory ${currentDir}: ${error}`);
    }
  }
  
  traverse(dir);
  return packageJsonFiles;
}

/**
 * Load and parse a package.json file
 */
function loadPackageJson(filePath: string): PackageJson | null {
  try {
    const content = fs.readFileSync(filePath, 'utf-8');
    return JSON.parse(content);
  } catch (error) {
    console.warn(`Failed to parse ${filePath}: ${error}`);
    return null;
  }
}

/**
 * Analyze dependency overlaps across all services
 */
function analyzeDependencies() {
  console.log('🔍 Analyzing dependencies across the monorepo...\n');
  
  // Find all package.json files, excluding node_modules and other irrelevant directories
  const packageJsonFiles = findPackageJsonFiles('.', [
    'node_modules',
    '.git',
    'dist',
    'build',
    '.nx',
    'tmp',
    'experimental-archive'
  ]);
  
  console.log(`Found ${packageJsonFiles.length} package.json files\n`);
  
  // Track all dependencies
  const dependencyMap = new Map<string, DependencyInfo>();
  const servicePackages: Array<{ path: string; name: string; hasNodeDeps: boolean }> = [];
  
  // Analyze each package.json
  for (const filePath of packageJsonFiles) {
    const packageJson = loadPackageJson(filePath);
    if (!packageJson) continue;
    
    const relativePath = path.relative('.', path.dirname(filePath));
    const isRootPackage = filePath === './package.json' || filePath === 'package.json';
    const isAppService = relativePath.startsWith('apps/');
    const isLibrary = relativePath.startsWith('libs/');
    
    // Skip the root package.json for dependency analysis
    if (isRootPackage) continue;
    
    const hasNodeDeps = Boolean(packageJson.dependencies || packageJson.devDependencies);
    servicePackages.push({
      path: relativePath,
      name: packageJson.name || path.basename(relativePath),
      hasNodeDeps
    });
    
    if (!hasNodeDeps) continue;
    
    // Process regular dependencies
    if (packageJson.dependencies) {
      for (const [depName, version] of Object.entries(packageJson.dependencies)) {
        // Skip catalog dependencies (N8N specific)
        if (version === 'catalog:') continue;
        
        if (!dependencyMap.has(depName)) {
          dependencyMap.set(depName, {
            version,
            services: [],
            isDev: false
          });
        }
        
        const depInfo = dependencyMap.get(depName)!;
        if (!depInfo.services.includes(relativePath)) {
          depInfo.services.push(relativePath);
        }
      }
    }
    
    // Process dev dependencies
    if (packageJson.devDependencies) {
      for (const [depName, version] of Object.entries(packageJson.devDependencies)) {
        // Skip catalog dependencies
        if (version === 'catalog:') continue;
        
        if (!dependencyMap.has(depName)) {
          dependencyMap.set(depName, {
            version,
            services: [],
            isDev: true
          });
        }
        
        const depInfo = dependencyMap.get(depName)!;
        if (!depInfo.services.includes(relativePath)) {
          depInfo.services.push(relativePath);
        }
        
        // Mark as dev dependency if it appears in devDependencies
        if (!depInfo.isDev) {
          depInfo.isDev = true;
        }
      }
    }
  }
  
  // Filter for overlapping dependencies (used by 2+ services)
  const overlappingDeps = Array.from(dependencyMap.entries())
    .filter(([_, info]) => info.services.length >= 2)
    .sort((a, b) => b[1].services.length - a[1].services.length);
  
  console.log('📊 Service Analysis:\n');
  
  // Group services by type
  const appServices = servicePackages.filter(s => s.path.startsWith('apps/'));
  const libServices = servicePackages.filter(s => s.path.startsWith('libs/'));
  const otherServices = servicePackages.filter(s => !s.path.startsWith('apps/') && !s.path.startsWith('libs/'));
  
  console.log(`   📱 App Services: ${appServices.length} (${appServices.filter(s => s.hasNodeDeps).length} with Node.js deps)`);
  console.log(`   📚 Libraries: ${libServices.length} (${libServices.filter(s => s.hasNodeDeps).length} with Node.js deps)`);
  console.log(`   🔧 Other: ${otherServices.length} (${otherServices.filter(s => s.hasNodeDeps).length} with Node.js deps)`);
  
  console.log('\n📦 Top Overlapping Dependencies:\n');
  
  if (overlappingDeps.length === 0) {
    console.log('   No overlapping dependencies found.');
  } else {
    overlappingDeps.slice(0, 20).forEach(([depName, info]) => {
      console.log(`   ${depName} (${info.services.length} services)${info.isDev ? ' [dev]' : ''}`);
      info.services.forEach(service => {
        console.log(`      • ${service}`);
      });
      console.log('');
    });
  }
  
  // Generate hoisting recommendations
  console.log('🎯 Hoisting Recommendations:\n');
  
  // Safe to hoist (3+ services, consistent versions)
  const safeToHoist = overlappingDeps.filter(([_, info]) => {
    if (info.services.length < 3) return false;
    
    // Check if all services use the same version
    const versions = new Set<string>();
    for (const servicePath of info.services) {
      const packageJsonPath = path.join(servicePath, 'package.json');
      const packageJson = loadPackageJson(packageJsonPath);
      if (packageJson) {
        const allDeps = { ...packageJson.dependencies, ...packageJson.devDependencies };
        if (allDeps[_]) {
          versions.add(allDeps[_]);
        }
      }
    }
    
    return versions.size === 1; // All services use same version
  });
  
  if (safeToHoist.length > 0) {
    console.log('   ✅ Safe to hoist (3+ services, same version):');
    safeToHoist.forEach(([depName, info]) => {
      console.log(`      • ${depName} (${info.services.length} services)`);
    });
  } else {
    console.log('   ⚠️  No dependencies are safe to hoist automatically.');
  }
  
  // Needs review (2+ services, different versions)
  const needsReview = overlappingDeps.filter(([depName, info]) => {
    if (info.services.length < 2) return false;
    
    const versions = new Set<string>();
    for (const servicePath of info.services) {
      const packageJsonPath = path.join(servicePath, 'package.json');
      const packageJson = loadPackageJson(packageJsonPath);
      if (packageJson) {
        const allDeps = { ...packageJson.dependencies, ...packageJson.devDependencies };
        if (allDeps[depName]) {
          versions.add(allDeps[depName]);
        }
      }
    }
    
    return versions.size > 1; // Different versions
  });
  
  if (needsReview.length > 0) {
    console.log('\n   ⚠️  Needs review (version conflicts):');
    needsReview.slice(0, 10).forEach(([depName, info]) => {
      console.log(`      • ${depName} (${info.services.length} services, different versions)`);
    });
  }
  
  console.log('\n==============================\n');
  
  return {
    totalServices: servicePackages.length,
    servicesWithDeps: servicePackages.filter(s => s.hasNodeDeps).length,
    overlappingDeps: overlappingDeps.length,
    safeToHoist: safeToHoist.length,
    needsReview: needsReview.length
  };
}

/**
 * Main function
 */
function main() {
  console.log('📋 Monorepo Dependency Analysis\n');
  console.log('==============================\n');
  
  const results = analyzeDependencies();
  
  console.log('🎯 Summary:\n');
  console.log(`   • Total services: ${results.totalServices}`);
  console.log(`   • Services with dependencies: ${results.servicesWithDeps}`);
  console.log(`   • Overlapping dependencies: ${results.overlappingDeps}`);
  console.log(`   • Safe to hoist: ${results.safeToHoist}`);
  console.log(`   • Need review: ${results.needsReview}\n`);
  
  if (results.safeToHoist > 0) {
    console.log('✅ Ready to proceed with automated hoisting!');
  } else {
    console.log('🔍 Consider manual dependency consolidation first.');
  }
  
  console.log('\n==============================\n');
}

// Run analysis
if (require.main === module) {
  main();
}

export { analyzeDependencies, findPackageJsonFiles };
