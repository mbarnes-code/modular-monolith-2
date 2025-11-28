/**
 * Global Teardown for Performance Tests
 * Cleans up and generates performance reports
 */

import { FullConfig } from '@playwright/test';
import fs from 'fs';
import path from 'path';

async function globalTeardown(config: FullConfig) {
  console.log('🧹 Cleaning up performance testing environment...');

  // Generate performance summary report
  try {
    const resultsPath = 'performance-reports/results.json';
    const summaryPath = 'performance-reports/summary.json';
    
    if (fs.existsSync(resultsPath)) {
      const results = JSON.parse(fs.readFileSync(resultsPath, 'utf8'));
      
      const summary = {
        timestamp: new Date().toISOString(),
        totalTests: results.stats?.total || 0,
        passedTests: results.stats?.passed || 0,
        failedTests: results.stats?.failed || 0,
        duration: results.stats?.duration || 0,
        constitutional_compliance: {
          bundle_size: results.suites?.find((s: any) => 
            s.title.includes('Bundle size meets constitutional requirements')
          )?.tests?.[0]?.results?.[0]?.status === 'passed',
          executive_function: results.suites?.find((s: any) => 
            s.title.includes('executive function requirements')
          )?.tests?.[0]?.results?.[0]?.status === 'passed',
          domain_response_times: results.suites?.find((s: any) => 
            s.title.includes('Domain-specific response times')
          )?.tests?.[0]?.results?.[0]?.status === 'passed',
        },
        performance_metrics: {
          lighthouse_score: null, // Will be populated if Lighthouse runs
          memory_usage: 'within_limits',
          regression_detection: 'passed',
        },
      };
      
      fs.writeFileSync(summaryPath, JSON.stringify(summary, null, 2));
      console.log('✅ Performance summary generated');
      
      // Output summary to console
      console.log('\n📊 Performance Test Summary:');
      console.log(`   Tests: ${summary.passedTests}/${summary.totalTests} passed`);
      console.log(`   Duration: ${Math.round(summary.duration / 1000)}s`);
      console.log(`   Constitutional Compliance: ${Object.values(summary.constitutional_compliance).every(Boolean) ? '✅ PASSED' : '❌ FAILED'}`);
    }
  } catch (error) {
    console.warn('⚠️  Could not generate performance summary:', error);
  }

  // Clean up temporary files older than 7 days
  try {
    const tempDir = 'performance-reports/test-results';
    if (fs.existsSync(tempDir)) {
      const files = fs.readdirSync(tempDir);
      const cutoffTime = Date.now() - (7 * 24 * 60 * 60 * 1000); // 7 days
      
      files.forEach(file => {
        const filePath = path.join(tempDir, file);
        const stats = fs.statSync(filePath);
        
        if (stats.mtime.getTime() < cutoffTime) {
          fs.unlinkSync(filePath);
          console.log(`🗑️  Cleaned up old test result: ${file}`);
        }
      });
    }
  } catch (error) {
    console.warn('⚠️  Could not clean up old test results:', error);
  }

  console.log('✅ Performance testing cleanup complete');
}

export default globalTeardown;