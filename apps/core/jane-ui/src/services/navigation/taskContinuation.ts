/**
 * Navigation-Aware Task Continuation Service
 * Preserves work context across tool switches to minimize cognitive rebuilding overhead
 */

import { useCallback, useEffect, useRef, useState } from 'react';
import { useGlobalStore, usePerformance } from '../../services/store';
import { useExecutiveFunctionPreferences } from './executiveFunctionPreferences';

export interface TaskContext {
  id: string;
  toolId: string;
  taskType: 'analysis' | 'creation' | 'modification' | 'review' | 'research' | 'planning';
  title: string;
  description?: string;
  
  // Context preservation data
  workingData: Record<string, any>;        // Tool-specific data
  activeSelection?: string;                // Current selection/focus
  scrollPosition?: { x: number; y: number }; // UI scroll state
  inputStates: Record<string, any>;        // Form inputs, filters, etc.
  navigationPath: string[];                // Where user navigated within tool
  
  // Cognitive context
  cognitiveLoad: number;                   // Load when context was saved
  focusDepth: 'surface' | 'moderate' | 'deep'; // How engaged user was
  sessionDuration: number;                 // How long user worked on this
  lastInteraction: Date;                   // When context was last updated
  
  // Collaboration context
  sharedWith?: string[];                   // Other users involved
  dependencies: string[];                  // Related tasks/contexts
  blockers: string[];                      // What's preventing progress
  
  // Recovery metadata
  saveReason: 'switch' | 'break' | 'interruption' | 'manual' | 'auto';
  confidence: number;                      // 0-100, how complete this context is
  expiresAt: Date;                        // When this context should be cleaned up
}

export interface TaskContinuation {
  context: TaskContext;
  resumptionStrategy: 'immediate' | 'guided' | 'gradual' | 'manual';
  estimatedReloadTime: number;             // seconds to get back to this state
  cognitiveReloadCost: number;            // 0-100, mental effort to resume
  recommendations: Array<{
    type: 'action' | 'reminder' | 'preparation';
    message: string;
    priority: 'low' | 'medium' | 'high';
  }>;
}

export interface ContextualMemory {
  shortTerm: TaskContext[];                // Last 5-10 contexts
  workingMemory: TaskContext[];           // Currently active contexts
  longTerm: Array<{                       // Patterns and frequent contexts
    pattern: string;
    contexts: TaskContext[];
    frequency: number;
    lastUsed: Date;
  }>;
}

/**
 * Task Continuation Service
 * Manages context preservation and intelligent task resumption
 */
export class TaskContinuationService {
  private contextualMemory: ContextualMemory = {
    shortTerm: [],
    workingMemory: [],
    longTerm: []
  };
  
  private contextSaveInterval: NodeJS.Timeout | null = null;
  private readonly MAX_SHORT_TERM = 10;
  private readonly MAX_WORKING_MEMORY = 5;
  private readonly CONTEXT_EXPIRY_HOURS = 24;

  constructor(
    private getUserPreferences: () => any,
    private onContextUpdate?: (contexts: TaskContext[]) => void
  ) {
    this.startAutoSave();
    this.loadPersistedContexts();
  }

  /**
   * Save current task context when switching tools
   */
  saveTaskContext(
    toolId: string,
    contextData: Partial<TaskContext>,
    saveReason: TaskContext['saveReason'] = 'switch'
  ): string {
    const contextId = `ctx_${toolId}_${Date.now()}`;
    const preferences = this.getUserPreferences();
    
    const context: TaskContext = {
      id: contextId,
      toolId,
      taskType: contextData.taskType || 'analysis',
      title: contextData.title || `Work in ${toolId}`,
      description: contextData.description,
      workingData: contextData.workingData || {},
      activeSelection: contextData.activeSelection,
      scrollPosition: contextData.scrollPosition,
      inputStates: contextData.inputStates || {},
      navigationPath: contextData.navigationPath || [],
      cognitiveLoad: contextData.cognitiveLoad || 50,
      focusDepth: this.calculateFocusDepth(contextData.sessionDuration || 0, contextData.cognitiveLoad || 50),
      sessionDuration: contextData.sessionDuration || 0,
      lastInteraction: new Date(),
      sharedWith: contextData.sharedWith,
      dependencies: contextData.dependencies || [],
      blockers: contextData.blockers || [],
      saveReason,
      confidence: this.calculateContextConfidence(contextData),
      expiresAt: new Date(Date.now() + this.CONTEXT_EXPIRY_HOURS * 60 * 60 * 1000)
    };

    // Add to working memory
    this.contextualMemory.workingMemory = this.contextualMemory.workingMemory
      .filter(ctx => ctx.toolId !== toolId) // Remove old context for same tool
      .concat(context)
      .slice(-this.MAX_WORKING_MEMORY);

    // Add to short-term memory
    this.contextualMemory.shortTerm = [context, ...this.contextualMemory.shortTerm]
      .slice(0, this.MAX_SHORT_TERM);

    this.persistContexts();
    this.onContextUpdate?.(this.contextualMemory.workingMemory);

    return contextId;
  }

  /**
   * Retrieve task context for resumption
   */
  getTaskContext(toolId: string): TaskContext | null {
    // Check working memory first
    const workingContext = this.contextualMemory.workingMemory
      .find(ctx => ctx.toolId === toolId && !this.isExpired(ctx));
    
    if (workingContext) return workingContext;

    // Check short-term memory
    const shortTermContext = this.contextualMemory.shortTerm
      .find(ctx => ctx.toolId === toolId && !this.isExpired(ctx));
    
    return shortTermContext || null;
  }

  /**
   * Generate continuation strategy for resuming work
   */
  generateContinuationStrategy(toolId: string): TaskContinuation | null {
    const context = this.getTaskContext(toolId);
    if (!context) return null;

    const timeSinceLastUse = Date.now() - context.lastInteraction.getTime();
    const preferences = this.getUserPreferences();
    
    // Calculate cognitive reload cost
    const cognitiveReloadCost = this.calculateReloadCost(context, timeSinceLastUse);
    
    // Determine resumption strategy
    const resumptionStrategy = this.determineResumptionStrategy(
      context, 
      cognitiveReloadCost, 
      preferences
    );
    
    // Estimate time to reload context
    const estimatedReloadTime = this.estimateReloadTime(context, resumptionStrategy);
    
    // Generate recommendations
    const recommendations = this.generateResumptionRecommendations(context, resumptionStrategy);

    return {
      context,
      resumptionStrategy,
      estimatedReloadTime,
      cognitiveReloadCost,
      recommendations
    };
  }

  /**
   * Update context with new information (auto-save)
   */
  updateTaskContext(toolId: string, updates: Partial<TaskContext>): void {
    const existingIndex = this.contextualMemory.workingMemory
      .findIndex(ctx => ctx.toolId === toolId);

    if (existingIndex >= 0) {
      this.contextualMemory.workingMemory[existingIndex] = {
        ...this.contextualMemory.workingMemory[existingIndex],
        ...updates,
        lastInteraction: new Date()
      };
      
      this.onContextUpdate?.(this.contextualMemory.workingMemory);
    }
  }

  /**
   * Clear expired contexts
   */
  cleanupExpiredContexts(): void {
    const now = Date.now();
    
    this.contextualMemory.workingMemory = this.contextualMemory.workingMemory
      .filter(ctx => !this.isExpired(ctx));
      
    this.contextualMemory.shortTerm = this.contextualMemory.shortTerm
      .filter(ctx => !this.isExpired(ctx));
      
    this.persistContexts();
  }

  /**
   * Get all active contexts for display
   */
  getActiveContexts(): TaskContext[] {
    return this.contextualMemory.workingMemory
      .filter(ctx => !this.isExpired(ctx))
      .sort((a, b) => b.lastInteraction.getTime() - a.lastInteraction.getTime());
  }

  /**
   * Get context history for a tool
   */
  getToolHistory(toolId: string, limit: number = 5): TaskContext[] {
    return this.contextualMemory.shortTerm
      .filter(ctx => ctx.toolId === toolId && !this.isExpired(ctx))
      .slice(0, limit);
  }

  /**
   * Find related contexts based on dependencies or patterns
   */
  findRelatedContexts(contextId: string): TaskContext[] {
    const context = this.contextualMemory.workingMemory
      .find(ctx => ctx.id === contextId) || 
      this.contextualMemory.shortTerm
        .find(ctx => ctx.id === contextId);
        
    if (!context) return [];

    // Find contexts with shared dependencies
    const relatedByDependency = this.contextualMemory.workingMemory
      .filter(ctx => 
        ctx.id !== contextId &&
        (ctx.dependencies?.some(dep => context.dependencies?.includes(dep)) ||
         context.dependencies?.includes(ctx.id) ||
         ctx.dependencies?.includes(context.id))
      );

    // Find contexts from similar time periods (working sessions)
    const sessionWindow = 30 * 60 * 1000; // 30 minutes
    const relatedBySession = this.contextualMemory.shortTerm
      .filter(ctx => 
        ctx.id !== contextId &&
        Math.abs(ctx.lastInteraction.getTime() - context.lastInteraction.getTime()) < sessionWindow
      );

    return [...relatedByDependency, ...relatedBySession]
      .reduce((unique, ctx) => {
        if (!unique.find(u => u.id === ctx.id)) {
          unique.push(ctx);
        }
        return unique;
      }, [] as TaskContext[])
      .slice(0, 5);
  }

  private calculateFocusDepth(sessionDuration: number, cognitiveLoad: number): TaskContext['focusDepth'] {
    if (sessionDuration > 45 && cognitiveLoad > 70) return 'deep';
    if (sessionDuration > 15 && cognitiveLoad > 50) return 'moderate';
    return 'surface';
  }

  private calculateContextConfidence(contextData: Partial<TaskContext>): number {
    let confidence = 50;
    
    // Boost confidence based on available data
    if (contextData.workingData && Object.keys(contextData.workingData).length > 0) confidence += 20;
    if (contextData.activeSelection) confidence += 10;
    if (contextData.inputStates && Object.keys(contextData.inputStates).length > 0) confidence += 15;
    if (contextData.navigationPath && contextData.navigationPath.length > 0) confidence += 10;
    if (contextData.sessionDuration && contextData.sessionDuration > 300) confidence += 15; // 5+ minutes
    
    return Math.min(100, confidence);
  }

  private calculateReloadCost(context: TaskContext, timeSinceLastUse: number): number {
    const baseReloadCost = 30;
    
    // Time decay - longer since last use = higher cost
    const timePenalty = Math.min(40, (timeSinceLastUse / (1000 * 60 * 60)) * 10); // 10 points per hour
    
    // Complexity penalty - deeper focus requires more effort to resume
    const focusPenalty = context.focusDepth === 'deep' ? 20 : context.focusDepth === 'moderate' ? 10 : 0;
    
    // Confidence penalty - incomplete context is harder to resume
    const confidencePenalty = (100 - context.confidence) * 0.2;
    
    return Math.min(100, baseReloadCost + timePenalty + focusPenalty + confidencePenalty);
  }

  private determineResumptionStrategy(
    context: TaskContext, 
    reloadCost: number, 
    preferences: any
  ): TaskContinuation['resumptionStrategy'] {
    const executiveFunctionChallenges = preferences?.executiveFunctionProfile?.workingMemoryChallenges || 5;
    
    // High reload cost or executive function challenges = need more support
    if (reloadCost > 70 || executiveFunctionChallenges > 7) return 'guided';
    if (reloadCost > 50 || executiveFunctionChallenges > 5) return 'gradual';
    if (reloadCost > 30) return 'immediate';
    
    return 'immediate';
  }

  private estimateReloadTime(context: TaskContext, strategy: TaskContinuation['resumptionStrategy']): number {
    const baseTime = 10; // 10 seconds minimum
    
    const strategyMultipliers = {
      immediate: 1,
      gradual: 1.5,
      guided: 2,
      manual: 3
    };
    
    const focusMultipliers = {
      surface: 1,
      moderate: 1.3,
      deep: 1.8
    };
    
    return Math.round(
      baseTime * 
      strategyMultipliers[strategy] * 
      focusMultipliers[context.focusDepth] *
      (1 + (100 - context.confidence) / 200)
    );
  }

  private generateResumptionRecommendations(
    context: TaskContext, 
    strategy: TaskContinuation['resumptionStrategy']
  ): TaskContinuation['recommendations'] {
    const recommendations: TaskContinuation['recommendations'] = [];

    // Context-specific preparation
    if (context.focusDepth === 'deep') {
      recommendations.push({
        type: 'preparation',
        message: 'You were in deep focus. Take a moment to recall your mental model.',
        priority: 'high'
      });
    }

    if (context.blockers.length > 0) {
      recommendations.push({
        type: 'reminder',
        message: `Remember: ${context.blockers.length} blocker(s) were preventing progress.`,
        priority: 'high'
      });
    }

    if (context.activeSelection) {
      recommendations.push({
        type: 'action',
        message: `Resume at: ${context.activeSelection}`,
        priority: 'medium'
      });
    }

    // Strategy-specific recommendations
    if (strategy === 'guided') {
      recommendations.push({
        type: 'action',
        message: 'Review context summary before diving back in.',
        priority: 'high'
      });
    }

    if (strategy === 'gradual') {
      recommendations.push({
        type: 'action',
        message: 'Start with light review before resuming active work.',
        priority: 'medium'
      });
    }

    return recommendations;
  }

  private isExpired(context: TaskContext): boolean {
    return Date.now() > context.expiresAt.getTime();
  }

  private startAutoSave(): void {
    // Auto-save working contexts every 30 seconds
    this.contextSaveInterval = setInterval(() => {
      this.persistContexts();
      this.cleanupExpiredContexts();
    }, 30000);
  }

  private persistContexts(): void {
    try {
      localStorage.setItem('task-contexts', JSON.stringify({
        ...this.contextualMemory,
        shortTerm: this.contextualMemory.shortTerm.map(ctx => ({
          ...ctx,
          lastInteraction: ctx.lastInteraction.toISOString(),
          expiresAt: ctx.expiresAt.toISOString()
        })),
        workingMemory: this.contextualMemory.workingMemory.map(ctx => ({
          ...ctx,
          lastInteraction: ctx.lastInteraction.toISOString(),
          expiresAt: ctx.expiresAt.toISOString()
        }))
      }));
    } catch (error) {
      console.warn('Failed to persist task contexts:', error);
    }
  }

  private loadPersistedContexts(): void {
    try {
      const saved = localStorage.getItem('task-contexts');
      if (saved) {
        const parsed = JSON.parse(saved);
        
        this.contextualMemory = {
          shortTerm: parsed.shortTerm?.map((ctx: any) => ({
            ...ctx,
            lastInteraction: new Date(ctx.lastInteraction),
            expiresAt: new Date(ctx.expiresAt)
          })) || [],
          workingMemory: parsed.workingMemory?.map((ctx: any) => ({
            ...ctx,
            lastInteraction: new Date(ctx.lastInteraction),
            expiresAt: new Date(ctx.expiresAt)
          })) || [],
          longTerm: parsed.longTerm || []
        };
        
        this.cleanupExpiredContexts();
      }
    } catch (error) {
      console.warn('Failed to load persisted task contexts:', error);
    }
  }

  destroy(): void {
    if (this.contextSaveInterval) {
      clearInterval(this.contextSaveInterval);
    }
  }
}

/**
 * React Hook for Task Continuation
 */
export function useTaskContinuation() {
  const { userPreferences } = useGlobalStore();
  const { currentPreferences } = useExecutiveFunctionPreferences();
  const { performanceMetrics } = usePerformance();
  
  const serviceRef = useRef<TaskContinuationService | null>(null);
  const [activeContexts, setActiveContexts] = useState<TaskContext[]>([]);
  const [currentToolContext, setCurrentToolContext] = useState<TaskContext | null>(null);

  // Initialize service
  useEffect(() => {
    if (!serviceRef.current) {
      serviceRef.current = new TaskContinuationService(
        () => ({ 
          executiveFunctionProfile: userPreferences?.executiveFunctionProfile,
          navigationPreferences: currentPreferences
        }),
        setActiveContexts
      );
    }

    return () => {
      serviceRef.current?.destroy();
    };
  }, [userPreferences, currentPreferences]);

  // Save context when switching tools
  const saveCurrentContext = useCallback((
    toolId: string, 
    contextData: Partial<TaskContext>,
    saveReason: TaskContext['saveReason'] = 'switch'
  ) => {
    if (!serviceRef.current) return null;
    
    return serviceRef.current.saveTaskContext(toolId, contextData, saveReason);
  }, []);

  // Get continuation strategy for a tool
  const getContinuationStrategy = useCallback((toolId: string): TaskContinuation | null => {
    if (!serviceRef.current) return null;
    
    return serviceRef.current.generateContinuationStrategy(toolId);
  }, []);

  // Update current context (auto-save)
  const updateContext = useCallback((toolId: string, updates: Partial<TaskContext>) => {
    if (!serviceRef.current) return;
    
    serviceRef.current.updateTaskContext(toolId, updates);
  }, []);

  // Get tool history
  const getToolHistory = useCallback((toolId: string, limit?: number) => {
    if (!serviceRef.current) return [];
    
    return serviceRef.current.getToolHistory(toolId, limit);
  }, []);

  // Find related contexts
  const findRelatedContexts = useCallback((contextId: string) => {
    if (!serviceRef.current) return [];
    
    return serviceRef.current.findRelatedContexts(contextId);
  }, []);

  return {
    activeContexts,
    currentToolContext,
    saveCurrentContext,
    getContinuationStrategy,
    updateContext,
    getToolHistory,
    findRelatedContexts,
    
    // Convenience methods
    hasContext: (toolId: string) => activeContexts.some(ctx => ctx.toolId === toolId),
    getRecentContexts: () => activeContexts.slice(0, 5)
  };
}