/**
 * MISP Service Adapter
 * TypeScript adapter for MISP (Malware Information Sharing Platform) integration
 * 
 * This adapter provides a unified interface for MISP functionality
 * within the executive function dashboard.
 */

import { BaseServiceAdapter } from '../base/base-adapter';
import {
    HealthStatus,
    ServiceAdapterConfig,
    ServiceAdapterResponse
} from '../base/types';

// MISP-specific types
export interface MISPEvent {
  id: string;
  info: string;
  threat_level_id: number;
  analysis: number;
  distribution: number;
  published: boolean;
  timestamp: string;
  attributes?: MISPAttribute[];
  tags?: MISPTag[];
}

export interface MISPAttribute {
  id: string;
  event_id: string;
  category: string;
  type: string;
  value: string;
  to_ids: boolean;
  distribution: number;
  timestamp: string;
  comment?: string;
  tags?: MISPTag[];
}

export interface MISPTag {
  id: string;
  name: string;
  colour: string;
  exportable: boolean;
}

export interface MISPOrganization {
  id: string;
  name: string;
  description: string;
  type: string;
  nationality: string;
  sector: string;
}

export interface MISPSearchParams {
  query?: string;
  category?: string;
  type?: string;
  tags?: string[];
  from_date?: string;
  to_date?: string;
  published?: boolean;
  limit?: number;
  page?: number;
}

export interface MISPImportOptions {
  format: 'misp_json' | 'stix' | 'csv' | 'ioc';
  distribution?: number;
  threat_level?: number;
  analysis?: number;
  tags?: string[];
}

export interface MISPExportOptions {
  format: 'misp_json' | 'stix' | 'csv' | 'pdf';
  event_ids?: string[];
  include_attributes?: boolean;
  include_correlations?: boolean;
  date_from?: string;
  date_to?: string;
}

/**
 * MISP Service Adapter Class
 */
export class MISPAdapter extends BaseServiceAdapter {
  private baseUrl: string;
  private apiKey: string;
  private initialized: boolean = false;

  constructor(config: ServiceAdapterConfig) {
    super(config);
    this.baseUrl = config.endpoint || 'http://localhost:8000/api/misp';
    this.apiKey = config.apiKey || '';
  }

  /**
   * Initialize the MISP adapter
   */
  async initialize(): Promise<boolean> {
    try {
      const healthCheck = await this.checkHealth();
      this.initialized = healthCheck.status === 'healthy';
      return this.initialized;
    } catch (error) {
      console.error('Failed to initialize MISP adapter:', error);
      return false;
    }
  }

  /**
   * Check service health
   */
  async checkHealth(): Promise<HealthStatus> {
    try {
      const response = await this.makeRequest('/health', 'GET');
      return {
        status: response.data.status === 'healthy' ? 'healthy' : 'unhealthy',
        message: response.data.message || 'MISP service status',
        timestamp: new Date().toISOString(),
        details: response.data
      };
    } catch (error) {
      return {
        status: 'unhealthy',
        message: `MISP service error: ${error}`,
        timestamp: new Date().toISOString()
      };
    }
  }

  // Event Management Methods

  /**
   * Create a new MISP event
   */
  async createEvent(eventData: Partial<MISPEvent>): Promise<ServiceAdapterResponse<MISPEvent>> {
    return this.makeRequest('/events', 'POST', eventData);
  }

  /**
   * Get MISP event by ID
   */
  async getEvent(eventId: string): Promise<ServiceAdapterResponse<MISPEvent>> {
    return this.makeRequest(`/events/${eventId}`, 'GET');
  }

  /**
   * Update MISP event
   */
  async updateEvent(eventId: string, eventData: Partial<MISPEvent>): Promise<ServiceAdapterResponse<MISPEvent>> {
    return this.makeRequest(`/events/${eventId}`, 'PUT', eventData);
  }

  /**
   * Delete MISP event
   */  
  async deleteEvent(eventId: string): Promise<ServiceAdapterResponse<void>> {
    return this.makeRequest(`/events/${eventId}`, 'DELETE');
  }

  /**
   * List MISP events with optional filters
   */
  async listEvents(filters?: MISPSearchParams): Promise<ServiceAdapterResponse<MISPEvent[]>> {
    const queryParams = filters ? new URLSearchParams(filters as any).toString() : '';
    const url = `/events${queryParams ? `?${queryParams}` : ''}`;
    return this.makeRequest(url, 'GET');
  }

  // Attribute Management Methods

  /**
   * Create a new MISP attribute
   */
  async createAttribute(attributeData: Partial<MISPAttribute>): Promise<ServiceAdapterResponse<MISPAttribute>> {
    return this.makeRequest('/attributes', 'POST', attributeData);
  }

  /**
   * Get MISP attribute by ID
   */
  async getAttribute(attributeId: string): Promise<ServiceAdapterResponse<MISPAttribute>> {
    return this.makeRequest(`/attributes/${attributeId}`, 'GET');
  }

  /**
   * Search MISP attributes
   */
  async searchAttributes(searchParams: MISPSearchParams): Promise<ServiceAdapterResponse<MISPAttribute[]>> {
    return this.makeRequest('/attributes/search', 'POST', searchParams);
  }

  /**
   * Get attribute correlations
   */
  async getAttributeCorrelations(attributeId: string): Promise<ServiceAdapterResponse<MISPAttribute[]>> {
    return this.makeRequest(`/attributes/${attributeId}/correlations`, 'GET');
  }

  // Organization Management Methods

  /**
   * Get all organizations
   */
  async getOrganizations(): Promise<ServiceAdapterResponse<MISPOrganization[]>> {
    return this.makeRequest('/organizations', 'GET');
  }

  /**
   * Get organization by ID
   */
  async getOrganization(orgId: string): Promise<ServiceAdapterResponse<MISPOrganization>> {
    return this.makeRequest(`/organizations/${orgId}`, 'GET');
  }

  // Search and Analysis Methods

  /**
   * Universal search across MISP data
   */
  async search(query: string, searchType: string = 'all'): Promise<ServiceAdapterResponse<any>> {
    return this.makeRequest('/search', 'POST', { query, search_type: searchType });
  }

  /**
   * Get correlation statistics
   */
  async getCorrelationStats(): Promise<ServiceAdapterResponse<any>> {
    return this.makeRequest('/correlations/stats', 'GET');
  }

  // Import/Export Methods

  /**
   * Import data into MISP  
   */
  async importData(data: any, options: MISPImportOptions): Promise<ServiceAdapterResponse<any>> {
    return this.makeRequest('/import', 'POST', { data, options });
  }

  /**
   * Export MISP data
   */
  async exportData(options: MISPExportOptions): Promise<ServiceAdapterResponse<any>> {
    return this.makeRequest('/export', 'POST', options);
  }

  // Feed Management Methods

  /**
   * Process external threat intelligence feed
   */
  async processFeed(feedData: any): Promise<ServiceAdapterResponse<any>> {
    return this.makeRequest('/feeds/process', 'POST', feedData);
  }

  /**
   * Get available feeds
   */
  async getFeeds(): Promise<ServiceAdapterResponse<any[]>> {
    return this.makeRequest('/feeds', 'GET');
  }

  // Taxonomy and Tag Methods

  /**
   * Get available taxonomies
   */
  async getTaxonomies(): Promise<ServiceAdapterResponse<any[]>> {
    return this.makeRequest('/taxonomies', 'GET');
  }

  /**
   * Get tags
   */
  async getTags(): Promise<ServiceAdapterResponse<MISPTag[]>> {
    return this.makeRequest('/tags', 'GET');
  }

  // Utility Methods

  /**
   * Get MISP statistics
   */
  async getStatistics(): Promise<ServiceAdapterResponse<any>> {
    return this.makeRequest('/statistics', 'GET');
  }

  /**
   * Get service status with detailed information
   */
  async getStatus(): Promise<ServiceAdapterResponse<any>> {
    return this.makeRequest('/status', 'GET');
  }

  // Protected helper methods

  /**
   * Make HTTP request to MISP API
   */
  protected async makeRequest(
    endpoint: string, 
    method: string, 
    data?: any
  ): Promise<ServiceAdapterResponse<any>> {
    try {
      const url = `${this.baseUrl}${endpoint}`;
      const headers = {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${this.apiKey}`,
        'Accept': 'application/json'
      };

      const options: RequestInit = {
        method,
        headers,
        ...(data && { body: JSON.stringify(data) })
      };

      const response = await fetch(url, options);
      const responseData = await response.json();

      return {
        success: response.ok,
        data: responseData,
        error: response.ok ? undefined : responseData.error || 'Unknown error',
        status: response.status,
        timestamp: new Date().toISOString()
      };

    } catch (error) {
      return {
        success: false,
        data: null,
        error: `Network error: ${error}`,
        status: 0,
        timestamp: new Date().toISOString()
      };
    }
  }

  /**
   * Get adapter configuration
   */
  getAdapterInfo() {
    return {
      name: 'MISP',
      version: '1.0.0',
      description: 'Malware Information Sharing Platform adapter',
      capabilities: [
        'event_management',
        'attribute_management', 
        'correlation_analysis',
        'organization_management',
        'import_export',
        'feed_processing',
        'taxonomy_support'
      ],
      initialized: this.initialized,
      endpoint: this.baseUrl
    };
  }
}

// Factory function for creating MISP adapter instances
export function createMISPAdapter(config: ServiceAdapterConfig): MISPAdapter {
  return new MISPAdapter(config);
}

// Default export
export default MISPAdapter;