/**
 * Enhanced Tool Switcher
 * Intelligent tool switching with cognitive load awareness and executive function support
 */

import React, { useState, useEffect, useRef, useMemo } from 'react';
import { useSharedContext } from '../../services/state/optimizedStateManager';
import { usePerformanceMonitor } from '../../services/performance/performanceMonitor';

interface Tool {
  id: string;
  name: string;
  domain: 'security' | 'productivity' | 'mtg' | 'ai' | 'infrastructure';
  description: string;
  complexity: number; // 1-100 cognitive load score
  lastUsed?: number;
  frequency: number; // Usage frequency score
  contextual?: boolean; // Whether it's contextually relevant
  estimatedSwitchTime: number; // Seconds to context switch
  prerequisites?: string[]; // Required tools/setup
  status: 'available' | 'loading' | 'error' | 'maintenance';
  icon: string;
  shortcut?: string;
}

interface ToolSwitcherProps {
  className?: string;
  maxRecentTools?: number;
  enablePredictive?: boolean;
  onToolSwitch?: (fromTool: string | null, toTool: string) => void;
}

// All 37 tools in the mental prosthetic platform
const ALL_TOOLS: Tool[] = [
  // Security Domain (13 tools)
  { id: 'misp', name: 'MISP', domain: 'security', description: 'Threat Intelligence Platform', complexity: 85, frequency: 0, estimatedSwitchTime: 15, status: 'available', icon: '🔍', shortcut: 'Ctrl+Shift+M' },
  { id: 'helk', name: 'HELK', domain: 'security', description: 'Hunting ELK Stack', complexity: 80, frequency: 0, estimatedSwitchTime: 20, status: 'available', icon: '🦌' },
  { id: 'securityonion', name: 'Security Onion', domain: 'security', description: 'Network Security Monitoring', complexity: 90, frequency: 0, estimatedSwitchTime: 25, status: 'available', icon: '🧅' },
  { id: 'maltrail', name: 'Maltrail', domain: 'security', description: 'Malicious Traffic Detection', complexity: 75, frequency: 0, estimatedSwitchTime: 12, status: 'available', icon: '🚨' },
  { id: 'yara-x', name: 'YARA-X', domain: 'security', description: 'Malware Identification Rules', complexity: 70, frequency: 0, estimatedSwitchTime: 8, status: 'available', icon: '🎯' },
  { id: 'cyberchef', name: 'CyberChef', domain: 'security', description: 'Data Analysis & Encoding', complexity: 60, frequency: 0, estimatedSwitchTime: 5, status: 'available', icon: '👨‍🍳', shortcut: 'Ctrl+Shift+C' },
  { id: 'nemesis', name: 'Nemesis', domain: 'security', description: 'Post-Exploitation Framework', complexity: 95, frequency: 0, estimatedSwitchTime: 30, status: 'available', icon: '⚡' },
  { id: 'rita', name: 'RITA', domain: 'security', description: 'Real Intelligence Threat Analytics', complexity: 85, frequency: 0, estimatedSwitchTime: 18, status: 'available', icon: '📊' },
  { id: 'blackarch', name: 'BlackArch Tools', domain: 'security', description: 'Penetration Testing Arsenal', complexity: 90, frequency: 0, estimatedSwitchTime: 20, status: 'available', icon: '🏴‍☠️' },
  { id: 'virustotal-mcp', name: 'VirusTotal MCP', domain: 'security', description: 'File & URL Analysis', complexity: 55, frequency: 0, estimatedSwitchTime: 8, status: 'available', icon: '🔬' },
  { id: 'malware-bazaar', name: 'MalwareBazaar MCP', domain: 'security', description: 'Malware Sample Database', complexity: 65, frequency: 0, estimatedSwitchTime: 10, status: 'available', icon: '💾' },
  { id: 'forensic-core', name: 'Forensic Core', domain: 'security', description: 'Digital Forensics Tools', complexity: 85, frequency: 0, estimatedSwitchTime: 22, status: 'available', icon: '🔍' },
  { id: 'intelligence', name: 'Intelligence Framework', domain: 'security', description: 'Threat Intelligence Analysis', complexity: 80, frequency: 0, estimatedSwitchTime: 15, status: 'available', icon: '🧠' },

  // Productivity Domain (8 tools)
  { id: 'n8n', name: 'n8n Workflows', domain: 'productivity', description: 'Workflow Automation Platform', complexity: 65, frequency: 0, estimatedSwitchTime: 12, status: 'available', icon: '🔗', shortcut: 'Ctrl+Shift+N' },
  { id: 'mealie', name: 'Mealie', domain: 'productivity', description: 'Recipe & Meal Planning', complexity: 40, frequency: 0, estimatedSwitchTime: 6, status: 'available', icon: '🍽️' },
  { id: 'dispatch', name: 'Dispatch', domain: 'productivity', description: 'Incident Management', complexity: 75, frequency: 0, estimatedSwitchTime: 15, status: 'available', icon: '🚨' },
  { id: 'actual-budget', name: 'Actual Budget', domain: 'productivity', description: 'Personal Finance Management', complexity: 55, frequency: 0, estimatedSwitchTime: 8, status: 'available', icon: '💰' },
  { id: 'firecrawl', name: 'Firecrawl', domain: 'productivity', description: 'Web Scraping & Data Extraction', complexity: 60, frequency: 0, estimatedSwitchTime: 10, status: 'available', icon: '🕷️' },
  { id: 'goose', name: 'Goose AI Assistant', domain: 'productivity', description: 'AI-Powered Task Automation', complexity: 50, frequency: 0, estimatedSwitchTime: 7, status: 'available', icon: '🪿' },
  { id: 'it-tools', name: 'IT Tools Collection', domain: 'productivity', description: 'Developer Utilities Hub', complexity: 45, frequency: 0, estimatedSwitchTime: 5, status: 'available', icon: '🔧' },
  { id: 'inspector', name: 'System Inspector', domain: 'productivity', description: 'System Monitoring & Analysis', complexity: 70, frequency: 0, estimatedSwitchTime: 12, status: 'available', icon: '📊' },

  // MTG Domain (4 tools)
  { id: 'commander-spellbook', name: 'Commander Spellbook', domain: 'mtg', description: 'MTG Combo Database', complexity: 70, frequency: 0, estimatedSwitchTime: 10, status: 'available', icon: '📚' },
  { id: 'mtg-commander-map', name: 'MTG Commander Map', domain: 'mtg', description: 'Commander Deck Visualization', complexity: 60, frequency: 0, estimatedSwitchTime: 8, status: 'available', icon: '🗺️' },
  { id: 'mtg-scripting-toolkit', name: 'MTG Scripting Toolkit', domain: 'mtg', description: 'Card Analysis & Automation', complexity: 80, frequency: 0, estimatedSwitchTime: 15, status: 'available', icon: '⚙️' },
  { id: 'mtg-card-analysis', name: 'MTG Card Analysis', domain: 'mtg', description: 'Statistical Card Analysis', complexity: 65, frequency: 0, estimatedSwitchTime: 12, status: 'available', icon: '📈' },

  // Infrastructure Domain (12 tools)
  { id: 'kong', name: 'Kong Gateway', domain: 'infrastructure', description: 'API Gateway Management', complexity: 85, frequency: 0, estimatedSwitchTime: 20, status: 'available', icon: '🌉' },
  { id: 'ghostwriter', name: 'Ghostwriter', domain: 'infrastructure', description: 'Report Generation Platform', complexity: 70, frequency: 0, estimatedSwitchTime: 12, status: 'available', icon: '👻' },
  { id: 'kasmvnc', name: 'KasmVNC', domain: 'infrastructure', description: 'Virtual Desktop Environment', complexity: 60, frequency: 0, estimatedSwitchTime: 25, status: 'available', icon: '🖥️' },
  { id: 'chroma-mcp', name: 'Chroma MCP Server', domain: 'ai', description: 'Vector Database Server', complexity: 75, frequency: 0, estimatedSwitchTime: 15, status: 'available', icon: '🎨' },
  { id: 'n8n-mcp-server', name: 'n8n MCP Server', domain: 'infrastructure', description: 'Workflow MCP Integration', complexity: 70, frequency: 0, estimatedSwitchTime: 10, status: 'available', icon: '🔌' },
  { id: 'firecrawl-mcp-server', name: 'Firecrawl MCP Server', domain: 'infrastructure', description: 'Web Scraping MCP Server', complexity: 65, frequency: 0, estimatedSwitchTime: 8, status: 'available', icon: '🕸️' },
  { id: 'filescope-mcp', name: 'FileScope MCP', domain: 'infrastructure', description: 'File Management Server', complexity: 55, frequency: 0, estimatedSwitchTime: 6, status: 'available', icon: '📁' },
  { id: 'spec-kit', name: 'Specification Kit', domain: 'infrastructure', description: 'Documentation & Specs', complexity: 45, frequency: 0, estimatedSwitchTime: 5, status: 'available', icon: '📋' },
  { id: 'lscript', name: 'LScript Engine', domain: 'infrastructure', description: 'Automation Scripting', complexity: 75, frequency: 0, estimatedSwitchTime: 12, status: 'available', icon: '📜' },
  { id: 'workflow-automation', name: 'Workflow Automation Hub', domain: 'infrastructure', description: 'Cross-Platform Automation', complexity: 80, frequency: 0, estimatedSwitchTime: 18, status: 'available', icon: '🔄' },
  { id: 'shared-services', name: 'Shared Services', domain: 'infrastructure', description: 'Common Platform Services', complexity: 50, frequency: 0, estimatedSwitchTime: 8, status: 'available', icon: '🤝' },
  { id: 'service-adapters', name: 'Service Adapters', domain: 'infrastructure', description: 'Integration Adapters', complexity: 70, frequency: 0, estimatedSwitchTime: 10, status: 'available', icon: '🔌' }
];

const DOMAIN_COLORS = {
  security: 'bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-300',
  productivity: 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-300',
  mtg: 'bg-purple-100 text-purple-800 dark:bg-purple-900/30 dark:text-purple-300',
  ai: 'bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-300',
  infrastructure: 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-300'
};

export function EnhancedToolSwitcher({ 
  className = '', 
  maxRecentTools = 8, 
  enablePredictive = true,
  onToolSwitch 
}: ToolSwitcherProps) {
  const sharedContext = useSharedContext();
  const { markUIInteraction, getCurrentMetrics } = usePerformanceMonitor();
  
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedDomain, setSelectedDomain] = useState<string>('all');
  const [isOpen, setIsOpen] = useState(false);
  const [selectedIndex, setSelectedIndex] = useState(0);
  const [toolUsageStats, setToolUsageStats] = useState<Record<string, { frequency: number; lastUsed: number }>>({});
  const [contextualSuggestions, setContextualSuggestions] = useState<string[]>([]);
  const [cognitiveLoadLimit, setCognitiveLoadLimit] = useState(75);
  const [showComplexityWarning, setShowComplexityWarning] = useState(false);
  
  const searchInputRef = useRef<HTMLInputElement>(null);
  const dropdownRef = useRef<HTMLDivElement>(null);

  // Enhanced tools with usage statistics
  const enhancedTools = useMemo(() => {
    return ALL_TOOLS.map(tool => ({
      ...tool,
      frequency: toolUsageStats[tool.id]?.frequency || 0,
      lastUsed: toolUsageStats[tool.id]?.lastUsed,
      contextual: contextualSuggestions.includes(tool.id)
    }));
  }, [toolUsageStats, contextualSuggestions]);

  // Filter and sort tools based on search and domain
  const filteredTools = useMemo(() => {
    let filtered = enhancedTools.filter(tool => {
      const matchesSearch = tool.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                           tool.description.toLowerCase().includes(searchTerm.toLowerCase()) ||
                           tool.domain.toLowerCase().includes(searchTerm.toLowerCase());
      
      const matchesDomain = selectedDomain === 'all' || tool.domain === selectedDomain;
      
      const withinComplexityLimit = tool.complexity <= cognitiveLoadLimit || tool.id === sharedContext.userFocus.currentTool;
      
      return matchesSearch && matchesDomain && withinComplexityLimit;
    });

    // Sort by relevance: contextual first, then by frequency, then by recent usage
    return filtered.sort((a, b) => {
      // Contextual suggestions first
      if (a.contextual && !b.contextual) return -1;
      if (!a.contextual && b.contextual) return 1;
      
      // Then by frequency
      if (a.frequency !== b.frequency) return b.frequency - a.frequency;
      
      // Then by recent usage
      const aLastUsed = a.lastUsed || 0;
      const bLastUsed = b.lastUsed || 0;
      if (aLastUsed !== bLastUsed) return bLastUsed - aLastUsed;
      
      // Finally by complexity (simpler tools first)
      return a.complexity - b.complexity;
    });
  }, [enhancedTools, searchTerm, selectedDomain, cognitiveLoadLimit, sharedContext.userFocus.currentTool, contextualSuggestions]);

  // Get recent tools
  const recentTools = useMemo(() => {
    const recent = enhancedTools
      .filter(tool => tool.lastUsed && tool.lastUsed > Date.now() - 24 * 60 * 60 * 1000) // Last 24 hours
      .sort((a, b) => (b.lastUsed || 0) - (a.lastUsed || 0))
      .slice(0, maxRecentTools);
    
    return recent;
  }, [enhancedTools, maxRecentTools]);

  // Predictive suggestions based on current context
  useEffect(() => {
    if (!enablePredictive) return;
    
    const currentTool = sharedContext.userFocus.currentTool;
    const currentDomain = enhancedTools.find(t => t.id === currentTool)?.domain;
    
    if (currentDomain) {
      // Suggest tools from same domain or complementary tools
      const suggestions = [];
      
      // Same domain tools (for workflow continuity)
      const sameDomainTools = enhancedTools
        .filter(t => t.domain === currentDomain && t.id !== currentTool)
        .slice(0, 3);
      suggestions.push(...sameDomainTools.map(t => t.id));
      
      // Cross-domain suggestions based on common workflows
      const crossDomainSuggestions = getCrossDomainSuggestions(currentTool);
      suggestions.push(...crossDomainSuggestions);
      
      setContextualSuggestions([...new Set(suggestions)]);
    }
  }, [sharedContext.userFocus.currentTool, enhancedTools, enablePredictive]);

  // Keyboard navigation
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (!isOpen) {
        // Global shortcuts when switcher is closed
        if (e.ctrlKey && e.shiftKey && e.key === 'P') {
          e.preventDefault();
          setIsOpen(true);
          setTimeout(() => searchInputRef.current?.focus(), 100);
        }
        return;
      }

      switch (e.key) {
        case 'Escape':
          e.preventDefault();
          setIsOpen(false);
          setSearchTerm('');
          setSelectedIndex(0);
          break;
        
        case 'ArrowDown':
          e.preventDefault();
          setSelectedIndex(prev => Math.min(prev + 1, filteredTools.length - 1));
          break;
        
        case 'ArrowUp':
          e.preventDefault();
          setSelectedIndex(prev => Math.max(prev - 1, 0));
          break;
        
        case 'Enter':
          e.preventDefault();
          if (filteredTools[selectedIndex]) {
            handleToolSwitch(filteredTools[selectedIndex]);
          }
          break;
      }
    };

    document.addEventListener('keydown', handleKeyDown);
    return () => document.removeEventListener('keydown', handleKeyDown);
  }, [isOpen, selectedIndex, filteredTools]);

  // Auto-adjust cognitive load limit based on performance
  useEffect(() => {
    const metrics = getCurrentMetrics();
    if (metrics && metrics.cognitiveLoad) {
      // If user is consistently performing well with complex tools, increase limit
      // If struggling, decrease limit
      const adjustedLimit = Math.min(100, Math.max(50, cognitiveLoadLimit + (metrics.cognitiveLoad > 80 ? -5 : 2)));
      if (adjustedLimit !== cognitiveLoadLimit) {
        setCognitiveLoadLimit(adjustedLimit);
      }
    }
  }, [getCurrentMetrics, cognitiveLoadLimit]);

  const getCrossDomainSuggestions = (currentTool: string): string[] => {
    const suggestions: Record<string, string[]> = {
      // Security → Other domains
      'misp': ['n8n', 'dispatch', 'ghostwriter'], // Threat intel → automation → incident response → reporting
      'helk': ['n8n', 'inspector', 'rita'], // Log analysis → automation → monitoring → analytics
      'cyberchef': ['firecrawl', 'it-tools'], // Data analysis → web scraping → utilities
      
      // Productivity → Other domains
      'n8n': ['misp', 'dispatch', 'firecrawl'], // Automation bridges many domains
      'mealie': ['actual-budget'], // Meal planning → budgeting
      'dispatch': ['misp', 'helk', 'ghostwriter'], // Incident response → threat intel → logging → reporting
      
      // MTG → Other domains (less common but possible)
      'commander-spellbook': ['mtg-scripting-toolkit', 'n8n'], // Research → automation
      
      // Infrastructure supports everything
      'kong': ['n8n', 'chroma-mcp'], // API gateway → workflow automation → AI services
    };
    
    return suggestions[currentTool] || [];
  };

  const handleToolSwitch = (tool: Tool) => {
    const previousTool = sharedContext.userFocus.currentTool;
    
    // Check complexity warning
    if (tool.complexity > cognitiveLoadLimit + 10) {
      setShowComplexityWarning(true);
      setTimeout(() => setShowComplexityWarning(false), 3000);
    }
    
    // Update usage statistics
    setToolUsageStats(prev => ({
      ...prev,
      [tool.id]: {
        frequency: (prev[tool.id]?.frequency || 0) + 1,
        lastUsed: Date.now()
      }
    }));
    
    // Track context switch
    sharedContext.setCurrentTool(tool.id);
    
    // Performance tracking
    markUIInteraction('tool-switch', {
      fromTool: previousTool,
      toTool: tool.id,
      domain: tool.domain,
      complexity: tool.complexity,
      estimatedSwitchTime: tool.estimatedSwitchTime
    });
    
    // Close switcher
    setIsOpen(false);
    setSearchTerm('');
    setSelectedIndex(0);
    
    // Notify parent
    onToolSwitch?.(previousTool, tool.id);
  };

  const getDomainStats = () => {
    const stats: Record<string, { count: number; avgComplexity: number }> = {};
    
    enhancedTools.forEach(tool => {
      if (!stats[tool.domain]) {
        stats[tool.domain] = { count: 0, avgComplexity: 0 };
      }
      stats[tool.domain].count++;
      stats[tool.domain].avgComplexity += tool.complexity;
    });
    
    Object.keys(stats).forEach(domain => {
      stats[domain].avgComplexity = Math.round(stats[domain].avgComplexity / stats[domain].count);
    });
    
    return stats;
  };

  return (
    <div className={`enhanced-tool-switcher ${className}`}>
      {/* Trigger Button */}
      <button
        onClick={() => setIsOpen(true)}
        className="flex items-center gap-2 px-4 py-2 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg hover:shadow-md transition-shadow"
        title="Switch Tools (Ctrl+Shift+P)"
      >
        <span className="text-xl">
          {sharedContext.userFocus.currentTool ? 
            enhancedTools.find(t => t.id === sharedContext.userFocus.currentTool)?.icon || '🔧' : 
            '🔧'
          }
        </span>
        <span className="text-sm font-medium text-gray-700 dark:text-gray-300">
          {sharedContext.userFocus.currentTool ? 
            enhancedTools.find(t => t.id === sharedContext.userFocus.currentTool)?.name || 'Switch Tool' : 
            'Switch Tool'
          }
        </span>
        <span className="text-xs text-gray-500 dark:text-gray-400">
          Ctrl+Shift+P
        </span>
      </button>

      {/* Complexity Warning */}
      {showComplexityWarning && (
        <div className="fixed top-4 right-4 bg-yellow-50 dark:bg-yellow-900/30 border border-yellow-200 dark:border-yellow-700 rounded-lg p-3 z-50 shadow-lg">
          <div className="flex items-center gap-2">
            <span className="text-yellow-600 dark:text-yellow-400">⚠️</span>
            <span className="text-sm font-medium text-yellow-800 dark:text-yellow-200">
              High complexity tool - consider current cognitive load
            </span>
          </div>
        </div>
      )}

      {/* Tool Switcher Modal */}
      {isOpen && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-start justify-center pt-[10vh] z-50">
          <div 
            ref={dropdownRef}
            className="bg-white dark:bg-gray-900 rounded-xl shadow-2xl border border-gray-200 dark:border-gray-700 w-full max-w-2xl mx-4 max-h-[80vh] overflow-hidden"
          >
            {/* Header */}
            <div className="p-4 border-b border-gray-200 dark:border-gray-700">
              <div className="flex items-center gap-3 mb-3">
                <input
                  ref={searchInputRef}
                  type="text"
                  placeholder="Search tools... (37 available)"
                  value={searchTerm}
                  onChange={(e) => {
                    setSearchTerm(e.target.value);
                    setSelectedIndex(0);
                  }}
                  className="flex-1 px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
                <button
                  onClick={() => setIsOpen(false)}
                  className="p-2 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300"
                >
                  ✕
                </button>
              </div>
              
              {/* Domain Filter */}
              <div className="flex gap-2 flex-wrap">
                {['all', 'security', 'productivity', 'mtg', 'ai', 'infrastructure'].map(domain => (
                  <button
                    key={domain}
                    onClick={() => {
                      setSelectedDomain(domain);
                      setSelectedIndex(0);
                    }}
                    className={`px-3 py-1 text-sm rounded-full capitalize ${
                      selectedDomain === domain 
                        ? 'bg-blue-600 text-white' 
                        : 'bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-600'
                    }`}
                  >
                    {domain}
                    {domain !== 'all' && (
                      <span className="ml-1 text-xs opacity-75">
                        {enhancedTools.filter(t => t.domain === domain).length}
                      </span>
                    )}
                  </button>
                ))}
              </div>

              {/* Cognitive Load Limit */}
              <div className="mt-3 flex items-center gap-3 text-sm">
                <span className="text-gray-600 dark:text-gray-400">Max Complexity:</span>
                <input
                  type="range"
                  min="50"
                  max="100"
                  value={cognitiveLoadLimit}
                  onChange={(e) => setCognitiveLoadLimit(Number(e.target.value))}
                  className="flex-1"
                />
                <span className="font-medium text-gray-900 dark:text-white w-12">
                  {cognitiveLoadLimit}%
                </span>
              </div>
            </div>

            {/* Recent Tools */}
            {recentTools.length > 0 && !searchTerm && (
              <div className="p-4 border-b border-gray-200 dark:border-gray-700">
                <h3 className="text-sm font-medium text-gray-600 dark:text-gray-400 mb-2">
                  Recent Tools
                </h3>
                <div className="flex gap-2 flex-wrap">
                  {recentTools.map(tool => (
                    <button
                      key={tool.id}
                      onClick={() => handleToolSwitch(tool)}
                      className="flex items-center gap-2 px-3 py-2 bg-gray-50 dark:bg-gray-800 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
                    >
                      <span>{tool.icon}</span>
                      <span className="text-sm font-medium">{tool.name}</span>
                      <span className={`text-xs px-2 py-1 rounded-full ${DOMAIN_COLORS[tool.domain]}`}>
                        {tool.domain}
                      </span>
                    </button>
                  ))}
                </div>
              </div>
            )}

            {/* Tool List */}
            <div className="max-h-96 overflow-y-auto">
              {filteredTools.length === 0 ? (
                <div className="p-8 text-center text-gray-500 dark:text-gray-400">
                  <p>No tools found matching your criteria</p>
                  <p className="text-sm mt-2">
                    Try adjusting the complexity limit or search terms
                  </p>
                </div>
              ) : (
                <div className="p-2">
                  {filteredTools.map((tool, index) => (
                    <div
                      key={tool.id}
                      onClick={() => handleToolSwitch(tool)}
                      className={`p-3 rounded-lg cursor-pointer transition-colors ${
                        index === selectedIndex 
                          ? 'bg-blue-50 dark:bg-blue-900/30 border border-blue-200 dark:border-blue-700' 
                          : 'hover:bg-gray-50 dark:hover:bg-gray-800'
                      } ${tool.id === sharedContext.userFocus.currentTool ? 'ring-2 ring-green-400' : ''}`}
                    >
                      <div className="flex items-center gap-3">
                        <span className="text-2xl">{tool.icon}</span>
                        <div className="flex-1 min-w-0">
                          <div className="flex items-center gap-2">
                            <h4 className="font-medium text-gray-900 dark:text-white">
                              {tool.name}
                            </h4>
                            {tool.contextual && (
                              <span className="text-xs bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-300 px-2 py-1 rounded-full">
                                Suggested
                              </span>
                            )}
                            {tool.id === sharedContext.userFocus.currentTool && (
                              <span className="text-xs bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-300 px-2 py-1 rounded-full">
                                Current
                              </span>
                            )}
                            {tool.shortcut && (
                              <span className="text-xs text-gray-500 dark:text-gray-400 font-mono">
                                {tool.shortcut}
                              </span>
                            )}
                          </div>
                          <p className="text-sm text-gray-600 dark:text-gray-400 truncate">
                            {tool.description}
                          </p>
                          <div className="flex items-center gap-3 mt-1">
                            <span className={`text-xs px-2 py-1 rounded-full ${DOMAIN_COLORS[tool.domain]}`}>
                              {tool.domain}
                            </span>
                            <span className={`text-xs ${
                              tool.complexity > 80 ? 'text-red-600 dark:text-red-400' :
                              tool.complexity > 60 ? 'text-yellow-600 dark:text-yellow-400' :
                              'text-green-600 dark:text-green-400'
                            }`}>
                              Complexity: {tool.complexity}%
                            </span>
                            <span className="text-xs text-gray-500 dark:text-gray-400">
                              ~{tool.estimatedSwitchTime}s switch time
                            </span>
                            {tool.frequency > 0 && (
                              <span className="text-xs text-gray-500 dark:text-gray-400">
                                Used {tool.frequency} times
                              </span>
                            )}
                          </div>
                        </div>
                        {tool.status === 'loading' && (
                          <div className="w-4 h-4 border-2 border-blue-500 border-t-transparent rounded-full animate-spin" />
                        )}
                        {tool.status === 'error' && (
                          <span className="text-red-500">⚠</span>
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>

            {/* Footer Stats */}
            <div className="p-4 border-t border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-800">
              <div className="flex justify-between items-center text-xs text-gray-500 dark:text-gray-400">
                <span>
                  Showing {filteredTools.length} of {enhancedTools.length} tools
                </span>
                <div className="flex gap-4">
                  <span>↑↓ Navigate</span>
                  <span>Enter Select</span>
                  <span>Esc Close</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}