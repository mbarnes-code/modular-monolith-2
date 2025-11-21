/**
 * Cognitive Load Manager
 * Advanced executive function support with load balancing and attention management
 */

import React, { useState, useEffect, useCallback } from 'react';
import { useSharedContext } from '../../services/state/optimizedStateManager';
import { usePerformanceMonitor } from '../../services/performance/performanceMonitor';

interface CognitiveLoad {
  visual: number;      // 0-100 visual complexity score
  cognitive: number;   // 0-100 mental processing required
  memory: number;      // 0-100 working memory usage
  attention: number;   // 0-100 attention demands
  total: number;       // Weighted average
}

interface TaskComplexity {
  id: string;
  name: string;
  domain: 'security' | 'productivity' | 'mtg' | 'ai' | 'infrastructure';
  baseComplexity: number;
  contextSwitches: number;
  estimatedDuration: number; // minutes
  priority: 'low' | 'medium' | 'high' | 'critical';
  dependencies: string[];
  completedSteps: number;
  totalSteps: number;
}

interface LoadRecommendation {
  type: 'reduce' | 'break' | 'defer' | 'simplify' | 'delegate';
  message: string;
  severity: 'info' | 'warning' | 'critical';
  actionRequired: boolean;
  suggestedDuration?: number; // minutes for breaks
  alternatives?: string[];
}

interface CognitiveLoadManagerProps {
  className?: string;
  autoManage?: boolean;
  onLoadChange?: (load: CognitiveLoad) => void;
}

// Executive function thresholds based on research
const LOAD_THRESHOLDS = {
  optimal: { total: 60, attention: 70, memory: 65, visual: 50 },
  warning: { total: 75, attention: 80, memory: 80, visual: 70 },
  critical: { total: 90, attention: 90, memory: 90, visual: 85 }
};

// Tool complexity profiles (based on executive function research)
const TOOL_COMPLEXITY_PROFILES = {
  // Security domain - High cognitive load due to threat analysis
  'misp': { base: 85, visual: 80, memory: 90, attention: 95 },
  'helk': { base: 80, visual: 75, memory: 85, attention: 90 },
  'securityonion': { base: 90, visual: 85, memory: 95, attention: 95 },
  'cyberchef': { base: 70, visual: 60, memory: 75, attention: 80 },
  
  // Productivity domain - Medium cognitive load
  'n8n': { base: 65, visual: 70, memory: 60, attention: 70 },
  'mealie': { base: 40, visual: 45, memory: 35, attention: 50 },
  'dispatch': { base: 75, visual: 65, memory: 80, attention: 85 },
  'actual-budget': { base: 55, visual: 60, memory: 50, attention: 65 },
  
  // MTG domain - Variable cognitive load
  'commander-spellbook': { base: 70, visual: 80, memory: 85, attention: 75 },
  'mtg-scripting': { base: 80, visual: 70, memory: 90, attention: 85 },
  
  // AI domain - High processing load
  'chroma-mcp': { base: 75, visual: 60, memory: 85, attention: 80 },
  'firecrawl': { base: 60, visual: 55, memory: 65, attention: 70 }
} as const;

export function CognitiveLoadManager({ 
  className = '', 
  autoManage = true, 
  onLoadChange 
}: CognitiveLoadManagerProps) {
  const sharedContext = useSharedContext();
  const { markUIInteraction, enableFocusMode, getCurrentMetrics } = usePerformanceMonitor();
  
  const [currentLoad, setCurrentLoad] = useState<CognitiveLoad>({
    visual: 20,
    cognitive: 25,
    memory: 20,
    attention: 30,
    total: 24
  });
  
  const [activeTasks, setActiveTasks] = useState<TaskComplexity[]>([]);
  const [recommendations, setRecommendations] = useState<LoadRecommendation[]>([]);
  const [loadHistory, setLoadHistory] = useState<{ timestamp: number; load: CognitiveLoad }[]>([]);
  const [showDetails, setShowDetails] = useState(false);
  const [adaptiveMode, setAdaptiveMode] = useState(true);
  const [userFatigueLevel, setUserFatigueLevel] = useState(0); // 0-100

  // Monitor current tool and context switches
  useEffect(() => {
    const currentTool = sharedContext.userFocus.currentTool;
    const contextSwitches = sharedContext.userFocus.contextSwitches || 0;
    
    if (currentTool) {
      updateCognitiveLoad(currentTool, contextSwitches);
    }
  }, [sharedContext.userFocus.currentTool, sharedContext.userFocus.contextSwitches]);

  // Track load over time
  useEffect(() => {
    const interval = setInterval(() => {
      setLoadHistory(prev => {
        const newEntry = { timestamp: Date.now(), load: currentLoad };
        return [newEntry, ...prev.slice(0, 59)]; // Keep 60 entries (1 hour of data)
      });
      
      // Calculate fatigue based on sustained high load
      const recentHighLoad = loadHistory.slice(0, 10).filter(entry => entry.load.total > LOAD_THRESHOLDS.warning.total).length;
      setUserFatigueLevel(Math.min(100, recentHighLoad * 10));
      
      // Generate recommendations if auto-manage is enabled
      if (autoManage) {
        generateRecommendations(currentLoad, userFatigueLevel);
      }
    }, 60000); // Update every minute

    return () => clearInterval(interval);
  }, [currentLoad, autoManage, userFatigueLevel]);

  const updateCognitiveLoad = useCallback((toolId: string, contextSwitches: number) => {
    const toolProfile = TOOL_COMPLEXITY_PROFILES[toolId as keyof typeof TOOL_COMPLEXITY_PROFILES];
    
    if (!toolProfile) {
      // Default profile for unknown tools
      const defaultLoad = {
        visual: 40,
        cognitive: 45,
        memory: 40,
        attention: 50,
        total: 44
      };
      setCurrentLoad(defaultLoad);
      onLoadChange?.(defaultLoad);
      return;
    }

    // Calculate dynamic load based on context switches, fatigue, and tool complexity
    const contextSwitchPenalty = Math.min(contextSwitches * 5, 30); // Max 30% penalty
    const fatiguePenalty = userFatigueLevel * 0.3; // Up to 30% increase when fatigued
    const timeOfDayAdjustment = getTimeOfDayAdjustment();
    
    const calculatedLoad = {
      visual: Math.min(100, toolProfile.visual + contextSwitchPenalty * 0.5 + timeOfDayAdjustment),
      cognitive: Math.min(100, toolProfile.base + contextSwitchPenalty + fatiguePenalty + timeOfDayAdjustment),
      memory: Math.min(100, toolProfile.memory + contextSwitchPenalty * 0.8 + fatiguePenalty * 0.8),
      attention: Math.min(100, toolProfile.attention + contextSwitchPenalty * 1.2 + fatiguePenalty * 0.6),
      total: 0
    };
    
    // Calculate weighted total (attention and cognitive load are most important)
    calculatedLoad.total = Math.round(
      (calculatedLoad.visual * 0.15) +
      (calculatedLoad.cognitive * 0.35) +
      (calculatedLoad.memory * 0.25) +
      (calculatedLoad.attention * 0.25)
    );

    setCurrentLoad(calculatedLoad);
    onLoadChange?.(calculatedLoad);
    markUIInteraction('cognitive-load-update');
  }, [userFatigueLevel, onLoadChange, markUIInteraction]);

  const getTimeOfDayAdjustment = (): number => {
    const hour = new Date().getHours();
    
    // Peak performance hours: 9-11 AM, 2-4 PM (reduced load)
    if ((hour >= 9 && hour <= 11) || (hour >= 14 && hour <= 16)) {
      return -10;
    }
    
    // Low energy hours: 1-3 PM, 7-9 PM (increased load)
    if ((hour >= 13 && hour <= 15) || (hour >= 19 && hour <= 21)) {
      return 15;
    }
    
    // Very low energy: early morning, late evening (high load increase)
    if (hour < 7 || hour > 22) {
      return 25;
    }
    
    return 0;
  };

  const generateRecommendations = (load: CognitiveLoad, fatigue: number) => {
    const newRecommendations: LoadRecommendation[] = [];

    // Critical load recommendations
    if (load.total > LOAD_THRESHOLDS.critical.total) {
      newRecommendations.push({
        type: 'break',
        message: 'Cognitive overload detected. Take a 15-20 minute break immediately.',
        severity: 'critical',
        actionRequired: true,
        suggestedDuration: 20,
        alternatives: ['Switch to low-complexity task', 'Use focus mode with reduced scope']
      });
    }
    
    // High attention load
    if (load.attention > LOAD_THRESHOLDS.critical.attention) {
      newRecommendations.push({
        type: 'simplify',
        message: 'Attention demand is very high. Consider simplifying the current task or using focus mode.',
        severity: 'warning',
        actionRequired: true,
        alternatives: ['Enable focus mode', 'Break task into smaller steps', 'Remove distractions']
      });
    }
    
    // High memory load
    if (load.memory > LOAD_THRESHOLDS.warning.memory) {
      newRecommendations.push({
        type: 'reduce',
        message: 'Working memory is strained. Close unnecessary tools or use external memory aids.',
        severity: 'warning',
        actionRequired: false,
        alternatives: ['Take notes for current progress', 'Close unused browser tabs', 'Use workflow templates']
      });
    }
    
    // Context switching penalty
    const contextSwitches = sharedContext.userFocus.contextSwitches || 0;
    if (contextSwitches > 5) {
      newRecommendations.push({
        type: 'simplify',
        message: `High context switching (${contextSwitches} switches). Focus on one domain at a time.`,
        severity: 'warning',
        actionRequired: false,
        alternatives: ['Enable focus mode', 'Batch similar tasks', 'Use workflow automation']
      });
    }
    
    // Fatigue-based recommendations
    if (fatigue > 70) {
      newRecommendations.push({
        type: 'break',
        message: 'High fatigue detected from sustained cognitive load. Consider a longer break or switching tasks.',
        severity: 'warning',
        actionRequired: true,
        suggestedDuration: 30,
        alternatives: ['Switch to low-complexity tasks', 'End work session', 'Take physical break']
      });
    }
    
    // Time-based recommendations
    const hour = new Date().getHours();
    if (hour > 20 && load.total > LOAD_THRESHOLDS.warning.total) {
      newRecommendations.push({
        type: 'defer',
        message: 'High cognitive load during low-energy hours. Consider deferring complex tasks.',
        severity: 'info',
        actionRequired: false,
        alternatives: ['Schedule for peak hours tomorrow', 'Switch to routine tasks', 'End work session']
      });
    }

    setRecommendations(newRecommendations);
  };

  const applyRecommendation = (recommendation: LoadRecommendation) => {
    markUIInteraction(`apply-recommendation-${recommendation.type}`);
    
    switch (recommendation.type) {
      case 'break':
        if (recommendation.suggestedDuration) {
          // Could integrate with AdvancedFocusMode for break timer
          alert(`Taking a ${recommendation.suggestedDuration}-minute break. Set a timer and step away from the screen.`);
        }
        break;
        
      case 'simplify':
        // Could trigger focus mode or workflow simplification
        enableFocusMode();
        break;
        
      case 'reduce':
        // Could trigger automatic cleanup or suggestions
        setShowDetails(true);
        break;
        
      case 'defer':
        // Could add to task queue for later
        console.log('Task deferred for optimal timing');
        break;
    }
  };

  const dismissRecommendation = (index: number) => {
    setRecommendations(prev => prev.filter((_, i) => i !== index));
    markUIInteraction('dismiss-recommendation');
  };

  const getLoadColor = (value: number): string => {
    if (value < LOAD_THRESHOLDS.optimal.total) return 'text-green-600';
    if (value < LOAD_THRESHOLDS.warning.total) return 'text-yellow-600';
    return 'text-red-600';
  };

  const getLoadBarColor = (value: number): string => {
    if (value < LOAD_THRESHOLDS.optimal.total) return 'bg-green-500';
    if (value < LOAD_THRESHOLDS.warning.total) return 'bg-yellow-500';
    return 'bg-red-500';
  };

  return (
    <div className={`cognitive-load-manager ${className}`}>
      <div className="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 p-4">
        {/* Header */}
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
            Cognitive Load Monitor
          </h3>
          <div className="flex items-center gap-2">
            <button
              onClick={() => setAdaptiveMode(!adaptiveMode)}
              className={`px-3 py-1 text-sm rounded ${
                adaptiveMode 
                  ? 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200' 
                  : 'bg-gray-100 text-gray-600 dark:bg-gray-700 dark:text-gray-400'
              }`}
            >
              Auto-Adapt {adaptiveMode ? 'On' : 'Off'}
            </button>
            <button
              onClick={() => setShowDetails(!showDetails)}
              className="text-sm text-blue-600 hover:text-blue-700 dark:text-blue-400"
            >
              {showDetails ? 'Hide' : 'Details'}
            </button>
          </div>
        </div>

        {/* Current Load Display */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4">
          {Object.entries(currentLoad).map(([key, value]) => (
            <div key={key} className="text-center">
              <div className={`text-2xl font-bold ${getLoadColor(value)}`}>
                {Math.round(value)}%
              </div>
              <div className="text-xs text-gray-500 dark:text-gray-400 capitalize mb-1">
                {key}
              </div>
              <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                <div
                  className={`h-2 rounded-full transition-all duration-500 ${getLoadBarColor(value)}`}
                  style={{ width: `${Math.min(100, value)}%` }}
                />
              </div>
            </div>
          ))}
        </div>

        {/* Fatigue Indicator */}
        {userFatigueLevel > 30 && (
          <div className="mb-4 p-3 bg-orange-50 dark:bg-orange-900/20 border border-orange-200 dark:border-orange-700 rounded-lg">
            <div className="flex items-center justify-between">
              <span className="text-orange-800 dark:text-orange-200 font-medium">
                Fatigue Level: {Math.round(userFatigueLevel)}%
              </span>
              <span className="text-sm text-orange-600 dark:text-orange-300">
                Consider taking breaks more frequently
              </span>
            </div>
          </div>
        )}

        {/* Active Recommendations */}
        {recommendations.length > 0 && (
          <div className="mb-4 space-y-2">
            <h4 className="font-medium text-gray-900 dark:text-white">Recommendations</h4>
            {recommendations.map((rec, index) => (
              <div
                key={index}
                className={`p-3 rounded-lg border ${
                  rec.severity === 'critical' 
                    ? 'bg-red-50 border-red-200 dark:bg-red-900/20 dark:border-red-700'
                    : rec.severity === 'warning'
                    ? 'bg-yellow-50 border-yellow-200 dark:bg-yellow-900/20 dark:border-yellow-700'
                    : 'bg-blue-50 border-blue-200 dark:bg-blue-900/20 dark:border-blue-700'
                }`}
              >
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <p className={`font-medium ${
                      rec.severity === 'critical' ? 'text-red-800 dark:text-red-200' :
                      rec.severity === 'warning' ? 'text-yellow-800 dark:text-yellow-200' :
                      'text-blue-800 dark:text-blue-200'
                    }`}>
                      {rec.message}
                    </p>
                    {rec.alternatives && (
                      <ul className="mt-2 text-sm text-gray-600 dark:text-gray-400">
                        {rec.alternatives.map((alt, altIndex) => (
                          <li key={altIndex} className="ml-4">• {alt}</li>
                        ))}
                      </ul>
                    )}
                  </div>
                  <div className="flex gap-2 ml-4">
                    {rec.actionRequired && (
                      <button
                        onClick={() => applyRecommendation(rec)}
                        className="px-3 py-1 text-sm bg-white dark:bg-gray-700 border border-gray-300 dark:border-gray-600 rounded hover:bg-gray-50 dark:hover:bg-gray-600 transition-colors"
                      >
                        Apply
                      </button>
                    )}
                    <button
                      onClick={() => dismissRecommendation(index)}
                      className="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300"
                    >
                      ×
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}

        {/* Detailed View */}
        {showDetails && (
          <div className="border-t border-gray-200 dark:border-gray-600 pt-4 mt-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {/* Current Context */}
              <div>
                <h5 className="font-medium text-gray-900 dark:text-white mb-2">Current Context</h5>
                <div className="text-sm space-y-1">
                  <div>
                    <span className="text-gray-500 dark:text-gray-400">Tool:</span>
                    <span className="ml-2 text-gray-900 dark:text-white">
                      {sharedContext.userFocus.currentTool || 'None'}
                    </span>
                  </div>
                  <div>
                    <span className="text-gray-500 dark:text-gray-400">Context Switches:</span>
                    <span className="ml-2 text-gray-900 dark:text-white">
                      {sharedContext.userFocus.contextSwitches || 0}
                    </span>
                  </div>
                  <div>
                    <span className="text-gray-500 dark:text-gray-400">Time of Day:</span>
                    <span className="ml-2 text-gray-900 dark:text-white">
                      {new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                    </span>
                  </div>
                </div>
              </div>

              {/* Load Trend */}
              <div>
                <h5 className="font-medium text-gray-900 dark:text-white mb-2">Recent Trend</h5>
                <div className="text-sm">
                  {loadHistory.length > 0 ? (
                    <div className="space-y-1">
                      {loadHistory.slice(0, 3).map((entry, index) => (
                        <div key={index} className="flex justify-between">
                          <span className="text-gray-500 dark:text-gray-400">
                            {new Date(entry.timestamp).toLocaleTimeString([], { 
                              hour: '2-digit', 
                              minute: '2-digit' 
                            })}
                          </span>
                          <span className={`font-medium ${getLoadColor(entry.load.total)}`}>
                            {Math.round(entry.load.total)}%
                          </span>
                        </div>
                      ))}
                    </div>
                  ) : (
                    <span className="text-gray-500 dark:text-gray-400">No history available</span>
                  )}
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Quick Actions */}
        <div className="flex gap-2 mt-4 pt-4 border-t border-gray-200 dark:border-gray-600">
          <button
            onClick={() => enableFocusMode()}
            className="px-3 py-1 text-sm bg-blue-600 text-white rounded hover:bg-blue-700 transition-colors"
          >
            Enable Focus
          </button>
          <button
            onClick={() => setRecommendations([])}
            className="px-3 py-1 text-sm border border-gray-300 dark:border-gray-600 rounded hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors"
          >
            Clear Alerts
          </button>
          <button
            onClick={() => {
              setLoadHistory([]);
              setUserFatigueLevel(0);
              markUIInteraction('reset-cognitive-load');
            }}
            className="px-3 py-1 text-sm text-gray-600 dark:text-gray-400 hover:text-gray-800 dark:hover:text-gray-200"
          >
            Reset
          </button>
        </div>
      </div>
    </div>
  );
}