'use client';

import React, { useEffect, useState } from 'react';
import { Alert, AlertDescription } from '../ui/alert';
import { Badge } from '../ui/badge';
import { Button } from '../ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '../ui/card';

interface DomainMetrics {
  domain: string;
  responseTime: number;
  threshold: number;
  status: 'healthy' | 'warning' | 'critical';
  lastUpdated: string;
  averageResponseTime: number;
  totalRequests: number;
  errorRate: number;
  successRate: number;
}

interface DomainDashboardProps {
  onRefresh?: () => void;
  showAlerts?: boolean;
}

const DOMAIN_THRESHOLDS = {
  Security: 1000, // <1s
  Productivity: 2000, // <2s
  MTG: 3000, // <3s
  Infrastructure: 5000, // <5s
};

const DOMAIN_COLORS = {
  Security: 'text-red-600 bg-red-50 border-red-200',
  Productivity: 'text-blue-600 bg-blue-50 border-blue-200',
  MTG: 'text-purple-600 bg-purple-50 border-purple-200',
  Infrastructure: 'text-green-600 bg-green-50 border-green-200',
};

export const DomainDashboard: React.FC<DomainDashboardProps> = ({
  onRefresh,
  showAlerts = true,
}) => {
  const [metrics, setMetrics] = useState<DomainMetrics[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [lastRefresh, setLastRefresh] = useState<Date>(new Date());

  // Mock data for development - replace with actual API calls
  const mockMetrics: DomainMetrics[] = [
    {
      domain: 'Security',
      responseTime: 850,
      threshold: DOMAIN_THRESHOLDS.Security,
      status: 'healthy',
      lastUpdated: new Date().toISOString(),
      averageResponseTime: 725,
      totalRequests: 1247,
      errorRate: 0.8,
      successRate: 99.2,
    },
    {
      domain: 'Productivity',
      responseTime: 1650,
      threshold: DOMAIN_THRESHOLDS.Productivity,
      status: 'healthy',
      lastUpdated: new Date().toISOString(),
      averageResponseTime: 1425,
      totalRequests: 3891,
      errorRate: 1.2,
      successRate: 98.8,
    },
    {
      domain: 'MTG',
      responseTime: 2200,
      threshold: DOMAIN_THRESHOLDS.MTG,
      status: 'healthy',
      lastUpdated: new Date().toISOString(),
      averageResponseTime: 2050,
      totalRequests: 567,
      errorRate: 0.5,
      successRate: 99.5,
    },
    {
      domain: 'Infrastructure',
      responseTime: 4100,
      threshold: DOMAIN_THRESHOLDS.Infrastructure,
      status: 'healthy',
      lastUpdated: new Date().toISOString(),
      averageResponseTime: 3850,
      totalRequests: 892,
      errorRate: 2.1,
      successRate: 97.9,
    },
  ];

  const fetchMetrics = async () => {
    try {
      setLoading(true);
      setError(null);
      
      // TODO: Replace with actual API call
      // const response = await fetch('/api/performance/domains');
      // const data = await response.json();
      
      // Simulate API delay
      // eslint-disable-next-line @typescript-eslint/no-explicit-any
      await new Promise(resolve => (globalThis as any).setTimeout(resolve, 500));
      
      setMetrics(mockMetrics);
      setLastRefresh(new Date());
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch metrics');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchMetrics();
    
    // Set up auto-refresh every 30 seconds
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    const interval = (globalThis as any).setInterval(fetchMetrics, 30000);
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    return () => (globalThis as any).clearInterval(interval);
  }, []);

  const handleRefresh = () => {
    fetchMetrics();
    onRefresh?.();
  };

  const getStatusIcon = (status: DomainMetrics['status']) => {
    switch (status) {
      case 'healthy':
        return <span className="w-4 h-4 text-green-500">✓</span>;
      case 'warning':
        return <span className="w-4 h-4 text-yellow-500">⚠</span>;
      case 'critical':
        return <span className="w-4 h-4 text-red-500">⚠</span>;
      default:
        return <span className="w-4 h-4 text-gray-500">⏱</span>;
    }
  };

  const getStatusBadge = (status: DomainMetrics['status']) => {
    const variants = {
      healthy: 'bg-green-100 text-green-800 border-green-200',
      warning: 'bg-yellow-100 text-yellow-800 border-yellow-200',
      critical: 'bg-red-100 text-red-800 border-red-200',
    };
    
    return (
      <Badge 
        variant="outline" 
        className={variants[status]}
      >
        {status.charAt(0).toUpperCase() + status.slice(1)}
      </Badge>
    );
  };

  const formatResponseTime = (ms: number) => {
    if (ms < 1000) {
      return `${ms}ms`;
    }
    return `${(ms / 1000).toFixed(2)}s`;
  };

  const criticalAlerts = metrics.filter(m => m.status === 'critical');
  const warningAlerts = metrics.filter(m => m.status === 'warning');

  if (loading && metrics.length === 0) {
    return (
      <div className="flex items-center justify-center p-8">
        <span className="animate-spin mr-2">⟳</span>
        <span>Loading domain performance metrics...</span>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold tracking-tight">Domain Performance Dashboard</h2>
          <p className="text-muted-foreground">
            Constitutional performance requirements monitoring across all domains
          </p>
        </div>
        <div className="flex items-center space-x-4">
          <span className="text-sm text-muted-foreground">
            Last updated: {lastRefresh.toLocaleTimeString()}
          </span>
          <Button
            onClick={handleRefresh}
            disabled={loading}
            variant="outline"
            size="sm"
          >
            <span className={`mr-2 ${loading ? 'animate-spin' : ''}`}>⟳</span>
            Refresh
          </Button>
        </div>
      </div>

      {/* Alerts */}
      {showAlerts && (criticalAlerts.length > 0 || warningAlerts.length > 0) && (
        <div className="space-y-2">
          {criticalAlerts.map((metric) => (
            <Alert key={`critical-${metric.domain}`} variant="destructive">
              <span className="h-4 w-4">⚠</span>
              <AlertDescription>
                <strong>{metric.domain} Domain</strong> is experiencing critical performance issues. 
                Response time: {formatResponseTime(metric.responseTime)} (threshold: {formatResponseTime(metric.threshold)})
              </AlertDescription>
            </Alert>
          ))}
          {warningAlerts.map((metric) => (
            <Alert key={`warning-${metric.domain}`} className="border-yellow-200 bg-yellow-50">
              <span className="h-4 w-4 text-yellow-600">⚠</span>
              <AlertDescription className="text-yellow-800">
                <strong>{metric.domain} Domain</strong> performance is above normal. 
                Response time: {formatResponseTime(metric.responseTime)} (threshold: {formatResponseTime(metric.threshold)})
              </AlertDescription>
            </Alert>
          ))}
        </div>
      )}

      {/* Error State */}
      {error && (
        <Alert variant="destructive">
          <span className="h-4 w-4">⚠</span>
          <AlertDescription>
            Error loading performance metrics: {error}
          </AlertDescription>
        </Alert>
      )}

      {/* Domain Metrics Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {metrics.map((metric) => (
          <Card key={metric.domain} className={`${DOMAIN_COLORS[metric.domain as keyof typeof DOMAIN_COLORS]} border-2`}>
            <CardHeader className="pb-3">
              <CardTitle className="flex items-center justify-between text-lg">
                <span>{metric.domain}</span>
                {getStatusIcon(metric.status)}
              </CardTitle>
              <div className="flex justify-between items-center">
                {getStatusBadge(metric.status)}
                <span className="text-sm text-muted-foreground">
                  Threshold: {formatResponseTime(metric.threshold)}
                </span>
              </div>
            </CardHeader>
            <CardContent className="space-y-4">
              {/* Current Response Time */}
              <div>
                <div className="flex justify-between items-baseline">
                  <span className="text-sm font-medium">Current Response</span>
                  <span className={`text-lg font-bold ${
                    metric.responseTime > metric.threshold ? 'text-red-600' : 'text-green-600'
                  }`}>
                    {formatResponseTime(metric.responseTime)}
                  </span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2 mt-1">
                  <div
                    className={`h-2 rounded-full transition-all duration-300 ${
                      metric.responseTime > metric.threshold ? 'bg-red-500' : 'bg-green-500'
                    }`}
                    style={{
                      width: `${Math.min((metric.responseTime / metric.threshold) * 100, 100)}%`
                    }}
                  />
                </div>
              </div>

              {/* Statistics */}
              <div className="grid grid-cols-2 gap-2 text-sm">
                <div>
                  <span className="text-muted-foreground">Avg Response</span>
                  <div className="font-medium">{formatResponseTime(metric.averageResponseTime)}</div>
                </div>
                <div>
                  <span className="text-muted-foreground">Success Rate</span>
                  <div className="font-medium">{metric.successRate}%</div>
                </div>
                <div>
                  <span className="text-muted-foreground">Total Requests</span>
                  <div className="font-medium">{metric.totalRequests.toLocaleString()}</div>
                </div>
                <div>
                  <span className="text-muted-foreground">Error Rate</span>
                  <div className="font-medium">{metric.errorRate}%</div>
                </div>
              </div>

              {/* Trend Indicator */}
              <div className="flex items-center justify-between text-sm">
                <span className="text-muted-foreground">Trend</span>
                <div className="flex items-center">
                  <span className="w-3 h-3 text-green-500 mr-1">↗</span>
                  <span className="text-green-600 text-xs">Improving</span>
                </div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Summary Statistics */}
      <Card>
        <CardHeader>
          <CardTitle>Overall Performance Summary</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="text-center">
              <div className="text-2xl font-bold text-green-600">
                {metrics.filter(m => m.status === 'healthy').length}
              </div>
              <div className="text-sm text-muted-foreground">Healthy Domains</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-yellow-600">
                {metrics.filter(m => m.status === 'warning').length}
              </div>
              <div className="text-sm text-muted-foreground">Warning Domains</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-red-600">
                {metrics.filter(m => m.status === 'critical').length}
              </div>
              <div className="text-sm text-muted-foreground">Critical Domains</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold">
                {metrics.reduce((acc, m) => acc + m.totalRequests, 0).toLocaleString()}
              </div>
              <div className="text-sm text-muted-foreground">Total Requests</div>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default DomainDashboard;