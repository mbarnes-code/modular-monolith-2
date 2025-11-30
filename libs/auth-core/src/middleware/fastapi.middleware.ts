// FastAPI middleware for authentication

import { NextFunction, Request, Response } from 'express';
import { AuthConfig } from '../config';
import { ApiKeyProvider, JWTProvider, SessionProvider } from '../providers';
import { AuthMiddlewareOptions, AuthStrategy, User } from '../types';

export class FastAPIAuthMiddleware {
  private jwtProvider: JWTProvider;
  private sessionProvider: SessionProvider;
  private apiKeyProvider: ApiKeyProvider;
  private config: AuthConfig;

  constructor(config: AuthConfig) {
    this.config = config;
    this.jwtProvider = new JWTProvider(config);
    this.sessionProvider = new SessionProvider(config);
    this.apiKeyProvider = new ApiKeyProvider(config);
  }

  /**
   * Create FastAPI-compatible middleware function
   */
  createMiddleware(options: AuthMiddlewareOptions = {}) {
    return async (req: Request, res: Response, next: NextFunction) => {
      try {
        // Skip authentication for excluded paths
        if (this.shouldSkipAuth(req.path, options.excludePaths || [])) {
          return next();
        }

        // Determine authentication strategy
        const strategy = this.detectAuthStrategy(req);
        
        // Authenticate based on strategy
        let user: User | null = null;
        let sessionId: string | undefined;

        switch (strategy) {
          case 'jwt':
            user = await this.authenticateJWT(req);
            break;
          case 'session':
            const sessionResult = await this.authenticateSession(req);
            user = sessionResult.user;
            sessionId = sessionResult.sessionId;
            break;
          case 'api-key':
            user = await this.authenticateApiKey(req);
            break;
          default:
            if (options.requireAuth !== false) {
              return this.sendUnauthorized(res, 'No valid authentication method found');
            }
        }

        // Check authentication requirement
        if (options.requireAuth !== false && !user) {
          return this.sendUnauthorized(res, 'Authentication required');
        }

        if (user) {
          // Check role requirements
          if (options.requiredRoles && !this.hasRequiredRoles(user, options.requiredRoles)) {
            return this.sendForbidden(res, 'Insufficient role permissions');
          }

          // Check permission requirements
          if (options.requiredPermissions && !this.hasRequiredPermissions(user, options.requiredPermissions)) {
            return this.sendForbidden(res, 'Insufficient permissions');
          }

          // Check MFA requirement
          if (options.requireMfa && sessionId) {
            const session = await this.sessionProvider.getSession(sessionId);
            if (session && !session.mfaVerified) {
              return this.sendUnauthorized(res, 'MFA verification required');
            }
          }

          // Update session activity
          if (sessionId) {
            await this.sessionProvider.updateSessionActivity(sessionId);
          }

          // Attach user to request
          (req as any).user = user;
          (req as any).sessionId = sessionId;
        }

        next();
      } catch (error) {
        console.error('Auth middleware error:', error);
        return this.sendUnauthorized(res, 'Authentication failed');
      }
    };
  }

  /**
   * Detect authentication strategy from request
   */
  private detectAuthStrategy(req: Request): AuthStrategy {
    // Check for API key in header
    if (req.headers['x-api-key'] || req.headers['authorization']?.startsWith('ApiKey ')) {
      return 'api-key';
    }

    // Check for JWT in Authorization header
    if (req.headers['authorization']?.startsWith('Bearer ')) {
      return 'jwt';
    }

    // Check for session cookie
    if (req.cookies && req.cookies[this.config.session.cookieName]) {
      return 'session';
    }

    return 'jwt'; // Default to JWT
  }

  /**
   * Authenticate using JWT
   */
  private async authenticateJWT(req: Request): Promise<User | null> {
    const authHeader = req.headers['authorization'];
    if (!authHeader || !authHeader.startsWith('Bearer ')) {
      return null;
    }

    const token = authHeader.substring(7);
    try {
      const payload = await this.jwtProvider.verifyToken(token);
      // Convert JWT payload to User object (implement based on your user service)
      return this.getUserFromJWTPayload(payload);
    } catch (error) {
      return null;
    }
  }

  /**
   * Authenticate using session
   */
  private async authenticateSession(req: Request): Promise<{ user: User | null; sessionId?: string }> {
    const sessionId = req.cookies?.[this.config.session.cookieName];
    if (!sessionId) {
      return { user: null };
    }

    try {
      const session = await this.sessionProvider.getSession(sessionId);
      if (!session) {
        return { user: null };
      }

      const user = await this.getUserById(session.userId);
      return { user, sessionId };
    } catch (error) {
      return { user: null };
    }
  }

  /**
   * Authenticate using API key
   */
  private async authenticateApiKey(req: Request): Promise<User | null> {
    let apiKey = req.headers['x-api-key'] as string;
    
    if (!apiKey) {
      const authHeader = req.headers['authorization'];
      if (authHeader?.startsWith('ApiKey ')) {
        apiKey = authHeader.substring(7);
      }
    }

    if (!apiKey) {
      return null;
    }

    try {
      const result = await this.apiKeyProvider.verifyApiKey(apiKey);
      return result?.user || null;
    } catch (error) {
      return null;
    }
  }

  /**
   * Check if path should skip authentication
   */
  private shouldSkipAuth(path: string, excludePaths: string[]): boolean {
    return excludePaths.some(excludePath => {
      if (excludePath.includes('*')) {
        const pattern = new RegExp(excludePath.replace(/\*/g, '.*'));
        return pattern.test(path);
      }
      return path === excludePath || path.startsWith(excludePath);
    });
  }

  /**
   * Check if user has required roles
   */
  private hasRequiredRoles(user: User, requiredRoles: string[]): boolean {
    const userRoles = user.roles.map(role => role.name);
    return requiredRoles.every(role => userRoles.includes(role));
  }

  /**
   * Check if user has required permissions
   */
  private hasRequiredPermissions(user: User, requiredPermissions: string[]): boolean {
    const userPermissions = user.permissions.map(p => `${p.resource}:${p.action}`);
    return requiredPermissions.every(permission => userPermissions.includes(permission));
  }

  /**
   * Send unauthorized response
   */
  private sendUnauthorized(res: Response, message: string): void {
    res.status(401).json({
      error: 'Unauthorized',
      message,
      code: 'AUTH_REQUIRED'
    });
  }

  /**
   * Send forbidden response
   */
  private sendForbidden(res: Response, message: string): void {
    res.status(403).json({
      error: 'Forbidden',
      message,
      code: 'INSUFFICIENT_PERMISSIONS'
    });
  }

  /**
   * Get user from JWT payload (implement based on your user service)
   */
  private async getUserFromJWTPayload(payload: any): Promise<User | null> {
    // Implementation depends on your user service
    throw new Error('getUserFromJWTPayload not implemented - integrate with user service');
  }

  /**
   * Get user by ID (implement based on your user service)
   */
  private async getUserById(userId: string): Promise<User | null> {
    // Implementation depends on your user service
    throw new Error('getUserById not implemented - integrate with user service');
  }
}

export default FastAPIAuthMiddleware;