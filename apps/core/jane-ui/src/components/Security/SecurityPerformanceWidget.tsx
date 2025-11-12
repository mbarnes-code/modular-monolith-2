/**
 * Security Performance Widget
 * 
 * Displays real-time performance monitoring for security domain
 * with constitutional compliance indicators.
 */

import React, { useEffect, useState } from 'react';
import { securityPerformanceMonitor } from '../../services/performance/SecurityPerformanceMonitor';
import './SecurityPerformanceWidget.css';

interface SecurityPerformanceWidgetProps {
  className?: string;
}

export const SecurityPerformanceWidget: React.FC<SecurityPerformanceWidgetProps> = ({
  className = ''
}) => {
  const [complianceStatus, setComplianceStatus] = useState({
    isCompliant: true,
    violations: [],
    overallScore: 100
  });
  const [recentAlerts, setRecentAlerts] = useState([]);
  const [stats, setStats] = useState({
    count: 0,
    averageResponseTime: 0,
    successRate: 100,
    thresholdViolations: 0
  });

  useEffect(() => {
    // Update performance data every 5 seconds
    const updatePerformanceData = () => {
      const compliance = securityPerformanceMonitor.getComplianceStatus();
      const alerts = securityPerformanceMonitor.getAlerts(5);
      const performanceStats = securityPerformanceMonitor.getStats();
      
      setComplianceStatus(compliance);
      setRecentAlerts(alerts);
      setStats(performanceStats);
    };

    // Initial load
    updatePerformanceData();

    // Set up periodic updates
    const interval = setInterval(updatePerformanceData, 5000);

    // Set up alert listener
    const handleAlert = (alert: any) => {
      setRecentAlerts(prev => [alert, ...prev.slice(0, 4)]);
    };
    
    securityPerformanceMonitor.onAlert(handleAlert);

    return () => {
      clearInterval(interval);
    };
  }, []);

  const getComplianceColor = (score: number) => {
    if (score >= 95) return '#10B981'; // Green
    if (score >= 85) return '#F59E0B'; // Yellow
    return '#EF4444'; // Red
  };

  const formatResponseTime = (time: number) => {
    if (time < 1000) {
      return `${Math.round(time)}ms`;
    }
    return `${(time / 1000).toFixed(1)}s`;
  };

  return (
    <div className={`security-performance-widget ${className}`}>
      <div className="widget-header">
        <h3 className="widget-title">Performance Monitor</h3>
        <div 
          className="compliance-indicator"
          style={{ backgroundColor: getComplianceColor(complianceStatus.overallScore) }}
          title={`Compliance Score: ${Math.round(complianceStatus.overallScore)}%`}
        >
          {complianceStatus.isCompliant ? '✓' : '⚠'}
        </div>
      </div>

      <div className="performance-metrics">
        <div className="metric-item">
          <span className="metric-label">Avg Response:</span>
          <span 
            className={`metric-value ${stats.averageResponseTime > 1000 ? 'warning' : 'normal'}`}
          >
            {formatResponseTime(stats.averageResponseTime)}
          </span>
        </div>

        <div className="metric-item">
          <span className="metric-label">Success Rate:</span>
          <span 
            className={`metric-value ${stats.successRate < 95 ? 'warning' : 'normal'}`}
          >
            {Math.round(stats.successRate)}%
          </span>
        </div>

        <div className="metric-item">
          <span className="metric-label">Operations:</span>
          <span className="metric-value">{stats.count}</span>
        </div>

        {stats.thresholdViolations > 0 && (
          <div className="metric-item">
            <span className="metric-label">Violations:</span>
            <span className="metric-value warning">{stats.thresholdViolations}</span>
          </div>
        )}
      </div>

      {complianceStatus.violations.length > 0 && (
        <div className="violations-section">
          <h4 className="violations-title">Constitutional Violations</h4>
          <div className="violations-list">
            {complianceStatus.violations.slice(0, 3).map((violation, index) => (
              <div key={index} className="violation-item">
                <span className="violation-operation">{violation.operation}</span>
                <span className="violation-time">
                  {formatResponseTime(violation.actualTime)} 
                  <span className="violation-threshold">
                    (&gt;{formatResponseTime(violation.threshold)})
                  </span>
                </span>
              </div>
            ))}
          </div>
        </div>
      )}

      {recentAlerts.length > 0 && (
        <div className="alerts-section">
          <h4 className="alerts-title">Recent Alerts</h4>
          <div className="alerts-list">
            {recentAlerts.slice(0, 2).map((alert: any) => (
              <div key={alert.id} className={`alert-item ${alert.severity}`}>
                <span className="alert-message">{alert.message}</span>
                <span className="alert-time">
                  {new Date(alert.timestamp).toLocaleTimeString()}
                </span>
              </div>
            ))}
          </div>
        </div>
      )}

      <div className="widget-footer">
        <small className="constitutional-note">
          Security Domain Target: &lt;1s response time
        </small>
      </div>
    </div>
  );
};

export default SecurityPerformanceWidget;