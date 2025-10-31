/* eslint-env serviceworker */
/* global self, caches, fetch, URL, console, performance, clients, Response */

// Jane Platform Service Worker
// Provides 24-hour offline capability as per constitutional requirements

const CACHE_NAME = 'jane-platform-v1';
const OFFLINE_CACHE_NAME = 'jane-offline-v1';

// Resources to cache for offline operation (constitutional 24-hour requirement)
const ESSENTIAL_RESOURCES = [
  '/',
  '/manifest.json',
  '/offline',
  '/security',
  '/productivity',
  '/mtg',
  '/infrastructure',
  // Core UI assets
  '/_next/static/css/',
  '/_next/static/js/',
  // Executive function UI patterns
  '/icons/icon-192x192.png',
  '/icons/icon-512x512.png'
];

// API endpoints that can work offline with cached data
const OFFLINE_API_PATTERNS = [
  /^\/api\/dashboard/,
  /^\/api\/preferences/,
  /^\/api\/tools\/status/,
  /^\/api\/user\/profile/
];

// Critical tool data that must be available offline
const OFFLINE_TOOL_DATA = [
  '/api/security/tools',
  '/api/productivity/tools',
  '/api/mtg/tools',
  '/api/infrastructure/tools'
];

self.addEventListener('install', (event) => {
  console.log('[SW] Installing Jane Platform Service Worker');
  
  event.waitUntil(
    Promise.all([
      // Cache essential resources
      caches.open(CACHE_NAME).then((cache) => {
        return cache.addAll(ESSENTIAL_RESOURCES);
      }),
      // Cache offline tool data
      caches.open(OFFLINE_CACHE_NAME).then((cache) => {
        return cache.addAll(OFFLINE_TOOL_DATA);
      })
    ]).then(() => {
      console.log('[SW] Essential resources cached for offline operation');
      // Skip waiting to activate immediately (executive function continuity)
      return self.skipWaiting();
    })
  );
});

self.addEventListener('activate', (event) => {
  console.log('[SW] Activating Jane Platform Service Worker');
  
  event.waitUntil(
    Promise.all([
      // Clean up old caches
      caches.keys().then((cacheNames) => {
        return Promise.all(
          cacheNames.map((cacheName) => {
            if (cacheName !== CACHE_NAME && cacheName !== OFFLINE_CACHE_NAME) {
              console.log('[SW] Deleting old cache:', cacheName);
              return caches.delete(cacheName);
            }
          })
        );
      }),
      // Take control of all clients (reduce context switching)
      self.clients.claim()
    ])
  );
});

self.addEventListener('fetch', (event) => {
  const { request } = event;
  const url = new URL(request.url);

  // Handle different request types for optimal offline experience

  // 1. Navigation requests (pages) - Cache First with Network Fallback
  if (request.mode === 'navigate') {
    event.respondWith(
      caches.match(request)
        .then((cachedResponse) => {
          if (cachedResponse) {
            // Update cache in background for next visit
            fetch(request)
              .then((response) => {
                if (response.ok) {
                  caches.open(CACHE_NAME).then((cache) => {
                    cache.put(request, response);
                  });
                }
              })
              .catch(() => {
                // Network failed, cached version is being served
                console.log('[SW] Serving cached page:', request.url);
              });
            return cachedResponse;
          }
          
          // Not in cache, try network
          return fetch(request)
            .then((response) => {
              if (response.ok) {
                // Cache successful response
                caches.open(CACHE_NAME).then((cache) => {
                  cache.put(request, response.clone());
                });
              }
              return response;
            })
            .catch(() => {
              // Network failed, return offline page
              return caches.match('/offline');
            });
        })
    );
    return;
  }

  // 2. API requests - Cache First for offline APIs, Network First for others
  if (url.pathname.startsWith('/api/')) {
    const isOfflineAPI = OFFLINE_API_PATTERNS.some(pattern => pattern.test(url.pathname));
    
    if (isOfflineAPI) {
      // Cache First strategy for offline-capable APIs
      event.respondWith(
        caches.match(request)
          .then((cachedResponse) => {
            if (cachedResponse) {
              // Update cache in background
              fetch(request)
                .then((response) => {
                  if (response.ok) {
                    caches.open(OFFLINE_CACHE_NAME).then((cache) => {
                      cache.put(request, response);
                    });
                  }
                })
                .catch(() => {
                  console.log('[SW] Background update failed for:', request.url);
                });
              return cachedResponse;
            }
            
            // Not cached, try network and cache successful responses
            return fetch(request)
              .then((response) => {
                if (response.ok) {
                  caches.open(OFFLINE_CACHE_NAME).then((cache) => {
                    cache.put(request, response.clone());
                  });
                }
                return response;
              })
              .catch(() => {
                // Return empty response for failed offline API
                return new Response('{"offline": true, "error": "Network unavailable"}', {
                  status: 503,
                  headers: { 'Content-Type': 'application/json' }
                });
              });
          })
      );
    } else {
      // Network First strategy for real-time APIs
      event.respondWith(
        fetch(request)
          .then((response) => {
            if (response.ok && request.method === 'GET') {
              // Cache successful GET responses
              caches.open(CACHE_NAME).then((cache) => {
                cache.put(request, response.clone());
              });
            }
            return response;
          })
          .catch(() => {
            // Network failed, try cache
            return caches.match(request)
              .then((cachedResponse) => {
                if (cachedResponse) {
                  return cachedResponse;
                }
                // No cache available
                return new Response('{"offline": true, "error": "Service unavailable"}', {
                  status: 503,
                  headers: { 'Content-Type': 'application/json' }
                });
              });
          })
      );
    }
    return;
  }

  // 3. Static assets - Cache First
  if (request.destination === 'image' || 
      request.destination === 'style' || 
      request.destination === 'script' ||
      url.pathname.startsWith('/_next/static/')) {
    event.respondWith(
      caches.match(request)
        .then((cachedResponse) => {
          if (cachedResponse) {
            return cachedResponse;
          }
          
          return fetch(request)
            .then((response) => {
              if (response.ok) {
                caches.open(CACHE_NAME).then((cache) => {
                  cache.put(request, response.clone());
                });
              }
              return response;
            });
        })
    );
    return;
  }

  // 4. Everything else - Network First
  event.respondWith(
    fetch(request)
      .catch(() => {
        return caches.match(request);
      })
  );
});

// Background sync for offline data synchronization
self.addEventListener('sync', (event) => {
  if (event.tag === 'jane-data-sync') {
    event.waitUntil(
      syncOfflineData()
    );
  }
});

// Push notifications for executive function reminders
self.addEventListener('push', (event) => {
  const options = {
    body: event.data ? event.data.text() : 'Executive function reminder',
    icon: '/icons/icon-192x192.png',
    badge: '/icons/badge-72x72.png',
    vibrate: [100, 50, 100], // ADHD-friendly vibration pattern
    data: {
      dateOfArrival: Date.now(),
      primaryKey: 1
    },
    actions: [
      {
        action: 'open',
        title: 'Open Jane Platform',
        icon: '/icons/action-open.png'
      },
      {
        action: 'dismiss',
        title: 'Dismiss',
        icon: '/icons/action-dismiss.png'
      }
    ]
  };

  event.waitUntil(
    self.registration.showNotification('Jane Platform', options)
  );
});

// Handle notification clicks
self.addEventListener('notificationclick', (event) => {
  event.notification.close();

  if (event.action === 'open') {
    event.waitUntil(
      clients.openWindow('/')
    );
  }
});

// Sync offline data when network is restored
async function syncOfflineData() {
  try {
    console.log('[SW] Starting offline data synchronization');
    
    // Get all cached data that needs syncing
    const cache = await caches.open(OFFLINE_CACHE_NAME);
    const requests = await cache.keys();
    
    const syncPromises = requests.map(async (request) => {
      try {
        // Attempt to fetch fresh data
        const response = await fetch(request);
        if (response.ok) {
          // Update cache with fresh data
          await cache.put(request, response.clone());
          console.log('[SW] Synced:', request.url);
        }
      } catch (error) {
        console.log('[SW] Failed to sync:', request.url, error);
      }
    });

    await Promise.allSettled(syncPromises);
    console.log('[SW] Offline data synchronization completed');
    
    // Notify all clients that sync is complete
    const clients = await self.clients.matchAll();
    clients.forEach(client => {
      client.postMessage({
        type: 'SYNC_COMPLETE',
        timestamp: Date.now()
      });
    });
    
  } catch (error) {
    console.error('[SW] Sync failed:', error);
  }
}

// Performance monitoring for constitutional <200ms requirement
self.addEventListener('message', (event) => {
  if (event.data && event.data.type === 'MEASURE_PERFORMANCE') {
    const startTime = event.data.startTime;
    const endTime = performance.now();
    const duration = endTime - startTime;
    
    // Log performance issues (constitutional requirement)
    if (duration > 200) {
      console.warn(`[SW] Performance violation: ${duration}ms > 200ms for ${event.data.operation}`);
    }
    
    // Send performance data back to client
    event.source.postMessage({
      type: 'PERFORMANCE_RESULT',
      operation: event.data.operation,
      duration: duration,
      timestamp: Date.now()
    });
  }
});