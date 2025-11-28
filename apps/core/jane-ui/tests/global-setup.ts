/**
 * Global Setup for Performance Tests
 * Ensures environment is ready for constitutional compliance testing
 */

import { chromium, FullConfig } from '@playwright/test';
import fs from 'fs';

async function globalSetup(config: FullConfig) {
  console.log('🚀 Setting up performance testing environment...');

  // Ensure required directories exist
  const dirs = [
    'performance-reports',
    'performance-reports/playwright',
    'performance-reports/lighthouse',
    'performance-reports/test-results',
  ];

  dirs.forEach(dir => {
    if (!fs.existsSync(dir)) {
      fs.mkdirSync(dir, { recursive: true });
      console.log(`✅ Created directory: ${dir}`);
    }
  });

  // Create performance baseline if it doesn't exist
  const baselinePath = 'performance-reports/baseline.json';
  if (!fs.existsSync(baselinePath)) {
    const baseline = {
      created: new Date().toISOString(),
      constitutional_thresholds: {
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
          maxMainBundle: 2 * 1024 * 1024,
          maxTotalSize: 5 * 1024 * 1024,
        },
      },
    };
    
    fs.writeFileSync(baselinePath, JSON.stringify(baseline, null, 2));
    console.log('✅ Created performance baseline');
  }

  // Warm up the application by making a request
  try {
    const browser = await chromium.launch();
    const page = await browser.newPage();
    
    console.log('🔥 Warming up application...');
    await page.goto('http://localhost:3000', { timeout: 30000 });
    await page.waitForLoadState('networkidle');
    
    await browser.close();
    console.log('✅ Application warmup complete');
  } catch (error) {
    console.warn('⚠️  Application warmup failed:', error);
  }

  console.log('✅ Performance testing environment ready');
}

export default globalSetup;