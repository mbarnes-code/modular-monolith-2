import cors from 'cors';
import express from 'express';
import { errorHandler, notFoundHandler, requestLogger } from './middleware';
import { createApiRoutes } from './routes';

export function createApp(): express.Application {
  const app = express();

  // Core middleware
  app.use(cors());
  app.use(express.json());
  app.use(requestLogger);

  // Root endpoint
  app.get('/', (req, res) => {
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
        'GET /system/stats': 'Get statistics',
        'GET /system': 'Get system information',
        'GET /system/health': 'Health check'
      }
    });
  });

  // API routes
  app.use('/api', createApiRoutes());

  // Error handling middleware (must be last)
  app.use(notFoundHandler);
  app.use(errorHandler);

  return app;
}
