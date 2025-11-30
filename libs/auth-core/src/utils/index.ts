// Utility functions for authentication system

import { v4 as uuidv4 } from 'uuid';

export class AuthUtils {
  /**
   * Generate unique identifier
   */
  static generateId(): string {
    return uuidv4();
  }

  /**
   * Parse Bearer token from Authorization header
   */
  static parseBearerToken(authHeader: string): string | null {
    if (!authHeader || !authHeader.startsWith('Bearer ')) {
      return null;
    }
    return authHeader.substring(7);
  }

  /**
   * Parse API key from header
   */
  static parseApiKey(authHeader: string, apiKeyHeader?: string): string | null {
    // Check X-API-Key header first
    if (apiKeyHeader) {
      return apiKeyHeader;
    }

    // Check Authorization header with ApiKey prefix
    if (authHeader?.startsWith('ApiKey ')) {
      return authHeader.substring(7);
    }

    return null;
  }

  /**
   * Format user display name
   */
  static formatDisplayName(firstName?: string, lastName?: string, email?: string): string {
    if (firstName && lastName) {
      return `${firstName} ${lastName}`;
    }
    if (firstName) {
      return firstName;
    }
    if (lastName) {
      return lastName;
    }
    if (email) {
      return email.split('@')[0];
    }
    return 'Unknown User';
  }

  /**
   * Check if email domain is allowed
   */
  static isEmailDomainAllowed(email: string, allowedDomains: string[]): boolean {
    if (allowedDomains.length === 0) {
      return true; // No restrictions
    }

    const domain = email.split('@')[1]?.toLowerCase();
    if (!domain) {
      return false;
    }

    return allowedDomains.some(allowedDomain => {
      const normalizedDomain = allowedDomain.toLowerCase();
      
      // Exact match
      if (domain === normalizedDomain) {
        return true;
      }
      
      // Subdomain match (if allowed domain starts with .)
      if (normalizedDomain.startsWith('.') && domain.endsWith(normalizedDomain)) {
        return true;
      }
      
      return false;
    });
  }

  /**
   * Extract IP address from request
   */
  static extractIpAddress(req: any): string {
    // Check for forwarded IPs (behind proxy)
    const forwarded = req.headers['x-forwarded-for'];
    if (forwarded) {
      return forwarded.split(',')[0].trim();
    }

    // Check for real IP (some proxies)
    if (req.headers['x-real-ip']) {
      return req.headers['x-real-ip'];
    }

    // Check for client IP (some CDNs)
    if (req.headers['x-client-ip']) {
      return req.headers['x-client-ip'];
    }

    // Fallback to connection remote address
    return req.connection?.remoteAddress || req.socket?.remoteAddress || 'unknown';
  }

  /**
   * Extract user agent from request
   */
  static extractUserAgent(req: any): string {
    return req.headers['user-agent'] || 'unknown';
  }

  /**
   * Create audit log entry
   */
  static createAuditEntry(
    action: string,
    outcome: 'success' | 'failure',
    userId?: string,
    sessionId?: string,
    ipAddress?: string,
    userAgent?: string,
    details?: any
  ) {
    return {
      id: uuidv4(),
      userId,
      sessionId,
      action,
      resource: 'auth',
      outcome,
      ipAddress: ipAddress || 'unknown',
      userAgent: userAgent || 'unknown',
      details,
      timestamp: new Date()
    };
  }

  /**
   * Mask sensitive data for logging
   */
  static maskSensitiveData(data: any, fields: string[] = ['password', 'token', 'secret']): any {
    if (!data || typeof data !== 'object') {
      return data;
    }

    const masked = { ...data };
    
    fields.forEach(field => {
      if (masked[field]) {
        masked[field] = '***MASKED***';
      }
    });

    return masked;
  }

  /**
   * Calculate password strength score
   */
  static calculatePasswordStrength(password: string): { score: number; feedback: string[] } {
    let score = 0;
    const feedback: string[] = [];

    // Length check
    if (password.length >= 12) {
      score += 2;
    } else if (password.length >= 8) {
      score += 1;
    } else {
      feedback.push('Use at least 8 characters');
    }

    // Character variety checks
    if (/[a-z]/.test(password)) score += 1;
    else feedback.push('Include lowercase letters');

    if (/[A-Z]/.test(password)) score += 1;
    else feedback.push('Include uppercase letters');

    if (/\d/.test(password)) score += 1;
    else feedback.push('Include numbers');

    if (/[^a-zA-Z\d]/.test(password)) score += 1;
    else feedback.push('Include special characters');

    // Common patterns check
    const commonPatterns = [
      /(.)\1{2,}/, // Repeated characters
      /123|234|345|456|567|678|789|890|abc|bcd|cde/, // Sequential patterns
      /password|123456|qwerty|admin/i // Common words
    ];

    if (commonPatterns.some(pattern => pattern.test(password))) {
      score -= 2;
      feedback.push('Avoid common patterns and words');
    }

    return {
      score: Math.max(0, Math.min(10, score)),
      feedback
    };
  }

  /**
   * Generate slug from string
   */
  static generateSlug(text: string): string {
    return text
      .toLowerCase()
      .replace(/[^a-z0-9]+/g, '-')
      .replace(/^-+|-+$/g, '')
      .substring(0, 50);
  }

  /**
   * Validate URL format
   */
  static isValidUrl(url: string): boolean {
    try {
      new URL(url);
      return true;
    } catch {
      return false;
    }
  }

  /**
   * Check if running in production environment
   */
  static isProduction(): boolean {
    return process.env.NODE_ENV === 'production';
  }

  /**
   * Generate CSRF token
   */
  static generateCSRFToken(): string {
    const crypto = require('crypto');
    return crypto.randomBytes(32).toString('hex');
  }

  /**
   * Verify CSRF token
   */
  static verifyCSRFToken(token: string, sessionToken: string): boolean {
    // Simple comparison - in production, use proper CSRF token validation
    return token === sessionToken;
  }
}

export default AuthUtils;