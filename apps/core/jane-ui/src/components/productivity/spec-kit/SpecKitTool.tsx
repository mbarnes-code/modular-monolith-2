/**
 * SpecKit Tool Component - Lazy Loaded
 * Productivity Domain - Constitutional Requirement: <2s response time
 */

import { useEffect } from 'react';
import { usePerformanceMonitor } from '../../../services/performance/performanceMonitor';

export default function SpecKitTool() {
  const { measureOperation } = usePerformanceMonitor();

  useEffect(() => {
    measureOperation('spec-kit-tool-init', async () => {
      console.log('📝 SpecKit tool initialized');
    }, 'productivity');
  }, [measureOperation]);

  return (
    <div className="max-w-6xl mx-auto p-6">
      <div className="mb-8">
        <div className="flex items-center gap-3 mb-2">
          <div className="flex items-center justify-center w-12 h-12 bg-blue-100 rounded-lg">
            <span className="text-2xl">📝</span>
          </div>
          <div>
            <h1 className="text-3xl font-bold text-gray-900">SpecKit</h1>
            <p className="text-gray-600">Specification and documentation toolkit</p>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-4 mb-8">
        <div className="bg-white p-4 rounded-lg border border-gray-200">
          <h3 className="font-semibold text-gray-900 mb-2">📄 Specs</h3>
          <div className="text-2xl font-bold text-blue-600">47</div>
          <p className="text-sm text-gray-500">Documents</p>
        </div>
        
        <div className="bg-white p-4 rounded-lg border border-gray-200">
          <h3 className="font-semibold text-gray-900 mb-2">📈 Templates</h3>
          <div className="text-2xl font-bold text-green-600">23</div>
          <p className="text-sm text-gray-500">Available</p>
        </div>
        
        <div className="bg-white p-4 rounded-lg border border-gray-200">
          <h3 className="font-semibold text-gray-900 mb-2">⚙️ Workflows</h3>
          <div className="text-2xl font-bold text-purple-600">12</div>
          <p className="text-sm text-gray-500">Automated</p>
        </div>
        
        <div className="bg-white p-4 rounded-lg border border-gray-200">
          <h3 className="font-semibold text-gray-900 mb-2">👥 Teams</h3>
          <div className="text-2xl font-bold text-orange-600">8</div>
          <p className="text-sm text-gray-500">Collaborating</p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white rounded-lg border border-gray-200 p-6">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Recent Documents</h2>
          <div className="space-y-3">
            <div className="flex items-center justify-between p-3 bg-blue-50 rounded-lg">
              <div className="flex items-center gap-3">
                <span className="text-xl">📝</span>
                <div>
                  <p className="font-medium">API Specification v2.1</p>
                  <p className="text-sm text-gray-500">Updated 2 hours ago</p>
                </div>
              </div>
              <button className="text-blue-600 hover:text-blue-700">
                <span className="text-sm">Edit</span>
              </button>
            </div>
            <div className="flex items-center justify-between p-3 bg-green-50 rounded-lg">
              <div className="flex items-center gap-3">
                <span className="text-xl">📊</span>
                <div>
                  <p className="font-medium">Requirements Document</p>
                  <p className="text-sm text-gray-500">Updated 4 hours ago</p>
                </div>
              </div>
              <button className="text-green-600 hover:text-green-700">
                <span className="text-sm">View</span>
              </button>
            </div>
            <div className="flex items-center justify-between p-3 bg-purple-50 rounded-lg">
              <div className="flex items-center gap-3">
                <span className="text-xl">🎨</span>
                <div>
                  <p className="font-medium">Design System Spec</p>
                  <p className="text-sm text-gray-500">Updated yesterday</p>
                </div>
              </div>
              <button className="text-purple-600 hover:text-purple-700">
                <span className="text-sm">Review</span>
              </button>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg border border-gray-200 p-6">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Templates</h2>
          <div className="grid grid-cols-2 gap-3">
            <button className="p-3 bg-blue-50 border border-blue-200 rounded-lg hover:bg-blue-100 text-left">
              <div className="text-blue-600 font-medium mb-1">📝 API Spec</div>
              <div className="text-xs text-gray-600">OpenAPI template</div>
            </button>
            <button className="p-3 bg-green-50 border border-green-200 rounded-lg hover:bg-green-100 text-left">
              <div className="text-green-600 font-medium mb-1">📊 Requirements</div>
              <div className="text-xs text-gray-600">Business reqs</div>
            </button>
            <button className="p-3 bg-purple-50 border border-purple-200 rounded-lg hover:bg-purple-100 text-left">
              <div className="text-purple-600 font-medium mb-1">🎨 Design Doc</div>
              <div className="text-xs text-gray-600">System design</div>
            </button>
            <button className="p-3 bg-orange-50 border border-orange-200 rounded-lg hover:bg-orange-100 text-left">
              <div className="text-orange-600 font-medium mb-1">🔬 Test Plan</div>
              <div className="text-xs text-gray-600">QA template</div>
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}