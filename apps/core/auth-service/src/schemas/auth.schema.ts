// Authentication schemas for request validation

export const loginSchema = {
  type: 'object',
  properties: {
    email: {
      type: 'string',
      format: 'email',
      description: 'User email address'
    },
    password: {
      type: 'string',
      minLength: 1,
      description: 'User password'
    },
    organizationId: {
      type: 'string',
      description: 'Optional organization ID for multi-tenant setups'
    },
    mfaCode: {
      type: 'string',
      pattern: '^[0-9]{6}$',
      description: 'MFA/TOTP code if required'
    },
    rememberMe: {
      type: 'boolean',
      default: false,
      description: 'Whether to extend session duration'
    }
  },
  required: ['email', 'password'],
  additionalProperties: false
};

export const registerSchema = {
  type: 'object',
  properties: {
    email: {
      type: 'string',
      format: 'email',
      description: 'User email address'
    },
    password: {
      type: 'string',
      minLength: 8,
      description: 'User password (minimum 8 characters)'
    },
    firstName: {
      type: 'string',
      minLength: 1,
      maxLength: 50,
      description: 'User first name'
    },
    lastName: {
      type: 'string',
      minLength: 1,
      maxLength: 50,
      description: 'User last name'
    },
    organizationId: {
      type: 'string',
      description: 'Optional organization ID'
    }
  },
  required: ['email', 'password'],
  additionalProperties: false
};

export const refreshSchema = {
  type: 'object',
  properties: {
    refreshToken: {
      type: 'string',
      minLength: 1,
      description: 'JWT refresh token'
    }
  },
  required: ['refreshToken'],
  additionalProperties: false
};

export const verifyEmailSchema = {
  type: 'object',
  properties: {
    token: {
      type: 'string',
      minLength: 1,
      description: 'Email verification token'
    }
  },
  required: ['token'],
  additionalProperties: false
};

export const resetPasswordRequestSchema = {
  type: 'object',
  properties: {
    email: {
      type: 'string',
      format: 'email',
      description: 'User email address'
    }
  },
  required: ['email'],
  additionalProperties: false
};

export const resetPasswordSchema = {
  type: 'object',
  properties: {
    token: {
      type: 'string',
      minLength: 1,
      description: 'Password reset token'
    },
    newPassword: {
      type: 'string',
      minLength: 8,
      description: 'New password (minimum 8 characters)'
    }
  },
  required: ['token', 'newPassword'],
  additionalProperties: false
};