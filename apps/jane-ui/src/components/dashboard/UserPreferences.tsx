/**
 * User Preferences Component
 * 
 * Executive function preference management
 */

'use client';

import React from 'react';

interface User {
  id: string;
  username: string;
  email: string;
  adhd_accommodations?: Record<string, unknown>;
  autism_accommodations?: Record<string, unknown>;
  ui_preferences?: Record<string, unknown>;
  preferred_domains?: string[];
}

interface UserPreferencesProps {
  user: User | null;
  onPreferencesUpdate: (preferences: Record<string, unknown>) => void;
  executiveFunctionEnabled: boolean;
}

export const UserPreferences: React.FC<UserPreferencesProps> = ({
  user,
  onPreferencesUpdate,
  executiveFunctionEnabled
}) => {
  if (!user) {
    return (
      <div className="user-preferences bg-white rounded-lg border border-gray-200 p-6">
        <h2 className="text-xl font-semibold mb-4">User Preferences</h2>
        <p className="text-gray-500">Please log in to manage your preferences.</p>
      </div>
    );
  }

  return (
    <div className="user-preferences bg-white rounded-lg border border-gray-200 p-6">
      <h2 className="text-xl font-semibold mb-4">User Preferences</h2>
      
      <div className="space-y-6">
        <div>
          <h3 className="text-lg font-medium mb-3">Executive Function Support</h3>
          <div className="space-y-3">
            <label className="flex items-center">
              <input
                type="checkbox"
                checked={!!user.adhd_accommodations}
                onChange={(e) => onPreferencesUpdate({
                  adhd_accommodations: e.target.checked ? { enabled: true } : null
                })}
                className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
              />
              <span className="ml-2 text-sm text-gray-700">Enable ADHD accommodations</span>
            </label>
            
            <label className="flex items-center">
              <input
                type="checkbox"
                checked={!!user.autism_accommodations}
                onChange={(e) => onPreferencesUpdate({
                  autism_accommodations: e.target.checked ? { enabled: true } : null
                })}
                className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
              />
              <span className="ml-2 text-sm text-gray-700">Enable autism accommodations</span>
            </label>
          </div>
        </div>

        <div>
          <h3 className="text-lg font-medium mb-3">UI Preferences</h3>
          <div className="space-y-3">
            <label className="flex items-center">
              <input
                type="checkbox"
                defaultChecked={false}
                className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
              />
              <span className="ml-2 text-sm text-gray-700">Reduce animations</span>
            </label>
            
            <label className="flex items-center">
              <input
                type="checkbox"
                defaultChecked={false}
                className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
              />
              <span className="ml-2 text-sm text-gray-700">High contrast mode</span>
            </label>
          </div>
        </div>

        <div>
          <h3 className="text-lg font-medium mb-3">Preferred Domains</h3>
          <div className="grid grid-cols-2 gap-3">
            {['security', 'productivity', 'mtg', 'infrastructure'].map((domain) => (
              <label key={domain} className="flex items-center">
                <input
                  type="checkbox"
                  defaultChecked={user.preferred_domains?.includes(domain)}
                  className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                />
                <span className="ml-2 text-sm text-gray-700 capitalize">{domain}</span>
              </label>
            ))}
          </div>
        </div>
      </div>

      {executiveFunctionEnabled && (
        <div className="mt-6 pt-6 border-t border-gray-200">
          <div className="flex items-center text-sm text-green-600">
            <div className="w-2 h-2 bg-green-400 rounded-full mr-2"></div>
            Executive function accommodations are active
          </div>
        </div>
      )}
    </div>
  );
};