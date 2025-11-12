import { OnexService } from '@jane-monorepo/onex-core';
import { Router } from 'express';
import { createCategoriesRoutes } from './categories.routes';
import { createSystemRoutes } from './system.routes';
import { createToolsRoutes } from './tools.routes';

export function createApiRoutes(onexService: OnexService): Router {
  const router = Router();

  // Root endpoint with API documentation
  router.get('/', (req, res) => {
    res.json({ 
      message: 'Onex Hacking Tools Library API',
      version: '1.0.0',
      description: 'API for managing and installing hacking tools',
      endpoints: {
        'GET /': 'This help message',
        'GET /tools': 'Get all tools',
        'GET /tools/search?q={query}': 'Search tools by name',
        'GET /tools/{name}': 'Get specific tool by name',
        'POST /tools/{name}/install': 'Install a tool',
        'GET /categories': 'Get all categories',
        'GET /categories/{key}/tools': 'Get tools by category',
        'GET /system': 'Get system information',
        'GET /stats': 'Get statistics',
        'GET /health': 'Health check'
      }
    });
  });

  // Mount sub-routes
  router.use('/tools', createToolsRoutes(onexService));
  router.use('/categories', createCategoriesRoutes(onexService));
  router.use('/system', createSystemRoutes(onexService));
  
  // Also mount stats and health at root level for backward compatibility
  const systemController = createSystemRoutes(onexService);
  router.get('/stats', (req, res, next) => {
    req.url = '/stats';
    systemController(req, res, next);
  });
  router.get('/health', (req, res, next) => {
    req.url = '/health';
    systemController(req, res, next);
  });

  return router;
}