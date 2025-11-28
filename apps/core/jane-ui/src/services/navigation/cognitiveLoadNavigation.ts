/**
 * Navigation-Specific Cognitive Load Management
 * Enhanced thresholds and decision logic for navigation actions based on current cognitive state
 */

import { Domain } from '../store';

export interface NavigationCognitiveState {
  canNavigate: boolean;
  shouldWarn: boolean;
  suggestedDelay: number; // milliseconds
  alternativeActions: NavigationAlternative[];
  riskLevel: 'low' | 'medium' | 'high' | 'critical';
}

export interface NavigationAlternative {
  type: 'defer' | 'simplify' | 'group' | 'focus_mode' | 'break';
  description: string;
  action: () => void;
}

export interface NavigationLoadThresholds {
  // Thresholds for allowing navigation actions
  navigate_safely: number;      // 0-60: Can navigate freely
  navigate_with_warning: number; // 61-75: Show warning but allow
  navigate_with_delay: number;   // 76-85: Force brief delay
  block_navigation: number;      // 86+: Block non-critical navigation
  
  // Context switching penalties
  same_domain_penalty: number;   // Minimal penalty for staying in domain
  cross_domain_penalty: number;  // Higher penalty for switching domains
  rapid_switch_penalty: number;  // Penalty for multiple quick switches
  
  // Tool complexity considerations
  complexity_multiplier: number; // How much tool complexity affects decision
  fatigue_multiplier: number;    // How much fatigue affects thresholds
}

export interface ToolNavigationMetrics {
  toolId: string;
  domain: Domain;
  baseComplexity: number;
  visualComplexity: number;
  cognitiveComplexity: number;
  memoryLoad: number;
  attentionDemand: number;
  averageSessionDuration: number; // minutes
  contextSwitchCost: number; // relative cost 1-10
}

// Navigation-specific thresholds (more conservative than general cognitive load)
const NAVIGATION_THRESHOLDS: NavigationLoadThresholds = {
  navigate_safely: 55,        // More conservative than general 60
  navigate_with_warning: 70,  // Earlier warning than general 75
  navigate_with_delay: 80,    // Force consideration pause
  block_navigation: 88,       // Block at high load
  
  same_domain_penalty: 2,     // Minimal penalty within domain
  cross_domain_penalty: 15,   // Significant penalty crossing domains
  rapid_switch_penalty: 25,   // High penalty for rapid switching
  
  complexity_multiplier: 1.3, // Navigation more sensitive to complexity
  fatigue_multiplier: 1.4     // Navigation more sensitive to fatigue
};

// Enhanced tool complexity profiles for navigation decisions
const NAVIGATION_TOOL_METRICS: Record<string, ToolNavigationMetrics> = {
  // Security Domain - High cognitive switching cost
  'misp': {
    toolId: 'misp',
    domain: 'security',
    baseComplexity: 85,
    visualComplexity: 80,
    cognitiveComplexity: 90,
    memoryLoad: 85,
    attentionDemand: 95,
    averageSessionDuration: 45,
    contextSwitchCost: 9
  },
  'helk': {
    toolId: 'helk',
    domain: 'security',
    baseComplexity: 80,
    visualComplexity: 75,
    cognitiveComplexity: 85,
    memoryLoad: 80,
    attentionDemand: 90,
    averageSessionDuration: 60,
    contextSwitchCost: 8
  },
  'securityonion': {
    toolId: 'securityonion',
    domain: 'security',
    baseComplexity: 90,
    visualComplexity: 85,
    cognitiveComplexity: 95,
    memoryLoad: 90,
    attentionDemand: 95,
    averageSessionDuration: 75,
    contextSwitchCost: 10
  },
  'cyberchef': {
    toolId: 'cyberchef',
    domain: 'security',
    baseComplexity: 70,
    visualComplexity: 60,
    cognitiveComplexity: 75,
    memoryLoad: 65,
    attentionDemand: 80,
    averageSessionDuration: 30,
    contextSwitchCost: 6
  },
  'maltrail': {
    toolId: 'maltrail',
    domain: 'security',
    baseComplexity: 75,
    visualComplexity: 70,
    cognitiveComplexity: 80,
    memoryLoad: 75,
    attentionDemand: 85,
    averageSessionDuration: 40,
    contextSwitchCost: 7
  },

  // Productivity Domain - Medium cognitive switching cost
  'n8n': {
    toolId: 'n8n',
    domain: 'productivity',
    baseComplexity: 65,
    visualComplexity: 70,
    cognitiveComplexity: 70,
    memoryLoad: 60,
    attentionDemand: 75,
    averageSessionDuration: 35,
    contextSwitchCost: 6
  },
  'mealie': {
    toolId: 'mealie',
    domain: 'productivity',
    baseComplexity: 40,
    visualComplexity: 45,
    cognitiveComplexity: 35,
    memoryLoad: 30,
    attentionDemand: 50,
    averageSessionDuration: 15,
    contextSwitchCost: 3
  },
  'dispatch': {
    toolId: 'dispatch',
    domain: 'productivity',
    baseComplexity: 75,
    visualComplexity: 65,
    cognitiveComplexity: 80,
    memoryLoad: 70,
    attentionDemand: 85,
    averageSessionDuration: 50,
    contextSwitchCost: 7
  },
  'actual-budget': {
    toolId: 'actual-budget',
    domain: 'productivity',
    baseComplexity: 55,
    visualComplexity: 60,
    cognitiveComplexity: 50,
    memoryLoad: 45,
    attentionDemand: 65,
    averageSessionDuration: 25,
    contextSwitchCost: 4
  },

  // MTG Domain - Variable cognitive switching cost
  'commander-spellbook': {
    toolId: 'commander-spellbook',
    domain: 'mtg',
    baseComplexity: 70,
    visualComplexity: 80,
    cognitiveComplexity: 75,
    memoryLoad: 85,
    attentionDemand: 75,
    averageSessionDuration: 40,
    contextSwitchCost: 6
  },
  'mtg-scripting': {
    toolId: 'mtg-scripting',
    domain: 'mtg',
    baseComplexity: 80,
    visualComplexity: 70,
    cognitiveComplexity: 90,
    memoryLoad: 85,
    attentionDemand: 85,
    averageSessionDuration: 55,
    contextSwitchCost: 8
  },

  // Infrastructure Domain - Lower cognitive switching cost
  'kong': {
    toolId: 'kong',
    domain: 'infrastructure',
    baseComplexity: 60,
    visualComplexity: 55,
    cognitiveComplexity: 65,
    memoryLoad: 55,
    attentionDemand: 70,
    averageSessionDuration: 30,
    contextSwitchCost: 5
  },
  'ghostwriter': {
    toolId: 'ghostwriter',
    domain: 'infrastructure',
    baseComplexity: 65,
    visualComplexity: 60,
    cognitiveComplexity: 70,
    memoryLoad: 60,
    attentionDemand: 75,
    averageSessionDuration: 35,
    contextSwitchCost: 5
  }
};

export class NavigationCognitiveLoadManager {
  private contextSwitchHistory: Array<{
    from: string;
    to: string;
    timestamp: number;
    domain: Domain;
  }> = [];

  private navigationDelayTimers: Map<string, NodeJS.Timeout> = new Map();

  /**
   * Evaluate whether navigation to a tool is cognitively safe
   */
  evaluateNavigation(
    currentTool: string | null,
    targetTool: string,
    currentCognitiveLoad: number,
    fatigueLevel: number,
    contextSwitches: number
  ): NavigationCognitiveState {
    const targetMetrics = NAVIGATION_TOOL_METRICS[targetTool];
    const currentMetrics = currentTool ? NAVIGATION_TOOL_METRICS[currentTool] : null;

    if (!targetMetrics) {
      // Unknown tool - use conservative defaults
      return this.createSafeNavigationState(targetTool);
    }

    // Calculate adjusted cognitive load for navigation decision
    const adjustedLoad = this.calculateNavigationLoad(
      currentCognitiveLoad,
      fatigueLevel,
      currentTool,
      targetTool,
      contextSwitches
    );

    // Determine navigation risk level
    const riskLevel = this.assessNavigationRisk(adjustedLoad, targetMetrics);

    // Generate navigation decision
    return this.generateNavigationDecision(
      adjustedLoad,
      riskLevel,
      currentTool,
      targetTool,
      targetMetrics
    );
  }

  private calculateNavigationLoad(
    baseCognitiveLoad: number,
    fatigueLevel: number,
    currentTool: string | null,
    targetTool: string,
    contextSwitches: number
  ): number {
    let adjustedLoad = baseCognitiveLoad;
    
    // Apply fatigue multiplier
    adjustedLoad += fatigueLevel * NAVIGATION_THRESHOLDS.fatigue_multiplier;

    // Apply context switching penalty
    if (currentTool && currentTool !== targetTool) {
      const currentMetrics = NAVIGATION_TOOL_METRICS[currentTool];
      const targetMetrics = NAVIGATION_TOOL_METRICS[targetTool];

      if (currentMetrics && targetMetrics) {
        if (currentMetrics.domain === targetMetrics.domain) {
          adjustedLoad += NAVIGATION_THRESHOLDS.same_domain_penalty;
        } else {
          adjustedLoad += NAVIGATION_THRESHOLDS.cross_domain_penalty;
        }

        // Add tool-specific context switch cost
        adjustedLoad += (currentMetrics.contextSwitchCost + targetMetrics.contextSwitchCost) / 2;
      }
    }

    // Apply rapid switching penalty
    const recentSwitches = this.getRecentContextSwitches(300000); // 5 minutes
    if (recentSwitches >= 3) {
      adjustedLoad += NAVIGATION_THRESHOLDS.rapid_switch_penalty;
    }

    // Apply target tool complexity
    const targetMetrics = NAVIGATION_TOOL_METRICS[targetTool];
    if (targetMetrics) {
      const complexityPenalty = (targetMetrics.baseComplexity * NAVIGATION_THRESHOLDS.complexity_multiplier) / 10;
      adjustedLoad += complexityPenalty;
    }

    return Math.min(100, adjustedLoad);
  }

  private assessNavigationRisk(
    adjustedLoad: number,
    targetMetrics: ToolNavigationMetrics
  ): 'low' | 'medium' | 'high' | 'critical' {
    if (adjustedLoad <= NAVIGATION_THRESHOLDS.navigate_safely) {
      return 'low';
    } else if (adjustedLoad <= NAVIGATION_THRESHOLDS.navigate_with_warning) {
      return 'medium';
    } else if (adjustedLoad <= NAVIGATION_THRESHOLDS.navigate_with_delay) {
      return 'high';
    } else {
      return 'critical';
    }
  }

  private generateNavigationDecision(
    adjustedLoad: number,
    riskLevel: 'low' | 'medium' | 'high' | 'critical',
    currentTool: string | null,
    targetTool: string,
    targetMetrics: ToolNavigationMetrics
  ): NavigationCognitiveState {
    const alternatives: NavigationAlternative[] = [];

    switch (riskLevel) {
      case 'low':
        return {
          canNavigate: true,
          shouldWarn: false,
          suggestedDelay: 0,
          alternativeActions: [],
          riskLevel: 'low'
        };

      case 'medium':
        alternatives.push({
          type: 'defer',
          description: `Consider completing current task before switching to ${targetMetrics.toolId}`,
          action: () => this.suggestTaskCompletion(currentTool)
        });

        return {
          canNavigate: true,
          shouldWarn: true,
          suggestedDelay: 1000, // 1 second warning
          alternativeActions: alternatives,
          riskLevel: 'medium'
        };

      case 'high':
        alternatives.push(
          {
            type: 'simplify',
            description: 'Reduce current cognitive load before navigating',
            action: () => this.triggerSimplification()
          },
          {
            type: 'focus_mode',
            description: 'Enable focus mode for current tool',
            action: () => this.enableFocusMode(currentTool)
          },
          {
            type: 'group',
            description: `Group ${targetTool} with similar tools for later`,
            action: () => this.addToToolGroup(targetTool)
          }
        );

        return {
          canNavigate: true,
          shouldWarn: true,
          suggestedDelay: 3000, // 3 second mandatory delay
          alternativeActions: alternatives,
          riskLevel: 'high'
        };

      case 'critical':
        alternatives.push(
          {
            type: 'break',
            description: 'Take a 5-10 minute break before switching tools',
            action: () => this.suggestBreak()
          },
          {
            type: 'defer',
            description: `Schedule ${targetTool} for later when cognitive load is lower`,
            action: () => this.scheduleForLater(targetTool)
          },
          {
            type: 'focus_mode',
            description: 'Complete current work in focus mode first',
            action: () => this.enableFocusMode(currentTool)
          }
        );

        return {
          canNavigate: false,
          shouldWarn: true,
          suggestedDelay: 5000, // 5 second block with alternatives
          alternativeActions: alternatives,
          riskLevel: 'critical'
        };
    }
  }

  private createSafeNavigationState(targetTool: string): NavigationCognitiveState {
    return {
      canNavigate: true,
      shouldWarn: false,
      suggestedDelay: 0,
      alternativeActions: [],
      riskLevel: 'low'
    };
  }

  private getRecentContextSwitches(timeWindowMs: number): number {
    const cutoff = Date.now() - timeWindowMs;
    return this.contextSwitchHistory.filter(switch_ => switch_.timestamp >= cutoff).length;
  }

  /**
   * Record a context switch for future cognitive load calculations
   */
  recordContextSwitch(fromTool: string, toTool: string, fromDomain: Domain, toDomain: Domain): void {
    this.contextSwitchHistory.push({
      from: fromTool,
      to: toTool,
      timestamp: Date.now(),
      domain: toDomain
    });

    // Keep only recent history (last hour)
    const oneHourAgo = Date.now() - (60 * 60 * 1000);
    this.contextSwitchHistory = this.contextSwitchHistory.filter(
      switch_ => switch_.timestamp >= oneHourAgo
    );
  }

  /**
   * Get tool complexity info for navigation UI
   */
  getToolComplexityInfo(toolId: string): ToolNavigationMetrics | null {
    return NAVIGATION_TOOL_METRICS[toolId] || null;
  }

  /**
   * Get recommended navigation delay based on current state
   */
  getRecommendedDelay(
    currentCognitiveLoad: number,
    targetComplexity: number
  ): number {
    if (currentCognitiveLoad > 80) return 5000; // 5s for high load
    if (currentCognitiveLoad > 70) return 3000; // 3s for medium-high load
    if (targetComplexity > 80) return 2000;     // 2s for complex tools
    return 0;
  }

  // Alternative action implementations (to be connected to actual services)
  private suggestTaskCompletion(currentTool: string | null): void {
    console.log(`Suggesting task completion for ${currentTool} before navigation`);
  }

  private triggerSimplification(): void {
    console.log('Triggering cognitive load simplification');
  }

  private enableFocusMode(tool: string | null): void {
    console.log(`Enabling focus mode for ${tool}`);
  }

  private addToToolGroup(toolId: string): void {
    console.log(`Adding ${toolId} to tool group for later access`);
  }

  private suggestBreak(): void {
    console.log('Suggesting cognitive break');
  }

  private scheduleForLater(toolId: string): void {
    console.log(`Scheduling ${toolId} for later when cognitive load is lower`);
  }

  /**
   * Clear all timers and reset state
   */
  cleanup(): void {
    this.navigationDelayTimers.forEach(timer => clearTimeout(timer));
    this.navigationDelayTimers.clear();
    this.contextSwitchHistory = [];
  }
}

// Singleton instance for app-wide use
export const navigationCognitiveLoadManager = new NavigationCognitiveLoadManager();