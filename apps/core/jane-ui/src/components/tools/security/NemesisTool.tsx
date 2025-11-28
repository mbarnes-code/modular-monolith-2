'use client';

import React, { useEffect, useState } from 'react';
import { usePerformanceMonitor } from '../../../services/performance/performanceMonitor';
import { ToolComponentProps } from '../../../services/toolLoader';

export function NemesisTool({ onClose, onError, toolId = 'nemesis', ...props }: ToolComponentProps) {
  const { measureOperation } = usePerformanceMonitor();
  const [isInitialized, setIsInitialized] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const initializeTool = async () => {
      try {
        await measureOperation(
          'nemesis-tool-init',
          async () => {
            await new Promise(resolve => setTimeout(resolve, 1200));
            setIsInitialized(true);
          },
          'security'
        );
      } catch (err) {
        const errorMsg = err instanceof Error ? err.message : 'Failed to initialize Nemesis';
        setError(errorMsg);
        onError?.(new Error(errorMsg));
      }
    };

    initializeTool();
  }, [measureOperation, onError]);

  if (error) {
    return (
      <div className="nemesis-tool-error p-6 bg-red-50 border border-red-200 rounded-lg">
        <h3 className="text-lg font-semibold text-red-800 mb-2">❌ Nemesis Tool Error</h3>
        <p className="text-red-700">{error}</p>
        <button onClick={onClose} className="mt-4 px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700">
          Close Tool
        </button>
      </div>
    );
  }

  if (!isInitialized) {
    return (
      <div className="nemesis-tool-loading flex items-center justify-center p-8 bg-purple-50 rounded-lg">
        <div className="text-center">
          <div className="animate-spin h-8 w-8 border-2 border-purple-500 border-t-transparent rounded-full mx-auto mb-4"></div>
          <p className="text-sm text-purple-600">Initializing Nemesis...</p>
          <p className="text-xs text-purple-400 mt-1">Post-exploitation data triage system</p>
        </div>
      </div>
    );
  }

  return (
    <div className="nemesis-tool bg-white border border-gray-200 rounded-lg shadow-sm" {...props}>
      <div className="nemesis-tool-header flex items-center justify-between p-4 border-b border-gray-200">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 bg-purple-100 rounded-lg flex items-center justify-center">
            <span className="text-purple-600 font-bold">⚔️</span>
          </div>
          <div>
            <h2 className="text-lg font-semibold text-gray-900">Nemesis</h2>
            <p className="text-sm text-gray-500">Post-Exploitation Data Triage</p>
          </div>
        </div>
        {onClose && (
          <button onClick={onClose} className="text-gray-400 hover:text-gray-600 transition-colors">
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        )}
      </div>

      <div className="nemesis-tool-content p-6">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="space-y-4">
            <div className="bg-purple-50 border border-purple-200 rounded-lg p-4">
              <h3 className="text-sm font-semibold text-purple-800 mb-2">📂 Data Sources</h3>
              <div className="space-y-2 text-xs">
                <div className="flex justify-between">
                  <span>File artifacts</span>
                  <span className="font-bold text-purple-700">1,247</span>
                </div>
                <div className="flex justify-between">
                  <span>Registry keys</span>
                  <span className="font-bold text-purple-700">89</span>
                </div>
                <div className="flex justify-between">
                  <span>Process data</span>
                  <span className="font-bold text-purple-700">156</span>
                </div>
              </div>
            </div>
            
            <div className="bg-orange-50 border border-orange-200 rounded-lg p-4">
              <h3 className="text-sm font-semibold text-orange-800 mb-2">🔍 Analysis Status</h3>
              <div className="space-y-2">
                <div className="flex items-center justify-between text-xs">
                  <span>Processing</span>
                  <div className="w-20 bg-gray-200 rounded-full h-2">
                    <div className="bg-orange-500 h-2 rounded-full" style={{ width: '65%' }}></div>
                  </div>
                </div>
                <div className="text-xs text-orange-600">65% complete • ~3 min remaining</div>
              </div>
            </div>
          </div>
          
          <div className="space-y-4">
            <div className="bg-red-50 border border-red-200 rounded-lg p-4">
              <h3 className="text-sm font-semibold text-red-800 mb-2">⚠️ Threat Indicators</h3>
              <div className="space-y-2">
                <div className="flex items-center gap-2 text-xs">
                  <span className="w-2 h-2 bg-red-500 rounded-full"></span>
                  <span>Suspicious PowerShell execution</span>
                </div>
                <div className="flex items-center gap-2 text-xs">
                  <span className="w-2 h-2 bg-yellow-500 rounded-full"></span>
                  <span>Unusual network connections</span>
                </div>
                <div className="flex items-center gap-2 text-xs">
                  <span className="w-2 h-2 bg-orange-500 rounded-full"></span>
                  <span>Modified system files</span>
                </div>
              </div>
            </div>
            
            <div className="bg-green-50 border border-green-200 rounded-lg p-4">
              <h3 className="text-sm font-semibold text-green-800 mb-2">✅ Enrichment Complete</h3>
              <div className="text-xs text-green-700">847 artifacts processed and categorized</div>
            </div>
          </div>
        </div>
        
        <div className="mt-6 flex gap-3">
          <button className="flex-1 bg-purple-600 text-white px-4 py-2 rounded-lg hover:bg-purple-700 transition-colors text-sm">
            📊 View Dashboard
          </button>
          <button className="flex-1 bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors text-sm">
            🔍 Deep Analysis
          </button>
          <button className="flex-1 bg-gray-600 text-white px-4 py-2 rounded-lg hover:bg-gray-700 transition-colors text-sm">
            📋 Export Report
          </button>
        </div>
      </div>
    </div>
  );
}