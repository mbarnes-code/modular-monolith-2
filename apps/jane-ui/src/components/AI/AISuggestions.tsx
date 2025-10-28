'use client';

import { useEffect, useState } from 'react';

interface Suggestion {
  id: string;
  title: string;
  description: string;
  action: string;
  priority: 'high' | 'medium' | 'low';
  tools?: string[];
  context?: string[];
}

interface AISuggestionsProps {
  className?: string;
  activeTool?: string;
  activeContext?: string[];
  onApplySuggestion?: (suggestion: Suggestion) => void;
}

export function AISuggestions({
  className = '',
  activeTool,
  activeContext = [],
  onApplySuggestion
}: AISuggestionsProps) {
  const [suggestions, setSuggestions] = useState<Suggestion[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [expanded, setExpanded] = useState(true);

  // Generate contextual suggestions based on active tool and context
  useEffect(() => {
    if (activeTool || activeContext.length > 0) {
      generateSuggestions();
    }
  }, [activeTool, activeContext]);

  const generateSuggestions = () => {
    setIsLoading(true);
    
    // Simulate AI suggestion generation
    setTimeout(() => {
      const mockSuggestions: Suggestion[] = [];
      
      if (activeTool === 'MISP') {
        mockSuggestions.push({
          id: 'misp-1',
          title: 'Create IOC Correlation',
          description: 'Based on recent threat data, consider creating correlations with YARA rules',
          action: 'correlate_iocs',
          priority: 'high',
          tools: ['MISP', 'YARA-X'],
          context: ['threat-intelligence', 'malware-analysis']
        });
      }
      
      if (activeContext.includes('task-management')) {
        mockSuggestions.push({
          id: 'task-1',
          title: 'Break Down Complex Task',
          description: 'This task seems complex. Would you like me to break it into smaller steps?',
          action: 'break_down_task',
          priority: 'medium',
          context: ['task-management', 'executive-function']
        });
      }
      
      // General productivity suggestions
      mockSuggestions.push({
        id: 'prod-1',
        title: 'Schedule Focus Time',
        description: 'You\'ve been context-switching frequently. Consider blocking time for deep work.',
        action: 'schedule_focus',
        priority: 'medium',
        context: ['productivity', 'executive-function']
      });
      
      setSuggestions(mockSuggestions);
      setIsLoading(false);
    }, 800);
  };

  const handleApplySuggestion = (suggestion: Suggestion) => {
    if (onApplySuggestion) {
      onApplySuggestion(suggestion);
    }
  };

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'high': return 'border-red-200 bg-red-50';
      case 'medium': return 'border-yellow-200 bg-yellow-50';
      case 'low': return 'border-gray-200 bg-gray-50';
      default: return 'border-gray-200 bg-gray-50';
    }
  };

  const getPriorityDot = (priority: string) => {
    switch (priority) {
      case 'high': return 'bg-red-500';
      case 'medium': return 'bg-yellow-500';
      case 'low': return 'bg-gray-500';
      default: return 'bg-gray-500';
    }
  };

  return (
    <div className={`bg-white border rounded-lg shadow-sm ${className}`}>
      {/* Header */}
      <div className="border-b p-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="w-6 h-6 bg-purple-100 rounded flex items-center justify-center">
              <span className="text-purple-600 text-xs">✨</span>
            </div>
            <h3 className="font-semibold text-gray-900">AI Suggestions</h3>
            {suggestions.length > 0 && (
              <span className="text-xs bg-purple-100 text-purple-700 px-2 py-1 rounded-full">
                {suggestions.length}
              </span>
            )}
          </div>
          <button
            onClick={() => setExpanded(!expanded)}
            className="text-gray-400 hover:text-gray-600"
          >
            <span className={`transform transition-transform ${expanded ? 'rotate-180' : ''}`}>
              ▼
            </span>
          </button>
        </div>
      </div>

      {/* Content */}
      {expanded && (
        <div className="p-4">
          {isLoading && (
            <div className="flex items-center justify-center py-8">
              <div className="flex space-x-1">
                <div className="w-2 h-2 bg-purple-400 rounded-full animate-pulse"></div>
                <div className="w-2 h-2 bg-purple-400 rounded-full animate-pulse" style={{animationDelay: '0.2s'}}></div>
                <div className="w-2 h-2 bg-purple-400 rounded-full animate-pulse" style={{animationDelay: '0.4s'}}></div>
              </div>
              <span className="text-sm text-gray-600 ml-3">Generating suggestions...</span>
            </div>
          )}

          {!isLoading && suggestions.length === 0 && (
            <div className="text-center py-8 text-gray-500">
              <div className="w-12 h-12 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-3">
                <span className="text-2xl">💡</span>
              </div>
              <p className="text-sm">No suggestions available</p>
              <p className="text-xs mt-1">Interact with tools to get contextual suggestions</p>
            </div>
          )}

          {!isLoading && suggestions.length > 0 && (
            <div className="space-y-3">
              {suggestions.map((suggestion) => (
                <div
                  key={suggestion.id}
                  className={`border rounded-lg p-3 ${getPriorityColor(suggestion.priority)}`}
                >
                  <div className="flex items-start gap-3">
                    <div className={`w-2 h-2 rounded-full mt-2 ${getPriorityDot(suggestion.priority)}`}></div>
                    <div className="flex-1">
                      <h4 className="font-medium text-gray-900 text-sm">
                        {suggestion.title}
                      </h4>
                      <p className="text-sm text-gray-600 mt-1">
                        {suggestion.description}
                      </p>
                      
                      {/* Tools and context */}
                      <div className="mt-2 flex flex-wrap gap-1">
                        {suggestion.tools && suggestion.tools.map((tool, index) => (
                          <span 
                            key={index}
                            className="inline-flex items-center px-2 py-1 rounded text-xs bg-blue-100 text-blue-700"
                          >
                            {tool}
                          </span>
                        ))}
                        {suggestion.context && suggestion.context.map((ctx, index) => (
                          <span 
                            key={index}
                            className="inline-flex items-center px-2 py-1 rounded text-xs bg-gray-100 text-gray-600"
                          >
                            {ctx}
                          </span>
                        ))}
                      </div>
                      
                      {/* Action button */}
                      <div className="mt-3">
                        <button
                          onClick={() => handleApplySuggestion(suggestion)}
                          className="text-xs bg-purple-600 text-white px-3 py-1 rounded hover:bg-purple-700 font-medium"
                        >
                          Apply Suggestion
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default AISuggestions;