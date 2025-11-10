/**
 * Mobile Theme Configuration
 * 
 * Executive function-focused mobile design system
 * Optimized for ADHD/autism accommodations on touch devices
 */

export const mobileTheme = {
  // Touch target sizes (iOS Human Interface Guidelines)
  touchTargets: {
    minimum: 44, // Minimum touch target size in pixels
    comfortable: 48, // Comfortable touch target size
    large: 52, // Large touch target for accessibility
    extraLarge: 56, // Extra large for complex actions
  },

  // Mobile-specific spacing
  spacing: {
    touch: {
      xs: 8, // Extra small spacing for touch interfaces
      sm: 12, // Small spacing
      md: 16, // Medium spacing (default)
      lg: 24, // Large spacing
      xl: 32, // Extra large spacing
    },
    // Safe areas for devices with notches/home indicators
    safeArea: {
      top: 44, // Status bar area
      bottom: 34, // Home indicator area (iPhone X+)
      sides: 16, // Left/right safe margins
    },
  },

  // Typography optimized for mobile screens
  typography: {
    mobile: {
      // Prevent zoom on iOS by ensuring 16px minimum
      minFontSize: 16,
      sizes: {
        xs: { fontSize: 16, lineHeight: 1.4 },  // Increased from 14px
        sm: { fontSize: 16, lineHeight: 1.4 },  // Increased from 14px  
        base: { fontSize: 18, lineHeight: 1.5 }, // Increased from 16px
        lg: { fontSize: 20, lineHeight: 1.5 },  // Increased from 18px
        xl: { fontSize: 24, lineHeight: 1.4 },  // Increased from 20px
        '2xl': { fontSize: 28, lineHeight: 1.3 }, // Increased from 24px
        '3xl': { fontSize: 32, lineHeight: 1.2 }, // Increased from 30px
      },
      // Reading optimizations for executive function
      reading: {
        lineHeight: 1.6, // Increased line height for better readability
        letterSpacing: '0.025em', // Slight letter spacing for dyslexia support
        wordSpacing: '0.1em', // Slight word spacing
      },
    },
  },

  // Color system optimized for mobile screens
  colors: {
    // High contrast options for executive function support
    highContrast: {
      foreground: '#000000',
      background: '#FFFFFF',
      primary: '#000000',
      secondary: '#666666',
      accent: '#0066CC',
      error: '#CC0000',
      success: '#006600',
      warning: '#CC6600',
    },
    
    // Standard color palette
    standard: {
      // Primary blue - calming for ADHD
      primary: {
        50: '#eff6ff',
        100: '#dbeafe',
        500: '#3b82f6',
        600: '#2563eb',
        700: '#1d4ed8',
        900: '#1e3a8a',
      },
      
      // Success green - positive reinforcement
      success: {
        50: '#f0fdf4',
        100: '#dcfce7',
        500: '#22c55e',
        600: '#16a34a',
        700: '#15803d',
      },
      
      // Warning amber - attention without anxiety
      warning: {
        50: '#fffbeb',
        100: '#fef3c7',
        500: '#f59e0b',
        600: '#d97706',
        700: '#b45309',
      },
      
      // Error red - clear but not alarming
      error: {
        50: '#fef2f2',
        100: '#fee2e2',
        500: '#ef4444',
        600: '#dc2626',
        700: '#b91c1c',
      },
    },
  },

  // Mobile-specific animations
  animations: {
    // Reduced motion for accessibility
    reducedMotion: {
      transition: 'none',
      animation: 'none',
    },
    
    // Standard animations optimized for touch
    standard: {
      fast: '150ms ease-out',
      normal: '250ms ease-out',
      slow: '400ms ease-out',
    },
    
    // Touch feedback animations
    touch: {
      press: 'transform 100ms ease-out',
      release: 'transform 150ms ease-out',
      ripple: 'opacity 300ms ease-out, transform 300ms ease-out',
    },
  },

  // Mobile breakpoints
  breakpoints: {
    mobile: {
      small: '320px',  // iPhone SE
      medium: '375px', // iPhone 12/13 Mini
      large: '414px',  // iPhone 12/13 Pro Max
    },
    tablet: {
      small: '768px',  // iPad Mini
      large: '1024px', // iPad Pro
    },
  },

  // Gesture configurations
  gestures: {
    // Swipe sensitivity
    swipe: {
      threshold: 50, // Minimum distance for swipe recognition
      velocity: 0.3, // Minimum velocity
    },
    
    // Long press configuration
    longPress: {
      duration: 500, // Milliseconds to trigger long press
      tolerance: 10,  // Movement tolerance during long press
    },
    
    // Tap configuration
    tap: {
      maxDuration: 200, // Maximum duration for tap
      tolerance: 10,    // Movement tolerance
    },
  },

  // Haptic feedback patterns
  haptics: {
    light: [10],           // Light tap
    medium: [20],          // Medium tap
    heavy: [30],           // Heavy tap
    success: [10, 50, 10], // Success pattern
    error: [50, 100, 50],  // Error pattern
    warning: [20, 20, 20], // Warning pattern
  },

  // Executive function specific configurations
  executiveFunction: {
    // Focus indicators
    focus: {
      ringWidth: 3,           // Focus ring width
      ringColor: '#2563eb',   // Focus ring color
      ringOpacity: 0.6,       // Focus ring opacity
      animationDuration: 150, // Focus animation duration
    },
    
    // Context preservation
    context: {
      preservationDelay: 100,    // Delay before context changes
      transitionDuration: 200,   // Context transition duration
      breadcrumbHeight: 44,      // Mobile breadcrumb height
    },
    
    // Cognitive load indicators
    cognitiveLoad: {
      low: { color: '#22c55e', threshold: 30 },
      medium: { color: '#f59e0b', threshold: 70 },
      high: { color: '#ef4444', threshold: 100 },
    },
  },

  // Accessibility enhancements
  accessibility: {
    // Minimum contrast ratios
    contrast: {
      normal: 4.5,  // WCAG AA
      large: 3.0,   // WCAG AA for large text
      enhanced: 7.0, // WCAG AAA
    },
    
    // Focus management
    focusManagement: {
      skipLinkHeight: 44,
      focusRingWidth: 3,
      focusRingOffset: 2,
    },
    
    // Screen reader optimizations
    screenReader: {
      announceDelay: 100,  // Delay before announcements
      politeness: 'polite', // Default aria-live politeness
    },
  },
} as const;

// Export individual theme sections for easier imports
export const {
  touchTargets,
  spacing,
  typography,
  colors,
  animations,
  breakpoints,
  gestures,
  haptics,
  executiveFunction,
  accessibility,
} = mobileTheme;

// Utility functions for theme usage
export const getMobileSpacing = (size: keyof typeof spacing.touch) => spacing.touch[size];
export const getTouchTarget = (size: keyof typeof touchTargets) => touchTargets[size];
export const getHapticPattern = (type: keyof typeof haptics) => haptics[type];

// Media queries for responsive design
export const mediaQueries = {
  mobile: `@media (max-width: ${breakpoints.tablet.small})`,
  tablet: `@media (min-width: ${breakpoints.tablet.small}) and (max-width: ${breakpoints.tablet.large})`,
  desktop: `@media (min-width: ${breakpoints.tablet.large})`,
  touch: '@media (pointer: coarse)',
  hover: '@media (hover: hover)',
  reducedMotion: '@media (prefers-reduced-motion: reduce)',
  highContrast: '@media (prefers-contrast: high)',
} as const;