import { NextFunction, Request, Response } from 'express';

export function errorHandler(
  err: any, 
  req: Request, 
  res: Response, 
  next: NextFunction
): void {
  console.error('Unhandled error:', err);
  res.status(500).json({
    success: false,
    message: 'Internal server error',
    error: process.env.NODE_ENV === 'development' ? err.message : 'Something went wrong'
  });
}

export function notFoundHandler(req: Request, res: Response): void {
  res.status(404).json({
    success: false,
    message: 'Endpoint not found',
    availableEndpoints: [
      'GET /',
      'GET /tools',
      'GET /tools/search?q={query}',
      'GET /tools/{name}',
      'POST /tools/{name}/install',
      'GET /categories',
      'GET /categories/{key}/tools',
      'GET /system',
      'GET /stats',
      'GET /health'
    ]
  });
}

export function requestLogger(req: Request, res: Response, next: NextFunction): void {
  const start = Date.now();
  const originalSend = res.send;
  
  res.send = function(body) {
    const duration = Date.now() - start;
    console.log(`${req.method} ${req.path} - ${res.statusCode} - ${duration}ms`);
    return originalSend.call(this, body);
  };
  
  next();
}