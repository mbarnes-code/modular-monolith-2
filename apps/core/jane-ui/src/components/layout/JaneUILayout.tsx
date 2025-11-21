/**
 * Enhanced Jane UI Layout
 * Integrates all Phase 3 UX enhancements with cognitive load management
 */

'use client';

import React, { useState, useEffect } from 'react';
import { EnhancedNavigation } from '../navigation/EnhancedNavigation';
import { EnhancedToolSwitcher } from '../navigation/EnhancedToolSwitcher';
import { WorkflowManager } from '../workflow/WorkflowManager';
import { AdvancedFocusMode } from '../focus/AdvancedFocusMode';
import { CognitiveLoadManager } from '../cognitive/CognitiveLoadManager';
import { useSharedContext } from '../../services/state/optimizedStateManager';
import { usePerformanceMonitor } from '../../services/performance/performanceMonitor';

interface JaneUILayoutProps {
  children: React.ReactNode;
}

interface LayoutMode {
  type: 'normal' | 'focus' | 'deep-work' | 'minimal';
  sidebar: boolean;
  distractions: boolean;
  cognitiveAids: boolean;
}

export function JaneUILayout({ children }: JaneUILayoutProps) {
  const sharedContext = useSharedContext();
  const { markUIInteraction, getCurrentMetrics } = usePerformanceMonitor();
  
  const [layoutMode, setLayoutMode] = useState<LayoutMode>({
    type: 'normal',
    sidebar: true,
    distractions: false,
    cognitiveAids: true
  });
  
  const [showWorkflowManager, setShowWorkflowManager] = useState(false);
  const [showCognitiveManager, setShowCognitiveManager] = useState(false);
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);
  const [adaptiveUI, setAdaptiveUI] = useState(true);

  // Auto-adapt layout based on cognitive load and focus mode
  useEffect(() => {
    if (!adaptiveUI || typeof window === 'undefined') return;

    try {
      const focusMode = sharedContext?.userFocus?.mode || 'normal';
      const metrics = getCurrentMetrics?.() || null;
      
      if (focusMode === 'deep-work' || focusMode === 'flow-state') {
        setLayoutMode({
          type: focusMode,
          sidebar: false,
          distractions: false,
          cognitiveAids: true
        });
      } else if (focusMode === 'focus') {
        setLayoutMode({
          type: 'focus',
          sidebar: true,
          distractions: false,
          cognitiveAids: true
        });
      } else if (metrics?.cognitiveLoad && metrics.cognitiveLoad > 80) {
        // High cognitive load - minimize UI
        setLayoutMode({
          type: 'minimal',
          sidebar: false,
          distractions: false,
          cognitiveAids: true
        });
      } else {
        // Normal mode
        setLayoutMode({
          type: 'normal',
          sidebar: true,
          distractions: false,
          cognitiveAids: true
        });
      }
    } catch (error) {
      console.warn('Layout adaptation error:', error);
      // Fallback to normal mode
      setLayoutMode({
        type: 'normal',
        sidebar: true,
        distractions: false,
        cognitiveAids: true
      });
    }
  }, [sharedContext?.userFocus?.mode, adaptiveUI]);

  // Keyboard shortcuts
  useEffect(() => {
    if (typeof window === 'undefined') return;

    const handleKeyDown = (e: KeyboardEvent) => {
      try {
        // Global shortcuts
        if (e.ctrlKey && e.shiftKey) {
          switch (e.key) {
            case 'W':
              e.preventDefault();
              setShowWorkflowManager(!showWorkflowManager);
              markUIInteraction?.('toggle-workflow-manager');
              break;
            case 'L':
              e.preventDefault();
              setShowCognitiveManager(!showCognitiveManager);
              markUIInteraction?.('toggle-cognitive-manager');
              break;
            case 'S':
              e.preventDefault();
              setSidebarCollapsed(!sidebarCollapsed);
              markUIInteraction?.('toggle-sidebar');
              break;
            case 'A':
              e.preventDefault();
              setAdaptiveUI(!adaptiveUI);
              markUIInteraction?.('toggle-adaptive-ui');
              break;
          }
        }

        // Focus mode shortcuts
        if (e.key === 'F1' && e.shiftKey) {
          e.preventDefault();
          // This will be handled by AdvancedFocusMode component
        }
      } catch (error) {
        console.warn('Keyboard shortcut error:', error);
      }
    };

    document.addEventListener('keydown', handleKeyDown);
    return () => document.removeEventListener('keydown', handleKeyDown);
  }, [showWorkflowManager, showCognitiveManager, sidebarCollapsed, adaptiveUI]);

  const handleFocusModeChange = (mode: 'normal' | 'focus' | 'deep-work', active: boolean) => {
    try {
      markUIInteraction?.('focus-mode-change', { mode, active });
      
      if (!active) {
        // Return to normal layout when focus mode ends
        setLayoutMode({
          type: 'normal',
          sidebar: true,
          distractions: false,
          cognitiveAids: true
        });
      }
    } catch (error) {
      console.warn('Focus mode change error:', error);
    }
  };

  const handleToolSwitch = (fromTool: string | null, toTool: string) => {
    try {
      markUIInteraction?.('layout-tool-switch', { fromTool, toTool });
    } catch (error) {
      console.warn('Tool switch error:', error);
    }
  };

  // Dynamic CSS classes based on layout mode
  const layoutClasses = {
    container: `jane-ui-layout ${layoutMode.type}-mode ${
      layoutMode.sidebar && !sidebarCollapsed ? 'with-sidebar' : 'no-sidebar'
    } ${layoutMode.distractions ? 'with-distractions' : 'minimal-distractions'}`,
    
    sidebar: `transition-all duration-300 ${
      sidebarCollapsed ? 'w-16' : 'w-80'
    } ${!layoutMode.sidebar ? 'hidden' : 'flex'}`,
    
    main: `flex-1 transition-all duration-300 ${
      layoutMode.type === 'minimal' ? 'p-2' : 'p-4'
    }`,
    
    header: `transition-all duration-300 ${
      layoutMode.type === 'deep-work' ? 'h-12' : 'h-16'
    }`
  };

  return (
    <div className={`${layoutClasses.container} min-h-screen bg-gray-50 dark:bg-gray-900`}>
      {/* Global Focus Mode Overlay */}
      <AdvancedFocusMode 
        onModeChange={handleFocusModeChange}
      />

      {/* Header */}
      <header className={`${layoutClasses.header} bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700 flex items-center justify-between px-4 z-40`}>
        {/* Left: Tool Switcher & Navigation Controls */}
        <div className="flex items-center gap-4">
          <EnhancedToolSwitcher 
            onToolSwitch={handleToolSwitch}
            enablePredictive={adaptiveUI}
          />
          
          {layoutMode.sidebar && (
            <button
              onClick={() => setSidebarCollapsed(!sidebarCollapsed)}
              className="p-2 text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200 rounded-md"
              title="Toggle Sidebar (Ctrl+Shift+S)"
            >
              {sidebarCollapsed ? '→' : '←'}
            </button>
          )}
        </div>

        {/* Center: Current Tool & Status */}
        <div className="flex items-center gap-3">
          <div className="text-center">
            <div className="text-sm font-medium text-gray-900 dark:text-white">
              {sharedContext?.userFocus?.currentTool || 'No Tool Selected'}
            </div>
            <div className="text-xs text-gray-500 dark:text-gray-400">
              {layoutMode.type} mode
              {sharedContext?.userFocus?.mode !== 'normal' && (
                <span className="ml-2 px-2 py-1 bg-blue-100 dark:bg-blue-900/30 text-blue-800 dark:text-blue-200 rounded-full">
                  Focus Active
                </span>
              )}
            </div>
          </div>
        </div>

        {/* Right: Controls & Settings */}
        <div className="flex items-center gap-2">
          {/* Workflow Manager Toggle */}
          <button
            onClick={() => setShowWorkflowManager(!showWorkflowManager)}
            className={`p-2 rounded-md transition-colors ${
              showWorkflowManager 
                ? 'bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-300' 
                : 'text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200'
            }`}
            title="Workflow Manager (Ctrl+Shift+W)"
          >
            🔄
          </button>

          {/* Cognitive Load Manager Toggle */}
          <button
            onClick={() => setShowCognitiveManager(!showCognitiveManager)}
            className={`p-2 rounded-md transition-colors ${
              showCognitiveManager 
                ? 'bg-yellow-100 text-yellow-700 dark:bg-yellow-900/30 dark:text-yellow-300' 
                : 'text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200'
            }`}
            title="Cognitive Load Manager (Ctrl+Shift+L)"
          >
            🧠
          </button>

          {/* Adaptive UI Toggle */}
          <button
            onClick={() => setAdaptiveUI(!adaptiveUI)}
            className={`p-2 rounded-md transition-colors ${
              adaptiveUI 
                ? 'bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-300' 
                : 'text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200'
            }`}
            title="Adaptive UI (Ctrl+Shift+A)"
          >
            🎯
          </button>
        </div>
      </header>

      <div className="flex flex-1">
        {/* Sidebar */}
        <aside className={layoutClasses.sidebar}>
          <div className="h-full bg-white dark:bg-gray-800 border-r border-gray-200 dark:border-gray-700 flex flex-col">
            {!sidebarCollapsed && (
              <>
                {/* Navigation */}
                <div className="flex-1 p-4">
                  <EnhancedNavigation />
                </div>

                {/* Workflow Manager Panel */}
                {showWorkflowManager && (
                  <div className="border-t border-gray-200 dark:border-gray-600 p-4">
                    <WorkflowManager className="h-64 overflow-y-auto" />
                  </div>
                )}

                {/* Cognitive Load Manager Panel */}
                {showCognitiveManager && layoutMode.cognitiveAids && (
                  <div className="border-t border-gray-200 dark:border-gray-600 p-4">
                    <CognitiveLoadManager />
                  </div>
                )}
              </>
            )}

            {/* Collapsed Sidebar Icons */}
            {sidebarCollapsed && (
              <div className="flex flex-col items-center gap-4 p-4">
                <button
                  onClick={() => setShowWorkflowManager(!showWorkflowManager)}
                  className="p-3 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700"
                  title="Workflows"
                >
                  🔄
                </button>
                <button
                  onClick={() => setShowCognitiveManager(!showCognitiveManager)}
                  className="p-3 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700"
                  title="Cognitive Load"
                >
                  🧠
                </button>
              </div>
            )}
          </div>
        </aside>

        {/* Main Content Area */}
        <main className={layoutClasses.main}>
          {/* Executive Function Status Bar (only in normal/focus modes) */}
          {layoutMode.cognitiveAids && layoutMode.type !== 'minimal' && layoutMode.type !== 'deep-work' && (
            <div className="mb-4 p-3 bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-700 rounded-lg">
              <div className="flex items-center justify-between text-sm">
                <div className="flex items-center gap-4">
                  <span className="text-blue-800 dark:text-blue-200">
                    Executive Function Status:
                  </span>
                  <div className="flex items-center gap-2">
                    <span className="w-2 h-2 bg-green-500 rounded-full"></span>
                    <span className="text-green-700 dark:text-green-300">Optimal</span>
                  </div>
                </div>
                <div className="flex items-center gap-4 text-xs text-blue-600 dark:text-blue-400">
                  <span>Context Switches: {sharedContext?.userFocus?.contextSwitches || 0}</span>
                  <span>Session: {Math.floor(((Date.now() - (sharedContext?.userFocus?.sessionStart || Date.now())) / 1000 / 60))}m</span>
                </div>
              </div>
            </div>
          )}

          {/* Content */}
          <div className="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 min-h-[calc(100vh-200px)]">
            {children}
          </div>
        </main>
      </div>

      {/* Floating Workflow Manager (when not in sidebar) */}
      {showWorkflowManager && (!layoutMode.sidebar || sidebarCollapsed) && (
        <div className="fixed bottom-4 right-4 w-96 z-50">
          <div className="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 shadow-2xl">
            <div className="p-4 border-b border-gray-200 dark:border-gray-600 flex items-center justify-between">
              <h3 className="font-medium text-gray-900 dark:text-white">
                Workflow Manager
              </h3>
              <button
                onClick={() => setShowWorkflowManager(false)}
                className="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300"
              >
                ×
              </button>
            </div>
            <div className="p-4 max-h-96 overflow-y-auto">
              <WorkflowManager />
            </div>
          </div>
        </div>
      )}

      {/* Floating Cognitive Load Manager (when not in sidebar) */}
      {showCognitiveManager && (!layoutMode.sidebar || sidebarCollapsed) && (
        <div className="fixed bottom-4 left-4 w-80 z-50">
          <div className="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 shadow-2xl">
            <div className="p-4 border-b border-gray-200 dark:border-gray-600 flex items-center justify-between">
              <h3 className="font-medium text-gray-900 dark:text-white">
                Cognitive Load
              </h3>
              <button
                onClick={() => setShowCognitiveManager(false)}
                className="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300"
              >
                ×
              </button>
            </div>
            <div className="p-4">
              <CognitiveLoadManager />
            </div>
          </div>
        </div>
      )}

      {/* Keyboard Shortcuts Help (accessible with F1) */}
      <div className="hidden" id="keyboard-shortcuts">
        <div className="space-y-2 text-sm">
          <div><kbd>Ctrl+Shift+P</kbd> Tool Switcher</div>
          <div><kbd>Ctrl+Shift+W</kbd> Workflow Manager</div>
          <div><kbd>Ctrl+Shift+L</kbd> Cognitive Load Manager</div>
          <div><kbd>Ctrl+Shift+S</kbd> Toggle Sidebar</div>
          <div><kbd>Ctrl+Shift+A</kbd> Toggle Adaptive UI</div>
          <div><kbd>Shift+F1</kbd> Focus Mode</div>
        </div>
      </div>

      {/* CSS Styles for Layout Modes */}
      <style jsx global>{`
        .jane-ui-layout {
          --transition-speed: 300ms;
        }

        .jane-ui-layout.focus-mode {
          --header-opacity: 0.9;
        }

        .jane-ui-layout.deep-work-mode {
          --header-opacity: 0.7;
        }

        .jane-ui-layout.minimal-mode {
          --header-opacity: 1;
        }

        .jane-ui-layout .transition-all {
          transition-property: all;
          transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
          transition-duration: var(--transition-speed);
        }

        /* Focus mode specific styles */
        .jane-ui-layout.focus-mode header {
          opacity: var(--header-opacity);
        }

        .jane-ui-layout.deep-work-mode * {
          animation: none !important;
        }

        /* Executive function friendly animations */
        @media (prefers-reduced-motion: reduce) {
          .jane-ui-layout .transition-all {
            transition: none;
          }
        }

        /* High contrast mode support */
        @media (prefers-contrast: high) {
          .jane-ui-layout {
            --border-width: 2px;
            --focus-ring-width: 3px;
          }
        }
      `}</style>
    </div>
  );
}