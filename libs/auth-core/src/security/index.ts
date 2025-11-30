// Security utilities for password hashing, validation, etc.

import * as bcrypt from 'bcrypt';
import { PasswordPolicy } from '../types';

export class SecurityUtils {
  private bcryptRounds: number;

  constructor(bcryptRounds: number = 12) {
    this.bcryptRounds = bcryptRounds;
  }

  /**
   * Hash password using bcrypt
   */
  async hashPassword(password: string): Promise<string> {
    return bcrypt.hash(password, this.bcryptRounds);
  }

  /**
   * Verify password against hash
   */
  async verifyPassword(password: string, hash: string): Promise<boolean> {
    return bcrypt.compare(password, hash);
  }

  /**
   * Validate password against policy
   */
  validatePassword(password: string, policy: PasswordPolicy): { valid: boolean; errors: string[] } {
    const errors: string[] = [];

    if (password.length < policy.minLength) {
      errors.push(`Password must be at least ${policy.minLength} characters long`);
    }

    if (policy.requireUppercase && !/[A-Z]/.test(password)) {
      errors.push('Password must contain at least one uppercase letter');
    }

    if (policy.requireLowercase && !/[a-z]/.test(password)) {
      errors.push('Password must contain at least one lowercase letter');
    }

    if (policy.requireNumbers && !/\d/.test(password)) {
      errors.push('Password must contain at least one number');
    }

    if (policy.requireSpecialChars && !/[!@#$%^&*(),.?":{}|<>]/.test(password)) {
      errors.push('Password must contain at least one special character');
    }

    return {
      valid: errors.length === 0,
      errors
    };
  }

  /**
   * Generate secure random password
   */
  generateSecurePassword(length: number = 16, includeSymbols: boolean = true): string {
    const lowercase = 'abcdefghijklmnopqrstuvwxyz';
    const uppercase = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
    const numbers = '0123456789';
    const symbols = '!@#$%^&*(),.?":{}|<>';

    let charset = lowercase + uppercase + numbers;
    if (includeSymbols) {
      charset += symbols;
    }

    let password = '';
    
    // Ensure at least one character from each required set
    password += lowercase[Math.floor(Math.random() * lowercase.length)];
    password += uppercase[Math.floor(Math.random() * uppercase.length)];
    password += numbers[Math.floor(Math.random() * numbers.length)];
    
    if (includeSymbols) {
      password += symbols[Math.floor(Math.random() * symbols.length)];
    }

    // Fill remaining length with random characters
    for (let i = password.length; i < length; i++) {
      password += charset[Math.floor(Math.random() * charset.length)];
    }

    // Shuffle the password
    return password.split('').sort(() => Math.random() - 0.5).join('');
  }

  /**
   * Generate secure random token
   */
  generateSecureToken(length: number = 32): string {
    const crypto = require('crypto');
    return crypto.randomBytes(length).toString('hex');
  }

  /**
   * Hash sensitive data (for storage)
   */
  hashSensitiveData(data: string, salt: string): string {
    const crypto = require('crypto');
    return crypto.createHash('sha256').update(data + salt).digest('hex');
  }

  /**
   * Generate TOTP secret for MFA
   */
  generateTOTPSecret(): string {
    const crypto = require('crypto');
    return crypto.randomBytes(20).toString('base32');
  }

  /**
   * Verify TOTP code
   */
  verifyTOTPCode(secret: string, token: string, window: number = 1): boolean {
    // This would require a TOTP library like 'speakeasy'
    // Implementation placeholder
    throw new Error('TOTP verification not implemented - requires speakeasy library');
  }

  /**
   * Generate email verification token
   */
  generateEmailVerificationToken(): string {
    return this.generateSecureToken(32);
  }

  /**
   * Generate password reset token
   */
  generatePasswordResetToken(): string {
    return this.generateSecureToken(32);
  }

  /**
   * Check if password has been compromised (basic check)
   */
  async checkPasswordCompromise(password: string): Promise<boolean> {
    // This could integrate with HaveIBeenPwned API or similar
    // For now, return false (not compromised)
    return false;
  }

  /**
   * Sanitize input to prevent XSS
   */
  sanitizeInput(input: string): string {
    return input
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#x27;')
      .replace(/\//g, '&#x2F;');
  }

  /**
   * Validate email format
   */
  isValidEmail(email: string): boolean {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
  }

  /**
   * Rate limiting check
   */
  async checkRateLimit(identifier: string, maxAttempts: number, windowMs: number): Promise<{ allowed: boolean; remaining: number; resetTime: Date }> {
    // This would integrate with Redis for rate limiting
    // Implementation placeholder
    return {
      allowed: true,
      remaining: maxAttempts - 1,
      resetTime: new Date(Date.now() + windowMs)
    };
  }
}

export default SecurityUtils;