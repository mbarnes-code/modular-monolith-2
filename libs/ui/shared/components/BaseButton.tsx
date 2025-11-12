/**
 * Base Button Component for Mental Prosthetic Platform
 * 
 * Provides a foundation button with accessibility, theming, and 
 * executive function accommodations built-in.
 */

import React, { forwardRef, ReactNode } from 'react';
import { a11y } from '../foundation/accessibility';
import { Theme } from '../foundation/theme';

// Button variants for different contexts
export type ButtonVariant = 
  | 'primary'     // Main action buttons
  | 'secondary'   // Secondary actions
  | 'outline'     // Less prominent actions
  | 'ghost'       // Minimal visual impact
  | 'danger'      // Destructive actions
  | 'success'     // Positive confirmations;

// Button sizes for different contexts
export type ButtonSize = 'xs' | 'sm' | 'md' | 'lg' | 'xl';

// Loading states for executive function feedback
export type ButtonLoadingState = 'idle' | 'loading' | 'success' | 'error';

export interface BaseButtonProps {
  // Core functionality
  children: ReactNode;
  variant?: ButtonVariant;
  size?: ButtonSize;
  
  // State management
  disabled?: boolean;
  loading?: boolean;
  loadingState?: ButtonLoadingState;
  
  // Interaction handlers
  onClick?: (event: React.MouseEvent<HTMLButtonElement>) => void;
  onFocus?: (event: React.FocusEvent<HTMLButtonElement>) => void;
  onBlur?: (event: React.FocusEvent<HTMLButtonElement>) => void;
  
  // Accessibility
  'aria-label'?: string;
  'aria-describedby'?: string;
  'aria-expanded'?: boolean;
  'aria-controls'?: string;
  'aria-pressed'?: boolean;
  title?: string;
  
  // Executive function support
  confirmationRequired?: boolean;
  confirmationMessage?: string;
  showLoadingText?: boolean;
  loadingText?: string;
  successMessage?: string;
  errorMessage?: string;
  
  // Visual customization
  fullWidth?: boolean;
  icon?: ReactNode;
  iconPosition?: 'left' | 'right';
  
  // HTML attributes
  type?: 'button' | 'submit' | 'reset';
  form?: string;
  name?: string;
  value?: string;
  
  // CSS customization
  className?: string;
  style?: React.CSSProperties;
  
  // Theme context (injected by provider)
  theme?: Theme;
}

// Get variant-specific styles
const getVariantStyles = (variant: ButtonVariant, theme?: Theme) => {
  const colors = theme?.colors || {
    primary: '#3b82f6',
    secondary: '#6b7280',
    accent: '#10b981',
    background: '#ffffff',
    surface: '#f9fafb',
    text: { primary: '#111827', secondary: '#6b7280', inverse: '#ffffff' },
    status: { success: '#10b981', error: '#ef4444', warning: '#f59e0b' }
  };
  
  const baseStyles = {
    border: 'none',
    borderRadius: '0.375rem',
    cursor: 'pointer',
    fontWeight: '500',
    transition: 'all 0.15s ease-in-out',
    display: 'inline-flex',
    alignItems: 'center',
    justifyContent: 'center',
    gap: '0.5rem',
    textDecoration: 'none',
    
    // Focus styles for accessibility
    '&:focus-visible': {
      outline: `2px solid ${colors.primary}`,
      outlineOffset: '2px',
    },
    
    // Disabled styles
    '&:disabled': {
      cursor: 'not-allowed',
      opacity: 0.6,
    },
  };
  
  switch (variant) {
    case 'primary':
      return {
        ...baseStyles,
        backgroundColor: colors.primary,
        color: colors.text.inverse,
        '&:hover:not(:disabled)': {
          backgroundColor: `${colors.primary}dd`, // Slightly transparent
          transform: 'translateY(-1px)',
        },
        '&:active:not(:disabled)': {
          transform: 'translateY(0)',
        },
      };
      
    case 'secondary':
      return {
        ...baseStyles,
        backgroundColor: colors.surface,
        color: colors.text.primary,
        border: `1px solid ${colors.secondary}`,
        '&:hover:not(:disabled)': {
          backgroundColor: colors.background,
          borderColor: colors.primary,
        },
      };
      
    case 'outline':
      return {
        ...baseStyles,
        backgroundColor: 'transparent',
        color: colors.primary,
        border: `1px solid ${colors.primary}`,
        '&:hover:not(:disabled)': {
          backgroundColor: colors.primary,
          color: colors.text.inverse,
        },
      };
      
    case 'ghost':
      return {
        ...baseStyles,
        backgroundColor: 'transparent',
        color: colors.text.secondary,
        '&:hover:not(:disabled)': {
          backgroundColor: colors.surface,
          color: colors.text.primary,
        },
      };
      
    case 'danger':
      return {
        ...baseStyles,
        backgroundColor: colors.status.error,
        color: colors.text.inverse,
        '&:hover:not(:disabled)': {
          backgroundColor: `${colors.status.error}dd`,
          transform: 'translateY(-1px)',
        },
      };
      
    case 'success':
      return {
        ...baseStyles,
        backgroundColor: colors.status.success,
        color: colors.text.inverse,
        '&:hover:not(:disabled)': {
          backgroundColor: `${colors.status.success}dd`,
          transform: 'translateY(-1px)',
        },
      };
      
    default:
      return baseStyles;
  }
};

// Get size-specific styles
const getSizeStyles = (size: ButtonSize, theme?: Theme) => {
  const spacing = theme?.spacing || {
    1: '0.25rem',
    2: '0.5rem', 
    3: '0.75rem',
    4: '1rem',
    6: '1.5rem',
  };
  
  const fontSize = theme?.typography.scale || {
    xs: '0.75rem',
    sm: '0.875rem',
    base: '1rem',
    lg: '1.125rem',
    xl: '1.25rem',
  };
  
  switch (size) {
    case 'xs':
      return {
        padding: `${spacing[1]} ${spacing[2]}`,
        fontSize: fontSize.xs,
        minHeight: '1.5rem',
      };
    case 'sm':
      return {
        padding: `${spacing[2]} ${spacing[3]}`,
        fontSize: fontSize.sm,
        minHeight: '2rem',
      };
    case 'md':
      return {
        padding: `${spacing[2]} ${spacing[4]}`,
        fontSize: fontSize.base,
        minHeight: '2.5rem',
      };
    case 'lg':
      return {
        padding: `${spacing[3]} ${spacing[6]}`,
        fontSize: fontSize.lg,
        minHeight: '3rem',
      };
    case 'xl':
      return {
        padding: `${spacing[4]} ${spacing[6]}`,
        fontSize: fontSize.xl,
        minHeight: '3.5rem',
      };
    default:
      return {
        padding: `${spacing[2]} ${spacing[4]}`,
        fontSize: fontSize.base,
        minHeight: '2.5rem',
      };
  }
};

// Loading spinner component
const LoadingSpinner: React.FC<{ size: ButtonSize }> = ({ size }) => {
  const spinnerSize = {
    xs: '12px',
    sm: '14px', 
    md: '16px',
    lg: '18px',
    xl: '20px',
  }[size];
  
  return (
    <svg
      width={spinnerSize}
      height={spinnerSize}
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
      style={{
        animation: 'spin 1s linear infinite',
      }}
    >
      <path d="M21 12a9 9 0 11-6.219-8.56"/>
    </svg>
  );
};

// Success/Error icons
const StatusIcon: React.FC<{ status: 'success' | 'error'; size: ButtonSize }> = ({ status, size }) => {
  const iconSize = {
    xs: '12px',
    sm: '14px',
    md: '16px', 
    lg: '18px',
    xl: '20px',
  }[size];
  
  if (status === 'success') {
    return (
      <svg width={iconSize} height={iconSize} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
        <path d="M20 6L9 17l-5-5"/>
      </svg>
    );
  }
  
  return (
    <svg width={iconSize} height={iconSize} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
      <circle cx="12" cy="12" r="10"/>
      <line x1="15" y1="9" x2="9" y2="15"/>
      <line x1="9" y1="9" x2="15" y2="15"/>
    </svg>
  );
};

export const BaseButton = forwardRef<HTMLButtonElement, BaseButtonProps>(
  ({
    children,
    variant = 'primary',
    size = 'md',
    disabled = false,
    loading = false,
    loadingState = 'idle',
    onClick,
    onFocus,
    onBlur,
    confirmationRequired = false,
    confirmationMessage = 'Are you sure?',
    showLoadingText = true,
    loadingText = 'Loading...',
    successMessage,
    errorMessage,
    fullWidth = false,
    icon,
    iconPosition = 'left',
    type = 'button',
    className = '',
    style = {},
    theme,
    ...ariaProps
  }, ref) => {
    const [isConfirming, setIsConfirming] = React.useState(false);
    const [internalLoadingState, setInternalLoadingState] = React.useState<ButtonLoadingState>('idle');
    
    // Use external loading state or internal state
    const currentLoadingState = loading ? 'loading' : loadingState || internalLoadingState;
    const isLoading = currentLoadingState === 'loading';
    const isDisabled = disabled || isLoading;
    
    // Handle click with confirmation and loading states
    const handleClick = async (event: React.MouseEvent<HTMLButtonElement>) => {
      if (isDisabled) return;
      
      // Handle confirmation flow
      if (confirmationRequired && !isConfirming) {
        const confirmed = window.confirm(confirmationMessage);
        if (!confirmed) return;
        setIsConfirming(true);
      }
      
      // Execute click handler
      if (onClick) {
        try {
          setInternalLoadingState('loading');
          
          // Announce loading state for screen readers
          a11y.aria.announce('Button activated, processing...', 'polite');
          
          await onClick(event);
          
          setInternalLoadingState('success');
          
          // Announce success
          if (successMessage) {
            a11y.aria.announce(successMessage, 'polite');
          }
          
          // Reset state after brief success display
          setTimeout(() => {
            setInternalLoadingState('idle');
            setIsConfirming(false);
          }, 1500);
          
        } catch (error) {
          setInternalLoadingState('error');
          
          // Announce error
          const errorMsg = errorMessage || 'Action failed. Please try again.';
          a11y.aria.announce(errorMsg, 'assertive');
          
          // Reset state after error display
          setTimeout(() => {
            setInternalLoadingState('idle');
            setIsConfirming(false);
          }, 3000);
        }
      }
    };
    
    // Build ARIA attributes
    const ariaAttributes = a11y.aria.buildAttributes({
      ...ariaProps,
      disabled: isDisabled,
      busy: isLoading,
    });
    
    // Determine button content based on state
    const getButtonContent = () => {
      if (currentLoadingState === 'loading') {
        return (
          <>
            <LoadingSpinner size={size} />
            {showLoadingText && loadingText}
          </>
        );
      }
      
      if (currentLoadingState === 'success' && successMessage) {
        return (
          <>
            <StatusIcon status="success" size={size} />
            {successMessage}
          </>
        );
      }
      
      if (currentLoadingState === 'error' && errorMessage) {
        return (
          <>
            <StatusIcon status="error" size={size} />
            {errorMessage}
          </>
        );
      }
      
      // Normal state content
      return (
        <>
          {icon && iconPosition === 'left' && icon}
          {children}
          {icon && iconPosition === 'right' && icon}
        </>
      );
    };
    
    // Combine styles
    const variantStyles = getVariantStyles(variant, theme);
    const sizeStyles = getSizeStyles(size, theme);
    
    const combinedStyles = {
      ...variantStyles,
      ...sizeStyles,
      width: fullWidth ? '100%' : 'auto',
      ...style,
    };
    
    // Add spinner animation CSS if not already present
    React.useEffect(() => {
      if (!document.querySelector('#button-spinner-styles')) {
        const style = document.createElement('style');
        style.id = 'button-spinner-styles';
        style.textContent = `
          @keyframes spin {
            from { transform: rotate(0deg); }
            to { transform: rotate(360deg); }
          }
        `;
        document.head.appendChild(style);
      }
    }, []);
    
    return (
      <button
        ref={ref}
        type={type}
        className={`base-button base-button--${variant} base-button--${size} ${className}`}
        style={combinedStyles}
        disabled={isDisabled}
        onClick={handleClick}
        onFocus={onFocus}
        onBlur={onBlur}
        {...ariaAttributes}
      >
        {getButtonContent()}
      </button>
    );
  }
);

BaseButton.displayName = 'BaseButton';

// Higher-order component for themed buttons
export const withTheme = (theme: Theme) => {
  return forwardRef<HTMLButtonElement, Omit<BaseButtonProps, 'theme'>>((props, ref) => (
    <BaseButton ref={ref} {...props} theme={theme} />
  ));
};

// Export types for domain-specific extensions
export type { BaseButtonProps, ButtonLoadingState, ButtonSize, ButtonVariant };
