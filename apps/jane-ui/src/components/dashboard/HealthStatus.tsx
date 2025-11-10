/**
 * Health Status Component
 * 
 * Displays system health with executive function accommodations
 */

'use client';

import React from 'react';

interface HealthData {
  overall_health: {
    score: number;
    status: string;
  };
  constitutional_compliance: boolean;
  domain_health: any;
  registry_health: any;
}

interface HealthStatusProps {
  health: HealthData;
  expanded: boolean;
  onToggleExpanded: () => void;
  executiveFunctionEnabled: boolean;
}

export const HealthStatus: React.FC<HealthStatusProps> = ({
  health,
  expanded,
  onToggleExpanded,
  executiveFunctionEnabled
}) => {
  const getStatusColor = (status: string) => {
    switch (status) {
      case 'excellent':
        return 'text-green-600 bg-green-50';
      case 'good':
        return 'text-blue-600 bg-blue-50';
      case 'fair':
        return 'text-amber-600 bg-amber-50';
      default:
        return 'text-red-600 bg-red-50';
    }
  };

  return (
    <div className="health-status bg-white rounded-lg border border-gray-200 p-6">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-xl font-semibold">System Health</h2>
        <button
          onClick={onToggleExpanded}
          className="text-blue-600 hover:text-blue-700 text-sm font-medium"
        >
          {expanded ? 'Show Less' : 'Show Details'}
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="text-center">
          <div className="text-3xl font-bold text-gray-900 mb-2">
            {health.overall_health.score}%
          </div>
          <div className={`inline-block px-3 py-1 rounded-full text-sm font-medium ${getStatusColor(health.overall_health.status)}`}>
            {health.overall_health.status}
          </div>
        </div>

        <div className="text-center">
          <div className="text-lg font-semibold text-gray-900 mb-2">
            Constitutional Compliance
          </div>
          <div className={`inline-block px-3 py-1 rounded-full text-sm font-medium ${
            health.constitutional_compliance 
              ? 'text-green-600 bg-green-50' 
              : 'text-red-600 bg-red-50'
          }`}>
            {health.constitutional_compliance ? 'Compliant' : 'Non-Compliant'}
          </div>
        </div>

        <div className="text-center">
          <div className="text-lg font-semibold text-gray-900 mb-2">
            Executive Function
          </div>
          <div className="inline-block px-3 py-1 rounded-full text-sm font-medium text-green-600 bg-green-50">
            {executiveFunctionEnabled ? 'Enabled' : 'Disabled'}
          </div>
        </div>
      </div>

      {expanded && (
        <div className="mt-6 pt-6 border-t border-gray-200">
          <div className="space-y-4">
            <h3 className="text-lg font-medium">Detailed Metrics</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="bg-gray-50 rounded-lg p-4">
                <h4 className="font-medium mb-2">Domain Health</h4>
                <p className="text-sm text-gray-600">All 4 domains operational</p>
              </div>
              <div className="bg-gray-50 rounded-lg p-4">
                <h4 className="font-medium mb-2">Tool Registry</h4>
                <p className="text-sm text-gray-600">37 tools registered</p>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};