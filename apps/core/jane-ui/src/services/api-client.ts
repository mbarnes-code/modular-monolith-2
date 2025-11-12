/**
 * API Client for Mental Prosthetic Platform
 * 
 * Unified HTTP client for all 37 tools with executive function support
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
}

class APIClient {
  private client: AxiosInstance;
  private readonly baseURL: string;
  private performanceMetrics: Map<string, number[]> = new Map();

  constructor(baseURL = '/api') {
    this.baseURL = baseURL;
    this.client = axios.create({
      baseURL,
      timeout: 30000,
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
        // Add auth header if available and not in browser environment
        if (typeof window !== 'undefined') {
          const token = localStorage.getItem('auth_token');
          if (token && !config.skipAuth) {
            config.headers = config.headers || {};
            config.headers.Authorization = `Bearer ${token}`;
          }
        }

        // Add performance tracking
        (config as RequestConfig & { startTime?: number }).startTime = Date.now();

        // Add executive function headers
        config.headers = config.headers || {};
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
        this.trackPerformance(response);
        return response;
      },
      async (error) => {
        if (error.response?.status === 401) {
          await this.handleAuthError();
        }

        if (error.config?.domain) {
          this.checkDomainPerformance(error.config.domain, error);
        }

        return Promise.reject(this.formatError(error));
      }
    );
  }

  private async handleAuthError(): Promise<void> {
    if (typeof window !== 'undefined') {
      localStorage.removeItem('auth_token');
      window.dispatchEvent(new CustomEvent('auth:expired'));
    }
  }

  private trackPerformance(response: AxiosResponse): void {
    const config = response.config as RequestConfig & { startTime?: number };
    const startTime = config.startTime;

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

      this.checkDomainPerformanceThreshold(config.domain, responseTime);
    }
  }

  private checkDomainPerformanceThreshold(domain: string | undefined, responseTime: number): void {
    const thresholds = {
      security: 1000,     // <1s
      productivity: 2000, // <2s
      mtg: 3000,         // <3s
      infrastructure: 5000 // <5s
    };

    const threshold = thresholds[domain as keyof typeof thresholds] || 2000;

    if (responseTime > threshold && typeof console !== 'undefined') {
      console.warn(`[Performance] ${domain} response time ${responseTime}ms exceeds threshold ${threshold}ms`);

      if (typeof window !== 'undefined') {
        window.dispatchEvent(new CustomEvent('performance:warning', {
          detail: { domain, responseTime, threshold }
        }));
      }
    }
  }

  private checkDomainPerformance(domain: string, error: unknown): void {
    if (typeof console !== 'undefined') {
      console.error(`[API Error] ${domain} domain error:`, error);
    }
  }

  private formatError(error: unknown): APIResponse {
    const axiosError = error as { response?: { data?: { message?: string; errors?: string[] } }; message?: string; config?: RequestConfig & { startTime?: number } };
    const response = axiosError.response;

    return {
      data: null,
      success: false,
      message: response?.data?.message || axiosError.message || 'An error occurred',
      errors: response?.data?.errors || [axiosError.message || 'Unknown error'],
      meta: {
        performance: {
          response_time_ms: axiosError.config?.startTime
            ? Date.now() - axiosError.config.startTime
            : 0,
          domain: axiosError.config?.domain || 'unknown',
          tool_name: axiosError.config?.toolName || 'unknown'
        }
      }
    };
  }

  // Generic request method
  async request<T = unknown>(config: RequestConfig): Promise<APIResponse<T>> {
    const response = await this.client.request(config);

    return {
      data: response.data,
      success: true,
      meta: {
        performance: {
          response_time_ms: (config as RequestConfig & { startTime?: number }).startTime
            ? Date.now() - (config as RequestConfig & { startTime?: number }).startTime!
            : 0,
          domain: config.domain || 'unknown',
          tool_name: config.toolName || 'unknown'
        }
      }
    };
  }

  // HTTP method shortcuts
  async get<T = unknown>(url: string, config?: RequestConfig): Promise<APIResponse<T>> {
    return this.request<T>({ ...config, method: 'GET', url });
  }

  async post<T = unknown>(url: string, data?: unknown, config?: RequestConfig): Promise<APIResponse<T>> {
    return this.request<T>({ ...config, method: 'POST', url, data });
  }

  async put<T = unknown>(url: string, data?: unknown, config?: RequestConfig): Promise<APIResponse<T>> {
    return this.request<T>({ ...config, method: 'PUT', url, data });
  }

  async patch<T = unknown>(url: string, data?: unknown, config?: RequestConfig): Promise<APIResponse<T>> {
    return this.request<T>({ ...config, method: 'PATCH', url, data });
  }

  async delete<T = unknown>(url: string, config?: RequestConfig): Promise<APIResponse<T>> {
    return this.request<T>({ ...config, method: 'DELETE', url });
  }

  // Domain-specific convenience methods
  async security<T = unknown>(url: string, config?: RequestConfig): Promise<APIResponse<T>> {
    return this.get<T>(url, { ...config, domain: 'security', timeout: 1000 });
  }

  async productivity<T = unknown>(url: string, config?: RequestConfig): Promise<APIResponse<T>> {
    return this.get<T>(url, { ...config, domain: 'productivity', timeout: 2000 });
  }

  async mtg<T = unknown>(url: string, config?: RequestConfig): Promise<APIResponse<T>> {
    return this.get<T>(url, { ...config, domain: 'mtg', timeout: 3000 });
  }

  async infrastructure<T = unknown>(url: string, config?: RequestConfig): Promise<APIResponse<T>> {
    return this.get<T>(url, { ...config, domain: 'infrastructure', timeout: 5000 });
  }

  // Performance metrics
  getPerformanceMetrics(): Record<string, { avg: number; max: number; min: number; count: number }> {
    const results: Record<string, { avg: number; max: number; min: number; count: number }> = {};

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
    if (typeof window !== 'undefined') {
      localStorage.setItem('auth_token', token);
    }
  }

  clearAuthToken(): void {
    if (typeof window !== 'undefined') {
      localStorage.removeItem('auth_token');
    }
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
