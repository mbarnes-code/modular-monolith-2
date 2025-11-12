import express from 'express';
import { join } from 'path';
import request from 'supertest';
import { BlackArchManager } from '../src/blackarch-manager';

// Import the main app setup
import '../src/main';

describe('BlackArch Service API', () => {
  let app: express.Application;
  let blackArch: BlackArchManager;

  beforeAll(() => {
    app = express();
    blackArch = new BlackArchManager();
    
    // Set up the same routes as in main.ts for testing
    app.use(express.json());
    app.use('/blackarch', express.static(join(__dirname, '../blackarch')));

    app.get('/', (req, res) => {
      const stats = blackArch.getStats();
      res.send({ 
        message: 'BlackArch Service API',
        description: 'BlackArch Linux penetration testing distribution service',
        stats
      });
    });

    app.get('/stats', (req, res) => {
      try {
        const stats = blackArch.getStats();
        res.send(stats);
      } catch (error) {
        res.status(500).send({ error: 'Failed to load statistics' });
      }
    });

    app.get('/groups', (req, res) => {
      try {
        const groups = blackArch.getToolGroups();
        res.send({ 
          groups,
          total: groups.length
        });
      } catch (error) {
        res.status(500).send({ error: 'Failed to load groups' });
      }
    });

    app.get('/packages', (req, res) => {
      try {
        const packages = blackArch.getAllPackages();
        const limit = req.query.limit ? parseInt(req.query.limit as string) : 50;
        const offset = req.query.offset ? parseInt(req.query.offset as string) : 0;
        
        const paginatedPackages = packages.slice(offset, offset + limit);
        
        res.send({ 
          packages: paginatedPackages,
          total: packages.length,
          limit,
          offset,
          hasMore: offset + limit < packages.length
        });
      } catch (error) {
        res.status(500).send({ error: 'Failed to load packages' });
      }
    });
  });

  describe('GET /', () => {
    it('should return service information', async () => {
      const response = await request(app)
        .get('/')
        .expect(200);

      expect(response.body.message).toBe('BlackArch Service API');
      expect(response.body.description).toContain('BlackArch Linux');
      expect(response.body.stats).toBeDefined();
      expect(response.body.stats.totalPackages).toBeGreaterThan(0);
    });
  });

  describe('GET /stats', () => {
    it('should return repository statistics', async () => {
      const response = await request(app)
        .get('/stats')
        .expect(200);

      expect(response.body.totalPackages).toBeGreaterThan(0);
      expect(response.body.totalGroups).toBeGreaterThan(0);
      expect(response.body.repositoryPath).toContain('blackarch');
    });
  });

  describe('GET /groups', () => {
    it('should return tool groups', async () => {
      const response = await request(app)
        .get('/groups')
        .expect(200);

      expect(Array.isArray(response.body.groups)).toBe(true);
      expect(response.body.total).toBeGreaterThan(0);
      expect(response.body.groups.length).toBe(response.body.total);
    });
  });

  describe('GET /packages', () => {
    it('should return paginated packages', async () => {
      const response = await request(app)
        .get('/packages')
        .expect(200);

      expect(Array.isArray(response.body.packages)).toBe(true);
      expect(response.body.total).toBeGreaterThan(0);
      expect(response.body.limit).toBe(50); // default limit
      expect(response.body.offset).toBe(0); // default offset
      expect(response.body.packages.length).toBeLessThanOrEqual(50);
    });

    it('should handle pagination parameters', async () => {
      const response = await request(app)
        .get('/packages?limit=10&offset=5')
        .expect(200);

      expect(response.body.limit).toBe(10);
      expect(response.body.offset).toBe(5);
      expect(response.body.packages.length).toBeLessThanOrEqual(10);
    });
  });
});