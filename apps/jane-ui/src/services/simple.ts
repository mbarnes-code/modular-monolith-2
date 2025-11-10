/**
 * Services for Mental Prosthetic Platform
 * 
 * Provides API client and state management functionality
 */

// Basic types
export interface APIResponse<T = unknown> {
  data: T;
  success: boolean;
  message?: string;
  errors?: string[];
}

export interface AppState {
  user: null | { id: string; username: string; preferences: Record<string, unknown> };
  activeTool: string | null;
  cognitiveLoad: number;
  performanceMetrics: Array<{
    domain: string;
    responseTime: number;
    timestamp: Date;
  }>;
}

export const initialState: AppState = {
  user: null,
  activeTool: null,
  cognitiveLoad: 0,
  performanceMetrics: []
};

// Simple fetch wrapper that works in browser environment
export const fetchAPI = async <T>(url: string, options?: {
  method?: string;
  body?: string;
  headers?: Record<string, string>;
}): Promise<APIResponse<T>> => {
  try {
    // This will work in browser environment
    const response = await (globalThis as any).fetch(url, {
      method: options?.method || 'GET',
      headers: {
        'Content-Type': 'application/json',
        ...options?.headers,
      },
      body: options?.body,
    });

    const data = await response.json();

    if (!response.ok) {
      return {
        data: null as T,
        success: false,
        message: data.message || 'Request failed',
        errors: data.errors || [data.message || 'Unknown error']
      };
    }

    return {
      data,
      success: true
    };
  } catch (error) {
    return {
      data: null as T,
      success: false,
      message: error instanceof Error ? error.message : 'Network error',
      errors: [error instanceof Error ? error.message : 'Network error']
    };
  }
};

// Executive function utilities
export const trackPerformance = (domain: string, startTime: number) => {
  const responseTime = Date.now() - startTime;
  const thresholds = {
    security: 1000,
    productivity: 2000,
    mtg: 3000,
    infrastructure: 5000
  };

  const threshold = (thresholds as any)[domain] || 2000;
  const isSlowResponse = responseTime > threshold;

  return {
    domain,
    responseTime,
    timestamp: new Date(),
    isSlowResponse,
    threshold
  };
};

export const calculateCognitiveLoad = (metrics: Array<{ responseTime: number; domain: string }>) => {
  if (metrics.length === 0) return 0;

  const averageResponseTime = metrics.reduce((sum, m) => sum + m.responseTime, 0) / metrics.length;
  const slowResponses = metrics.filter(m => {
    const thresholds = { security: 1000, productivity: 2000, mtg: 3000, infrastructure: 5000 };
    return m.responseTime > ((thresholds as any)[m.domain] || 2000);
  }).length;

  // Calculate load based on performance and slow responses
  const baseLoad = Math.min((averageResponseTime / 1000) * 10, 50); // Max 50 from response time
  const penaltyLoad = (slowResponses / metrics.length) * 50; // Max 50 from slow responses

  return Math.min(Math.round(baseLoad + penaltyLoad), 100);
};