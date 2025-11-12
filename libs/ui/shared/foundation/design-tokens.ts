/**
 * Design Tokens for Mental Prosthetic Platform
 * 
 * Provides the foundation for consistent design across all domains
 * with executive function accommodations and accessibility compliance.
 */

// Color System with Executive Function Accommodations
export const colors = {
  // Neutral palette for cognitive clarity
  neutral: {
    50: '#fafafa',
    100: '#f5f5f5',
    200: '#e5e5e5',
    300: '#d4d4d4',
    400: '#a3a3a3',
    500: '#737373',
    600: '#525252',
    700: '#404040',
    800: '#262626',
    900: '#171717',
    950: '#0a0a0a',
  },

  // Primary colors with high contrast for focus
  primary: {
    50: '#eff6ff',
    100: '#dbeafe', 
    200: '#bfdbfe',
    300: '#93c5fd',
    400: '#60a5fa',
    500: '#3b82f6', // Main primary
    600: '#2563eb',
    700: '#1d4ed8',
    800: '#1e40af',
    900: '#1e3a8a',
  },

  // Semantic colors with clear meaning
  semantic: {
    success: {
      light: '#dcfce7',
      base: '#22c55e',
      dark: '#15803d',
      contrast: '#ffffff',
    },
    warning: {
      light: '#fef3c7',
      base: '#f59e0b',
      dark: '#d97706',
      contrast: '#000000',
    },
    error: {
      light: '#fee2e2',
      base: '#ef4444',
      dark: '#dc2626',
      contrast: '#ffffff',
    },
    info: {
      light: '#dbeafe',
      base: '#3b82f6',
      dark: '#2563eb',
      contrast: '#ffffff',
    },
  },

  // Domain-specific color palettes
  domains: {
    security: {
      primary: '#dc2626',    // Red for alerts
      secondary: '#f59e0b',  // Amber for warnings
      accent: '#059669',     // Green for safe
      background: '#fefefe',
      surface: '#f9fafb',
    },
    productivity: {
      primary: '#2563eb',    // Blue for focus
      secondary: '#7c3aed',  // Purple for creativity
      accent: '#059669',     // Green for completion
      background: '#fefefe',
      surface: '#f8fafc',
    },
    tcg: {
      primary: '#7c2d12',    // Brown for artifacts
      secondary: '#be185d',  // Magenta for magic
      accent: '#0d9488',     // Teal for strategy
      background: '#fffbeb',
      surface: '#fef7ed',
    },
    infrastructure: {
      primary: '#374151',    // Gray for systems
      secondary: '#4338ca',  // Indigo for networks  
      accent: '#059669',     // Green for healthy
      background: '#fefefe',
      surface: '#f9fafb',
    },
    finance: {
      primary: '#059669',    // Green for money
      secondary: '#dc2626',  // Red for expenses
      accent: '#2563eb',     // Blue for planning
      background: '#fefefe',
      surface: '#f0fdf4',
    },
  },
};

// Typography with executive function support
export const typography = {
  fontFamily: {
    base: [
      '-apple-system',
      'BlinkMacSystemFont', 
      '"Segoe UI"',
      'Roboto',
      '"Helvetica Neue"',
      'Arial',
      'sans-serif'
    ].join(', '),
    mono: [
      '"SF Mono"',
      'Monaco',
      'Consolas',
      '"Liberation Mono"',
      '"Courier New"',
      'monospace'
    ].join(', '),
    // ADHD-friendly font option
    dyslexic: [
      '"OpenDyslexic"',
      'Arial',
      'sans-serif'
    ].join(', '),
  },

  // Scale optimized for readability and focus
  fontSize: {
    xs: '0.75rem',      // 12px
    sm: '0.875rem',     // 14px  
    base: '1rem',       // 16px - minimum for accessibility
    lg: '1.125rem',     // 18px
    xl: '1.25rem',      // 20px
    '2xl': '1.5rem',    // 24px
    '3xl': '1.875rem',  // 30px
    '4xl': '2.25rem',   // 36px
    '5xl': '3rem',      // 48px
    '6xl': '3.75rem',   // 60px
  },

  fontWeight: {
    light: 300,
    normal: 400,
    medium: 500,
    semibold: 600,
    bold: 700,
    extrabold: 800,
  },

  lineHeight: {
    tight: 1.25,
    snug: 1.375,
    normal: 1.5,
    relaxed: 1.625,  // Better for executive function
    loose: 2,
  },

  letterSpacing: {
    tighter: '-0.05em',
    tight: '-0.025em',
    normal: '0',
    wide: '0.025em',
    wider: '0.05em',
    widest: '0.1em',
  },
};

// Spacing system with consistent rhythm
export const spacing = {
  0: '0',
  1: '0.25rem',     // 4px
  2: '0.5rem',      // 8px
  3: '0.75rem',     // 12px
  4: '1rem',        // 16px
  5: '1.25rem',     // 20px
  6: '1.5rem',      // 24px
  8: '2rem',        // 32px
  10: '2.5rem',     // 40px
  12: '3rem',       // 48px
  16: '4rem',       // 64px
  20: '5rem',       // 80px
  24: '6rem',       // 96px
  32: '8rem',       // 128px
  40: '10rem',      // 160px
  48: '12rem',      // 192px
  56: '14rem',      // 224px
  64: '16rem',      // 256px
};

// Border radius for consistent rounding
export const borderRadius = {
  none: '0',
  sm: '0.125rem',    // 2px
  base: '0.25rem',   // 4px
  md: '0.375rem',    // 6px
  lg: '0.5rem',      // 8px
  xl: '0.75rem',     // 12px
  '2xl': '1rem',     // 16px
  '3xl': '1.5rem',   // 24px
  full: '9999px',
};

// Shadows for depth hierarchy
export const shadows = {
  none: 'none',
  sm: '0 1px 2px 0 rgb(0 0 0 / 0.05)',
  base: '0 1px 3px 0 rgb(0 0 0 / 0.1), 0 1px 2px -1px rgb(0 0 0 / 0.1)',
  md: '0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1)',
  lg: '0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1)',
  xl: '0 20px 25px -5px rgb(0 0 0 / 0.1), 0 8px 10px -6px rgb(0 0 0 / 0.1)',
  '2xl': '0 25px 50px -12px rgb(0 0 0 / 0.25)',
  inner: 'inset 0 2px 4px 0 rgb(0 0 0 / 0.05)',
};

// Breakpoints for responsive design
export const breakpoints = {
  xs: '475px',
  sm: '640px',
  md: '768px',
  lg: '1024px',
  xl: '1280px',
  '2xl': '1536px',
};

// Z-index layers for proper stacking
export const zIndex = {
  hide: -1,
  auto: 'auto',
  base: 0,
  docked: 10,
  dropdown: 1000,
  sticky: 1100,
  banner: 1200,
  overlay: 1300,
  modal: 1400,
  popover: 1500,
  skipLink: 1600,
  toast: 1700,
  tooltip: 1800,
};

// Animation and transition tokens
export const animation = {
  duration: {
    fast: '150ms',
    normal: '200ms',
    slow: '300ms',
    slower: '500ms',
  },

  easing: {
    linear: 'linear',
    in: 'cubic-bezier(0.4, 0, 1, 1)',
    out: 'cubic-bezier(0, 0, 0.2, 1)',
    inOut: 'cubic-bezier(0.4, 0, 0.2, 1)',
  },

  // Executive function friendly - reduced motion option
  reducedMotion: {
    duration: '1ms',
    easing: 'linear',
  },
};

// Focus indicators for accessibility and executive function
export const focus = {
  ring: {
    width: '2px',
    style: 'solid',
    color: colors.primary[500],
    offset: '2px',
  },
  
  // High contrast option for better visibility
  highContrast: {
    width: '3px',
    style: 'solid', 
    color: '#000000',
    offset: '1px',
  },
};

// Executive function accommodations
export const executiveFunction = {
  // Clear visual hierarchy
  hierarchy: {
    primary: {
      fontSize: typography.fontSize['2xl'],
      fontWeight: typography.fontWeight.bold,
      color: colors.neutral[900],
      marginBottom: spacing[6],
    },
    secondary: {
      fontSize: typography.fontSize.xl,
      fontWeight: typography.fontWeight.semibold,
      color: colors.neutral[800],
      marginBottom: spacing[4],
    },
    tertiary: {
      fontSize: typography.fontSize.lg,
      fontWeight: typography.fontWeight.medium,
      color: colors.neutral[700],
      marginBottom: spacing[3],
    },
  },

  // Context preservation helpers
  breadcrumb: {
    fontSize: typography.fontSize.sm,
    color: colors.neutral[600],
    spacing: spacing[2],
  },

  // Progress indicators for task completion
  progress: {
    height: '8px',
    borderRadius: borderRadius.full,
    background: colors.neutral[200],
    fill: colors.primary[500],
  },

  // Status indicators with clear meaning
  status: {
    todo: colors.neutral[400],
    inProgress: colors.semantic.info.base,
    complete: colors.semantic.success.base,
    blocked: colors.semantic.error.base,
    paused: colors.semantic.warning.base,
  },
};

// Export complete design system
export const designTokens = {
  colors,
  typography,
  spacing,
  borderRadius,
  shadows,
  breakpoints,
  zIndex,
  animation,
  focus,
  executiveFunction,
} as const;

// Type definitions for TypeScript
export type ColorToken = keyof typeof colors.neutral;
export type SpacingToken = keyof typeof spacing;
export type TypographySize = keyof typeof typography.fontSize;
export type BreakpointToken = keyof typeof breakpoints;