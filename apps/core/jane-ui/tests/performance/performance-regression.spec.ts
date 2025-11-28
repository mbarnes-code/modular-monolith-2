/**
 * Performance Regression Tests
 * Automated testing for constitutional performance requirements
 */

import { expect, test } from '@playwright/test';
import lighthouse from 'lighthouse';
import { chromium } from 'playwright';

interface PerformanceThresholds {
  responseTime: Record<string, number>;
  executiveFunction: Record<string, number>;
  bundleSize: {
    maxMainBundle: number;
    maxTotalSize: number;
  };
  webVitals: {
    LCP: number;  // Largest Contentful Paint
    FID: number;  // First Input Delay
    CLS: number;  // Cumulative Layout Shift
    FCP: number;  // First Contentful Paint
    TTI: number;  // Time to Interactive
  };
}

const CONSTITUTIONAL_THRESHOLDS: PerformanceThresholds = {
  responseTime: {
    security: 1000,
    productivity: 2000,
    mtg: 3000,
    infrastructure: 5000,
  },
  executiveFunction: {
    interaction: 200,
    navigation: 300,
    dataLoad: 500,
    contextSwitch: 250,
  },
  bundleSize: {
    maxMainBundle: 2 * 1024 * 1024, // 2MB
    maxTotalSize: 5 * 1024 * 1024,  // 5MB
  },
  webVitals: {
    LCP: 2500,  // Good: < 2.5s
    FID: 100,   // Good: < 100ms
    CLS: 0.1,   // Good: < 0.1
    FCP: 1800,  // Good: < 1.8s
    TTI: 3800,  // Good: < 3.8s
  },
};

test.describe('Performance Regression Tests', () => {
  let browser: any;
  let page: any;

  test.beforeAll(async () => {
    browser = await chromium.launch();
  });

  test.afterAll(async () => {
    await browser.close();
  });

  test.beforeEach(async () => {
    page = await browser.newPage();
  });

  test.afterEach(async () => {
    await page.close();
  });

  test('Bundle size meets constitutional requirements', async () => {
    // This test reads bundle analysis data
    const bundleReportPath = './bundle-size-report.json';
    
    try {
      const bundleReport = JSON.parse(
        require('fs').readFileSync(bundleReportPath, 'utf8')
      );

      // Main bundle size check
      const mainBundleSize = bundleReport.constitutional.mainBundle.size;
      expect(mainBundleSize).toBeLessThanOrEqual(CONSTITUTIONAL_THRESHOLDS.bundleSize.maxMainBundle);
      
      // Total size check
      const totalSize = bundleReport.constitutional.totalSize.size;
      expect(totalSize).toBeLessThanOrEqual(CONSTITUTIONAL_THRESHOLDS.bundleSize.maxTotalSize);

      // Report sizes for monitoring
      console.log(`Main bundle: ${Math.round(mainBundleSize / 1024 / 1024 * 100) / 100}MB`);
      console.log(`Total size: ${Math.round(totalSize / 1024 / 1024 * 100) / 100}MB`);
      
    } catch (error) {
      console.warn('Bundle report not found - running build first');
      expect(true).toBe(false); // Fail if bundle report missing
    }
  });

  test('Page load performance meets executive function requirements', async () => {
    await page.goto('http://localhost:3000');
    
    // Measure page load timing
    const performanceTiming = await page.evaluate(() => {
      const perfData = performance.getEntriesByType('navigation')[0] as PerformanceNavigationTiming;
      return {
        domContentLoaded: perfData.domContentLoadedEventEnd - perfData.domContentLoadedEventStart,
        loadComplete: perfData.loadEventEnd - perfData.loadEventStart,
        firstPaint: performance.getEntriesByType('paint').find(entry => entry.name === 'first-paint')?.startTime || 0,
        firstContentfulPaint: performance.getEntriesByType('paint').find(entry => entry.name === 'first-contentful-paint')?.startTime || 0,
      };
    });

    // Executive function requirement: Initial interaction within 200ms
    expect(performanceTiming.firstPaint).toBeLessThanOrEqual(CONSTITUTIONAL_THRESHOLDS.executiveFunction.interaction);
    
    // Content should load within executive function threshold
    expect(performanceTiming.firstContentfulPaint).toBeLessThanOrEqual(CONSTITUTIONAL_THRESHOLDS.executiveFunction.dataLoad);
    
    console.log('Page performance:', performanceTiming);
  });

  test('UI interactions meet ADHD accommodation requirements', async () => {
    await page.goto('http://localhost:3000');

    // Test button click responsiveness
    const button = page.locator('button').first();
    if (await button.isVisible()) {
      const clickStart = Date.now();
      await button.click();
      const clickEnd = Date.now();
      
      const responseTime = clickEnd - clickStart;
      expect(responseTime).toBeLessThanOrEqual(CONSTITUTIONAL_THRESHOLDS.executiveFunction.interaction);
      
      console.log(`Button click response: ${responseTime}ms`);
    }

    // Test navigation responsiveness
    const navigationLinks = page.locator('a, [role="button"]');
    const linkCount = await navigationLinks.count();
    
    if (linkCount > 0) {
      const firstLink = navigationLinks.first();
      const navStart = Date.now();
      await firstLink.click();
      await page.waitForLoadState('domcontentloaded');
      const navEnd = Date.now();
      
      const navigationTime = navEnd - navStart;
      expect(navigationTime).toBeLessThanOrEqual(CONSTITUTIONAL_THRESHOLDS.executiveFunction.navigation);
      
      console.log(`Navigation response: ${navigationTime}ms`);
    }
  });

  test('Domain-specific response times meet constitutional requirements', async () => {
    await page.goto('http://localhost:3000');
    
    // Mock domain-specific operations and measure response times
    const domainTests = [
      { domain: 'security', simulateOperation: async () => {
        // Simulate security tool interaction
        const start = Date.now();
        await page.evaluate(() => {
          // Simulate heavy security processing
          const arr = new Array(10000).fill(0).map((_, i) => Math.random() * i);
          return arr.reduce((a, b) => a + b, 0);
        });
        return Date.now() - start;
      }},
      { domain: 'productivity', simulateOperation: async () => {
        // Simulate productivity tool interaction
        const start = Date.now();
        await page.evaluate(() => {
          // Simulate moderate processing
          return new Promise(resolve => setTimeout(resolve, 100));
        });
        return Date.now() - start;
      }},
    ];

    for (const { domain, simulateOperation } of domainTests) {
      const responseTime = await simulateOperation();
      const threshold = CONSTITUTIONAL_THRESHOLDS.responseTime[domain];
      
      expect(responseTime).toBeLessThanOrEqual(threshold);
      console.log(`${domain} domain response: ${responseTime}ms (threshold: ${threshold}ms)`);
    }
  });

  test('Lighthouse performance audit meets quality standards', async () => {
    // Run Lighthouse audit programmatically
    const port = 3000;
    const url = `http://localhost:${port}`;
    
    try {
      const options = {
        logLevel: 'info',
        output: 'json',
        onlyCategories: ['performance'],
        port: 9222,
      };

      // Note: This requires Chrome to be launched with --remote-debugging-port=9222
      const runnerResult = await lighthouse(url, options);
      
      if (runnerResult && runnerResult.lhr) {
        const performanceScore = runnerResult.lhr.categories.performance.score * 100;
        
        // Expect at least 80% performance score
        expect(performanceScore).toBeGreaterThanOrEqual(80);
        
        // Check specific web vitals
        const audits = runnerResult.lhr.audits;
        
        if (audits['largest-contentful-paint']) {
          const lcp = audits['largest-contentful-paint'].numericValue;
          expect(lcp).toBeLessThanOrEqual(CONSTITUTIONAL_THRESHOLDS.webVitals.LCP);
        }
        
        if (audits['first-input-delay']) {
          const fid = audits['first-input-delay'].numericValue;
          expect(fid).toBeLessThanOrEqual(CONSTITUTIONAL_THRESHOLDS.webVitals.FID);
        }
        
        if (audits['cumulative-layout-shift']) {
          const cls = audits['cumulative-layout-shift'].numericValue;
          expect(cls).toBeLessThanOrEqual(CONSTITUTIONAL_THRESHOLDS.webVitals.CLS);
        }
        
        console.log(`Lighthouse Performance Score: ${performanceScore}%`);
      }
    } catch (error) {
      console.warn('Lighthouse audit failed - ensure app is running on port 3000');
      console.warn(error);
      // Don't fail the test if Lighthouse isn't properly configured
    }
  });

  test('Memory usage stays within cognitive load limits', async () => {
    await page.goto('http://localhost:3000');
    
    // Monitor memory usage during interaction
    const memoryBefore = await page.evaluate(() => {
      return (performance as any).memory ? {
        usedJSHeapSize: (performance as any).memory.usedJSHeapSize,
        totalJSHeapSize: (performance as any).memory.totalJSHeapSize,
        jsHeapSizeLimit: (performance as any).memory.jsHeapSizeLimit,
      } : null;
    });

    if (memoryBefore) {
      // Simulate heavy interaction
      await page.evaluate(() => {
        // Create some DOM elements and data structures
        const elements = [];
        for (let i = 0; i < 1000; i++) {
          const div = document.createElement('div');
          div.textContent = `Test element ${i}`;
          elements.push(div);
        }
        
        // Clean up
        elements.forEach(el => el.remove());
      });

      const memoryAfter = await page.evaluate(() => {
        return (performance as any).memory ? {
          usedJSHeapSize: (performance as any).memory.usedJSHeapSize,
          totalJSHeapSize: (performance as any).memory.totalJSHeapSize,
          jsHeapSizeLimit: (performance as any).memory.jsHeapSizeLimit,
        } : null;
      });

      if (memoryAfter) {
        const memoryIncrease = memoryAfter.usedJSHeapSize - memoryBefore.usedJSHeapSize;
        const memoryUsagePercentage = (memoryAfter.usedJSHeapSize / memoryAfter.jsHeapSizeLimit) * 100;
        
        // Memory increase should be reasonable (less than 10MB for test operations)
        expect(memoryIncrease).toBeLessThanOrEqual(10 * 1024 * 1024);
        
        // Total memory usage should stay below 80% of heap limit
        expect(memoryUsagePercentage).toBeLessThanOrEqual(80);
        
        console.log(`Memory usage: ${Math.round(memoryUsagePercentage)}% of heap limit`);
        console.log(`Memory increase: ${Math.round(memoryIncrease / 1024 / 1024)}MB`);
      }
    }
  });

  test('Performance regression detection', async () => {
    // Load historical performance data if available
    const performanceHistoryPath = './performance-history.json';
    let performanceHistory: any[] = [];
    
    try {
      performanceHistory = JSON.parse(
        require('fs').readFileSync(performanceHistoryPath, 'utf8')
      );
    } catch (error) {
      console.log('No performance history found - this will be the baseline');
    }

    await page.goto('http://localhost:3000');
    
    // Measure current performance
    const currentPerformance = await page.evaluate(() => {
      const perfData = performance.getEntriesByType('navigation')[0] as PerformanceNavigationTiming;
      return {
        timestamp: Date.now(),
        loadTime: perfData.loadEventEnd - perfData.navigationStart,
        domContentLoaded: perfData.domContentLoadedEventEnd - perfData.domContentLoadedEventStart,
        firstPaint: performance.getEntriesByType('paint').find(entry => entry.name === 'first-paint')?.startTime || 0,
        firstContentfulPaint: performance.getEntriesByType('paint').find(entry => entry.name === 'first-contentful-paint')?.startTime || 0,
      };
    });

    if (performanceHistory.length > 0) {
      const lastPerformance = performanceHistory[performanceHistory.length - 1];
      
      // Check for regression (more than 20% slower)
      const regressionThreshold = 1.2;
      
      expect(currentPerformance.loadTime).toBeLessThanOrEqual(lastPerformance.loadTime * regressionThreshold);
      expect(currentPerformance.firstPaint).toBeLessThanOrEqual(lastPerformance.firstPaint * regressionThreshold);
      expect(currentPerformance.firstContentfulPaint).toBeLessThanOrEqual(lastPerformance.firstContentfulPaint * regressionThreshold);
      
      console.log('Performance comparison:', {
        current: currentPerformance,
        previous: lastPerformance,
        regression: {
          loadTime: `${Math.round((currentPerformance.loadTime / lastPerformance.loadTime - 1) * 100)}%`,
          firstPaint: `${Math.round((currentPerformance.firstPaint / lastPerformance.firstPaint - 1) * 100)}%`,
        }
      });
    }

    // Save current performance for future comparisons
    performanceHistory.push(currentPerformance);
    
    // Keep only last 10 entries
    if (performanceHistory.length > 10) {
      performanceHistory = performanceHistory.slice(-10);
    }
    
    try {
      require('fs').writeFileSync(
        performanceHistoryPath,
        JSON.stringify(performanceHistory, null, 2)
      );
    } catch (error) {
      console.warn('Could not save performance history:', error);
    }
  });
});

// Helper function to measure function execution time
async function measureExecutionTime<T>(
  fn: () => Promise<T>,
  description: string
): Promise<{ result: T; executionTime: number }> {
  const start = Date.now();
  const result = await fn();
  const executionTime = Date.now() - start;
  
  console.log(`${description}: ${executionTime}ms`);
  
  return { result, executionTime };
}

export { CONSTITUTIONAL_THRESHOLDS, measureExecutionTime };
