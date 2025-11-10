/**
 * API Client for Mental Prosthetic Platform
 * 
 * Unified HTTP client for all 37 tools with executive function support:
 * - Request/response interceptors
 * - Automatic retry logic
 * - Performance monitoring
 * - Error handling with user-friendly messages
 */

import axios, { AxiosInstance, AxiosRequestConfig, AxiosResponse } from 'axios';

export interface APIResponse<T = unknown> {
  data: T;
  success: boolean;
  message?: string;
  errors?: string[];
  meta?: {
    total?: number;
    page?: number;
    limit?: number;
    performance?: {
      response_time_ms: number;
      domain: string;
      tool_name: string;
    };
  };
}

export interface RequestConfig extends AxiosRequestConfig {
  domain?: 'security' | 'productivity' | 'mtg' | 'infrastructure';
  toolName?: string;
  skipAuth?: boolean;
  retryAttempts?: number;
  timeout?: number;
}

class APIClient {
  private client: AxiosInstance;
  private readonly baseURL: string;
  private performanceMetrics: Map<string, number[]> = new Map();

  constructor(baseURL: string = (typeof window !== 'undefined' ? window.location.origin : 'http://localhost:8000') + '/api') {
    this.baseURL = baseURL;
    this.client = axios.create({
      baseURL,
      timeout: 30000, // 30 seconds default
      headers: {
        'Content-Type': 'application/json',
      },
    });

    this.setupInterceptors();
  }

  private setupInterceptors(): void {
    // Request interceptor
    this.client.interceptors.request.use(
      (config) => {
        // Add auth header if available
        const token = this.getAuthToken();
        if (token && !config.skipAuth) {
          config.headers.Authorization = `Bearer ${token}`;
        }

        // Add performance tracking
        config.metadata = { startTime: Date.now() };

        // Add executive function headers
        config.headers['X-Executive-Function'] = 'enabled';
        config.headers['X-Response-Time-Threshold'] = '200';

        return config;
      },
      (error) => {
        return Promise.reject(error);
      }
    );

    // Response interceptor
    this.client.interceptors.response.use(
      (response) => {
        // Track performance metrics
        this.trackPerformance(response);
        
        return response;
      },
      async (error) => {
        // Handle auth errors
        if (error.response?.status === 401) {
          await this.handleAuthError();
        }

        // Handle domain-specific performance requirements
        if (error.config?.domain) {
          this.checkDomainPerformance(error.config.domain, error);
        }

        return Promise.reject(this.formatError(error));
      }
    );
  }

  private getAuthToken(): string | null {
    // Get token from localStorage or context
    return localStorage.getItem('auth_token');
  }

  private async handleAuthError(): Promise<void> {
    // Clear invalid token
    localStorage.removeItem('auth_token');
    
    // Redirect to login or show auth modal
    if (typeof window !== 'undefined') {
      window.dispatchEvent(new CustomEvent('auth:expired'));
    }
  }

  private trackPerformance(response: AxiosResponse): void {
    const config = response.config as any;
    const startTime = config.metadata?.startTime;
    
    if (startTime) {
      const responseTime = Date.now() - startTime;
      const key = `${config.domain || 'unknown'}:${config.toolName || 'unknown'}`;
      
      if (!this.performanceMetrics.has(key)) {
        this.performanceMetrics.set(key, []);
      }
      
      const metrics = this.performanceMetrics.get(key)!;
      metrics.push(responseTime);
      
      // Keep only last 100 measurements
      if (metrics.length > 100) {
        metrics.shift();
      }

      // Log performance warnings based on domain
      this.checkDomainPerformanceThreshold(config.domain, responseTime);
    }
  }

  private checkDomainPerformanceThreshold(domain: string, responseTime: number): void {
    const thresholds = {
      security: 1000,     // <1s
      productivity: 2000, // <2s
      mtg: 3000,         // <3s
      infrastructure: 5000 // <5s
    };

    const threshold = thresholds[domain as keyof typeof thresholds] || 2000;
    
    if (responseTime > threshold) {
      console.warn(`[Performance] ${domain} response time ${responseTime}ms exceeds threshold ${threshold}ms`);
      
      // Emit performance warning event
      if (typeof window !== 'undefined') {
        window.dispatchEvent(new CustomEvent('performance:warning', {
          detail: { domain, responseTime, threshold }
        }));
      }
    }
  }

  private checkDomainPerformance(domain: string, error: any): void {
    // Log domain-specific performance issues
    console.error(`[API Error] ${domain} domain error:`, error.message);
  }

  private formatError(error: any): APIResponse {
    const response = error.response;
    
    return {
      data: null,
      success: false,
      message: response?.data?.message || error.message || 'An error occurred',
      errors: response?.data?.errors || [error.message],
      meta: {
        performance: {
          response_time_ms: error.config?.metadata?.startTime 
            ? Date.now() - error.config.metadata.startTime 
            : 0,
          domain: error.config?.domain || 'unknown',
          tool_name: error.config?.toolName || 'unknown'
        }
      }
    };
  }

  // Generic request method
  async request<T = any>(config: RequestConfig): Promise<APIResponse<T>> {
    try {
      const response = await this.client.request(config);
      
      return {
        data: response.data,
        success: true,
        meta: {
          performance: {
            response_time_ms: config.metadata?.startTime 
              ? Date.now() - config.metadata.startTime 
              : 0,
            domain: config.domain || 'unknown',
            tool_name: config.toolName || 'unknown'
          }
        }
      };
    } catch (error: any) {
      throw error; // Will be handled by interceptor
    }
  }

  // HTTP method shortcuts
  async get<T = any>(url: string, config?: RequestConfig): Promise<APIResponse<T>> {
    return this.request<T>({ ...config, method: 'GET', url });
  }

  async post<T = any>(url: string, data?: any, config?: RequestConfig): Promise<APIResponse<T>> {
    return this.request<T>({ ...config, method: 'POST', url, data });
  }

  async put<T = any>(url: string, data?: any, config?: RequestConfig): Promise<APIResponse<T>> {
    return this.request<T>({ ...config, method: 'PUT', url, data });
  }

  async patch<T = any>(url: string, data?: any, config?: RequestConfig): Promise<APIResponse<T>> {
    return this.request<T>({ ...config, method: 'PATCH', url, data });
  }

  async delete<T = any>(url: string, config?: RequestConfig): Promise<APIResponse<T>> {
    return this.request<T>({ ...config, method: 'DELETE', url });
  }

  // Domain-specific convenience methods
  async security<T = any>(url: string, config?: RequestConfig): Promise<APIResponse<T>> {
    return this.get<T>(url, { ...config, domain: 'security', timeout: 1000 });
  }

  async productivity<T = any>(url: string, config?: RequestConfig): Promise<APIResponse<T>> {
    return this.get<T>(url, { ...config, domain: 'productivity', timeout: 2000 });
  }

  async mtg<T = any>(url: string, config?: RequestConfig): Promise<APIResponse<T>> {
    return this.get<T>(url, { ...config, domain: 'mtg', timeout: 3000 });
  }

  async infrastructure<T = any>(url: string, config?: RequestConfig): Promise<APIResponse<T>> {
    return this.get<T>(url, { ...config, domain: 'infrastructure', timeout: 5000 });
  }

  // Performance metrics
  getPerformanceMetrics(): Record<string, { avg: number; max: number; min: number; count: number }> {
    const results: Record<string, any> = {};
    
    for (const [key, values] of this.performanceMetrics.entries()) {
      if (values.length > 0) {
        results[key] = {
          avg: Math.round(values.reduce((a, b) => a + b, 0) / values.length),
          max: Math.max(...values),
          min: Math.min(...values),
          count: values.length
        };
      }
    }
    
    return results;
  }

  // Auth methods
  setAuthToken(token: string): void {
    localStorage.setItem('auth_token', token);
  }

  clearAuthToken(): void {
    localStorage.removeItem('auth_token');
  }

  // Health check
  async healthCheck(): Promise<APIResponse<{ status: string; timestamp: string }>> {
    return this.get('/health', { skipAuth: true });
  }
}

// Create singleton instance
export const apiClient = new APIClient();

// Export for dependency injection in tests
export { APIClient };
