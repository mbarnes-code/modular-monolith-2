'use client';

import { AIChat, AIContextProvider, AISuggestions } from '@/components/AI';
import { Reminders, TaskBreakdown } from '@/components/Tasks';
import { useEffect, useState } from 'react';

interface ContextData {
  activeTool?: string;
  currentWorkspace?: string;
  activeProjects: string[];
  recentActivity: string[];
  userPreferences: {
    preferredDomains: string[];
    workingStyle: 'focused' | 'multitask' | 'structured';
    reminderFrequency: 'minimal' | 'moderate' | 'frequent';
  };
}

export default function AIAssistantPage() {
  const [contextData, setContextData] = useState<ContextData>({
    activeProjects: [],
    recentActivity: [],
    userPreferences: {
      preferredDomains: ['security', 'productivity'],
      workingStyle: 'focused',
      reminderFrequency: 'moderate'
    }
  });
  const [activeView, setActiveView] = useState<'chat' | 'breakdown' | 'reminders'>('chat');
  const [isExpanded, setIsExpanded] = useState(false);

  // Load user context and recent activity
  useEffect(() => {
    loadUserContext();
  }, []);

  const loadUserContext = async () => {
    // Simulate loading user context from various sources
    const mockContext: ContextData = {
      activeTool: 'MISP',
      currentWorkspace: 'Threat Analysis',
      activeProjects: [
        'Q4 Security Assessment',
        'MTG Deck Optimization',
        'Infrastructure Monitoring Setup'
      ],
      recentActivity: [
        'Analyzed IoCs in MISP',
        'Created workflow in n8n',
        'Reviewed security alerts',
        'Updated task reminders'
      ],
      userPreferences: {
        preferredDomains: ['security', 'productivity', 'infrastructure'],
        workingStyle: 'focused',
        reminderFrequency: 'moderate'
      }
    };
    
    setContextData(mockContext);
  };

  const handleSuggestionApply = (suggestion: any) => {
    // Handle applying AI suggestions
    console.log('Applying suggestion:', suggestion);
    
    // Could trigger specific actions based on suggestion type
    switch (suggestion.action) {
      case 'break_down_task':
        setActiveView('breakdown');
        break;
      case 'schedule_focus':
        setActiveView('reminders');
        break;
      case 'correlate_iocs':
        // Navigate to MISP or trigger correlation workflow
        break;
      default:
        // General handling
        break;
    }
  };

  const handleReminderAction = (reminderId: string, action: string) => {
    console.log('Reminder action:', reminderId, action);
    // Handle reminder actions - could update backend state
  };

  const handleTaskUpdate = (breakdown: any) => {
    console.log('Task breakdown updated:', breakdown);
    // Handle task breakdown updates
  };

  const getActiveContext = (): string[] => {
    const context: string[] = [];
    
    if (contextData.activeTool) {
      context.push(`tool:${contextData.activeTool}`);
    }
    
    if (contextData.currentWorkspace) {
      context.push(`workspace:${contextData.currentWorkspace}`);
    }
    
    contextData.activeProjects.forEach(project => {
      context.push(`project:${project}`);
    });
    
    context.push(`style:${contextData.userPreferences.workingStyle}`);
    
    return context;
  };

  return (
    <AIContextProvider 
      activeTool={contextData.activeTool}
      activeContext={getActiveContext()}
    >
      <div className="min-h-screen bg-gray-50">
        {/* Header */}
        <div className="bg-white border-b shadow-sm">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex items-center justify-between h-16">
              <div className="flex items-center gap-4">
                <h1 className="text-xl font-semibold text-gray-900">AI Assistant</h1>
                
                {/* Context indicators */}
                <div className="flex items-center gap-2">
                  {contextData.activeTool && (
                    <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                      {contextData.activeTool}
                    </span>
                  )}
                  {contextData.currentWorkspace && (
                    <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                      {contextData.currentWorkspace}
                    </span>
                  )}
                </div>
              </div>
              
              <div className="flex items-center gap-4">
                {/* View toggles */}
                <div className="flex bg-gray-100 rounded-lg p-1">
                  <button
                    onClick={() => setActiveView('chat')}
                    className={`px-3 py-1.5 text-sm font-medium rounded-md transition-colors ${
                      activeView === 'chat'
                        ? 'bg-white text-gray-900 shadow-sm'
                        : 'text-gray-600 hover:text-gray-900'
                    }`}
                  >
                    Chat
                  </button>
                  <button
                    onClick={() => setActiveView('breakdown')}
                    className={`px-3 py-1.5 text-sm font-medium rounded-md transition-colors ${
                      activeView === 'breakdown'
                        ? 'bg-white text-gray-900 shadow-sm'
                        : 'text-gray-600 hover:text-gray-900'
                    }`}
                  >
                    Tasks
                  </button>
                  <button
                    onClick={() => setActiveView('reminders')}
                    className={`px-3 py-1.5 text-sm font-medium rounded-md transition-colors ${
                      activeView === 'reminders'
                        ? 'bg-white text-gray-900 shadow-sm'
                        : 'text-gray-600 hover:text-gray-900'
                    }`}
                  >
                    Reminders
                  </button>
                </div>
                
                {/* Expand toggle */}
                <button
                  onClick={() => setIsExpanded(!isExpanded)}
                  className="text-gray-400 hover:text-gray-600"
                >
                  <span className="sr-only">
                    {isExpanded ? 'Collapse' : 'Expand'} interface
                  </span>
                  {isExpanded ? '⌄' : '⌃'}
                </button>
              </div>
            </div>
          </div>
        </div>

        {/* Main content */}
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className={`grid gap-6 ${isExpanded ? 'grid-cols-1' : 'grid-cols-1 lg:grid-cols-3'}`}>
            {/* Left sidebar - Context & Suggestions */}
            {!isExpanded && (
              <div className="space-y-6">
                {/* Current Context */}
                <div className="bg-white border rounded-lg shadow-sm p-4">
                  <h3 className="font-semibold text-gray-900 mb-3">Current Context</h3>
                  
                  <div className="space-y-3">
                    {contextData.activeTool && (
                      <div>
                        <span className="text-sm font-medium text-gray-600">Active Tool:</span>
                        <span className="ml-2 text-sm text-gray-900">{contextData.activeTool}</span>
                      </div>
                    )}
                    
                    {contextData.currentWorkspace && (
                      <div>
                        <span className="text-sm font-medium text-gray-600">Workspace:</span>
                        <span className="ml-2 text-sm text-gray-900">{contextData.currentWorkspace}</span>
                      </div>
                    )}
                    
                    {contextData.activeProjects.length > 0 && (
                      <div>
                        <span className="text-sm font-medium text-gray-600">Active Projects:</span>
                        <div className="mt-1 space-y-1">
                          {contextData.activeProjects.map((project, index) => (
                            <div key={index} className="text-sm text-gray-700">
                              • {project}
                            </div>
                          ))}
                        </div>
                      </div>
                    )}
                    
                    {contextData.recentActivity.length > 0 && (
                      <div>
                        <span className="text-sm font-medium text-gray-600">Recent Activity:</span>
                        <div className="mt-1 space-y-1">
                          {contextData.recentActivity.slice(0, 3).map((activity, index) => (
                            <div key={index} className="text-xs text-gray-600">
                              • {activity}
                            </div>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                </div>

                {/* AI Suggestions */}
                <AISuggestions
                  activeTool={contextData.activeTool}
                  activeContext={getActiveContext()}
                  onApplySuggestion={handleSuggestionApply}
                />
              </div>
            )}

            {/* Main content area */}
            <div className={`${isExpanded ? 'col-span-1' : 'col-span-1 lg:col-span-2'}`}>
              {activeView === 'chat' && (
                <AIChat
                  className="h-[600px]"
                  activeTool={contextData.activeTool}
                  activeContext={getActiveContext()}
                />
              )}
              
              {activeView === 'breakdown' && (
                <TaskBreakdown
                  className="h-[600px]"
                  onTaskUpdate={handleTaskUpdate}
                />
              )}
              
              {activeView === 'reminders' && (
                <Reminders
                  className="h-[600px]"
                  onReminderAction={handleReminderAction}
                />
              )}
            </div>
          </div>

          {/* Executive Function Status Bar */}
          <div className="mt-6 bg-white border rounded-lg shadow-sm p-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-6">
                <div className="flex items-center gap-2">
                  <div className="w-3 h-3 bg-green-500 rounded-full"></div>
                  <span className="text-sm text-gray-600">Focus Mode: Active</span>
                </div>
                
                <div className="flex items-center gap-2">
                  <div className="w-3 h-3 bg-blue-500 rounded-full"></div>
                  <span className="text-sm text-gray-600">
                    Context: {getActiveContext().length} items
                  </span>
                </div>
                
                <div className="flex items-center gap-2">
                  <div className="w-3 h-3 bg-yellow-500 rounded-full"></div>
                  <span className="text-sm text-gray-600">
                    Working Style: {contextData.userPreferences.workingStyle}
                  </span>
                </div>
              </div>
              
              <div className="text-xs text-gray-500">
                Last updated: {new Date().toLocaleTimeString()}
              </div>
            </div>
          </div>
        </div>
      </div>
    </AIContextProvider>
  );
}