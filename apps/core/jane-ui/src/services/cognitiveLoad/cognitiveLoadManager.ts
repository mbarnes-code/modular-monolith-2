/**
 * Cognitive Load Management System for Jane-UI Mental Prosthetic Platform
 * Executive function accommodations and ADHD-friendly navigation
 * 
 * Features:
 * - Context switching management
 * - Active tool limitation (max 5 tools)
 * - Task breakdown workflows
 * - Focus mode implementation
 * - Progress tracking and time estimates
 */

import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import { usePerformanceMonitor } from '../performance/performanceMonitor';

// Executive function accommodation settings
export const COGNITIVE_LOAD_CONFIG = {
  maxActiveTools: 5, // Reduce cognitive load
  contextSwitchDelay: 300, // ms - prevent rapid switching
  focusModeTimeout: 25 * 60 * 1000, // 25 minutes (Pomodoro)
  taskBreakdownThreshold: 3, // Break down tasks with >3 steps
  progressUpdateInterval: 5000, // 5 seconds
  quickSwitchHistorySize: 3, // Recently used tools
} as const;

// Tool usage context for cognitive load management
export interface ToolContext {
  id: string;
  name: string;
  domain: string;
  lastAccessed: Date;
  sessionDuration: number;
  taskProgress: number; // 0-100
  isInFocus: boolean;
  estimatedTimeRemaining?: number;
}

// Cognitive load state management
interface CognitiveLoadState {
  // Active tool management
  activeTools: Map<string, ToolContext>;
  focusedTool: string | null;
  quickSwitchHistory: string[];
  
  // Executive function features
  focusModeActive: boolean;
  focusModeStartTime: Date | null;
  taskBreakdownActive: boolean;
  currentTaskSteps: string[];
  completedSteps: number;
  
  // Context switching management
  lastContextSwitch: Date | null;
  contextSwitchCount: number;
  sessionStartTime: Date;
  
  // Actions
  activateTool: (toolId: string, toolName: string, domain: string) => void;
  deactivateTool: (toolId: string) => void;
  switchToTool: (toolId: string) => Promise<boolean>;
  enterFocusMode: (toolId: string) => void;
  exitFocusMode: () => void;
  updateTaskProgress: (toolId: string, progress: number) => void;
  breakdownTask: (steps: string[]) => void;
  completeTaskStep: () => void;
  getCognitiveLoadScore: () => number;
  getContextSwitchRate: () => number;
  canActivateNewTool: () => boolean;
}

// Zustand store for cognitive load management
export const useCognitiveLoadStore = create<CognitiveLoadState>()(persist(
  (set, get) => ({
    // Initial state
    activeTools: new Map(),
    focusedTool: null,
    quickSwitchHistory: [],
    focusModeActive: false,
    focusModeStartTime: null,
    taskBreakdownActive: false,
    currentTaskSteps: [],
    completedSteps: 0,
    lastContextSwitch: null,
    contextSwitchCount: 0,
    sessionStartTime: new Date(),

    // Activate a new tool with cognitive load checks
    activateTool: (toolId: string, toolName: string, domain: string) => {
      const state = get();
      
      // Check if we can activate a new tool
      if (!state.canActivateNewTool() && !state.activeTools.has(toolId)) {
        console.warn('🧠 Cognitive load limit reached. Consider closing other tools first.');
        return;
      }

      const now = new Date();
      const toolContext: ToolContext = {
        id: toolId,
        name: toolName,
        domain,
        lastAccessed: now,
        sessionDuration: 0,
        taskProgress: 0,
        isInFocus: false,
      };

      set((state) => {
        const newActiveTools = new Map(state.activeTools);
        newActiveTools.set(toolId, toolContext);
        
        // Update quick switch history
        const newHistory = [toolId, ...state.quickSwitchHistory.filter(id => id !== toolId)]
          .slice(0, COGNITIVE_LOAD_CONFIG.quickSwitchHistorySize);

        return {
          activeTools: newActiveTools,
          quickSwitchHistory: newHistory,
          lastContextSwitch: now,
          contextSwitchCount: state.contextSwitchCount + 1,
        };
      });
    },

    // Deactivate a tool and clean up context
    deactivateTool: (toolId: string) => {
      set((state) => {
        const newActiveTools = new Map(state.activeTools);
        newActiveTools.delete(toolId);
        
        const newFocusedTool = state.focusedTool === toolId ? null : state.focusedTool;
        const shouldExitFocusMode = state.focusModeActive && state.focusedTool === toolId;

        return {
          activeTools: newActiveTools,
          focusedTool: newFocusedTool,
          focusModeActive: shouldExitFocusMode ? false : state.focusModeActive,
          focusModeStartTime: shouldExitFocusMode ? null : state.focusModeStartTime,
        };
      });
    },

    // Context-aware tool switching with delays
    switchToTool: async (toolId: string): Promise<boolean> => {
      const state = get();
      const now = new Date();
      
      // Prevent rapid context switching
      if (state.lastContextSwitch && 
          (now.getTime() - state.lastContextSwitch.getTime()) < COGNITIVE_LOAD_CONFIG.contextSwitchDelay) {
        console.log('🧠 Context switch too rapid. Please wait a moment.');
        return false;
      }

      // Check if tool is already active
      if (!state.activeTools.has(toolId)) {
        console.warn(`🧠 Tool ${toolId} is not active. Activate it first.`);
        return false;
      }

      // Update tool context
      set((state) => {
        const newActiveTools = new Map(state.activeTools);
        const toolContext = newActiveTools.get(toolId);
        if (toolContext) {
          toolContext.lastAccessed = now;
          toolContext.isInFocus = true;
          newActiveTools.set(toolId, toolContext);
        }

        // Clear focus from other tools
        for (const [id, context] of newActiveTools) {
          if (id !== toolId) {
            context.isInFocus = false;
          }
        }

        return {
          activeTools: newActiveTools,
          focusedTool: toolId,
          lastContextSwitch: now,
          contextSwitchCount: state.contextSwitchCount + 1,
        };
      });

      return true;
    },

    // Enter focus mode for deep work
    enterFocusMode: (toolId: string) => {
      const state = get();
      
      if (!state.activeTools.has(toolId)) {
        console.warn(`🧠 Cannot enter focus mode: tool ${toolId} is not active.`);
        return;
      }

      set({
        focusModeActive: true,
        focusModeStartTime: new Date(),
        focusedTool: toolId,
      });

      // Set timer to automatically exit focus mode
      setTimeout(() => {
        const currentState = get();
        if (currentState.focusModeActive) {
          currentState.exitFocusMode();
        }
      }, COGNITIVE_LOAD_CONFIG.focusModeTimeout);
    },

    // Exit focus mode
    exitFocusMode: () => {
      set({
        focusModeActive: false,
        focusModeStartTime: null,
      });
    },

    // Update task progress for a tool
    updateTaskProgress: (toolId: string, progress: number) => {
      set((state) => {
        const newActiveTools = new Map(state.activeTools);
        const toolContext = newActiveTools.get(toolId);
        if (toolContext) {
          toolContext.taskProgress = Math.max(0, Math.min(100, progress));
          newActiveTools.set(toolId, toolContext);
        }
        return { activeTools: newActiveTools };
      });
    },

    // Break down complex tasks into manageable steps
    breakdownTask: (steps: string[]) => {
      if (steps.length > COGNITIVE_LOAD_CONFIG.taskBreakdownThreshold) {
        set({
          taskBreakdownActive: true,
          currentTaskSteps: steps,
          completedSteps: 0,
        });
      }
    },

    // Complete a task step
    completeTaskStep: () => {
      set((state) => {
        const newCompletedSteps = state.completedSteps + 1;
        const isTaskComplete = newCompletedSteps >= state.currentTaskSteps.length;
        
        return {
          completedSteps: newCompletedSteps,
          taskBreakdownActive: isTaskComplete ? false : state.taskBreakdownActive,
          currentTaskSteps: isTaskComplete ? [] : state.currentTaskSteps,
        };
      });
    },

    // Calculate cognitive load score (0-100)
    getCognitiveLoadScore: (): number => {
      const state = get();
      const activeToolCount = state.activeTools.size;
      const baseLoad = (activeToolCount / COGNITIVE_LOAD_CONFIG.maxActiveTools) * 70;
      
      // Add penalties for context switching
      const sessionDuration = (new Date().getTime() - state.sessionStartTime.getTime()) / (1000 * 60); // minutes
      const switchRate = state.contextSwitchCount / Math.max(sessionDuration, 1);
      const switchPenalty = Math.min(switchRate * 5, 20);
      
      // Add bonus for focus mode
      const focusBonus = state.focusModeActive ? -15 : 0;
      
      return Math.max(0, Math.min(100, baseLoad + switchPenalty + focusBonus));
    },

    // Get context switch rate (switches per minute)
    getContextSwitchRate: (): number => {
      const state = get();
      const sessionDuration = (new Date().getTime() - state.sessionStartTime.getTime()) / (1000 * 60);
      return state.contextSwitchCount / Math.max(sessionDuration, 1);
    },

    // Check if a new tool can be activated
    canActivateNewTool: (): boolean => {
      const state = get();
      return state.activeTools.size < COGNITIVE_LOAD_CONFIG.maxActiveTools;
    },
  }),
  {
    name: 'cognitive-load-storage',
    partialize: (state) => ({
      quickSwitchHistory: state.quickSwitchHistory,
      sessionStartTime: state.sessionStartTime,
      contextSwitchCount: state.contextSwitchCount,
    }),
  }
));

// Hook for cognitive load management with performance monitoring
export function useCognitiveLoadManager() {
  const store = useCognitiveLoadStore();
  const { measureOperation } = usePerformanceMonitor();

  const activateToolWithMonitoring = async (toolId: string, toolName: string, domain: string) => {
    await measureOperation(
      `cognitive-load-activate-${toolId}`,
      async () => {
        store.activateTool(toolId, toolName, domain);
      },
      'ui'
    );
  };

  const switchToToolWithMonitoring = async (toolId: string): Promise<boolean> => {
    return await measureOperation(
      `cognitive-load-switch-${toolId}`,
      async () => {
        return await store.switchToTool(toolId);
      },
      'ui'
    );
  };

  return {
    ...store,
    activateTool: activateToolWithMonitoring,
    switchToTool: switchToToolWithMonitoring,
  };
}

// Cognitive load indicator component props
export interface CognitiveLoadIndicatorProps {
  showDetails?: boolean;
  className?: string;
}

// Executive function accommodation utilities
export const ExecutiveFunctionUtils = {
  // Break down complex tasks
  createTaskBreakdown: (task: string, complexity: number): string[] => {
    if (complexity <= COGNITIVE_LOAD_CONFIG.taskBreakdownThreshold) {
      return [task];
    }
    
    // Simple heuristic task breakdown
    return [
      `Prepare for: ${task}`,
      `Execute: ${task}`,
      `Review results of: ${task}`,
      `Document completion of: ${task}`,
    ];
  },

  // Estimate task duration based on complexity
  estimateTaskDuration: (complexity: number, domain: string): number => {
    const baseTime = {
      security: 2, // minutes
      productivity: 5,
      mtg: 10,
      infrastructure: 15,
      ai: 8,
    }[domain] || 5;
    
    return baseTime * complexity;
  },

  // Generate executive function-friendly time estimates
  formatTimeEstimate: (minutes: number): string => {
    if (minutes < 5) return 'Quick task (~2-5 min)';
    if (minutes < 15) return 'Short task (~5-15 min)';
    if (minutes < 30) return 'Medium task (~15-30 min)';
    if (minutes < 60) return 'Long task (~30-60 min)';
    return 'Extended task (>1 hour)';
  },
};