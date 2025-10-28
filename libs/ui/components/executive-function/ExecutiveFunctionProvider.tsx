/**
 * Executive Function Provider
 * 
 * React Context Provider for executive function accommodations
 * Provides settings and state management across all 37 tools
 */

import React, { createContext, ReactNode, useContext, useEffect, useReducer } from 'react';
import {
    ADHDAccommodationOptions,
    AutismAccommodationOptions,
    CognitiveLoadMetrics,
    ContextState,
    ExecutiveFunctionSettings,
    TaskProgress
} from './types';

interface ExecutiveFunctionState {
  settings: ExecutiveFunctionSettings;
  contextState: ContextState;
  tasks: TaskProgress[];
  adhdOptions: ADHDAccommodationOptions;
  autismOptions: AutismAccommodationOptions;
  cognitiveLoad: CognitiveLoadMetrics;
  isInitialized: boolean;
}

type ExecutiveFunctionAction =
  | { type: 'UPDATE_SETTINGS'; payload: Partial<ExecutiveFunctionSettings> }
  | { type: 'UPDATE_CONTEXT_STATE'; payload: Partial<ContextState> }
  | { type: 'ADD_TASK'; payload: TaskProgress }
  | { type: 'UPDATE_TASK'; payload: { taskId: string; updates: Partial<TaskProgress> } }
  | { type: 'REMOVE_TASK'; payload: string }
  | { type: 'UPDATE_ADHD_OPTIONS'; payload: Partial<ADHDAccommodationOptions> }
  | { type: 'UPDATE_AUTISM_OPTIONS'; payload: Partial<AutismAccommodationOptions> }
  | { type: 'UPDATE_COGNITIVE_LOAD'; payload: Partial<CognitiveLoadMetrics> }
  | { type: 'INITIALIZE'; payload: Partial<ExecutiveFunctionState> }
  | { type: 'RESET_TO_DEFAULTS' };

const defaultSettings: ExecutiveFunctionSettings = {
  adhd_mode_enabled: false,
  focus_assist_enabled: true,
  context_switching_warning: true,
  progress_tracking_enabled: true,
  ui_response_time_threshold: 200,
  distraction_filtering: 'medium',
  executive_function_reminders: true,
  tool_switching_confirmation: true,
  workflow_guidance_level: 'moderate'
};

const defaultContextState: ContextState = {
  current_tool: '',
  active_workflows: [],
  user_focus_state: 'focused',
  session_duration: 0,
  context_switches_count: 0,
  tools_in_use: 1,
  preserved_state: {}
};

const defaultADHDOptions: ADHDAccommodationOptions = {
  timer_reminders: true,
  break_suggestions: true,
  hyperfocus_warnings: true,
  task_chunking_enabled: true,
  dopamine_feedback: 'moderate'
};

const defaultAutismOptions: AutismAccommodationOptions = {
  sensory_preferences: {
    reduce_animations: false,
    high_contrast: false,
    minimize_sounds: false
  },
  routine_preservation: true,
  change_notifications: true,
  predictable_navigation: true
};

const defaultCognitiveLoad: CognitiveLoadMetrics = {
  current_load: 30,
  optimal_range: [20, 70],
  overload_warning_threshold: 80,
  tools_in_use: 1,
  context_switches_per_hour: 0,
  focus_duration_average: 25
};

const initialState: ExecutiveFunctionState = {
  settings: defaultSettings,
  contextState: defaultContextState,
  tasks: [],
  adhdOptions: defaultADHDOptions,
  autismOptions: defaultAutismOptions,
  cognitiveLoad: defaultCognitiveLoad,
  isInitialized: false
};

function executiveFunctionReducer(
  state: ExecutiveFunctionState,
  action: ExecutiveFunctionAction
): ExecutiveFunctionState {
  switch (action.type) {
    case 'UPDATE_SETTINGS':
      return {
        ...state,
        settings: { ...state.settings, ...action.payload }
      };

    case 'UPDATE_CONTEXT_STATE':
      return {
        ...state,
        contextState: { ...state.contextState, ...action.payload }
      };

    case 'ADD_TASK':
      return {
        ...state,
        tasks: [...state.tasks, action.payload]
      };

    case 'UPDATE_TASK':
      return {
        ...state,
        tasks: state.tasks.map(task =>
          task.task_id === action.payload.taskId
            ? { ...task, ...action.payload.updates }
            : task
        )
      };

    case 'REMOVE_TASK':
      return {
        ...state,
        tasks: state.tasks.filter(task => task.task_id !== action.payload)
      };

    case 'UPDATE_ADHD_OPTIONS':
      return {
        ...state,
        adhdOptions: { ...state.adhdOptions, ...action.payload }
      };

    case 'UPDATE_AUTISM_OPTIONS':
      return {
        ...state,
        autismOptions: { ...state.autismOptions, ...action.payload }
      };

    case 'UPDATE_COGNITIVE_LOAD':
      return {
        ...state,
        cognitiveLoad: { ...state.cognitiveLoad, ...action.payload }
      };

    case 'INITIALIZE':
      return {
        ...state,
        ...action.payload,
        isInitialized: true
      };

    case 'RESET_TO_DEFAULTS':
      return {
        ...initialState,
        isInitialized: true
      };

    default:
      return state;
  }
}

const ExecutiveFunctionContext = createContext<{
  state: ExecutiveFunctionState;
  dispatch: React.Dispatch<ExecutiveFunctionAction>;
} | null>(null);

interface ExecutiveFunctionProviderProps {
  children: ReactNode;
  initialSettings?: Partial<ExecutiveFunctionSettings>;
  storageKey?: string;
  autoSave?: boolean;
}

export const ExecutiveFunctionProvider: React.FC<ExecutiveFunctionProviderProps> = ({
  children,
  initialSettings,
  storageKey = 'mental-prosthetic-executive-function',
  autoSave = true
}) => {
  const [state, dispatch] = useReducer(executiveFunctionReducer, initialState);

  // Load settings from localStorage on mount
  useEffect(() => {
    try {
      const savedState = localStorage.getItem(storageKey);
      if (savedState) {
        const parsed = JSON.parse(savedState);
        dispatch({ type: 'INITIALIZE', payload: parsed });
      } else if (initialSettings) {
        dispatch({
          type: 'INITIALIZE',
          payload: { settings: { ...defaultSettings, ...initialSettings } }
        });
      } else {
        dispatch({ type: 'INITIALIZE', payload: {} });
      }
    } catch (error) {
      console.warn('[ExecutiveFunctionProvider] Failed to load saved state:', error);
      dispatch({ type: 'INITIALIZE', payload: {} });
    }
  }, [storageKey, initialSettings]);

  // Auto-save to localStorage when state changes
  useEffect(() => {
    if (!autoSave || !state.isInitialized) return;

    try {
      const stateToSave = {
        settings: state.settings,
        adhdOptions: state.adhdOptions,
        autismOptions: state.autismOptions,
        // Don't save dynamic state like contextState, tasks, cognitiveLoad
      };
      localStorage.setItem(storageKey, JSON.stringify(stateToSave));
    } catch (error) {
      console.warn('[ExecutiveFunctionProvider] Failed to save state:', error);
    }
  }, [state.settings, state.adhdOptions, state.autismOptions, state.isInitialized, autoSave, storageKey]);

  // Update cognitive load based on context changes
  useEffect(() => {
    if (!state.isInitialized) return;

    const calculateCognitiveLoad = () => {
      const baseLoad = 20;
      const toolLoad = state.contextState.tools_in_use * 15;
      const workflowLoad = state.contextState.active_workflows.length * 10;
      const switchingPenalty = Math.min(state.contextState.context_switches_count * 2, 30);
      
      const totalLoad = Math.min(100, baseLoad + toolLoad + workflowLoad + switchingPenalty);
      
      return {
        current_load: totalLoad,
        tools_in_use: state.contextState.active_workflows.length,
        context_switches_per_hour: state.contextState.context_switches_count
      };
    };

    const newMetrics = calculateCognitiveLoad();
    dispatch({ type: 'UPDATE_COGNITIVE_LOAD', payload: newMetrics });
  }, [
    state.contextState.active_workflows,
    state.contextState.context_switches_count,
    state.isInitialized
  ]);

  return (
    <ExecutiveFunctionContext.Provider value={{ state, dispatch }}>
      {children}
    </ExecutiveFunctionContext.Provider>
  );
};

// Custom hooks for using the context
export const useExecutiveFunction = () => {
  const context = useContext(ExecutiveFunctionContext);
  if (!context) {
    throw new Error('useExecutiveFunction must be used within ExecutiveFunctionProvider');
  }
  return context;
};

export const useExecutiveFunctionSettings = () => {
  const { state, dispatch } = useExecutiveFunction();
  
  const updateSettings = (updates: Partial<ExecutiveFunctionSettings>) => {
    dispatch({ type: 'UPDATE_SETTINGS', payload: updates });
  };

  return { settings: state.settings, updateSettings };
};

export const useContextState = () => {
  const { state, dispatch } = useExecutiveFunction();
  
  const updateContextState = (updates: Partial<ContextState>) => {
    dispatch({ type: 'UPDATE_CONTEXT_STATE', payload: updates });
  };

  const switchTool = (toolName: string) => {
    const newSwitchCount = state.contextState.context_switches_count + 1;
    updateContextState({
      current_tool: toolName,
      context_switches_count: newSwitchCount
    });
  };

  const addWorkflow = (workflowId: string) => {
    const newWorkflows = [...state.contextState.active_workflows, workflowId];
    updateContextState({ active_workflows: newWorkflows });
  };

  const removeWorkflow = (workflowId: string) => {
    const newWorkflows = state.contextState.active_workflows.filter(id => id !== workflowId);
    updateContextState({ active_workflows: newWorkflows });
  };

  return {
    contextState: state.contextState,
    updateContextState,
    switchTool,
    addWorkflow,
    removeWorkflow
  };
};

export const useTaskTracking = () => {
  const { state, dispatch } = useExecutiveFunction();
  
  const addTask = (task: TaskProgress) => {
    dispatch({ type: 'ADD_TASK', payload: task });
  };

  const updateTask = (taskId: string, updates: Partial<TaskProgress>) => {
    dispatch({ type: 'UPDATE_TASK', payload: { taskId, updates } });
  };

  const removeTask = (taskId: string) => {
    dispatch({ type: 'REMOVE_TASK', payload: taskId });
  };

  return {
    tasks: state.tasks,
    addTask,
    updateTask,
    removeTask
  };
};

export const useCognitiveLoad = () => {
  const { state, dispatch } = useExecutiveFunction();
  
  const updateCognitiveLoad = (updates: Partial<CognitiveLoadMetrics>) => {
    dispatch({ type: 'UPDATE_COGNITIVE_LOAD', payload: updates });
  };

  const isOverloaded = state.cognitiveLoad.current_load > state.cognitiveLoad.overload_warning_threshold;
  const isInOptimalRange = state.cognitiveLoad.current_load >= state.cognitiveLoad.optimal_range[0] &&
                           state.cognitiveLoad.current_load <= state.cognitiveLoad.optimal_range[1];

  return {
    cognitiveLoad: state.cognitiveLoad,
    updateCognitiveLoad,
    isOverloaded,
    isInOptimalRange
  };
};