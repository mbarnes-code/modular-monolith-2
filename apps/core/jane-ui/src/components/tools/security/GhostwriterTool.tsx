'use client';

import React, { useEffect, useState } from 'react';
import { usePerformanceMonitor } from '../../../services/performance/performanceMonitor';
import { ToolComponentProps } from '../../../services/toolLoader';

export function GhostwriterTool({ onClose, onError, toolId = 'ghostwriter', ...props }: ToolComponentProps) {
  const { measureOperation } = usePerformanceMonitor();
  const [isInitialized, setIsInitialized] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const initializeTool = async () => {
      try {
        await measureOperation(
          'ghostwriter-tool-init',
          async () => {
            await new Promise(resolve => setTimeout(resolve, 700));
            setIsInitialized(true);
          },
          'security'
        );
      } catch (err) {
        const errorMsg = err instanceof Error ? err.message : 'Failed to initialize Ghostwriter';
        setError(errorMsg);
        onError?.(new Error(errorMsg));
      }
    };

    initializeTool();
  }, [measureOperation, onError]);

  if (error) {
    return (
      <div className="ghostwriter-tool-error p-6 bg-red-50 border border-red-200 rounded-lg">
        <h3 className="text-lg font-semibold text-red-800 mb-2">❌ Ghostwriter Tool Error</h3>
        <p className="text-red-700">{error}</p>
        <button onClick={onClose} className="mt-4 px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700">
          Close Tool
        </button>
      </div>
    );
  }

  if (!isInitialized) {
    return (
      <div className="ghostwriter-tool-loading flex items-center justify-center p-8 bg-indigo-50 rounded-lg">
        <div className="text-center">
          <div className="animate-spin h-8 w-8 border-2 border-indigo-500 border-t-transparent rounded-full mx-auto mb-4"></div>
          <p className="text-sm text-indigo-600">Initializing Ghostwriter...</p>
          <p className="text-xs text-indigo-400 mt-1">Collaborative report writing platform</p>
        </div>
      </div>
    );
  }

  return (
    <div className="ghostwriter-tool bg-white border border-gray-200 rounded-lg shadow-sm" {...props}>
      <div className="ghostwriter-tool-header flex items-center justify-between p-4 border-b border-gray-200">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 bg-indigo-100 rounded-lg flex items-center justify-center">
            <span className="text-indigo-600 font-bold">📝</span>
          </div>
          <div>
            <h2 className="text-lg font-semibold text-gray-900">Ghostwriter</h2>
            <p className="text-sm text-gray-500">Collaborative Report Writing</p>
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

      <div className="ghostwriter-tool-content p-6">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="lg:col-span-2 space-y-4">
            <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
              <h3 className="text-sm font-semibold text-blue-800 mb-3">📄 Active Projects</h3>
              <div className="space-y-2">
                <div className="bg-white rounded-lg p-3 border border-blue-100">
                  <div className="flex items-center justify-between mb-2">
                    <h4 className="text-sm font-semibold text-gray-800">Red Team Assessment - ACME Corp</h4>
                    <span className="text-xs px-2 py-1 bg-yellow-100 text-yellow-800 rounded">In Progress</span>
                  </div>
                  <div className="text-xs text-gray-600 mb-2">Last updated: 2 hours ago</div>
                  <div className="flex items-center gap-2 text-xs">
                    <span className="text-blue-600">👥 3 collaborators</span>
                    <span className="text-gray-400">•</span>
                    <span className="text-green-600">📁 12 findings</span>
                  </div>
                </div>
                
                <div className="bg-white rounded-lg p-3 border border-blue-100">
                  <div className="flex items-center justify-between mb-2">
                    <h4 className="text-sm font-semibold text-gray-800">Vulnerability Assessment - Beta Inc</h4>
                    <span className="text-xs px-2 py-1 bg-green-100 text-green-800 rounded">Ready for Review</span>
                  </div>
                  <div className="text-xs text-gray-600 mb-2">Last updated: 1 day ago</div>
                  <div className="flex items-center gap-2 text-xs">
                    <span className="text-blue-600">👥 2 collaborators</span>
                    <span className="text-gray-400">•</span>
                    <span className="text-orange-600">📁 8 findings</span>
                  </div>
                </div>
              </div>
            </div>
            
            <div className="bg-gray-50 border border-gray-200 rounded-lg p-4">
              <h3 className="text-sm font-semibold text-gray-800 mb-3">✍️ Recent Activity</h3>
              <div className="space-y-2 text-xs">
                <div className="flex items-center gap-2">
                  <span className="w-2 h-2 bg-blue-500 rounded-full"></span>
                  <span>Alice updated Executive Summary in ACME Corp project</span>
                  <span className="text-gray-400 ml-auto">1h ago</span>
                </div>
                <div className="flex items-center gap-2">
                  <span className="w-2 h-2 bg-green-500 rounded-full"></span>
                  <span>Bob added new finding: SQL Injection in login form</span>
                  <span className="text-gray-400 ml-auto">3h ago</span>
                </div>
                <div className="flex items-center gap-2">
                  <span className="w-2 h-2 bg-purple-500 rounded-full"></span>
                  <span>Carol reviewed and approved Beta Inc report</span>
                  <span className="text-gray-400 ml-auto">1d ago</span>
                </div>
              </div>
            </div>
          </div>
          
          <div className="space-y-4">
            <div className="bg-green-50 border border-green-200 rounded-lg p-4">
              <h3 className="text-sm font-semibold text-green-800 mb-3">📈 Quick Stats</h3>
              <div className="space-y-3">
                <div className="flex justify-between text-xs">
                  <span>Active Projects</span>
                  <span className="font-bold text-green-700">2</span>
                </div>
                <div className="flex justify-between text-xs">
                  <span>Pending Reviews</span>
                  <span className="font-bold text-orange-700">1</span>
                </div>
                <div className="flex justify-between text-xs">
                  <span>Completed This Month</span>
                  <span className="font-bold text-blue-700">5</span>
                </div>
                <div className="flex justify-between text-xs">
                  <span>Team Members</span>
                  <span className="font-bold text-purple-700">8</span>
                </div>
              </div>
            </div>
            
            <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
              <h3 className="text-sm font-semibold text-yellow-800 mb-2">🔔 Reminders</h3>
              <div className="space-y-2 text-xs">
                <div className="flex items-start gap-2">
                  <span className="w-2 h-2 bg-red-500 rounded-full mt-1"></span>
                  <span>ACME Corp report due tomorrow</span>
                </div>
                <div className="flex items-start gap-2">
                  <span className="w-2 h-2 bg-yellow-500 rounded-full mt-1"></span>
                  <span>Team meeting Friday 2 PM</span>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <div className="mt-6 flex gap-3">
          <button className="flex-1 bg-indigo-600 text-white px-4 py-2 rounded-lg hover:bg-indigo-700 transition-colors text-sm">
            ➕ New Project
          </button>
          <button className="flex-1 bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors text-sm">
            📄 Templates
          </button>
          <button className="flex-1 bg-gray-600 text-white px-4 py-2 rounded-lg hover:bg-gray-700 transition-colors text-sm">
            📋 Archive
          </button>
        </div>
      </div>
    </div>
  );
}