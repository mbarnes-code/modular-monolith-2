'use client';

import { useEffect, useState } from 'react';
import { COGNITIVE_LOAD_CONFIG, CognitiveLoadIndicatorProps, useCognitiveLoadStore } from '../../services/cognitiveLoad/cognitiveLoadManager';

export function CognitiveLoadIndicator({ showDetails = false, className = '' }: CognitiveLoadIndicatorProps) {
  const {
    activeTools,
    focusModeActive,
    focusModeStartTime,
    taskBreakdownActive,
    currentTaskSteps,
    completedSteps,
    getCognitiveLoadScore,
    getContextSwitchRate,
    canActivateNewTool,
  } = useCognitiveLoadStore();

  const [loadScore, setLoadScore] = useState(0);
  const [switchRate, setSwitchRate] = useState(0);
  const [focusTimeRemaining, setFocusTimeRemaining] = useState(0);

  // Update metrics every second
  useEffect(() => {
    const updateMetrics = () => {
      setLoadScore(getCognitiveLoadScore());
      setSwitchRate(getContextSwitchRate());
      
      if (focusModeActive && focusModeStartTime) {
        const elapsed = Date.now() - focusModeStartTime.getTime();
        const remaining = Math.max(0, COGNITIVE_LOAD_CONFIG.focusModeTimeout - elapsed);
        setFocusTimeRemaining(remaining);
      } else {
        setFocusTimeRemaining(0);
      }
    };

    updateMetrics();
    const interval = setInterval(updateMetrics, 1000);
    return () => clearInterval(interval);
  }, [getCognitiveLoadScore, getContextSwitchRate, focusModeActive, focusModeStartTime]);

  // Get load score color
  const getLoadScoreColor = (score: number) => {
    if (score < 30) return 'text-green-600 bg-green-50';
    if (score < 60) return 'text-yellow-600 bg-yellow-50';
    if (score < 80) return 'text-orange-600 bg-orange-50';
    return 'text-red-600 bg-red-50';
  };

  // Get load score icon
  const getLoadScoreIcon = (score: number) => {
    if (score < 30) return '🧠'; // Good cognitive state
    if (score < 60) return '🤔'; // Moderate load
    if (score < 80) return '😵‍💫'; // High load
    return '🤯'; // Overload
  };

  // Format time remaining
  const formatTimeRemaining = (ms: number) => {
    const minutes = Math.floor(ms / (1000 * 60));
    const seconds = Math.floor((ms % (1000 * 60)) / 1000);
    return `${minutes}:${seconds.toString().padStart(2, '0')}`;
  };

  return (
    <div className={`cognitive-load-indicator ${className}`}>
      {/* Compact indicator */}
      <div className={`inline-flex items-center gap-2 px-3 py-2 rounded-lg border ${getLoadScoreColor(loadScore)}`}>
        <span className="text-lg">{getLoadScoreIcon(loadScore)}</span>
        <div className="flex flex-col">
          <span className="text-xs font-medium">Cognitive Load</span>
          <span className="text-sm font-bold">{Math.round(loadScore)}%</span>
        </div>
        
        {/* Active tools count */}
        <div className="flex items-center gap-1">
          <span className="text-xs">Tools:</span>
          <span className={`text-xs font-bold ${
            activeTools.size >= COGNITIVE_LOAD_CONFIG.maxActiveTools ? 'text-red-600' : 'text-gray-600'
          }`}>
            {activeTools.size}/{COGNITIVE_LOAD_CONFIG.maxActiveTools}
          </span>
        </div>

        {/* Focus mode indicator */}
        {focusModeActive && (
          <div className="flex items-center gap-1 px-2 py-1 bg-purple-100 text-purple-800 rounded text-xs">
            <span>🎯</span>
            <span>Focus: {formatTimeRemaining(focusTimeRemaining)}</span>
          </div>
        )}
      </div>

      {/* Detailed breakdown */}
      {showDetails && (
        <div className="mt-4 space-y-3">
          {/* Active tools list */}
          <div className="bg-white border border-gray-200 rounded-lg p-4">
            <h4 className="text-sm font-semibold text-gray-900 mb-2">Active Tools</h4>
            {activeTools.size === 0 ? (
              <p className="text-xs text-gray-500">No active tools</p>
            ) : (
              <div className="space-y-2">
                {Array.from(activeTools.values()).map((tool) => (
                  <div key={tool.id} className="flex items-center justify-between text-xs">
                    <div className="flex items-center gap-2">
                      <span className={`w-2 h-2 rounded-full ${
                        tool.isInFocus ? 'bg-blue-500' : 'bg-gray-300'
                      }`} />
                      <span className="font-medium">{tool.name}</span>
                      <span className="text-gray-500">({tool.domain})</span>
                    </div>
                    <div className="flex items-center gap-2">
                      {tool.taskProgress > 0 && (
                        <div className="w-16 bg-gray-200 rounded-full h-1">
                          <div 
                            className="bg-blue-500 h-1 rounded-full" 
                            style={{ width: `${tool.taskProgress}%` }}
                          />
                        </div>
                      )}
                      <span className="text-gray-400">
                        {Math.round((Date.now() - tool.lastAccessed.getTime()) / 1000 / 60)}m
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* Task breakdown */}
          {taskBreakdownActive && currentTaskSteps.length > 0 && (
            <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
              <h4 className="text-sm font-semibold text-blue-900 mb-2">
                Task Progress ({completedSteps}/{currentTaskSteps.length})
              </h4>
              <div className="space-y-1">
                {currentTaskSteps.map((step, index) => (
                  <div key={index} className="flex items-center gap-2 text-xs">
                    <span className={`w-4 h-4 rounded flex items-center justify-center text-xs ${
                      index < completedSteps 
                        ? 'bg-green-500 text-white' 
                        : index === completedSteps 
                        ? 'bg-blue-500 text-white'
                        : 'bg-gray-200 text-gray-500'
                    }`}>
                      {index < completedSteps ? '✓' : index + 1}
                    </span>
                    <span className={index < completedSteps ? 'line-through text-gray-500' : 'text-gray-900'}>
                      {step}
                    </span>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Performance metrics */}
          <div className="bg-gray-50 border border-gray-200 rounded-lg p-4">
            <h4 className="text-sm font-semibold text-gray-900 mb-2">Performance Metrics</h4>
            <div className="grid grid-cols-2 gap-4 text-xs">
              <div>
                <span className="text-gray-600">Context Switches:</span>
                <span className="ml-2 font-bold">{switchRate.toFixed(1)}/min</span>
              </div>
              <div>
                <span className="text-gray-600">Can Add Tool:</span>
                <span className={`ml-2 font-bold ${
                  canActivateNewTool() ? 'text-green-600' : 'text-red-600'
                }`}>
                  {canActivateNewTool() ? 'Yes' : 'No'}
                </span>
              </div>
            </div>
          </div>

          {/* Executive function tips */}
          {loadScore > 70 && (
            <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
              <h4 className="text-sm font-semibold text-yellow-900 mb-2">💡 Executive Function Tips</h4>
              <ul className="text-xs text-yellow-800 space-y-1">
                <li>• Consider closing some tools to reduce cognitive load</li>
                <li>• Try focus mode for deep work on one tool</li>
                <li>• Take a short break to reset mental state</li>
                {!taskBreakdownActive && <li>• Break complex tasks into smaller steps</li>}
              </ul>
            </div>
          )}
        </div>
      )}
    </div>
  );
}