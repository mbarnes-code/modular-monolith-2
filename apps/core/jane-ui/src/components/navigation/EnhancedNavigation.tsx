/**
 * Enhanced Navigation Component with Executive Function Support
 * Cognitive load management for 37-tool mental prosthetic platform
 */

import { useEffect, useMemo, useState } from 'react';
import { usePerformanceMonitor } from '../../services/performance/performanceMonitor';
import { useCrossDomainSync, useSharedContext } from '../../services/state/optimizedStateManager';

interface Tool {
  id: string;
  name: string;
  domain: 'security' | 'productivity' | 'mtg' | 'infrastructure';
  icon: string;
  path: string;
  priority: 'critical' | 'high' | 'medium' | 'low';
  description: string;
}

interface EnhancedNavigationProps {
  tools: Tool[];
  currentTool?: string;
  onToolSelect: (toolId: string) => void;
}

const DOMAIN_COLORS = {
  security: 'bg-red-500',
  productivity: 'bg-blue-500',
  mtg: 'bg-green-500',
  infrastructure: 'bg-gray-500',
};

const DOMAIN_ICONS = {
  security: '🛡️',
  productivity: '⚡',
  mtg: '🃏',
  infrastructure: '⚙️',
};

export function EnhancedNavigation({ tools, currentTool, onToolSelect }: EnhancedNavigationProps) {
  const sharedContext = useSharedContext();
  const { subscribeToEvents } = useCrossDomainSync();
  const { trackToolSwitch, markUIInteraction } = usePerformanceMonitor();
  
  const [searchQuery, setSearchQuery] = useState('');
  const [focusMode, setFocusMode] = useState(false);
  const [expandedDomains, setExpandedDomains] = useState<Set<string>>(new Set(['security', 'productivity']));

  // Quick switch history from shared context
  const quickSwitchHistory = useMemo(() => {
    return sharedContext.activeTools.slice(-5);
  }, [sharedContext.activeTools]);

  // Filter tools based on search and focus mode
  const filteredTools = useMemo(() => {
    let filtered = tools;

    // Apply search filter
    if (searchQuery) {
      filtered = filtered.filter(tool =>
        tool.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
        tool.description.toLowerCase().includes(searchQuery.toLowerCase()) ||
        tool.domain.toLowerCase().includes(searchQuery.toLowerCase())
      );
    }

    // In focus mode, only show current tool and recently used
    if (focusMode) {
      filtered = filtered.filter(tool =>
        tool.id === currentTool || quickSwitchHistory.includes(tool.id)
      );
    }

    return filtered;
  }, [tools, searchQuery, focusMode, currentTool, quickSwitchHistory]);

  // Group tools by domain
  const toolsByDomain = useMemo(() => {
    const grouped: Record<string, Tool[]> = {};
    filteredTools.forEach(tool => {
      if (!grouped[tool.domain]) {
        grouped[tool.domain] = [];
      }
      grouped[tool.domain].push(tool);
    });

    // Sort tools within each domain by priority
    Object.values(grouped).forEach(domainTools => {
      domainTools.sort((a, b) => {
        const priorityOrder = { critical: 0, high: 1, medium: 2, low: 3 };
        return priorityOrder[a.priority] - priorityOrder[b.priority];
      });
    });

    return grouped;
  }, [filteredTools]);

  // Handle tool selection with performance tracking
  const handleToolSelect = (toolId: string) => {
    markUIInteraction('tool-select');
    
    if (currentTool && currentTool !== toolId) {
      trackToolSwitch(currentTool, toolId);
    }

    sharedContext.addActiveTool(toolId);
    onToolSelect(toolId);
  };

  // Toggle domain expansion
  const toggleDomain = (domain: string) => {
    markUIInteraction('domain-toggle');
    
    const newExpanded = new Set(expandedDomains);
    if (newExpanded.has(domain)) {
      newExpanded.delete(domain);
    } else {
      newExpanded.add(domain);
    }
    setExpandedDomains(newExpanded);
  };

  // Toggle focus mode
  const toggleFocusMode = () => {
    markUIInteraction('focus-mode-toggle');
    setFocusMode(!focusMode);
    sharedContext.setFocusMode(focusMode ? 'normal' : 'focus', currentTool);
  };

  // Subscribe to cross-domain events
  useEffect(() => {
    const unsubscribe = subscribeToEvents(
      ['focus:changed', 'workflow:changed'],
      (event, data) => {
        if (event === 'focus:changed') {
          setFocusMode(data.mode === 'focus' || data.mode === 'deep-work');
        }
      }
    );

    return unsubscribe;
  }, [subscribeToEvents]);

  return (
    <nav className="enhanced-navigation h-full bg-white dark:bg-gray-900 border-r border-gray-200 dark:border-gray-700 flex flex-col">
      {/* Header with search and focus mode toggle */}
      <div className="p-4 border-b border-gray-200 dark:border-gray-700">
        <div className="flex items-center gap-2 mb-3">
          <h2 className="text-lg font-semibold text-gray-900 dark:text-white">
            Jane Tools
          </h2>
          <button
            onClick={toggleFocusMode}
            className={`p-1 rounded text-sm transition-colors ${
              focusMode
                ? 'bg-orange-100 text-orange-700 dark:bg-orange-900 dark:text-orange-300'
                : 'bg-gray-100 text-gray-600 dark:bg-gray-800 dark:text-gray-400'
            }`}
            title={focusMode ? 'Exit focus mode' : 'Enable focus mode'}
          >
            {focusMode ? '🎯' : '👁️'}
          </button>
        </div>
        
        <input
          type="text"
          placeholder="Search tools..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg 
                   bg-white dark:bg-gray-800 text-gray-900 dark:text-white
                   focus:ring-2 focus:ring-blue-500 focus:border-transparent
                   transition-colors duration-200"
        />
      </div>

      {/* Quick switch section */}
      {quickSwitchHistory.length > 0 && (
        <div className="p-4 border-b border-gray-200 dark:border-gray-700">
          <h3 className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            Recent Tools
          </h3>
          <div className="flex flex-wrap gap-1">
            {quickSwitchHistory.map(toolId => {
              const tool = tools.find(t => t.id === toolId);
              if (!tool) return null;
              
              return (
                <button
                  key={toolId}
                  onClick={() => handleToolSelect(toolId)}
                  className={`px-2 py-1 text-xs rounded transition-colors ${
                    currentTool === toolId
                      ? 'bg-blue-500 text-white'
                      : 'bg-gray-100 text-gray-700 hover:bg-gray-200 dark:bg-gray-800 dark:text-gray-300 dark:hover:bg-gray-700'
                  }`}
                  title={tool.description}
                >
                  {tool.name}
                </button>
              );
            })}
          </div>
        </div>
      )}

      {/* Tool list by domain */}
      <div className="flex-1 overflow-y-auto">
        {Object.entries(toolsByDomain).map(([domain, domainTools]) => (
          <div key={domain} className="border-b border-gray-100 dark:border-gray-800">
            <button
              onClick={() => toggleDomain(domain)}
              className="w-full p-3 text-left hover:bg-gray-50 dark:hover:bg-gray-800 
                       transition-colors duration-150 flex items-center justify-between"
            >
              <div className="flex items-center gap-2">
                <span className="text-lg">{DOMAIN_ICONS[domain as keyof typeof DOMAIN_ICONS]}</span>
                <span className="font-medium text-gray-900 dark:text-white capitalize">
                  {domain}
                </span>
                <span className="text-xs bg-gray-200 dark:bg-gray-700 px-2 py-1 rounded">
                  {domainTools.length}
                </span>
              </div>
              <span className={`transform transition-transform ${
                expandedDomains.has(domain) ? 'rotate-90' : ''
              }`}>
                ▶
              </span>
            </button>

            {expandedDomains.has(domain) && (
              <div className="pb-2">
                {domainTools.map(tool => (
                  <button
                    key={tool.id}
                    onClick={() => handleToolSelect(tool.id)}
                    className={`w-full p-3 text-left hover:bg-gray-50 dark:hover:bg-gray-800 
                             transition-all duration-150 flex items-center gap-3 ${
                      currentTool === tool.id
                        ? 'bg-blue-50 dark:bg-blue-900/20 border-r-2 border-blue-500'
                        : ''
                    }`}
                    title={tool.description}
                  >
                    <span className="text-lg">{tool.icon}</span>
                    <div className="flex-1 min-w-0">
                      <div className="font-medium text-gray-900 dark:text-white text-sm">
                        {tool.name}
                      </div>
                      <div className="text-xs text-gray-500 dark:text-gray-400 truncate">
                        {tool.description}
                      </div>
                    </div>
                    {tool.priority === 'critical' && (
                      <span className="w-2 h-2 bg-red-500 rounded-full" title="Critical tool" />
                    )}
                  </button>
                ))}
              </div>
            )}
          </div>
        ))}
      </div>

      {/* Active tools indicator */}
      {sharedContext.activeTools.length > 0 && (
        <div className="p-4 border-t border-gray-200 dark:border-gray-700">
          <div className="text-xs text-gray-500 dark:text-gray-400 mb-2">
            Active Tools ({sharedContext.activeTools.length}/5)
          </div>
          <div className="flex flex-wrap gap-1">
            {sharedContext.activeTools.map(toolId => {
              const tool = tools.find(t => t.id === toolId);
              if (!tool) return null;
              
              return (
                <div
                  key={toolId}
                  className={`px-2 py-1 text-xs rounded flex items-center gap-1 ${
                    DOMAIN_COLORS[tool.domain]
                  } text-white`}
                >
                  <span>{tool.icon}</span>
                  <span>{tool.name}</span>
                  <button
                    onClick={() => sharedContext.removeActiveTool(toolId)}
                    className="ml-1 hover:bg-white/20 rounded px-1"
                    title="Remove from active tools"
                  >
                    ×
                  </button>
                </div>
              );
            })}
          </div>
        </div>
      )}
    </nav>
  );
}

// CSS for focus mode (add to global styles)
export const focusModeStyles = `
  .focus-mode {
    --animation-speed: 0.1s;
  }
  
  .focus-mode .enhanced-navigation {
    border-right: 2px solid #f97316;
  }
  
  .focus-mode .enhanced-navigation::before {
    content: '';
    position: absolute;
    top: 0;
    right: -2px;
    height: 100%;
    width: 2px;
    background: linear-gradient(to bottom, #f97316, #ea580c);
    animation: pulse 2s infinite;
  }
  
  @keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.5; }
  }
`;