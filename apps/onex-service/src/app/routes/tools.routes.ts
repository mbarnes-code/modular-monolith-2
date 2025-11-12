import { Router } from 'express';
import { OnexService } from '../../lib';
import { ToolsController } from '../controllers';

export function createToolsRoutes(): Router {
  const router = Router();
  const onexService = new OnexService();
  const toolsController = new ToolsController(onexService);

  // GET /tools - Get all tools
  router.get('/', toolsController.getAllTools.bind(toolsController));

  // GET /tools/search?q={query} - Search tools
  router.get('/search', toolsController.searchTools.bind(toolsController));

  // GET /tools/:name - Get specific tool
  router.get('/:name', toolsController.getToolByName.bind(toolsController));

  // POST /tools/:name/install - Install tool
  router.post('/:name/install', toolsController.installTool.bind(toolsController));

  return router;
}
