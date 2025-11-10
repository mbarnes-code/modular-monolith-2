/**
 * Performance Monitor - Task T050 COMPLETED
 * 
 * Performance monitoring for <200ms response time validation
 * - Constitutional compliance monitoring
 * - Domain-specific performance tiers
 * - Real-time metrics collection
 * - Executive function impact tracking
 */

'use client';

import React, { createContext, useCallback, useContext, useEffect, useState } from 'react';

interface PerformanceMetric {
  name: string;
  value: number;
  timestamp: number;
  domain: 'security' | 'productivity' | 'mtg' | 'infrastructure' | 'ui';
  threshold: number;
  compliant: boolean;
}

interface DomainThresholds {
  security: number;    // <1s
  productivity: number; // <2s
  mtg: number;         // <3s
  infrastructure: number; // <5s
  ui: number;          // <200ms
}

interface PerformanceState {
  metrics: PerformanceMetric[];
  realTimeMetrics: Map<string, number>;
  constitutionalCompliance: boolean;
  overallScore: number;
  domainScores: Record<string, number>;
  isMonitoring: boolean;
  alerts: PerformanceAlert[];
}

interface PerformanceAlert {
  id: string;
  type: 'warning' | 'error' | 'info';
  domain: string;
  message: string;
  threshold: number;
  actual: number;
  timestamp: number;
  resolved: boolean;
}

interface PerformanceReport {
  timestamp: number;
  overallScore: number;
  constitutionalCompliance: boolean;
  domainBreakdown: Record<string, {
    score: number;
    compliant: boolean;
    averageResponseTime: number;
    threshold: number;
  }>;
  recommendations: string[];
  criticalIssues: PerformanceAlert[];
}

interface PerformanceContextType {
  state: PerformanceState;
  startMonitoring: () => void;
  stopMonitoring: () => void;
  recordMetric: (name: string, value: number, domain: keyof DomainThresholds) => void;
  recordUIInteraction: (interactionType: string, duration: number) => void;
  generateReport: () => PerformanceReport;
  clearMetrics: () => void;
  getConstitutionalStatus: () => boolean;
}

const DOMAIN_THRESHOLDS: DomainThresholds = {
  security: 1000,        // 1s for security tools (threat analysis criticality)
  productivity: 2000,    // 2s for productivity tools (task management workflows)
  mtg: 3000,            // 3s for MTG tools (game analysis complexity)
  infrastructure: 5000,  // 5s for infrastructure tools (system operations tolerance)
  ui: 200               // 200ms for UI interactions (executive function support)
};

const PerformanceContext = createContext<PerformanceContextType | null>(null);

export function PerformanceMonitorProvider({ children }: { children: React.ReactNode }) {
  const [state, setState] = useState<PerformanceState>({
    metrics: [],
    realTimeMetrics: new Map(),
    constitutionalCompliance: true,
    overallScore: 100,
    domainScores: {},
    isMonitoring: false,
    alerts: []
  });

  const [monitoringInterval, setMonitoringInterval] = useState<unknown>(null);

  // Browser detection helper
  const isBrowser = () => typeof window !== 'undefined';

  const recordMetric = useCallback((name: string, value: number, domain: keyof DomainThresholds) => {
    const threshold = DOMAIN_THRESHOLDS[domain];
    const compliant = value <= threshold;
    const timestamp = Date.now();

    const metric: PerformanceMetric = {
      name,
      value,
      timestamp,
      domain,
      threshold,
      compliant
    };

    setState(prev => {
      const newMetrics = [...prev.metrics.slice(-99), metric]; // Keep last 100 metrics
      const newRealTimeMetrics = new Map(prev.realTimeMetrics);
      newRealTimeMetrics.set(`${domain}-${name}`, value);

      // Generate alert if not compliant
      const alerts = [...prev.alerts];
      if (!compliant) {
        const alert: PerformanceAlert = {
          id: `${timestamp}-${domain}-${name}`,
          type: value > threshold * 2 ? 'error' : 'warning',
          domain,
          message: `${name} exceeded ${domain} threshold: ${value}ms > ${threshold}ms`,
          threshold,
          actual: value,
          timestamp,
          resolved: false
        };
        alerts.push(alert);
      }

      // Calculate scores
      const domainMetrics = newMetrics.filter(m => m.domain === domain);
      const domainScore = domainMetrics.length > 0 
        ? (domainMetrics.filter(m => m.compliant).length / domainMetrics.length) * 100
        : 100;

      const newDomainScores = { ...prev.domainScores, [domain]: domainScore };
      const overallScore = Object.values(newDomainScores).reduce((sum, score) => sum + score, 0) / 
        Math.max(Object.keys(newDomainScores).length, 1);

      const constitutionalCompliance = overallScore >= 80 && 
        newDomainScores.ui >= 90; // UI must be especially responsive

      return {
        ...prev,
        metrics: newMetrics,
        realTimeMetrics: newRealTimeMetrics,
        domainScores: newDomainScores,
        overallScore,
        constitutionalCompliance,
        alerts: alerts.slice(-50) // Keep last 50 alerts
      };
    });
  }, []);

  const recordUIInteraction = useCallback((interactionType: string, duration: number) => {
    recordMetric(`ui-${interactionType}`, duration, 'ui');
  }, [recordMetric]);

  const startMonitoring = useCallback(() => {
    if (!isBrowser() || state.isMonitoring) return;

    setState(prev => ({ ...prev, isMonitoring: true }));

    // Monitor performance API metrics
    const interval = (globalThis as any).setInterval?.(() => {
      if (!isBrowser()) return;

      try {
        const performance = (globalThis as any).performance;
        if (!performance) return;

        // Navigation timing
        const navigation = performance.getEntriesByType?.('navigation')?.[0];
        if (navigation) {
          recordMetric('page-load', navigation.loadEventEnd - navigation.fetchStart, 'ui');
          recordMetric('dom-content-loaded', navigation.domContentLoadedEventEnd - navigation.fetchStart, 'ui');
        }

        // Resource timing
        const resources = performance.getEntriesByType?.('resource') || [];
        resources.forEach((resource: any) => {
          if (resource.duration > 0) {
            const domain = resource.name.includes('api') ? 'productivity' : 'ui';
            recordMetric(`resource-${resource.name.split('/').pop()}`, resource.duration, domain);
          }
        });

        // Memory usage (if available)
        const memory = (performance as any).memory;
        if (memory) {
          const memoryUsage = (memory.usedJSHeapSize / memory.totalJSHeapSize) * 100;
          recordMetric('memory-usage', memoryUsage, 'infrastructure');
        }

      } catch (error) {
        // Silently fail if performance APIs not available
      }
    }, 5000); // Check every 5 seconds

    setMonitoringInterval(interval);
  }, [state.isMonitoring, recordMetric]);

  const stopMonitoring = useCallback(() => {
    setState(prev => ({ ...prev, isMonitoring: false }));
    
    if (monitoringInterval && isBrowser()) {
      (globalThis as any).clearInterval?.(monitoringInterval);
      setMonitoringInterval(null);
    }
  }, [monitoringInterval]);

  const generateReport = useCallback((): PerformanceReport => {
    const timestamp = Date.now();
    const { metrics, overallScore, constitutionalCompliance, domainScores, alerts } = state;

    // Calculate domain breakdown
    const domainBreakdown: Record<string, any> = {};
    Object.keys(DOMAIN_THRESHOLDS).forEach(domain => {
      const domainMetrics = metrics.filter(m => m.domain === domain);
      const compliantMetrics = domainMetrics.filter(m => m.compliant);
      const averageResponseTime = domainMetrics.length > 0
        ? domainMetrics.reduce((sum, m) => sum + m.value, 0) / domainMetrics.length
        : 0;

      domainBreakdown[domain] = {
        score: domainScores[domain] || 100,
        compliant: (domainScores[domain] || 100) >= 80,
        averageResponseTime,
        threshold: DOMAIN_THRESHOLDS[domain as keyof DomainThresholds]
      };
    });

    // Generate recommendations
    const recommendations: string[] = [];
    if (!constitutionalCompliance) {
      recommendations.push('Overall performance below constitutional requirements (80%)');
    }

    Object.entries(domainBreakdown).forEach(([domain, data]) => {
      if (!data.compliant) {
        recommendations.push(`Optimize ${domain} performance: ${data.averageResponseTime.toFixed(0)}ms > ${data.threshold}ms`);
      }
    });

    if (domainBreakdown.ui.averageResponseTime > 200) {
      recommendations.push('Critical: UI responsiveness below executive function requirements (<200ms)');
    }

    const criticalIssues = alerts.filter(alert => 
      alert.type === 'error' && !alert.resolved
    );

    return {
      timestamp,
      overallScore,
      constitutionalCompliance,
      domainBreakdown,
      recommendations,
      criticalIssues
    };
  }, [state]);

  const clearMetrics = useCallback(() => {
    setState(prev => ({
      ...prev,
      metrics: [],
      realTimeMetrics: new Map(),
      alerts: [],
      overallScore: 100,
      domainScores: {},
      constitutionalCompliance: true
    }));
  }, []);

  const getConstitutionalStatus = useCallback(() => {
    return state.constitutionalCompliance;
  }, [state.constitutionalCompliance]);

  // Auto-start monitoring
  useEffect(() => {
    if (isBrowser()) {
      startMonitoring();
    }

    return () => {
      stopMonitoring();
    };
  }, [startMonitoring, stopMonitoring]);

  // Monitor UI interactions
  useEffect(() => {
    if (!isBrowser()) return;

    const startTimes = new Map();

    const handleInteractionStart = (type: string) => (event: any) => {
      startTimes.set(event.target, { type, start: performance.now() });
    };

    const handleInteractionEnd = (event: any) => {
      const startData = startTimes.get(event.target);
      if (startData) {
        const duration = performance.now() - startData.start;
        recordUIInteraction(startData.type, duration);
        startTimes.delete(event.target);
      }
    };

    const globalObj = globalThis as any;
    
    // Monitor common UI interactions
    globalObj.addEventListener?.('click', handleInteractionStart('click'));
    globalObj.addEventListener?.('mouseup', handleInteractionEnd);
    globalObj.addEventListener?.('keydown', handleInteractionStart('keydown'));
    globalObj.addEventListener?.('keyup', handleInteractionEnd);

    return () => {
      globalObj.removeEventListener?.('click', handleInteractionStart('click'));
      globalObj.removeEventListener?.('mouseup', handleInteractionEnd);
      globalObj.removeEventListener?.('keydown', handleInteractionStart('keydown'));
      globalObj.removeEventListener?.('keyup', handleInteractionEnd);
    };
  }, [recordUIInteraction]);

  const contextValue: PerformanceContextType = {
    state,
    startMonitoring,
    stopMonitoring,
    recordMetric,
    recordUIInteraction,
    generateReport,
    clearMetrics,
    getConstitutionalStatus
  };

  return (
    <PerformanceContext.Provider value={contextValue}>
      {children}
      
      {/* Performance indicator overlay (for development) */}
      {state.isMonitoring && !state.constitutionalCompliance && (
        <div
          style={{
            position: 'fixed',
            top: '10px',
            right: '10px',
            background: '#ff6b6b',
            color: 'white',
            padding: '8px 12px',
            borderRadius: '4px',
            fontSize: '12px',
            fontWeight: 'bold',
            zIndex: 9999,
            pointerEvents: 'none'
          }}
        >
          ⚠️ Performance: {state.overallScore.toFixed(0)}%
        </div>
      )}
    </PerformanceContext.Provider>
  );
}

export function usePerformanceMonitor() {
  const context = useContext(PerformanceContext);
  if (!context) {
    throw new Error('usePerformanceMonitor must be used within PerformanceMonitorProvider');
  }
  return context;
}

// Performance timing hook for measuring component render times
export function usePerformanceTiming(componentName: string, domain: keyof DomainThresholds = 'ui') {
  const { recordMetric } = usePerformanceMonitor();
  
  useEffect(() => {
    const startTime = performance.now();
    
    return () => {
      const endTime = performance.now();
      const duration = endTime - startTime;
      recordMetric(`component-${componentName}`, duration, domain);
    };
  }, [componentName, domain, recordMetric]);
}

// Higher-order component for automatic performance monitoring
export function withPerformanceMonitoring<P extends object>(
  WrappedComponent: React.ComponentType<P>,
  componentName: string,
  domain: keyof DomainThresholds = 'ui'
) {
  return function PerformanceMonitoredComponent(props: P) {
    usePerformanceTiming(componentName, domain);
    return <WrappedComponent {...props} />;
  };
}

// Export types
export type {
    DomainThresholds, PerformanceAlert, PerformanceMetric, PerformanceReport, PerformanceState
};
