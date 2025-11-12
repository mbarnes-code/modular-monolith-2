/**
 * Secure Session Management Service
 * 
 * Provides secure session management for remote connections
 * with executive function accommodations and ADHD/autism support
 */

/* eslint-env browser */
/* global crypto, localStorage, sessionStorage, navigator, console, clearTimeout, setTimeout, clearInterval, setInterval, window */
import React from 'react';

export interface SessionConfig {
  sessionTimeout: number; // in milliseconds
  refreshThreshold: number; // time before expiry to refresh
  maxConcurrentSessions: number;
  requireBiometric?: boolean;
  enableRememberMe?: boolean;
}

export interface SessionData {
  sessionId: string;
  userId: string;
  deviceId: string;
  createdAt: number;
  expiresAt: number;
  lastActivity: number;
  permissions: string[];
  metadata: Record<string, unknown>;
}

export interface AuthToken {
  accessToken: string;
  refreshToken: string;
  tokenType: 'Bearer';
  expiresIn: number;
  issuedAt: number;
}

export type SessionStatus = 'active' | 'expired' | 'refreshing' | 'invalid' | 'unauthenticated';

const DEFAULT_CONFIG: SessionConfig = {
  sessionTimeout: 24 * 60 * 60 * 1000, // 24 hours for constitutional requirement
  refreshThreshold: 5 * 60 * 1000, // 5 minutes before expiry
  maxConcurrentSessions: 3, // Multiple device support
  requireBiometric: false,
  enableRememberMe: true,
};

export class SecureSessionManager {
  private config: SessionConfig;
  private currentSession: SessionData | null = null;
  private authToken: AuthToken | null = null;
  private refreshTimer: number | null = null;
  private sessionListeners: Set<(status: SessionStatus) => void> = new Set();
  private deviceId: string;

  constructor(config: Partial<SessionConfig> = {}) {
    this.config = { ...DEFAULT_CONFIG, ...config };
    this.deviceId = this.generateDeviceId();
    this.initializeFromStorage();
  }

  /**
   * Initialize session from stored data
   */
  private initializeFromStorage(): void {
    try {
      const storedSession = localStorage.getItem('jane-session');
      const storedAuth = sessionStorage.getItem('jane-auth');

      if (storedSession) {
        const sessionData = JSON.parse(storedSession) as SessionData;
        if (this.isValidSession(sessionData)) {
          this.currentSession = sessionData;
          this.notifyListeners('active');
        } else {
          this.clearStoredSession();
        }
      }

      if (storedAuth) {
        const authData = JSON.parse(storedAuth) as AuthToken;
        if (this.isValidToken(authData)) {
          this.authToken = authData;
          this.scheduleTokenRefresh();
        } else {
          this.clearStoredAuth();
        }
      }
    } catch (error) {
      console.error('[SessionManager] Failed to initialize from storage:', error);
      this.clearAllStorage();
    }
  }

  /**
   * Start a new secure session
   */
  async startSession(credentials: {
    username: string;
    password: string;
    rememberMe?: boolean;
    biometricData?: ArrayBuffer;
  }): Promise<SessionData> {
    try {
      // Authenticate with backend
      const authResponse = await this.authenticate(credentials);
      
      // Create session data
      const now = Date.now();
      const sessionData: SessionData = {
        sessionId: this.generateSessionId(),
        userId: authResponse.userId,
        deviceId: this.deviceId,
        createdAt: now,
        expiresAt: now + this.config.sessionTimeout,
        lastActivity: now,
        permissions: authResponse.permissions,
        metadata: {
          userAgent: navigator.userAgent,
          platform: navigator.platform,
          biometricEnabled: !!credentials.biometricData,
          rememberMe: credentials.rememberMe || false,
        },
      };

      // Store session and auth data
      this.currentSession = sessionData;
      this.authToken = {
        accessToken: authResponse.accessToken,
        refreshToken: authResponse.refreshToken,
        tokenType: 'Bearer',
        expiresIn: authResponse.expiresIn,
        issuedAt: now,
      };

      // Persist to storage
      this.persistSession(credentials.rememberMe || false);
      
      // Schedule token refresh
      this.scheduleTokenRefresh();

      // Notify listeners
      this.notifyListeners('active');

      console.log('[SessionManager] Session started successfully');
      return sessionData;
    } catch (error) {
      console.error('[SessionManager] Failed to start session:', error);
      throw error;
    }
  }

  /**
   * Refresh current session
   */
  async refreshSession(): Promise<void> {
    if (!this.currentSession || !this.authToken) {
      throw new Error('No active session to refresh');
    }

    try {
      this.notifyListeners('refreshing');

      const refreshResponse = await this.refreshToken(this.authToken.refreshToken);
      
      // Update auth token
      this.authToken = {
        accessToken: refreshResponse.accessToken,
        refreshToken: refreshResponse.refreshToken,
        tokenType: 'Bearer',
        expiresIn: refreshResponse.expiresIn,
        issuedAt: Date.now(),
      };

      // Update session expiry
      const now = Date.now();
      this.currentSession.expiresAt = now + this.config.sessionTimeout;
      this.currentSession.lastActivity = now;

      // Persist updated data
      this.persistSession(true);
      
      // Schedule next refresh
      this.scheduleTokenRefresh();

      this.notifyListeners('active');
      console.log('[SessionManager] Session refreshed successfully');
    } catch (error) {
      console.error('[SessionManager] Failed to refresh session:', error);
      await this.endSession();
      throw error;
    }
  }

  /**
   * End current session
   */
  async endSession(): Promise<void> {
    try {
      if (this.currentSession && this.authToken) {
        // Notify backend of session termination
        await this.revokeToken(this.authToken.refreshToken);
      }
    } catch (error) {
      console.error('[SessionManager] Failed to revoke token:', error);
    } finally {
      // Clear local data
      this.currentSession = null;
      this.authToken = null;
      
      if (this.refreshTimer) {
        clearTimeout(this.refreshTimer);
        this.refreshTimer = null;
      }

      this.clearAllStorage();
      this.notifyListeners('unauthenticated');
      console.log('[SessionManager] Session ended');
    }
  }

  /**
   * Update session activity
   */
  updateActivity(): void {
    if (this.currentSession) {
      this.currentSession.lastActivity = Date.now();
      this.persistSession(true);
    }
  }

  /**
   * Get current session status
   */
  getSessionStatus(): SessionStatus {
    if (!this.currentSession || !this.authToken) {
      return 'unauthenticated';
    }

    if (!this.isValidSession(this.currentSession)) {
      return 'expired';
    }

    if (!this.isValidToken(this.authToken)) {
      return 'expired';
    }

    return 'active';
  }

  /**
   * Get current session data
   */
  getCurrentSession(): SessionData | null {
    return this.currentSession;
  }

  /**
   * Get auth token for API requests
   */
  getAuthToken(): string | null {
    return this.authToken ? `${this.authToken.tokenType} ${this.authToken.accessToken}` : null;
  }

  /**
   * Subscribe to session status changes
   */
  onSessionStatusChange(listener: (status: SessionStatus) => void): () => void {
    this.sessionListeners.add(listener);
    return () => this.sessionListeners.delete(listener);
  }

  /**
   * Check if user has specific permission
   */
  hasPermission(permission: string): boolean {
    return this.currentSession?.permissions.includes(permission) || false;
  }

  // Private helper methods

  private async authenticate(_credentials: {
    username: string;
    password: string;
    biometricData?: ArrayBuffer;
  }): Promise<{
    userId: string;
    accessToken: string;
    refreshToken: string;
    expiresIn: number;
    permissions: string[];
  }> {
    // In a real implementation, this would make an API call
    // For now, simulate authentication
    await new Promise(resolve => setTimeout(resolve, 500));

    // Simulate successful authentication
    return {
      userId: `user-${Date.now()}`,
      accessToken: this.generateToken(),
      refreshToken: this.generateToken(),
      expiresIn: 3600000, // 1 hour
      permissions: ['read', 'write', 'admin'], // Example permissions
    };
  }

  private async refreshToken(_refreshToken: string): Promise<{
    accessToken: string;
    refreshToken: string;
    expiresIn: number;
  }> {
    // In a real implementation, this would make an API call
    await new Promise(resolve => setTimeout(resolve, 200));

    return {
      accessToken: this.generateToken(),
      refreshToken: this.generateToken(),
      expiresIn: 3600000, // 1 hour
    };
  }

  private async revokeToken(_refreshToken: string): Promise<void> {
    // In a real implementation, this would make an API call
    await new Promise(resolve => setTimeout(resolve, 100));
  }

  private generateSessionId(): string {
    return `session-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
  }

  private generateToken(): string {
    const array = new Uint8Array(32);
    crypto.getRandomValues(array);
    return Array.from(array, byte => byte.toString(16).padStart(2, '0')).join('');
  }

  private generateDeviceId(): string {
    let deviceId = localStorage.getItem('jane-device-id');
    if (!deviceId) {
      deviceId = `device-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
      localStorage.setItem('jane-device-id', deviceId);
    }
    return deviceId;
  }

  private isValidSession(session: SessionData): boolean {
    const now = Date.now();
    return session.expiresAt > now && (now - session.lastActivity) < this.config.sessionTimeout;
  }

  private isValidToken(token: AuthToken): boolean {
    const now = Date.now();
    return (token.issuedAt + token.expiresIn) > now;
  }

  private persistSession(persistent: boolean): void {
    if (this.currentSession) {
      if (persistent) {
        localStorage.setItem('jane-session', JSON.stringify(this.currentSession));
      } else {
        sessionStorage.setItem('jane-session', JSON.stringify(this.currentSession));
      }
    }

    if (this.authToken) {
      // Auth tokens are always stored in session storage for security
      sessionStorage.setItem('jane-auth', JSON.stringify(this.authToken));
    }
  }

  private scheduleTokenRefresh(): void {
    if (this.refreshTimer) {
      clearTimeout(this.refreshTimer);
    }

    if (!this.authToken) return;

    const now = Date.now();
    const expiryTime = this.authToken.issuedAt + this.authToken.expiresIn;
    const refreshTime = expiryTime - this.config.refreshThreshold;
    const timeUntilRefresh = Math.max(0, refreshTime - now);

    this.refreshTimer = window.setTimeout(() => {
      this.refreshSession().catch(error => {
        console.error('[SessionManager] Automatic refresh failed:', error);
      });
    }, timeUntilRefresh);
  }

  private notifyListeners(status: SessionStatus): void {
    this.sessionListeners.forEach(listener => {
      try {
        listener(status);
      } catch (error) {
        console.error('[SessionManager] Listener error:', error);
      }
    });
  }

  private clearStoredSession(): void {
    localStorage.removeItem('jane-session');
    sessionStorage.removeItem('jane-session');
  }

  private clearStoredAuth(): void {
    sessionStorage.removeItem('jane-auth');
  }

  private clearAllStorage(): void {
    this.clearStoredSession();
    this.clearStoredAuth();
  }
}

// Singleton instance
export const sessionManager = new SecureSessionManager();

// React hook for session management
export function useSession() {
  const [sessionStatus, setSessionStatus] = React.useState<SessionStatus>('unauthenticated');
  const [currentSession, setCurrentSession] = React.useState<SessionData | null>(null);

  React.useEffect(() => {
    // Initialize session status
    setSessionStatus(sessionManager.getSessionStatus());
    setCurrentSession(sessionManager.getCurrentSession());

    // Subscribe to session changes
    const unsubscribe = sessionManager.onSessionStatusChange((status) => {
      setSessionStatus(status);
      setCurrentSession(sessionManager.getCurrentSession());
    });

    return unsubscribe;
  }, []);

  const login = React.useCallback(async (credentials: {
    username: string;
    password: string;
    rememberMe?: boolean;
  }) => {
    await sessionManager.startSession(credentials);
  }, []);

  const logout = React.useCallback(async () => {
    await sessionManager.endSession();
  }, []);

  const hasPermission = React.useCallback((permission: string) => {
    return sessionManager.hasPermission(permission);
  }, []);

  return {
    sessionStatus,
    currentSession,
    login,
    logout,
    hasPermission,
    updateActivity: sessionManager.updateActivity.bind(sessionManager),
    getAuthToken: sessionManager.getAuthToken.bind(sessionManager),
  };
}

// Activity tracker for executive function support
export class SessionActivityTracker {
  private lastActivity: number = Date.now();
  private activityTimer: number | null = null;
  private readonly ACTIVITY_INTERVAL = 30000; // 30 seconds

  start(): void {
    this.updateActivity();
    this.scheduleActivityUpdate();
  }

  stop(): void {
    if (this.activityTimer) {
      clearInterval(this.activityTimer);
      this.activityTimer = null;
    }
  }

  private updateActivity(): void {
    this.lastActivity = Date.now();
    sessionManager.updateActivity();
  }

  private scheduleActivityUpdate(): void {
    this.activityTimer = window.setInterval(() => {
      this.updateActivity();
    }, this.ACTIVITY_INTERVAL);
  }
}

export const activityTracker = new SessionActivityTracker();