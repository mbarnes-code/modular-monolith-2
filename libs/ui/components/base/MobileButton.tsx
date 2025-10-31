/**
 * Mobile-Optimized Button Component with Executive Function Support
 * 
 * Enhanced button for mobile devices with ADHD/autism accommodations:
 * - Touch-friendly sizes (minimum 44px iOS guidelines)
 * - Haptic feedback support
 * - Voice guidance integration
 * - Enhanced visual feedback for touch
 * - Gesture recognition
 */

import React, { ButtonHTMLAttributes, forwardRef, useCallback, useState } from 'react';
import { useCognitiveLoad, useExecutiveFunction } from '../executive-function';

interface MobileButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'danger' | 'ghost';
  size?: 'sm' | 'md' | 'lg' | 'xl';
  loading?: boolean;
  highContrast?: boolean;
  cognitive?: 'low' | 'medium' | 'high';
  /** Mobile-specific props */
  mobileOptions?: {
    /** Enable haptic feedback */
    hapticFeedback?: boolean;
    /** Enable voice guidance */
    voiceGuidance?: boolean;
    /** Minimum touch target size */
    minTouchSize?: number;
    /** Enhanced press feedback */
    enhancedFeedback?: boolean;
    /** Long press handler */
    onLongPress?: () => void;
    /** Long press duration in ms */
    longPressDuration?: number;
  };
}

export const MobileButton = forwardRef<HTMLButtonElement, MobileButtonProps>(({
  children,
  variant = 'primary',
  size = 'md',
  loading = false,
  highContrast,
  cognitive = 'medium',
  className = '',
  disabled,
  mobileOptions = {},
  ...props
}, ref) => {
  const { state } = useExecutiveFunction();
  const { cognitiveLoad, updateCognitiveLoad } = useCognitiveLoad();
  const [isPressed, setIsPressed] = useState(false);
  const [longPressTimer, setLongPressTimer] = useState<NodeJS.Timeout | null>(null);

  const {
    hapticFeedback = true,
    voiceGuidance = false,
    minTouchSize = 44, // iOS accessibility guideline
    enhancedFeedback = true,
    onLongPress,
    longPressDuration = 500
  } = mobileOptions;
  
  // Use high contrast if user preference or explicit prop
  const useHighContrast = highContrast ?? state.autismOptions.sensory_preferences?.high_contrast ?? false;
  
  // Check if device is mobile
  const isMobile = typeof window !== 'undefined' && (
    window.innerWidth < 768 || 'ontouchstart' in window
  );

  // Haptic feedback helper
  const triggerHapticFeedback = useCallback((type: 'light' | 'medium' | 'heavy' = 'light') => {
    if (!hapticFeedback || !isMobile) return;

    if ('vibrate' in navigator) {
      const patterns = {
        light: [10],
        medium: [20],
        heavy: [30]
      };
      navigator.vibrate(patterns[type]);
    }
  }, [hapticFeedback, isMobile]);

  // Voice guidance helper
  const announceAction = useCallback((action: string) => {
    if (!voiceGuidance || !isMobile) return;

    const buttonText = typeof children === 'string' ? children : 'Button';
    const announcement = `${action} ${buttonText}`;

    if ('speechSynthesis' in window) {
      const utterance = new SpeechSynthesisUtterance(announcement);
      utterance.volume = 0.3;
      utterance.rate = 1.5;
      speechSynthesis.speak(utterance);
    }
  }, [voiceGuidance, isMobile, children]);

  const handleTouchStart = useCallback((e: React.TouchEvent<HTMLButtonElement>) => {
    if (disabled || loading) return;

    setIsPressed(true);
    triggerHapticFeedback('light');
    
    if (onLongPress) {
      const timer = setTimeout(() => {
        triggerHapticFeedback('medium');
        onLongPress();
        announceAction('Long pressed');
      }, longPressDuration);
      setLongPressTimer(timer);
    }

    props.onTouchStart?.(e);
  }, [disabled, loading, triggerHapticFeedback, onLongPress, longPressDuration, announceAction, props]);

  const handleTouchEnd = useCallback((e: React.TouchEvent<HTMLButtonElement>) => {
    setIsPressed(false);
    
    if (longPressTimer) {
      clearTimeout(longPressTimer);
      setLongPressTimer(null);
    }

    props.onTouchEnd?.(e);
  }, [longPressTimer, props]);

  const handleClick = (e: React.MouseEvent<HTMLButtonElement>) => {
    if (disabled || loading) return;

    // Track cognitive load
    const loadIncrease = cognitive === 'low' ? 1 : cognitive === 'medium' ? 2 : 3;
    updateCognitiveLoad({
      current_load: Math.min(100, cognitiveLoad.current_load + loadIncrease)
    });
    
    // Mobile-specific feedback
    if (isMobile) {
      triggerHapticFeedback('medium');
      announceAction('Pressed');
    }
    
    // Enhanced visual feedback for mobile
    if (enhancedFeedback) {
      const button = e.currentTarget;
      const originalTransform = button.style.transform;
      button.style.transform = 'scale(0.95)';
      
      setTimeout(() => {
        button.style.transform = originalTransform;
      }, 150);
    }
    
    props.onClick?.(e);
  };

  const baseClasses = [
    'inline-flex items-center justify-center',
    'font-medium rounded-lg transition-all duration-150',
    'focus:outline-none focus:ring-4 focus:ring-offset-2',
    'disabled:opacity-50 disabled:cursor-not-allowed',
    'select-none',
    'active:scale-95', // Enhanced press feedback
    // Mobile-specific classes
    isMobile && 'touch-manipulation', // Optimize for touch
    isPressed && enhancedFeedback && 'scale-95 shadow-inner',
  ].filter(Boolean);

  const variantClasses = {
    primary: useHighContrast 
      ? 'bg-black text-white hover:bg-gray-800 focus:ring-black active:bg-gray-900'
      : 'bg-blue-600 text-white hover:bg-blue-700 focus:ring-blue-300 active:bg-blue-800',
    secondary: useHighContrast
      ? 'bg-white text-black border-2 border-black hover:bg-gray-100 focus:ring-gray-300'
      : 'bg-gray-200 text-gray-900 hover:bg-gray-300 focus:ring-gray-300 active:bg-gray-400',
    danger: useHighContrast
      ? 'bg-black text-white border-2 border-red-600 hover:bg-red-800 focus:ring-red-300'
      : 'bg-red-600 text-white hover:bg-red-700 focus:ring-red-300 active:bg-red-800',
    ghost: useHighContrast
      ? 'text-black hover:bg-gray-200 border-2 border-gray-400 focus:ring-gray-300'
      : 'text-gray-700 hover:bg-gray-100 focus:ring-gray-300 active:bg-gray-200'
  };

  const sizeClasses = {
    // Mobile sizes ensure minimum touch target of 44px
    sm: isMobile ? 'px-4 py-3 text-sm min-h-[44px] min-w-[44px]' : 'px-3 py-1.5 text-sm',
    md: isMobile ? 'px-6 py-4 text-base min-h-[48px]' : 'px-4 py-2 text-base',
    lg: isMobile ? 'px-8 py-5 text-lg min-h-[52px]' : 'px-6 py-3 text-lg',
    xl: 'px-10 py-6 text-xl min-h-[56px]' // Extra large for mobile
  };

  // Ensure minimum touch size
  const touchSizeStyle = isMobile && minTouchSize ? {
    minHeight: `${minTouchSize}px`,
    minWidth: size === 'sm' ? `${minTouchSize}px` : 'auto'
  } : {};

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
      style={touchSizeStyle}
      disabled={disabled || loading}
      onClick={handleClick}
      onTouchStart={handleTouchStart}
      onTouchEnd={handleTouchEnd}
      // Enhanced accessibility for mobile
      role="button"
      tabIndex={disabled ? -1 : 0}
      aria-pressed={isPressed}
      aria-label={typeof children === 'string' ? children : undefined}
      {...props}
    >
      {loading ? (
        <div className="flex items-center">
          <svg 
            className={`animate-spin mr-2 ${size === 'sm' ? 'h-4 w-4' : size === 'lg' || size === 'xl' ? 'h-6 w-6' : 'h-5 w-5'}`}
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
          <span>Loading...</span>
        </div>
      ) : children}
      
      {/* Long press indicator */}
      {onLongPress && (
        <div className="sr-only">
          Long press for additional options
        </div>
      )}
    </button>
  );
});

MobileButton.displayName = 'MobileButton';