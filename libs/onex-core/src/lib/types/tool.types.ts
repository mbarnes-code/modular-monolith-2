export interface Tool {
  name: string;
  packageName: string;
  category: string | null;
  url: string;
  installer: ToolInstaller;
  dependencies: string[];
}

export interface Category {
  displayName: string;
  key: string;
}

export type ToolInstaller = 'package_manager' | 'git' | 'curl' | 'wget';

export interface InstallResult {
  success: boolean;
  message: string;
  toolName: string;
}

export interface SystemInfo {
  packageManager: string;
  system: string;
  hasRoot: boolean;
  binPath: string;
  homePath: string;
}