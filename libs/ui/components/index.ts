/**
 * Mental Prosthetic UI Component Library
 * 
 * React components with ADHD/autism accommodations
 * for executive function support across all 37 tools
 */

// Executive Function Components
export {
    ContextPreserver, ExecutiveFunctionProvider, FocusIndicator, TaskTracker,
    WorkflowGuide, useCognitiveLoad, useContextState, useExecutiveFunction,
    useExecutiveFunctionSettings, useTaskTracking
} from './executive-function';

// Executive Function Types
export type {
    ADHDAccommodationOptions,
    AutismAccommodationOptions,
    CognitiveLoadMetrics, ContextState, ExecutiveFunctionSettings,
    FocusAccommodation, TaskProgress,
    WorkflowStep
} from './executive-function/types';

// Base UI Components
export { Button, Input } from './base';

// Domain-Specific Components (future expansion)
// export { SecurityTool, ProductivityTool, MTGTool, InfrastructureTool } from './domain';

// Layout Components (future expansion)
// export { Navigation, Sidebar, Dashboard, ToolSwitcher } from './layout';

// Version and metadata
export const UI_LIBRARY_VERSION = '1.0.0';
export const SUPPORTED_ACCOMMODATIONS = [
  'ADHD support',
  'Autism accommodations',
  'Executive function enhancement',
  'Context preservation',
  'Focus assistance',
  'Task tracking',
  'Workflow guidance',
  'Cognitive load management'
] as const;