/**
 * vLLM Tool Component - Lazy Loaded
 * AI Domain - Constitutional Requirement: <2s response time
 */

import { useEffect } from 'react';
import { usePerformanceMonitor } from '../../../services/performance/performanceMonitor';

export default function VllmTool() {
  const { measureOperation } = usePerformanceMonitor();

  useEffect(() => {
    measureOperation('vllm-tool-init', async () => {
      console.log('🚀 vLLM tool initialized');
    }, 'ai');
  }, [measureOperation]);

  return (
    <div className="max-w-6xl mx-auto p-6">
      <div className="mb-8">
        <div className="flex items-center gap-3 mb-2">
          <div className="flex items-center justify-center w-12 h-12 bg-gradient-to-r from-blue-100 to-purple-100 rounded-lg">
            <span className="text-2xl">🚀</span>
          </div>
          <div>
            <h1 className="text-3xl font-bold text-gray-900">vLLM</h1>
            <p className="text-gray-600">High-throughput and memory-efficient LLM serving</p>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-4 mb-8">
        <div className="bg-white p-4 rounded-lg border border-gray-200">
          <h3 className="font-semibold text-gray-900 mb-2">🤖 Models</h3>
          <div className="text-2xl font-bold text-blue-600">7</div>
          <p className="text-sm text-gray-500">Loaded</p>
        </div>
        
        <div className="bg-white p-4 rounded-lg border border-gray-200">
          <h3 className="font-semibold text-gray-900 mb-2">📊 Requests</h3>
          <div className="text-2xl font-bold text-green-600">14.2K</div>
          <p className="text-sm text-gray-500">Today</p>
        </div>
        
        <div className="bg-white p-4 rounded-lg border border-gray-200">
          <h3 className="font-semibold text-gray-900 mb-2">⚡ Throughput</h3>
          <div className="text-2xl font-bold text-purple-600">847</div>
          <p className="text-sm text-gray-500">Tokens/sec</p>
        </div>
        
        <div className="bg-white p-4 rounded-lg border border-gray-200">
          <h3 className="font-semibold text-gray-900 mb-2">💾 Memory</h3>
          <div className="text-2xl font-bold text-orange-600">23.4GB</div>
          <p className="text-sm text-gray-500">Used</p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white rounded-lg border border-gray-200 p-6">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Active Models</h2>
          <div className="space-y-3">
            <div className="flex items-center justify-between p-3 bg-gradient-to-r from-blue-50 to-purple-50 rounded-lg">
              <div className="flex items-center gap-3">
                <div className="w-3 h-3 bg-green-500 rounded-full"></div>
                <div>
                  <p className="font-medium">Llama-2-7B-Chat</p>
                  <p className="text-sm text-gray-500">7B parameters • 13.1GB</p>
                </div>
              </div>
              <div className="text-right">
                <p className="font-medium text-green-600">Active</p>
                <p className="text-sm text-gray-500">247 req/min</p>
              </div>
            </div>
            <div className="flex items-center justify-between p-3 bg-gradient-to-r from-green-50 to-emerald-50 rounded-lg">
              <div className="flex items-center gap-3">
                <div className="w-3 h-3 bg-green-500 rounded-full"></div>
                <div>
                  <p className="font-medium">CodeLlama-13B</p>
                  <p className="text-sm text-gray-500">13B parameters • 24.2GB</p>
                </div>
              </div>
              <div className="text-right">
                <p className="font-medium text-green-600">Active</p>
                <p className="text-sm text-gray-500">89 req/min</p>
              </div>
            </div>
            <div className="flex items-center justify-between p-3 bg-gradient-to-r from-yellow-50 to-orange-50 rounded-lg">
              <div className="flex items-center gap-3">
                <div className="w-3 h-3 bg-yellow-500 rounded-full"></div>
                <div>
                  <p className="font-medium">Mistral-7B-Instruct</p>
                  <p className="text-sm text-gray-500">7B parameters • 14.1GB</p>
                </div>
              </div>
              <div className="text-right">
                <p className="font-medium text-yellow-600">Warmup</p>
                <p className="text-sm text-gray-500">0 req/min</p>
              </div>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg border border-gray-200 p-6">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Performance Metrics</h2>
          <div className="space-y-4">
            <div className="flex justify-between items-center">
              <span className="text-gray-600">GPU Utilization</span>
              <span className="font-bold text-blue-600">87%</span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-2">
              <div className="bg-blue-500 h-2 rounded-full" style={{width: '87%'}}></div>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-gray-600">Queue Length</span>
              <span className="font-bold text-green-600">12</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-gray-600">Avg Latency</span>
              <span className="font-bold text-purple-600">234ms</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-gray-600">Cache Hit Rate</span>
              <span className="font-bold text-orange-600">78%</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}