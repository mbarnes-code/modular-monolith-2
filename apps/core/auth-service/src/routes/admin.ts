// Admin routes

import { FastifyInstance } from 'fastify';

export default async function adminRoutes(fastify: FastifyInstance) {
  // Get all users (admin only)
  fastify.get('/users', {
    schema: {
      tags: ['Admin'],
      description: 'Get all users (admin only)',
      security: [{ Bearer: [] }],
    },
  }, async (request, reply) => {
    // Implementation placeholder
    return { message: 'Admin routes not yet implemented' };
  });
}