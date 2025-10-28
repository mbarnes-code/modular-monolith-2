/**
 * Workflow Guide Component
 * 
 * Step-by-step workflow guidance with executive function support
 * Reduces cognitive load by breaking complex tasks into manageable steps
 */

import React, { useEffect, useState } from 'react';
import { WorkflowStep } from './types';

interface WorkflowGuideProps {
  /** Array of workflow steps */
  steps: WorkflowStep[];
  /** Current active step ID */
  currentStepId?: string;
  /** Whether to show executive function notes */
  showExecutiveFunctionNotes?: boolean;
  /** Whether to show accommodation suggestions */
  showAccommodationSuggestions?: boolean;
  /** Whether to auto-advance to next step when current is completed */
  autoAdvance?: boolean;
  /** Callback when step is completed */
  onStepComplete?: (stepId: string) => void;
  /** Callback when workflow is completed */
  onWorkflowComplete?: () => void;
  /** Custom CSS class name */
  className?: string;
}

export const WorkflowGuide: React.FC<WorkflowGuideProps> = ({
  steps,
  currentStepId,
  showExecutiveFunctionNotes = true,
  showAccommodationSuggestions = true,
  autoAdvance = false,
  onStepComplete,
  onWorkflowComplete,
  className = ''
}) => {
  const [localCurrentStep, setLocalCurrentStep] = useState<string | null>(
    currentStepId || steps.find(step => step.is_current)?.step_id || steps[0]?.step_id || null
  );

  const currentStep = steps.find(step => step.step_id === localCurrentStep);
  const currentStepIndex = steps.findIndex(step => step.step_id === localCurrentStep);
  const completedSteps = steps.filter(step => step.is_completed).length;
  const totalSteps = steps.length;
  const progressPercentage = totalSteps > 0 ? (completedSteps / totalSteps) * 100 : 0;

  useEffect(() => {
    if (currentStepId && currentStepId !== localCurrentStep) {
      setLocalCurrentStep(currentStepId);
    }
  }, [currentStepId, localCurrentStep]);

  const handleStepComplete = () => {
    if (!currentStep) return;

    onStepComplete?.(currentStep.step_id);

    if (autoAdvance && currentStepIndex < steps.length - 1) {
      const nextStep = steps[currentStepIndex + 1];
      setLocalCurrentStep(nextStep.step_id);
    } else if (currentStepIndex === steps.length - 1) {
      // This was the last step
      onWorkflowComplete?.();
    }
  };

  const navigateToStep = (stepId: string) => {
    setLocalCurrentStep(stepId);
  };

  const formatDuration = (minutes: number): string => {
    if (minutes < 60) return `${minutes} min`;
    const hours = Math.floor(minutes / 60);
    const mins = minutes % 60;
    return mins > 0 ? `${hours}h ${mins}m` : `${hours}h`;
  };

  const getTotalEstimatedTime = (): number => {
    return steps.reduce((total, step) => total + step.estimated_duration, 0);
  };

  const getRemainingTime = (): number => {
    const currentIndex = currentStepIndex;
    if (currentIndex === -1) return 0;
    
    return steps
      .slice(currentIndex)
      .reduce((total, step) => total + step.estimated_duration, 0);
  };

  if (!steps.length) {
    return (
      <div className={`workflow-guide empty ${className}`}>
        <p>No workflow steps available.</p>
      </div>
    );
  }

  return (
    <div className={`mental-prosthetic-workflow-guide ${className}`}>
      {/* Progress Overview */}
      <div className="workflow-header">
        <h3>Workflow Progress</h3>
        <div className="progress-stats">
          <span className="step-counter">
            Step {currentStepIndex + 1} of {totalSteps}
          </span>
          <span className="completion-rate">
            {Math.round(progressPercentage)}% complete
          </span>
        </div>
        <div className="progress-bar">
          <div 
            className="progress-fill"
            style={{ width: `${progressPercentage}%` }}
          />
        </div>
        <div className="time-estimates">
          <span>Total: {formatDuration(getTotalEstimatedTime())}</span>
          <span>Remaining: {formatDuration(getRemainingTime())}</span>
        </div>
      </div>

      {/* Current Step Details */}
      {currentStep && (
        <div className="current-step">
          <div className="step-header">
            <h4>{currentStep.step_title}</h4>
            <span className="step-duration">
              ~{formatDuration(currentStep.estimated_duration)}
            </span>
          </div>
          
          <p className="step-description">{currentStep.step_description}</p>

          {currentStep.required_tools.length > 0 && (
            <div className="required-tools">
              <strong>Required tools:</strong>
              <ul>
                {currentStep.required_tools.map((tool, index) => (
                  <li key={index}>{tool}</li>
                ))}
              </ul>
            </div>
          )}

          {showExecutiveFunctionNotes && currentStep.executive_function_notes.length > 0 && (
            <div className="executive-function-notes">
              <strong>Executive Function Notes:</strong>
              <ul>
                {currentStep.executive_function_notes.map((note, index) => (
                  <li key={index}>{note}</li>
                ))}
              </ul>
            </div>
          )}

          {showAccommodationSuggestions && currentStep.accommodation_suggestions.length > 0 && (
            <div className="accommodation-suggestions">
              <strong>Accommodation Suggestions:</strong>
              <ul>
                {currentStep.accommodation_suggestions.map((suggestion, index) => (
                  <li key={index}>{suggestion}</li>
                ))}
              </ul>
            </div>
          )}

          <div className="step-actions">
            <button
              onClick={handleStepComplete}
              className="complete-step-btn"
              disabled={currentStep.is_completed}
            >
              {currentStep.is_completed ? '✓ Completed' : 'Mark Complete'}
            </button>
          </div>
        </div>
      )}

      {/* Step Navigation */}
      <div className="step-navigation">
        <h4>All Steps</h4>
        <div className="step-list">
          {steps.map((step, index) => (
            <button
              key={step.step_id}
              onClick={() => navigateToStep(step.step_id)}
              className={`step-nav-item ${
                step.step_id === localCurrentStep ? 'current' : ''
              } ${step.is_completed ? 'completed' : ''}`}
              aria-label={`Step ${index + 1}: ${step.step_title}`}
            >
              <span className="step-number">{index + 1}</span>
              <span className="step-title">{step.step_title}</span>
              <span className="step-status">
                {step.is_completed ? '✓' : step.step_id === localCurrentStep ? '→' : ''}
              </span>
            </button>
          ))}
        </div>
      </div>

      <style jsx>{`
        .mental-prosthetic-workflow-guide {
          border: 1px solid #e2e8f0;
          border-radius: 8px;
          padding: 20px;
          background: white;
          font-family: system-ui, -apple-system, sans-serif;
          max-width: 800px;
        }

        .workflow-header {
          margin-bottom: 24px;
          padding-bottom: 16px;
          border-bottom: 2px solid #f1f5f9;
        }

        .workflow-header h3 {
          margin: 0 0 12px 0;
          color: #1e293b;
        }

        .progress-stats {
          display: flex;
          justify-content: space-between;
          margin-bottom: 8px;
          font-size: 14px;
          color: #64748b;
        }

        .progress-bar {
          width: 100%;
          height: 12px;
          background: #f1f5f9;
          border-radius: 6px;
          overflow: hidden;
          margin-bottom: 8px;
        }

        .progress-fill {
          height: 100%;
          background: linear-gradient(90deg, #3b82f6, #1d4ed8);
          transition: width 0.3s ease;
        }

        .time-estimates {
          display: flex;
          gap: 16px;
          font-size: 14px;
          color: #64748b;
        }

        .current-step {
          background: #f8fafc;
          border: 2px solid #3b82f6;
          border-radius: 8px;
          padding: 20px;
          margin-bottom: 24px;
        }

        .step-header {
          display: flex;
          justify-content: space-between;
          align-items: flex-start;
          margin-bottom: 12px;
        }

        .step-header h4 {
          margin: 0;
          color: #1e293b;
          font-size: 18px;
        }

        .step-duration {
          background: #dbeafe;
          color: #1e40af;
          padding: 4px 8px;
          border-radius: 4px;
          font-size: 12px;
          font-weight: 500;
        }

        .step-description {
          color: #374151;
          line-height: 1.6;
          margin-bottom: 16px;
        }

        .required-tools,
        .executive-function-notes,
        .accommodation-suggestions {
          margin-bottom: 16px;
        }

        .required-tools strong,
        .executive-function-notes strong,
        .accommodation-suggestions strong {
          color: #374151;
          display: block;
          margin-bottom: 8px;
        }

        .required-tools ul,
        .executive-function-notes ul,
        .accommodation-suggestions ul {
          margin: 0;
          padding-left: 20px;
        }

        .required-tools li,
        .executive-function-notes li,
        .accommodation-suggestions li {
          margin: 4px 0;
          color: #64748b;
        }

        .executive-function-notes {
          background: #fef3c7;
          padding: 12px;
          border-radius: 6px;
          border-left: 4px solid #f59e0b;
        }

        .accommodation-suggestions {
          background: #ecfdf5;
          padding: 12px;
          border-radius: 6px;
          border-left: 4px solid #10b981;
        }

        .step-actions {
          display: flex;
          gap: 12px;
          margin-top: 16px;
        }

        .complete-step-btn {
          background: #22c55e;
          color: white;
          border: none;
          padding: 10px 20px;
          border-radius: 6px;
          font-size: 14px;
          font-weight: 500;
          cursor: pointer;
          transition: all 0.15s ease;
        }

        .complete-step-btn:hover:not(:disabled) {
          background: #16a34a;
          transform: translateY(-1px);
        }

        .complete-step-btn:disabled {
          background: #94a3b8;
          cursor: not-allowed;
        }

        .step-navigation h4 {
          margin: 0 0 12px 0;
          color: #374151;
        }

        .step-list {
          display: flex;
          flex-direction: column;
          gap: 4px;
        }

        .step-nav-item {
          display: flex;
          align-items: center;
          gap: 12px;
          padding: 12px;
          border: 1px solid #e2e8f0;
          border-radius: 6px;
          background: white;
          cursor: pointer;
          transition: all 0.15s ease;
          text-align: left;
        }

        .step-nav-item:hover {
          border-color: #cbd5e1;
          box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }

        .step-nav-item.current {
          border-color: #3b82f6;
          background: #dbeafe;
        }

        .step-nav-item.completed {
          background: #f0fdf4;
          border-color: #22c55e;
        }

        .step-number {
          display: flex;
          align-items: center;
          justify-content: center;
          width: 24px;
          height: 24px;
          background: #f1f5f9;
          border-radius: 50%;
          font-size: 12px;
          font-weight: 600;
          color: #64748b;
        }

        .step-nav-item.current .step-number {
          background: #3b82f6;
          color: white;
        }

        .step-nav-item.completed .step-number {
          background: #22c55e;
          color: white;
        }

        .step-title {
          flex: 1;
          font-size: 14px;
          color: #374151;
        }

        .step-status {
          font-size: 16px;
          color: #64748b;
        }

        .step-nav-item.current .step-status {
          color: #3b82f6;
        }

        .step-nav-item.completed .step-status {
          color: #22c55e;
        }
      `}</style>
    </div>
  );
};