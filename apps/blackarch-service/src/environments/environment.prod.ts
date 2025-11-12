export const environment = {
  production: true,
  port: process.env.PORT ? Number(process.env.PORT) : 3000,
  host: process.env.HOST ?? '0.0.0.0',
  blackarch: {
    maxSearchResults: 100,
    defaultPageSize: 20,
    repositoryPath: process.env.BLACKARCH_PATH ?? '/usr/share/blackarch'
  },
  logging: {
    level: 'info'
  }
};