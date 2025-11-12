/**
 * Base Card Component for Mental Prosthetic Platform
 * 
 * Provides foundation card/container functionality with accessibility,
 * theming, and executive function accommodations built-in.
 */

import React, { forwardRef, KeyboardEvent, MouseEvent, ReactNode } from 'react';
import { a11y } from '../foundation/accessibility';
import { Theme } from '../foundation/theme';

// Card variants for different contexts
export type CardVariant = 'elevated' | 'outlined' | 'filled' | 'ghost';

// Card sizes
export type CardSize = 'sm' | 'md' | 'lg' | 'xl';

// Card padding options
export type CardPadding = 'none' | 'sm' | 'md' | 'lg';

// Card interaction states
export type CardInteractionState = 'idle' | 'hover' | 'focus' | 'active';

export interface BaseCardProps {
  // Content
  children?: ReactNode;
  
  // Visual customization
  variant?: CardVariant;
  size?: CardSize;
  padding?: CardPadding;
  
  // Layout
  fullWidth?: boolean;
  fullHeight?: boolean;
  
  // Interactive behavior
  clickable?: boolean;
  disabled?: boolean;
  loading?: boolean;
  
  // Event handlers
  onClick?: (event: MouseEvent<HTMLDivElement>) => void;
  onKeyDown?: (event: KeyboardEvent<HTMLDivElement>) => void;
  onMouseEnter?: (event: MouseEvent<HTMLDivElement>) => void;
  onMouseLeave?: (event: MouseEvent<HTMLDivElement>) => void;
  onFocus?: (event: React.FocusEvent<HTMLDivElement>) => void;
  onBlur?: (event: React.FocusEvent<HTMLDivElement>) => void;
  
  // Header section
  header?: ReactNode;
  title?: string;
  subtitle?: string;
  headerActions?: ReactNode;
  
  // Footer section
  footer?: ReactNode;
  actions?: ReactNode;
  
  // Executive function support
  contextualHelp?: string;
  progressIndicator?: {
    current: number;
    total: number;
    label?: string;
  };
  
  // Status indicators
  status?: 'default' | 'success' | 'warning' | 'error' | 'info';
  statusMessage?: string;
  
  // Accessibility
  'aria-label'?: string;
  'aria-labelledby'?: string;
  'aria-describedby'?: string;
  role?: string;
  tabIndex?: number;
  id?: string;
  
  // CSS customization
  className?: string;
  style?: React.CSSProperties;
  
  // Theme context
  theme?: Theme;
}

// Status icon component
const StatusIcon: React.FC<{ status: 'success' | 'warning' | 'error' | 'info'; size?: number }> = ({ 
  status, 
  size = 16 
}) => {
  const getStatusColor = () => {
    switch (status) {
      case 'success': return '#10b981';
      case 'warning': return '#f59e0b';
      case 'error': return '#ef4444';
      case 'info': return '#3b82f6';
      default: return '#6b7280';
    }
  };
  
  const color = getStatusColor();
  
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 24 24"
      fill="none"
      stroke={color}
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
      aria-hidden="true"
    >
      {status === 'success' && (
        <>
          <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/>
          <polyline points="22,4 12,14.01 9,11.01"/>
        </>
      )}
      {status === 'warning' && (
        <>
          <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/>
          <line x1="12" y1="9" x2="12" y2="13"/>
          <line x1="12" y1="17" x2="12.01" y2="17"/>
        </>
      )}
      {status === 'error' && (
        <>
          <circle cx="12" cy="12" r="10"/>
          <line x1="15" y1="9" x2="9" y2="15"/>
          <line x1="9" y1="9" x2="15" y2="15"/>
        </>
      )}
      {status === 'info' && (
        <>
          <circle cx="12" cy="12" r="10"/>
          <line x1="12" y1="16" x2="12" y2="12"/>
          <line x1="12" y1="8" x2="12.01" y2="8"/>
        </>
      )}
    </svg>
  );
};

// Loading spinner component
const LoadingSpinner: React.FC<{ size?: number; color?: string }> = ({ 
  size = 20, 
  color = '#3b82f6' 
}) => (
  <svg
    width={size}
    height={size}
    viewBox="0 0 24 24"
    fill="none"
    stroke={color}
    strokeWidth="2"
    strokeLinecap="round"
    strokeLinejoin="round"
    style={{ animation: 'spin 1s linear infinite' }}
    aria-hidden="true"
  >
    <path d="M21 12a9 9 0 11-6.219-8.56"/>
  </svg>
);

// Get variant-specific styles
const getVariantStyles = (variant: CardVariant, theme?: Theme): React.CSSProperties => {
  const colors = theme?.colors || {
    background: '#ffffff',
    surface: '#f9fafb',
    border: { default: '#e5e7eb' },
  };
  
  // Use theme shadows if available, otherwise fallback to defaults
  const shadows = {
    sm: '0 1px 2px 0 rgb(0 0 0 / 0.05)',
    md: '0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1)',
    lg: '0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1)',
  };
  
  const borderHover = '#d1d5db';
  
  const baseStyles: React.CSSProperties = {
    borderRadius: '0.5rem',
    transition: 'all 0.15s ease-in-out',
  };
  
  switch (variant) {
    case 'elevated':
      return {
        ...baseStyles,
        backgroundColor: colors.background,
        boxShadow: shadows.md,
        border: 'none',
      };
      
    case 'outlined':
      return {
        ...baseStyles,
        backgroundColor: colors.background,
        border: `1px solid ${colors.border?.default || '#e5e7eb'}`,
        boxShadow: 'none',
      };
      
    case 'filled':
      return {
        ...baseStyles,
        backgroundColor: colors.surface,
        border: 'none',
        boxShadow: 'none',
      };
      
    case 'ghost':
      return {
        ...baseStyles,
        backgroundColor: 'transparent',
        border: 'none',
        boxShadow: 'none',
      };
      
    default:
      return {
        ...baseStyles,
        backgroundColor: colors.background,
        border: `1px solid ${colors.border?.default || '#e5e7eb'}`,
        boxShadow: shadows.sm,
      };
  }
};

// Get size-specific styles
const getSizeStyles = (size: CardSize) => {
  switch (size) {
    case 'sm':
      return {
        minWidth: '12rem',
        maxWidth: '24rem',
      };
    case 'lg':
      return {
        minWidth: '24rem',
        maxWidth: '48rem',
      };
    case 'xl':
      return {
        minWidth: '32rem',
        maxWidth: '64rem',
      };
    default: // 'md'
      return {
        minWidth: '16rem',
        maxWidth: '32rem',
      };
  }
};

// Get padding styles
const getPaddingStyles = (padding: CardPadding, theme?: Theme) => {
  const spacing = theme?.spacing || {
    4: '1rem',
    6: '1.5rem',
    8: '2rem',
  };
  
  switch (padding) {
    case 'none':
      return { padding: '0' };
    case 'sm':
      return { padding: spacing[4] };
    case 'lg':
      return { padding: spacing[8] };
    default: // 'md'
      return { padding: spacing[6] };
  }
};

export const BaseCard = forwardRef<HTMLDivElement, BaseCardProps>(
  ({
    children,
    variant = 'elevated',
    size = 'md',
    padding = 'md',
    fullWidth = false,
    fullHeight = false,
    clickable = false,
    disabled = false,
    loading = false,
    onClick,
    onKeyDown,
    onMouseEnter,
    onMouseLeave,
    onFocus,
    onBlur,
    header,
    title,
    subtitle,
    headerActions,
    footer,
    actions,
    contextualHelp,
    progressIndicator,
    status = 'default',
    statusMessage,
    role,
    tabIndex,
    id,
    className = '',
    style = {},
    theme,
    ...ariaProps
  }, ref) => {
    
    // Handle click events
    const handleClick = (event: MouseEvent<HTMLDivElement>) => {
      if (disabled || loading) return;
      
      if (onClick) {
        onClick(event);
      }
    };
    
    // Handle keyboard events for accessibility
    const handleKeyDown = (event: KeyboardEvent<HTMLDivElement>) => {
      if (disabled || loading) return;
      
      if (clickable && (event.key === 'Enter' || event.key === ' ')) {
        event.preventDefault();
        if (onClick) {
          onClick(event as any);
        }
      }
      
      if (onKeyDown) {
        onKeyDown(event);
      }
    };
    
    // Handle focus events with contextual help
    const handleFocus = (event: React.FocusEvent<HTMLDivElement>) => {
      if (contextualHelp) {
        a11y.aria.announce(contextualHelp, 'polite');
      }
      
      if (onFocus) {
        onFocus(event);
      }
    };
    
    // Build accessibility attributes
    const accessibilityAttributes = {
      role: clickable ? 'button' : role,
      tabIndex: clickable ? (disabled ? -1 : 0) : tabIndex,
      'aria-disabled': disabled || undefined,
      'aria-busy': loading || undefined,
      ...ariaProps,
    };
    
    // Combine styles
    const variantStyles = getVariantStyles(variant, theme);
    const sizeStyles = getSizeStyles(size);
    const paddingStyles = getPaddingStyles(padding, theme);
    
    const cardStyles: React.CSSProperties = {
      ...variantStyles,
      ...sizeStyles,
      ...paddingStyles,
      width: fullWidth ? '100%' : undefined,
      height: fullHeight ? '100%' : undefined,
      cursor: clickable && !disabled ? 'pointer' : 'default',
      opacity: disabled ? 0.6 : 1,
      pointerEvents: (disabled ? 'none' : 'auto') as React.CSSProperties['pointerEvents'],
      position: 'relative',
      ...style,
    };
    
    // Header content
    const headerContent = header || (title || subtitle || headerActions) ? (
      <div
        className="base-card-header"
        style={{
          display: 'flex',
          alignItems: 'flex-start',
          justifyContent: 'space-between',
          marginBottom: '1rem',
        }}
      >
        <div className="base-card-header-content">
          {title && (
            <h3
              className="base-card-title"
              style={{
                margin: '0 0 0.25rem 0',
                fontSize: '1.125rem',
                fontWeight: '600',
                color: theme?.colors?.text?.primary || '#111827',
              }}
            >
              {title}
            </h3>
          )}
          {subtitle && (
            <p
              className="base-card-subtitle"
              style={{
                margin: 0,
                fontSize: '0.875rem',
                color: theme?.colors?.text?.secondary || '#6b7280',
              }}
            >
              {subtitle}
            </p>
          )}
        </div>
        {headerActions && (
          <div className="base-card-header-actions">
            {headerActions}
          </div>
        )}
      </div>
    ) : null;
    
    // Status indicator
    const statusIndicator = status !== 'default' ? (
      <div
        className="base-card-status"
        style={{
          display: 'flex',
          alignItems: 'center',
          gap: '0.5rem',
          marginBottom: '0.75rem',
          padding: '0.5rem',
          borderRadius: '0.25rem',
          backgroundColor: (() => {
            switch (status) {
              case 'success': return '#f0fdf4';
              case 'warning': return '#fffbeb';
              case 'error': return '#fef2f2';
              case 'info': return '#eff6ff';
              default: return 'transparent';
            }
          })(),
        }}
      >
        <StatusIcon status={status as any} />
        {statusMessage && (
          <span
            style={{
              fontSize: '0.875rem',
              color: (() => {
                switch (status) {
                  case 'success': return '#166534';
                  case 'warning': return '#92400e';
                  case 'error': return '#991b1b';
                  case 'info': return '#1e40af';
                  default: return theme?.colors?.text?.primary || '#111827';
                }
              })(),
            }}
          >
            {statusMessage}
          </span>
        )}
      </div>
    ) : null;
    
    // Progress indicator for executive function support
    const progressContent = progressIndicator ? (
      <div
        className="base-card-progress"
        style={{
          marginBottom: '1rem',
        }}
      >
        {progressIndicator.label && (
          <div
            style={{
              display: 'flex',
              justifyContent: 'space-between',
              alignItems: 'center',
              marginBottom: '0.25rem',
            }}
          >
            <span
              style={{
                fontSize: '0.875rem',
                color: theme?.colors?.text?.secondary || '#6b7280',
              }}
            >
              {progressIndicator.label}
            </span>
            <span
              style={{
                fontSize: '0.875rem',
                color: theme?.colors?.text?.secondary || '#6b7280',
              }}
            >
              {progressIndicator.current}/{progressIndicator.total}
            </span>
          </div>
        )}
        <div
          style={{
            height: '4px',
            backgroundColor: theme?.colors?.surface || '#f3f4f6',
            borderRadius: '2px',
            overflow: 'hidden',
          }}
        >
          <div
            style={{
              height: '100%',
              width: `${(progressIndicator.current / progressIndicator.total) * 100}%`,
              backgroundColor: theme?.colors?.primary || '#3b82f6',
              transition: 'width 0.3s ease-in-out',
            }}
          />
        </div>
      </div>
    ) : null;
    
    // Footer content
    const footerContent = footer || actions ? (
      <div
        className="base-card-footer"
        style={{
          marginTop: 'auto',
          paddingTop: '1rem',
          borderTop: `1px solid ${theme?.colors?.border?.default || '#e5e7eb'}`,
        }}
      >
        {footer || actions}
      </div>
    ) : null;
    
    return (
      <div
        ref={ref}
        id={id}
        className={`base-card base-card--${variant} base-card--${size} ${
          clickable ? 'base-card--clickable' : ''
        } ${disabled ? 'base-card--disabled' : ''} ${loading ? 'base-card--loading' : ''} ${className}`}
        style={cardStyles}
        onClick={handleClick}
        onKeyDown={handleKeyDown}
        onMouseEnter={onMouseEnter}
        onMouseLeave={onMouseLeave}
        onFocus={handleFocus}
        onBlur={onBlur}
        {...accessibilityAttributes}
      >
        {/* Loading overlay */}
        {loading && (
          <div
            className="base-card-loading-overlay"
            style={{
              position: 'absolute',
              inset: 0,
              backgroundColor: 'rgba(255, 255, 255, 0.8)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              borderRadius: 'inherit',
              zIndex: 10,
            }}
          >
            <LoadingSpinner color={theme?.colors?.primary} />
          </div>
        )}
        
        {/* Card content */}
        <div
          className="base-card-content"
          style={{
            display: 'flex',
            flexDirection: 'column',
            height: '100%',
          }}
        >
          {headerContent}
          {statusIndicator}
          {progressContent}
          
          <div
            className="base-card-body"
            style={{
              flex: 1,
            }}
          >
            {children}
          </div>
          
          {footerContent}
        </div>
        
        {/* Add spinner keyframes to document head */}
        <style>
          {`
            @keyframes spin {
              from {
                transform: rotate(0deg);
              }
              to {
                transform: rotate(360deg);
              }
            }
          `}
        </style>
      </div>
    );
  }
);

BaseCard.displayName = 'BaseCard';

// Higher-order component for themed cards
export const withTheme = (theme: Theme) => {
  return forwardRef<HTMLDivElement, Omit<BaseCardProps, 'theme'>>((props, ref) => (
    <BaseCard ref={ref} {...props} theme={theme} />
  ));
};

// Export types for domain-specific extensions (already declared above)
// Types are exported with their declarations above