/**
 * Kong Gateway Tool Component - Lazy Loaded
 * Infrastructure Domain - Constitutional Requirement: <5s response time
 */

import { useEffect } from 'react';
import { usePerformanceMonitor } from '../../../services/performance/performanceMonitor';

export default function KongTool() {
  const { measureOperation } = usePerformanceMonitor();

  useEffect(() => {
    measureOperation('kong-tool-init', async () => {
      console.log('🦍 Kong Gateway tool initialized');
    }, 'infrastructure');
  }, [measureOperation]);

  return (
    <div className="max-w-6xl mx-auto p-6">
      <div className="mb-8">
        <div className="flex items-center gap-3 mb-2">
          <div className="flex items-center justify-center w-12 h-12 bg-blue-100 rounded-lg">
            <span className="text-2xl">🦍</span>
          </div>
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Kong Gateway</h1>
            <p className="text-gray-600">API Gateway and Service Mesh platform</p>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-4 mb-8">
        <div className="bg-white p-4 rounded-lg border border-gray-200">
          <h3 className="font-semibold text-gray-900 mb-2">🌐 Services</h3>
          <div className="text-2xl font-bold text-blue-600">23</div>
          <p className="text-sm text-gray-500">Active services</p>
        </div>
        
        <div className="bg-white p-4 rounded-lg border border-gray-200">
          <h3 className="font-semibold text-gray-900 mb-2">🔌 Routes</h3>
          <div className="text-2xl font-bold text-green-600">87</div>
          <p className="text-sm text-gray-500">Configured routes</p>
        </div>
        
        <div className="bg-white p-4 rounded-lg border border-gray-200">
          <h3 className="font-semibold text-gray-900 mb-2">🔌 Plugins</h3>
          <div className="text-2xl font-bold text-purple-600">34</div>
          <p className="text-sm text-gray-500">Active plugins</p>
        </div>
        
        <div className="bg-white p-4 rounded-lg border border-gray-200">
          <h3 className="font-semibold text-gray-900 mb-2">📈 Requests</h3>
          <div className="text-2xl font-bold text-orange-600">2.3M</div>
          <p className="text-sm text-gray-500">Today</p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white rounded-lg border border-gray-200 p-6">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Service Health</h2>
          <div className="space-y-3">
            <div className="flex items-center justify-between p-3 bg-green-50 rounded-lg">
              <div className="flex items-center gap-3">
                <div className="w-3 h-3 bg-green-500 rounded-full"></div>
                <div>
                  <p className="font-medium">API Gateway</p>
                  <p className="text-sm text-gray-500">api.example.com</p>
                </div>
              </div>
              <div className="text-right">
                <p className="font-medium text-green-600">Healthy</p>
                <p className="text-sm text-gray-500">99.9%</p>
              </div>
            </div>
            <div className="flex items-center justify-between p-3 bg-green-50 rounded-lg">
              <div className="flex items-center gap-3">
                <div className="w-3 h-3 bg-green-500 rounded-full"></div>
                <div>
                  <p className="font-medium">User Service</p>
                  <p className="text-sm text-gray-500">users.internal</p>
                </div>
              </div>
              <div className="text-right">
                <p className="font-medium text-green-600">Healthy</p>
                <p className="text-sm text-gray-500">99.7%</p>
              </div>
            </div>
            <div className="flex items-center justify-between p-3 bg-yellow-50 rounded-lg">
              <div className="flex items-center gap-3">
                <div className="w-3 h-3 bg-yellow-500 rounded-full"></div>
                <div>
                  <p className="font-medium">Payment Service</p>
                  <p className="text-sm text-gray-500">payments.internal</p>
                </div>
              </div>
              <div className="text-right">
                <p className="font-medium text-yellow-600">Degraded</p>
                <p className="text-sm text-gray-500">95.2%</p>
              </div>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg border border-gray-200 p-6">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Traffic Analytics</h2>
          <div className="space-y-4">
            <div className="flex justify-between items-center">
              <span className="text-gray-600">Requests per Second</span>
              <span className="font-bold text-blue-600">847 RPS</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-gray-600">Average Latency</span>
              <span className="font-bold text-green-600">23ms</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-gray-600">Error Rate</span>
              <span className="font-bold text-red-600">0.3%</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-gray-600">Active Connections</span>
              <span className="font-bold text-purple-600">1,249</span>
            </div>
            <div className="mt-4">
              <div className="flex items-center justify-between mb-2">
                <span className="text-sm text-gray-600">Rate Limiting</span>
                <span className="text-sm text-orange-600">Active</span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div className="bg-orange-500 h-2 rounded-full" style={{width: '67%'}}></div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}