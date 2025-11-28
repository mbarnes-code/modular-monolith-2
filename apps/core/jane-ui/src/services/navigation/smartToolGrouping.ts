/**
 * Smart Tool Grouping and Clustering Service
 * Intelligent tool bundling based on usage patterns, workflows, and cognitive load optimization
 */

import { useCallback, useEffect, useMemo, useState } from 'react';
import { useGlobalStore, usePerformance } from '../../services/store';
import { useContextSwitchPrevention } from './contextSwitchPrevention';

export interface Tool {
  id: string;
  name: string;
  display_name: string;
  domain: 'security' | 'productivity' | 'mtg' | 'infrastructure';
  category: string;
  tags: string[];
  complexity_score: number;
  cognitive_load_score: number;
  typical_session_duration: number; // minutes
  common_workflows?: string[];
  dependencies?: string[];
}

export interface ToolGroup {
  id: string;
  name: string;
  description: string;
  tools: Tool[];
  groupType: 'workflow' | 'domain' | 'complexity' | 'frequency' | 'contextual';
  cohesionScore: number; // 0-100, how well tools work together
  cognitiveEfficiency: number; // 0-100, cognitive load reduction when used together
  switchingCost: number; // 0-100, cost of switching between tools in group
  recommendationStrength: number; // 0-100, how strongly to recommend this grouping
  usagePattern: {
    frequency: number;
    sessionDuration: number;
    timeOfDay: number[]; // hours when typically used
    userTypes: string[];
  };
  metadata: {
    createdAt: Date;
    lastUsed?: Date;
    successRate: number; // 0-100, how often users find this grouping helpful
    userFeedback: number; // -100 to 100, user rating
  };
}

export interface ClusteringConfig {
  maxGroupSize: number;
  minCohesionScore: number;
  preferredGroupTypes: Array<ToolGroup['groupType']>;
  prioritizeFrequentlyUsed: boolean;
  considerTimeOfDay: boolean;
  adaptToUserBehavior: boolean;
  enableContextualGrouping: boolean;
}

const DEFAULT_CONFIG: ClusteringConfig = {
  maxGroupSize: 6,
  minCohesionScore: 65,
  preferredGroupTypes: ['workflow', 'domain', 'contextual'],
  prioritizeFrequentlyUsed: true,
  considerTimeOfDay: true,
  adaptToUserBehavior: true,
  enableContextualGrouping: true
};

/**
 * Smart Tool Clustering Service
 * Uses ML-inspired algorithms to group tools for optimal cognitive efficiency
 */
export class SmartToolClusteringService {
  private config: ClusteringConfig;
  private usageHistory: Map<string, number[]> = new Map();
  private cooccurrenceMatrix: Map<string, Map<string, number>> = new Map();
  private temporalPatterns: Map<string, number[]> = new Map(); // 24-hour usage patterns

  constructor(config: Partial<ClusteringConfig> = {}) {
    this.config = { ...DEFAULT_CONFIG, ...config };
  }

  /**
   * Analyze tool usage patterns and build co-occurrence data
   */
  analyzeUsagePatterns(tools: Tool[], usageEvents: Array<{
    toolId: string;
    timestamp: Date;
    sessionDuration: number;
    context?: string;
  }>) {
    // Build co-occurrence matrix
    this.buildCooccurrenceMatrix(usageEvents);
    
    // Analyze temporal patterns
    this.analyzeTemporalPatterns(usageEvents);
    
    // Calculate usage frequencies
    this.calculateUsageFrequencies(usageEvents);
  }

  private buildCooccurrenceMatrix(events: Array<{ toolId: string; timestamp: Date }>) {
    // Group events by time windows (30-minute sessions)
    const sessions = this.groupIntoSessions(events, 30 * 60 * 1000);
    
    sessions.forEach(session => {
      const toolIds = Array.from(new Set(session.map(e => e.toolId)));
      
      // Build co-occurrence pairs
      for (let i = 0; i < toolIds.length; i++) {
        for (let j = i + 1; j < toolIds.length; j++) {
          const tool1 = toolIds[i];
          const tool2 = toolIds[j];
          
          this.incrementCooccurrence(tool1, tool2);
          this.incrementCooccurrence(tool2, tool1);
        }
      }
    });
  }

  private groupIntoSessions(events: Array<{ toolId: string; timestamp: Date }>, sessionGap: number) {
    const sorted = events.sort((a, b) => a.timestamp.getTime() - b.timestamp.getTime());
    const sessions: typeof events[] = [];
    let currentSession: typeof events = [];
    
    sorted.forEach(event => {
      if (currentSession.length === 0 || 
          event.timestamp.getTime() - currentSession[currentSession.length - 1].timestamp.getTime() <= sessionGap) {
        currentSession.push(event);
      } else {
        if (currentSession.length > 1) {
          sessions.push([...currentSession]);
        }
        currentSession = [event];
      }
    });
    
    if (currentSession.length > 1) {
      sessions.push(currentSession);
    }
    
    return sessions;
  }

  private incrementCooccurrence(tool1: string, tool2: string) {
    if (!this.cooccurrenceMatrix.has(tool1)) {
      this.cooccurrenceMatrix.set(tool1, new Map());
    }
    const tool1Map = this.cooccurrenceMatrix.get(tool1)!;
    tool1Map.set(tool2, (tool1Map.get(tool2) || 0) + 1);
  }

  private analyzeTemporalPatterns(events: Array<{ toolId: string; timestamp: Date }>) {
    events.forEach(event => {
      const hour = event.timestamp.getHours();
      if (!this.temporalPatterns.has(event.toolId)) {
        this.temporalPatterns.set(event.toolId, new Array(24).fill(0));
      }
      const pattern = this.temporalPatterns.get(event.toolId)!;
      pattern[hour]++;
    });
  }

  private calculateUsageFrequencies(events: Array<{ toolId: string; timestamp: Date }>) {
    const frequencies = new Map<string, number>();
    events.forEach(event => {
      frequencies.set(event.toolId, (frequencies.get(event.toolId) || 0) + 1);
    });
    
    // Convert to normalized scores (0-100)
    const maxFreq = Math.max(...Array.from(frequencies.values()));
    frequencies.forEach((freq, toolId) => {
      this.usageHistory.set(toolId, [Math.round((freq / maxFreq) * 100)]);
    });
  }

  /**
   * Generate smart tool groups using multiple clustering strategies
   */
  generateToolGroups(tools: Tool[]): ToolGroup[] {
    const groups: ToolGroup[] = [];
    
    // Strategy 1: Workflow-based grouping
    if (this.config.preferredGroupTypes.includes('workflow')) {
      groups.push(...this.createWorkflowGroups(tools));
    }
    
    // Strategy 2: Domain-based grouping with cognitive optimization
    if (this.config.preferredGroupTypes.includes('domain')) {
      groups.push(...this.createDomainGroups(tools));
    }
    
    // Strategy 3: Frequency-based grouping
    if (this.config.preferredGroupTypes.includes('frequency')) {
      groups.push(...this.createFrequencyGroups(tools));
    }
    
    // Strategy 4: Complexity-based grouping
    if (this.config.preferredGroupTypes.includes('complexity')) {
      groups.push(...this.createComplexityGroups(tools));
    }
    
    // Strategy 5: Contextual co-occurrence grouping
    if (this.config.enableContextualGrouping && this.config.preferredGroupTypes.includes('contextual')) {
      groups.push(...this.createContextualGroups(tools));
    }
    
    // Filter and optimize groups
    return this.optimizeGroups(groups);
  }

  private createWorkflowGroups(tools: Tool[]): ToolGroup[] {
    const workflowMap = new Map<string, Tool[]>();
    
    tools.forEach(tool => {
      (tool.common_workflows || []).forEach(workflow => {
        if (!workflowMap.has(workflow)) {
          workflowMap.set(workflow, []);
        }
        workflowMap.get(workflow)!.push(tool);
      });
    });
    
    return Array.from(workflowMap.entries())
      .filter(([_, tools]) => tools.length >= 2 && tools.length <= this.config.maxGroupSize)
      .map(([workflow, groupTools]) => ({
        id: `workflow-${workflow.toLowerCase().replace(/\s+/g, '-')}`,
        name: `${workflow} Workflow`,
        description: `Tools commonly used together for ${workflow.toLowerCase()} tasks`,
        tools: groupTools,
        groupType: 'workflow' as const,
        cohesionScore: this.calculateWorkflowCohesion(groupTools),
        cognitiveEfficiency: this.calculateCognitiveEfficiency(groupTools),
        switchingCost: this.calculateSwitchingCost(groupTools),
        recommendationStrength: this.calculateRecommendationStrength(groupTools, 'workflow'),
        usagePattern: this.analyzeGroupUsagePattern(groupTools),
        metadata: {
          createdAt: new Date(),
          successRate: 85, // Initial estimate
          userFeedback: 0
        }
      }));
  }

  private createDomainGroups(tools: Tool[]): ToolGroup[] {
    const domainMap = new Map<string, Tool[]>();
    
    tools.forEach(tool => {
      if (!domainMap.has(tool.domain)) {
        domainMap.set(tool.domain, []);
      }
      domainMap.get(tool.domain)!.push(tool);
    });
    
    return Array.from(domainMap.entries())
      .map(([domain, groupTools]) => {
        // Sub-group large domains by complexity/category
        if (groupTools.length > this.config.maxGroupSize) {
          return this.createDomainSubgroups(domain, groupTools);
        }
        
        return [{
          id: `domain-${domain}`,
          name: `${domain.charAt(0).toUpperCase() + domain.slice(1)} Tools`,
          description: `All ${domain} domain tools for focused work`,
          tools: groupTools,
          groupType: 'domain' as const,
          cohesionScore: this.calculateDomainCohesion(groupTools),
          cognitiveEfficiency: this.calculateCognitiveEfficiency(groupTools),
          switchingCost: this.calculateSwitchingCost(groupTools),
          recommendationStrength: this.calculateRecommendationStrength(groupTools, 'domain'),
          usagePattern: this.analyzeGroupUsagePattern(groupTools),
          metadata: {
            createdAt: new Date(),
            successRate: 80,
            userFeedback: 0
          }
        }];
      })
      .flat();
  }

  private createDomainSubgroups(domain: string, tools: Tool[]): ToolGroup[] {
    // Group by complexity levels
    const complexityGroups = {
      basic: tools.filter(t => t.complexity_score <= 3),
      intermediate: tools.filter(t => t.complexity_score > 3 && t.complexity_score <= 7),
      advanced: tools.filter(t => t.complexity_score > 7)
    };
    
    return Object.entries(complexityGroups)
      .filter(([_, groupTools]) => groupTools.length > 0)
      .map(([level, groupTools]) => ({
        id: `domain-${domain}-${level}`,
        name: `${domain.charAt(0).toUpperCase() + domain.slice(1)} - ${level.charAt(0).toUpperCase() + level.slice(1)}`,
        description: `${level.charAt(0).toUpperCase() + level.slice(1)} ${domain} tools`,
        tools: groupTools,
        groupType: 'domain' as const,
        cohesionScore: this.calculateDomainCohesion(groupTools),
        cognitiveEfficiency: this.calculateCognitiveEfficiency(groupTools),
        switchingCost: this.calculateSwitchingCost(groupTools),
        recommendationStrength: this.calculateRecommendationStrength(groupTools, 'domain'),
        usagePattern: this.analyzeGroupUsagePattern(groupTools),
        metadata: {
          createdAt: new Date(),
          successRate: 75,
          userFeedback: 0
        }
      }));
  }

  private createFrequencyGroups(tools: Tool[]): ToolGroup[] {
    const sortedByFrequency = tools
      .map(tool => ({
        tool,
        frequency: this.usageHistory.get(tool.id)?.[0] || 0
      }))
      .sort((a, b) => b.frequency - a.frequency);
    
    const groups = [];
    const frequentTools = sortedByFrequency.filter(t => t.frequency > 50).map(t => t.tool);
    
    if (frequentTools.length >= 2) {
      // Create groups of 3-5 most frequently used tools
      for (let i = 0; i < frequentTools.length; i += 4) {
        const groupTools = frequentTools.slice(i, i + 4);
        if (groupTools.length >= 2) {
          groups.push({
            id: `frequency-${i / 4}`,
            name: `Frequently Used ${i === 0 ? 'Primary' : 'Secondary'}`,
            description: `Your most frequently accessed tools for quick access`,
            tools: groupTools,
            groupType: 'frequency' as const,
            cohesionScore: this.calculateFrequencyCohesion(groupTools),
            cognitiveEfficiency: this.calculateCognitiveEfficiency(groupTools),
            switchingCost: this.calculateSwitchingCost(groupTools),
            recommendationStrength: this.calculateRecommendationStrength(groupTools, 'frequency'),
            usagePattern: this.analyzeGroupUsagePattern(groupTools),
            metadata: {
              createdAt: new Date(),
              successRate: 90,
              userFeedback: 0
            }
          });
        }
      }
    }
    
    return groups;
  }

  private createComplexityGroups(tools: Tool[]): ToolGroup[] {
    const complexityLevels = {
      simple: tools.filter(t => t.complexity_score <= 3),
      moderate: tools.filter(t => t.complexity_score > 3 && t.complexity_score <= 6),
      complex: tools.filter(t => t.complexity_score > 6)
    };
    
    return Object.entries(complexityLevels)
      .filter(([_, groupTools]) => groupTools.length >= 2)
      .map(([level, groupTools]) => ({
        id: `complexity-${level}`,
        name: `${level.charAt(0).toUpperCase() + level.slice(1)} Tools`,
        description: `Tools with ${level} cognitive demands for balanced mental load`,
        tools: groupTools.slice(0, this.config.maxGroupSize),
        groupType: 'complexity' as const,
        cohesionScore: this.calculateComplexityCohesion(groupTools),
        cognitiveEfficiency: this.calculateCognitiveEfficiency(groupTools),
        switchingCost: this.calculateSwitchingCost(groupTools),
        recommendationStrength: this.calculateRecommendationStrength(groupTools, 'complexity'),
        usagePattern: this.analyzeGroupUsagePattern(groupTools),
        metadata: {
          createdAt: new Date(),
          successRate: 70,
          userFeedback: 0
        }
      }));
  }

  private createContextualGroups(tools: Tool[]): ToolGroup[] {
    const groups: ToolGroup[] = [];
    const processed = new Set<string>();
    
    tools.forEach(tool => {
      if (processed.has(tool.id)) return;
      
      const cooccurrences = this.cooccurrenceMatrix.get(tool.id);
      if (!cooccurrences) return;
      
      // Find tools that frequently co-occur with this tool
      const relatedTools = Array.from(cooccurrences.entries())
        .filter(([_, count]) => count >= 3) // Minimum co-occurrence threshold
        .sort(([_, a], [__, b]) => b - a)
        .slice(0, this.config.maxGroupSize - 1)
        .map(([toolId]) => tools.find(t => t.id === toolId))
        .filter(t => t && !processed.has(t.id)) as Tool[];
      
      if (relatedTools.length >= 1) {
        const groupTools = [tool, ...relatedTools];
        groupTools.forEach(t => processed.add(t.id));
        
        groups.push({
          id: `contextual-${tool.id}`,
          name: `${tool.display_name} Context`,
          description: `Tools frequently used together with ${tool.display_name}`,
          tools: groupTools,
          groupType: 'contextual' as const,
          cohesionScore: this.calculateContextualCohesion(groupTools),
          cognitiveEfficiency: this.calculateCognitiveEfficiency(groupTools),
          switchingCost: this.calculateSwitchingCost(groupTools),
          recommendationStrength: this.calculateRecommendationStrength(groupTools, 'contextual'),
          usagePattern: this.analyzeGroupUsagePattern(groupTools),
          metadata: {
            createdAt: new Date(),
            successRate: 85,
            userFeedback: 0
          }
        });
      }
    });
    
    return groups;
  }

  // Cohesion calculation methods
  private calculateWorkflowCohesion(tools: Tool[]): number {
    // Tools in same workflow should have similar complexity and session duration
    const avgComplexity = tools.reduce((sum, t) => sum + t.complexity_score, 0) / tools.length;
    const complexityVariance = tools.reduce((sum, t) => sum + Math.pow(t.complexity_score - avgComplexity, 2), 0) / tools.length;
    
    // Lower variance = higher cohesion
    return Math.max(0, Math.min(100, 100 - complexityVariance * 10));
  }

  private calculateDomainCohesion(tools: Tool[]): number {
    // Same domain tools have natural cohesion, but complexity spread matters
    const avgComplexity = tools.reduce((sum, t) => sum + t.complexity_score, 0) / tools.length;
    const complexitySpread = Math.max(...tools.map(t => t.complexity_score)) - Math.min(...tools.map(t => t.complexity_score));
    
    return Math.max(60, Math.min(100, 100 - complexitySpread * 5));
  }

  private calculateFrequencyCohesion(tools: Tool[]): number {
    // Frequently used tools together have high cohesion
    const frequencies = tools.map(t => this.usageHistory.get(t.id)?.[0] || 0);
    const avgFreq = frequencies.reduce((sum, f) => sum + f, 0) / frequencies.length;
    
    return Math.min(100, avgFreq * 1.2);
  }

  private calculateComplexityCohesion(tools: Tool[]): number {
    // Tools with similar complexity have high cohesion
    const complexities = tools.map(t => t.complexity_score);
    const variance = complexities.reduce((sum, c) => sum + Math.pow(c - complexities.reduce((s, x) => s + x, 0) / complexities.length, 2), 0) / complexities.length;
    
    return Math.max(0, Math.min(100, 100 - variance * 15));
  }

  private calculateContextualCohesion(tools: Tool[]): number {
    if (tools.length < 2) return 0;
    
    let totalCooccurrence = 0;
    let pairs = 0;
    
    for (let i = 0; i < tools.length; i++) {
      for (let j = i + 1; j < tools.length; j++) {
        const cooccurrence = this.cooccurrenceMatrix.get(tools[i].id)?.get(tools[j].id) || 0;
        totalCooccurrence += cooccurrence;
        pairs++;
      }
    }
    
    const avgCooccurrence = totalCooccurrence / pairs;
    return Math.min(100, avgCooccurrence * 20);
  }

  private calculateCognitiveEfficiency(tools: Tool[]): number {
    // Lower total cognitive load = higher efficiency
    const totalLoad = tools.reduce((sum, t) => sum + t.cognitive_load_score, 0);
    const avgLoad = totalLoad / tools.length;
    
    // Efficiency is inverse of cognitive load
    return Math.max(0, Math.min(100, 100 - avgLoad * 10));
  }

  private calculateSwitchingCost(tools: Tool[]): number {
    // Cost based on complexity differences and domain differences
    let totalCost = 0;
    let pairs = 0;
    
    for (let i = 0; i < tools.length; i++) {
      for (let j = i + 1; j < tools.length; j++) {
        const complexityDiff = Math.abs(tools[i].complexity_score - tools[j].complexity_score);
        const domainDiff = tools[i].domain !== tools[j].domain ? 20 : 0;
        
        totalCost += complexityDiff * 5 + domainDiff;
        pairs++;
      }
    }
    
    return pairs > 0 ? Math.min(100, totalCost / pairs) : 0;
  }

  private calculateRecommendationStrength(tools: Tool[], groupType: string): number {
    const baseStrength = {
      workflow: 90,
      frequency: 85,
      contextual: 80,
      domain: 75,
      complexity: 65
    }[groupType] || 50;
    
    // Adjust based on usage patterns and tool count
    const sizeBonus = Math.max(0, 5 - Math.abs(tools.length - 3)); // Optimal size is around 3 tools
    const usageBonus = tools.reduce((sum, t) => sum + (this.usageHistory.get(t.id)?.[0] || 0), 0) / tools.length / 10;
    
    return Math.min(100, baseStrength + sizeBonus + usageBonus);
  }

  private analyzeGroupUsagePattern(tools: Tool[]) {
    const frequencies = tools.map(t => this.usageHistory.get(t.id)?.[0] || 0);
    const avgFrequency = frequencies.reduce((sum, f) => sum + f, 0) / frequencies.length;
    
    // Analyze temporal patterns
    const hourlyUsage = new Array(24).fill(0);
    tools.forEach(tool => {
      const pattern = this.temporalPatterns.get(tool.id);
      if (pattern) {
        pattern.forEach((count, hour) => {
          hourlyUsage[hour] += count;
        });
      }
    });
    
    const peakHours = hourlyUsage
      .map((count, hour) => ({ hour, count }))
      .filter(h => h.count > 0)
      .sort((a, b) => b.count - a.count)
      .slice(0, 3)
      .map(h => h.hour);
    
    return {
      frequency: avgFrequency,
      sessionDuration: tools.reduce((sum, t) => sum + t.typical_session_duration, 0) / tools.length,
      timeOfDay: peakHours,
      userTypes: ['power-user', 'casual'] // Placeholder - would be determined by actual usage analysis
    };
  }

  private optimizeGroups(groups: ToolGroup[]): ToolGroup[] {
    // Filter groups that meet minimum standards
    const filtered = groups.filter(group => 
      group.cohesionScore >= this.config.minCohesionScore &&
      group.tools.length >= 2 &&
      group.tools.length <= this.config.maxGroupSize
    );
    
    // Sort by recommendation strength
    const sorted = filtered.sort((a, b) => b.recommendationStrength - a.recommendationStrength);
    
    // Remove duplicate tools across groups (keep in highest-scoring group)
    const toolAssignments = new Map<string, string>();
    const optimized = sorted.filter(group => {
      const unassignedTools = group.tools.filter(tool => !toolAssignments.has(tool.id));
      
      if (unassignedTools.length >= 2) {
        // Update group with only unassigned tools
        group.tools = unassignedTools;
        unassignedTools.forEach(tool => toolAssignments.set(tool.id, group.id));
        
        // Recalculate metrics with reduced tool set
        group.cohesionScore = this.recalculateCohesion(group);
        group.cognitiveEfficiency = this.calculateCognitiveEfficiency(group.tools);
        group.switchingCost = this.calculateSwitchingCost(group.tools);
        
        return group.cohesionScore >= this.config.minCohesionScore;
      }
      
      return false;
    });
    
    return optimized;
  }

  private recalculateCohesion(group: ToolGroup): number {
    switch (group.groupType) {
      case 'workflow': return this.calculateWorkflowCohesion(group.tools);
      case 'domain': return this.calculateDomainCohesion(group.tools);
      case 'frequency': return this.calculateFrequencyCohesion(group.tools);
      case 'complexity': return this.calculateComplexityCohesion(group.tools);
      case 'contextual': return this.calculateContextualCohesion(group.tools);
      default: return 50;
    }
  }
}

/**
 * React Hook for Smart Tool Grouping
 */
export function useSmartToolGrouping(tools: Tool[], config?: Partial<ClusteringConfig>) {
  const { performanceMetrics } = usePerformance();
  const { activeTools } = useGlobalStore();
  const { getSwitchingStats } = useContextSwitchPrevention();
  
  const [clustering] = useState(() => new SmartToolClusteringService(config));
  const [groups, setGroups] = useState<ToolGroup[]>([]);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  
  // Generate usage events from performance metrics and active tools
  const usageEvents = useMemo(() => {
    return performanceMetrics.map(metric => ({
      toolId: metric.toolName,
      timestamp: new Date(metric.timestamp),
      sessionDuration: metric.responseTime / 1000 / 60, // Convert to minutes
      context: metric.context
    }));
  }, [performanceMetrics]);
  
  // Analyze and generate groups
  useEffect(() => {
    if (tools.length === 0) return;
    
    setIsAnalyzing(true);
    
    // Analyze usage patterns
    clustering.analyzeUsagePatterns(tools, usageEvents);
    
    // Generate groups
    const generatedGroups = clustering.generateToolGroups(tools);
    setGroups(generatedGroups);
    
    setIsAnalyzing(false);
  }, [tools, usageEvents, clustering]);
  
  // Update group feedback
  const updateGroupFeedback = useCallback((groupId: string, feedback: number) => {
    setGroups(prev => prev.map(group => 
      group.id === groupId 
        ? { ...group, metadata: { ...group.metadata, userFeedback: feedback } }
        : group
    ));
  }, []);
  
  // Get recommended groups for current context
  const getContextualRecommendations = useCallback((currentToolId?: string) => {
    if (!currentToolId) return groups.slice(0, 3);
    
    // Find groups containing current tool or related tools
    const contextualGroups = groups.filter(group => 
      group.tools.some(tool => tool.id === currentToolId) ||
      group.groupType === 'contextual'
    );
    
    return contextualGroups.length > 0 ? contextualGroups : groups.slice(0, 3);
  }, [groups]);
  
  return {
    groups,
    isAnalyzing,
    updateGroupFeedback,
    getContextualRecommendations,
    switchingStats: getSwitchingStats()
  };
}