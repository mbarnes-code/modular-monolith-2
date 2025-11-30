// React Auth Provider for easy integration

import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { AuthClient } from './auth-client';
import { AuthClientConfig, LoginRequest, RegisterRequest, UserProfile } from '../types';

interface AuthContextValue {
  user: UserProfile | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (request: LoginRequest) => Promise<void>;
  register: (request: RegisterRequest) => Promise<void>;
  logout: () => Promise<void>;
  refreshToken: () => Promise<void>;
}

const AuthContext = createContext<AuthContextValue | undefined>(undefined);

interface AuthProviderProps {
  children: ReactNode;
  config: AuthClientConfig;
}

export function AuthProvider({ children, config }: AuthProviderProps) {
  const [authClient] = useState(() => new AuthClient(config));
  const [user, setUser] = useState<UserProfile | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    initializeAuth();
  }, []);

  const initializeAuth = async () => {
    try {
      // Load tokens from storage
      authClient.loadTokensFromStorage();
      
      if (authClient.isAuthenticated()) {
        // Get user profile
        const profile = await authClient.getProfile();
        setUser(profile);
      }
    } catch (error) {
      console.error('Auth initialization error:', error);
      authClient.clearTokens();
    } finally {
      setIsLoading(false);
    }
  };

  const login = async (request: LoginRequest) => {
    setIsLoading(true);
    try {
      const response = await authClient.login(request);
      if (response.success && response.user) {
        setUser(response.user);
      } else {
        throw new Error(response.error?.message || 'Login failed');
      }
    } finally {
      setIsLoading(false);
    }
  };

  const register = async (request: RegisterRequest) => {
    setIsLoading(true);
    try {
      const response = await authClient.register(request);
      if (!response.success) {
        throw new Error(response.error?.message || 'Registration failed');
      }
    } finally {
      setIsLoading(false);
    }
  };

  const logout = async () => {
    setIsLoading(true);
    try {
      await authClient.logout();
      setUser(null);
    } finally {
      setIsLoading(false);
    }
  };

  const refreshToken = async () => {
    try {
      await authClient.refreshAccessToken();
    } catch (error) {
      // Refresh failed, logout user
      setUser(null);
      authClient.clearTokens();
      throw error;
    }
  };

  const value: AuthContextValue = {
    user,
    isAuthenticated: !!user,
    isLoading,
    login,
    register,
    logout,
    refreshToken,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth(): AuthContextValue {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}

// HOC for protected routes
interface WithAuthProps {
  redirectTo?: string;
  requireRoles?: string[];
}

export function withAuth<P extends object>(
  Component: React.ComponentType<P>,
  options: WithAuthProps = {}
) {
  return function AuthenticatedComponent(props: P) {
    const { user, isAuthenticated, isLoading } = useAuth();

    if (isLoading) {
      return <div>Loading...</div>;
    }

    if (!isAuthenticated) {
      // Redirect to login or show login form
      if (options.redirectTo) {
        window.location.href = options.redirectTo;
        return null;
      }
      return <div>Please log in to access this page</div>;
    }

    // Check role requirements
    if (options.requireRoles && user) {
      const userRoles = user.roles?.map(role => role.name) || [];
      const hasRequiredRole = options.requireRoles.some(role => userRoles.includes(role));
      
      if (!hasRequiredRole) {
        return <div>You don't have permission to access this page</div>;
      }
    }

    return <Component {...props} />;
  };
}