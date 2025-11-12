import { Router } from 'express';
import { OnexService } from '../../lib';
import { CategoriesController } from '../controllers';

export function createCategoriesRoutes(): Router {
  const router = Router();
  const onexService = new OnexService();
  const categoriesController = new CategoriesController(onexService);

  // GET /categories - Get all categories
  router.get('/', categoriesController.getAllCategories.bind(categoriesController));

  // GET /categories/:key/tools - Get tools by category
  router.get('/:key/tools', categoriesController.getToolsByCategory.bind(categoriesController));

  return router;
}
