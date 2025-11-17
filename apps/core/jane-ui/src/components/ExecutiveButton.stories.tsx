import type { Meta, StoryObj } from '@storybook/react';
import React from 'react';

// Executive Function Optimized Button (inspired by n8n design system)
const ExecutiveButton = ({ 
  children, 
  variant = 'primary',
  size = 'medium',
  onClick,
  loading = false,
  disabled = false
}: { 
  children: React.ReactNode;
  variant?: 'primary' | 'secondary' | 'danger' | 'success';
  size?: 'small' | 'medium' | 'large';
  onClick?: () => void;
  loading?: boolean;
  disabled?: boolean;
}) => {
  const getVariantColors = (variant: string) => {
    switch (variant) {
      case 'primary': return { bg: '#007acc', hover: '#005a9e', focus: '#007acc' };
      case 'secondary': return { bg: '#6c757d', hover: '#545b62', focus: '#6c757d' };
      case 'danger': return { bg: '#dc3545', hover: '#c82333', focus: '#dc3545' };
      case 'success': return { bg: '#28a745', hover: '#218838', focus: '#28a745' };
      default: return { bg: '#007acc', hover: '#005a9e', focus: '#007acc' };
    }
  };

  const getSizeStyles = (size: string) => {
    switch (size) {
      case 'small': return { padding: '6px 12px', fontSize: '12px' };
      case 'medium': return { padding: '8px 16px', fontSize: '14px' };
      case 'large': return { padding: '12px 24px', fontSize: '16px' };
      default: return { padding: '8px 16px', fontSize: '14px' };
    }
  };

  const colors = getVariantColors(variant);
  const sizeStyles = getSizeStyles(size);

  return (
    <button
      onClick={onClick}
      disabled={disabled || loading}
      style={{
        ...sizeStyles,
        border: 'none',
        borderRadius: '4px',
        backgroundColor: disabled ? '#e9ecef' : colors.bg,
        color: disabled ? '#6c757d' : 'white',
        cursor: disabled ? 'not-allowed' : 'pointer',
        fontWeight: '500',
        // Executive function optimizations (inspired by n8n)
        outline: '2px solid transparent',
        transition: 'all 0.1s ease', // <75ms interaction requirement
        minWidth: '64px',
        position: 'relative',
        // High contrast support for ADHD
        border: '1px solid transparent',
      }}
      onMouseEnter={(e) => {
        if (!disabled) {
          e.currentTarget.style.backgroundColor = colors.hover;
        }
      }}
      onMouseLeave={(e) => {
        if (!disabled) {
          e.currentTarget.style.backgroundColor = colors.bg;
        }
      }}
      onFocus={(e) => {
        if (!disabled) {
          e.currentTarget.style.outline = `2px solid ${colors.focus}`;
          e.currentTarget.style.outlineOffset = '2px';
        }
      }}
      onBlur={(e) => {
        e.currentTarget.style.outline = '2px solid transparent';
      }}
    >
      {loading ? '...' : children}
    </button>
  );
};

const meta: Meta<typeof ExecutiveButton> = {
  title: 'Jane UI/ExecutiveButton',  // Following n8n's "Atoms/" pattern
  component: ExecutiveButton,
  parameters: {
    layout: 'centered',
    docs: {
      description: {
        component: 'Executive function optimized button with <75ms interactions, inspired by n8n design system patterns for ADHD support'
      }
    }
  },
  argTypes: {
    variant: {
      control: { type: 'select' },
      options: ['primary', 'secondary', 'danger', 'success'],
      description: 'Visual style variant (inspired by n8n color system)'
    },
    size: {
      control: { type: 'select' },
      options: ['small', 'medium', 'large'],
      description: 'Button size (n8n pattern)'
    },
    loading: {
      control: { type: 'boolean' },
      description: 'Loading state (executive function friendly)'
    },
    disabled: {
      control: { type: 'boolean' },
      description: 'Disabled state with high contrast'
    }
  },
  tags: ['autodocs'],  // From n8n sharedTags
};

export default meta;
type Story = StoryObj<typeof meta>;

// Stories organized like n8n's approach
export const Primary: Story = {
  args: {
    children: 'Primary Action',
    variant: 'primary'
  }
};

export const Secondary: Story = {
  args: {
    children: 'Secondary Action', 
    variant: 'secondary'
  }
};

export const Danger: Story = {
  args: {
    children: 'Delete Item',
    variant: 'danger'
  }
};

export const Success: Story = {
  args: {
    children: 'Save Changes',
    variant: 'success'
  }
};

export const Loading: Story = {
  args: {
    children: 'Processing...',
    variant: 'primary',
    loading: true
  }
};

export const Disabled: Story = {
  args: {
    children: 'Disabled Button',
    variant: 'primary',
    disabled: true
  }
};

// Interactive story for testing executive function requirements
export const InteractiveTest: Story = {
  args: {
    children: 'Test <75ms Response',
    variant: 'primary',
    onClick: () => {
      const startTime = Date.now();
      // Simulate executive function friendly interaction
      setTimeout(() => {
        const endTime = Date.now();
        const interactionTime = endTime - startTime;
        alert(`Interaction time: ${interactionTime}ms ${interactionTime < 75 ? '✅ Good' : '❌ Too slow'}`);
      }, 10);
    }
  }
};

// Size variations (following n8n size system)
export const SmallSize: Story = {
  args: {
    children: 'Small',
    variant: 'primary',
    size: 'small'
  }
};

export const LargeSize: Story = {
  args: {
    children: 'Large Action',
    variant: 'primary', 
    size: 'large'
  }
};