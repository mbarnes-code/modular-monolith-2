export const environment = {
  production: true,
  port: process.env.PORT || 3002,
  host: process.env.HOST || '0.0.0.0',
  
  // Database Configuration
  supabaseUrl: process.env.SUPABASE_URL,
  supabaseServiceToken: process.env.SUPABASE_SERVICE_TOKEN,
  
  // Redis Configuration
  redisUrl: process.env.REDIS_URL || 'redis://localhost:6379',
  
  // Authentication
  authSecret: process.env.AUTH_SECRET,
  
  // External APIs
  openaiApiKey: process.env.OPENAI_API_KEY,
  anthropicApiKey: process.env.ANTHROPIC_API_KEY,
  
  // Monitoring
  sentryDsn: process.env.SENTRY_DSN,
  
  // Feature Flags
  features: {
    enableBullBoard: false, // Disabled in production
    enableMetrics: true,
    enableDebugLogging: false,
  }
};