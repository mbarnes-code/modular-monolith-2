/**
 * IT Tools Component - Lazy Loaded
 * Productivity Domain - Constitutional Requirement: <2s response time
 */

import { useEffect } from 'react';
import { usePerformanceMonitor } from '../../../services/performance/performanceMonitor';

export default function ItToolsTool() {
  const { measureOperation } = usePerformanceMonitor();

  useEffect(() => {
    measureOperation('it-tools-tool-init', async () => {
      console.log('🔧 IT Tools initialized');
    }, 'productivity');
  }, [measureOperation]);

  return (
    <div className="max-w-6xl mx-auto p-6">
      <div className="mb-8">
        <div className="flex items-center gap-3 mb-2">
          <div className="flex items-center justify-center w-12 h-12 bg-gray-100 rounded-lg">
            <span className="text-2xl">🔧</span>
          </div>
          <div>
            <h1 className="text-3xl font-bold text-gray-900">IT Tools</h1>
            <p className="text-gray-600">Collection of handy online tools for developers</p>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4 mb-8">
        <div className="bg-white p-4 rounded-lg border border-gray-200 hover:shadow-md transition-shadow cursor-pointer">
          <div className="text-2xl mb-2">🔐</div>
          <h3 className="font-semibold text-gray-900 mb-1">Encoders/Decoders</h3>
          <p className="text-sm text-gray-600">Base64, URL, HTML encoding</p>
        </div>
        
        <div className="bg-white p-4 rounded-lg border border-gray-200 hover:shadow-md transition-shadow cursor-pointer">
          <div className="text-2xl mb-2">🔒</div>
          <h3 className="font-semibold text-gray-900 mb-1">Hash Functions</h3>
          <p className="text-sm text-gray-600">MD5, SHA, HMAC generators</p>
        </div>
        
        <div className="bg-white p-4 rounded-lg border border-gray-200 hover:shadow-md transition-shadow cursor-pointer">
          <div className="text-2xl mb-2">🎨</div>
          <h3 className="font-semibold text-gray-900 mb-1">Color Tools</h3>
          <p className="text-sm text-gray-600">Palettes, converters, pickers</p>
        </div>
        
        <div className="bg-white p-4 rounded-lg border border-gray-200 hover:shadow-md transition-shadow cursor-pointer">
          <div className="text-2xl mb-2">🗺️</div>
          <h3 className="font-semibold text-gray-900 mb-1">Text Tools</h3>
          <p className="text-sm text-gray-600">Diff, case converters, lorem</p>
        </div>
        
        <div className="bg-white p-4 rounded-lg border border-gray-200 hover:shadow-md transition-shadow cursor-pointer">
          <div className="text-2xl mb-2">📊</div>
          <h3 className="font-semibold text-gray-900 mb-1">Math Tools</h3>
          <p className="text-sm text-gray-600">Calculators, converters</p>
        </div>
        
        <div className="bg-white p-4 rounded-lg border border-gray-200 hover:shadow-md transition-shadow cursor-pointer">
          <div className="text-2xl mb-2">🌐</div>
          <h3 className="font-semibold text-gray-900 mb-1">Network Tools</h3>
          <p className="text-sm text-gray-600">IP tools, DNS lookup</p>
        </div>
        
        <div className="bg-white p-4 rounded-lg border border-gray-200 hover:shadow-md transition-shadow cursor-pointer">
          <div className="text-2xl mb-2">🗺️</div>
          <h3 className="font-semibold text-gray-900 mb-1">Date Tools</h3>
          <p className="text-sm text-gray-600">Formatters, converters</p>
        </div>
        
        <div className="bg-white p-4 rounded-lg border border-gray-200 hover:shadow-md transition-shadow cursor-pointer">
          <div className="text-2xl mb-2">📁</div>
          <h3 className="font-semibold text-gray-900 mb-1">File Tools</h3>
          <p className="text-sm text-gray-600">Validators, formatters</p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white rounded-lg border border-gray-200 p-6">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Popular Tools</h2>
          <div className="space-y-3">
            <div className="flex items-center justify-between p-3 bg-blue-50 rounded-lg">
              <div className="flex items-center gap-3">
                <span className="text-xl">🔐</span>
                <div>
                  <p className="font-medium">Base64 Encoder</p>
                  <p className="text-sm text-gray-500">Encode/decode base64 strings</p>
                </div>
              </div>
              <span className="text-sm text-gray-400">2.1K uses</span>
            </div>
            <div className="flex items-center justify-between p-3 bg-green-50 rounded-lg">
              <div className="flex items-center gap-3">
                <span className="text-xl">🔒</span>
                <div>
                  <p className="font-medium">Hash Generator</p>
                  <p className="text-sm text-gray-500">Generate MD5, SHA hashes</p>
                </div>
              </div>
              <span className="text-sm text-gray-400">1.8K uses</span>
            </div>
            <div className="flex items-center justify-between p-3 bg-purple-50 rounded-lg">
              <div className="flex items-center gap-3">
                <span className="text-xl">🎨</span>
                <div>
                  <p className="font-medium">Color Picker</p>
                  <p className="text-sm text-gray-500">Pick and convert colors</p>
                </div>
              </div>
              <span className="text-sm text-gray-400">1.4K uses</span>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg border border-gray-200 p-6">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Quick Access</h2>
          <div className="grid grid-cols-2 gap-3">
            <button className="p-3 bg-gray-50 border border-gray-200 rounded-lg hover:bg-gray-100 text-left">
              <div className="text-lg mb-1">🔐</div>
              <div className="font-medium text-sm">URL Encode</div>
            </button>
            <button className="p-3 bg-gray-50 border border-gray-200 rounded-lg hover:bg-gray-100 text-left">
              <div className="text-lg mb-1">🔍</div>
              <div className="font-medium text-sm">JWT Decode</div>
            </button>
            <button className="p-3 bg-gray-50 border border-gray-200 rounded-lg hover:bg-gray-100 text-left">
              <div className="text-lg mb-1">📊</div>
              <div className="font-medium text-sm">JSON Format</div>
            </button>
            <button className="p-3 bg-gray-50 border border-gray-200 rounded-lg hover:bg-gray-100 text-left">
              <div className="text-lg mb-1">✨</div>
              <div className="font-medium text-sm">UUID Gen</div>
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}