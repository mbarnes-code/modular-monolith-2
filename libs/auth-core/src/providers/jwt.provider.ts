// JWT Provider implementation

import jwt from 'jsonwebtoken';
import { AuthConfig } from '../config';
import { AuthToken, JWTPayload, User } from '../types';

export class JWTProvider {
  private config: AuthConfig;

  constructor(config: AuthConfig) {
    this.config = config;
  }

  /**
   * Generate JWT access and refresh tokens for a user
   */
  async generateTokens(user: User, organizationId?: string): Promise<AuthToken> {
    const payload: Omit<JWTPayload, 'iat' | 'exp'> = {
      sub: user.id,
      email: user.email,
      roles: user.roles.map(r => r.name),
      permissions: user.permissions.map(p => `${p.resource}:${p.action}`),
      org: organizationId || user.organizationId,
      aud: this.config.jwt.audience,
      iss: this.config.jwt.issuer,
      jti: this.generateJTI()
    };

    const accessToken = jwt.sign(payload, this.config.jwt.secret, {
      expiresIn: this.config.jwt.accessTokenExpiry,
      algorithm: 'HS256'
    });

    const refreshPayload = {
      sub: user.id,
      type: 'refresh',
      jti: this.generateJTI()
    };

    const refreshToken = jwt.sign(refreshPayload, this.config.jwt.refreshSecret, {
      expiresIn: this.config.jwt.refreshTokenExpiry,
      algorithm: 'HS256'
    });

    return {
      accessToken,
      refreshToken,
      tokenType: 'Bearer',
      expiresIn: this.config.jwt.accessTokenExpiry,
      scope: 'read write'
    };
  }

  /**
   * Verify and decode JWT token
   */
  async verifyToken(token: string): Promise<JWTPayload> {
    try {
      const decoded = jwt.verify(token, this.config.jwt.secret, {
        audience: this.config.jwt.audience,
        issuer: this.config.jwt.issuer,
        algorithms: ['HS256']
      }) as JWTPayload;

      // Check if token is blacklisted
      if (decoded.jti && await this.isTokenBlacklisted(decoded.jti)) {
        throw new Error('Token has been revoked');
      }

      return decoded;
    } catch (error) {
      throw new Error(`Invalid token: ${error.message}`);
    }
  }

  /**
   * Refresh access token using refresh token
   */
  async refreshAccessToken(refreshToken: string): Promise<AuthToken> {
    try {
      const decoded = jwt.verify(refreshToken, this.config.jwt.refreshSecret) as any;
      
      if (decoded.type !== 'refresh') {
        throw new Error('Invalid refresh token');
      }

      // Get user from database (implement based on your user service)
      const user = await this.getUserById(decoded.sub);
      if (!user || !user.isActive) {
        throw new Error('User not found or inactive');
      }

      return this.generateTokens(user);
    } catch (error) {
      throw new Error(`Invalid refresh token: ${error.message}`);
    }
  }

  /**
   * Revoke token by adding to blacklist
   */
  async revokeToken(token: string): Promise<void> {
    try {
      const decoded = jwt.decode(token) as JWTPayload;
      if (decoded && decoded.jti) {
        await this.blacklistToken(decoded.jti, decoded.exp);
      }
    } catch (error) {
      // Token might be invalid, but that's okay for revocation
    }
  }

  /**
   * Generate unique JWT ID
   */
  private generateJTI(): string {
    return `${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
  }

  /**
   * Check if token is blacklisted (implement with Redis)
   */
  private async isTokenBlacklisted(jti: string): Promise<boolean> {
    // Implementation depends on your Redis service
    // return await this.redisService.exists(`blacklist:${jti}`);
    return false; // Placeholder
  }

  /**
   * Add token to blacklist (implement with Redis)
   */
  private async blacklistToken(jti: string, exp: number): Promise<void> {
    // Implementation depends on your Redis service
    // const ttl = exp - Math.floor(Date.now() / 1000);
    // await this.redisService.setex(`blacklist:${jti}`, ttl, '1');
  }

  /**
   * Get user by ID (implement based on your user service)
   */
  private async getUserById(userId: string): Promise<User | null> {
    // Implementation depends on your user service
    // return await this.userService.findById(userId);
    throw new Error('getUserById not implemented - integrate with user service');
  }
}

export default JWTProvider;