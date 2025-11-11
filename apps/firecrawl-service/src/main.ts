/**
 * Firecrawl Service - NX Project Entry Point
 * This is the main entry point for the Firecrawl service in the NX monorepo
 */

import { logger } from '@firecrawl/core';
import { app } from './app';
import { environment } from './environments/environment';
import { shutdownOtel } from './otel';
import { nuqShutdown } from './services/worker/nuq';

const { port: PORT, host: HOST } = environment;

// Start the server
const server = app.listen(PORT, HOST, () => {
  logger.info(`🔥 Firecrawl Service is running on ${HOST}:${PORT}`);
});

// Graceful shutdown handlers
const exitHandler = async () => {
  logger.info("SIGTERM signal received: closing HTTP server");
  if (process.env.IS_KUBERNETES === "true") {
    // Account for GCE load balancer drain timeout
    logger.info("Waiting 60s for GCE load balancer drain timeout");
    await new Promise(resolve => setTimeout(resolve, 60000));
  }
  server.close(() => {
    logger.info("Server closed.");
    nuqShutdown().finally(() => {
      logger.info("NUQ shutdown complete");
      shutdownOtel().finally(() => {
        logger.info("OTEL shutdown");
        process.exit(0);
      });
    });
  });
};

process.on("SIGTERM", exitHandler);
process.on("SIGINT", exitHandler);