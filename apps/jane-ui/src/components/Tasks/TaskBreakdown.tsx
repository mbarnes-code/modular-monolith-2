'use client';

import { useState } from 'react';

interface SubTask {
  id: string;
  title: string;
  description: string;
  estimatedMinutes: number;
  domain: 'security' | 'productivity' | 'mtg' | 'infrastructure';
  tools: string[];
  completed: boolean;
  dependencies?: string[];
}

interface TaskBreakdownData {
  originalTask: string;
  complexity: 'low' | 'medium' | 'high';
  totalEstimatedMinutes: number;
  subTasks: SubTask[];
  suggestedOrder: string[];
  executiveFunctionNotes: string[];
}

interface TaskBreakdownProps {
  className?: string;
  initialTask?: string;
  onTaskUpdate?: (breakdown: TaskBreakdownData) => void;
  onSubTaskComplete?: (subTaskId: string) => void;
}

export function TaskBreakdown({
  className = '',
  initialTask = '',
  onTaskUpdate,
  onSubTaskComplete
}: TaskBreakdownProps) {
  const [originalTask, setOriginalTask] = useState(initialTask);
  const [breakdown, setBreakdown] = useState<TaskBreakdownData | null>(null);
  const [isGenerating, setIsGenerating] = useState(false);
  const [activeSubTask, setActiveSubTask] = useState<string | null>(null);

  const generateBreakdown = async () => {
    if (!originalTask.trim()) return;
    
    setIsGenerating(true);
    
    // Simulate AI task breakdown generation
    setTimeout(() => {
      const mockBreakdown: TaskBreakdownData = {
        originalTask: originalTask.trim(),
        complexity: originalTask.length > 100 ? 'high' : originalTask.length > 50 ? 'medium' : 'low',
        totalEstimatedMinutes: 0,
        subTasks: generateMockSubTasks(originalTask.trim()),
        suggestedOrder: [],
        executiveFunctionNotes: [
          'Break tasks into 25-minute focused sessions',
          'Take 5-minute breaks between subtasks',
          'Use timers to maintain focus',
          'Check off completed items for dopamine boost'
        ]
      };
      
      mockBreakdown.totalEstimatedMinutes = mockBreakdown.subTasks.reduce(
        (total, task) => total + task.estimatedMinutes, 
        0
      );
      
      mockBreakdown.suggestedOrder = mockBreakdown.subTasks
        .sort((a, b) => {
          // Sort by dependencies first, then by domain priority
          const domainPriority = { security: 1, productivity: 2, mtg: 3, infrastructure: 4 };
          return domainPriority[a.domain] - domainPriority[b.domain];
        })
        .map(task => task.id);
      
      setBreakdown(mockBreakdown);
      setIsGenerating(false);
      
      if (onTaskUpdate) {
        onTaskUpdate(mockBreakdown);
      }
    }, 2000);
  };

  const generateMockSubTasks = (task: string): SubTask[] => {
    const baseSubTasks: Partial<SubTask>[] = [];
    
    if (task.toLowerCase().includes('security') || task.toLowerCase().includes('threat')) {
      baseSubTasks.push(
        { title: 'Gather Threat Intelligence', domain: 'security', tools: ['MISP', 'HELK'], estimatedMinutes: 20 },
        { title: 'Analyze IOCs', domain: 'security', tools: ['YARA-X'], estimatedMinutes: 30 },
        { title: 'Generate Report', domain: 'productivity', tools: ['n8n'], estimatedMinutes: 15 }
      );
    } else if (task.toLowerCase().includes('productivity') || task.toLowerCase().includes('workflow')) {
      baseSubTasks.push(
        { title: 'Map Current Process', domain: 'productivity', tools: ['n8n'], estimatedMinutes: 25 },
        { title: 'Identify Optimization Points', domain: 'productivity', tools: ['Actual Budget'], estimatedMinutes: 20 },
        { title: 'Implement Automation', domain: 'productivity', tools: ['n8n'], estimatedMinutes: 45 }
      );
    } else {
      // Generic task breakdown
      baseSubTasks.push(
        { title: 'Research and Planning', domain: 'productivity', tools: ['Inspector'], estimatedMinutes: 20 },
        { title: 'Execute Core Work', domain: 'productivity', tools: [], estimatedMinutes: 30 },
        { title: 'Review and Document', domain: 'productivity', tools: ['n8n'], estimatedMinutes: 15 }
      );
    }
    
    return baseSubTasks.map((task, index) => ({
      id: `subtask-${index + 1}`,
      title: task.title || '',
      description: `Detailed description for ${task.title}`,
      domain: task.domain || 'productivity',
      tools: task.tools || [],
      estimatedMinutes: task.estimatedMinutes || 20,
      completed: false
    } as SubTask));
  };

  const handleSubTaskToggle = (subTaskId: string) => {
    if (!breakdown) return;
    
    const updatedSubTasks = breakdown.subTasks.map(task => 
      task.id === subTaskId ? { ...task, completed: !task.completed } : task
    );
    
    const updatedBreakdown = { ...breakdown, subTasks: updatedSubTasks };
    setBreakdown(updatedBreakdown);
    
    if (onSubTaskComplete) {
      onSubTaskComplete(subTaskId);
    }
  };

  const getDomainColor = (domain: string) => {
    switch (domain) {
      case 'security': return 'border-red-200 bg-red-50 text-red-700';
      case 'productivity': return 'border-green-200 bg-green-50 text-green-700';
      case 'mtg': return 'border-purple-200 bg-purple-50 text-purple-700';
      case 'infrastructure': return 'border-blue-200 bg-blue-50 text-blue-700';
      default: return 'border-gray-200 bg-gray-50 text-gray-700';
    }
  };

  const getComplexityColor = (complexity: string) => {
    switch (complexity) {
      case 'low': return 'text-green-600 bg-green-100';
      case 'medium': return 'text-yellow-600 bg-yellow-100';
      case 'high': return 'text-red-600 bg-red-100';
      default: return 'text-gray-600 bg-gray-100';
    }
  };

  const completedTasks = breakdown?.subTasks.filter(task => task.completed).length || 0;
  const totalTasks = breakdown?.subTasks.length || 0;
  const progressPercentage = totalTasks > 0 ? (completedTasks / totalTasks) * 100 : 0;

  return (
    <div className={`bg-white border rounded-lg shadow-sm ${className}`}>
      {/* Header */}
      <div className="border-b p-4">
        <h3 className="font-semibold text-gray-900 mb-3">AI Task Breakdown</h3>
        
        {/* Task input */}
        <div className="space-y-3">
          <textarea
            value={originalTask}
            onChange={(e) => setOriginalTask(e.target.value)}
            placeholder="Describe your task or goal..."
            className="w-full border rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-blue-500 resize-none"
            rows={3}
          />
          <button
            onClick={generateBreakdown}
            disabled={!originalTask.trim() || isGenerating}
            className="bg-blue-600 text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {isGenerating ? 'Generating Breakdown...' : 'Break Down Task'}
          </button>
        </div>
      </div>

      {/* Loading State */}
      {isGenerating && (
        <div className="p-6 text-center">
          <div className="flex items-center justify-center mb-4">
            <div className="flex space-x-1">
              <div className="w-3 h-3 bg-blue-400 rounded-full animate-pulse"></div>
              <div className="w-3 h-3 bg-blue-400 rounded-full animate-pulse" style={{animationDelay: '0.2s'}}></div>
              <div className="w-3 h-3 bg-blue-400 rounded-full animate-pulse" style={{animationDelay: '0.4s'}}></div>
            </div>
          </div>
          <p className="text-sm text-gray-600">AI is analyzing your task and creating an optimized breakdown...</p>
        </div>
      )}

      {/* Breakdown Results */}
      {breakdown && !isGenerating && (
        <div className="p-4 space-y-4">
          {/* Overview */}
          <div className="bg-gray-50 rounded-lg p-4">
            <div className="flex items-center justify-between mb-3">
              <h4 className="font-medium text-gray-900">Task Overview</h4>
              <span className={`text-xs px-2 py-1 rounded-full ${getComplexityColor(breakdown.complexity)}`}>
                {breakdown.complexity} complexity
              </span>
            </div>
            
            <div className="grid grid-cols-2 gap-4 text-sm">
              <div>
                <span className="text-gray-600">Total subtasks:</span>
                <span className="ml-2 font-medium">{breakdown.subTasks.length}</span>
              </div>
              <div>
                <span className="text-gray-600">Estimated time:</span>
                <span className="ml-2 font-medium">{breakdown.totalEstimatedMinutes} min</span>
              </div>
            </div>
            
            {/* Progress bar */}
            <div className="mt-3">
              <div className="flex justify-between text-xs text-gray-600 mb-1">
                <span>Progress</span>
                <span>{completedTasks}/{totalTasks} completed</span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div 
                  className="bg-blue-600 h-2 rounded-full transition-all duration-300"
                  style={{ width: `${progressPercentage}%` }}
                ></div>
              </div>
            </div>
          </div>

          {/* Executive Function Notes */}
          <div className="bg-blue-50 rounded-lg p-4">
            <h4 className="font-medium text-blue-900 mb-2">Executive Function Tips</h4>
            <ul className="space-y-1 text-sm text-blue-800">
              {breakdown.executiveFunctionNotes.map((note, index) => (
                <li key={index} className="flex items-start gap-2">
                  <span className="text-blue-600 mt-1">•</span>
                  <span>{note}</span>
                </li>
              ))}
            </ul>
          </div>

          {/* Subtasks */}
          <div className="space-y-3">
            <h4 className="font-medium text-gray-900">Subtasks</h4>
            
            {breakdown.subTasks.map((subTask, index) => (
              <div
                key={subTask.id}
                className={`border rounded-lg p-4 transition-all duration-200 ${
                  activeSubTask === subTask.id ? 'border-blue-300 bg-blue-50' : 'border-gray-200'
                } ${subTask.completed ? 'opacity-75' : ''}`}
                onClick={() => setActiveSubTask(activeSubTask === subTask.id ? null : subTask.id)}
              >
                <div className="flex items-start gap-3">
                  {/* Checkbox */}
                  <input
                    type="checkbox"
                    checked={subTask.completed}
                    onChange={() => handleSubTaskToggle(subTask.id)}
                    className="mt-1 w-4 h-4 text-blue-600 rounded focus:ring-blue-500"
                    onClick={(e) => e.stopPropagation()}
                  />
                  
                  <div className="flex-1">
                    {/* Task header */}
                    <div className="flex items-start justify-between">
                      <div>
                        <h5 className={`font-medium text-sm ${subTask.completed ? 'line-through text-gray-500' : 'text-gray-900'}`}>
                          {index + 1}. {subTask.title}
                        </h5>
                        <p className="text-xs text-gray-600 mt-1">
                          {subTask.description}
                        </p>
                      </div>
                      
                      <div className="flex items-center gap-2">
                        <span className={`text-xs px-2 py-1 rounded ${getDomainColor(subTask.domain)}`}>
                          {subTask.domain}
                        </span>
                        <span className="text-xs text-gray-500">
                          {subTask.estimatedMinutes}min
                        </span>
                      </div>
                    </div>
                    
                    {/* Tools */}
                    {subTask.tools.length > 0 && (
                      <div className="mt-2 flex flex-wrap gap-1">
                        <span className="text-xs text-gray-500">Tools:</span>
                        {subTask.tools.map((tool, toolIndex) => (
                          <span 
                            key={toolIndex}
                            className="text-xs bg-gray-100 text-gray-700 px-2 py-1 rounded"
                          >
                            {tool}
                          </span>
                        ))}
                      </div>
                    )}
                    
                    {/* Expanded details */}
                    {activeSubTask === subTask.id && (
                      <div className="mt-3 pt-3 border-t border-gray-200">
                        <div className="text-xs text-gray-600 space-y-1">
                          <p><strong>Focus time:</strong> {subTask.estimatedMinutes} minutes</p>
                          <p><strong>Domain:</strong> {subTask.domain}</p>
                          <p><strong>Executive function tip:</strong> Set a timer and work in focused bursts</p>
                        </div>
                      </div>
                    )}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
      
      {/* Empty state */}
      {!breakdown && !isGenerating && (
        <div className="p-8 text-center text-gray-500">
          <div className="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <span className="text-2xl">🎯</span>
          </div>
          <p className="text-sm mb-2">AI-Powered Task Breakdown</p>
          <p className="text-xs">
            Enter a task above and I'll break it down into manageable steps
            with executive function support
          </p>
        </div>
      )}
    </div>
  );
}

export default TaskBreakdown;