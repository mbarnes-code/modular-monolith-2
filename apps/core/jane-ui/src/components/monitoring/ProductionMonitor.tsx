/**
 * Production Performance Monitor
 * Comprehensive monitoring system for production deployment
 */

import { useCallback, useEffect, useState } from 'react';
import { usePerformanceMonitor } from '../../services/performance/performanceMonitor';

interface ProductionMetrics {
  // Core Performance Metrics
  pageLoadTime: number;
  firstContentfulPaint: number;
  largestContentfulPaint: number;
  cumulativeLayoutShift: number;
  firstInputDelay: number;
  
  // Application-Specific Metrics
  toolSwitchTime: number;
  focusModeEngagement: number;
  cognitiveLoadAverage: number;
  workflowCompletion: number;
  
  // Infrastructure Metrics
  apiResponseTime: number;
  errorRate: number;
  memoryUsage: number;
  bundleSize: number;
  
  // Executive Function Metrics
  contextSwitchFrequency: number;
  sessionDuration: number;
  taskCompletionRate: number;
  userSatisfactionScore: number;
}

interface PerformanceAlert {
  id: string;
  type: 'error' | 'warning' | 'info';
  metric: keyof ProductionMetrics;
  value: number;
  threshold: number;
  message: string;
  timestamp: number;
  resolved?: boolean;
}

interface MonitoringConfig {
  enabled: boolean;
  reportingInterval: number; // milliseconds
  alertThresholds: Partial<ProductionMetrics>;
  constitutionalCompliance: {
    security: number;    // <1s per constitution
    productivity: number; // <2s per constitution
    mtg: number;         // <3s per constitution
    infrastructure: number; // <5s per constitution
  };
}

const DEFAULT_CONFIG: MonitoringConfig = {
  enabled: true,
  reportingInterval: 30000, // 30 seconds
  alertThresholds: {
    pageLoadTime: 3000,
    firstContentfulPaint: 1800,
    largestContentfulPaint: 2500,
    cumulativeLayoutShift: 0.1,
    firstInputDelay: 100,
    toolSwitchTime: 500,
    apiResponseTime: 1000,
    errorRate: 0.05,
    cognitiveLoadAverage: 80,
  },
  constitutionalCompliance: {
    security: 1000,      // 1s
    productivity: 2000,  // 2s  
    mtg: 3000,          // 3s
    infrastructure: 5000 // 5s
  }
};

export function ProductionMonitor() {
  const { getCurrentMetrics } = usePerformanceMonitor();
  
  const [isEnabled, setIsEnabled] = useState(false);
  const [config, setConfig] = useState<MonitoringConfig>(DEFAULT_CONFIG);
  const [currentMetrics, setCurrentMetrics] = useState<Partial<ProductionMetrics>>({});
  const [alerts, setAlerts] = useState<PerformanceAlert[]>([]);
  const [historicalData, setHistoricalData] = useState<Array<{ timestamp: number; metrics: Partial<ProductionMetrics> }>>([]);
  const [showDetails, setShowDetails] = useState(false);

  // Web Vitals Collection
  const collectWebVitals = useCallback(() => {
    if (typeof window === 'undefined') return;

    // Performance Observer for Web Vitals
    if ('PerformanceObserver' in window) {
      // Largest Contentful Paint
      const lcpObserver = new PerformanceObserver((list) => {
        const entries = list.getEntries();
        const lastEntry = entries[entries.length - 1] as any;
        if (lastEntry) {
          setCurrentMetrics(prev => ({ 
            ...prev, 
            largestContentfulPaint: lastEntry.startTime 
          }));
        }
      });
      
      try {
        lcpObserver.observe({ entryTypes: ['largest-contentful-paint'] });
      } catch (e) {
        console.warn('LCP observer not supported');
      }

      // First Input Delay
      const fidObserver = new PerformanceObserver((list) => {
        const entries = list.getEntries();
        entries.forEach((entry: any) => {
          setCurrentMetrics(prev => ({ 
            ...prev, 
            firstInputDelay: entry.processingStart - entry.startTime 
          }));
        });
      });
      
      try {
        fidObserver.observe({ entryTypes: ['first-input'] });
      } catch (e) {
        console.warn('FID observer not supported');
      }

      // Layout Shift
      const clsObserver = new PerformanceObserver((list) => {
        let clsValue = 0;
        const entries = list.getEntries();
        entries.forEach((entry: any) => {
          if (!entry.hadRecentInput) {
            clsValue += entry.value;
          }
        });
        setCurrentMetrics(prev => ({ 
          ...prev, 
          cumulativeLayoutShift: clsValue 
        }));
      });
      
      try {
        clsObserver.observe({ entryTypes: ['layout-shift'] });
      } catch (e) {
        console.warn('CLS observer not supported');
      }
    }

    // Navigation Timing API
    if ('performance' in window && window.performance.timing) {
      const timing = window.performance.timing;
      const pageLoadTime = timing.loadEventEnd - timing.navigationStart;
      
      setCurrentMetrics(prev => ({
        ...prev,
        pageLoadTime: pageLoadTime,
        firstContentfulPaint: timing.responseStart - timing.navigationStart
      }));
    }

    // Memory usage (if available)
    if ('memory' in (performance as any)) {
      const memory = (performance as any).memory;
      setCurrentMetrics(prev => ({
        ...prev,
        memoryUsage: memory.usedJSHeapSize / memory.totalJSHeapSize
      }));
    }
  }, []);

  // Application-specific metrics collection
  const collectAppMetrics = useCallback(() => {
    const perfMetrics = getCurrentMetrics();
    
    if (perfMetrics) {
      setCurrentMetrics(prev => ({
        ...prev,
        cognitiveLoadAverage: perfMetrics.cognitiveLoad || 0,
        toolSwitchTime: perfMetrics.averageResponseTime || 0,
        apiResponseTime: perfMetrics.apiLatency || 0,
        errorRate: perfMetrics.errorRate || 0
      }));
    }

    // Collect bundle size info with constitutional compliance checking
    if (typeof window !== 'undefined' && 'navigator' in window) {
      // Estimate bundle size from resource timing
      const resources = performance.getEntriesByType('resource');
      const jsResources = resources.filter(r => r.name.endsWith('.js'));
      const totalSize = jsResources.reduce((sum, r: any) => sum + (r.transferSize || 0), 0);
      
      // Constitutional bundle size thresholds (bytes)
      const BUNDLE_THRESHOLDS = {
        maxMainBundle: 2 * 1024 * 1024,    // 2MB constitutional requirement
        maxTotalSize: 5 * 1024 * 1024,     // 5MB platform scalability
      };
      
      // Check for constitutional compliance
      const bundleCompliance = totalSize <= BUNDLE_THRESHOLDS.maxTotalSize;
      
      setCurrentMetrics(prev => ({
        ...prev,
        bundleSize: totalSize,
        bundleCompliance
      }));
    }
  }, [getCurrentMetrics]);

  // Alert generation
  const checkThresholds = useCallback((metrics: Partial<ProductionMetrics>) => {
    const newAlerts: PerformanceAlert[] = [];

    Object.entries(config.alertThresholds).forEach(([key, threshold]) => {
      const metricKey = key as keyof ProductionMetrics;
      const value = metrics[metricKey];
      
      if (typeof value === 'number' && typeof threshold === 'number') {
        if (value > threshold) {
          const alertId = `${metricKey}-${Date.now()}`;
          const severity = value > threshold * 1.5 ? 'error' : 'warning';
          
          newAlerts.push({
            id: alertId,
            type: severity,
            metric: metricKey,
            value,
            threshold,
            message: `${metricKey} (${Math.round(value)}) exceeded threshold (${threshold})`,
            timestamp: Date.now()
          });
        }
      }
    });

    // Constitutional compliance checks
    Object.entries(config.constitutionalCompliance).forEach(([domain, threshold]) => {
      const domainResponseTime = metrics.apiResponseTime || 0;
      
      if (domainResponseTime > threshold) {
        newAlerts.push({
          id: `constitutional-${domain}-${Date.now()}`,
          type: 'error',
          metric: 'apiResponseTime',
          value: domainResponseTime,
          threshold,
          message: `Constitutional violation: ${domain} domain response time (${Math.round(domainResponseTime)}ms) exceeds requirement (${threshold}ms)`,
          timestamp: Date.now()
        });
      }
    });

    if (newAlerts.length > 0) {
      setAlerts(prev => [...newAlerts, ...prev].slice(0, 50)); // Keep last 50 alerts
    }
  }, [config]);

  // Main monitoring loop
  useEffect(() => {
    if (!isEnabled) return;

    const interval = setInterval(() => {
      collectWebVitals();
      collectAppMetrics();
      
      // Store historical data
      setHistoricalData(prev => {
        const newEntry = { timestamp: Date.now(), metrics: currentMetrics };
        return [newEntry, ...prev.slice(0, 99)]; // Keep last 100 entries
      });
      
      // Check thresholds
      checkThresholds(currentMetrics);
    }, config.reportingInterval);

    // Initial collection
    collectWebVitals();
    collectAppMetrics();

    return () => clearInterval(interval);
  }, [isEnabled, config.reportingInterval, currentMetrics, collectWebVitals, collectAppMetrics, checkThresholds]);

  // Performance score calculation
  const calculatePerformanceScore = useCallback((): number => {
    const weights = {
      pageLoadTime: 0.2,
      firstContentfulPaint: 0.15,
      largestContentfulPaint: 0.15,
      cumulativeLayoutShift: 0.1,
      firstInputDelay: 0.1,
      toolSwitchTime: 0.15,
      cognitiveLoadAverage: 0.1,
      errorRate: 0.05
    };

    let totalScore = 0;
    let totalWeight = 0;

    Object.entries(weights).forEach(([metric, weight]) => {
      const value = currentMetrics[metric as keyof ProductionMetrics];
      if (typeof value === 'number') {
        const threshold = config.alertThresholds[metric as keyof ProductionMetrics] || 1000;
        const score = Math.max(0, 100 - (value / threshold) * 100);
        totalScore += score * weight;
        totalWeight += weight;
      }
    });

    return totalWeight > 0 ? Math.round(totalScore / totalWeight) : 0;
  }, [currentMetrics, config.alertThresholds]);

  const dismissAlert = (alertId: string) => {
    setAlerts(prev => prev.map(alert => 
      alert.id === alertId ? { ...alert, resolved: true } : alert
    ));
  };

  const exportMetrics = () => {
    const data = {
      currentMetrics,
      alerts: alerts.filter(a => !a.resolved),
      historicalData: historicalData.slice(0, 20), // Last 20 entries
      config,
      performanceScore: calculatePerformanceScore(),
      timestamp: new Date().toISOString()
    };

    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `jane-performance-report-${new Date().toISOString().split('T')[0]}.json`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  const performanceScore = calculatePerformanceScore();
  const activeAlerts = alerts.filter(a => !a.resolved);
  const criticalAlerts = activeAlerts.filter(a => a.type === 'error');

  if (!isEnabled) {
    return (
      <div className="production-monitor p-4 bg-gray-50 dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700">
        <div className="flex items-center justify-between">
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
            Production Monitor
          </h3>
          <button
            onClick={() => setIsEnabled(true)}
            className="px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 transition-colors"
          >
            Enable Monitoring
          </button>
        </div>
        <p className="text-sm text-gray-600 dark:text-gray-400 mt-2">
          Performance monitoring is currently disabled
        </p>
      </div>
    );
  }

  return (
    <div className="production-monitor p-4 bg-white dark:bg-gray-900 rounded-lg border border-gray-200 dark:border-gray-700">
      {/* Header */}
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-3">
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
            Production Monitor
          </h3>
          <div className={`w-3 h-3 rounded-full ${
            performanceScore >= 90 ? 'bg-green-500' :
            performanceScore >= 70 ? 'bg-yellow-500' : 'bg-red-500'
          }`} title={`Performance Score: ${performanceScore}`} />
        </div>
        <div className="flex items-center gap-2">
          <button
            onClick={() => setShowDetails(!showDetails)}
            className="px-3 py-1 text-sm border border-gray-300 dark:border-gray-600 rounded hover:bg-gray-50 dark:hover:bg-gray-800"
          >
            {showDetails ? 'Hide' : 'Details'}
          </button>
          <button
            onClick={exportMetrics}
            className="px-3 py-1 text-sm bg-blue-600 text-white rounded hover:bg-blue-700 transition-colors"
          >
            Export
          </button>
          <button
            onClick={() => setIsEnabled(false)}
            className="px-3 py-1 text-sm bg-red-600 text-white rounded hover:bg-red-700 transition-colors"
          >
            Stop
          </button>
        </div>
      </div>

      {/* Performance Score */}
      <div className="mb-4 p-4 bg-gray-50 dark:bg-gray-800 rounded-lg">
        <div className="flex items-center justify-between mb-2">
          <span className="text-sm font-medium text-gray-700 dark:text-gray-300">
            Overall Performance Score
          </span>
          <span className={`text-lg font-bold ${
            performanceScore >= 90 ? 'text-green-600 dark:text-green-400' :
            performanceScore >= 70 ? 'text-yellow-600 dark:text-yellow-400' : 
            'text-red-600 dark:text-red-400'
          }`}>
            {performanceScore}/100
          </span>
        </div>
        <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
          <div
            className={`h-2 rounded-full transition-all duration-500 ${
              performanceScore >= 90 ? 'bg-green-500' :
              performanceScore >= 70 ? 'bg-yellow-500' : 'bg-red-500'
            }`}
            style={{ width: `${performanceScore}%` }}
          />
        </div>
      </div>

      {/* Active Alerts */}
      {activeAlerts.length > 0 && (
        <div className="mb-4">
          <h4 className="text-sm font-medium text-gray-900 dark:text-white mb-2">
            Active Alerts ({activeAlerts.length})
            {criticalAlerts.length > 0 && (
              <span className="ml-2 px-2 py-1 text-xs bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-300 rounded-full">
                {criticalAlerts.length} Critical
              </span>
            )}
          </h4>
          <div className="space-y-2 max-h-40 overflow-y-auto">
            {activeAlerts.slice(0, 5).map(alert => (
              <div
                key={alert.id}
                className={`p-3 rounded border ${
                  alert.type === 'error' 
                    ? 'bg-red-50 border-red-200 dark:bg-red-900/20 dark:border-red-700'
                    : 'bg-yellow-50 border-yellow-200 dark:bg-yellow-900/20 dark:border-yellow-700'
                }`}
              >
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <p className={`text-sm font-medium ${
                      alert.type === 'error' 
                        ? 'text-red-800 dark:text-red-200'
                        : 'text-yellow-800 dark:text-yellow-200'
                    }`}>
                      {alert.message}
                    </p>
                    <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">
                      {new Date(alert.timestamp).toLocaleTimeString()}
                    </p>
                  </div>
                  <button
                    onClick={() => dismissAlert(alert.id)}
                    className="ml-2 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300"
                  >
                    ×
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Key Metrics */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4">
        {[
          { key: 'pageLoadTime', label: 'Page Load', unit: 'ms' },
          { key: 'toolSwitchTime', label: 'Tool Switch', unit: 'ms' },
          { key: 'cognitiveLoadAverage', label: 'Cognitive Load', unit: '%' },
          { key: 'errorRate', label: 'Error Rate', unit: '%' }
        ].map(({ key, label, unit }) => {
          const value = currentMetrics[key as keyof ProductionMetrics];
          const threshold = config.alertThresholds[key as keyof ProductionMetrics];
          
          return (
            <div key={key} className="text-center p-3 bg-gray-50 dark:bg-gray-800 rounded">
              <div className={`text-lg font-semibold ${
                value && threshold && value > threshold 
                  ? 'text-red-600 dark:text-red-400' 
                  : 'text-gray-900 dark:text-white'
              }`}>
                {typeof value === 'number' ? Math.round(value) : '—'}{unit}
              </div>
              <div className="text-xs text-gray-500 dark:text-gray-400">{label}</div>
            </div>
          );
        })}
      </div>

      {/* Constitutional Compliance */}
      <div className="mb-4 p-4 bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-700 rounded-lg">
        <h4 className="text-sm font-medium text-blue-800 dark:text-blue-200 mb-2">
          Constitutional Compliance Status
        </h4>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-3 text-xs">
          {Object.entries(config.constitutionalCompliance).map(([domain, threshold]) => {
            const responseTime = currentMetrics.apiResponseTime || 0;
            const compliant = responseTime <= threshold;
            
            return (
              <div key={domain} className="flex items-center justify-between">
                <span className="capitalize text-blue-700 dark:text-blue-300">{domain}:</span>
                <span className={`font-medium ${
                  compliant 
                    ? 'text-green-600 dark:text-green-400' 
                    : 'text-red-600 dark:text-red-400'
                }`}>
                  {compliant ? '✓' : '⚠'} {threshold}ms
                </span>
              </div>
            );
          })}
        </div>
      </div>

      {/* Detailed Metrics */}
      {showDetails && (
        <div className="border-t border-gray-200 dark:border-gray-600 pt-4">
          <h4 className="text-sm font-medium text-gray-900 dark:text-white mb-3">
            Detailed Metrics
          </h4>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
            {Object.entries(currentMetrics).map(([key, value]) => (
              <div key={key} className="flex justify-between">
                <span className="text-gray-600 dark:text-gray-400 capitalize">
                  {key.replace(/([A-Z])/g, ' $1').toLowerCase()}:
                </span>
                <span className="font-medium text-gray-900 dark:text-white">
                  {typeof value === 'number' ? Math.round(value) : String(value)}
                </span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Monitoring Status */}
      <div className="mt-4 pt-4 border-t border-gray-200 dark:border-gray-600 text-xs text-gray-500 dark:text-gray-400">
        <div className="flex justify-between">
          <span>Update interval: {config.reportingInterval / 1000}s</span>
          <span>Data points: {historicalData.length}/100</span>
          <span>Last update: {new Date().toLocaleTimeString()}</span>
        </div>
      </div>
    </div>
  );
}