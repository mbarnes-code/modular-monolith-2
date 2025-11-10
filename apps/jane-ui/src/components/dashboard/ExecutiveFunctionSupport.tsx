/**
 * Executive Function Support Component
 * 
 * Provides real-time cognitive load monitoring and accommodations
 */

'use client';

import React from 'react';

interface ExecutiveFunctionConfig {
  adhdSupport: boolean;
  autismSupport: boolean;
  reducedAnimations: boolean;
  highContrast: boolean;
  largeText: boolean;
  cognitiveLoadReduction: boolean;
  contextSwitchingMinimization: boolean;
  responseTimeOptimization: boolean;
}

interface ExecutiveFunctionSupportProps {
  config: ExecutiveFunctionConfig;
  cognitiveLoad: 'low' | 'medium' | 'high';
  onLoadReduction: () => void;
}

export const ExecutiveFunctionSupport: React.FC<ExecutiveFunctionSupportProps> = ({
  config,
  cognitiveLoad,
  onLoadReduction
}) => {
  if (!config.adhdSupport && !config.autismSupport) {
    return null;
  }

  return (
    <div className="fixed top-4 right-4 z-50">
      <div className="bg-white border border-gray-200 rounded-lg shadow-lg p-3 max-w-xs">
        <div className="flex items-center justify-between mb-2">
          <span className="text-sm font-medium text-gray-700">
            Executive Function
          </span>
          <div className={`w-3 h-3 rounded-full ${
            cognitiveLoad === 'low' ? 'bg-green-400' :
            cognitiveLoad === 'medium' ? 'bg-amber-400' :
            'bg-red-400'
          }`} />
        </div>
        
        <div className="text-xs text-gray-500 space-y-1">
          {config.adhdSupport && (
            <div className="flex items-center">
              <div className="w-2 h-2 bg-blue-400 rounded-full mr-2"></div>
              <span>ADHD accommodations active</span>
            </div>
          )}
          {config.autismSupport && (
            <div className="flex items-center">
              <div className="w-2 h-2 bg-purple-400 rounded-full mr-2"></div>
              <span>Autism accommodations active</span>
            </div>
          )}
        </div>

        {cognitiveLoad === 'high' && (
          <button
            onClick={onLoadReduction}
            className="mt-2 w-full px-2 py-1 bg-amber-100 text-amber-800 rounded text-xs hover:bg-amber-200 transition-colors"
          >
            Reduce Cognitive Load
          </button>
        )}
      </div>
    </div>
  );
};