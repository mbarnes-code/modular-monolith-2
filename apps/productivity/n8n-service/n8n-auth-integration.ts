/**
 * N8N Service Integration with Central Auth Service
 * 
 * This configuration integrates N8N with our central authentication service
 * to provide unified SSO across the modular monolith.
 */

// Environment configuration for N8N integration
export const n8nAuthConfig = {
  // Central auth service configuration
  authService: {
    baseUrl: process.env.AUTH_SERVICE_URL || 'http://localhost:3001',
    clientId: process.env.N8N_OIDC_CLIENT_ID || 'n8n-service',
    clientSecret: process.env.N8N_OIDC_CLIENT_SECRET,
  },
  
  // OIDC endpoints derived from central auth service
  oidc: {
    discoveryEndpoint: `${process.env.AUTH_SERVICE_URL || 'http://localhost:3001'}/oauth2/.well-known/openid_configuration`,
    authorizationEndpoint: `${process.env.AUTH_SERVICE_URL || 'http://localhost:3001'}/oauth2/authorize`,
    tokenEndpoint: `${process.env.AUTH_SERVICE_URL || 'http://localhost:3001'}/oauth2/token`,
    userinfoEndpoint: `${process.env.AUTH_SERVICE_URL || 'http://localhost:3001'}/oauth2/userinfo`,
    jwksEndpoint: `${process.env.AUTH_SERVICE_URL || 'http://localhost:3001'}/oauth2/jwks`,
  },

  // N8N specific configuration
  n8n: {
    callbackUrl: `${process.env.N8N_BASE_URL || 'http://localhost:5678'}/rest/sso/oidc/callback`,
    loginEnabled: process.env.N8N_SSO_ENABLED === 'true',
    prompt: 'select_account',
    scopes: ['openid', 'profile', 'email'],
  },

  // User attribute mapping
  userMapping: {
    id: 'sub',
    email: 'email',
    firstName: 'given_name',
    lastName: 'family_name',
    displayName: 'name',
    username: 'preferred_username',
  },
};

/**
 * Initialize N8N with central auth service
 */
export async function initializeN8NAuth() {
  try {
    // Load OIDC service
    const { Container } = await import('@n8n/di');
    const { OidcService } = await import('./src/packages/cli/src/sso.ee/oidc/oidc.service.ee');
    
    const oidcService = Container.get(OidcService);
    
    // Configure OIDC to use central auth service
    await oidcService.saveConfig({
      clientId: n8nAuthConfig.authService.clientId,
      clientSecret: n8nAuthConfig.authService.clientSecret,
      discoveryEndpoint: n8nAuthConfig.oidc.discoveryEndpoint,
      loginEnabled: n8nAuthConfig.n8n.loginEnabled,
      prompt: n8nAuthConfig.n8n.prompt,
    });

    console.log('✅ N8N integrated with central auth service');
    console.log('   Discovery Endpoint:', n8nAuthConfig.oidc.discoveryEndpoint);
    console.log('   Login Enabled:', n8nAuthConfig.n8n.loginEnabled);
    
    return true;
  } catch (error) {
    console.error('❌ Failed to initialize N8N auth integration:', error);
    return false;
  }
}

/**
 * Environment variables required for N8N SSO integration
 */
export const requiredEnvVars = [
  'AUTH_SERVICE_URL',
  'N8N_OIDC_CLIENT_ID', 
  'N8N_OIDC_CLIENT_SECRET',
  'N8N_BASE_URL',
  'N8N_SSO_ENABLED',
];

/**
 * Validate environment configuration
 */
export function validateN8NAuthConfig(): string[] {
  const missing: string[] = [];
  
  requiredEnvVars.forEach(varName => {
    if (!process.env[varName]) {
      missing.push(varName);
    }
  });
  
  return missing;
}

export default n8nAuthConfig;