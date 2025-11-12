import express from 'express';
import { join } from 'path';
import { BlackArchManager } from './blackarch-manager';

const host = process.env.HOST ?? 'localhost';
const port = process.env.PORT ? Number(process.env.PORT) : 3000;

const app = express();
const blackArch = new BlackArchManager();

// Middleware
app.use(express.json());

// Serve static files from the blackarch directory
app.use('/blackarch', express.static(join(__dirname, '../blackarch')));

app.get('/', (req, res) => {
  const stats = blackArch.getStats();
  res.send({ 
    message: 'BlackArch Service API',
    description: 'BlackArch Linux penetration testing distribution service',
    stats,
    endpoints: {
      '/': 'Service information',
      '/stats': 'Repository statistics',
      '/packages': 'List all packages',
      '/packages/:name': 'Get package information',
      '/packages/search/:keyword': 'Search packages by keyword',
      '/groups': 'List tool groups',
      '/official': 'List official packages',
      '/broken': 'List broken packages',
      '/blackarch/*': 'Static files from BlackArch repository'
    }
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

app.get('/packages/:name', (req, res) => {
  try {
    const packageName = req.params.name;
    const packageInfo = blackArch.getPackageInfo(packageName);
    
    if (!packageInfo) {
      res.status(404).send({ error: 'Package not found' });
      return;
    }
    
    res.send(packageInfo);
  } catch (error) {
    res.status(500).send({ error: 'Failed to load package information' });
  }
});

app.get('/packages/search/:keyword', (req, res) => {
  try {
    const keyword = req.params.keyword;
    const packages = blackArch.searchPackages(keyword);
    
    res.send({ 
      keyword,
      packages,
      total: packages.length
    });
  } catch (error) {
    res.status(500).send({ error: 'Failed to search packages' });
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

app.get('/official', (req, res) => {
  try {
    const packages = blackArch.getOfficialPackages();
    res.send({ 
      packages,
      total: packages.length
    });
  } catch (error) {
    res.status(500).send({ error: 'Failed to load official packages' });
  }
});

app.get('/broken', (req, res) => {
  try {
    const packages = blackArch.getBrokenPackages();
    res.send({ 
      packages,
      total: packages.length
    });
  } catch (error) {
    res.status(500).send({ error: 'Failed to load broken packages' });
  }
});

app.listen(port, host, () => {
  console.log(`[ BlackArch Service ready ] http://${host}:${port}`);
});
