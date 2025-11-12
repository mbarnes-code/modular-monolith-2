import { Router } from 'express';
import { blackArchController } from '../controllers/blackarch.controller';

export const blackArchRouter = Router();

// Health check
blackArchRouter.get('/health', (req, res) => {
  res.json({ status: 'OK', timestamp: new Date().toISOString() });
});

// Statistics
blackArchRouter.get('/stats', blackArchController.getStats.bind(blackArchController));

// Packages
blackArchRouter.get('/packages', blackArchController.getAllPackages.bind(blackArchController));
blackArchRouter.get('/packages/search', blackArchController.searchPackages.bind(blackArchController));
blackArchRouter.get('/packages/:name', blackArchController.getPackage.bind(blackArchController));

// Groups
blackArchRouter.get('/groups', blackArchController.getGroups.bind(blackArchController));