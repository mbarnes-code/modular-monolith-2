// Configuration validation schemas using Joi

import Joi from 'joi';

export const environmentSchema = Joi.object({
  name: Joi.string().valid('development', 'staging', 'production').required(),
  debug: Joi.boolean().default(false),
  logLevel: Joi.string().valid('error', 'warn', 'info', 'debug').default('info'),
});

export const jwtConfigSchema = Joi.object({
  issuer: Joi.string().uri().required(),
  audience: Joi.string().required(),
  algorithm: Joi.string().valid('HS256', 'RS256', 'ES256').default('HS256'),
  publicKey: Joi.string().when('algorithm', {
    is: Joi.string().valid('RS256', 'ES256'),
    then: Joi.required(),
    otherwise: Joi.optional(),
  }),
  privateKey: Joi.string().when('algorithm', {
    is: Joi.string().valid('RS256', 'ES256'),
    then: Joi.required(),
    otherwise: Joi.optional(),
  }),
  accessTokenTTL: Joi.number().integer().min(300).max(86400).default(3600), // 5min to 24h
  refreshTokenTTL: Joi.number().integer().min(86400).max(2592000).default(604800), // 1day to 30days
  clockTolerance: Joi.number().integer().min(0).max(300).default(30), // up to 5min
});

export const redisClusterConfigSchema = Joi.object({
  host: Joi.string().hostname().required(),
  port: Joi.number().port().default(6379),
  password: Joi.string().optional(),
  database: Joi.number().integer().min(0).max(15).default(0),
});

export const redisConfigSchema = Joi.object({
  cluster: Joi.array().items(redisClusterConfigSchema).min(1).required(),
  keyPrefix: Joi.string().default('mm-auth'),
  ttl: Joi.object({
    session: Joi.number().integer().min(300).default(28800), // 5min to default 8h
    tokenBlacklist: Joi.number().integer().min(300).default(86400), // 5min to default 24h
    rateLimitWindow: Joi.number().integer().min(60).default(900), // 1min to default 15min
  }).default(),
});

export const databaseConnectionSchema = Joi.object({
  host: Joi.string().hostname().required(),
  port: Joi.number().port().default(5432),
  database: Joi.string().required(),
  username: Joi.string().required(),
  password: Joi.string().required(),
  ssl: Joi.boolean().default(false),
});

export const databaseConfigSchema = Joi.object({
  primary: databaseConnectionSchema.required(),
  replicas: Joi.array().items(databaseConnectionSchema).optional(),
  pool: Joi.object({
    min: Joi.number().integer().min(1).default(2),
    max: Joi.number().integer().min(2).default(20),
    idleTimeout: Joi.number().integer().min(1000).default(30000),
  }).default(),
});

export const passwordPolicyConfigSchema = Joi.object({
  minLength: Joi.number().integer().min(4).max(128).default(8),
  maxLength: Joi.number().integer().min(8).max(256).default(128),
  requireUppercase: Joi.boolean().default(true),
  requireLowercase: Joi.boolean().default(true),
  requireNumbers: Joi.boolean().default(true),
  requireSpecialChars: Joi.boolean().default(true),
  preventReuse: Joi.number().integer().min(0).max(24).default(5),
  maxAge: Joi.number().integer().min(30).max(365).default(90), // 30 days to 1 year
  bcryptRounds: Joi.number().integer().min(8).max(15).default(12),
});

export const rateLimitingConfigSchema = Joi.object({
  login: Joi.object({
    maxAttempts: Joi.number().integer().min(3).max(20).default(5),
    windowMs: Joi.number().integer().min(60000).default(900000), // 1min to default 15min
    blockDuration: Joi.number().integer().min(300000).default(900000), // 5min to default 15min
  }).default(),
  api: Joi.object({
    maxRequests: Joi.number().integer().min(10).max(10000).default(100),
    windowMs: Joi.number().integer().min(1000).default(60000), // 1sec to default 1min
  }).default(),
  passwordReset: Joi.object({
    maxAttempts: Joi.number().integer().min(1).max(10).default(3),
    windowMs: Joi.number().integer().min(300000).default(3600000), // 5min to default 1hour
  }).default(),
});

export const corsConfigSchema = Joi.object({
  allowedOrigins: Joi.array().items(Joi.string().uri()).required(),
  allowedMethods: Joi.array().items(Joi.string()).default(['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS']),
  allowedHeaders: Joi.array().items(Joi.string()).default(['Authorization', 'Content-Type', 'X-Requested-With']),
  credentials: Joi.boolean().default(true),
  maxAge: Joi.number().integer().min(0).default(86400), // 24 hours
});

export const securityConfigSchema = Joi.object({
  passwordPolicy: passwordPolicyConfigSchema.default(),
  rateLimiting: rateLimitingConfigSchema.default(),
  csrf: Joi.object({
    enabled: Joi.boolean().default(true),
    tokenLength: Joi.number().integer().min(16).max(64).default(32),
    cookieName: Joi.string().default('_csrf'),
    headerName: Joi.string().default('X-CSRF-Token'),
  }).default(),
  cors: corsConfigSchema.required(),
  encryption: Joi.object({
    algorithm: Joi.string().default('aes-256-gcm'),
    keySize: Joi.number().integer().default(32),
    ivSize: Joi.number().integer().default(16),
    saltRounds: Joi.number().integer().min(8).max(15).default(12),
  }).default(),
});

export const oauth2ProviderConfigSchema = Joi.object({
  clientId: Joi.string().required(),
  clientSecret: Joi.string().required(),
  authorizeUrl: Joi.string().uri().required(),
  tokenUrl: Joi.string().uri().required(),
  userInfoUrl: Joi.string().uri().optional(),
  scope: Joi.array().items(Joi.string()).default(['openid', 'profile', 'email']),
  redirectUri: Joi.string().uri().required(),
  additionalParams: Joi.object().pattern(Joi.string(), Joi.string()).optional(),
});

export const samlProviderConfigSchema = Joi.object({
  entityId: Joi.string().required(),
  ssoUrl: Joi.string().uri().required(),
  certificate: Joi.string().required(),
  attributeMapping: Joi.object({
    email: Joi.string().required(),
    firstName: Joi.string().optional(),
    lastName: Joi.string().optional(),
    groups: Joi.string().optional(),
  }).required(),
  signRequests: Joi.boolean().default(false),
  wantAssertionsSigned: Joi.boolean().default(true),
});

export const ldapProviderConfigSchema = Joi.object({
  url: Joi.string().uri({ scheme: ['ldap', 'ldaps'] }).required(),
  bindDN: Joi.string().required(),
  bindPassword: Joi.string().required(),
  searchBase: Joi.string().required(),
  searchFilter: Joi.string().required(),
  attributes: Joi.object({
    email: Joi.string().required(),
    firstName: Joi.string().optional(),
    lastName: Joi.string().optional(),
    groups: Joi.string().optional(),
  }).required(),
  tlsOptions: Joi.object({
    rejectUnauthorized: Joi.boolean().default(true),
    ca: Joi.array().items(Joi.string()).optional(),
  }).optional(),
});

export const oidcProviderConfigSchema = Joi.object({
  issuer: Joi.string().uri().required(),
  clientId: Joi.string().required(),
  clientSecret: Joi.string().required(),
  scope: Joi.array().items(Joi.string()).default(['openid', 'profile', 'email']),
  redirectUri: Joi.string().uri().required(),
  responseType: Joi.string().default('code'),
  additionalParams: Joi.object().pattern(Joi.string(), Joi.string()).optional(),
});

export const authProviderConfigSchema = Joi.object({
  id: Joi.string().required(),
  name: Joi.string().required(),
  type: Joi.string().valid('local', 'oauth2', 'saml', 'ldap', 'oidc').required(),
  enabled: Joi.boolean().default(true),
  organizationIds: Joi.array().items(Joi.string()).optional(),
  config: Joi.when('type', {
    switch: [
      { is: 'oauth2', then: oauth2ProviderConfigSchema },
      { is: 'saml', then: samlProviderConfigSchema },
      { is: 'ldap', then: ldapProviderConfigSchema },
      { is: 'oidc', then: oidcProviderConfigSchema },
      { is: 'local', then: Joi.object() },
    ],
  }),
  displayName: Joi.string().required(),
  icon: Joi.string().optional(),
  order: Joi.number().integer().min(0).default(0),
});

export const organizationSettingsSchema = Joi.object({
  passwordPolicy: passwordPolicyConfigSchema.optional(),
  sessionTimeout: Joi.number().integer().min(300).max(86400).default(28800), // 5min to 24h, default 8h
  maxConcurrentSessions: Joi.number().integer().min(1).max(100).default(5),
  mfaRequired: Joi.boolean().default(false),
  ssoEnabled: Joi.boolean().default(false),
  allowedEmailDomains: Joi.array().items(Joi.string().domain()).default([]),
  customFields: Joi.object().pattern(Joi.string(), Joi.any()).default({}),
});

export const organizationConfigSchema = Joi.object({
  id: Joi.string().required(),
  name: Joi.string().required(),
  slug: Joi.string().pattern(/^[a-z0-9-]+$/).required(),
  domain: Joi.string().domain().optional(),
  settings: organizationSettingsSchema.required(),
});

export const serviceConfigSchema = Joi.object({
  name: Joi.string().required(),
  clientId: Joi.string().required(),
  clientSecret: Joi.string().required(),
  redirectUris: Joi.array().items(Joi.string().uri()).required(),
  allowedScopes: Joi.array().items(Joi.string()).default(['openid', 'profile', 'email']),
  tokenEndpointAuthMethod: Joi.string().valid('client_secret_basic', 'client_secret_post', 'none').default('client_secret_post'),
  grantTypes: Joi.array().items(Joi.string().valid('authorization_code', 'refresh_token', 'client_credentials')).default(['authorization_code', 'refresh_token']),
  responseTypes: Joi.array().items(Joi.string().valid('code', 'id_token', 'token')).default(['code']),
  isPublic: Joi.boolean().default(false),
  pkceRequired: Joi.boolean().default(true),
});

export const globalAuthConfigSchema = Joi.object({
  environment: environmentSchema.required(),
  jwt: jwtConfigSchema.required(),
  redis: redisConfigSchema.required(),
  database: databaseConfigSchema.required(),
  security: securityConfigSchema.required(),
  organizations: Joi.array().items(organizationConfigSchema).min(1).required(),
  providers: Joi.array().items(authProviderConfigSchema).default([]),
  services: Joi.array().items(serviceConfigSchema).default([]),
});