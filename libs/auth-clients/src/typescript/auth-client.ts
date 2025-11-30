// TypeScript/JavaScript client for Auth Service

import axios, { AxiosInstance, AxiosResponse } from 'axios';
import qs from 'qs';
import { AuthClientConfig, LoginRequest, LoginResponse, RefreshResponse, RegisterRequest, RegisterResponse, UserProfile } from '../types';

export class AuthClient {
  private http: AxiosInstance;
  private config: AuthClientConfig;
  private accessToken?: string;
  private refreshToken?: string;

  constructor(config: AuthClientConfig) {
    this.config = config;
    this.http = axios.create({
      baseURL: config.baseURL,
      timeout: config.timeout || 10000,
      withCredentials: true, // For session cookies
    });

    // Add request interceptor to include auth token
    this.http.interceptors.request.use((config) => {
      if (this.accessToken) {
        config.headers.Authorization = `Bearer ${this.accessToken}`;
      }
      return config;
    });

    // Add response interceptor to handle token refresh
    this.http.interceptors.response.use(
      (response) => response,
      async (error) => {
        if (error.response?.status === 401 && this.refreshToken) {
          try {
            await this.refreshAccessToken();
            // Retry the original request
            return this.http.request(error.config);
          } catch (refreshError) {
            // Refresh failed, clear tokens and redirect to login
            this.clearTokens();
            if (this.config.onAuthError) {
              this.config.onAuthError(error);
            }
            throw error;
          }
        }
        throw error;
      }
    );
  }

  /**
   * Login with email and password
   */
  async login(request: LoginRequest): Promise<LoginResponse> {
    try {
      const response: AxiosResponse<LoginResponse> = await this.http.post('/auth/login', request);
      
      if (response.data.success && response.data.tokens) {
        this.setTokens(response.data.tokens.accessToken, response.data.tokens.refreshToken);
      }
      
      return response.data;
    } catch (error: any) {
      throw this.handleError(error);
    }
  }

  /**
   * Register new user
   */
  async register(request: RegisterRequest): Promise<RegisterResponse> {
    try {
      const response: AxiosResponse<RegisterResponse> = await this.http.post('/auth/register', request);
      return response.data;
    } catch (error: any) {
      throw this.handleError(error);
    }
  }

  /**
   * Logout current user
   */
  async logout(): Promise<void> {
    try {
      await this.http.post('/auth/logout');
    } catch (error) {
      // Continue with logout even if server request fails
    } finally {
      this.clearTokens();
    }
  }

  /**
   * Refresh access token
   */
  async refreshAccessToken(): Promise<RefreshResponse> {
    if (!this.refreshToken) {
      throw new Error('No refresh token available');
    }

    try {
      const response: AxiosResponse<RefreshResponse> = await this.http.post('/auth/refresh', {
        refreshToken: this.refreshToken
      });

      if (response.data.success && response.data.tokens) {
        this.setTokens(response.data.tokens.accessToken, response.data.tokens.refreshToken);
      }

      return response.data;
    } catch (error: any) {
      throw this.handleError(error);
    }
  }

  /**
   * Get current user profile
   */
  async getProfile(): Promise<UserProfile> {
    try {
      const response: AxiosResponse<UserProfile> = await this.http.get('/users/me');
      return response.data;
    } catch (error: any) {
      throw this.handleError(error);
    }
  }

  /**
   * Verify email address
   */
  async verifyEmail(token: string): Promise<{ success: boolean; message?: string }> {
    try {
      const response = await this.http.post('/auth/verify-email', { token });
      return response.data;
    } catch (error: any) {
      throw this.handleError(error);
    }
  }

  /**
   * Request password reset
   */
  async requestPasswordReset(email: string): Promise<{ success: boolean; message?: string }> {
    try {
      const response = await this.http.post('/auth/reset-password/request', { email });
      return response.data;
    } catch (error: any) {
      throw this.handleError(error);
    }
  }

  /**
   * Reset password with token
   */
  async resetPassword(token: string, newPassword: string): Promise<{ success: boolean; message?: string }> {
    try {
      const response = await this.http.post('/auth/reset-password', { token, newPassword });
      return response.data;
    } catch (error: any) {
      throw this.handleError(error);
    }
  }

  /**
   * Generate OAuth2 authorization URL
   */
  generateAuthorizationUrl(params: {
    clientId: string;
    redirectUri: string;
    scope?: string[];
    state?: string;
    codeChallenge?: string;
  }): string {
    const queryParams = {
      response_type: 'code',
      client_id: params.clientId,
      redirect_uri: params.redirectUri,
      scope: (params.scope || ['openid', 'profile', 'email']).join(' '),
      state: params.state,
      ...(params.codeChallenge && {
        code_challenge: params.codeChallenge,
        code_challenge_method: 'S256'
      })
    };

    const query = qs.stringify(queryParams, { skipNulls: true });
    return `${this.config.baseURL}/oauth2/authorize?${query}`;
  }

  /**
   * Exchange authorization code for tokens
   */
  async exchangeCodeForToken(params: {
    code: string;
    clientId: string;
    clientSecret?: string;
    redirectUri: string;
    codeVerifier?: string;
  }): Promise<any> {
    try {
      const response = await this.http.post('/oauth2/token', {
        grant_type: 'authorization_code',
        code: params.code,
        client_id: params.clientId,
        client_secret: params.clientSecret,
        redirect_uri: params.redirectUri,
        code_verifier: params.codeVerifier
      });

      return response.data;
    } catch (error: any) {
      throw this.handleError(error);
    }
  }

  /**
   * Get OIDC user info
   */
  async getUserInfo(accessToken?: string): Promise<any> {
    try {
      const headers = accessToken ? { Authorization: `Bearer ${accessToken}` } : {};
      const response = await this.http.get('/oauth2/userinfo', { headers });
      return response.data;
    } catch (error: any) {
      throw this.handleError(error);
    }
  }

  /**
   * Check if user is authenticated
   */
  isAuthenticated(): boolean {
    return !!this.accessToken;
  }

  /**
   * Get current access token
   */
  getAccessToken(): string | undefined {
    return this.accessToken;
  }

  /**
   * Set tokens manually (useful for SSR or token persistence)
   */
  setTokens(accessToken: string, refreshToken?: string): void {
    this.accessToken = accessToken;
    if (refreshToken) {
      this.refreshToken = refreshToken;
    }
    
    // Store tokens if storage is configured
    if (this.config.tokenStorage) {
      this.config.tokenStorage.setItem('access_token', accessToken);
      if (refreshToken) {
        this.config.tokenStorage.setItem('refresh_token', refreshToken);
      }
    }
  }

  /**
   * Clear all tokens
   */
  clearTokens(): void {
    this.accessToken = undefined;
    this.refreshToken = undefined;
    
    // Clear stored tokens
    if (this.config.tokenStorage) {
      this.config.tokenStorage.removeItem('access_token');
      this.config.tokenStorage.removeItem('refresh_token');
    }
  }

  /**
   * Load tokens from storage
   */
  loadTokensFromStorage(): void {
    if (this.config.tokenStorage) {
      const accessToken = this.config.tokenStorage.getItem('access_token');
      const refreshToken = this.config.tokenStorage.getItem('refresh_token');
      
      if (accessToken) {
        this.accessToken = accessToken;
      }
      if (refreshToken) {
        this.refreshToken = refreshToken;
      }
    }
  }

  /**
   * Handle and transform errors
   */
  private handleError(error: any): Error {
    if (error.response?.data?.error) {
      const apiError = error.response.data.error;
      const errorMessage = `${apiError.code}: ${apiError.message}`;
      const customError = new Error(errorMessage);
      (customError as any).code = apiError.code;
      (customError as any).details = apiError.details;
      return customError;
    }
    
    return error;
  }
}

export default AuthClient;