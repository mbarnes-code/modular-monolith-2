import { MealieApp } from './mealie-app';

describe('MealieApp', () => {
  let app: MealieApp;
  
  beforeEach(() => {
    app = new MealieApp({
      port: 9925,
      host: 'localhost',
      database: {
        url: 'postgresql://test:test@localhost:5432/mealie_test',
        type: 'postgresql'
      },
      frontend: {
        enabled: false,
        path: './frontend/dist',
        api_url: 'http://localhost:9925'
      }
    });
  });

  it('should create an instance', () => {
    expect(app).toBeDefined();
  });

  it('should have express app instance', () => {
    expect(app.getApp()).toBeDefined();
  });
});