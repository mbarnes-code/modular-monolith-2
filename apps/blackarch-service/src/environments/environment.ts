export const environment = {
  production: false,
  port: process.env.PORT ? Number(process.env.PORT) : 3000,
  host: process.env.HOST ?? 'localhost',
  blackarch: {
    maxSearchResults: 1000,
    defaultPageSize: 50,
    repositoryPath: process.env.BLACKARCH_PATH
  },
  logging: {
    level: 'debug'
  }
};