import type { StorybookConfig } from '@storybook/nextjs';

const config: StorybookConfig = {
  stories: ['../**/*.@(mdx|stories.@(js|jsx|ts|tsx))'],
  addons: [
    '@storybook/addon-essentials',   // Core Storybook functionality
    '@storybook/addon-a11y',         // Accessibility testing (executive function support)
    '@storybook/addon-links',        // Cross-story navigation
    // Temporarily disabled problematic addons
    // 'storybook-dark-mode',           
    // '@storybook/addon-themes',       
    // '@storybook/addon-interactions', 
  ],
  framework: {
    name: "@storybook/react-vite",
    options: {},
  },
  
  // Executive function optimizations (inspired by n8n)
  core: {
    disableTelemetry: true,  // Reduce distractions
  },
  
  // Performance settings for <75ms interactions
  features: {
    interactionsDebugger: true,
    buildStoriesJson: true,
  },
};

export default config;

// To customize your webpack configuration you can use the webpackFinal field.
// Check https://storybook.js.org/docs/react/builders/webpack#extending-storybooks-webpack-config
// and https://nx.dev/recipes/storybook/custom-builder-configs
