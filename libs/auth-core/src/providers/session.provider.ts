// Session Provider implementation with Redis

import { createClient, RedisClientType } from 'redis';
import { v4 as uuidv4 } from 'uuid';
import { AuthConfig } from '../config';
import { SessionData, SessionPolicy, User } from '../types';

export class SessionProvider {
  private redisClient: RedisClientType;
  private config: AuthConfig;
  private connected: boolean = false;

  constructor(config: AuthConfig) {
    this.config = config;
    this.redisClient = createClient({
      url: config.redis.url,
      password: config.redis.password,
      database: config.redis.database || 0,
    });

    this.redisClient.on('error', (err) => {
      console.error('Redis client error:', err);
    });
  }

  /**
   * Initialize Redis connection
   */
  async connect(): Promise<void> {
    if (!this.connected) {
      await this.redisClient.connect();
      this.connected = true;
    }
  }

  /**
   * Close Redis connection
   */
  async disconnect(): Promise<void> {
    if (this.connected) {
      await this.redisClient.disconnect();
      this.connected = false;
    }
  }

  /**
   * Create a new session for a user
   */
  async createSession(
    user: User,
    ipAddress: string,
    userAgent: string,
    organizationId?: string
  ): Promise<SessionData> {
    await this.connect();

    const sessionId = uuidv4();
    const now = new Date();
    const policy = this.getSessionPolicy(user, organizationId);
    
    const sessionData: SessionData = {
      sessionId,
      userId: user.id,
      organizationId: organizationId || user.organizationId,
      ipAddress,
      userAgent,
      createdAt: now,
      lastActivity: now,
      expiresAt: new Date(now.getTime() + policy.maxDuration * 1000),
      mfaVerified: false,
    };

    // Check concurrent session limit
    await this.enforceConcurrentSessionLimit(user.id, policy.maxConcurrentSessions);

    // Store session data
    const sessionKey = this.getSessionKey(sessionId);
    await this.redisClient.setEx(
      sessionKey,
      policy.maxDuration,
      JSON.stringify(sessionData)
    );

    // Add to user's active sessions
    const userSessionsKey = this.getUserSessionsKey(user.id);
    await this.redisClient.sAdd(userSessionsKey, sessionId);
    await this.redisClient.expire(userSessionsKey, policy.maxDuration);

    return sessionData;
  }

  /**
   * Get session data by session ID
   */
  async getSession(sessionId: string): Promise<SessionData | null> {
    await this.connect();

    const sessionKey = this.getSessionKey(sessionId);
    const sessionJson = await this.redisClient.get(sessionKey);

    if (!sessionJson) {
      return null;
    }

    const sessionData: SessionData = JSON.parse(sessionJson);

    // Check if session has expired
    if (new Date() > sessionData.expiresAt) {
      await this.destroySession(sessionId);
      return null;
    }

    return sessionData;
  }

  /**
   * Update session activity timestamp
   */
  async updateSessionActivity(sessionId: string): Promise<void> {
    await this.connect();

    const sessionData = await this.getSession(sessionId);
    if (!sessionData) {
      return;
    }

    sessionData.lastActivity = new Date();

    const sessionKey = this.getSessionKey(sessionId);
    const ttl = await this.redisClient.ttl(sessionKey);
    
    if (ttl > 0) {
      await this.redisClient.setEx(
        sessionKey,
        ttl,
        JSON.stringify(sessionData)
      );
    }
  }

  /**
   * Mark session as MFA verified
   */
  async setMfaVerified(sessionId: string): Promise<void> {
    await this.connect();

    const sessionData = await this.getSession(sessionId);
    if (!sessionData) {
      return;
    }

    sessionData.mfaVerified = true;

    const sessionKey = this.getSessionKey(sessionId);
    const ttl = await this.redisClient.ttl(sessionKey);
    
    if (ttl > 0) {
      await this.redisClient.setEx(
        sessionKey,
        ttl,
        JSON.stringify(sessionData)
      );
    }
  }

  /**
   * Destroy a specific session
   */
  async destroySession(sessionId: string): Promise<void> {
    await this.connect();

    const sessionData = await this.getSession(sessionId);
    if (sessionData) {
      // Remove from user's active sessions
      const userSessionsKey = this.getUserSessionsKey(sessionData.userId);
      await this.redisClient.sRem(userSessionsKey, sessionId);
    }

    // Remove session data
    const sessionKey = this.getSessionKey(sessionId);
    await this.redisClient.del(sessionKey);
  }

  /**
   * Destroy all sessions for a user
   */
  async destroyAllUserSessions(userId: string): Promise<void> {
    await this.connect();

    const userSessionsKey = this.getUserSessionsKey(userId);
    const sessionIds = await this.redisClient.sMembers(userSessionsKey);

    // Delete all session data
    const pipeline = this.redisClient.multi();
    for (const sessionId of sessionIds) {
      pipeline.del(this.getSessionKey(sessionId));
    }
    pipeline.del(userSessionsKey);
    await pipeline.exec();
  }

  /**
   * Get all active sessions for a user
   */
  async getUserSessions(userId: string): Promise<SessionData[]> {
    await this.connect();

    const userSessionsKey = this.getUserSessionsKey(userId);
    const sessionIds = await this.redisClient.sMembers(userSessionsKey);

    const sessions: SessionData[] = [];
    for (const sessionId of sessionIds) {
      const sessionData = await this.getSession(sessionId);
      if (sessionData) {
        sessions.push(sessionData);
      }
    }

    return sessions;
  }

  /**
   * Clean up expired sessions
   */
  async cleanupExpiredSessions(): Promise<void> {
    // Redis handles TTL automatically, but we can implement additional cleanup if needed
    // This method could be called periodically to clean up orphaned data
  }

  /**
   * Enforce concurrent session limit for a user
   */
  private async enforceConcurrentSessionLimit(
    userId: string,
    maxSessions: number
  ): Promise<void> {
    const sessions = await this.getUserSessions(userId);
    
    if (sessions.length >= maxSessions) {
      // Sort by last activity and remove oldest sessions
      sessions.sort((a, b) => a.lastActivity.getTime() - b.lastActivity.getTime());
      
      const sessionsToRemove = sessions.slice(0, sessions.length - maxSessions + 1);
      for (const session of sessionsToRemove) {
        await this.destroySession(session.sessionId);
      }
    }
  }

  /**
   * Get session policy for user/organization
   */
  private getSessionPolicy(user: User, organizationId?: string): SessionPolicy {
    // Default policy - in practice, this would be fetched from organization settings
    return {
      maxDuration: 8 * 60 * 60, // 8 hours
      idleTimeout: 30 * 60, // 30 minutes
      maxConcurrentSessions: 5,
      requireMfaForSensitive: user.mfaEnabled,
    };
  }

  /**
   * Generate session Redis key
   */
  private getSessionKey(sessionId: string): string {
    return `${this.config.redis.keyPrefix}:session:${sessionId}`;
  }

  /**
   * Generate user sessions Redis key
   */
  private getUserSessionsKey(userId: string): string {
    return `${this.config.redis.keyPrefix}:user-sessions:${userId}`;
  }
}

export default SessionProvider;