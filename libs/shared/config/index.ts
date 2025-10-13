// Configuration management for the monorepo
export interface AppConfig {
  apiUrl: string;
  environment: 'development' | 'production' | 'test';
}

export const defaultConfig: AppConfig = {
  apiUrl: process.env.API_URL || 'http://localhost:8000',
  environment: (process.env.NODE_ENV as AppConfig['environment']) || 'development',
};

export function getConfig(): AppConfig {
  return defaultConfig;
}
