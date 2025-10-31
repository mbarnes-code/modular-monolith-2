/**
 * Mobile-Optimized Input Component with Executive Function Support
 * 
 * Enhanced input for mobile devices with ADHD/autism accommodations:
 * - Touch-friendly sizing and spacing
 * - Virtual keyboard optimization
 * - Voice input support
 * - Auto-correction and suggestions
 * - Focus management for mobile
 */

import React, { InputHTMLAttributes, forwardRef, useCallback, useEffect, useRef, useState } from 'react';
import { useExecutiveFunction } from '../executive-function';

interface MobileInputProps extends Omit<InputHTMLAttributes<HTMLInputElement>, 'size'> {
  label?: string;
  error?: string;
  hint?: string;
  size?: 'sm' | 'md' | 'lg';
  variant?: 'default' | 'filled' | 'borderless';
  highContrast?: boolean;
  /** Mobile-specific options */
  mobileOptions?: {
    /** Enable voice input */
    voiceInput?: boolean;
    /** Optimize for virtual keyboard */
    keyboardOptimized?: boolean;
    /** Auto-focus on mobile */
    autoFocusMobile?: boolean;
    /** Enable predictive text */
    predictiveText?: boolean;
    /** Enable spell check */
    spellCheck?: boolean;
    /** Haptic feedback on input */
    hapticFeedback?: boolean;
    /** Voice guidance for errors */
    voiceGuidance?: boolean;
  };
}

export const MobileInput = forwardRef<HTMLInputElement, MobileInputProps>(({
  label,
  error,
  hint,
  size = 'md',
  variant = 'default',
  highContrast,
  className = '',
  type = 'text',
  disabled,
  mobileOptions = {},
  onChange,
  onFocus,
  onBlur,
  ...props
}, ref) => {
  const { state } = useExecutiveFunction();
  const [isFocused, setIsFocused] = useState(false);
  const [isListening, setIsListening] = useState(false);
  const voiceRecognitionRef = useRef<any>(null);

  const {
    voiceInput = false,
    keyboardOptimized = true,
    autoFocusMobile = false,
    predictiveText = true,
    spellCheck = true,
    hapticFeedback = false,
    voiceGuidance = false
  } = mobileOptions;

  // Use high contrast if user preference or explicit prop
  const useHighContrast = highContrast ?? state.autismOptions.sensory_preferences?.high_contrast ?? false;
  
  // Check if device is mobile
  const isMobile = typeof window !== 'undefined' && (
    window.innerWidth < 768 || 'ontouchstart' in window
  );

  // Auto-focus on mobile if enabled
  useEffect(() => {
    if (autoFocusMobile && isMobile && ref && 'current' in ref && ref.current) {
      // Delay to ensure proper focus after keyboard appears
      const timer = setTimeout(() => {
        ref.current?.focus();
      }, 100);
      return () => clearTimeout(timer);
    }
  }, [autoFocusMobile, isMobile, ref]);

  // Haptic feedback helper
  const triggerHapticFeedback = useCallback((type: 'light' | 'medium' = 'light') => {
    if (!hapticFeedback || !isMobile) return;

    if ('vibrate' in navigator) {
      const patterns = {
        light: [5],
        medium: [10]
      };
      navigator.vibrate(patterns[type]);
    }
  }, [hapticFeedback, isMobile]);

  // Voice guidance helper
  const announceMessage = useCallback((message: string) => {
    if (!voiceGuidance || !isMobile) return;

    if ('speechSynthesis' in window) {
      const utterance = new SpeechSynthesisUtterance(message);
      utterance.volume = 0.3;
      utterance.rate = 1.2;
      speechSynthesis.speak(utterance);
    }
  }, [voiceGuidance, isMobile]);

  // Voice input functionality
  const startVoiceInput = useCallback(() => {
    if (!voiceInput || !isMobile) return;

    const SpeechRecognition = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;
    
    if (!SpeechRecognition) {
      announceMessage('Voice input not supported on this device');
      return;
    }

    const recognition = new SpeechRecognition();
    recognition.continuous = false;
    recognition.interimResults = false;
    recognition.lang = 'en-US';

    recognition.onstart = () => {
      setIsListening(true);
      triggerHapticFeedback('light');
      announceMessage('Listening...');
    };

    recognition.onresult = (event: any) => {
      const transcript = event.results[0][0].transcript;
      
      if (ref && 'current' in ref && ref.current) {
        ref.current.value = transcript;
        
        // Trigger change event
        const changeEvent = new Event('input', { bubbles: true });
        ref.current.dispatchEvent(changeEvent);
        
        if (onChange) {
          onChange(changeEvent as any);
        }
      }
      
      triggerHapticFeedback('medium');
      announceMessage(`Text entered: ${transcript}`);
    };

    recognition.onerror = (event: any) => {
      announceMessage(`Voice input error: ${event.error}`);
      triggerHapticFeedback('medium');
    };

    recognition.onend = () => {
      setIsListening(false);
    };

    voiceRecognitionRef.current = recognition;
    recognition.start();
  }, [voiceInput, isMobile, announceMessage, triggerHapticFeedback, ref, onChange]);

  const handleFocus = (e: React.FocusEvent<HTMLInputElement>) => {
    setIsFocused(true);
    triggerHapticFeedback('light');
    
    if (label) {
      announceMessage(`Focused on ${label} input`);
    }
    
    onFocus?.(e);
  };

  const handleBlur = (e: React.FocusEvent<HTMLInputElement>) => {
    setIsFocused(false);
    onBlur?.(e);
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    // Provide subtle feedback on mobile
    if (isMobile && e.target.value !== props.value) {
      triggerHapticFeedback('light');
    }
    
    onChange?.(e);
  };

  // Base classes for input
  const baseClasses = [
    'w-full transition-all duration-200',
    'focus:outline-none',
    'disabled:opacity-50 disabled:cursor-not-allowed',
    // Mobile-specific optimizations
    isMobile && 'touch-manipulation',
  ].filter(Boolean);

  // Size classes optimized for mobile
  const sizeClasses = {
    sm: isMobile ? 'px-4 py-3 text-base min-h-[44px]' : 'px-3 py-2 text-sm',
    md: isMobile ? 'px-4 py-4 text-base min-h-[48px]' : 'px-4 py-3 text-base',
    lg: isMobile ? 'px-6 py-5 text-lg min-h-[52px]' : 'px-6 py-4 text-lg'
  };

  // Variant classes
  const variantClasses = {
    default: useHighContrast
      ? 'border-2 border-black bg-white text-black focus:border-blue-600 focus:ring-2 focus:ring-blue-300'
      : 'border border-gray-300 bg-white text-gray-900 focus:border-blue-500 focus:ring-2 focus:ring-blue-200',
    filled: useHighContrast
      ? 'border-2 border-black bg-gray-100 text-black focus:bg-white focus:border-blue-600'
      : 'border border-transparent bg-gray-100 text-gray-900 focus:bg-white focus:border-blue-500 focus:ring-2 focus:ring-blue-200',
    borderless: useHighContrast
      ? 'border-b-2 border-black bg-transparent text-black focus:border-blue-600'
      : 'border-b border-gray-300 bg-transparent text-gray-900 focus:border-blue-500'
  };

  // Error state classes
  const errorClasses = error
    ? useHighContrast
      ? 'border-red-600 focus:border-red-600 focus:ring-red-300'
      : 'border-red-500 focus:border-red-500 focus:ring-red-200'
    : '';

  const inputClasses = [
    ...baseClasses,
    sizeClasses[size],
    variantClasses[variant],
    errorClasses,
    variant !== 'borderless' && 'rounded-lg',
    className
  ].join(' ');

  // Get appropriate input mode and keyboard type for mobile
  const getInputMode = () => {
    if (!keyboardOptimized) return undefined;
    
    switch (type) {
      case 'email':
        return 'email';
      case 'tel':
        return 'tel';
      case 'url':
        return 'url';
      case 'number':
        return 'numeric';
      case 'search':
        return 'search';
      default:
        return 'text';
    }
  };

  return (
    <div className="w-full">
      {/* Label */}
      {label && (
        <label 
          htmlFor={props.id}
          className={`block text-sm font-medium mb-2 ${
            useHighContrast ? 'text-black' : 'text-gray-700'
          } ${error ? 'text-red-600' : ''}`}
        >
          {label}
          {props.required && <span className="text-red-500 ml-1">*</span>}
        </label>
      )}

      {/* Input container */}
      <div className="relative">
        <input
          ref={ref}
          type={type}
          className={inputClasses}
          disabled={disabled}
          onChange={handleChange}
          onFocus={handleFocus}
          onBlur={handleBlur}
          // Mobile optimizations
          inputMode={getInputMode()}
          autoComplete={keyboardOptimized ? 'on' : 'off'}
          autoCorrect={predictiveText && type === 'text' ? 'on' : 'off'}
          spellCheck={spellCheck && type === 'text'}
          // Prevent zoom on iOS
          style={isMobile ? { fontSize: Math.max(16, parseFloat(getComputedStyle(document.documentElement).fontSize)) } : undefined}
          {...props}
        />

        {/* Voice input button */}
        {voiceInput && isMobile && (
          <button
            type="button"
            onClick={startVoiceInput}
            disabled={disabled || isListening}
            className={`absolute right-3 top-1/2 transform -translate-y-1/2 p-2 rounded-full
              ${isListening 
                ? 'bg-red-100 text-red-600 animate-pulse' 
                : useHighContrast
                  ? 'text-black hover:bg-gray-200'
                  : 'text-gray-400 hover:text-gray-600 hover:bg-gray-100'
              } transition-colors duration-200`}
            aria-label={isListening ? 'Listening...' : 'Start voice input'}
          >
            {isListening ? (
              <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M7 4a3 3 0 016 0v4a3 3 0 11-6 0V4zm4 10.93A7.001 7.001 0 0017 8a1 1 0 10-2 0A5 5 0 015 8a1 1 0 00-2 0 7.001 7.001 0 006 6.93V17H6a1 1 0 100 2h8a1 1 0 100-2h-3v-2.07z" clipRule="evenodd" />
              </svg>
            ) : (
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z" />
              </svg>
            )}
          </button>
        )}
      </div>

      {/* Hint text */}
      {hint && !error && (
        <p className={`mt-2 text-sm ${useHighContrast ? 'text-gray-800' : 'text-gray-600'}`}>
          {hint}
        </p>
      )}

      {/* Error message */}
      {error && (
        <p className="mt-2 text-sm text-red-600" role="alert">
          {error}
        </p>
      )}
    </div>
  );
});

MobileInput.displayName = 'MobileInput';