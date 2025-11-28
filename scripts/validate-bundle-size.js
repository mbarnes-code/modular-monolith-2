#!/usr/bin/env node

/**
 * Automated Bundle Size Validation for Jane-UI
 * Constitutional compliance monitoring with CI/CD integration
 * 
 * Features:
 * - Constitutional threshold enforcement (2MB main, 5MB total)
 * - Domain-specific chunk validation
 * - Performance regression detection
 * - CI/CD integration with exit codes
 * - Progressive warnings for bundle growth
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

// Constitutional bundle size limits
const BUNDLE_LIMITS = {
  mainBundle: 2 * 1024 * 1024, // 2MB
  totalSize: 5 * 1024 * 1024,  // 5MB
  chunkWarning: 244 * 1024,    // 244KB (webpack default)
  domainChunks: {
    'security-tools': 500 * 1024,    // 500KB
    'productivity-tools': 400 * 1024, // 400KB
    'mtg-tools': 300 * 1024,         // 300KB
    'ai-tools': 350 * 1024,          // 350KB
    'infrastructure-tools': 200 * 1024, // 200KB
  },
};

// Performance regression thresholds
const REGRESSION_THRESHOLDS = {
  mainBundleIncrease: 0.05,    // 5% increase
  totalSizeIncrease: 0.03,     // 3% increase
  newChunkSizeLimit: 100 * 1024, // 100KB for new chunks
};

class BundleSizeValidator {
  constructor() {
    this.projectRoot = path.resolve(__dirname, '..');
    this.jane_ui_path = path.join(this.projectRoot, 'apps/core/jane-ui');
    this.buildPath = path.join(this.jane_ui_path, '.next');
    this.reportPath = path.join(this.jane_ui_path, 'bundle-size-report.json');
    this.historyPath = path.join(this.jane_ui_path, 'bundle-size-history.json');
    this.errors = [];
    this.warnings = [];
  }

  // Check if build exists and is recent
  validateBuildExists() {
    if (!fs.existsSync(this.buildPath)) {
      this.errors.push('❌ No build found. Run `npx nx build jane-ui` first.');
      return false;
    }

    const buildStat = fs.statSync(this.buildPath);
    const buildAge = Date.now() - buildStat.mtime.getTime();
    const maxAge = 10 * 60 * 1000; // 10 minutes

    if (buildAge > maxAge) {
      this.warnings.push('⚠️  Build is older than 10 minutes. Consider rebuilding for accurate results.');
    }

    return true;
  }

  // Analyze bundle sizes from Next.js build
  analyzeBundleSizes() {
    try {
      // Run Next.js build analysis
      const buildManifest = path.join(this.buildPath, 'static/chunks/manifest.json');
      const buildId = this.getBuildId();
      
      if (!buildId) {
        this.errors.push('❌ Could not determine build ID');
        return null;
      }

      const analysis = this.parseNextJSBundle(buildId);
      return analysis;
    } catch (error) {
      this.errors.push(`❌ Bundle analysis failed: ${error.message}`);
      return null;
    }
  }

  // Get Next.js build ID
  getBuildId() {
    try {
      const buildIdPath = path.join(this.buildPath, 'BUILD_ID');
      if (fs.existsSync(buildIdPath)) {
        return fs.readFileSync(buildIdPath, 'utf8').trim();
      }
      return null;
    } catch (error) {
      return null;
    }
  }

  // Parse Next.js bundle for size analysis
  parseNextJSBundle(buildId) {
    const staticPath = path.join(this.buildPath, 'static');
    const chunksPath = path.join(staticPath, 'chunks');
    
    let totalSize = 0;
    const chunks = {};
    const domainChunks = {};

    // Analyze chunks directory
    if (fs.existsSync(chunksPath)) {
      const files = this.getAllFiles(chunksPath);
      
      for (const file of files) {
        if (file.endsWith('.js')) {
          const stat = fs.statSync(file);
          const relativePath = path.relative(chunksPath, file);
          const size = stat.size;
          
          totalSize += size;
          chunks[relativePath] = size;
          
          // Categorize domain chunks
          this.categorizeDomainChunk(relativePath, size, domainChunks);
        }
      }
    }

    // Analyze pages directory
    const pagesPath = path.join(this.buildPath, 'static/chunks/pages');
    if (fs.existsSync(pagesPath)) {
      const files = this.getAllFiles(pagesPath);
      
      for (const file of files) {
        if (file.endsWith('.js')) {
          const stat = fs.statSync(file);
          totalSize += stat.size;
        }
      }
    }

    // Find main bundle (largest chunk or _app chunk)
    const mainBundle = this.identifyMainBundle(chunks);

    return {
      totalSize,
      mainBundle,
      chunks,
      domainChunks,
      timestamp: new Date().toISOString(),
      buildId,
    };
  }

  // Get all files recursively
  getAllFiles(dir) {
    const files = [];
    
    if (!fs.existsSync(dir)) {
      return files;
    }

    const items = fs.readdirSync(dir);
    
    for (const item of items) {
      const fullPath = path.join(dir, item);
      const stat = fs.statSync(fullPath);
      
      if (stat.isDirectory()) {
        files.push(...this.getAllFiles(fullPath));
      } else {
        files.push(fullPath);
      }
    }
    
    return files;
  }

  // Categorize chunks by domain
  categorizeDomainChunk(chunkPath, size, domainChunks) {
    const domains = [
      { name: 'security-tools', pattern: /(security|Security|dispatch|nemesis|cyberchef|misp|helk|maltrail|ghostwriter|yara|rita)/i },
      { name: 'productivity-tools', pattern: /(productivity|Productivity|mealie|actual|n8n|inspector|firecrawl|spec-kit)/i },
      { name: 'mtg-tools', pattern: /(mtg|MTG|tcg|commander|spellbook|scripting)/i },
      { name: 'ai-tools', pattern: /(ai|AI|chroma|goose|vllm|llm)/i },
      { name: 'infrastructure-tools', pattern: /(infrastructure|Infrastructure|kasmvnc|kong)/i },
    ];

    for (const domain of domains) {
      if (domain.pattern.test(chunkPath)) {
        if (!domainChunks[domain.name]) {
          domainChunks[domain.name] = { size: 0, chunks: [] };
        }
        domainChunks[domain.name].size += size;
        domainChunks[domain.name].chunks.push({ path: chunkPath, size });
        return;
      }
    }

    // Vendor/other chunks
    const vendorDomain = 'vendor';
    if (!domainChunks[vendorDomain]) {
      domainChunks[vendorDomain] = { size: 0, chunks: [] };
    }
    domainChunks[vendorDomain].size += size;
    domainChunks[vendorDomain].chunks.push({ path: chunkPath, size });
  }

  // Identify main bundle from chunks
  identifyMainBundle(chunks) {
    // Look for _app or main chunks
    const appChunk = Object.entries(chunks).find(([path]) => 
      path.includes('_app') || path.includes('main')
    );
    
    if (appChunk) {
      return { path: appChunk[0], size: appChunk[1] };
    }

    // Fall back to largest chunk
    const largestChunk = Object.entries(chunks)
      .sort(([,a], [,b]) => b - a)[0];
    
    return largestChunk ? { path: largestChunk[0], size: largestChunk[1] } : null;
  }

  // Validate against constitutional limits
  validateConstitutionalCompliance(analysis) {
    let compliant = true;

    // Main bundle size check
    if (analysis.mainBundle && analysis.mainBundle.size > BUNDLE_LIMITS.mainBundle) {
      this.errors.push(
        `❌ CONSTITUTIONAL VIOLATION: Main bundle (${this.formatSize(analysis.mainBundle.size)}) ` +
        `exceeds limit (${this.formatSize(BUNDLE_LIMITS.mainBundle)})`
      );
      compliant = false;
    }

    // Total size check
    if (analysis.totalSize > BUNDLE_LIMITS.totalSize) {
      this.errors.push(
        `❌ CONSTITUTIONAL VIOLATION: Total bundle size (${this.formatSize(analysis.totalSize)}) ` +
        `exceeds limit (${this.formatSize(BUNDLE_LIMITS.totalSize)})`
      );
      compliant = false;
    }

    // Domain chunk checks
    for (const [domain, info] of Object.entries(analysis.domainChunks)) {
      const limit = BUNDLE_LIMITS.domainChunks[domain];
      if (limit && info.size > limit) {
        this.errors.push(
          `❌ Domain chunk '${domain}' (${this.formatSize(info.size)}) ` +
          `exceeds limit (${this.formatSize(limit)})`
        );
        compliant = false;
      }
    }

    // Individual chunk warnings
    for (const [chunkPath, size] of Object.entries(analysis.chunks)) {
      if (size > BUNDLE_LIMITS.chunkWarning) {
        this.warnings.push(
          `⚠️  Large chunk detected: ${chunkPath} (${this.formatSize(size)})`
        );
      }
    }

    return compliant;
  }

  // Check for performance regressions
  checkPerformanceRegression(currentAnalysis) {
    if (!fs.existsSync(this.historyPath)) {
      this.warnings.push('⚠️  No bundle size history found. Creating baseline.');
      return true;
    }

    try {
      const history = JSON.parse(fs.readFileSync(this.historyPath, 'utf8'));
      const lastAnalysis = history[history.length - 1];
      
      if (!lastAnalysis) {
        return true;
      }

      let hasRegression = false;

      // Check main bundle regression
      if (currentAnalysis.mainBundle && lastAnalysis.mainBundle) {
        const increase = (currentAnalysis.mainBundle.size - lastAnalysis.mainBundle.size) / lastAnalysis.mainBundle.size;
        if (increase > REGRESSION_THRESHOLDS.mainBundleIncrease) {
          this.warnings.push(
            `⚠️  Main bundle regression: +${(increase * 100).toFixed(1)}% ` +
            `(${this.formatSize(currentAnalysis.mainBundle.size - lastAnalysis.mainBundle.size)})`
          );
          hasRegression = true;
        }
      }

      // Check total size regression
      const totalIncrease = (currentAnalysis.totalSize - lastAnalysis.totalSize) / lastAnalysis.totalSize;
      if (totalIncrease > REGRESSION_THRESHOLDS.totalSizeIncrease) {
        this.warnings.push(
          `⚠️  Total size regression: +${(totalIncrease * 100).toFixed(1)}% ` +
          `(${this.formatSize(currentAnalysis.totalSize - lastAnalysis.totalSize)})`
        );
        hasRegression = true;
      }

      return !hasRegression;
    } catch (error) {
      this.warnings.push(`⚠️  Could not check performance regression: ${error.message}`);
      return true;
    }
  }

  // Update bundle size history
  updateHistory(analysis) {
    let history = [];
    
    if (fs.existsSync(this.historyPath)) {
      try {
        history = JSON.parse(fs.readFileSync(this.historyPath, 'utf8'));
      } catch (error) {
        this.warnings.push(`⚠️  Could not read history: ${error.message}`);
      }
    }

    history.push(analysis);
    
    // Keep only last 50 builds
    if (history.length > 50) {
      history = history.slice(-50);
    }

    try {
      fs.writeFileSync(this.historyPath, JSON.stringify(history, null, 2));
    } catch (error) {
      this.warnings.push(`⚠️  Could not update history: ${error.message}`);
    }
  }

  // Generate detailed report
  generateReport(analysis, compliant, regressionFree) {
    const report = {
      timestamp: analysis.timestamp,
      buildId: analysis.buildId,
      constitutional: {
        compliant,
        mainBundle: {
          size: analysis.mainBundle?.size || 0,
          limit: BUNDLE_LIMITS.mainBundle,
          usage: ((analysis.mainBundle?.size || 0) / BUNDLE_LIMITS.mainBundle * 100).toFixed(1) + '%',
        },
        totalSize: {
          size: analysis.totalSize,
          limit: BUNDLE_LIMITS.totalSize,
          usage: (analysis.totalSize / BUNDLE_LIMITS.totalSize * 100).toFixed(1) + '%',
        },
      },
      performance: {
        regressionFree,
      },
      domains: {},
      chunks: analysis.chunks,
      errors: this.errors,
      warnings: this.warnings,
    };

    // Add domain analysis
    for (const [domain, info] of Object.entries(analysis.domainChunks)) {
      report.domains[domain] = {
        size: info.size,
        chunks: info.chunks.length,
        limit: BUNDLE_LIMITS.domainChunks[domain] || null,
      };
    }

    // Save report
    try {
      fs.writeFileSync(this.reportPath, JSON.stringify(report, null, 2));
    } catch (error) {
      this.warnings.push(`⚠️  Could not save report: ${error.message}`);
    }

    return report;
  }

  // Format bytes as human readable
  formatSize(bytes) {
    if (bytes === 0) return '0 B';
    const k = 1024;
    const sizes = ['B', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  }

  // Print results to console
  printResults(report) {
    console.log('\n🔍 Bundle Size Validation Results');
    console.log('================================\n');

    // Constitutional compliance
    const complianceIcon = report.constitutional.compliant ? '✅' : '❌';
    console.log(`🏛️  Constitutional Compliance: ${complianceIcon} ${report.constitutional.compliant ? 'COMPLIANT' : 'VIOLATION'}\n`);

    // Core metrics
    console.log('🎯 Core Metrics:');
    console.log(`   Main Bundle: ${this.formatSize(report.constitutional.mainBundle.size)} / ${this.formatSize(report.constitutional.mainBundle.limit)} (${report.constitutional.mainBundle.usage})`);
    console.log(`   Total Size:  ${this.formatSize(report.constitutional.totalSize.size)} / ${this.formatSize(report.constitutional.totalSize.limit)} (${report.constitutional.totalSize.usage})\n`);

    // Domain breakdown
    console.log('🏗️  Domain Breakdown:');
    for (const [domain, info] of Object.entries(report.domains)) {
      const status = info.limit && info.size > info.limit ? '❌' : '✅';
      console.log(`   ${domain}: ${this.formatSize(info.size)} (${info.chunks} chunks) ${status}`);
    }
    console.log('');

    // Errors
    if (this.errors.length > 0) {
      console.log('❌ Errors:');
      this.errors.forEach(error => console.log(`   ${error}`));
      console.log('');
    }

    // Warnings
    if (this.warnings.length > 0) {
      console.log('⚠️  Warnings:');
      this.warnings.forEach(warning => console.log(`   ${warning}`));
      console.log('');
    }

    console.log(`📄 Detailed report saved: ${this.reportPath}`);
  }

  // Main validation process
  async validate() {
    console.log('🔍 Starting bundle size validation...');

    // Check if build exists
    if (!this.validateBuildExists()) {
      return { success: false, errors: this.errors };
    }

    // Analyze bundle sizes
    const analysis = this.analyzeBundleSizes();
    if (!analysis) {
      return { success: false, errors: this.errors };
    }

    // Validate constitutional compliance
    const compliant = this.validateConstitutionalCompliance(analysis);
    
    // Check performance regression
    const regressionFree = this.checkPerformanceRegression(analysis);
    
    // Update history
    this.updateHistory(analysis);
    
    // Generate and save report
    const report = this.generateReport(analysis, compliant, regressionFree);
    
    // Print results
    this.printResults(report);
    
    const success = compliant && this.errors.length === 0;
    
    return {
      success,
      compliant,
      regressionFree,
      report,
      errors: this.errors,
      warnings: this.warnings,
    };
  }
}

// CLI execution
if (require.main === module) {
  const validator = new BundleSizeValidator();
  
  validator.validate().then(result => {
    if (!result.success) {
      console.log('\n❌ Bundle size validation failed!');
      process.exit(1);
    } else {
      console.log('\n✅ Bundle size validation passed!');
      process.exit(0);
    }
  }).catch(error => {
    console.error('💥 Validation crashed:', error);
    process.exit(1);
  });
}

module.exports = { BundleSizeValidator, BUNDLE_LIMITS, REGRESSION_THRESHOLDS };