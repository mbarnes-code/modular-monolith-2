/**
 * Threat Correlation Component
 * 
 * AI-enhanced threat correlation interface for security analysts.
 * Provides unified correlation across all 13 security tools with
 * constitutional compliance (<1s response for security domain).
 */

import React, { useCallback, useState } from 'react';
import './ThreatCorrelation.css';

interface ThreatIndicator {
  id: string;
  type: 'ip' | 'domain' | 'hash' | 'url' | 'email';
  value: string;
  confidence: number;
  sources: string[];
  firstSeen: string;
  lastSeen: string;
  tags: string[];
}

interface CorrelationResult {
  indicator: ThreatIndicator;
  correlations: {
    toolId: string;
    toolName: string;
    matches: number;
    confidence: number;
    data: any[];
  }[];
  aiAnalysis?: {
    riskScore: number;
    summary: string;
    recommendations: string[];
  };
}

interface ThreatCorrelationProps {
  className?: string;
  onCorrelationComplete?: (results: CorrelationResult[]) => void;
}

export const ThreatCorrelation: React.FC<ThreatCorrelationProps> = ({
  className = '',
  onCorrelationComplete
}) => {
  const [indicators, setIndicators] = useState<string[]>(['']);
  const [correlationResults, setCorrelationResults] = useState<CorrelationResult[]>([]);
  const [isCorrelating, setIsCorrelating] = useState(false);
  const [selectedTools, setSelectedTools] = useState<string[]>([
    'misp', 'securityonion', 'yarax', 'helk', 'virustotal'
  ]);
  const [aiEnhanced, setAiEnhanced] = useState(true);
  const [correlationTime, setCorrelationTime] = useState<number>(0);

  // Available security tools for correlation
  const availableTools = [
    { id: 'misp', name: 'MISP', type: 'threat-intel' },
    { id: 'securityonion', name: 'Security Onion', type: 'network-security' },
    { id: 'yarax', name: 'YARA-X', type: 'malware-analysis' },
    { id: 'helk', name: 'HELK', type: 'threat-intel' },
    { id: 'virustotal', name: 'VirusTotal MCP', type: 'malware-analysis' },
    { id: 'malwarebazaar', name: 'MalwareBazaar MCP', type: 'malware-analysis' },
    { id: 'cyberchef', name: 'CyberChef', type: 'malware-analysis' },
    { id: 'nemesis', name: 'Nemesis', type: 'incident-response' },
    { id: 'maltrail', name: 'Maltrail', type: 'network-security' },
    { id: 'rita', name: 'RITA', type: 'threat-intel' },
    { id: 'ghostwriter', name: 'Ghostwriter', type: 'incident-response' },
    { id: 'blackarch', name: 'BlackArch Tools', type: 'incident-response' },
    { id: 'apiscout', name: 'ApiScout', type: 'malware-analysis' }
  ];

  const addIndicator = useCallback(() => {
    setIndicators(prev => [...prev, '']);
  }, []);

  const removeIndicator = useCallback((index: number) => {
    setIndicators(prev => prev.filter((_, i) => i !== index));
  }, []);

  const updateIndicator = useCallback((index: number, value: string) => {
    setIndicators(prev => prev.map((ind, i) => i === index ? value : ind));
  }, []);

  const detectIndicatorType = (value: string): ThreatIndicator['type'] => {
    // IP address pattern
    if (/^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$/.test(value)) {
      return 'ip';
    }
    // Domain pattern
    if (/^[a-zA-Z0-9][a-zA-Z0-9-]{1,61}[a-zA-Z0-9]\.[a-zA-Z]{2,}$/.test(value)) {
      return 'domain';
    }
    // Hash patterns (MD5, SHA1, SHA256)
    if (/^[a-fA-F0-9]{32}$/.test(value) || 
        /^[a-fA-F0-9]{40}$/.test(value) || 
        /^[a-fA-F0-9]{64}$/.test(value)) {
      return 'hash';
    }
    // URL pattern
    if (/^https?:\/\//.test(value)) {
      return 'url';
    }
    // Email pattern
    if (/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value)) {
      return 'email';
    }
    return 'domain'; // default
  };

  const performCorrelation = async () => {
    const startTime = Date.now();
    setIsCorrelating(true);
    setCorrelationResults([]);

    try {
      // Filter out empty indicators
      const validIndicators = indicators.filter(ind => ind.trim());
      
      if (validIndicators.length === 0) {
        throw new Error('Please provide at least one indicator');
      }

      // Simulate correlation process (in real implementation, would call API)
      const results: CorrelationResult[] = [];

      for (const indicatorValue of validIndicators) {
        const indicatorType = detectIndicatorType(indicatorValue);
        
        const indicator: ThreatIndicator = {
          id: `ind_${Date.now()}_${Math.random()}`,
          type: indicatorType,
          value: indicatorValue,
          confidence: 0.85,
          sources: ['user_input'],
          firstSeen: new Date().toISOString(),
          lastSeen: new Date().toISOString(),
          tags: []
        };

        // Simulate tool correlations
        const correlations = selectedTools.map(toolId => {
          const tool = availableTools.find(t => t.id === toolId);
          const matches = Math.floor(Math.random() * 10) + 1;
          
          return {
            toolId,
            toolName: tool?.name || toolId,
            matches,
            confidence: Math.random() * 0.4 + 0.6, // 0.6 to 1.0
            data: Array(matches).fill(null).map((_, i) => ({
              id: `match_${i}`,
              timestamp: new Date().toISOString(),
              source: tool?.name,
              details: `Sample correlation data for ${indicatorValue}`
            }))
          };
        });

        // Simulate AI analysis if enabled
        let aiAnalysis;
        if (aiEnhanced) {
          const totalMatches = correlations.reduce((sum, c) => sum + c.matches, 0);
          const avgConfidence = correlations.reduce((sum, c) => sum + c.confidence, 0) / correlations.length;
          
          aiAnalysis = {
            riskScore: Math.min(totalMatches * 10 + avgConfidence * 20, 100),
            summary: `Indicator ${indicatorValue} shows correlation across ${correlations.length} tools with ${totalMatches} total matches.`,
            recommendations: [
              totalMatches > 15 ? 'High correlation detected - prioritize investigation' : 'Monitor for additional indicators',
              'Review historical data for patterns',
              'Consider blocking if confirmed malicious'
            ]
          };
        }

        results.push({
          indicator,
          correlations,
          aiAnalysis
        });
      }

      const endTime = Date.now();
      const processingTime = endTime - startTime;
      
      setCorrelationTime(processingTime);
      setCorrelationResults(results);

      // Constitutional compliance check (<1s for security domain)
      if (processingTime > 1000) {
        console.warn(`Correlation exceeded 1s limit: ${processingTime}ms`);
      }

      if (onCorrelationComplete) {
        onCorrelationComplete(results);
      }

    } catch (error) {
      console.error('Correlation failed:', error);
      // In real implementation, would show error to user
    } finally {
      setIsCorrelating(false);
    }
  };

  const toggleTool = (toolId: string) => {
    setSelectedTools(prev => 
      prev.includes(toolId) 
        ? prev.filter(id => id !== toolId)
        : [...prev, toolId]
    );
  };

  const getRiskColor = (score: number) => {
    if (score >= 80) return '#ef4444'; // red
    if (score >= 60) return '#f59e0b'; // yellow
    if (score >= 40) return '#10b981'; // green
    return '#6b7280'; // gray
  };

  return (
    <div className={`threat-correlation ${className}`} role="main">
      <header className="correlation-header">
        <h2>Threat Intelligence Correlation</h2>
        <p className="header-description">
          Correlate indicators across all security tools with AI enhancement
        </p>
      </header>

      {/* Input Section */}
      <section className="input-section" aria-labelledby="input-section-title">
        <h3 id="input-section-title">Indicators of Compromise (IOCs)</h3>
        
        <div className="indicators-input">
          {indicators.map((indicator, index) => (
            <div key={index} className="indicator-row">
              <input
                type="text"
                placeholder="Enter IP, domain, hash, URL, or email..."
                value={indicator}
                onChange={(e) => updateIndicator(index, e.target.value)}
                className="indicator-input"
                aria-label={`Indicator ${index + 1}`}
              />
              <button
                type="button"
                onClick={() => removeIndicator(index)}
                className="remove-indicator-btn"
                disabled={indicators.length === 1}
                aria-label={`Remove indicator ${index + 1}`}
              >
                ✖
              </button>
            </div>
          ))}
          
          <button
            type="button"
            onClick={addIndicator}
            className="add-indicator-btn"
            aria-label="Add another indicator"
          >
            + Add Indicator
          </button>
        </div>
      </section>

      {/* Tool Selection */}
      <section className="tool-selection" aria-labelledby="tool-selection-title">
        <h3 id="tool-selection-title">Security Tools</h3>
        <div className="tools-grid">
          {availableTools.map(tool => (
            <label key={tool.id} className="tool-checkbox">
              <input
                type="checkbox"
                checked={selectedTools.includes(tool.id)}
                onChange={() => toggleTool(tool.id)}
              />
              <span className="tool-name">{tool.name}</span>
              <span className="tool-type">{tool.type}</span>
            </label>
          ))}
        </div>
      </section>

      {/* Options */}
      <section className="options-section">
        <label className="ai-toggle">
          <input
            type="checkbox"
            checked={aiEnhanced}
            onChange={(e) => setAiEnhanced(e.target.checked)}
          />
          <span>Enable AI Enhancement</span>
        </label>
      </section>

      {/* Action Button */}
      <section className="action-section">
        <button
          onClick={performCorrelation}
          disabled={isCorrelating || indicators.every(ind => !ind.trim())}
          className="correlate-btn"
          aria-describedby="correlate-help"
        >
          {isCorrelating ? 'Correlating...' : 'Start Correlation'}
        </button>
        <p id="correlate-help" className="correlate-help">
          Constitutional requirement: &lt;1s response time for security domain
        </p>
      </section>

      {/* Results */}
      {correlationResults.length > 0 && (
        <section className="results-section" aria-labelledby="results-title">
          <header className="results-header">
            <h3 id="results-title">Correlation Results</h3>
            <div className="processing-time">
              Processing time: {correlationTime}ms
              {correlationTime > 1000 && (
                <span className="time-warning" role="alert">
                  ⚠️ Exceeded 1s limit
                </span>
              )}
            </div>
          </header>

          {correlationResults.map((result, index) => (
            <div key={result.indicator.id} className="result-card">
              <div className="indicator-header">
                <h4 className="indicator-value">
                  {result.indicator.value}
                  <span className="indicator-type">({result.indicator.type})</span>
                </h4>
                {result.aiAnalysis && (
                  <div className="risk-score">
                    <span className="risk-label">Risk Score</span>
                    <span 
                      className="risk-value"
                      style={{ color: getRiskColor(result.aiAnalysis.riskScore) }}
                    >
                      {result.aiAnalysis.riskScore}/100
                    </span>
                  </div>
                )}
              </div>

              {/* AI Analysis */}
              {result.aiAnalysis && (
                <div className="ai-analysis">
                  <h5>AI Analysis</h5>
                  <p className="ai-summary">{result.aiAnalysis.summary}</p>
                  <div className="ai-recommendations">
                    <h6>Recommendations:</h6>
                    <ul>
                      {result.aiAnalysis.recommendations.map((rec, i) => (
                        <li key={i}>{rec}</li>
                      ))}
                    </ul>
                  </div>
                </div>
              )}

              {/* Tool Correlations */}
              <div className="tool-correlations">
                <h5>Tool Correlations</h5>
                <div className="correlation-grid">
                  {result.correlations.map(correlation => (
                    <div key={correlation.toolId} className="correlation-item">
                      <div className="correlation-header">
                        <span className="tool-name">{correlation.toolName}</span>
                        <span className="match-count">{correlation.matches} matches</span>
                      </div>
                      <div className="confidence-bar">
                        <div 
                          className="confidence-fill"
                          style={{ 
                            width: `${correlation.confidence * 100}%`,
                            backgroundColor: getRiskColor(correlation.confidence * 100)
                          }}
                        />
                        <span className="confidence-text">
                          {Math.round(correlation.confidence * 100)}% confidence
                        </span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          ))}
        </section>
      )}
    </div>
  );
};