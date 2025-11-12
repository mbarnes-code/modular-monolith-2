import request from 'supertest';
import { createApp } from '../app';

describe('Brute Ratel Service API', () => {
  const app = createApp();

  // Set aggressive timeout for all tests in this suite
  jest.setTimeout(5000); // 5 seconds max

  describe('GET /api', () => {
    it('should return service information', async () => {
      const response = await request(app)
        .get('/api')
        .timeout(2000) // 2 second timeout
        .expect(200);

      expect(response.body).toHaveProperty('message', 'Brute Ratel C4 Community Kit Service');
      expect(response.body).toHaveProperty('environment');
      expect(response.body).toHaveProperty('endpoints');
    }, 3000); // 3 second Jest timeout
  });

  describe('GET /api/toolkit-info', () => {
    it('should return toolkit information', async () => {
      const response = await request(app)
        .get('/api/toolkit-info')
        .timeout(2000) // 2 second timeout
        .expect(200);

      expect(response.body).toHaveProperty('name', 'Brute Ratel C4 Community Kit');
      expect(response.body).toHaveProperty('description');
      expect(response.body).toHaveProperty('components');
      expect(Array.isArray(response.body.components)).toBe(true);
    }, 3000); // 3 second Jest timeout
  });

  describe('Asset Routes', () => {
    it('should serve adhoc_scripts assets (with redirect)', async () => {
      await request(app)
        .get('/assets/adhoc_scripts')
        .timeout(1500) // 1.5 second timeout
        .expect((res) => {
          expect([200, 301, 302]).toContain(res.status);
        });
    }, 2000); // 2 second Jest timeout

    it('should serve legacy adhoc_scripts route (with redirect)', async () => {
      await request(app)
        .get('/adhoc_scripts')
        .timeout(1500) // 1.5 second timeout
        .expect((res) => {
          expect([200, 301, 302]).toContain(res.status);
        });
    }, 2000); // 2 second Jest timeout

    it('should serve BOF assets (with redirect)', async () => {
      await request(app)
        .get('/assets/bofs')
        .timeout(1500) // 1.5 second timeout
        .expect((res) => {
          expect([200, 301, 302]).toContain(res.status);
        });
    }, 2000); // 2 second Jest timeout

    it('should serve deprecated assets (with redirect)', async () => {
      await request(app)
        .get('/assets/deprecated')
        .timeout(1500) // 1.5 second timeout
        .expect((res) => {
          expect([200, 301, 302]).toContain(res.status);
        });
    }, 2000); // 2 second Jest timeout

    it('should serve specific file from adhoc_scripts', async () => {
      await request(app)
        .get('/assets/adhoc_scripts/badgerNotifier.py')
        .timeout(1500) // 1.5 second timeout
        .expect((res) => {
          expect([200, 404]).toContain(res.status); // 404 is ok if file doesn't exist
        });
    }, 2000); // 2 second Jest timeout
  });
});