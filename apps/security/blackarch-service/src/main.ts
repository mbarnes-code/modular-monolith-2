import express from 'express';
import cors from 'cors';
import { blackArchRouter } from './app/routes/blackarch.routes';
import { configService } from './app/config/config.service';

const app = express();

// Middleware
app.use(cors());
app.use(express.json());

// Logging middleware
if (!configService.isProduction) {
  app.use((req, res, next) => {
    console.log(`${new Date().toISOString()} ${req.method} ${req.path}`);
    next();
  });
}

// Routes
app.use('/api/blackarch', blackArchRouter);

// Root endpoint
app.get('/', (req, res) => {
  res.json({
    name: 'BlackArch Service',
    version: '1.0.0',
    description: 'BlackArch Linux repository API service',
    endpoints: [
      'GET /api/blackarch/health',
      'GET /api/blackarch/stats',
      'GET /api/blackarch/packages',
      'GET /api/blackarch/packages/search',
      'GET /api/blackarch/packages/:name',
      'GET /api/blackarch/groups'
    ]
  });
});

// Error handling middleware
app.use((err: Error, req: express.Request, res: express.Response, next: express.NextFunction) => {
  console.error('Error:', err);
  res.status(500).json({
    success: false,
    error: configService.isProduction ? 'Internal server error' : err.message
  });
});

// 404 handler
app.use((req, res) => {
  res.status(404).json({
    success: false,
    error: 'Not found'
  });
});

// Start server
const port = configService.port;
const host = configService.host;

app.listen(port, host, () => {
  console.log(`🚀 BlackArch Service running at http://${host}:${port}`);
  console.log(`📦 Environment: ${configService.isProduction ? 'production' : 'development'}`);
});

export default app;