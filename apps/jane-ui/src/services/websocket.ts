/**
 * WebSocket Service - Task T048 COMPLETED
 * 
 * Simplified WebSocket service for real-time updates in executive function platform
 * - Real-time tool status updates
 * - Performance metrics streaming
 * - Cross-tool synchronization
 * - Executive function state updates
 */

interface WebSocketMessage {
  type: string;
  payload: Record<string, unknown>;
  timestamp: string;
  sessionId?: string;
}

interface ToolStatusMessage extends WebSocketMessage {
  type: 'tool_status';
  payload: {
    toolId: string;
    status: 'active' | 'inactive' | 'maintenance';
    healthScore: number;
    responseTime?: number;
  };
}

interface PerformanceMetricMessage extends WebSocketMessage {
  type: 'performance_metric';
  payload: {
    domain: 'security' | 'productivity' | 'mtg' | 'infrastructure';
    toolId: string;
    responseTime: number;
    uptime: number;
    constitutionalCompliance: boolean;
  };
}

interface ExecutiveFunctionMessage extends WebSocketMessage {
  type: 'executive_function';
  payload: {
    cognitiveLoad: number;
    taskSwitches: number;
    focusTime: number;
    suggestions: string[];
  };
}

interface SyncMessage extends WebSocketMessage {
  type: 'sync';
  payload: {
    toolId: string;
    state: Record<string, unknown>;
    userId: string;
  };
}

type WSMessage = ToolStatusMessage | PerformanceMetricMessage | ExecutiveFunctionMessage | SyncMessage;

interface WebSocketConfig {
  url: string;
  reconnectInterval: number;
  maxReconnectAttempts: number;
  heartbeatInterval: number;
  enableLogging: boolean;
}

interface WebSocketState {
  connected: boolean;
  connecting: boolean;
  error: string | null;
  lastMessage: WSMessage | null;
  reconnectAttempts: number;
  messagesReceived: number;
  messagesSent: number;
}

const DEFAULT_CONFIG: WebSocketConfig = {
  url: 'ws://localhost:8000/ws',
  reconnectInterval: 5000,
  maxReconnectAttempts: 10,
  heartbeatInterval: 30000,
  enableLogging: false
};

class WebSocketService {
  private ws: unknown = null;
  private config: WebSocketConfig;
  private state: WebSocketState = {
    connected: false,
    connecting: false,
    error: null,
    lastMessage: null,
    reconnectAttempts: 0,
    messagesReceived: 0,
    messagesSent: 0
  };

  private listeners: Map<string, Array<(message: WSMessage) => void>> = new Map();
  private reconnectTimer: unknown = null;
  private heartbeatTimer: unknown = null;
  private sessionId: string | null = null;

  constructor(config: Partial<WebSocketConfig> = {}) {
    this.config = { ...DEFAULT_CONFIG, ...config };
    
    // Auto-connect in browser environment
    if (this.isBrowser()) {
      this.connect();
    }
  }

  private isBrowser(): boolean {
    return typeof window !== 'undefined' && typeof WebSocket !== 'undefined';
  }

  // Connection management
  connect(sessionId?: string): Promise<void> {
    if (!this.isBrowser()) {
      return Promise.reject(new Error('WebSocket not available in this environment'));
    }

    if (this.state.connected || this.state.connecting) {
      return Promise.resolve();
    }

    this.sessionId = sessionId || this.sessionId;
    this.setState({ connecting: true, error: null });

    return new Promise((resolve, reject) => {
      try {
        const wsUrl = this.sessionId 
          ? `${this.config.url}?sessionId=${this.sessionId}`
          : this.config.url;

        // Create WebSocket instance
        const WebSocketConstructor = (globalThis as { WebSocket?: new (url: string) => unknown }).WebSocket;
        if (!WebSocketConstructor) {
          throw new Error('WebSocket not available');
        }

        this.ws = new WebSocketConstructor(wsUrl);
        const ws = this.ws as {
          onopen: (() => void) | null;
          onclose: ((event: { reason?: string; wasClean?: boolean }) => void) | null;
          onerror: ((error: unknown) => void) | null;
          onmessage: ((event: { data: string }) => void) | null;
          close: (code?: number, reason?: string) => void;
          send: (data: string) => void;
        };

        ws.onopen = () => {
          this.setState({ 
            connected: true, 
            connecting: false, 
            reconnectAttempts: 0,
            error: null 
          });
          
          this.startHeartbeat();
          this.log('WebSocket connected');
          resolve();
        };

        ws.onclose = (event) => {
          this.setState({ 
            connected: false, 
            connecting: false,
            error: event.reason || 'Connection closed'
          });
          
          this.stopHeartbeat();
          this.log('WebSocket disconnected:', event.reason);
          
          if (!event.wasClean && this.state.reconnectAttempts < this.config.maxReconnectAttempts) {
            this.scheduleReconnect();
          }
        };

        ws.onerror = (error) => {
          this.setState({ 
            connecting: false,
            error: 'WebSocket error occurred'
          });
          
          this.log('WebSocket error:', error);
          reject(error);
        };

        ws.onmessage = (event) => {
          try {
            const message: WSMessage = JSON.parse(event.data);
            this.handleMessage(message);
          } catch (error) {
            this.log('Failed to parse WebSocket message:', error);
          }
        };

      } catch (error) {
        this.setState({ 
          connecting: false,
          error: error instanceof Error ? error.message : 'Failed to create WebSocket'
        });
        reject(error);
      }
    });
  }

  disconnect(): void {
    if (this.reconnectTimer && this.isBrowser()) {
      (globalThis as { clearTimeout?: (id: unknown) => void }).clearTimeout?.(this.reconnectTimer);
      this.reconnectTimer = null;
    }

    this.stopHeartbeat();

    if (this.ws) {
      const ws = this.ws as { close?: (code?: number, reason?: string) => void };
      ws.close?.(1000, 'Intentional disconnect');
      this.ws = null;
    }

    this.setState({ 
      connected: false, 
      connecting: false,
      reconnectAttempts: 0 
    });
  }

  // Message handling
  private handleMessage(message: WSMessage): void {
    this.setState({ 
      lastMessage: message,
      messagesReceived: this.state.messagesReceived + 1
    });

    this.log('Received message:', message);

    // Notify type-specific listeners
    const typeListeners = this.listeners.get(message.type) || [];
    typeListeners.forEach(listener => {
      try {
        listener(message);
      } catch (error) {
        this.log('Error in message listener:', error);
      }
    });

    // Notify all message listeners
    const allListeners = this.listeners.get('*') || [];
    allListeners.forEach(listener => {
      try {
        listener(message);
      } catch (error) {
        this.log('Error in universal message listener:', error);
      }
    });
  }

  sendMessage(type: string, payload: Record<string, unknown>): boolean {
    if (!this.ws || !this.state.connected) {
      this.log('Cannot send message: WebSocket not connected');
      return false;
    }

    const message: WebSocketMessage = {
      type,
      payload,
      timestamp: new Date().toISOString(),
      sessionId: this.sessionId || undefined
    };

    try {
      const ws = this.ws as { send?: (data: string) => void };
      ws.send?.(JSON.stringify(message));
      this.setState({ 
        messagesSent: this.state.messagesSent + 1 
      });
      this.log('Sent message:', message);
      return true;
    } catch (error) {
      this.log('Failed to send message:', error);
      return false;
    }
  }

  // Listeners
  on(messageType: string, listener: (message: WSMessage) => void): () => void {
    if (!this.listeners.has(messageType)) {
      this.listeners.set(messageType, []);
    }

    const listeners = this.listeners.get(messageType)!;
    listeners.push(listener);

    // Return unsubscribe function
    return () => {
      const index = listeners.indexOf(listener);
      if (index > -1) {
        listeners.splice(index, 1);
      }
    };
  }

  off(messageType: string, listener: (message: WSMessage) => void): void {
    const listeners = this.listeners.get(messageType);
    if (listeners) {
      const index = listeners.indexOf(listener);
      if (index > -1) {
        listeners.splice(index, 1);
      }
    }
  }

  // Specific message handlers
  onToolStatus(callback: (message: ToolStatusMessage) => void): () => void {
    return this.on('tool_status', callback as (message: WSMessage) => void);
  }

  onPerformanceMetric(callback: (message: PerformanceMetricMessage) => void): () => void {
    return this.on('performance_metric', callback as (message: WSMessage) => void);
  }

  onExecutiveFunction(callback: (message: ExecutiveFunctionMessage) => void): () => void {
    return this.on('executive_function', callback as (message: WSMessage) => void);
  }

  onSync(callback: (message: SyncMessage) => void): () => void {
    return this.on('sync', callback as (message: WSMessage) => void);
  }

  // Message sending helpers
  sendToolStatusUpdate(toolId: string, status: 'active' | 'inactive' | 'maintenance', healthScore: number): boolean {
    return this.sendMessage('tool_status_update', {
      toolId,
      status,
      healthScore,
      timestamp: new Date().toISOString()
    });
  }

  sendExecutiveFunctionUpdate(cognitiveLoad: number, taskSwitches: number): boolean {
    return this.sendMessage('executive_function_update', {
      cognitiveLoad,
      taskSwitches,
      timestamp: new Date().toISOString()
    });
  }

  sendToolStateSync(toolId: string, state: Record<string, unknown>): boolean {
    return this.sendMessage('tool_state_sync', {
      toolId,
      state,
      userId: this.sessionId,
      timestamp: new Date().toISOString()
    });
  }

  requestPerformanceMetrics(domains?: string[]): boolean {
    return this.sendMessage('request_performance_metrics', {
      domains,
      timestamp: new Date().toISOString()
    });
  }

  // Connection utilities
  private scheduleReconnect(): void {
    if (this.reconnectTimer || !this.isBrowser()) return;

    this.setState({ 
      reconnectAttempts: this.state.reconnectAttempts + 1 
    });

    const delay = Math.min(
      this.config.reconnectInterval * Math.pow(2, this.state.reconnectAttempts - 1),
      30000 // Max 30 seconds
    );

    this.log(`Scheduling reconnect in ${delay}ms (attempt ${this.state.reconnectAttempts})`);

    const globalObj = globalThis as { setTimeout?: (callback: () => void, delay: number) => unknown };
    this.reconnectTimer = globalObj.setTimeout?.(() => {
      this.reconnectTimer = null;
      if (!this.state.connected) {
        this.connect(this.sessionId || undefined);
      }
    }, delay);
  }

  private startHeartbeat(): void {
    if (!this.isBrowser()) return;

    const globalObj = globalThis as { setInterval?: (callback: () => void, interval: number) => unknown };
    this.heartbeatTimer = globalObj.setInterval?.(() => {
      if (this.state.connected) {
        this.sendMessage('heartbeat', {
          timestamp: new Date().toISOString()
        });
      }
    }, this.config.heartbeatInterval);
  }

  private stopHeartbeat(): void {
    if (this.heartbeatTimer && this.isBrowser()) {
      const globalObj = globalThis as { clearInterval?: (id: unknown) => void };
      globalObj.clearInterval?.(this.heartbeatTimer);
      this.heartbeatTimer = null;
    }
  }

  // State management
  private setState(updates: Partial<WebSocketState>): void {
    this.state = { ...this.state, ...updates };
  }

  getState(): WebSocketState {
    return { ...this.state };
  }

  isConnected(): boolean {
    return this.state.connected;
  }

  getConnectionStats(): { 
    messagesReceived: number; 
    messagesSent: number; 
    reconnectAttempts: number; 
  } {
    return {
      messagesReceived: this.state.messagesReceived,
      messagesSent: this.state.messagesSent,
      reconnectAttempts: this.state.reconnectAttempts
    };
  }

  // Utilities
  private log(message: string, ...args: unknown[]): void {
    if (this.config.enableLogging && this.isBrowser()) {
      const globalObj = globalThis as { console?: { log: (message: string, ...args: unknown[]) => void } };
      globalObj.console?.log(`[WebSocket] ${message}`, ...args);
    }
  }

  updateConfig(updates: Partial<WebSocketConfig>): void {
    this.config = { ...this.config, ...updates };
  }

  // Cleanup
  destroy(): void {
    this.disconnect();
    this.listeners.clear();
  }
}

// Check environment for singleton creation
const isDevelopment = typeof globalThis !== 'undefined' && 
  (globalThis as { process?: { env?: { NODE_ENV?: string } } }).process?.env?.NODE_ENV === 'development';

// Create singleton instance
export const webSocketService = new WebSocketService({
  enableLogging: isDevelopment
});

// Export types and service
export type { 
  WSMessage, 
  ToolStatusMessage, 
  PerformanceMetricMessage, 
  ExecutiveFunctionMessage,
  SyncMessage,
  WebSocketConfig,
  WebSocketState 
};
export { WebSocketService };
export default webSocketService;