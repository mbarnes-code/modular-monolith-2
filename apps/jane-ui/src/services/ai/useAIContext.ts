'use client';

import { useCallback, useEffect, useState } from 'react';
import { useCrossToolContext, type ContextSuggestion, type ToolContext } from './crossToolContext';

interface AIContextHookProps {
  activeTool?: string;
  activeContext?: string[];
  autoRefresh?: boolean;
  refreshInterval?: number;
}

interface AIContextState {
  suggestions: ContextSuggestion[];
  isLoading: boolean;
  error: string | null;
  lastUpdated: Date | null;
}

export function useAIContext({
  activeTool,
  activeContext = [],
  autoRefresh = true,
  refreshInterval = 30000 // 30 seconds
}: AIContextHookProps = {}) {
  const [state, setState] = useState<AIContextState>({
    suggestions: [],
    isLoading: false,
    error: null,
    lastUpdated: null
  });

  const {
    registerContext,
    getContext,
    getSuggestions,
    updateBehaviorPattern,
    getDomainPerformance
  } = useCrossToolContext(activeTool);

  // Update tool context when active tool or context changes
  useEffect(() => {
    if (activeTool) {
      const toolContext: Partial<ToolContext> = {
        currentState: {
          activeContext: activeContext,
          timestamp: Date.now(),
          contextItems: activeContext.length
        },
        recentActions: [
          'context_updated',
          `switched_to_${activeTool}`,
          'ui_interaction'
        ]
      };

      registerContext(activeTool, toolContext);
    }
  }, [activeTool, activeContext, registerContext]);

  // Refresh suggestions
  const refreshSuggestions = useCallback(async () => {
    if (!activeTool) {
      setState(prev => ({ ...prev, suggestions: [] }));
      return;
    }

    setState(prev => ({ ...prev, isLoading: true, error: null }));

    try {
      // Simulate API call delay for realistic behavior
      await new Promise(resolve => setTimeout(resolve, 500));
      
      const suggestions = getSuggestions(activeTool, 5);
      
      setState(prev => ({
        ...prev,
        suggestions,
        isLoading: false,
        lastUpdated: new Date()
      }));
    } catch (error) {
      setState(prev => ({
        ...prev,
        isLoading: false,
        error: error instanceof Error ? error.message : 'Failed to load suggestions'
      }));
    }
  }, [activeTool, getSuggestions]);

  // Auto-refresh suggestions
  useEffect(() => {
    refreshSuggestions();

    if (autoRefresh && refreshInterval > 0) {
      const interval = setInterval(refreshSuggestions, refreshInterval);
      return () => clearInterval(interval);
    }
  }, [refreshSuggestions, autoRefresh, refreshInterval]);

  // Apply suggestion and update behavior patterns
  const applySuggestion = useCallback((suggestion: ContextSuggestion) => {
    if (!activeTool) return;

    // Update behavior pattern for learning
    updateBehaviorPattern(`${activeTool}:${suggestion.type}:applied`, 1);
    updateBehaviorPattern(`global:suggestion_applied`, 0.5);

    // Remove applied suggestion from list
    setState(prev => ({
      ...prev,
      suggestions: prev.suggestions.filter(s => s.id !== suggestion.id)
    }));

    // Update tool context with applied suggestion
    const toolContext: Partial<ToolContext> = {
      currentState: {
        lastAppliedSuggestion: suggestion.id,
        suggestionType: suggestion.type,
        appliedAt: Date.now()
      },
      recentActions: [
        `applied_suggestion:${suggestion.type}`,
        'user_interaction',
        'suggestion_applied'
      ]
    };

    registerContext(activeTool, toolContext);

    return suggestion;
  }, [activeTool, updateBehaviorPattern, registerContext]);

  // Dismiss suggestion and update behavior patterns
  const dismissSuggestion = useCallback((suggestion: ContextSuggestion) => {
    if (!activeTool) return;

    // Update behavior pattern for learning (negative feedback)
    updateBehaviorPattern(`${activeTool}:${suggestion.type}:dismissed`, 1);
    updateBehaviorPattern(`global:suggestion_dismissed`, 0.5);

    // Remove dismissed suggestion from list
    setState(prev => ({
      ...prev,
      suggestions: prev.suggestions.filter(s => s.id !== suggestion.id)
    }));

    return suggestion;
  }, [activeTool, updateBehaviorPattern]);

  // Get current cross-tool context
  const getCurrentContext = useCallback(() => {
    if (!activeTool) return null;
    return getContext(activeTool);
  }, [activeTool, getContext]);

  // Get domain-specific performance information
  const getDomainInfo = useCallback(() => {
    if (!activeTool) return null;
    
    // Determine domain from tool
    const domain = getDomainForTool(activeTool);
    return getDomainPerformance(domain);
  }, [activeTool, getDomainPerformance]);

  // Helper function to get domain from tool name
  const getDomainForTool = (toolName: string): string => {
    const securityTools = ['MISP', 'HELK', 'SecurityOnion', 'YARA-X', 'CyberChef', 'Nemesis', 'Maltrail'];
    const productivityTools = ['n8n', 'Mealie', 'Dispatch', 'Actual Budget', 'Firecrawl', 'Goose', 'IT-Tools', 'Inspector'];
    const mtgTools = ['Commander Spellbook', 'MTG Commander Map', 'MTG Scripting Toolkit'];
    const infrastructureTools = ['Kong', 'Ghostwriter', 'KasmVNC'];

    if (securityTools.includes(toolName)) return 'security';
    if (productivityTools.includes(toolName)) return 'productivity';  
    if (mtgTools.includes(toolName)) return 'mtg';
    if (infrastructureTools.includes(toolName)) return 'infrastructure';
    return 'productivity'; // Default
  };

  // Filter suggestions by type
  const getSuggestionsByType = useCallback((type: string) => {
    return state.suggestions.filter(s => s.type === type);
  }, [state.suggestions]);

  // Get high-priority suggestions
  const getHighPrioritySuggestions = useCallback(() => {
    return state.suggestions.filter(s => s.confidence > 0.8);
  }, [state.suggestions]);

  // Get suggestions for specific tools
  const getSuggestionsForTool = useCallback((toolName: string) => {
    return state.suggestions.filter(s => s.involvedTools.includes(toolName));
  }, [state.suggestions]);

  return {
    // State
    ...state,
    
    // Actions
    refreshSuggestions,
    applySuggestion,
    dismissSuggestion,
    
    // Context
    getCurrentContext,
    getDomainInfo,
    
    // Filtered data
    getSuggestionsByType,
    getHighPrioritySuggestions,
    getSuggestionsForTool,
    
    // Metadata
    activeTool,
    activeContext,
    hasActiveTool: !!activeTool,
    suggestionCount: state.suggestions.length,
    highPriorityCount: state.suggestions.filter(s => s.confidence > 0.8).length
  };
}

export type { AIContextHookProps, AIContextState };
