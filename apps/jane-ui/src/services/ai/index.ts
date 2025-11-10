// AI Services Export
export { crossToolContextService, useCrossToolContext } from './crossToolContext';
export { useAIContext } from './useAIContext';
export { proactiveReminderService, useProactiveReminders } from './proactiveReminders';

export type {
  ToolContext,
  CrossToolContext, 
  ContextSuggestion
} from './crossToolContext';

export type {
  AIContextHookProps,
  AIContextState
} from './useAIContext';

export type {
  UserPattern,
  ProactiveReminder,
  PatternRecognitionState
} from './proactiveReminders';