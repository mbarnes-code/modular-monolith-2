// Route registration for auth service

import { FastifyInstance } from 'fastify';

export async function registerRoutes(fastify: FastifyInstance) {
  // Register authentication routes
  await fastify.register(require('./routes/auth'), { prefix: '/auth' });
  
  // Register user management routes
  await fastify.register(require('./routes/users'), { prefix: '/users' });
  
  // Register organization routes
  await fastify.register(require('./routes/organizations'), { prefix: '/organizations' });
  
  // Register OAuth2/OIDC routes
  await fastify.register(require('./routes/oauth2'), { prefix: '/oauth2' });
  
  // Register admin routes
  await fastify.register(require('./routes/admin'), { prefix: '/admin' });
}