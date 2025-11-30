// Main entry point for authentication service

import { createDefaultConfig, validateConfig } from '@modular-monolith/auth-core';
import Fastify from 'fastify';
import { config } from './config';
import { registerPlugins } from './plugins';
import { registerRoutes } from './routes';

async function start() {
  // Create and validate auth configuration
  const authConfig = createDefaultConfig();
  validateConfig(authConfig);

  // Create Fastify instance
  const fastify = Fastify({
    logger: {
      level: config.logLevel,
      transport: config.isDevelopment ? {
        target: 'pino-pretty',
        options: {
          translateTime: 'HH:MM:ss Z',
          ignore: 'pid,hostname',
        },
      } : undefined,
    },
  });

  try {
    // Register plugins
    await registerPlugins(fastify, authConfig);

    // Register routes
    await registerRoutes(fastify);

    // Start server
    const address = await fastify.listen({
      port: config.port,
      host: config.host,
    });

    fastify.log.info(`Auth service started at ${address}`);
    fastify.log.info(`API documentation available at ${address}/docs`);

  } catch (error) {
    fastify.log.error(error);
    process.exit(1);
  }
}

// Handle process signals
process.on('SIGINT', async () => {
  console.log('Received SIGINT, shutting down gracefully...');
  process.exit(0);
});

process.on('SIGTERM', async () => {
  console.log('Received SIGTERM, shutting down gracefully...');
  process.exit(0);
});

// Start the server
start();