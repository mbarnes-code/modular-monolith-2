/**
 * YARA-X Tool Component - Lazy Loaded
 * Security Domain - Constitutional Requirement: <1s response time
 */

import { useEffect } from 'react';
import { usePerformanceMonitor } from '../../../services/performance/performanceMonitor';

export default function YaraXTool() {
  const { measureOperation } = usePerformanceMonitor();

  useEffect(() => {
    measureOperation('yara-x-tool-init', async () => {
      console.log('🔍 YARA-X tool initialized');
    }, 'security');
  }, [measureOperation]);

  return (
    <div className="max-w-6xl mx-auto p-6">
      <div className="mb-8">
        <div className="flex items-center gap-3 mb-2">
          <div className="flex items-center justify-center w-12 h-12 bg-yellow-100 rounded-lg">
            <span className="text-2xl">🔍</span>
          </div>
          <div>
            <h1 className="text-3xl font-bold text-gray-900">YARA-X</h1>
            <p className="text-gray-600">Next-generation malware identification and classification</p>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-4 mb-8">
        <div className="bg-white p-4 rounded-lg border border-gray-200">
          <h3 className="font-semibold text-gray-900 mb-2">📄 Rules</h3>
          <div className="text-2xl font-bold text-yellow-600">3,247</div>
          <p className="text-sm text-gray-500">Active rules</p>
        </div>
        
        <div className="bg-white p-4 rounded-lg border border-gray-200">
          <h3 className="font-semibold text-gray-900 mb-2">🔍 Scans</h3>
          <div className="text-2xl font-bold text-blue-600">18,392</div>
          <p className="text-sm text-gray-500">This month</p>
        </div>
        
        <div className="bg-white p-4 rounded-lg border border-gray-200">
          <h3 className="font-semibold text-gray-900 mb-2">⚠️ Matches</h3>
          <div className="text-2xl font-bold text-red-600">247</div>
          <p className="text-sm text-gray-500">Detections</p>
        </div>
        
        <div className="bg-white p-4 rounded-lg border border-gray-200">
          <h3 className="font-semibold text-gray-900 mb-2">⚡ Performance</h3>
          <div className="text-2xl font-bold text-green-600">0.15s</div>
          <p className="text-sm text-gray-500">Avg scan time</p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white rounded-lg border border-gray-200 p-6">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Recent Detections</h2>
          <div className="space-y-3">
            <div className="p-3 bg-red-50 rounded-lg">
              <div className="flex items-center justify-between mb-1">
                <span className="font-medium text-red-800">Trojan.Win32.Agent</span>
                <span className="text-xs bg-red-100 text-red-800 px-2 py-1 rounded">Critical</span>
              </div>
              <p className="text-sm text-gray-600">malicious_file.exe</p>
              <p className="text-xs text-gray-500 mt-1">Rule: trojan_agent_variant_2024</p>
            </div>
            <div className="p-3 bg-orange-50 rounded-lg">
              <div className="flex items-center justify-between mb-1">
                <span className="font-medium text-orange-800">Suspicious Packer</span>
                <span className="text-xs bg-orange-100 text-orange-800 px-2 py-1 rounded">High</span>
              </div>
              <p className="text-sm text-gray-600">packed_binary.dll</p>
              <p className="text-xs text-gray-500 mt-1">Rule: upx_packer_suspicious</p>
            </div>
            <div className="p-3 bg-yellow-50 rounded-lg">
              <div className="flex items-center justify-between mb-1">
                <span className="font-medium text-yellow-800">Crypto Miner</span>
                <span className="text-xs bg-yellow-100 text-yellow-800 px-2 py-1 rounded">Medium</span>
              </div>
              <p className="text-sm text-gray-600">miner.exe</p>
              <p className="text-xs text-gray-500 mt-1">Rule: coinminer_generic</p>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg border border-gray-200 p-6">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Scan Statistics</h2>
          <div className="space-y-4">
            <div className="flex justify-between items-center">
              <span className="text-gray-600">Files Scanned Today</span>
              <span className="font-bold text-blue-600">4,729</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-gray-600">Clean Files</span>
              <span className="font-bold text-green-600">4,482</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-gray-600">Threats Detected</span>
              <span className="font-bold text-red-600">247</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-gray-600">Detection Rate</span>
              <span className="font-bold text-purple-600">5.2%</span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-2 mt-2">
              <div className="bg-red-500 h-2 rounded-full" style={{width: '5.2%'}}></div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}