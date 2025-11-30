// User and role models

export interface BaseEntity {
  id: string;
  createdAt: Date;
  updatedAt: Date;
}

export interface UserModel extends BaseEntity {
  email: string;
  username?: string;
  firstName?: string;
  lastName?: string;
  passwordHash?: string;
  isActive: boolean;
  emailVerified: boolean;
  emailVerificationToken?: string;
  emailVerificationExpiresAt?: Date;
  mfaEnabled: boolean;
  mfaSecret?: string;
  passwordResetToken?: string;
  passwordResetExpiresAt?: Date;
  lastLoginAt?: Date;
  loginAttempts: number;
  lockedUntil?: Date;
  organizationId?: string;
  avatar?: string;
  timezone?: string;
  locale?: string;
  preferences?: Record<string, any>;
}

export interface RoleModel extends BaseEntity {
  name: string;
  description?: string;
  isSystemRole: boolean;
  organizationId?: string;
}

export interface PermissionModel extends BaseEntity {
  name: string;
  resource: string;
  action: string;
  description?: string;
  isSystemPermission: boolean;
}

export interface UserRoleModel {
  userId: string;
  roleId: string;
  assignedAt: Date;
  assignedBy: string;
}

export interface RolePermissionModel {
  roleId: string;
  permissionId: string;
}

export interface UserPermissionModel {
  userId: string;
  permissionId: string;
  assignedAt: Date;
  assignedBy: string;
}

export interface OrganizationModel extends BaseEntity {
  name: string;
  slug: string;
  domain?: string;
  isActive: boolean;
  settings: OrganizationSettingsModel;
  logo?: string;
  website?: string;
}

export interface OrganizationSettingsModel {
  passwordPolicy: PasswordPolicyModel;
  sessionPolicy: SessionPolicyModel;
  mfaRequired: boolean;
  ssoEnabled: boolean;
  allowedEmailDomains: string[];
  enableApiKeys: boolean;
  enableAuditLog: boolean;
}

export interface PasswordPolicyModel {
  minLength: number;
  requireUppercase: boolean;
  requireLowercase: boolean;
  requireNumbers: boolean;
  requireSpecialChars: boolean;
  maxAge?: number;
  preventReuse?: number;
}

export interface SessionPolicyModel {
  maxDuration: number;
  idleTimeout: number;
  maxConcurrentSessions: number;
  requireMfaForSensitive: boolean;
}

export interface ApiKeyModel extends BaseEntity {
  name: string;
  keyHash: string;
  userId: string;
  organizationId?: string;
  isActive: boolean;
  expiresAt?: Date;
  lastUsedAt?: Date;
  scopes: string[];
}

export interface AuditLogModel extends BaseEntity {
  userId?: string;
  organizationId?: string;
  sessionId?: string;
  action: string;
  resource: string;
  resourceId?: string;
  outcome: 'success' | 'failure';
  ipAddress: string;
  userAgent: string;
  details?: Record<string, any>;
}

export interface AuthProviderModel extends BaseEntity {
  name: string;
  type: 'local' | 'oauth2' | 'saml' | 'ldap';
  organizationId?: string;
  isEnabled: boolean;
  config: Record<string, any>;
  displayName?: string;
  icon?: string;
  order: number;
}

// Database table names (for ORM configuration)
export const TableNames = {
  USERS: 'users',
  ROLES: 'roles',
  PERMISSIONS: 'permissions',
  USER_ROLES: 'user_roles',
  ROLE_PERMISSIONS: 'role_permissions',
  USER_PERMISSIONS: 'user_permissions',
  ORGANIZATIONS: 'organizations',
  API_KEYS: 'api_keys',
  AUDIT_LOGS: 'audit_logs',
  AUTH_PROVIDERS: 'auth_providers',
} as const;

// Default system roles
export const SystemRoles = {
  SUPER_ADMIN: 'super_admin',
  ORG_ADMIN: 'org_admin',
  USER: 'user',
} as const;

// Default system permissions
export const SystemPermissions = {
  // User management
  USER_CREATE: 'user:create',
  USER_READ: 'user:read',
  USER_UPDATE: 'user:update',
  USER_DELETE: 'user:delete',
  
  // Role management
  ROLE_CREATE: 'role:create',
  ROLE_READ: 'role:read',
  ROLE_UPDATE: 'role:update',
  ROLE_DELETE: 'role:delete',
  
  // Organization management
  ORG_CREATE: 'organization:create',
  ORG_READ: 'organization:read',
  ORG_UPDATE: 'organization:update',
  ORG_DELETE: 'organization:delete',
  
  // API key management
  API_KEY_CREATE: 'api_key:create',
  API_KEY_READ: 'api_key:read',
  API_KEY_UPDATE: 'api_key:update',
  API_KEY_DELETE: 'api_key:delete',
  
  // Audit log access
  AUDIT_LOG_READ: 'audit_log:read',
} as const;