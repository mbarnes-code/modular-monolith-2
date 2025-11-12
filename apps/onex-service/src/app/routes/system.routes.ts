import { OnexService } from '@jane-monorepo/onex-core';
import { Router } from 'express';
import { SystemController } from '../controllers/system.controller';

export function createSystemRoutes(onexService: OnexService): Router {
  const router = Router();
  const systemController = new SystemController(onexService);

  // GET /system - Get system information
  router.get('/', (req, res) => systemController.getSystemInfo(req, res));
  
  // GET /stats - Get statistics
  router.get('/stats', (req, res) => systemController.getStats(req, res));
  
  // GET /health - Health check
  router.get('/health', (req, res) => systemController.getHealth(req, res));

  return router;
}