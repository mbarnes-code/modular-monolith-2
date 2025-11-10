import { DEFAULT_PATHS, DEFAULT_PORTS } from '@mealie/shared';

export const environment = {
  production: false,
  host: process.env.MEALIE_HOST || '0.0.0.0',
  port: parseInt(process.env.MEALIE_PORT || DEFAULT_PORTS.INTEGRATION_SERVICE.toString()),
  database: {
    url: process.env.DATABASE_URL || 'postgresql://postgres:postgres@localhost:5432/mealie_dev',
    type: 'postgresql' as const
  },
  frontend: {
    enabled: process.env.MEALIE_FRONTEND_ENABLED !== 'false',
    path: process.env.MEALIE_FRONTEND_PATH || DEFAULT_PATHS.WEB_OUTPUT,
    api_url: process.env.MEALIE_API_URL || `http://localhost:${DEFAULT_PORTS.INTEGRATION_SERVICE}`
  },
  auth: {
    secret: process.env.JWT_SECRET || 'mealie-dev-secret-key',
    algorithm: 'HS256' as const,
    expires_in: '24h'
  },
  storage: {
    data_dir: process.env.DATA_DIR || DEFAULT_PATHS.DATA_DIR,
    backup_dir: process.env.BACKUP_DIR || DEFAULT_PATHS.BACKUP_DIR
  },
  features: {
    allow_signup: process.env.ALLOW_SIGNUP !== 'false',
    allow_group_self_join: process.env.ALLOW_GROUP_SELF_JOIN === 'true',
    max_group_size: parseInt(process.env.MAX_GROUP_SIZE || '50'),
    max_file_size: process.env.MAX_FILE_SIZE || '100MB'
  }
};