// Session management exports

export { SessionProvider } from '../providers/session.provider';

// Session-specific utilities
export class SessionUtils {
  /**
   * Generate session ID
   */
  static generateSessionId(): string {
    const crypto = require('crypto');
    return crypto.randomUUID();
  }

  /**
   * Check if session is expired
   */
  static isExpired(expiresAt: Date): boolean {
    return new Date() > expiresAt;
  }

  /**
   * Calculate session remaining time in seconds
   */
  static getRemainingTime(expiresAt: Date): number {
    const now = new Date().getTime();
    const expiry = expiresAt.getTime();
    return Math.max(0, Math.floor((expiry - now) / 1000));
  }

  /**
   * Check if session is idle based on last activity
   */
  static isIdle(lastActivity: Date, idleTimeoutSeconds: number): boolean {
    const now = new Date().getTime();
    const lastActivityTime = lastActivity.getTime();
    return (now - lastActivityTime) > (idleTimeoutSeconds * 1000);
  }

  /**
   * Extend session expiration
   */
  static extendSession(currentExpiry: Date, extensionSeconds: number): Date {
    return new Date(currentExpiry.getTime() + (extensionSeconds * 1000));
  }
}