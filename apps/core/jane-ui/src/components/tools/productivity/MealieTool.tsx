'use client';

import { useEffect, useState } from 'react';
import { usePerformanceMonitor } from '../../../services/performance/performanceMonitor';
import { ToolComponentProps } from '../../../services/toolLoader';

export function MealieTool({ onClose, onError, toolId = 'mealie', ...props }: ToolComponentProps) {
  const { measureOperation } = usePerformanceMonitor();
  const [isInitialized, setIsInitialized] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const initializeTool = async () => {
      try {
        await measureOperation(
          'mealie-tool-init',
          async () => {
            // Productivity domain constitutional compliance (<2s)
            await new Promise(resolve => setTimeout(resolve, 600));
            setIsInitialized(true);
          },
          'productivity'
        );
      } catch (err) {
        const errorMsg = err instanceof Error ? err.message : 'Failed to initialize Mealie';
        setError(errorMsg);
        onError?.(new Error(errorMsg));
      }
    };

    initializeTool();
  }, [measureOperation, onError]);

  if (error) {
    return (
      <div className="mealie-tool-error p-6 bg-red-50 border border-red-200 rounded-lg">
        <h3 className="text-lg font-semibold text-red-800 mb-2">❌ Mealie Tool Error</h3>
        <p className="text-red-700">{error}</p>
        <button onClick={onClose} className="mt-4 px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700">
          Close Tool
        </button>
      </div>
    );
  }

  if (!isInitialized) {
    return (
      <div className="mealie-tool-loading flex items-center justify-center p-8 bg-green-50 rounded-lg">
        <div className="text-center">
          <div className="animate-spin h-8 w-8 border-2 border-green-500 border-t-transparent rounded-full mx-auto mb-4"></div>
          <p className="text-sm text-green-600">Initializing Mealie...</p>
          <p className="text-xs text-green-400 mt-1">Recipe management • Executive function support</p>
        </div>
      </div>
    );
  }

  return (
    <div className="mealie-tool bg-white border border-gray-200 rounded-lg shadow-sm" {...props}>
      <div className="mealie-tool-header flex items-center justify-between p-4 border-b border-gray-200">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 bg-green-100 rounded-lg flex items-center justify-center">
            <span className="text-green-600 font-bold">🍽️</span>
          </div>
          <div>
            <h2 className="text-lg font-semibold text-gray-900">Mealie</h2>
            <p className="text-sm text-gray-500">Recipe Management & Meal Planning</p>
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

      <div className="mealie-tool-content p-6">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="lg:col-span-2 space-y-4">
            <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
              <h3 className="text-sm font-semibold text-blue-800 mb-3">📊 This Week's Meal Plan</h3>
              <div className="grid grid-cols-7 gap-2 text-xs">
                {['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'].map((day, index) => (
                  <div key={day} className="bg-white rounded p-2 text-center border border-blue-100">
                    <div className="font-semibold text-blue-700 mb-1">{day}</div>
                    <div className="text-gray-600 text-xs">
                      {index === 0 && 'Pasta Carbonara'}
                      {index === 1 && 'Chicken Stir Fry'}
                      {index === 2 && 'Taco Tuesday'}
                      {index === 3 && 'Thai Curry'}
                      {index === 4 && 'Pizza Night'}
                      {index === 5 && 'Grilled Salmon'}
                      {index === 6 && 'Sunday Roast'}
                    </div>
                  </div>
                ))}
              </div>
            </div>
            
            <div className="bg-green-50 border border-green-200 rounded-lg p-4">
              <h3 className="text-sm font-semibold text-green-800 mb-3">🎆 Featured Recipes</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                <div className="bg-white rounded-lg p-3 border border-green-100">
                  <div className="flex items-center gap-3 mb-2">
                    <div className="w-12 h-12 bg-orange-100 rounded-lg flex items-center justify-center">
                      <span className="text-orange-600">🍝</span>
                    </div>
                    <div>
                      <h4 className="text-sm font-semibold text-gray-800">Creamy Mushroom Risotto</h4>
                      <div className="flex items-center gap-2 text-xs text-gray-600">
                        <span>⏱️ 35 min</span>
                        <span>•</span>
                        <span>👥 4 servings</span>
                        <span>•</span>
                        <span>⭐ 4.8/5</span>
                      </div>
                    </div>
                  </div>
                  <div className="flex gap-2">
                    <button className="flex-1 bg-green-600 text-white px-2 py-1 rounded text-xs hover:bg-green-700">
                      Cook Now
                    </button>
                    <button className="flex-1 bg-gray-200 text-gray-700 px-2 py-1 rounded text-xs hover:bg-gray-300">
                      Add to Plan
                    </button>
                  </div>
                </div>
                
                <div className="bg-white rounded-lg p-3 border border-green-100">
                  <div className="flex items-center gap-3 mb-2">
                    <div className="w-12 h-12 bg-red-100 rounded-lg flex items-center justify-center">
                      <span className="text-red-600">🍕</span>
                    </div>
                    <div>
                      <h4 className="text-sm font-semibold text-gray-800">Margherita Pizza</h4>
                      <div className="flex items-center gap-2 text-xs text-gray-600">
                        <span>⏱️ 45 min</span>
                        <span>•</span>
                        <span>👥 2 servings</span>
                        <span>•</span>
                        <span>⭐ 4.9/5</span>
                      </div>
                    </div>
                  </div>
                  <div className="flex gap-2">
                    <button className="flex-1 bg-green-600 text-white px-2 py-1 rounded text-xs hover:bg-green-700">
                      Cook Now
                    </button>
                    <button className="flex-1 bg-gray-200 text-gray-700 px-2 py-1 rounded text-xs hover:bg-gray-300">
                      Add to Plan
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
          
          <div className="space-y-4">
            <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
              <h3 className="text-sm font-semibold text-yellow-800 mb-3">📋 Shopping List</h3>
              <div className="space-y-2 text-xs">
                <div className="flex items-center gap-2">
                  <input type="checkbox" className="rounded" />
                  <span>Arborio rice (1 lb)</span>
                </div>
                <div className="flex items-center gap-2">
                  <input type="checkbox" className="rounded" />
                  <span>Mixed mushrooms (8 oz)</span>
                </div>
                <div className="flex items-center gap-2">
                  <input type="checkbox" className="rounded" checked readOnly />
                  <span className="line-through text-gray-500">Heavy cream (1 cup)</span>
                </div>
                <div className="flex items-center gap-2">
                  <input type="checkbox" className="rounded" />
                  <span>Parmesan cheese (4 oz)</span>
                </div>
                <div className="flex items-center gap-2">
                  <input type="checkbox" className="rounded" />
                  <span>Fresh basil</span>
                </div>
              </div>
              <button className="w-full mt-3 bg-yellow-600 text-white px-3 py-1 rounded text-xs hover:bg-yellow-700">
                📧 Email List
              </button>
            </div>
            
            <div className="bg-purple-50 border border-purple-200 rounded-lg p-4">
              <h3 className="text-sm font-semibold text-purple-800 mb-2">🎯 Executive Function Support</h3>
              <div className="space-y-2 text-xs">
                <div className="flex items-center gap-2">
                  <span className="text-green-600">✅</span>
                  <span>Meal plan breakdown by day</span>
                </div>
                <div className="flex items-center gap-2">
                  <span className="text-green-600">✅</span>
                  <span>Auto-generated shopping lists</span>
                </div>
                <div className="flex items-center gap-2">
                  <span className="text-green-600">✅</span>
                  <span>Recipe difficulty ratings</span>
                </div>
                <div className="flex items-center gap-2">
                  <span className="text-green-600">✅</span>
                  <span>Time estimates and prep steps</span>
                </div>
              </div>
            </div>
            
            <div className="bg-gray-50 border border-gray-200 rounded-lg p-4">
              <h3 className="text-sm font-semibold text-gray-800 mb-2">📈 Quick Stats</h3>
              <div className="grid grid-cols-2 gap-2 text-xs">
                <div className="text-center">
                  <div className="text-lg font-bold text-blue-600">47</div>
                  <div className="text-gray-600">Recipes</div>
                </div>
                <div className="text-center">
                  <div className="text-lg font-bold text-green-600">12</div>
                  <div className="text-gray-600">Favorites</div>
                </div>
                <div className="text-center">
                  <div className="text-lg font-bold text-orange-600">3</div>
                  <div className="text-gray-600">Categories</div>
                </div>
                <div className="text-center">
                  <div className="text-lg font-bold text-purple-600">28</div>
                  <div className="text-gray-600">Days Planned</div>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <div className="mt-6 flex gap-3">
          <button className="flex-1 bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 transition-colors text-sm">
            ➕ Add Recipe
          </button>
          <button className="flex-1 bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors text-sm">
            📊 Plan Week
          </button>
          <button className="flex-1 bg-purple-600 text-white px-4 py-2 rounded-lg hover:bg-purple-700 transition-colors text-sm">
            🔍 Browse
          </button>
        </div>
      </div>
    </div>
  );
}