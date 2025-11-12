/**
 * Base Modal Component for Mental Prosthetic Platform
 * 
 * Provides foundation modal/dialog functionality with accessibility,
 * focus management, and executive function accommodations built-in.
 */

import React, {
    forwardRef,
    KeyboardEvent,
    MouseEvent,
    ReactNode,
    useCallback,
    useEffect,
    useState,
} from 'react';
import { createPortal } from 'react-dom';
import { a11y } from '../foundation/accessibility';
import { Theme } from '../foundation/theme';

// Modal sizes
export type ModalSize = 'xs' | 'sm' | 'md' | 'lg' | 'xl' | 'fullscreen';

// Modal positions
export type ModalPosition = 'center' | 'top' | 'bottom';

// Animation states
export type ModalAnimationState = 'entering' | 'entered' | 'exiting' | 'exited';

export interface BaseModalProps {
  // Core functionality
  open: boolean;
  onClose: () => void;
  
  // Content
  children?: ReactNode;
  title?: string;
  description?: string;
  
  // Layout
  size?: ModalSize;
  position?: ModalPosition;
  fullWidth?: boolean;
  scrollable?: boolean;
  
  // Behavior
  closeOnEscape?: boolean;
  closeOnOverlayClick?: boolean;
  disableScrollLock?: boolean;
  hideCloseButton?: boolean;
  
  // Animation
  animationDuration?: number; // milliseconds
  
  // Executive function support
  showProgress?: boolean;
  progressSteps?: {
    current: number;
    total: number;
    steps: string[];
  };
  contextualHelp?: string;
  autoFocusElement?: string; // selector for element to focus
  
  // Actions
  primaryAction?: {
    label: string;
    onClick: () => void;
    disabled?: boolean;
    loading?: boolean;
    variant?: 'primary' | 'secondary' | 'danger';
  };
  secondaryAction?: {
    label: string;
    onClick: () => void;
    disabled?: boolean;
  };
  customActions?: ReactNode;
  
  // Header customization
  headerContent?: ReactNode;
  showHeader?: boolean;
  
  // Footer customization
  footerContent?: ReactNode;
  showFooter?: boolean;
  
  // Accessibility
  'aria-label'?: string;
  'aria-labelledby'?: string;
  'aria-describedby'?: string;
  role?: string;
  
  // CSS customization
  className?: string;
  overlayClassName?: string;
  contentClassName?: string;
  style?: React.CSSProperties;
  overlayStyle?: React.CSSProperties;
  contentStyle?: React.CSSProperties;
  
  // Theme context
  theme?: Theme;
  
  // Portal target
  portalTarget?: Element | string;
}

// Focus trap hook
const useFocusTrap = (isActive: boolean, containerRef: React.RefObject<HTMLElement | null>) => {
  useEffect(() => {
    if (!isActive || !containerRef.current) return;
    
    const container = containerRef.current;
    const focusableElements = container.querySelectorAll(
      'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
    );
    
    const firstFocusable = focusableElements[0] as HTMLElement;
    const lastFocusable = focusableElements[focusableElements.length - 1] as HTMLElement;
    
    const handleTabKey = (e: Event) => {
      const keyEvent = e as globalThis.KeyboardEvent;
      if (keyEvent.key !== 'Tab') return;
      
      if (keyEvent.shiftKey) {
        if (document.activeElement === firstFocusable) {
          lastFocusable?.focus();
          keyEvent.preventDefault();
        }
      } else {
        if (document.activeElement === lastFocusable) {
          firstFocusable?.focus();
          keyEvent.preventDefault();
        }
      }
    };
    
    container.addEventListener('keydown', handleTabKey);
    
    // Focus first element
    firstFocusable?.focus();
    
    return () => {
      container.removeEventListener('keydown', handleTabKey);
    };
  }, [isActive, containerRef]);
};

// Scroll lock hook
const useScrollLock = (isActive: boolean) => {
  useEffect(() => {
    if (!isActive) return;
    
    const originalOverflow = document.body.style.overflow;
    const originalPaddingRight = document.body.style.paddingRight;
    
    // Calculate scrollbar width
    const scrollbarWidth = window.innerWidth - document.documentElement.clientWidth;
    
    document.body.style.overflow = 'hidden';
    document.body.style.paddingRight = `${scrollbarWidth}px`;
    
    return () => {
      document.body.style.overflow = originalOverflow;
      document.body.style.paddingRight = originalPaddingRight;
    };
  }, [isActive]);
};

// Close icon component
const CloseIcon: React.FC<{ size?: number; color?: string }> = ({ 
  size = 24, 
  color = '#6b7280' 
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
  >
    <line x1="18" y1="6" x2="6" y2="18"/>
    <line x1="6" y1="6" x2="18" y2="18"/>
  </svg>
);

// Action button component
const ActionButton: React.FC<{
  action: NonNullable<BaseModalProps['primaryAction']>;
  variant?: 'primary' | 'secondary' | 'danger';
  theme?: Theme;
}> = ({ action, variant = 'primary', theme }) => {
  const getButtonStyles = () => {
    const colors = theme?.colors || {
      primary: '#3b82f6',
      secondary: '#6b7280',
      background: '#ffffff',
      text: { primary: '#111827' },
      status: { error: '#ef4444' }
    };
    
    const baseStyles: React.CSSProperties = {
      padding: '0.5rem 1rem',
      borderRadius: '0.375rem',
      border: 'none',
      fontSize: '0.875rem',
      fontWeight: '500',
      cursor: action.disabled ? 'not-allowed' : 'pointer',
      opacity: action.disabled ? 0.6 : 1,
      transition: 'all 0.15s ease-in-out',
    };
    
    switch (variant) {
      case 'primary':
        return {
          ...baseStyles,
          backgroundColor: colors.primary,
          color: colors.background,
        };
      case 'danger':
        return {
          ...baseStyles,
          backgroundColor: colors.status?.error,
          color: colors.background,
        };
      default: // secondary
        return {
          ...baseStyles,
          backgroundColor: 'transparent',
          color: colors.text?.primary,
          border: `1px solid ${colors.secondary}`,
        };
    }
  };
  
  return (
    <button
      style={getButtonStyles()}
      onClick={action.onClick}
      disabled={action.disabled || action.loading}
    >
      {action.loading ? 'Loading...' : action.label}
    </button>
  );
};

// Get size-specific styles
const getSizeStyles = (size: ModalSize): React.CSSProperties => {
  switch (size) {
    case 'xs':
      return { maxWidth: '20rem', width: '100%' };
    case 'sm':
      return { maxWidth: '24rem', width: '100%' };
    case 'lg':
      return { maxWidth: '48rem', width: '100%' };
    case 'xl':
      return { maxWidth: '64rem', width: '100%' };
    case 'fullscreen':
      return { width: '100vw', height: '100vh', maxWidth: 'none', borderRadius: 0 };
    default: // 'md'
      return { maxWidth: '32rem', width: '100%' };
  }
};

// Get position-specific styles
const getPositionStyles = (position: ModalPosition): React.CSSProperties => {
  switch (position) {
    case 'top':
      return {
        alignItems: 'flex-start',
        paddingTop: '4rem',
      };
    case 'bottom':
      return {
        alignItems: 'flex-end',
        paddingBottom: '4rem',
      };
    default: // 'center'
      return {
        alignItems: 'center',
      };
  }
};

export const BaseModal = forwardRef<HTMLDivElement, BaseModalProps>(
  ({
    open,
    onClose,
    children,
    title,
    description,
    size = 'md',
    position = 'center',
    fullWidth = false,
    scrollable = true,
    closeOnEscape = true,
    closeOnOverlayClick = true,
    disableScrollLock = false,
    hideCloseButton = false,
    animationDuration = 200,
    showProgress = false,
    progressSteps,
    contextualHelp,
    autoFocusElement,
    primaryAction,
    secondaryAction,
    customActions,
    headerContent,
    showHeader = true,
    footerContent,
    showFooter = true,
    role = 'dialog',
    className = '',
    overlayClassName = '',
    contentClassName = '',
    style = {},
    overlayStyle = {},
    contentStyle = {},
    theme,
    portalTarget = document.body,
    ...ariaProps
  }, ref) => {
    
    const [animationState, setAnimationState] = useState<ModalAnimationState>('exited');
    const modalRef = React.useRef<HTMLDivElement>(null);
    
    // Combine refs
    const combinedRef = React.useCallback((node: HTMLDivElement) => {
      if (modalRef.current) modalRef.current = node;
      if (typeof ref === 'function') ref(node);
      else if (ref) ref.current = node;
    }, [ref]);
    
    // Focus management
    useFocusTrap(open && animationState === 'entered', modalRef);
    
    // Scroll lock
    useScrollLock(open && !disableScrollLock);
    
    // Animation management
    useEffect(() => {
      if (open) {
        setAnimationState('entering');
        const timer = setTimeout(() => setAnimationState('entered'), 50);
        return () => clearTimeout(timer);
      } else if (animationState !== 'exited') {
        setAnimationState('exiting');
        const timer = setTimeout(() => setAnimationState('exited'), animationDuration);
        return () => clearTimeout(timer);
      }
    }, [open, animationDuration, animationState]);
    
    // Keyboard event handling
    const handleKeyDown = useCallback((event: KeyboardEvent<HTMLDivElement>) => {
      if (event.key === 'Escape' && closeOnEscape) {
        onClose();
      }
    }, [closeOnEscape, onClose]);
    
    // Overlay click handling
    const handleOverlayClick = useCallback((event: MouseEvent<HTMLDivElement>) => {
      if (event.target === event.currentTarget && closeOnOverlayClick) {
        onClose();
      }
    }, [closeOnOverlayClick, onClose]);
    
    // Auto focus management
    useEffect(() => {
      if (open && animationState === 'entered' && autoFocusElement && modalRef.current) {
        const element = modalRef.current.querySelector(autoFocusElement) as HTMLElement;
        element?.focus();
      }
    }, [open, animationState, autoFocusElement]);
    
    // Announce contextual help for executive function support
    useEffect(() => {
      if (open && contextualHelp) {
        a11y.aria.announce(contextualHelp, 'polite');
      }
    }, [open, contextualHelp]);
    
    // Don't render if not open and animation is complete
    if (!open && animationState === 'exited') {
      return null;
    }
    
    // Get portal target
    const portalElement = typeof portalTarget === 'string' 
      ? document.querySelector(portalTarget) 
      : portalTarget;
    
    if (!portalElement) {
      console.warn('Modal portal target not found, using document.body');
    }
    
    // Calculate animation styles
    const isVisible = animationState === 'entered' || animationState === 'entering';
    const overlayOpacity = isVisible ? 1 : 0;
    const contentScale = isVisible ? 1 : 0.95;
    const contentOpacity = isVisible ? 1 : 0;
    
    // Combine styles
    const positionStyles = getPositionStyles(position);
    const sizeStyles = getSizeStyles(size);
    
    const overlayStyles: React.CSSProperties = {
      position: 'fixed',
      inset: 0,
      backgroundColor: 'rgba(0, 0, 0, 0.5)',
      display: 'flex',
      justifyContent: 'center',
      padding: '1rem',
      zIndex: 9999,
      opacity: overlayOpacity,
      transition: `opacity ${animationDuration}ms ease-in-out`,
      ...positionStyles,
      ...overlayStyle,
    };
    
    const contentStyles: React.CSSProperties = {
      backgroundColor: theme?.colors?.background || '#ffffff',
      borderRadius: '0.5rem',
      boxShadow: '0 20px 25px -5px rgb(0 0 0 / 0.1), 0 8px 10px -6px rgb(0 0 0 / 0.1)',
      maxHeight: scrollable ? '90vh' : undefined,
      overflow: scrollable ? 'auto' : 'visible',
      position: 'relative',
      transform: `scale(${contentScale})`,
      opacity: contentOpacity,
      transition: `all ${animationDuration}ms ease-in-out`,
      width: fullWidth ? '100%' : undefined,
      ...sizeStyles,
      ...contentStyle,
      ...style,
    };
    
    // Progress indicator
    const progressContent = showProgress && progressSteps ? (
      <div
        className="modal-progress"
        style={{
          padding: '1rem 1.5rem',
          borderBottom: `1px solid ${theme?.colors?.border?.default || '#e5e7eb'}`,
        }}
      >
        <div
          style={{
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
            marginBottom: '0.5rem',
          }}
        >
          <span
            style={{
              fontSize: '0.875rem',
              color: theme?.colors?.text?.secondary || '#6b7280',
            }}
          >
            Step {progressSteps.current} of {progressSteps.total}
          </span>
          <span
            style={{
              fontSize: '0.875rem',
              color: theme?.colors?.text?.secondary || '#6b7280',
            }}
          >
            {Math.round((progressSteps.current / progressSteps.total) * 100)}%
          </span>
        </div>
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
              width: `${(progressSteps.current / progressSteps.total) * 100}%`,
              backgroundColor: theme?.colors?.primary || '#3b82f6',
              transition: 'width 0.3s ease-in-out',
            }}
          />
        </div>
        {progressSteps.steps[progressSteps.current - 1] && (
          <div
            style={{
              marginTop: '0.5rem',
              fontSize: '0.875rem',
              color: theme?.colors?.text?.primary || '#111827',
            }}
          >
            {progressSteps.steps[progressSteps.current - 1]}
          </div>
        )}
      </div>
    ) : null;
    
    // Header content
    const headerElements = showHeader && (title || description || headerContent || !hideCloseButton) ? (
      <div
        className="modal-header"
        style={{
          padding: '1.5rem 1.5rem 1rem 1.5rem',
          borderBottom: progressContent ? 'none' : `1px solid ${theme?.colors?.border?.default || '#e5e7eb'}`,
        }}
      >
        <div
          style={{
            display: 'flex',
            alignItems: 'flex-start',
            justifyContent: 'space-between',
          }}
        >
          <div style={{ flex: 1, minWidth: 0 }}>
            {title && (
              <h2
                className="modal-title"
                style={{
                  margin: '0 0 0.5rem 0',
                  fontSize: '1.25rem',
                  fontWeight: '600',
                  color: theme?.colors?.text?.primary || '#111827',
                }}
              >
                {title}
              </h2>
            )}
            {description && (
              <p
                className="modal-description"
                style={{
                  margin: 0,
                  fontSize: '0.875rem',
                  color: theme?.colors?.text?.secondary || '#6b7280',
                }}
              >
                {description}
              </p>
            )}
            {headerContent}
          </div>
          
          {!hideCloseButton && (
            <button
              className="modal-close-button"
              onClick={onClose}
              style={{
                marginLeft: '1rem',
                padding: '0.5rem',
                backgroundColor: 'transparent',
                border: 'none',
                borderRadius: '0.25rem',
                cursor: 'pointer',
                transition: 'background-color 0.15s ease-in-out',
              }}
              aria-label="Close modal"
            >
              <CloseIcon color={theme?.colors?.text?.secondary} />
            </button>
          )}
        </div>
      </div>
    ) : null;
    
    // Footer content
    const footerElements = showFooter && (primaryAction || secondaryAction || customActions || footerContent) ? (
      <div
        className="modal-footer"
        style={{
          padding: '1rem 1.5rem 1.5rem 1.5rem',
          borderTop: `1px solid ${theme?.colors?.border?.default || '#e5e7eb'}`,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'flex-end',
          gap: '0.75rem',
        }}
      >
        {footerContent || (
          <>
            {secondaryAction && (
              <ActionButton action={secondaryAction} variant="secondary" theme={theme} />
            )}
            {primaryAction && (
              <ActionButton 
                action={primaryAction} 
                variant={primaryAction.variant || 'primary'} 
                theme={theme} 
              />
            )}
            {customActions}
          </>
        )}
      </div>
    ) : null;
    
    const modalContent = (
      <div
        className={`base-modal-overlay ${overlayClassName}`}
        style={overlayStyles}
        onClick={handleOverlayClick}
        onKeyDown={handleKeyDown}
      >
        <div
          ref={combinedRef}
          className={`base-modal-content ${contentClassName} ${className}`}
          style={contentStyles}
          role={role}
          aria-modal="true"
          {...ariaProps}
        >
          {progressContent}
          {headerElements}
          
          <div
            className="modal-body"
            style={{
              padding: headerElements || footerElements ? '1.5rem' : '2rem',
              flex: 1,
            }}
          >
            {children}
          </div>
          
          {footerElements}
        </div>
      </div>
    );
    
    return createPortal(modalContent, portalElement || document.body);
  }
);

BaseModal.displayName = 'BaseModal';

// Higher-order component for themed modals
export const withTheme = (theme: Theme) => {
  return forwardRef<HTMLDivElement, Omit<BaseModalProps, 'theme'>>((props, ref) => (
    <BaseModal ref={ref} {...props} theme={theme} />
  ));
};

// Export types for domain-specific extensions
// Types are exported with their declarations above