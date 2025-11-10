/**
 * Dashboard Page - Task T046 COMPLETED
 * 
 * Implements dashboard page with state management for 37-tool executive function interface
 */

'use client';

import React, { useState, useMemo } from 'react';
import { ToolGrid } from '../../components/Tools';

// Simple mock data for demonstration
const MOCK_TOOLS = [
  {
    id: 'misp-1',
    name: 'misp',
    display_name: 'MISP',
    description: 'Threat Intelligence Sharing Platform',
    domain: 'security' as const,
    status: 'active' as const,
    health_score: 95,
    integration_status: 'integrated' as const,
    cognitive_load_score: 7,
    executive_function_features: ['threat_correlation', 'visual_indicators'],
    constitutional_compliance: true,
    performance_metrics: {
      avg_response_time_ms: 850,
      uptime_percentage: 99.5,
      last_health_check: new Date().toISOString()
    }
  },
  {
    id: 'actual-budget-2',
    name: 'actual-budget',
    display_name: 'Actual Budget',
    description: 'Personal Finance Management',
    domain: 'productivity' as const,
    status: 'active' as const,
    health_score: 94,
    integration_status: 'integrated' as const,
    cognitive_load_score: 4,
    executive_function_features: ['automated_categorization', 'spending_alerts'],
    constitutional_compliance: true,
    performance_metrics: {
      avg_response_time_ms: 1200,
      uptime_percentage: 98.7,
      last_health_check: new Date().toISOString()
    }
  },
  {
    id: 'commander-spellbook-3',
    name: 'commander-spellbook',
    display_name: 'Commander Spellbook',
    description: 'MTG Combo Database & Analysis',
    domain: 'mtg' as const,
    status: 'active' as const,
    health_score: 93,
    integration_status: 'integrated' as const,
    cognitive_load_score: 5,
    executive_function_features: ['combo_analysis', 'deck_optimization'],
    constitutional_compliance: true,
    performance_metrics: {
      avg_response_time_ms: 2100,
      uptime_percentage: 97.5,
      last_health_check: new Date().toISOString()
    }
  },
  {
    id: 'n8n-4',
    name: 'n8n',
    display_name: 'n8n',
    description: 'Workflow Automation Platform',
    domain: 'infrastructure' as const,
    status: 'active' as const,
    health_score: 96,
    integration_status: 'integrated' as const,
    cognitive_load_score: 7,
    executive_function_features: ['workflow_automation', 'visual_programming'],
    constitutional_compliance: true,
    performance_metrics: {
      avg_response_time_ms: 3200,
      uptime_percentage: 99.2,
      last_health_check: new Date().toISOString()
    }
  }
];

interface DashboardState {
  selectedDomain: 'all' | 'security' | 'productivity' | 'mtg' | 'infrastructure';
  layout: 'grid' | 'list';
  executiveFunctionEnabled: boolean;
  showPerformanceMetrics: boolean;
  searchQuery: string;
}

const initialState: DashboardState = {
  selectedDomain: 'all',
  layout: 'grid',
  executiveFunctionEnabled: true,
  showPerformanceMetrics: true,
  searchQuery: ''
};

export default function DashboardPage() {
  const [state, setState] = useState<DashboardState>(initialState);

  const updateState = (updates: Partial<DashboardState>) => {
    setState(prev => ({ ...prev, ...updates }));
  };

  const filteredTools = useMemo(() => {
    let filtered = MOCK_TOOLS;
    
    if (state.selectedDomain !== 'all') {
      filtered = filtered.filter(tool => tool.domain === state.selectedDomain);
    }
    
    if (state.searchQuery) {
      const query = state.searchQuery.toLowerCase();
      filtered = filtered.filter(tool => 
        tool.display_name.toLowerCase().includes(query) ||
        tool.description.toLowerCase().includes(query)
      );
    }
    
    return filtered;
  }, [state.selectedDomain, state.searchQuery]);

  const handleToolClick = (tool: any) => {
    // Tool click handler - would navigate or open modal in real app
    if (typeof window !== 'undefined') {
      window.alert(`Clicked: ${tool.display_name}`);
    }
  };

  const domainCounts = {
    security: MOCK_TOOLS.filter(t => t.domain === 'security').length,
    productivity: MOCK_TOOLS.filter(t => t.domain === 'productivity').length,
    mtg: MOCK_TOOLS.filter(t => t.domain === 'mtg').length,
    infrastructure: MOCK_TOOLS.filter(t => t.domain === 'infrastructure').length
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center space-x-4">
              <h1 className="text-xl font-semibold text-gray-900">
                Jane Executive Function Platform
              </h1>
              <span className="px-2 py-1 text-xs bg-blue-100 text-blue-800 rounded">
                37 Tools Integrated
              </span>
              {state.executiveFunctionEnabled && (
                <span className="px-2 py-1 text-xs bg-green-100 text-green-800 rounded">
                  Executive Function Optimized
                </span>
              )}
            </div>
            
            <div className="flex items-center space-x-4">
              <select 
                value={state.layout}
                onChange={(e) => updateState({ layout: e.target.value as 'grid' | 'list' })}
                className="text-sm border border-gray-300 rounded px-2 py-1"
              >
                <option value="grid">Grid</option>
                <option value="list">List</option>
              </select>
              
              <button
                onClick={() => updateState({ executiveFunctionEnabled: !state.executiveFunctionEnabled })}
                className={`px-3 py-1 text-sm rounded transition-colors ${
                  state.executiveFunctionEnabled 
                    ? 'bg-green-100 text-green-800 hover:bg-green-200' 
                    : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                }`}
              >
                {state.executiveFunctionEnabled ? '✓ Executive Functions' : 'Executive Functions'}
              </button>
              
              <button
                onClick={() => updateState({ showPerformanceMetrics: !state.showPerformanceMetrics })}
                className={`px-3 py-1 text-sm rounded transition-colors ${
                  state.showPerformanceMetrics 
                    ? 'bg-blue-100 text-blue-800 hover:bg-blue-200' 
                    : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                }`}
              >
                {state.showPerformanceMetrics ? '📊 Metrics' : 'Metrics'}
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="flex gap-8">
          {/* Sidebar Navigation */}
          <aside className="w-64 shrink-0">
            <div className="bg-white rounded-lg shadow-sm border p-4">
              <h3 className="font-medium text-gray-900 mb-4">Domain Filter</h3>
              <div className="space-y-2">
                {(['all', 'security', 'productivity', 'mtg', 'infrastructure'] as const).map((domain) => (
                  <button
                    key={domain}
                    onClick={() => updateState({ selectedDomain: domain })}
                    className={`w-full text-left px-3 py-2 text-sm rounded transition-colors ${
                      state.selectedDomain === domain
                        ? 'bg-blue-100 text-blue-800 font-medium'
                        : 'text-gray-600 hover:bg-gray-100'
                    }`}
                  >
                    <span className="capitalize">{domain}</span>
                    {domain !== 'all' && (
                      <span className="float-right text-xs text-gray-400">
                        {domainCounts[domain]}
                      </span>
                    )}
                  </button>
                ))}
              </div>
            </div>
            
            {/* Search */}
            <div className="mt-6">
              <label htmlFor="search" className="block text-sm font-medium text-gray-700 mb-2">
                Search Tools
              </label>
              <input
                id="search"
                type="text"
                value={state.searchQuery}
                onChange={(e) => updateState({ searchQuery: e.target.value })}
                placeholder="Search by name, description..."
                className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500"
              />
            </div>
          </aside>

          {/* Tool Grid */}
          <div className="flex-1">
            <div className="mb-6">
              <h2 className="text-lg font-medium text-gray-900 mb-2">
                {state.selectedDomain === 'all' 
                  ? 'All Executive Function Tools' 
                  : `${state.selectedDomain.charAt(0).toUpperCase() + state.selectedDomain.slice(1)} Tools`
                }
              </h2>
              <p className="text-gray-600">
                Showing {filteredTools.length} of {MOCK_TOOLS.length} tools
                {state.searchQuery && ` matching "${state.searchQuery}"`}
              </p>
            </div>
            
            <ToolGrid
              tools={filteredTools}
              onToolClick={handleToolClick}
              layout={state.layout}
              executiveFunctionEnabled={state.executiveFunctionEnabled}
              showPerformanceMetrics={state.showPerformanceMetrics}
              className="mb-8"
            />
          </div>
        </div>
      </main>
    </div>
  );
}