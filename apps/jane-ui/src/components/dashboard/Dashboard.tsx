/**
 * Executive Function Dashboard - Main Component
 * 
 * Constitutional Requirements:
 * - Unified access to all 37 tools across 4 domains
 * - ADHD/autism-friendly UI with <200ms interactions
 * - Context switching reduction and cognitive load optimization
 * - WCAG 2.1 AA compliance for accessibility
 */

'use client';

import { AnimatePresence, motion } from 'framer-motion';
import {
    AlertCircle,
    Filter,
    Grid,
    Heart,
    Settings,
    User
} from 'lucide-react';
import React, { useCallback, useEffect, useMemo, useState } from 'react';

import { DomainCard } from './DomainCard';
import { ExecutiveFunctionSupport } from './ExecutiveFunctionSupport';
import { HealthStatus } from './HealthStatus';
import { QuickActions } from './QuickActions';
import { SearchBar } from './SearchBar';
import { ToolGrid } from './ToolGrid';
import { UserPreferences } from './UserPreferences';

import { useAuth } from '../../hooks/useAuth';
import { useDashboard } from '../../hooks/useDashboard';
import { useExecutiveFunction } from '../../hooks/useExecutiveFunction';

interface DashboardProps {
  initialView?: 'overview' | 'domains' | 'tools' | 'health';
  className?: string;
}

interface DashboardState {
  currentView: 'overview' | 'domains' | 'tools' | 'health' | 'preferences';
  searchQuery: string;
  selectedDomain: string | null;
  showQuickActions: boolean;
  healthExpanded: boolean;
  cognitiveLoadLevel: 'low' | 'medium' | 'high';
}

export const Dashboard: React.FC<DashboardProps> = ({ 
  initialView = 'overview',
  className = ''
}) => {
  // State management
  const [state, setState] = useState<DashboardState>({
    currentView: initialView,
    searchQuery: '',
    selectedDomain: null,
    showQuickActions: true,
    healthExpanded: false,
    cognitiveLoadLevel: 'medium'
  });

  // Custom hooks for data and functionality
  const { user, isAuthenticated } = useAuth();
  const { 
    dashboard, 
    domains, 
    tools, 
    health, 
    recommendations,
    loading, 
    error,
    refreshDashboard,
    searchTools
  } = useDashboard();
  
  const {
    cognitiveLoadAssessment,
    applyExecutiveFunctionSupport,
    optimizeForADHD,
    optimizeForAutism,
    reduceCognitiveLoad
  } = useExecutiveFunction(user);

  // Executive function optimizations based on user preferences
  const executiveFunctionConfig = useMemo(() => {
    if (!user) return null;

    return {
      adhdSupport: user.adhd_accommodations?.enabled || false,
      autismSupport: user.autism_accommodations?.enabled || false,
      reducedAnimations: user.ui_preferences?.reduce_animations || false,
      highContrast: user.ui_preferences?.high_contrast || false,
      largeText: user.ui_preferences?.large_text || false,
      cognitiveLoadReduction: user.adhd_accommodations?.reduce_cognitive_load || false,
      contextSwitchingMinimization: true,
      responseTimeOptimization: true
    };
  }, [user]);

  // Handle view changes with executive function considerations
  const handleViewChange = useCallback((
    newView: DashboardState['currentView']
  ) => {
    // Provide gentle transition feedback for executive function support
    setState(prev => ({
      ...prev,
      currentView: newView,
      searchQuery: newView !== prev.currentView ? '' : prev.searchQuery
    }));

    // Announce view change for screen readers
    const announcement = `Switched to ${newView} view`;
    if (typeof window !== 'undefined' && window.speechSynthesis) {
      const utterance = new SpeechSynthesisUtterance(announcement);
      utterance.volume = 0.1; // Low volume for non-intrusive feedback
      window.speechSynthesis.speak(utterance);
    }
  }, []);

  // Handle search with debouncing for executive function support
  const handleSearch = useCallback((query: string) => {
    setState(prev => ({ ...prev, searchQuery: query }));
    
    // Debounced search to reduce cognitive load
    if (query.length >= 2) {
      const timeoutId = setTimeout(() => {
        searchTools(query, state.selectedDomain);
      }, 300); // 300ms debounce
      
      return () => clearTimeout(timeoutId);
    }
  }, [searchTools, state.selectedDomain]);

  // Handle domain selection with context preservation
  const handleDomainSelect = useCallback((domainName: string | null) => {
    setState(prev => ({
      ...prev,
      selectedDomain: domainName,
      currentView: domainName ? 'domains' : 'overview'
    }));
  }, []);

  // Monitor cognitive load and provide assistance
  useEffect(() => {
    if (cognitiveLoadAssessment && executiveFunctionConfig) {
      const currentLoad = cognitiveLoadAssessment.current_level;
      
      if (currentLoad !== state.cognitiveLoadLevel) {
        setState(prev => ({ ...prev, cognitiveLoadLevel: currentLoad }));
        
        // Apply appropriate accommodations
        if (currentLoad === 'high') {
          reduceCognitiveLoad();
        }
      }
    }
  }, [cognitiveLoadAssessment, executiveFunctionConfig, state.cognitiveLoadLevel, reduceCognitiveLoad]);

  // Auto-refresh dashboard data
  useEffect(() => {
    const interval = setInterval(() => {
      if (document.visibilityState === 'visible') {
        refreshDashboard();
      }
    }, 30000); // Refresh every 30 seconds when visible

    return () => clearInterval(interval);
  }, [refreshDashboard]);

  // Error boundary and loading states
  if (error) {
    return (
      <div className={`dashboard-error ${className}`} role="alert">
        <AlertCircle className="w-8 h-8 text-red-500 mb-4" />
        <h2 className="text-xl font-semibold mb-2">Dashboard Temporarily Unavailable</h2>
        <p className="text-gray-600 mb-4">
          We're working to resolve this issue. Please try again in a moment.
        </p>
        <button 
          onClick={refreshDashboard}
          className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 transition-colors"
        >
          Try Again
        </button>
      </div>
    );
  }

  if (loading && !dashboard) {
    return (
      <div className={`dashboard-loading ${className}`} role="status" aria-live="polite">
        <div className="flex items-center justify-center min-h-[400px]">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
          <span className="ml-4 text-lg">Loading your executive function dashboard...</span>
        </div>
      </div>
    );
  }

  // Main dashboard layout with executive function optimizations
  return (
    <div 
      className={`dashboard-container ${className}`}
      data-executive-function-enabled={!!executiveFunctionConfig}
      data-cognitive-load={state.cognitiveLoadLevel}
    >
      {/* Executive Function Support Overlay */}
      {executiveFunctionConfig && (
        <ExecutiveFunctionSupport 
          config={executiveFunctionConfig}
          cognitiveLoad={state.cognitiveLoadLevel}
          onLoadReduction={reduceCognitiveLoad}
        />
      )}

      {/* Dashboard Header */}
      <header className="dashboard-header bg-white shadow-sm border-b border-gray-200 px-6 py-4">
        <div className="flex items-center justify-between">
          {/* Welcome Section */}
          <div className="flex items-center space-x-4">
            <div className="flex items-center space-x-2">
              <Grid className="w-6 h-6 text-blue-600" />
              <h1 className="text-2xl font-bold text-gray-900">
                Executive Function Dashboard
              </h1>
            </div>
            {user && (
              <div className="hidden md:flex items-center space-x-2 text-sm text-gray-600">
                <User className="w-4 h-4" />
                <span>Welcome, {user.username}</span>
              </div>
            )}
          </div>

          {/* Header Actions */}
          <div className="flex items-center space-x-4">
            {/* Quick Health Status */}
            {health && (
              <div className="flex items-center space-x-2">
                <Heart 
                  className={`w-5 h-5 ${
                    health.overall_health.status === 'excellent' ? 'text-green-500' :
                    health.overall_health.status === 'good' ? 'text-blue-500' :
                    health.overall_health.status === 'fair' ? 'text-yellow-500' :
                    'text-red-500'
                  }`} 
                />
                <span className="text-sm font-medium">
                  {health.overall_health.score}% Healthy
                </span>
              </div>
            )}

            {/* View Toggle */}
            <div className="flex items-center space-x-1 bg-gray-100 rounded-lg p-1">
              {(['overview', 'domains', 'tools', 'health'] as const).map((view) => (
                <button
                  key={view}
                  onClick={() => handleViewChange(view)}
                  className={`px-3 py-1 text-sm rounded transition-all duration-150 ${
                    state.currentView === view 
                      ? 'bg-white text-blue-600 shadow-sm' 
                      : 'text-gray-600 hover:text-gray-900'
                  }`}
                  aria-pressed={state.currentView === view}
                >
                  {view.charAt(0).toUpperCase() + view.slice(1)}
                </button>
              ))}
            </div>

            {/* Settings */}
            <button
              onClick={() => handleViewChange('preferences')}
              className="p-2 text-gray-600 hover:text-gray-900 transition-colors"
              aria-label="User preferences and settings"
            >
              <Settings className="w-5 h-5" />
            </button>
          </div>
        </div>

        {/* Search Bar - Always visible for executive function support */}
        <div className="mt-4">
          <SearchBar
            value={state.searchQuery}
            onChange={handleSearch}
            placeholder="Search across all 37 tools and 4 domains..."
            executiveFunctionEnabled={!!executiveFunctionConfig}
          />
        </div>
      </header>

      {/* Main Dashboard Content */}
      <main className="dashboard-main flex-1 overflow-y-auto">
        <div className="max-w-7xl mx-auto px-6 py-6">
          <AnimatePresence mode="wait">
            <motion.div
              key={state.currentView}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              transition={{ 
                duration: executiveFunctionConfig?.reducedAnimations ? 0.1 : 0.3,
                ease: 'easeInOut'
              }}
            >
              {/* Overview View */}
              {state.currentView === 'overview' && (
                <div className="overview-layout space-y-6">
                  {/* Quick Actions Bar */}
                  {state.showQuickActions && dashboard?.quick_actions && (
                    <QuickActions
                      actions={dashboard.quick_actions}
                      onActionClick={(action) => console.log('Quick action:', action)}
                      executiveFunctionEnabled={!!executiveFunctionConfig}
                    />
                  )}

                  {/* Domain Cards */}
                  <section aria-labelledby="domains-heading">
                    <h2 id="domains-heading" className="text-xl font-semibold mb-4">
                      Executive Function Domains
                      <span className="ml-2 text-sm text-gray-500">
                        ({domains?.length || 4} domains, {dashboard?.tool_summary?.total_tools || 37} tools)
                      </span>
                    </h2>
                    <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-6">
                      {domains?.map((domain) => (
                        <DomainCard
                          key={domain.name}
                          domain={domain}
                          onClick={() => handleDomainSelect(domain.name)}
                          executiveFunctionEnabled={!!executiveFunctionConfig}
                        />
                      ))}
                    </div>
                  </section>

                  {/* Recommendations */}
                  {recommendations && recommendations.length > 0 && (
                    <section aria-labelledby="recommendations-heading">
                      <h2 id="recommendations-heading" className="text-xl font-semibold mb-4">
                        Personalized Recommendations
                      </h2>
                      <ToolGrid
                        tools={recommendations}
                        onToolClick={(tool) => console.log('Tool clicked:', tool)}
                        layout="grid"
                        executiveFunctionEnabled={!!executiveFunctionConfig}
                      />
                    </section>
                  )}
                </div>
              )}

              {/* Domains View */}
              {state.currentView === 'domains' && (
                <div className="domains-layout">
                  {state.selectedDomain ? (
                    <div>
                      {/* Domain details and tools */}
                      <h2 className="text-2xl font-bold mb-6">
                        {state.selectedDomain.charAt(0).toUpperCase() + state.selectedDomain.slice(1)} Domain
                      </h2>
                      <ToolGrid
                        tools={tools?.filter(tool => tool.domain === state.selectedDomain) || []}
                        onToolClick={(tool) => console.log('Tool clicked:', tool)}
                        layout="grid"
                        executiveFunctionEnabled={!!executiveFunctionConfig}
                      />
                    </div>
                  ) : (
                    <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-6">
                      {domains?.map((domain) => (
                        <DomainCard
                          key={domain.name}
                          domain={domain}
                          onClick={() => handleDomainSelect(domain.name)}
                          executiveFunctionEnabled={!!executiveFunctionConfig}
                          detailed={true}
                        />
                      ))}
                    </div>
                  )}
                </div>
              )}

              {/* Tools View */}
              {state.currentView === 'tools' && (
                <div className="tools-layout">
                  <div className="flex items-center justify-between mb-6">
                    <h2 className="text-2xl font-bold">
                      All Tools
                      <span className="ml-2 text-lg text-gray-500">
                        ({tools?.length || 0} tools)
                      </span>
                    </h2>
                    <div className="flex items-center space-x-2">
                      <Filter className="w-4 h-4 text-gray-500" />
                      <select
                        value={state.selectedDomain || ''}
                        onChange={(e) => handleDomainSelect(e.target.value || null)}
                        className="border rounded px-3 py-1 text-sm"
                      >
                        <option value="">All Domains</option>
                        {domains?.map(domain => (
                          <option key={domain.name} value={domain.name}>
                            {domain.display_name}
                          </option>
                        ))}
                      </select>
                    </div>
                  </div>
                  
                  <ToolGrid
                    tools={tools || []}
                    onToolClick={(tool) => console.log('Tool clicked:', tool)}
                    layout="list"
                    executiveFunctionEnabled={!!executiveFunctionConfig}
                  />
                </div>
              )}

              {/* Health View */}
              {state.currentView === 'health' && health && (
                <HealthStatus
                  health={health}
                  expanded={state.healthExpanded}
                  onToggleExpanded={() => setState(prev => ({
                    ...prev,
                    healthExpanded: !prev.healthExpanded
                  }))}
                  executiveFunctionEnabled={!!executiveFunctionConfig}
                />
              )}

              {/* Preferences View */}
              {state.currentView === 'preferences' && (
                <UserPreferences
                  user={user}
                  onPreferencesUpdate={(prefs) => console.log('Preferences updated:', prefs)}
                  executiveFunctionEnabled={!!executiveFunctionConfig}
                />
              )}
            </motion.div>
          </AnimatePresence>
        </div>
      </main>

      {/* Cognitive Load Monitor */}
      {executiveFunctionConfig && state.cognitiveLoadLevel === 'high' && (
        <div className="fixed bottom-4 right-4 bg-amber-100 border border-amber-300 rounded-lg p-4 shadow-lg">
          <div className="flex items-center space-x-2">
            <AlertCircle className="w-5 h-5 text-amber-600" />
            <div>
              <p className="text-sm font-medium text-amber-800">High Cognitive Load Detected</p>
              <p className="text-xs text-amber-700">Consider taking a break or simplifying your view</p>
            </div>
            <button
              onClick={reduceCognitiveLoad}
              className="ml-2 px-2 py-1 bg-amber-200 text-amber-800 rounded text-xs hover:bg-amber-300"
            >
              Simplify
            </button>
          </div>
        </div>
      )}
    </div>
  );
};