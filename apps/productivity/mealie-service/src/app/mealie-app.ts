import express = require('express');
import { HTTP_STATUS, MealieConfig } from '@mealie/shared';
import { promises as fs } from 'fs';
import path = require('path');

// Re-export for backward compatibility
export { MealieConfig };

/**
 * MealieApp - Main application class for Mealie service
 * 
 * Integrates the existing Mealie codebase into the Jane platform:
 * - Serves the Nuxt.js frontend (if enabled)
 * - Proxies API calls to the Python backend
 * - Provides integration endpoints for Jane orchestrator
 */
export class MealieApp {
  private app: express.Application;
  private config: MealieConfig;

  constructor(config: MealieConfig) {
    this.config = config;
    this.app = express();
    this.setupMiddleware();
    this.setupRoutes();
  }

  private setupMiddleware(): void {
    this.app.use(express.json());
    this.app.use(express.urlencoded({ extended: true }));
    
    // CORS for Jane platform integration
    this.app.use((req, res, next) => {
      res.header('Access-Control-Allow-Origin', '*');
      res.header('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,PATCH,OPTIONS');
      res.header('Access-Control-Allow-Headers', 'Content-Type, Authorization, Content-Length, X-Requested-With');
      
      if (req.method === 'OPTIONS') {
        res.sendStatus(200);
      } else {
        next();
      }
    });
  }

  private setupRoutes(): void {
    // Health check endpoint
    this.app.get('/health', (req, res) => {
      res.json({
        status: 'healthy',
        service: 'mealie-service',
        timestamp: new Date().toISOString(),
        version: '3.3.2'
      });
    });

    // Jane platform integration endpoints
    this.app.get('/api/jane/status', (req, res) => {
      res.json({
        service: 'mealie',
        status: 'active',
        features: {
          recipe_management: true,
          meal_planning: true,
          shopping_lists: true,
          recipe_import: true,
          nutritional_analysis: true
        },
        endpoints: {
          frontend: this.config.frontend.enabled ? `http://${this.config.host}:${this.config.port}` : null,
          api: `http://${this.config.host}:${this.config.port}/api`
        }
      });
    });

    // Serve frontend if enabled
    if (this.config.frontend.enabled) {
      this.setupFrontendRouting();
    }

    // API proxy routes (will be implemented to proxy to Python backend)
    this.app.use('/api', this.createApiProxy());
  }

  private async setupFrontendRouting(): Promise<void> {
    const frontendPath = path.resolve(this.config.frontend.path);
    
    try {
      await fs.access(frontendPath);
      this.app.use(express.static(frontendPath));
      
      // SPA fallback
      this.app.get('*', (req, res) => {
        if (!req.path.startsWith('/api')) {
          res.sendFile(path.join(frontendPath, 'index.html'));
        }
      });
    } catch (error) {
      console.warn(`Frontend path not found: ${frontendPath}. Frontend serving disabled.`);
    }
  }

  private createApiProxy(): express.Router {
    const router = express.Router();
    
    // TODO: Implement proxy to Python FastAPI backend
    // This will forward requests to the actual Mealie Python service
    
    router.use((req, res) => {
      res.status(HTTP_STATUS.NOT_IMPLEMENTED).json({
        error: 'API proxy not yet implemented',
        message: 'This endpoint will proxy to the Mealie Python backend',
        path: req.originalUrl,
        method: req.method
      });
    });

    return router;
  }

  async start(): Promise<void> {
    return new Promise((resolve) => {
      this.app.listen(this.config.port, this.config.host, () => {
        resolve();
      });
    });
  }

  getApp(): express.Application {
    return this.app;
  }
}