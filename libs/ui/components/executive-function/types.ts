/**
 * Executive Function Types
 * 
 * TypeScript interfaces for executive function accommodations
 * across all 37 mental prosthetic tools
 */

export interface ExecutiveFunctionSettings {
  adhd_mode_enabled: boolean;
  focus_assist_enabled: boolean;
  context_switching_warning: boolean;
  progress_tracking_enabled: boolean;
  ui_response_time_threshold: number; // ms, default 200ms
  distraction_filtering: 'none' | 'low' | 'medium' | 'high';
  executive_function_reminders: boolean;
  tool_switching_confirmation: boolean;
  workflow_guidance_level: 'minimal' | 'moderate' | 'comprehensive';
}

export interface FocusAccommodation {
  reduce_visual_noise: boolean;
  enhance_focus_indicators: boolean;
  minimize_context_switching: boolean;
  provide_progress_feedback: boolean;
}

export interface ContextState {
  current_tool: string;
  active_workflows: string[];
  user_focus_state: 'focused' | 'distracted' | 'transitioning';
  session_duration: number; // minutes
  context_switches_count: number;
  tools_in_use: number;
  preserved_state: Record<string, unknown>;
}

export interface TaskProgress {
  task_id: string;
  task_title: string;
  completion_percentage: number;
  estimated_time_remaining: number; // minutes
  subtasks_completed: number;
  subtasks_total: number;
  last_activity: Date;
  executive_function_accommodations_used: string[];
}

export interface WorkflowStep {
  step_id: string;
  step_title: string;
  step_description: string;
  is_completed: boolean;
  is_current: boolean;
  estimated_duration: number; // minutes
  required_tools: string[];
  executive_function_notes: string[];
  accommodation_suggestions: string[];
}

export interface ADHDAccommodationOptions {
  timer_reminders: boolean;
  break_suggestions: boolean;
  hyperfocus_warnings: boolean;
  task_chunking_enabled: boolean;
  dopamine_feedback: 'none' | 'minimal' | 'moderate' | 'high';
}

export interface AutismAccommodationOptions {
  sensory_preferences: {
    reduce_animations: boolean;
    high_contrast: boolean;
    minimize_sounds: boolean;
  };
  routine_preservation: boolean;
  change_notifications: boolean;
  predictable_navigation: boolean;
}

export interface CognitiveLoadMetrics {
  current_load: number; // 0-100
  optimal_range: [number, number];
  overload_warning_threshold: number;
  tools_in_use: number;
  context_switches_per_hour: number;
  focus_duration_average: number; // minutes
}