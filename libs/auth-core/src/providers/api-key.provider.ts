// API Key Provider implementation

import { createHash, randomBytes } from 'crypto';
import { AuthConfig } from '../config';
import { ApiKey, Permission, User } from '../types';

export class ApiKeyProvider {
  private config: AuthConfig;

  constructor(config: AuthConfig) {
    this.config = config;
  }

  /**
   * Generate new API key for a user
   */
  async generateApiKey(
    user: User,
    name: string,
    permissions: Permission[],
    expiresAt?: Date
  ): Promise<{ apiKey: ApiKey; rawKey: string }> {
    // Generate random key
    const rawKey = this.generateRawKey();
    const keyHash = this.hashKey(rawKey);

    const apiKey: ApiKey = {
      id: this.generateKeyId(),
      name,
      keyHash,
      userId: user.id,
      organizationId: user.organizationId,
      permissions,
      isActive: true,
      expiresAt,
      lastUsedAt: undefined,
      createdAt: new Date(),
    };

    // Store in database (implement based on your data layer)
    await this.storeApiKey(apiKey);

    return { apiKey, rawKey };
  }

  /**
   * Verify API key and return associated user/permissions
   */
  async verifyApiKey(rawKey: string): Promise<{ user: User; apiKey: ApiKey } | null> {
    const keyHash = this.hashKey(rawKey);
    
    // Find API key by hash
    const apiKey = await this.findApiKeyByHash(keyHash);
    
    if (!apiKey) {
      return null;
    }

    // Check if key is active
    if (!apiKey.isActive) {
      throw new Error('API key is disabled');
    }

    // Check if key has expired
    if (apiKey.expiresAt && new Date() > apiKey.expiresAt) {
      throw new Error('API key has expired');
    }

    // Get associated user
    const user = await this.getUserById(apiKey.userId);
    if (!user || !user.isActive) {
      throw new Error('Associated user is inactive');
    }

    // Update last used timestamp
    await this.updateLastUsed(apiKey.id);

    return { user, apiKey };
  }

  /**
   * Revoke API key
   */
  async revokeApiKey(keyId: string, userId: string): Promise<void> {
    const apiKey = await this.findApiKeyById(keyId);
    
    if (!apiKey) {
      throw new Error('API key not found');
    }

    if (apiKey.userId !== userId) {
      throw new Error('API key does not belong to user');
    }

    await this.updateApiKeyStatus(keyId, false);
  }

  /**
   * Get all API keys for a user
   */
  async getUserApiKeys(userId: string): Promise<ApiKey[]> {
    return this.findApiKeysByUserId(userId);
  }

  /**
   * Rotate API key (generate new key, keep same permissions)
   */
  async rotateApiKey(keyId: string, userId: string): Promise<{ apiKey: ApiKey; rawKey: string }> {
    const existingKey = await this.findApiKeyById(keyId);
    
    if (!existingKey) {
      throw new Error('API key not found');
    }

    if (existingKey.userId !== userId) {
      throw new Error('API key does not belong to user');
    }

    // Revoke old key
    await this.revokeApiKey(keyId, userId);

    // Get user for new key generation
    const user = await this.getUserById(userId);
    if (!user) {
      throw new Error('User not found');
    }

    // Generate new key with same permissions
    return this.generateApiKey(
      user,
      existingKey.name,
      existingKey.permissions,
      existingKey.expiresAt
    );
  }

  /**
   * Check if API key has specific permission
   */
  hasPermission(apiKey: ApiKey, resource: string, action: string): boolean {
    return apiKey.permissions.some(
      permission => permission.resource === resource && permission.action === action
    );
  }

  /**
   * Generate raw API key string
   */
  private generateRawKey(): string {
    const prefix = this.config.apiKey.keyPrefix || 'mm';
    const randomPart = randomBytes(32).toString('hex');
    return `${prefix}_${randomPart}`;
  }

  /**
   * Hash API key for storage
   */
  private hashKey(rawKey: string): string {
    return createHash('sha256').update(rawKey + this.config.apiKey.hashSalt).digest('hex');
  }

  /**
   * Generate unique API key ID
   */
  private generateKeyId(): string {
    return randomBytes(16).toString('hex');
  }

  /**
   * Store API key in database (implement based on your data layer)
   */
  private async storeApiKey(apiKey: ApiKey): Promise<void> {
    // Implementation depends on your database service
    throw new Error('storeApiKey not implemented - integrate with database service');
  }

  /**
   * Find API key by hash (implement based on your data layer)
   */
  private async findApiKeyByHash(keyHash: string): Promise<ApiKey | null> {
    // Implementation depends on your database service
    throw new Error('findApiKeyByHash not implemented - integrate with database service');
  }

  /**
   * Find API key by ID (implement based on your data layer)
   */
  private async findApiKeyById(keyId: string): Promise<ApiKey | null> {
    // Implementation depends on your database service
    throw new Error('findApiKeyById not implemented - integrate with database service');
  }

  /**
   * Find API keys by user ID (implement based on your data layer)
   */
  private async findApiKeysByUserId(userId: string): Promise<ApiKey[]> {
    // Implementation depends on your database service
    throw new Error('findApiKeysByUserId not implemented - integrate with database service');
  }

  /**
   * Update API key status (implement based on your data layer)
   */
  private async updateApiKeyStatus(keyId: string, isActive: boolean): Promise<void> {
    // Implementation depends on your database service
    throw new Error('updateApiKeyStatus not implemented - integrate with database service');
  }

  /**
   * Update last used timestamp (implement based on your data layer)
   */
  private async updateLastUsed(keyId: string): Promise<void> {
    // Implementation depends on your database service
    throw new Error('updateLastUsed not implemented - integrate with database service');
  }

  /**
   * Get user by ID (implement based on your user service)
   */
  private async getUserById(userId: string): Promise<User | null> {
    // Implementation depends on your user service
    throw new Error('getUserById not implemented - integrate with user service');
  }
}

export default ApiKeyProvider;