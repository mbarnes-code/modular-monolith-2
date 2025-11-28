/**
 * Cognitive Load Optimization Validation Script
 * Real-world performance testing and validation of cognitive load management features
 */

import { performance } from 'perf_hooks';
import { NavigationCognitiveLoadManager } from '../cognitiveLoadNavigation';
import { SmartToolClusteringService } from '../smartToolGrouping';
import { TaskContinuationService } from '../taskContinuation';

// Mock 37 tools from the mental prosthetic platform
const FULL_TOOL_SET = [
  // Security Domain (13 tools)
  { id: 'misp', name: 'MISP', domain: 'security', complexity: 8, cognitiveLoad: 9 },
  { id: 'helk', name: 'HELK', domain: 'security', complexity: 9, cognitiveLoad: 8 },
  { id: 'securityonion', name: 'Security Onion', domain: 'security', complexity: 9, cognitiveLoad: 9 },
  { id: 'maltrail', name: 'Maltrail', domain: 'security', complexity: 6, cognitiveLoad: 7 },
  { id: 'yarax', name: 'YARA-X', domain: 'security', complexity: 7, cognitiveLoad: 8 },
  { id: 'cyberchef', name: 'CyberChef', domain: 'security', complexity: 7, cognitiveLoad: 8 },
  { id: 'nemesis', name: 'Nemesis', domain: 'security', complexity: 8, cognitiveLoad: 9 },
  { id: 'volatility', name: 'Volatility', domain: 'security', complexity: 9, cognitiveLoad: 9 },
  { id: 'ghidra', name: 'Ghidra', domain: 'security', complexity: 10, cognitiveLoad: 10 },
  { id: 'ida', name: 'IDA Pro', domain: 'security', complexity: 10, cognitiveLoad: 10 },
  { id: 'wireshark', name: 'Wireshark', domain: 'security', complexity: 8, cognitiveLoad: 8 },
  { id: 'nmap', name: 'Nmap', domain: 'security', complexity: 6, cognitiveLoad: 6 },
  { id: 'burpsuite', name: 'Burp Suite', domain: 'security', complexity: 8, cognitiveLoad: 8 },

  // Productivity Domain (8 tools)
  { id: 'n8n', name: 'n8n', domain: 'productivity', complexity: 6, cognitiveLoad: 6 },
  { id: 'mealie', name: 'Mealie', domain: 'productivity', complexity: 3, cognitiveLoad: 2 },
  { id: 'dispatch', name: 'Dispatch', domain: 'productivity', complexity: 5, cognitiveLoad: 5 },
  { id: 'actualbudget', name: 'Actual Budget', domain: 'productivity', complexity: 4, cognitiveLoad: 4 },
  { id: 'firecrawl', name: 'Firecrawl', domain: 'productivity', complexity: 5, cognitiveLoad: 5 },
  { id: 'goose', name: 'Goose', domain: 'productivity', complexity: 7, cognitiveLoad: 7 },
  { id: 'ittools', name: 'IT-Tools', domain: 'productivity', complexity: 4, cognitiveLoad: 3 },
  { id: 'inspector', name: 'Inspector', domain: 'productivity', complexity: 6, cognitiveLoad: 6 },

  // MTG Domain (4 tools)
  { id: 'commanderspellbook', name: 'Commander Spellbook', domain: 'mtg', complexity: 5, cognitiveLoad: 4 },
  { id: 'mtgcommander', name: 'MTG Commander Map', domain: 'mtg', complexity: 6, cognitiveLoad: 5 },
  { id: 'mtgscripting', name: 'MTG Scripting Toolkit', domain: 'mtg', complexity: 8, cognitiveLoad: 7 },
  { id: 'cardanalysis', name: 'Card Analysis Tool', domain: 'mtg', complexity: 4, cognitiveLoad: 3 },

  // Infrastructure Domain (12 tools)
  { id: 'kong', name: 'Kong Gateway', domain: 'infrastructure', complexity: 7, cognitiveLoad: 7 },
  { id: 'ghostwriter', name: 'Ghostwriter', domain: 'infrastructure', complexity: 6, cognitiveLoad: 6 },
  { id: 'kasmvnc', name: 'KasmVNC', domain: 'infrastructure', complexity: 5, cognitiveLoad: 5 },
  { id: 'mcpserver1', name: 'MCP Server 1', domain: 'infrastructure', complexity: 6, cognitiveLoad: 6 },
  { id: 'mcpserver2', name: 'MCP Server 2', domain: 'infrastructure', complexity: 6, cognitiveLoad: 6 },
  { id: 'mcpserver3', name: 'MCP Server 3', domain: 'infrastructure', complexity: 6, cognitiveLoad: 6 },
  { id: 'workflow1', name: 'Workflow Automation 1', domain: 'infrastructure', complexity: 5, cognitiveLoad: 5 },
  { id: 'workflow2', name: 'Workflow Automation 2', domain: 'infrastructure', complexity: 5, cognitiveLoad: 5 },
  { id: 'monitoring', name: 'Monitoring Dashboard', domain: 'infrastructure', complexity: 4, cognitiveLoad: 4 },
  { id: 'logging', name: 'Log Aggregation', domain: 'infrastructure', complexity: 5, cognitiveLoad: 5 },
  { id: 'metrics', name: 'Metrics Collection', domain: 'infrastructure', complexity: 4, cognitiveLoad: 4 },
  { id: 'alerting', name: 'Alert Management', domain: 'infrastructure', complexity: 3, cognitiveLoad: 3 }
];

interface ValidationResults {
  performanceTests: {
    navigationEvaluation: {
      averageTime: number;
      maxTime: number;
      successRate: number;
      target: number;
      passed: boolean;
    };
    toolClustering: {
      time: number;
      groupsGenerated: number;
      target: number;
      passed: boolean;
    };
    contextOperations: {
      saveTime: number;
      retrieveTime: number;
      strategyTime: number;
      targets: { save: number; retrieve: number; strategy: number };
      passed: boolean;
    };
  };
  functionalTests: {
    cognitiveLoadAccuracy: {
      score: number;
      passed: boolean;
    };
    executiveFunctionSupport: {
      score: number;
      passed: boolean;
    };
    contextPreservation: {
      score: number;
      passed: boolean;
    };
  };
  domainPerformance: {
    security: { averageResponseTime: number; target: number; passed: boolean };
    productivity: { averageResponseTime: number; target: number; passed: boolean };
    mtg: { averageResponseTime: number; target: number; passed: boolean };
    infrastructure: { averageResponseTime: number; target: number; passed: boolean };
  };
  overallScore: number;
  recommendations: string[];
}

export class CognitiveLoadValidationSuite {
  private results: ValidationResults = {
    performanceTests: {
      navigationEvaluation: { averageTime: 0, maxTime: 0, successRate: 0, target: 50, passed: false },
      toolClustering: { time: 0, groupsGenerated: 0, target: 500, passed: false },
      contextOperations: {
        saveTime: 0, retrieveTime: 0, strategyTime: 0,
        targets: { save: 20, retrieve: 10, strategy: 100 },
        passed: false
      }
    },
    functionalTests: {
      cognitiveLoadAccuracy: { score: 0, passed: false },
      executiveFunctionSupport: { score: 0, passed: false },
      contextPreservation: { score: 0, passed: false }
    },
    domainPerformance: {
      security: { averageResponseTime: 0, target: 1000, passed: false },
      productivity: { averageResponseTime: 0, target: 2000, passed: false },
      mtg: { averageResponseTime: 0, target: 3000, passed: false },
      infrastructure: { averageResponseTime: 0, target: 5000, passed: false }
    },
    overallScore: 0,
    recommendations: []
  };

  async runFullValidation(): Promise<ValidationResults> {
    console.log('🧠 Starting Cognitive Load Optimization Validation Suite...\n');
    
    await this.runPerformanceTests();
    await this.runFunctionalTests();
    await this.runDomainPerformanceTests();
    
    this.calculateOverallScore();
    this.generateRecommendations();
    
    this.printResults();
    return this.results;
  }

  private async runPerformanceTests(): Promise<void> {
    console.log('⚡ Running Performance Tests...');
    
    // Test 1: Navigation Evaluation Performance
    await this.testNavigationEvaluation();
    
    // Test 2: Tool Clustering Performance
    await this.testToolClustering();
    
    // Test 3: Context Operations Performance
    await this.testContextOperations();
    
    console.log('✅ Performance tests completed\n');
  }

  private async testNavigationEvaluation(): Promise<void> {
    const manager = new NavigationCognitiveLoadManager();
    const iterations = 1000;
    const times: number[] = [];
    let successCount = 0;

    for (let i = 0; i < iterations; i++) {
      const fromTool = FULL_TOOL_SET[Math.floor(Math.random() * FULL_TOOL_SET.length)];
      const toTool = FULL_TOOL_SET[Math.floor(Math.random() * FULL_TOOL_SET.length)];
      const currentLoad = Math.random() * 100;

      const start = performance.now();
      try {
        const result = manager.evaluateNavigation(fromTool.id, toTool.id, currentLoad);
        const end = performance.now();
        
        times.push(end - start);
        if (result && result.riskLevel) {
          successCount++;
        }
      } catch (error) {
        times.push(1000); // Penalty for errors
      }
    }

    this.results.performanceTests.navigationEvaluation = {
      averageTime: times.reduce((sum, time) => sum + time, 0) / times.length,
      maxTime: Math.max(...times),
      successRate: (successCount / iterations) * 100,
      target: 50,
      passed: times.reduce((sum, time) => sum + time, 0) / times.length < 50
    };
  }

  private async testToolClustering(): Promise<void> {
    const clustering = new SmartToolClusteringService();
    
    // Generate realistic usage events
    const usageEvents = this.generateUsageEvents(5000); // 5000 events
    
    const start = performance.now();
    clustering.analyzeUsagePatterns(FULL_TOOL_SET as any, usageEvents);
    const groups = clustering.generateToolGroups(FULL_TOOL_SET as any);
    const end = performance.now();

    this.results.performanceTests.toolClustering = {
      time: end - start,
      groupsGenerated: groups.length,
      target: 500,
      passed: (end - start) < 500
    };
  }

  private async testContextOperations(): Promise<void> {
    const continuation = new TaskContinuationService(() => ({
      executiveFunctionProfile: { workingMemoryChallenges: 5 }
    }));

    const testData = {
      taskType: 'analysis' as const,
      title: 'Performance test context',
      workingData: { complexData: Array.from({ length: 100 }, (_, i) => ({ id: i, value: Math.random() })) },
      sessionDuration: 1800
    };

    // Test save performance
    const saveStart = performance.now();
    const contextId = continuation.saveTaskContext('test-tool', testData);
    const saveEnd = performance.now();

    // Test retrieve performance
    const retrieveStart = performance.now();
    const context = continuation.getTaskContext('test-tool');
    const retrieveEnd = performance.now();

    // Test strategy generation performance
    const strategyStart = performance.now();
    const strategy = continuation.generateContinuationStrategy('test-tool');
    const strategyEnd = performance.now();

    const saveTime = saveEnd - saveStart;
    const retrieveTime = retrieveEnd - retrieveStart;
    const strategyTime = strategyEnd - strategyStart;

    this.results.performanceTests.contextOperations = {
      saveTime,
      retrieveTime,
      strategyTime,
      targets: { save: 20, retrieve: 10, strategy: 100 },
      passed: saveTime < 20 && retrieveTime < 10 && strategyTime < 100
    };

    continuation.destroy();
  }

  private async runFunctionalTests(): Promise<void> {
    console.log('🔍 Running Functional Tests...');
    
    await this.testCognitiveLoadAccuracy();
    await this.testExecutiveFunctionSupport();
    await this.testContextPreservation();
    
    console.log('✅ Functional tests completed\n');
  }

  private async testCognitiveLoadAccuracy(): Promise<void> {
    const manager = new NavigationCognitiveLoadManager();
    let score = 0;
    const testCases = 100;

    for (let i = 0; i < testCases; i++) {
      const highComplexityTool = FULL_TOOL_SET.find(t => t.complexity >= 8);
      const lowComplexityTool = FULL_TOOL_SET.find(t => t.complexity <= 3);
      
      if (highComplexityTool && lowComplexityTool) {
        const highComplexityLoad = manager.assessToolComplexity(highComplexityTool.id);
        const lowComplexityLoad = manager.assessToolComplexity(lowComplexityTool.id);
        
        // High complexity tools should have higher cognitive load
        if (highComplexityLoad > lowComplexityLoad) {
          score += 1;
        }
      }
    }

    this.results.functionalTests.cognitiveLoadAccuracy = {
      score: (score / testCases) * 100,
      passed: (score / testCases) > 0.85 // 85% accuracy threshold
    };
  }

  private async testExecutiveFunctionSupport(): Promise<void> {
    const manager = new NavigationCognitiveLoadManager();
    let supportScore = 0;
    const testCases = 50;

    for (let i = 0; i < testCases; i++) {
      const highLoadScenario = manager.evaluateNavigation('ghidra', 'ida', 85);
      
      // Should provide recommendations for high-load scenarios
      if (highLoadScenario.recommendations.length > 0) supportScore += 1;
      
      // Should flag high-risk scenarios
      if (highLoadScenario.riskLevel === 'high' || highLoadScenario.riskLevel === 'critical') {
        supportScore += 1;
      }
    }

    this.results.functionalTests.executiveFunctionSupport = {
      score: (supportScore / (testCases * 2)) * 100,
      passed: (supportScore / (testCases * 2)) > 0.8
    };
  }

  private async testContextPreservation(): Promise<void> {
    const continuation = new TaskContinuationService(() => ({}));
    let preservationScore = 0;
    const testCases = 20;

    for (let i = 0; i < testCases; i++) {
      const contextData = {
        taskType: 'analysis' as const,
        title: `Test context ${i}`,
        workingData: { testData: `data-${i}`, number: i },
        activeSelection: `line-${i * 10}`,
        sessionDuration: 300 + i * 60
      };

      const contextId = continuation.saveTaskContext(`tool-${i}`, contextData);
      const retrieved = continuation.getTaskContext(`tool-${i}`);

      if (retrieved) {
        // Check data preservation
        if (retrieved.title === contextData.title) preservationScore += 1;
        if (retrieved.workingData.testData === contextData.workingData.testData) preservationScore += 1;
        if (retrieved.activeSelection === contextData.activeSelection) preservationScore += 1;
        if (retrieved.confidence > 0) preservationScore += 1;
      }
    }

    this.results.functionalTests.contextPreservation = {
      score: (preservationScore / (testCases * 4)) * 100,
      passed: (preservationScore / (testCases * 4)) > 0.9
    };

    continuation.destroy();
  }

  private async runDomainPerformanceTests(): Promise<void> {
    console.log('🎯 Running Domain Performance Tests...');
    
    const manager = new NavigationCognitiveLoadManager();
    const domains = ['security', 'productivity', 'mtg', 'infrastructure'] as const;

    for (const domain of domains) {
      const domainTools = FULL_TOOL_SET.filter(t => t.domain === domain);
      const times: number[] = [];

      // Test intra-domain navigation performance
      for (let i = 0; i < 100; i++) {
        const fromTool = domainTools[Math.floor(Math.random() * domainTools.length)];
        const toTool = domainTools[Math.floor(Math.random() * domainTools.length)];

        const start = performance.now();
        manager.evaluateNavigation(fromTool.id, toTool.id, Math.random() * 100);
        const end = performance.now();

        times.push(end - start);
      }

      const averageTime = times.reduce((sum, time) => sum + time, 0) / times.length;
      const target = this.results.domainPerformance[domain].target;

      this.results.domainPerformance[domain] = {
        averageResponseTime: averageTime,
        target,
        passed: averageTime < target
      };
    }

    console.log('✅ Domain performance tests completed\n');
  }

  private generateUsageEvents(count: number): Array<{
    toolId: string;
    timestamp: Date;
    sessionDuration: number;
    context?: string;
  }> {
    const events = [];
    const now = new Date();

    for (let i = 0; i < count; i++) {
      const tool = FULL_TOOL_SET[Math.floor(Math.random() * FULL_TOOL_SET.length)];
      const timestamp = new Date(now.getTime() - Math.random() * 7 * 24 * 60 * 60 * 1000); // Last 7 days
      
      events.push({
        toolId: tool.id,
        timestamp,
        sessionDuration: Math.random() * 3600, // 0-60 minutes
        context: tool.domain
      });
    }

    return events.sort((a, b) => a.timestamp.getTime() - b.timestamp.getTime());
  }

  private calculateOverallScore(): void {
    const weights = {
      performance: 0.4,
      functional: 0.4,
      domain: 0.2
    };

    // Performance score
    const perfTests = this.results.performanceTests;
    const perfScore = (
      (perfTests.navigationEvaluation.passed ? 100 : 0) * 0.4 +
      (perfTests.toolClustering.passed ? 100 : 0) * 0.3 +
      (perfTests.contextOperations.passed ? 100 : 0) * 0.3
    );

    // Functional score
    const funcTests = this.results.functionalTests;
    const funcScore = (
      funcTests.cognitiveLoadAccuracy.score * 0.4 +
      funcTests.executiveFunctionSupport.score * 0.4 +
      funcTests.contextPreservation.score * 0.2
    );

    // Domain score
    const domainTests = this.results.domainPerformance;
    const domainScore = Object.values(domainTests).reduce((sum, domain) => 
      sum + (domain.passed ? 25 : 0), 0
    );

    this.results.overallScore = 
      perfScore * weights.performance +
      funcScore * weights.functional +
      domainScore * weights.domain;
  }

  private generateRecommendations(): void {
    const recommendations: string[] = [];

    // Performance recommendations
    if (!this.results.performanceTests.navigationEvaluation.passed) {
      recommendations.push(
        `Navigation evaluation averaging ${this.results.performanceTests.navigationEvaluation.averageTime.toFixed(2)}ms exceeds 50ms target. Consider optimizing load calculations.`
      );
    }

    if (!this.results.performanceTests.toolClustering.passed) {
      recommendations.push(
        `Tool clustering took ${this.results.performanceTests.toolClustering.time.toFixed(2)}ms, exceeding 500ms target. Consider caching or algorithmic optimization.`
      );
    }

    // Functional recommendations
    if (this.results.functionalTests.cognitiveLoadAccuracy.score < 90) {
      recommendations.push(
        `Cognitive load accuracy at ${this.results.functionalTests.cognitiveLoadAccuracy.score.toFixed(1)}% could be improved. Review complexity scoring algorithms.`
      );
    }

    if (this.results.functionalTests.executiveFunctionSupport.score < 85) {
      recommendations.push(
        `Executive function support scoring ${this.results.functionalTests.executiveFunctionSupport.score.toFixed(1)}%. Enhance recommendation engine and risk assessment.`
      );
    }

    // Domain recommendations
    Object.entries(this.results.domainPerformance).forEach(([domain, results]) => {
      if (!results.passed) {
        recommendations.push(
          `${domain.charAt(0).toUpperCase() + domain.slice(1)} domain performance (${results.averageResponseTime.toFixed(2)}ms) exceeds ${results.target}ms target.`
        );
      }
    });

    if (recommendations.length === 0) {
      recommendations.push('🎉 All tests passed! Cognitive load optimization is performing within targets.');
    }

    this.results.recommendations = recommendations;
  }

  private printResults(): void {
    console.log('📊 COGNITIVE LOAD OPTIMIZATION VALIDATION RESULTS');
    console.log('='.repeat(60));
    console.log(`Overall Score: ${this.results.overallScore.toFixed(1)}/100`);
    console.log('');

    // Performance Results
    console.log('⚡ PERFORMANCE TESTS');
    console.log('-'.repeat(30));
    const perf = this.results.performanceTests;
    console.log(`Navigation Evaluation: ${perf.navigationEvaluation.averageTime.toFixed(2)}ms avg (target: ${perf.navigationEvaluation.target}ms) ${perf.navigationEvaluation.passed ? '✅' : '❌'}`);
    console.log(`Tool Clustering: ${perf.toolClustering.time.toFixed(2)}ms (target: ${perf.toolClustering.target}ms) ${perf.toolClustering.passed ? '✅' : '❌'}`);
    console.log(`Context Save: ${perf.contextOperations.saveTime.toFixed(2)}ms (target: ${perf.contextOperations.targets.save}ms)`);
    console.log(`Context Retrieve: ${perf.contextOperations.retrieveTime.toFixed(2)}ms (target: ${perf.contextOperations.targets.retrieve}ms)`);
    console.log(`Strategy Generation: ${perf.contextOperations.strategyTime.toFixed(2)}ms (target: ${perf.contextOperations.targets.strategy}ms)`);
    console.log(`Context Operations: ${perf.contextOperations.passed ? '✅' : '❌'}`);
    console.log('');

    // Functional Results
    console.log('🔍 FUNCTIONAL TESTS');
    console.log('-'.repeat(30));
    const func = this.results.functionalTests;
    console.log(`Cognitive Load Accuracy: ${func.cognitiveLoadAccuracy.score.toFixed(1)}% ${func.cognitiveLoadAccuracy.passed ? '✅' : '❌'}`);
    console.log(`Executive Function Support: ${func.executiveFunctionSupport.score.toFixed(1)}% ${func.executiveFunctionSupport.passed ? '✅' : '❌'}`);
    console.log(`Context Preservation: ${func.contextPreservation.score.toFixed(1)}% ${func.contextPreservation.passed ? '✅' : '❌'}`);
    console.log('');

    // Domain Results
    console.log('🎯 DOMAIN PERFORMANCE');
    console.log('-'.repeat(30));
    Object.entries(this.results.domainPerformance).forEach(([domain, results]) => {
      console.log(`${domain.charAt(0).toUpperCase() + domain.slice(1)} Domain: ${results.averageResponseTime.toFixed(2)}ms (target: ${results.target}ms) ${results.passed ? '✅' : '❌'}`);
    });
    console.log('');

    // Recommendations
    console.log('💡 RECOMMENDATIONS');
    console.log('-'.repeat(30));
    this.results.recommendations.forEach((rec, index) => {
      console.log(`${index + 1}. ${rec}`);
    });
  }
}

// Export for use in automated testing
export { ValidationResults };

// Run validation if called directly
if (require.main === module) {
  const validator = new CognitiveLoadValidationSuite();
  validator.runFullValidation().then(results => {
    process.exit(results.overallScore >= 80 ? 0 : 1); // Pass if score >= 80
  });
}