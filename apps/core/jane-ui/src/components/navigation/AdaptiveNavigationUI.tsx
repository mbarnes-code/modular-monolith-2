/**
 * Adaptive Navigation UI Component
 * Navigation interface with cognitive load awareness and smart guidance
 */

import { AnimatePresence, motion } from 'framer-motion';
import {
    AlertTriangle,
    Brain,
    Briefcase,
    Clock,
    Gamepad2,
    Minus,
    Server,
    Shield,
    TrendingDown,
    TrendingUp,
    Zap
} from 'lucide-react';
import React, { useState } from 'react';
import { useAdaptiveNavigation } from '../../services/navigation/useAdaptiveNavigation';
import { useGlobalStore } from '../../services/store';

interface AdaptiveNavigationUIProps {
  tools: Array<{
    id: string;
    name: string;
    display_name: string;
    domain: 'security' | 'productivity' | 'mtg' | 'infrastructure';
    status: 'active' | 'inactive' | 'maintenance';
    complexity_score?: number;
  }>;
  onToolSelect?: (toolId: string) => void;
  className?: string;
}

const getDomainIcon = (domain: string) => {
  switch (domain) {
    case 'security': return Shield;
    case 'productivity': return Briefcase;
    case 'mtg': return Gamepad2;
    case 'infrastructure': return Server;
    default: return Server;
  }
};

const getDomainColor = (domain: string) => {
  switch (domain) {
    case 'security': return 'bg-red-500';
    case 'productivity': return 'bg-blue-500';
    case 'mtg': return 'bg-purple-500';
    case 'infrastructure': return 'bg-green-500';
    default: return 'bg-gray-500';
  }
};

const getRiskColor = (risk: 'low' | 'medium' | 'high' | 'critical') => {
  switch (risk) {
    case 'low': return 'text-green-600 bg-green-50 border-green-200';
    case 'medium': return 'text-yellow-700 bg-yellow-50 border-yellow-200';
    case 'high': return 'text-orange-700 bg-orange-50 border-orange-200';
    case 'critical': return 'text-red-700 bg-red-50 border-red-200';
  }
};

export function AdaptiveNavigationUI({ 
  tools, 
  onToolSelect, 
  className = '' 
}: AdaptiveNavigationUIProps) {
  const { activeTool } = useGlobalStore();
  const {
    navigationState,
    requestNavigation,
    cancelPendingNavigation,
    dismissWarning,
    getToolComplexityPreview,
    canNavigateDirectly,
    getNavigationDelay,
    getNavigationRisk
  } = useAdaptiveNavigation();

  const [hoveredTool, setHoveredTool] = useState<string | null>(null);
  const [showComplexityDetails, setShowComplexityDetails] = useState(false);

  // Group tools by domain for better cognitive organization
  const toolsByDomain = tools.reduce((acc, tool) => {
    if (!acc[tool.domain]) {
      acc[tool.domain] = [];
    }
    acc[tool.domain].push(tool);
    return acc;
  }, {} as Record<string, typeof tools>);

  const handleToolClick = async (toolId: string) => {
    const success = await requestNavigation(toolId);
    if (success) {
      onToolSelect?.(toolId);
    }
  };

  const getTrendIcon = (trend: 'improving' | 'stable' | 'declining') => {
    switch (trend) {
      case 'improving': return TrendingUp;
      case 'declining': return TrendingDown;
      case 'stable': default: return Minus;
    }
  };

  const getTrendColor = (trend: 'improving' | 'stable' | 'declining') => {
    switch (trend) {
      case 'improving': return 'text-green-600';
      case 'declining': return 'text-red-600';
      case 'stable': default: return 'text-gray-600';
    }
  };

  return (
    <div className={`adaptive-navigation-ui ${className}`}>
      {/* Cognitive Load Status Header */}
      <div className="mb-4 p-3 bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Brain className="w-5 h-5 text-blue-600" />
            <span className="font-medium text-gray-900 dark:text-white">Navigation Intelligence</span>
          </div>
          <div className="flex items-center gap-2">
            {/* Cognitive Load Trend */}
            <div className="flex items-center gap-1 text-sm">
              {React.createElement(getTrendIcon(navigationState.cognitiveLoadTrend), {
                className: `w-4 h-4 ${getTrendColor(navigationState.cognitiveLoadTrend)}`
              })}
              <span className={`text-xs ${getTrendColor(navigationState.cognitiveLoadTrend)}`}>
                {navigationState.cognitiveLoadTrend}
              </span>
            </div>
            <button
              onClick={() => setShowComplexityDetails(!showComplexityDetails)}
              className="text-xs text-blue-600 hover:text-blue-700"
            >
              {showComplexityDetails ? 'Hide' : 'Details'}
            </button>
          </div>
        </div>

        {/* Navigation Status Warnings */}
        <AnimatePresence>
          {navigationState.navigationWarnings.length > 0 && (
            <motion.div
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: 'auto' }}
              exit={{ opacity: 0, height: 0 }}
              className="mt-3 space-y-2"
            >
              {navigationState.navigationWarnings.map((warning, index) => (
                <div
                  key={index}
                  className="flex items-start gap-2 p-2 bg-yellow-50 border border-yellow-200 rounded text-sm"
                >
                  <AlertTriangle className="w-4 h-4 text-yellow-600 mt-0.5 flex-shrink-0" />
                  <span className="text-yellow-800 flex-1">{warning}</span>
                  <button
                    onClick={() => dismissWarning(index)}
                    className="text-yellow-600 hover:text-yellow-800"
                  >
                    ×
                  </button>
                </div>
              ))}
            </motion.div>
          )}
        </AnimatePresence>

        {/* Pending Navigation Status */}
        <AnimatePresence>
          {navigationState.pendingNavigation && (
            <motion.div
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: 'auto' }}
              exit={{ opacity: 0, height: 0 }}
              className="mt-3 p-3 bg-blue-50 border border-blue-200 rounded"
            >
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <Clock className="w-4 h-4 text-blue-600" />
                  <span className="text-sm font-medium text-blue-800">
                    Navigation delay: {Math.ceil(navigationState.pendingNavigation.remainingDelay / 1000)}s
                  </span>
                </div>
                <button
                  onClick={cancelPendingNavigation}
                  className="text-xs text-blue-600 hover:text-blue-800 border border-blue-300 px-2 py-1 rounded"
                >
                  Cancel
                </button>
              </div>
              <div className="mt-2 w-full bg-blue-200 rounded-full h-2">
                <motion.div
                  className="bg-blue-600 h-2 rounded-full"
                  initial={{ width: '100%' }}
                  animate={{ width: '0%' }}
                  transition={{ 
                    duration: navigationState.pendingNavigation.remainingDelay / 1000,
                    ease: 'linear'
                  }}
                />
              </div>
            </motion.div>
          )}
        </AnimatePresence>

        {/* Suggested Alternatives */}
        <AnimatePresence>
          {navigationState.suggestedAlternatives.length > 0 && (
            <motion.div
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: 'auto' }}
              exit={{ opacity: 0, height: 0 }}
              className="mt-3 p-2 bg-gray-50 rounded text-sm"
            >
              <div className="font-medium text-gray-700 mb-1">Suggested alternatives:</div>
              <ul className="text-gray-600 space-y-1">
                {navigationState.suggestedAlternatives.map((alt, index) => (
                  <li key={index} className="ml-4">• {alt}</li>
                ))}
              </ul>
            </motion.div>
          )}
        </AnimatePresence>
      </div>

      {/* Tools Grid by Domain */}
      <div className="space-y-6">
        {Object.entries(toolsByDomain).map(([domain, domainTools]) => {
          const DomainIcon = getDomainIcon(domain);
          
          return (
            <div key={domain} className="space-y-3">
              {/* Domain Header */}
              <div className="flex items-center gap-2 px-2">
                <div className={`p-1.5 rounded ${getDomainColor(domain)} text-white`}>
                  <DomainIcon className="w-4 h-4" />
                </div>
                <h3 className="font-semibold text-gray-900 dark:text-white capitalize">
                  {domain} Tools
                </h3>
                <span className="text-sm text-gray-500">
                  {domainTools.filter(t => t.status === 'active').length}/{domainTools.length} active
                </span>
              </div>

              {/* Tools Grid */}
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
                {domainTools.map((tool) => {
                  const isActive = activeTool === tool.id;
                  const canNavigate = canNavigateDirectly(tool.id);
                  const navigationDelay = getNavigationDelay(tool.id);
                  const riskLevel = getNavigationRisk(tool.id);
                  const complexityInfo = getToolComplexityPreview(tool.id);

                  return (
                    <motion.div
                      key={tool.id}
                      whileHover={{ scale: 1.02 }}
                      whileTap={{ scale: 0.98 }}
                      className={`
                        relative p-3 rounded-lg border cursor-pointer transition-all
                        ${isActive 
                          ? 'bg-blue-50 border-blue-200 ring-2 ring-blue-500 ring-opacity-50' 
                          : 'bg-white hover:bg-gray-50 border-gray-200'
                        }
                        ${tool.status === 'maintenance' ? 'opacity-60' : ''}
                        ${!canNavigate && !isActive ? 'border-orange-200 bg-orange-50' : ''}
                      `}
                      onMouseEnter={() => setHoveredTool(tool.id)}
                      onMouseLeave={() => setHoveredTool(null)}
                      onClick={() => handleToolClick(tool.id)}
                    >
                      {/* Tool Header */}
                      <div className="flex items-start justify-between mb-2">
                        <div className="flex-1">
                          <h4 className="font-medium text-gray-900 text-sm">
                            {tool.display_name}
                          </h4>
                          <div className="flex items-center gap-2 mt-1">
                            {/* Status indicator */}
                            <div className={`w-2 h-2 rounded-full ${
                              tool.status === 'active' ? 'bg-green-400' :
                              tool.status === 'maintenance' ? 'bg-yellow-400' :
                              'bg-gray-400'
                            }`} />
                            <span className="text-xs text-gray-500 capitalize">
                              {tool.status}
                            </span>
                          </div>
                        </div>

                        {/* Navigation Risk Indicator */}
                        {!isActive && (
                          <div className={`
                            px-2 py-1 rounded text-xs font-medium border
                            ${getRiskColor(riskLevel)}
                          `}>
                            {riskLevel}
                          </div>
                        )}
                      </div>

                      {/* Navigation Delay Warning */}
                      {navigationDelay > 0 && !isActive && (
                        <div className="flex items-center gap-1 text-xs text-orange-600 mb-2">
                          <Clock className="w-3 h-3" />
                          <span>{Math.ceil(navigationDelay / 1000)}s delay</span>
                        </div>
                      )}

                      {/* Complexity Preview (on hover or when details shown) */}
                      <AnimatePresence>
                        {(showComplexityDetails || hoveredTool === tool.id) && complexityInfo && (
                          <motion.div
                            initial={{ opacity: 0, height: 0 }}
                            animate={{ opacity: 1, height: 'auto' }}
                            exit={{ opacity: 0, height: 0 }}
                            className="mt-2 pt-2 border-t border-gray-200 text-xs text-gray-600"
                          >
                            <div className="grid grid-cols-2 gap-1">
                              <div>Cognitive: {complexityInfo.cognitiveComplexity}%</div>
                              <div>Memory: {complexityInfo.memoryLoad}%</div>
                              <div>Visual: {complexityInfo.visualComplexity}%</div>
                              <div>Attention: {complexityInfo.attentionDemand}%</div>
                            </div>
                            <div className="mt-1 flex items-center gap-1">
                              <Zap className="w-3 h-3" />
                              <span>Switch cost: {complexityInfo.contextSwitchCost}/10</span>
                            </div>
                          </motion.div>
                        )}
                      </AnimatePresence>

                      {/* Navigation Blocked Overlay */}
                      {navigationState.isNavigationBlocked && !isActive && riskLevel === 'critical' && (
                        <div className="absolute inset-0 bg-red-100 bg-opacity-75 rounded-lg flex items-center justify-center">
                          <div className="text-center">
                            <AlertTriangle className="w-6 h-6 text-red-600 mx-auto mb-1" />
                            <div className="text-xs text-red-700 font-medium">
                              Navigation blocked
                            </div>
                          </div>
                        </div>
                      )}

                      {/* Active Tool Indicator */}
                      {isActive && (
                        <div className="absolute -top-1 -right-1 w-3 h-3 bg-blue-500 rounded-full border-2 border-white" />
                      )}
                    </motion.div>
                  );
                })}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}