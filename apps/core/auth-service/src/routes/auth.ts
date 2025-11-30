// Authentication routes

import { JWTProvider, SecurityUtils, SessionProvider } from '@modular-monolith/auth-core';
import { FastifyInstance, FastifyReply, FastifyRequest } from 'fastify';
import { loginSchema, refreshSchema, registerSchema } from '../schemas/auth.schema';
import { AuthService } from '../services/auth.service';
import { UserService } from '../services/user.service';

export default async function authRoutes(fastify: FastifyInstance) {
  const authConfig = (fastify as any).authConfig;
  const jwtProvider = new JWTProvider(authConfig);
  const sessionProvider = new SessionProvider(authConfig);
  const securityUtils = new SecurityUtils(authConfig.security.bcryptRounds);
  const userService = new UserService();
  const authService = new AuthService(jwtProvider, sessionProvider, userService);

  // Login endpoint
  fastify.post('/login', {
    schema: {
      body: loginSchema,
      tags: ['Authentication'],
      description: 'Authenticate user and return tokens',
    },
  }, async (request: FastifyRequest, reply: FastifyReply) => {
    const { email, password, organizationId, mfaCode, rememberMe } = request.body as any;
    
    try {
      const ipAddress = request.ip;
      const userAgent = request.headers['user-agent'] || 'unknown';

      const result = await authService.authenticateUser({
        email,
        password,
        organizationId,
        mfaCode,
        rememberMe,
      }, ipAddress, userAgent);

      if (result.success && result.tokens && result.session) {
        // Set session cookie
        reply.setCookie(authConfig.session.cookieName, result.session.sessionId, {
          httpOnly: true,
          secure: !fastify.config.isDevelopment,
          sameSite: 'lax',
          maxAge: authConfig.jwt.accessTokenExpiry,
        });

        return {
          success: true,
          user: result.user,
          tokens: result.tokens,
        };
      } else {
        reply.code(401);
        return result;
      }
    } catch (error) {
      fastify.log.error(error);
      reply.code(500);
      return { success: false, error: { code: 'INTERNAL_ERROR', message: 'Authentication failed' } };
    }
  });

  // Register endpoint
  fastify.post('/register', {
    schema: {
      body: registerSchema,
      tags: ['Authentication'],
      description: 'Register new user account',
    },
  }, async (request: FastifyRequest, reply: FastifyReply) => {
    const { email, password, firstName, lastName, organizationId } = request.body as any;
    
    try {
      const result = await authService.registerUser({
        email,
        password,
        firstName,
        lastName,
        organizationId,
      });

      if (result.success) {
        reply.code(201);
        return {
          success: true,
          user: result.user,
          message: 'Registration successful. Please check your email for verification.',
        };
      } else {
        reply.code(400);
        return result;
      }
    } catch (error) {
      fastify.log.error(error);
      reply.code(500);
      return { success: false, error: { code: 'INTERNAL_ERROR', message: 'Registration failed' } };
    }
  });

  // Refresh token endpoint
  fastify.post('/refresh', {
    schema: {
      body: refreshSchema,
      tags: ['Authentication'],
      description: 'Refresh access token using refresh token',
    },
  }, async (request: FastifyRequest, reply: FastifyReply) => {
    const { refreshToken } = request.body as any;
    
    try {
      const newTokens = await jwtProvider.refreshAccessToken(refreshToken);
      
      return {
        success: true,
        tokens: newTokens,
      };
    } catch (error) {
      fastify.log.error(error);
      reply.code(401);
      return { success: false, error: { code: 'INVALID_REFRESH_TOKEN', message: 'Refresh token is invalid or expired' } };
    }
  });

  // Logout endpoint
  fastify.post('/logout', {
    schema: {
      tags: ['Authentication'],
      description: 'Logout user and invalidate session',
      security: [{ Bearer: [] }],
    },
  }, async (request: FastifyRequest, reply: FastifyReply) => {
    try {
      const sessionId = request.cookies[authConfig.session.cookieName];
      const authHeader = request.headers.authorization;
      
      if (sessionId) {
        await sessionProvider.destroySession(sessionId);
      }
      
      if (authHeader) {
        const token = authHeader.replace('Bearer ', '');
        await jwtProvider.revokeToken(token);
      }

      // Clear session cookie
      reply.clearCookie(authConfig.session.cookieName);
      
      return { success: true, message: 'Logged out successfully' };
    } catch (error) {
      fastify.log.error(error);
      reply.code(500);
      return { success: false, error: { code: 'LOGOUT_ERROR', message: 'Logout failed' } };
    }
  });

  // Verify email endpoint
  fastify.post('/verify-email', {
    schema: {
      tags: ['Authentication'],
      description: 'Verify user email address',
    },
  }, async (request: FastifyRequest, reply: FastifyReply) => {
    const { token } = request.body as any;
    
    try {
      const result = await authService.verifyEmail(token);
      
      if (result.success) {
        return { success: true, message: 'Email verified successfully' };
      } else {
        reply.code(400);
        return result;
      }
    } catch (error) {
      fastify.log.error(error);
      reply.code(500);
      return { success: false, error: { code: 'VERIFICATION_ERROR', message: 'Email verification failed' } };
    }
  });

  // Request password reset
  fastify.post('/reset-password/request', {
    schema: {
      tags: ['Authentication'],
      description: 'Request password reset email',
    },
  }, async (request: FastifyRequest, reply: FastifyReply) => {
    const { email } = request.body as any;
    
    try {
      await authService.requestPasswordReset(email);
      
      return { 
        success: true, 
        message: 'If an account with that email exists, a password reset link has been sent.' 
      };
    } catch (error) {
      fastify.log.error(error);
      // Always return success to prevent email enumeration
      return { 
        success: true, 
        message: 'If an account with that email exists, a password reset link has been sent.' 
      };
    }
  });

  // Reset password
  fastify.post('/reset-password', {
    schema: {
      tags: ['Authentication'],
      description: 'Reset password using reset token',
    },
  }, async (request: FastifyRequest, reply: FastifyReply) => {
    const { token, newPassword } = request.body as any;
    
    try {
      const result = await authService.resetPassword(token, newPassword);
      
      if (result.success) {
        return { success: true, message: 'Password reset successfully' };
      } else {
        reply.code(400);
        return result;
      }
    } catch (error) {
      fastify.log.error(error);
      reply.code(500);
      return { success: false, error: { code: 'RESET_ERROR', message: 'Password reset failed' } };
    }
  });
}