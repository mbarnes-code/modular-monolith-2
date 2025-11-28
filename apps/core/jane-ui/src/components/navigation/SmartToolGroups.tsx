/**
 * Smart Tool Groups UI Component
 * Visual interface for intelligent tool grouping and clustering
 */

import { AnimatePresence, motion } from 'framer-motion';
import {
    ChevronDown,
    ChevronRight,
    Clock,
    Minus,
    MoreVertical,
    Package,
    RefreshCw,
    Star,
    Target,
    ThumbsDown,
    ThumbsUp,
    TrendingDown,
    TrendingUp,
    Users,
    Zap
} from 'lucide-react';
import { useMemo, useState } from 'react';
import { useSmartToolGrouping, type Tool, type ToolGroup } from '../../services/navigation/smartToolGrouping';
import { useAdaptiveNavigation } from '../../services/navigation/useAdaptiveNavigation';

interface SmartToolGroupsProps {
  tools: Tool[];
  currentTool?: string;
  onToolSelect?: (toolId: string) => void;
  onGroupSelect?: (group: ToolGroup) => void;
  className?: string;
}

interface GroupDisplayMode {
  layout: 'grid' | 'list' | 'compact';
  sortBy: 'recommendation' | 'cohesion' | 'efficiency' | 'frequency';
  filterBy: ToolGroup['groupType'] | 'all';
  showMetrics: boolean;
}

export function SmartToolGroups({ 
  tools, 
  currentTool, 
  onToolSelect, 
  onGroupSelect,
  className = '' 
}: SmartToolGroupsProps) {
  const { 
    groups, 
    isAnalyzing, 
    updateGroupFeedback, 
    getContextualRecommendations 
  } = useSmartToolGrouping(tools);
  
  const { requestNavigation } = useAdaptiveNavigation();
  
  const [displayMode, setDisplayMode] = useState<GroupDisplayMode>({
    layout: 'grid',
    sortBy: 'recommendation',
    filterBy: 'all',
    showMetrics: true
  });
  
  const [expandedGroups, setExpandedGroups] = useState<Set<string>>(new Set());
  const [hoveredGroup, setHoveredGroup] = useState<string | null>(null);
  const [feedbackGroup, setFeedbackGroup] = useState<string | null>(null);

  // Filter and sort groups based on display mode
  const processedGroups = useMemo(() => {
    let filtered = displayMode.filterBy === 'all' 
      ? groups 
      : groups.filter(group => group.groupType === displayMode.filterBy);
    
    // Sort groups
    const sorted = filtered.sort((a, b) => {
      switch (displayMode.sortBy) {
        case 'recommendation': return b.recommendationStrength - a.recommendationStrength;
        case 'cohesion': return b.cohesionScore - a.cohesionScore;
        case 'efficiency': return b.cognitiveEfficiency - a.cognitiveEfficiency;
        case 'frequency': return b.usagePattern.frequency - a.usagePattern.frequency;
        default: return 0;
      }
    });
    
    return sorted;
  }, [groups, displayMode]);

  // Get contextual recommendations for current tool
  const contextualGroups = useMemo(() => {
    return getContextualRecommendations(currentTool);
  }, [getContextualRecommendations, currentTool]);

  const handleGroupToggle = (groupId: string) => {
    setExpandedGroups(prev => {
      const next = new Set(prev);
      if (next.has(groupId)) {
        next.delete(groupId);
      } else {
        next.add(groupId);
      }
      return next;
    });
  };

  const handleToolClick = async (toolId: string) => {
    try {
      await requestNavigation(toolId);
      onToolSelect?.(toolId);
    } catch (error) {
      console.error('Navigation request failed:', error);
    }
  };

  const handleGroupFeedback = (groupId: string, positive: boolean) => {
    const feedback = positive ? 10 : -10;
    updateGroupFeedback(groupId, feedback);
    setFeedbackGroup(null);
  };

  const getGroupTypeIcon = (type: ToolGroup['groupType']) => {
    switch (type) {
      case 'workflow': return <Target className="w-4 h-4" />;
      case 'domain': return <Package className="w-4 h-4" />;
      case 'frequency': return <Clock className="w-4 h-4" />;
      case 'complexity': return <Zap className="w-4 h-4" />;
      case 'contextual': return <Users className="w-4 h-4" />;
      default: return <Package className="w-4 h-4" />;
    }
  };

  const getGroupTypeColor = (type: ToolGroup['groupType']) => {
    switch (type) {
      case 'workflow': return 'text-purple-600 bg-purple-100';
      case 'domain': return 'text-blue-600 bg-blue-100';
      case 'frequency': return 'text-green-600 bg-green-100';
      case 'complexity': return 'text-orange-600 bg-orange-100';
      case 'contextual': return 'text-indigo-600 bg-indigo-100';
      default: return 'text-gray-600 bg-gray-100';
    }
  };

  const getMetricTrend = (value: number, threshold: number = 70) => {
    if (value >= threshold) return <TrendingUp className="w-3 h-3 text-green-500" />;
    if (value >= threshold - 20) return <Minus className="w-3 h-3 text-yellow-500" />;
    return <TrendingDown className="w-3 h-3 text-red-500" />;
  };

  if (isAnalyzing) {
    return (
      <div className={`smart-tool-groups ${className}`}>
        <div className="flex items-center justify-center p-8">
          <div className="flex items-center gap-3 text-gray-600">
            <RefreshCw className="w-5 h-5 animate-spin" />
            <span>Analyzing tool patterns...</span>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className={`smart-tool-groups space-y-6 ${className}`}>
      {/* Header with controls */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <h3 className="text-lg font-semibold text-gray-900">Smart Tool Groups</h3>
          <span className="px-2 py-1 bg-blue-100 text-blue-800 text-xs rounded">
            {processedGroups.length} groups
          </span>
        </div>
        
        <div className="flex items-center gap-2">
          {/* Filter by group type */}
          <select
            value={displayMode.filterBy}
            onChange={(e) => setDisplayMode(prev => ({ 
              ...prev, 
              filterBy: e.target.value as GroupDisplayMode['filterBy']
            }))}
            className="text-sm border border-gray-300 rounded px-2 py-1"
          >
            <option value="all">All Types</option>
            <option value="workflow">Workflow</option>
            <option value="domain">Domain</option>
            <option value="frequency">Frequency</option>
            <option value="complexity">Complexity</option>
            <option value="contextual">Contextual</option>
          </select>
          
          {/* Sort options */}
          <select
            value={displayMode.sortBy}
            onChange={(e) => setDisplayMode(prev => ({ 
              ...prev, 
              sortBy: e.target.value as GroupDisplayMode['sortBy']
            }))}
            className="text-sm border border-gray-300 rounded px-2 py-1"
          >
            <option value="recommendation">Recommendation</option>
            <option value="cohesion">Cohesion</option>
            <option value="efficiency">Efficiency</option>
            <option value="frequency">Frequency</option>
          </select>
          
          {/* Layout toggle */}
          <div className="flex border border-gray-300 rounded overflow-hidden">
            {['grid', 'list', 'compact'].map(layout => (
              <button
                key={layout}
                onClick={() => setDisplayMode(prev => ({ 
                  ...prev, 
                  layout: layout as GroupDisplayMode['layout']
                }))}
                className={`px-2 py-1 text-xs ${
                  displayMode.layout === layout 
                    ? 'bg-blue-500 text-white' 
                    : 'bg-white text-gray-600 hover:bg-gray-50'
                }`}
              >
                {layout.charAt(0).toUpperCase() + layout.slice(1)}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Contextual recommendations for current tool */}
      {currentTool && contextualGroups.length > 0 && (
        <div className="bg-blue-50 rounded-lg p-4 border border-blue-200">
          <h4 className="text-sm font-medium text-blue-900 mb-3">
            Recommended for current context
          </h4>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
            {contextualGroups.slice(0, 3).map(group => (
              <motion.div
                key={group.id}
                whileHover={{ scale: 1.02 }}
                className="bg-white rounded border border-blue-200 p-3 cursor-pointer hover:shadow-sm"
                onClick={() => onGroupSelect?.(group)}
              >
                <div className="flex items-center gap-2 mb-2">
                  <div className={`p-1 rounded ${getGroupTypeColor(group.groupType)}`}>
                    {getGroupTypeIcon(group.groupType)}
                  </div>
                  <span className="text-sm font-medium text-gray-900">{group.name}</span>
                </div>
                <div className="text-xs text-gray-600 mb-2">{group.description}</div>
                <div className="flex items-center justify-between text-xs">
                  <span className="text-gray-500">{group.tools.length} tools</span>
                  <div className="flex items-center gap-1">
                    <Star className="w-3 h-3 text-yellow-500" />
                    <span>{Math.round(group.recommendationStrength)}</span>
                  </div>
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      )}

      {/* Groups display */}
      <div className={`groups-container ${
        displayMode.layout === 'grid' ? 'grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4' :
        displayMode.layout === 'list' ? 'space-y-3' :
        'space-y-2'
      }`}>
        <AnimatePresence>
          {processedGroups.map(group => (
            <motion.div
              key={group.id}
              layout
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              className={`group-card bg-white rounded-lg border border-gray-200 hover:shadow-md transition-all duration-200 ${
                hoveredGroup === group.id ? 'ring-2 ring-blue-200' : ''
              }`}
              onMouseEnter={() => setHoveredGroup(group.id)}
              onMouseLeave={() => setHoveredGroup(null)}
            >
              {/* Group header */}
              <div className="p-4 border-b border-gray-100">
                <div className="flex items-start justify-between">
                  <div className="flex items-start gap-3">
                    <div className={`p-2 rounded-lg ${getGroupTypeColor(group.groupType)}`}>
                      {getGroupTypeIcon(group.groupType)}
                    </div>
                    
                    <div className="flex-1">
                      <div className="flex items-center gap-2">
                        <h4 className="font-medium text-gray-900">{group.name}</h4>
                        <span className="px-2 py-0.5 bg-gray-100 text-gray-600 text-xs rounded capitalize">
                          {group.groupType}
                        </span>
                      </div>
                      
                      <p className="text-sm text-gray-600 mt-1 line-clamp-2">
                        {group.description}
                      </p>
                      
                      {displayMode.showMetrics && (
                        <div className="flex items-center gap-4 mt-2 text-xs text-gray-500">
                          <div className="flex items-center gap-1">
                            <span>Cohesion:</span>
                            <span className="font-medium">{Math.round(group.cohesionScore)}%</span>
                            {getMetricTrend(group.cohesionScore)}
                          </div>
                          <div className="flex items-center gap-1">
                            <span>Efficiency:</span>
                            <span className="font-medium">{Math.round(group.cognitiveEfficiency)}%</span>
                            {getMetricTrend(group.cognitiveEfficiency)}
                          </div>
                        </div>
                      )}
                    </div>
                  </div>
                  
                  <div className="flex items-center gap-1">
                    <div className="flex items-center gap-1 text-xs text-gray-500">
                      <Star className="w-3 h-3 text-yellow-500" />
                      <span>{Math.round(group.recommendationStrength)}</span>
                    </div>
                    
                    <button
                      onClick={() => setFeedbackGroup(feedbackGroup === group.id ? null : group.id)}
                      className="p-1 text-gray-400 hover:text-gray-600 rounded"
                    >
                      <MoreVertical className="w-4 h-4" />
                    </button>
                  </div>
                </div>
                
                {/* Feedback menu */}
                <AnimatePresence>
                  {feedbackGroup === group.id && (
                    <motion.div
                      initial={{ opacity: 0, scale: 0.95 }}
                      animate={{ opacity: 1, scale: 1 }}
                      exit={{ opacity: 0, scale: 0.95 }}
                      className="absolute right-4 top-16 bg-white rounded-lg shadow-lg border border-gray-200 py-2 z-10"
                    >
                      <button
                        onClick={() => handleGroupFeedback(group.id, true)}
                        className="flex items-center gap-2 px-3 py-2 text-sm text-gray-700 hover:bg-gray-50 w-full"
                      >
                        <ThumbsUp className="w-4 h-4 text-green-500" />
                        Helpful grouping
                      </button>
                      <button
                        onClick={() => handleGroupFeedback(group.id, false)}
                        className="flex items-center gap-2 px-3 py-2 text-sm text-gray-700 hover:bg-gray-50 w-full"
                      >
                        <ThumbsDown className="w-4 h-4 text-red-500" />
                        Not helpful
                      </button>
                    </motion.div>
                  )}
                </AnimatePresence>
              </div>
              
              {/* Tools in group */}
              <div className="p-4">
                <div className="flex items-center justify-between mb-3">
                  <span className="text-sm text-gray-600">
                    {group.tools.length} tools
                  </span>
                  
                  <button
                    onClick={() => handleGroupToggle(group.id)}
                    className="flex items-center gap-1 text-sm text-blue-600 hover:text-blue-800"
                  >
                    {expandedGroups.has(group.id) ? (
                      <>
                        <ChevronDown className="w-4 h-4" />
                        Collapse
                      </>
                    ) : (
                      <>
                        <ChevronRight className="w-4 h-4" />
                        Expand
                      </>
                    )}
                  </button>
                </div>
                
                {/* Tool preview (always show first 3) */}
                <div className="grid grid-cols-3 gap-2 mb-3">
                  {group.tools.slice(0, 3).map(tool => (
                    <button
                      key={tool.id}
                      onClick={() => handleToolClick(tool.id)}
                      className={`p-2 rounded text-xs text-center border transition-colors ${
                        currentTool === tool.id
                          ? 'bg-blue-100 border-blue-300 text-blue-800'
                          : 'bg-gray-50 border-gray-200 text-gray-700 hover:bg-gray-100'
                      }`}
                    >
                      {tool.display_name}
                    </button>
                  ))}
                </div>
                
                {/* Expanded tool list */}
                <AnimatePresence>
                  {expandedGroups.has(group.id) && group.tools.length > 3 && (
                    <motion.div
                      initial={{ opacity: 0, height: 0 }}
                      animate={{ opacity: 1, height: 'auto' }}
                      exit={{ opacity: 0, height: 0 }}
                      className="grid grid-cols-2 gap-2"
                    >
                      {group.tools.slice(3).map(tool => (
                        <button
                          key={tool.id}
                          onClick={() => handleToolClick(tool.id)}
                          className={`p-2 rounded text-xs text-left border transition-colors ${
                            currentTool === tool.id
                              ? 'bg-blue-100 border-blue-300 text-blue-800'
                              : 'bg-gray-50 border-gray-200 text-gray-700 hover:bg-gray-100'
                          }`}
                        >
                          <div className="font-medium">{tool.display_name}</div>
                          <div className="text-gray-500 capitalize">{tool.domain}</div>
                        </button>
                      ))}
                    </motion.div>
                  )}
                </AnimatePresence>
                
                {/* Group actions */}
                <div className="flex items-center gap-2 mt-3 pt-3 border-t border-gray-100">
                  <button
                    onClick={() => onGroupSelect?.(group)}
                    className="flex-1 px-3 py-2 bg-blue-50 text-blue-700 text-sm rounded hover:bg-blue-100 transition-colors"
                  >
                    Use Group
                  </button>
                  
                  <div className="text-xs text-gray-500">
                    Switch cost: {Math.round(group.switchingCost)}%
                  </div>
                </div>
              </div>
            </motion.div>
          ))}
        </AnimatePresence>
      </div>
      
      {processedGroups.length === 0 && (
        <div className="text-center py-8 text-gray-500">
          <Package className="w-12 h-12 mx-auto mb-3 opacity-50" />
          <p>No tool groups found matching current criteria.</p>
          <p className="text-sm mt-1">Try adjusting filters or using tools to build usage patterns.</p>
        </div>
      )}
    </div>
  );
}