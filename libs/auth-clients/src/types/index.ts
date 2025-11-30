// Type definitions for auth clients

import { AuthToken, Permission, Role, User } from '@modular-monolith/auth-core';

export interface AuthClientConfig {
  baseURL: string;
  timeout?: number;
  tokenStorage?: TokenStorage;
  onAuthError?: (error: any) => void;
}

export interface TokenStorage {
  getItem(key: string): string | null;
  setItem(key: string, value: string): void;
  removeItem(key: string): void;
}

export interface LoginRequest {
  email: string;
  password: string;
  organizationId?: string;
  mfaCode?: string;
  rememberMe?: boolean;
}

export interface LoginResponse {
  success: boolean;
  user?: User;
  tokens?: AuthToken;
  error?: {
    code: string;
    message: string;
    details?: any;
  };
  requiresMfa?: boolean;
  mfaChallenge?: {
    type: 'totp' | 'sms' | 'email';
    challengeId: string;
    expiresAt: Date;
  };
}

export interface RegisterRequest {
  email: string;
  password: string;
  firstName?: string;
  lastName?: string;
  organizationId?: string;
}

export interface RegisterResponse {
  success: boolean;
  user?: User;
  error?: {
    code: string;
    message: string;
    details?: any;
  };
}

export interface RefreshRequest {
  refreshToken: string;
}

export interface RefreshResponse {
  success: boolean;
  tokens?: AuthToken;
  error?: {
    code: string;
    message: string;
  };
}

export interface UserProfile {
  id: string;
  email: string;
  username?: string;
  firstName?: string;
  lastName?: string;
  roles?: Role[];
  permissions?: Permission[];
  organizationId?: string;
  isActive: boolean;
  emailVerified: boolean;
  mfaEnabled: boolean;
  lastLoginAt?: Date;
  createdAt: Date;
  updatedAt: Date;
  avatar?: string;
  timezone?: string;
  locale?: string;
  preferences?: Record<string, any>;
}

// Browser storage implementations
export class LocalStorageAdapter implements TokenStorage {
  getItem(key: string): string | null {
    if (typeof window === 'undefined') return null;
    return localStorage.getItem(key);
  }

  setItem(key: string, value: string): void {
    if (typeof window === 'undefined') return;
    localStorage.setItem(key, value);
  }

  removeItem(key: string): void {
    if (typeof window === 'undefined') return;
    localStorage.removeItem(key);
  }
}

export class SessionStorageAdapter implements TokenStorage {
  getItem(key: string): string | null {
    if (typeof window === 'undefined') return null;
    return sessionStorage.getItem(key);
  }

  setItem(key: string, value: string): void {
    if (typeof window === 'undefined') return;
    sessionStorage.setItem(key, value);
  }

  removeItem(key: string): void {
    if (typeof window === 'undefined') return;
    sessionStorage.removeItem(key);
  }
}

export class MemoryStorageAdapter implements TokenStorage {
  private storage: Map<string, string> = new Map();

  getItem(key: string): string | null {
    return this.storage.get(key) || null;
  }

  setItem(key: string, value: string): void {
    this.storage.set(key, value);
  }

  removeItem(key: string): void {
    this.storage.delete(key);
  }
}