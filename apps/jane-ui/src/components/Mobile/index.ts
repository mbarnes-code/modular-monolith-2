/**
 * Mobile Components Index
 * Executive function-optimized mobile components for Jane Platform
 */

export { default as MobileDashboard } from './MobileDashboard';
export { default as MobileLayout } from './MobileLayout';
export { default as MobileNavigation } from './MobileNavigation';

// Mobile-specific types
export interface MobileViewport {
  width: number;
  height: number;
  isMobile: boolean;
  isTablet: boolean;
  orientation: 'portrait' | 'landscape';
}

export interface MobileGesture {
  type: 'swipe' | 'tap' | 'longPress' | 'pinch';
  direction?: 'up' | 'down' | 'left' | 'right';
  target: object;
  timestamp: number;
}

// ADHD/Autism mobile accommodations
export interface ExecutiveFunctionMobileConfig {
  reducedMotion: boolean;
  highContrast: boolean;
  largeText: boolean;
  simplifiedNavigation: boolean;
  vibrationFeedback: boolean;
  autoHideElements: boolean;
}