/**
 * Offline Data Cache Service
 * 
 * Provides 24-hour offline capability per constitutional requirements
 * Manages data caching, synchronization, and offline-first operations
 * for executive function continuity
 */

/* eslint-env browser */
/* global console */
import { DBSchema, IDBPDatabase, openDB } from 'idb';

// Type definitions for cached data
type DomainType = 'security' | 'productivity' | 'mtg' | 'infrastructure';
type CacheableData = Record<string, unknown>;
type PreferencesData = Record<string, unknown>;
type WorkflowState = Record<string, unknown>;
type TaskData = Record<string, unknown>;
type SyncData = Record<string, unknown>;

// Database schema for offline data
interface OfflineDataDB extends DBSchema {
  // Tool data cache
  toolData: {
    key: string;
    value: {
      id: string;
      toolId: string;
      domain: DomainType;
      data: CacheableData;
      timestamp: number;
      expiresAt: number;
      version: string;
    };
    indexes: { 'by-tool': string; 'by-domain': string; 'by-timestamp': number };
  };

  // User preferences cache
  preferences: {
    key: string;
    value: {
      id: string;
      userId: string;
      preferences: PreferencesData;
      timestamp: number;
      synchronized: boolean;
    };
  };

  // Workflow state cache
  workflows: {
    key: string;
    value: {
      id: string;
      workflowId: string;
      state: WorkflowState;
      timestamp: number;
      lastSaved: number;
      priority: 'high' | 'medium' | 'low';
    };
    indexes: { 'by-priority': string; 'by-timestamp': number };
  };

  // Task management cache
  tasks: {
    key: string;
    value: {
      id: string;
      taskId: string;
      title: string;
      status: 'pending' | 'in-progress' | 'completed';
      data: TaskData;
      timestamp: number;
      dueDate?: number;
    };
    indexes: { 'by-status': string; 'by-due-date': number };
  };

  // Sync queue for when connection is restored
  syncQueue: {
    key: string;
    value: {
      id: string;
      action: 'create' | 'update' | 'delete';
      resource: string;
      data: SyncData;
      timestamp: number;
      retryCount: number;
      priority: number;
    };
    indexes: { 'by-priority': number; 'by-timestamp': number };
  };

  // Cache metadata
  metadata: {
    key: string;
    value: {
      key: string;
      lastSync: number;
      cacheSize: number;
      version: string;
    };
  };
}

export class OfflineDataCache {
  private db: IDBPDatabase<OfflineDataDB> | null = null;
  private readonly DB_NAME = 'jane-offline-cache';
  private readonly DB_VERSION = 1;
  private readonly CACHE_DURATION = 24 * 60 * 60 * 1000; // 24 hours
  private readonly MAX_CACHE_SIZE = 50 * 1024 * 1024; // 50MB limit
  
  private syncListeners: Set<(status: 'syncing' | 'synced' | 'error') => void> = new Set();

  /**
   * Initialize the offline cache database
   */
  async initialize(): Promise<void> {
    try {
      this.db = await openDB<OfflineDataDB>(this.DB_NAME, this.DB_VERSION, {
        upgrade(db) {
          // Tool data store
          const toolStore = db.createObjectStore('toolData', { keyPath: 'id' });
          toolStore.createIndex('by-tool', 'toolId');
          toolStore.createIndex('by-domain', 'domain');
          toolStore.createIndex('by-timestamp', 'timestamp');

          // Preferences store
          db.createObjectStore('preferences', { keyPath: 'id' });

          // Workflows store
          const workflowStore = db.createObjectStore('workflows', { keyPath: 'id' });
          workflowStore.createIndex('by-priority', 'priority');
          workflowStore.createIndex('by-timestamp', 'timestamp');

          // Tasks store
          const taskStore = db.createObjectStore('tasks', { keyPath: 'id' });
          taskStore.createIndex('by-status', 'status');
          taskStore.createIndex('by-due-date', 'dueDate');

          // Sync queue store
          const syncStore = db.createObjectStore('syncQueue', { keyPath: 'id' });
          syncStore.createIndex('by-priority', 'priority');
          syncStore.createIndex('by-timestamp', 'timestamp');

          // Metadata store
          db.createObjectStore('metadata', { keyPath: 'key' });
        },
      });

      // Clean up expired data on initialization
      await this.cleanupExpiredData();
      
      console.log('[OfflineCache] Initialized successfully');
    } catch (error) {
      console.error('[OfflineCache] Failed to initialize:', error);
      throw error;
    }
  }

  /**
   * Cache tool data for offline access
   */
  async cacheToolData(toolId: string, domain: DomainType, data: CacheableData, ttl?: number): Promise<void> {
    if (!this.db) throw new Error('Database not initialized');

    const now = Date.now();
    const expiresAt = now + (ttl || this.CACHE_DURATION);

    const cacheEntry = {
      id: `tool-${toolId}-${now}`,
      toolId,
      domain,
      data,
      timestamp: now,
      expiresAt,
      version: '1.0.0',
    };

    try {
      await this.db.put('toolData', cacheEntry);
      await this.updateCacheMetadata();
      console.log(`[OfflineCache] Cached data for tool: ${toolId}`);
    } catch (error) {
      console.error(`[OfflineCache] Failed to cache tool data for ${toolId}:`, error);
      throw error;
    }
  }

  /**
   * Retrieve cached tool data
   */
  async getToolData(toolId: string): Promise<CacheableData | null> {
    if (!this.db) throw new Error('Database not initialized');

    try {
      const tx = this.db.transaction('toolData', 'readonly');
      const store = tx.objectStore('toolData');
      const index = store.index('by-tool');
      
      const entries = await index.getAll(toolId);
      
      if (entries.length === 0) return null;

      // Get the most recent non-expired entry
      const now = Date.now();
      const validEntries = entries
        .filter(entry => entry.expiresAt > now)
        .sort((a, b) => b.timestamp - a.timestamp);

      if (validEntries.length === 0) {
        // Clean up expired entries
        await this.cleanupToolData(toolId);
        return null;
      }

      return validEntries[0].data;
    } catch (error) {
      console.error(`[OfflineCache] Failed to get tool data for ${toolId}:`, error);
      return null;
    }
  }

  /**
   * Cache user preferences
   */
  async cachePreferences(userId: string, preferences: PreferencesData): Promise<void> {
    if (!this.db) throw new Error('Database not initialized');

    const cacheEntry = {
      id: `prefs-${userId}`,
      userId,
      preferences,
      timestamp: Date.now(),
      synchronized: false,
    };

    try {
      await this.db.put('preferences', cacheEntry);
      console.log(`[OfflineCache] Cached preferences for user: ${userId}`);
    } catch (error) {
      console.error(`[OfflineCache] Failed to cache preferences:`, error);
      throw error;
    }
  }

  /**
   * Get cached preferences
   */
  async getPreferences(userId: string): Promise<PreferencesData | null> {
    if (!this.db) throw new Error('Database not initialized');

    try {
      const entry = await this.db.get('preferences', `prefs-${userId}`);
      return entry ? entry.preferences : null;
    } catch (error) {
      console.error(`[OfflineCache] Failed to get preferences:`, error);
      return null;
    }
  }

  /**
   * Cache workflow state for executive function continuity
   */
  async cacheWorkflowState(workflowId: string, state: WorkflowState, priority: 'high' | 'medium' | 'low' = 'medium'): Promise<void> {
    if (!this.db) throw new Error('Database not initialized');

    const now = Date.now();
    const cacheEntry = {
      id: `workflow-${workflowId}`,
      workflowId,
      state,
      timestamp: now,
      lastSaved: now,
      priority,
    };

    try {
      await this.db.put('workflows', cacheEntry);
      console.log(`[OfflineCache] Cached workflow state: ${workflowId}`);
    } catch (error) {
      console.error(`[OfflineCache] Failed to cache workflow state:`, error);
      throw error;
    }
  }

  /**
   * Get cached workflow state
   */
  async getWorkflowState(workflowId: string): Promise<WorkflowState | null> {
    if (!this.db) throw new Error('Database not initialized');

    try {
      const entry = await this.db.get('workflows', `workflow-${workflowId}`);
      return entry ? entry.state : null;
    } catch (error) {
      console.error(`[OfflineCache] Failed to get workflow state:`, error);
      return null;
    }
  }

  /**
   * Add item to sync queue for when connection is restored
   */
  async addToSyncQueue(action: 'create' | 'update' | 'delete', resource: string, data: SyncData, priority: number = 1): Promise<void> {
    if (!this.db) throw new Error('Database not initialized');

    const queueItem = {
      id: `sync-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`,
      action,
      resource,
      data,
      timestamp: Date.now(),
      retryCount: 0,
      priority,
    };

    try {
      await this.db.put('syncQueue', queueItem);
      console.log(`[OfflineCache] Added to sync queue: ${action} ${resource}`);
    } catch (error) {
      console.error(`[OfflineCache] Failed to add to sync queue:`, error);
      throw error;
    }
  }

  /**
   * Process sync queue when connection is restored
   */
  async processSyncQueue(): Promise<void> {
    if (!this.db) throw new Error('Database not initialized');

    this.notifySyncListeners('syncing');

    try {
      const tx = this.db.transaction('syncQueue', 'readonly');
      const store = tx.objectStore('syncQueue');
      const index = store.index('by-priority');
      
      const queueItems = await index.getAll();
      
      // Sort by priority (higher priority first) then by timestamp
      const sortedItems = queueItems.sort((a, b) => {
        if (a.priority !== b.priority) {
          return b.priority - a.priority;
        }
        return a.timestamp - b.timestamp;
      });

      let successCount = 0;
      let errorCount = 0;

      for (const item of sortedItems) {
        try {
          await this.syncItem(item);
          await this.db.delete('syncQueue', item.id);
          successCount++;
        } catch (error) {
          console.error(`[OfflineCache] Failed to sync item ${item.id}:`, error);
          
          // Increment retry count
          item.retryCount++;
          
          if (item.retryCount < 3) {
            // Update retry count and keep in queue
            await this.db.put('syncQueue', item);
          } else {
            // Remove from queue after 3 failed attempts
            await this.db.delete('syncQueue', item.id);
          }
          
          errorCount++;
        }
      }

      console.log(`[OfflineCache] Sync completed: ${successCount} success, ${errorCount} errors`);
      this.notifySyncListeners(errorCount === 0 ? 'synced' : 'error');
      
      // Update last sync timestamp
      await this.updateLastSyncTime();
      
    } catch (error) {
      console.error('[OfflineCache] Failed to process sync queue:', error);
      this.notifySyncListeners('error');
      throw error;
    }
  }

  /**
   * Get cache statistics for monitoring
   */
  async getCacheStats(): Promise<{
    toolDataCount: number;
    preferencesCount: number;
    workflowsCount: number;
    tasksCount: number;
    syncQueueCount: number;
    totalSize: number;
    lastSync: number;
  }> {
    if (!this.db) throw new Error('Database not initialized');

    try {
      const [toolData, preferences, workflows, tasks, syncQueue, metadata] = await Promise.all([
        this.db.count('toolData'),
        this.db.count('preferences'),
        this.db.count('workflows'),
        this.db.count('tasks'),
        this.db.count('syncQueue'),
        this.db.get('metadata', 'cache-stats'),
      ]);

      return {
        toolDataCount: toolData,
        preferencesCount: preferences,
        workflowsCount: workflows,
        tasksCount: tasks,
        syncQueueCount: syncQueue,
        totalSize: metadata?.cacheSize || 0,
        lastSync: metadata?.lastSync || 0,
      };
    } catch (error) {
      console.error('[OfflineCache] Failed to get cache stats:', error);
      throw error;
    }
  }

  /**
   * Clear expired data to maintain performance
   */
  async cleanupExpiredData(): Promise<void> {
    if (!this.db) return;

    const now = Date.now();

    try {
      // Clean up expired tool data
      const tx = this.db.transaction('toolData', 'readwrite');
      const store = tx.objectStore('toolData');
      const cursor = await store.openCursor();
      
      let deletedCount = 0;
      
      if (cursor) {
        do {
          if (cursor.value.expiresAt < now) {
            await cursor.delete();
            deletedCount++;
          }
        } while (await cursor.continue());
      }

      if (deletedCount > 0) {
        console.log(`[OfflineCache] Cleaned up ${deletedCount} expired entries`);
        await this.updateCacheMetadata();
      }
    } catch (error) {
      console.error('[OfflineCache] Failed to cleanup expired data:', error);
    }
  }

  /**
   * Subscribe to sync status updates
   */
  onSyncStatusChange(listener: (status: 'syncing' | 'synced' | 'error') => void): () => void {
    this.syncListeners.add(listener);
    return () => this.syncListeners.delete(listener);
  }

  // Private helper methods

  private async syncItem(item: any): Promise<void> {
    // In a real implementation, this would make API calls to sync data
    // For now, we'll simulate the sync operation
    await new Promise(resolve => setTimeout(resolve, 100));
    
    // Simulate 90% success rate
    if (Math.random() < 0.1) {
      throw new Error('Simulated sync failure');
    }
  }

  private notifySyncListeners(status: 'syncing' | 'synced' | 'error'): void {
    this.syncListeners.forEach(listener => {
      try {
        listener(status);
      } catch (error) {
        console.error('[OfflineCache] Sync listener error:', error);
      }
    });
  }

  private async updateCacheMetadata(): Promise<void> {
    if (!this.db) return;

    try {
      // Calculate approximate cache size
      const stats = await this.getCacheStats();
      const approximateSize = (stats.toolDataCount + stats.preferencesCount + stats.workflowsCount) * 1024; // Rough estimate

      await this.db.put('metadata', {
        key: 'cache-stats',
        lastSync: Date.now(),
        cacheSize: approximateSize,
        version: '1.0.0',
      });
    } catch (error) {
      console.error('[OfflineCache] Failed to update cache metadata:', error);
    }
  }

  private async updateLastSyncTime(): Promise<void> {
    if (!this.db) return;

    try {
      const existing = await this.db.get('metadata', 'cache-stats');
      await this.db.put('metadata', {
        key: 'cache-stats',
        lastSync: Date.now(),
        cacheSize: existing?.cacheSize || 0,
        version: existing?.version || '1.0.0',
      });
    } catch (error) {
      console.error('[OfflineCache] Failed to update last sync time:', error);
    }
  }

  private async cleanupToolData(toolId: string): Promise<void> {
    if (!this.db) return;

    try {
      const tx = this.db.transaction('toolData', 'readwrite');
      const store = tx.objectStore('toolData');
      const index = store.index('by-tool');
      
      const entries = await index.getAll(toolId);
      const now = Date.now();
      
      for (const entry of entries) {
        if (entry.expiresAt < now) {
          await store.delete(entry.id);
        }
      }
    } catch (error) {
      console.error(`[OfflineCache] Failed to cleanup tool data for ${toolId}:`, error);
    }
  }
}

// Singleton instance
export const offlineCache = new OfflineDataCache();