// Authentication service implementation

import {
    AuthRequest,
    AuthResponse,
    AuthUtils,
    JWTProvider,
    SecurityUtils,
    SessionProvider,
    User
} from '@modular-monolith/auth-core';
import { EmailService } from './email.service';
import { UserService } from './user.service';

export interface RegisterRequest {
  email: string;
  password: string;
  firstName?: string;
  lastName?: string;
  organizationId?: string;
}

export class AuthService {
  private jwtProvider: JWTProvider;
  private sessionProvider: SessionProvider;
  private userService: UserService;
  private securityUtils: SecurityUtils;
  private emailService: EmailService;

  constructor(
    jwtProvider: JWTProvider,
    sessionProvider: SessionProvider,
    userService: UserService
  ) {
    this.jwtProvider = jwtProvider;
    this.sessionProvider = sessionProvider;
    this.userService = userService;
    this.securityUtils = new SecurityUtils();
    this.emailService = new EmailService();
  }

  /**
   * Authenticate user with email/password
   */
  async authenticateUser(
    authRequest: AuthRequest,
    ipAddress: string,
    userAgent: string
  ): Promise<AuthResponse> {
    try {
      // Find user by email
      const user = await this.userService.findByEmail(authRequest.email);
      
      if (!user) {
        return {
          success: false,
          error: { code: 'INVALID_CREDENTIALS', message: 'Invalid email or password' }
        };
      }

      // Check if user is active
      if (!user.isActive) {
        return {
          success: false,
          error: { code: 'ACCOUNT_DISABLED', message: 'Account is disabled' }
        };
      }

      // Check if account is locked
      if (user.lockedUntil && new Date() < user.lockedUntil) {
        return {
          success: false,
          error: { code: 'ACCOUNT_LOCKED', message: 'Account is temporarily locked' }
        };
      }

      // Verify password
      if (!user.passwordHash || !await this.securityUtils.verifyPassword(authRequest.password, user.passwordHash)) {
        // Increment login attempts
        await this.userService.incrementLoginAttempts(user.id);
        
        return {
          success: false,
          error: { code: 'INVALID_CREDENTIALS', message: 'Invalid email or password' }
        };
      }

      // Check if MFA is required
      if (user.mfaEnabled && !authRequest.mfaCode) {
        return {
          success: false,
          requiresMfa: true,
          mfaChallenge: {
            type: 'totp',
            challengeId: AuthUtils.generateId(),
            expiresAt: new Date(Date.now() + 5 * 60 * 1000) // 5 minutes
          }
        };
      }

      // Verify MFA code if provided
      if (user.mfaEnabled && authRequest.mfaCode) {
        const mfaValid = await this.verifyMFACode(user, authRequest.mfaCode);
        if (!mfaValid) {
          return {
            success: false,
            error: { code: 'INVALID_MFA', message: 'Invalid MFA code' }
          };
        }
      }

      // Generate tokens
      const tokens = await this.jwtProvider.generateTokens(user, authRequest.organizationId);

      // Create session
      const session = await this.sessionProvider.createSession(
        user,
        ipAddress,
        userAgent,
        authRequest.organizationId
      );

      // Mark MFA as verified in session if MFA was used
      if (user.mfaEnabled && authRequest.mfaCode) {
        await this.sessionProvider.setMfaVerified(session.sessionId);
      }

      // Reset login attempts on successful login
      await this.userService.resetLoginAttempts(user.id);

      // Update last login time
      await this.userService.updateLastLogin(user.id);

      return {
        success: true,
        user,
        tokens,
        session
      };

    } catch (error) {
      console.error('Authentication error:', error);
      return {
        success: false,
        error: { code: 'AUTH_ERROR', message: 'Authentication failed' }
      };
    }
  }

  /**
   * Register new user
   */
  async registerUser(registerRequest: RegisterRequest): Promise<AuthResponse> {
    try {
      // Check if user already exists
      const existingUser = await this.userService.findByEmail(registerRequest.email);
      if (existingUser) {
        return {
          success: false,
          error: { code: 'USER_EXISTS', message: 'User with this email already exists' }
        };
      }

      // Validate password strength (implement based on your password policy)
      const passwordValidation = this.securityUtils.validatePassword(
        registerRequest.password,
        {
          minLength: 8,
          requireUppercase: true,
          requireLowercase: true,
          requireNumbers: true,
          requireSpecialChars: true
        }
      );

      if (!passwordValidation.valid) {
        return {
          success: false,
          error: { 
            code: 'WEAK_PASSWORD', 
            message: 'Password does not meet requirements',
            details: passwordValidation.errors
          }
        };
      }

      // Hash password
      const passwordHash = await this.securityUtils.hashPassword(registerRequest.password);

      // Generate email verification token
      const emailVerificationToken = this.securityUtils.generateEmailVerificationToken();

      // Create user
      const user = await this.userService.create({
        email: registerRequest.email,
        passwordHash,
        firstName: registerRequest.firstName,
        lastName: registerRequest.lastName,
        organizationId: registerRequest.organizationId,
        emailVerificationToken,
        emailVerificationExpiresAt: new Date(Date.now() + 24 * 60 * 60 * 1000) // 24 hours
      });

      // Send verification email
      await this.emailService.sendVerificationEmail(user.email, emailVerificationToken);

      return {
        success: true,
        user
      };

    } catch (error) {
      console.error('Registration error:', error);
      return {
        success: false,
        error: { code: 'REGISTRATION_ERROR', message: 'Registration failed' }
      };
    }
  }

  /**
   * Verify email address
   */
  async verifyEmail(token: string): Promise<{ success: boolean; error?: any }> {
    try {
      const user = await this.userService.findByEmailVerificationToken(token);
      
      if (!user) {
        return { success: false, error: { code: 'INVALID_TOKEN', message: 'Invalid verification token' } };
      }

      if (user.emailVerificationExpiresAt && new Date() > user.emailVerificationExpiresAt) {
        return { success: false, error: { code: 'TOKEN_EXPIRED', message: 'Verification token has expired' } };
      }

      await this.userService.verifyEmail(user.id);
      
      return { success: true };
    } catch (error) {
      console.error('Email verification error:', error);
      return { success: false, error: { code: 'VERIFICATION_ERROR', message: 'Email verification failed' } };
    }
  }

  /**
   * Request password reset
   */
  async requestPasswordReset(email: string): Promise<void> {
    const user = await this.userService.findByEmail(email);
    
    if (user && user.isActive) {
      const resetToken = this.securityUtils.generatePasswordResetToken();
      const expiresAt = new Date(Date.now() + 60 * 60 * 1000); // 1 hour
      
      await this.userService.setPasswordResetToken(user.id, resetToken, expiresAt);
      await this.emailService.sendPasswordResetEmail(user.email, resetToken);
    }
    
    // Always return void to prevent email enumeration
  }

  /**
   * Reset password using reset token
   */
  async resetPassword(token: string, newPassword: string): Promise<{ success: boolean; error?: any }> {
    try {
      const user = await this.userService.findByPasswordResetToken(token);
      
      if (!user) {
        return { success: false, error: { code: 'INVALID_TOKEN', message: 'Invalid reset token' } };
      }

      if (user.passwordResetExpiresAt && new Date() > user.passwordResetExpiresAt) {
        return { success: false, error: { code: 'TOKEN_EXPIRED', message: 'Reset token has expired' } };
      }

      // Validate new password
      const passwordValidation = this.securityUtils.validatePassword(
        newPassword,
        {
          minLength: 8,
          requireUppercase: true,
          requireLowercase: true,
          requireNumbers: true,
          requireSpecialChars: true
        }
      );

      if (!passwordValidation.valid) {
        return {
          success: false,
          error: { 
            code: 'WEAK_PASSWORD', 
            message: 'Password does not meet requirements',
            details: passwordValidation.errors
          }
        };
      }

      // Hash new password
      const passwordHash = await this.securityUtils.hashPassword(newPassword);

      // Update password and clear reset token
      await this.userService.updatePassword(user.id, passwordHash);
      
      return { success: true };
    } catch (error) {
      console.error('Password reset error:', error);
      return { success: false, error: { code: 'RESET_ERROR', message: 'Password reset failed' } };
    }
  }

  /**
   * Verify MFA code
   */
  private async verifyMFACode(user: User, code: string): Promise<boolean> {
    if (!user.mfaSecret) {
      return false;
    }

    try {
      return this.securityUtils.verifyTOTPCode(user.mfaSecret, code);
    } catch (error) {
      console.error('MFA verification error:', error);
      return false;
    }
  }
}