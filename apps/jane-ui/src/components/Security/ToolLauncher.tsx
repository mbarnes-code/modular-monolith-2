/**
 * Security Tool Launcher Component
 * 
 * Unified launcher for all 13 security tools with executive function
 * accommodations and constitutional compliance.
 */

import React, { useCallback, useState } from 'react';
import './ToolLauncher.css';

interface SecurityTool {
  id: string;
  name: string;
  description: string;
  category: 'threat-intel' | 'network-security' | 'malware-analysis' | 'incident-response';
  status: 'online' | 'offline' | 'error';
  launchUrl?: string;
  requiresConfig?: boolean;
  features: string[];
  icon: string;
}

interface ToolLauncherProps {
  className?: string;
  onToolLaunch?: (toolId: string, context?: any) => void;
  selectedTool?: string;
}

export const ToolLauncher: React.FC<ToolLauncherProps> = ({
  className = '',
  onToolLaunch,
  selectedTool
}) => {
  const [launchingTool, setLaunchingTool] = useState<string | null>(null);
  const [selectedCategory, setSelectedCategory] = useState<string>('all');
  const [searchQuery, setSearchQuery] = useState('');
  const [toolContext, setToolContext] = useState<Record<string, any>>({});

  // Security tools configuration (13 tools per requirements)
  const securityTools: SecurityTool[] = [
    {
      id: 'misp',
      name: 'MISP',
      description: 'Threat Intelligence Platform for sharing, storing and correlating IOCs',
      category: 'threat-intel',
      status: 'online',
      launchUrl: '/tools/misp',
      requiresConfig: false,
      features: ['IOC Management', 'Threat Sharing', 'Event Correlation', 'API Integration'],
      icon: '🛡️'
    },
    {
      id: 'securityonion',
      name: 'Security Onion',
      description: 'Network Security Monitoring platform with Suricata, Zeek, and more',
      category: 'network-security',
      status: 'online',
      launchUrl: '/tools/securityonion',
      requiresConfig: false,
      features: ['Network Monitoring', 'Alert Management', 'Hunt Platform', 'PCAP Analysis'],
      icon: '🌐'
    },
    {
      id: 'yarax',
      name: 'YARA-X',
      description: 'Advanced malware pattern matching and classification engine',
      category: 'malware-analysis',
      status: 'online',
      launchUrl: '/tools/yarax',
      requiresConfig: true,
      features: ['Pattern Matching', 'Rule Management', 'File Scanning', 'Custom Rules'],
      icon: '🔍'
    },
    {
      id: 'helk',
      name: 'HELK',
      description: 'Hunting ELK Stack for threat hunting and analysis',
      category: 'threat-intel',
      status: 'online',
      launchUrl: '/tools/helk',
      requiresConfig: false,
      features: ['Log Analysis', 'Threat Hunting', 'Data Visualization', 'Search Queries'],
      icon: '📊'
    },
    {
      id: 'cyberchef',
      name: 'CyberChef',
      description: 'Swiss Army knife for data transformation and analysis',
      category: 'malware-analysis',
      status: 'online',
      launchUrl: '/tools/cyberchef',
      requiresConfig: false,
      features: ['Data Encoding', 'Cryptography', 'Format Analysis', 'Recipe Builder'],
      icon: '🍳'
    },
    {
      id: 'nemesis',
      name: 'Nemesis',
      description: 'Offensive security and red team collaboration platform',
      category: 'incident-response',
      status: 'online',
      launchUrl: '/tools/nemesis',
      requiresConfig: true,
      features: ['Attack Simulation', 'Team Collaboration', 'Evidence Collection', 'Reporting'],
      icon: '⚔️'
    },
    {
      id: 'maltrail',
      name: 'Maltrail',
      description: 'Malicious network traffic detection system',
      category: 'network-security',
      status: 'online',
      launchUrl: '/tools/maltrail',
      requiresConfig: false,
      features: ['Traffic Analysis', 'Threat Detection', 'Real-time Monitoring', 'Custom Rules'],
      icon: '🚨'
    },
    {
      id: 'ghostwriter',
      name: 'Ghostwriter',
      description: 'Penetration testing report generation and management',
      category: 'incident-response',
      status: 'online',
      launchUrl: '/tools/ghostwriter',
      requiresConfig: true,
      features: ['Report Generation', 'Finding Management', 'Template System', 'Collaboration'],
      icon: '📝'
    },
    {
      id: 'rita',
      name: 'RITA',
      description: 'Real Intelligence Threat Analytics for network data analysis',
      category: 'threat-intel',
      status: 'online',
      launchUrl: '/tools/rita',
      requiresConfig: false,
      features: ['Beacon Detection', 'DNS Analysis', 'Long Connection Analysis', 'Statistical Analysis'],
      icon: '📡'
    },
    {
      id: 'malwarebazaar',
      name: 'MalwareBazaar MCP',
      description: 'Malware sample database and analysis platform',
      category: 'malware-analysis',
      status: 'online',
      launchUrl: '/tools/malwarebazaar',
      requiresConfig: false,
      features: ['Sample Database', 'Hash Lookup', 'Family Classification', 'API Access'],
      icon: '🗃️'
    },
    {
      id: 'virustotal',
      name: 'VirusTotal MCP',
      description: 'File and URL analysis with multiple antivirus engines',
      category: 'malware-analysis',
      status: 'online',
      launchUrl: '/tools/virustotal',
      requiresConfig: true,
      features: ['Multi-engine Scanning', 'URL Analysis', 'Reputation Lookup', 'Community Comments'],
      icon: '🔬'
    },
    {
      id: 'blackarch',
      name: 'BlackArch Tools',
      description: 'Comprehensive penetration testing and security toolkit',
      category: 'incident-response',
      status: 'online',
      launchUrl: '/tools/blackarch',
      requiresConfig: true,
      features: ['Penetration Testing', 'Exploitation Tools', 'Forensics', 'Reverse Engineering'],
      icon: '🏴'
    },
    {
      id: 'apiscout',
      name: 'ApiScout',
      description: 'Windows API usage analysis for malware research',
      category: 'malware-analysis',
      status: 'online',
      launchUrl: '/tools/apiscout',
      requiresConfig: false,
      features: ['API Analysis', 'Import Reconstruction', 'Signature Matching', 'Malware Research'],
      icon: '🔎'
    }
  ];

  const filteredTools = securityTools.filter(tool => {
    const matchesCategory = selectedCategory === 'all' || tool.category === selectedCategory;
    const matchesSearch = searchQuery === '' || 
      tool.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      tool.description.toLowerCase().includes(searchQuery.toLowerCase()) ||
      tool.features.some(feature => feature.toLowerCase().includes(searchQuery.toLowerCase()));
    
    return matchesCategory && matchesSearch;
  });

  const handleToolLaunch = useCallback(async (tool: SecurityTool) => {
    if (tool.status !== 'online') {
      return;
    }

    setLaunchingTool(tool.id);

    try {
      // Simulate launch delay (constitutional requirement: <200ms UI response)
      await new Promise(resolve => setTimeout(resolve, 100));

      if (onToolLaunch) {
        onToolLaunch(tool.id, toolContext[tool.id]);
      }

      // In real implementation, would navigate to tool or open in new context
      if (tool.launchUrl) {
        // window.open(tool.launchUrl, '_blank');
      }

    } catch (error) {
      console.error(`Failed to launch ${tool.name}:`, error);
    } finally {
      setLaunchingTool(null);
    }
  }, [onToolLaunch, toolContext]);

  const updateToolContext = (toolId: string, key: string, value: any) => {
    setToolContext(prev => ({
      ...prev,
      [toolId]: {
        ...prev[toolId],
        [key]: value
      }
    }));
  };

  const getStatusIndicator = (status: string) => {
    switch (status) {
      case 'online':
        return <span className="status-indicator online" title="Online">🟢</span>;
      case 'offline':
        return <span className="status-indicator offline" title="Offline">🔴</span>;
      case 'error':
        return <span className="status-indicator error" title="Error">⚠️</span>;
      default:
        return <span className="status-indicator unknown" title="Unknown">❓</span>;
    }
  };

  const getCategoryCount = (category: string) => {
    return securityTools.filter(tool => tool.category === category).length;
  };

  return (
    <div className={`tool-launcher ${className}`} role="main">
      <header className="launcher-header">
        <h2>Security Tool Launcher</h2>
        <p className="header-description">
          Launch and configure all 13 security tools from unified interface
        </p>
      </header>

      {/* Search and Filter Controls */}
      <section className="controls-section" aria-labelledby="controls-title">
        <h3 id="controls-title" className="sr-only">Search and Filter Controls</h3>
        
        <div className="search-box">
          <input
            type="text"
            placeholder="Search tools, features, or descriptions..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="search-input"
            aria-label="Search security tools"
          />
          <span className="search-icon">🔍</span>
        </div>

        <nav className="category-filter" role="navigation" aria-label="Tool categories">
          <button
            className={selectedCategory === 'all' ? 'active' : ''}
            onClick={() => setSelectedCategory('all')}
            aria-pressed={selectedCategory === 'all'}
          >
            All Tools ({securityTools.length})
          </button>
          <button
            className={selectedCategory === 'threat-intel' ? 'active' : ''}
            onClick={() => setSelectedCategory('threat-intel')}
            aria-pressed={selectedCategory === 'threat-intel'}
          >
            🛡️ Threat Intel ({getCategoryCount('threat-intel')})
          </button>
          <button
            className={selectedCategory === 'network-security' ? 'active' : ''}
            onClick={() => setSelectedCategory('network-security')}
            aria-pressed={selectedCategory === 'network-security'}
          >
            🌐 Network Security ({getCategoryCount('network-security')})
          </button>
          <button
            className={selectedCategory === 'malware-analysis' ? 'active' : ''}
            onClick={() => setSelectedCategory('malware-analysis')}
            aria-pressed={selectedCategory === 'malware-analysis'}
          >
            🔍 Malware Analysis ({getCategoryCount('malware-analysis')})
          </button>
          <button
            className={selectedCategory === 'incident-response' ? 'active' : ''}
            onClick={() => setSelectedCategory('incident-response')}
            aria-pressed={selectedCategory === 'incident-response'}
          >
            🚨 Incident Response ({getCategoryCount('incident-response')})
          </button>
        </nav>
      </section>

      {/* Tools List */}
      <main className="tools-list" role="list" aria-label="Available security tools">
        {filteredTools.map(tool => (
          <article
            key={tool.id}
            className={`tool-item ${selectedTool === tool.id ? 'selected' : ''}`}
            role="listitem"
          >
            <div className="tool-info">
              <div className="tool-header">
                <div className="tool-identity">
                  <span className="tool-icon" aria-hidden="true">{tool.icon}</span>
                  <h3 className="tool-name">{tool.name}</h3>
                  {getStatusIndicator(tool.status)}
                </div>
                {tool.requiresConfig && (
                  <span className="config-required" title="Configuration required">⚙️</span>
                )}
              </div>

              <p className="tool-description">{tool.description}</p>

              <div className="tool-features">
                <h4 className="features-title">Key Features:</h4>
                <ul className="features-list">
                  {tool.features.map((feature, index) => (
                    <li key={index} className="feature-item">{feature}</li>
                  ))}
                </ul>
              </div>

              {/* Tool-specific context inputs */}
              {tool.requiresConfig && (
                <div className="tool-config">
                  <h4 className="config-title">Configuration:</h4>
                  <div className="config-inputs">
                    {tool.id === 'yarax' && (
                      <input
                        type="text"
                        placeholder="Rules directory path..."
                        onChange={(e) => updateToolContext(tool.id, 'rulesPath', e.target.value)}
                        className="config-input"
                        aria-label="YARA-X rules directory"
                      />
                    )}
                    {tool.id === 'virustotal' && (
                      <input
                        type="password"
                        placeholder="API key..."
                        onChange={(e) => updateToolContext(tool.id, 'apiKey', e.target.value)}
                        className="config-input"
                        aria-label="VirusTotal API key"
                      />
                    )}
                    {(tool.id === 'nemesis' || tool.id === 'ghostwriter') && (
                      <input
                        type="text"
                        placeholder="Project name..."
                        onChange={(e) => updateToolContext(tool.id, 'project', e.target.value)}
                        className="config-input"
                        aria-label={`${tool.name} project name`}
                      />
                    )}
                    {tool.id === 'blackarch' && (
                      <select
                        onChange={(e) => updateToolContext(tool.id, 'mode', e.target.value)}
                        className="config-input"
                        aria-label="BlackArch operation mode"
                      >
                        <option value="">Select mode...</option>
                        <option value="pentest">Penetration Testing</option>
                        <option value="forensics">Digital Forensics</option>
                        <option value="reverse">Reverse Engineering</option>
                        <option value="exploit">Exploitation</option>
                      </select>
                    )}
                  </div>
                </div>
              )}
            </div>

            <div className="tool-actions">
              <button
                onClick={() => handleToolLaunch(tool)}
                disabled={tool.status !== 'online' || launchingTool === tool.id}
                className={`launch-btn ${tool.status}`}
                aria-label={`Launch ${tool.name}`}
              >
                {launchingTool === tool.id ? (
                  <>
                    <span className="loading-spinner" aria-hidden="true">⏳</span>
                    Launching...
                  </>
                ) : (
                  <>
                    <span className="launch-icon" aria-hidden="true">🚀</span>
                    Launch
                  </>
                )}
              </button>

              <button
                className="config-btn"
                onClick={() => {
                  // Handle tool configuration
                }}
                aria-label={`Configure ${tool.name}`}
                title="Tool Settings"
              >
                ⚙️
              </button>

              <button
                className="help-btn"
                onClick={() => {
                  // Handle help/documentation
                }}
                aria-label={`Help for ${tool.name}`}
                title="Documentation"
              >
                ❓
              </button>
            </div>
          </article>
        ))}
      </main>

      {filteredTools.length === 0 && (
        <div className="no-tools-message" role="status">
          <p>No tools found matching your search criteria.</p>
          <button 
            onClick={() => {
              setSearchQuery('');
              setSelectedCategory('all');
            }}
            className="clear-filters-btn"
          >
            Clear Filters
          </button>
        </div>
      )}
    </div>
  );
};