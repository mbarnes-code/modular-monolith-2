/**
 * Mealie Tool Component - Lazy Loaded
 * Productivity Domain - Constitutional Requirement: <2s response time
 */

import { useEffect } from 'react';
import { usePerformanceMonitor } from '../../../services/performance/performanceMonitor';

export default function MealieTool() {
  const { measureOperation } = usePerformanceMonitor();

  useEffect(() => {
    measureOperation('mealie-tool-init', async () => {
      console.log('🍽️ Mealie tool initialized');
    }, 'productivity');
  }, [measureOperation]);

  return (
    <div className="max-w-6xl mx-auto p-6">
      <div className="mb-8">
        <div className="flex items-center gap-3 mb-2">
          <div className="flex items-center justify-center w-12 h-12 bg-green-100 rounded-lg">
            <span className="text-2xl">🍽️</span>
          </div>
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Mealie</h1>
            <p className="text-gray-600">Recipe management and meal planning platform</p>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-4 mb-8">
        <div className="bg-white p-4 rounded-lg border border-gray-200">
          <h3 className="font-semibold text-gray-900 mb-2">📚 Recipes</h3>
          <div className="text-2xl font-bold text-green-600">127</div>
          <p className="text-sm text-gray-500">In collection</p>
        </div>
        
        <div className="bg-white p-4 rounded-lg border border-gray-200">
          <h3 className="font-semibold text-gray-900 mb-2">📅 Meal Plans</h3>
          <div className="text-2xl font-bold text-blue-600">3</div>
          <p className="text-sm text-gray-500">This week</p>
        </div>
        
        <div className="bg-white p-4 rounded-lg border border-gray-200">
          <h3 className="font-semibold text-gray-900 mb-2">📋 Shopping Lists</h3>
          <div className="text-2xl font-bold text-orange-600">2</div>
          <p className="text-sm text-gray-500">Active</p>
        </div>
        
        <div className="bg-white p-4 rounded-lg border border-gray-200">
          <h3 className="font-semibold text-gray-900 mb-2">⭐ Favorites</h3>
          <div className="text-2xl font-bold text-yellow-600">15</div>
          <p className="text-sm text-gray-500">Top recipes</p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white rounded-lg border border-gray-200 p-6">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Recent Recipes</h2>
          <div className="space-y-3">
            <div className="flex items-center gap-3 p-3 bg-gray-50 rounded-lg">
              <span className="text-2xl">🍝</span>
              <div>
                <p className="font-medium">Spaghetti Carbonara</p>
                <p className="text-sm text-gray-500">Added 2 days ago</p>
              </div>
            </div>
            <div className="flex items-center gap-3 p-3 bg-gray-50 rounded-lg">
              <span className="text-2xl">🍔</span>
              <div>
                <p className="font-medium">Chicken Teriyaki Bowl</p>
                <p className="text-sm text-gray-500">Added 5 days ago</p>
              </div>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg border border-gray-200 p-6">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">This Week's Meals</h2>
          <div className="space-y-3">
            <div className="flex items-center justify-between p-3 bg-blue-50 rounded-lg">
              <div>
                <p className="font-medium">Tonight</p>
                <p className="text-sm text-gray-600">Beef Stir Fry</p>
              </div>
              <span className="text-xl">🥩</span>
            </div>
            <div className="flex items-center justify-between p-3 bg-green-50 rounded-lg">
              <div>
                <p className="font-medium">Tomorrow</p>
                <p className="text-sm text-gray-600">Salmon with Rice</p>
              </div>
              <span className="text-xl">🍣</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}