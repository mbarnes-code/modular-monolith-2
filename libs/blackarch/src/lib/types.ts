// BlackArch Package Information
export interface BlackArchPackage {
  name: string;
  version: string;
  release: string;
  description: string;
  url: string;
  license: string[];
  arch: string[];
  depends: string[];
  groups: string[];
  path: string;
}

// Repository Statistics
export interface BlackArchStats {
  total: number;
  official: number;
  broken: number;
  working: number;
}

// Pagination Information
export interface Pagination {
  page: number;
  limit: number;
  total: number;
  totalPages: number;
  hasNext: boolean;
  hasPrev: boolean;
}

// Paginated Response
export interface PaginatedResponse<T> {
  success: boolean;
  data: T[];
  pagination: Pagination;
  error?: string;
}

// API Response wrapper
export interface ApiResponse<T = any> {
  success: boolean;
  data?: T;
  error?: string;
  message?: string;
}

// Search Result
export interface SearchResult {
  keyword: string;
  packages: string[];
  total: number;
}

// Service Configuration
export interface BlackArchConfig {
  repositoryPath?: string;
  maxSearchResults?: number;
  defaultPageSize?: number;
}

// Error Types
export enum BlackArchErrorType {
  FILE_NOT_FOUND = 'FILE_NOT_FOUND',
  PARSE_ERROR = 'PARSE_ERROR',
  INVALID_PACKAGE = 'INVALID_PACKAGE',
  REPOSITORY_ERROR = 'REPOSITORY_ERROR'
}

export class BlackArchError extends Error {
  public readonly type?: BlackArchErrorType;
  public override readonly cause?: Error;

  constructor(
    message: string,
    type?: BlackArchErrorType,
    cause?: Error
  ) {
    super(message);
    this.name = 'BlackArchError';
    this.type = type;
    this.cause = cause;
  }
}