/**
 * Actual Budget Tool Component - Lazy Loaded
 * Productivity Domain - Constitutional Requirement: <2s response time
 */

import { useEffect } from 'react';
import { usePerformanceMonitor } from '../../../services/performance/performanceMonitor';

export default function ActualTool() {
  const { measureOperation } = usePerformanceMonitor();

  useEffect(() => {
    measureOperation('actual-tool-init', async () => {
      console.log('💰 Actual Budget tool initialized');
    }, 'productivity');
  }, [measureOperation]);

  return (
    <div className="max-w-6xl mx-auto p-6">
      <div className="mb-8">
        <div className="flex items-center gap-3 mb-2">
          <div className="flex items-center justify-center w-12 h-12 bg-green-100 rounded-lg">
            <span className="text-2xl">💰</span>
          </div>
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Actual Budget</h1>
            <p className="text-gray-600">Personal finance management and budgeting platform</p>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-4 mb-8">
        <div className="bg-white p-4 rounded-lg border border-gray-200">
          <h3 className="font-semibold text-gray-900 mb-2">💳 Accounts</h3>
          <div className="text-2xl font-bold text-blue-600">5</div>
          <p className="text-sm text-gray-500">Active accounts</p>
        </div>
        
        <div className="bg-white p-4 rounded-lg border border-gray-200">
          <h3 className="font-semibold text-gray-900 mb-2">📊 Budget</h3>
          <div className="text-2xl font-bold text-green-600">$3,247</div>
          <p className="text-sm text-gray-500">Remaining this month</p>
        </div>
        
        <div className="bg-white p-4 rounded-lg border border-gray-200">
          <h3 className="font-semibold text-gray-900 mb-2">📋 Transactions</h3>
          <div className="text-2xl font-bold text-orange-600">42</div>
          <p className="text-sm text-gray-500">This month</p>
        </div>
        
        <div className="bg-white p-4 rounded-lg border border-gray-200">
          <h3 className="font-semibold text-gray-900 mb-2">📈 Net Worth</h3>
          <div className="text-2xl font-bold text-purple-600">$45.2K</div>
          <p className="text-sm text-gray-500">Total assets</p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white rounded-lg border border-gray-200 p-6">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Budget Overview</h2>
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <span className="text-gray-600">Housing</span>
              <div className="flex items-center gap-2">
                <div className="w-24 bg-gray-200 rounded-full h-2">
                  <div className="bg-blue-500 h-2 rounded-full" style={{width: '75%'}}></div>
                </div>
                <span className="text-sm font-medium">$1,200</span>
              </div>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-gray-600">Food</span>
              <div className="flex items-center gap-2">
                <div className="w-24 bg-gray-200 rounded-full h-2">
                  <div className="bg-green-500 h-2 rounded-full" style={{width: '60%'}}></div>
                </div>
                <span className="text-sm font-medium">$480</span>
              </div>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-gray-600">Transportation</span>
              <div className="flex items-center gap-2">
                <div className="w-24 bg-gray-200 rounded-full h-2">
                  <div className="bg-yellow-500 h-2 rounded-full" style={{width: '45%'}}></div>
                </div>
                <span className="text-sm font-medium">$320</span>
              </div>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg border border-gray-200 p-6">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Recent Transactions</h2>
          <div className="space-y-3">
            <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
              <div className="flex items-center gap-3">
                <span className="text-xl">🏪</span>
                <div>
                  <p className="font-medium">Grocery Store</p>
                  <p className="text-sm text-gray-500">Food & Dining</p>
                </div>
              </div>
              <span className="font-medium text-red-600">-$127.45</span>
            </div>
            <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
              <div className="flex items-center gap-3">
                <span className="text-xl">⛽</span>
                <div>
                  <p className="font-medium">Gas Station</p>
                  <p className="text-sm text-gray-500">Transportation</p>
                </div>
              </div>
              <span className="font-medium text-red-600">-$52.30</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}