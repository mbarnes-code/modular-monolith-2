#!/usr/bin/env node

/**
 * Bundle Size Measurement and Validation Script
 * Constitutional compliance for Jane-UI mental prosthetic platform
 * 
 * Enforces:
 * - Main bundle <2MB (constitutional requirement)
 * - Total bundle size <5MB (platform scalability)
 * - Domain chunk size monitoring (security, productivity, mtg, ai)
 * - Progressive warnings at 50%, 80%, 100% thresholds
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

// Constitutional thresholds (bytes)
const BUNDLE_THRESHOLDS = {
  maxMainBundle: 2 * 1024 * 1024,     // 2MB - constitutional requirement
  maxTotalSize: 5 * 1024 * 1024,     // 5MB - platform scalability
  chunkSizeWarning: 244 * 1024,      // 244KB - webpack default
  domainChunkLimits: {
    'security-tools': 1.5 * 1024 * 1024,    // 1.5MB - critical response <1s
    'productivity-tools': 1 * 1024 * 1024,   // 1MB - workflow efficiency <2s
    'mtg-tools': 800 * 1024,                 // 800KB - analysis complexity <3s
    'ai-tools': 1.2 * 1024 * 1024,          // 1.2MB - AI processing overhead
    'vendor': 2 * 1024 * 1024,              // 2MB - external dependencies
  }
};

// Warning thresholds (percentages)
const WARNING_LEVELS = {
  info: 0.5,      // 50% - informational
  warn: 0.8,      // 80% - warning
  error: 1.0,     // 100% - error/critical
  critical: 1.2   // 120% - build failure
};

class BundleSizeAnalyzer {
  constructor(projectPath, validate = false) {
    this.projectPath = projectPath;
    this.validate = validate;
    this.buildDir = path.join(projectPath, '.next');
    this.staticDir = path.join(this.buildDir, 'static', 'chunks');
    this.violations = [];
    this.recommendations = [];
  }

  /**
   * Main analysis entry point
   */
  async analyze() {
    console.log('🔍 Analyzing bundle sizes for Jane-UI...');
    
    // Ensure build exists
    if (!fs.existsSync(this.buildDir)) {
      throw new Error('Build directory not found. Run "npm run build" first.');
    }

    // Collect bundle metrics
    const metrics = await this.collectBundleMetrics();
    
    // Validate against thresholds
    const report = this.validateThresholds(metrics);
    
    // Generate recommendations
    this.generateRecommendations(metrics, report);
    
    // Output results
    this.outputResults(metrics, report);
    
    // Handle validation mode
    if (this.validate && this.violations.length > 0) {
      process.exit(1);
    }
    
    return { metrics, report, violations: this.violations };
  }

  /**
   * Collect bundle size metrics from build output
   */
  async collectBundleMetrics() {
    const metrics = {
      mainBundleSize: 0,
      totalBundleSize: 0,
      domainChunks: {},
      allChunks: {},
      timestamp: new Date().toISOString()
    };

    // Read static chunks directory
    if (!fs.existsSync(this.staticDir)) {
      console.warn('⚠️  Static chunks directory not found');
      return metrics;
    }

    const chunkFiles = fs.readdirSync(this.staticDir)
      .filter(file => file.endsWith('.js'))
      .map(file => {
        const filePath = path.join(this.staticDir, file);
        const stats = fs.statSync(filePath);
        return {
          name: file,
          size: stats.size,
          path: filePath
        };
      });

    // Process each chunk
    for (const chunk of chunkFiles) {
      metrics.allChunks[chunk.name] = chunk.size;
      metrics.totalBundleSize += chunk.size;

      // Identify main bundle (typically the largest or contains 'main')
      if (chunk.name.includes('main') || chunk.name.includes('app')) {
        metrics.mainBundleSize = Math.max(metrics.mainBundleSize, chunk.size);
      }

      // Categorize domain chunks
      this.categorizeDomainChunk(chunk, metrics.domainChunks);
    }

    // If no explicit main bundle found, use largest chunk
    if (metrics.mainBundleSize === 0 && chunkFiles.length > 0) {
      const largestChunk = chunkFiles.reduce((prev, current) => 
        current.size > prev.size ? current : prev
      );
      metrics.mainBundleSize = largestChunk.size;
      console.log(`📊 Using largest chunk as main bundle: ${largestChunk.name}`);
    }

    return metrics;
  }

  /**
   * Categorize chunks by domain for specialized monitoring
   */
  categorizeDomainChunk(chunk, domainChunks) {
    const chunkName = chunk.name.toLowerCase();
    
    // Domain-specific chunk patterns
    const domainPatterns = {
      'security-tools': ['security', 'misp', 'helk', 'maltrail', 'nemesis', 'yara'],
      'productivity-tools': ['productivity', 'n8n', 'mealie', 'dispatch', 'actual'],
      'mtg-tools': ['mtg', 'tcg', 'commander', 'spellbook'],
      'ai-tools': ['ai', 'llm', 'mcp', 'chroma'],
      'vendor': ['vendor', 'node_modules', 'runtime', 'webpack']
    };

    for (const [domain, patterns] of Object.entries(domainPatterns)) {
      if (patterns.some(pattern => chunkName.includes(pattern))) {
        if (!domainChunks[domain]) {
          domainChunks[domain] = { size: 0, chunks: [] };
        }
        domainChunks[domain].size += chunk.size;
        domainChunks[domain].chunks.push(chunk.name);
        return;
      }
    }

    // Uncategorized chunks
    if (!domainChunks['other']) {
      domainChunks['other'] = { size: 0, chunks: [] };
    }
    domainChunks['other'].size += chunk.size;
    domainChunks['other'].chunks.push(chunk.name);
  }

  /**
   * Validate bundle sizes against constitutional thresholds
   */
  validateThresholds(metrics) {
    const report = {
      mainBundle: this.validateSize('Main Bundle', metrics.mainBundleSize, BUNDLE_THRESHOLDS.maxMainBundle),
      totalSize: this.validateSize('Total Bundle Size', metrics.totalBundleSize, BUNDLE_THRESHOLDS.maxTotalSize),
      domainChunks: {},
      overallCompliance: true
    };

    // Validate domain-specific chunks
    for (const [domain, data] of Object.entries(metrics.domainChunks)) {
      const limit = BUNDLE_THRESHOLDS.domainChunkLimits[domain];
      if (limit) {
        report.domainChunks[domain] = this.validateSize(
          `${domain.charAt(0).toUpperCase() + domain.slice(1)} Chunks`, 
          data.size, 
          limit
        );
      }
    }

    // Check overall compliance
    report.overallCompliance = !this.violations.some(v => v.severity === 'critical' || v.severity === 'error');

    return report;
  }

  /**
   * Validate individual size against threshold with progressive warnings
   */
  validateSize(name, actualSize, threshold) {
    const ratio = actualSize / threshold;
    const result = {
      name,
      actualSize,
      threshold,
      ratio,
      status: 'ok',
      severity: 'info'
    };

    // Determine status and severity
    if (ratio >= WARNING_LEVELS.critical) {
      result.status = 'critical';
      result.severity = 'critical';
      this.violations.push({
        type: 'bundle_size',
        name,
        message: `${name} (${this.formatSize(actualSize)}) exceeds critical threshold (${this.formatSize(threshold)}) by ${((ratio - 1) * 100).toFixed(1)}%`,
        actualSize,
        threshold,
        severity: 'critical'
      });
    } else if (ratio >= WARNING_LEVELS.error) {
      result.status = 'error';
      result.severity = 'error';
      this.violations.push({
        type: 'bundle_size',
        name,
        message: `${name} (${this.formatSize(actualSize)}) exceeds threshold (${this.formatSize(threshold)}) by ${((ratio - 1) * 100).toFixed(1)}%`,
        actualSize,
        threshold,
        severity: 'error'
      });
    } else if (ratio >= WARNING_LEVELS.warn) {
      result.status = 'warning';
      result.severity = 'warn';
      console.warn(`⚠️  ${name} approaching threshold: ${this.formatSize(actualSize)} / ${this.formatSize(threshold)} (${(ratio * 100).toFixed(1)}%)`);
    } else if (ratio >= WARNING_LEVELS.info) {
      result.status = 'info';
      result.severity = 'info';
      console.log(`ℹ️  ${name} at ${(ratio * 100).toFixed(1)}% of threshold`);
    }

    return result;
  }

  /**
   * Generate optimization recommendations based on analysis
   */
  generateRecommendations(metrics, report) {
    // Main bundle size recommendations
    if (report.mainBundle.ratio > WARNING_LEVELS.warn) {
      this.recommendations.push({
        type: 'optimization',
        priority: 'high',
        message: 'Consider implementing tool-level lazy loading to reduce main bundle size',
        details: 'Move tool components to dynamic imports: import(\'./components/SecurityTools\')'
      });
    }

    // Total size recommendations
    if (report.totalSize.ratio > WARNING_LEVELS.warn) {
      this.recommendations.push({
        type: 'optimization',
        priority: 'high',
        message: 'Enable aggressive code splitting and tree shaking',
        details: 'Review webpack.config.js splitChunks configuration and eliminate unused exports'
      });
    }

    // Domain-specific recommendations
    for (const [domain, validation] of Object.entries(report.domainChunks)) {
      if (validation.ratio > WARNING_LEVELS.warn) {
        this.recommendations.push({
          type: 'domain_optimization',
          priority: 'medium',
          domain,
          message: `${domain} chunks are large - consider domain-specific lazy loading`,
          details: `Break down ${domain} into smaller, on-demand loaded components`
        });
      }
    }

    // Vendor chunk recommendations
    if (metrics.domainChunks.vendor && metrics.domainChunks.vendor.size > BUNDLE_THRESHOLDS.domainChunkLimits.vendor) {
      this.recommendations.push({
        type: 'dependency_optimization',
        priority: 'medium',
        message: 'Vendor bundle is large - audit dependencies',
        details: 'Use bundle analyzer to identify large dependencies and consider alternatives'
      });
    }
  }

  /**
   * Output comprehensive results
   */
  outputResults(metrics, report) {
    console.log('\n📊 Bundle Size Analysis Results');
    console.log('================================');
    
    // Main metrics
    console.log(`\n🎯 Core Metrics:`);
    console.log(`   Main Bundle: ${this.formatSize(metrics.mainBundleSize)} / ${this.formatSize(BUNDLE_THRESHOLDS.maxMainBundle)} (${this.getStatusIcon(report.mainBundle.status)})`);
    console.log(`   Total Size:  ${this.formatSize(metrics.totalBundleSize)} / ${this.formatSize(BUNDLE_THRESHOLDS.maxTotalSize)} (${this.getStatusIcon(report.totalSize.status)})`);
    
    // Domain chunks
    if (Object.keys(metrics.domainChunks).length > 0) {
      console.log(`\n🏗️  Domain Chunks:`);
      for (const [domain, data] of Object.entries(metrics.domainChunks)) {
        const validation = report.domainChunks[domain];
        const status = validation ? this.getStatusIcon(validation.status) : '📦';
        console.log(`   ${domain}: ${this.formatSize(data.size)} (${data.chunks.length} chunks) ${status}`);
      }
    }

    // Violations
    if (this.violations.length > 0) {
      console.log(`\n❌ Violations (${this.violations.length}):`);
      this.violations.forEach(violation => {
        const icon = violation.severity === 'critical' ? '🚨' : violation.severity === 'error' ? '❌' : '⚠️';
        console.log(`   ${icon} ${violation.message}`);
      });
    } else {
      console.log(`\n✅ All bundle size thresholds met!`);
    }

    // Recommendations
    if (this.recommendations.length > 0) {
      console.log(`\n💡 Recommendations (${this.recommendations.length}):`);
      this.recommendations.forEach(rec => {
        const icon = rec.priority === 'high' ? '🔥' : rec.priority === 'medium' ? '📋' : 'ℹ️';
        console.log(`   ${icon} ${rec.message}`);
        if (rec.details) {
          console.log(`      ${rec.details}`);
        }
      });
    }

    // Constitutional compliance summary
    console.log(`\n🏛️  Constitutional Compliance: ${report.overallCompliance ? '✅ COMPLIANT' : '❌ VIOLATIONS'}`);
    
    // Write JSON report for CI consumption
    this.writeJSONReport(metrics, report);
  }

  /**
   * Write structured JSON report for CI/CD consumption
   */
  writeJSONReport(metrics, report) {
    const jsonReport = {
      timestamp: metrics.timestamp,
      constitutional_compliance: report.overallCompliance,
      constitutional: {
        mainBundle: {
          size: metrics.mainBundleSize,
          limit: BUNDLE_THRESHOLDS.maxMainBundle,
          compliant: metrics.mainBundleSize <= BUNDLE_THRESHOLDS.maxMainBundle
        },
        totalSize: {
          size: metrics.totalBundleSize,
          limit: BUNDLE_THRESHOLDS.maxTotalSize,
          compliant: metrics.totalBundleSize <= BUNDLE_THRESHOLDS.maxTotalSize
        }
      },
      metrics: {
        main_bundle_size: metrics.mainBundleSize,
        total_bundle_size: metrics.totalBundleSize,
        domain_chunks: metrics.domainChunks,
        all_chunks: metrics.allChunks
      },
      thresholds: BUNDLE_THRESHOLDS,
      violations: this.violations,
      recommendations: this.recommendations,
      validation_summary: {
        main_bundle: report.mainBundle,
        total_size: report.totalSize,
        domain_chunks: report.domainChunks
      }
    };

    const reportPath = path.join(this.projectPath, 'bundle-size-report.json');
    fs.writeFileSync(reportPath, JSON.stringify(jsonReport, null, 2));
    console.log(`\n📄 Detailed report saved: ${reportPath}`);
  }

  /**
   * Utility methods
   */
  formatSize(bytes) {
    if (bytes === 0) return '0 B';
    const k = 1024;
    const sizes = ['B', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  }

  getStatusIcon(status) {
    const icons = {
      ok: '✅',
      info: 'ℹ️',
      warning: '⚠️',
      error: '❌',
      critical: '🚨'
    };
    return icons[status] || '❓';
  }
}

// CLI Interface
async function main() {
  const args = process.argv.slice(2);
  const validate = args.includes('--validate');
  const projectPath = args.find(arg => arg.startsWith('--project='))?.split('=')[1] || 
                     path.join(__dirname, '..', 'apps', 'core', 'jane-ui');

  try {
    const analyzer = new BundleSizeAnalyzer(projectPath, validate);
    await analyzer.analyze();
    
    if (validate) {
      console.log('\n✅ Bundle size validation completed successfully');
    }
  } catch (error) {
    console.error('\n❌ Bundle size analysis failed:', error.message);
    process.exit(1);
  }
}

// Run if called directly
if (require.main === module) {
  main().catch(error => {
    console.error('Fatal error:', error);
    process.exit(1);
  });
}

module.exports = { BundleSizeAnalyzer, BUNDLE_THRESHOLDS };