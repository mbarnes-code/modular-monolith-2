/**
 * n8n Tool Component - Lazy Loaded
 * Productivity Domain - Constitutional Requirement: <2s response time
 */

import { useEffect } from 'react';
import { usePerformanceMonitor } from '../../../services/performance/performanceMonitor';

export default function N8nTool() {
  const { measureOperation } = usePerformanceMonitor();

  useEffect(() => {
    measureOperation('n8n-tool-init', async () => {
      console.log('🔄 n8n tool initialized');
    }, 'productivity');
  }, [measureOperation]);

  return (
    <div className="max-w-6xl mx-auto p-6">
      <div className="mb-8">
        <div className="flex items-center gap-3 mb-2">
          <div className="flex items-center justify-center w-12 h-12 bg-purple-100 rounded-lg">
            <span className="text-2xl">🔄</span>
          </div>
          <div>
            <h1 className="text-3xl font-bold text-gray-900">n8n</h1>
            <p className="text-gray-600">Workflow automation platform for productivity enhancement</p>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-4 mb-8">
        <div className="bg-white p-4 rounded-lg border border-gray-200">
          <h3 className="font-semibold text-gray-900 mb-2">⚙️ Workflows</h3>
          <div className="text-2xl font-bold text-purple-600">12</div>
          <p className="text-sm text-gray-500">Active automations</p>
        </div>
        
        <div className="bg-white p-4 rounded-lg border border-gray-200">
          <h3 className="font-semibold text-gray-900 mb-2">🚀 Executions</h3>
          <div className="text-2xl font-bold text-green-600">1,247</div>
          <p className="text-sm text-gray-500">This month</p>
        </div>
        
        <div className="bg-white p-4 rounded-lg border border-gray-200">
          <h3 className="font-semibild text-gray-900 mb-2">🔌 Integrations</h3>
          <div className="text-2xl font-bold text-blue-600">8</div>
          <p className="text-sm text-gray-500">Connected services</p>
        </div>
        
        <div className="bg-white p-4 rounded-lg border border-gray-200">
          <h3 className="font-semibold text-gray-900 mb-2">🟢 Status</h3>
          <div className="text-lg font-bold text-green-600">Running</div>
          <p className="text-sm text-gray-500">All systems operational</p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white rounded-lg border border-gray-200 p-6">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Recent Workflows</h2>
          <div className="space-y-3">
            <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
              <div className="flex items-center gap-3">
                <span className="text-xl">💬</span>
                <div>
                  <p className="font-medium">Slack Notifications</p>
                  <p className="text-sm text-gray-500">Triggered 5 times today</p>
                </div>
              </div>
              <div className="w-3 h-3 bg-green-500 rounded-full"></div>
            </div>
            <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
              <div className="flex items-center gap-3">
                <span className="text-xl">📧</span>
                <div>
                  <p className="font-medium">Email Processing</p>
                  <p className="text-sm text-gray-500">Last run 2 hours ago</p>
                </div>
              </div>
              <div className="w-3 h-3 bg-green-500 rounded-full"></div>
            </div>
            <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
              <div className="flex items-center gap-3">
                <span className="text-xl">📄</span>
                <div>
                  <p className="font-medium">Data Sync</p>
                  <p className="text-sm text-gray-500">Scheduled for 6 PM</p>
                </div>
              </div>
              <div className="w-3 h-3 bg-yellow-500 rounded-full"></div>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg border border-gray-200 p-6">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Execution Statistics</h2>
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <span className="text-gray-600">Success Rate</span>
              <div className="flex items-center gap-2">
                <div className="w-24 bg-gray-200 rounded-full h-2">
                  <div className="bg-green-500 h-2 rounded-full" style={{width: '94%'}}></div>
                </div>
                <span className="text-sm font-medium">94%</span>
              </div>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-gray-600">Avg. Execution Time</span>
              <span className="font-medium">2.3s</span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-gray-600">Failed Executions</span>
              <span className="font-medium text-red-600">7</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}