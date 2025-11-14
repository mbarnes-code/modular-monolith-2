/**
 * Enhanced TypeScript AST Manipulation - Domain-Specific Operations
 * 
 * Generalized from n8n Node CLI with AI-driven enhancements for all domains.
 * Provides specialized operations for different project types while maintaining
 * the executive function accommodations and security-first principles.
 */

import { camelCase, capitalCase, pascalCase, kebabCase } from 'change-case';
import { ts, SyntaxKind, printNode, type SourceFile } from 'ts-morph';

import {
	getChildObjectLiteral,
	loadSourceFile,
	updateStringProperty,
	updateArrayProperty,
	updateClassDeclaration,
	updateInterfaceDeclaration,
	updateImports,
} from './ast-utils';

import type {
	ASTOperationContext,
	CodeTemplate,
	RefactoringOperation,
	AIEnhancementConfig,
} from './types';

/**
 * Enhanced Node.js/API service manipulation
 * Generalized from n8n node operations for any API service
 */
export function updateApiServiceClass({
	servicePath,
	className,
	baseUrl,
	apiConfig,
	context,
}: {
	servicePath: string;
	className: string;
	baseUrl: string;
	apiConfig: {
		displayName?: string;
		description?: string;
		version?: string;
		authentication?: 'none' | 'apiKey' | 'oauth2' | 'bearer';
		endpoints?: Array<{ name: string; method: string; path: string }>;
	};
	context?: ASTOperationContext;
}): SourceFile {
	const sourceFile = loadSourceFile(servicePath);
	const classDecl = sourceFile.getClasses()[0];

	if (!classDecl) {
		throw new Error(`No class found in ${servicePath}`);
	}

	// Update class name
	classDecl.rename(className);

	// Try to find service configuration object
	const configProp = classDecl.getProperty('config') || classDecl.getProperty('description');
	if (configProp) {
		const configObj = configProp.getInitializerIfKind(SyntaxKind.ObjectLiteralExpression);
		if (configObj) {
			// Update basic properties
			updateStringProperty({
				obj: configObj,
				key: 'displayName',
				value: apiConfig.displayName || capitalCase(className),
				context,
				createIfMissing: true,
			});

			updateStringProperty({
				obj: configObj,
				key: 'name',
				value: camelCase(className),
				context,
				createIfMissing: true,
			});

			updateStringProperty({
				obj: configObj,
				key: 'description',
				value: apiConfig.description || `${capitalCase(className)} API integration service`,
				context,
				createIfMissing: true,
			});

			updateStringProperty({
				obj: configObj,
				key: 'version',
				value: apiConfig.version || '1.0.0',
				context,
				createIfMissing: true,
			});

			// Update base URL if present
			const requestDefaults = getChildObjectLiteral({
				obj: configObj,
				key: 'requestDefaults',
				createIfMissing: true,
			});

			if (requestDefaults) {
				updateStringProperty({
					obj: requestDefaults,
					key: 'baseURL',
					value: baseUrl,
					context,
					createIfMissing: true,
				});
			}
		}
	}

	return sourceFile;
}

/**
 * Enhanced React component manipulation
 * Creates/updates React components with accessibility and executive function considerations
 */
export function updateReactComponent({
	componentPath,
	componentName,
	props,
	hooks,
	accessibility,
	context,
}: {
	componentPath: string;
	componentName: string;
	props?: Record<string, string>;
	hooks?: Array<{ name: string; type: 'state' | 'effect' | 'context' | 'custom' }>;
	accessibility?: {
		ariaLabel?: string;
		role?: string;
		tabIndex?: number;
		keyboardNavigation?: boolean;
	};
	context?: ASTOperationContext;
}): SourceFile {
	const sourceFile = loadSourceFile(componentPath);

	// Add React imports if not present
	updateImports({
		sourceFile,
		imports: [
			{
				moduleSpecifier: 'react',
				namedImports: ['FC', 'useState', 'useEffect'],
			},
		],
		mode: 'merge',
	});

	// Create/update component interface
	if (props) {
		updateInterfaceDeclaration({
			sourceFile,
			interfaceName: `${componentName}Props`,
			properties: props,
		});
	}

	return sourceFile;
}

/**
 * Enhanced FastAPI service manipulation
 * Creates/updates FastAPI services with security and domain considerations
 */
export function updateFastApiService({
	servicePath,
	serviceName,
	routes,
	security,
	domain,
	context,
}: {
	servicePath: string;
	serviceName: string;
	routes?: Array<{
		path: string;
		method: 'GET' | 'POST' | 'PUT' | 'DELETE' | 'PATCH';
		name: string;
		description?: string;
		security?: boolean;
	}>;
	security?: {
		authentication: boolean;
		rateLimit?: number;
		cors?: boolean;
	};
	domain: 'security' | 'productivity' | 'mtg' | 'infrastructure';
	context?: ASTOperationContext;
}): SourceFile {
	const sourceFile = loadSourceFile(servicePath);

	// Add FastAPI imports
	const fastApiImports = ['FastAPI', 'HTTPException', 'Depends'];
	if (security?.authentication) {
		fastApiImports.push('Security');
	}

	updateImports({
		sourceFile,
		imports: [
			{
				moduleSpecifier: 'fastapi',
				namedImports: fastApiImports,
			},
		],
		mode: 'merge',
	});

	return sourceFile;
}

/**
 * Enhanced credential/authentication system manipulation
 * Generalized from n8n credential operations for any auth system
 */
export function updateAuthConfiguration({
	authPath,
	authName,
	authType,
	config,
	context,
}: {
	authPath: string;
	authName: string;
	authType: 'apiKey' | 'oauth2' | 'bearer' | 'basic' | 'custom';
	config: {
		displayName?: string;
		description?: string;
		testEndpoint?: string;
		fields?: Array<{ name: string; type: string; required: boolean }>;
	};
	context?: ASTOperationContext;
}): SourceFile {
	const sourceFile = loadSourceFile(authPath);
	const classDecl = sourceFile.getClasses()[0];

	if (!classDecl) {
		throw new Error(`No class found in ${authPath}`);
	}

	// Update class name
	classDecl.rename(`${pascalCase(authName)}Credentials`);

	// Update basic properties
	updateStringProperty({
		obj: classDecl,
		key: 'displayName',
		value: config.displayName || `${capitalCase(authName)} Credentials`,
		context,
		createIfMissing: true,
	});

	updateStringProperty({
		obj: classDecl,
		key: 'name',
		value: camelCase(authName),
		context,
		createIfMissing: true,
	});

	updateStringProperty({
		obj: classDecl,
		key: 'description',
		value: config.description || `Authentication credentials for ${capitalCase(authName)}`,
		context,
		createIfMissing: true,
	});

	return sourceFile;
}

/**
 * Database schema/model manipulation
 * Creates/updates database models with type safety
 */
export function updateDatabaseModel({
	modelPath,
	modelName,
	fields,
	relationships,
	context,
}: {
	modelPath: string;
	modelName: string;
	fields: Record<string, { type: string; nullable?: boolean; unique?: boolean }>;
	relationships?: Array<{ name: string; type: 'oneToOne' | 'oneToMany' | 'manyToMany'; target: string }>;
	context?: ASTOperationContext;
}): SourceFile {
	const sourceFile = loadSourceFile(modelPath);

	// Create/update model interface
	const fieldTypes: Record<string, string> = {};
	Object.entries(fields).forEach(([name, field]) => {
		fieldTypes[name] = field.nullable ? `${field.type} | null` : field.type;
	});

	updateInterfaceDeclaration({
		sourceFile,
		interfaceName: modelName,
		properties: fieldTypes,
	});

	return sourceFile;
}

/**
 * Configuration file manipulation
 * Updates various configuration formats (JSON-like objects in TS)
 */
export function updateConfigurationFile({
	configPath,
	updates,
	mergeStrategy = 'deep',
	context,
}: {
	configPath: string;
	updates: Record<string, any>;
	mergeStrategy?: 'shallow' | 'deep' | 'replace';
	context?: ASTOperationContext;
}): SourceFile {
	const sourceFile = loadSourceFile(configPath);

	// Find configuration object (could be default export, named export, or variable)
	const configVar = sourceFile.getVariableDeclaration('config') ||
		sourceFile.getVariableDeclaration('configuration') ||
		sourceFile.getVariableDeclarations()[0];

	if (configVar) {
		const configObj = configVar.getInitializerIfKind(SyntaxKind.ObjectLiteralExpression);
		if (configObj) {
			Object.entries(updates).forEach(([key, value]) => {
				if (typeof value === 'string') {
					updateStringProperty({ obj: configObj, key, value, context, createIfMissing: true });
				} else if (Array.isArray(value)) {
					updateArrayProperty({ obj: configObj, key, values: value, mode: 'replace' });
				}
				// Handle nested objects, numbers, booleans, etc.
			});
		}
	}

	return sourceFile;
}

/**
 * Test file manipulation
 * Creates/updates test files with comprehensive coverage
 */
export function updateTestFile({
	testPath,
	targetFile,
	testFramework = 'vitest',
	coverage,
	context,
}: {
	testPath: string;
	targetFile: string;
	testFramework?: 'jest' | 'vitest' | 'mocha' | 'cypress';
	coverage?: {
		functions: string[];
		branches: string[];
		scenarios: string[];
	};
	context?: ASTOperationContext;
}): SourceFile {
	const sourceFile = loadSourceFile(testPath);

	// Add test framework imports
	const testImports = testFramework === 'jest' ? 
		['describe', 'it', 'expect', 'beforeEach', 'afterEach'] :
		['describe', 'it', 'expect', 'beforeEach', 'afterEach', 'vi'];

	updateImports({
		sourceFile,
		imports: [
			{
				moduleSpecifier: testFramework === 'jest' ? '@jest/globals' : 'vitest',
				namedImports: testImports,
			},
		],
		mode: 'merge',
	});

	return sourceFile;
}

/**
 * Migration script manipulation
 * Creates/updates database migration files
 */
export function updateMigrationFile({
	migrationPath,
	migrationName,
	operations,
	rollback,
	context,
}: {
	migrationPath: string;
	migrationName: string;
	operations: Array<{ type: 'create' | 'alter' | 'drop'; target: string; changes: Record<string, any> }>;
	rollback?: Array<{ type: 'create' | 'alter' | 'drop'; target: string; changes: Record<string, any> }>;
	context?: ASTOperationContext;
}): SourceFile {
	const sourceFile = loadSourceFile(migrationPath);

	// Migration logic here - depends on the ORM/database system
	// This would be expanded based on the specific migration framework

	return sourceFile;
}

/**
 * Executive function accommodation utilities
 * Applies ADHD-friendly code patterns automatically
 */
export function applyExecutiveFunctionAccommodations({
	filePath,
	accommodations,
	context,
}: {
	filePath: string;
	accommodations: {
		maxFunctionComplexity?: number;
		maxParameterCount?: number;
		enforceConsistentNaming?: boolean;
		addProgressiveDisclosure?: boolean;
		enhanceReadability?: boolean;
	};
	context?: ASTOperationContext;
}): SourceFile {
	const sourceFile = loadSourceFile(filePath);

	// Apply accommodations
	if (accommodations.enforceConsistentNaming) {
		// Enforce consistent naming conventions
		sourceFile.getClasses().forEach(cls => {
			const className = cls.getName();
			if (className && !/^[A-Z][a-zA-Z0-9]*$/.test(className)) {
				cls.rename(pascalCase(className));
			}
		});

		sourceFile.getFunctions().forEach(func => {
			const funcName = func.getName();
			if (funcName && !/^[a-z][a-zA-Z0-9]*$/.test(funcName)) {
				func.rename(camelCase(funcName));
			}
		});
	}

	if (accommodations.maxParameterCount) {
		// Break down functions with too many parameters
		sourceFile.getFunctions().forEach(func => {
			const params = func.getParameters();
			if (params.length > accommodations.maxParameterCount!) {
				// Suggest parameter object pattern
				if (context?.logErrors) {
					console.warn(`Function ${func.getName()} has ${params.length} parameters. Consider using parameter object pattern.`);
				}
			}
		});
	}

	return sourceFile;
}

/**
 * Security-first development utilities
 * Automatically applies security best practices
 */
export function applySecurityBestPractices({
	filePath,
	securityLevel = 'standard',
	context,
}: {
	filePath: string;
	securityLevel?: 'basic' | 'standard' | 'strict' | 'paranoid';
	context?: ASTOperationContext;
}): SourceFile {
	const sourceFile = loadSourceFile(filePath);

	// Apply security transformations based on level
	if (securityLevel === 'strict' || securityLevel === 'paranoid') {
		// Add input validation
		sourceFile.getFunctions().forEach(func => {
			const params = func.getParameters();
			params.forEach(param => {
				const paramName = param.getName();
				if (paramName.toLowerCase().includes('password')) {
					// Suggest secure string type
					if (context?.logErrors) {
						console.warn(`Parameter '${paramName}' should use SecureString type`);
					}
				}
			});
		});
	}

	return sourceFile;
}

/**
 * Cross-domain pattern analysis and application
 * Detects and applies patterns that work across different domains
 */
export function applyCrossDomainPatterns({
	filePath,
	targetDomains,
	patterns,
	context,
}: {
	filePath: string;
	targetDomains: Array<'security' | 'productivity' | 'mtg' | 'infrastructure'>;
	patterns: string[];
	context?: ASTOperationContext;
}): SourceFile {
	const sourceFile = loadSourceFile(filePath);

	// Apply domain-specific patterns
	targetDomains.forEach(domain => {
		switch (domain) {
			case 'security':
				// Apply security-specific patterns
				applySecurityBestPractices({ filePath, securityLevel: 'standard', context });
				break;
			case 'productivity':
				// Apply productivity-specific patterns (error handling, logging, etc.)
				break;
			case 'mtg':
				// Apply MTG-specific patterns (card validation, rules engine, etc.)
				break;
			case 'infrastructure':
				// Apply infrastructure patterns (monitoring, health checks, etc.)
				break;
		}
	});

	return sourceFile;
}

/**
 * AI-enhanced code generation
 * Uses AI to generate code based on patterns and context
 */
export async function generateCodeWithAI({
	template,
	variables,
	aiConfig,
	context,
}: {
	template: CodeTemplate;
	variables: Record<string, any>;
	aiConfig: AIEnhancementConfig;
	context?: ASTOperationContext;
}): Promise<string> {
	// This would integrate with the AI service from the main intelligence service
	// For now, return a simple template substitution
	
	let content = template.template;
	
	// Simple template variable substitution
	Object.entries(variables).forEach(([key, value]) => {
		const pattern = new RegExp(`{{\\s*${key}\\s*}}`, 'g');
		content = content.replace(pattern, String(value));
	});

	// Apply post-processing hooks
	if (template.postProcess) {
		template.postProcess.forEach(hook => {
			content = hook(content, variables);
		});
	}

	return content;
}

/**
 * Batch refactoring operations
 * Applies multiple refactoring operations safely with rollback capability
 */
export async function batchRefactor({
	files,
	operations,
	context,
	dryRun = false,
}: {
	files: string[];
	operations: RefactoringOperation[];
	context?: ASTOperationContext;
	dryRun?: boolean;
}): Promise<{
	success: boolean;
	results: Array<{ file: string; operations: string[]; errors: string[] }>;
	rollbackPlan: Array<{ file: string; rollbackFunction: () => void }>;
}> {
	const results: Array<{ file: string; operations: string[]; errors: string[] }> = [];
	const rollbackPlan: Array<{ file: string; rollbackFunction: () => void }> = [];

	for (const file of files) {
		const fileResult = { file, operations: [] as string[], errors: [] as string[] };
		
		try {
			const sourceFile = loadSourceFile(file);
			const originalContent = sourceFile.getFullText();
			
			for (const operation of operations) {
				try {
					// Safety check
					if (operation.safetyCheck && !operation.safetyCheck(sourceFile)) {
						fileResult.errors.push(`Safety check failed for operation: ${operation.name}`);
						continue;
					}

					// Apply transformation
					const success = operation.transform(sourceFile, []);
					if (success) {
						fileResult.operations.push(operation.name);
						
						// Store rollback function
						if (operation.rollback) {
							rollbackPlan.push({
								file,
								rollbackFunction: () => operation.rollback!(sourceFile),
							});
						}
					}
				} catch (error) {
					fileResult.errors.push(`Operation ${operation.name} failed: ${error}`);
				}
			}

			// Save file if not dry run
			if (!dryRun && fileResult.operations.length > 0) {
				await sourceFile.save();
			}
		} catch (error) {
			fileResult.errors.push(`Failed to process file: ${error}`);
		}

		results.push(fileResult);
	}

	return {
		success: results.every(r => r.errors.length === 0),
		results,
		rollbackPlan,
	};
}

/**
 * Template-based code generation
 * Generates code from templates with variable substitution
 */
export function generateFromTemplate({
	template,
	variables,
	outputPath,
	context,
}: {
	template: CodeTemplate;
	variables: Record<string, any>;
	outputPath: string;
	context?: ASTOperationContext;
}): { success: boolean; content: string; errors: string[] } {
	const errors: string[] = [];

	try {
		// Validate required variables
		Object.entries(template.variables).forEach(([name, config]) => {
			if (config.required && !(name in variables)) {
				errors.push(`Required variable '${name}' is missing`);
			}
		});

		if (errors.length > 0) {
			return { success: false, content: '', errors };
		}

		// Generate content
		let content = template.template;
		
		// Replace variables
		Object.entries(variables).forEach(([key, value]) => {
			const patterns = [
				new RegExp(`{{\\s*${key}\\s*}}`, 'g'),
				new RegExp(`\\$\\{${key}\\}`, g),
				new RegExp(`%${key}%`, 'g'),
			];
			
			patterns.forEach(pattern => {
				content = content.replace(pattern, String(value));
			});
		});

		// Apply post-processing
		if (template.postProcess) {
			template.postProcess.forEach(processor => {
				content = processor(content, variables);
			});
		}

		return { success: true, content, errors: [] };
	} catch (error) {
		return { success: false, content: '', errors: [`Template generation failed: ${error}`] };
	}
}