/**
 * Security Alerts Page
 * 
 * Real-time security alert monitoring and management interface
 * with constitutional compliance (<1s response for security domain).
 */

import React, { useCallback, useState } from 'react';
import './SecurityAlertsPage.css';

interface SecurityAlert {
  id: string;
  severity: 'critical' | 'high' | 'medium' | 'low';
  title: string;
  description: string;
  source: string;
  timestamp: string;
  status: 'new' | 'investigating' | 'resolved' | 'false_positive';
  indicators: string[];
  assignedTo?: string;
}

interface SecurityAlertsPageProps {
  className?: string;
}

export const SecurityAlertsPage: React.FC<SecurityAlertsPageProps> = ({
  className = ''
}) => {
  const [alerts, setAlerts] = useState<SecurityAlert[]>([]);
  const [selectedAlert, setSelectedAlert] = useState<SecurityAlert | null>(null);
  const [filterSeverity, setFilterSeverity] = useState<string>('all');
  const [filterStatus, setFilterStatus] = useState<string>('all');
  const [isLoading, setIsLoading] = useState(false);

  const handleAlertSelect = useCallback((alert: SecurityAlert) => {
    setSelectedAlert(alert);
  }, []);

  const handleStatusUpdate = useCallback((alertId: string, newStatus: SecurityAlert['status']) => {
    setAlerts(prev => prev.map(alert => 
      alert.id === alertId 
        ? { ...alert, status: newStatus }
        : alert
    ));
  }, []);

  const getSeverityColor = (severity: SecurityAlert['severity']) => {
    switch (severity) {
      case 'critical': return '#dc2626';
      case 'high': return '#ea580c';
      case 'medium': return '#ca8a04';
      case 'low': return '#16a34a';
      default: return '#6b7280';
    }
  };

  const getStatusBadge = (status: SecurityAlert['status']) => {
    const statusConfig = {
      new: { label: 'New', color: '#dc2626' },
      investigating: { label: 'Investigating', color: '#ea580c' },
      resolved: { label: 'Resolved', color: '#16a34a' },
      false_positive: { label: 'False Positive', color: '#6b7280' }
    };
    
    return statusConfig[status] || statusConfig.new;
  };

  return (
    <div className={`security-alerts-page ${className}`} role="main">
      <header className="alerts-header">
        <h1 className="page-title">Security Alerts</h1>
        <div className="header-actions">
          <button className="refresh-button" disabled={isLoading}>
            <span aria-hidden="true">🔄</span>
            Refresh Alerts
          </button>
        </div>
      </header>

      <div className="alerts-controls">
        <div className="filter-group">
          <label htmlFor="severity-filter" className="filter-label">Severity:</label>
          <select 
            id="severity-filter"
            value={filterSeverity}
            onChange={(e) => setFilterSeverity(e.target.value)}
            className="filter-select"
          >
            <option value="all">All Severities</option>
            <option value="critical">Critical</option>
            <option value="high">High</option>
            <option value="medium">Medium</option>
            <option value="low">Low</option>
          </select>
        </div>

        <div className="filter-group">
          <label htmlFor="status-filter" className="filter-label">Status:</label>
          <select 
            id="status-filter"
            value={filterStatus}
            onChange={(e) => setFilterStatus(e.target.value)}
            className="filter-select"
          >
            <option value="all">All Statuses</option>
            <option value="new">New</option>
            <option value="investigating">Investigating</option>
            <option value="resolved">Resolved</option>
            <option value="false_positive">False Positive</option>
          </select>
        </div>

        <div className="stats-summary">
          <span className="stat-item">
            <span className="stat-label">Total Alerts:</span>
            <span className="stat-value">{alerts.length}</span>
          </span>
        </div>
      </div>

      <div className="alerts-layout">
        <div className="alerts-list">
          <h2 className="section-title">Active Alerts</h2>
          
          {alerts.length === 0 ? (
            <div className="empty-state">
              <span className="empty-icon" aria-hidden="true">🛡️</span>
              <h3>No Security Alerts</h3>
              <p>All systems are currently secure. New alerts will appear here when detected.</p>
            </div>
          ) : (
            <div className="alert-items">
              {alerts.map(alert => (
                <div 
                  key={alert.id}
                  className={`alert-item ${selectedAlert?.id === alert.id ? 'selected' : ''}`}
                  onClick={() => handleAlertSelect(alert)}
                  role="button"
                  tabIndex={0}
                  onKeyDown={(e) => {
                    if (e.key === 'Enter' || e.key === ' ') {
                      e.preventDefault();
                      handleAlertSelect(alert);
                    }
                  }}
                >
                  <div className="alert-header">
                    <div 
                      className="severity-indicator"
                      style={{ backgroundColor: getSeverityColor(alert.severity) }}
                      aria-label={`${alert.severity} severity`}
                    />
                    <h3 className="alert-title">{alert.title}</h3>
                    <span 
                      className="status-badge"
                      style={{ backgroundColor: getStatusBadge(alert.status).color }}
                    >
                      {getStatusBadge(alert.status).label}
                    </span>
                  </div>
                  
                  <p className="alert-description">{alert.description}</p>
                  
                  <div className="alert-meta">
                    <span className="alert-source">Source: {alert.source}</span>
                    <span className="alert-time">
                      {new Date(alert.timestamp).toLocaleString()}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {selectedAlert && (
          <aside className="alert-details" role="complementary" aria-label="Alert details">
            <div className="details-header">
              <h2 className="details-title">Alert Details</h2>
              <button 
                className="close-details"
                onClick={() => setSelectedAlert(null)}
                aria-label="Close alert details"
              >
                <span aria-hidden="true">✕</span>
              </button>
            </div>

            <div className="details-content">
              <div className="detail-section">
                <h3>Basic Information</h3>
                <div className="detail-grid">
                  <div className="detail-item">
                    <span className="detail-label">Severity:</span>
                    <span className="detail-value severity-value" style={{ color: getSeverityColor(selectedAlert.severity) }}>
                      {selectedAlert.severity.toUpperCase()}
                    </span>
                  </div>
                  <div className="detail-item">
                    <span className="detail-label">Status:</span>
                    <select
                      value={selectedAlert.status}
                      onChange={(e) => handleStatusUpdate(selectedAlert.id, e.target.value as SecurityAlert['status'])}
                      className="status-select"
                    >
                      <option value="new">New</option>
                      <option value="investigating">Investigating</option>
                      <option value="resolved">Resolved</option>
                      <option value="false_positive">False Positive</option>
                    </select>
                  </div>
                  <div className="detail-item">
                    <span className="detail-label">Source:</span>
                    <span className="detail-value">{selectedAlert.source}</span>
                  </div>
                  <div className="detail-item">
                    <span className="detail-label">Timestamp:</span>
                    <span className="detail-value">
                      {new Date(selectedAlert.timestamp).toLocaleString()}
                    </span>
                  </div>
                </div>
              </div>

              <div className="detail-section">
                <h3>Description</h3>
                <p className="alert-full-description">{selectedAlert.description}</p>
              </div>

              {selectedAlert.indicators.length > 0 && (
                <div className="detail-section">
                  <h3>Indicators of Compromise</h3>
                  <ul className="indicators-list">
                    {selectedAlert.indicators.map((indicator, index) => (
                      <li key={index} className="indicator-item">
                        <code className="indicator-value">{indicator}</code>
                      </li>
                    ))}
                  </ul>
                </div>
              )}

              <div className="detail-actions">
                <button className="action-button primary">
                  <span aria-hidden="true">🔍</span>
                  Investigate
                </button>
                <button className="action-button secondary">
                  <span aria-hidden="true">🎯</span>
                  Hunt Threats
                </button>
                <button className="action-button secondary">
                  <span aria-hidden="true">📋</span>
                  Create Incident
                </button>
              </div>
            </div>
          </aside>
        )}
      </div>
    </div>
  );
};

export default SecurityAlertsPage;