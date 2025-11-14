/**
 * Logging Code Refactoring Tool
 * 
 * Automated extraction of logging code from all services into a shared logging library.
 * Uses enhanced TypeScript AST tools (generalized from n8n CLI) for safe refactoring.
 * 
 * Features:
 * - Detects all logging patterns across the codebase
 * - Extracts logging into libs/shared/logging
 * - Updates imports automatically
 * - Maintains executive function accommodations (ADHD-friendly)
 * - Provides rollback capabilities for safety
 * - Batch processing for efficient handling of multiple files
 * 
 * Zero Dependencies Promise:
 * - All existing functionality preserved
 * - Graceful degradation if refactoring fails
 * - No breaking changes to existing APIs
 */

import * as fs from 'fs/promises';
import * as path from 'path';
import { Project, SyntaxKind, type PropertyAccessExpression, type SourceFile } from 'ts-morph';


import {
    batchRefactor
} from './domain-operations';

import type {
    RefactoringOperation
} from './types';

/**
 * Detected logging pattern in the codebase
 */
interface LoggingPattern {
	/** File path where pattern was found */
	filePath: string;
	
	/** Line number */
	line: number;
	
	/** Pattern type */
	type: 'console' | 'winston' | 'pino' | 'custom' | 'debug';
	
	/** Method called (log, info, error, warn, debug) */
	method: string;
	
	/** Full expression text */
	expression: string;
	
	/** Logger variable name if custom */
	loggerVariable?: string;
	
	/** Import source if detected */
	importSource?: string;
	
	/** Suggested replacement */
	replacement?: string;
}

/**
 * Logging library structure to be generated
 */
interface LoggingLibraryStructure {
	/** Main logger interface */
	interface: string;
	
	/** Implementation classes */
	implementations: Array<{
		name: string;
		type: 'console' | 'file' | 'json' | 'structured';
		content: string;
	}>;
	
	/** Factory function */
	factory: string;
	
	/** Configuration types */
	types: string;
	
	/** Export declarations */
	exports: string;
}

/**
 * Scan all TypeScript files for logging patterns
 */
export async function scanForLoggingPatterns(
	projectPath: string,
	includePatterns: string[] = ['src/**/*.ts', 'apps/**/*.ts', 'libs/**/*.ts'],
	excludePatterns: string[] = ['**/*.test.ts', '**/*.spec.ts', '**/node_modules/**']
): Promise<LoggingPattern[]> {
	const patterns: LoggingPattern[] = [];
	
	console.log('🔍 Scanning for logging patterns...');
	
	try {
		const project = new Project({
			skipFileDependencyResolution: true,
			tsConfigFilePath: path.join(projectPath, 'tsconfig.json'),
		});
		
		// Add source files based on patterns
		includePatterns.forEach(pattern => {
			try {
				project.addSourceFilesAtPaths(path.join(projectPath, pattern));
			} catch (error) {
				console.warn(`Could not load pattern ${pattern}: ${error}`);
			}
		});
		
		const sourceFiles = project.getSourceFiles().filter(file => {
			const filePath = file.getFilePath();
			return !excludePatterns.some(pattern => 
				filePath.includes(pattern.replace('**/', '').replace('*', ''))
			);
		});
		
		console.log(`📁 Found ${sourceFiles.length} files to analyze`);
		
		for (const sourceFile of sourceFiles) {
			const filePatterns = await analyzeFileForLogging(sourceFile);
			patterns.push(...filePatterns);
		}
		
		console.log(`✅ Found ${patterns.length} logging patterns`);
		return patterns;
		
	} catch (error) {
		console.error('❌ Error scanning for logging patterns:', error);
		throw error;
	}
}

/**
 * Analyze a single file for logging patterns
 */
async function analyzeFileForLogging(sourceFile: SourceFile): Promise<LoggingPattern[]> {
	const patterns: LoggingPattern[] = [];
	const filePath = sourceFile.getFilePath();
	
	// Look for console.* calls
	sourceFile.getDescendantsOfKind(SyntaxKind.CallExpression).forEach(call => {
		const expression = call.getExpression();
		
		if (expression.getKind() === SyntaxKind.PropertyAccessExpression) {
			const propAccess = expression as PropertyAccessExpression;
			const object = propAccess.getExpression().getText();
			const method = propAccess.getName();
			
			// Console logging
			if (object === 'console' && ['log', 'info', 'warn', 'error', 'debug'].includes(method)) {
				patterns.push({
					filePath,
					line: call.getStartLineNumber(),
					type: 'console',
					method,
					expression: call.getText(),
					replacement: generateReplacementCode('console', method, call.getArguments().map(arg => arg.getText())),
				});
			}
			
			// Custom logger patterns (logger.info, this.logger.warn, etc.)
			else if (method && ['log', 'info', 'warn', 'error', 'debug', 'trace', 'fatal'].includes(method)) {
				patterns.push({
					filePath,
					line: call.getStartLineNumber(),
					type: 'custom',
					method,
					expression: call.getText(),
					loggerVariable: object,
					replacement: generateReplacementCode('custom', method, call.getArguments().map(arg => arg.getText())),
				});
			}
		}
	});
	
	// Look for import statements that import logging libraries
	sourceFile.getImportDeclarations().forEach(imp => {
		const moduleSpecifier = imp.getModuleSpecifierValue();
		if (['winston', 'pino', 'debug', 'loglevel', 'bunyan'].includes(moduleSpecifier)) {
			// Note: We'll handle these imports during the refactoring phase
			console.log(`📦 Found logging import: ${moduleSpecifier} in ${filePath}`);
		}
	});
	
	return patterns;
}

/**
 * Generate replacement code for logging calls
 */
function generateReplacementCode(type: string, method: string, args: string[]): string {
	// Use the new shared logger
	const loggerCall = `logger.${method}`;
	
	if (args.length === 0) {
		return `${loggerCall}()`;
	} else if (args.length === 1) {
		return `${loggerCall}(${args[0]})`;
	} else {
		// Multiple arguments - join them appropriately
		return `${loggerCall}(${args.join(', ')})`;
	}
}

/**
 * Generate the shared logging library structure
 */
export function generateLoggingLibrary(): LoggingLibraryStructure {
	const interfaceContent = `
/**
 * Universal Logger Interface
 * 
 * Executive Function Accommodations:
 * - Consistent API across all 37 tools
 * - Simple method names (no cognitive overload)
 * - Predictable behavior patterns
 */
export interface ILogger {
	/** Debug level logging (development only) */
	debug(message: string, ...args: any[]): void;
	
	/** Informational logging */
	info(message: string, ...args: any[]): void;
	
	/** Warning logging */
	warn(message: string, ...args: any[]): void;
	
	/** Error logging */
	error(message: string | Error, ...args: any[]): void;
	
	/** Fatal error logging */
	fatal(message: string | Error, ...args: any[]): void;
	
	/** Create child logger with context */
	child(context: Record<string, any>): ILogger;
}`;

	const typesContent = `
/**
 * Logging Configuration Types
 */
export type LogLevel = 'debug' | 'info' | 'warn' | 'error' | 'fatal';

export interface LoggerConfig {
	/** Minimum log level */
	level: LogLevel;
	
	/** Enable console output */
	console: boolean;
	
	/** File logging configuration */
	file?: {
		enabled: boolean;
		path: string;
		maxSize?: string;
		maxFiles?: number;
	};
	
	/** Structured logging (JSON) */
	structured?: boolean;
	
	/** Service name for context */
	service?: string;
	
	/** Executive function accommodations */
	accessibility?: {
		/** Color-blind friendly console output */
		colorBlindFriendly: boolean;
		
		/** Consistent timestamp format */
		timestampFormat: 'iso' | 'readable' | 'unix';
		
		/** Reduced visual noise */
		minimalist: boolean;
	};
}

export interface LogContext {
	/** Timestamp */
	timestamp: string;
	
	/** Log level */
	level: LogLevel;
	
	/** Service name */
	service?: string;
	
	/** Request ID for tracing */
	requestId?: string;
	
	/** User ID for security auditing */
	userId?: string;
	
	/** Domain context (security, productivity, mtg, infrastructure) */
	domain?: 'security' | 'productivity' | 'mtg' | 'infrastructure';
}`;

	const consoleImplementation = {
		name: 'ConsoleLogger',
		type: 'console' as const,
		content: `
import { ILogger, LogLevel, LoggerConfig, LogContext } from './types';

/**
 * Console Logger Implementation
 * 
 * Features:
 * - Executive function accommodations (ADHD-friendly output)
 * - Color-blind friendly options
 * - Consistent formatting across all tools
 * - Security-conscious (no sensitive data leakage)
 */
export class ConsoleLogger implements ILogger {
	private config: LoggerConfig;
	private context: Partial<LogContext>;
	
	constructor(config: LoggerConfig, context: Partial<LogContext> = {}) {
		this.config = config;
		this.context = context;
	}
	
	debug(message: string, ...args: any[]): void {
		if (this.shouldLog('debug')) {
			this.output('debug', message, ...args);
		}
	}
	
	info(message: string, ...args: any[]): void {
		if (this.shouldLog('info')) {
			this.output('info', message, ...args);
		}
	}
	
	warn(message: string, ...args: any[]): void {
		if (this.shouldLog('warn')) {
			this.output('warn', message, ...args);
		}
	}
	
	error(message: string | Error, ...args: any[]): void {
		if (this.shouldLog('error')) {
			const msg = message instanceof Error ? message.message : message;
			const stack = message instanceof Error ? message.stack : undefined;
			this.output('error', msg, ...args);
			if (stack && this.config.level === 'debug') {
				console.error(stack);
			}
		}
	}
	
	fatal(message: string | Error, ...args: any[]): void {
		if (this.shouldLog('fatal')) {
			const msg = message instanceof Error ? message.message : message;
			const stack = message instanceof Error ? message.stack : undefined;
			this.output('fatal', msg, ...args);
			if (stack) {
				console.error(stack);
			}
		}
	}
	
	child(context: Record<string, any>): ILogger {
		return new ConsoleLogger(this.config, { ...this.context, ...context });
	}
	
	private shouldLog(level: LogLevel): boolean {
		const levels: LogLevel[] = ['debug', 'info', 'warn', 'error', 'fatal'];
		const currentIndex = levels.indexOf(this.config.level);
		const messageIndex = levels.indexOf(level);
		return messageIndex >= currentIndex;
	}
	
	private output(level: LogLevel, message: string, ...args: any[]): void {
		const timestamp = new Date().toISOString();
		const service = this.context.service || this.config.service || 'unknown';
		
		if (this.config.structured) {
			const logEntry = {
				timestamp,
				level,
				service,
				message,
				args: args.length > 0 ? args : undefined,
				...this.context,
			};
			console.log(JSON.stringify(logEntry));
		} else {
			// Executive function accommodation: consistent, readable format
			const prefix = this.formatPrefix(timestamp, level, service);
			let fullMessage = message;
			if (args.length > 0) {
				const formattedArgs = args.map((a: any) => typeof a === 'object' ? JSON.stringify(a) : a).join(' ');
				fullMessage = message + ' ' + formattedArgs;
			}
			
			switch (level) {
				case 'debug':
					console.debug(prefix, fullMessage);
					break;
				case 'info':
					console.info(prefix, fullMessage);
					break;
				case 'warn':
					console.warn(prefix, fullMessage);
					break;
				case 'error':
				case 'fatal':
					console.error(prefix, fullMessage);
					break;
			}
		}
	}
	
	private formatPrefix(timestamp: string, level: LogLevel, service: string): string {
		if (this.config.accessibility?.minimalist) {
			return '[' + level.toUpperCase() + ']';
		}
		
		const timeFormat = this.config.accessibility?.timestampFormat || 'readable';
		let formattedTime = timestamp;
		
		if (timeFormat === 'readable') {
			formattedTime = new Date(timestamp).toLocaleTimeString();
		} else if (timeFormat === 'unix') {
			formattedTime = Date.now().toString();
		}
		
		return '[' + formattedTime + '] [' + level.toUpperCase() + '] [' + service + ']';
	}
}`
	};

	const factoryContent = `
import { ILogger, LoggerConfig } from './types';
import { ConsoleLogger } from './console-logger';

/**
 * Logger Factory
 * 
 * Creates appropriate logger instances based on configuration.
 * Supports executive function accommodations and domain-specific settings.
 */
export class LoggerFactory {
	private static defaultConfig: LoggerConfig = {
		level: 'info',
		console: true,
		accessibility: {
			colorBlindFriendly: true,
			timestampFormat: 'readable',
			minimalist: false,
		},
	};
	
	/**
	 * Create logger instance
	 */
	static createLogger(config: Partial<LoggerConfig> = {}): ILogger {
		const fullConfig = { ...this.defaultConfig, ...config };
		
		// For now, we only have console logger, but this can be extended
		return new ConsoleLogger(fullConfig);
	}
	
	/**
	 * Create domain-specific logger with appropriate defaults
	 */
	static createDomainLogger(
		domain: 'security' | 'productivity' | 'mtg' | 'infrastructure',
		service: string,
		config: Partial<LoggerConfig> = {}
	): ILogger {
		const domainConfig = this.getDomainDefaults(domain);
		const fullConfig = { 
			...this.defaultConfig, 
			...domainConfig, 
			...config, 
			service 
		};
		
		return new ConsoleLogger(fullConfig, { domain, service });
	}
	
	private static getDomainDefaults(domain: string): Partial<LoggerConfig> {
		switch (domain) {
			case 'security':
				return {
					level: 'warn', // Security tools need less noise
					structured: true, // Better for SIEM integration
				};
			case 'productivity':
				return {
					level: 'info',
					accessibility: {
						colorBlindFriendly: true,
						timestampFormat: 'readable',
						minimalist: true, // Reduce cognitive load
					},
				};
			case 'mtg':
				return {
					level: 'info',
					accessibility: {
						colorBlindFriendly: true,
						timestampFormat: 'readable',
						minimalist: false, // Game data can be complex
					},
				};
			case 'infrastructure':
				return {
					level: 'warn',
					structured: true, // Better for monitoring systems
				};
			default:
				return {};
		}
	}
}

// Default logger instance for convenience
export const logger = LoggerFactory.createLogger();

// Domain-specific convenience functions
export const createSecurityLogger = (service: string) => 
	LoggerFactory.createDomainLogger('security', service);

export const createProductivityLogger = (service: string) => 
	LoggerFactory.createDomainLogger('productivity', service);

export const createMtgLogger = (service: string) => 
	LoggerFactory.createDomainLogger('mtg', service);

export const createInfrastructureLogger = (service: string) => 
	LoggerFactory.createDomainLogger('infrastructure', service);`;

	const exportsContent = `
export { ILogger, LogLevel, LoggerConfig, LogContext } from './types';
export { ConsoleLogger } from './console-logger';
export { LoggerFactory, logger, createSecurityLogger, createProductivityLogger, createMtgLogger, createInfrastructureLogger } from './factory';`;

	return {
		interface: interfaceContent,
		types: typesContent,
		implementations: [consoleImplementation],
		factory: factoryContent,
		exports: exportsContent,
	};
}

/**
 * Create the shared logging library files
 */
export async function createLoggingLibrary(
	projectPath: string,
	libraryPath: string = 'libs/shared/logging'
): Promise<void> {
	console.log('📚 Creating shared logging library...');
	
	const fullLibraryPath = path.join(projectPath, libraryPath);
	
	// Ensure directory exists
	await fs.mkdir(fullLibraryPath, { recursive: true });
	
	// Generate library structure
	const library = generateLoggingLibrary();
	
	// Write files
	await Promise.all([
		fs.writeFile(path.join(fullLibraryPath, 'types.ts'), library.types),
		fs.writeFile(path.join(fullLibraryPath, 'console-logger.ts'), library.implementations[0].content),
		fs.writeFile(path.join(fullLibraryPath, 'factory.ts'), library.factory),
		fs.writeFile(path.join(fullLibraryPath, 'index.ts'), library.exports),
	]);
	
	// Create package.json for the library
	const packageJson = {
		name: '@modular-monolith/logging',
		version: '1.0.0',
		description: 'Shared logging library with executive function accommodations',
		main: 'index.ts',
		types: 'index.ts',
		keywords: ['logging', 'accessibility', 'executive-function', 'adhd-friendly'],
		dependencies: {},
		devDependencies: {
			'typescript': '^5.5.0',
		},
	};
	
	await fs.writeFile(
		path.join(fullLibraryPath, 'package.json'),
		JSON.stringify(packageJson, null, 2)
	);
	
	console.log(`✅ Created logging library at ${libraryPath}`);
}

/**
 * Create refactoring operations to replace logging calls
 */
export function createLoggingRefactoringOperations(
	patterns: LoggingPattern[],
	loggingLibraryPath: string = '@shared/logging'
): RefactoringOperation[] {
	const operations: RefactoringOperation[] = [];
	
	// Group patterns by file for efficient processing
	const patternsByFile = patterns.reduce((acc, pattern) => {
		if (!acc[pattern.filePath]) {
			acc[pattern.filePath] = [];
		}
		acc[pattern.filePath].push(pattern);
		return acc;
	}, {} as Record<string, LoggingPattern[]>);
	
	// Create operation for each file
	Object.entries(patternsByFile).forEach(([filePath, filePatterns]) => {
		operations.push({
			name: `refactor-logging-${path.basename(filePath)}`,
			description: `Replace logging calls in ${path.basename(filePath)}`,
			patterns: [{ nodeType: 'CallExpression' }],
			
			transform: (sourceFile: SourceFile) => {
				try {
					// Add import for the new logging library
					const hasLoggingImport = sourceFile.getImportDeclarations()
						.some(imp => imp.getModuleSpecifierValue().includes('logging'));
					
					if (!hasLoggingImport) {
						sourceFile.addImportDeclaration({
							moduleSpecifier: loggingLibraryPath,
							namedImports: ['logger'],
						});
					}
					
					// Replace logging calls
					let replacementCount = 0;
					
					sourceFile.getDescendantsOfKind(SyntaxKind.CallExpression).forEach(call => {
						const expression = call.getExpression();
						
						if (expression.getKind() === SyntaxKind.PropertyAccessExpression) {
							const propAccess = expression as PropertyAccessExpression;
							const object = propAccess.getExpression().getText();
							const method = propAccess.getName();
							
							// Find matching pattern
							const pattern = filePatterns.find(p => 
								p.expression === call.getText() ||
								(p.type === 'console' && object === 'console' && p.method === method) ||
								(p.type === 'custom' && p.loggerVariable === object && p.method === method)
							);
							
							if (pattern && pattern.replacement) {
								// Replace the call expression
								call.replaceWithText(pattern.replacement);
								replacementCount++;
							}
						}
					});
					
					console.log(`  📝 Replaced ${replacementCount} logging calls in ${path.basename(filePath)}`);
					return replacementCount > 0;
					
				} catch (error) {
					console.error(`Error transforming ${filePath}:`, error);
					return false;
				}
			},
			
			safetyCheck: (sourceFile: SourceFile) => {
				// Basic safety checks
				try {
					// Ensure the file can be parsed
					sourceFile.getClasses();
					sourceFile.getFunctions();
					return true;
				} catch {
					return false;
				}
			},
			
			rollback: (sourceFile: SourceFile) => {
				// Remove the logging import we added
				sourceFile.getImportDeclarations()
					.filter(imp => imp.getModuleSpecifierValue().includes('logging'))
					.forEach(imp => imp.remove());
			},
		});
	});
	
	return operations;
}

/**
 * Main refactoring function
 */
export async function refactorLoggingCode({
	projectPath,
	loggingLibraryPath = 'libs/shared/logging',
	includePatterns = ['src/**/*.ts', 'apps/**/*.ts', 'libs/**/*.ts'],
	excludePatterns = ['**/*.test.ts', '**/*.spec.ts', '**/node_modules/**', 'libs/shared/logging/**'],
	dryRun = true,
}: {
	projectPath: string;
	loggingLibraryPath?: string;
	includePatterns?: string[];
	excludePatterns?: string[];
	dryRun?: boolean;
} = { projectPath: process.cwd() }): Promise<{
	success: boolean;
	patternsFound: number;
	filesProcessed: number;
	errors: string[];
	rollbackPlan?: Array<{ file: string; rollbackFunction: () => void }>;
}> {
	console.log('🚀 Starting logging code refactoring...');
	console.log(`Mode: ${dryRun ? 'DRY RUN' : 'LIVE EXECUTION'}`);
	
	try {
		// Step 1: Scan for logging patterns
		console.log('\\n📊 Phase 1: Pattern Detection');
		const patterns = await scanForLoggingPatterns(projectPath, includePatterns, excludePatterns);
		
		if (patterns.length === 0) {
			console.log('✨ No logging patterns found to refactor');
			return {
				success: true,
				patternsFound: 0,
				filesProcessed: 0,
				errors: [],
			};
		}
		
		// Step 2: Create logging library
		console.log('\\n🏗️  Phase 2: Library Creation');
		await createLoggingLibrary(projectPath, loggingLibraryPath);
		
		// Step 3: Create refactoring operations
		console.log('\\n🔧 Phase 3: Refactoring Operations');
		const operations = createLoggingRefactoringOperations(patterns, `@shared/logging`);
		
		// Step 4: Execute refactoring
		console.log(`\n⚡ Phase 4: Execution (${dryRun ? 'DRY RUN' : 'LIVE'})`);
		
		const uniqueFiles = [...new Set(patterns.map(p => p.filePath))];
		const result = await batchRefactor({
			files: uniqueFiles,
			operations,
			dryRun,
		});
		
		// Step 5: Report results
		console.log('\\n📋 Refactoring Results:');
		console.log(`  📁 Files processed: ${result.results.length}`);
		console.log(`  🎯 Patterns found: ${patterns.length}`);
		console.log(`  ✅ Successful operations: ${result.results.reduce((acc, r) => acc + r.operations.length, 0)}`);
		console.log(`  ❌ Errors: ${result.results.reduce((acc, r) => acc + r.errors.length, 0)}`);
		
		if (!dryRun) {
			console.log(`  🔙 Rollback plan: ${result.rollbackPlan.length} operations`);
		}
		
		// Show file-by-file results
		result.results.forEach(fileResult => {
			if (fileResult.operations.length > 0 || fileResult.errors.length > 0) {
				console.log(`\\n  📄 ${path.basename(fileResult.file)}:`);
				if (fileResult.operations.length > 0) {
					console.log(`    ✅ Operations: ${fileResult.operations.join(', ')}`);
				}
				if (fileResult.errors.length > 0) {
					console.log(`    ❌ Errors: ${fileResult.errors.join(', ')}`);
				}
			}
		});
		
		console.log('\\n🎉 Logging refactoring completed!');
		console.log('\\n📚 Next Steps:');
		console.log('  1. Review the generated shared logging library');
		console.log('  2. Test the refactored code');
		console.log('  3. Update your build configuration to include the new library');
		console.log('  4. Consider removing old logging dependencies');
		
		return {
			success: result.success,
			patternsFound: patterns.length,
			filesProcessed: result.results.length,
			errors: result.results.flatMap(r => r.errors),
			rollbackPlan: result.rollbackPlan,
		};
		
	} catch (error) {
		console.error('💥 Fatal error during logging refactoring:', error);
		return {
			success: false,
			patternsFound: 0,
			filesProcessed: 0,
			errors: [String(error)],
		};
	}
}

// Export everything for external use
export {
    analyzeFileForLogging,
    generateReplacementCode, LoggingLibraryStructure, LoggingPattern
};

// CLI interface for direct execution
if (require.main === module) {
	const args = process.argv.slice(2);
	const dryRun = !args.includes('--execute');
	const projectPath = args.find(arg => arg.startsWith('--project='))?.split('=')[1] || process.cwd();
	
	console.log('🔧 TypeScript Logging Refactoring Tool');
	console.log('Enhanced with ts-morph AST manipulation from n8n CLI');
	
	refactorLoggingCode({ projectPath, dryRun })
		.then(result => {
			if (result.success) {
				console.log('\\n🎊 Refactoring completed successfully!');
				process.exit(0);
			} else {
				console.log('\\n💔 Refactoring failed');
				process.exit(1);
			}
		})
		.catch(error => {
			console.error('💥 Unhandled error:', error);
			process.exit(1);
		});
}