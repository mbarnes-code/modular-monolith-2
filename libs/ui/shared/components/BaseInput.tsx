/**
 * Base Input Component for Mental Prosthetic Platform
 * 
 * Provides foundation input functionality with accessibility, validation,
 * and executive function accommodations built-in.
 */

import React, { forwardRef, ReactNode, useEffect, useState } from 'react';
import { a11y } from '../foundation/accessibility';
import { Theme } from '../foundation/theme';

// Input variants for different contexts
export type InputVariant = 'default' | 'filled' | 'outline' | 'underline';

// Input sizes
export type InputSize = 'sm' | 'md' | 'lg';

// Input types
export type InputType = 
  | 'text' | 'email' | 'password' | 'tel' | 'url' | 'search'
  | 'number' | 'date' | 'time' | 'datetime-local' 
  | 'month' | 'week' | 'color';

// Validation state
export type ValidationState = 'valid' | 'invalid' | 'warning' | 'pending';

export interface BaseInputProps {
  // Core functionality
  type?: InputType;
  value?: string | number;
  defaultValue?: string | number;
  placeholder?: string;
  
  // Input behavior
  disabled?: boolean;
  readOnly?: boolean;
  required?: boolean;
  autoFocus?: boolean;
  autoComplete?: string;
  
  // Validation
  validationState?: ValidationState;
  errorMessage?: string;
  warningMessage?: string;
  helpText?: string;
  
  // Visual customization
  variant?: InputVariant;
  size?: InputSize;
  fullWidth?: boolean;
  
  // Icons and decorations
  leftIcon?: ReactNode;
  rightIcon?: ReactNode;
  leftAdornment?: ReactNode;
  rightAdornment?: ReactNode;
  
  // Labels and descriptions
  label?: string;
  hideLabel?: boolean; // For accessibility - label still present but visually hidden
  description?: string;
  
  // Event handlers
  onChange?: (value: string, event: React.ChangeEvent<HTMLInputElement>) => void;
  onFocus?: (event: React.FocusEvent<HTMLInputElement>) => void;
  onBlur?: (event: React.FocusEvent<HTMLInputElement>) => void;
  onKeyDown?: (event: React.KeyboardEvent<HTMLInputElement>) => void;
  onKeyUp?: (event: React.KeyboardEvent<HTMLInputElement>) => void;
  
  // Validation handlers
  onValidate?: (value: string) => string | null; // Return error message or null
  validateOnBlur?: boolean;
  validateOnChange?: boolean;
  debounceValidation?: number; // milliseconds
  
  // Executive function support
  showCharacterCount?: boolean;
  maxLength?: number;
  showProgress?: boolean; // For progressive disclosure
  contextHint?: string; // Additional context for memory support
  
  // Accessibility
  'aria-label'?: string;
  'aria-describedby'?: string;
  'aria-invalid'?: boolean;
  'aria-required'?: boolean;
  id?: string;
  name?: string;
  
  // HTML attributes
  min?: number | string;
  max?: number | string;
  step?: number | string;
  pattern?: string;
  
  // CSS customization
  className?: string;
  style?: React.CSSProperties;
  
  // Theme context
  theme?: Theme;
}

// Generate unique IDs for accessibility
let idCounter = 0;
const generateId = () => `input-${++idCounter}`;

// Get variant-specific styles
const getVariantStyles = (variant: InputVariant, validationState: ValidationState, theme?: Theme) => {
  const colors = theme?.colors || {
    primary: '#3b82f6',
    secondary: '#6b7280', 
    background: '#ffffff',
    surface: '#f9fafb',
    text: { primary: '#111827', secondary: '#6b7280', disabled: '#9ca3af' },
    border: { default: '#d1d5db', focus: '#3b82f6', error: '#ef4444' },
    status: { success: '#10b981', error: '#ef4444', warning: '#f59e0b' }
  };
  
  const baseStyles = {
    fontFamily: 'inherit',
    fontSize: 'inherit',
    lineHeight: '1.5',
    transition: 'all 0.15s ease-in-out',
    
    '&:focus': {
      outline: 'none',
    },
    
    '&:disabled': {
      cursor: 'not-allowed',
      opacity: 0.6,
      backgroundColor: colors.surface,
      color: colors.text.disabled,
    },
    
    '&::placeholder': {
      color: colors.text.secondary,
    },
  };
  
  // Validation-specific border colors
  let borderColor = colors.border.default;
  let focusBorderColor = colors.border.focus;
  
  switch (validationState) {
    case 'invalid':
      borderColor = colors.status.error;
      focusBorderColor = colors.status.error;
      break;
    case 'warning':
      borderColor = colors.status.warning;
      focusBorderColor = colors.status.warning;
      break;
    case 'valid':
      borderColor = colors.status.success;
      focusBorderColor = colors.status.success;
      break;
  }
  
  switch (variant) {
    case 'filled':
      return {
        ...baseStyles,
        backgroundColor: colors.surface,
        border: 'none',
        borderRadius: '0.375rem',
        '&:focus': {
          backgroundColor: colors.background,
          boxShadow: `0 0 0 2px ${focusBorderColor}`,
        },
      };
      
    case 'outline':
      return {
        ...baseStyles,
        backgroundColor: 'transparent',
        border: `1px solid ${borderColor}`,
        borderRadius: '0.375rem',
        '&:focus': {
          borderColor: focusBorderColor,
          boxShadow: `0 0 0 1px ${focusBorderColor}`,
        },
      };
      
    case 'underline':
      return {
        ...baseStyles,
        backgroundColor: 'transparent',
        border: 'none',
        borderBottom: `2px solid ${borderColor}`,
        borderRadius: '0',
        '&:focus': {
          borderBottomColor: focusBorderColor,
        },
      };
      
    default: // 'default'
      return {
        ...baseStyles,
        backgroundColor: colors.background,
        border: `1px solid ${borderColor}`,
        borderRadius: '0.25rem',
        '&:focus': {
          borderColor: focusBorderColor,
          boxShadow: `0 0 0 1px ${focusBorderColor}`,
        },
      };
  }
};

// Get size-specific styles
const getSizeStyles = (size: InputSize, theme?: Theme) => {
  const spacing = theme?.spacing || {
    2: '0.5rem',
    3: '0.75rem',
    4: '1rem',
  };
  
  const fontSize = theme?.typography.scale || {
    sm: '0.875rem',
    base: '1rem',
    lg: '1.125rem',
  };
  
  switch (size) {
    case 'sm':
      return {
        padding: `${spacing[2]} ${spacing[3]}`,
        fontSize: fontSize.sm,
        minHeight: '2rem',
      };
    case 'lg':
      return {
        padding: `${spacing[3]} ${spacing[4]}`,
        fontSize: fontSize.lg,
        minHeight: '3rem',
      };
    default: // 'md'
      return {
        padding: `${spacing[2]} ${spacing[4]}`,
        fontSize: fontSize.base,
        minHeight: '2.5rem',
      };
  }
};

// Validation icon component
const ValidationIcon: React.FC<{ state: ValidationState; size: InputSize }> = ({ state, size }) => {
  if (state === 'pending' || state === 'valid') return null;
  
  const iconSize = {
    sm: '14px',
    md: '16px',
    lg: '18px',
  }[size];
  
  const color = state === 'invalid' ? '#ef4444' : '#f59e0b';
  
  return (
    <svg
      width={iconSize}
      height={iconSize}
      viewBox="0 0 24 24"
      fill="none"
      stroke={color}
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      {state === 'invalid' ? (
        <>
          <circle cx="12" cy="12" r="10"/>
          <line x1="15" y1="9" x2="9" y2="15"/>
          <line x1="9" y1="9" x2="15" y2="15"/>
        </>
      ) : (
        <>
          <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/>
          <line x1="12" y1="9" x2="12" y2="13"/>
          <line x1="12" y1="17" x2="12.01" y2="17"/>
        </>
      )}
    </svg>
  );
};

export const BaseInput = forwardRef<HTMLInputElement, BaseInputProps>(
  ({
    type = 'text',
    value,
    defaultValue,
    placeholder,
    disabled = false,
    readOnly = false,
    required = false,
    autoFocus = false,
    validationState = 'valid',
    errorMessage,
    warningMessage,
    helpText,
    variant = 'default',
    size = 'md',
    fullWidth = false,
    leftIcon,
    rightIcon,
    leftAdornment,
    rightAdornment,
    label,
    hideLabel = false,
    description,
    onChange,
    onFocus,
    onBlur,
    onKeyDown,
    onKeyUp,
    onValidate,
    validateOnBlur = true,
    validateOnChange = false,
    debounceValidation = 300,
    showCharacterCount = false,
    maxLength,
    showProgress = false,
    contextHint,
    id: providedId,
    name,
    className = '',
    style = {},
    theme,
    ...htmlProps
  }, ref) => {
    // State management
    const [internalValue, setInternalValue] = useState(defaultValue?.toString() || '');
    const [internalValidationState, setInternalValidationState] = useState<ValidationState>('valid');
    const [internalErrorMessage, setInternalErrorMessage] = useState<string>('');
    const [isFocused, setIsFocused] = useState(false);
    
    // Generate unique ID for accessibility
    const inputId = providedId || generateId();
    const errorId = `${inputId}-error`;
    const helpId = `${inputId}-help`;
    const descId = `${inputId}-desc`;
    
    // Use controlled or uncontrolled value
    const currentValue = value !== undefined ? value.toString() : internalValue;
    const currentValidationState = validationState !== 'valid' ? validationState : internalValidationState;
    const currentErrorMessage = errorMessage || warningMessage || internalErrorMessage;
    
    // Debounced validation
    useEffect(() => {
      if (!validateOnChange || !onValidate) return;
      
      const timeoutId = setTimeout(() => {
        const error = onValidate(currentValue);
        if (error) {
          setInternalValidationState('invalid');
          setInternalErrorMessage(error);
        } else {
          setInternalValidationState('valid');
          setInternalErrorMessage('');
        }
      }, debounceValidation);
      
      return () => clearTimeout(timeoutId);
    }, [currentValue, onValidate, validateOnChange, debounceValidation]);
    
    // Handle value changes
    const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
      const newValue = event.target.value;
      
      if (value === undefined) {
        setInternalValue(newValue);
      }
      
      if (onChange) {
        onChange(newValue, event);
      }
    };
    
    // Handle focus events
    const handleFocus = (event: React.FocusEvent<HTMLInputElement>) => {
      setIsFocused(true);
      
      // Announce context hint for executive function support
      if (contextHint) {
        a11y.aria.announce(contextHint, 'polite');
      }
      
      if (onFocus) {
        onFocus(event);
      }
    };
    
    // Handle blur events with validation
    const handleBlur = (event: React.FocusEvent<HTMLInputElement>) => {
      setIsFocused(false);
      
      // Validate on blur if enabled
      if (validateOnBlur && onValidate) {
        const error = onValidate(currentValue);
        if (error) {
          setInternalValidationState('invalid');
          setInternalErrorMessage(error);
          
          // Announce validation error
          a11y.aria.announceError(label || 'Field', error);
        } else {
          setInternalValidationState('valid');
          setInternalErrorMessage('');
        }
      }
      
      if (onBlur) {
        onBlur(event);
      }
    };
    
    // Character count calculation
    const characterCount = currentValue.length;
    const characterProgress = maxLength ? (characterCount / maxLength) * 100 : 0;
    const isNearLimit = maxLength && characterCount > maxLength * 0.8;
    const isOverLimit = maxLength && characterCount > maxLength;
    
    // Build accessibility attributes
    const ariaDescribedBy = [
      description && descId,
      helpText && helpId,
      currentErrorMessage && errorId,
    ].filter(Boolean).join(' ');
    
    const ariaAttributes = a11y.aria.buildAttributes({
      required,
      invalid: currentValidationState === 'invalid',
      describedBy: ariaDescribedBy || undefined,
    });
    
    // Combine styles
    const variantStyles = getVariantStyles(variant, currentValidationState, theme);
    const sizeStyles = getSizeStyles(size, theme);
    
    const inputStyles = {
      ...variantStyles,
      ...sizeStyles,
      width: fullWidth ? '100%' : 'auto',
      paddingLeft: leftIcon || leftAdornment ? '2.5rem' : undefined,
      paddingRight: rightIcon || rightAdornment || currentValidationState !== 'valid' ? '2.5rem' : undefined,
      ...style,
    };
    
    return (
      <div className={`base-input-container ${className}`}>
        {/* Label */}
        {label && (
          <label
            htmlFor={inputId}
            className={`base-input-label ${hideLabel ? 'sr-only' : ''}`}
            style={{
              display: 'block',
              marginBottom: '0.25rem',
              fontSize: '0.875rem',
              fontWeight: '500',
              color: theme?.colors?.text?.primary || '#111827',
            }}
          >
            {label}
            {required && (
              <span style={{ color: theme?.colors?.status?.error || '#ef4444', marginLeft: '0.25rem' }}>
                *
              </span>
            )}
          </label>
        )}
        
        {/* Description */}
        {description && (
          <div
            id={descId}
            className="base-input-description"
            style={{
              marginBottom: '0.5rem',
              fontSize: '0.875rem',
              color: theme?.colors?.text?.secondary || '#6b7280',
            }}
          >
            {description}
          </div>
        )}
        
        {/* Input container with icons/adornments */}
        <div
          className="base-input-wrapper"
          style={{
            position: 'relative',
            display: 'flex',
            alignItems: 'center',
          }}
        >
          {/* Left icon/adornment */}
          {(leftIcon || leftAdornment) && (
            <div
              className="base-input-left-element"
              style={{
                position: 'absolute',
                left: '0.75rem',
                zIndex: 1,
                pointerEvents: leftAdornment ? 'auto' : 'none',
              }}
            >
              {leftIcon || leftAdornment}
            </div>
          )}
          
          {/* Input element */}
          <input
            ref={ref}
            id={inputId}
            name={name}
            type={type}
            value={currentValue}
            placeholder={placeholder}
            disabled={disabled}
            readOnly={readOnly}
            maxLength={maxLength}
            autoFocus={autoFocus}
            className={`base-input base-input--${variant} base-input--${size}`}
            style={inputStyles}
            onChange={handleChange}
            onFocus={handleFocus}
            onBlur={handleBlur}
            onKeyDown={onKeyDown}
            onKeyUp={onKeyUp}
            {...ariaAttributes}
            {...htmlProps}
          />
          
          {/* Right icon/adornment */}
          {(rightIcon || rightAdornment || currentValidationState !== 'valid') && (
            <div
              className="base-input-right-element"
              style={{
                position: 'absolute',
                right: '0.75rem',
                zIndex: 1,
                display: 'flex',
                alignItems: 'center',
                gap: '0.25rem',
                pointerEvents: rightAdornment ? 'auto' : 'none',
              }}
            >
              {rightIcon || rightAdornment}
              {currentValidationState !== 'valid' && (
                <ValidationIcon state={currentValidationState} size={size} />
              )}
            </div>
          )}
        </div>
        
        {/* Character count */}
        {showCharacterCount && maxLength && (
          <div
            className="base-input-character-count"
            style={{
              marginTop: '0.25rem',
              fontSize: '0.75rem',
              textAlign: 'right',
              color: isOverLimit
                ? theme?.colors?.status?.error || '#ef4444'
                : isNearLimit
                ? theme?.colors?.status?.warning || '#f59e0b'
                : theme?.colors?.text?.secondary || '#6b7280',
            }}
          >
            {characterCount}/{maxLength}
          </div>
        )}
        
        {/* Progress indicator for long inputs */}
        {showProgress && maxLength && (
          <div
            className="base-input-progress"
            style={{
              marginTop: '0.25rem',
              height: '2px',
              backgroundColor: theme?.colors?.surface || '#f3f4f6',
              borderRadius: '1px',
              overflow: 'hidden',
            }}
          >
            <div
              style={{
                height: '100%',
                width: `${Math.min(characterProgress, 100)}%`,
                backgroundColor: isOverLimit
                  ? theme?.colors?.status?.error || '#ef4444'
                  : theme?.colors?.primary || '#3b82f6',
                transition: 'width 0.2s ease-in-out',
              }}
            />
          </div>
        )}
        
        {/* Help text */}
        {helpText && !currentErrorMessage && (
          <div
            id={helpId}
            className="base-input-help"
            style={{
              marginTop: '0.25rem',
              fontSize: '0.875rem',
              color: theme?.colors?.text?.secondary || '#6b7280',
            }}
          >
            {helpText}
          </div>
        )}
        
        {/* Error/Warning message */}
        {currentErrorMessage && (
          <div
            id={errorId}
            className={`base-input-message base-input-message--${currentValidationState}`}
            role={currentValidationState === 'invalid' ? 'alert' : 'status'}
            style={{
              marginTop: '0.25rem',
              fontSize: '0.875rem',
              color: currentValidationState === 'invalid'
                ? theme?.colors?.status?.error || '#ef4444'
                : theme?.colors?.status?.warning || '#f59e0b',
            }}
          >
            {currentErrorMessage}
          </div>
        )}
      </div>
    );
  }
);

BaseInput.displayName = 'BaseInput';

// Higher-order component for themed inputs
export const withTheme = (theme: Theme) => {
  return forwardRef<HTMLInputElement, Omit<BaseInputProps, 'theme'>>((props, ref) => (
    <BaseInput ref={ref} {...props} theme={theme} />
  ));
};

// Export types for domain-specific extensions
export type { BaseInputProps, InputSize, InputType, InputVariant, ValidationState };
