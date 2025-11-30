// Authentication and authorization type definitions

export interface User {
  id: string;
  email: string;
  username?: string;
  firstName?: string;
  lastName?: string;
  roles: Role[];
  permissions: Permission[];
  organizationId?: string;
  isActive: boolean;
  emailVerified: boolean;
  mfaEnabled: boolean;
  lastLoginAt?: Date;
  createdAt: Date;
  updatedAt: Date;
}

export interface Role {
  id: string;
  name: string;
  description?: string;
  permissions: Permission[];
  organizationId?: string;
  isSystemRole: boolean;
}

export interface Permission {
  id: string;
  name: string;
  resource: string;
  action: string;
  description?: string;
}

export interface Organization {
  id: string;
  name: string;
  slug: string;
  settings: OrganizationSettings;
  isActive: boolean;
  createdAt: Date;
  updatedAt: Date;
}

export interface OrganizationSettings {
  passwordPolicy: PasswordPolicy;
  sessionPolicy: SessionPolicy;
  mfaRequired: boolean;
  ssoEnabled: boolean;
  allowedEmailDomains?: string[];
}

export interface PasswordPolicy {
  minLength: number;
  requireUppercase: boolean;
  requireLowercase: boolean;
  requireNumbers: boolean;
  requireSpecialChars: boolean;
  maxAge?: number; // days
  preventReuse?: number; // last N passwords
}

export interface SessionPolicy {
  maxDuration: number; // seconds
  idleTimeout: number; // seconds
  maxConcurrentSessions: number;
  requireMfaForSensitive: boolean;
}

export interface AuthToken {
  accessToken: string;
  refreshToken?: string;
  tokenType: 'Bearer';
  expiresIn: number;
  scope?: string;
}

export interface JWTPayload {
  sub: string; // user ID
  email: string;
  roles: string[];
  permissions: string[];
  org?: string; // organization ID
  iat: number;
  exp: number;
  aud: string;
  iss: string;
  jti?: string; // JWT ID for blacklisting
}

export interface SessionData {
  sessionId: string;
  userId: string;
  organizationId?: string;
  ipAddress: string;
  userAgent: string;
  createdAt: Date;
  lastActivity: Date;
  expiresAt: Date;
  mfaVerified: boolean;
}

export interface AuthRequest {
  email: string;
  password: string;
  organizationId?: string;
  mfaCode?: string;
  rememberMe?: boolean;
}

export interface AuthResponse {
  success: boolean;
  user?: User;
  tokens?: AuthToken;
  session?: SessionData;
  error?: AuthError;
  requiresMfa?: boolean;
  mfaChallenge?: MfaChallenge;
}

export interface MfaChallenge {
  type: 'totp' | 'sms' | 'email';
  challengeId: string;
  expiresAt: Date;
}

export interface AuthError {
  code: string;
  message: string;
  details?: any;
}

export interface OAuth2Config {
  clientId: string;
  clientSecret: string;
  redirectUri: string;
  scope: string[];
  authorizeUrl: string;
  tokenUrl: string;
  userInfoUrl?: string;
  jwksUrl?: string;
}

export interface SAMLConfig {
  entryPoint: string;
  issuer: string;
  cert: string;
  privateCert?: string;
  callbackUrl: string;
  signatureAlgorithm: string;
}

export interface LDAPConfig {
  url: string;
  bindDN: string;
  bindCredentials: string;
  searchBase: string;
  searchFilter: string;
  searchAttributes?: string[];
  tlsOptions?: any;
}

export interface AuthProvider {
  name: string;
  type: 'local' | 'oauth2' | 'saml' | 'ldap';
  config: OAuth2Config | SAMLConfig | LDAPConfig | any;
  isEnabled: boolean;
}

export interface AuthMiddlewareOptions {
  excludePaths?: string[];
  requireAuth?: boolean;
  requireMfa?: boolean;
  requiredRoles?: string[];
  requiredPermissions?: string[];
}

export type AuthStrategy = 'jwt' | 'session' | 'api-key';

export interface ApiKey {
  id: string;
  name: string;
  keyHash: string;
  userId: string;
  organizationId?: string;
  permissions: Permission[];
  isActive: boolean;
  expiresAt?: Date;
  lastUsedAt?: Date;
  createdAt: Date;
}

export interface AuditLog {
  id: string;
  userId?: string;
  sessionId?: string;
  action: string;
  resource: string;
  outcome: 'success' | 'failure';
  ipAddress: string;
  userAgent: string;
  details?: any;
  timestamp: Date;
}

// Event types for auth system
export interface AuthEvent {
  type: AuthEventType;
  userId?: string;
  sessionId?: string;
  organizationId?: string;
  data: any;
  timestamp: Date;
}

export type AuthEventType =
  | 'user.login.success'
  | 'user.login.failure'
  | 'user.logout'
  | 'user.mfa.setup'
  | 'user.mfa.verify'
  | 'user.password.change'
  | 'user.password.reset'
  | 'session.created'
  | 'session.expired'
  | 'token.issued'
  | 'token.revoked'
  | 'api-key.created'
  | 'api-key.revoked';