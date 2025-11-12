/**
 * Global State Management with Zustand
 * 
 * Provides cross-domain state management for all 37 tools
 * with executive function accommodations
 */

import { create } from 'zustand';
import { persist } from 'zustand/middleware';

// Domain types
export type Domain = 'security' | 'productivity' | 'mtg' | 'infrastructure';

export interface Tool {
  id: string;
  name: string;
  domain: Domain;
  isActive: boolean;
  lastUsed?: Date;
  context?: Record<string, unknown>;
}

export interface User {
  id: string;
  username: string;
  preferences: {
    adhd_mode: boolean;
    high_contrast: boolean;
    reduce_animations: boolean;
    focus_assist: boolean;
    response_threshold: number;
  };
}

export interface PerformanceMetrics {
  domain: Domain;
  toolName: string;
  responseTime: number;
  timestamp: Date;
}

export interface GlobalState {
  // User & Auth
  user: User | null;
  isAuthenticated: boolean;
  authToken: string | null;

  // Tools & Navigation
  activeTool: string | null;
  activeTools: Tool[];
  navigationHistory: string[];

  // Performance & Metrics
  performanceMetrics: PerformanceMetrics[];
  cognitiveLoad: number;
  alertsEnabled: boolean;

  // Executive Function
  contextSwitches: number;
  sessionStartTime: Date | null;
  taskHistory: Array<{
    tool: string;
    action: string;
    timestamp: Date;
    duration?: number;
  }>;

  // Actions
  setUser: (user: User | null) => void;
  setAuth: (token: string | null) => void;
  
  setActiveTool: (toolId: string) => void;
  addActiveTool: (tool: Tool) => void;
  removeActiveTool: (toolId: string) => void;
  
  addPerformanceMetric: (metric: PerformanceMetrics) => void;
  updateCognitiveLoad: (load: number) => void;
  
  incrementContextSwitches: () => void;
  addTaskHistory: (task: { tool: string; action: string; duration?: number }) => void;
  
  reset: () => void;
}

const useGlobalStore = create<GlobalState>()(
  persist(
    (set, get) => ({
      // Initial state
      user: null,
      isAuthenticated: false,
      authToken: null,
      
      activeTool: null,
      activeTools: [],
      navigationHistory: [],
      
      performanceMetrics: [],
      cognitiveLoad: 0,
      alertsEnabled: true,
      
      contextSwitches: 0,
      sessionStartTime: null,
      taskHistory: [],

      // Actions
      setUser: (user: User | null) => {
        set({ user, isAuthenticated: !!user });
      },

      setAuth: (token: string | null) => {
        set({ authToken: token, isAuthenticated: !!token });
      },

      setActiveTool: (toolId: string) => {
        const currentTool = get().activeTool;
        
        // Track context switch if changing tools
        if (currentTool && currentTool !== toolId) {
          set(state => ({
            contextSwitches: state.contextSwitches + 1,
            navigationHistory: [...state.navigationHistory.slice(-9), toolId] // Keep last 10
          }));
        }

        // Set session start time if first tool activation
        if (!get().sessionStartTime) {
          set({ sessionStartTime: new Date() });
        }

        set({ activeTool: toolId });
      },

      addActiveTool: (tool: Tool) => {
        set(state => {
          const existing = state.activeTools.find(t => t.id === tool.id);
          if (existing) {
            // Update existing tool
            return {
              activeTools: state.activeTools.map(t => 
                t.id === tool.id ? { ...t, ...tool, lastUsed: new Date() } : t
              )
            };
          } else {
            // Add new tool
            return {
              activeTools: [...state.activeTools, { ...tool, lastUsed: new Date() }]
            };
          }
        });
      },

      removeActiveTool: (toolId: string) => {
        set(state => ({
          activeTools: state.activeTools.filter(t => t.id !== toolId),
          activeTool: state.activeTool === toolId ? null : state.activeTool
        }));
      },

      addPerformanceMetric: (metric: PerformanceMetrics) => {
        set(state => {
          const newMetrics = [...state.performanceMetrics, metric];
          
          // Keep only last 1000 metrics
          if (newMetrics.length > 1000) {
            newMetrics.splice(0, newMetrics.length - 1000);
          }

          // Update cognitive load based on response time
          const domainThresholds = {
            security: 1000,
            productivity: 2000,
            mtg: 3000,
            infrastructure: 5000
          };

          const threshold = domainThresholds[metric.domain];
          const overThreshold = metric.responseTime > threshold;
          const cognitiveLoadIncrease = overThreshold ? 5 : -1;
          const newCognitiveLoad = Math.max(0, Math.min(100, state.cognitiveLoad + cognitiveLoadIncrease));

          return {
            performanceMetrics: newMetrics,
            cognitiveLoad: newCognitiveLoad
          };
        });
      },

      updateCognitiveLoad: (load: number) => {
        set({ cognitiveLoad: Math.max(0, Math.min(100, load)) });
      },

      incrementContextSwitches: () => {
        set(state => ({ contextSwitches: state.contextSwitches + 1 }));
      },

      addTaskHistory: (task: { tool: string; action: string; duration?: number }) => {
        set(state => {
          const newHistory = [...state.taskHistory, {
            ...task,
            timestamp: new Date()
          }];

          // Keep only last 100 tasks
          if (newHistory.length > 100) {
            newHistory.shift();
          }

          return { taskHistory: newHistory };
        });
      },

      reset: () => {
        set({
          activeTool: null,
          activeTools: [],
          navigationHistory: [],
          performanceMetrics: [],
          cognitiveLoad: 0,
          contextSwitches: 0,
          sessionStartTime: null,
          taskHistory: []
        });
      }
    }),
    {
      name: 'mental-prosthetic-storage',
      partialize: (state) => ({
        // Only persist user preferences and settings
        user: state.user,
        authToken: state.authToken,
        isAuthenticated: state.isAuthenticated,
        alertsEnabled: state.alertsEnabled
      })
    }
  )
);

// Selectors for derived state
export const useAuth = () => useGlobalStore(state => ({
  user: state.user,
  isAuthenticated: state.isAuthenticated,
  authToken: state.authToken,
  setUser: state.setUser,
  setAuth: state.setAuth
}));

export const useTools = () => useGlobalStore(state => ({
  activeTool: state.activeTool,
  activeTools: state.activeTools,
  navigationHistory: state.navigationHistory,
  setActiveTool: state.setActiveTool,
  addActiveTool: state.addActiveTool,
  removeActiveTool: state.removeActiveTool
}));

export const usePerformance = () => useGlobalStore(state => ({
  performanceMetrics: state.performanceMetrics,
  cognitiveLoad: state.cognitiveLoad,
  contextSwitches: state.contextSwitches,
  addPerformanceMetric: state.addPerformanceMetric,
  updateCognitiveLoad: state.updateCognitiveLoad,
  incrementContextSwitches: state.incrementContextSwitches
}));

export const useTaskHistory = () => useGlobalStore(state => ({
  taskHistory: state.taskHistory,
  sessionStartTime: state.sessionStartTime,
  addTaskHistory: state.addTaskHistory
}));

export const useExecutiveFunctionMetrics = () => {
  const { contextSwitches, cognitiveLoad, sessionStartTime, taskHistory } = useGlobalStore();
  
  const sessionDuration = sessionStartTime 
    ? Math.floor((Date.now() - sessionStartTime.getTime()) / 1000 / 60) // minutes
    : 0;

  const averageTaskDuration = taskHistory.length > 0
    ? taskHistory
        .filter(t => t.duration)
        .reduce((acc, t) => acc + (t.duration || 0), 0) / taskHistory.filter(t => t.duration).length
    : 0;

  const contextSwitchRate = sessionDuration > 0 ? contextSwitches / sessionDuration : 0;

  return {
    contextSwitches,
    cognitiveLoad,
    sessionDuration,
    averageTaskDuration,
    contextSwitchRate,
    isOverloaded: cognitiveLoad > 80,
    needsBreak: sessionDuration > 90 && contextSwitchRate > 2 // More than 2 switches per minute after 90 min
  };
};

export default useGlobalStore;