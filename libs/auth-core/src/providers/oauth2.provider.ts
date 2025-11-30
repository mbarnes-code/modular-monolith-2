// OAuth2/OIDC Provider implementation

import axios from 'axios';
import { AuthConfig } from '../config';
import { AuthToken, OAuth2Config } from '../types';

export class OAuth2Provider {
  private config: AuthConfig;
  private oauth2Config: OAuth2Config;

  constructor(config: AuthConfig, oauth2Config: OAuth2Config) {
    this.config = config;
    this.oauth2Config = oauth2Config;
  }

  /**
   * Generate OAuth2 authorization URL
   */
  getAuthorizationUrl(state?: string, codeChallenge?: string): string {
    const params = new URLSearchParams({
      client_id: this.oauth2Config.clientId,
      redirect_uri: this.oauth2Config.redirectUri,
      response_type: 'code',
      scope: this.oauth2Config.scope.join(' '),
      state: state || this.generateState(),
    });

    // Add PKCE challenge if provided (for public clients)
    if (codeChallenge) {
      params.append('code_challenge', codeChallenge);
      params.append('code_challenge_method', 'S256');
    }

    return `${this.oauth2Config.authorizeUrl}?${params.toString()}`;
  }

  /**
   * Exchange authorization code for tokens
   */
  async exchangeCodeForToken(
    code: string,
    codeVerifier?: string
  ): Promise<AuthToken> {
    const tokenData = {
      grant_type: 'authorization_code',
      client_id: this.oauth2Config.clientId,
      client_secret: this.oauth2Config.clientSecret,
      code,
      redirect_uri: this.oauth2Config.redirectUri,
    };

    // Add PKCE verifier if provided
    if (codeVerifier) {
      tokenData['code_verifier'] = codeVerifier;
    }

    try {
      const response = await axios.post(this.oauth2Config.tokenUrl, tokenData, {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
      });

      return {
        accessToken: response.data.access_token,
        refreshToken: response.data.refresh_token,
        tokenType: response.data.token_type || 'Bearer',
        expiresIn: response.data.expires_in,
        scope: response.data.scope,
      };
    } catch (error) {
      throw new Error(`Failed to exchange code for token: ${error.message}`);
    }
  }

  /**
   * Refresh OAuth2 token
   */
  async refreshToken(refreshToken: string): Promise<AuthToken> {
    const tokenData = {
      grant_type: 'refresh_token',
      client_id: this.oauth2Config.clientId,
      client_secret: this.oauth2Config.clientSecret,
      refresh_token: refreshToken,
    };

    try {
      const response = await axios.post(this.oauth2Config.tokenUrl, tokenData, {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
      });

      return {
        accessToken: response.data.access_token,
        refreshToken: response.data.refresh_token || refreshToken,
        tokenType: response.data.token_type || 'Bearer',
        expiresIn: response.data.expires_in,
        scope: response.data.scope,
      };
    } catch (error) {
      throw new Error(`Failed to refresh token: ${error.message}`);
    }
  }

  /**
   * Get user information from OAuth2 provider
   */
  async getUserInfo(accessToken: string): Promise<any> {
    if (!this.oauth2Config.userInfoUrl) {
      throw new Error('User info URL not configured');
    }

    try {
      const response = await axios.get(this.oauth2Config.userInfoUrl, {
        headers: {
          Authorization: `Bearer ${accessToken}`,
        },
      });

      return response.data;
    } catch (error) {
      throw new Error(`Failed to get user info: ${error.message}`);
    }
  }

  /**
   * Validate OAuth2 token by checking with provider
   */
  async validateToken(accessToken: string): Promise<boolean> {
    try {
      await this.getUserInfo(accessToken);
      return true;
    } catch (error) {
      return false;
    }
  }

  /**
   * Revoke OAuth2 token
   */
  async revokeToken(token: string): Promise<void> {
    // Check if provider supports token revocation
    const revokeUrl = this.oauth2Config['revokeUrl'];
    if (!revokeUrl) {
      return; // Provider doesn't support revocation
    }

    try {
      await axios.post(revokeUrl, {
        token,
        client_id: this.oauth2Config.clientId,
        client_secret: this.oauth2Config.clientSecret,
      });
    } catch (error) {
      // Log error but don't throw - revocation is best effort
      console.warn(`Failed to revoke token: ${error.message}`);
    }
  }

  /**
   * Generate PKCE code challenge from verifier
   */
  static generateCodeChallenge(codeVerifier: string): string {
    const crypto = require('crypto');
    return crypto
      .createHash('sha256')
      .update(codeVerifier)
      .digest('base64url');
  }

  /**
   * Generate PKCE code verifier
   */
  static generateCodeVerifier(): string {
    const crypto = require('crypto');
    return crypto.randomBytes(32).toString('base64url');
  }

  /**
   * Generate state parameter for CSRF protection
   */
  private generateState(): string {
    const crypto = require('crypto');
    return crypto.randomBytes(16).toString('hex');
  }

  /**
   * Validate state parameter to prevent CSRF
   */
  validateState(providedState: string, expectedState: string): boolean {
    return providedState === expectedState;
  }
}

export default OAuth2Provider;