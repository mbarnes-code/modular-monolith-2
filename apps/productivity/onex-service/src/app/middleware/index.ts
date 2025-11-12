import { NextFunction, Request, Response } from 'express';

export function errorHandler(err: any, req: Request, res: Response, next: NextFunction): void {
  console.error('Unhandled error:', err);
  
  // Don't send error details in production
  const isDevelopment = process.env.NODE_ENV === 'development';
  
  res.status(500).json({
    success: false,
    message: 'Internal server error',
    error: isDevelopment ? err.message : 'Something went wrong',
    timestamp: new Date().toISOString(),
    path: req.path
  });
}

export function notFoundHandler(req: Request, res: Response): void {
  res.status(404).json({
    success: false,
    message: 'Endpoint not found',
    path: req.path,
    method: req.method,
    availableEndpoints: [
      'GET /tools',
      'GET /tools/search?q={query}',
      'GET /tools/{name}',
      'POST /tools/{name}/install',
      'GET /categories',
      'GET /categories/{key}/tools',
      'GET /system',
      'GET /system/stats',
      'GET /system/health'
    ],
    timestamp: new Date().toISOString()
  });
}

export function requestLogger(req: Request, res: Response, next: NextFunction): void {
  const start = Date.now();
  
  res.on('finish', () => {
    const duration = Date.now() - start;
    console.log(`${req.method} ${req.path} - ${res.statusCode} (${duration}ms)`);
  });
  
  next();
}
