/**
 * Workflow Builder Component
 * 
 * Interface for generating n8n workflows from detected patterns
 * with user approval workflow and customization options.
 */

import {
    Alert,
    AlertCircle,
    AlertDescription,
    Badge,
    Button,
    Card,
    CardContent,
    CardHeader,
    CardTitle,
    CheckCircle,
    Download,
    Input,
    Label,
    Play,
    Progress,
    Settings,
    Switch,
    Textarea
} from '@/components/ui';
import React, { useEffect, useState } from 'react';

interface WorkflowPattern {
  id: string;
  pattern_name: string;
  description: string;
  category: string;
  occurrence_count: number;
  confidence_score: number;
  tool_sequence: string[];
}

interface GeneratedWorkflow {
  id: string;
  workflow_id: string;
  workflow_name: string;
  description: string;
  category: string;
  is_active: boolean;
  is_validated: boolean;
  generation_confidence: number;
}

interface WorkflowBuilderProps {
  pattern?: WorkflowPattern;
  onWorkflowGenerated?: (workflow: GeneratedWorkflow) => void;
  onClose?: () => void;
}

export const WorkflowBuilder: React.FC<WorkflowBuilderProps> = ({
  pattern,
  onWorkflowGenerated,
  onClose
}) => {
  const [workflowName, setWorkflowName] = useState('');
  const [workflowDescription, setWorkflowDescription] = useState('');
  const [autoActivate, setAutoActivate] = useState(false);
  const [isGenerating, setIsGenerating] = useState(false);
  const [isValidating, setIsValidating] = useState(false);
  const [generatedWorkflow, setGeneratedWorkflow] = useState<GeneratedWorkflow | null>(null);
  const [validationResult, setValidationResult] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);
  const [currentStep, setCurrentStep] = useState<'configure' | 'generate' | 'validate' | 'complete'>('configure');

  useEffect(() => {
    if (pattern) {
      setWorkflowName(`Auto-${pattern.pattern_name}`);
      setWorkflowDescription(
        `Automated workflow for ${pattern.pattern_name}. ` +
        `Detected ${pattern.occurrence_count} times with ${Math.round(pattern.confidence_score * 100)}% confidence.`
      );
    }
  }, [pattern]);

  const generateWorkflow = async () => {
    if (!pattern) return;

    try {
      setIsGenerating(true);
      setError(null);
      setCurrentStep('generate');

      const response = await fetch('/api/adaptive-workflows/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          pattern_id: pattern.id,
          workflow_name: workflowName || undefined,
          auto_activate: autoActivate
        })
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to generate workflow');
      }

      const workflow = await response.json();
      setGeneratedWorkflow(workflow);
      
      // Auto-validate if not auto-activated
      if (!autoActivate) {
        setCurrentStep('validate');
        await validateWorkflow(workflow.workflow_id);
      } else {
        setCurrentStep('complete');
      }

      onWorkflowGenerated?.(workflow);

    } catch (err) {
      setError(err instanceof Error ? err.message : 'Generation failed');
      setCurrentStep('configure');
    } finally {
      setIsGenerating(false);
    }
  };

  const validateWorkflow = async (workflowId: string) => {
    try {
      setIsValidating(true);
      setError(null);

      const response = await fetch('/api/adaptive-workflows/validate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          workflow_id: workflowId,
          test_historical_data: true,
          max_test_scenarios: 10
        })
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Validation failed');
      }

      const result = await response.json();
      setValidationResult(result);
      setCurrentStep('complete');

    } catch (err) {
      setError(err instanceof Error ? err.message : 'Validation failed');
    } finally {
      setIsValidating(false);
    }
  };

  const exportWorkflow = async () => {
    if (!generatedWorkflow) return;

    try {
      const response = await fetch(
        `/api/adaptive-workflows/workflows/${generatedWorkflow.workflow_id}/export`
      );

      if (!response.ok) {
        throw new Error('Failed to export workflow');
      }

      const workflowData = await response.json();
      
      // Download as JSON file
      const blob = new Blob([JSON.stringify(workflowData, null, 2)], {
        type: 'application/json'
      });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `${generatedWorkflow.workflow_name}.json`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);

    } catch (err) {
      setError(err instanceof Error ? err.message : 'Export failed');
    }
  };

  const activateWorkflow = async () => {
    if (!generatedWorkflow) return;

    try {
      const response = await fetch(
        `/api/adaptive-workflows/workflows/${generatedWorkflow.workflow_id}/activate`,
        { method: 'PUT' }
      );

      if (!response.ok) {
        throw new Error('Failed to activate workflow');
      }

      setGeneratedWorkflow({
        ...generatedWorkflow,
        is_active: true
      });

    } catch (err) {
      setError(err instanceof Error ? err.message : 'Activation failed');
    }
  };

  const getStepStatus = (step: string) => {
    const steps = ['configure', 'generate', 'validate', 'complete'];
    const currentIndex = steps.indexOf(currentStep);
    const stepIndex = steps.indexOf(step);
    
    if (stepIndex < currentIndex) return 'completed';
    if (stepIndex === currentIndex) return 'current';
    return 'pending';
  };

  if (!pattern) {
    return (
      <Card>
        <CardContent className="pt-6">
          <div className="text-center text-gray-500">
            <Settings className="h-12 w-12 mx-auto mb-4 opacity-50" />
            <p>Select a pattern to generate a workflow</p>
          </div>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card className="w-full max-w-4xl">
      <CardHeader>
        <CardTitle className="flex items-center justify-between">
          <span>Workflow Builder</span>
          {onClose && (
            <Button variant="outline" size="sm" onClick={onClose}>
              Close
            </Button>
          )}
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-6">
        {/* Progress Steps */}
        <div className="flex items-center justify-between">
          {[
            { step: 'configure', label: 'Configure', icon: Settings },
            { step: 'generate', label: 'Generate', icon: Play },
            { step: 'validate', label: 'Validate', icon: CheckCircle },
            { step: 'complete', label: 'Complete', icon: Download }
          ].map(({ step, label, icon: Icon }, index) => {
            const status = getStepStatus(step);
            return (
              <div key={step} className="flex items-center">
                <div className={`
                  flex items-center justify-center w-10 h-10 rounded-full border-2
                  ${status === 'completed' ? 'bg-green-500 border-green-500 text-white' :
                    status === 'current' ? 'bg-blue-500 border-blue-500 text-white' :
                    'bg-gray-100 border-gray-300 text-gray-500'}
                `}>
                  <Icon className="h-5 w-5" />
                </div>
                <div className="ml-2 text-sm font-medium">
                  {label}
                </div>
                {index < 3 && (
                  <div className={`
                    ml-4 h-0.5 w-16
                    ${status === 'completed' ? 'bg-green-500' : 'bg-gray-300'}
                  `} />
                )}
              </div>
            );
          })}
        </div>

        {/* Error Display */}
        {error && (
          <Alert variant="destructive">
            <AlertCircle className="h-4 w-4" />
            <AlertDescription>{error}</AlertDescription>
          </Alert>
        )}

        {/* Pattern Information */}
        <Card>
          <CardHeader>
            <CardTitle className="text-lg">Source Pattern</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <Label className="text-sm font-medium">Pattern Name</Label>
                <p className="text-sm text-gray-600">{pattern.pattern_name}</p>
              </div>
              <div>
                <Label className="text-sm font-medium">Category</Label>
                <Badge className="ml-2">{pattern.category}</Badge>
              </div>
              <div>
                <Label className="text-sm font-medium">Occurrences</Label>
                <p className="text-sm text-gray-600">{pattern.occurrence_count}</p>
              </div>
              <div>
                <Label className="text-sm font-medium">Confidence</Label>
                <div className="flex items-center gap-2">
                  <Progress value={pattern.confidence_score * 100} className="w-20" />
                  <span className="text-sm">{Math.round(pattern.confidence_score * 100)}%</span>
                </div>
              </div>
              <div className="col-span-2">
                <Label className="text-sm font-medium">Tools</Label>
                <div className="flex flex-wrap gap-1 mt-1">
                  {pattern.tool_sequence.map((tool, index) => (
                    <Badge key={index} variant="outline" className="text-xs">
                      {tool}
                    </Badge>
                  ))}
                </div>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Configuration Step */}
        {currentStep === 'configure' && (
          <Card>
            <CardHeader>
              <CardTitle className="text-lg">Workflow Configuration</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div>
                <Label htmlFor="workflow-name">Workflow Name</Label>
                <Input
                  id="workflow-name"
                  value={workflowName}
                  onChange={(e) => setWorkflowName(e.target.value)}
                  placeholder="Enter workflow name"
                />
              </div>

              <div>
                <Label htmlFor="workflow-description">Description</Label>
                <Textarea
                  id="workflow-description"
                  value={workflowDescription}
                  onChange={(e) => setWorkflowDescription(e.target.value)}
                  placeholder="Describe what this workflow does"
                  rows={3}
                />
              </div>

              <div className="flex items-center space-x-2">
                <Switch
                  id="auto-activate"
                  checked={autoActivate}
                  onCheckedChange={setAutoActivate}
                />
                <Label htmlFor="auto-activate">
                  Activate immediately (skip validation)
                </Label>
              </div>

              <Button
                onClick={generateWorkflow}
                disabled={isGenerating || !workflowName.trim()}
                className="w-full"
              >
                {isGenerating ? 'Generating Workflow...' : 'Generate Workflow'}
              </Button>
            </CardContent>
          </Card>
        )}

        {/* Generation Progress */}
        {currentStep === 'generate' && isGenerating && (
          <Card>
            <CardContent className="pt-6">
              <div className="text-center">
                <div className="animate-spin h-8 w-8 border-4 border-blue-500 border-t-transparent rounded-full mx-auto mb-4" />
                <p className="text-lg font-medium">Generating Workflow...</p>
                <p className="text-sm text-gray-600">
                  Creating n8n workflow from pattern analysis
                </p>
              </div>
            </CardContent>
          </Card>
        )}

        {/* Validation Progress */}
        {currentStep === 'validate' && isValidating && (
          <Card>
            <CardContent className="pt-6">
              <div className="text-center">
                <div className="animate-pulse h-8 w-8 bg-blue-500 rounded-full mx-auto mb-4" />
                <p className="text-lg font-medium">Validating Workflow...</p>
                <p className="text-sm text-gray-600">
                  Testing against historical data
                </p>
              </div>
            </CardContent>
          </Card>
        )}

        {/* Completion Step */}
        {currentStep === 'complete' && generatedWorkflow && (
          <Card>
            <CardHeader>
              <CardTitle className="text-lg flex items-center gap-2">
                <CheckCircle className="h-5 w-5 text-green-600" />
                Workflow Generated Successfully
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <Label className="text-sm font-medium">Workflow Name</Label>
                  <p className="text-sm text-gray-600">{generatedWorkflow.workflow_name}</p>
                </div>
                <div>
                  <Label className="text-sm font-medium">Status</Label>
                  <Badge className={generatedWorkflow.is_active ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'}>
                    {generatedWorkflow.is_active ? 'Active' : 'Inactive'}
                  </Badge>
                </div>
              </div>

              {validationResult && (
                <div className="border rounded-lg p-4">
                  <h4 className="font-medium mb-2">Validation Results</h4>
                  <div className="grid grid-cols-2 gap-4 text-sm">
                    <div>
                      <span className="text-gray-600">Success Rate:</span>
                      <span className="ml-2 font-medium">
                        {Math.round(validationResult.success_rate * 100)}%
                      </span>
                    </div>
                    <div>
                      <span className="text-gray-600">Test Count:</span>
                      <span className="ml-2 font-medium">{validationResult.test_count}</span>
                    </div>
                    <div>
                      <span className="text-gray-600">Avg Time:</span>
                      <span className="ml-2 font-medium">
                        {validationResult.average_execution_time.toFixed(2)}s
                      </span>
                    </div>
                    <div>
                      <span className="text-gray-600">Valid:</span>
                      <Badge className={validationResult.is_valid ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}>
                        {validationResult.is_valid ? 'Yes' : 'No'}
                      </Badge>
                    </div>
                  </div>
                  <p className="text-sm text-gray-600 mt-2">
                    {validationResult.recommendation}
                  </p>
                </div>
              )}

              <div className="flex gap-2">
                <Button onClick={exportWorkflow} variant="outline">
                  <Download className="h-4 w-4 mr-2" />
                  Export for n8n
                </Button>
                
                {!generatedWorkflow.is_active && validationResult?.is_valid && (
                  <Button onClick={activateWorkflow}>
                    <Play className="h-4 w-4 mr-2" />
                    Activate Workflow
                  </Button>
                )}
              </div>
            </CardContent>
          </Card>
        )}
      </CardContent>
    </Card>
  );
};

export default WorkflowBuilder;