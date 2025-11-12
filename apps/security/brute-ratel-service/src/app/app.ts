/**
 * Brute Ratel C4 Community Kit Application
 */
import express from 'express';
import * as path from 'path';
import { environment } from '../environments/environment';

export function createApp() {
  const app = express();

  // Middleware
  app.use(express.json());
  app.use(express.static(path.join(__dirname, '..', 'assets')));

  // Serve toolkit assets
  app.use('/assets/adhoc_scripts', express.static(path.join(__dirname, '..', 'assets', 'adhoc_scripts')));
  app.use('/assets/bofs', express.static(path.join(__dirname, '..', 'assets', 'bofs')));
  app.use('/assets/deprecated', express.static(path.join(__dirname, '..', 'assets', 'deprecated')));
  app.use('/assets/patch_envexit', express.static(path.join(__dirname, '..', 'assets', 'patch_envexit')));

  // Legacy compatibility routes
  app.use('/adhoc_scripts', express.static(path.join(__dirname, '..', 'assets', 'adhoc_scripts')));
  app.use('/bofs', express.static(path.join(__dirname, '..', 'assets', 'bofs')));
  app.use('/deprecated', express.static(path.join(__dirname, '..', 'assets', 'deprecated')));
  app.use('/patch_envexit', express.static(path.join(__dirname, '..', 'assets', 'patch_envexit')));

  // API Routes
  app.get('/api', (req, res) => {
    res.json({ 
      message: 'Brute Ratel C4 Community Kit Service',
      environment: environment.name,
      endpoints: {
        adhoc_scripts: '/assets/adhoc_scripts',
        bofs: '/assets/bofs',
        deprecated: '/assets/deprecated',
        patch_envexit: '/assets/patch_envexit',
        toolkit_info: '/api/toolkit-info'
      }
    });
  });

  app.get('/api/toolkit-info', (req, res) => {
    res.json({
      name: 'Brute Ratel C4 Community Kit',
      description: 'Security toolkit containing scripts, BOFs, and utilities for Brute Ratel C4',
      components: [
        'Adhoc Scripts (Python, Shell)',
        'Beacon Object Files (BOFs)',
        'Deprecated Payloads',
        'Patch Environment Exit Utilities'
      ]
    });
  });

  return app;
}

export function startServer(port = 3333) {
  const app = createApp();
  const server = app.listen(port, () => {
    console.log(`🚀 Brute Ratel C4 Community Kit Service running at http://localhost:${port}`);
    console.log(`📚 API Documentation: http://localhost:${port}/api`);
    if (!environment.production) {
      console.log(`🔧 Environment: ${environment.name}`);
    }
  });

  server.on('error', console.error);
  return server;
}