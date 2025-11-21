/**
 * Performance Components - Enhanced for Jane-UI Platform
 * Constitutional compliance with executive function accommodations
 */

export { PerformanceDashboard } from './monitoring/PerformanceDashboard';
export { EnhancedNavigation, focusModeStyles } from './navigation/EnhancedNavigation';

// Performance monitoring services
export { 
  performanceMonitor, 
  usePerformanceMonitor 
} from '../services/performance/performanceMonitor';

// State management exports
export {
  useSharedContext,
  useSecurityStore,
  useProductivityStore,
  useMTGStore,
  useCrossDomainSync,
  eventBus
} from '../services/state/optimizedStateManager';

// Performance types
export type {
  PerformanceConfig,
  PerformanceMetrics,
  NavigationOptimization,
  OptimizedStateManagement,
  ComponentOptimization,
  BundleAnalysis
} from '../types/performance';