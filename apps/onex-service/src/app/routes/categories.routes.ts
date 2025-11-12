import { OnexService } from '@jane-monorepo/onex-core';
import { Router } from 'express';
import { CategoriesController } from '../controllers/categories.controller';

export function createCategoriesRoutes(onexService: OnexService): Router {
  const router = Router();
  const categoriesController = new CategoriesController(onexService);

  // GET /categories - Get all categories
  router.get('/', (req, res) => categoriesController.getAllCategories(req, res));
  
  // GET /categories/:key/tools - Get tools by category
  router.get('/:key/tools', (req, res) => categoriesController.getToolsByCategory(req, res));

  return router;
}