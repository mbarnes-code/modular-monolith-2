import request from 'supertest';
import { createApp } from '../app';

describe('Brute Ratel Service API - Quick Tests', () => {
  const app = createApp();

  // Aggressive timeout for critical tests only
  jest.setTimeout(3000);

  describe('Core API', () => {
    it('should return service information quickly', async () => {
      const response = await request(app)
        .get('/api')
        .timeout(1000) // 1 second timeout
        .expect(200);

      expect(response.body).toHaveProperty('message', 'Brute Ratel C4 Community Kit Service');
      expect(response.body).toHaveProperty('endpoints');
    }, 1500); // 1.5 second Jest timeout

    it('should return toolkit info quickly', async () => {
      const response = await request(app)
        .get('/api/toolkit-info')
        .timeout(1000) // 1 second timeout
        .expect(200);

      expect(response.body).toHaveProperty('name', 'Brute Ratel C4 Community Kit');
      expect(Array.isArray(response.body.components)).toBe(true);
    }, 1500); // 1.5 second Jest timeout
  });
});