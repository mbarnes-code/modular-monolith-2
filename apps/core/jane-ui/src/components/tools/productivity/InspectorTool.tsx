'use client';

import { useEffect, useState } from 'react';
import { usePerformanceMonitor } from '../../../services/performance/performanceMonitor';
import { ToolComponentProps } from '../../../services/toolLoader';

export function InspectorTool({ onClose, onError, toolId = 'inspector', ...props }: ToolComponentProps) {
  const { measureOperation } = usePerformanceMonitor();
  const [isInitialized, setIsInitialized] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const initializeTool = async () => {
      try {
        await measureOperation(
          'inspector-tool-init',
          async () => {
            await new Promise(resolve => setTimeout(resolve, 400));
            setIsInitialized(true);
          },
          'productivity'
        );
      } catch (err) {
        const errorMsg = err instanceof Error ? err.message : 'Failed to initialize Inspector';
        setError(errorMsg);
        onError?.(new Error(errorMsg));
      }
    };

    initializeTool();
  }, [measureOperation, onError]);

  if (error) {
    return (
      <div className="inspector-tool-error p-6 bg-red-50 border border-red-200 rounded-lg">
        <h3 className="text-lg font-semibold text-red-800 mb-2">❌ Inspector Tool Error</h3>
        <p className="text-red-700">{error}</p>
        <button onClick={onClose} className="mt-4 px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700">
          Close Tool
        </button>
      </div>
    );
  }

  if (!isInitialized) {
    return (
      <div className="inspector-tool-loading flex items-center justify-center p-8 bg-indigo-50 rounded-lg">
        <div className="text-center">
          <div className="animate-spin h-8 w-8 border-2 border-indigo-500 border-t-transparent rounded-full mx-auto mb-4"></div>
          <p className="text-sm text-indigo-600">Initializing Inspector...</p>
          <p className="text-xs text-indigo-400 mt-1">Code and document analysis toolkit</p>
        </div>
      </div>
    );
  }

  return (
    <div className="inspector-tool bg-white border border-gray-200 rounded-lg shadow-sm" {...props}>
      <div className="inspector-tool-header flex items-center justify-between p-4 border-b border-gray-200">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 bg-indigo-100 rounded-lg flex items-center justify-center">
            <span className="text-indigo-600 font-bold">🔍</span>
          </div>
          <div>
            <h2 className="text-lg font-semibold text-gray-900">Inspector</h2>
            <p className="text-sm text-gray-500">Code & Document Analysis Toolkit</p>
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

      <div className="inspector-tool-content p-6">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div className="space-y-4">
            <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
              <h3 className="text-sm font-semibold text-blue-800 mb-3">📁 Analysis Tools</h3>
              <div className="grid grid-cols-2 gap-2">
                <button className="p-3 bg-white border border-blue-200 rounded text-xs hover:bg-blue-100 text-left">
                  <div className="font-semibold text-gray-800">📝 Code Review</div>
                  <div className="text-gray-600">Static analysis & linting</div>
                </button>
                <button className="p-3 bg-white border border-blue-200 rounded text-xs hover:bg-blue-100 text-left">
                  <div className="font-semibold text-gray-800">📈 Metrics</div>
                  <div className="text-gray-600">Complexity & coverage</div>
                </button>
                <button className="p-3 bg-white border border-blue-200 rounded text-xs hover:bg-blue-100 text-left">
                  <div className="font-semibold text-gray-800">🔍 Dependencies</div>
                  <div className="text-gray-600">Package analysis</div>
                </button>
                <button className="p-3 bg-white border border-blue-200 rounded text-xs hover:bg-blue-100 text-left">
                  <div className="font-semibold text-gray-800">🛡️ Security</div>
                  <div className="text-gray-600">Vulnerability scan</div>
                </button>
              </div>
            </div>
            
            <div className="bg-green-50 border border-green-200 rounded-lg p-4">
              <h3 className="text-sm font-semibold text-green-800 mb-3">📄 Recent Analysis</h3>
              <div className="space-y-2">
                <div className="bg-white rounded-lg p-3 border border-green-100">
                  <div className="flex items-center justify-between mb-2">
                    <h4 className="text-sm font-semibold text-gray-800">jane-ui/src/components</h4>
                    <span className="text-xs px-2 py-1 bg-green-100 text-green-800 rounded">Clean</span>
                  </div>
                  <div className="text-xs text-gray-600 mb-2">TypeScript • React components • 2 hours ago</div>
                  <div className="flex items-center gap-4 text-xs">
                    <span className="text-green-600">0 issues</span>
                    <span className="text-blue-600">85% coverage</span>
                    <span className="text-purple-600">Low complexity</span>
                  </div>
                </div>
                
                <div className="bg-white rounded-lg p-3 border border-yellow-100">
                  <div className="flex items-center justify-between mb-2">
                    <h4 className="text-sm font-semibold text-gray-800">security/DispatchTool.tsx</h4>
                    <span className="text-xs px-2 py-1 bg-yellow-100 text-yellow-800 rounded">Warnings</span>
                  </div>
                  <div className="text-xs text-gray-600 mb-2">TypeScript • React component • 1 hour ago</div>
                  <div className="flex items-center gap-4 text-xs">
                    <span className="text-yellow-600">3 warnings</span>
                    <span className="text-blue-600">78% coverage</span>
                    <span className="text-orange-600">Medium complexity</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
          
          <div className="space-y-4">
            <div className="bg-orange-50 border border-orange-200 rounded-lg p-4">
              <h3 className="text-sm font-semibold text-orange-800 mb-3">⚠️ Issues Found</h3>
              <div className="space-y-2 text-xs">
                <div className="bg-white rounded p-2 border border-red-200">
                  <div className="flex items-center justify-between mb-1">
                    <span className="font-semibold text-red-700">ESLint Error</span>
                    <span className="text-gray-500">Line 45</span>
                  </div>
                  <div className="text-gray-700">Unused variable 'errorHandler'</div>
                  <div className="text-red-600">toolLoader.ts</div>
                </div>
                
                <div className="bg-white rounded p-2 border border-yellow-200">
                  <div className="flex items-center justify-between mb-1">
                    <span className="font-semibold text-yellow-700">TypeScript Warning</span>
                    <span className="text-gray-500">Line 23</span>
                  </div>
                  <div className="text-gray-700">Property might be undefined</div>
                  <div className="text-yellow-600">DispatchTool.tsx</div>
                </div>
                
                <div className="bg-white rounded p-2 border border-blue-200">
                  <div className="flex items-center justify-between mb-1">
                    <span className="font-semibold text-blue-700">Code Style</span>
                    <span className="text-gray-500">Line 12</span>
                  </div>
                  <div className="text-gray-700">Prefer const assertion</div>
                  <div className="text-blue-600">cognitiveLoadManager.ts</div>
                </div>
              </div>
            </div>
            
            <div className="bg-purple-50 border border-purple-200 rounded-lg p-4">
              <h3 className="text-sm font-semibold text-purple-800 mb-3">📈 Project Metrics</h3>
              <div className="grid grid-cols-2 gap-3">
                <div className="bg-white rounded p-3 text-center">
                  <div className="text-lg font-bold text-blue-600">47</div>
                  <div className="text-xs text-gray-600">Files Analyzed</div>
                </div>
                <div className="bg-white rounded p-3 text-center">
                  <div className="text-lg font-bold text-green-600">82%</div>
                  <div className="text-xs text-gray-600">Test Coverage</div>
                </div>
                <div className="bg-white rounded p-3 text-center">
                  <div className="text-lg font-bold text-purple-600">3.2</div>
                  <div className="text-xs text-gray-600">Avg Complexity</div>
                </div>
                <div className="bg-white rounded p-3 text-center">
                  <div className="text-lg font-bold text-orange-600">12</div>
                  <div className="text-xs text-gray-600">Dependencies</div>
                </div>
              </div>
            </div>
            
            <div className="bg-gray-50 border border-gray-200 rounded-lg p-4">
              <h3 className="text-sm font-semibold text-gray-800 mb-2">🎯 Executive Function Features</h3>
              <div className="space-y-2 text-xs">
                <div className="flex items-center gap-2">
                  <span className="text-green-600">✅</span>
                  <span>Quick issue prioritization</span>
                </div>
                <div className="flex items-center gap-2">
                  <span className="text-green-600">✅</span>
                  <span>Visual code quality indicators</span>
                </div>
                <div className="flex items-center gap-2">
                  <span className="text-green-600">✅</span>
                  <span>Automated fix suggestions</span>
                </div>
                <div className="flex items-center gap-2">
                  <span className="text-green-600">✅</span>
                  <span>Progress tracking for improvements</span>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <div className="mt-6 flex gap-3">
          <button className="flex-1 bg-indigo-600 text-white px-4 py-2 rounded-lg hover:bg-indigo-700 transition-colors text-sm">
            🔍 Analyze Project
          </button>
          <button className="flex-1 bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors text-sm">
            📈 View Report
          </button>
          <button className="flex-1 bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 transition-colors text-sm">
            ⚙️ Configure
          </button>
        </div>
      </div>
    </div>
  );
}