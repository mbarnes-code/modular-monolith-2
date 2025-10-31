'use client';

import React, { useCallback, useEffect, useState } from 'react';
import { Alert, AlertDescription } from '../ui/alert';
import { Badge } from '../ui/badge';
import { Button } from '../ui/button';
import { Card, CardContent } from '../ui/card';

interface PerformanceAlert {
  id: string;
  type: 'critical' | 'warning' | 'info';
  domain: 'Security' | 'Productivity' | 'MTG' | 'Infrastructure';
  title: string;
  message: string;
  threshold: number;
  actual: number;
  timestamp: number;
  resolved: boolean;
  acknowledged: boolean;
}

interface AlertSystemProps {
  className?: string;
  onAlertAction?: (alertId: string, action: 'acknowledge' | 'resolve' | 'dismiss') => void;
  realTimeUpdates?: boolean;
}

export const AlertSystem: React.FC<AlertSystemProps> = ({
  className = '',
  onAlertAction,
  realTimeUpdates = true
}) => {
  const [alerts, setAlerts] = useState<PerformanceAlert[]>([]);
  const [filter, setFilter] = useState<'all' | 'critical' | 'warning' | 'unresolved'>('all');
  const [sortBy, setSortBy] = useState<'timestamp' | 'severity' | 'domain'>('timestamp');
  const [soundEnabled, setSoundEnabled] = useState(true);

  // Generate mock alerts for development
  const generateMockAlerts = useCallback((): PerformanceAlert[] => {
    const domains: PerformanceAlert['domain'][] = ['Security', 'Productivity', 'MTG', 'Infrastructure'];
    const alertTypes: Array<{ type: PerformanceAlert['type'], threshold: number }> = [
      { type: 'critical', threshold: 1.5 },
      { type: 'warning', threshold: 1.2 },
      { type: 'info', threshold: 1.0 }
    ];

    const mockAlerts: PerformanceAlert[] = [];
    const now = Date.now();

    // Generate some recent alerts
    for (let i = 0; i < 8; i++) {
      const domain = domains[Math.floor(Math.random() * domains.length)];
      const alertType = alertTypes[Math.floor(Math.random() * alertTypes.length)];
      const domainThresholds = {
        Security: 1000,
        Productivity: 2000,
        MTG: 3000,
        Infrastructure: 5000
      };
      
      const threshold = domainThresholds[domain];
      const actual = threshold * alertType.threshold;
      
      mockAlerts.push({
        id: `alert-${i + 1}`,
        type: alertType.type,
        domain,
        title: `${domain} Domain Performance Alert`,
        message: alertType.type === 'critical' 
          ? `Critical performance degradation detected in ${domain} domain`
          : alertType.type === 'warning'
          ? `Performance threshold exceeded in ${domain} domain`
          : `Performance monitoring alert for ${domain} domain`,
        threshold,
        actual: Math.round(actual),
        timestamp: now - (i * 15 * 60 * 1000), // alerts every 15 minutes
        resolved: Math.random() > 0.7, // 30% resolved
        acknowledged: Math.random() > 0.5 // 50% acknowledged
      });
    }

    return mockAlerts.sort((a, b) => b.timestamp - a.timestamp);
  }, []);

  const fetchAlerts = useCallback(async () => {
    try {
      // TODO: Replace with actual API call
      // const response = await fetch('/api/performance/alerts');
      // const data = await response.json();
      
      // Simulate API delay
      // eslint-disable-next-line @typescript-eslint/no-explicit-any
      await new Promise(resolve => (globalThis as any).setTimeout(resolve, 300));
      
      const mockAlerts = generateMockAlerts();
      setAlerts(mockAlerts);
    } catch {
      // Handle error silently or with user notification
    }
  }, [generateMockAlerts]);

  useEffect(() => {
    fetchAlerts();
    
    if (realTimeUpdates) {
      // Set up real-time updates every 30 seconds
      // eslint-disable-next-line @typescript-eslint/no-explicit-any
      const interval = (globalThis as any).setInterval(fetchAlerts, 30000);
      // eslint-disable-next-line @typescript-eslint/no-explicit-any
      return () => (globalThis as any).clearInterval(interval);
    }
  }, [fetchAlerts, realTimeUpdates]);

  // Play alert sound for critical alerts
  useEffect(() => {
    if (soundEnabled) {
      const criticalAlerts = alerts.filter(a => a.type === 'critical' && !a.acknowledged && !a.resolved);
      if (criticalAlerts.length > 0) {
        // In a real implementation, play an actual sound
        // Critical alert sound would play here
      }
    }
  }, [alerts, soundEnabled]);

  const handleAlertAction = (alertId: string, action: 'acknowledge' | 'resolve' | 'dismiss') => {
    setAlerts(prev => prev.map(alert => {
      if (alert.id === alertId) {
        switch (action) {
          case 'acknowledge':
            return { ...alert, acknowledged: true };
          case 'resolve':
            return { ...alert, resolved: true, acknowledged: true };
          case 'dismiss':
            return alert; // For now, just keep the alert
          default:
            return alert;
        }
      }
      return alert;
    }));

    onAlertAction?.(alertId, action);
  };

  const getFilteredAlerts = () => {
    let filtered = alerts;

    switch (filter) {
      case 'critical':
        filtered = alerts.filter(a => a.type === 'critical');
        break;
      case 'warning':
        filtered = alerts.filter(a => a.type === 'warning');
        break;
      case 'unresolved':
        filtered = alerts.filter(a => !a.resolved);
        break;
      default:
        filtered = alerts;
    }

    // Sort alerts
    return filtered.sort((a, b) => {
      switch (sortBy) {
        case 'severity': {
          const severityOrder = { critical: 3, warning: 2, info: 1 };
          return severityOrder[b.type] - severityOrder[a.type];
        }
        case 'domain':
          return a.domain.localeCompare(b.domain);
        case 'timestamp':
        default:
          return b.timestamp - a.timestamp;
      }
    });
  };

  const formatTime = (timestamp: number) => {
    const now = Date.now();
    const diff = now - timestamp;
    
    if (diff < 60000) return 'Just now';
    if (diff < 3600000) return `${Math.floor(diff / 60000)}m ago`;
    if (diff < 86400000) return `${Math.floor(diff / 3600000)}h ago`;
    return new Date(timestamp).toLocaleDateString();
  };

  const formatResponseTime = (ms: number) => {
    if (ms < 1000) return `${ms}ms`;
    return `${(ms / 1000).toFixed(2)}s`;
  };

  const getAlertIcon = (type: PerformanceAlert['type']) => {
    switch (type) {
      case 'critical': return '🚨';
      case 'warning': return '⚠️';
      case 'info': return 'ℹ️';
      default: return '📊';
    }
  };

  const getAlertVariant = (type: PerformanceAlert['type']) => {
    switch (type) {
      case 'critical': return 'destructive';
      case 'warning': return 'default';
      case 'info': return 'default';
      default: return 'default';
    }
  };

  const getDomainColor = (domain: string) => {
    const colors = {
      Security: 'bg-red-100 text-red-800 border-red-200',
      Productivity: 'bg-blue-100 text-blue-800 border-blue-200',
      MTG: 'bg-purple-100 text-purple-800 border-purple-200',
      Infrastructure: 'bg-green-100 text-green-800 border-green-200',
    };
    return colors[domain as keyof typeof colors] || 'bg-gray-100 text-gray-800 border-gray-200';
  };

  const filteredAlerts = getFilteredAlerts();
  const criticalCount = alerts.filter(a => a.type === 'critical' && !a.resolved).length;
  const warningCount = alerts.filter(a => a.type === 'warning' && !a.resolved).length;
  const unresolvedCount = alerts.filter(a => !a.resolved).length;

  return (
    <div className={`space-y-6 ${className}`}>
      {/* Header and Controls */}
      <div className="flex flex-col lg:flex-row justify-between items-start lg:items-center gap-4">
        <div>
          <h2 className="text-2xl font-bold tracking-tight">Performance Alerts</h2>
          <p className="text-gray-600">
            Real-time performance monitoring and alerting system
          </p>
        </div>
        
        <div className="flex items-center gap-4">
          {/* Sound Toggle */}
          <Button
            onClick={() => setSoundEnabled(!soundEnabled)}
            variant="outline"
            size="sm"
          >
            {soundEnabled ? '🔊' : '🔇'} Sound {soundEnabled ? 'On' : 'Off'}
          </Button>
          
          {/* Refresh Button */}
          <Button
            onClick={fetchAlerts}
            variant="outline"
            size="sm"
          >
            <span className="mr-2">⟳</span>
            Refresh
          </Button>
        </div>
      </div>

      {/* Alert Summary */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <Card>
          <CardContent className="p-4">
            <div className="text-center">
              <div className="text-2xl font-bold text-red-600">{criticalCount}</div>
              <div className="text-sm text-gray-600">Critical Alerts</div>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4">
            <div className="text-center">
              <div className="text-2xl font-bold text-yellow-600">{warningCount}</div>
              <div className="text-sm text-gray-600">Warning Alerts</div>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4">
            <div className="text-center">
              <div className="text-2xl font-bold text-gray-600">{unresolvedCount}</div>
              <div className="text-sm text-gray-600">Unresolved</div>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4">
            <div className="text-center">
              <div className="text-2xl font-bold text-gray-600">{alerts.length}</div>
              <div className="text-sm text-gray-600">Total Alerts</div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Filters and Sorting */}
      <div className="flex flex-wrap gap-4 items-center">
        <div className="flex gap-2">
          <span className="text-sm font-medium">Filter:</span>
          {(['all', 'critical', 'warning', 'unresolved'] as const).map((filterOption) => (
            <Button
              key={filterOption}
              onClick={() => setFilter(filterOption)}
              variant={filter === filterOption ? 'default' : 'outline'}
              size="sm"
            >
              {filterOption.charAt(0).toUpperCase() + filterOption.slice(1)}
            </Button>
          ))}
        </div>
        
        <div className="flex gap-2">
          <span className="text-sm font-medium">Sort by:</span>
          {(['timestamp', 'severity', 'domain'] as const).map((sortOption) => (
            <Button
              key={sortOption}
              onClick={() => setSortBy(sortOption)}
              variant={sortBy === sortOption ? 'default' : 'outline'}
              size="sm"
            >
              {sortOption.charAt(0).toUpperCase() + sortOption.slice(1)}
            </Button>
          ))}
        </div>
      </div>

      {/* Alerts List */}
      <div className="space-y-4">
        {filteredAlerts.length === 0 ? (
          <Card>
            <CardContent className="p-8 text-center">
              <div className="text-4xl mb-4">✅</div>
              <h3 className="text-lg font-medium mb-2">No alerts found</h3>
              <p className="text-gray-600">
                {filter === 'all' 
                  ? 'All systems are performing within normal parameters.'
                  : `No ${filter} alerts at this time.`
                }
              </p>
            </CardContent>
          </Card>
        ) : (
          filteredAlerts.map((alert) => (
            <Alert key={alert.id} variant={getAlertVariant(alert.type)}>
              <div className="flex items-start justify-between w-full">
                <div className="flex items-start space-x-3 flex-1">
                  <span className="text-lg" role="img" aria-label={alert.type}>
                    {getAlertIcon(alert.type)}
                  </span>
                  
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2 mb-2">
                      <h4 className="font-medium">{alert.title}</h4>
                      <Badge variant="outline" className={getDomainColor(alert.domain)}>
                        {alert.domain}
                      </Badge>
                      {alert.resolved && (
                        <Badge variant="outline" className="bg-green-100 text-green-800 border-green-200">
                          Resolved
                        </Badge>
                      )}
                      {alert.acknowledged && !alert.resolved && (
                        <Badge variant="outline" className="bg-yellow-100 text-yellow-800 border-yellow-200">
                          Acknowledged
                        </Badge>
                      )}
                    </div>
                    
                    <AlertDescription>
                      <p className="mb-2">{alert.message}</p>
                      <div className="text-sm text-gray-600">
                        <span>Response time: </span>
                        <span className="font-mono">{formatResponseTime(alert.actual)}</span>
                        <span> (threshold: {formatResponseTime(alert.threshold)})</span>
                        <span className="ml-4">•</span>
                        <span className="ml-2">{formatTime(alert.timestamp)}</span>
                      </div>
                    </AlertDescription>
                  </div>
                </div>
                
                <div className="flex gap-2 ml-4">
                  {!alert.acknowledged && (
                    <Button
                      onClick={() => handleAlertAction(alert.id, 'acknowledge')}
                      variant="outline"
                      size="sm"
                    >
                      Acknowledge
                    </Button>
                  )}
                  {!alert.resolved && (
                    <Button
                      onClick={() => handleAlertAction(alert.id, 'resolve')}
                      variant="outline"
                      size="sm"
                    >
                      Resolve
                    </Button>
                  )}
                </div>
              </div>
            </Alert>
          ))
        )}
      </div>
    </div>
  );
};

export default AlertSystem;