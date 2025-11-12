'use client';

interface ToolContext {
  toolName: string;
  domain: 'security' | 'productivity' | 'mtg' | 'infrastructure';
  currentState: Record<string, any>;
  recentActions: string[];
  activeWorkflow?: string;
  relatedTools: string[];
}

interface CrossToolContext {
  primaryTool: string;
  secondaryTools: string[];
  sharedData: Record<string, any>;
  workflows: string[];
  userIntent: string;
  executiveFunctionNeeds: string[];
}

interface ContextSuggestion {
  id: string;
  type: 'workflow' | 'data_flow' | 'tool_switch' | 'task_breakdown' | 'reminder';
  title: string;
  description: string;
  confidence: number;
  involvedTools: string[];
  estimatedTimeMinutes: number;
  executiveFunctionBenefit: string;
  actionData: Record<string, any>;
}

class CrossToolContextService {
  private toolContexts: Map<string, ToolContext> = new Map();
  private crossToolSuggestions: ContextSuggestion[] = [];
  private userBehaviorPatterns: Record<string, number> = {};

  /**
   * Register context from a specific tool
   */
  registerToolContext(toolName: string, context: Partial<ToolContext>) {
    const existingContext = this.toolContexts.get(toolName) || {
      toolName,
      domain: this.getDomainForTool(toolName),
      currentState: {},
      recentActions: [],
      relatedTools: []
    };

    const updatedContext: ToolContext = {
      ...existingContext,
      ...context,
      toolName
    };

    this.toolContexts.set(toolName, updatedContext);
    this.generateCrossToolSuggestions();
  }

  /**
   * Get current cross-tool context analysis
   */
  getCrossToolContext(primaryTool: string): CrossToolContext {
    const primary = this.toolContexts.get(primaryTool);
    if (!primary) {
      return {
        primaryTool,
        secondaryTools: [],
        sharedData: {},
        workflows: [],
        userIntent: 'unknown',
        executiveFunctionNeeds: []
      };
    }

    const secondaryTools = this.findRelatedActiveTools(primaryTool);
    const sharedData = this.extractSharedData(primaryTool, secondaryTools);
    const workflows = this.identifyPotentialWorkflows(primaryTool, secondaryTools);
    const userIntent = this.inferUserIntent(primary, secondaryTools);
    const executiveFunctionNeeds = this.identifyExecutiveFunctionNeeds(primary);

    return {
      primaryTool,
      secondaryTools,
      sharedData,
      workflows,
      userIntent,
      executiveFunctionNeeds
    };
  }

  /**
   * Get AI suggestions based on cross-tool context
   */
  getContextualSuggestions(primaryTool: string, maxSuggestions: number = 5): ContextSuggestion[] {
    const crossContext = this.getCrossToolContext(primaryTool);
    const suggestions = this.generateSuggestionsFromContext(crossContext);
    
    return suggestions
      .sort((a, b) => b.confidence - a.confidence)
      .slice(0, maxSuggestions);
  }

  /**
   * Update user behavior patterns for learning
   */
  updateUserBehaviorPattern(pattern: string, weight: number = 1) {
    this.userBehaviorPatterns[pattern] = (this.userBehaviorPatterns[pattern] || 0) + weight;
  }

  /**
   * Get domain-specific performance context
   */
  getDomainPerformanceContext(domain: string): { 
    targetResponseTime: number; 
    currentPerformance: number; 
    recommendations: string[] 
  } {
    const performanceTargets = {
      security: 1000,      // <1s
      productivity: 2000,  // <2s
      mtg: 3000,          // <3s
      infrastructure: 5000 // <5s
    };

    return {
      targetResponseTime: performanceTargets[domain as keyof typeof performanceTargets] || 2000,
      currentPerformance: Math.random() * 2500, // Mock current performance
      recommendations: this.getPerformanceRecommendations(domain)
    };
  }

  private getDomainForTool(toolName: string): 'security' | 'productivity' | 'mtg' | 'infrastructure' {
    const securityTools = ['MISP', 'HELK', 'SecurityOnion', 'YARA-X', 'CyberChef', 'Nemesis', 'Maltrail'];
    const productivityTools = ['n8n', 'Mealie', 'Dispatch', 'Actual Budget', 'Firecrawl', 'Goose', 'IT-Tools', 'Inspector'];
    const mtgTools = ['Commander Spellbook', 'MTG Commander Map', 'MTG Scripting Toolkit'];
    const infrastructureTools = ['Kong', 'Ghostwriter', 'KasmVNC'];

    if (securityTools.includes(toolName)) return 'security';
    if (productivityTools.includes(toolName)) return 'productivity';
    if (mtgTools.includes(toolName)) return 'mtg';
    if (infrastructureTools.includes(toolName)) return 'infrastructure';
    return 'productivity'; // Default
  }

  private findRelatedActiveTools(primaryTool: string): string[] {
    const primaryContext = this.toolContexts.get(primaryTool);
    if (!primaryContext) return [];

    const relatedTools: string[] = [];
    
    // Find tools in the same domain
    for (const [toolName, context] of this.toolContexts.entries()) {
      if (toolName !== primaryTool && context.domain === primaryContext.domain) {
        relatedTools.push(toolName);
      }
    }

    // Find tools with shared data patterns
    for (const [toolName, context] of this.toolContexts.entries()) {
      if (toolName !== primaryTool && this.hasSharedDataPatterns(primaryContext, context)) {
        relatedTools.push(toolName);
      }
    }

    return [...new Set(relatedTools)]; // Remove duplicates
  }

  private hasSharedDataPatterns(context1: ToolContext, context2: ToolContext): boolean {
    // Check for common data patterns (simplified)
    const state1Keys = Object.keys(context1.currentState);
    const state2Keys = Object.keys(context2.currentState);
    
    const commonKeys = state1Keys.filter(key => state2Keys.includes(key));
    return commonKeys.length > 0;
  }

  private extractSharedData(primaryTool: string, secondaryTools: string[]): Record<string, any> {
    const sharedData: Record<string, any> = {};
    const primaryContext = this.toolContexts.get(primaryTool);
    
    if (!primaryContext) return sharedData;

    for (const toolName of secondaryTools) {
      const context = this.toolContexts.get(toolName);
      if (!context) continue;

      // Find common data keys
      for (const key in primaryContext.currentState) {
        if (key in context.currentState) {
          sharedData[key] = {
            primary: primaryContext.currentState[key],
            [toolName]: context.currentState[key]
          };
        }
      }
    }

    return sharedData;
  }

  private identifyPotentialWorkflows(primaryTool: string, secondaryTools: string[]): string[] {
    const workflows: string[] = [];
    const primaryContext = this.toolContexts.get(primaryTool);
    
    if (!primaryContext) return workflows;

    // Security domain workflows
    if (primaryContext.domain === 'security') {
      if (secondaryTools.includes('YARA-X')) {
        workflows.push('threat-analysis-workflow');
      }
      if (secondaryTools.includes('n8n')) {
        workflows.push('security-automation-workflow');
      }
    }

    // Productivity domain workflows
    if (primaryContext.domain === 'productivity') {
      if (secondaryTools.includes('n8n')) {
        workflows.push('process-automation-workflow');
      }
      if (secondaryTools.includes('Actual Budget')) {
        workflows.push('resource-planning-workflow');
      }
    }

    // Cross-domain workflows
    if (primaryContext.domain === 'security' && secondaryTools.some(t => this.getDomainForTool(t) === 'productivity')) {
      workflows.push('security-reporting-workflow');
    }

    return workflows;
  }

  private inferUserIntent(primaryContext: ToolContext, secondaryTools: string[]): string {
    const recentActions = primaryContext.recentActions;
    
    if (recentActions.some(action => action.includes('analyze') || action.includes('investigate'))) {
      return 'analysis';
    }
    
    if (recentActions.some(action => action.includes('create') || action.includes('generate'))) {
      return 'creation';
    }
    
    if (recentActions.some(action => action.includes('report') || action.includes('document'))) {
      return 'documentation';
    }
    
    if (secondaryTools.length > 2) {
      return 'workflow_orchestration';
    }
    
    return 'exploration';
  }

  private identifyExecutiveFunctionNeeds(context: ToolContext): string[] {
    const needs: string[] = [];
    
    // Task switching support
    if (context.recentActions.length > 5) {
      needs.push('task_switching_support');
    }
    
    // Focus maintenance
    if (context.domain === 'security' && context.recentActions.length > 3) {
      needs.push('focus_maintenance');
    }
    
    // Memory support
    if (Object.keys(context.currentState).length > 10) {
      needs.push('memory_support');
    }
    
    // Time management
    if (context.activeWorkflow) {
      needs.push('time_management');
    }
    
    return needs;
  }

  private generateSuggestionsFromContext(crossContext: CrossToolContext): ContextSuggestion[] {
    const suggestions: ContextSuggestion[] = [];
    
    // Workflow suggestions
    for (const workflow of crossContext.workflows) {
      suggestions.push({
        id: `workflow-${workflow}`,
        type: 'workflow',
        title: `Create ${workflow.replace('-', ' ')} automation`,
        description: `Automate the workflow between ${crossContext.primaryTool} and related tools`,
        confidence: 0.8,
        involvedTools: [crossContext.primaryTool, ...crossContext.secondaryTools.slice(0, 2)],
        estimatedTimeMinutes: 15,
        executiveFunctionBenefit: 'Reduces cognitive load by automating repetitive tasks',
        actionData: { workflow, tools: crossContext.secondaryTools }
      });
    }
    
    // Task breakdown suggestions
    if (crossContext.userIntent === 'analysis' && crossContext.secondaryTools.length > 1) {
      suggestions.push({
        id: 'breakdown-analysis',
        type: 'task_breakdown',
        title: 'Break down analysis task',
        description: 'Split complex analysis across multiple tools for better focus',
        confidence: 0.9,
        involvedTools: [crossContext.primaryTool, ...crossContext.secondaryTools],
        estimatedTimeMinutes: 5,
        executiveFunctionBenefit: 'Improves focus by creating clear, manageable steps',
        actionData: { intent: crossContext.userIntent, tools: crossContext.secondaryTools }
      });
    }
    
    // Executive function reminders
    for (const need of crossContext.executiveFunctionNeeds) {
      suggestions.push({
        id: `reminder-${need}`,
        type: 'reminder',
        title: this.getReminderTitle(need),
        description: this.getReminderDescription(need),
        confidence: 0.7,
        involvedTools: [crossContext.primaryTool],
        estimatedTimeMinutes: 1,
        executiveFunctionBenefit: this.getExecutiveFunctionBenefit(need),
        actionData: { need, context: crossContext }
      });
    }
    
    return suggestions;
  }

  private getReminderTitle(need: string): string {
    const titles = {
      task_switching_support: 'Save context before switching',
      focus_maintenance: 'Schedule focus break',
      memory_support: 'Document current state',
      time_management: 'Set time boundary'
    };
    return titles[need as keyof typeof titles] || 'Executive function reminder';
  }

  private getReminderDescription(need: string): string {
    const descriptions = {
      task_switching_support: 'Save your current work state to reduce cognitive load when switching tasks',
      focus_maintenance: 'Take a 5-minute break to maintain cognitive performance',
      memory_support: 'Document important information to reduce working memory load',
      time_management: 'Set a timer to maintain awareness of time spent on this task'
    };
    return descriptions[need as keyof typeof descriptions] || 'General executive function support';
  }

  private getExecutiveFunctionBenefit(need: string): string {
    const benefits = {
      task_switching_support: 'Reduces cognitive switching cost and maintains context',
      focus_maintenance: 'Prevents cognitive fatigue and maintains performance',
      memory_support: 'Offloads working memory to external storage',
      time_management: 'Maintains temporal awareness and prevents hyperfocus'
    };
    return benefits[need as keyof typeof benefits] || 'General executive function support';
  }

  private getPerformanceRecommendations(domain: string): string[] {
    const recommendations = {
      security: [
        'Pre-load threat intelligence data',
        'Use caching for frequent queries',
        'Optimize correlation algorithms'
      ],
      productivity: [
        'Batch similar operations',
        'Use keyboard shortcuts',
        'Enable auto-save features'
      ],
      mtg: [
        'Cache deck statistics',
        'Use incremental search',
        'Pre-calculate synergies'
      ],
      infrastructure: [
        'Monitor resource usage',
        'Use connection pooling',
        'Implement health checks'
      ]
    };
    
    return recommendations[domain as keyof typeof recommendations] || [];
  }

  private generateCrossToolSuggestions() {
    // This would be called whenever tool context is updated
    // Implementation would analyze all current contexts and generate suggestions
    this.crossToolSuggestions = [];
    
    for (const [toolName] of this.toolContexts) {
      const suggestions = this.getContextualSuggestions(toolName, 3);
      this.crossToolSuggestions.push(...suggestions);
    }
    
    // Remove duplicates and sort by confidence
    this.crossToolSuggestions = this.crossToolSuggestions
      .filter((suggestion, index, self) => 
        index === self.findIndex(s => s.id === suggestion.id)
      )
      .sort((a, b) => b.confidence - a.confidence);
  }
}

// Create singleton instance
export const crossToolContextService = new CrossToolContextService();

// React hook for using the service
export function useCrossToolContext(primaryTool?: string) {
  const registerContext = (toolName: string, context: Partial<ToolContext>) => {
    crossToolContextService.registerToolContext(toolName, context);
  };

  const getContext = (tool: string = primaryTool || '') => {
    return crossToolContextService.getCrossToolContext(tool);
  };

  const getSuggestions = (tool: string = primaryTool || '', maxSuggestions?: number) => {
    return crossToolContextService.getContextualSuggestions(tool, maxSuggestions);
  };

  const updateBehaviorPattern = (pattern: string, weight?: number) => {
    crossToolContextService.updateUserBehaviorPattern(pattern, weight);
  };

  const getDomainPerformance = (domain: string) => {
    return crossToolContextService.getDomainPerformanceContext(domain);
  };

  return {
    registerContext,
    getContext,
    getSuggestions,
    updateBehaviorPattern,
    getDomainPerformance
  };
}

export type { ContextSuggestion, CrossToolContext, ToolContext };
