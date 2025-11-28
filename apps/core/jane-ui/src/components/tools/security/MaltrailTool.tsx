'use client';

import React, { useEffect, useState } from 'react';
import { usePerformanceMonitor } from '../../../services/performance/performanceMonitor';
import { ToolComponentProps } from '../../../services/toolLoader';

export function MaltrailTool({ onClose, onError, toolId = 'maltrail', ...props }: ToolComponentProps) {
  const { measureOperation } = usePerformanceMonitor();
  const [isInitialized, setIsInitialized] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const initializeTool = async () => {
      try {
        await measureOperation(
          'maltrail-tool-init',
          async () => {
            await new Promise(resolve => setTimeout(resolve, 800));
            setIsInitialized(true);
          },
          'security'
        );
      } catch (err) {
        const errorMsg = err instanceof Error ? err.message : 'Failed to initialize Maltrail';
        setError(errorMsg);
        onError?.(new Error(errorMsg));
      }
    };

    initializeTool();
  }, [measureOperation, onError]);

  if (error) {
    return (
      <div className="maltrail-tool-error p-6 bg-red-50 border border-red-200 rounded-lg">
        <h3 className="text-lg font-semibold text-red-800 mb-2">❌ Maltrail Tool Error</h3>
        <p className="text-red-700">{error}</p>
        <button onClick={onClose} className="mt-4 px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700">
          Close Tool
        </button>
      </div>
    );
  }

  if (!isInitialized) {
    return (
      <div className="maltrail-tool-loading flex items-center justify-center p-8 bg-red-50 rounded-lg">
        <div className="text-center">
          <div className="animate-spin h-8 w-8 border-2 border-red-500 border-t-transparent rounded-full mx-auto mb-4"></div>
          <p className="text-sm text-red-600">Initializing Maltrail...</p>
          <p className="text-xs text-red-400 mt-1">Malicious traffic detection system</p>
        </div>
      </div>
    );
  }

  return (
    <div className="maltrail-tool bg-white border border-gray-200 rounded-lg shadow-sm" {...props}>
      <div className="maltrail-tool-header flex items-center justify-between p-4 border-b border-gray-200">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 bg-red-100 rounded-lg flex items-center justify-center">
            <span className="text-red-600 font-bold">🔥</span>
          </div>
          <div>
            <h2 className="text-lg font-semibold text-gray-900">Maltrail</h2>
            <p className="text-sm text-gray-500">Malicious Traffic Detection</p>
          </div>
        </div>
        {onClose && (
          <button onClick={onClose} className="text-gray-400 hover:text-gray-600 transition-colors">
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        )}
      </div>

      <div className="maltrail-tool-content p-6">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div className="space-y-4">
            <div className="bg-red-50 border border-red-200 rounded-lg p-4">
              <h3 className="text-sm font-semibold text-red-800 mb-3">🚨 Threat Detection</h3>
              <div className="space-y-3">
                <div className="flex items-center justify-between text-xs">
                  <span>Malicious IPs</span>
                  <span className="font-bold text-red-700">23 blocked</span>
                </div>
                <div className="flex items-center justify-between text-xs">
                  <span>Suspicious Domains</span>
                  <span className="font-bold text-orange-700">8 detected</span>
                </div>
                <div className="flex items-center justify-between text-xs">
                  <span>Malware Signatures</span>
                  <span className="font-bold text-yellow-700">3 matches</span>
                </div>
                <div className="flex items-center justify-between text-xs">
                  <span>C2 Communications</span>
                  <span className="font-bold text-purple-700">1 active</span>
                </div>
              </div>
            </div>
            
            <div className="bg-orange-50 border border-orange-200 rounded-lg p-4">
              <h3 className="text-sm font-semibold text-orange-800 mb-3">🔍 Recent Detections</h3>
              <div className="space-y-2 text-xs">
                <div className="bg-white rounded p-2 border border-red-200">
                  <div className="flex items-center justify-between mb-1">
                    <span className="font-semibold text-red-700">Malicious IP</span>
                    <span className="text-gray-500">2 min ago</span>
                  </div>
                  <div className="text-gray-700">192.168.100.50 → 185.220.101.182</div>
                  <div className="text-red-600">Known botnet C2 server</div>
                </div>
                
                <div className="bg-white rounded p-2 border border-orange-200">
                  <div className="flex items-center justify-between mb-1">
                    <span className="font-semibold text-orange-700">Suspicious Domain</span>
                    <span className="text-gray-500">5 min ago</span>
                  </div>
                  <div className="text-gray-700">evil-domain.tk</div>
                  <div className="text-orange-600">DGA-generated domain</div>
                </div>
                
                <div className="bg-white rounded p-2 border border-yellow-200">
                  <div className="flex items-center justify-between mb-1">
                    <span className="font-semibold text-yellow-700">Port Scan</span>
                    <span className="text-gray-500">8 min ago</span>
                  </div>
                  <div className="text-gray-700">10.0.1.100 scanning 22,80,443,8080</div>
                  <div className="text-yellow-600">Reconnaissance activity</div>
                </div>
              </div>
            </div>
          </div>
          
          <div className="space-y-4">
            <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
              <h3 className="text-sm font-semibold text-blue-800 mb-3">📈 Traffic Analysis</h3>
              <div className="space-y-3">
                <div className="bg-white rounded p-3">
                  <div className="text-xs text-gray-600 mb-1">Total Traffic (Last Hour)</div>
                  <div className="text-lg font-bold text-blue-700">2.3 GB</div>
                  <div className="w-full bg-gray-200 rounded-full h-2 mt-2">
                    <div className="bg-blue-500 h-2 rounded-full" style={{ width: '78%' }}></div>
                  </div>
                </div>
                
                <div className="grid grid-cols-2 gap-2 text-xs">
                  <div className="bg-white rounded p-2 text-center">
                    <div className="font-bold text-green-600">Clean</div>
                    <div className="text-gray-600">89.2%</div>
                  </div>
                  <div className="bg-white rounded p-2 text-center">
                    <div className="font-bold text-red-600">Malicious</div>
                    <div className="text-gray-600">10.8%</div>
                  </div>
                </div>
              </div>
            </div>
            
            <div className="bg-gray-50 border border-gray-200 rounded-lg p-4">
              <h3 className="text-sm font-semibold text-gray-800 mb-3">⚙️ System Status</h3>
              <div className="space-y-2 text-xs">
                <div className="flex items-center justify-between">
                  <span>Sensor Status</span>
                  <div className="flex items-center gap-1">
                    <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                    <span className="font-bold text-green-700">Active</span>
                  </div>
                </div>
                <div className="flex items-center justify-between">
                  <span>Rules Updated</span>
                  <span className="font-bold text-gray-700">2 hours ago</span>
                </div>
                <div className="flex items-center justify-between">
                  <span>Database Size</span>
                  <span className="font-bold text-gray-700">145 MB</span>
                </div>
                <div className="flex items-center justify-between">
                  <span>Active Trails</span>
                  <span className="font-bold text-blue-700">1,247</span>
                </div>
              </div>
            </div>
            
            <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
              <h3 className="text-sm font-semibold text-yellow-800 mb-2">📊 Top Threats</h3>
              <div className="space-y-1 text-xs">
                <div className="flex justify-between">
                  <span>Emotet Botnet</span>
                  <span className="font-bold text-red-600">15 hits</span>
                </div>
                <div className="flex justify-between">
                  <span>TrickBot C2</span>
                  <span className="font-bold text-red-600">8 hits</span>
                </div>
                <div className="flex justify-between">
                  <span>Suspicious DNS</span>
                  <span className="font-bold text-orange-600">6 hits</span>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <div className="mt-6 flex gap-3">
          <button className="flex-1 bg-red-600 text-white px-4 py-2 rounded-lg hover:bg-red-700 transition-colors text-sm">
            🔥 View Alerts
          </button>
          <button className="flex-1 bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors text-sm">
            📈 Analytics
          </button>
          <button className="flex-1 bg-gray-600 text-white px-4 py-2 rounded-lg hover:bg-gray-700 transition-colors text-sm">
            ⚙️ Settings
          </button>
        </div>
      </div>
    </div>
  );
}