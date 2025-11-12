import { Router } from 'express';
import { OnexService } from '../../lib';
import { SystemController } from '../controllers';

export function createSystemRoutes(): Router {
  const router = Router();
  const onexService = new OnexService();
  const systemController = new SystemController(onexService);

  // GET /system - Get system information
  router.get('/', systemController.getSystemInfo.bind(systemController));

  // GET /stats - Get statistics
  router.get('/stats', systemController.getStats.bind(systemController));

  // GET /health - Health check
  router.get('/health', systemController.healthCheck.bind(systemController));

  return router;
}
