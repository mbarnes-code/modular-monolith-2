/**
 * Accessible Input Component with Executive Function Support
 * 
 * Enhanced input with ADHD/autism accommodations:
 * - Clear focus indicators
 * - Real-time validation feedback
 * - Reduced cognitive load
 * - Consistent styling
 */

import React, { forwardRef, InputHTMLAttributes, useState } from 'react';
import { useExecutiveFunction } from '../executive-function';

interface InputProps extends InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
  helpText?: string;
  highContrast?: boolean;
  clearOnEscape?: boolean;
  validationDelay?: number;
}

export const Input = forwardRef<HTMLInputElement, InputProps>(({
  label,
  error,
  helpText,
  highContrast,
  clearOnEscape = true,
  validationDelay = 300,
  className = '',
  onChange,
  onKeyDown,
  ...props
}, ref) => {
  const { state } = useExecutiveFunction();
  const [isFocused, setIsFocused] = useState(false);
  
  // Use high contrast if user preference or explicit prop
  const useHighContrast = highContrast ?? state.autismOptions.sensory_preferences?.high_contrast ?? false;
  
  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (clearOnEscape && e.key === 'Escape') {
      const input = e.currentTarget;
      input.value = '';
      input.blur();
    }
    onKeyDown?.(e);
  };

  const baseClasses = [
    'block w-full rounded-md transition-all duration-100',
    'focus:outline-none focus:ring-2 focus:ring-offset-1',
    'disabled:opacity-50 disabled:cursor-not-allowed'
  ];

  const inputClasses = useHighContrast
    ? [
        'border-2 border-black bg-white text-black',
        'focus:border-black focus:ring-black',
        error ? 'border-red-600 focus:border-red-600 focus:ring-red-600' : ''
      ]
    : [
        'border border-gray-300 bg-white text-gray-900',
        'focus:border-blue-500 focus:ring-blue-500',
        error ? 'border-red-300 focus:border-red-500 focus:ring-red-500' : ''
      ];

  const labelClasses = useHighContrast
    ? 'block text-sm font-bold text-black mb-1'
    : 'block text-sm font-medium text-gray-700 mb-1';

  const errorClasses = useHighContrast
    ? 'text-sm font-bold text-red-800 mt-1'
    : 'text-sm text-red-600 mt-1';

  const helpClasses = useHighContrast
    ? 'text-sm text-gray-800 mt-1'
    : 'text-sm text-gray-500 mt-1';

  const combinedClasses = [
    ...baseClasses,
    ...inputClasses,
    'px-3 py-2',
    isFocused && state.settings.focus_assist_enabled 
      ? 'ring-2 ring-offset-2 ring-blue-400' 
      : '',
    className
  ].filter(Boolean).join(' ');

  const inputId = props.id || `input-${Math.random().toString(36).substr(2, 9)}`;

  return (
    <div className="w-full">
      {label && (
        <label htmlFor={inputId} className={labelClasses}>
          {label}
        </label>
      )}
      
      <input
        ref={ref}
        id={inputId}
        className={combinedClasses}
        onChange={onChange}
        onKeyDown={handleKeyDown}
        onFocus={(e) => {
          setIsFocused(true);
          props.onFocus?.(e);
        }}
        onBlur={(e) => {
          setIsFocused(false);
          props.onBlur?.(e);
        }}
        aria-invalid={error ? 'true' : 'false'}
        aria-describedby={
          [
            error ? `${inputId}-error` : '',
            helpText ? `${inputId}-help` : ''
          ].filter(Boolean).join(' ') || undefined
        }
        {...props}
      />
      
      {error && (
        <p id={`${inputId}-error`} className={errorClasses} role="alert">
          {error}
        </p>
      )}
      
      {helpText && !error && (
        <p id={`${inputId}-help`} className={helpClasses}>
          {helpText}
        </p>
      )}
    </div>
  );
});

Input.displayName = 'Input';