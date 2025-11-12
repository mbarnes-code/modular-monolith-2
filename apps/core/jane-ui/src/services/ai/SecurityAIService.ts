/**
 * Security AI Service
 * 
 * AI assistance integration for security domain components.
 * Provides context-aware recommendations and threat intelligence queries.
 */

import { AIService } from '../../services/ai/AIService';
import { securityPerformanceMonitor } from '../performance/SecurityPerformanceMonitor';

interface SecurityContext {
  domain: 'security';
  tool?: string;
  alertId?: string;
  indicators?: string[];
  severity?: 'critical' | 'high' | 'medium' | 'low';
  threatType?: string;
}

interface ThreatIntelRequest {
  indicators: string[];
  context?: string;
  sources?: string[];
}

interface ThreatIntelResponse {
  matches: Array<{
    indicator: string;
    source: string;
    confidence: number;
    description: string;
    recommendations: string[];
  }>;
  overallRisk: 'critical' | 'high' | 'medium' | 'low';
  recommendations: string[];
}

interface SecurityRecommendation {
  id: string;
  type: 'investigation' | 'containment' | 'mitigation' | 'hunting';
  title: string;
  description: string;
  priority: number;
  confidence: number;
  actions: Array<{
    tool: string;
    action: string;
    parameters?: Record<string, unknown>;
  }>;
}

export class SecurityAIService {
  private aiService: AIService;
  private contextHistory: SecurityContext[] = [];

  constructor() {
    this.aiService = new AIService({
      domain: 'security',
      responseTimeTarget: 1000, // Constitutional requirement: <1s for security domain
      specialization: 'threat_analysis'
    });
  }

  /**
   * Get AI-powered security recommendations based on context
   */
  async getSecurityRecommendations(context: SecurityContext): Promise<SecurityRecommendation[]> {
    const endTiming = securityPerformanceMonitor.startTiming('security_ai_recommendations');
    
    try {
      // Add to context history for better recommendations
      this.contextHistory.push(context);
      
      // Keep only last 10 contexts to prevent memory bloat
      if (this.contextHistory.length > 10) {
        this.contextHistory = this.contextHistory.slice(-10);
      }

      const prompt = this.buildRecommendationPrompt(context);
      const response = await this.aiService.query({
        prompt,
        context: {
          domain: 'security',
          previousContexts: this.contextHistory.slice(-3), // Last 3 contexts
          timestamp: new Date().toISOString()
        },
        options: {
          maxTokens: 1000,
          temperature: 0.3, // Lower temperature for more deterministic security recommendations
          responseFormat: 'structured'
        }
      });

      const recommendations = this.parseRecommendations(response);
      endTiming({ success: true, tool: context.tool });
      
      return recommendations;

    } catch (error) {
      endTiming({ success: false, tool: context.tool });
      return this.getFallbackRecommendations(context);
    }
  }

  /**
   * Query threat intelligence for indicators of compromise
   */
  async queryThreatIntelligence(request: ThreatIntelRequest): Promise<ThreatIntelResponse> {
    const startTime = Date.now();
    
    try {
      const prompt = this.buildThreatIntelPrompt(request);
      const response = await this.aiService.query({
        prompt,
        context: {
          domain: 'security',
          operation: 'threat_intelligence',
          indicators: request.indicators,
          timestamp: new Date().toISOString()
        },
        options: {
          maxTokens: 1500,
          temperature: 0.2, // Very low temperature for factual threat intel
          responseFormat: 'structured'
        }
      });

      const threatIntel = this.parseThreatIntelligence(response);
      
      // Validate response time
      const responseTime = Date.now() - startTime;
      if (responseTime > 1000) {
        console.warn(`Threat intelligence query exceeded 1s: ${responseTime}ms`);
      }

      return threatIntel;

    } catch (error) {
      console.error('Threat intelligence query failed:', error);
      return this.getFallbackThreatIntel(request);
    }
  }

  /**
   * Analyze security alert and provide AI-powered insights
   */
  async analyzeSecurityAlert(alert: {
    id: string;
    title: string;
    description: string;
    severity: string;
    indicators: string[];
    source: string;
  }): Promise<{
    analysis: string;
    riskAssessment: string;
    nextSteps: string[];
    relatedThreats: string[];
    confidence: number;
  }> {
    const startTime = Date.now();
    
    try {
      const context: SecurityContext = {
        domain: 'security',
        alertId: alert.id,
        indicators: alert.indicators,
        severity: alert.severity as SecurityContext['severity'],
        tool: alert.source
      };

      const prompt = this.buildAlertAnalysisPrompt(alert, context);
      const response = await this.aiService.query({
        prompt,
        context: {
          domain: 'security',
          operation: 'alert_analysis',
          alertId: alert.id,
          timestamp: new Date().toISOString()
        },
        options: {
          maxTokens: 1200,
          temperature: 0.25,
          responseFormat: 'structured'
        }
      });

      const analysis = this.parseAlertAnalysis(response);
      
      // Validate response time
      const responseTime = Date.now() - startTime;
      if (responseTime > 1000) {
        console.warn(`Alert analysis exceeded 1s: ${responseTime}ms`);
      }

      return analysis;

    } catch (error) {
      console.error('Alert analysis failed:', error);
      return this.getFallbackAlertAnalysis();
    }
  }

  /**
   * Generate hunt queries based on threat context
   */
  async generateHuntQueries(context: {
    threatType?: string;
    indicators?: string[];
    timeframe?: string;
    environment?: string;
  }): Promise<Array<{
    name: string;
    query: string;
    description: string;
    tools: string[];
    confidence: number;
  }>> {
    const startTime = Date.now();
    
    try {
      const prompt = this.buildHuntQueryPrompt(context);
      const response = await this.aiService.query({
        prompt,
        context: {
          domain: 'security',
          operation: 'hunt_generation',
          timestamp: new Date().toISOString()
        },
        options: {
          maxTokens: 1000,
          temperature: 0.4, // Slightly higher for creative query generation
          responseFormat: 'structured'
        }
      });

      const queries = this.parseHuntQueries(response);
      
      // Validate response time
      const responseTime = Date.now() - startTime;
      if (responseTime > 1000) {
        console.warn(`Hunt query generation exceeded 1s: ${responseTime}ms`);
      }

      return queries;

    } catch (error) {
      console.error('Hunt query generation failed:', error);
      return this.getFallbackHuntQueries();
    }
  }

  // Private helper methods

  private buildRecommendationPrompt(context: SecurityContext): string {
    return `
      As a security analyst AI, provide actionable recommendations based on the following context:
      
      Domain: ${context.domain}
      Tool: ${context.tool || 'Unknown'}
      Alert ID: ${context.alertId || 'N/A'}
      Severity: ${context.severity || 'Unknown'}
      Indicators: ${context.indicators?.join(', ') || 'None'}
      Threat Type: ${context.threatType || 'Unknown'}
      
      Previous contexts: ${JSON.stringify(this.contextHistory.slice(-3))}
      
      Provide 3-5 specific, actionable recommendations prioritized by urgency and effectiveness.
      Focus on immediate next steps and tool-specific actions.
      
      Response format: JSON array of recommendations with id, type, title, description, priority (1-5), confidence (0-1), and actions array.
    `;
  }

  private buildThreatIntelPrompt(request: ThreatIntelRequest): string {
    return `
      Analyze the following indicators of compromise for threat intelligence:
      
      Indicators: ${request.indicators.join(', ')}
      Context: ${request.context || 'General threat analysis'}
      Sources: ${request.sources?.join(', ') || 'All available sources'}
      
      Provide detailed threat intelligence analysis including:
      - Individual indicator analysis with confidence scores
      - Overall risk assessment
      - Specific recommendations for response actions
      
      Response format: JSON with matches array, overallRisk, and recommendations array.
    `;
  }

  private buildAlertAnalysisPrompt(alert: any, context: SecurityContext): string {
    return `
      Analyze this security alert and provide detailed insights:
      
      Alert Title: ${alert.title}
      Description: ${alert.description}
      Severity: ${alert.severity}
      Source: ${alert.source}
      Indicators: ${alert.indicators.join(', ')}
      
      Context: ${JSON.stringify(context)}
      
      Provide comprehensive analysis including:
      - Technical analysis of the alert
      - Risk assessment and potential impact
      - Recommended next steps
      - Related threat patterns
      - Confidence level in the analysis
      
      Response format: JSON with analysis, riskAssessment, nextSteps array, relatedThreats array, and confidence (0-1).
    `;
  }

  private buildHuntQueryPrompt(context: any): string {
    return `
      Generate threat hunting queries based on the following context:
      
      Threat Type: ${context.threatType || 'General threats'}
      Indicators: ${context.indicators?.join(', ') || 'None specified'}
      Timeframe: ${context.timeframe || 'Last 30 days'}
      Environment: ${context.environment || 'Enterprise network'}
      
      Generate 3-5 effective hunt queries that can be used across different security tools.
      Focus on queries that are likely to detect the specified threat patterns.
      
      Response format: JSON array with name, query, description, tools array, and confidence (0-1).
    `;
  }

  // Parser methods
  private parseRecommendations(response: any): SecurityRecommendation[] {
    try {
      if (typeof response === 'string') {
        response = JSON.parse(response);
      }
      
      if (Array.isArray(response)) {
        return response.map((rec, index) => ({
          id: rec.id || `rec_${index}`,
          type: rec.type || 'investigation',
          title: rec.title || 'Security Recommendation',
          description: rec.description || 'No description available',
          priority: rec.priority || 3,
          confidence: rec.confidence || 0.5,
          actions: rec.actions || []
        }));
      }
      
      return [];
    } catch (error) {
      console.error('Failed to parse recommendations:', error);
      return [];
    }
  }

  private parseThreatIntelligence(response: any): ThreatIntelResponse {
    try {
      if (typeof response === 'string') {
        response = JSON.parse(response);
      }
      
      return {
        matches: response.matches || [],
        overallRisk: response.overallRisk || 'medium',
        recommendations: response.recommendations || []
      };
    } catch (error) {
      console.error('Failed to parse threat intelligence:', error);
      return { matches: [], overallRisk: 'medium', recommendations: [] };
    }
  }

  private parseAlertAnalysis(response: any): any {
    try {
      if (typeof response === 'string') {
        response = JSON.parse(response);
      }
      
      return {
        analysis: response.analysis || 'Unable to analyze alert',
        riskAssessment: response.riskAssessment || 'Risk assessment unavailable',
        nextSteps: response.nextSteps || [],
        relatedThreats: response.relatedThreats || [],
        confidence: response.confidence || 0.5
      };
    } catch (error) {
      console.error('Failed to parse alert analysis:', error);
      return {
        analysis: 'Analysis failed',
        riskAssessment: 'Unable to assess risk',
        nextSteps: [],
        relatedThreats: [],
        confidence: 0
      };
    }
  }

  private parseHuntQueries(response: any): any[] {
    try {
      if (typeof response === 'string') {
        response = JSON.parse(response);
      }
      
      if (Array.isArray(response)) {
        return response.map((query, index) => ({
          name: query.name || `Hunt Query ${index + 1}`,
          query: query.query || '',
          description: query.description || 'No description available',
          tools: query.tools || [],
          confidence: query.confidence || 0.5
        }));
      }
      
      return [];
    } catch (error) {
      console.error('Failed to parse hunt queries:', error);
      return [];
    }
  }

  // Fallback methods for error cases
  private getFallbackRecommendations(context: SecurityContext): SecurityRecommendation[] {
    return [
      {
        id: 'fallback_1',
        type: 'investigation',
        title: 'Review Alert Details',
        description: 'Manually review the alert details and indicators for initial assessment',
        priority: 3,
        confidence: 0.8,
        actions: [
          { tool: 'manual', action: 'review_alert' }
        ]
      }
    ];
  }

  private getFallbackThreatIntel(request: ThreatIntelRequest): ThreatIntelResponse {
    return {
      matches: [],
      overallRisk: 'medium',
      recommendations: ['Manual threat intelligence lookup recommended']
    };
  }

  private getFallbackAlertAnalysis(): any {
    return {
      analysis: 'Automated analysis unavailable - manual review required',
      riskAssessment: 'Unable to automatically assess risk level',
      nextSteps: ['Manual investigation required'],
      relatedThreats: [],
      confidence: 0.1
    };
  }

  private getFallbackHuntQueries(): any[] {
    return [
      {
        name: 'Basic Process Monitoring',
        query: 'process_name != null AND parent_process != null',
        description: 'Monitor process execution patterns',
        tools: ['elasticsearch', 'splunk'],
        confidence: 0.6
      }
    ];
  }
}