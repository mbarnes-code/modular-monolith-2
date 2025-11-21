/**
 * Cross-Domain Workflow Manager
 * Orchestrates multi-tool workflows for the 37-tool mental prosthetic platform
 */

import React, { useState, useEffect } from 'react';
import { useSharedContext, useCrossDomainSync } from '../../services/state/optimizedStateManager';
import { usePerformanceMonitor } from '../../services/performance/performanceMonitor';

interface WorkflowStep {
  id: string;
  toolDomain: string;
  tool: string;
  title: string;
  description: string;
  estimatedTime: number; // in minutes
  dependencies: string[]; // step IDs that must complete first
  completed: boolean;
  data?: any;
  status: 'pending' | 'active' | 'completed' | 'blocked' | 'error';
}

interface WorkflowTemplate {
  id: string;
  name: string;
  description: string;
  category: 'security' | 'productivity' | 'analysis' | 'reporting';
  steps: Omit<WorkflowStep, 'completed' | 'status' | 'data'>[];
  estimatedDuration: number;
  complexity: 'beginner' | 'intermediate' | 'advanced';
}

const PREDEFINED_WORKFLOWS: WorkflowTemplate[] = [
  {
    id: 'threat-analysis-complete',
    name: 'Complete Threat Analysis',
    description: 'Full security analysis workflow from threat detection to report generation',
    category: 'security',
    estimatedDuration: 45,
    complexity: 'advanced',
    steps: [
      {
        id: 'step1',
        toolDomain: 'security',
        tool: 'maltrail',
        title: 'Network Traffic Analysis',
        description: 'Analyze network traffic for suspicious patterns',
        estimatedTime: 10,
        dependencies: []
      },
      {
        id: 'step2',
        toolDomain: 'security',
        tool: 'misp',
        title: 'Threat Intelligence Lookup',
        description: 'Cross-reference findings with threat intelligence database',
        estimatedTime: 15,
        dependencies: ['step1']
      },
      {
        id: 'step3',
        toolDomain: 'security',
        tool: 'cyberchef',
        title: 'Data Analysis & Decoding',
        description: 'Decode and analyze suspicious data artifacts',
        estimatedTime: 10,
        dependencies: ['step1']
      },
      {
        id: 'step4',
        toolDomain: 'security',
        tool: 'ghostwriter',
        title: 'Generate Analysis Report',
        description: 'Compile findings into comprehensive security report',
        estimatedTime: 10,
        dependencies: ['step2', 'step3']
      }
    ]
  },
  {
    id: 'meal-planning-automation',
    name: 'Automated Meal Planning',
    description: 'Complete meal planning workflow with shopping list generation',
    category: 'productivity',
    estimatedDuration: 20,
    complexity: 'beginner',
    steps: [
      {
        id: 'step1',
        toolDomain: 'productivity',
        tool: 'mealie',
        title: 'Plan Weekly Meals',
        description: 'Select recipes and plan meals for the week',
        estimatedTime: 10,
        dependencies: []
      },
      {
        id: 'step2',
        toolDomain: 'productivity',
        tool: 'mealie',
        title: 'Generate Shopping List',
        description: 'Create shopping list from meal plan ingredients',
        estimatedTime: 5,
        dependencies: ['step1']
      },
      {
        id: 'step3',
        toolDomain: 'productivity',
        tool: 'n8n',
        title: 'Schedule Grocery Delivery',
        description: 'Automate grocery ordering through n8n workflow',
        estimatedTime: 5,
        dependencies: ['step2']
      }
    ]
  },
  {
    id: 'deck-optimization',
    name: 'MTG Deck Optimization',
    description: 'Comprehensive deck analysis and improvement workflow',
    category: 'analysis',
    estimatedDuration: 30,
    complexity: 'intermediate',
    steps: [
      {
        id: 'step1',
        toolDomain: 'mtg',
        tool: 'commander-spellbook',
        title: 'Analyze Current Deck',
        description: 'Import and analyze deck composition and synergies',
        estimatedTime: 10,
        dependencies: []
      },
      {
        id: 'step2',
        toolDomain: 'mtg',
        tool: 'mtg-scripting',
        title: 'Run Optimization Scripts',
        description: 'Execute mana curve and synergy optimization scripts',
        estimatedTime: 10,
        dependencies: ['step1']
      },
      {
        id: 'step3',
        toolDomain: 'mtg',
        tool: 'commander-spellbook',
        title: 'Generate Recommendations',
        description: 'Get card suggestions and combo recommendations',
        estimatedTime: 10,
        dependencies: ['step2']
      }
    ]
  }
];

interface WorkflowManagerProps {
  className?: string;
}

export function WorkflowManager({ className = '' }: WorkflowManagerProps) {
  const sharedContext = useSharedContext();
  const { subscribeToEvents, syncData } = useCrossDomainSync();
  const { measureOperation, markUIInteraction } = usePerformanceMonitor();
  
  const [selectedTemplate, setSelectedTemplate] = useState<WorkflowTemplate | null>(null);
  const [activeWorkflow, setActiveWorkflow] = useState<WorkflowStep[] | null>(null);
  const [currentStepIndex, setCurrentStepIndex] = useState(0);
  const [showTemplateSelector, setShowTemplateSelector] = useState(true);

  // Load existing workflow from shared context
  useEffect(() => {
    if (sharedContext.currentWorkflow) {
      const workflow = sharedContext.currentWorkflow;
      setActiveWorkflow(workflow.steps);
      setCurrentStepIndex(workflow.currentStep);
      setShowTemplateSelector(false);
    }
  }, [sharedContext.currentWorkflow]);

  // Subscribe to workflow events
  useEffect(() => {
    const unsubscribe = subscribeToEvents(
      ['workflow:step-completed', 'tool:activated'],
      (event, data) => {
        if (event === 'workflow:step-completed') {
          handleStepCompletion(data.stepIndex, data.data);
        } else if (event === 'tool:activated' && activeWorkflow) {
          // Auto-advance workflow if user switches to next expected tool
          const currentStep = activeWorkflow[currentStepIndex];
          if (currentStep && data === currentStep.tool) {
            updateStepStatus(currentStepIndex, 'active');
          }
        }
      }
    );

    return unsubscribe;
  }, [subscribeToEvents, activeWorkflow, currentStepIndex]);

  const startWorkflow = async (template: WorkflowTemplate) => {
    markUIInteraction('workflow-start');
    
    const workflowSteps: WorkflowStep[] = template.steps.map(step => ({
      ...step,
      completed: false,
      status: 'pending' as const
    }));

    // Mark first step as active
    if (workflowSteps.length > 0) {
      workflowSteps[0].status = 'active';
    }

    const workflow = {
      id: `${template.id}-${Date.now()}`,
      name: template.name,
      steps: workflowSteps,
      currentStep: 0
    };

    await measureOperation('workflow-initialization', () => {
      setActiveWorkflow(workflowSteps);
      setCurrentStepIndex(0);
      setShowTemplateSelector(false);
      sharedContext.setWorkflow(workflow);
      
      // Sync workflow data across domains
      syncData('workflow', 'active-workflow', workflow);
    }, 'productivity');
  };

  const updateStepStatus = (stepIndex: number, status: WorkflowStep['status']) => {
    if (!activeWorkflow) return;

    const updatedWorkflow = [...activeWorkflow];
    updatedWorkflow[stepIndex] = { ...updatedWorkflow[stepIndex], status };
    setActiveWorkflow(updatedWorkflow);
  };

  const handleStepCompletion = (stepIndex: number, data?: any) => {
    if (!activeWorkflow) return;

    const updatedWorkflow = [...activeWorkflow];
    updatedWorkflow[stepIndex] = {
      ...updatedWorkflow[stepIndex],
      completed: true,
      status: 'completed',
      data
    };

    // Find next available step (not blocked by dependencies)
    let nextStepIndex = -1;
    for (let i = stepIndex + 1; i < updatedWorkflow.length; i++) {
      const step = updatedWorkflow[i];
      const dependenciesMet = step.dependencies.every(depId => {
        const depStep = updatedWorkflow.find(s => s.id === depId);
        return depStep?.completed;
      });
      
      if (dependenciesMet && step.status === 'pending') {
        nextStepIndex = i;
        updatedWorkflow[i] = { ...step, status: 'active' };
        break;
      }
    }

    setActiveWorkflow(updatedWorkflow);
    
    if (nextStepIndex >= 0) {
      setCurrentStepIndex(nextStepIndex);
    } else {
      // Workflow completed
      const allCompleted = updatedWorkflow.every(step => step.completed);
      if (allCompleted) {
        // Workflow finished
        setTimeout(() => {
          setShowTemplateSelector(true);
          setActiveWorkflow(null);
          sharedContext.setWorkflow(undefined);
        }, 2000);
      }
    }
  };

  const calculateProgress = () => {
    if (!activeWorkflow) return 0;
    const completed = activeWorkflow.filter(step => step.completed).length;
    return (completed / activeWorkflow.length) * 100;
  };

  const getTimeRemaining = () => {
    if (!activeWorkflow) return 0;
    return activeWorkflow
      .filter(step => !step.completed)
      .reduce((total, step) => total + step.estimatedTime, 0);
  };

  if (showTemplateSelector) {
    return (
      <div className={`workflow-manager ${className}`}>
        <div className="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 p-6">
          <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">
            Cross-Domain Workflows
          </h2>
          <p className="text-gray-600 dark:text-gray-300 mb-6">
            Orchestrated workflows that span multiple tools in your mental prosthetic platform.
          </p>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {PREDEFINED_WORKFLOWS.map(template => (
              <div
                key={template.id}
                className="workflow-card border border-gray-200 dark:border-gray-600 rounded-lg p-4 hover:shadow-md transition-shadow cursor-pointer"
                onClick={() => startWorkflow(template)}
              >
                <div className="flex items-center justify-between mb-2">
                  <h3 className="font-semibold text-gray-900 dark:text-white">
                    {template.name}
                  </h3>
                  <span className={`text-xs px-2 py-1 rounded-full ${
                    template.complexity === 'beginner' ? 'bg-green-100 text-green-700' :
                    template.complexity === 'intermediate' ? 'bg-yellow-100 text-yellow-700' :
                    'bg-red-100 text-red-700'
                  }`}>
                    {template.complexity}
                  </span>
                </div>
                <p className="text-sm text-gray-600 dark:text-gray-400 mb-3">
                  {template.description}
                </p>
                <div className="flex items-center justify-between text-xs text-gray-500">
                  <span>{template.steps.length} steps</span>
                  <span>~{template.estimatedDuration}min</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className={`workflow-manager ${className}`}>
      <div className="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 p-6">
        {/* Workflow Header */}
        <div className="flex items-center justify-between mb-6">
          <div>
            <h2 className="text-xl font-semibold text-gray-900 dark:text-white">
              Active Workflow
            </h2>
            <p className="text-sm text-gray-600 dark:text-gray-400">
              {selectedTemplate?.name} • {getTimeRemaining()}min remaining
            </p>
          </div>
          <button
            onClick={() => setShowTemplateSelector(true)}
            className="px-3 py-2 text-sm border border-gray-300 dark:border-gray-600 rounded-md hover:bg-gray-50 dark:hover:bg-gray-700"
          >
            Change Workflow
          </button>
        </div>

        {/* Progress Bar */}
        <div className="mb-6">
          <div className="flex items-center justify-between mb-2">
            <span className="text-sm font-medium text-gray-700 dark:text-gray-300">
              Progress
            </span>
            <span className="text-sm text-gray-600 dark:text-gray-400">
              {Math.round(calculateProgress())}%
            </span>
          </div>
          <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
            <div
              className="bg-blue-600 h-2 rounded-full transition-all duration-300"
              style={{ width: `${calculateProgress()}%` }}
            />
          </div>
        </div>

        {/* Workflow Steps */}
        <div className="space-y-3">
          {activeWorkflow?.map((step, index) => (
            <div
              key={step.id}
              className={`workflow-step flex items-center gap-4 p-3 rounded-lg border ${
                step.status === 'active' ? 'border-blue-300 bg-blue-50 dark:bg-blue-900/20' :
                step.status === 'completed' ? 'border-green-300 bg-green-50 dark:bg-green-900/20' :
                step.status === 'blocked' ? 'border-red-300 bg-red-50 dark:bg-red-900/20' :
                'border-gray-200 dark:border-gray-600'
              }`}
            >
              {/* Step Status Icon */}
              <div className={`w-8 h-8 rounded-full flex items-center justify-center ${
                step.status === 'completed' ? 'bg-green-500 text-white' :
                step.status === 'active' ? 'bg-blue-500 text-white' :
                step.status === 'blocked' ? 'bg-red-500 text-white' :
                'bg-gray-300 text-gray-600'
              }`}>
                {step.status === 'completed' ? '✓' :
                 step.status === 'active' ? '▶' :
                 step.status === 'blocked' ? '⚠' :
                 index + 1}
              </div>

              {/* Step Content */}
              <div className="flex-1">
                <div className="flex items-center gap-2 mb-1">
                  <h4 className="font-medium text-gray-900 dark:text-white">
                    {step.title}
                  </h4>
                  <span className="text-xs px-2 py-1 bg-gray-100 dark:bg-gray-700 rounded">
                    {step.tool}
                  </span>
                  <span className="text-xs text-gray-500">
                    {step.estimatedTime}min
                  </span>
                </div>
                <p className="text-sm text-gray-600 dark:text-gray-400">
                  {step.description}
                </p>
                {step.dependencies.length > 0 && (
                  <p className="text-xs text-gray-500 mt-1">
                    Depends on: {step.dependencies.join(', ')}
                  </p>
                )}
              </div>

              {/* Action Button */}
              {step.status === 'active' && (
                <button
                  onClick={() => handleStepCompletion(index)}
                  className="px-3 py-1 text-sm bg-blue-600 text-white rounded hover:bg-blue-700"
                >
                  Complete
                </button>
              )}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}