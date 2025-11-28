/**
 * Adaptive Navigation Hook
 * Provides cognitive load-aware navigation with smart decision making
 */

import { useCallback, useEffect, useRef, useState } from 'react';
import { useGlobalStore, usePerformance } from '../store';
import {
    NavigationCognitiveState,
    ToolNavigationMetrics,
    navigationCognitiveLoadManager
} from './cognitiveLoadNavigation';

interface AdaptiveNavigationState {
  currentNavState: NavigationCognitiveState | null;
  pendingNavigation: {
    targetTool: string;
    timestamp: number;
    remainingDelay: number;
  } | null;
  navigationWarnings: string[];
  suggestedAlternatives: string[];
  isNavigationBlocked: boolean;
  cognitiveLoadTrend: 'improving' | 'stable' | 'declining';
}

interface AdaptiveNavigationHook {
  // State
  navigationState: AdaptiveNavigationState;
  
  // Actions  
  requestNavigation: (targetTool: string, force?: boolean) => Promise<boolean>;
  cancelPendingNavigation: () => void;
  dismissWarning: (index: number) => void;
  getToolComplexityPreview: (toolId: string) => ToolNavigationMetrics | null;
  
  // Utilities
  canNavigateDirectly: (targetTool: string) => boolean;
  getNavigationDelay: (targetTool: string) => number;
  getNavigationRisk: (targetTool: string) => 'low' | 'medium' | 'high' | 'critical';
}

export function useAdaptiveNavigation(): AdaptiveNavigationHook {
  const { activeTool, setActiveTool, navigationHistory } = useGlobalStore();
  const { cognitiveLoad, contextSwitches } = usePerformance();
  
  const [navigationState, setNavigationState] = useState<AdaptiveNavigationState>({
    currentNavState: null,
    pendingNavigation: null,
    navigationWarnings: [],
    suggestedAlternatives: [],
    isNavigationBlocked: false,
    cognitiveLoadTrend: 'stable'
  });

  const pendingTimeoutRef = useRef<NodeJS.Timeout | null>(null);
  const loadHistoryRef = useRef<Array<{ timestamp: number; load: number }>>([]);

  // Track cognitive load trend
  useEffect(() => {
    loadHistoryRef.current.push({
      timestamp: Date.now(),
      load: cognitiveLoad
    });

    // Keep only last 10 minutes of data
    const tenMinutesAgo = Date.now() - (10 * 60 * 1000);
    loadHistoryRef.current = loadHistoryRef.current.filter(
      entry => entry.timestamp >= tenMinutesAgo
    );

    // Calculate trend
    if (loadHistoryRef.current.length >= 3) {
      const recent = loadHistoryRef.current.slice(-3);
      const trend = recent[2].load - recent[0].load;
      
      setNavigationState(prev => ({
        ...prev,
        cognitiveLoadTrend: trend < -5 ? 'improving' : trend > 5 ? 'declining' : 'stable'
      }));
    }
  }, [cognitiveLoad]);

  // Clean up pending navigation timeout
  useEffect(() => {
    return () => {
      if (pendingTimeoutRef.current) {
        clearTimeout(pendingTimeoutRef.current);
      }
    };
  }, []);

  const requestNavigation = useCallback(async (
    targetTool: string, 
    force: boolean = false
  ): Promise<boolean> => {
    // Don't evaluate same tool
    if (activeTool === targetTool) {
      return true;
    }

    // If forced, bypass cognitive load checks
    if (force) {
      setActiveTool(targetTool);
      return true;
    }

    // Get current fatigue level (simplified calculation)
    const sessionDuration = Date.now() - (Date.now() - (2 * 60 * 60 * 1000)); // Assuming 2h max session
    const fatigueLevel = Math.min(100, (sessionDuration / (1000 * 60 * 60)) * 25); // 25% per hour

    // Evaluate navigation with cognitive load manager
    const navState = navigationCognitiveLoadManager.evaluateNavigation(
      activeTool,
      targetTool,
      cognitiveLoad,
      fatigueLevel,
      contextSwitches
    );

    setNavigationState(prev => ({
      ...prev,
      currentNavState: navState,
      navigationWarnings: navState.shouldWarn ? [
        `Cognitive load is ${navState.riskLevel}. Navigation to ${targetTool} may be challenging.`
      ] : [],
      suggestedAlternatives: navState.alternativeActions.map(alt => alt.description),
      isNavigationBlocked: !navState.canNavigate
    }));

    // Handle navigation based on risk level
    if (!navState.canNavigate) {
      // Navigation blocked - show alternatives
      return false;
    }

    if (navState.suggestedDelay > 0) {
      // Navigation with delay
      return new Promise((resolve) => {
        setNavigationState(prev => ({
          ...prev,
          pendingNavigation: {
            targetTool,
            timestamp: Date.now(),
            remainingDelay: navState.suggestedDelay
          }
        }));

        // Start countdown
        const startTime = Date.now();
        const updateCountdown = () => {
          const elapsed = Date.now() - startTime;
          const remaining = Math.max(0, navState.suggestedDelay - elapsed);
          
          setNavigationState(prev => ({
            ...prev,
            pendingNavigation: prev.pendingNavigation ? {
              ...prev.pendingNavigation,
              remainingDelay: remaining
            } : null
          }));

          if (remaining > 0) {
            requestAnimationFrame(updateCountdown);
          }
        };
        updateCountdown();

        pendingTimeoutRef.current = setTimeout(() => {
          // Record context switch and navigate
          if (activeTool) {
            const currentDomain = getToolDomain(activeTool);
            const targetDomain = getToolDomain(targetTool);
            navigationCognitiveLoadManager.recordContextSwitch(
              activeTool,
              targetTool,
              currentDomain,
              targetDomain
            );
          }

          setActiveTool(targetTool);
          setNavigationState(prev => ({
            ...prev,
            pendingNavigation: null,
            currentNavState: null
          }));
          resolve(true);
        }, navState.suggestedDelay);
      });
    } else {
      // Immediate navigation
      if (activeTool) {
        const currentDomain = getToolDomain(activeTool);
        const targetDomain = getToolDomain(targetTool);
        navigationCognitiveLoadManager.recordContextSwitch(
          activeTool,
          targetTool,
          currentDomain,
          targetDomain
        );
      }

      setActiveTool(targetTool);
      return true;
    }
  }, [activeTool, cognitiveLoad, contextSwitches, setActiveTool]);

  const cancelPendingNavigation = useCallback(() => {
    if (pendingTimeoutRef.current) {
      clearTimeout(pendingTimeoutRef.current);
      pendingTimeoutRef.current = null;
    }

    setNavigationState(prev => ({
      ...prev,
      pendingNavigation: null,
      currentNavState: null,
      navigationWarnings: [],
      suggestedAlternatives: []
    }));
  }, []);

  const dismissWarning = useCallback((index: number) => {
    setNavigationState(prev => ({
      ...prev,
      navigationWarnings: prev.navigationWarnings.filter((_, i) => i !== index)
    }));
  }, []);

  const getToolComplexityPreview = useCallback((toolId: string): ToolNavigationMetrics | null => {
    return navigationCognitiveLoadManager.getToolComplexityInfo(toolId);
  }, []);

  const canNavigateDirectly = useCallback((targetTool: string): boolean => {
    if (activeTool === targetTool) return true;

    const fatigueLevel = Math.min(100, (Date.now() / (1000 * 60 * 60)) * 25);
    const navState = navigationCognitiveLoadManager.evaluateNavigation(
      activeTool,
      targetTool,
      cognitiveLoad,
      fatigueLevel,
      contextSwitches
    );

    return navState.canNavigate && navState.suggestedDelay === 0;
  }, [activeTool, cognitiveLoad, contextSwitches]);

  const getNavigationDelay = useCallback((targetTool: string): number => {
    if (activeTool === targetTool) return 0;

    const fatigueLevel = Math.min(100, (Date.now() / (1000 * 60 * 60)) * 25);
    const navState = navigationCognitiveLoadManager.evaluateNavigation(
      activeTool,
      targetTool,
      cognitiveLoad,
      fatigueLevel,
      contextSwitches
    );

    return navState.suggestedDelay;
  }, [activeTool, cognitiveLoad, contextSwitches]);

  const getNavigationRisk = useCallback((targetTool: string): 'low' | 'medium' | 'high' | 'critical' => {
    if (activeTool === targetTool) return 'low';

    const fatigueLevel = Math.min(100, (Date.now() / (1000 * 60 * 60)) * 25);
    const navState = navigationCognitiveLoadManager.evaluateNavigation(
      activeTool,
      targetTool,
      cognitiveLoad,
      fatigueLevel,
      contextSwitches
    );

    return navState.riskLevel;
  }, [activeTool, cognitiveLoad, contextSwitches]);

  return {
    navigationState,
    requestNavigation,
    cancelPendingNavigation,
    dismissWarning,
    getToolComplexityPreview,
    canNavigateDirectly,
    getNavigationDelay,
    getNavigationRisk
  };
}

// Helper function to get domain from tool ID
function getToolDomain(toolId: string): 'security' | 'productivity' | 'mtg' | 'infrastructure' {
  // Security tools
  if (['misp', 'helk', 'securityonion', 'cyberchef', 'maltrail', 'nemesis', 'yara-x'].includes(toolId)) {
    return 'security';
  }
  
  // Productivity tools
  if (['n8n', 'mealie', 'dispatch', 'actual-budget', 'firecrawl', 'goose', 'it-tools', 'inspector'].includes(toolId)) {
    return 'productivity';
  }
  
  // MTG tools
  if (['commander-spellbook', 'mtg-scripting', 'mtg-commander-map', 'card-analysis'].includes(toolId)) {
    return 'mtg';
  }
  
  // Infrastructure tools (default)
  return 'infrastructure';
}