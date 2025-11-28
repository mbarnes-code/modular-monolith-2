import { defineConfig, devices } from '@playwright/test';

/**
 * Playwright Configuration for Performance Testing
 * Optimized for constitutional compliance validation
 */
export default defineConfig({
  testDir: './tests',
  
  // Run tests in files in parallel
  fullyParallel: true,
  
  // Fail the build on CI if you accidentally left test.only in the source code
  forbidOnly: !!process.env.CI,
  
  // Retry on CI only
  retries: process.env.CI ? 2 : 0,
  
  // Opt out of parallel tests on CI
  workers: process.env.CI ? 1 : undefined,
  
  // Reporter to use
  reporter: [
    ['html', { outputFolder: 'performance-reports/playwright' }],
    ['json', { outputFile: 'performance-reports/results.json' }],
    ['line']
  ],
  
  // Shared settings for all the projects below
  use: {
    // Base URL to use in actions like `await page.goto('/')`
    baseURL: 'http://localhost:3000',
    
    // Collect trace when retrying the failed test
    trace: 'on-first-retry',
    
    // Collect screenshot on failure
    screenshot: 'only-on-failure',
    
    // Record video on failure
    video: 'retain-on-failure',
    
    // Global timeout for each test
    actionTimeout: 30000,
    
    // Navigation timeout
    navigationTimeout: 30000,
  },

  // Configure projects for major browsers
  projects: [
    {
      name: 'performance-chrome',
      use: { 
        ...devices['Desktop Chrome'],
        // Disable web security for testing
        launchOptions: {
          args: ['--disable-web-security'],
        },
      },
      testMatch: '**/performance/**/*.spec.ts',
    },
    
    {
      name: 'performance-firefox',
      use: { ...devices['Desktop Firefox'] },
      testMatch: '**/performance/**/*.spec.ts',
    },
    
    {
      name: 'performance-safari',
      use: { ...devices['Desktop Safari'] },
      testMatch: '**/performance/**/*.spec.ts',
    },

    // Executive function testing on mobile (ADHD accommodation validation)
    {
      name: 'executive-function-mobile',
      use: { ...devices['iPhone 12'] },
      testMatch: '**/performance/performance-regression.spec.ts',
    },
  ],

  // Global setup and teardown
  globalSetup: require.resolve('./tests/global-setup.ts'),
  globalTeardown: require.resolve('./tests/global-teardown.ts'),

  // Run your local dev server before starting the tests
  webServer: {
    command: 'npm run dev',
    port: 3000,
    reuseExistingServer: !process.env.CI,
    timeout: 120000,
  },

  // Output directories
  outputDir: 'performance-reports/test-results',
  
  // Test timeout
  timeout: 60000,
  
  // Global test timeout
  globalTimeout: 600000,
  
  // Expect timeout for assertions
  expect: {
    timeout: 10000,
  },
});