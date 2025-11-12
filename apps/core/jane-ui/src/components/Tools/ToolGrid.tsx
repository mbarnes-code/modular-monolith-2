/**
 * Tool Grid Component - Task T045 COMPLETED
 * 
 * Displays all 37 executive function tools in grid format with executive function accommodations
 */

'use client';

import React, { useMemo, useState } from 'react';

interface Tool {
  id: string;
  name: string;
  display_name: string;
  description: string;
  domain: 'security' | 'productivity' | 'mtg' | 'infrastructure';
  url?: string;
  status: 'active' | 'inactive' | 'maintenance';
  health_score: number;
  last_used?: string;
  integration_status: 'integrated' | 'partial' | 'pending';
  cognitive_load_score: number;
  executive_function_features: string[];  
  constitutional_compliance: boolean;
  performance_metrics?: {
    avg_response_time_ms: number;
    uptime_percentage: number;
    last_health_check: string;
  };
}

interface ToolGridProps {
  tools: Tool[];
  onToolClick: (tool: Tool) => void;
  layout: 'grid' | 'list';
  executiveFunctionEnabled: boolean;
  showPerformanceMetrics?: boolean;
  cognitiveLoadFilter?: 'low' | 'medium' | 'high' | null;
  domainFilter?: 'security' | 'productivity' | 'mtg' | 'infrastructure' | null;
  className?: string;
}

const DOMAIN_CONFIG = {
  security: { icon: '🛡️', count: 13, target: 1000 },
  productivity: { icon: '💼', count: 8, target: 2000 },
  mtg: { icon: '🎮', count: 4, target: 3000 },
  infrastructure: { icon: '⚙️', count: 12, target: 5000 }
} as const;

const ToolCard: React.FC<{
  tool: Tool;
  onClick: () => void;
  layout: 'grid' | 'list';
  executiveFunctionEnabled: boolean;
  showPerformanceMetrics: boolean;
}> = ({ tool, onClick, layout, executiveFunctionEnabled, showPerformanceMetrics }) => {
  const [showDetails, setShowDetails] = useState(false);
  
  const statusClass = {
    active: 'text-green-600 bg-green-50',
    maintenance: 'text-amber-600 bg-amber-50',
    inactive: 'text-gray-600 bg-gray-50'
  }[tool.status];

  const healthClass = tool.health_score >= 90 ? 'text-green-600' :
                     tool.health_score >= 70 ? 'text-amber-600' : 'text-red-600';

  const cognitiveLoad = tool.cognitive_load_score <= 3 ? 'Low' :
                       tool.cognitive_load_score <= 6 ? 'Medium' : 'High';

  if (layout === 'list') {
    return (
      <div 
        className="bg-white border rounded-lg p-4 hover:shadow-md cursor-pointer"
        onClick={onClick}
        role="button"
        tabIndex={0}
        onKeyDown={(e) => e.key === 'Enter' && onClick()}
      >
        <div className="flex justify-between items-start">
          <div className="flex-1">
            <div className="flex items-center gap-2 mb-1">
              <span className="text-lg">{DOMAIN_CONFIG[tool.domain].icon}</span>
              <h3 className="font-medium text-gray-900">{tool.display_name}</h3>
              <span className={`px-2 py-1 text-xs rounded ${statusClass}`}>
                {tool.status}
              </span>
              {tool.constitutional_compliance && <span className="text-green-500">✓</span>}
            </div>
            <p className="text-sm text-gray-600 mb-2">{tool.description}</p>
            <div className="flex gap-2">
              <span className="px-2 py-1 text-xs bg-gray-100 rounded capitalize">
                {tool.domain}
              </span>
              <span className="px-2 py-1 text-xs bg-blue-100 rounded">
                {tool.integration_status}
              </span>
            </div>
          </div>
          
          {showPerformanceMetrics && (
            <div className="text-sm text-right">
              <div className={`${healthClass} mb-1`}>♥ {tool.health_score}%</div>
              {tool.performance_metrics && (
                <div className="text-gray-600">
                  ⏱ {tool.performance_metrics.avg_response_time_ms}ms
                </div>
              )}
            </div>
          )}
          
          <button 
            onClick={(e) => { e.stopPropagation(); setShowDetails(!showDetails); }}
            className="ml-2 text-gray-400 hover:text-gray-600"
          >
            ℹ
          </button>
        </div>
        
        {showDetails && (
          <div className="mt-4 pt-4 border-t border-gray-100">
            <div className="grid grid-cols-2 gap-4 text-sm mb-3">
              <div>Domain Tools: {DOMAIN_CONFIG[tool.domain].count}</div>
              <div>Target: &lt;{DOMAIN_CONFIG[tool.domain].target}ms</div>
            </div>
            {executiveFunctionEnabled && (
              <div className="mb-2">
                <span className="text-xs text-gray-500">Cognitive Load: </span>
                <span className="text-xs px-2 py-1 bg-gray-100 rounded">{cognitiveLoad}</span>
              </div>
            )}
            {tool.executive_function_features.length > 0 && (
              <div className="flex flex-wrap gap-1">
                {tool.executive_function_features.map((feature, idx) => (
                  <span key={idx} className="px-2 py-1 text-xs bg-blue-50 text-blue-700 rounded">
                    {feature}
                  </span>
                ))}
              </div>
            )}
          </div>
        )}
      </div>
    );
  }

  // Grid layout
  return (
    <div 
      className="bg-white border rounded-lg p-6 hover:shadow-md cursor-pointer"
      onClick={onClick}
      role="button"
      tabIndex={0}
      onKeyDown={(e) => e.key === 'Enter' && onClick()}
    >
      <div className="flex justify-between items-start mb-4">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 bg-gray-100 rounded-lg flex items-center justify-center">
            <span className="text-lg">{DOMAIN_CONFIG[tool.domain].icon}</span>
          </div>
          <div>
            <h3 className="font-medium text-gray-900">{tool.display_name}</h3>
            <p className="text-sm text-gray-500 capitalize">{tool.domain}</p>
          </div>
        </div>
        <div className="flex items-center gap-1">
          <div className={`w-2 h-2 rounded-full ${
            tool.status === 'active' ? 'bg-green-400' :
            tool.status === 'maintenance' ? 'bg-amber-400' : 'bg-gray-400'
          }`} />
          {tool.constitutional_compliance && <span className="text-green-500 text-sm">✓</span>}
        </div>
      </div>

      <p className="text-sm text-gray-600 mb-4 line-clamp-2">{tool.description}</p>

      <div className="space-y-3 mb-4">
        <div className="flex justify-between text-sm">
          <span className="text-gray-500">Health Score</span>
          <span className={`${healthClass} font-medium`}>♥ {tool.health_score}%</span>
        </div>
        
        {executiveFunctionEnabled && (
          <div className="flex justify-between text-sm">
            <span className="text-gray-500">Cognitive Load</span>
            <span className="px-2 py-1 text-xs bg-gray-100 rounded">{cognitiveLoad}</span>
          </div>
        )}
        
        {showPerformanceMetrics && tool.performance_metrics && (
          <div className="flex justify-between text-sm">
            <span className="text-gray-500">Response Time</span>
            <span className="text-gray-600">⏱ {tool.performance_metrics.avg_response_time_ms}ms</span>
          </div>
        )}
      </div>

      <div className="flex justify-between items-center pt-3 border-t border-gray-100">
        <div className="flex items-center gap-2">
          <div className={`w-2 h-2 rounded-full ${
            tool.integration_status === 'integrated' ? 'bg-green-400' :
            tool.integration_status === 'partial' ? 'bg-amber-400' : 'bg-gray-400'
          }`} />
          <span className="text-xs text-gray-500">{tool.integration_status}</span>
        </div>
        {tool.last_used && (
          <span className="text-xs text-gray-400">
            Used {new Date(tool.last_used).toLocaleDateString()}
          </span>
        )}
      </div>

      {executiveFunctionEnabled && tool.executive_function_features.length > 0 && (
        <div className="mt-3 pt-3 border-t border-gray-100">
          <div className="flex flex-wrap gap-1">
            {tool.executive_function_features.slice(0, 2).map((feature, idx) => (
              <span key={idx} className="px-2 py-1 text-xs bg-blue-50 text-blue-700 rounded">
                {feature}
              </span>
            ))}
            {tool.executive_function_features.length > 2 && (
              <span className="px-2 py-1 text-xs bg-gray-100 text-gray-600 rounded">
                +{tool.executive_function_features.length - 2} more
              </span>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export const ToolGrid: React.FC<ToolGridProps> = ({
  tools,
  onToolClick,
  layout,
  executiveFunctionEnabled,
  showPerformanceMetrics = false,
  cognitiveLoadFilter = null,
  domainFilter = null,
  className = ''
}) => {
  const filteredTools = useMemo(() => {
    let filtered = tools;
    
    if (cognitiveLoadFilter) {
      filtered = filtered.filter(tool => {
        const load = tool.cognitive_load_score <= 3 ? 'low' :
                    tool.cognitive_load_score <= 6 ? 'medium' : 'high';
        return load === cognitiveLoadFilter;
      });
    }
    
    if (domainFilter) {
      filtered = filtered.filter(tool => tool.domain === domainFilter);
    }
    
    return filtered;
  }, [tools, cognitiveLoadFilter, domainFilter]);

  const domainStats = useMemo(() => {
    return Object.entries(DOMAIN_CONFIG).map(([domain, config]) => ({
      domain: domain as Tool['domain'],
      ...config,
      active: filteredTools.filter(t => t.domain === domain && t.status === 'active').length,
      total: filteredTools.filter(t => t.domain === domain).length,
      health: Math.round(
        filteredTools
          .filter(t => t.domain === domain)
          .reduce((sum, t) => sum + t.health_score, 0) / 
        Math.max(1, filteredTools.filter(t => t.domain === domain).length)
      )
    }));
  }, [filteredTools]);

  if (filteredTools.length === 0) {
    return (
      <div className={`text-center py-12 ${className}`}>
        <div className="text-6xl mb-4">⚙️</div>
        <h3 className="text-lg font-medium text-gray-900 mb-2">No Tools Found</h3>
        <p className="text-gray-500">
          {cognitiveLoadFilter || domainFilter ? 'No tools match the current filters.' : 'No tools are available.'}
        </p>
      </div>
    );
  }

  return (
    <div className={`tool-grid ${className}`}>
      {/* Domain Summary */}
      {!domainFilter && (
        <div className="mb-6 p-4 bg-gray-50 rounded-lg">
          <h3 className="text-sm font-medium text-gray-900 mb-3">
            37-Tool Domain Distribution (Constitutional Compliance)
          </h3>
          <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
            {domainStats.map((stat) => (
              <div key={stat.domain} className="text-center">
                <div className="w-8 h-8 mx-auto mb-2 bg-white rounded-lg border flex items-center justify-center">
                  <span className="text-sm">{stat.icon}</span>
                </div>
                <div className="text-sm">
                  <div className="font-medium capitalize">{stat.domain}</div>
                  <div className="text-gray-500">{stat.active} / {stat.count} active</div>
                  <div className="text-xs text-gray-400">{stat.health}% health</div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Tools Grid/List */}
      <div className={
        layout === 'grid' 
          ? 'grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6'
          : 'space-y-4'
      }>
        {filteredTools.map((tool) => (
          <ToolCard
            key={tool.id}
            tool={tool}
            onClick={() => onToolClick(tool)}
            layout={layout}
            executiveFunctionEnabled={executiveFunctionEnabled}
            showPerformanceMetrics={showPerformanceMetrics}
          />
        ))}
      </div>

      {/* Summary Stats */}
      <div className="mt-8 pt-6 border-t border-gray-200">
        <div className="flex justify-between text-sm text-gray-500">
          <div className="flex items-center gap-4">
            <span>Showing {filteredTools.length} of {tools.length} tools</span>
            <span className="flex items-center gap-1">
              <span>📊</span>
              <span>
                {Math.round(
                  filteredTools.reduce((sum, t) => sum + t.health_score, 0) / 
                  Math.max(1, filteredTools.length)
                )}% avg health
              </span>
            </span>
          </div>
          <div className="flex items-center gap-4">
            {executiveFunctionEnabled && (
              <span className="flex items-center gap-1">
                <span className="text-green-500">✓</span>
                <span>Executive function optimized</span>
              </span>
            )}
            <span className="flex items-center gap-1">
              <span className="text-blue-500">✓</span>
              <span>Constitutional compliance active</span>
            </span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ToolGrid;