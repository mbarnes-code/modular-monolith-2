/**
 * N8N Configuration Patch for Central Auth Service Integration
 * 
 * This file patches N8N's OIDC configuration to automatically
 * integrate with our central authentication service.
 */

import { Container } from '@n8n/di';
import { GlobalConfig } from '@n8n/config';
import { OidcService } from './src/packages/cli/src/sso.ee/oidc/oidc.service.ee';
import { Logger } from '@n8n/backend-common';
import { n8nAuthConfig, validateN8NAuthConfig } from './n8n-auth-integration';

/**
 * Patch N8N's OIDC service to use central auth service
 */
export async function patchN8NOidcService() {
  const logger = Container.get(Logger);
  
  try {
    // Validate configuration
    const missingVars = validateN8NAuthConfig();
    if (missingVars.length > 0) {
      logger.warn(`Missing environment variables for SSO: ${missingVars.join(', ')}`);
      logger.warn('N8N will run with local authentication only');
      return false;
    }

    // Get OIDC service instance
    const oidcService = Container.get(OidcService);
    
    // Configure OIDC with central auth service settings
    const oidcConfig = {
      clientId: n8nAuthConfig.authService.clientId,
      clientSecret: n8nAuthConfig.authService.clientSecret!,
      discoveryEndpoint: n8nAuthConfig.oidc.discoveryEndpoint,
      loginEnabled: n8nAuthConfig.n8n.loginEnabled,
      prompt: n8nAuthConfig.n8n.prompt,
    };

    // Save the configuration to N8N's settings
    await oidcService.saveConfig(oidcConfig);
    
    logger.info('✅ N8N OIDC configured for central auth service');
    logger.info(`   Client ID: ${oidcConfig.clientId}`);
    logger.info(`   Discovery: ${oidcConfig.discoveryEndpoint}`);
    logger.info(`   Login Enabled: ${oidcConfig.loginEnabled}`);
    
    return true;
  } catch (error) {
    logger.error('❌ Failed to patch N8N OIDC service:', error);
    return false;
  }
}

/**
 * Hook into N8N's startup process to configure SSO
 */
export async function integrateWithN8NStartup() {
  const logger = Container.get(Logger);
  
  try {
    // Wait for N8N services to initialize
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    // Apply our OIDC configuration
    const success = await patchN8NOidcService();
    
    if (success) {
      logger.info('🔗 N8N successfully integrated with central auth service');
      
      // Log SSO endpoints for reference
      logger.info('SSO Endpoints:');
      logger.info(`  Login: ${n8nAuthConfig.n8n.callbackUrl.replace('/callback', '/login')}`);
      logger.info(`  Callback: ${n8nAuthConfig.n8n.callbackUrl}`);
    } else {
      logger.warn('⚠️  N8N running without central auth integration');
    }
    
    return success;
  } catch (error) {
    logger.error('Failed to integrate N8N with central auth service:', error);
    return false;
  }
}

/**
 * Custom N8N startup hook
 * This should be called during N8N initialization
 */
export async function n8nAuthStartupHook() {
  const logger = Container.get(Logger);
  
  logger.info('🚀 Initializing N8N with central auth service integration...');
  
  // Validate environment
  const missingVars = validateN8NAuthConfig();
  if (missingVars.length > 0) {
    logger.warn(`Missing SSO environment variables: ${missingVars.join(', ')}`);
    logger.warn('Add these to your .env file to enable SSO integration');
    return;
  }

  // Integrate with central auth service
  await integrateWithN8NStartup();
}

export default {
  patchN8NOidcService,
  integrateWithN8NStartup,
  n8nAuthStartupHook,
};