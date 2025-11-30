// SAML Provider implementation

import { Strategy as SamlStrategy } from 'passport-saml';
import { SAMLConfig, User } from '../types';

export class SAMLProvider {
  private config: SAMLConfig;
  private strategy: SamlStrategy;

  constructor(config: SAMLConfig) {
    this.config = config;
    this.strategy = new SamlStrategy(
      {
        entryPoint: config.entryPoint,
        issuer: config.issuer,
        cert: config.cert,
        privateCert: config.privateCert,
        callbackUrl: config.callbackUrl,
        signatureAlgorithm: config.signatureAlgorithm || 'sha256',
      },
      this.verifyCallback.bind(this)
    );
  }

  /**
   * Get SAML strategy for Passport
   */
  getStrategy(): SamlStrategy {
    return this.strategy;
  }

  /**
   * Generate SAML authentication request URL
   */
  async getAuthUrl(relayState?: string): Promise<string> {
    return new Promise((resolve, reject) => {
      this.strategy.authenticate(
        { 
          body: {},
          query: relayState ? { RelayState: relayState } : {}
        } as any,
        {
          successRedirect: (url: string) => resolve(url),
          failureRedirect: (url: string) => reject(new Error(`SAML auth failed: ${url}`))
        } as any
      );
    });
  }

  /**
   * Process SAML response
   */
  async processResponse(body: any): Promise<any> {
    return new Promise((resolve, reject) => {
      this.strategy.authenticate(
        { body } as any,
        {
          successRedirect: (user: any) => resolve(user),
          failureRedirect: (error: any) => reject(error)
        } as any
      );
    });
  }

  /**
   * Generate service provider metadata
   */
  getMetadata(): string {
    return this.strategy.generateServiceProviderMetadata(
      this.config.cert,
      this.config.cert
    );
  }

  /**
   * Verify callback for SAML strategy
   */
  private async verifyCallback(
    profile: any,
    done: (error: any, user?: any) => void
  ): Promise<void> {
    try {
      // Transform SAML profile to internal user format
      const user = await this.transformSamlProfile(profile);
      done(null, user);
    } catch (error) {
      done(error);
    }
  }

  /**
   * Transform SAML profile to internal user format
   */
  private async transformSamlProfile(profile: any): Promise<Partial<User>> {
    // Extract user attributes from SAML profile
    const email = profile.email || profile['http://schemas.xmlsoap.org/ws/2005/05/identity/claims/emailaddress'];
    const firstName = profile.firstName || profile['http://schemas.xmlsoap.org/ws/2005/05/identity/claims/givenname'];
    const lastName = profile.lastName || profile['http://schemas.xmlsoap.org/ws/2005/05/identity/claims/surname'];
    const username = profile.nameID || email;

    if (!email) {
      throw new Error('Email is required from SAML response');
    }

    return {
      email,
      username,
      firstName,
      lastName,
      emailVerified: true, // Assume email is verified if coming from SAML
    };
  }

  /**
   * Logout from SAML provider
   */
  async logout(nameID: string, sessionIndex?: string): Promise<string> {
    return new Promise((resolve, reject) => {
      this.strategy.logout(
        { user: { nameID, sessionIndex } } as any,
        (error: any, url?: string) => {
          if (error) {
            reject(error);
          } else {
            resolve(url || '');
          }
        }
      );
    });
  }
}

export default SAMLProvider;