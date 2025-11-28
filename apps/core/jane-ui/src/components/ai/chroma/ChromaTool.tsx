/**
 * Chroma DB Tool Component - Lazy Loaded
 * AI Domain - Constitutional Requirement: <2s response time
 */

import { useEffect } from 'react';
import { usePerformanceMonitor } from '../../../services/performance/performanceMonitor';

export default function ChromaTool() {
  const { measureOperation } = usePerformanceMonitor();

  useEffect(() => {
    measureOperation('chroma-tool-init', async () => {
      console.log('🧠 Chroma DB tool initialized');
    }, 'ai');
  }, [measureOperation]);

  return (
    <div className="max-w-6xl mx-auto p-6">
      <div className="mb-8">
        <div className="flex items-center gap-3 mb-2">
          <div className="flex items-center justify-center w-12 h-12 bg-gradient-to-r from-purple-100 to-pink-100 rounded-lg">
            <span className="text-2xl">🧠</span>
          </div>
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Chroma DB</h1>
            <p className="text-gray-600">Vector database for AI workflows and semantic search</p>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-4 mb-8">
        <div className="bg-white p-4 rounded-lg border border-gray-200">
          <h3 className="font-semibold text-gray-900 mb-2">📀 Collections</h3>
          <div className="text-2xl font-bold text-purple-600">12</div>
          <p className="text-sm text-gray-500">Vector collections</p>
        </div>
        
        <div className="bg-white p-4 rounded-lg border border-gray-200">
          <h3 className="font-semibold text-gray-900 mb-2">📊 Vectors</h3>
          <div className="text-2xl font-bold text-blue-600">847K</div>
          <p className="text-sm text-gray-500">Stored embeddings</p>
        </div>
        
        <div className="bg-white p-4 rounded-lg border border-gray-200">
          <h3 className="font-semibold text-gray-900 mb-2">🔍 Queries</h3>
          <div className="text-2xl font-bold text-green-600">2,341</div>
          <p className="text-sm text-gray-500">This month</p>
        </div>
        
        <div className="bg-white p-4 rounded-lg border border-gray-200">
          <h3 className="font-semibold text-gray-900 mb-2">🚀 Performance</h3>
          <div className="text-2xl font-bold text-orange-600">0.23s</div>
          <p className="text-sm text-gray-500">Avg query time</p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white rounded-lg border border-gray-200 p-6">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Collections</h2>
          <div className="space-y-3">
            <div className="flex items-center justify-between p-3 bg-gradient-to-r from-purple-50 to-pink-50 rounded-lg">
              <div className="flex items-center gap-3">
                <span className="text-xl">📝</span>
                <div>
                  <p className="font-medium">Documents</p>
                  <p className="text-sm text-gray-500">125,432 embeddings</p>
                </div>
              </div>
              <div className="text-right">
                <p className="font-medium text-purple-600">Active</p>
                <p className="text-sm text-gray-500">1536d</p>
              </div>
            </div>
            <div className="flex items-center justify-between p-3 bg-gradient-to-r from-blue-50 to-cyan-50 rounded-lg">
              <div className="flex items-center gap-3">
                <span className="text-xl">🗨️</span>
                <div>
                  <p className="font-medium">Conversations</p>
                  <p className="text-sm text-gray-500">43,291 embeddings</p>
                </div>
              </div>
              <div className="text-right">
                <p className="font-medium text-blue-600">Active</p>
                <p className="text-sm text-gray-500">384d</p>
              </div>
            </div>
            <div className="flex items-center justify-between p-3 bg-gradient-to-r from-green-50 to-emerald-50 rounded-lg">
              <div className="flex items-center gap-3">
                <span className="text-xl">📊</span>
                <div>
                  <p className="font-medium">Analytics</p>
                  <p className="text-sm text-gray-500">78,923 embeddings</p>
                </div>
              </div>
              <div className="text-right">
                <p className="font-medium text-green-600">Active</p>
                <p className="text-sm text-gray-500">768d</p>
              </div>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg border border-gray-200 p-6">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Semantic Search</h2>
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Query</label>
              <input 
                type="text" 
                placeholder="Enter semantic search query..."
                className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:ring-2 focus:ring-purple-500 focus:border-transparent"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Collection</label>
              <select className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm">
                <option>Documents</option>
                <option>Conversations</option>
                <option>Analytics</option>
              </select>
            </div>
            <div className="flex items-center justify-between">
              <label className="text-sm font-medium text-gray-700">Results</label>
              <select className="border border-gray-300 rounded px-2 py-1 text-sm">
                <option>10</option>
                <option>25</option>
                <option>50</option>
              </select>
            </div>
            <button className="w-full bg-gradient-to-r from-purple-600 to-pink-600 text-white py-2 px-4 rounded-lg hover:from-purple-700 hover:to-pink-700 transition-colors">
              🔍 Search Vectors
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}