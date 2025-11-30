// OAuth2/OIDC routes for SSO integration

import { FastifyInstance, FastifyReply, FastifyRequest } from 'fastify';

export default async function oauth2Routes(fastify: FastifyInstance) {
  const authConfig = (fastify as any).authConfig;

  // OAuth2 Authorization endpoint
  fastify.get('/authorize', {
    schema: {
      tags: ['OAuth2'],
      description: 'OAuth2 authorization endpoint',
      querystring: {
        type: 'object',
        properties: {
          response_type: { type: 'string', enum: ['code'] },
          client_id: { type: 'string' },
          redirect_uri: { type: 'string' },
          scope: { type: 'string' },
          state: { type: 'string' },
          code_challenge: { type: 'string' },
          code_challenge_method: { type: 'string', enum: ['S256'] },
        },
        required: ['response_type', 'client_id', 'redirect_uri'],
      },
    },
  }, async (request: FastifyRequest, reply: FastifyReply) => {
    const query = request.query as any;
    
    try {
      // Validate client ID and redirect URI
      // In a real implementation, you would validate against registered clients
      
      // For now, redirect to login with OAuth parameters
      const loginUrl = new URL('/auth/login', `${request.protocol}://${request.hostname}`);
      Object.entries(query).forEach(([key, value]) => {
        loginUrl.searchParams.set(key, value as string);
      });
      
      reply.redirect(302, loginUrl.toString());
    } catch (error) {
      fastify.log.error(error);
      reply.code(400);
      return { error: 'invalid_request', error_description: 'Invalid OAuth2 request' };
    }
  });

  // OAuth2 Token endpoint
  fastify.post('/token', {
    schema: {
      tags: ['OAuth2'],
      description: 'OAuth2 token endpoint',
      body: {
        type: 'object',
        properties: {
          grant_type: { type: 'string', enum: ['authorization_code', 'refresh_token'] },
          code: { type: 'string' },
          redirect_uri: { type: 'string' },
          client_id: { type: 'string' },
          client_secret: { type: 'string' },
          refresh_token: { type: 'string' },
          code_verifier: { type: 'string' },
        },
        required: ['grant_type', 'client_id'],
      },
    },
  }, async (request: FastifyRequest, reply: FastifyReply) => {
    const body = request.body as any;
    
    try {
      if (body.grant_type === 'authorization_code') {
        // Handle authorization code flow
        // In a real implementation, you would:
        // 1. Validate the authorization code
        // 2. Verify client credentials
        // 3. Generate access and refresh tokens
        
        return {
          access_token: 'mock_access_token',
          token_type: 'Bearer',
          expires_in: 3600,
          refresh_token: 'mock_refresh_token',
          scope: 'openid profile email',
        };
      } else if (body.grant_type === 'refresh_token') {
        // Handle refresh token flow
        return {
          access_token: 'mock_new_access_token',
          token_type: 'Bearer',
          expires_in: 3600,
          refresh_token: body.refresh_token,
          scope: 'openid profile email',
        };
      } else {
        reply.code(400);
        return { error: 'unsupported_grant_type' };
      }
    } catch (error) {
      fastify.log.error(error);
      reply.code(400);
      return { error: 'invalid_request' };
    }
  });

  // OIDC UserInfo endpoint
  fastify.get('/userinfo', {
    schema: {
      tags: ['OAuth2'],
      description: 'OIDC UserInfo endpoint',
      security: [{ Bearer: [] }],
    },
  }, async (request: FastifyRequest, reply: FastifyReply) => {
    try {
      // Verify access token and return user info
      // In a real implementation, you would validate the token and return user data
      
      return {
        sub: 'user123',
        email: 'user@example.com',
        email_verified: true,
        name: 'John Doe',
        given_name: 'John',
        family_name: 'Doe',
        picture: 'https://example.com/avatar.jpg',
      };
    } catch (error) {
      fastify.log.error(error);
      reply.code(401);
      return { error: 'invalid_token' };
    }
  });

  // OIDC Discovery endpoint
  fastify.get('/.well-known/openid-configuration', {
    schema: {
      tags: ['OAuth2'],
      description: 'OIDC Discovery endpoint',
    },
  }, async (request: FastifyRequest) => {
    const baseUrl = `${request.protocol}://${request.hostname}${request.hostname === 'localhost' ? `:${fastify.server.address()?.port}` : ''}`;
    
    return {
      issuer: baseUrl,
      authorization_endpoint: `${baseUrl}/oauth2/authorize`,
      token_endpoint: `${baseUrl}/oauth2/token`,
      userinfo_endpoint: `${baseUrl}/oauth2/userinfo`,
      jwks_uri: `${baseUrl}/oauth2/.well-known/jwks.json`,
      response_types_supported: ['code'],
      subject_types_supported: ['public'],
      id_token_signing_alg_values_supported: ['HS256'],
      scopes_supported: ['openid', 'profile', 'email'],
      token_endpoint_auth_methods_supported: ['client_secret_post', 'client_secret_basic'],
      code_challenge_methods_supported: ['S256'],
    };
  });

  // JWKS endpoint
  fastify.get('/.well-known/jwks.json', {
    schema: {
      tags: ['OAuth2'],
      description: 'JSON Web Key Set endpoint',
    },
  }, async () => {
    // In a real implementation, you would return actual public keys
    return {
      keys: [
        {
          kty: 'oct',
          use: 'sig',
          kid: 'default',
          alg: 'HS256',
        }
      ]
    };
  });
}