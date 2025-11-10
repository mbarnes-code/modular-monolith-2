/**
 * Actual Budget Service Integration
 *
 * This service provides integration with Actual Budget, a local-first personal finance tool.
 * It acts as a bridge between the Actual Budget application and the Jane platform.
 */

import { resolve } from 'path';

export class ActualService {
  private actualPath: string;

  constructor() {
    // Path to the actual budget directory (now in actual-budget subdirectory)
    // Check if we're running from dist/ or from source
    const isInDist = __dirname.includes('/dist/');
    if (isInDist) {
      // Running from compiled code in dist/apps/actual-service/src/app/
      // Need to go back to workspace root, then to apps/actual-service/actual-budget
      this.actualPath = resolve(__dirname, '../../../../../apps/actual-service/actual-budget');
    } else {
      // Running from source in apps/actual-service/src/app/
      this.actualPath = resolve(__dirname, '../../actual-budget');
    }
  }

  /**
   * Get the path to the Actual Budget installation
   */
  getActualPath(): string {
    return this.actualPath;
  }

  /**
   * Check if Actual Budget is properly installed
   */
  async isInstalled(): Promise<boolean> {
    try {
      const fs = require('fs');
      const path = resolve(this.actualPath, 'package.json');
      return fs.existsSync(path);
    } catch (error) {
      return false;
    }
  }

  /**
   * Get Actual Budget configuration
   */
  async getConfiguration(): Promise<any> {
    if (!(await this.isInstalled())) {
      throw new Error('Actual Budget is not installed');
    }

    try {
      const fs = require('fs');
      const packagePath = resolve(this.actualPath, 'package.json');
      const packageJson = JSON.parse(fs.readFileSync(packagePath, 'utf-8'));

      return {
        name: packageJson.name,
        version: packageJson.version,
        description: packageJson.description,
        path: this.actualPath,
      };
    } catch (error) {
      throw new Error(`Failed to read Actual configuration: ${error}`);
    }
  }

  /**
   * Get the path to specific Actual Budget packages
   */
  getPackagePath(packageName: string): string {
    return resolve(this.actualPath, 'packages', packageName);
  }

  /**
   * Get the path to Actual Budget build output
   */
  getBuildPath(): string {
    return resolve(this.actualPath, 'build');
  }

  /**
   * Get the path to Actual Budget data directory
   */
  getDataPath(): string {
    return resolve(this.actualPath, 'data');
  }
}

export default ActualService;