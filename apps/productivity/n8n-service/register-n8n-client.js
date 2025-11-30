#!/usr/bin/env node
/**
 * Register N8N as OAuth2 Client in Central Auth Service
 * 
 * This script registers N8N as an OAuth2/OIDC client in the central
 * authentication service to enable SSO integration.
 */

const { AuthClient } = require('@modular-monolith/auth-clients/node');

async function registerN8NClient() {
  const authServiceUrl = process.env.AUTH_SERVICE_URL || 'http://localhost:3001';
  const n8nBaseUrl = process.env.N8N_BASE_URL || 'http://localhost:5678';
  
  console.log('🔧 Registering N8N as OAuth2 client...');
  console.log(`   Auth Service: ${authServiceUrl}`);
  console.log(`   N8N Base URL: ${n8nBaseUrl}`);
  
  try {
    // Initialize auth client
    const authClient = new AuthClient({
      baseUrl: authServiceUrl,
      // Use admin credentials or API key for client registration
      apiKey: process.env.AUTH_SERVICE_ADMIN_API_KEY,
    });
    
    // N8N OAuth2 client configuration
    const clientConfig = {
      clientId: 'n8n-service',
      clientName: 'N8N Workflow Automation',
      clientType: 'confidential',
      grantTypes: ['authorization_code', 'refresh_token'],
      responseTypes: ['code'],
      redirectUris: [
        `${n8nBaseUrl}/rest/sso/oidc/callback`,
      ],
      scopes: ['openid', 'profile', 'email'],
      tokenEndpointAuthMethod: 'client_secret_basic',
      applicationMetadata: {
        description: 'N8N Workflow Automation Platform',
        homepage: n8nBaseUrl,
        logoUri: `${n8nBaseUrl}/favicon.ico`,
        policyUri: `${n8nBaseUrl}/privacy`,
        tosUri: `${n8nBaseUrl}/terms`,
      },
    };
    
    // Register the client
    const response = await authClient.post('/admin/oauth2/clients', clientConfig);
    
    if (response.success) {
      const { clientId, clientSecret } = response.data;
      
      console.log('✅ N8N OAuth2 client registered successfully!');
      console.log('');
      console.log('📋 Add these environment variables to your N8N configuration:');
      console.log('');
      console.log(`N8N_OIDC_CLIENT_ID=${clientId}`);
      console.log(`N8N_OIDC_CLIENT_SECRET=${clientSecret}`);
      console.log('');
      console.log('🔗 OIDC Discovery Endpoint:');
      console.log(`${authServiceUrl}/oauth2/.well-known/openid_configuration`);
      
      // Write to .env.local for convenience
      const fs = require('fs');
      const envContent = `
# N8N SSO Configuration (Generated ${new Date().toISOString()})
AUTH_SERVICE_URL=${authServiceUrl}
N8N_OIDC_CLIENT_ID=${clientId}
N8N_OIDC_CLIENT_SECRET=${clientSecret}
N8N_BASE_URL=${n8nBaseUrl}
N8N_SSO_ENABLED=true
N8N_USER_MANAGEMENT_AUTHENTICATION_METHOD=oidc
`;
      
      fs.writeFileSync('.env.n8n-sso', envContent.trim());
      console.log('💾 Configuration saved to .env.n8n-sso');
      
    } else {
      console.error('❌ Failed to register N8N client:', response.error);
      process.exit(1);
    }
    
  } catch (error) {
    console.error('❌ Error registering N8N client:', error.message);
    
    if (error.response) {
      console.error('Response:', error.response.data);
    }
    
    process.exit(1);
  }
}

async function main() {
  // Check required environment variables
  const requiredVars = ['AUTH_SERVICE_URL', 'AUTH_SERVICE_ADMIN_API_KEY'];
  const missing = requiredVars.filter(varName => !process.env[varName]);
  
  if (missing.length > 0) {
    console.error('❌ Missing required environment variables:');
    missing.forEach(varName => {
      console.error(`   ${varName}`);
    });
    console.error('');
    console.error('Example usage:');
    console.error('AUTH_SERVICE_URL=http://localhost:3001 \\');
    console.error('AUTH_SERVICE_ADMIN_API_KEY=your-admin-key \\');
    console.error('N8N_BASE_URL=http://localhost:5678 \\');
    console.error('node register-n8n-client.js');
    process.exit(1);
  }
  
  await registerN8NClient();
}

if (require.main === module) {
  main().catch(console.error);
}

module.exports = { registerN8NClient };