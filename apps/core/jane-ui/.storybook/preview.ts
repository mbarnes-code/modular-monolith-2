import type { Preview } from '@storybook/react';
import React from 'react';

const preview: Preview = {
  parameters: {
    // Executive function accommodations (inspired by n8n)
    layout: 'centered',
    backgrounds: {
      default: 'light',
      values: [
        {
          name: 'light',
          value: '#ffffff',
        },
        {
          name: 'dark', 
          value: '#1a1a1a',
        },
        {
          name: 'high-contrast',  // ADHD-friendly (from n8n pattern)
          value: '#000000',
        },
      ],
    },
    
    controls: {
      matchers: {
        color: /(background|color)$/i,
        date: /Date$/i,
      },
    },
    
    // Accessibility testing (from n8n addon)
    a11y: {
      element: '#storybook-root',
      config: {},
      options: {},
      manual: true,
    },
    
    // Performance monitoring for <75ms interactions
    docs: {
      extractComponentDescription: (component, { notes }) => {
        if (notes) {
          return typeof notes === 'string' ? notes : notes.markdown || notes.text;
        }
        return null;
      },
    },
  },
  
  // Global decorators for executive function support (n8n inspired)
  decorators: [
    (Story, context) => {
      return React.createElement(
        'div',
        {
          style: { 
            padding: '1rem',
            // High contrast mode for ADHD (n8n theme pattern)
            outline: context.globals.highContrast ? '2px solid #007acc' : 'none'
          }
        },
        React.createElement(Story)
      );
    },
  ],
  
  // Executive function theme switcher (n8n addon pattern)
  globalTypes: {
    highContrast: {
      description: 'High contrast mode for executive function support',
      defaultValue: false,
      toolbar: {
        title: 'High Contrast',
        icon: 'accessibility',
        items: [
          { value: false, title: 'Normal' },
          { value: true, title: 'High Contrast (ADHD)' },
        ],
      },
    },
  },
};

export default preview;
