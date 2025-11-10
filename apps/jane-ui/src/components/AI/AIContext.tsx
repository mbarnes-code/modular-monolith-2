'use client';

import React from 'react';

interface AIContextProviderProps {
  children: React.ReactNode;
  activeTool?: string;
  activeContext?: string[];
}

interface AIContextValue {
  activeTool?: string;
  activeContext: string[];
  setActiveTool: (tool?: string) => void;
  setActiveContext: (context: string[]) => void;
}

const AIContext = React.createContext<AIContextValue | undefined>(undefined);

export function AIContextProvider({ 
  children, 
  activeTool, 
  activeContext = [] 
}: AIContextProviderProps) {
  const [currentTool, setCurrentTool] = React.useState<string | undefined>(activeTool);
  const [currentContext, setCurrentContext] = React.useState<string[]>(activeContext);

  const value: AIContextValue = {
    activeTool: currentTool,
    activeContext: currentContext,
    setActiveTool: setCurrentTool,
    setActiveContext: setCurrentContext,
  };

  return (
    <AIContext.Provider value={value}>
      {children}
    </AIContext.Provider>
  );
}

export function useAIContext() {
  const context = React.useContext(AIContext);
  if (context === undefined) {
    throw new Error('useAIContext must be used within an AIContextProvider');
  }
  return context;
}

export { AIContext };
