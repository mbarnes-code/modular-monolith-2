/**
 * Performance Monitoring Dashboard Component
 * Constitutional compliance tracking for 37-tool mental prosthetic platform
 */

import { useEffect, useState } from 'react';
import { usePerformanceMonitor } from '../../services/performance/performanceMonitor';
import { PerformanceMetrics } from '../../types/performance';

interface PerformanceDashboardProps {
  className?: string;
  compact?: boolean;
}

export function PerformanceDashboard({ className = '', compact = false }: PerformanceDashboardProps) {
  const { getMetrics, getComplianceReport } = usePerformanceMonitor();
  const [metrics, setMetrics] = useState<PerformanceMetrics[]>([]);
  const [complianceReport, setComplianceReport] = useState<Record<string, any>>({});
  const [refreshInterval, setRefreshInterval] = useState<NodeJS.Timeout | null>(null);

  // Refresh data periodically
  useEffect(() => {
    const updateData = () => {
      setMetrics(getMetrics());
      setComplianceReport(getComplianceReport());
    };

    updateData();
    
    const interval = setInterval(updateData, 5000); // Update every 5 seconds
    setRefreshInterval(interval);

    return () => {
      if (interval) clearInterval(interval);
    };
  }, [getMetrics, getComplianceReport]);

  // Get recent violations
  const recentViolations = metrics
    .filter(m => !m.compliant)
    .slice(-10)
    .reverse();

  // Calculate overall compliance
  const overallCompliance = Object.values(complianceReport)
    .reduce((acc, domain: any) => acc + (domain.percentage || 0), 0) / 
    Math.max(Object.keys(complianceReport).length, 1);

  if (compact) {
    return (
      <div className={`performance-dashboard-compact ${className}`}>
        <div className="flex items-center gap-4 p-3 bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700">
          {/* Overall compliance indicator */}
          <div className="flex items-center gap-2">
            <div className={`w-3 h-3 rounded-full ${
              overallCompliance >= 95 ? 'bg-green-500' :
              overallCompliance >= 90 ? 'bg-yellow-500' : 'bg-red-500'
            }`} />
            <span className="text-sm font-medium text-gray-700 dark:text-gray-300">
              {overallCompliance.toFixed(1)}% compliant
            </span>
          </div>

          {/* Domain status indicators */}
          <div className="flex gap-2">
            {Object.entries(complianceReport).map(([domain, data]: [string, any]) => (
              <div key={domain} className="flex items-center gap-1">
                <span className="text-xs text-gray-500 capitalize">{domain}:</span>
                <span className={`text-xs font-medium ${
                  data.percentage >= 95 ? 'text-green-600' :
                  data.percentage >= 90 ? 'text-yellow-600' : 'text-red-600'
                }`}>
                  {data.percentage}%
                </span>
              </div>
            ))}
          </div>

          {/* Violations indicator */}
          {recentViolations.length > 0 && (
            <div className="flex items-center gap-1 text-red-600">
              <span className="text-sm">⚠️</span>
              <span className="text-xs">{recentViolations.length} issues</span>
            </div>
          )}
        </div>
      </div>
    );
  }

  return (
    <div className={`performance-dashboard ${className}`}>
      <div className="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 p-6">
        {/* Header */}
        <div className="flex items-center justify-between mb-6">
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
            Performance Monitor
          </h3>
          <div className="flex items-center gap-2">
            <div className={`w-2 h-2 rounded-full ${
              overallCompliance >= 95 ? 'bg-green-500' :
              overallCompliance >= 90 ? 'bg-yellow-500' : 'bg-red-500'
            } animate-pulse`} />
            <span className="text-sm text-gray-500">Live</span>
          </div>
        </div>

        {/* Overall compliance */}
        <div className="mb-6">
          <div className="flex items-center justify-between mb-2">
            <span className="text-sm font-medium text-gray-700 dark:text-gray-300">
              Overall Compliance
            </span>
            <span className="text-sm font-bold text-gray-900 dark:text-white">
              {overallCompliance.toFixed(1)}%
            </span>
          </div>
          <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
            <div
              className={`h-2 rounded-full transition-all duration-500 ${
                overallCompliance >= 95 ? 'bg-green-500' :
                overallCompliance >= 90 ? 'bg-yellow-500' : 'bg-red-500'
              }`}
              style={{ width: `${overallCompliance}%` }}
            />
          </div>
        </div>

        {/* Domain-specific compliance */}
        <div className="mb-6">
          <h4 className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-3">
            Domain Performance
          </h4>
          <div className="grid grid-cols-2 gap-4">
            {Object.entries(complianceReport).map(([domain, data]: [string, any]) => (
              <div key={domain} className="p-3 bg-gray-50 dark:bg-gray-700 rounded-lg">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-sm font-medium capitalize text-gray-700 dark:text-gray-300">
                    {domain}
                  </span>
                  <span className={`text-sm font-bold ${
                    data.percentage >= 95 ? 'text-green-600' :
                    data.percentage >= 90 ? 'text-yellow-600' : 'text-red-600'
                  }`}>
                    {data.percentage}%
                  </span>
                </div>
                <div className="w-full bg-gray-200 dark:bg-gray-600 rounded-full h-1">
                  <div
                    className={`h-1 rounded-full transition-all duration-500 ${
                      data.percentage >= 95 ? 'bg-green-500' :
                      data.percentage >= 90 ? 'bg-yellow-500' : 'bg-red-500'
                    }`}
                    style={{ width: `${data.percentage}%` }}
                  />
                </div>
                <div className="text-xs text-gray-500 mt-1">
                  {data.compliant}/{data.total} operations
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Recent violations */}
        {recentViolations.length > 0 && (
          <div>
            <h4 className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-3">
              Recent Performance Issues
            </h4>
            <div className="space-y-2 max-h-48 overflow-y-auto">
              {recentViolations.map((violation, index) => (
                <div key={index} className="flex items-center gap-3 p-2 bg-red-50 dark:bg-red-900/20 rounded border-l-2 border-red-500">
                  <span className="text-red-500">⚠️</span>
                  <div className="flex-1 min-w-0">
                    <div className="text-sm font-medium text-red-800 dark:text-red-300">
                      {violation.operation}
                    </div>
                    <div className="text-xs text-red-600 dark:text-red-400">
                      {violation.duration}ms (threshold: {violation.threshold}ms) • {violation.domain}
                    </div>
                  </div>
                  <div className="text-xs text-gray-500">
                    {new Date(violation.timestamp).toLocaleTimeString()}
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Performance thresholds reference */}
        <div className="mt-6 pt-4 border-t border-gray-200 dark:border-gray-700">
          <h4 className="text-xs font-medium text-gray-500 mb-2">Constitutional Thresholds</h4>
          <div className="grid grid-cols-2 gap-2 text-xs text-gray-500">
            <div>Security: &lt;1s (Critical)</div>
            <div>Productivity: &lt;2s (High)</div>
            <div>MTG: &lt;3s (Medium)</div>
            <div>Infrastructure: &lt;5s (Low)</div>
            <div>UI Interaction: &lt;200ms (Executive Function)</div>
            <div>Navigation: &lt;300ms (Context Switching)</div>
          </div>
        </div>
      </div>
    </div>
  );
}