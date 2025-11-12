/**
 * Theme System for Mental Prosthetic Platform
 * 
 * Provides consistent theming across all domains while allowing
 * domain-specific customizations and executive function accommodations.
 */

import { designTokens, colors } from './design-tokens';

// Theme configuration interface
export interface ThemeConfig {
  domain: 'security' | 'productivity' | 'tcg' | 'infrastructure' | 'finance' | 'core';
  variant: 'light' | 'dark' | 'high-contrast';
  executiveFunctionMode: 'standard' | 'enhanced' | 'minimal';
  reducedMotion: boolean;
  dyslexicFont: boolean;
}

// Base theme structure
export interface Theme {
  colors: {
    primary: string;
    secondary: string;
    accent: string;
    background: string;
    surface: string;
    text: {
      primary: string;
      secondary: string;
      disabled: string;
      inverse: string;
    };
    border: {
      default: string;
      focus: string;
      error: string;
    };
    status: {
      success: string;
      warning: string;
      error: string;
      info: string;
    };
  };
  typography: {
    fontFamily: string;
    scale: typeof designTokens.typography.fontSize;
    weights: typeof designTokens.typography.fontWeight;
    lineHeight: typeof designTokens.typography.lineHeight;
  };
  spacing: typeof designTokens.spacing;
  shadows: typeof designTokens.shadows;
  animation: typeof designTokens.animation;
  focus: typeof designTokens.focus;
  executiveFunction: typeof designTokens.executiveFunction;
}

// Create base theme
function createBaseTheme(config: ThemeConfig): Theme {
  const { domain, variant, executiveFunctionMode, reducedMotion, dyslexicFont } = config;
  
  // Domain-specific colors
  const domainColors = domain === 'core' 
    ? colors.domains.productivity 
    : colors.domains[domain as keyof typeof colors.domains] || colors.domains.productivity;
  
  // Variant-specific color adjustments
  const variantColors = getVariantColors(variant, domainColors);
  
  // Executive function adjustments
  const execColors = getExecutiveFunctionColors(executiveFunctionMode, variantColors);
  
  return {
    colors: execColors,
    typography: {
      fontFamily: dyslexicFont 
        ? designTokens.typography.fontFamily.dyslexic
        : designTokens.typography.fontFamily.base,
      scale: designTokens.typography.fontSize,
      weights: designTokens.typography.fontWeight,
      lineHeight: executiveFunctionMode === 'enhanced' 
        ? { ...designTokens.typography.lineHeight, normal: 1.6, relaxed: 1.8 }
        : designTokens.typography.lineHeight,
    },
    spacing: designTokens.spacing,
    shadows: variant === 'high-contrast' 
      ? { ...designTokens.shadows, base: 'none', md: 'none', lg: 'none' }
      : designTokens.shadows,
    animation: reducedMotion 
      ? { 
          ...designTokens.animation, 
          duration: {
            fast: designTokens.animation.reducedMotion.duration,
            normal: designTokens.animation.reducedMotion.duration,
            slow: designTokens.animation.reducedMotion.duration,
            slower: designTokens.animation.reducedMotion.duration,
          }
        }
      : designTokens.animation,
    focus: variant === 'high-contrast'
      ? { ring: designTokens.focus.highContrast, highContrast: designTokens.focus.highContrast }
      : designTokens.focus,
    executiveFunction: designTokens.executiveFunction,
  };
}

// Variant-specific color logic
function getVariantColors(variant: ThemeConfig['variant'], domainColors: any) {
  switch (variant) {
    case 'dark':
      return {
        primary: domainColors.primary,
        secondary: domainColors.secondary,
        accent: domainColors.accent,
        background: colors.neutral[900],
        surface: colors.neutral[800],
        text: {
          primary: colors.neutral[50],
          secondary: colors.neutral[300],
          disabled: colors.neutral[500],
          inverse: colors.neutral[900],
        },
        border: {
          default: colors.neutral[700],
          focus: domainColors.primary,
          error: colors.semantic.error.base,
        },
        status: {
          success: colors.semantic.success.base,
          warning: colors.semantic.warning.base,
          error: colors.semantic.error.base,
          info: colors.semantic.info.base,
        },
      };

    case 'high-contrast':
      return {
        primary: '#000000',
        secondary: '#333333',
        accent: domainColors.accent,
        background: '#ffffff',
        surface: '#f5f5f5',
        text: {
          primary: '#000000',
          secondary: '#333333',
          disabled: '#666666',
          inverse: '#ffffff',
        },
        border: {
          default: '#000000',
          focus: '#000000',
          error: '#cc0000',
        },
        status: {
          success: '#008000',
          warning: '#ff8c00',
          error: '#cc0000',
          info: '#0000cc',
        },
      };

    default: // light
      return {
        primary: domainColors.primary,
        secondary: domainColors.secondary,
        accent: domainColors.accent,
        background: domainColors.background,
        surface: domainColors.surface,
        text: {
          primary: colors.neutral[900],
          secondary: colors.neutral[700],
          disabled: colors.neutral[400],
          inverse: colors.neutral[50],
        },
        border: {
          default: colors.neutral[300],
          focus: domainColors.primary,
          error: colors.semantic.error.base,
        },
        status: {
          success: colors.semantic.success.base,
          warning: colors.semantic.warning.base,
          error: colors.semantic.error.base,
          info: colors.semantic.info.base,
        },
      };
  }
}

// Executive function color adjustments
function getExecutiveFunctionColors(mode: ThemeConfig['executiveFunctionMode'], baseColors: any) {
  switch (mode) {
    case 'enhanced':
      // Higher contrast and more distinctive colors
      return {
        ...baseColors,
        text: {
          ...baseColors.text,
          primary: '#000000', // Always black for maximum contrast
        },
        border: {
          ...baseColors.border,
          focus: '#0066cc', // Strong blue for focus
        },
      };

    case 'minimal':
      // Reduced visual noise
      return {
        ...baseColors,
        border: {
          ...baseColors.border,
          default: 'transparent',
        },
      };

    default: // standard
      return baseColors;
  }
}

// Pre-defined themes for each domain
export const securityTheme = createBaseTheme({
  domain: 'security',
  variant: 'light',
  executiveFunctionMode: 'enhanced', // Enhanced for critical security work
  reducedMotion: false,
  dyslexicFont: false,
});

export const productivityTheme = createBaseTheme({
  domain: 'productivity',
  variant: 'light',
  executiveFunctionMode: 'enhanced', // Enhanced for focus
  reducedMotion: false,
  dyslexicFont: false,
});

export const tcgTheme = createBaseTheme({
  domain: 'tcg',
  variant: 'light',
  executiveFunctionMode: 'standard',
  reducedMotion: false,
  dyslexicFont: false,
});

export const infrastructureTheme = createBaseTheme({
  domain: 'infrastructure',
  variant: 'light',
  executiveFunctionMode: 'standard',
  reducedMotion: false,
  dyslexicFont: false,
});

export const financeTheme = createBaseTheme({
  domain: 'finance',
  variant: 'light',
  executiveFunctionMode: 'enhanced', // Enhanced for financial accuracy
  reducedMotion: false,
  dyslexicFont: false,
});

// Theme registry
export const themes = {
  security: securityTheme,
  productivity: productivityTheme,
  tcg: tcgTheme,
  infrastructure: infrastructureTheme,
  finance: financeTheme,
} as const;

// CSS Custom Properties generator
export function generateCSSCustomProperties(theme: Theme): Record<string, string> {
  return {
    // Colors
    '--color-primary': theme.colors.primary,
    '--color-secondary': theme.colors.secondary,
    '--color-accent': theme.colors.accent,
    '--color-background': theme.colors.background,
    '--color-surface': theme.colors.surface,
    
    '--color-text-primary': theme.colors.text.primary,
    '--color-text-secondary': theme.colors.text.secondary,
    '--color-text-disabled': theme.colors.text.disabled,
    '--color-text-inverse': theme.colors.text.inverse,
    
    '--color-border-default': theme.colors.border.default,
    '--color-border-focus': theme.colors.border.focus,
    '--color-border-error': theme.colors.border.error,
    
    '--color-status-success': theme.colors.status.success,
    '--color-status-warning': theme.colors.status.warning,
    '--color-status-error': theme.colors.status.error,
    '--color-status-info': theme.colors.status.info,
    
    // Typography
    '--font-family': theme.typography.fontFamily,
    '--font-size-xs': theme.typography.scale.xs,
    '--font-size-sm': theme.typography.scale.sm,
    '--font-size-base': theme.typography.scale.base,
    '--font-size-lg': theme.typography.scale.lg,
    '--font-size-xl': theme.typography.scale.xl,
    '--font-size-2xl': theme.typography.scale['2xl'],
    
    '--font-weight-normal': theme.typography.weights.normal.toString(),
    '--font-weight-medium': theme.typography.weights.medium.toString(),
    '--font-weight-semibold': theme.typography.weights.semibold.toString(),
    '--font-weight-bold': theme.typography.weights.bold.toString(),
    
    '--line-height-tight': theme.typography.lineHeight.tight.toString(),
    '--line-height-normal': theme.typography.lineHeight.normal.toString(),
    '--line-height-relaxed': theme.typography.lineHeight.relaxed.toString(),
    
    // Spacing
    '--spacing-1': theme.spacing[1],
    '--spacing-2': theme.spacing[2],
    '--spacing-3': theme.spacing[3],
    '--spacing-4': theme.spacing[4],
    '--spacing-6': theme.spacing[6],
    '--spacing-8': theme.spacing[8],
    '--spacing-12': theme.spacing[12],
    '--spacing-16': theme.spacing[16],
    
    // Focus
    '--focus-ring-width': theme.focus.ring.width,
    '--focus-ring-color': theme.focus.ring.color,
    '--focus-ring-offset': theme.focus.ring.offset,
    
    // Animation
    '--animation-duration-fast': theme.animation.duration.fast,
    '--animation-duration-normal': theme.animation.duration.normal,
    '--animation-duration-slow': theme.animation.duration.slow,
    '--animation-easing-out': theme.animation.easing.out,
  };
}

// CSS string generator for injection
export function generateThemeCSS(theme: Theme): string {
  const properties = generateCSSCustomProperties(theme);
  const cssRules = Object.entries(properties)
    .map(([property, value]) => `  ${property}: ${value};`)
    .join('\n');
    
  return `:root {\n${cssRules}\n}`;
}

// Theme factory function
export function createTheme(config: ThemeConfig): Theme {
  return createBaseTheme(config);
}

// Theme utilities
export const themeUtils = {
  // Get color with opacity
  withOpacity: (color: string, opacity: number): string => {
    // Simple implementation - in practice would use a color library
    return `${color}${Math.round(opacity * 255).toString(16).padStart(2, '0')}`;
  },
  
  // Get contrasting text color
  getContrastText: (backgroundColor: string, theme: Theme): string => {
    // Simple implementation - would use proper contrast calculation
    return backgroundColor === theme.colors.background 
      ? theme.colors.text.primary 
      : theme.colors.text.inverse;
  },
  
  // Responsive breakpoint helper
  breakpoint: (size: keyof typeof designTokens.breakpoints): string => {
    return `@media (min-width: ${designTokens.breakpoints[size]})`;
  },
};

export type ThemeName = keyof typeof themes;