/**
 * Cache Integration Service
 * 
 * Provides high-level interface for integrating offline cache
 * with the Jane Mental Prosthetic Platform
 */

/* eslint-env browser */
/* global console, navigator, window, setInterval, clearInterval */
import React from 'react';
import { offlineCache } from './cache';

export type SyncStatus = 'online' | 'offline' | 'syncing' | 'error';

export interface CacheIntegrationService {
  initialize(): Promise<void>;
  getSyncStatus(): SyncStatus;
  onSyncStatusChange(callback: (status: SyncStatus) => void): () => void;
  clearCache(): Promise<void>;
  getCacheSize(): Promise<number>;
}

class CacheIntegration implements CacheIntegrationService {
  private syncStatus: SyncStatus = 'offline';
  private syncStatusListeners: Set<(status: SyncStatus) => void> = new Set();
  private onlineListener?: () => void;
  private offlineListener?: () => void;

  async initialize(): Promise<void> {
    try {
      // Initialize offline cache
      await offlineCache.initialize();

      // Set up network status monitoring
      this.setupNetworkMonitoring();

      // Set up sync status monitoring
      offlineCache.onSyncStatusChange((status) => {
        if (status === 'syncing') {
          this.updateSyncStatus('syncing');
        } else if (status === 'synced') {
          this.updateSyncStatus('online');
        } else if (status === 'error') {
          this.updateSyncStatus('error');
        }
      });

      // Initial sync status
      this.updateSyncStatus(navigator.onLine ? 'online' : 'offline');

      console.log('[CacheIntegration] Initialized successfully');
    } catch (error) {
      console.error('[CacheIntegration] Failed to initialize:', error);
      throw error;
    }
  }

  getSyncStatus(): SyncStatus {
    return this.syncStatus;
  }

  onSyncStatusChange(callback: (status: SyncStatus) => void): () => void {
    this.syncStatusListeners.add(callback);
    return () => this.syncStatusListeners.delete(callback);
  }

  async clearCache(): Promise<void> {
    // This would clear the IndexedDB cache
    // Implementation depends on the IDB library's capabilities
    console.log('[CacheIntegration] Cache clear requested');
  }

  async getCacheSize(): Promise<number> {
    try {
      const stats = await offlineCache.getCacheStats();
      return stats.totalSize;
    } catch (error) {
      console.error('[CacheIntegration] Failed to get cache size:', error);
      return 0;
    }
  }

  private setupNetworkMonitoring(): void {
    this.onlineListener = () => {
      this.updateSyncStatus('online');
      // Trigger sync when coming back online
      offlineCache.processSyncQueue().catch(error => {
        console.error('[CacheIntegration] Failed to process sync queue:', error);
        this.updateSyncStatus('error');
      });
    };

    this.offlineListener = () => {
      this.updateSyncStatus('offline');
    };

    if (typeof window !== 'undefined') {
      window.addEventListener('online', this.onlineListener);
      window.addEventListener('offline', this.offlineListener);
    }
  }

  private updateSyncStatus(status: SyncStatus): void {
    if (this.syncStatus !== status) {
      this.syncStatus = status;
      this.syncStatusListeners.forEach(callback => {
        try {
          callback(status);
        } catch (error) {
          console.error('[CacheIntegration] Sync status callback error:', error);
        }
      });
    }
  }

  destroy(): void {
    if (this.onlineListener && typeof window !== 'undefined') {
      window.removeEventListener('online', this.onlineListener);
    }
    if (this.offlineListener && typeof window !== 'undefined') {
      window.removeEventListener('offline', this.offlineListener);
    }
    this.syncStatusListeners.clear();
  }
}

// Singleton instance
export const cacheIntegration = new CacheIntegration();

// React hook for using cache integration
export function useCacheIntegration() {
  const [syncStatus, setSyncStatus] = React.useState<SyncStatus>('offline');
  const [cacheSize, setCacheSize] = React.useState<number>(0);

  React.useEffect(() => {
    const unsubscribe = cacheIntegration.onSyncStatusChange(setSyncStatus);
    
    // Update cache size periodically
    const updateCacheSize = async () => {
      const size = await cacheIntegration.getCacheSize();
      setCacheSize(size);
    };

    updateCacheSize();
    const interval = setInterval(updateCacheSize, 30000); // Every 30 seconds

    return () => {
      unsubscribe();
      clearInterval(interval);
    };
  }, []);

  return {
    syncStatus,
    cacheSize,
    clearCache: cacheIntegration.clearCache.bind(cacheIntegration),
  };
}

// Export for testing and debugging
export { offlineCache };
