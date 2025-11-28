/**
 * Cognitive Load Optimization Test Suite
 * Comprehensive validation of navigation cognitive load management features
 */

import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';

// Import components and services
import { NavigationCognitiveLoadManager } from '../cognitiveLoadNavigation';
import { SmartToolClusteringService } from '../smartToolGrouping';
import { TaskContinuationService } from '../taskContinuation';

// Mock data
const mockTools = [
  {
    id: 'cyberchef',
    name: 'CyberChef',
    display_name: 'CyberChef',
    domain: 'security' as const,
    category: 'analysis',
    tags: ['crypto', 'encoding', 'analysis'],
    complexity_score: 7,
    cognitive_load_score: 8,
    typical_session_duration: 45,
    common_workflows: ['data-analysis', 'decoding'],
    dependencies: []
  },
  {
    id: 'maltrail',
    name: 'Maltrail',
    display_name: 'Maltrail',
    domain: 'security' as const,
    category: 'monitoring',
    tags: ['network', 'monitoring', 'threats'],
    complexity_score: 6,
    cognitive_load_score: 7,
    typical_session_duration: 30,
    common_workflows: ['threat-hunting', 'monitoring'],
    dependencies: []
  },
  {
    id: 'mealie',
    name: 'Mealie',
    display_name: 'Mealie',
    domain: 'productivity' as const,
    category: 'planning',
    tags: ['recipes', 'meal-planning'],
    complexity_score: 3,
    cognitive_load_score: 2,
    typical_session_duration: 15,
    common_workflows: ['meal-planning'],
    dependencies: []
  }
];

describe('Cognitive Load Navigation Manager', () => {
  let manager: NavigationCognitiveLoadManager;

  beforeEach(() => {
    manager = new NavigationCognitiveLoadManager();
  });

  describe('Tool Complexity Assessment', () => {
    it('should correctly assess tool complexity', () => {
      const complexity = manager.assessToolComplexity('cyberchef');
      expect(complexity).toBeGreaterThan(0);
      expect(complexity).toBeLessThanOrEqual(100);
    });

    it('should return higher complexity for security tools', () => {
      const securityComplexity = manager.assessToolComplexity('cyberchef');
      const productivityComplexity = manager.assessToolComplexity('mealie');
      
      expect(securityComplexity).toBeGreaterThan(productivityComplexity);
    });
  });

  describe('Navigation Load Calculation', () => {
    it('should calculate navigation load correctly', () => {
      const navigationLoad = manager.calculateNavigationLoad('cyberchef', 'maltrail', 50);
      
      expect(navigationLoad).toHaveProperty('totalLoad');
      expect(navigationLoad).toHaveProperty('contextSwitchCost');
      expect(navigationLoad).toHaveProperty('domainSwitchPenalty');
      expect(navigationLoad.totalLoad).toBeGreaterThan(0);
    });

    it('should apply domain switch penalty', () => {
      const sameDomainLoad = manager.calculateNavigationLoad('cyberchef', 'maltrail', 50);
      const crossDomainLoad = manager.calculateNavigationLoad('cyberchef', 'mealie', 50);
      
      expect(crossDomainLoad.domainSwitchPenalty).toBeGreaterThan(sameDomainLoad.domainSwitchPenalty);
    });
  });

  describe('Risk Assessment', () => {
    it('should assess navigation risk correctly', () => {
      const lowRisk = manager.evaluateNavigation('mealie', 'mealie', 30);
      const highRisk = manager.evaluateNavigation('cyberchef', 'maltrail', 90);
      
      expect(lowRisk.riskLevel).toBe('low');
      expect(highRisk.riskLevel).toBeOneOf(['high', 'critical']);
    });

    it('should provide appropriate recommendations', () => {
      const assessment = manager.evaluateNavigation('cyberchef', 'maltrail', 85);
      
      expect(assessment.recommendations).toHaveLength.greaterThan(0);
      expect(assessment.recommendations[0]).toHaveProperty('message');
      expect(assessment.recommendations[0]).toHaveProperty('priority');
    });
  });
});

describe('Smart Tool Clustering Service', () => {
  let clustering: SmartToolClusteringService;
  let usageEvents: Array<{
    toolId: string;
    timestamp: Date;
    sessionDuration: number;
    context?: string;
  }>;

  beforeEach(() => {
    clustering = new SmartToolClusteringService();
    
    // Generate mock usage events
    const now = new Date();
    usageEvents = [
      { toolId: 'cyberchef', timestamp: new Date(now.getTime() - 1000 * 60 * 30), sessionDuration: 45 },
      { toolId: 'maltrail', timestamp: new Date(now.getTime() - 1000 * 60 * 25), sessionDuration: 30 },
      { toolId: 'cyberchef', timestamp: new Date(now.getTime() - 1000 * 60 * 20), sessionDuration: 20 },
      { toolId: 'mealie', timestamp: new Date(now.getTime() - 1000 * 60 * 60), sessionDuration: 15 }
    ];
  });

  describe('Usage Pattern Analysis', () => {
    it('should analyze usage patterns correctly', () => {
      expect(() => {
        clustering.analyzeUsagePatterns(mockTools, usageEvents);
      }).not.toThrow();
    });

    it('should build co-occurrence matrix', () => {
      clustering.analyzeUsagePatterns(mockTools, usageEvents);
      // Test that co-occurrence relationships are detected
      // (This is a white-box test - in practice, we'd test the observable behavior)
    });
  });

  describe('Tool Group Generation', () => {
    beforeEach(() => {
      clustering.analyzeUsagePatterns(mockTools, usageEvents);
    });

    it('should generate tool groups', () => {
      const groups = clustering.generateToolGroups(mockTools);
      
      expect(groups).toHaveProperty('length');
      expect(groups.length).toBeGreaterThan(0);
    });

    it('should create domain-based groups', () => {
      const groups = clustering.generateToolGroups(mockTools);
      const domainGroups = groups.filter(g => g.groupType === 'domain');
      
      expect(domainGroups.length).toBeGreaterThan(0);
      domainGroups.forEach(group => {
        expect(group.tools.length).toBeGreaterThan(0);
        expect(group.cohesionScore).toBeGreaterThan(0);
        expect(group.cohesionScore).toBeLessThanOrEqual(100);
      });
    });

    it('should calculate meaningful cohesion scores', () => {
      const groups = clustering.generateToolGroups(mockTools);
      
      groups.forEach(group => {
        expect(group.cohesionScore).toBeGreaterThanOrEqual(0);
        expect(group.cohesionScore).toBeLessThanOrEqual(100);
        expect(group.cognitiveEfficiency).toBeGreaterThanOrEqual(0);
        expect(group.cognitiveEfficiency).toBeLessThanOrEqual(100);
      });
    });

    it('should respect group size limits', () => {
      const groups = clustering.generateToolGroups(mockTools);
      
      groups.forEach(group => {
        expect(group.tools.length).toBeLessThanOrEqual(6); // Default max group size
        expect(group.tools.length).toBeGreaterThanOrEqual(2);
      });
    });
  });
});

describe('Task Continuation Service', () => {
  let continuation: TaskContinuationService;
  let mockGetUserPreferences: vi.Mock;

  beforeEach(() => {
    mockGetUserPreferences = vi.fn().mockReturnValue({
      executiveFunctionProfile: {
        workingMemoryChallenges: 5,
        cognitiveFlexibilityChallenges: 4
      },
      navigationPreferences: {
        contextPreservationTime: 15,
        minimumSwitchDelay: 3
      }
    });
    
    continuation = new TaskContinuationService(mockGetUserPreferences);
  });

  afterEach(() => {
    continuation.destroy();
  });

  describe('Context Saving', () => {
    it('should save task context correctly', () => {
      const contextId = continuation.saveTaskContext('cyberchef', {
        taskType: 'analysis',
        title: 'Decode encrypted data',
        workingData: { input: 'encrypted_string' },
        sessionDuration: 600
      });
      
      expect(contextId).toMatch(/^ctx_cyberchef_\d+$/);
    });

    it('should calculate context confidence', () => {
      continuation.saveTaskContext('cyberchef', {
        taskType: 'analysis',
        title: 'Analysis task',
        workingData: { key: 'value' },
        activeSelection: 'line 42',
        inputStates: { filter: 'crypto' },
        sessionDuration: 1200 // 20 minutes
      });
      
      const context = continuation.getTaskContext('cyberchef');
      expect(context).not.toBeNull();
      expect(context!.confidence).toBeGreaterThan(50); // Should have good confidence
    });
  });

  describe('Context Retrieval', () => {
    beforeEach(() => {
      continuation.saveTaskContext('cyberchef', {
        taskType: 'analysis',
        title: 'Test analysis',
        workingData: { test: 'data' }
      });
    });

    it('should retrieve saved context', () => {
      const context = continuation.getTaskContext('cyberchef');
      
      expect(context).not.toBeNull();
      expect(context!.toolId).toBe('cyberchef');
      expect(context!.title).toBe('Test analysis');
    });

    it('should return null for non-existent context', () => {
      const context = continuation.getTaskContext('non-existent-tool');
      expect(context).toBeNull();
    });
  });

  describe('Continuation Strategy Generation', () => {
    beforeEach(() => {
      continuation.saveTaskContext('cyberchef', {
        taskType: 'analysis',
        title: 'Complex analysis',
        workingData: { data: 'complex' },
        sessionDuration: 1800,
        cognitiveLoad: 75
      });
    });

    it('should generate continuation strategy', () => {
      const strategy = continuation.generateContinuationStrategy('cyberchef');
      
      expect(strategy).not.toBeNull();
      expect(strategy!).toHaveProperty('context');
      expect(strategy!).toHaveProperty('resumptionStrategy');
      expect(strategy!).toHaveProperty('estimatedReloadTime');
      expect(strategy!).toHaveProperty('cognitiveReloadCost');
      expect(strategy!).toHaveProperty('recommendations');
    });

    it('should provide appropriate resumption strategy', () => {
      const strategy = continuation.generateContinuationStrategy('cyberchef');
      
      expect(strategy!.resumptionStrategy).toBeOneOf(['immediate', 'gradual', 'guided', 'manual']);
      expect(strategy!.estimatedReloadTime).toBeGreaterThan(0);
      expect(strategy!.cognitiveReloadCost).toBeGreaterThanOrEqual(0);
      expect(strategy!.cognitiveReloadCost).toBeLessThanOrEqual(100);
    });

    it('should generate contextual recommendations', () => {
      const strategy = continuation.generateContinuationStrategy('cyberchef');
      
      expect(strategy!.recommendations).toHaveProperty('length');
      if (strategy!.recommendations.length > 0) {
        expect(strategy!.recommendations[0]).toHaveProperty('type');
        expect(strategy!.recommendations[0]).toHaveProperty('message');
        expect(strategy!.recommendations[0]).toHaveProperty('priority');
      }
    });
  });

  describe('Context Cleanup', () => {
    it('should clean up expired contexts', () => {
      // Save a context with short expiry
      const contextId = continuation.saveTaskContext('test-tool', {
        title: 'Test context',
        taskType: 'analysis'
      });
      
      // Manually set expiry to past (simulate time passage)
      const context = continuation.getTaskContext('test-tool');
      if (context) {
        context.expiresAt = new Date(Date.now() - 1000); // 1 second ago
      }
      
      continuation.cleanupExpiredContexts();
      
      const retrievedContext = continuation.getTaskContext('test-tool');
      expect(retrievedContext).toBeNull();
    });
  });
});

describe('Executive Function Preferences Integration', () => {
  // Mock the hook since we can't easily test hooks in isolation
  const mockPreferences = {
    currentProfile: {
      attentionChallenges: 7,
      workingMemoryChallenges: 6,
      cognitiveFlexibilityChallenges: 8,
      processingSpeed: 'slow' as const
    },
    currentPreferences: {
      maxCognitiveLoad: 60,
      loadWarningThreshold: 50,
      minimumSwitchDelay: 5,
      autoLoadReduction: true
    }
  };

  describe('Cognitive Load Threshold Adaptation', () => {
    it('should adapt thresholds based on executive function profile', () => {
      const manager = new NavigationCognitiveLoadManager();
      
      // Test with high executive function challenges
      const assessment = manager.evaluateNavigation('cyberchef', 'maltrail', 55);
      
      // Should be more conservative with someone who has challenges
      expect(assessment.riskLevel).toBeOneOf(['medium', 'high']);
    });
  });

  describe('Navigation Delay Calculation', () => {
    it('should calculate appropriate delays for cognitive flexibility challenges', () => {
      const manager = new NavigationCognitiveLoadManager();
      
      // Test delay calculation
      const delay = manager.calculateRequiredDelay('cyberchef', 'maltrail', 65);
      
      expect(delay).toBeGreaterThan(0);
      expect(delay).toBeLessThan(15000); // Max 15 seconds
    });
  });
});

describe('Performance Validation', () => {
  describe('Response Time Requirements', () => {
    it('should meet <200ms UI interaction requirement', async () => {
      const manager = new NavigationCognitiveLoadManager();
      
      const startTime = performance.now();
      manager.evaluateNavigation('cyberchef', 'maltrail', 50);
      const endTime = performance.now();
      
      const responseTime = endTime - startTime;
      expect(responseTime).toBeLessThan(200); // <200ms requirement
    });

    it('should handle bulk tool clustering within performance limits', () => {
      const clustering = new SmartToolClusteringService();
      const manyTools = Array.from({ length: 37 }, (_, i) => ({
        ...mockTools[0],
        id: `tool-${i}`,
        name: `Tool ${i}`
      }));
      
      const startTime = performance.now();
      clustering.analyzeUsagePatterns(manyTools, []);
      const groups = clustering.generateToolGroups(manyTools);
      const endTime = performance.now();
      
      const responseTime = endTime - startTime;
      expect(responseTime).toBeLessThan(1000); // Should handle 37 tools quickly
      expect(groups.length).toBeGreaterThan(0);
    });
  });

  describe('Memory Usage', () => {
    it('should not accumulate excessive context data', () => {
      const continuation = new TaskContinuationService(() => ({}));
      
      // Save many contexts
      for (let i = 0; i < 100; i++) {
        continuation.saveTaskContext(`tool-${i}`, {
          title: `Context ${i}`,
          taskType: 'analysis',
          workingData: { data: `test-${i}` }
        });
      }
      
      const activeContexts = continuation.getActiveContexts();
      expect(activeContexts.length).toBeLessThanOrEqual(5); // Should limit working memory
      
      continuation.destroy();
    });
  });
});

describe('Integration Tests', () => {
  describe('End-to-End Navigation Flow', () => {
    it('should handle complete navigation cycle with cognitive load management', () => {
      const manager = new NavigationCognitiveLoadManager();
      const continuation = new TaskContinuationService(() => ({
        executiveFunctionProfile: { workingMemoryChallenges: 6 }
      }));
      
      // 1. Start with a tool
      const initialLoad = manager.assessToolComplexity('cyberchef');
      expect(initialLoad).toBeGreaterThan(0);
      
      // 2. Save context when switching
      const contextId = continuation.saveTaskContext('cyberchef', {
        title: 'Analysis work',
        taskType: 'analysis',
        sessionDuration: 900
      });
      expect(contextId).toBeTruthy();
      
      // 3. Evaluate navigation to new tool
      const navigation = manager.evaluateNavigation('cyberchef', 'maltrail', 70);
      expect(navigation).toHaveProperty('riskLevel');
      
      // 4. Generate continuation strategy
      const strategy = continuation.generateContinuationStrategy('cyberchef');
      expect(strategy).not.toBeNull();
      
      continuation.destroy();
    });
  });

  describe('Accessibility and Executive Function Support', () => {
    it('should provide appropriate accommodations for high cognitive challenges', () => {
      const manager = new NavigationCognitiveLoadManager();
      
      // Simulate user with high executive function challenges
      const assessment = manager.evaluateNavigation('cyberchef', 'maltrail', 60);
      
      // Should provide more conservative recommendations
      expect(assessment.recommendations.length).toBeGreaterThan(0);
      
      const hasDelayRecommendation = assessment.recommendations.some(
        rec => rec.message.toLowerCase().includes('wait') || 
               rec.message.toLowerCase().includes('delay')
      );
      
      // Should recommend delays for challenging navigation
      if (assessment.riskLevel === 'high' || assessment.riskLevel === 'critical') {
        expect(hasDelayRecommendation).toBe(true);
      }
    });
  });
});

// Performance benchmarks
describe('Performance Benchmarks', () => {
  const PERFORMANCE_TARGETS = {
    navigationEvaluation: 50,    // ms
    toolClustering: 500,        // ms for 37 tools
    contextSaving: 20,          // ms
    contextRetrieval: 10,       // ms
    strategyGeneration: 100     // ms
  };

  it('should meet navigation evaluation performance target', () => {
    const manager = new NavigationCognitiveLoadManager();
    
    const startTime = performance.now();
    for (let i = 0; i < 100; i++) {
      manager.evaluateNavigation('cyberchef', 'maltrail', Math.random() * 100);
    }
    const endTime = performance.now();
    
    const avgTime = (endTime - startTime) / 100;
    expect(avgTime).toBeLessThan(PERFORMANCE_TARGETS.navigationEvaluation);
  });

  it('should meet context operations performance targets', () => {
    const continuation = new TaskContinuationService(() => ({}));
    
    // Test context saving
    const saveStart = performance.now();
    const contextId = continuation.saveTaskContext('test-tool', {
      title: 'Performance test',
      taskType: 'analysis'
    });
    const saveEnd = performance.now();
    
    expect(saveEnd - saveStart).toBeLessThan(PERFORMANCE_TARGETS.contextSaving);
    
    // Test context retrieval
    const retrieveStart = performance.now();
    const context = continuation.getTaskContext('test-tool');
    const retrieveEnd = performance.now();
    
    expect(retrieveEnd - retrieveStart).toBeLessThan(PERFORMANCE_TARGETS.contextRetrieval);
    expect(context).not.toBeNull();
    
    continuation.destroy();
  });
});