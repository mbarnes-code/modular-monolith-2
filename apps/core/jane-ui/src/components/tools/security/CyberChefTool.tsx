'use client';

import React, { useEffect, useState } from 'react';
import { usePerformanceMonitor } from '../../../services/performance/performanceMonitor';
import { ToolComponentProps } from '../../../services/toolLoader';

export function CyberChefTool({ onClose, onError, toolId = 'cyberchef', ...props }: ToolComponentProps) {
  const { measureOperation } = usePerformanceMonitor();
  const [isInitialized, setIsInitialized] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const initializeTool = async () => {
      try {
        await measureOperation(
          'cyberchef-tool-init',
          async () => {
            await new Promise(resolve => setTimeout(resolve, 600));
            setIsInitialized(true);
          },
          'security'
        );
      } catch (err) {
        const errorMsg = err instanceof Error ? err.message : 'Failed to initialize CyberChef';
        setError(errorMsg);
        onError?.(new Error(errorMsg));
      }
    };

    initializeTool();
  }, [measureOperation, onError]);

  if (error) {
    return (
      <div className="cyberchef-tool-error p-6 bg-red-50 border border-red-200 rounded-lg">
        <h3 className="text-lg font-semibold text-red-800 mb-2">❌ CyberChef Tool Error</h3>
        <p className="text-red-700">{error}</p>
        <button onClick={onClose} className="mt-4 px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700">
          Close Tool
        </button>
      </div>
    );
  }

  if (!isInitialized) {
    return (
      <div className="cyberchef-tool-loading flex items-center justify-center p-8 bg-orange-50 rounded-lg">
        <div className="text-center">
          <div className="animate-spin h-8 w-8 border-2 border-orange-500 border-t-transparent rounded-full mx-auto mb-4"></div>
          <p className="text-sm text-orange-600">Initializing CyberChef...</p>
          <p className="text-xs text-orange-400 mt-1">Data transformation toolkit</p>
        </div>
      </div>
    );
  }

  return (
    <div className="cyberchef-tool bg-white border border-gray-200 rounded-lg shadow-sm" {...props}>
      <div className="cyberchef-tool-header flex items-center justify-between p-4 border-b border-gray-200">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 bg-orange-100 rounded-lg flex items-center justify-center">
            <span className="text-orange-600 font-bold">🍳</span>
          </div>
          <div>
            <h2 className="text-lg font-semibold text-gray-900">CyberChef</h2>
            <p className="text-sm text-gray-500">Data Transformation Toolkit</p>
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

      <div className="cyberchef-tool-content p-6">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div className="space-y-4">
            <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
              <h3 className="text-sm font-semibold text-blue-800 mb-3">🔧 Recipe Categories</h3>
              <div className="grid grid-cols-2 gap-2 text-xs">
                <div className="bg-white rounded p-2 text-center hover:bg-blue-100 cursor-pointer">
                  <div className="font-semibold">Encoding</div>
                  <div className="text-gray-500">Base64, URL, HTML</div>
                </div>
                <div className="bg-white rounded p-2 text-center hover:bg-blue-100 cursor-pointer">
                  <div className="font-semibold">Crypto</div>
                  <div className="text-gray-500">AES, RSA, Hash</div>
                </div>
                <div className="bg-white rounded p-2 text-center hover:bg-blue-100 cursor-pointer">
                  <div className="font-semibold">Forensics</div>
                  <div className="text-gray-500">Extract, Parse</div>
                </div>
                <div className="bg-white rounded p-2 text-center hover:bg-blue-100 cursor-pointer">
                  <div className="font-semibold">Network</div>
                  <div className="text-gray-500">IP, DNS, PCAP</div>
                </div>
              </div>
            </div>
            
            <div className="bg-gray-50 border border-gray-200 rounded-lg p-4">
              <h3 className="text-sm font-semibold text-gray-800 mb-2">📝 Input Data</h3>
              <textarea 
                className="w-full h-24 p-2 border border-gray-300 rounded text-xs font-mono"
                placeholder="Paste your data here for transformation..."
              />
            </div>
          </div>
          
          <div className="space-y-4">
            <div className="bg-green-50 border border-green-200 rounded-lg p-4">
              <h3 className="text-sm font-semibold text-green-800 mb-2">📊 Active Recipe</h3>
              <div className="space-y-2">
                <div className="flex items-center gap-2 text-xs bg-white rounded p-2">
                  <span className="w-2 h-2 bg-green-500 rounded-full"></span>
                  <span>From Base64</span>
                  <button className="ml-auto text-red-500 hover:text-red-700">×</button>
                </div>
                <div className="flex items-center gap-2 text-xs bg-white rounded p-2">
                  <span className="w-2 h-2 bg-green-500 rounded-full"></span>
                  <span>URL Decode</span>
                  <button className="ml-auto text-red-500 hover:text-red-700">×</button>
                </div>
              </div>
              <button className="mt-2 w-full bg-green-600 text-white px-3 py-1 rounded text-xs hover:bg-green-700">
                ▶ Execute Recipe
              </button>
            </div>
            
            <div className="bg-gray-50 border border-gray-200 rounded-lg p-4">
              <h3 className="text-sm font-semibold text-gray-800 mb-2">📄 Output</h3>
              <div className="bg-white border border-gray-300 rounded p-2 h-24 overflow-auto">
                <div className="text-xs font-mono text-gray-600">Output will appear here...</div>
              </div>
            </div>
          </div>
        </div>
        
        <div className="mt-6 flex gap-3">
          <button className="flex-1 bg-orange-600 text-white px-4 py-2 rounded-lg hover:bg-orange-700 transition-colors text-sm">
            📋 Save Recipe
          </button>
          <button className="flex-1 bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors text-sm">
            🔄 Load Recipe
          </button>
          <button className="flex-1 bg-gray-600 text-white px-4 py-2 rounded-lg hover:bg-gray-700 transition-colors text-sm">
            📥 Export
          </button>
        </div>
      </div>
    </div>
  );
}