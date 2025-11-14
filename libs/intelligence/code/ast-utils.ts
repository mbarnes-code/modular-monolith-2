/**
 * TypeScript AST Utilities - Generalized from n8n Node CLI
 * 
 * Enhanced for all TypeScript projects with AI-driven code intelligence.
 * Based on ts-morph v26.0.0 for robust AST manipulation.
 * 
 * Features:
 * - Project-agnostic AST operations
 * - Type-safe property updates
 * - Intelligent code generation patterns
 * - Executive function accommodations (consistent patterns)
 * - Security-first development practices
 * 
 * Zero Dependencies Promise:
 * - Works standalone or with AI enhancement
 * - Graceful degradation if AI services unavailable
 * - Preserves all existing functionality
 */

import {
	Project,
	SyntaxKind,
	type ClassDeclaration,
	type ObjectLiteralExpression,
	type PropertyAssignment,
	type PropertyDeclaration,
	type SourceFile,
	type InterfaceDeclaration,
	type TypeAliasDeclaration,
	type EnumDeclaration,
	type FunctionDeclaration,
	type VariableDeclaration,
	type ModuleDeclaration,
} from 'ts-morph';

import type { ProjectConfig, ASTOperationContext, CodeGenerationHint } from './types';

/**
 * Load a single TypeScript source file for AST manipulation
 * Enhanced with project context awareness
 */
export const loadSourceFile = (
	path: string,
	projectConfig?: ProjectConfig
): SourceFile => {
	const project = new Project({
		skipFileDependencyResolution: projectConfig?.skipDependencies ?? true,
		tsConfigFilePath: projectConfig?.tsConfigPath,
		useInMemoryFileSystem: projectConfig?.useInMemory ?? false,
		compilerOptions: projectConfig?.compilerOptions,
	});

	return project.addSourceFileAtPath(path);
};

/**
 * Load multiple source files as a project
 * Useful for cross-file refactoring and analysis
 */
export const loadProject = (
	paths: string[] | string,
	projectConfig?: ProjectConfig
): Project => {
	const project = new Project({
		skipFileDependencyResolution: projectConfig?.skipDependencies ?? true,
		tsConfigFilePath: projectConfig?.tsConfigPath,
		useInMemoryFileSystem: projectConfig?.useInMemory ?? false,
		compilerOptions: projectConfig?.compilerOptions,
	});

	if (Array.isArray(paths)) {
		paths.forEach(path => project.addSourceFileAtPath(path));
	} else {
		// Glob pattern support
		project.addSourceFilesAtPaths(paths);
	}

	return project;
};

/**
 * Type-safe string property updater with validation
 * Enhanced with context awareness and error handling
 */
const setStringInitializer = (
	prop: PropertyAssignment | PropertyDeclaration,
	value: string,
	context?: ASTOperationContext
): void => {
	try {
		const initializer = prop.getInitializerIfKind(SyntaxKind.StringLiteral);
		if (initializer) {
			initializer.setLiteralValue(value);
		} else {
			// Handle non-string literals gracefully
			if (context?.forceStringConversion) {
				prop.setInitializer(`"${value.replace(/"/g, '\\"')}"`);
			} else {
				throw new Error(`Property initializer is not a string literal`);
			}
		}
	} catch (error) {
		if (context?.logErrors) {
			console.warn(`Failed to update string property: ${error}`);
		}
		throw error;
	}
};

/**
 * Enhanced string property updater with type safety and context
 */
export const updateStringProperty = ({
	obj,
	key,
	value,
	context,
	createIfMissing = false,
}: {
	obj: ObjectLiteralExpression | ClassDeclaration | InterfaceDeclaration;
	key: string;
	value: string;
	context?: ASTOperationContext;
	createIfMissing?: boolean;
}): boolean => {
	try {
		let prop = obj.getProperty(key);
		
		if (!prop && createIfMissing) {
			// Create missing property
			if (obj instanceof ObjectLiteralExpression) {
				obj.addPropertyAssignment({ name: key, initializer: `"${value}"` });
				return true;
			} else if (obj instanceof ClassDeclaration) {
				obj.addProperty({ name: key, initializer: `"${value}"` });
				return true;
			}
		}
		
		if (!prop) {
			if (context?.logErrors) {
				console.warn(`Property '${key}' not found in object`);
			}
			return false;
		}

		if (prop.isKind(SyntaxKind.PropertyAssignment)) {
			setStringInitializer(prop.asKindOrThrow(SyntaxKind.PropertyAssignment), value, context);
		} else if (prop.isKind(SyntaxKind.PropertyDeclaration)) {
			setStringInitializer(prop.asKindOrThrow(SyntaxKind.PropertyDeclaration), value, context);
		} else if (prop.isKind(SyntaxKind.PropertySignature)) {
			// Interface property - update type annotation if needed
			if (context?.updateInterfaceTypes) {
				prop.setType('string');
			}
		}
		
		return true;
	} catch (error) {
		if (context?.logErrors) {
			console.error(`Error updating property '${key}':`, error);
		}
		return false;
	}
};

/**
 * Enhanced object literal retrieval with type safety
 */
export const getChildObjectLiteral = ({
	obj,
	key,
	createIfMissing = false,
}: {
	obj: ObjectLiteralExpression;
	key: string;
	createIfMissing?: boolean;
}): ObjectLiteralExpression | null => {
	try {
		let prop = obj.getProperty(key);
		
		if (!prop && createIfMissing) {
			obj.addPropertyAssignment({ name: key, initializer: '{}' });
			prop = obj.getProperty(key);
		}
		
		if (!prop) return null;

		return prop
			.asKindOrThrow(SyntaxKind.PropertyAssignment)
			.getInitializerIfKind(SyntaxKind.ObjectLiteralExpression) || null;
	} catch (error) {
		console.warn(`Error getting child object '${key}':`, error);
		return null;
	}
};

/**
 * Enhanced array manipulation utilities
 */
export const updateArrayProperty = ({
	obj,
	key,
	values,
	mode = 'replace',
}: {
	obj: ObjectLiteralExpression | ClassDeclaration;
	key: string;
	values: string[];
	mode?: 'replace' | 'append' | 'prepend' | 'merge';
}): boolean => {
	try {
		const prop = obj.getProperty(key);
		if (!prop) return false;

		const arrayLiteral = prop
			.asKindOrThrow(SyntaxKind.PropertyAssignment)
			.getInitializerIfKind(SyntaxKind.ArrayLiteralExpression);

		if (!arrayLiteral) return false;

		switch (mode) {
			case 'replace':
				arrayLiteral.removeElements();
				values.forEach(value => arrayLiteral.addElement(`"${value}"`));
				break;
			case 'append':
				values.forEach(value => arrayLiteral.addElement(`"${value}"`));
				break;
			case 'prepend':
				values.reverse().forEach(value => arrayLiteral.insertElement(0, `"${value}"`));
				break;
			case 'merge':
				const existing = arrayLiteral.getElements().map(el => el.getText().replace(/"/g, ''));
				const newValues = values.filter(v => !existing.includes(v));
				newValues.forEach(value => arrayLiteral.addElement(`"${value}"`));
				break;
		}

		return true;
	} catch (error) {
		console.error(`Error updating array property '${key}':`, error);
		return false;
	}
};

/**
 * Type-safe class manipulation utilities
 */
export const updateClassDeclaration = ({
	sourceFile,
	className,
	updates,
	context,
}: {
	sourceFile: SourceFile;
	className: string;
	updates: {
		name?: string;
		properties?: Record<string, string>;
		methods?: Array<{ name: string; body: string; returnType?: string }>;
		implements?: string[];
		extends?: string;
	};
	context?: ASTOperationContext;
}): ClassDeclaration | null => {
	try {
		const classDecl = sourceFile.getClass(className);
		if (!classDecl) return null;

		// Update class name
		if (updates.name) {
			classDecl.rename(updates.name);
		}

		// Update properties
		if (updates.properties) {
			Object.entries(updates.properties).forEach(([key, value]) => {
				updateStringProperty({ obj: classDecl, key, value, context, createIfMissing: true });
			});
		}

		// Add/update methods
		if (updates.methods) {
			updates.methods.forEach(method => {
				const existing = classDecl.getMethod(method.name);
				if (existing) {
					existing.setBodyText(method.body);
					if (method.returnType) {
						existing.setReturnType(method.returnType);
					}
				} else {
					classDecl.addMethod({
						name: method.name,
						statements: method.body,
						returnType: method.returnType,
					});
				}
			});
		}

		// Update implements
		if (updates.implements) {
			classDecl.setImplements(updates.implements);
		}

		// Update extends
		if (updates.extends) {
			classDecl.setExtends(updates.extends);
		}

		return classDecl;
	} catch (error) {
		if (context?.logErrors) {
			console.error(`Error updating class '${className}':`, error);
		}
		return null;
	}
};

/**
 * Interface manipulation utilities
 */
export const updateInterfaceDeclaration = ({
	sourceFile,
	interfaceName,
	properties,
	methods,
	extends: extendsInterfaces,
}: {
	sourceFile: SourceFile;
	interfaceName: string;
	properties?: Record<string, string>;
	methods?: Array<{ name: string; parameters: Array<{ name: string; type: string }>; returnType: string }>;
	extends?: string[];
}): InterfaceDeclaration | null => {
	try {
		let interfaceDecl = sourceFile.getInterface(interfaceName);
		
		if (!interfaceDecl) {
			interfaceDecl = sourceFile.addInterface({
				name: interfaceName,
				isExported: true,
			});
		}

		// Add/update properties
		if (properties) {
			Object.entries(properties).forEach(([name, type]) => {
				const existing = interfaceDecl.getProperty(name);
				if (existing) {
					existing.setType(type);
				} else {
					interfaceDecl.addProperty({ name, type });
				}
			});
		}

		// Add/update methods
		if (methods) {
			methods.forEach(method => {
				const existing = interfaceDecl.getMethod(method.name);
				if (existing) {
					existing.setParameters(method.parameters);
					existing.setReturnType(method.returnType);
				} else {
					interfaceDecl.addMethod({
						name: method.name,
						parameters: method.parameters,
						returnType: method.returnType,
					});
				}
			});
		}

		// Update extends
		if (extendsInterfaces) {
			interfaceDecl.setExtends(extendsInterfaces);
		}

		return interfaceDecl;
	} catch (error) {
		console.error(`Error updating interface '${interfaceName}':`, error);
		return null;
	}
};

/**
 * Import management utilities
 */
export const updateImports = ({
	sourceFile,
	imports,
	mode = 'merge',
}: {
	sourceFile: SourceFile;
	imports: Array<{
		moduleSpecifier: string;
		namedImports?: string[];
		defaultImport?: string;
		namespaceImport?: string;
	}>;
	mode?: 'replace' | 'merge';
}): void => {
	if (mode === 'replace') {
		sourceFile.getImportDeclarations().forEach(imp => imp.remove());
	}

	imports.forEach(imp => {
		const existingImport = sourceFile.getImportDeclaration(imp.moduleSpecifier);
		
		if (existingImport && mode === 'merge') {
			// Merge with existing import
			if (imp.namedImports) {
				const existingNamed = existingImport.getNamedImports().map(ni => ni.getName());
				const newNamed = imp.namedImports.filter(ni => !existingNamed.includes(ni));
				if (newNamed.length > 0) {
					existingImport.addNamedImports(newNamed);
				}
			}
		} else {
			// Add new import
			sourceFile.addImportDeclaration({
				moduleSpecifier: imp.moduleSpecifier,
				namedImports: imp.namedImports,
				defaultImport: imp.defaultImport,
				namespaceImport: imp.namespaceImport,
			});
		}
	});
};

/**
 * Code generation hints for AI enhancement
 */
export const generateCodeHints = (sourceFile: SourceFile): CodeGenerationHint[] => {
	const hints: CodeGenerationHint[] = [];
	
	// Analyze patterns for AI enhancement
	const classes = sourceFile.getClasses();
	const interfaces = sourceFile.getInterfaces();
	const functions = sourceFile.getFunctions();
	
	// Executive function accommodation patterns
	classes.forEach(cls => {
		const methods = cls.getMethods();
		if (methods.length > 7) {
			hints.push({
				type: 'executive_function',
				suggestion: 'Consider breaking large class into smaller focused classes',
				location: cls.getNameNode()?.getStartLineNumber() || 0,
				impact: 'High - Reduces cognitive load for ADHD-friendly development',
			});
		}
	});
	
	// Security pattern detection
	functions.forEach(func => {
		const params = func.getParameters();
		params.forEach(param => {
			if (param.getName().toLowerCase().includes('password') && !param.getType().getText().includes('SecureString')) {
				hints.push({
					type: 'security',
					suggestion: 'Consider using SecureString type for password parameters',
					location: param.getStartLineNumber(),
					impact: 'High - Improves security posture',
				});
			}
		});
	});
	
	return hints;
};

/**
 * Batch operations for efficient multi-file processing
 */
export const batchProcess = async ({
	files,
	operations,
	projectConfig,
	parallelism = 4,
}: {
	files: string[];
	operations: Array<(sourceFile: SourceFile) => void>;
	projectConfig?: ProjectConfig;
	parallelism?: number;
}): Promise<{ processed: number; errors: string[] }> => {
	const errors: string[] = [];
	let processed = 0;
	
	// Process in batches to avoid memory issues
	const batches = [];
	for (let i = 0; i < files.length; i += parallelism) {
		batches.push(files.slice(i, i + parallelism));
	}
	
	for (const batch of batches) {
		await Promise.all(
			batch.map(async (file) => {
				try {
					const sourceFile = loadSourceFile(file, projectConfig);
					operations.forEach(op => op(sourceFile));
					await sourceFile.save();
					processed++;
				} catch (error) {
					errors.push(`${file}: ${error}`);
				}
			})
		);
	}
	
	return { processed, errors };
};

/**
 * AI-enhanced code analysis for pattern detection
 */
export const analyzeCodePatterns = (sourceFile: SourceFile): {
	complexity: number;
	maintainability: number;
	securityScore: number;
	accessibilityScore: number;
	executiveFunctionScore: number;
} => {
	// Complexity analysis
	const cyclomaticComplexity = calculateCyclomaticComplexity(sourceFile);
	
	// Maintainability analysis
	const maintainabilityIndex = calculateMaintainabilityIndex(sourceFile);
	
	// Security analysis
	const securityScore = analyzeSecurityPatterns(sourceFile);
	
	// Accessibility analysis (for UI components)
	const accessibilityScore = analyzeAccessibilityPatterns(sourceFile);
	
	// Executive function analysis (ADHD-friendly patterns)
	const executiveFunctionScore = analyzeExecutiveFunctionPatterns(sourceFile);
	
	return {
		complexity: cyclomaticComplexity,
		maintainability: maintainabilityIndex,
		securityScore,
		accessibilityScore,
		executiveFunctionScore,
	};
};

// Helper functions for analysis
function calculateCyclomaticComplexity(sourceFile: SourceFile): number {
	// Simplified complexity calculation
	const functions = sourceFile.getFunctions();
	const methods = sourceFile.getClasses().flatMap(c => c.getMethods());
	
	let totalComplexity = 0;
	[...functions, ...methods].forEach(func => {
		let complexity = 1; // Base complexity
		
		// Count decision points
		const body = func.getBody();
		if (body) {
			const text = body.getText();
			complexity += (text.match(/\bif\b|\bwhile\b|\bfor\b|\bswitch\b|\bcatch\b/g) || []).length;
		}
		
		totalComplexity += complexity;
	});
	
	return totalComplexity;
}

function calculateMaintainabilityIndex(sourceFile: SourceFile): number {
	// Simplified maintainability calculation (0-100 scale)
	const linesOfCode = sourceFile.getEndLineNumber();
	const classes = sourceFile.getClasses().length;
	const functions = sourceFile.getFunctions().length;
	
	// Higher is better
	const baseScore = 100;
	const locPenalty = Math.min(linesOfCode / 10, 30);
	const complexityBonus = Math.min((classes + functions) * 2, 20);
	
	return Math.max(0, baseScore - locPenalty + complexityBonus);
}

function analyzeSecurityPatterns(sourceFile: SourceFile): number {
	// Security pattern analysis (0-100 scale, higher is better)
	let score = 80; // Base score
	
	const text = sourceFile.getFullText();
	
	// Deduct points for security anti-patterns
	if (text.includes('eval(')) score -= 20;
	if (text.includes('innerHTML')) score -= 10;
	if (text.includes('document.write')) score -= 15;
	if (text.match(/password.*=.*["'].*["']/)) score -= 25;
	
	// Add points for security patterns
	if (text.includes('sanitize')) score += 5;
	if (text.includes('validate')) score += 5;
	if (text.includes('escape')) score += 5;
	
	return Math.max(0, Math.min(100, score));
}

function analyzeAccessibilityPatterns(sourceFile: SourceFile): number {
	// Accessibility pattern analysis for React/UI components
	let score = 60; // Base score
	
	const text = sourceFile.getFullText();
	
	// Check for accessibility patterns
	if (text.includes('aria-')) score += 10;
	if (text.includes('role=')) score += 5;
	if (text.includes('alt=')) score += 5;
	if (text.includes('tabIndex')) score += 5;
	
	// Check for accessibility anti-patterns
	if (text.includes('tabIndex={-1}') && !text.includes('focusable')) score -= 5;
	
	return Math.max(0, Math.min(100, score));
}

function analyzeExecutiveFunctionPatterns(sourceFile: SourceFile): number {
	// Executive function accommodation analysis (ADHD-friendly patterns)
	let score = 70; // Base score
	
	const classes = sourceFile.getClasses();
	const functions = sourceFile.getFunctions();
	
	// Analyze cognitive load patterns
	classes.forEach(cls => {
		const methods = cls.getMethods();
		if (methods.length <= 5) score += 5; // Small, focused classes
		if (methods.length > 10) score -= 10; // Large, complex classes
	});
	
	functions.forEach(func => {
		const params = func.getParameters();
		if (params.length <= 3) score += 2; // Simple parameter lists
		if (params.length > 7) score -= 5; // Complex parameter lists
		
		// Check for consistent naming
		const name = func.getName();
		if (name && /^[a-z][a-zA-Z0-9]*$/.test(name)) score += 1; // Consistent camelCase
	});
	
	return Math.max(0, Math.min(100, score));
}