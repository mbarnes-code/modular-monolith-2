// Configuration for auth service

export interface Config {
  port: number;
  host: string;
  isDevelopment: boolean;
  logLevel: string;
  database: {
    url: string;
    maxConnections: number;
  };
  redis: {
    url: string;
    password?: string;
    database: number;
  };
  cors: {
    origin: string[];
    credentials: boolean;
  };
  rateLimit: {
    max: number;
    timeWindow: number;
  };
  email: {
    host: string;
    port: number;
    user: string;
    password: string;
    from: string;
  };
}

export const config: Config = {
  port: parseInt(process.env.PORT || '3001'),
  host: process.env.HOST || '0.0.0.0',
  isDevelopment: process.env.NODE_ENV !== 'production',
  logLevel: process.env.LOG_LEVEL || 'info',
  
  database: {
    url: process.env.DATABASE_URL || 'postgresql://localhost:5432/auth_service',
    maxConnections: parseInt(process.env.DB_MAX_CONNECTIONS || '10'),
  },
  
  redis: {
    url: process.env.REDIS_URL || 'redis://localhost:6379',
    password: process.env.REDIS_PASSWORD,
    database: parseInt(process.env.REDIS_DATABASE || '0'),
  },
  
  cors: {
    origin: process.env.CORS_ORIGIN?.split(',') || ['http://localhost:3000'],
    credentials: true,
  },
  
  rateLimit: {
    max: parseInt(process.env.RATE_LIMIT_MAX || '100'),
    timeWindow: parseInt(process.env.RATE_LIMIT_WINDOW || '60000'), // 1 minute
  },
  
  email: {
    host: process.env.EMAIL_HOST || 'localhost',
    port: parseInt(process.env.EMAIL_PORT || '587'),
    user: process.env.EMAIL_USER || '',
    password: process.env.EMAIL_PASSWORD || '',
    from: process.env.EMAIL_FROM || 'noreply@modular-monolith.com',
  },
};