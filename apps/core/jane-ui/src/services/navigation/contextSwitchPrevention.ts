/**
 * Context Switch Prevention Service
 * Proactive mechanisms to reduce cognitive overhead from tool switching
 */

import { useState, useEffect, useCallback, useRef } from 'react';
import { useGlobalStore, usePerformance } from '../store';

interface ContextSwitchEvent {
  fromTool: string;
  toTool: string;
  timestamp: number;
  reason: 'user_initiated' | 'workflow_required' | 'distraction' | 'unknown';
  duration: number; // ms spent in previous tool
  productivity_score: number; // 0-100 estimated productivity in previous tool
}

interface ContextSwitchPattern {
  pattern_type: 'rapid_switching' | 'domain_jumping' | 'unfinished_tasks' | 'distraction_loop';
  frequency: number; // occurrences in last hour
  severity: 'low' | 'medium' | 'high' | 'critical';
  tools_involved: string[];
  suggested_mitigation: string;
}

interface PreventionStrategy {
  strategy_id: string;
  name: string;
  description: string;
  effectiveness: number; // 0-100 based on user history
  cognitive_load_reduction: number; // estimated reduction percentage
  implementation: () => void;
}

interface ContextSwitchPreventionState {
  recentSwitches: ContextSwitchEvent[];
  detectedPatterns: ContextSwitchPattern[];
  activePreventions: PreventionStrategy[];
  switchingRisk: 'low' | 'medium' | 'high' | 'critical';
  recommendedActions: string[];
  focusModeActive: boolean;
  taskCompletionBuffer: Array<{
    toolId: string;
    taskDescription: string;
    estimatedTimeRemaining: number;
    priority: 'low' | 'medium' | 'high';
  }>;
}

// Thresholds for context switch prevention
const PREVENTION_THRESHOLDS = {
  rapid_switching: 3, // switches in 5 minutes
  minimum_tool_duration: 30000, // 30 seconds minimum
  distraction_pattern: 5, // return to same tool within 5 minutes
  productivity_threshold: 40, // below 40% = likely unproductive switch
  critical_switching_rate: 8 // switches per hour
};

export class ContextSwitchPreventionService {
  private switchHistory: ContextSwitchEvent[] = [];
  private detectedPatterns: ContextSwitchPattern[] = [];
  private activePreventions: PreventionStrategy[] = [];
  private toolStartTimes: Map<string, number> = new Map();
  private taskBuffers: Map<string, any[]> = new Map();

  constructor() {
    this.initializePreventionStrategies();
  }

  private initializePreventionStrategies(): void {
    this.activePreventions = [
      {
        strategy_id: 'completion_prompt',
        name: 'Task Completion Prompts',
        description: 'Prompt user to complete current task before switching',
        effectiveness: 75,
        cognitive_load_reduction: 25,
        implementation: () => this.showCompletionPrompt()
      },
      {
        strategy_id: 'focus_mode_suggestion',
        name: 'Automatic Focus Mode',
        description: 'Suggest focus mode when rapid switching detected',
        effectiveness: 85,
        cognitive_load_reduction: 40,
        implementation: () => this.suggestFocusMode()
      },
      {
        strategy_id: 'tool_grouping',
        name: 'Smart Tool Grouping',
        description: 'Group related tools to reduce switching overhead',
        effectiveness: 65,
        cognitive_load_reduction: 20,
        implementation: () => this.enableToolGrouping()
      },
      {
        strategy_id: 'break_reminder',
        name: 'Cognitive Break Reminders',
        description: 'Suggest breaks when switching patterns indicate fatigue',
        effectiveness: 70,
        cognitive_load_reduction: 30,
        implementation: () => this.suggestCognitiveBreak()
      },
      {
        strategy_id: 'workflow_preservation',
        name: 'Workflow State Preservation',
        description: 'Save and restore tool states to reduce context rebuilding',
        effectiveness: 80,
        cognitive_load_reduction: 35,
        implementation: () => this.preserveWorkflowState()
      }
    ];
  }

  /**
   * Record a context switch and analyze for prevention opportunities
   */
  recordContextSwitch(fromTool: string, toTool: string, reason: ContextSwitchEvent['reason'] = 'user_initiated'): ContextSwitchEvent {
    const now = Date.now();
    const previousStartTime = this.toolStartTimes.get(fromTool) || now;
    const duration = now - previousStartTime;

    // Calculate productivity score based on time spent and switching patterns
    const productivityScore = this.calculateProductivityScore(fromTool, duration, reason);

    const switchEvent: ContextSwitchEvent = {
      fromTool,
      toTool,
      timestamp: now,
      reason,
      duration,
      productivity_score: productivityScore
    };

    this.switchHistory.push(switchEvent);
    this.toolStartTimes.set(toTool, now);

    // Keep only recent history (last 2 hours)
    const twoHoursAgo = now - (2 * 60 * 60 * 1000);
    this.switchHistory = this.switchHistory.filter(event => event.timestamp >= twoHoursAgo);

    // Analyze patterns and trigger prevention if needed
    this.analyzeAndPrevent();

    return switchEvent;
  }

  private calculateProductivityScore(toolId: string, duration: number, reason: ContextSwitchEvent['reason']): number {
    let score = 50; // Base score

    // Duration factor
    if (duration < 10000) score -= 30; // Very short duration = likely unproductive
    else if (duration < 30000) score -= 15; // Short duration
    else if (duration > 300000) score += 20; // Long focused duration = productive

    // Reason factor
    switch (reason) {
      case 'workflow_required':
        score += 10;
        break;
      case 'distraction':
        score -= 25;
        break;
      case 'user_initiated':
        score += 5;
        break;
    }

    // Pattern factor - check if this is part of a rapid switching pattern
    const recentSwitches = this.getRecentSwitches(300000); // Last 5 minutes
    if (recentSwitches.length > 3) {
      score -= 20; // Rapid switching penalty
    }

    return Math.max(0, Math.min(100, score));
  }

  private analyzeAndPrevent(): void {
    this.detectedPatterns = [];
    
    // Detect rapid switching
    const rapidSwitches = this.detectRapidSwitching();
    if (rapidSwitches.length > 0) {
      this.detectedPatterns.push(...rapidSwitches);
    }

    // Detect domain jumping
    const domainJumping = this.detectDomainJumping();
    if (domainJumping.length > 0) {
      this.detectedPatterns.push(...domainJumping);
    }

    // Detect unfinished task patterns
    const unfinishedTasks = this.detectUnfinishedTasks();
    if (unfinishedTasks.length > 0) {
      this.detectedPatterns.push(...unfinishedTasks);
    }

    // Detect distraction loops
    const distractionLoops = this.detectDistractionLoops();
    if (distractionLoops.length > 0) {
      this.detectedPatterns.push(...distractionLoops);
    }

    // Trigger appropriate prevention strategies
    this.triggerPreventionStrategies();
  }

  private detectRapidSwitching(): ContextSwitchPattern[] {
    const patterns: ContextSwitchPattern[] = [];
    const recentSwitches = this.getRecentSwitches(300000); // Last 5 minutes

    if (recentSwitches.length >= PREVENTION_THRESHOLDS.rapid_switching) {
      const toolsInvolved = [...new Set([
        ...recentSwitches.map(s => s.fromTool),
        ...recentSwitches.map(s => s.toTool)
      ])];

      patterns.push({
        pattern_type: 'rapid_switching',
        frequency: recentSwitches.length,
        severity: recentSwitches.length > 5 ? 'critical' : recentSwitches.length > 3 ? 'high' : 'medium',
        tools_involved: toolsInvolved,
        suggested_mitigation: 'Enable focus mode or take a cognitive break'
      });
    }

    return patterns;
  }

  private detectDomainJumping(): ContextSwitchPattern[] {
    const patterns: ContextSwitchPattern[] = [];
    const recentSwitches = this.getRecentSwitches(600000); // Last 10 minutes

    // Count domain switches
    let domainSwitches = 0;
    const domains = new Set<string>();
    
    recentSwitches.forEach(switch_ => {
      const fromDomain = this.getToolDomain(switch_.fromTool);
      const toDomain = this.getToolDomain(switch_.toTool);
      
      domains.add(fromDomain);
      domains.add(toDomain);
      
      if (fromDomain !== toDomain) {
        domainSwitches++;
      }
    });

    if (domainSwitches > 2 && domains.size > 2) {
      patterns.push({
        pattern_type: 'domain_jumping',
        frequency: domainSwitches,
        severity: domainSwitches > 4 ? 'high' : 'medium',
        tools_involved: [...domains],
        suggested_mitigation: 'Group tasks by domain and complete one domain at a time'
      });
    }

    return patterns;
  }

  private detectUnfinishedTasks(): ContextSwitchPattern[] {
    const patterns: ContextSwitchPattern[] = [];
    const recentSwitches = this.getRecentSwitches(1800000); // Last 30 minutes

    // Look for tools with very short durations (likely unfinished tasks)
    const shortDurationSwitches = recentSwitches.filter(
      switch_ => switch_.duration < PREVENTION_THRESHOLDS.minimum_tool_duration &&
                 switch_.productivity_score < PREVENTION_THRESHOLDS.productivity_threshold
    );

    if (shortDurationSwitches.length > 2) {
      const toolsInvolved = [...new Set(shortDurationSwitches.map(s => s.fromTool))];
      
      patterns.push({
        pattern_type: 'unfinished_tasks',
        frequency: shortDurationSwitches.length,
        severity: shortDurationSwitches.length > 4 ? 'high' : 'medium',
        tools_involved: toolsInvolved,
        suggested_mitigation: 'Complete current task before switching or add to task buffer'
      });
    }

    return patterns;
  }

  private detectDistractionLoops(): ContextSwitchPattern[] {
    const patterns: ContextSwitchPattern[] = [];
    const recentSwitches = this.getRecentSwitches(300000); // Last 5 minutes

    // Look for patterns where user returns to the same tool quickly (distraction loop)
    const toolReturnCounts = new Map<string, number>();
    
    recentSwitches.forEach(switch_ => {
      const returnSwitches = recentSwitches.filter(
        s => s.toTool === switch_.fromTool && s.timestamp > switch_.timestamp
      );
      
      if (returnSwitches.length > 0) {
        const count = toolReturnCounts.get(switch_.fromTool) || 0;\n        toolReturnCounts.set(switch_.fromTool, count + 1);\n      }\n    });\n\n    toolReturnCounts.forEach((count, tool) => {\n      if (count >= 2) {\n        patterns.push({\n          pattern_type: 'distraction_loop',\n          frequency: count,\n          severity: count > 3 ? 'high' : 'medium',\n          tools_involved: [tool],\n          suggested_mitigation: 'Enable focus mode to prevent distractions'\n        });\n      }\n    });\n\n    return patterns;\n  }\n\n  private triggerPreventionStrategies(): void {\n    const criticalPatterns = this.detectedPatterns.filter(p => p.severity === 'critical');\n    const highPatterns = this.detectedPatterns.filter(p => p.severity === 'high');\n\n    // Trigger immediate prevention for critical patterns\n    if (criticalPatterns.length > 0) {\n      this.activePreventions.forEach(strategy => {\n        if (strategy.effectiveness > 80) {\n          strategy.implementation();\n        }\n      });\n    }\n\n    // Suggest prevention for high-severity patterns\n    if (highPatterns.length > 0) {\n      this.activePreventions.forEach(strategy => {\n        if (strategy.effectiveness > 70) {\n          // Queue suggestion rather than immediate implementation\n          console.log(`Suggesting prevention strategy: ${strategy.name}`);\n        }\n      });\n    }\n  }\n\n  private getRecentSwitches(timeWindowMs: number): ContextSwitchEvent[] {\n    const cutoff = Date.now() - timeWindowMs;\n    return this.switchHistory.filter(event => event.timestamp >= cutoff);\n  }\n\n  private getToolDomain(toolId: string): string {\n    // Security tools\n    if (['misp', 'helk', 'securityonion', 'cyberchef', 'maltrail', 'nemesis', 'yara-x'].includes(toolId)) {\n      return 'security';\n    }\n    \n    // Productivity tools\n    if (['n8n', 'mealie', 'dispatch', 'actual-budget', 'firecrawl', 'goose', 'it-tools', 'inspector'].includes(toolId)) {\n      return 'productivity';\n    }\n    \n    // MTG tools\n    if (['commander-spellbook', 'mtg-scripting', 'mtg-commander-map', 'card-analysis'].includes(toolId)) {\n      return 'mtg';\n    }\n    \n    // Infrastructure tools (default)\n    return 'infrastructure';\n  }\n\n  // Prevention strategy implementations\n  private showCompletionPrompt(): void {\n    console.log('Showing task completion prompt');\n    // Implementation would show a modal or notification\n  }\n\n  private suggestFocusMode(): void {\n    console.log('Suggesting focus mode activation');\n    // Implementation would trigger focus mode or show suggestion\n  }\n\n  private enableToolGrouping(): void {\n    console.log('Enabling smart tool grouping');\n    // Implementation would group related tools in UI\n  }\n\n  private suggestCognitiveBreak(): void {\n    console.log('Suggesting cognitive break');\n    // Implementation would show break reminder\n  }\n\n  private preserveWorkflowState(): void {\n    console.log('Preserving workflow state');\n    // Implementation would save current tool states\n  }\n\n  /**\n   * Get current prevention state for UI display\n   */\n  getPreventionState(): ContextSwitchPreventionState {\n    const recentSwitches = this.getRecentSwitches(3600000); // Last hour\n    const switchingRate = recentSwitches.length;\n    \n    let switchingRisk: 'low' | 'medium' | 'high' | 'critical' = 'low';\n    if (switchingRate > PREVENTION_THRESHOLDS.critical_switching_rate) {\n      switchingRisk = 'critical';\n    } else if (switchingRate > 6) {\n      switchingRisk = 'high';\n    } else if (switchingRate > 3) {\n      switchingRisk = 'medium';\n    }\n\n    const recommendedActions = this.detectedPatterns.map(pattern => pattern.suggested_mitigation);\n\n    return {\n      recentSwitches,\n      detectedPatterns: this.detectedPatterns,\n      activePreventions: this.activePreventions,\n      switchingRisk,\n      recommendedActions,\n      focusModeActive: false, // Would be connected to actual focus mode state\n      taskCompletionBuffer: [] // Would be populated with actual pending tasks\n    };\n  }\n\n  /**\n   * Manually trigger a prevention strategy\n   */\n  triggerPrevention(strategyId: string): void {\n    const strategy = this.activePreventions.find(s => s.strategy_id === strategyId);\n    if (strategy) {\n      strategy.implementation();\n    }\n  }\n\n  /**\n   * Get switching statistics for analytics\n   */\n  getSwitchingStats(): {\n    hourlyRate: number;\n    averageProductivity: number;\n    mostSwitchedTools: Array<{ tool: string; count: number }>;\n    dominantPatterns: ContextSwitchPattern[];\n  } {\n    const recentSwitches = this.getRecentSwitches(3600000); // Last hour\n    \n    const toolSwitchCounts = new Map<string, number>();\n    let totalProductivity = 0;\n    \n    recentSwitches.forEach(switch_ => {\n      const count = toolSwitchCounts.get(switch_.fromTool) || 0;\n      toolSwitchCounts.set(switch_.fromTool, count + 1);\n      totalProductivity += switch_.productivity_score;\n    });\n\n    const mostSwitchedTools = Array.from(toolSwitchCounts.entries())\n      .map(([tool, count]) => ({ tool, count }))\n      .sort((a, b) => b.count - a.count)\n      .slice(0, 5);\n\n    return {\n      hourlyRate: recentSwitches.length,\n      averageProductivity: recentSwitches.length > 0 ? totalProductivity / recentSwitches.length : 0,\n      mostSwitchedTools,\n      dominantPatterns: this.detectedPatterns.filter(p => p.severity === 'high' || p.severity === 'critical')\n    };\n  }\n\n  /**\n   * Reset all prevention state\n   */\n  reset(): void {\n    this.switchHistory = [];\n    this.detectedPatterns = [];\n    this.toolStartTimes.clear();\n    this.taskBuffers.clear();\n  }\n}\n\n// Hook for using context switch prevention\nexport function useContextSwitchPrevention() {\n  const [preventionService] = useState(() => new ContextSwitchPreventionService());\n  const [preventionState, setPreventionState] = useState<ContextSwitchPreventionState>({\n    recentSwitches: [],\n    detectedPatterns: [],\n    activePreventions: [],\n    switchingRisk: 'low',\n    recommendedActions: [],\n    focusModeActive: false,\n    taskCompletionBuffer: []\n  });\n\n  // Update prevention state periodically\n  useEffect(() => {\n    const interval = setInterval(() => {\n      setPreventionState(preventionService.getPreventionState());\n    }, 10000); // Update every 10 seconds\n\n    return () => clearInterval(interval);\n  }, [preventionService]);\n\n  const recordSwitch = useCallback((fromTool: string, toTool: string, reason?: ContextSwitchEvent['reason']) => {\n    return preventionService.recordContextSwitch(fromTool, toTool, reason);\n  }, [preventionService]);\n\n  const triggerPrevention = useCallback((strategyId: string) => {\n    preventionService.triggerPrevention(strategyId);\n  }, [preventionService]);\n\n  const getSwitchingStats = useCallback(() => {\n    return preventionService.getSwitchingStats();\n  }, [preventionService]);\n\n  return {\n    preventionState,\n    recordSwitch,\n    triggerPrevention,\n    getSwitchingStats,\n    resetPrevention: preventionService.reset.bind(preventionService)\n  };\n}