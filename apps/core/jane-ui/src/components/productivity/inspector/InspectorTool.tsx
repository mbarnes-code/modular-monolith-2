/**
 * Inspector Tool Component - Lazy Loaded
 * Productivity Domain - Constitutional Requirement: <2s response time
 */

import { useEffect } from 'react';
import { usePerformanceMonitor } from '../../../services/performance/performanceMonitor';

export default function InspectorTool() {
  const { measureOperation } = usePerformanceMonitor();

  useEffect(() => {
    measureOperation('inspector-tool-init', async () => {
      console.log('🔍 Inspector tool initialized');
    }, 'productivity');
  }, [measureOperation]);

  return (
    <div className="max-w-6xl mx-auto p-6">
      <div className="mb-8">
        <div className="flex items-center gap-3 mb-2">
          <div className="flex items-center justify-center w-12 h-12 bg-blue-100 rounded-lg">
            <span className="text-2xl">🔍</span>
          </div>
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Inspector</h1>
            <p className="text-gray-600">System monitoring and inspection platform</p>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-4 mb-8">
        <div className="bg-white p-4 rounded-lg border border-gray-200">
          <h3 className="font-semibold text-gray-900 mb-2">📊 CPU Usage</h3>
          <div className="text-2xl font-bold text-blue-600">23%</div>
          <p className="text-sm text-gray-500">Average load</p>
        </div>
        
        <div className="bg-white p-4 rounded-lg border border-gray-200">
          <h3 className="font-semibold text-gray-900 mb-2">🧠 Memory</h3>
          <div className="text-2xl font-bold text-green-600">4.2GB</div>
          <p className="text-sm text-gray-500">Of 16GB used</p>
        </div>
        
        <div className="bg-white p-4 rounded-lg border border-gray-200">
          <h3 className="font-semibold text-gray-900 mb-2">💾 Disk Space</h3>
          <div className="text-2xl font-bold text-yellow-600">128GB</div>
          <p className="text-sm text-gray-500">Available</p>
        </div>
        
        <div className="bg-white p-4 rounded-lg border border-gray-200">
          <h3 className="font-semibold text-gray-900 mb-2">🌐 Network</h3>
          <div className="text-2xl font-bold text-purple-600">45Mbps</div>
          <p className="text-sm text-gray-500">Current throughput</p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white rounded-lg border border-gray-200 p-6">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Active Processes</h2>
          <div className="space-y-3">
            <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
              <div className="flex items-center gap-3">
                <span className="text-xl">💻</span>
                <div>
                  <p className="font-medium">node</p>
                  <p className="text-sm text-gray-500">PID: 1234</p>
                </div>
              </div>
              <div className="text-right">
                <p className="font-medium">12.3%</p>
                <p className="text-sm text-gray-500">CPU</p>
              </div>
            </div>
            <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
              <div className="flex items-center gap-3">
                <span className="text-xl">🔍</span>
                <div>
                  <p className="font-medium">chrome</p>
                  <p className="text-sm text-gray-500">PID: 5678</p>
                </div>
              </div>
              <div className="text-right">
                <p className="font-medium">8.7%</p>
                <p className="text-sm text-gray-500">CPU</p>
              </div>
            </div>
            <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
              <div className="flex items-center gap-3">
                <span className="text-xl">🐍</span>
                <div>
                  <p className="font-medium">python</p>
                  <p className="text-sm text-gray-500">PID: 9012</p>
                </div>
              </div>
              <div className="text-right">
                <p className="font-medium">5.2%</p>
                <p className="text-sm text-gray-500">CPU</p>
              </div>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg border border-gray-200 p-6">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">System Health</h2>
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <span className="text-gray-600">System Load</span>
              <div className="flex items-center gap-2">
                <div className="w-24 bg-gray-200 rounded-full h-2">
                  <div className="bg-green-500 h-2 rounded-full" style={{width: '35%'}}></div>
                </div>
                <span className="text-sm font-medium text-green-600">Normal</span>
              </div>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-gray-600">Memory Usage</span>
              <div className="flex items-center gap-2">
                <div className="w-24 bg-gray-200 rounded-full h-2">
                  <div className="bg-yellow-500 h-2 rounded-full" style={{width: '65%'}}></div>
                </div>
                <span className="text-sm font-medium text-yellow-600">Moderate</span>
              </div>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-gray-600">Disk I/O</span>
              <div className="flex items-center gap-2">
                <div className="w-24 bg-gray-200 rounded-full h-2">
                  <div className="bg-green-500 h-2 rounded-full" style={{width: '25%'}}></div>
                </div>
                <span className="text-sm font-medium text-green-600">Low</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}