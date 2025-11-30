// Plugin registration for auth service

import { AuthConfig } from '@modular-monolith/auth-core';
import { FastifyInstance } from 'fastify';
import { config } from './config';

export async function registerPlugins(fastify: FastifyInstance, authConfig: AuthConfig) {
  // Register Helmet for security headers
  await fastify.register(require('@fastify/helmet'), {
    contentSecurityPolicy: config.isDevelopment ? false : undefined,
  });

  // Register CORS
  await fastify.register(require('@fastify/cors'), {
    origin: config.cors.origin,
    credentials: config.cors.credentials,
  });

  // Register rate limiting
  await fastify.register(require('@fastify/rate-limit'), {
    max: config.rateLimit.max,
    timeWindow: config.rateLimit.timeWindow,
  });

  // Register Redis
  await fastify.register(require('@fastify/redis'), {
    host: new URL(config.redis.url).hostname,
    port: parseInt(new URL(config.redis.url).port) || 6379,
    password: config.redis.password,
    db: config.redis.database,
  });

  // Register cookies
  await fastify.register(require('@fastify/cookie'), {
    secret: authConfig.jwt.secret,
    parseOptions: {
      httpOnly: true,
      secure: !config.isDevelopment,
      sameSite: 'lax',
    },
  });

  // Register JWT
  await fastify.register(require('@fastify/jwt'), {
    secret: authConfig.jwt.secret,
  });

  // Register Swagger for API documentation
  if (config.isDevelopment) {
    await fastify.register(require('@fastify/swagger'), {
      swagger: {
        info: {
          title: 'Auth Service API',
          description: 'Central authentication service for modular monolith',
          version: '1.0.0',
        },
        host: `localhost:${config.port}`,
        schemes: ['http', 'https'],
        consumes: ['application/json'],
        produces: ['application/json'],
        securityDefinitions: {
          Bearer: {
            type: 'apiKey',
            name: 'Authorization',
            in: 'header',
          },
        },
      },
    });

    await fastify.register(require('@fastify/swagger-ui'), {
      routePrefix: '/docs',
      uiConfig: {
        docExpansion: 'list',
        deepLinking: false,
      },
    });
  }

  // Add custom properties to fastify instance
  fastify.decorate('authConfig', authConfig);

  // Health check endpoint
  fastify.get('/health', async () => {
    return { 
      status: 'healthy',
      timestamp: new Date().toISOString(),
      version: '1.0.0',
    };
  });
}