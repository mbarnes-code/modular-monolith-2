/**
 * Optimized State Management for 37-Tool Mental Prosthetic Platform
 * Cross-domain communication with selective persistence and executive function support
 */

import { create } from 'zustand';
import { createJSONStorage, persist, subscribeWithSelector } from 'zustand/middleware';
import { immer } from 'zustand/middleware/immer';

// Event bus for cross-tool communication
class EventBus {
  private listeners: Map<string, Array<(data: any) => void>> = new Map();

  emit(event: string, data?: any): void {
    const eventListeners = this.listeners.get(event);
    if (eventListeners) {
      eventListeners.forEach(listener => listener(data));
    }
  }

  on(event: string, listener: (data: any) => void): () => void {
    if (!this.listeners.has(event)) {
      this.listeners.set(event, []);
    }
    this.listeners.get(event)!.push(listener);

    // Return unsubscribe function
    return () => {
      const eventListeners = this.listeners.get(event);
      if (eventListeners) {
        const index = eventListeners.indexOf(listener);
        if (index > -1) {
          eventListeners.splice(index, 1);
        }
      }
    };
  }

  off(event: string): void {
    this.listeners.delete(event);
  }
}

export const eventBus = new EventBus();

// Shared context for cross-domain workflows
interface SharedContext {
  currentWorkflow?: {
    id: string;
    name: string;
    steps: Array<{
      toolDomain: string;
      tool: string;
      completed: boolean;
      data?: any;
    }>;
    currentStep: number;
  };
  activeTools: string[];
  userFocus: {
    mode: 'normal' | 'focus' | 'deep-work';
    currentTool?: string;
    timeRemaining?: number;
  };
  crossToolData: Record<string, any>; // Shared data between tools
}

interface SharedContextStore extends SharedContext {
  // Actions
  setWorkflow: (workflow: SharedContext['currentWorkflow']) => void;
  completeWorkflowStep: (stepIndex: number, data?: any) => void;
  addActiveTool: (tool: string) => void;
  removeActiveTool: (tool: string) => void;
  setFocusMode: (mode: SharedContext['userFocus']['mode'], tool?: string, duration?: number) => void;
  setCrossToolData: (key: string, data: any) => void;
  getCrossToolData: (key: string) => any;
  clearCrossToolData: (key: string) => void;
}

// Shared context store with selective persistence
export const useSharedContext = create<SharedContextStore>()(
  persist(
    subscribeWithSelector(
      immer((set, get) => ({
        // Initial state
        currentWorkflow: undefined,
        activeTools: [],
        userFocus: {
          mode: 'normal',
        },
        crossToolData: {},

        // Actions
        setWorkflow: (workflow) => set((state) => {
          state.currentWorkflow = workflow;
          eventBus.emit('workflow:changed', workflow);
        }),

        completeWorkflowStep: (stepIndex, data) => set((state) => {
          if (state.currentWorkflow && state.currentWorkflow.steps[stepIndex]) {
            state.currentWorkflow.steps[stepIndex].completed = true;
            state.currentWorkflow.steps[stepIndex].data = data;
            state.currentWorkflow.currentStep = Math.min(
              stepIndex + 1,
              state.currentWorkflow.steps.length - 1
            );
            eventBus.emit('workflow:step-completed', { stepIndex, data });
          }
        }),

        addActiveTool: (tool) => set((state) => {
          if (!state.activeTools.includes(tool)) {
            // Respect cognitive load limit of 5 tools
            if (state.activeTools.length >= 5) {
              // Remove oldest tool
              state.activeTools.shift();
            }
            state.activeTools.push(tool);
            eventBus.emit('tool:activated', tool);
          }
        }),

        removeActiveTool: (tool) => set((state) => {
          const index = state.activeTools.indexOf(tool);
          if (index > -1) {
            state.activeTools.splice(index, 1);
            eventBus.emit('tool:deactivated', tool);
          }
        }),

        setFocusMode: (mode, tool, duration) => set((state) => {
          state.userFocus.mode = mode;
          state.userFocus.currentTool = tool;
          state.userFocus.timeRemaining = duration;
          eventBus.emit('focus:changed', { mode, tool, duration });
        }),

        setCrossToolData: (key, data) => set((state) => {
          state.crossToolData[key] = data;
          eventBus.emit('cross-tool-data:updated', { key, data });
        }),

        getCrossToolData: (key) => get().crossToolData[key],

        clearCrossToolData: (key) => set((state) => {
          delete state.crossToolData[key];
          eventBus.emit('cross-tool-data:cleared', key);
        }),
      }))
    ),
    {
      name: 'jane-shared-context',
      storage: createJSONStorage(() => localStorage),
      // Selective persistence - only persist user preferences and workflow state
      partialize: (state) => ({
        userFocus: state.userFocus,
        currentWorkflow: state.currentWorkflow,
        // Don't persist activeTools or crossToolData for security
      }),
    }
  )
);

// Domain-specific stores with optimizations

// Security Domain Store
interface SecurityState {
  threats: any[];
  alerts: any[];
  scanStatus: Record<string, 'idle' | 'scanning' | 'completed' | 'error'>;
  misp: {
    connected: boolean;
    lastSync: number;
    events: any[];
  };
}

interface SecurityStore extends SecurityState {
  addThreat: (threat: any) => void;
  updateScanStatus: (tool: string, status: SecurityState['scanStatus'][string]) => void;
  syncMISP: () => Promise<void>;
  clearAlerts: () => void;
}

export const useSecurityStore = create<SecurityStore>()(
  subscribeWithSelector(
    immer((set, get) => ({
      // Initial state
      threats: [],
      alerts: [],
      scanStatus: {},
      misp: {
        connected: false,
        lastSync: 0,
        events: [],
      },

      // Actions
      addThreat: (threat) => set((state) => {
        state.threats.push(threat);
        state.alerts.push({
          id: Date.now(),
          type: 'threat',
          severity: threat.severity || 'medium',
          message: threat.message,
          timestamp: Date.now(),
        });
        eventBus.emit('security:threat-detected', threat);
      }),

      updateScanStatus: (tool, status) => set((state) => {
        state.scanStatus[tool] = status;
        eventBus.emit('security:scan-status', { tool, status });
      }),

      syncMISP: async () => {
        set((state) => {
          state.misp.connected = true;
        });
        // Implement MISP sync logic here
        eventBus.emit('security:misp-sync-started');
      },

      clearAlerts: () => set((state) => {
        state.alerts = [];
      }),
    }))
  )
);

// Productivity Domain Store
interface ProductivityState {
  tasks: any[];
  workflows: any[];
  n8nStatus: 'connected' | 'disconnected' | 'syncing';
  activeAutomations: string[];
}

interface ProductivityStore extends ProductivityState {
  addTask: (task: any) => void;
  completeTask: (taskId: string) => void;
  triggerWorkflow: (workflowId: string) => void;
  updateN8NStatus: (status: ProductivityState['n8nStatus']) => void;
}

export const useProductivityStore = create<ProductivityStore>()(
  subscribeWithSelector(
    immer((set, get) => ({
      // Initial state
      tasks: [],
      workflows: [],
      n8nStatus: 'disconnected',
      activeAutomations: [],

      // Actions
      addTask: (task) => set((state) => {
        state.tasks.push(task);
        eventBus.emit('productivity:task-added', task);
      }),

      completeTask: (taskId) => set((state) => {
        const task = state.tasks.find(t => t.id === taskId);
        if (task) {
          task.completed = true;
          task.completedAt = Date.now();
          eventBus.emit('productivity:task-completed', task);
        }
      }),

      triggerWorkflow: (workflowId) => set((state) => {
        if (!state.activeAutomations.includes(workflowId)) {
          state.activeAutomations.push(workflowId);
          eventBus.emit('productivity:workflow-triggered', workflowId);
        }
      }),

      updateN8NStatus: (status) => set((state) => {
        state.n8nStatus = status;
        eventBus.emit('productivity:n8n-status', status);
      }),
    }))
  )
);

// MTG Domain Store
interface MTGState {
  decks: any[];
  collection: any[];
  gameHistory: any[];
  commanderRecommendations: any[];
}

interface MTGStore extends MTGState {
  addDeck: (deck: any) => void;
  updateCollection: (cards: any[]) => void;
  recordGame: (game: any) => void;
  getRecommendations: (commander: string) => any[];
}

export const useMTGStore = create<MTGStore>()(
  persist(
    subscribeWithSelector(
      immer((set, get) => ({
        // Initial state
        decks: [],
        collection: [],
        gameHistory: [],
        commanderRecommendations: [],

        // Actions
        addDeck: (deck) => set((state) => {
          state.decks.push(deck);
          eventBus.emit('mtg:deck-added', deck);
        }),

        updateCollection: (cards) => set((state) => {
          state.collection = cards;
          eventBus.emit('mtg:collection-updated', cards);
        }),

        recordGame: (game) => set((state) => {
          state.gameHistory.push(game);
          eventBus.emit('mtg:game-recorded', game);
        }),

        getRecommendations: (commander) => {
          return get().commanderRecommendations.filter(r => 
            r.commander === commander
          );
        },
      }))
    ),
    {
      name: 'jane-mtg-store',
      storage: createJSONStorage(() => localStorage),
    }
  )
);

// Hook for cross-domain communication
export function useCrossDomainSync() {
  const sharedContext = useSharedContext();

  const syncData = (domain: string, key: string, data: any) => {
    sharedContext.setCrossToolData(`${domain}:${key}`, data);
  };

  const getData = (domain: string, key: string) => {
    return sharedContext.getCrossToolData(`${domain}:${key}`);
  };

  const subscribeToEvents = (events: string[], callback: (event: string, data: any) => void) => {
    const unsubscribes = events.map(event => 
      eventBus.on(event, (data) => callback(event, data))
    );

    return () => unsubscribes.forEach(fn => fn());
  };

  return {
    syncData,
    getData,
    subscribeToEvents,
    eventBus,
  };
}