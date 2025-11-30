// Configuration for authentication system

export interface AuthConfig {
  jwt: {
    secret: string;
    refreshSecret: string;
    issuer: string;
    audience: string;
    accessTokenExpiry: number; // seconds
    refreshTokenExpiry: number; // seconds
  };
  redis: {
    url: string;
    password?: string;
    database?: number;
    keyPrefix: string;
  };
  apiKey: {
    keyPrefix: string;
    hashSalt: string;
  };
  security: {
    bcryptRounds: number;
    maxLoginAttempts: number;
    lockoutDuration: number; // seconds
  };
  session: {
    cookieName: string;
    secure: boolean;
    sameSite: 'strict' | 'lax' | 'none';
    httpOnly: boolean;
  };
}

/**
 * Create default configuration
 */
export function createDefaultConfig(): AuthConfig {
  return {
    jwt: {
      secret: process.env.JWT_SECRET || 'default-jwt-secret-change-in-production',
      refreshSecret: process.env.JWT_REFRESH_SECRET || 'default-refresh-secret-change-in-production',
      issuer: process.env.JWT_ISSUER || 'modular-monolith-auth',
      audience: process.env.JWT_AUDIENCE || 'modular-monolith',
      accessTokenExpiry: parseInt(process.env.JWT_ACCESS_EXPIRY || '3600'), // 1 hour
      refreshTokenExpiry: parseInt(process.env.JWT_REFRESH_EXPIRY || '604800'), // 7 days
    },
    redis: {
      url: process.env.REDIS_URL || 'redis://localhost:6379',
      password: process.env.REDIS_PASSWORD,
      database: parseInt(process.env.REDIS_DATABASE || '0'),
      keyPrefix: process.env.REDIS_KEY_PREFIX || 'mm-auth',
    },
    apiKey: {
      keyPrefix: process.env.API_KEY_PREFIX || 'mm',
      hashSalt: process.env.API_KEY_SALT || 'default-salt-change-in-production',
    },
    security: {
      bcryptRounds: parseInt(process.env.BCRYPT_ROUNDS || '12'),
      maxLoginAttempts: parseInt(process.env.MAX_LOGIN_ATTEMPTS || '5'),
      lockoutDuration: parseInt(process.env.LOCKOUT_DURATION || '900'), // 15 minutes
    },
    session: {
      cookieName: process.env.SESSION_COOKIE_NAME || 'mm-session',
      secure: process.env.NODE_ENV === 'production',
      sameSite: (process.env.COOKIE_SAMESITE as any) || 'lax',
      httpOnly: true,
    },
  };
}

/**
 * Validate configuration
 */
export function validateConfig(config: AuthConfig): void {
  if (!config.jwt.secret || config.jwt.secret === 'default-jwt-secret-change-in-production') {
    throw new Error('JWT_SECRET must be set in production');
  }
  
  if (!config.jwt.refreshSecret || config.jwt.refreshSecret === 'default-refresh-secret-change-in-production') {
    throw new Error('JWT_REFRESH_SECRET must be set in production');
  }
  
  if (!config.apiKey.hashSalt || config.apiKey.hashSalt === 'default-salt-change-in-production') {
    throw new Error('API_KEY_SALT must be set in production');
  }
  
  if (config.security.bcryptRounds < 10) {
    throw new Error('BCRYPT_ROUNDS should be at least 10 for security');
  }
}