/**
 * Performance Configuration for 37-Tool Mental Prosthetic Platform
 * Constitutional compliance with executive function accommodations
 */

export interface PerformanceConfig {
  domains: {
    security: { threshold: 1000; critical: true };
    productivity: { threshold: 2000; priority: 'high' };
    mtg: { threshold: 3000; priority: 'medium' };
    infrastructure: { threshold: 5000; priority: 'low' };
  };
  ui: {
    interaction: 200; // Executive function requirement
    navigation: 300;
    dataLoad: 500;
  };
  bundleSize: {
    maxMainBundle: '2MB';
    maxTotalSize: '5MB';
    chunkSizeWarning: '244KB'; // Webpack default
  };
}

export interface NavigationOptimization {
  contextSwitching: {
    maxActiveTools: 5; // Reduce cognitive load
    persistentContext: boolean; // Maintain state
    quickSwitch: string[]; // Recently used tools
  };
  executiveFunction: {
    taskBreakdown: boolean;
    progressIndicators: boolean;
    timeEstimates: boolean;
    focusMode: boolean;
  };
}

export interface OptimizedStateManagement {
  persistence: {
    strategy: 'selective'; // Don't persist everything
    compression: boolean;
    encryption: boolean; // For sensitive security data
  };
  performance: {
    lazyLoading: boolean;
    stateNormalization: boolean;
    memoization: boolean;
  };
  crossDomain: {
    eventBus: boolean; // Tool-to-tool communication
    sharedContext: boolean;
    workflowState: boolean;
  };
}

export interface ComponentOptimization {
  lazyLoading: {
    toolComponents: boolean; // Load tools on demand
    routeBasedSplitting: boolean;
    priorityLoading: boolean; // Load frequent tools first
  };
  caching: {
    componentCache: boolean;
    apiResponseCache: boolean;
    imageOptimization: boolean;
  };
  accessibility: {
    adhdOptimizations: boolean;
    screenReaderSupport: boolean;
    keyboardNavigation: boolean;
  };
}

export interface PerformanceMetrics {
  timestamp: number;
  domain: 'security' | 'productivity' | 'mtg' | 'infrastructure';
  operation: string;
  duration: number;
  threshold: number;
  compliant: boolean;
  userId?: string;
}

export interface BundleAnalysis {
  mainBundleSize: number;
  totalSize: number;
  chunks: Array<{
    name: string;
    size: number;
    domain?: string;
  }>;
  warnings: string[];
  recommendations: string[];
}

export interface BundleSizeMetrics {
  mainBundleSize: number;
  totalBundleSize: number;
  domainChunks: Record<string, { size: number; chunks: string[] }>;
  violations: BundleSizeViolation[];
  recommendations: BundleOptimization[];
  constitutionalCompliance: boolean;
  timestamp: string;
}

export interface BundleSizeViolation {
  type: 'bundle_size' | 'domain_chunk' | 'dependency';
  name: string;
  message: string;
  actualSize: number;
  threshold: number;
  severity: 'info' | 'warn' | 'error' | 'critical';
}

export interface BundleOptimization {
  type: 'optimization' | 'domain_optimization' | 'dependency_optimization';
  priority: 'low' | 'medium' | 'high';
  domain?: string;
  message: string;
  details?: string;
}