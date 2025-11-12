import request from 'supertest';
import app from './main';

describe('BlackArch Service API', () => {
  describe('GET /', () => {
    it('should return API information', async () => {
      const response = await request(app).get('/');
      
      expect(response.status).toBe(200);
      expect(response.body).toHaveProperty('name', 'BlackArch Service');
      expect(response.body).toHaveProperty('version', '1.0.0');
      expect(response.body).toHaveProperty('description');
      expect(response.body).toHaveProperty('endpoints');
      expect(Array.isArray(response.body.endpoints)).toBe(true);
    });
  });

  describe('GET /api/blackarch/health', () => {
    it('should return health status', async () => {
      const response = await request(app).get('/api/blackarch/health');
      
      expect(response.status).toBe(200);
      expect(response.body).toHaveProperty('status', 'OK');
      expect(response.body).toHaveProperty('timestamp');
    });
  });

  describe('GET /api/blackarch/stats', () => {
    it('should return repository statistics', async () => {
      const response = await request(app).get('/api/blackarch/stats');
      
      expect(response.status).toBe(200);
      expect(response.body).toHaveProperty('success', true);
      expect(response.body).toHaveProperty('data');
      expect(response.body.data).toHaveProperty('total');
      expect(response.body.data).toHaveProperty('official');
      expect(response.body.data).toHaveProperty('broken');
      expect(response.body.data).toHaveProperty('working');
    });
  });

  describe('GET /api/blackarch/packages', () => {
    it('should return paginated packages', async () => {
      const response = await request(app).get('/api/blackarch/packages');
      
      expect(response.status).toBe(200);
      expect(response.body).toHaveProperty('success', true);
      expect(response.body).toHaveProperty('data');
      expect(response.body).toHaveProperty('pagination');
      expect(Array.isArray(response.body.data)).toBe(true);
      expect(response.body.pagination).toHaveProperty('page');
      expect(response.body.pagination).toHaveProperty('limit');
      expect(response.body.pagination).toHaveProperty('total');
    });

    it('should accept pagination parameters', async () => {
      const response = await request(app)
        .get('/api/blackarch/packages')
        .query({ page: 2, limit: 5 });
      
      expect(response.status).toBe(200);
      expect(response.body.pagination.page).toBe(2);
      expect(response.body.pagination.limit).toBe(5);
    });

    it('should filter by group', async () => {
      const response = await request(app)
        .get('/api/blackarch/packages')
        .query({ group: 'blackarch-test' });
      
      expect(response.status).toBe(200);
      expect(response.body).toHaveProperty('success', true);
    });
  });

  describe('GET /api/blackarch/packages/search', () => {
    it('should search packages', async () => {
      const response = await request(app)
        .get('/api/blackarch/packages/search')
        .query({ q: 'test' });
      
      expect(response.status).toBe(200);
      expect(response.body).toHaveProperty('success', true);
      expect(response.body).toHaveProperty('data');
      expect(response.body).toHaveProperty('pagination');
      expect(Array.isArray(response.body.data)).toBe(true);
    });

    it('should return 400 for missing query', async () => {
      const response = await request(app).get('/api/blackarch/packages/search');
      
      expect(response.status).toBe(400);
      expect(response.body).toHaveProperty('success', false);
      expect(response.body).toHaveProperty('error');
    });
  });

  describe('GET /api/blackarch/groups', () => {
    it('should return list of groups', async () => {
      const response = await request(app).get('/api/blackarch/groups');
      
      expect(response.status).toBe(200);
      expect(response.body).toHaveProperty('success', true);
      expect(response.body).toHaveProperty('data');
      expect(Array.isArray(response.body.data)).toBe(true);
    });
  });

  describe('404 handler', () => {
    it('should return 404 for unknown routes', async () => {
      const response = await request(app).get('/unknown-route');
      
      expect(response.status).toBe(404);
      expect(response.body).toHaveProperty('success', false);
      expect(response.body).toHaveProperty('error', 'Not found');
    });
  });
});