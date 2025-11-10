/**
 * Quick Actions Component
 * 
 * Provides immediate access to frequently used actions
 * with executive function accommodations
 */

'use client';

import React from 'react';

interface QuickAction {
  id: string;
  title: string;
  description: string;
  action_type: string;
  target: string;
  icon: string;
  color: string;
}

interface QuickActionsProps {
  actions: QuickAction[];
  onActionClick: (action: QuickAction) => void;
  executiveFunctionEnabled: boolean;
}

export const QuickActions: React.FC<QuickActionsProps> = ({
  actions,
  onActionClick,
  executiveFunctionEnabled
}) => {
  return (
    <div className="quick-actions bg-white rounded-lg border border-gray-200 p-4">
      <h3 className="text-lg font-semibold mb-3">Quick Actions</h3>
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
        {actions.map((action) => (
          <button
            key={action.id}
            onClick={() => onActionClick(action)}
            className="flex flex-col items-center p-3 rounded-lg border border-gray-200 hover:border-blue-300 hover:bg-blue-50 transition-colors"
            style={{ borderLeftColor: action.color, borderLeftWidth: '3px' }}
          >
            <div className="text-sm font-medium text-gray-900 mb-1">
              {action.title}
            </div>
            <div className="text-xs text-gray-500 text-center">
              {action.description}
            </div>
          </button>
        ))}
      </div>
      {executiveFunctionEnabled && (
        <div className="mt-3 text-xs text-gray-500 flex items-center">
          <div className="w-2 h-2 bg-green-400 rounded-full mr-2"></div>
          Executive function optimized
        </div>
      )}
    </div>
  );
};