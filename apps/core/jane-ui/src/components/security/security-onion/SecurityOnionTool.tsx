/**
 * Security Onion Tool Component - Lazy Loaded
 * Security Domain - Constitutional Requirement: <1s response time
 */

import { useEffect } from 'react';
import { usePerformanceMonitor } from '../../../services/performance/performanceMonitor';

export default function SecurityOnionTool() {
  const { measureOperation } = usePerformanceMonitor();

  useEffect(() => {
    measureOperation('security-onion-tool-init', async () => {
      console.log('🧅 Security Onion tool initialized');
    }, 'security');
  }, [measureOperation]);

  return (
    <div className="max-w-6xl mx-auto p-6">
      <div className="mb-8">
        <div className="flex items-center gap-3 mb-2">
          <div className="flex items-center justify-center w-12 h-12 bg-green-100 rounded-lg">
            <span className="text-2xl">🧅</span>
          </div>
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Security Onion</h1>
            <p className="text-gray-600">Network security monitoring platform</p>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-4 mb-8">
        <div className="bg-white p-4 rounded-lg border border-gray-200">
          <h3 className="font-semibold text-gray-900 mb-2">📊 Events</h3>
          <div className="text-2xl font-bold text-red-600">2,847</div>
          <p className="text-sm text-gray-500">Last 24h</p>
        </div>
        
        <div className="bg-white p-4 rounded-lg border border-gray-200">
          <h3 className="font-semibold text-gray-900 mb-2">🔍 Alerts</h3>
          <div className="text-2xl font-bold text-orange-600">143</div>
          <p className="text-sm text-gray-500">Active alerts</p>
        </div>
        
        <div className="bg-white p-4 rounded-lg border border-gray-200">
          <h3 className="font-semibold text-gray-900 mb-2">🌐 Sensors</h3>
          <div className="text-2xl font-bold text-green-600">8/8</div>
          <p className="text-sm text-gray-500">Online</p>
        </div>
        
        <div className="bg-white p-4 rounded-lg border border-gray-200">
          <h3 className="font-semibold text-gray-900 mb-2">💾 Storage</h3>
          <div className="text-2xl font-bold text-blue-600">73%</div>
          <p className="text-sm text-gray-500">Used</p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white rounded-lg border border-gray-200 p-6">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Alert Summary</h2>
          <div className="space-y-3">
            <div className="flex items-center justify-between p-3 bg-red-50 rounded-lg">
              <div>
                <p className="font-medium text-red-800">High Priority</p>
                <p className="text-sm text-red-600">Potential malware communication</p>
              </div>
              <span className="text-xl font-bold text-red-600">12</span>
            </div>
            <div className="flex items-center justify-between p-3 bg-orange-50 rounded-lg">
              <div>
                <p className="font-medium text-orange-800">Medium Priority</p>
                <p className="text-sm text-orange-600">Suspicious network activity</p>
              </div>
              <span className="text-xl font-bold text-orange-600">47</span>
            </div>
            <div className="flex items-center justify-between p-3 bg-yellow-50 rounded-lg">
              <div>
                <p className="font-medium text-yellow-800">Low Priority</p>
                <p className="text-sm text-yellow-600">Policy violations</p>
              </div>
              <span className="text-xl font-bold text-yellow-600">84</span>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg border border-gray-200 p-6">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Network Overview</h2>
          <div className="space-y-4">
            <div className="flex justify-between items-center">
              <span className="text-gray-600">Bandwidth Usage</span>
              <span className="font-bold text-blue-600">847 Mbps</span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-2">
              <div className="bg-blue-500 h-2 rounded-full" style={{width: '68%'}}></div>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-gray-600">Active Flows</span>
              <span className="font-bold text-green-600">23,847</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-gray-600">Unique IPs</span>
              <span className="font-bold text-purple-600">1,429</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}