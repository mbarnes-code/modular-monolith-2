/**
 * Accessible Button Component with Executive Function Support
 * 
 * Enhanced button with ADHD/autism accommodations:
 * - Clear visual feedback (<75ms response)
 * - Consistent styling patterns
 * - High contrast options
 * - Focus management
 */

import React, { ButtonHTMLAttributes, forwardRef } from 'react';
import { useCognitiveLoad, useExecutiveFunction } from '../executive-function';

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'danger' | 'ghost';
  size?: 'sm' | 'md' | 'lg';
  loading?: boolean;
  highContrast?: boolean;
  cognitive?: 'low' | 'medium' | 'high';
}

export const Button = forwardRef<HTMLButtonElement, ButtonProps>(({
  children,
  variant = 'primary',
  size = 'md',
  loading = false,
  highContrast,
  cognitive = 'medium',
  className = '',
  disabled,
  ...props
}, ref) => {
  const { state } = useExecutiveFunction();
  const { cognitiveLoad, updateCognitiveLoad } = useCognitiveLoad();
  
  // Use high contrast if user preference or explicit prop
  const useHighContrast = highContrast ?? state.autismOptions.sensory_preferences?.high_contrast ?? false;
  
  const handleClick = (e: React.MouseEvent<HTMLButtonElement>) => {
    // Track cognitive load
    const loadIncrease = cognitive === 'low' ? 1 : cognitive === 'medium' ? 2 : 3;
    updateCognitiveLoad({
      current_load: Math.min(100, cognitiveLoad.current_load + loadIncrease)
    });
    
    // Provide immediate visual feedback
    const button = e.currentTarget;
    button.style.transform = 'scale(0.98)';
    setTimeout(() => {
      button.style.transform = '';
    }, 100);
    
    props.onClick?.(e);
  };

  const baseClasses = [
    'inline-flex items-center justify-center',
    'font-medium rounded-md transition-all duration-75',
    'focus:outline-none focus:ring-2 focus:ring-offset-2',
    'disabled:opacity-50 disabled:cursor-not-allowed',
    'select-none'
  ];

  const variantClasses = {
    primary: useHighContrast 
      ? 'bg-black text-white hover:bg-gray-800 focus:ring-black'
      : 'bg-blue-600 text-white hover:bg-blue-700 focus:ring-blue-500',
    secondary: useHighContrast
      ? 'bg-white text-black border-2 border-black hover:bg-gray-100'
      : 'bg-gray-200 text-gray-900 hover:bg-gray-300 focus:ring-gray-500',
    danger: useHighContrast
      ? 'bg-black text-white border-2 border-red-600 hover:bg-red-800'
      : 'bg-red-600 text-white hover:bg-red-700 focus:ring-red-500',
    ghost: useHighContrast
      ? 'text-black hover:bg-gray-200 border border-gray-400'
      : 'text-gray-700 hover:bg-gray-100 focus:ring-gray-500'
  };

  const sizeClasses = {
    sm: 'px-3 py-1.5 text-sm',
    md: 'px-4 py-2 text-base',
    lg: 'px-6 py-3 text-lg'
  };

  const classes = [
    ...baseClasses,
    variantClasses[variant],
    sizeClasses[size],
    className
  ].join(' ');

  return (
    <button
      ref={ref}
      className={classes}
      disabled={disabled || loading}
      onClick={handleClick}
      {...props}
    >
      {loading && (
        <svg 
          className="animate-spin -ml-1 mr-2 h-4 w-4" 
          fill="none" 
          viewBox="0 0 24 24"
        >
          <circle 
            className="opacity-25" 
            cx="12" 
            cy="12" 
            r="10" 
            stroke="currentColor" 
            strokeWidth="4"
          />
          <path 
            className="opacity-75" 
            fill="currentColor" 
            d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
          />
        </svg>
      )}
      {children}
    </button>
  );
});

Button.displayName = 'Button';