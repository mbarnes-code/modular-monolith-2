/**
 * TypeScript Code Intelligence Library - Main Entry Point
 * 
 * Enhanced TypeScript AST manipulation and code intelligence tools.
 * Generalized from n8n Node CLI for universal TypeScript project support.
 * 
 * Features:
 * - Project-agnostic AST operations
 * - AI-enhanced code generation
 * - Executive function accommodations (ADHD-friendly patterns)
 * - Security-first development practices
 * - Cross-domain pattern analysis
 * - Batch processing with rollback capabilities
 * 
 * Zero Dependencies Promise:
 * - All functionality works standalone
 * - Graceful degradation if AI services unavailable
 * - Preserves existing codebases without breaking changes
 */

// Core AST utilities
export {
	loadSourceFile,
	loadProject,
	updateStringProperty,
	getChildObjectLiteral,
	updateArrayProperty,
	updateClassDeclaration,
	updateInterfaceDeclaration,
	updateImports,
	generateCodeHints,
	batchProcess,
	analyzeCodePatterns,
} from './ast-utils';

// Domain-specific operations
export {
	updateApiServiceClass,
	updateReactComponent,
	updateFastApiService,
	updateAuthConfiguration,
	updateDatabaseModel,
	updateConfigurationFile,
	updateTestFile,
	updateMigrationFile,
	applyExecutiveFunctionAccommodations,
	applySecurityBestPractices,
	applyCrossDomainPatterns,
	generateCodeWithAI,
	batchRefactor,
	generateFromTemplate,
} from './domain-operations';

// Type definitions
export type {
	ProjectConfig,
	ASTOperationContext,
	CodeGenerationHint,
	CodeTemplate,
	TemplateVariable,
	RefactoringOperation,
	CodeAnalysisResult,
	DetectedPattern,
	BatchProcessingConfig,
	BatchProgress,
	BatchError,
	AIEnhancementConfig,
	SecurityAnalysisConfig,
	SecurityRule,
	ExecutiveFunctionConfig,
	CrossDomainConfig,
	DomainConfig,
	CrossDomainRule,
	CodeGenerationRequest,
	CodeGenerationResponse,
} from './types';

// Re-export ts-morph types for convenience
export type {
	Project,
	SourceFile,
	ClassDeclaration,
	InterfaceDeclaration,
	FunctionDeclaration,
	VariableDeclaration,
	PropertyAssignment,
	PropertyDeclaration,
	ObjectLiteralExpression,
	ArrayLiteralExpression,
	SyntaxKind,
} from 'ts-morph';

// Version and metadata
export const VERSION = '1.0.0';
export const DESCRIPTION = 'Enhanced TypeScript AST manipulation and code intelligence';

/**
 * Quick-start utility for common operations
 */
export class CodeIntelligence {
	private static instance: CodeIntelligence;
	
	public static getInstance(): CodeIntelligence {
		if (!CodeIntelligence.instance) {
			CodeIntelligence.instance = new CodeIntelligence();
		}
		return CodeIntelligence.instance;
	}
	
	/**
	 * Quick file analysis
	 */
	public analyzeFile(filePath: string) {
		const sourceFile = loadSourceFile(filePath);
		return analyzeCodePatterns(sourceFile);
	}
	
	/**
	 * Quick class update
	 */
	public updateClass(filePath: string, className: string, updates: any) {
		const sourceFile = loadSourceFile(filePath);
		return updateClassDeclaration({ sourceFile, className, updates });
	}
	
	/**
	 * Quick configuration update
	 */
	public updateConfig(filePath: string, updates: Record<string, any>) {
		return updateConfigurationFile({ configPath: filePath, updates });
	}
}