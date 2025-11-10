/**
 * Security Dashboard Component
 * 
 * Main dashboard for the security domain, providing access to all 13 security tools
 * with executive function accommodations and constitutional compliance.
 */

import React, { useEffect, useState } from 'react';
import { SecurityAIService } from '../../services/ai/SecurityAIService';
import './SecurityDashboard.css';
import { SecurityPerformanceWidget } from './SecurityPerformanceWidget';

interface SecurityTool {
  id: string;
  name: string;
  description: string;
  status: 'online' | 'offline' | 'error';
  category: 'threat-intel' | 'network-security' | 'malware-analysis' | 'incident-response';
  lastUpdate: string;
  healthScore: number;
}

interface SecurityDashboardProps {
  className?: string;
  onToolSelect?: (toolId: string) => void;
}

export const SecurityDashboard: React.FC<SecurityDashboardProps> = ({
  className = '',
  onToolSelect
}) => {
  const [tools, setTools] = useState<SecurityTool[]>([]);
  const [selectedCategory, setSelectedCategory] = useState<string>('all');
  const [loading, setLoading] = useState(true);
  const [healthStatus, setHealthStatus] = useState({
    overall: 95,
    critical: 0,
    warnings: 2
  });
  const [aiRecommendations, setAiRecommendations] = useState<Array<{
    id: string;
    title: string;
    description: string;
    priority: number;
  }>>([]);
  const [aiService] = useState(() => new SecurityAIService());

  // Security tools configuration (13 tools per requirements)
  const securityTools: SecurityTool[] = [
    {
      id: 'misp',
      name: 'MISP',
      description: 'Threat Intelligence Platform',
      status: 'online',
      category: 'threat-intel',
      lastUpdate: new Date().toISOString(),
      healthScore: 98
    },
    {
      id: 'securityonion',
      name: 'Security Onion',
      description: 'Network Security Monitoring',
      status: 'online',
      category: 'network-security',
      lastUpdate: new Date().toISOString(),
      healthScore: 95
    },
    {
      id: 'yarax',
      name: 'YARA-X',
      description: 'Malware Pattern Matching',
      status: 'online',
      category: 'malware-analysis',
      lastUpdate: new Date().toISOString(),
      healthScore: 92
    },
    {
      id: 'helk',
      name: 'HELK',
      description: 'Hunting ELK Stack',
      status: 'online',
      category: 'threat-intel',
      lastUpdate: new Date().toISOString(),
      healthScore: 90
    },
    {
      id: 'cyberchef',
      name: 'CyberChef',
      description: 'Data Analysis & Transformation',
      status: 'online',
      category: 'malware-analysis',
      lastUpdate: new Date().toISOString(),
      healthScore: 96
    },
    {
      id: 'nemesis',
      name: 'Nemesis',
      description: 'Offensive Security Framework',
      status: 'online',
      category: 'incident-response',
      lastUpdate: new Date().toISOString(),
      healthScore: 88
    },
    {
      id: 'maltrail',
      name: 'Maltrail',
      description: 'Malicious Network Traffic Detection',
      status: 'online',
      category: 'network-security',
      lastUpdate: new Date().toISOString(),
      healthScore: 93
    },
    {
      id: 'ghostwriter',
      name: 'Ghostwriter',
      description: 'Reporting & Documentation',
      status: 'online',
      category: 'incident-response',
      lastUpdate: new Date().toISOString(),
      healthScore: 94
    },
    {
      id: 'rita',
      name: 'RITA',
      description: 'Real Intelligence Threat Analytics',
      status: 'online',
      category: 'threat-intel',
      lastUpdate: new Date().toISOString(),
      healthScore: 91
    },
    {
      id: 'malwarebazaar',
      name: 'MalwareBazaar MCP',
      description: 'Malware Sample Database',
      status: 'online',
      category: 'malware-analysis',
      lastUpdate: new Date().toISOString(),
      healthScore: 89
    },
    {
      id: 'virustotal',
      name: 'VirusTotal MCP',
      description: 'File & URL Analysis',
      status: 'online',
      category: 'malware-analysis',
      lastUpdate: new Date().toISOString(),
      healthScore: 97
    },
    {
      id: 'blackarch',
      name: 'BlackArch Tools',
      description: 'Penetration Testing Suite',
      status: 'online',
      category: 'incident-response',
      lastUpdate: new Date().toISOString(),
      healthScore: 85
    },
    {
      id: 'apiscout',
      name: 'ApiScout',
      description: 'API Usage Analysis',
      status: 'online',
      category: 'malware-analysis',
      lastUpdate: new Date().toISOString(),
      healthScore: 87
    }
  ];

  useEffect(() => {
    // Simulate loading tools data
    const loadTools = async () => {
      setLoading(true);
      
      // Simulate API call delay
      await new Promise(resolve => setTimeout(resolve, 500));
      
      setTools(securityTools);
      setLoading(false);
    };

    loadTools();
  }, []);

  const filteredTools = selectedCategory === 'all' 
    ? tools 
    : tools.filter(tool => tool.category === selectedCategory);

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'online': return '#10B981'; // green
      case 'offline': return '#6B7280'; // gray
      case 'error': return '#EF4444'; // red
      default: return '#6B7280';
    }
  };

  const getCategoryIcon = (category: string) => {
    switch (category) {
      case 'threat-intel': return '🛡️';
      case 'network-security': return '🌐';
      case 'malware-analysis': return '🔍';
      case 'incident-response': return '🚨';
      default: return '🔧';
    }
  };

  const handleToolClick = async (toolId: string) => {
    if (onToolSelect) {
      onToolSelect(toolId);
    }
    
    // Constitutional requirement: <200ms UI response
    // Tool selection should be immediate, AI recommendations async
    
    // Get AI recommendations asynchronously (doesn't block UI)
    try {
      const recommendations = await aiService.getSecurityRecommendations({
        domain: 'security',
        tool: toolId
      });
      
      setAiRecommendations(recommendations.slice(0, 3)); // Show top 3 recommendations
    } catch (error) {
      // Silently fail to not impact user experience
      setAiRecommendations([]);
    }
  };

  if (loading) {
    return (
      <div className={`security-dashboard loading ${className}`}>
        <div className="loading-spinner" aria-live="polite">
          Loading security tools...
        </div>
      </div>
    );
  }

  return (
    <div className={`security-dashboard ${className}`} role="main">
      {/* Header with Health Status */}
      <header className="dashboard-header">
        <h1>Security Operations Center</h1>
        <div className="health-indicators" role="status" aria-live="polite">
          <div className="health-metric">
            <span className="health-label">Overall Health</span>
            <span className="health-value">{healthStatus.overall}%</span>
          </div>
          <div className="health-metric">
            <span className="health-label">Critical Issues</span>
            <span className="health-value critical">{healthStatus.critical}</span>
          </div>
          <div className="health-metric">
            <span className="health-label">Warnings</span>
            <span className="health-value warning">{healthStatus.warnings}</span>
          </div>
        </div>
      </header>

      {/* Category Filter */}
      <nav className="category-filter" role="navigation" aria-label="Tool categories">
        <button
          className={selectedCategory === 'all' ? 'active' : ''}
          onClick={() => setSelectedCategory('all')}
          aria-pressed={selectedCategory === 'all'}
        >
          All Tools ({tools.length})
        </button>
        <button
          className={selectedCategory === 'threat-intel' ? 'active' : ''}
          onClick={() => setSelectedCategory('threat-intel')}
          aria-pressed={selectedCategory === 'threat-intel'}
        >
          🛡️ Threat Intel ({tools.filter(t => t.category === 'threat-intel').length})
        </button>
        <button
          className={selectedCategory === 'network-security' ? 'active' : ''}
          onClick={() => setSelectedCategory('network-security')}
          aria-pressed={selectedCategory === 'network-security'}
        >
          🌐 Network Security ({tools.filter(t => t.category === 'network-security').length})
        </button>
        <button
          className={selectedCategory === 'malware-analysis' ? 'active' : ''}
          onClick={() => setSelectedCategory('malware-analysis')}
          aria-pressed={selectedCategory === 'malware-analysis'}
        >
          🔍 Malware Analysis ({tools.filter(t => t.category === 'malware-analysis').length})
        </button>
        <button
          className={selectedCategory === 'incident-response' ? 'active' : ''}
          onClick={() => setSelectedCategory('incident-response')}
          aria-pressed={selectedCategory === 'incident-response'}
        >
          🚨 Incident Response ({tools.filter(t => t.category === 'incident-response').length})
        </button>
      </nav>

      {/* Tools Grid */}
      <main className="tools-grid" role="grid" aria-label="Security tools">
        {filteredTools.map((tool) => (
          <div
            key={tool.id}
            className="tool-card"
            role="gridcell"
            tabIndex={0}
            onClick={() => handleToolClick(tool.id)}
            onKeyDown={(e) => {
              if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                handleToolClick(tool.id);
              }
            }}
            aria-label={`${tool.name}: ${tool.description}, Status: ${tool.status}`}
          >
            <div className="tool-header">
              <div className="tool-icon">
                {getCategoryIcon(tool.category)}
              </div>
              <div className="tool-status">
                <div
                  className="status-indicator"
                  style={{ backgroundColor: getStatusColor(tool.status) }}
                  aria-label={`Status: ${tool.status}`}
                />
              </div>
            </div>
            
            <div className="tool-content">
              <h3 className="tool-name">{tool.name}</h3>
              <p className="tool-description">{tool.description}</p>
              
              <div className="tool-metrics">
                <div className="metric">
                  <span className="metric-label">Health</span>
                  <span className="metric-value">{tool.healthScore}%</span>
                </div>
                <div className="metric">
                  <span className="metric-label">Updated</span>
                  <span className="metric-value">
                    {new Date(tool.lastUpdate).toLocaleTimeString()}
                  </span>
                </div>
              </div>
            </div>
            
            <div className="tool-actions">
              <button 
                className="action-button primary"
                onClick={(e) => {
                  e.stopPropagation();
                  handleToolClick(tool.id);
                }}
                aria-label={`Launch ${tool.name}`}
              >
                Launch
              </button>
              <button 
                className="action-button secondary"
                onClick={(e) => {
                  e.stopPropagation();
                  // Handle tool configuration
                }}
                aria-label={`Configure ${tool.name}`}
              >
                ⚙️
              </button>
            </div>
          </div>
        ))}
      </main>

      {/* Performance Monitor */}
      <aside className="performance-section" role="complementary" aria-label="Performance monitoring">
        <SecurityPerformanceWidget />
      </aside>

      {/* Quick Actions */}
      <aside className="quick-actions" role="complementary" aria-label="Quick actions">
        <h2>Quick Actions</h2>
        <div className="action-buttons">
          <button 
            className="quick-action-btn threat-hunt"
            onClick={() => handleToolClick('threat-hunt')}
          >
            🎯 Start Threat Hunt
          </button>
          <button 
            className="quick-action-btn incident-create"
            onClick={() => handleToolClick('incident-create')}
          >
            📋 Create Incident
          </button>
          <button 
            className="quick-action-btn malware-scan"
            onClick={() => handleToolClick('malware-scan')}
          >
            🔍 Quick Malware Scan
          </button>
          <button 
            className="quick-action-btn intel-search"
            onClick={() => handleToolClick('intel-search')}
          >
            🛡️ Threat Intel Search
          </button>
        </div>
      </aside>

      {/* AI Recommendations */}
      {aiRecommendations.length > 0 && (
        <aside className="ai-recommendations" role="complementary" aria-label="AI recommendations">
          <h2>🤖 AI Recommendations</h2>
          <div className="recommendations-list">
            {aiRecommendations.map((rec) => (
              <div key={rec.id} className="recommendation-item">
                <div className="recommendation-header">
                  <h3 className="recommendation-title">{rec.title}</h3>
                  <span className={`priority-badge priority-${rec.priority}`}>
                    P{rec.priority}
                  </span>
                </div>
                <p className="recommendation-description">{rec.description}</p>
              </div>
            ))}
          </div>
        </aside>
      )}
    </div>
  );
};