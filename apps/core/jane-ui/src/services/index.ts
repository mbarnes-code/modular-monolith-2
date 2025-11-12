/**
 * Services Index
 * 
 * Exports all service modules for the Mental Prosthetic Platform
 */

// API Client (simplified version without complex dependencies)
export interface APIResponse<T = unknown> {
  data: T;
  success: boolean;
  message?: string;
  errors?: string[];
}

// Simple API client for executive function support
class SimpleAPIClient {
  private baseURL: string;

  constructor(baseURL = '/api') {
    this.baseURL = baseURL;
  }

  private async request<T>(url: string, options?: RequestInit): Promise<APIResponse<T>> {
    try {
      const response = await fetch(`${this.baseURL}${url}`, {
        headers: {
          'Content-Type': 'application/json',
          ...options?.headers,
        },
        ...options,
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
  }

  async get<T>(url: string): Promise<APIResponse<T>> {
    return this.request<T>(url, { method: 'GET' });
  }

  async post<T>(url: string, data: unknown): Promise<APIResponse<T>> {
    return this.request<T>(url, {
      method: 'POST',
      body: JSON.stringify(data)
    });
  }

  async put<T>(url: string, data: unknown): Promise<APIResponse<T>> {
    return this.request<T>(url, {
      method: 'PUT',
      body: JSON.stringify(data)
    });
  }

  async delete<T>(url: string): Promise<APIResponse<T>> {
    return this.request<T>(url, { method: 'DELETE' });
  }
}

// Create API client instance
export const apiClient = new SimpleAPIClient();

// State management using React Context (to be expanded)
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

// Export types and utilities
export { SimpleAPIClient };
export type { APIResponse };
