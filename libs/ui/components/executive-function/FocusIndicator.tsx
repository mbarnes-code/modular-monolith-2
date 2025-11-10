/**
 * Focus Indicator Component
 * 
 * Enhanced focus indicators for ADHD/autism support
 * Provides clear visual feedback for current focus areas
 */

import React, { useEffect, useState } from 'react';
import { FocusAccommodation } from './types';

interface FocusIndicatorProps {
  /** Current focus target element ID */
  targetId?: string;
  /** Focus accommodation settings */
  accommodations: FocusAccommodation;
  /** Whether to show enhanced focus ring */
  enhanced?: boolean;
  /** Custom focus indicator color */
  focusColor?: string;
  /** Accessibility label */
  ariaLabel?: string;
  /** Callback when focus changes */
  onFocusChange?: (targetId: string | null) => void;
}

export const FocusIndicator: React.FC<FocusIndicatorProps> = ({
  targetId,
  accommodations,
  enhanced = false,
  focusColor = '#007ACC',
  ariaLabel = 'Current focus indicator',
  onFocusChange
}) => {
  const [currentFocus, setCurrentFocus] = useState<string | null>(targetId || null);
  const [isVisible, setIsVisible] = useState(false);

  useEffect(() => {
    if (!accommodations.enhance_focus_indicators) return;

    const handleFocusIn = (event: FocusEvent) => {
      const target = event.target as HTMLElement;
      const focusId = target.id || target.getAttribute('data-focus-id');
      
      if (focusId) {
        setCurrentFocus(focusId);
        setIsVisible(true);
        onFocusChange?.(focusId);
      }
    };

    const handleFocusOut = () => {
      // Delay hiding to prevent flicker during focus transitions
      setTimeout(() => {
        if (!document.activeElement || document.activeElement === document.body) {
          setIsVisible(false);
          setCurrentFocus(null);
          onFocusChange?.(null);
        }
      }, 100);
    };

    document.addEventListener('focusin', handleFocusIn);
    document.addEventListener('focusout', handleFocusOut);

    return () => {
      document.removeEventListener('focusin', handleFocusIn);
      document.removeEventListener('focusout', handleFocusOut);
    };
  }, [accommodations.enhance_focus_indicators, onFocusChange]);

  if (!accommodations.enhance_focus_indicators || !isVisible || !currentFocus) {
    return null;
  }

  const focusStyles = {
    position: 'absolute' as const,
    pointerEvents: 'none' as const,
    border: enhanced ? `3px solid ${focusColor}` : `2px solid ${focusColor}`,
    borderRadius: '4px',
    boxShadow: enhanced 
      ? `0 0 0 1px white, 0 0 0 4px ${focusColor}40, 0 0 10px ${focusColor}60`
      : `0 0 0 1px white, 0 0 5px ${focusColor}40`,
    transition: 'all 0.15s ease-out',
    zIndex: 9999,
  };

  const updatePosition = () => {
    const targetElement = document.getElementById(currentFocus) || 
                         document.querySelector(`[data-focus-id="${currentFocus}"]`);
    
    if (!targetElement) return null;

    const rect = targetElement.getBoundingClientRect();
    const scrollX = window.pageXOffset || document.documentElement.scrollLeft;
    const scrollY = window.pageYOffset || document.documentElement.scrollTop;

    return {
      ...focusStyles,
      left: rect.left + scrollX - 2,
      top: rect.top + scrollY - 2,
      width: rect.width + 4,
      height: rect.height + 4,
    };
  };

  const indicatorStyle = updatePosition();
  if (!indicatorStyle) return null;

  return (
    <div
      role="presentation"
      aria-label={ariaLabel}
      style={indicatorStyle}
      className="mental-prosthetic-focus-indicator"
    />
  );
};