'use client';
/* eslint-disable no-undef */

import { useEffect } from 'react';

// Extend ServiceWorkerRegistration interface for background sync
declare global {
  interface ServiceWorkerRegistration {
    sync?: {
      register(tag: string): Promise<void>;
    };
  }
}

/**
 * PWA Service Worker Registration Component
 * Handles registration and lifecycle events for Jane Platform PWA
 * Provides 24-hour offline capability per constitutional requirements
 */
export default function ServiceWorkerRegistration() {
  useEffect(() => {
    if (typeof window !== 'undefined' && 'serviceWorker' in navigator) {
      // Register service worker for offline capability
      navigator.serviceWorker
        .register('/sw.js', {
          scope: '/',
          updateViaCache: 'none', // Always check for updates
        })
        .then((registration) => {
          console.log('[PWA] Service Worker registered successfully:', registration.scope);

          // Check for updates every 30 minutes (executive function continuity)
          setInterval(() => {
            registration.update();
          }, 30 * 60 * 1000);

          // Handle service worker updates
          registration.addEventListener('updatefound', () => {
            const newWorker = registration.installing;
            if (newWorker) {
              newWorker.addEventListener('statechange', () => {
                if (newWorker.state === 'installed' && navigator.serviceWorker.controller) {
                  // New service worker is available
                  // Show update notification (ADHD-friendly, non-intrusive)
                  showUpdateNotification();
                }
              });
            }
          });
        })
        .catch((error) => {
          console.error('[PWA] Service Worker registration failed:', error);
        });

      // Listen for service worker messages
      navigator.serviceWorker.addEventListener('message', (event) => {
        const { type, ...data } = event.data;

        switch (type) {
          case 'SYNC_COMPLETE':
            console.log('[PWA] Data sync completed:', data);
            // Update UI to show sync status
            updateSyncStatus('synced', data.timestamp);
            break;

          case 'PERFORMANCE_RESULT':
            // Log performance data for constitutional compliance monitoring
            if (data.duration > 200) {
              console.warn('[PWA] Performance violation:', data);
            }
            break;

          default:
            console.log('[PWA] Service Worker message:', event.data);
        }
      });

      // Handle online/offline events for executive function continuity
      const handleOnline = () => {
        console.log('[PWA] Connection restored');
        updateSyncStatus('online');
        
        // Trigger background sync
        navigator.serviceWorker.ready.then((registration) => {
          if (registration.sync) {
            return registration.sync.register('jane-data-sync');
          }
        });
      };

      const handleOffline = () => {
        console.log('[PWA] Connection lost - entering offline mode');
        updateSyncStatus('offline');
      };

      window.addEventListener('online', handleOnline);
      window.addEventListener('offline', handleOffline);

      // Initialize sync status
      updateSyncStatus(navigator.onLine ? 'online' : 'offline');

      // Cleanup event listeners
      return () => {
        window.removeEventListener('online', handleOnline);
        window.removeEventListener('offline', handleOffline);
      };
    }
  }, []);

  return null; // This component doesn't render anything
}

/**
 * Show update notification in an ADHD-friendly way
 */
function showUpdateNotification() {
  // Create a subtle, dismissible notification
  const notification = document.createElement('div');
  notification.id = 'jane-update-notification';
  notification.innerHTML = `
    <div style="
      position: fixed;
      top: 20px;
      right: 20px;
      background: #2563eb;
      color: white;
      padding: 16px 24px;
      border-radius: 12px;
      box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
      z-index: 10000;
      font-family: system-ui, -apple-system, sans-serif;
      font-size: 14px;
      max-width: 300px;
      animation: slideIn 0.3s ease-out;
    ">
      <div style="display: flex; align-items: center; justify-content: space-between;">
        <div>
          <div style="font-weight: 600; margin-bottom: 4px;">✨ Update Available</div>
          <div style="opacity: 0.9;">Refresh to get the latest features</div>
        </div>
        <button onclick="location.reload()" style="
          background: rgba(255, 255, 255, 0.2);
          border: none;
          color: white;
          padding: 8px 12px;
          border-radius: 6px;
          cursor: pointer;
          margin-left: 12px;
          font-size: 12px;
        ">
          Refresh
        </button>
      </div>
      <button onclick="this.parentElement.remove()" style="
        position: absolute;
        top: 8px;
        right: 8px;
        background: none;
        border: none;
        color: white;
        cursor: pointer;
        font-size: 16px;
        opacity: 0.7;
      ">
        ×
      </button>
    </div>
    <style>
      @keyframes slideIn {
        from { transform: translateX(100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
      }
    </style>
  `;

  document.body.appendChild(notification);

  // Auto-remove after 10 seconds (ADHD-friendly timeout)
  setTimeout(() => {
    const elem = document.getElementById('jane-update-notification');
    if (elem) {
      elem.remove();
    }
  }, 10000);
}

/**
 * Update sync status in the UI
 */
function updateSyncStatus(status: 'online' | 'offline' | 'synced', timestamp?: number) {
  // Store sync status in localStorage for persistence
  const syncData = {
    status,
    timestamp: timestamp || Date.now(),
  };
  
  localStorage.setItem('jane-sync-status', JSON.stringify(syncData));
  
  // Update any existing sync indicators in the UI
  const syncIndicators = document.querySelectorAll('[data-jane-sync-status]');
  syncIndicators.forEach((indicator) => {
    const element = indicator as HTMLElement;
    element.setAttribute('data-jane-sync-status', status);
    
    // Update visual appearance based on status
    switch (status) {
      case 'online':
        element.style.color = '#10b981';
        element.textContent = '🟢 Online';
        break;
      case 'offline':
        element.style.color = '#f59e0b';
        element.textContent = '🟡 Offline';
        break;
      case 'synced':
        element.style.color = '#10b981';
        element.textContent = '✅ Synced';
        break;
    }
  });

  // Dispatch custom event for other components to listen to
  window.dispatchEvent(new CustomEvent('jane-sync-status', {
    detail: syncData
  }));
}