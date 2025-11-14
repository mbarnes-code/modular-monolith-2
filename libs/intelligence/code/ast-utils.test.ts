/**
 * TypeScript AST Utilities - Comprehensive Test Suite
 * 
 * Enhanced test suite based on n8n CLI patterns, extended for all TypeScript projects.
 * Tests core AST manipulation, domain operations, and AI-enhanced features.
 */

import { describe, it, expect, beforeEach, afterEach } from 'vitest';
import { Project, SyntaxKind } from 'ts-morph';
import { vol } from 'memfs';

import {
	loadSourceFile,
	loadProject,
	updateStringProperty,
	getChildObjectLiteral,
	updateArrayProperty,
	updateClassDeclaration,
	updateInterfaceDeclaration,
	updateImports,
	analyzeCodePatterns,
	batchProcess,
} from './ast-utils';

import {
	updateApiServiceClass,
	updateReactComponent,
	updateAuthConfiguration,
	applyExecutiveFunctionAccommodations,
	applySecurityBestPractices,
	batchRefactor,
	generateFromTemplate,
} from './domain-operations';

import type { ProjectConfig, ASTOperationContext, CodeTemplate } from './types';

// Mock file system for testing
jest.mock('fs');

describe('Enhanced TypeScript AST Utilities', () => {
	const createSourceFile = (content: string, path: string = 'test.ts') => {
		const project = new Project({ useInMemoryFileSystem: true });
		return project.createSourceFile(path, content);
	};

	const createProjectConfig = (): ProjectConfig => ({
		skipDependencies: true,
		useInMemory: true,
		compilerOptions: {
			target: 'ES2020',
			module: 'ESNext',
			strict: true,
		},
	});

	describe('Core AST Operations', () => {
		describe('updateStringProperty', () => {
			it('should update object literal property', () => {
				const content = 'export const config = { name: "oldName", version: "1.0.0" };';
				const sourceFile = createSourceFile(content);
				const configVar = sourceFile.getVariableDeclarationOrThrow('config');
				const configObj = configVar.getInitializerIfKindOrThrow(SyntaxKind.ObjectLiteralExpression);

				const success = updateStringProperty({ obj: configObj, key: 'name', value: 'newName' });

				expect(success).toBe(true);
				expect(sourceFile.getFullText()).toContain('name: "newName"');
				expect(sourceFile.getFullText()).not.toContain('name: "oldName"');
			});

			it('should update class property', () => {
				const content = 'export class Config { name = "oldName"; version = "1.0.0"; }';
				const sourceFile = createSourceFile(content);
				const classDecl = sourceFile.getClassOrThrow('Config');

				const success = updateStringProperty({ obj: classDecl, key: 'name', value: 'newName' });

				expect(success).toBe(true);
				expect(sourceFile.getFullText()).toContain('name = "newName"');
			});

			it('should create missing property when requested', () => {
				const content = 'export const config = { version: "1.0.0" };';
				const sourceFile = createSourceFile(content);
				const configVar = sourceFile.getVariableDeclarationOrThrow('config');
				const configObj = configVar.getInitializerIfKindOrThrow(SyntaxKind.ObjectLiteralExpression);

				const success = updateStringProperty({
					obj: configObj,
					key: 'name',
					value: 'newName',
					createIfMissing: true,
				});

				expect(success).toBe(true);
				expect(sourceFile.getFullText()).toContain('name: "newName"');
			});

			it('should handle errors gracefully with context', () => {
				const content = 'export const config = { name: "test", count: 42 };';
				const sourceFile = createSourceFile(content);
				const configVar = sourceFile.getVariableDeclarationOrThrow('config');
				const configObj = configVar.getInitializerIfKindOrThrow(SyntaxKind.ObjectLiteralExpression);

				const context: ASTOperationContext = { logErrors: true };
				const success = updateStringProperty({ obj: configObj, key: 'count', value: 'new', context });

				expect(success).toBe(false);
			});
		});

		describe('getChildObjectLiteral', () => {
			it('should return nested object', () => {
				const content = `
export const config = {
    database: { host: "localhost", port: "5432" },
    cache: { ttl: "3600" }
};`;
				const sourceFile = createSourceFile(content);
				const configVar = sourceFile.getVariableDeclarationOrThrow('config');
				const configObj = configVar.getInitializerIfKindOrThrow(SyntaxKind.ObjectLiteralExpression);

				const dbObj = getChildObjectLiteral({ obj: configObj, key: 'database' });

				expect(dbObj).not.toBeNull();
				expect(dbObj!.getProperty('host')).toBeDefined();
				expect(dbObj!.getProperty('port')).toBeDefined();
			});

			it('should create missing object when requested', () => {
				const content = 'export const config = { cache: { ttl: "3600" } };';
				const sourceFile = createSourceFile(content);
				const configVar = sourceFile.getVariableDeclarationOrThrow('config');
				const configObj = configVar.getInitializerIfKindOrThrow(SyntaxKind.ObjectLiteralExpression);

				const dbObj = getChildObjectLiteral({ obj: configObj, key: 'database', createIfMissing: true });

				expect(dbObj).not.toBeNull();
				expect(sourceFile.getFullText()).toContain('database: {}');
			});

			it('should return null for non-object property', () => {
				const content = 'export const config = { name: "test", count: 42 };';
				const sourceFile = createSourceFile(content);
				const configVar = sourceFile.getVariableDeclarationOrThrow('config');
				const configObj = configVar.getInitializerIfKindOrThrow(SyntaxKind.ObjectLiteralExpression);

				const result = getChildObjectLiteral({ obj: configObj, key: 'name' });

				expect(result).toBeNull();
			});
		});

		describe('updateArrayProperty', () => {
			it('should replace array elements', () => {
				const content = 'export const config = { tags: ["old1", "old2"] };';
				const sourceFile = createSourceFile(content);
				const configVar = sourceFile.getVariableDeclarationOrThrow('config');
				const configObj = configVar.getInitializerIfKindOrThrow(SyntaxKind.ObjectLiteralExpression);

				const success = updateArrayProperty({
					obj: configObj,
					key: 'tags',
					values: ['new1', 'new2', 'new3'],
					mode: 'replace',
				});

				expect(success).toBe(true);
				expect(sourceFile.getFullText()).toContain('"new1"');
				expect(sourceFile.getFullText()).toContain('"new2"');
				expect(sourceFile.getFullText()).toContain('"new3"');
				expect(sourceFile.getFullText()).not.toContain('"old1"');
			});

			it('should append to array', () => {
				const content = 'export const config = { tags: ["existing"] };';
				const sourceFile = createSourceFile(content);
				const configVar = sourceFile.getVariableDeclarationOrThrow('config');
				const configObj = configVar.getInitializerIfKindOrThrow(SyntaxKind.ObjectLiteralExpression);

				const success = updateArrayProperty({
					obj: configObj,
					key: 'tags',
					values: ['new1', 'new2'],
					mode: 'append',
				});

				expect(success).toBe(true);
				expect(sourceFile.getFullText()).toContain('"existing"');
				expect(sourceFile.getFullText()).toContain('"new1"');
				expect(sourceFile.getFullText()).toContain('"new2"');
			});

			it('should merge unique values', () => {
				const content = 'export const config = { tags: ["existing", "old"] };';
				const sourceFile = createSourceFile(content);
				const configVar = sourceFile.getVariableDeclarationOrThrow('config');
				const configObj = configVar.getInitializerIfKindOrThrow(SyntaxKind.ObjectLiteralExpression);

				const success = updateArrayProperty({
					obj: configObj,
					key: 'tags',
					values: ['existing', 'new1', 'new2'],
					mode: 'merge',
				});

				expect(success).toBe(true);
				expect(sourceFile.getFullText()).toContain('"existing"');
				expect(sourceFile.getFullText()).toContain('"new1"');
				expect(sourceFile.getFullText()).toContain('"new2"');
				// Should only have one instance of "existing"
				expect((sourceFile.getFullText().match(/"existing"/g) || []).length).toBe(1);
			});
		});

		describe('updateClassDeclaration', () => {
			it('should update class with all features', () => {
				const content = `
export class OldService {
	name = "old";
	getValue() { return "old"; }
}`;
				const sourceFile = createSourceFile(content);

				const result = updateClassDeclaration({
					sourceFile,
					className: 'OldService',
					updates: {
						name: 'NewService',
						properties: { name: 'new', version: '2.0.0' },
						methods: [{ name: 'getValue', body: 'return "new";', returnType: 'string' }],
						implements: ['IService'],
						extends: 'BaseService',
					},
				});

				expect(result).not.toBeNull();
				expect(sourceFile.getFullText()).toContain('class NewService extends BaseService implements IService');
				expect(sourceFile.getFullText()).toContain('name = "new"');
				expect(sourceFile.getFullText()).toContain('version = "2.0.0"');
			});
		});

		describe('updateImports', () => {
			it('should merge imports correctly', () => {
				const content = `import { useState } from 'react';`;
				const sourceFile = createSourceFile(content);

				updateImports({
					sourceFile,
					imports: [
						{
							moduleSpecifier: 'react',
							namedImports: ['useEffect', 'useContext'],
						},
						{
							moduleSpecifier: 'lodash',
							namedImports: ['debounce'],
						},
					],
					mode: 'merge',
				});

				const finalText = sourceFile.getFullText();
				expect(finalText).toContain('useState');
				expect(finalText).toContain('useEffect');
				expect(finalText).toContain('useContext');
				expect(finalText).toContain('debounce');
			});
		});
	});

	describe('Domain-Specific Operations', () => {
		describe('updateApiServiceClass', () => {
			it('should update API service configuration', () => {
				const content = `
export class ApiService {
	config = {
		displayName: "Old API",
		name: "oldApi",
		requestDefaults: {
			baseURL: "https://old.api.com"
		}
	};
}`;
				const sourceFile = createSourceFile(content, 'test-service.ts');
				vol.fromJSON({ '/test-service.ts': content });

				const result = updateApiServiceClass({
					servicePath: '/test-service.ts',
					className: 'NewApiService',
					baseUrl: 'https://new.api.com',
					apiConfig: {
						displayName: 'New API Service',
						description: 'Enhanced API integration',
						version: '2.0.0',
					},
				});

				expect(result.getFullText()).toContain('class NewApiService');
				expect(result.getFullText()).toContain('displayName: "New API Service"');
				expect(result.getFullText()).toContain('baseURL: "https://new.api.com"');
			});
		});

		describe('updateAuthConfiguration', () => {
			it('should update authentication class', () => {
				const content = `
export class OldCredentials {
	displayName = "Old Auth";
	name = "oldAuth";
}`;
				const sourceFile = createSourceFile(content, 'test-auth.ts');
				vol.fromJSON({ '/test-auth.ts': content });

				const result = updateAuthConfiguration({
					authPath: '/test-auth.ts',
					authName: 'newAuth',
					authType: 'apiKey',
					config: {
						displayName: 'New Authentication',
						description: 'Enhanced auth system',
					},
				});

				expect(result.getFullText()).toContain('class NewAuthCredentials');
				expect(result.getFullText()).toContain('displayName: "New Authentication"');
			});
		});

		describe('applyExecutiveFunctionAccommodations', () => {
			it('should enforce consistent naming', () => {
				const content = `
export class bad_class_name {
	bad_method_name() {}
}

export function Bad_Function_Name() {}
`;
				const sourceFile = createSourceFile(content, 'test-naming.ts');
				vol.fromJSON({ '/test-naming.ts': content });

				const result = applyExecutiveFunctionAccommodations({
					filePath: '/test-naming.ts',
					accommodations: {
						enforceConsistentNaming: true,
					},
				});

				expect(result.getFullText()).toContain('class BadClassName');
				expect(result.getFullText()).toContain('function badFunctionName');
			});

			it('should warn about complex functions', () => {
				const content = `
export function complexFunction(a: string, b: number, c: boolean, d: object, e: any, f: string) {
	return a + b;
}`;
				const sourceFile = createSourceFile(content, 'test-complex.ts');
				vol.fromJSON({ '/test-complex.ts': content });

				const consoleSpy = jest.spyOn(console, 'warn').mockImplementation();

				applyExecutiveFunctionAccommodations({
					filePath: '/test-complex.ts',
					accommodations: {
						maxParameterCount: 4,
					},
					context: { logErrors: true },
				});

				expect(consoleSpy).toHaveBeenCalledWith(
					expect.stringContaining('complexFunction has 6 parameters')
				);

				consoleSpy.mockRestore();
			});
		});
	});

	describe('Code Analysis', () => {
		describe('analyzeCodePatterns', () => {
			it('should analyze code quality metrics', () => {
				const content = `
export class TestService {
	private password = "hardcoded123";
	
	public authenticate(user: string, pass: string) {
		if (user && pass) {
			for (let i = 0; i < 10; i++) {
				if (this.validateUser(user)) {
					return true;
				}
			}
		}
		return false;
	}
	
	private validateUser(user: string): boolean {
		return user.length > 0;
	}
}`;
				const sourceFile = createSourceFile(content);

				const analysis = analyzeCodePatterns(sourceFile);

				expect(analysis.complexity).toBeGreaterThan(1);
				expect(analysis.maintainability).toBeGreaterThan(0);
				expect(analysis.securityScore).toBeLessThan(80); // Should detect hardcoded password
				expect(analysis.executiveFunctionScore).toBeGreaterThan(0);
			});
		});
	});

	describe('Template Generation', () => {
		describe('generateFromTemplate', () => {
			it('should generate code from template', () => {
				const template: CodeTemplate = {
					name: 'react-component',
					category: 'component',
					template: `
import React from 'react';

interface {{componentName}}Props {
	{{#each props}}
	{{name}}: {{type}};
	{{/each}}
}

export const {{componentName}}: React.FC<{{componentName}}Props> = (props) => {
	return (
		<div className="{{kebabCase componentName}}">
			<h1>{{componentName}}</h1>
		</div>
	);
};`,
					variables: {
						componentName: {
							type: 'string',
							description: 'Name of the React component',
							required: true,
						},
						props: {
							type: 'array',
							description: 'Component props',
							required: false,
							default: [],
						},
					},
					fileExtension: 'tsx',
				};

				const result = generateFromTemplate({
					template,
					variables: {
						componentName: 'UserProfile',
						props: [
							{ name: 'userId', type: 'string' },
							{ name: 'onEdit', type: '() => void' },
						],
					},
					outputPath: 'UserProfile.tsx',
				});

				expect(result.success).toBe(true);
				expect(result.content).toContain('UserProfile');
				expect(result.content).toContain('React.FC<UserProfileProps>');
			});

			it('should validate required variables', () => {
				const template: CodeTemplate = {
					name: 'test-template',
					category: 'test',
					template: 'Hello {{name}}!',
					variables: {
						name: {
							type: 'string',
							description: 'Name to greet',
							required: true,
						},
					},
					fileExtension: 'ts',
				};

				const result = generateFromTemplate({
					template,
					variables: {},
					outputPath: 'test.ts',
				});

				expect(result.success).toBe(false);
				expect(result.errors).toContain("Required variable 'name' is missing");
			});
		});
	});

	describe('Batch Operations', () => {
		describe('batchProcess', () => {
			it('should process multiple files in parallel', async () => {
				const files = ['file1.ts', 'file2.ts', 'file3.ts'];
				const fileContents = {
					'/file1.ts': 'export const config = { name: "file1" };',
					'/file2.ts': 'export const config = { name: "file2" };',
					'/file3.ts': 'export const config = { name: "file3" };',
				};

				vol.fromJSON(fileContents);

				const operations = [
					(sourceFile: any) => {
						const configVar = sourceFile.getVariableDeclaration('config');
						if (configVar) {
							const configObj = configVar.getInitializerIfKind(SyntaxKind.ObjectLiteralExpression);
							if (configObj) {
								updateStringProperty({ obj: configObj, key: 'name', value: 'updated' });
							}
						}
					},
				];

				const result = await batchProcess({
					files: files.map(f => `/${f}`),
					operations,
					parallelism: 2,
				});

				expect(result.processed).toBe(3);
				expect(result.errors).toHaveLength(0);
			});
		});
	});

	afterEach(() => {
		vol.reset();
	});
});