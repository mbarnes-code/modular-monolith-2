'use client';

import { useEffect, useState } from 'react';
import { usePerformanceMonitor } from '../../../services/performance/performanceMonitor';
import { ToolComponentProps } from '../../../services/toolLoader';

export function ActualTool({ onClose, onError, toolId = 'actual', ...props }: ToolComponentProps) {
  const { measureOperation } = usePerformanceMonitor();
  const [isInitialized, setIsInitialized] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const initializeTool = async () => {
      try {
        await measureOperation(
          'actual-tool-init',
          async () => {
            await new Promise(resolve => setTimeout(resolve, 800));
            setIsInitialized(true);
          },
          'productivity'
        );
      } catch (err) {
        const errorMsg = err instanceof Error ? err.message : 'Failed to initialize Actual Budget';
        setError(errorMsg);
        onError?.(new Error(errorMsg));
      }
    };

    initializeTool();
  }, [measureOperation, onError]);

  if (error) {
    return (
      <div className="actual-tool-error p-6 bg-red-50 border border-red-200 rounded-lg">
        <h3 className="text-lg font-semibold text-red-800 mb-2">❌ Actual Budget Tool Error</h3>
        <p className="text-red-700">{error}</p>
        <button onClick={onClose} className="mt-4 px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700">
          Close Tool
        </button>
      </div>
    );
  }

  if (!isInitialized) {
    return (
      <div className="actual-tool-loading flex items-center justify-center p-8 bg-blue-50 rounded-lg">
        <div className="text-center">
          <div className="animate-spin h-8 w-8 border-2 border-blue-500 border-t-transparent rounded-full mx-auto mb-4"></div>
          <p className="text-sm text-blue-600">Initializing Actual Budget...</p>
          <p className="text-xs text-blue-400 mt-1">Personal finance management</p>
        </div>
      </div>
    );
  }

  return (
    <div className="actual-tool bg-white border border-gray-200 rounded-lg shadow-sm" {...props}>
      <div className="actual-tool-header flex items-center justify-between p-4 border-b border-gray-200">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 bg-blue-100 rounded-lg flex items-center justify-center">
            <span className="text-blue-600 font-bold">💰</span>
          </div>
          <div>
            <h2 className="text-lg font-semibold text-gray-900">Actual Budget</h2>
            <p className="text-sm text-gray-500">Personal Finance Management</p>
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

      <div className="actual-tool-content p-6">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="lg:col-span-2 space-y-4">
            <div className="bg-green-50 border border-green-200 rounded-lg p-4">
              <h3 className="text-sm font-semibold text-green-800 mb-3">📈 Monthly Overview</h3>
              <div className="grid grid-cols-3 gap-4 mb-4">
                <div className="bg-white rounded-lg p-3 text-center">
                  <div className="text-xs text-gray-600 mb-1">Income</div>
                  <div className="text-lg font-bold text-green-600">$4,200</div>
                  <div className="text-xs text-green-500">↑ +2.3%</div>
                </div>
                <div className="bg-white rounded-lg p-3 text-center">
                  <div className="text-xs text-gray-600 mb-1">Expenses</div>
                  <div className="text-lg font-bold text-red-600">$3,150</div>
                  <div className="text-xs text-red-500">↑ +5.1%</div>
                </div>
                <div className="bg-white rounded-lg p-3 text-center">
                  <div className="text-xs text-gray-600 mb-1">Saved</div>
                  <div className="text-lg font-bold text-blue-600">$1,050</div>
                  <div className="text-xs text-blue-500">↓ -12.5%</div>
                </div>
              </div>
              
              <div className="bg-white rounded-lg p-3">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-xs font-medium text-gray-700">Budget Progress</span>
                  <span className="text-xs text-gray-500">75% of month elapsed</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-3">
                  <div className="bg-green-500 h-3 rounded-full" style={{ width: '68%' }}></div>
                </div>
                <div className="flex justify-between text-xs text-gray-600 mt-1">
                  <span>On track</span>
                  <span>68% spent</span>
                </div>
              </div>
            </div>
            
            <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
              <h3 className="text-sm font-semibold text-blue-800 mb-3">📋 Budget Categories</h3>
              <div className="space-y-3">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <div className="w-8 h-8 bg-orange-100 rounded-lg flex items-center justify-center">
                      <span className="text-orange-600 text-sm">🏠</span>
                    </div>
                    <div>
                      <div className="text-sm font-medium text-gray-800">Housing</div>
                      <div className="text-xs text-gray-600">$1,200 / $1,200</div>
                    </div>
                  </div>
                  <div className="text-right">
                    <div className="text-sm font-bold text-gray-800">100%</div>
                    <div className="w-16 bg-gray-200 rounded-full h-2">
                      <div className="bg-orange-500 h-2 rounded-full" style={{ width: '100%' }}></div>
                    </div>
                  </div>
                </div>
                
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <div className="w-8 h-8 bg-red-100 rounded-lg flex items-center justify-center">
                      <span className="text-red-600 text-sm">🍽️</span>
                    </div>
                    <div>
                      <div className="text-sm font-medium text-gray-800">Food</div>
                      <div className="text-xs text-gray-600">$380 / $450</div>
                    </div>
                  </div>
                  <div className="text-right">
                    <div className="text-sm font-bold text-gray-800">84%</div>
                    <div className="w-16 bg-gray-200 rounded-full h-2">
                      <div className="bg-red-500 h-2 rounded-full" style={{ width: '84%' }}></div>
                    </div>
                  </div>
                </div>
                
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <div className="w-8 h-8 bg-blue-100 rounded-lg flex items-center justify-center">
                      <span className="text-blue-600 text-sm">🚗</span>
                    </div>
                    <div>
                      <div className="text-sm font-medium text-gray-800">Transportation</div>
                      <div className="text-xs text-gray-600">$180 / $300</div>
                    </div>
                  </div>
                  <div className="text-right">
                    <div className="text-sm font-bold text-gray-800">60%</div>
                    <div className="w-16 bg-gray-200 rounded-full h-2">
                      <div className="bg-blue-500 h-2 rounded-full" style={{ width: '60%' }}></div>
                    </div>
                  </div>
                </div>
                
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <div className="w-8 h-8 bg-purple-100 rounded-lg flex items-center justify-center">
                      <span className="text-purple-600 text-sm">🎭</span>
                    </div>
                    <div>
                      <div className="text-sm font-medium text-gray-800">Entertainment</div>
                      <div className="text-xs text-gray-600">$95 / $200</div>
                    </div>
                  </div>
                  <div className="text-right">
                    <div className="text-sm font-bold text-gray-800">48%</div>
                    <div className="w-16 bg-gray-200 rounded-full h-2">
                      <div className="bg-purple-500 h-2 rounded-full" style={{ width: '48%' }}></div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          
          <div className="space-y-4">
            <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
              <h3 className="text-sm font-semibold text-yellow-800 mb-3">⚠️ Alerts</h3>
              <div className="space-y-2 text-xs">
                <div className="bg-white rounded p-2 border border-red-200">
                  <div className="font-semibold text-red-700">Overspent</div>
                  <div className="text-gray-700">Housing category exceeded by $50</div>
                </div>
                <div className="bg-white rounded p-2 border border-yellow-200">
                  <div className="font-semibold text-yellow-700">Upcoming</div>
                  <div className="text-gray-700">Car insurance due in 3 days</div>
                </div>
              </div>
            </div>
            
            <div className="bg-purple-50 border border-purple-200 rounded-lg p-4">
              <h3 className="text-sm font-semibold text-purple-800 mb-2">🎯 Executive Function Features</h3>
              <div className="space-y-2 text-xs">
                <div className="flex items-center gap-2">
                  <span className="text-green-600">✅</span>
                  <span>Automatic categorization</span>
                </div>
                <div className="flex items-center gap-2">
                  <span className="text-green-600">✅</span>
                  <span>Spending pattern analysis</span>
                </div>
                <div className="flex items-center gap-2">
                  <span className="text-green-600">✅</span>
                  <span>Goal tracking with progress</span>
                </div>
                <div className="flex items-center gap-2">
                  <span className="text-green-600">✅</span>
                  <span>Bill reminder system</span>
                </div>
              </div>
            </div>
            
            <div className="bg-gray-50 border border-gray-200 rounded-lg p-4">
              <h3 className="text-sm font-semibold text-gray-800 mb-3">🎯 Goals</h3>
              <div className="space-y-3">
                <div>
                  <div className="flex justify-between text-xs mb-1">
                    <span>Emergency Fund</span>
                    <span>$3,200 / $5,000</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2">
                    <div className="bg-green-500 h-2 rounded-full" style={{ width: '64%' }}></div>
                  </div>
                </div>
                
                <div>
                  <div className="flex justify-between text-xs mb-1">
                    <span>Vacation Fund</span>
                    <span>$850 / $2,000</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2">
                    <div className="bg-blue-500 h-2 rounded-full" style={{ width: '43%' }}></div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <div className="mt-6 flex gap-3">
          <button className="flex-1 bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors text-sm">
            ➕ Add Transaction
          </button>
          <button className="flex-1 bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 transition-colors text-sm">
            📈 Reports
          </button>
          <button className="flex-1 bg-purple-600 text-white px-4 py-2 rounded-lg hover:bg-purple-700 transition-colors text-sm">
            ⚙️ Settings
          </button>
        </div>
      </div>
    </div>
  );
}