import { OnexService } from '@jane-monorepo/onex-core';
import cors from 'cors';
import express from 'express';
import { errorHandler, notFoundHandler, requestLogger } from './middleware';
import { createApiRoutes } from './routes';

export function createApp(): express.Application {
  const app = express();
  const onexService = new OnexService();

  // Basic middleware
  app.use(cors());
  app.use(express.json());
  app.use(requestLogger);

  // API routes
  app.use('/', createApiRoutes(onexService));

  // Error handling
  app.use('*', notFoundHandler);
  app.use(errorHandler);

  return app;
}

export function getOnexServiceInfo(): {
  toolsCount: number;
  categoriesCount: number;
  system: string;
  packageManager: string;
} {
  const onexService = new OnexService();
  const stats = onexService.getStats();
  const systemInfo = onexService.getSystemInfo();
  
  return {
    toolsCount: stats.toolsCount,
    categoriesCount: stats.categoriesCount,
    system: systemInfo.system,
    packageManager: systemInfo.packageManager
  };
}