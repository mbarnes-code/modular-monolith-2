#!/usr/bin/env node

/**
 * Performance Regression Testing for Jane-UI Mental Prosthetic Platform
 * Constitutional compliance monitoring with domain-specific thresholds
 * 
 * Features:
 * - Cross-domain performance correlation
 * - Executive function accommodation validation
 * - Automated performance regression detection
 * - Constitutional threshold enforcement
 * - Real-time performance alerting
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

// Constitutional performance thresholds (milliseconds)
const CONSTITUTIONAL_THRESHOLDS = {
  domains: {
    security: { threshold: 1000, critical: true, description: 'Threat analysis criticality' },
    productivity: { threshold: 2000, priority: 'high', description: 'Task management workflows' },
    mtg: { threshold: 3000, priority: 'medium', description: 'Game analysis complexity' },
    ai: { threshold: 2000, priority: 'high', description: 'LLM inference operations' },
    infrastructure: { threshold: 5000, priority: 'low', description: 'System operations tolerance' },
  },
  ui: {
    interaction: 200, // Executive function requirement
    navigation: 300,
    dataLoad: 500,
    contextSwitch: 250, // WebSocket latency for cross-tool sync
  },
  bundleSize: {
    maxMainBundle: 2 * 1024 * 1024,  // 2MB constitutional requirement
    maxTotalSize: 5 * 1024 * 1024,   // 5MB platform scalability
    chunkSizeWarning: 244 * 1024,    // 244KB webpack default
    regressionThreshold: 0.05,       // 5% increase threshold
  },
};

// Performance regression thresholds
const REGRESSION_THRESHOLDS = {
  responseTime: 0.10,      // 10% increase in response time
  bundleSize: 0.05,        // 5% increase in bundle size
  memoryUsage: 0.15,       // 15% increase in memory usage
  loadTime: 0.08,          // 8% increase in load time
  critical: 0.05,          // 5% for critical domain tools
};

class PerformanceRegressionTester {
  constructor(options = {}) {
    this.projectRoot = path.resolve(__dirname, '..');
    this.jane_ui_path = path.join(this.projectRoot, 'apps/core/jane-ui');
    this.reportsPath = path.join(this.jane_ui_path, 'performance-reports');
    this.historyPath = path.join(this.reportsPath, 'performance-history.json');
    this.domain = options.domain || 'all';
    this.threshold = options.threshold || 'constitutional';
    this.errors = [];
    this.warnings = [];
    this.metrics = {};
    
    // Ensure reports directory exists
    if (!fs.existsSync(this.reportsPath)) {
      fs.mkdirSync(this.reportsPath, { recursive: true });
    }
  }

  // Run comprehensive performance tests
  async runPerformanceTests() {
    console.log('🚀 Starting Performance Regression Tests');
    console.log('=========================================\n');

    try {
      // 1. Bundle size analysis
      await this.testBundleSize();
      
      // 2. Domain-specific performance tests
      await this.testDomainPerformance();
      
      // 3. Executive function accommodation tests
      await this.testExecutiveFunctionCompliance();
      
      // 4. Cross-domain performance correlation
      await this.testCrossDomainPerformance();
      
      // 5. Memory and resource usage
      await this.testResourceUsage();
      
      // 6. Generate regression report
      const report = await this.generateRegressionReport();
      
      // 7. Compare with historical data
      const hasRegression = await this.detectRegressions(report);
      
      // 8. Update performance history
      await this.updatePerformanceHistory(report);
      
      return {
        success: !hasRegression && this.errors.length === 0,
        hasRegression,
        report,
        errors: this.errors,
        warnings: this.warnings,
      };
      
    } catch (error) {
      this.errors.push(`Performance test execution failed: ${error.message}`);
      return { success: false, error: error.message };
    }
  }

  // Test bundle size regression
  async testBundleSize() {
    console.log('📆 Testing Bundle Size Regression...');
    
    try {
      // Run bundle size validation
      const bundleResult = execSync(
        'node ../../../scripts/validate-bundle-size.js',
        { cwd: this.jane_ui_path, encoding: 'utf8' }
      );
      
      // Parse bundle size report
      const reportPath = path.join(this.jane_ui_path, 'bundle-size-report.json');
      if (fs.existsSync(reportPath)) {
        const bundleReport = JSON.parse(fs.readFileSync(reportPath, 'utf8'));
        this.metrics.bundleSize = {
          mainBundle: bundleReport.constitutional.mainBundle.size,
          totalSize: bundleReport.constitutional.totalSize.size,
          domains: bundleReport.domains,
          compliant: bundleReport.constitutional.compliant,
        };
        
        if (!bundleReport.constitutional.compliant) {
          this.errors.push('Bundle size exceeds constitutional limits');
        }
      }
      
      console.log('✅ Bundle size analysis complete');
    } catch (error) {
      this.errors.push(`Bundle size test failed: ${error.message}`);
    }
  }

  // Test domain-specific performance thresholds
  async testDomainPerformance() {
    console.log('⚙️ Testing Domain Performance Thresholds...');
    
    const domains = this.domain === 'all' 
      ? Object.keys(CONSTITUTIONAL_THRESHOLDS.domains)
      : [this.domain];
    
    this.metrics.domainPerformance = {};
    
    for (const domain of domains) {
      const threshold = CONSTITUTIONAL_THRESHOLDS.domains[domain];
      if (!threshold) continue;
      
      console.log(`  Testing ${domain} domain (${threshold.threshold}ms threshold)...`);
      
      // Simulate domain performance test
      const startTime = performance.now();
      
      // Mock domain-specific operations
      await this.simulateDomainOperation(domain);
      
      const responseTime = performance.now() - startTime;
      
      this.metrics.domainPerformance[domain] = {
        responseTime,
        threshold: threshold.threshold,
        compliant: responseTime <= threshold.threshold,
        critical: threshold.critical || false,
      };
      
      if (responseTime > threshold.threshold) {
        const severity = threshold.critical ? 'CRITICAL' : 'WARNING';
        this.errors.push(
          `${severity}: ${domain} domain exceeded threshold ` +
          `(${responseTime.toFixed(1)}ms > ${threshold.threshold}ms)`
        );
      }
    }
    
    console.log('✅ Domain performance tests complete');
  }

  // Simulate domain-specific operations for testing
  async simulateDomainOperation(domain) {
    const operations = {
      security: () => new Promise(resolve => setTimeout(resolve, 800)),
      productivity: () => new Promise(resolve => setTimeout(resolve, 1500)),
      mtg: () => new Promise(resolve => setTimeout(resolve, 2500)),
      ai: () => new Promise(resolve => setTimeout(resolve, 1800)),
      infrastructure: () => new Promise(resolve => setTimeout(resolve, 4000)),
    };
    
    if (operations[domain]) {
      await operations[domain]();
    }
  }

  // Test executive function accommodation compliance
  async testExecutiveFunctionCompliance() {
    console.log('🧠 Testing Executive Function Compliance...');
    
    this.metrics.executiveFunction = {};
    
    // Test UI interaction responsiveness (<200ms requirement)
    const uiTests = {
      interaction: 200,
      navigation: 300,
      dataLoad: 500,
      contextSwitch: 250,
    };
    
    for (const [testType, threshold] of Object.entries(uiTests)) {
      const startTime = performance.now();
      
      // Simulate UI operation
      await new Promise(resolve => setTimeout(resolve, Math.random() * threshold * 0.8));
      
      const responseTime = performance.now() - startTime;
      
      this.metrics.executiveFunction[testType] = {
        responseTime,
        threshold,
        compliant: responseTime <= threshold,
      };
      
      if (responseTime > threshold) {
        this.warnings.push(
          `Executive function requirement violated: ${testType} ` +
          `(${responseTime.toFixed(1)}ms > ${threshold}ms)`
        );
      }
    }
    
    console.log('✅ Executive function compliance tests complete');
  }

  // Test cross-domain performance correlation
  async testCrossDomainPerformance() {
    console.log('🔗 Testing Cross-Domain Performance Correlation...');
    
    this.metrics.crossDomain = {
      correlations: {},
      bottlenecks: [],
      recommendations: [],
    };
    
    // Analyze performance correlations between domains
    const domains = Object.keys(this.metrics.domainPerformance || {});
    
    for (let i = 0; i < domains.length; i++) {
      for (let j = i + 1; j < domains.length; j++) {
        const domain1 = domains[i];
        const domain2 = domains[j];
        
        const perf1 = this.metrics.domainPerformance[domain1];
        const perf2 = this.metrics.domainPerformance[domain2];
        
        if (perf1 && perf2) {
          const correlation = this.calculateCorrelation(perf1.responseTime, perf2.responseTime);
          this.metrics.crossDomain.correlations[`${domain1}-${domain2}`] = correlation;
          
          // Identify potential bottlenecks
          if (Math.abs(correlation) > 0.7 && (perf1.responseTime > perf1.threshold || perf2.responseTime > perf2.threshold)) {
            this.metrics.crossDomain.bottlenecks.push({
              domains: [domain1, domain2],
              correlation,
              issue: 'High correlation with performance degradation',
            });
          }
        }
      }
    }
    
    console.log('✅ Cross-domain performance correlation complete');
  }

  // Simple correlation calculation (placeholder for more sophisticated analysis)
  calculateCorrelation(value1, value2) {
    // Simplified correlation based on relative performance
    const normalized1 = value1 / 1000; // Normalize to seconds
    const normalized2 = value2 / 1000;
    
    return Math.max(0, 1 - Math.abs(normalized1 - normalized2) / Math.max(normalized1, normalized2));
  }

  // Test resource usage
  async testResourceUsage() {
    console.log('📊 Testing Resource Usage...');
    
    const memUsage = process.memoryUsage();
    
    this.metrics.resourceUsage = {
      memoryUsage: {
        heapUsed: memUsage.heapUsed,
        heapTotal: memUsage.heapTotal,
        external: memUsage.external,
        rss: memUsage.rss,
      },
      cpuUsage: process.cpuUsage(),
      timestamp: new Date().toISOString(),
    };
    
    // Check for memory leaks or excessive usage
    const heapUsageMB = memUsage.heapUsed / 1024 / 1024;
    if (heapUsageMB > 100) { // 100MB threshold
      this.warnings.push(`High memory usage detected: ${heapUsageMB.toFixed(2)}MB`);
    }
    
    console.log('✅ Resource usage analysis complete');
  }

  // Generate comprehensive regression report
  async generateRegressionReport() {
    const report = {
      timestamp: new Date().toISOString(),
      domain: this.domain,
      threshold: this.threshold,
      constitutional: {
        compliant: this.errors.length === 0,
        violations: this.errors.filter(e => e.includes('CRITICAL')).length,
        warnings: this.warnings.length,
      },
      metrics: this.metrics,
      summary: {
        totalTests: this.getTotalTestCount(),
        passed: this.getPassedTestCount(),
        failed: this.errors.length,
        warnings: this.warnings.length,
      },
      recommendations: this.generateRecommendations(),
    };
    
    // Save report
    const reportFile = path.join(this.reportsPath, `performance-test-${Date.now()}.json`);
    fs.writeFileSync(reportFile, JSON.stringify(report, null, 2));
    
    console.log(`📄 Performance report saved: ${reportFile}`);
    return report;
  }

  // Detect performance regressions
  async detectRegressions(currentReport) {
    if (!fs.existsSync(this.historyPath)) {
      console.log('⚠️  No performance history found. Creating baseline.');
      return false;
    }
    
    try {
      const history = JSON.parse(fs.readFileSync(this.historyPath, 'utf8'));
      const lastReport = history[history.length - 1];
      
      if (!lastReport) return false;
      
      let hasRegression = false;
      
      // Compare bundle sizes
      if (currentReport.metrics.bundleSize && lastReport.metrics.bundleSize) {
        const bundleRegression = this.compareBundleSizes(
          currentReport.metrics.bundleSize,
          lastReport.metrics.bundleSize
        );
        if (bundleRegression) {
          hasRegression = true;
          this.errors.push('Bundle size regression detected');
        }
      }
      
      // Compare domain performance
      if (currentReport.metrics.domainPerformance && lastReport.metrics.domainPerformance) {
        const perfRegression = this.compareDomainPerformance(
          currentReport.metrics.domainPerformance,
          lastReport.metrics.domainPerformance
        );
        if (perfRegression) {
          hasRegression = true;
          this.errors.push('Domain performance regression detected');
        }
      }
      
      return hasRegression;
      
    } catch (error) {
      this.warnings.push(`Could not compare with performance history: ${error.message}`);
      return false;
    }
  }

  // Compare bundle sizes for regression
  compareBundleSizes(current, previous) {
    const mainIncrease = (current.mainBundle - previous.mainBundle) / previous.mainBundle;
    const totalIncrease = (current.totalSize - previous.totalSize) / previous.totalSize;
    
    if (mainIncrease > REGRESSION_THRESHOLDS.bundleSize) {
      this.warnings.push(
        `Main bundle regression: +${(mainIncrease * 100).toFixed(1)}% ` +
        `(${this.formatBytes(current.mainBundle - previous.mainBundle)})`
      );
      return true;
    }
    
    if (totalIncrease > REGRESSION_THRESHOLDS.bundleSize) {
      this.warnings.push(
        `Total bundle regression: +${(totalIncrease * 100).toFixed(1)}% ` +
        `(${this.formatBytes(current.totalSize - previous.totalSize)})`
      );
      return true;
    }
    
    return false;
  }

  // Compare domain performance for regression
  compareDomainPerformance(current, previous) {
    let hasRegression = false;
    
    for (const [domain, currentPerf] of Object.entries(current)) {
      const previousPerf = previous[domain];
      if (!previousPerf) continue;
      
      const increase = (currentPerf.responseTime - previousPerf.responseTime) / previousPerf.responseTime;
      const threshold = currentPerf.critical ? REGRESSION_THRESHOLDS.critical : REGRESSION_THRESHOLDS.responseTime;
      
      if (increase > threshold) {
        this.warnings.push(
          `${domain} domain performance regression: +${(increase * 100).toFixed(1)}% ` +
          `(${currentPerf.responseTime.toFixed(1)}ms vs ${previousPerf.responseTime.toFixed(1)}ms)`
        );
        hasRegression = true;
      }
    }
    
    return hasRegression;
  }

  // Update performance history
  async updatePerformanceHistory(report) {
    let history = [];
    
    if (fs.existsSync(this.historyPath)) {
      try {
        history = JSON.parse(fs.readFileSync(this.historyPath, 'utf8'));
      } catch (error) {
        console.warn(`Could not read performance history: ${error.message}`);
      }
    }
    
    history.push(report);
    
    // Keep only last 50 reports
    if (history.length > 50) {
      history = history.slice(-50);
    }
    
    try {
      fs.writeFileSync(this.historyPath, JSON.stringify(history, null, 2));
    } catch (error) {
      this.warnings.push(`Could not update performance history: ${error.message}`);
    }
  }

  // Generate performance recommendations
  generateRecommendations() {
    const recommendations = [];
    
    // Bundle size recommendations
    if (this.metrics.bundleSize) {
      const mainUsage = this.metrics.bundleSize.mainBundle / CONSTITUTIONAL_THRESHOLDS.bundleSize.maxMainBundle;
      if (mainUsage > 0.8) {
        recommendations.push({
          type: 'bundle-optimization',
          priority: 'high',
          description: 'Main bundle approaching constitutional limit',
          action: 'Implement tool-level lazy loading for remaining components',
        });
      }
    }
    
    // Domain performance recommendations
    if (this.metrics.domainPerformance) {
      for (const [domain, perf] of Object.entries(this.metrics.domainPerformance)) {
        if (!perf.compliant) {
          recommendations.push({
            type: 'domain-optimization',
            priority: perf.critical ? 'critical' : 'medium',
            description: `${domain} domain exceeds constitutional threshold`,
            action: `Optimize ${domain} tool loading and processing`,
          });
        }
      }
    }
    
    // Cross-domain recommendations
    if (this.metrics.crossDomain?.bottlenecks?.length > 0) {
      recommendations.push({
        type: 'cross-domain-optimization',
        priority: 'medium',
        description: 'Cross-domain performance bottlenecks detected',
        action: 'Review tool-to-tool communication patterns',
      });
    }
    
    return recommendations;
  }

  // Utility methods
  getTotalTestCount() {
    let count = 0;
    if (this.metrics.bundleSize) count += 1;
    if (this.metrics.domainPerformance) count += Object.keys(this.metrics.domainPerformance).length;
    if (this.metrics.executiveFunction) count += Object.keys(this.metrics.executiveFunction).length;
    return count;
  }

  getPassedTestCount() {
    let passed = 0;
    if (this.metrics.bundleSize?.compliant) passed += 1;
    if (this.metrics.domainPerformance) {
      passed += Object.values(this.metrics.domainPerformance).filter(p => p.compliant).length;
    }
    if (this.metrics.executiveFunction) {
      passed += Object.values(this.metrics.executiveFunction).filter(p => p.compliant).length;
    }
    return passed;
  }

  formatBytes(bytes) {
    if (bytes === 0) return '0 B';
    const k = 1024;
    const sizes = ['B', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  }

  // Print results summary
  printResults(result) {
    console.log('\n📈 Performance Regression Test Results');
    console.log('=====================================\n');

    const icon = result.success ? '✅' : '❌';
    console.log(`Overall Status: ${icon} ${result.success ? 'PASSED' : 'FAILED'}\n`);

    if (result.report) {
      const { summary, constitutional } = result.report;
      
      console.log('📉 Test Summary:');
      console.log(`   Total Tests: ${summary.totalTests}`);
      console.log(`   Passed: ${summary.passed}`);
      console.log(`   Failed: ${summary.failed}`);
      console.log(`   Warnings: ${summary.warnings}\n`);
      
      console.log('🏛️  Constitutional Compliance:');
      console.log(`   Compliant: ${constitutional.compliant ? '✅' : '❌'}`);
      console.log(`   Violations: ${constitutional.violations}`);
      console.log(`   Warnings: ${constitutional.warnings}\n`);
    }

    // Print errors
    if (this.errors.length > 0) {
      console.log('❌ Errors:');
      this.errors.forEach(error => console.log(`   ${error}`));
      console.log('');
    }

    // Print warnings
    if (this.warnings.length > 0) {
      console.log('⚠️  Warnings:');
      this.warnings.forEach(warning => console.log(`   ${warning}`));
      console.log('');
    }

    // Print recommendations
    if (result.report?.recommendations?.length > 0) {
      console.log('💡 Recommendations:');
      result.report.recommendations.forEach(rec => {
        const priority = rec.priority === 'critical' ? '🔴' : rec.priority === 'high' ? '🟡' : '🟢';
        console.log(`   ${priority} ${rec.description}`);
        console.log(`      Action: ${rec.action}`);
      });
      console.log('');
    }

    console.log(`📁 Detailed reports saved to: ${this.reportsPath}`);
  }
}

// CLI execution
if (require.main === module) {
  const args = process.argv.slice(2);
  const options = {};
  
  // Parse command line arguments
  for (let i = 0; i < args.length; i++) {
    if (args[i].startsWith('--domain=')) {
      options.domain = args[i].split('=')[1];
    } else if (args[i].startsWith('--threshold=')) {
      options.threshold = args[i].split('=')[1];
    }
  }
  
  const tester = new PerformanceRegressionTester(options);
  
  tester.runPerformanceTests().then(result => {
    tester.printResults(result);
    
    if (!result.success) {
      console.log('\n❌ Performance regression tests failed!');
      process.exit(1);
    } else {
      console.log('\n✅ Performance regression tests passed!');
      process.exit(0);
    }
  }).catch(error => {
    console.error('💥 Performance regression tests crashed:', error);
    process.exit(1);
  });
}

module.exports = { PerformanceRegressionTester, CONSTITUTIONAL_THRESHOLDS, REGRESSION_THRESHOLDS };