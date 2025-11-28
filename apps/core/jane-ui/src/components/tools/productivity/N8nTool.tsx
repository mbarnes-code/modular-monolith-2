'use client';

import { useEffect, useState } from 'react';
import { usePerformanceMonitor } from '../../../services/performance/performanceMonitor';
import { ToolComponentProps } from '../../../services/toolLoader';

export function N8nTool({ onClose, onError, toolId = 'n8n', ...props }: ToolComponentProps) {
  const { measureOperation } = usePerformanceMonitor();
  const [isInitialized, setIsInitialized] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const initializeTool = async () => {
      try {
        await measureOperation(
          'n8n-tool-init',
          async () => {
            await new Promise(resolve => setTimeout(resolve, 1000));
            setIsInitialized(true);
          },
          'productivity'
        );
      } catch (err) {
        const errorMsg = err instanceof Error ? err.message : 'Failed to initialize n8n';
        setError(errorMsg);
        onError?.(new Error(errorMsg));
      }
    };

    initializeTool();
  }, [measureOperation, onError]);

  if (error) {
    return (
      <div className="n8n-tool-error p-6 bg-red-50 border border-red-200 rounded-lg">
        <h3 className="text-lg font-semibold text-red-800 mb-2">❌ n8n Tool Error</h3>
        <p className="text-red-700">{error}</p>
        <button onClick={onClose} className="mt-4 px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700">
          Close Tool
        </button>
      </div>
    );
  }

  if (!isInitialized) {
    return (
      <div className="n8n-tool-loading flex items-center justify-center p-8 bg-purple-50 rounded-lg">
        <div className="text-center">
          <div className="animate-spin h-8 w-8 border-2 border-purple-500 border-t-transparent rounded-full mx-auto mb-4"></div>
          <p className="text-sm text-purple-600">Initializing n8n...</p>
          <p className="text-xs text-purple-400 mt-1">Workflow automation platform</p>
        </div>
      </div>
    );
  }

  return (
    <div className="n8n-tool bg-white border border-gray-200 rounded-lg shadow-sm" {...props}>
      <div className="n8n-tool-header flex items-center justify-between p-4 border-b border-gray-200">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 bg-purple-100 rounded-lg flex items-center justify-center">
            <span className="text-purple-600 font-bold">⚡</span>
          </div>
          <div>
            <h2 className="text-lg font-semibold text-gray-900">n8n</h2>
            <p className="text-sm text-gray-500">Workflow Automation Platform</p>
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

      <div className="n8n-tool-content p-6">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div className="space-y-4">
            <div className="bg-green-50 border border-green-200 rounded-lg p-4">
              <h3 className="text-sm font-semibold text-green-800 mb-3">✅ Active Workflows</h3>
              <div className="space-y-3">
                <div className="bg-white rounded-lg p-3 border border-green-100">
                  <div className="flex items-center justify-between mb-2">
                    <h4 className="text-sm font-semibold text-gray-800">Security Alert Processor</h4>
                    <div className="flex items-center gap-1">
                      <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                      <span className="text-xs text-green-700">Running</span>
                    </div>
                  </div>
                  <div className="text-xs text-gray-600 mb-2">MISP → Slack → Dispatch</div>
                  <div className="flex items-center justify-between text-xs">
                    <span>Last run: 2 min ago</span>
                    <span className="text-green-600">847 executions</span>
                  </div>
                </div>
                
                <div className="bg-white rounded-lg p-3 border border-green-100">
                  <div className="flex items-center justify-between mb-2">
                    <h4 className="text-sm font-semibold text-gray-800">Budget Tracker</h4>
                    <div className="flex items-center gap-1">
                      <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                      <span className="text-xs text-green-700">Running</span>
                    </div>
                  </div>
                  <div className="text-xs text-gray-600 mb-2">Bank API → Actual Budget → Notifications</div>
                  <div className="flex items-center justify-between text-xs">
                    <span>Last run: 1 hour ago</span>
                    <span className="text-green-600">1,203 executions</span>
                  </div>
                </div>
                
                <div className="bg-white rounded-lg p-3 border border-yellow-100">
                  <div className="flex items-center justify-between mb-2">
                    <h4 className="text-sm font-semibold text-gray-800">Meal Plan Generator</h4>
                    <div className="flex items-center gap-1">
                      <div className="w-2 h-2 bg-yellow-500 rounded-full"></div>
                      <span className="text-xs text-yellow-700">Paused</span>
                    </div>
                  </div>
                  <div className="text-xs text-gray-600 mb-2">Schedule → AI API → Mealie</div>
                  <div className="flex items-center justify-between text-xs">
                    <span>Last run: 2 days ago</span>
                    <span className="text-yellow-600">45 executions</span>
                  </div>
                </div>
              </div>
            </div>
            
            <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
              <h3 className="text-sm font-semibold text-blue-800 mb-3">📈 Execution Stats</h3>
              <div className="grid grid-cols-2 gap-4">
                <div className="bg-white rounded p-3 text-center">
                  <div className="text-lg font-bold text-green-600">2,095</div>
                  <div className="text-xs text-gray-600">Successful</div>
                </div>
                <div className="bg-white rounded p-3 text-center">
                  <div className="text-lg font-bold text-red-600">23</div>
                  <div className="text-xs text-gray-600">Failed</div>
                </div>
                <div className="bg-white rounded p-3 text-center">
                  <div className="text-lg font-bold text-blue-600">99.1%</div>
                  <div className="text-xs text-gray-600">Success Rate</div>
                </div>
                <div className="bg-white rounded p-3 text-center">
                  <div className="text-lg font-bold text-purple-600">3.2s</div>
                  <div className="text-xs text-gray-600">Avg Runtime</div>
                </div>
              </div>
            </div>
          </div>
          
          <div className="space-y-4">
            <div className="bg-orange-50 border border-orange-200 rounded-lg p-4">
              <h3 className="text-sm font-semibold text-orange-800 mb-3">🛠️ Workflow Templates</h3>
              <div className="space-y-2">
                <button className="w-full text-left p-3 bg-white border border-orange-200 rounded text-xs hover:bg-orange-100">
                  <div className="font-semibold text-gray-800">Email to Task</div>
                  <div className="text-gray-600">Gmail → Parser → Project Management</div>
                </button>
                <button className="w-full text-left p-3 bg-white border border-orange-200 rounded text-xs hover:bg-orange-100">
                  <div className="font-semibold text-gray-800">Social Media Monitor</div>
                  <div className="text-gray-600">Twitter API → Sentiment → Alerts</div>
                </button>
                <button className="w-full text-left p-3 bg-white border border-orange-200 rounded text-xs hover:bg-orange-100">
                  <div className="font-semibold text-gray-800">Data Backup</div>
                  <div className="text-gray-600">Database → Transform → Cloud Storage</div>
                </button>
                <button className="w-full text-left p-3 bg-white border border-orange-200 rounded text-xs hover:bg-orange-100">
                  <div className="font-semibold text-gray-800">Expense Tracker</div>
                  <div className="text-gray-600">Receipt Scanner → OCR → Budget App</div>
                </button>
              </div>
            </div>
            
            <div className="bg-red-50 border border-red-200 rounded-lg p-4">
              <h3 className="text-sm font-semibold text-red-800 mb-2">⚠️ Recent Errors</h3>
              <div className="space-y-2 text-xs">
                <div className="bg-white rounded p-2">
                  <div className="font-semibold text-red-700">API Rate Limit</div>
                  <div className="text-gray-700">Twitter API exceeded in Social Monitor</div>
                  <div className="text-gray-500">15 min ago</div>
                </div>
                <div className="bg-white rounded p-2">
                  <div className="font-semibold text-orange-700">Connection Timeout</div>
                  <div className="text-gray-700">Database connection failed in Backup workflow</div>
                  <div className="text-gray-500">1 hour ago</div>
                </div>
              </div>
            </div>
            
            <div className="bg-purple-50 border border-purple-200 rounded-lg p-4">
              <h3 className="text-sm font-semibold text-purple-800 mb-2">🎯 Executive Function Support</h3>
              <div className="space-y-2 text-xs">
                <div className="flex items-center gap-2">
                  <span className="text-green-600">✅</span>
                  <span>Visual workflow builder</span>
                </div>
                <div className="flex items-center gap-2">
                  <span className="text-green-600">✅</span>
                  <span>Template library for common tasks</span>
                </div>
                <div className="flex items-center gap-2">
                  <span className="text-green-600">✅</span>
                  <span>Error handling with retry logic</span>
                </div>
                <div className="flex items-center gap-2">
                  <span className="text-green-600">✅</span>
                  <span>Execution history and debugging</span>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <div className="mt-6 flex gap-3">
          <button className="flex-1 bg-purple-600 text-white px-4 py-2 rounded-lg hover:bg-purple-700 transition-colors text-sm">
            ➕ New Workflow
          </button>
          <button className="flex-1 bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors text-sm">
            📈 Analytics
          </button>
          <button className="flex-1 bg-orange-600 text-white px-4 py-2 rounded-lg hover:bg-orange-700 transition-colors text-sm">
            📚 Templates
          </button>
        </div>
      </div>
    </div>
  );
}