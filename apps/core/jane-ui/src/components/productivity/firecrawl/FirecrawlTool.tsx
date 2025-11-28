/**
 * Firecrawl Tool Component - Lazy Loaded
 * Productivity Domain - Constitutional Requirement: <2s response time
 */

import { useEffect } from 'react';
import { usePerformanceMonitor } from '../../../services/performance/performanceMonitor';

export default function FirecrawlTool() {
  const { measureOperation } = usePerformanceMonitor();

  useEffect(() => {
    measureOperation('firecrawl-tool-init', async () => {
      console.log('🔥 Firecrawl tool initialized');
    }, 'productivity');
  }, [measureOperation]);

  return (
    <div className="max-w-6xl mx-auto p-6">
      <div className="mb-8">
        <div className="flex items-center gap-3 mb-2">
          <div className="flex items-center justify-center w-12 h-12 bg-orange-100 rounded-lg">
            <span className="text-2xl">🔥</span>
          </div>
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Firecrawl</h1>
            <p className="text-gray-600">Turn websites into LLM-ready markdown and structured data</p>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-4 mb-8">
        <div className="bg-white p-4 rounded-lg border border-gray-200">
          <h3 className="font-semibold text-gray-900 mb-2">🌐 Pages</h3>
          <div className="text-2xl font-bold text-orange-600">12,847</div>
          <p className="text-sm text-gray-500">Crawled</p>
        </div>
        
        <div className="bg-white p-4 rounded-lg border border-gray-200">
          <h3 className="font-semibold text-gray-900 mb-2">📄 Documents</h3>
          <div className="text-2xl font-bold text-blue-600">8,392</div>
          <p className="text-sm text-gray-500">Processed</p>
        </div>
        
        <div className="bg-white p-4 rounded-lg border border-gray-200">
          <h3 className="font-semibold text-gray-900 mb-2">⚙️ Jobs</h3>
          <div className="text-2xl font-bold text-green-600">23</div>
          <p className="text-sm text-gray-500">Active</p>
        </div>
        
        <div className="bg-white p-4 rounded-lg border border-gray-200">
          <h3 className="font-semibold text-gray-900 mb-2">🚀 Speed</h3>
          <div className="text-2xl font-bold text-purple-600">3.2s</div>
          <p className="text-sm text-gray-500">Avg process</p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white rounded-lg border border-gray-200 p-6">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Recent Crawls</h2>
          <div className="space-y-3">
            <div className="flex items-center justify-between p-3 bg-green-50 rounded-lg">
              <div className="flex items-center gap-3">
                <div className="w-3 h-3 bg-green-500 rounded-full"></div>
                <div>
                  <p className="font-medium">docs.example.com</p>
                  <p className="text-sm text-gray-500">247 pages • 2.3MB</p>
                </div>
              </div>
              <span className="text-sm text-green-600">Complete</span>
            </div>
            <div className="flex items-center justify-between p-3 bg-blue-50 rounded-lg">
              <div className="flex items-center gap-3">
                <div className="w-3 h-3 bg-blue-500 rounded-full animate-pulse"></div>
                <div>
                  <p className="font-medium">blog.startup.io</p>
                  <p className="text-sm text-gray-500">89/150 pages • 1.1MB</p>
                </div>
              </div>
              <span className="text-sm text-blue-600">Running</span>
            </div>
            <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
              <div className="flex items-center gap-3">
                <div className="w-3 h-3 bg-gray-400 rounded-full"></div>
                <div>
                  <p className="font-medium">news.site.com</p>
                  <p className="text-sm text-gray-500">0/500 pages • Queued</p>
                </div>
              </div>
              <span className="text-sm text-gray-600">Pending</span>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg border border-gray-200 p-6">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Output Formats</h2>
          <div className="grid grid-cols-2 gap-3">
            <div className="p-3 bg-gray-50 rounded-lg text-center">
              <div className="text-2xl mb-2">🗂️</div>
              <div className="font-medium">Markdown</div>
              <div className="text-sm text-gray-500">LLM-ready</div>
            </div>
            <div className="p-3 bg-gray-50 rounded-lg text-center">
              <div className="text-2xl mb-2">📊</div>
              <div className="font-medium">JSON</div>
              <div className="text-sm text-gray-500">Structured</div>
            </div>
            <div className="p-3 bg-gray-50 rounded-lg text-center">
              <div className="text-2xl mb-2">📝</div>
              <div className="font-medium">HTML</div>
              <div className="text-sm text-gray-500">Clean</div>
            </div>
            <div className="p-3 bg-gray-50 rounded-lg text-center">
              <div className="text-2xl mb-2">📄</div>
              <div className="font-medium">CSV</div>
              <div className="text-sm text-gray-500">Tabular</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}