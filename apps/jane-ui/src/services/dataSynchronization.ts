/**
 * Data Synchronization Service
 * 
 * Manages seamless data synchronization during offline/online transitions
 * for the Jane Mental Prosthetic Platform with executive function continuity
 */

/* eslint-env browser */
/* global console, navigator, window, setTimeout, clearInterval, setInterval */
import React from 'react';
import { offlineCache } from './cache';

export type SyncOperation = 'sync' | 'conflict_resolution' | 'merge' | 'rollback';
export type SyncPriority = 'critical' | 'high' | 'medium' | 'low';
export type ConflictResolution = 'server_wins' | 'client_wins' | 'merge' | 'manual';

export interface SyncItem {
  id: string;
  type: 'toolData' | 'preferences' | 'workflows' | 'tasks';
  resourceId: string;
  operation: 'create' | 'update' | 'delete';
  data: Record<string, unknown>;
  localTimestamp: number;
  serverTimestamp?: number;
  priority: SyncPriority;
  retryCount: number;
  maxRetries: number;
}

export interface SyncConflict {
  id: string;
  type: string;
  resourceId: string;
  localData: Record<string, unknown>;
  serverData: Record<string, unknown>;
  localTimestamp: number;
  serverTimestamp: number;
}

export interface SyncResult {
  success: boolean;
  synced: number;
  failed: number;
  conflicts: SyncConflict[];
  errors: Array<{ item: SyncItem; error: string }>;
}

export interface SyncProgress {
  operation: SyncOperation;
  current: number;
  total: number;
  percentage: number;
  currentItem?: string;
}

export class DataSynchronizationService {
  private syncQueue: SyncItem[] = [];
  private isOnline: boolean = navigator.onLine;
  private isSyncing: boolean = false;
  private syncListeners: Set<(progress: SyncProgress) => void> = new Set();
  private conflictListeners: Set<(conflicts: SyncConflict[]) => void> = new Set();
  private syncInterval: number | null = null;

  private readonly SYNC_INTERVAL = 60000; // 1 minute
  private readonly BATCH_SIZE = 10; // Process 10 items at a time
  private readonly MAX_RETRIES = 3;

  constructor() {
    this.setupNetworkMonitoring();
    this.setupPeriodicSync();
  }

  /**
   * Initialize synchronization service
   */
  async initialize(): Promise<void> {
    try {
      // Load pending sync items from cache
      await this.loadPendingSyncItems();
      
      // Start automatic sync if online
      if (this.isOnline) {
        await this.performSync();
      }

      console.log('[SyncService] Initialized successfully');
    } catch (error) {
      console.error('[SyncService] Failed to initialize:', error);
      throw error;
    }
  }

  /**
   * Add item to sync queue
   */
  async addToSyncQueue(
    type: 'toolData' | 'preferences' | 'workflows' | 'tasks',
    resourceId: string,
    operation: 'create' | 'update' | 'delete',
    data: Record<string, unknown>,
    priority: SyncPriority = 'medium'
  ): Promise<void> {
    const syncItem: SyncItem = {
      id: `sync-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`,
      type,
      resourceId,
      operation,
      data,
      localTimestamp: Date.now(),
      priority,
      retryCount: 0,
      maxRetries: this.MAX_RETRIES,
    };

    this.syncQueue.push(syncItem);
    await this.persistSyncQueue();

    // Also add to offline cache sync queue
    await offlineCache.addToSyncQueue(
      operation,
      `${type}/${resourceId}`,
      data,
      this.getPriorityValue(priority)
    );

    console.log(`[SyncService] Added to sync queue: ${type}/${resourceId}`);

    // Attempt immediate sync if online
    if (this.isOnline && !this.isSyncing) {
      this.performSync().catch(error => {
        console.error('[SyncService] Immediate sync failed:', error);
      });
    }
  }

  /**
   * Perform full synchronization
   */
  async performSync(): Promise<SyncResult> {
    if (this.isSyncing) {
      throw new Error('Sync already in progress');
    }

    if (!this.isOnline) {
      throw new Error('Cannot sync while offline');
    }

    this.isSyncing = true;
    const conflicts: SyncConflict[] = [];
    const errors: Array<{ item: SyncItem; error: string }> = [];
    let synced = 0;
    let failed = 0;

    try {
      this.notifyProgress({
        operation: 'sync',
        current: 0,
        total: this.syncQueue.length,
        percentage: 0,
      });

      // Sort by priority (critical first)
      const sortedQueue = this.sortByPriority([...this.syncQueue]);
      
      // Process in batches
      for (let i = 0; i < sortedQueue.length; i += this.BATCH_SIZE) {
        const batch = sortedQueue.slice(i, i + this.BATCH_SIZE);
        
        for (const item of batch) {
          try {
            this.notifyProgress({
              operation: 'sync',
              current: i + synced + 1,
              total: sortedQueue.length,
              percentage: Math.round(((i + synced + 1) / sortedQueue.length) * 100),
              currentItem: `${item.type}/${item.resourceId}`,
            });

            const result = await this.syncItem(item);
            
            if (result.success) {
              synced++;
              this.removeSyncItem(item.id);
            } else if (result.conflict) {
              conflicts.push(result.conflict);
              this.removeSyncItem(item.id); // Remove from queue, handle conflict separately
            } else {
              item.retryCount++;
              if (item.retryCount >= item.maxRetries) {
                errors.push({ item, error: result.error || 'Max retries exceeded' });
                this.removeSyncItem(item.id);
                failed++;
              }
            }
          } catch (error) {
            console.error(`[SyncService] Failed to sync item ${item.id}:`, error);
            item.retryCount++;
            if (item.retryCount >= item.maxRetries) {
              errors.push({ item, error: error instanceof Error ? error.message : String(error) });
              this.removeSyncItem(item.id);
              failed++;
            }
          }
        }

        // Small delay between batches to prevent overwhelming the server
        await new Promise(resolve => setTimeout(resolve, 100));
      }

      // Handle conflicts if any
      if (conflicts.length > 0) {
        this.notifyConflicts(conflicts);
      }

      // Persist updated sync queue
      await this.persistSyncQueue();

      const result: SyncResult = {
        success: errors.length === 0 && conflicts.length === 0,
        synced,
        failed,
        conflicts,
        errors,
      };

      console.log(`[SyncService] Sync completed: ${synced} synced, ${failed} failed, ${conflicts.length} conflicts`);
      return result;

    } finally {
      this.isSyncing = false;
      this.notifyProgress({
        operation: 'sync',
        current: this.syncQueue.length,
        total: this.syncQueue.length,
        percentage: 100,
      });
    }
  }

  /**
   * Resolve sync conflict
   */
  async resolveConflict(
    conflict: SyncConflict,
    resolution: ConflictResolution,
    customData?: Record<string, unknown>
  ): Promise<void> {
    try {
      let resolvedData: Record<string, unknown>;

      switch (resolution) {
        case 'server_wins':
          resolvedData = conflict.serverData;
          break;
        case 'client_wins':
          resolvedData = conflict.localData;
          break;
        case 'merge':
          resolvedData = this.mergeData(conflict.localData, conflict.serverData);
          break;
        case 'manual':
          if (!customData) {
            throw new Error('Custom data required for manual resolution');
          }
          resolvedData = customData;
          break;
        default:
          throw new Error(`Unknown conflict resolution: ${resolution}`);
      }

      // Apply resolution by syncing the resolved data
      await this.addToSyncQueue(
        conflict.type as 'toolData' | 'preferences' | 'workflows' | 'tasks',
        conflict.resourceId,
        'update',
        resolvedData,
        'high'
      );

      console.log(`[SyncService] Conflict resolved: ${conflict.id} using ${resolution}`);
    } catch (error) {
      console.error(`[SyncService] Failed to resolve conflict ${conflict.id}:`, error);
      throw error;
    }
  }

  /**
   * Get sync status
   */
  getSyncStatus(): {
    isOnline: boolean;
    isSyncing: boolean;
    queueSize: number;
    lastSync?: number;
  } {
    return {
      isOnline: this.isOnline,
      isSyncing: this.isSyncing,
      queueSize: this.syncQueue.length,
      // Would get from cache in real implementation
      lastSync: Date.now(),
    };
  }

  /**
   * Force sync when coming online
   */
  async forceSync(): Promise<SyncResult> {
    if (!this.isOnline) {
      throw new Error('Cannot force sync while offline');
    }

    return this.performSync();
  }

  /**
   * Subscribe to sync progress
   */
  onSyncProgress(listener: (progress: SyncProgress) => void): () => void {
    this.syncListeners.add(listener);
    return () => this.syncListeners.delete(listener);
  }

  /**
   * Subscribe to conflict notifications
   */
  onConflicts(listener: (conflicts: SyncConflict[]) => void): () => void {
    this.conflictListeners.add(listener);
    return () => this.conflictListeners.delete(listener);
  }

  // Private helper methods

  private setupNetworkMonitoring(): void {
    if (typeof window !== 'undefined') {
      window.addEventListener('online', () => {
        this.isOnline = true;
        console.log('[SyncService] Network online - starting sync');
        this.performSync().catch(error => {
          console.error('[SyncService] Auto-sync after coming online failed:', error);
        });
      });

      window.addEventListener('offline', () => {
        this.isOnline = false;
        console.log('[SyncService] Network offline - sync paused');
      });
    }
  }

  private setupPeriodicSync(): void {
    if (typeof window !== 'undefined') {
      this.syncInterval = window.setInterval(() => {
        if (this.isOnline && !this.isSyncing && this.syncQueue.length > 0) {
          this.performSync().catch(error => {
            console.error('[SyncService] Periodic sync failed:', error);
          });
        }
      }, this.SYNC_INTERVAL);
    }
  }

  private async syncItem(item: SyncItem): Promise<{
    success: boolean;
    conflict?: SyncConflict;
    error?: string;
  }> {
    try {
      // In a real implementation, this would make API calls
      // For now, simulate sync behavior
      await new Promise(resolve => setTimeout(resolve, 100));

      // Simulate some conflicts (10% chance)
      if (Math.random() < 0.1) {
        return {
          success: false,
          conflict: {
            id: `conflict-${item.id}`,
            type: item.type,
            resourceId: item.resourceId,
            localData: item.data,
            serverData: { ...item.data, serverModified: true },
            localTimestamp: item.localTimestamp,
            serverTimestamp: Date.now() + 1000,
          },
        };
      }

      // Simulate some failures (5% chance)
      if (Math.random() < 0.05) {
        return {
          success: false,
          error: 'Simulated sync failure',
        };
      }

      return { success: true };
    } catch (error) {
      return {
        success: false,
        error: error instanceof Error ? error.message : String(error),
      };
    }
  }

  private sortByPriority(items: SyncItem[]): SyncItem[] {
    const priorityOrder = { critical: 0, high: 1, medium: 2, low: 3 };
    return items.sort((a, b) => {
      const aPriority = priorityOrder[a.priority];
      const bPriority = priorityOrder[b.priority];
      if (aPriority !== bPriority) {
        return aPriority - bPriority;
      }
      return a.localTimestamp - b.localTimestamp;
    });
  }

  private mergeData(localData: Record<string, unknown>, serverData: Record<string, unknown>): Record<string, unknown> {
    // Simple merge strategy - in practice, this would be more sophisticated
    return {
      ...serverData,
      ...localData,
      _merged: true,
      _mergeTimestamp: Date.now(),
    };
  }

  private getPriorityValue(priority: SyncPriority): number {
    const values = { critical: 4, high: 3, medium: 2, low: 1 };
    return values[priority];
  }

  private removeSyncItem(id: string): void {
    this.syncQueue = this.syncQueue.filter(item => item.id !== id);
  }

  private async loadPendingSyncItems(): Promise<void> {
    // In a real implementation, this would load from IndexedDB
    // For now, just initialize empty queue
    this.syncQueue = [];
  }

  private async persistSyncQueue(): Promise<void> {
    // In a real implementation, this would persist to IndexedDB
    // For now, just log the queue size
    console.log(`[SyncService] Sync queue size: ${this.syncQueue.length}`);
  }

  private notifyProgress(progress: SyncProgress): void {
    this.syncListeners.forEach(listener => {
      try {
        listener(progress);
      } catch (error) {
        console.error('[SyncService] Progress listener error:', error);
      }
    });
  }

  private notifyConflicts(conflicts: SyncConflict[]): void {
    this.conflictListeners.forEach(listener => {
      try {
        listener(conflicts);
      } catch (error) {
        console.error('[SyncService] Conflict listener error:', error);
      }
    });
  }

  destroy(): void {
    if (this.syncInterval) {
      clearInterval(this.syncInterval);
      this.syncInterval = null;
    }
    this.syncListeners.clear();
    this.conflictListeners.clear();
  }
}

// Singleton instance
export const dataSynchronization = new DataSynchronizationService();

// React hook for data synchronization
export function useDataSync() {
  const [syncStatus, setSyncStatus] = React.useState(dataSynchronization.getSyncStatus());
  const [syncProgress, setSyncProgress] = React.useState<SyncProgress | null>(null);
  const [conflicts, setConflicts] = React.useState<SyncConflict[]>([]);

  React.useEffect(() => {
    // Set up progress monitoring
    const unsubscribeProgress = dataSynchronization.onSyncProgress(setSyncProgress);
    const unsubscribeConflicts = dataSynchronization.onConflicts(setConflicts);

    // Update sync status periodically
    const updateStatus = () => {
      setSyncStatus(dataSynchronization.getSyncStatus());
    };

    updateStatus();
    const statusInterval = setInterval(updateStatus, 5000);

    return () => {
      unsubscribeProgress();
      unsubscribeConflicts();
      clearInterval(statusInterval);
    };
  }, []);

  const forceSync = React.useCallback(async () => {
    try {
      await dataSynchronization.forceSync();
    } catch (error) {
      console.error('[useDataSync] Force sync failed:', error);
      throw error;
    }
  }, []);

  const resolveConflict = React.useCallback(async (
    conflict: SyncConflict,
    resolution: ConflictResolution,
    customData?: Record<string, unknown>
  ) => {
    await dataSynchronization.resolveConflict(conflict, resolution, customData);
    // Remove resolved conflict from state
    setConflicts(prev => prev.filter(c => c.id !== conflict.id));
  }, []);

  return {
    syncStatus,
    syncProgress,
    conflicts,
    forceSync,
    resolveConflict,
  };
}