/**
 * Context Preserver Component
 * 
 * Preserves user context and state to reduce cognitive load
 * when switching between tools or losing focus
 */

import React, { useCallback, useEffect, useRef } from 'react';
import { ContextState } from './types';

interface ContextPreserverProps {
  /** Unique context identifier */
  contextId: string;
  /** Current context state */
  contextState: ContextState;
  /** Callback to save context */
  onSaveContext: (contextId: string, state: ContextState) => void;
  /** Callback to restore context */
  onRestoreContext: (contextId: string) => ContextState | null;
  /** Auto-save interval in milliseconds */
  autoSaveInterval?: number;
  /** Children components to preserve context for */
  children: React.ReactNode;
}

export const ContextPreserver: React.FC<ContextPreserverProps> = ({
  contextId,
  contextState,
  onSaveContext,
  onRestoreContext,
  autoSaveInterval = 30000, // 30 seconds
  children
}) => {
  const saveTimeoutRef = useRef<NodeJS.Timeout | null>(null);
  const lastSavedStateRef = useRef<string>('');

  const saveContext = useCallback(() => {
    const currentStateString = JSON.stringify(contextState);
    
    // Only save if state has changed
    if (currentStateString !== lastSavedStateRef.current) {
      onSaveContext(contextId, contextState);
      lastSavedStateRef.current = currentStateString;
      
      console.debug(`[ContextPreserver] Context saved for ${contextId}`, {
        tool: contextState.current_tool,
        workflows: contextState.active_workflows.length,
        switches: contextState.context_switches_count
      });
    }
  }, [contextId, contextState, onSaveContext]);

  // Auto-save context at regular intervals
  useEffect(() => {
    if (saveTimeoutRef.current) {
      clearInterval(saveTimeoutRef.current);
    }

    saveTimeoutRef.current = setInterval(saveContext, autoSaveInterval);

    return () => {
      if (saveTimeoutRef.current) {
        clearInterval(saveTimeoutRef.current);
      }
    };
  }, [saveContext, autoSaveInterval]);

  // Save context when component unmounts or context changes significantly
  useEffect(() => {
    const handleBeforeUnload = () => {
      saveContext();
    };

    const handleVisibilityChange = () => {
      if (document.visibilityState === 'hidden') {
        saveContext();
      }
    };

    window.addEventListener('beforeunload', handleBeforeUnload);
    document.addEventListener('visibilitychange', handleVisibilityChange);

    return () => {
      window.removeEventListener('beforeunload', handleBeforeUnload);
      document.removeEventListener('visibilitychange', handleVisibilityChange);
      saveContext(); // Final save on unmount
    };
  }, [saveContext]);

  // Save context when tool or workflow changes
  useEffect(() => {
    saveContext();
  }, [contextState.current_tool, contextState.active_workflows, saveContext]);

  // Restore context on mount if available
  useEffect(() => {
    const restoredContext = onRestoreContext(contextId);
    if (restoredContext) {
      console.debug(`[ContextPreserver] Context restored for ${contextId}`, {
        tool: restoredContext.current_tool,
        workflows: restoredContext.active_workflows.length,
        sessionDuration: restoredContext.session_duration
      });
    }
  }, [contextId, onRestoreContext]);

  return (
    <div 
      className="mental-prosthetic-context-preserver"
      data-context-id={contextId}
      data-current-tool={contextState.current_tool}
      data-focus-state={contextState.user_focus_state}
    >
      {children}
    </div>
  );
};