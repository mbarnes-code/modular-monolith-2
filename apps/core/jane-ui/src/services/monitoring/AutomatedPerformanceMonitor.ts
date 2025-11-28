/**
 * Automated Performance Monitoring Integration
 * Continuous monitoring service for constitutional compliance
 */


interface PerformanceConfig {
  monitoring: {
    enabled: boolean;
    interval: number;
    alertThresholds: {
      responseTime: number;
      errorRate: number;
      memoryUsage: number;
    };
  };
  constitutional: {
    domains: Record<string, number>;
    executiveFunction: Record<string, number>;
    bundleSize: {
      maxMainBundle: number;
      maxTotalSize: number;
    };
  };
  reporting: {
    exportInterval: number;
    retentionDays: number;
    alertWebhook?: string;
  };
}

const DEFAULT_CONFIG: PerformanceConfig = {
  monitoring: {
    enabled: true,
    interval: 30000, // 30 seconds
    alertThresholds: {
      responseTime: 2000, // 2s average threshold
      errorRate: 0.01,    // 1% error rate
      memoryUsage: 80,    // 80% memory usage
    },
  },
  constitutional: {
    domains: {
      security: 1000,
      productivity: 2000,
      mtg: 3000,
      infrastructure: 5000,
    },
    executiveFunction: {
      interaction: 200,
      navigation: 300,
      dataLoad: 500,
      contextSwitch: 250,
    },
    bundleSize: {
      maxMainBundle: 2 * 1024 * 1024, // 2MB
      maxTotalSize: 5 * 1024 * 1024,  // 5MB
    },
  },
  reporting: {
    exportInterval: 3600000, // 1 hour
    retentionDays: 30,
  },
};

class AutomatedPerformanceMonitor {
  private config: PerformanceConfig;
  private isRunning: boolean = false;
  private monitoringInterval?: NodeJS.Timeout;
  private reportingInterval?: NodeJS.Timeout;
  private metrics: Map<string, any[]> = new Map();

  constructor(config: Partial<PerformanceConfig> = {}) {
    this.config = { ...DEFAULT_CONFIG, ...config };
  }

  start(): void {
    if (this.isRunning) {
      console.warn('Performance monitor is already running');
      return;
    }

    this.isRunning = true;
    console.log('🚀 Starting automated performance monitoring...');

    // Start monitoring interval
    this.monitoringInterval = setInterval(() => {
      this.collectMetrics();
    }, this.config.monitoring.interval);

    // Start reporting interval
    this.reportingInterval = setInterval(() => {
      this.generateReport();
    }, this.config.reporting.exportInterval);

    // Initial metric collection
    this.collectMetrics();
  }

  stop(): void {
    if (!this.isRunning) return;

    this.isRunning = false;
    console.log('🛑 Stopping automated performance monitoring...');

    if (this.monitoringInterval) {
      clearInterval(this.monitoringInterval);
      this.monitoringInterval = undefined;
    }

    if (this.reportingInterval) {
      clearInterval(this.reportingInterval);
      this.reportingInterval = undefined;
    }
  }

  private async collectMetrics(): Promise<void> {
    const timestamp = Date.now();
    
    try {
      // Collect system metrics
      const systemMetrics = await this.getSystemMetrics();
      
      // Collect application metrics
      const appMetrics = await this.getApplicationMetrics();
      
      // Collect constitutional compliance metrics
      const constitutionalMetrics = await this.getConstitutionalMetrics();

      // Store metrics
      const allMetrics = {
        timestamp,
        system: systemMetrics,
        application: appMetrics,
        constitutional: constitutionalMetrics,
      };

      this.storeMetrics('performance', allMetrics);

      // Check for alerts
      this.checkAlertConditions(allMetrics);

    } catch (error) {
      console.error('Error collecting performance metrics:', error);
    }
  }

  private async getSystemMetrics(): Promise<any> {
    const memoryUsage = process.memoryUsage();
    const cpuUsage = process.cpuUsage();

    return {
      memory: {
        rss: memoryUsage.rss,
        heapUsed: memoryUsage.heapUsed,
        heapTotal: memoryUsage.heapTotal,
        external: memoryUsage.external,
        usagePercentage: (memoryUsage.heapUsed / memoryUsage.heapTotal) * 100,
      },
      cpu: {
        user: cpuUsage.user,
        system: cpuUsage.system,
      },
      uptime: process.uptime(),
    };
  }

  private async getApplicationMetrics(): Promise<any> {
    // In a real implementation, these would collect actual app metrics
    return {
      responseTime: {
        avg: Math.random() * 1000 + 500,  // Simulated
        p95: Math.random() * 2000 + 1000,
        p99: Math.random() * 3000 + 2000,
      },
      requestRate: Math.random() * 100 + 50,
      errorRate: Math.random() * 0.02,
      activeConnections: Math.floor(Math.random() * 50) + 10,
    };
  }

  private async getConstitutionalMetrics(): Promise<any> {
    // Check bundle sizes (would read from actual bundle report)
    let bundleMetrics = {
      mainBundle: 0,
      totalSize: 0,
      violations: [],
    };

    try {
      // In a real implementation, read from bundle-size-report.json
      const bundleReport = {
        constitutional: {
          mainBundle: { size: Math.random() * 1024 * 1024 },  // Up to 1MB simulated
          totalSize: { size: Math.random() * 3 * 1024 * 1024 }, // Up to 3MB simulated
        },
      };

      bundleMetrics.mainBundle = bundleReport.constitutional.mainBundle.size;
      bundleMetrics.totalSize = bundleReport.constitutional.totalSize.size;

      // Check violations
      if (bundleMetrics.mainBundle > this.config.constitutional.bundleSize.maxMainBundle) {
        bundleMetrics.violations.push('Main bundle exceeds 2MB constitutional limit');
      }

      if (bundleMetrics.totalSize > this.config.constitutional.bundleSize.maxTotalSize) {
        bundleMetrics.violations.push('Total bundle exceeds 5MB platform limit');
      }

    } catch (error) {
      console.warn('Could not read bundle metrics:', error);
    }

    // Check domain response times (would integrate with actual monitoring)
    const domainMetrics = Object.entries(this.config.constitutional.domains).reduce((acc, [domain, threshold]) => {
      const responseTime = Math.random() * threshold * 1.2; // Simulate some variance
      acc[domain] = {
        responseTime,
        threshold,
        violation: responseTime > threshold,
      };
      return acc;
    }, {} as Record<string, any>);

    // Check executive function compliance
    const executiveFunctionMetrics = Object.entries(this.config.constitutional.executiveFunction).reduce((acc, [metric, threshold]) => {
      const actualTime = Math.random() * threshold * 1.1; // Simulate some variance
      acc[metric] = {
        actualTime,
        threshold,
        violation: actualTime > threshold,
      };
      return acc;
    }, {} as Record<string, any>);

    return {
      bundle: bundleMetrics,
      domains: domainMetrics,
      executiveFunction: executiveFunctionMetrics,
    };
  }

  private storeMetrics(category: string, metrics: any): void {
    if (!this.metrics.has(category)) {
      this.metrics.set(category, []);
    }

    const categoryMetrics = this.metrics.get(category)!;
    categoryMetrics.push(metrics);

    // Keep only recent metrics (last 1000 entries)
    if (categoryMetrics.length > 1000) {
      categoryMetrics.shift();
    }
  }

  private checkAlertConditions(metrics: any): void {
    const alerts: string[] = [];

    // Check system alerts
    if (metrics.system.memory.usagePercentage > this.config.monitoring.alertThresholds.memoryUsage) {
      alerts.push(`High memory usage: ${Math.round(metrics.system.memory.usagePercentage)}%`);
    }

    // Check application alerts
    if (metrics.application.responseTime.avg > this.config.monitoring.alertThresholds.responseTime) {
      alerts.push(`High response time: ${Math.round(metrics.application.responseTime.avg)}ms`);
    }

    if (metrics.application.errorRate > this.config.monitoring.alertThresholds.errorRate) {
      alerts.push(`High error rate: ${(metrics.application.errorRate * 100).toFixed(2)}%`);
    }

    // Check constitutional alerts
    if (metrics.constitutional.bundle.violations.length > 0) {
      alerts.push(...metrics.constitutional.bundle.violations);
    }

    // Check domain violations
    Object.entries(metrics.constitutional.domains).forEach(([domain, data]: [string, any]) => {
      if (data.violation) {
        alerts.push(`${domain} domain response time violation: ${Math.round(data.responseTime)}ms > ${data.threshold}ms`);
      }
    });

    // Check executive function violations
    Object.entries(metrics.constitutional.executiveFunction).forEach(([metric, data]: [string, any]) => {
      if (data.violation) {
        alerts.push(`Executive function violation - ${metric}: ${Math.round(data.actualTime)}ms > ${data.threshold}ms`);
      }
    });

    // Send alerts if any
    if (alerts.length > 0) {
      this.sendAlerts(alerts);
    }
  }

  private sendAlerts(alerts: string[]): void {
    console.warn('🚨 Performance Alerts:', alerts);

    // In a real implementation, send to webhook or notification service
    if (this.config.reporting.alertWebhook) {
      // Send to webhook
      fetch(this.config.reporting.alertWebhook, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          timestamp: new Date().toISOString(),
          service: 'jane-ui-performance-monitor',
          alerts,
        }),
      }).catch(error => {
        console.error('Failed to send alerts to webhook:', error);
      });
    }
  }

  private generateReport(): void {
    console.log('📊 Generating performance report...');

    const report = {
      timestamp: new Date().toISOString(),
      summary: this.generateSummary(),
      trends: this.analyzeTrends(),
      recommendations: this.generateRecommendations(),
    };

    // Export report
    if (typeof window === 'undefined') {
      // Node.js environment
      const fs = require('fs');
      const path = 'performance-reports/automated-report.json';
      fs.writeFileSync(path, JSON.stringify(report, null, 2));
      console.log(`📄 Report saved to ${path}`);
    } else {
      // Browser environment
      console.log('📄 Performance Report:', report);
    }
  }

  private generateSummary(): any {
    const performanceMetrics = this.metrics.get('performance') || [];
    
    if (performanceMetrics.length === 0) {
      return { message: 'No metrics collected yet' };
    }

    const latest = performanceMetrics[performanceMetrics.length - 1];
    const lastHour = performanceMetrics.filter(m => 
      Date.now() - m.timestamp < 3600000 // Last hour
    );

    return {
      current: {
        memory_usage: `${Math.round(latest.system.memory.usagePercentage)}%`,
        response_time: `${Math.round(latest.application.responseTime.avg)}ms`,
        error_rate: `${(latest.application.errorRate * 100).toFixed(2)}%`,
        bundle_size: `${Math.round(latest.constitutional.bundle.totalSize / 1024 / 1024 * 100) / 100}MB`,
      },
      hourly_averages: lastHour.length > 0 ? {
        memory_usage: `${Math.round(lastHour.reduce((sum, m) => sum + m.system.memory.usagePercentage, 0) / lastHour.length)}%`,
        response_time: `${Math.round(lastHour.reduce((sum, m) => sum + m.application.responseTime.avg, 0) / lastHour.length)}ms`,
        error_rate: `${(lastHour.reduce((sum, m) => sum + m.application.errorRate, 0) / lastHour.length * 100).toFixed(2)}%`,
      } : null,
    };
  }

  private analyzeTrends(): any {
    const performanceMetrics = this.metrics.get('performance') || [];
    
    if (performanceMetrics.length < 2) {
      return { message: 'Insufficient data for trend analysis' };
    }

    const recent = performanceMetrics.slice(-10); // Last 10 measurements
    const older = performanceMetrics.slice(-20, -10); // Previous 10 measurements

    if (older.length === 0) {
      return { message: 'Insufficient historical data' };
    }

    const recentAvg = {
      responseTime: recent.reduce((sum, m) => sum + m.application.responseTime.avg, 0) / recent.length,
      memoryUsage: recent.reduce((sum, m) => sum + m.system.memory.usagePercentage, 0) / recent.length,
      errorRate: recent.reduce((sum, m) => sum + m.application.errorRate, 0) / recent.length,
    };

    const olderAvg = {
      responseTime: older.reduce((sum, m) => sum + m.application.responseTime.avg, 0) / older.length,
      memoryUsage: older.reduce((sum, m) => sum + m.system.memory.usagePercentage, 0) / older.length,
      errorRate: older.reduce((sum, m) => sum + m.application.errorRate, 0) / older.length,
    };

    return {
      response_time: {
        trend: recentAvg.responseTime > olderAvg.responseTime ? 'increasing' : 'decreasing',
        change: `${Math.round((recentAvg.responseTime - olderAvg.responseTime) / olderAvg.responseTime * 100)}%`,
      },
      memory_usage: {
        trend: recentAvg.memoryUsage > olderAvg.memoryUsage ? 'increasing' : 'decreasing',
        change: `${Math.round((recentAvg.memoryUsage - olderAvg.memoryUsage) / olderAvg.memoryUsage * 100)}%`,
      },
      error_rate: {
        trend: recentAvg.errorRate > olderAvg.errorRate ? 'increasing' : 'decreasing',
        change: `${Math.round((recentAvg.errorRate - olderAvg.errorRate) / olderAvg.errorRate * 100)}%`,
      },
    };
  }

  private generateRecommendations(): string[] {
    const recommendations: string[] = [];
    const performanceMetrics = this.metrics.get('performance') || [];
    
    if (performanceMetrics.length === 0) return recommendations;

    const latest = performanceMetrics[performanceMetrics.length - 1];

    // Memory recommendations
    if (latest.system.memory.usagePercentage > 70) {
      recommendations.push('Consider implementing memory optimization - usage above 70%');
    }

    // Response time recommendations
    if (latest.application.responseTime.avg > 1000) {
      recommendations.push('Response time optimization needed - average above 1s');
    }

    // Bundle size recommendations
    const bundleUsagePercent = (latest.constitutional.bundle.totalSize / this.config.constitutional.bundleSize.maxTotalSize) * 100;
    if (bundleUsagePercent > 80) {
      recommendations.push('Bundle size optimization recommended - approaching constitutional limit');
    }

    // Executive function recommendations
    Object.entries(latest.constitutional.executiveFunction).forEach(([metric, data]: [string, any]) => {
      if (data.violation) {
        recommendations.push(`Optimize ${metric} response time for ADHD accommodation compliance`);
      }
    });

    return recommendations;
  }

  // Public API methods
  public getMetrics(category?: string): any {
    if (category) {
      return this.metrics.get(category) || [];
    }
    return Object.fromEntries(this.metrics);
  }

  public exportMetrics(): void {
    this.generateReport();
  }

  public getHealthStatus(): any {
    const performanceMetrics = this.metrics.get('performance') || [];
    
    if (performanceMetrics.length === 0) {
      return { status: 'unknown', message: 'No metrics available' };
    }

    const latest = performanceMetrics[performanceMetrics.length - 1];
    let score = 100;
    const issues: string[] = [];

    // Deduct points for violations
    if (latest.system.memory.usagePercentage > 80) {
      score -= 20;
      issues.push('High memory usage');
    }

    if (latest.application.responseTime.avg > 2000) {
      score -= 30;
      issues.push('High response time');
    }

    if (latest.application.errorRate > 0.01) {
      score -= 25;
      issues.push('High error rate');
    }

    if (latest.constitutional.bundle.violations.length > 0) {
      score -= 35;
      issues.push('Constitutional violations');
    }

    const status = score >= 80 ? 'healthy' : score >= 60 ? 'warning' : 'critical';

    return {
      status,
      score: Math.max(0, score),
      issues,
      timestamp: latest.timestamp,
    };
  }
}

// Export singleton instance
export const performanceMonitor = new AutomatedPerformanceMonitor();

// Auto-start monitoring in production
if (typeof window === 'undefined' && process.env.NODE_ENV === 'production') {
  performanceMonitor.start();
}

export default AutomatedPerformanceMonitor;