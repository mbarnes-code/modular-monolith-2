import { exec } from 'child_process';
import * as fs from 'fs';
import * as os from 'os';
import { promisify } from 'util';
import { InstallResult, SystemInfo, Tool } from '../../shared/types/tool.types';

const execAsync = promisify(exec);

export class SystemService {
  private systemInfo: SystemInfo;

  constructor() {
    this.systemInfo = this.detectSystem();
  }

  private detectSystem(): SystemInfo {
    const platform = os.platform();
    const homePath = os.homedir();
    
    let packageManager = 'apt-get';
    let system = 'linux';
    let binPath = '/usr/bin';
    
    // Check for different package managers
    const packageManagers = [
      { name: 'pkg', path: '/data/data/com.termux/files/usr/bin/pkg', sys: 'termux' },
      { name: 'apt', path: '/data/data/com.termux/files/usr/bin/apt', sys: 'termux' },
      { name: 'apt-get', path: '/data/data/com.termux/files/usr/bin/apt-get', sys: 'termux' },
      { name: 'apt-get', path: '/usr/bin/apt-get', sys: 'linux' },
      { name: 'apt', path: '/usr/bin/apt', sys: 'linux' },
      { name: 'yum', path: '/usr/bin/yum', sys: 'fedora' },
      { name: 'apk', path: '/usr/bin/apk', sys: 'alpine' },
      { name: 'brew', path: '/usr/local/bin/brew', sys: 'mac' }
    ];

    for (const pm of packageManagers) {
      if (fs.existsSync(pm.path)) {
        packageManager = pm.name;
        system = pm.sys;
        break;
      }
    }

    // Detect bin path
    const binPaths = [
      '/data/data/com.termux/files/usr/bin',
      '/usr/bin',
      '/bin',
      '/usr/sbin',
      '/sbin'
    ];

    for (const path of binPaths) {
      if (fs.existsSync(path)) {
        binPath = path;
        break;
      }
    }

    return {
      packageManager,
      system,
      hasRoot: this.checkRootAccess(),
      binPath,
      homePath
    };
  }

  private checkRootAccess(): boolean {
    const sudoPaths = [
      '/usr/lib/sudo',
      '/usr/bin/sudo',
      '/usr/sbin/sudo',
      '/lib/sudo',
      '/bin/sudo',
      '/sbin/sudo',
      '/data/data/com.termux/files/usr/bin/sudo'
    ];

    return sudoPaths.some(path => fs.existsSync(path));
  }

  public getSystemInfo(): SystemInfo {
    return { ...this.systemInfo };
  }

  public async checkOnlineStatus(): Promise<boolean> {
    try {
      await execAsync('ping -c 1 google.com');
      return true;
    } catch {
      return false;
    }
  }

  public async installTool(tool: Tool): Promise<InstallResult> {
    const isOnline = await this.checkOnlineStatus();
    
    if (!isOnline) {
      return {
        success: false,
        message: 'Sorry: you are offline!!',
        toolName: tool.name
      };
    }

    try {
      // Check if tool is already installed
      const isInstalled = await this.isToolInstalled(tool);
      if (isInstalled) {
        return {
          success: false,
          message: `Sorry: '${tool.name}' is already installed!!`,
          toolName: tool.name
        };
      }

      // Install dependencies first
      if (tool.dependencies.length > 0) {
        for (const dep of tool.dependencies) {
          await this.installDependency(dep);
        }
      }

      // Install the tool based on its installer type
      await this.performInstallation(tool);

      // Verify installation
      const installSuccess = await this.isToolInstalled(tool);
      
      return {
        success: installSuccess,
        message: installSuccess 
          ? `'${tool.name}' is installed successfully !!`
          : `Sorry: '${tool.name}' is not installed !!`,
        toolName: tool.name
      };

    } catch (error) {
      return {
        success: false,
        message: `Installation failed: ${error instanceof Error ? error.message : 'Unknown error'}`,
        toolName: tool.name
      };
    }
  }

  private async isToolInstalled(tool: Tool): Promise<boolean> {
    const checkPaths = [
      `${this.systemInfo.binPath}/${tool.packageName}`,
      `${this.systemInfo.homePath}/${tool.packageName}`,
      `${this.systemInfo.homePath}/${tool.name}`
    ];

    return checkPaths.some(path => fs.existsSync(path));
  }

  private async installDependency(dependency: string): Promise<void> {
    const depPath = `${this.systemInfo.binPath}/${dependency}`;
    
    if (!fs.existsSync(depPath)) {
      const sudo = this.systemInfo.hasRoot ? 'sudo ' : '';
      const command = `${sudo}${this.systemInfo.packageManager} install ${dependency} -y`;
      await execAsync(command);
    }
  }

  private async performInstallation(tool: Tool): Promise<void> {
    const sudo = this.systemInfo.hasRoot ? 'sudo ' : '';

    switch (tool.installer) {
      case 'package_manager':
        if (tool.packageName && tool.packageName !== 'null') {
          const command = `${sudo}${this.systemInfo.packageManager} install ${tool.packageName} -y`;
          await execAsync(command);
        }
        break;

      case 'git':
        if (tool.url && tool.url !== 'null') {
          const targetPath = `${this.systemInfo.homePath}/${tool.name}`;
          const command = `${sudo}git clone ${tool.url} ${targetPath}`;
          await execAsync(command);
        }
        break;

      case 'curl':
        if (tool.url && tool.url !== 'null') {
          const targetPath = `${this.systemInfo.homePath}/${tool.packageName}`;
          const command = `${sudo}curl -o ${targetPath} ${tool.url}`;
          await execAsync(command);
        }
        break;

      case 'wget':
        if (tool.url && tool.url !== 'null') {
          const targetPath = `${this.systemInfo.homePath}/${tool.packageName}`;
          const command = `${sudo}wget ${tool.url} -O ${targetPath}`;
          await execAsync(command);
        }
        break;

      default:
        throw new Error(`Unsupported installer type: ${tool.installer}`);
    }
  }
}