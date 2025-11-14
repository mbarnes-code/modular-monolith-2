/**
 * TypeScript Types for AST Manipulation
 * 
 * Comprehensive type definitions for the generalized ts-morph utilities.
 * Supports all TypeScript project types with executive function accommodations.
 */

import type { CompilerOptions, SourceFile } from 'ts-morph';

/**
 * Project configuration for ts-morph operations
 */
export interface ProjectConfig {
	/** Path to tsconfig.json file */
	tsConfigPath?: string;
	
	/** Skip dependency resolution for faster loading */
	skipDependencies?: boolean;
	
	/** Use in-memory file system for temporary operations */
	useInMemory?: boolean;
	
	/** TypeScript compiler options override */
	compilerOptions?: CompilerOptions;
	
	/** Include patterns for file loading */
	includePatterns?: string[];
	
	/** Exclude patterns for file loading */
	excludePatterns?: string[];
}

/**
 * Context for AST operations with error handling and logging
 */
export interface ASTOperationContext {
	/** Enable error logging */
	logErrors?: boolean;
	
	/** Force string conversion for non-string properties */
	forceStringConversion?: boolean;
	
	/** Update interface type annotations */
	updateInterfaceTypes?: boolean;
	
	/** Preserve code formatting */
	preserveFormatting?: boolean;
	
	/** Validation mode for operations */
	validationMode?: 'strict' | 'lenient' | 'none';
	
	/** Target domain for context-aware operations */
	domain?: 'security' | 'productivity' | 'mtg' | 'infrastructure';
}

/**
 * Code generation hints for AI enhancement
 */
export interface CodeGenerationHint {
	/** Type of hint */
	type: 'security' | 'performance' | 'accessibility' | 'executive_function' | 'maintainability';
	
	/** Human-readable suggestion */
	suggestion: string;
	
	/** Line number where hint applies */
	location: number;
	
	/** Impact assessment */
	impact: 'Low' | 'Medium' | 'High' | 'Critical';
	
	/** Automated fix available */
	autoFixable?: boolean;
	
	/** Code snippet for fix */
	fixCode?: string;
}

/**
 * Template configuration for code generation
 */
export interface CodeTemplate {
	/** Template name */
	name: string;
	
	/** Template category */
	category: 'component' | 'service' | 'utility' | 'test' | 'config';
	
	/** Template content with placeholders */
	template: string;
	
	/** Required variables for template */
	variables: Record<string, TemplateVariable>;
	
	/** Output file extension */
	fileExtension: string;
	
	/** Post-processing hooks */
	postProcess?: Array<(content: string, variables: Record<string, any>) => string>;
}

/**
 * Template variable definition
 */
export interface TemplateVariable {
	/** Variable type */
	type: 'string' | 'boolean' | 'number' | 'array' | 'object';
	
	/** Variable description */
	description: string;
	
	/** Default value */
	default?: any;
	
	/** Required variable */
	required?: boolean;
	
	/** Validation pattern (for strings) */
	pattern?: string;
	
	/** Possible values (for enums) */
	options?: string[];
}

/**
 * Refactoring operation definition
 */
export interface RefactoringOperation {
	/** Operation name */
	name: string;
	
	/** Operation description */
	description: string;
	
	/** Target patterns to match */
	patterns: Array<{
		/** AST node type to match */
		nodeType: string;
		
		/** Additional conditions */
		conditions?: Record<string, any>;
	}>;
	
	/** Transformation function */
	transform: (sourceFile: SourceFile, matches: any[]) => boolean;
	
	/** Safety check function */
	safetyCheck?: (sourceFile: SourceFile) => boolean;
	
	/** Rollback function */
	rollback?: (sourceFile: SourceFile) => boolean;
}

/**
 * Analysis result for code quality metrics
 */
export interface CodeAnalysisResult {
	/** File path */
	filePath: string;
	
	/** Analysis timestamp */
	timestamp: Date;
	
	/** Quality metrics */
	metrics: {
		complexity: number;
		maintainability: number;
		securityScore: number;
		accessibilityScore: number;
		executiveFunctionScore: number;
	};
	
	/** Generated hints */
	hints: CodeGenerationHint[];
	
	/** Detected patterns */
	patterns: DetectedPattern[];
	
	/** Overall health score */
	healthScore: number;
}

/**
 * Detected code pattern
 */
export interface DetectedPattern {
	/** Pattern type */
	type: 'anti-pattern' | 'good-practice' | 'security-risk' | 'performance-issue' | 'accessibility-issue';
	
	/** Pattern name */
	name: string;
	
	/** Pattern description */
	description: string;
	
	/** Location in file */
	location: {
		startLine: number;
		endLine: number;
		startColumn?: number;
		endColumn?: number;
	};
	
	/** Severity level */
	severity: 'info' | 'warning' | 'error' | 'critical';
	
	/** Suggested fix */
	suggestedFix?: string;
}

/**
 * Batch processing configuration
 */
export interface BatchProcessingConfig {
	/** Files to process */
	files: string[];
	
	/** Operations to apply */
	operations: RefactoringOperation[];
	
	/** Parallel processing limit */
	parallelism: number;
	
	/** Continue on errors */
	continueOnError: boolean;
	
	/** Create backup files */
	createBackups: boolean;
	
	/** Progress callback */
	onProgress?: (progress: BatchProgress) => void;
	
	/** Error callback */
	onError?: (error: BatchError) => void;
}

/**
 * Batch processing progress
 */
export interface BatchProgress {
	/** Total files to process */
	total: number;
	
	/** Files processed */
	processed: number;
	
	/** Files with errors */
	errors: number;
	
	/** Current file being processed */
	currentFile?: string;
	
	/** Estimated time remaining (ms) */
	estimatedTimeRemaining?: number;
}

/**
 * Batch processing error
 */
export interface BatchError {
	/** File path */
	filePath: string;
	
	/** Error message */
	message: string;
	
	/** Error details */
	details?: any;
	
	/** Operation that failed */
	operation?: string;
	
	/** Recoverable error */
	recoverable: boolean;
}

/**
 * AI Enhancement configuration
 */
export interface AIEnhancementConfig {
	/** Enable AI-driven suggestions */
	enableSuggestions: boolean;
	
	/** Enable automatic fixes */
	enableAutoFix: boolean;
	
	/** AI model preferences */
	modelPreferences: {
		/** Preferred model for code generation */
		codeGeneration?: string;
		
		/** Preferred model for analysis */
		analysis?: string;
		
		/** Preferred model for refactoring */
		refactoring?: string;
	};
	
	/** Context window size for AI operations */
	contextWindowSize: number;
	
	/** Maximum tokens for AI responses */
	maxTokens: number;
	
	/** Temperature for AI creativity */
	temperature: number;
}

/**
 * Security analysis configuration
 */
export interface SecurityAnalysisConfig {
	/** Enable vulnerability scanning */
	enableVulnerabilityScanning: boolean;
	
	/** Security rules to apply */
	rules: SecurityRule[];
	
	/** Severity threshold for reporting */
	severityThreshold: 'low' | 'medium' | 'high' | 'critical';
	
	/** Include third-party dependencies */
	includeThirdParty: boolean;
}

/**
 * Security rule definition
 */
export interface SecurityRule {
	/** Rule ID */
	id: string;
	
	/** Rule name */
	name: string;
	
	/** Rule description */
	description: string;
	
	/** Pattern to match */
	pattern: string | RegExp;
	
	/** Rule severity */
	severity: 'low' | 'medium' | 'high' | 'critical';
	
	/** Suggested fix */
	suggestedFix?: string;
	
	/** Rule category */
	category: 'injection' | 'xss' | 'auth' | 'crypto' | 'data-leak' | 'other';
}

/**
 * Executive function accommodation settings
 */
export interface ExecutiveFunctionConfig {
	/** Maximum cognitive complexity per function */
	maxComplexityPerFunction: number;
	
	/** Maximum parameters per function */
	maxParametersPerFunction: number;
	
	/** Maximum methods per class */
	maxMethodsPerClass: number;
	
	/** Enforce consistent naming conventions */
	enforceNamingConventions: boolean;
	
	/** Require function documentation */
	requireFunctionDocs: boolean;
	
	/** Maximum nesting depth */
	maxNestingDepth: number;
	
	/** Enforce single responsibility principle */
	enforceSingleResponsibility: boolean;
}

/**
 * Cross-domain integration configuration
 */
export interface CrossDomainConfig {
	/** Domain mappings */
	domainMappings: Record<string, DomainConfig>;
	
	/** Shared patterns between domains */
	sharedPatterns: string[];
	
	/** Cross-domain validation rules */
	validationRules: CrossDomainRule[];
}

/**
 * Domain-specific configuration
 */
export interface DomainConfig {
	/** Domain name */
	name: string;
	
	/** Domain-specific patterns */
	patterns: string[];
	
	/** Domain-specific rules */
	rules: Record<string, any>;
	
	/** Integration endpoints */
	integrationPoints: string[];
}

/**
 * Cross-domain validation rule
 */
export interface CrossDomainRule {
	/** Rule name */
	name: string;
	
	/** Source domain */
	sourceDomain: string;
	
	/** Target domain */
	targetDomain: string;
	
	/** Validation function */
	validate: (sourceCode: string, targetCode: string) => boolean;
	
	/** Error message template */
	errorMessage: string;
}

/**
 * Code generation request
 */
export interface CodeGenerationRequest {
	/** Generation type */
	type: 'component' | 'service' | 'utility' | 'test' | 'migration';
	
	/** Target framework/library */
	framework: 'react' | 'angular' | 'vue' | 'node' | 'fastapi' | 'generic';
	
	/** Generation parameters */
	parameters: Record<string, any>;
	
	/** Template to use */
	template?: string;
	
	/** Output configuration */
	output: {
		/** Output directory */
		directory: string;
		
		/** File naming pattern */
		fileNamePattern: string;
		
		/** Overwrite existing files */
		overwrite: boolean;
	};
	
	/** Post-generation hooks */
	postGeneration?: Array<(filePath: string, content: string) => void>;
}

/**
 * Code generation response
 */
export interface CodeGenerationResponse {
	/** Success status */
	success: boolean;
	
	/** Generated files */
	generatedFiles: string[];
	
	/** Generation errors */
	errors: string[];
	
	/** Generation warnings */
	warnings: string[];
	
	/** Generation metadata */
	metadata: {
		/** Generation timestamp */
		timestamp: Date;
		
		/** Template used */
		template?: string;
		
		/** AI model used */
		aiModel?: string;
		
		/** Generation time (ms) */
		generationTime: number;
	};
}