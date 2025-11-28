/**
 * Tool-Level Lazy Loading System for Jane-UI Mental Prosthetic Platform
 * Constitutional compliance with executive function accommodations
 * 
 * Features:
 * - Dynamic imports for all 37 tools
 * - Priority loading for frequently used tools
 * - Executive function-friendly loading states
 * - Domain-specific loading optimization
 * - Performance monitoring integration
 */

import { useCallback, useEffect, useState } from 'react';
import { usePerformanceMonitor } from './performance/performanceMonitor';

// Tool priority levels based on usage analytics and constitutional criticality
export const TOOL_PRIORITIES = {
  critical: ['dispatch', 'nemesis', 'cyberchef'], // Security tools (<1s requirement)
  high: ['mealie', 'actual', 'n8n', 'inspector', 'misp', 'it-tools', 'chroma', 'goose'], // Frequently used tools
  medium: ['commander-spellbook', 'mtg-scripting', 'security-onion', 'yara-x', 'rita', 'kong', 'vllm'], // Specialized tools
  low: ['ghostwriter', 'helk', 'maltrail', 'kasmvnc', 'firecrawl', 'spec-kit'], // Infrastructure/occasional use
} as const;

// Executive function accommodations for tool loading
export const LOADING_ACCOMMODATIONS = {
  showProgress: true,
  showTimeEstimate: true,
  showLoadingContext: true,
  maintainUserState: true,
  preventLoadingFlicker: true,
} as const;

// Tool metadata for optimization and user experience
export interface ToolMetadata {
  id: string;
  name: string;
  domain: 'security' | 'productivity' | 'mtg' | 'infrastructure' | 'ai';
  priority: keyof typeof TOOL_PRIORITIES;
  estimatedLoadTime: number; // milliseconds
  description: string;
  icon: string;
  frequentlyUsed: boolean;
  lastUsed?: Date;
  constitutionalThreshold: number; // domain-specific response time requirement
}

// Comprehensive tool registry for the 37-tool platform
export const TOOL_REGISTRY: Record<string, ToolMetadata> = {
  // Security Domain Tools (Constitutional Requirement: <1s)
  'dispatch': {
    id: 'dispatch',
    name: 'Dispatch',
    domain: 'security',
    priority: 'critical',
    estimatedLoadTime: 800,
    description: 'Incident management and response coordination',
    icon: '🚨',
    frequentlyUsed: true,
    constitutionalThreshold: 1000,
  },
  'nemesis': {
    id: 'nemesis',
    name: 'Nemesis',
    domain: 'security',
    priority: 'critical',
    estimatedLoadTime: 900,
    description: 'Post-exploitation framework for threat hunting',
    icon: '🕵️',
    frequentlyUsed: true,
    constitutionalThreshold: 1000,
  },
  'cyberchef': {
    id: 'cyberchef',
    name: 'CyberChef',
    domain: 'security',
    priority: 'critical',
    estimatedLoadTime: 700,
    description: 'Cyber Swiss Army Knife for data operations',
    icon: '🔧',
    frequentlyUsed: true,
    constitutionalThreshold: 1000,
  },
  'ghostwriter': {
    id: 'ghostwriter',
    name: 'Ghostwriter',
    domain: 'security',
    priority: 'low',
    estimatedLoadTime: 1200,
    description: 'Automated reporting and documentation',
    icon: '👻',
    frequentlyUsed: false,
    constitutionalThreshold: 1000,
  },
  'helk': {
    id: 'helk',
    name: 'HELK',
    domain: 'security',
    priority: 'low',
    estimatedLoadTime: 1500,
    description: 'Hunting ELK for threat detection',
    icon: '🦌',
    frequentlyUsed: false,
    constitutionalThreshold: 1000,
  },
  'maltrail': {
    id: 'maltrail',
    name: 'Maltrail',
    domain: 'security',
    priority: 'low',
    estimatedLoadTime: 1100,
    description: 'Malicious network traffic detection',
    icon: '🕸️',
    frequentlyUsed: false,
    constitutionalThreshold: 1000,
  },
  'misp': {
    id: 'misp',
    name: 'MISP',
    domain: 'security',
    priority: 'high',
    estimatedLoadTime: 950,
    description: 'Malware Information Sharing Platform',
    icon: '🚨',
    frequentlyUsed: true,
    constitutionalThreshold: 1000,
  },
  'security-onion': {
    id: 'security-onion',
    name: 'Security Onion',
    domain: 'security',
    priority: 'medium',
    estimatedLoadTime: 1300,
    description: 'Network security monitoring platform',
    icon: '🧅',
    frequentlyUsed: false,
    constitutionalThreshold: 1000,
  },
  'yara-x': {
    id: 'yara-x',
    name: 'YARA-X',
    domain: 'security',
    priority: 'medium',
    estimatedLoadTime: 850,
    description: 'Next-generation malware identification',
    icon: '🔍',
    frequentlyUsed: false,
    constitutionalThreshold: 1000,
  },
  'rita': {
    id: 'rita',
    name: 'RITA',
    domain: 'security',
    priority: 'medium',
    estimatedLoadTime: 1150,
    description: 'Real Intelligence Threat Analytics',
    icon: '🕵️',
    frequentlyUsed: false,
    constitutionalThreshold: 1000,
  },

  // Productivity Domain Tools (Constitutional Requirement: <2s)
  'mealie': {
    id: 'mealie',
    name: 'Mealie',
    domain: 'productivity',
    priority: 'high',
    estimatedLoadTime: 600,
    description: 'Recipe management and meal planning',
    icon: '🍽️',
    frequentlyUsed: true,
    constitutionalThreshold: 2000,
  },
  'actual': {
    id: 'actual',
    name: 'Actual Budget',
    domain: 'productivity',
    priority: 'high',
    estimatedLoadTime: 800,
    description: 'Personal finance and budgeting',
    icon: '💰',
    frequentlyUsed: true,
    constitutionalThreshold: 2000,
  },
  'n8n': {
    id: 'n8n',
    name: 'n8n',
    domain: 'productivity',
    priority: 'high',
    estimatedLoadTime: 1000,
    description: 'Workflow automation platform',
    icon: '🔄',
    frequentlyUsed: true,
    constitutionalThreshold: 2000,
  },
  'inspector': {
    id: 'inspector',
    name: 'Inspector',
    domain: 'productivity',
    priority: 'high',
    estimatedLoadTime: 700,
    description: 'System monitoring and inspection',
    icon: '🔍',
    frequentlyUsed: true,
    constitutionalThreshold: 2000,
  },
  'it-tools': {
    id: 'it-tools',
    name: 'IT Tools',
    domain: 'productivity',
    priority: 'medium',
    estimatedLoadTime: 750,
    description: 'Collection of handy online tools for developers',
    icon: '🔧',
    frequentlyUsed: true,
    constitutionalThreshold: 2000,
  },
  'firecrawl': {
    id: 'firecrawl',
    name: 'Firecrawl',
    domain: 'productivity',
    priority: 'medium',
    estimatedLoadTime: 1200,
    description: 'Turn websites into LLM-ready markdown',
    icon: '🔥',
    frequentlyUsed: false,
    constitutionalThreshold: 2000,
  },
  'spec-kit': {
    id: 'spec-kit',
    name: 'SpecKit',
    domain: 'productivity',
    priority: 'low',
    estimatedLoadTime: 900,
    description: 'Specification and documentation toolkit',
    icon: '📝',
    frequentlyUsed: false,
    constitutionalThreshold: 2000,
  },

  // MTG Domain Tools (Constitutional Requirement: <3s)
  'commander-spellbook': {
    id: 'commander-spellbook',
    name: 'Commander Spellbook',
    domain: 'mtg',
    priority: 'medium',
    estimatedLoadTime: 1200,
    description: 'Magic: The Gathering combo database',
    icon: '🧙',
    frequentlyUsed: true,
    constitutionalThreshold: 3000,
  },
  'mtg-scripting': {
    id: 'mtg-scripting',
    name: 'MTG Scripting Toolkit',
    domain: 'mtg',
    priority: 'medium',
    estimatedLoadTime: 1400,
    description: 'Advanced MTG deck analysis and scripting',
    icon: '⚔️',
    frequentlyUsed: false,
    constitutionalThreshold: 3000,
  },

  // Infrastructure Domain Tools (Constitutional Requirement: <5s)
  'kasmvnc': {
    id: 'kasmvnc',
    name: 'KasmVNC',
    domain: 'infrastructure',
    priority: 'low',
    estimatedLoadTime: 2000,
    description: 'Web-based VNC client',
    icon: '🖥️',
    frequentlyUsed: false,
    constitutionalThreshold: 5000,
  },
  'kong': {
    id: 'kong',
    name: 'Kong Gateway',
    domain: 'infrastructure',
    priority: 'medium',
    estimatedLoadTime: 1800,
    description: 'API Gateway and Service Mesh platform',
    icon: '🦍',
    frequentlyUsed: false,
    constitutionalThreshold: 5000,
  },

  // AI Domain Tools (Constitutional Requirement: <2s - productivity adjacent)
  'chroma': {
    id: 'chroma',
    name: 'Chroma DB',
    domain: 'ai',
    priority: 'high',
    estimatedLoadTime: 900,
    description: 'Vector database for AI workflows',
    icon: '🧠',
    frequentlyUsed: true,
    constitutionalThreshold: 2000,
  },
  'goose': {
    id: 'goose',
    name: 'Goose AI',
    domain: 'ai',
    priority: 'high',
    estimatedLoadTime: 1100,
    description: 'Developer-focused AI assistant',
    icon: '🪿',
    frequentlyUsed: true,
    constitutionalThreshold: 2000,
  },
  'vllm': {
    id: 'vllm',
    name: 'vLLM',
    domain: 'ai',
    priority: 'medium',
    estimatedLoadTime: 1600,
    description: 'High-throughput LLM serving',
    icon: '🚀',
    frequentlyUsed: false,
    constitutionalThreshold: 2000,
  },
};

// Dynamic import function with performance monitoring
export const importToolComponent = async (toolId: string): Promise<React.ComponentType<any>> => {
  const tool = TOOL_REGISTRY[toolId];
  if (!tool) {
    throw new Error(`Tool "${toolId}" not found in registry`);
  }

  const startTime = performance.now();
  
  try {
    let componentModule;

    // Domain-specific dynamic imports
    switch (tool.domain) {
      case 'security':
        switch (toolId) {
          case 'dispatch':
            componentModule = await import('../components/security/dispatch/DispatchTool');
            break;
          case 'nemesis':
            componentModule = await import('../components/security/nemesis/NemesisTool');
            break;
          case 'cyberchef':
            componentModule = await import('../components/security/cyberchef/CyberChefTool');
            break;
          case 'ghostwriter':
            componentModule = await import('../components/security/ghostwriter/GhostwriterTool');
            break;
          case 'helk':
            componentModule = await import('../components/security/helk/HelkTool');
            break;
          case 'maltrail':
            componentModule = await import('../components/security/maltrail/MaltrailTool');
            break;
          case 'misp':
            componentModule = await import('../components/security/misp/MispTool');
            break;
          case 'security-onion':
            componentModule = await import('../components/security/security-onion/SecurityOnionTool');
            break;
          case 'yara-x':
            componentModule = await import('../components/security/yara-x/YaraXTool');
            break;
          case 'rita':
            componentModule = await import('../components/security/rita/RitaTool');
            break;
          default:
            throw new Error(`Security tool "${toolId}" not implemented`);
        }
        break;

      case 'productivity':
        switch (toolId) {
          case 'mealie':
            componentModule = await import('../components/productivity/mealie/MealieTool');
            break;
          case 'actual':
            componentModule = await import('../components/productivity/actual/ActualTool');
            break;
          case 'n8n':
            componentModule = await import('../components/productivity/n8n/N8nTool');
            break;
          case 'inspector':
            componentModule = await import('../components/productivity/inspector/InspectorTool');
            break;
          case 'it-tools':
            componentModule = await import('../components/productivity/it-tools/ItToolsTool');
            break;
          case 'firecrawl':
            componentModule = await import('../components/productivity/firecrawl/FirecrawlTool');
            break;
          case 'spec-kit':
            componentModule = await import('../components/productivity/spec-kit/SpecKitTool');
            break;
          default:
            throw new Error(`Productivity tool "${toolId}" not implemented`);
        }
        break;

      case 'mtg':
        switch (toolId) {
          case 'commander-spellbook':
            componentModule = await import('../components/mtg/commander-spellbook/CommanderSpellbookTool');
            break;
          case 'mtg-scripting':
            componentModule = await import('../components/mtg/scripting/MtgScriptingTool');
            break;
          default:
            throw new Error(`MTG tool "${toolId}" not implemented`);
        }
        break;

      case 'infrastructure':
        switch (toolId) {
          case 'kasmvnc':
            componentModule = await import('../components/infrastructure/kasmvnc/KasmVncTool');
            break;
          case 'kong':
            componentModule = await import('../components/infrastructure/kong/KongTool');
            break;
          default:
            throw new Error(`Infrastructure tool "${toolId}" not implemented`);
        }
        break;

      case 'ai':
        switch (toolId) {
          case 'chroma':
            componentModule = await import('../components/ai/chroma/ChromaTool');
            break;
          case 'goose':
            componentModule = await import('../components/ai/goose/GooseTool');
            break;
          case 'vllm':
            componentModule = await import('../components/ai/vllm/VllmTool');
            break;
          default:
            throw new Error(`AI tool "${toolId}" not implemented`);
        }
        break;

      default:
        throw new Error(`Unknown domain "${tool.domain}" for tool "${toolId}"`);
    }

    const loadTime = performance.now() - startTime;
    
    // Performance compliance validation
    if (loadTime > tool.constitutionalThreshold) {
      console.warn(`⚠️ Constitutional violation: ${tool.name} loaded in ${loadTime}ms (threshold: ${tool.constitutionalThreshold}ms)`);
    }

    // Update tool usage analytics
    TOOL_REGISTRY[toolId].lastUsed = new Date();

    return componentModule.default || componentModule;
  } catch (error) {
    const loadTime = performance.now() - startTime;
    console.error(`❌ Failed to load tool "${toolId}" after ${loadTime}ms:`, error);
    
    // Return error boundary component
    return ({ error: errorDetails }: { error?: Error }) => (
      <div className="p-6 border border-red-200 rounded-lg bg-red-50">
        <h3 className="text-lg font-semibold text-red-800 mb-2">
          {tool.icon} {tool.name} - Loading Error
        </h3>
        <p className="text-red-600 mb-4">{tool.description}</p>
        <details className="text-sm text-red-500">
          <summary>Technical Details</summary>
          <pre className="mt-2 text-xs">{error?.message || 'Unknown error'}</pre>
        </details>
      </div>
    );
  }
};

// Executive function-friendly loading component
export interface ToolLoaderProps {
  toolId: string;
  onLoadComplete?: (component: React.ComponentType<any>) => void;
  onLoadError?: (error: Error) => void;
  fallback?: React.ComponentType<any>;
}

export function ToolLoader({ 
  toolId, 
  onLoadComplete, 
  onLoadError, 
  fallback: FallbackComponent 
}: ToolLoaderProps) {
  const [isLoading, setIsLoading] = useState(true);
  const [loadProgress, setLoadProgress] = useState(0);
  const [Component, setComponent] = useState<React.ComponentType<any> | null>(null);
  const [error, setError] = useState<Error | null>(null);
  const { measureOperation } = usePerformanceMonitor();

  const tool = TOOL_REGISTRY[toolId];

  const loadTool = useCallback(async () => {
    if (!tool) {
      const error = new Error(`Tool "${toolId}" not found`);
      setError(error);
      onLoadError?.(error);
      return;
    }

    try {
      setIsLoading(true);
      setLoadProgress(0);

      // Simulate progressive loading for executive function accommodation
      const progressInterval = setInterval(() => {
        setLoadProgress(prev => Math.min(prev + 20, 90));
      }, tool.estimatedLoadTime / 5);

      const result = await measureOperation(
        `tool-load-${toolId}`,
        () => importToolComponent(toolId),
        tool.domain
      );

      clearInterval(progressInterval);
      setLoadProgress(100);
      
      setComponent(() => result);
      onLoadComplete?.(result);
    } catch (err) {
      const error = err as Error;
      setError(error);
      onLoadError?.(error);
    } finally {
      setTimeout(() => {
        setIsLoading(false);
        setLoadProgress(0);
      }, 300); // Brief delay for visual stability
    }
  }, [toolId, tool, measureOperation, onLoadComplete, onLoadError]);

  useEffect(() => {
    loadTool();
  }, [loadTool]);

  // Executive function-friendly loading state
  if (isLoading && !Component) {
    return (
      <div className="flex flex-col items-center justify-center p-8 bg-gray-50 rounded-lg">
        <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mb-4">
          <span className="text-3xl animate-pulse">{tool?.icon || '⚙️'}</span>
        </div>
        
        <h3 className="text-lg font-semibold text-gray-800 mb-2">
          Loading {tool?.name || 'Tool'}
        </h3>
        
        <p className="text-sm text-gray-600 mb-4 text-center max-w-xs">
          {tool?.description || 'Preparing your tool...'}
        </p>

        {/* Progress bar for executive function support */}
        <div className="w-full max-w-xs bg-gray-200 rounded-full h-2 mb-2">
          <div 
            className="bg-blue-500 h-2 rounded-full transition-all duration-300 ease-out"
            style={{ width: `${loadProgress}%` }}
          />
        </div>

        {/* Time estimate for executive function support */}
        <div className="text-xs text-gray-500">
          Estimated: {Math.ceil((tool?.estimatedLoadTime || 1000) / 1000)}s
        </div>
      </div>
    );
  }

  // Error state with recovery options
  if (error) {
    if (FallbackComponent) {
      return <FallbackComponent error={error} />;
    }

    return (
      <div className="p-6 border border-red-200 rounded-lg bg-red-50">
        <div className="flex items-start gap-3">
          <div className="w-10 h-10 bg-red-100 rounded-lg flex items-center justify-center flex-shrink-0">
            <span className="text-xl">⚠️</span>
          </div>
          <div className="flex-1">
            <h3 className="text-lg font-semibold text-red-800 mb-2">
              {tool?.name || 'Tool'} Unavailable
            </h3>
            <p className="text-red-600 mb-4">
              {tool?.description || 'This tool could not be loaded.'}
            </p>
            <button
              onClick={loadTool}
              className="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors text-sm font-medium"
            >
              Try Again
            </button>
          </div>
        </div>
      </div>
    );
  }

  // Render the loaded component
  if (Component) {
    return <Component />;
  }

  return null;
}

// Hook for managing multiple tool loading with priority
export function useToolLoader() {
  const [loadedTools, setLoadedTools] = useState<Map<string, React.ComponentType<any>>>(new Map());
  const [loadingTools, setLoadingTools] = useState<Set<string>>(new Set());
  const [erroredTools, setErroredTools] = useState<Map<string, Error>>(new Map());

  const loadTool = useCallback(async (toolId: string): Promise<React.ComponentType<any> | null> => {
    if (loadedTools.has(toolId)) {
      return loadedTools.get(toolId)!;
    }

    if (loadingTools.has(toolId)) {
      return null; // Already loading
    }

    setLoadingTools(prev => new Set(prev).add(toolId));
    setErroredTools(prev => {
      const next = new Map(prev);
      next.delete(toolId);
      return next;
    });

    try {
      const component = await importToolComponent(toolId);
      
      setLoadedTools(prev => new Map(prev).set(toolId, component));
      return component;
    } catch (error) {
      setErroredTools(prev => new Map(prev).set(toolId, error as Error));
      return null;
    } finally {
      setLoadingTools(prev => {
        const next = new Set(prev);
        next.delete(toolId);
        return next;
      });
    }
  }, [loadedTools, loadingTools]);

  // Preload frequently used tools based on priority
  const preloadFrequentTools = useCallback(async () => {
    const frequentTools = Object.values(TOOL_REGISTRY)
      .filter(tool => tool.frequentlyUsed)
      .sort((a, b) => {
        const priorityOrder = { critical: 0, high: 1, medium: 2, low: 3 };
        return priorityOrder[a.priority] - priorityOrder[b.priority];
      });

    // Load critical tools immediately
    const criticalTools = frequentTools.filter(tool => tool.priority === 'critical');
    await Promise.all(criticalTools.map(tool => loadTool(tool.id)));

    // Load high priority tools with slight delay for executive function accommodation
    setTimeout(() => {
      const highPriorityTools = frequentTools.filter(tool => tool.priority === 'high');
      Promise.all(highPriorityTools.map(tool => loadTool(tool.id)));
    }, 1000);
  }, [loadTool]);

  return {
    loadTool,
    preloadFrequentTools,
    loadedTools: Array.from(loadedTools.keys()),
    loadingTools: Array.from(loadingTools),
    erroredTools: Array.from(erroredTools.entries()),
    isToolLoaded: (toolId: string) => loadedTools.has(toolId),
    isToolLoading: (toolId: string) => loadingTools.has(toolId),
    getToolError: (toolId: string) => erroredTools.get(toolId),
  };
}