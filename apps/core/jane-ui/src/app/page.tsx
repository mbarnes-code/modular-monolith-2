'use client';

import { MonitoringDashboard, ProductionAlerts, ProductionMonitorProvider } from '../components/monitoring';

export default function Home() {
  return (
    <ProductionMonitorProvider>
      <main className="min-h-screen bg-gray-50 dark:bg-gray-900 p-8">
      <div className="max-w-4xl mx-auto">
        {/* Welcome Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
            Jane Mental Prosthetic Platform - Phase 3 & 4 Complete ✅
          </h1>
          <p className="text-lg text-gray-600 dark:text-gray-400">
            Executive function support consolidating 37 specialized tools
          </p>
        </div>

        {/* Phase Completion Summary */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
          <div className="bg-green-50 dark:bg-green-900/20 p-6 rounded-lg border border-green-200 dark:border-green-700">
            <h2 className="text-xl font-semibold text-green-800 dark:text-green-200 mb-4">
              ✅ Phase 3: UX Polish Complete
            </h2>
            <ul className="text-sm text-green-700 dark:text-green-300 space-y-2">
              <li>• Advanced Focus Mode with deep work sessions</li>
              <li>• Cognitive Load Manager with executive function support</li>
              <li>• Enhanced Tool Switcher (37 tools, predictive suggestions)</li>
              <li>• Cross-domain Workflow Manager with automation</li>
              <li>• Adaptive UI Layout with keyboard shortcuts</li>
            </ul>
          </div>

          <div className="bg-blue-50 dark:bg-blue-900/20 p-6 rounded-lg border border-blue-200 dark:border-blue-700">
            <h2 className="text-xl font-semibold text-blue-800 dark:text-blue-200 mb-4">
              ✅ Phase 4: Production Readiness
            </h2>
            <ul className="text-sm text-blue-700 dark:text-blue-300 space-y-2">
              <li>• Production Performance Monitor with Web Vitals</li>
              <li>• Constitutional compliance validation</li>
              <li>• Domain-specific performance thresholds</li>
              <li>• Real-time alerting and metrics export</li>
              <li>• SSR-safe component architecture</li>
            </ul>
          </div>
        </div>

        {/* Constitutional Compliance Status */}
        <div className="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 p-6 mb-8">
          <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">
            Constitutional Performance Requirements
          </h2>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="text-center p-3 bg-red-50 dark:bg-red-900/20 rounded border border-red-200 dark:border-red-700">
              <div className="text-lg font-bold text-red-600 dark:text-red-400">Security</div>
              <div className="text-sm text-red-800 dark:text-red-300">&lt; 1 second</div>
            </div>
            <div className="text-center p-3 bg-green-50 dark:bg-green-900/20 rounded border border-green-200 dark:border-green-700">
              <div className="text-lg font-bold text-green-600 dark:text-green-400">Productivity</div>
              <div className="text-sm text-green-800 dark:text-green-300">&lt; 2 seconds</div>
            </div>
            <div className="text-center p-3 bg-purple-50 dark:bg-purple-900/20 rounded border border-purple-200 dark:border-purple-700">
              <div className="text-lg font-bold text-purple-600 dark:text-purple-400">MTG</div>
              <div className="text-sm text-purple-800 dark:text-purple-300">&lt; 3 seconds</div>
            </div>
            <div className="text-center p-3 bg-gray-50 dark:bg-gray-700 rounded border border-gray-200 dark:border-gray-600">
              <div className="text-lg font-bold text-gray-600 dark:text-gray-400">Infrastructure</div>
              <div className="text-sm text-gray-800 dark:text-gray-300">&lt; 5 seconds</div>
            </div>
          </div>
        </div>

        {/* Key Features Implemented */}
        <div className="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 p-6 mb-8">
          <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">
            Executive Function Features
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <h3 className="font-semibold text-gray-900 dark:text-white mb-2">🧠 Cognitive Load Management</h3>
              <ul className="text-sm text-gray-600 dark:text-gray-400 space-y-1">
                <li>• Real-time load monitoring with domain-specific thresholds</li>
                <li>• Context switching penalty calculation</li>
                <li>• Fatigue detection and break recommendations</li>
                <li>• Tool complexity filtering based on current capacity</li>
              </ul>
            </div>
            <div>
              <h3 className="font-semibold text-gray-900 dark:text-white mb-2">🎯 Focus & Productivity</h3>
              <ul className="text-sm text-gray-600 dark:text-gray-400 space-y-1">
                <li>• Multiple focus modes (Pomodoro, Deep Work, Flow State)</li>
                <li>• Distraction tracking and session statistics</li>
                <li>• Workflow automation for multi-tool tasks</li>
                <li>• Predictive tool suggestions based on context</li>
              </ul>
            </div>
          </div>
        </div>

        {/* Technical Architecture */}
        <div className="bg-gray-50 dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 p-6">
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
            Technical Implementation
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 text-sm">
            <div>
              <span className="text-gray-600 dark:text-gray-400">Frontend:</span>
              <div className="font-medium text-gray-900 dark:text-white">Next.js 15.5.2 + React 19.1.0</div>
            </div>
            <div>
              <span className="text-gray-600 dark:text-gray-400">State Management:</span>
              <div className="font-medium text-gray-900 dark:text-white">Zustand + Event Bus</div>
            </div>
            <div>
              <span className="text-gray-600 dark:text-gray-400">Performance:</span>
              <div className="font-medium text-green-600 dark:text-green-400">Web Vitals Monitoring ✓</div>
            </div>
            <div>
              <span className="text-gray-600 dark:text-gray-400">Bundle Analysis:</span>
              <div className="font-medium text-green-600 dark:text-green-400">Domain-specific Chunking ✓</div>
            </div>
            <div>
              <span className="text-gray-600 dark:text-gray-400">Accessibility:</span>
              <div className="font-medium text-green-600 dark:text-green-400">WCAG 2.1 AA ✓</div>
            </div>
            <div>
              <span className="text-gray-600 dark:text-gray-400">Executive Support:</span>
              <div className="font-medium text-green-600 dark:text-green-400">ADHD/Autism Optimized ✓</div>
            </div>
          </div>
        </div>

        {/* Next Steps Notice */}
        <div className="mt-8 p-4 bg-yellow-50 dark:bg-yellow-900/20 border border-yellow-200 dark:border-yellow-700 rounded-lg">
          <h4 className="font-medium text-yellow-800 dark:text-yellow-200 mb-2">
            🚀 Implementation Complete - Next Steps
          </h4>
          <p className="text-sm text-yellow-700 dark:text-yellow-300">
            Phase 3 & 4 UX optimizations and production monitoring are now implemented. 
            The enhanced layout with full cognitive load management is available in the JaneUILayout component.
            To activate, simply import and use JaneUILayout in place of this simple layout.
          </p>
        </div>
      </div>
      
      {/* Production Monitoring Components */}
      <ProductionAlerts />
      <MonitoringDashboard />
    </main>
    </ProductionMonitorProvider>
  );
}
