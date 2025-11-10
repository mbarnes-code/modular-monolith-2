/**
 * Security Performance Monitor
 * 
 * Monitors security domain response times and ensures constitutional compliance
 * with the <1s requirement for security operations.
 */

interface PerformanceMetric {
  operation: string;
  responseTime: number;
  timestamp: string;
  success: boolean;
  tool?: string;
  userId?: string;
}

interface PerformanceThresholds {
  security: number; // <1s for security domain
  ui: number; // <200ms for UI responses
  aiRecommendations: number; // <1s for AI recommendations
  threatIntel: number; // <1s for threat intelligence
}

interface PerformanceAlert {
  id: string;
  type: 'threshold_exceeded' | 'consecutive_failures' | 'system_degradation';
  severity: 'warning' | 'critical';
  message: string;
  metric: PerformanceMetric;
  timestamp: string;
}

export class SecurityPerformanceMonitor {
  private metrics: PerformanceMetric[] = [];
  private alerts: PerformanceAlert[] = [];
  private thresholds: PerformanceThresholds = {
    security: 1000, // 1 second
    ui: 200, // 200ms
    aiRecommendations: 1000, // 1 second
    threatIntel: 1000 // 1 second
  };
  
  private alertCallback?: (alert: PerformanceAlert) => void;
  private metricsCallback?: (metrics: PerformanceMetric[]) => void;

  constructor() {
    // Keep metrics for last hour only to prevent memory bloat
    setInterval(() => {
      this.cleanupOldMetrics();
    }, 5 * 60 * 1000); // Every 5 minutes
  }

  /**
   * Record a performance metric
   */
  recordMetric(operation: string, responseTime: number, options: {
    success?: boolean;
    tool?: string;
    userId?: string;
  } = {}): void {
    const metric: PerformanceMetric = {
      operation,
      responseTime,
      timestamp: new Date().toISOString(),
      success: options.success ?? true,
      tool: options.tool,
      userId: options.userId
    };

    this.metrics.push(metric);
    
    // Check for threshold violations
    this.checkThresholds(metric);
    
    // Trigger metrics callback
    if (this.metricsCallback) {
      this.metricsCallback([...this.metrics]);
    }
  }

  /**
   * Start timing an operation
   */
  startTiming(operation: string): () => void {
    const startTime = performance.now();
    
    return (options: { success?: boolean; tool?: string; userId?: string } = {}) => {
      const endTime = performance.now();
      const responseTime = endTime - startTime;
      
      this.recordMetric(operation, responseTime, options);
    };
  }

  /**
   * Decorator for timing async functions
   */
  timeAsync<T extends (...args: any[]) => Promise<any>>(
    operation: string,
    fn: T,
    options: { tool?: string; userId?: string } = {}
  ): T {
    return (async (...args: Parameters<T>) => {
      const endTiming = this.startTiming(operation);
      
      try {
        const result = await fn(...args);
        endTiming({ success: true, ...options });
        return result;
      } catch (error) {
        endTiming({ success: false, ...options });
        throw error;
      }
    }) as T;
  }

  /**
   * Get performance statistics
   */
  getStats(operation?: string, timeRange?: { start: Date; end: Date }): {
    count: number;
    averageResponseTime: number;
    maxResponseTime: number;
    minResponseTime: number;
    successRate: number;
    thresholdViolations: number;
  } {
    let filteredMetrics = this.metrics;

    if (operation) {
      filteredMetrics = filteredMetrics.filter(m => m.operation === operation);
    }

    if (timeRange) {
      filteredMetrics = filteredMetrics.filter(m => {
        const timestamp = new Date(m.timestamp);
        return timestamp >= timeRange.start && timestamp <= timeRange.end;
      });
    }

    if (filteredMetrics.length === 0) {
      return {
        count: 0,
        averageResponseTime: 0,
        maxResponseTime: 0,
        minResponseTime: 0,
        successRate: 0,
        thresholdViolations: 0
      };
    }

    const responseTimes = filteredMetrics.map(m => m.responseTime);
    const successfulMetrics = filteredMetrics.filter(m => m.success);
    const thresholdViolations = filteredMetrics.filter(m => 
      this.isThresholdViolation(m.operation, m.responseTime)
    );

    return {
      count: filteredMetrics.length,
      averageResponseTime: responseTimes.reduce((a, b) => a + b, 0) / responseTimes.length,
      maxResponseTime: Math.max(...responseTimes),
      minResponseTime: Math.min(...responseTimes),
      successRate: (successfulMetrics.length / filteredMetrics.length) * 100,
      thresholdViolations: thresholdViolations.length
    };
  }

  /**
   * Get recent alerts
   */
  getAlerts(limit: number = 10): PerformanceAlert[] {
    return this.alerts
      .sort((a, b) => new Date(b.timestamp).getTime() - new Date(a.timestamp).getTime())
      .slice(0, limit);
  }

  /**
   * Check constitutional compliance
   */
  getComplianceStatus(): {
    isCompliant: boolean;
    violations: Array<{
      operation: string;
      threshold: number;
      actualTime: number;
      violationCount: number;
    }>;
    overallScore: number;
  } {
    const recentMetrics = this.getRecentMetrics(15); // Last 15 minutes
    const operationGroups = this.groupMetricsByOperation(recentMetrics);
    
    const violations: Array<{
      operation: string;
      threshold: number;
      actualTime: number;
      violationCount: number;
    }> = [];

    let totalScore = 0;
    let operationCount = 0;

    for (const [operation, metrics] of Object.entries(operationGroups)) {
      const threshold = this.getThresholdForOperation(operation);
      const violatingMetrics = metrics.filter(m => m.responseTime > threshold);
      const avgResponseTime = metrics.reduce((sum, m) => sum + m.responseTime, 0) / metrics.length;
      
      if (violatingMetrics.length > 0) {
        violations.push({
          operation,
          threshold,
          actualTime: avgResponseTime,
          violationCount: violatingMetrics.length
        });
      }

      // Score based on compliance (0-100)
      const complianceRate = 1 - (violatingMetrics.length / metrics.length);
      totalScore += complianceRate * 100;
      operationCount++;
    }

    const overallScore = operationCount > 0 ? totalScore / operationCount : 100;
    const isCompliant = violations.length === 0;

    return {
      isCompliant,
      violations,
      overallScore
    };
  }

  /**
   * Set callback for performance alerts
   */
  onAlert(callback: (alert: PerformanceAlert) => void): void {
    this.alertCallback = callback;
  }

  /**
   * Set callback for metrics updates
   */
  onMetricsUpdate(callback: (metrics: PerformanceMetric[]) => void): void {
    this.metricsCallback = callback;
  }

  // Private methods

  private checkThresholds(metric: PerformanceMetric): void {
    const threshold = this.getThresholdForOperation(metric.operation);
    
    if (metric.responseTime > threshold) {
      const alert: PerformanceAlert = {
        id: `alert_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
        type: 'threshold_exceeded',
        severity: metric.responseTime > threshold * 2 ? 'critical' : 'warning',
        message: `${metric.operation} exceeded threshold: ${metric.responseTime}ms > ${threshold}ms`,
        metric,
        timestamp: new Date().toISOString()
      };
      
      this.alerts.push(alert);
      
      if (this.alertCallback) {
        this.alertCallback(alert);
      }
    }
  }

  private isThresholdViolation(operation: string, responseTime: number): boolean {
    const threshold = this.getThresholdForOperation(operation);
    return responseTime > threshold;
  }

  private getThresholdForOperation(operation: string): number {
    // Map operations to thresholds
    if (operation.includes('security') || operation.includes('threat') || operation.includes('alert')) {
      return this.thresholds.security;
    }
    
    if (operation.includes('ui') || operation.includes('click') || operation.includes('navigation')) {
      return this.thresholds.ui;
    }
    
    if (operation.includes('ai') || operation.includes('recommendation')) {
      return this.thresholds.aiRecommendations;
    }
    
    if (operation.includes('intel') || operation.includes('correlation')) {
      return this.thresholds.threatIntel;
    }
    
    // Default to security threshold (most strict)
    return this.thresholds.security;
  }

  private cleanupOldMetrics(): void {
    const oneHourAgo = new Date(Date.now() - 60 * 60 * 1000);
    this.metrics = this.metrics.filter(m => new Date(m.timestamp) >= oneHourAgo);
    
    // Also cleanup old alerts (keep last 24 hours)
    const twentyFourHoursAgo = new Date(Date.now() - 24 * 60 * 60 * 1000);
    this.alerts = this.alerts.filter(a => new Date(a.timestamp) >= twentyFourHoursAgo);
  }

  private getRecentMetrics(minutes: number): PerformanceMetric[] {
    const cutoff = new Date(Date.now() - minutes * 60 * 1000);
    return this.metrics.filter(m => new Date(m.timestamp) >= cutoff);
  }

  private groupMetricsByOperation(metrics: PerformanceMetric[]): Record<string, PerformanceMetric[]> {
    return metrics.reduce((groups, metric) => {
      if (!groups[metric.operation]) {
        groups[metric.operation] = [];
      }
      groups[metric.operation].push(metric);
      return groups;
    }, {} as Record<string, PerformanceMetric[]>);
  }
}

// Global singleton instance
export const securityPerformanceMonitor = new SecurityPerformanceMonitor();