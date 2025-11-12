import { BlackArchError, BlackArchPackage, BlackArchStats } from 'blackarch';
import * as fs from 'fs';
import * as path from 'path';
import { configService } from '../config/config.service';

export class BlackArchService {
  private packages: BlackArchPackage[] = [];
  private repositoryPath: string;
  
  constructor() {
    this.repositoryPath = this.findRepositoryPath();
    this.loadPackages();
  }
  
  private findRepositoryPath(): string {
    // Try configured path first
    if (configService.blackarchConfig.repositoryPath) {
      if (fs.existsSync(configService.blackarchConfig.repositoryPath)) {
        return configService.blackarchConfig.repositoryPath;
      }
    }
    
    // Development paths
    const devPaths = [
      path.join(process.cwd(), 'src', 'assets', 'blackarch'),
      path.join(process.cwd(), 'assets', 'blackarch'),
      path.join(__dirname, '..', '..', 'assets', 'blackarch'),
      path.join(__dirname, '..', 'assets', 'blackarch'),
      path.join(process.cwd(), 'apps', 'blackarch-service', 'src', 'assets', 'blackarch'),
      path.join(process.cwd(), 'dist', 'apps', 'blackarch-service', 'assets', 'blackarch')
    ];
    
    for (const devPath of devPaths) {
      if (fs.existsSync(devPath)) {
        return devPath;
      }
    }
    
    throw new BlackArchError('BlackArch repository not found in any expected location');
  }
  
  private loadPackages(): void {
    try {
      this.packages = this.loadPackagesRecursively(this.repositoryPath);
    } catch (error) {
      throw new BlackArchError(`Failed to load packages: ${error instanceof Error ? error.message : String(error)}`);
    }
  }
  
  private loadPackagesRecursively(dir: string): BlackArchPackage[] {
    const packages: BlackArchPackage[] = [];
    
    try {
      const entries = fs.readdirSync(dir, { withFileTypes: true });
      
      for (const entry of entries) {
        const fullPath = path.join(dir, entry.name);
        
        if (entry.isDirectory()) {
          packages.push(...this.loadPackagesRecursively(fullPath));
        } else if (entry.name === 'PKGBUILD') {
          try {
            const pkg = this.parsePKGBUILD(fullPath);
            if (pkg) {
              packages.push(pkg);
            }
          } catch (error) {
            console.warn(`Failed to parse PKGBUILD at ${fullPath}:`, error);
          }
        }
      }
    } catch (error) {
      console.warn(`Failed to read directory ${dir}:`, error);
    }
    
    return packages;
  }
  
  private parsePKGBUILD(pkgbuildPath: string): BlackArchPackage | null {
    try {
      const content = fs.readFileSync(pkgbuildPath, 'utf-8');
      const lines = content.split('\n');
      
      const pkg: Partial<BlackArchPackage> = {
        path: path.dirname(pkgbuildPath)
      };
      
      for (const line of lines) {
        const trimmed = line.trim();
        
        if (trimmed.startsWith('pkgname=')) {
          pkg.name = this.extractValue(trimmed);
        } else if (trimmed.startsWith('pkgver=')) {
          pkg.version = this.extractValue(trimmed);
        } else if (trimmed.startsWith('pkgrel=')) {
          pkg.release = this.extractValue(trimmed);
        } else if (trimmed.startsWith('pkgdesc=')) {
          pkg.description = this.extractValue(trimmed);
        } else if (trimmed.startsWith('url=')) {
          pkg.url = this.extractValue(trimmed);
        } else if (trimmed.startsWith('license=')) {
          const licenseValue = this.extractValue(trimmed);
          pkg.license = licenseValue ? [licenseValue] : undefined;
        } else if (trimmed.startsWith('arch=')) {
          const archValue = this.extractValue(trimmed);
          pkg.arch = archValue ? [archValue] : undefined;
        } else if (trimmed.startsWith('depends=')) {
          const dependsValue = this.extractValue(trimmed);
          pkg.depends = dependsValue ? [dependsValue] : undefined;
        } else if (trimmed.startsWith('groups=')) {
          const groupsValue = this.extractValue(trimmed);
          pkg.groups = groupsValue ? [groupsValue] : undefined;
        }
      }
      
      if (pkg.name) {
        return {
          name: pkg.name,
          version: pkg.version || 'unknown',
          release: pkg.release || '1',
          description: pkg.description || '',
          url: pkg.url || '',
          license: pkg.license || [],
          arch: pkg.arch || [],
          depends: pkg.depends || [],
          groups: pkg.groups || [],
          path: pkg.path || ''
        };
      }
      
      return null;
    } catch (error) {
      return null;
    }
  }
  
  private extractValue(line: string): string {
    const match = line.match(/=(.*)$/);
    if (match) {
      let value = match[1].trim();
      // Remove quotes if present
      if ((value.startsWith('"') && value.endsWith('"')) ||
          (value.startsWith("'") && value.endsWith("'"))) {
        value = value.slice(1, -1);
      }
      // Handle arrays (simplified)
      if (value.startsWith('(') && value.endsWith(')')) {
        value = value.slice(1, -1).split(/\s+/)[0] || '';
      }
      return value;
    }
    return '';
  }
  
  public getStats(): BlackArchStats {
    const official = this.packages.filter(p => !p.name.includes('-git')).length;
    const broken = this.packages.filter(p => !p.description || p.description.toLowerCase().includes('broken')).length;
    
    return {
      total: this.packages.length,
      official,
      broken,
      working: this.packages.length - broken
    };
  }
  
  public getAllPackages(): BlackArchPackage[] {
    return [...this.packages];
  }
  
  public getPackage(name: string): BlackArchPackage | undefined {
    return this.packages.find(p => p.name === name);
  }
  
  public searchPackages(query: string): BlackArchPackage[] {
    const searchTerm = query.toLowerCase();
    const maxResults = configService.blackarchConfig.maxSearchResults;
    
    return this.packages
      .filter(p => 
        p.name.toLowerCase().includes(searchTerm) ||
        p.description.toLowerCase().includes(searchTerm)
      )
      .slice(0, maxResults);
  }
  
  public getPackagesByGroup(group?: string): BlackArchPackage[] {
    if (!group) {
      return [...this.packages];
    }
    
    return this.packages.filter(p => 
      p.groups.some(g => g.toLowerCase() === group.toLowerCase())
    );
  }
  
  public getGroups(): string[] {
    const groups = new Set<string>();
    
    for (const pkg of this.packages) {
      for (const group of pkg.groups) {
        groups.add(group);
      }
    }
    
    return Array.from(groups).sort();
  }
}

// Singleton instance
export const blackArchService = new BlackArchService();