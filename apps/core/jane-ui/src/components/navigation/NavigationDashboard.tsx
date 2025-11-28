/**
 * Navigation Dashboard with Cognitive Load Integration
 * Comprehensive view combining heat maps, trends, and real-time indicators
 */

import { AnimatePresence, motion } from 'framer-motion';
import {
    Brain,
    Download,
    Filter,
    Maximize2,
    Minimize2,
    RefreshCw
} from 'lucide-react';
import { useEffect, useMemo, useState } from 'react';
import { useContextSwitchPrevention } from '../../services/navigation/contextSwitchPrevention';
import { useAdaptiveNavigation } from '../../services/navigation/useAdaptiveNavigation';
import { useGlobalStore, usePerformance } from '../../services/store';
import {
    CognitiveHeatMap,
    LoadTrendVisualizer,
    RealTimeLoadIndicator,
    type CognitiveLoadData,
    type ToolLoadVisualization
} from './CognitiveLoadVisualization';

interface NavigationDashboardProps {
  tools: Array<{
    id: string;
    name: string;
    display_name: string;
    domain: 'security' | 'productivity' | 'mtg' | 'infrastructure';
    status: 'active' | 'inactive' | 'maintenance';
    health_score: number;
    cognitive_load_score: number;
  }>;
  onToolSelect?: (toolId: string) => void;
  className?: string;
}

export function NavigationDashboard({ 
  tools, 
  onToolSelect, 
  className = '' 
}: NavigationDashboardProps) {
  const { performanceMetrics, cognitiveLoad } = usePerformance();
  const { activeTool, activeTools } = useGlobalStore();
  const { navigationState } = useAdaptiveNavigation();
  const { preventionState, getSwitchingStats } = useContextSwitchPrevention();

  const [selectedTool, setSelectedTool] = useState<string | null>(null);
  const [hoveredTool, setHoveredTool] = useState<string | null>(null);
  const [timeWindow, setTimeWindow] = useState(30); // minutes
  const [viewMode, setViewMode] = useState<'overview' | 'detailed' | 'analytics'>('overview');
  const [loadHistory, setLoadHistory] = useState<CognitiveLoadData[]>([]);
  const [isExpanded, setIsExpanded] = useState(false);
  const [showFilters, setShowFilters] = useState(false);
  const [domainFilter, setDomainFilter] = useState<string | null>(null);

  // Generate current cognitive load data
  const currentLoadData: CognitiveLoadData = useMemo(() => ({
    visual: Math.min(100, cognitiveLoad * 0.8 + Math.random() * 20),
    cognitive: cognitiveLoad,
    memory: Math.min(100, cognitiveLoad * 0.9 + Math.random() * 15),
    attention: Math.min(100, cognitiveLoad * 1.1 + Math.random() * 10),
    total: cognitiveLoad,
    timestamp: Date.now()
  }), [cognitiveLoad]);

  // Update load history
  useEffect(() => {
    const interval = setInterval(() => {
      setLoadHistory(prev => {
        const newHistory = [...prev, currentLoadData];
        // Keep only data within time window + buffer
        const cutoff = Date.now() - (timeWindow * 60 * 1000 * 1.5);
        return newHistory.filter(entry => entry.timestamp >= cutoff);
      });
    }, 30000); // Update every 30 seconds

    return () => clearInterval(interval);
  }, [currentLoadData, timeWindow]);

  // Generate tool visualization data
  const toolVisualizationData: ToolLoadVisualization[] = useMemo(() => {
    const switchingStats = getSwitchingStats();
    
    return tools.map(tool => {
      // Calculate access frequency from switching stats
      const toolSwitches = switchingStats.mostSwitchedTools.find(t => t.tool === tool.id);
      const accessFrequency = toolSwitches ? toolSwitches.count : 0;
      
      // Calculate load based on tool complexity and current context
      const baseLoad = tool.cognitive_load_score * 10; // Scale to 0-100
      const contextualLoad = activeTool === tool.id ? cognitiveLoad : baseLoad;
      
      // Determine trend based on recent performance
      const recentMetrics = performanceMetrics
        .filter(m => m.toolName === tool.id)
        .slice(-5);
      
      let trend: 'increasing' | 'decreasing' | 'stable' = 'stable';
      if (recentMetrics.length >= 3) {
        const avgEarly = recentMetrics.slice(0, 2).reduce((sum, m) => sum + m.responseTime, 0) / 2;
        const avgRecent = recentMetrics.slice(-2).reduce((sum, m) => sum + m.responseTime, 0) / 2;
        
        if (avgRecent > avgEarly * 1.2) trend = 'increasing';
        else if (avgRecent < avgEarly * 0.8) trend = 'decreasing';
      }

      return {
        toolId: tool.id,
        toolName: tool.display_name,
        domain: tool.domain,
        currentLoad: Math.min(100, contextualLoad),
        averageLoad: baseLoad,
        peakLoad: Math.min(100, baseLoad * 1.5),
        accessFrequency,
        lastUsed: activeTools.find(t => t.id === tool.id)?.lastUsed?.getTime() || 0,
        trend
      };
    });
  }, [tools, activeTool, cognitiveLoad, performanceMetrics, activeTools, getSwitchingStats]);

  // Filter tools by domain if filter is active
  const filteredTools = useMemo(() => {
    return domainFilter 
      ? toolVisualizationData.filter(tool => tool.domain === domainFilter)
      : toolVisualizationData;
  }, [toolVisualizationData, domainFilter]);

  const handleToolHover = (toolId: string | null) => {
    setHoveredTool(toolId);
  };

  const handleToolSelect = (toolId: string) => {
    setSelectedTool(toolId);
    onToolSelect?.(toolId);
  };

  const exportData = () => {
    const exportData = {
      timestamp: new Date().toISOString(),
      currentLoad: currentLoadData,
      loadHistory,
      toolData: filteredTools,
      switchingStats: getSwitchingStats(),
      navigationState
    };
    
    const blob = new Blob([JSON.stringify(exportData, null, 2)], { 
      type: 'application/json' 
    });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `cognitive-load-data-${Date.now()}.json`;
    a.click();
    URL.revokeObjectURL(url);
  };

  const refreshData = () => {
    setLoadHistory([]);
    setSelectedTool(null);
    setHoveredTool(null);
  };

  const thresholds = {
    optimal: 60,
    warning: 75, 
    critical: 90
  };

  const domains = ['security', 'productivity', 'mtg', 'infrastructure'];

  return (
    <div className={`navigation-dashboard ${className}`}>
      <motion.div
        layout
        className={`bg-gray-50 rounded-lg border border-gray-200 transition-all duration-300 ${
          isExpanded ? 'fixed inset-4 z-50' : 'relative'
        }`}
      >
        {/* Header */}
        <div className="flex items-center justify-between p-4 border-b border-gray-200 bg-white rounded-t-lg">
          <div className="flex items-center gap-3">
            <Brain className="w-5 h-5 text-blue-600" />
            <h2 className="text-lg font-semibold text-gray-900">
              Cognitive Navigation Dashboard
            </h2>
            {hoveredTool && (
              <motion.div
                initial={{ opacity: 0, scale: 0.8 }}
                animate={{ opacity: 1, scale: 1 }}
                className="px-2 py-1 bg-blue-100 text-blue-800 rounded text-sm"
              >
                {toolVisualizationData.find(t => t.toolId === hoveredTool)?.toolName}
              </motion.div>
            )}
          </div>
          
          <div className="flex items-center gap-2">
            {/* View mode selector */}
            <div className="flex border border-gray-300 rounded overflow-hidden">
              {[
                { mode: 'overview' as const, label: 'Overview' },
                { mode: 'detailed' as const, label: 'Detailed' },
                { mode: 'analytics' as const, label: 'Analytics' }
              ].map(({ mode, label }) => (
                <button
                  key={mode}
                  onClick={() => setViewMode(mode)}
                  className={`px-3 py-1 text-sm ${
                    viewMode === mode 
                      ? 'bg-blue-500 text-white' 
                      : 'bg-white text-gray-600 hover:bg-gray-50'
                  }`}
                >
                  {label}
                </button>
              ))}
            </div>
            
            {/* Controls */}
            <button
              onClick={() => setShowFilters(!showFilters)}
              className={`p-2 rounded ${
                showFilters ? 'bg-blue-100 text-blue-600' : 'text-gray-600 hover:bg-gray-100'
              }`}
              title="Filters"
            >
              <Filter className="w-4 h-4" />
            </button>
            
            <button
              onClick={refreshData}
              className="p-2 text-gray-600 hover:bg-gray-100 rounded"
              title="Refresh data"
            >
              <RefreshCw className="w-4 h-4" />
            </button>
            
            <button
              onClick={exportData}
              className="p-2 text-gray-600 hover:bg-gray-100 rounded"
              title="Export data"
            >
              <Download className="w-4 h-4" />
            </button>
            
            <button
              onClick={() => setIsExpanded(!isExpanded)}
              className="p-2 text-gray-600 hover:bg-gray-100 rounded"
              title={isExpanded ? 'Minimize' : 'Expand'}
            >
              {isExpanded ? <Minimize2 className="w-4 h-4" /> : <Maximize2 className="w-4 h-4" />}
            </button>
          </div>
        </div>

        {/* Filters */}
        <AnimatePresence>
          {showFilters && (
            <motion.div
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: 'auto' }}
              exit={{ opacity: 0, height: 0 }}
              className="px-4 py-3 bg-gray-50 border-b border-gray-200"
            >
              <div className="flex items-center gap-4">
                <span className="text-sm font-medium text-gray-700">Filters:</span>
                
                <div className="flex items-center gap-2">
                  <span className="text-sm text-gray-600">Domain:</span>
                  <select
                    value={domainFilter || ''}
                    onChange={(e) => setDomainFilter(e.target.value || null)}
                    className="text-sm border border-gray-300 rounded px-2 py-1"
                  >
                    <option value="">All Domains</option>
                    {domains.map(domain => (
                      <option key={domain} value={domain} className="capitalize">
                        {domain}
                      </option>
                    ))}
                  </select>
                </div>
                
                <div className="flex items-center gap-2">
                  <span className="text-sm text-gray-600">Time Window:</span>
                  <select
                    value={timeWindow}
                    onChange={(e) => setTimeWindow(Number(e.target.value))}
                    className="text-sm border border-gray-300 rounded px-2 py-1"
                  >
                    <option value={15}>15 minutes</option>
                    <option value={30}>30 minutes</option>
                    <option value={60}>1 hour</option>
                    <option value={120}>2 hours</option>
                  </select>
                </div>
              </div>
            </motion.div>
          )}
        </AnimatePresence>

        {/* Dashboard Content */}
        <div className="p-4 space-y-6 overflow-auto" style={{ 
          maxHeight: isExpanded ? 'calc(100vh - 200px)' : '600px' 
        }}>
          {viewMode === 'overview' && (
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              {/* Real-time indicator */}
              <div className="lg:col-span-1">
                <RealTimeLoadIndicator
                  currentLoad={currentLoadData}
                  thresholds={thresholds}
                />
              </div>
              
              {/* Heat map */}
              <div className="lg:col-span-2">
                <CognitiveHeatMap
                  tools={filteredTools}
                  selectedTool={selectedTool}
                  onToolHover={handleToolHover}
                  onToolSelect={handleToolSelect}
                />
              </div>
            </div>
          )}

          {viewMode === 'detailed' && (
            <div className="space-y-6">
              {/* Real-time and trend side by side */}
              <div className="grid grid-cols-1 xl:grid-cols-2 gap-6">
                <RealTimeLoadIndicator
                  currentLoad={currentLoadData}
                  thresholds={thresholds}
                />
                <LoadTrendVisualizer
                  loadHistory={loadHistory}
                  timeWindow={timeWindow}
                />
              </div>
              
              {/* Full-width heat map */}
              <CognitiveHeatMap
                tools={filteredTools}
                selectedTool={selectedTool}
                onToolHover={handleToolHover}
                onToolSelect={handleToolSelect}
              />
            </div>
          )}

          {viewMode === 'analytics' && (
            <div className="space-y-6">
              {/* Trend visualization */}
              <LoadTrendVisualizer
                loadHistory={loadHistory}
                timeWindow={timeWindow}
              />
              
              {/* Analytics cards */}
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                <div className="bg-white rounded-lg border border-gray-200 p-4">
                  <div className="text-sm text-gray-600 mb-1">Avg Load</div>
                  <div className="text-2xl font-bold text-gray-900">
                    {Math.round(loadHistory.length > 0 ? 
                      loadHistory.reduce((sum, h) => sum + h.total, 0) / loadHistory.length : 
                      currentLoadData.total
                    )}%
                  </div>
                </div>
                
                <div className="bg-white rounded-lg border border-gray-200 p-4">
                  <div className="text-sm text-gray-600 mb-1">Peak Load</div>
                  <div className="text-2xl font-bold text-red-600">
                    {Math.round(Math.max(...loadHistory.map(h => h.total), currentLoadData.total))}%
                  </div>
                </div>
                
                <div className="bg-white rounded-lg border border-gray-200 p-4">
                  <div className="text-sm text-gray-600 mb-1">Context Switches</div>
                  <div className="text-2xl font-bold text-orange-600">
                    {preventionState.recentSwitches.length}
                  </div>
                </div>
                
                <div className="bg-white rounded-lg border border-gray-200 p-4">
                  <div className="text-sm text-gray-600 mb-1">Active Tools</div>
                  <div className="text-2xl font-bold text-green-600">
                    {filteredTools.filter(t => t.accessFrequency > 0).length}
                  </div>
                </div>
              </div>
              
              {/* Detailed heat map */}
              <CognitiveHeatMap
                tools={filteredTools}
                selectedTool={selectedTool}
                onToolHover={handleToolHover}
                onToolSelect={handleToolSelect}
              />
            </div>
          )}

          {/* Selected tool details */}
          <AnimatePresence>
            {selectedTool && (
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -20 }}
                className="bg-white rounded-lg border border-gray-200 p-4"
              >
                <div className="flex items-center justify-between mb-3">
                  <h3 className="font-semibold text-gray-900">
                    Tool Details: {toolVisualizationData.find(t => t.toolId === selectedTool)?.toolName}
                  </h3>
                  <button
                    onClick={() => setSelectedTool(null)}
                    className="text-gray-400 hover:text-gray-600"
                  >
                    ×
                  </button>
                </div>
                
                {(() => {
                  const tool = toolVisualizationData.find(t => t.toolId === selectedTool);
                  if (!tool) return null;
                  
                  return (
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
                      <div>
                        <div className="text-gray-600">Current Load</div>
                        <div className="font-semibold">{Math.round(tool.currentLoad)}%</div>
                      </div>
                      <div>
                        <div className="text-gray-600">Average Load</div>
                        <div className="font-semibold">{Math.round(tool.averageLoad)}%</div>
                      </div>
                      <div>
                        <div className="text-gray-600">Access Frequency</div>
                        <div className="font-semibold">{tool.accessFrequency}</div>
                      </div>
                      <div>
                        <div className="text-gray-600">Domain</div>
                        <div className="font-semibold capitalize">{tool.domain}</div>
                      </div>
                    </div>
                  );
                })()}
              </motion.div>
            )}
          </AnimatePresence>
        </div>
      </motion.div>
    </div>
  );
}