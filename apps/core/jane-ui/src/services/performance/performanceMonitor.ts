/**
 * Enhanced Performance Monitor for Jane-UI
 * Constitutional compliance with domain-specific thresholds and executive function accommodations
 */

import { NavigationOptimization, PerformanceConfig, PerformanceMetrics } from '../types/performance';

class PerformanceMonitor {
  private config: PerformanceConfig;
  private metrics: PerformanceMetrics[] = [];
  private navigationState: NavigationOptimization;

  constructor() {
    this.config = {
      domains: {
        security: { threshold: 1000, critical: true },
        productivity: { threshold: 2000, priority: 'high' },
        mtg: { threshold: 3000, priority: 'medium' },
        infrastructure: { threshold: 5000, priority: 'low' },
      },
      ui: {
        interaction: 200, // Executive function requirement
        navigation: 300,
        dataLoad: 500,
      },
      bundleSize: {
        maxMainBundle: '2MB',
        maxTotalSize: '5MB',
        chunkSizeWarning: '244KB',
      },
    };

    this.navigationState = {
      contextSwitching: {
        maxActiveTools: 5,
        persistentContext: true,
        quickSwitch: [],
      },
      executiveFunction: {
        taskBreakdown: true,
        progressIndicators: true,
        timeEstimates: true,
        focusMode: false,
      },
    };

    this.initializePerformanceObserver();
  }

  private initializePerformanceObserver(): void {
    if (typeof window !== 'undefined' && 'PerformanceObserver' in window) {
      const observer = new PerformanceObserver((list) => {
        for (const entry of list.getEntries()) {
          this.processPerformanceEntry(entry);
        }
      });

      observer.observe({ entryTypes: ['measure', 'navigation', 'paint'] });
    }
  }

  private processPerformanceEntry(entry: PerformanceEntry): void {
    // Process different types of performance entries
    if (entry.entryType === 'measure') {
      this.recordCustomMetric(entry.name, entry.duration);
    } else if (entry.entryType === 'navigation') {
      this.recordNavigationMetric(entry as PerformanceNavigationTiming);
    } else if (entry.entryType === 'paint') {
      this.recordPaintMetric(entry as PerformancePaintTiming);
    }
  }

  private recordCustomMetric(operation: string, duration: number): void {
    const domain = this.inferDomain(operation);
    const threshold = this.config.domains[domain].threshold;
    const compliant = duration <= threshold;

    const metric: PerformanceMetrics = {
      timestamp: Date.now(),
      domain,
      operation,
      duration,
      threshold,
      compliant,
    };

    this.metrics.push(metric);

    // Alert on critical violations
    if (!compliant && (domain === 'security' || duration > threshold * 2)) {
      this.alertPerformanceViolation(metric);
    }

    // Trim metrics array to prevent memory leaks (keep last 1000)
    if (this.metrics.length > 1000) {
      this.metrics = this.metrics.slice(-1000);
    }
  }

  private recordNavigationMetric(entry: PerformanceNavigationTiming): void {
    const loadTime = entry.loadEventEnd - entry.navigationStart;
    this.recordCustomMetric('page-load', loadTime);
  }

  private recordPaintMetric(entry: PerformancePaintTiming): void {
    if (entry.name === 'first-contentful-paint') {
      this.recordCustomMetric('fcp', entry.startTime);
    } else if (entry.name === 'largest-contentful-paint') {
      this.recordCustomMetric('lcp', entry.startTime);
    }
  }

  private inferDomain(operation: string): keyof PerformanceConfig['domains'] {
    const lowerOp = operation.toLowerCase();
    
    if (lowerOp.includes('security') || lowerOp.includes('misp') || lowerOp.includes('malware')) {
      return 'security';
    } else if (lowerOp.includes('productivity') || lowerOp.includes('n8n') || lowerOp.includes('dispatch')) {
      return 'productivity';
    } else if (lowerOp.includes('mtg') || lowerOp.includes('tcg') || lowerOp.includes('commander')) {
      return 'mtg';
    } else {
      return 'infrastructure';
    }
  }

  private alertPerformanceViolation(metric: PerformanceMetrics): void {
    console.warn(`🚨 Performance Violation: ${metric.operation} took ${metric.duration}ms (threshold: ${metric.threshold}ms)`);
    
    // Could integrate with error reporting service
    if (typeof window !== 'undefined') {
      window.dispatchEvent(new CustomEvent('performance-violation', { 
        detail: metric 
      }));
    }
  }

  // Public API methods
  public measureOperation<T>(
    operation: string, 
    fn: () => Promise<T> | T,
    domain?: keyof PerformanceConfig['domains']
  ): Promise<T> | T {
    const start = performance.now();
    
    const finish = (result: T) => {
      const duration = performance.now() - start;
      const targetDomain = domain || this.inferDomain(operation);
      const threshold = this.config.domains[targetDomain].threshold;
      
      this.recordCustomMetric(operation, duration);
      return result;
    };

    try {
      const result = fn();
      
      if (result instanceof Promise) {
        return result.then(finish);
      } else {
        return finish(result);
      }
    } catch (error) {
      const duration = performance.now() - start;
      this.recordCustomMetric(`${operation}-error`, duration);
      throw error;
    }
  }

  public markUIInteraction(interaction: string): void {
    const threshold = this.config.ui.interaction;
    performance.mark(`ui-${interaction}-start`);
    
    // Measure after next tick to capture React updates
    setTimeout(() => {
      performance.mark(`ui-${interaction}-end`);
      performance.measure(`ui-${interaction}`, `ui-${interaction}-start`, `ui-${interaction}-end`);
    }, 0);
  }

  public trackToolSwitch(fromTool: string, toTool: string): void {
    const start = performance.now();
    
    // Update quick switch history
    const { quickSwitch } = this.navigationState.contextSwitching;
    if (!quickSwitch.includes(toTool)) {
      quickSwitch.unshift(toTool);
      if (quickSwitch.length > 5) quickSwitch.pop();
    }
    
    // Record context switch timing
    requestIdleCallback(() => {
      const duration = performance.now() - start;
      this.recordCustomMetric(`context-switch-${fromTool}-to-${toTool}`, duration);
    });
  }

  public enableFocusMode(): void {
    this.navigationState.executiveFunction.focusMode = true;
    document.body.classList.add('focus-mode');
    
    // Disable non-critical animations and effects
    document.documentElement.style.setProperty('--animation-speed', '0.1s');
  }

  public disableFocusMode(): void {
    this.navigationState.executiveFunction.focusMode = false;
    document.body.classList.remove('focus-mode');
    
    // Restore animations
    document.documentElement.style.removeProperty('--animation-speed');
  }

  public getMetrics(domain?: keyof PerformanceConfig['domains']): PerformanceMetrics[] {
    if (domain) {
      return this.metrics.filter(m => m.domain === domain);
    }
    return [...this.metrics];
  }

  public getComplianceReport(): Record<string, { compliant: number; total: number; percentage: number }> {
    const report: Record<string, { compliant: number; total: number; percentage: number }> = {};
    
    for (const domain of Object.keys(this.config.domains) as Array<keyof PerformanceConfig['domains']>) {
      const domainMetrics = this.metrics.filter(m => m.domain === domain);
      const compliant = domainMetrics.filter(m => m.compliant).length;
      const total = domainMetrics.length;
      
      report[domain] = {
        compliant,
        total,
        percentage: total > 0 ? Math.round((compliant / total) * 100) : 100,
      };
    }
    
    return report;
  }

  public clearMetrics(): void {
    this.metrics = [];
  }
}

// Singleton instance
export const performanceMonitor = new PerformanceMonitor();

// React hook for performance monitoring
export function usePerformanceMonitor() {
  return {
    measureOperation: performanceMonitor.measureOperation.bind(performanceMonitor),
    markUIInteraction: performanceMonitor.markUIInteraction.bind(performanceMonitor),
    trackToolSwitch: performanceMonitor.trackToolSwitch.bind(performanceMonitor),
    enableFocusMode: performanceMonitor.enableFocusMode.bind(performanceMonitor),
    disableFocusMode: performanceMonitor.disableFocusMode.bind(performanceMonitor),
    getMetrics: performanceMonitor.getMetrics.bind(performanceMonitor),
    getComplianceReport: performanceMonitor.getComplianceReport.bind(performanceMonitor),
  };
}