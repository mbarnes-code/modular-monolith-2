/**
 * Mobile-Optimized Focus Indicator Component
 * 
 * Enhanced focus indicators for ADHD/autism support on mobile devices
 * Provides touch-friendly visual feedback with gesture support
 */

import React, { useCallback, useEffect, useState } from 'react';
import { FocusAccommodation } from './types';

interface MobileFocusIndicatorProps {
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
  /** Mobile-specific settings */
  mobileSettings?: {
    /** Touch feedback enabled */
    touchFeedback?: boolean;
    /** Haptic feedback for supported devices */
    hapticFeedback?: boolean;
    /** Larger touch targets */
    largeTouchTargets?: boolean;
    /** Voice guidance */
    voiceGuidance?: boolean;
  };
  /** Callback when focus changes */
  onFocusChange?: (targetId: string | null) => void;
}

export const MobileFocusIndicator: React.FC<MobileFocusIndicatorProps> = ({
  targetId,
  accommodations,
  enhanced = false,
  focusColor = '#007ACC',
  ariaLabel = 'Current focus indicator',
  mobileSettings = {},
  onFocusChange
}) => {
  const [currentFocus, setCurrentFocus] = useState<string | null>(targetId || null);
  const [isVisible, setIsVisible] = useState(false);
  const [isMobile, setIsMobile] = useState(false);
  const [touchPosition, setTouchPosition] = useState<{ x: number; y: number } | null>(null);

  const {
    touchFeedback = true,
    hapticFeedback = true,
    largeTouchTargets = true,
    voiceGuidance = false
  } = mobileSettings;

  // Detect mobile viewport
  useEffect(() => {
    const checkMobile = () => {
      setIsMobile(window.innerWidth < 768 || 'ontouchstart' in window);
    };

    checkMobile();
    window.addEventListener('resize', checkMobile);
    return () => window.removeEventListener('resize', checkMobile);
  }, []);

  // Haptic feedback helper
  const triggerHapticFeedback = useCallback((type: 'light' | 'medium' | 'heavy' = 'light') => {
    if (!hapticFeedback || !isMobile) return;

    // Check if device supports haptic feedback
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
  const announceElement = useCallback((elementId: string) => {
    if (!voiceGuidance || !isMobile) return;

    const element = document.getElementById(elementId);
    if (!element) return;

    const text = element.getAttribute('aria-label') || 
                 element.getAttribute('title') ||
                 element.textContent?.substring(0, 50) ||
                 'Element focused';

    // Use Web Speech API if available
    if ('speechSynthesis' in window) {
      const utterance = new SpeechSynthesisUtterance(`Focused on ${text}`);
      utterance.volume = 0.5;
      utterance.rate = 1.2;
      speechSynthesis.speak(utterance);
    }
  }, [voiceGuidance, isMobile]);

  // Enhanced mobile focus handling
  useEffect(() => {
    if (!accommodations.enhance_focus_indicators) return;

    const handleFocusIn = (event: FocusEvent) => {
      const target = event.target as HTMLElement;
      const focusId = target.id || target.getAttribute('data-focus-id');
      
      if (focusId) {
        setCurrentFocus(focusId);
        setIsVisible(true);
        onFocusChange?.(focusId);
        
        // Mobile-specific feedback
        if (isMobile) {
          triggerHapticFeedback('light');
          announceElement(focusId);
        }
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

    // Touch-specific handlers for mobile
    const handleTouchStart = (event: TouchEvent) => {
      if (!isMobile || !touchFeedback) return;

      const touch = event.touches[0];
      const target = document.elementFromPoint(touch.clientX, touch.clientY) as HTMLElement;
      
      if (target?.id || target?.getAttribute('data-focus-id')) {
        setTouchPosition({ x: touch.clientX, y: touch.clientY });
        triggerHapticFeedback('light');
      }
    };

    const handleTouchEnd = () => {
      if (!isMobile) return;
      
      setTimeout(() => {
        setTouchPosition(null);
      }, 300);
    };

    // Add event listeners
    document.addEventListener('focusin', handleFocusIn);
    document.addEventListener('focusout', handleFocusOut);
    
    if (isMobile) {
      document.addEventListener('touchstart', handleTouchStart, { passive: true });
      document.addEventListener('touchend', handleTouchEnd, { passive: true });
    }

    return () => {
      document.removeEventListener('focusin', handleFocusIn);
      document.removeEventListener('focusout', handleFocusOut);
      
      if (isMobile) {
        document.removeEventListener('touchstart', handleTouchStart);
        document.removeEventListener('touchend', handleTouchEnd);
      }
    };
  }, [accommodations.enhance_focus_indicators, onFocusChange, isMobile, touchFeedback, triggerHapticFeedback, announceElement]);

  if (!accommodations.enhance_focus_indicators || !isVisible || !currentFocus) {
    return null;
  }

  const getMobileFocusStyles = () => {
    const baseStyles = {
      position: 'absolute' as const,
      pointerEvents: 'none' as const,
      borderRadius: isMobile ? '8px' : '4px', // Larger radius on mobile
      transition: 'all 0.15s ease-out',
      zIndex: 9999,
    };

    if (isMobile) {
      return {
        ...baseStyles,
        border: enhanced ? `4px solid ${focusColor}` : `3px solid ${focusColor}`,
        boxShadow: enhanced 
          ? `0 0 0 2px white, 0 0 0 6px ${focusColor}40, 0 0 15px ${focusColor}60`
          : `0 0 0 1px white, 0 0 8px ${focusColor}40`,
        // Add glow effect for better visibility on mobile
        background: `linear-gradient(45deg, ${focusColor}10, ${focusColor}05)`,
      };
    } else {
      return {
        ...baseStyles,
        border: enhanced ? `3px solid ${focusColor}` : `2px solid ${focusColor}`,
        boxShadow: enhanced 
          ? `0 0 0 1px white, 0 0 0 4px ${focusColor}40, 0 0 10px ${focusColor}60`
          : `0 0 0 1px white, 0 0 5px ${focusColor}40`,
      };
    }
  };

  const updatePosition = () => {
    const targetElement = document.getElementById(currentFocus) || 
                         document.querySelector(`[data-focus-id="${currentFocus}"]`);
    
    if (!targetElement) return null;

    const rect = targetElement.getBoundingClientRect();
    const scrollX = window.pageXOffset || document.documentElement.scrollLeft;
    const scrollY = window.pageYOffset || document.documentElement.scrollTop;

    // Mobile adjustments
    const padding = isMobile ? (largeTouchTargets ? 8 : 4) : 2;
    const minSize = isMobile ? 44 : 0; // iOS minimum touch target size

    return {
      ...getMobileFocusStyles(),
      left: rect.left + scrollX - padding,
      top: rect.top + scrollY - padding,
      width: Math.max(rect.width + (padding * 2), minSize),
      height: Math.max(rect.height + (padding * 2), minSize),
    };
  };

  const indicatorStyle = updatePosition();
  if (!indicatorStyle) return null;

  return (
    <>
      {/* Main focus indicator */}
      <div
        role="presentation"
        aria-label={ariaLabel}
        style={indicatorStyle}
        className="mental-prosthetic-focus-indicator mobile-optimized"
      />
      
      {/* Touch feedback indicator */}
      {isMobile && touchPosition && touchFeedback && (
        <div
          role="presentation"
          style={{
            position: 'fixed',
            left: touchPosition.x - 20,
            top: touchPosition.y - 20,
            width: 40,
            height: 40,
            borderRadius: '50%',
            background: `radial-gradient(circle, ${focusColor}40, transparent)`,
            pointerEvents: 'none',
            zIndex: 10000,
            animation: 'touchRipple 0.3s ease-out forwards',
          }}
        />
      )}
      
      {/* CSS Animation for touch ripple */}
      <style dangerouslySetInnerHTML={{
        __html: `
          @keyframes touchRipple {
            0% {
              transform: scale(0);
              opacity: 1;
            }
            100% {
              transform: scale(1);
              opacity: 0;
            }
          }
          
          .mental-prosthetic-focus-indicator.mobile-optimized {
            backdrop-filter: blur(1px);
          }
          
          @media (max-width: 768px) {
            .mental-prosthetic-focus-indicator {
              border-width: 3px !important;
              box-shadow: 0 0 0 1px white, 0 0 8px rgba(0, 122, 204, 0.4) !important;
            }
          }
          
          @media (prefers-contrast: high) {
            .mental-prosthetic-focus-indicator {
              border-color: #000 !important;
              box-shadow: 0 0 0 2px #fff, 0 0 0 4px #000 !important;
            }
          }
          
          @media (prefers-reduced-motion: reduce) {
            .mental-prosthetic-focus-indicator {
              transition: none !important;
            }
          }
        `
      }} />
    </>
  );
};