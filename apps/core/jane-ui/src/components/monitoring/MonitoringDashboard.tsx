/**
 * Production Monitoring Dashboard
 * Real-time health and performance monitoring for the 37-tool platform
 */

import {
    Activity,
    AlertTriangle,
    CheckCircle,
    Download,
    Eye,
    EyeOff,
    Gauge,
    Heart,
    Monitor,
    Package,
    RefreshCw,
    Server,
    TrendingUp,
    Zap
} from 'lucide-react';
import { useEffect, useState } from 'react';
import { useProductionMonitor } from '../../services/monitoring/ProductionMonitor';

interface MonitoringDashboardProps {
  className?: string;
  autoRefresh?: boolean;
  refreshInterval?: number;
}

export function MonitoringDashboard({ 
  className = '', 
  autoRefresh = true, 
  refreshInterval = 30000 
}: MonitoringDashboardProps) {
  const {
    metrics,
    alerts,
    isHealthy,
    healthScore,
    getMetricHistory,
    exportMetrics
  } = useProductionMonitor();

  const [selectedMetric, setSelectedMetric] = useState<string>('overview');
  const [timeRange, setTimeRange] = useState<number>(3600000); // 1 hour
  const [isMinimized, setIsMinimized] = useState(false);
  const [showDetails, setShowDetails] = useState(false);

  // Real-time metric history for charts
  const [metricChartData, setMetricChartData] = useState<Record<string, any[]>>({});

  useEffect(() => {
    if (autoRefresh) {
      const interval = setInterval(() => {
        // Update chart data
        setMetricChartData({
          responseTime: getMetricHistory('responseTime', timeRange),
          errorRate: getMetricHistory('errorRate', timeRange),
          cognitiveLoad: getMetricHistory('cognitiveLoad', timeRange),
          healthScore: getMetricHistory('healthScore', timeRange)
        });
      }, refreshInterval);

      return () => clearInterval(interval);
    }
  }, [autoRefresh, refreshInterval, timeRange, getMetricHistory]);

  const formatMetricValue = (value: number, type: string): string => {
    switch (type) {
      case 'ms':
        return `${Math.round(value)}ms`;
      case 'mb':
        return `${Math.round(value / 1024 / 1024 * 100) / 100}MB`;
      case 'kb':
        return `${Math.round(value / 1024)}KB`;
      case 'percent':
        return `${Math.round(value)}%`;
      case 'rate':
        return `${(value * 100).toFixed(2)}%`;
      default:
        return Math.round(value).toString();
    }
  };

  const getMetricStatus = (actual: number, threshold: number, type: 'lower' | 'higher' = 'lower') => {
    const isGood = type === 'lower' ? actual <= threshold : actual >= threshold;
    return {
      status: isGood ? 'good' : actual > threshold * 1.5 ? 'critical' : 'warning',
      color: isGood ? 'text-green-600' : actual > threshold * 1.5 ? 'text-red-600' : 'text-yellow-600',
      bgColor: isGood ? 'bg-green-50' : actual > threshold * 1.5 ? 'bg-red-50' : 'bg-yellow-50',
      borderColor: isGood ? 'border-green-200' : actual > threshold * 1.5 ? 'border-red-200' : 'border-yellow-200'
    };
  };

  const unacknowledgedAlerts = alerts.filter(alert => !alert.resolved);
  const criticalAlerts = unacknowledgedAlerts.filter(alert => alert.type === 'critical');

  if (isMinimized) {
    return (
      <div className={`monitoring-dashboard-minimized ${className}`}>
        <div className="fixed bottom-4 left-4 z-40">
          <button
            onClick={() => setIsMinimized(false)}
            className={`flex items-center gap-2 px-3 py-2 rounded-lg shadow-lg transition-colors ${
              isHealthy 
                ? 'bg-green-100 text-green-800 border border-green-200' 
                : 'bg-red-100 text-red-800 border border-red-200'
            }`}
          >
            <Heart className={`w-4 h-4 ${isHealthy ? 'text-green-600' : 'text-red-600'}`} />
            <span className="font-semibold">{healthScore}%</span>
            {unacknowledgedAlerts.length > 0 && (
              <span className="px-2 py-1 bg-red-500 text-white rounded-full text-xs">
                {unacknowledgedAlerts.length}
              </span>
            )}
            <Eye className="w-4 h-4" />
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className={`monitoring-dashboard ${className}`}>
      <div className="fixed bottom-4 left-4 right-4 z-40 bg-white border border-gray-200 rounded-lg shadow-xl max-h-96 overflow-hidden">
        {/* Header */}
        <div className="flex items-center justify-between p-4 border-b border-gray-200 bg-gray-50">
          <div className="flex items-center gap-3">
            <Monitor className="w-5 h-5 text-blue-600" />
            <h3 className="font-semibold text-gray-900">Production Monitor</h3>
            
            {/* Health indicator */}
            <div className={`flex items-center gap-2 px-3 py-1 rounded-full ${
              isHealthy ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
            }`}>
              <Heart className={`w-4 h-4 ${isHealthy ? 'text-green-600' : 'text-red-600'}`} />
              <span className="font-semibold">{healthScore}%</span>
            </div>

            {/* Alert badge */}
            {unacknowledgedAlerts.length > 0 && (
              <div className="flex items-center gap-1">
                <AlertTriangle className={`w-4 h-4 ${
                  criticalAlerts.length > 0 ? 'text-red-500' : 'text-yellow-500'
                }`} />
                <span className={`px-2 py-1 rounded-full text-xs font-semibold ${
                  criticalAlerts.length > 0 
                    ? 'bg-red-100 text-red-800' 
                    : 'bg-yellow-100 text-yellow-800'
                }`}>
                  {unacknowledgedAlerts.length} alerts
                </span>
              </div>
            )}
          </div>

          <div className="flex items-center gap-2">
            <button
              onClick={() => setShowDetails(!showDetails)}
              className="p-1 text-gray-500 hover:text-gray-700 rounded"
              title={showDetails ? 'Hide details' : 'Show details'}
            >
              {showDetails ? <TrendingUp className="w-4 h-4" /> : <Gauge className="w-4 h-4" />}
            </button>
            
            <button
              onClick={exportMetrics}
              className="p-1 text-gray-500 hover:text-gray-700 rounded"
              title="Export metrics"
            >
              <Download className="w-4 h-4" />
            </button>
            
            <button
              onClick={() => setIsMinimized(true)}
              className="p-1 text-gray-500 hover:text-gray-700 rounded"
              title="Minimize"
            >
              <EyeOff className="w-4 h-4" />
            </button>
          </div>
        </div>

        {/* Content */}
        <div className="overflow-y-auto" style={{ maxHeight: '300px' }}>
          {!showDetails ? (
            /* Overview Mode */
            <div className="p-4">
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                {/* Response Time */}
                <div className="metric-card bg-white border border-gray-200 rounded-lg p-3">
                  <div className="flex items-center gap-2 mb-2">
                    <Zap className="w-4 h-4 text-blue-500" />
                    <span className="text-sm font-medium text-gray-700">Response Time</span>
                  </div>
                  <div className="space-y-1">
                    {Object.entries(metrics.responseTime).map(([domain, time]) => {
                      const threshold = {
                        security: 1000,
                        productivity: 2000,
                        mtg: 3000,
                        infrastructure: 5000,
                        ai: 2000
                      }[domain] || 5000;
                      
                      const status = getMetricStatus(time, threshold);
                      
                      return (
                        <div key={domain} className="flex items-center justify-between text-xs">
                          <span className="capitalize text-gray-600">{domain}</span>
                          <span className={`font-semibold ${status.color}`}>
                            {formatMetricValue(time, 'ms')}
                          </span>
                        </div>
                      );
                    })}
                  </div>
                </div>

                {/* Bundle Size */}
                <div className="metric-card bg-white border border-gray-200 rounded-lg p-3">
                  <div className="flex items-center gap-2 mb-2">
                    <Package className="w-4 h-4 text-purple-500" />
                    <span className="text-sm font-medium text-gray-700">Bundle Size</span>
                  </div>
                  <div className="space-y-1">
                    <div className="flex items-center justify-between text-xs">
                      <span className="text-gray-600">Main</span>
                      <span className={`font-semibold ${
                        metrics.bundleSize.main <= 2 * 1024 * 1024 ? 'text-green-600' : 'text-red-600'
                      }`}>
                        {formatMetricValue(metrics.bundleSize.main, 'mb')}
                      </span>
                    </div>
                    <div className="flex items-center justify-between text-xs">
                      <span className="text-gray-600">Total</span>
                      <span className={`font-semibold ${
                        metrics.bundleSize.total <= 5 * 1024 * 1024 ? 'text-green-600' : 'text-red-600'
                      }`}>
                        {formatMetricValue(metrics.bundleSize.total, 'mb')}
                      </span>
                    </div>
                    <div className="text-xs text-gray-500">
                      {formatMetricValue((metrics.bundleSize.total / (5 * 1024 * 1024)) * 100, 'percent')} of limit
                    </div>
                  </div>
                </div>

                {/* Executive Function */}
                <div className="metric-card bg-white border border-gray-200 rounded-lg p-3">
                  <div className="flex items-center gap-2 mb-2">
                    <Activity className="w-4 h-4 text-green-500" />
                    <span className="text-sm font-medium text-gray-700">Executive Function</span>
                  </div>
                  <div className="space-y-1">
                    {Object.entries(metrics.executiveFunction).map(([metric, time]) => {
                      const threshold = {
                        interaction: 200,
                        navigation: 300,
                        dataLoad: 500,
                        contextSwitch: 250
                      }[metric] || 300;
                      
                      const status = getMetricStatus(time, threshold);
                      
                      return (
                        <div key={metric} className="flex items-center justify-between text-xs">
                          <span className="capitalize text-gray-600">{metric}</span>
                          <span className={`font-semibold ${status.color}`}>
                            {formatMetricValue(time, 'ms')}
                          </span>
                        </div>
                      );
                    })}
                  </div>
                </div>

                {/* System Health */}
                <div className="metric-card bg-white border border-gray-200 rounded-lg p-3">
                  <div className="flex items-center gap-2 mb-2">
                    <Server className="w-4 h-4 text-orange-500" />
                    <span className="text-sm font-medium text-gray-700">System Health</span>
                  </div>
                  <div className="space-y-1">
                    <div className="flex items-center justify-between text-xs">
                      <span className="text-gray-600">Error Rate</span>
                      <span className={`font-semibold ${
                        metrics.errorRate <= 0.01 ? 'text-green-600' : 'text-red-600'
                      }`}>
                        {formatMetricValue(metrics.errorRate, 'rate')}
                      </span>
                    </div>
                    <div className="flex items-center justify-between text-xs">
                      <span className="text-gray-600">Cognitive Load</span>
                      <span className={`font-semibold ${
                        metrics.cognitiveLoad <= 80 ? 'text-green-600' : 'text-red-600'
                      }`}>
                        {formatMetricValue(metrics.cognitiveLoad, 'percent')}
                      </span>
                    </div>
                    <div className="flex items-center justify-between text-xs">
                      <span className="text-gray-600">Uptime</span>
                      <span className="font-semibold text-green-600">
                        {formatMetricValue(metrics.uptime, 'percent')}
                      </span>
                    </div>
                  </div>
                </div>
              </div>

              {/* Recent Alerts */}
              {unacknowledgedAlerts.length > 0 && (
                <div className="mt-4 p-3 bg-gray-50 rounded-lg">
                  <div className="flex items-center gap-2 mb-2">
                    <AlertTriangle className="w-4 h-4 text-red-500" />
                    <span className="text-sm font-medium text-gray-700">Active Alerts</span>
                    <span className="px-2 py-1 bg-red-100 text-red-800 rounded-full text-xs">
                      {criticalAlerts.length} critical
                    </span>
                  </div>
                  <div className="space-y-1 max-h-20 overflow-y-auto">
                    {unacknowledgedAlerts.slice(0, 3).map(alert => (
                      <div key={alert.id} className="text-xs text-gray-600 flex items-center gap-2">
                        <span className={`w-2 h-2 rounded-full ${
                          alert.type === 'critical' ? 'bg-red-500' : 'bg-yellow-500'
                        }`} />
                        <span className="flex-1 truncate">{alert.message}</span>
                        <span className="text-gray-400">
                          {alert.timestamp.toLocaleTimeString()}
                        </span>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          ) : (
            /* Detailed Mode */
            <div className="p-4">
              <div className="space-y-4">
                {/* Trend Charts Placeholder */}
                <div className="bg-gray-50 rounded-lg p-4">
                  <h4 className="font-medium text-gray-900 mb-3">Performance Trends</h4>
                  <div className="grid grid-cols-2 gap-4">
                    <div className="bg-white rounded border p-3">
                      <div className="text-sm font-medium text-gray-700 mb-2">Response Time Trend</div>
                      <div className="h-16 bg-gradient-to-r from-blue-100 to-blue-200 rounded flex items-end justify-between px-2">
                        {[...Array(8)].map((_, i) => (
                          <div 
                            key={i} 
                            className="bg-blue-500 w-2 rounded-t" 
                            style={{ height: `${20 + Math.random() * 40}px` }}
                          />
                        ))}
                      </div>
                    </div>
                    <div className="bg-white rounded border p-3">
                      <div className="text-sm font-medium text-gray-700 mb-2">Health Score</div>
                      <div className="h-16 bg-gradient-to-r from-green-100 to-green-200 rounded flex items-end justify-between px-2">
                        {[...Array(8)].map((_, i) => (
                          <div 
                            key={i} 
                            className="bg-green-500 w-2 rounded-t" 
                            style={{ height: `${30 + Math.random() * 30}px` }}
                          />
                        ))}
                      </div>
                    </div>
                  </div>
                </div>

                {/* Constitutional Compliance */}
                <div className="bg-gray-50 rounded-lg p-4">
                  <h4 className="font-medium text-gray-900 mb-3">Constitutional Compliance</h4>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                    <div className="flex items-center gap-3">
                      <CheckCircle className={`w-5 h-5 ${
                        metrics.bundleSize.total <= 5 * 1024 * 1024 ? 'text-green-500' : 'text-red-500'
                      }`} />
                      <div>
                        <div className="text-sm font-medium">Bundle Size Limit</div>
                        <div className="text-xs text-gray-600">
                          {formatMetricValue(metrics.bundleSize.total, 'mb')} / 5MB
                        </div>
                      </div>
                    </div>
                    <div className="flex items-center gap-3">
                      <CheckCircle className={`w-5 h-5 ${
                        Object.values(metrics.executiveFunction).every(v => v <= 200) ? 'text-green-500' : 'text-red-500'
                      }`} />
                      <div>
                        <div className="text-sm font-medium">ADHD Accommodations</div>
                        <div className="text-xs text-gray-600">
                          &lt;200ms UI interactions
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="px-4 py-2 bg-gray-50 border-t border-gray-200 text-xs text-gray-500 flex items-center justify-between">
          <div>Last updated: {metrics.lastUpdated.toLocaleTimeString()}</div>
          <div className="flex items-center gap-2">
            <RefreshCw className="w-3 h-3" />
            <span>Auto-refresh: {autoRefresh ? `${refreshInterval / 1000}s` : 'Off'}</span>
          </div>
        </div>
      </div>
    </div>
  );
}