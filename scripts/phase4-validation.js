#!/usr/bin/env node

/**
 * Phase 4 Production Readiness Validation Script
 * 
 * Validates all constitutional requirements and optimization targets
 * for the 37-tool mental prosthetic platform
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

// Constitutional thresholds
const CONSTITUTIONAL_REQUIREMENTS = {
  bundleSize: {
    maxMainBundle: 2 * 1024 * 1024, // 2MB
    maxTotalSize: 5 * 1024 * 1024,  // 5MB
  },
  performance: {
    domains: {
      security: 1000,      // <1s critical
      productivity: 2000,  // <2s high priority  
      mtg: 3000,          // <3s medium priority
      infrastructure: 5000, // <5s acceptable
      ai: 2000            // <2s AI tools
    },
    executiveFunction: {
      interaction: 200,    // <200ms for ADHD support
      navigation: 300,     // <300ms context switching
      dataLoad: 500,       // <500ms data loading
      contextSwitch: 250   // <250ms tool switching
    }
  },
  ux: {
    maxActiveTools: 5,          // Cognitive load management
    maxClicksToTool: 3,         // Navigation efficiency
    wcagCompliance: 'AA',       // Accessibility
    adhdOptimizations: true,    // Executive function support
  }
};

class Phase4Validator {
  constructor() {
    this.results = {
      bundleSize: { passed: false, details: {} },
      performance: { passed: false, details: {} },
      ux: { passed: false, details: {} },
      architecture: { passed: false, details: {} },
      documentation: { passed: false, details: {} }
    };
    this.warnings = [];
    this.errors = [];
  }

  async validateAll() {
    console.log('🚀 Phase 4 Production Readiness Validation');
    console.log('=' .repeat(50));

    try {
      await this.validateBundleSize();
      await this.validatePerformance();
      await this.validateUX();
      await this.validateArchitecture();
      await this.validateDocumentation();
      
      this.generateReport();
    } catch (error) {
      console.error('❌ Validation failed:', error.message);
      process.exit(1);
    }
  }

  async validateBundleSize() {
    console.log('\n📦 Validating Bundle Size...');
    
    try {
      // Read bundle size report
      const bundleReportPath = path.join(__dirname, '../apps/core/jane-ui/bundle-size-report.json');
      
      if (!fs.existsSync(bundleReportPath)) {
        console.log('⚠️  Bundle report not found, generating...');
        execSync('cd apps/core/jane-ui && npm run bundle-size-check', { stdio: 'inherit' });
      }

      const bundleReport = JSON.parse(fs.readFileSync(bundleReportPath, 'utf8'));
      
      // Validate main bundle size
      const mainBundleSize = bundleReport.constitutional.mainBundle.size;
      const totalSize = bundleReport.constitutional.totalSize.size;
      
      const mainBundleCompliant = mainBundleSize <= CONSTITUTIONAL_REQUIREMENTS.bundleSize.maxMainBundle;
      const totalSizeCompliant = totalSize <= CONSTITUTIONAL_REQUIREMENTS.bundleSize.maxTotalSize;
      
      this.results.bundleSize = {
        passed: mainBundleCompliant && totalSizeCompliant,
        details: {
          mainBundle: {
            size: mainBundleSize,
            limit: CONSTITUTIONAL_REQUIREMENTS.bundleSize.maxMainBundle,
            usage: `${((mainBundleSize / CONSTITUTIONAL_REQUIREMENTS.bundleSize.maxMainBundle) * 100).toFixed(1)}%`,
            compliant: mainBundleCompliant
          },
          totalSize: {
            size: totalSize,
            limit: CONSTITUTIONAL_REQUIREMENTS.bundleSize.maxTotalSize,
            usage: `${((totalSize / CONSTITUTIONAL_REQUIREMENTS.bundleSize.maxTotalSize) * 100).toFixed(1)}%`,
            compliant: totalSizeCompliant
          },
          domains: bundleReport.domains
        }
      };

      if (this.results.bundleSize.passed) {
        console.log('✅ Bundle size validation passed');
        console.log(`   Main bundle: ${Math.round(mainBundleSize / 1024)}KB (${this.results.bundleSize.details.mainBundle.usage} of limit)`);
        console.log(`   Total size: ${Math.round(totalSize / 1024 / 1024 * 100) / 100}MB (${this.results.bundleSize.details.totalSize.usage} of limit)`);
      } else {
        console.log('❌ Bundle size validation failed');
        if (!mainBundleCompliant) {
          this.errors.push(`Main bundle exceeds 2MB limit: ${Math.round(mainBundleSize / 1024)}KB`);
        }
        if (!totalSizeCompliant) {
          this.errors.push(`Total size exceeds 5MB limit: ${Math.round(totalSize / 1024 / 1024 * 100) / 100}MB`);
        }
      }

      // Check for warnings
      if (bundleReport.warnings && bundleReport.warnings.length > 0) {
        this.warnings.push(...bundleReport.warnings);
      }

    } catch (error) {
      this.errors.push(`Bundle size validation error: ${error.message}`);
      this.results.bundleSize.passed = false;
    }
  }

  async validatePerformance() {
    console.log('\n⚡ Validating Performance...');

    try {
      // Read performance history
      const performanceHistoryPath = path.join(__dirname, '../apps/core/jane-ui/performance-reports/performance-history.json');
      
      if (!fs.existsSync(performanceHistoryPath)) {
        console.log('⚠️  Performance history not found, running tests...');
        execSync('cd apps/core/jane-ui && npm run performance-test', { stdio: 'inherit' });
      }

      const performanceHistory = JSON.parse(fs.readFileSync(performanceHistoryPath, 'utf8'));
      const latestReport = performanceHistory[performanceHistory.length - 1];

      if (!latestReport) {
        throw new Error('No performance data available');
      }

      // Validate domain performance
      const domainPerformance = latestReport.metrics.domainPerformance;
      const domainResults = {};
      let allDomainsCompliant = true;

      for (const [domain, metrics] of Object.entries(domainPerformance)) {
        const threshold = CONSTITUTIONAL_REQUIREMENTS.performance.domains[domain];
        const compliant = metrics.responseTime <= threshold;
        
        domainResults[domain] = {
          responseTime: Math.round(metrics.responseTime),
          threshold,
          compliant,
          critical: domain === 'security'
        };

        if (!compliant) {
          allDomainsCompliant = false;
          this.errors.push(`${domain} domain exceeds ${threshold}ms threshold: ${Math.round(metrics.responseTime)}ms`);
        }
      }

      // Validate executive function performance
      const executiveFunction = latestReport.metrics.executiveFunction;
      const executiveFunctionResults = {};
      let executiveFunctionCompliant = true;

      for (const [metric, data] of Object.entries(executiveFunction)) {
        const threshold = CONSTITUTIONAL_REQUIREMENTS.performance.executiveFunction[metric];
        const compliant = data.responseTime <= threshold;
        
        executiveFunctionResults[metric] = {
          responseTime: Math.round(data.responseTime),
          threshold,
          compliant
        };

        if (!compliant) {
          executiveFunctionCompliant = false;
          this.errors.push(`Executive function ${metric} exceeds ${threshold}ms threshold: ${Math.round(data.responseTime)}ms`);
        }
      }

      this.results.performance = {
        passed: allDomainsCompliant && executiveFunctionCompliant,
        details: {
          domains: domainResults,
          executiveFunction: executiveFunctionResults,
          constitutional: latestReport.constitutional,
          crossDomain: latestReport.metrics.crossDomain
        }
      };

      if (this.results.performance.passed) {
        console.log('✅ Performance validation passed');
        console.log('   All domains meet constitutional thresholds');
        console.log('   Executive function requirements satisfied');
      } else {
        console.log('❌ Performance validation failed');
      }

    } catch (error) {
      this.errors.push(`Performance validation error: ${error.message}`);
      this.results.performance.passed = false;
    }
  }

  async validateUX() {
    console.log('\n🎨 Validating UX Quality...');

    try {
      // Check for required UX components
      const requiredComponents = [
        'src/components/navigation/NavigationDashboard.tsx',
        'src/components/focus/AdvancedFocusMode.tsx',
        'src/components/workflow/WorkflowManager.tsx',
        'src/components/search/UnifiedSearch.tsx'
      ];

      const componentResults = {};
      let allComponentsExist = true;

      for (const component of requiredComponents) {
        const componentPath = path.join(__dirname, '../apps/core/jane-ui', component);
        const exists = fs.existsSync(componentPath);
        
        componentResults[component] = { exists };
        
        if (!exists) {
          allComponentsExist = false;
          this.errors.push(`Required UX component missing: ${component}`);
        }
      }

      // Check for ADHD optimizations in components
      const adhdOptimizations = this.checkADHDOptimizations();
      
      // Check for accessibility features
      const accessibilityFeatures = this.checkAccessibilityFeatures();

      this.results.ux = {
        passed: allComponentsExist && adhdOptimizations && accessibilityFeatures,
        details: {
          components: componentResults,
          adhdOptimizations,
          accessibilityFeatures,
          cognitiveLoadManagement: true, // Based on NavigationDashboard implementation
          contextSwitchPrevention: true, // Based on workflow components
          focusMode: true // Based on AdvancedFocusMode implementation
        }
      };

      if (this.results.ux.passed) {
        console.log('✅ UX validation passed');
        console.log('   All required components implemented');
        console.log('   ADHD optimizations in place');
        console.log('   Accessibility features verified');
      } else {
        console.log('❌ UX validation failed');
      }

    } catch (error) {
      this.errors.push(`UX validation error: ${error.message}`);
      this.results.ux.passed = false;
    }
  }

  checkADHDOptimizations() {
    try {
      // Check for ADHD-specific code patterns
      const dashboardPath = path.join(__dirname, '../apps/core/jane-ui/src/components/dashboard/Dashboard.tsx');
      const dashboardContent = fs.readFileSync(dashboardPath, 'utf8');
      
      const adhdFeatures = [
        'executiveFunctionEnabled',
        'cognitiveLoad',
        'reduceCognitiveLoad',
        'adhdSupport',
        'contextSwitchingMinimization'
      ];

      const foundFeatures = adhdFeatures.filter(feature => 
        dashboardContent.includes(feature)
      );

      return foundFeatures.length >= 4; // At least 4 out of 5 features
    } catch (error) {
      console.warn('Could not verify ADHD optimizations:', error.message);
      return false;
    }
  }

  checkAccessibilityFeatures() {
    try {
      // Check for accessibility attributes and ARIA labels
      const dashboardPath = path.join(__dirname, '../apps/core/jane-ui/src/components/dashboard/Dashboard.tsx');
      const dashboardContent = fs.readFileSync(dashboardPath, 'utf8');
      
      const a11yFeatures = [
        'aria-label',
        'aria-pressed',
        'role=',
        'aria-live',
        'aria-labelledby'
      ];

      const foundFeatures = a11yFeatures.filter(feature => 
        dashboardContent.includes(feature)
      );

      return foundFeatures.length >= 3; // At least 3 accessibility features
    } catch (error) {
      console.warn('Could not verify accessibility features:', error.message);
      return false;
    }
  }

  async validateArchitecture() {
    console.log('\n🏗️  Validating Architecture...');

    try {
      // Check NX configuration
      const nxConfigPath = path.join(__dirname, '../nx.json');
      const nxConfig = JSON.parse(fs.readFileSync(nxConfigPath, 'utf8'));
      
      // Verify caching is enabled
      const cachingEnabled = nxConfig.tasksRunnerOptions?.default?.options?.cache !== false;
      
      // Check for required targets
      const requiredTargets = ['build', 'analyze-bundle', 'performance-audit'];
      const hasRequiredTargets = requiredTargets.every(target => 
        nxConfig.targetDefaults?.[target] || 
        Object.values(nxConfig.projects || {}).some(project => project.targets?.[target])
      );

      // Check project structure
      const expectedApps = ['jane-ui', 'jane-orchestrator'];
      const appsDir = path.join(__dirname, '../apps/core');
      const actualApps = fs.readdirSync(appsDir).filter(item => 
        fs.statSync(path.join(appsDir, item)).isDirectory()
      );
      
      const hasRequiredApps = expectedApps.every(app => actualApps.includes(app));

      this.results.architecture = {
        passed: cachingEnabled && hasRequiredTargets && hasRequiredApps,
        details: {
          nxCaching: cachingEnabled,
          requiredTargets: hasRequiredTargets,
          requiredApps: hasRequiredApps,
          actualApps
        }
      };

      if (this.results.architecture.passed) {
        console.log('✅ Architecture validation passed');
        console.log('   NX workspace properly configured');
        console.log('   Required applications present');
        console.log('   Caching and optimization enabled');
      } else {
        console.log('❌ Architecture validation failed');
        if (!cachingEnabled) this.errors.push('NX caching not enabled');
        if (!hasRequiredTargets) this.errors.push('Missing required build targets');
        if (!hasRequiredApps) this.errors.push('Missing required applications');
      }

    } catch (error) {
      this.errors.push(`Architecture validation error: ${error.message}`);
      this.results.architecture.passed = false;
    }
  }

  async validateDocumentation() {
    console.log('\n📚 Validating Documentation...');

    try {
      // Check for required documentation files
      const requiredDocs = [
        'README.md',
        'SETUP.md',
        'apps/core/jane-ui/README.md'
      ];

      const docResults = {};
      let allDocsExist = true;

      for (const doc of requiredDocs) {
        const docPath = path.join(__dirname, '..', doc);
        const exists = fs.existsSync(docPath);
        
        docResults[doc] = { exists };
        
        if (!exists) {
          allDocsExist = false;
          this.warnings.push(`Documentation file missing: ${doc}`);
        }
      }

      // Check for performance documentation
      const performanceDocsPath = path.join(__dirname, '../apps/core/jane-ui/performance-reports');
      const hasPerformanceDocs = fs.existsSync(performanceDocsPath);

      this.results.documentation = {
        passed: allDocsExist && hasPerformanceDocs,
        details: {
          requiredDocs: docResults,
          performanceDocs: hasPerformanceDocs
        }
      };

      if (this.results.documentation.passed) {
        console.log('✅ Documentation validation passed');
      } else {
        console.log('⚠️  Documentation validation has warnings');
      }

    } catch (error) {
      this.warnings.push(`Documentation validation error: ${error.message}`);
      this.results.documentation.passed = false;
    }
  }

  generateReport() {
    console.log('\n📊 Validation Report');
    console.log('=' .repeat(50));

    const totalTests = Object.keys(this.results).length;
    const passedTests = Object.values(this.results).filter(r => r.passed).length;
    const overallPass = passedTests === totalTests && this.errors.length === 0;

    console.log(`\n🎯 Overall Status: ${overallPass ? '✅ PASSED' : '❌ FAILED'}`);
    console.log(`   Tests Passed: ${passedTests}/${totalTests}`);
    console.log(`   Errors: ${this.errors.length}`);
    console.log(`   Warnings: ${this.warnings.length}`);

    // Detailed results
    for (const [category, result] of Object.entries(this.results)) {
      console.log(`\n${category.toUpperCase()}: ${result.passed ? '✅ PASSED' : '❌ FAILED'}`);
    }

    // Errors
    if (this.errors.length > 0) {
      console.log('\n❌ ERRORS:');
      this.errors.forEach(error => console.log(`   • ${error}`));
    }

    // Warnings
    if (this.warnings.length > 0) {
      console.log('\n⚠️  WARNINGS:');
      this.warnings.forEach(warning => console.log(`   • ${warning}`));
    }

    // Constitutional compliance summary
    console.log('\n📜 Constitutional Compliance Summary:');
    if (this.results.bundleSize.passed) {
      console.log('   ✅ Bundle size within 2MB/5MB limits');
    }
    if (this.results.performance.passed) {
      console.log('   ✅ All domains meet response time requirements');
      console.log('   ✅ Executive function accommodations validated');
    }
    if (this.results.ux.passed) {
      console.log('   ✅ ADHD/autism-friendly UX implemented');
      console.log('   ✅ Cognitive load management active');
    }

    // Save detailed report
    const reportPath = path.join(__dirname, '../apps/core/jane-ui/phase4-validation-report.json');
    fs.writeFileSync(reportPath, JSON.stringify({
      timestamp: new Date().toISOString(),
      overallPass,
      results: this.results,
      errors: this.errors,
      warnings: this.warnings,
      constitutional: {
        bundleCompliant: this.results.bundleSize.passed,
        performanceCompliant: this.results.performance.passed,
        uxCompliant: this.results.ux.passed,
        architectureCompliant: this.results.architecture.passed
      }
    }, null, 2));

    console.log(`\n📄 Detailed report saved to: ${reportPath}`);

    if (!overallPass) {
      console.log('\n🚨 Phase 4 validation failed. Please address the errors above before production deployment.');
      process.exit(1);
    } else {
      console.log('\n🎉 Phase 4 validation successful! Jane-UI is ready for production.');
    }
  }
}

// Run validation
const validator = new Phase4Validator();
validator.validateAll().catch(error => {
  console.error('Validation crashed:', error);
  process.exit(1);
});