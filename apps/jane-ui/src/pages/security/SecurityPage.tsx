/**
 * Security Workflow Pages
 * 
 * Main security domain page with integrated workflow management
 * and constitutional compliance (<1s response for security domain).
 */

import React, { useState } from 'react';
import {
    IncidentResponse,
    SecurityAlerts,
    SecurityDashboard,
    ThreatCorrelation,
    ThreatHunting,
    ToolLauncher
} from '../../components/Security';
import './SecurityPage.css';

type SecurityView = 
  | 'dashboard' 
  | 'alerts' 
  | 'hunting' 
  | 'correlation' 
  | 'tools' 
  | 'incidents';

interface SecurityPageProps {
  className?: string;
  initialView?: SecurityView;
}

export const SecurityPage: React.FC<SecurityPageProps> = ({
  className = '',
  initialView = 'dashboard'
}) => {
  const [activeView, setActiveView] = useState<SecurityView>(initialView);
  const [isLoading, setIsLoading] = useState(false);
  const [workflowContext, setWorkflowContext] = useState<any>({});

  const navigationItems = [
    { id: 'dashboard', label: 'SOC Dashboard', icon: '🎯', description: 'Overview and tool access' },
    { id: 'alerts', label: 'Security Alerts', icon: '🚨', description: 'Real-time threat alerts' },
    { id: 'hunting', label: 'Threat Hunting', icon: '🔍', description: 'Proactive threat discovery' },
    { id: 'correlation', label: 'Threat Intel', icon: '🛡️', description: 'IOC correlation analysis' },
    { id: 'tools', label: 'Tool Launcher', icon: '🚀', description: 'Launch security tools' },
    { id: 'incidents', label: 'Incidents', icon: '📋', description: 'Incident response management' }
  ];

  const handleViewChange = async (newView: SecurityView) => {
    if (newView === activeView) return;

    setIsLoading(true);
    
    // Constitutional requirement: <200ms UI response
    const startTime = Date.now();
    
    try {
      // Simulate view transition delay
      await new Promise(resolve => setTimeout(resolve, 50));
      
      setActiveView(newView);
      
      const responseTime = Date.now() - startTime;
      if (responseTime > 200) {
        console.warn(`Security view change exceeded 200ms: ${responseTime}ms`);
      }
      
    } catch (error) {
      console.error('View change failed:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleToolLaunch = (toolId: string, context?: any) => {
    setWorkflowContext(prev => ({
      ...prev,
      lastLaunchedTool: toolId,
      toolContext: context,
      timestamp: new Date().toISOString()
    }));
  };

  const handleCorrelationComplete = (results: any[]) => {
    setWorkflowContext(prev => ({
      ...prev,
      correlationResults: results,
      timestamp: new Date().toISOString()
    }));
  };

  const renderActiveView = () => {
    const baseProps = {
      className: 'security-view-content'
    };

    switch (activeView) {
      case 'dashboard':
        return (
          <SecurityDashboard 
            {...baseProps}
            onToolSelect={handleToolLaunch}
          />
        );
      
      case 'alerts':
        return (
          <SecurityAlerts 
            {...baseProps}
          />
        );
      
      case 'hunting':
        return (
          <ThreatHunting 
            {...baseProps}
          />
        );
      
      case 'correlation':
        return (
          <ThreatCorrelation 
            {...baseProps}
            onCorrelationComplete={handleCorrelationComplete}
          />
        );
      
      case 'tools':
        return (
          <ToolLauncher 
            {...baseProps}
            onToolLaunch={handleToolLaunch}
          />
        );
      
      case 'incidents':
        return (
          <IncidentResponse 
            {...baseProps}
          />
        );
      
      default:
        return (
          <SecurityDashboard 
            {...baseProps}
            onToolSelect={handleToolLaunch}
          />
        );
    }
  };

  return (
    <div className={`security-page ${className}`} role="main">
      {/* Header */}
      <header className="security-header">
        <div className="header-content">
          <h1 className="page-title">Security Operations Center</h1>
          <div className="header-status">
            <span className="domain-badge">Security Domain</span>
            <span className="performance-indicator">
              <span className="performance-label">Target Response:</span>
              <span className="performance-value">&lt;1s</span>
            </span>
          </div>
        </div>
      </header>

      {/* Navigation */}
      <nav className="security-navigation" role="navigation" aria-label="Security workflows">
        <div className="nav-items">
          {navigationItems.map(item => (
            <button
              key={item.id}
              onClick={() => handleViewChange(item.id as SecurityView)}
              className={`nav-item ${activeView === item.id ? 'active' : ''}`}
              disabled={isLoading}
              aria-pressed={activeView === item.id}
              aria-describedby={`nav-desc-${item.id}`}
            >
              <span className="nav-icon" aria-hidden="true">{item.icon}</span>
              <div className="nav-content">
                <span className="nav-label">{item.label}</span>
                <span 
                  id={`nav-desc-${item.id}`}
                  className="nav-description"
                >
                  {item.description}
                </span>
              </div>
            </button>
          ))}
        </div>
      </nav>

      {/* Main Content */}
      <main className="security-main">
        {isLoading && (
          <div className="loading-overlay" aria-live="polite">
            <div className="loading-content">
              <span className="loading-spinner" aria-hidden="true">⏳</span>
              <span>Loading security workflow...</span>
            </div>
          </div>
        )}
        
        <div className={`view-container ${isLoading ? 'loading' : ''}`}>
          {renderActiveView()}
        </div>
      </main>

      {/* Workflow Context Panel */}
      {Object.keys(workflowContext).length > 0 && (
        <aside className="workflow-context" role="complementary" aria-label="Workflow context">
          <h3>Workflow Context</h3>
          <div className="context-content">
            {workflowContext.lastLaunchedTool && (
              <div className="context-item">
                <span className="context-label">Last Tool:</span>
                <span className="context-value">{workflowContext.lastLaunchedTool}</span>
              </div>
            )}
            {workflowContext.correlationResults && (
              <div className="context-item">
                <span className="context-label">Correlations:</span>
                <span className="context-value">
                  {workflowContext.correlationResults.length} results
                </span>
              </div>
            )}
            {workflowContext.timestamp && (
              <div className="context-item">
                <span className="context-label">Updated:</span>
                <span className="context-value">
                  {new Date(workflowContext.timestamp).toLocaleTimeString()}
                </span>
              </div>
            )}
          </div>
        </aside>
      )}
    </div>
  );
};

export default SecurityPage;