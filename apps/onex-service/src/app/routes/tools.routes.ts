import { OnexService } from '@jane-monorepo/onex-core';
import { Router } from 'express';
import { ToolsController } from '../controllers/tools.controller';

export function createToolsRoutes(onexService: OnexService): Router {
  const router = Router();
  const toolsController = new ToolsController(onexService);

  // GET /tools - Get all tools
  router.get('/', (req, res) => toolsController.getAllTools(req, res));
  
  // GET /tools/search - Search tools
  router.get('/search', (req, res) => toolsController.searchTools(req, res));
  
  // GET /tools/:name - Get specific tool
  router.get('/:name', (req, res) => toolsController.getToolByName(req, res));
  
  // POST /tools/:name/install - Install tool
  router.post('/:name/install', (req, res) => toolsController.installTool(req, res));

  return router;
}