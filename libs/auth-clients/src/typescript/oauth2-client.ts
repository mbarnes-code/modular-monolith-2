// OAuth2 specific client implementation

import { AuthClientConfig } from '../types';
import { AuthClient } from './auth-client';

export interface OAuth2Config {
  clientId: string;
  clientSecret?: string; // Only for confidential clients
  redirectUri: string;
  scope?: string[];
  usePKCE?: boolean; // Use PKCE for public clients
}

export class OAuth2Client extends AuthClient {
  private oauth2Config: OAuth2Config;

  constructor(config: AuthClientConfig, oauth2Config: OAuth2Config) {
    super(config);
    this.oauth2Config = oauth2Config;
  }

  /**
   * Start OAuth2 authorization flow
   */
  async startAuthorizationFlow(state?: string): Promise<{ authUrl: string; codeVerifier?: string }> {
    let codeVerifier: string | undefined;
    let codeChallenge: string | undefined;

    // Generate PKCE challenge if using PKCE
    if (this.oauth2Config.usePKCE) {
      codeVerifier = this.generateCodeVerifier();
      codeChallenge = await this.generateCodeChallenge(codeVerifier);
    }

    const authUrl = this.generateAuthorizationUrl({
      clientId: this.oauth2Config.clientId,
      redirectUri: this.oauth2Config.redirectUri,
      scope: this.oauth2Config.scope,
      state,
      codeChallenge,
    });

    return { authUrl, codeVerifier };
  }

  /**
   * Complete OAuth2 authorization flow
   */
  async completeAuthorizationFlow(code: string, codeVerifier?: string): Promise<any> {
    return this.exchangeCodeForToken({
      code,
      clientId: this.oauth2Config.clientId,
      clientSecret: this.oauth2Config.clientSecret,
      redirectUri: this.oauth2Config.redirectUri,
      codeVerifier,
    });
  }

  /**
   * Full OAuth2 redirect flow for browser environments
   */
  redirectToAuthorization(state?: string): void {
    const { authUrl, codeVerifier } = this.startAuthorizationFlow(state);
    
    // Store code verifier for PKCE
    if (codeVerifier && this.config.tokenStorage) {
      this.config.tokenStorage.setItem('oauth2_code_verifier', codeVerifier);
    }

    // Redirect to authorization server
    window.location.href = authUrl;
  }

  /**
   * Handle OAuth2 callback (typically called on redirect page)
   */
  async handleCallback(): Promise<any> {
    const urlParams = new URLSearchParams(window.location.search);
    const code = urlParams.get('code');
    const state = urlParams.get('state');
    const error = urlParams.get('error');

    if (error) {
      throw new Error(`OAuth2 error: ${error}`);
    }

    if (!code) {
      throw new Error('No authorization code received');
    }

    // Get stored code verifier for PKCE
    let codeVerifier: string | undefined;
    if (this.oauth2Config.usePKCE && this.config.tokenStorage) {
      codeVerifier = this.config.tokenStorage.getItem('oauth2_code_verifier') || undefined;
      this.config.tokenStorage.removeItem('oauth2_code_verifier');
    }

    // Exchange code for tokens
    const tokenResponse = await this.completeAuthorizationFlow(code, codeVerifier);

    // Set tokens in client
    if (tokenResponse.access_token) {
      this.setTokens(tokenResponse.access_token, tokenResponse.refresh_token);
    }

    return tokenResponse;
  }

  /**
   * Generate PKCE code verifier
   */
  private generateCodeVerifier(): string {
    const array = new Uint8Array(32);
    crypto.getRandomValues(array);
    return btoa(String.fromCharCode.apply(null, array))
      .replace(/\+/g, '-')
      .replace(/\//g, '_')
      .replace(/=/g, '');
  }

  /**
   * Generate PKCE code challenge
   */
  private async generateCodeChallenge(verifier: string): Promise<string> {
    const encoder = new TextEncoder();
    const data = encoder.encode(verifier);
    const digest = await crypto.subtle.digest('SHA-256', data);
    return btoa(String.fromCharCode.apply(null, new Uint8Array(digest)))
      .replace(/\+/g, '-')
      .replace(/\//g, '_')
      .replace(/=/g, '');
  }
}