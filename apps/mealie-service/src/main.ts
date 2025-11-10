/**
 * Mealie Service - Recipe Management and Meal Planning
 * 
 * This service integrates Mealie functionality into the Jane platform:
 * - Recipe import and management
 * - Meal planning and shopping lists
 * - Recipe sharing and organization
 * - Nutritional analysis and dietary tracking
 */

import { MealieApp } from './app/mealie-app';
import { environment } from './environments/environment';

async function bootstrap() {
  const app = new MealieApp({
    port: environment.port,
    host: environment.host,
    database: environment.database,
    frontend: environment.frontend
  });

  await app.start();
  console.log(`Mealie Service started on ${environment.host}:${environment.port}`);
}

bootstrap().catch((error) => {
  console.error('Failed to start Mealie Service:', error);
  process.exit(1);
});