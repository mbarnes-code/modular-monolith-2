/**
 * Task Continuation UI Component
 * Interface for resuming interrupted work with context preservation
 */

import { AnimatePresence, motion } from 'framer-motion';
import {
    AlertTriangle,
    BookOpen,
    CheckCircle,
    ChevronDown,
    ChevronRight,
    Clock,
    Layers,
    Link,
    Play,
    RotateCcw,
    Target,
    X,
    Zap
} from 'lucide-react';
import React, { useEffect, useState } from 'react';
import {
    useTaskContinuation,
    type TaskContext,
    type TaskContinuation
} from '../../services/navigation/taskContinuation';

interface TaskContinuationUIProps {
  toolId: string;
  onResume?: (context: TaskContext) => void;
  onDismiss?: () => void;
  className?: string;
}

interface ContextResumeProps {
  continuation: TaskContinuation;
  onResume: (context: TaskContext) => void;
  onDismiss: () => void;
}

function ContextResumeCard({ continuation, onResume, onDismiss }: ContextResumeProps) {
  const [expanded, setExpanded] = useState(false);
  const [resumeStep, setResumeStep] = useState<'preview' | 'preparing' | 'ready'>('preview');
  
  const { context, resumptionStrategy, estimatedReloadTime, cognitiveReloadCost, recommendations } = continuation;
  
  const handleResume = () => {
    if (resumptionStrategy === 'immediate') {
      onResume(context);
    } else {
      setResumeStep('preparing');
      
      // Simulate preparation time
      setTimeout(() => {
        setResumeStep('ready');
      }, estimatedReloadTime * 200); // Scaled down for demo
    }
  };

  const getReloadCostColor = (cost: number) => {
    if (cost <= 30) return 'text-green-600 bg-green-100';
    if (cost <= 60) return 'text-yellow-600 bg-yellow-100';
    return 'text-red-600 bg-red-100';
  };

  const getStrategyIcon = (strategy: TaskContinuation['resumptionStrategy']) => {
    switch (strategy) {
      case 'immediate': return <Zap className="w-4 h-4" />;
      case 'gradual': return <Clock className="w-4 h-4" />;
      case 'guided': return <BookOpen className="w-4 h-4" />;
      case 'manual': return <Target className="w-4 h-4" />;
    }
  };

  const getTaskTypeIcon = (type: TaskContext['taskType']) => {
    switch (type) {
      case 'analysis': return '🔍';
      case 'creation': return '✨';
      case 'modification': return '✏️';
      case 'review': return '👀';
      case 'research': return '📚';
      case 'planning': return '📋';
      default: return '📄';
    }
  };

  const getFocusDepthBadge = (depth: TaskContext['focusDepth']) => {
    const styles = {
      surface: 'bg-blue-100 text-blue-800',
      moderate: 'bg-purple-100 text-purple-800',
      deep: 'bg-red-100 text-red-800'
    };
    
    return (
      <span className={`px-2 py-1 rounded text-xs ${styles[depth]}`}>
        {depth} focus
      </span>
    );
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -20 }}
      className="bg-white rounded-lg border border-gray-200 shadow-sm overflow-hidden"
    >
      {/* Header */}
      <div className="p-4 border-b border-gray-100">
        <div className="flex items-start justify-between">
          <div className="flex items-center gap-3">
            <div className="text-2xl">{getTaskTypeIcon(context.taskType)}</div>
            <div>
              <h3 className="font-medium text-gray-900">{context.title}</h3>
              <div className="flex items-center gap-2 mt-1">
                {getFocusDepthBadge(context.focusDepth)}
                <span className="text-xs text-gray-500">
                  {Math.round((Date.now() - context.lastInteraction.getTime()) / (1000 * 60))} min ago
                </span>
              </div>
            </div>
          </div>
          
          <div className="flex items-center gap-2">
            <div className={`px-2 py-1 rounded text-xs ${getReloadCostColor(cognitiveReloadCost)}`}>
              {Math.round(cognitiveReloadCost)}% effort
            </div>
            <button
              onClick={onDismiss}
              className="p-1 text-gray-400 hover:text-gray-600 rounded"
            >
              <X className="w-4 h-4" />
            </button>
          </div>
        </div>
        
        {context.description && (
          <p className="text-sm text-gray-600 mt-2">{context.description}</p>
        )}
      </div>

      {/* Resume Strategy */}
      <div className="p-4 bg-gray-50 border-b border-gray-100">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            {getStrategyIcon(resumptionStrategy)}
            <span className="text-sm font-medium text-gray-700 capitalize">
              {resumptionStrategy} resumption
            </span>
            <span className="text-xs text-gray-500">
              (~{estimatedReloadTime}s to resume)
            </span>
          </div>
          
          <button
            onClick={() => setExpanded(!expanded)}
            className="flex items-center gap-1 text-sm text-blue-600 hover:text-blue-800"
          >
            Details
            {expanded ? <ChevronDown className="w-4 h-4" /> : <ChevronRight className="w-4 h-4" />}
          </button>
        </div>
      </div>

      {/* Expanded Details */}
      <AnimatePresence>
        {expanded && (
          <motion.div
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: 'auto', opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            className="border-b border-gray-100"
          >
            <div className="p-4 space-y-4">
              {/* Context Details */}
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
                <div>
                  <div className="text-gray-600">Session</div>
                  <div className="font-medium">
                    {Math.round(context.sessionDuration / 60)}m
                  </div>
                </div>
                <div>
                  <div className="text-gray-600">Cognitive Load</div>
                  <div className="font-medium">{context.cognitiveLoad}%</div>
                </div>
                <div>
                  <div className="text-gray-600">Confidence</div>
                  <div className="font-medium">{context.confidence}%</div>
                </div>
                <div>
                  <div className="text-gray-600">Dependencies</div>
                  <div className="font-medium">{context.dependencies.length}</div>
                </div>
              </div>

              {/* Working Data Preview */}
              {Object.keys(context.workingData).length > 0 && (
                <div>
                  <div className="text-sm font-medium text-gray-700 mb-2">Working Data</div>
                  <div className="bg-gray-100 rounded p-2 text-xs">
                    <pre className="text-gray-600 line-clamp-3">
                      {JSON.stringify(context.workingData, null, 2)}
                    </pre>
                  </div>
                </div>
              )}

              {/* Navigation Path */}
              {context.navigationPath.length > 0 && (
                <div>
                  <div className="text-sm font-medium text-gray-700 mb-2">Navigation Path</div>
                  <div className="flex items-center gap-1 text-xs text-gray-600">
                    {context.navigationPath.map((path, index) => (
                      <React.Fragment key={index}>
                        <span className="bg-gray-100 px-2 py-1 rounded">{path}</span>
                        {index < context.navigationPath.length - 1 && (
                          <ChevronRight className="w-3 h-3" />
                        )}
                      </React.Fragment>
                    ))}
                  </div>
                </div>
              )}

              {/* Blockers */}
              {context.blockers.length > 0 && (
                <div>
                  <div className="text-sm font-medium text-gray-700 mb-2 flex items-center gap-2">
                    <AlertTriangle className="w-4 h-4 text-red-500" />
                    Blockers
                  </div>
                  <div className="space-y-1">
                    {context.blockers.map((blocker, index) => (
                      <div key={index} className="text-sm text-red-600 bg-red-50 px-2 py-1 rounded">
                        {blocker}
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Recommendations */}
      {recommendations.length > 0 && (
        <div className="p-4 bg-blue-50 border-b border-gray-100">
          <div className="text-sm font-medium text-blue-900 mb-2">Recommendations</div>
          <div className="space-y-2">
            {recommendations.map((rec, index) => (
              <div key={index} className="flex items-start gap-2 text-sm">
                <div className={`p-1 rounded text-xs ${
                  rec.priority === 'high' ? 'bg-red-100 text-red-700' :
                  rec.priority === 'medium' ? 'bg-yellow-100 text-yellow-700' :
                  'bg-gray-100 text-gray-700'
                }`}>
                  {rec.type === 'action' ? '⚡' : rec.type === 'reminder' ? '💭' : '📝'}
                </div>
                <span className="text-gray-700">{rec.message}</span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Actions */}
      <div className="p-4">
        {resumeStep === 'preview' && (
          <div className="flex items-center gap-3">
            <button
              onClick={handleResume}
              className="flex-1 flex items-center justify-center gap-2 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
            >
              <Play className="w-4 h-4" />
              Resume Work
            </button>
            
            <button
              onClick={onDismiss}
              className="px-4 py-2 text-gray-600 hover:text-gray-800 border border-gray-300 rounded"
            >
              Start Fresh
            </button>
          </div>
        )}

        {resumeStep === 'preparing' && (
          <div className="flex items-center justify-center gap-3 text-blue-600">
            <div className="animate-spin">
              <RotateCcw className="w-4 h-4" />
            </div>
            <span className="text-sm">Preparing context...</span>
          </div>
        )}

        {resumeStep === 'ready' && (
          <button
            onClick={() => onResume(context)}
            className="w-full flex items-center justify-center gap-2 px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700"
          >
            <CheckCircle className="w-4 h-4" />
            Ready to Resume
          </button>
        )}
      </div>
    </motion.div>
  );
}

export function TaskContinuationUI({ 
  toolId, 
  onResume, 
  onDismiss, 
  className = '' 
}: TaskContinuationUIProps) {
  const { getContinuationStrategy, findRelatedContexts } = useTaskContinuation();
  
  const [continuation, setContinuation] = useState<TaskContinuation | null>(null);
  const [relatedContexts, setRelatedContexts] = useState<TaskContext[]>([]);
  const [showRelated, setShowRelated] = useState(false);

  useEffect(() => {
    const strategy = getContinuationStrategy(toolId);
    setContinuation(strategy);

    if (strategy) {
      const related = findRelatedContexts(strategy.context.id);
      setRelatedContexts(related);
    }
  }, [toolId, getContinuationStrategy, findRelatedContexts]);

  const handleResume = (context: TaskContext) => {
    onResume?.(context);
  };

  const handleDismiss = () => {
    onDismiss?.();
  };

  if (!continuation) {
    return null;
  }

  return (
    <div className={`task-continuation-ui ${className}`}>
      <div className="space-y-4">
        {/* Main continuation card */}
        <ContextResumeCard
          continuation={continuation}
          onResume={handleResume}
          onDismiss={handleDismiss}
        />

        {/* Related contexts */}
        {relatedContexts.length > 0 && (
          <div className="bg-gray-50 rounded-lg p-4">
            <button
              onClick={() => setShowRelated(!showRelated)}
              className="flex items-center gap-2 text-sm font-medium text-gray-700 mb-3"
            >
              <Link className="w-4 h-4" />
              Related Work ({relatedContexts.length})
              {showRelated ? <ChevronDown className="w-4 h-4" /> : <ChevronRight className="w-4 h-4" />}
            </button>

            <AnimatePresence>
              {showRelated && (
                <motion.div
                  initial={{ height: 0, opacity: 0 }}
                  animate={{ height: 'auto', opacity: 1 }}
                  exit={{ height: 0, opacity: 0 }}
                  className="space-y-2"
                >
                  {relatedContexts.map(context => (
                    <div
                      key={context.id}
                      className="flex items-center justify-between p-3 bg-white rounded border border-gray-200"
                    >
                      <div className="flex items-center gap-3">
                        <div className="text-lg">{getTaskTypeIcon(context.taskType)}</div>
                        <div>
                          <div className="text-sm font-medium text-gray-900">{context.title}</div>
                          <div className="text-xs text-gray-500">
                            {context.toolId} • {Math.round((Date.now() - context.lastInteraction.getTime()) / (1000 * 60))} min ago
                          </div>
                        </div>
                      </div>
                      
                      <button
                        onClick={() => handleResume(context)}
                        className="px-3 py-1 text-xs bg-blue-100 text-blue-700 rounded hover:bg-blue-200"
                      >
                        Resume
                      </button>
                    </div>
                  ))}
                </motion.div>
              )}
            </AnimatePresence>
          </div>
        )}
      </div>
    </div>
  );

  function getTaskTypeIcon(type: TaskContext['taskType']) {
    switch (type) {
      case 'analysis': return '🔍';
      case 'creation': return '✨';
      case 'modification': return '✏️';
      case 'review': return '👀';
      case 'research': return '📚';
      case 'planning': return '📋';
      default: return '📄';
    }
  }
}

/**
 * Context Summary Widget for Active Tasks
 */
interface ActiveContextsWidgetProps {
  onContextSelect?: (context: TaskContext) => void;
  className?: string;
}

export function ActiveContextsWidget({ 
  onContextSelect, 
  className = '' 
}: ActiveContextsWidgetProps) {
  const { activeContexts, hasContext } = useTaskContinuation();
  const [expanded, setExpanded] = useState(false);

  if (activeContexts.length === 0) {
    return null;
  }

  return (
    <div className={`active-contexts-widget bg-white rounded-lg border border-gray-200 shadow-sm ${className}`}>
      <div className="p-3 border-b border-gray-100">
        <button
          onClick={() => setExpanded(!expanded)}
          className="flex items-center justify-between w-full text-left"
        >
          <div className="flex items-center gap-2">
            <Layers className="w-4 h-4 text-blue-600" />
            <span className="text-sm font-medium text-gray-900">Active Contexts</span>
            <span className="px-2 py-0.5 bg-blue-100 text-blue-800 text-xs rounded">
              {activeContexts.length}
            </span>
          </div>
          {expanded ? <ChevronDown className="w-4 h-4" /> : <ChevronRight className="w-4 h-4" />}
        </button>
      </div>

      <AnimatePresence>
        {expanded && (
          <motion.div
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: 'auto', opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            className="max-h-64 overflow-auto"
          >
            <div className="p-2 space-y-1">
              {activeContexts.map(context => (
                <button
                  key={context.id}
                  onClick={() => onContextSelect?.(context)}
                  className="w-full flex items-center gap-3 p-2 rounded hover:bg-gray-50 text-left"
                >
                  <div className="text-sm">{getTaskTypeIcon(context.taskType)}</div>
                  <div className="flex-1 min-w-0">
                    <div className="text-sm font-medium text-gray-900 truncate">
                      {context.title}
                    </div>
                    <div className="text-xs text-gray-500">
                      {context.toolId} • {Math.round(context.sessionDuration / 60)}m session
                    </div>
                  </div>
                  <div className="text-xs text-gray-400">
                    {Math.round((Date.now() - context.lastInteraction.getTime()) / (1000 * 60))}m
                  </div>
                </button>
              ))}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );

  function getTaskTypeIcon(type: TaskContext['taskType']) {
    switch (type) {
      case 'analysis': return '🔍';
      case 'creation': return '✨';
      case 'modification': return '✏️';
      case 'review': return '👀';
      case 'research': return '📚';
      case 'planning': return '📋';
      default: return '📄';
    }
  }
}