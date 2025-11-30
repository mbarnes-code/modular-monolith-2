// Configuration type definitions

export interface GlobalAuthConfig {
  environment: Environment;
  jwt: JWTConfig;
  redis: RedisConfig;
  database: DatabaseConfig;
  security: SecurityConfig;
  organizations: OrganizationConfig[];
  providers: AuthProviderConfig[];
  services: ServiceConfig[];
}

export interface Environment {
  name: 'development' | 'staging' | 'production';
  debug: boolean;
  logLevel: 'error' | 'warn' | 'info' | 'debug';
}

export interface JWTConfig {
  issuer: string;
  audience: string;
  algorithm: 'HS256' | 'RS256' | 'ES256';
  publicKey?: string;
  privateKey?: string;
  accessTokenTTL: number; // seconds
  refreshTokenTTL: number; // seconds
  clockTolerance: number; // seconds
}

export interface RedisConfig {
  cluster: RedisClusterConfig[];
  keyPrefix: string;
  ttl: {
    session: number;
    tokenBlacklist: number;
    rateLimitWindow: number;
  };
}

export interface RedisClusterConfig {
  host: string;
  port: number;
  password?: string;
  database: number;
}

export interface DatabaseConfig {
  primary: DatabaseConnection;
  replicas?: DatabaseConnection[];
  pool: {
    min: number;
    max: number;
    idleTimeout: number;
  };
}

export interface DatabaseConnection {
  host: string;
  port: number;
  database: string;
  username: string;
  password: string;
  ssl?: boolean;
}

export interface SecurityConfig {
  passwordPolicy: PasswordPolicyConfig;
  rateLimiting: RateLimitingConfig;
  csrf: CSRFConfig;
  cors: CORSConfig;
  encryption: EncryptionConfig;
}

export interface PasswordPolicyConfig {
  minLength: number;
  maxLength: number;
  requireUppercase: boolean;
  requireLowercase: boolean;
  requireNumbers: boolean;
  requireSpecialChars: boolean;
  preventReuse: number; // last N passwords
  maxAge: number; // days
  bcryptRounds: number;
}

export interface RateLimitingConfig {
  login: {
    maxAttempts: number;
    windowMs: number;
    blockDuration: number;
  };
  api: {
    maxRequests: number;
    windowMs: number;
  };
  passwordReset: {
    maxAttempts: number;
    windowMs: number;
  };
}

export interface CSRFConfig {
  enabled: boolean;
  tokenLength: number;
  cookieName: string;
  headerName: string;
}

export interface CORSConfig {
  allowedOrigins: string[];
  allowedMethods: string[];
  allowedHeaders: string[];
  credentials: boolean;
  maxAge: number;
}

export interface EncryptionConfig {
  algorithm: string;
  keySize: number;
  ivSize: number;
  saltRounds: number;
}

export interface OrganizationConfig {
  id: string;
  name: string;
  slug: string;
  domain?: string;
  settings: OrganizationSettings;
}

export interface OrganizationSettings {
  passwordPolicy?: Partial<PasswordPolicyConfig>;
  sessionTimeout: number;
  maxConcurrentSessions: number;
  mfaRequired: boolean;
  ssoEnabled: boolean;
  allowedEmailDomains: string[];
  customFields: Record<string, any>;
}

export interface AuthProviderConfig {
  id: string;
  name: string;
  type: 'local' | 'oauth2' | 'saml' | 'ldap' | 'oidc';
  enabled: boolean;
  organizationIds?: string[]; // If empty, available to all orgs
  config: OAuth2ProviderConfig | SAMLProviderConfig | LDAPProviderConfig | OIDCProviderConfig;
  displayName: string;
  icon?: string;
  order: number;
}

export interface OAuth2ProviderConfig {
  clientId: string;
  clientSecret: string;
  authorizeUrl: string;
  tokenUrl: string;
  userInfoUrl?: string;
  scope: string[];
  redirectUri: string;
  additionalParams?: Record<string, string>;
}

export interface SAMLProviderConfig {
  entityId: string;
  ssoUrl: string;
  certificate: string;
  attributeMapping: {
    email: string;
    firstName?: string;
    lastName?: string;
    groups?: string;
  };
  signRequests: boolean;
  wantAssertionsSigned: boolean;
}

export interface LDAPProviderConfig {
  url: string;
  bindDN: string;
  bindPassword: string;
  searchBase: string;
  searchFilter: string;
  attributes: {
    email: string;
    firstName?: string;
    lastName?: string;
    groups?: string;
  };
  tlsOptions?: {
    rejectUnauthorized: boolean;
    ca?: string[];
  };
}

export interface OIDCProviderConfig {
  issuer: string;
  clientId: string;
  clientSecret: string;
  scope: string[];
  redirectUri: string;
  responseType: string;
  additionalParams?: Record<string, string>;
}

export interface ServiceConfig {
  name: string;
  clientId: string;
  clientSecret: string;
  redirectUris: string[];
  allowedScopes: string[];
  tokenEndpointAuthMethod: 'client_secret_basic' | 'client_secret_post' | 'none';
  grantTypes: string[];
  responseTypes: string[];
  isPublic: boolean;
  pkceRequired: boolean;
}

export interface ConfigValidationResult {
  valid: boolean;
  errors: ConfigValidationError[];
  warnings: ConfigValidationWarning[];
}

export interface ConfigValidationError {
  path: string;
  message: string;
  value?: any;
}

export interface ConfigValidationWarning {
  path: string;
  message: string;
  suggestion?: string;
}