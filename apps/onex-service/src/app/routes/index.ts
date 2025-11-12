import { Router } from 'express';
import { createCategoriesRoutes } from './categories.routes';
import { createSystemRoutes } from './system.routes';
import { createToolsRoutes } from './tools.routes';

export function createApiRoutes(): Router {
  const router = Router();

  // Mount route groups
  router.use('/tools', createToolsRoutes());
  router.use('/categories', createCategoriesRoutes());
  router.use('/system', createSystemRoutes());

  return router;
}

// Barrel exports
export * from './categories.routes';
export * from './system.routes';
export * from './tools.routes';

