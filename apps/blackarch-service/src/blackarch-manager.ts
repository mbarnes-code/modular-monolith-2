import { readFileSync, readdirSync, statSync } from 'fs';
import { join } from 'path';

export class BlackArchManager {
  private blackArchPath: string;

  constructor() {
    // In the built version, __dirname points to dist/blackarch-service/apps/blackarch-service/src
    // We need to go up to find the blackarch directory
    const possiblePaths = [
      join(__dirname, '../blackarch'), // Development mode
      join(__dirname, '../../blackarch'), // Built mode
      join(__dirname, '../../../blackarch'), // Alternative built path
    ];
    
    // Find the first path that exists
    const { existsSync } = require('fs');
    this.blackArchPath = possiblePaths.find(path => existsSync(path)) || possiblePaths[0];
  }

  /**
   * Get all available tool groups
   */
  getToolGroups(): string[] {
    try {
      const groupsPath = join(this.blackArchPath, 'lists/groups');
      const content = readFileSync(groupsPath, 'utf-8');
      return content.split('\n').filter(line => line.trim());
    } catch (error) {
      console.error('Error reading groups:', error);
      return [];
    }
  }

  /**
   * Get official packages list
   */
  getOfficialPackages(): string[] {
    try {
      const officialPath = join(this.blackArchPath, 'lists/official');
      const content = readFileSync(officialPath, 'utf-8');
      return content.split('\n').filter(line => line.trim());
    } catch (error) {
      console.error('Error reading official packages:', error);
      return [];
    }
  }

  /**
   * Get broken packages list
   */
  getBrokenPackages(): string[] {
    try {
      const brokenPath = join(this.blackArchPath, 'lists/broken');
      const content = readFileSync(brokenPath, 'utf-8');
      return content.split('\n').filter(line => line.trim());
    } catch (error) {
      console.error('Error reading broken packages:', error);
      return [];
    }
  }

  /**
   * Get all packages from packages directory
   */
  getAllPackages(): string[] {
    try {
      const packagesPath = join(this.blackArchPath, 'packages');
      return readdirSync(packagesPath).filter(item => {
        const itemPath = join(packagesPath, item);
        return statSync(itemPath).isDirectory();
      });
    } catch (error) {
      console.error('Error reading packages directory:', error);
      return [];
    }
  }

  /**
   * Get package information by name
   */
  getPackageInfo(packageName: string): any {
    try {
      const packagePath = join(this.blackArchPath, 'packages', packageName);
      const pkgbuildPath = join(packagePath, 'PKGBUILD');
      
      if (!statSync(pkgbuildPath).isFile()) {
        return null;
      }

      const pkgbuild = readFileSync(pkgbuildPath, 'utf-8');
      
      // Basic PKGBUILD parsing
      const lines = pkgbuild.split('\n');
      const info: any = { name: packageName };
      
      lines.forEach(line => {
        if (line.startsWith('pkgname=')) {
          info.pkgname = line.split('=')[1].replace(/['"]/g, '');
        } else if (line.startsWith('pkgver=')) {
          info.version = line.split('=')[1].replace(/['"]/g, '');
        } else if (line.startsWith('pkgdesc=')) {
          info.description = line.split('=')[1].replace(/['"]/g, '');
        } else if (line.startsWith('url=')) {
          info.url = line.split('=')[1].replace(/['"]/g, '');
        } else if (line.startsWith('arch=')) {
          info.arch = line.split('=')[1];
        } else if (line.startsWith('license=')) {
          info.license = line.split('=')[1];
        }
      });

      return info;
    } catch (error) {
      console.error(`Error reading package ${packageName}:`, error);
      return null;
    }
  }

  /**
   * Search packages by keyword
   */
  searchPackages(keyword: string): string[] {
    const allPackages = this.getAllPackages();
    const searchTerm = keyword.toLowerCase();
    
    return allPackages.filter(pkg => {
      if (pkg.toLowerCase().includes(searchTerm)) {
        return true;
      }
      
      // Also search in package description
      const info = this.getPackageInfo(pkg);
      if (info && info.description && info.description.toLowerCase().includes(searchTerm)) {
        return true;
      }
      
      return false;
    });
  }

  /**
   * Get statistics about the BlackArch repository
   */
  getStats(): any {
    const allPackages = this.getAllPackages();
    const officialPackages = this.getOfficialPackages();
    const brokenPackages = this.getBrokenPackages();
    const groups = this.getToolGroups();

    return {
      totalPackages: allPackages.length,
      officialPackages: officialPackages.length,
      brokenPackages: brokenPackages.length,
      totalGroups: groups.length,
      repositoryPath: this.blackArchPath
    };
  }
}