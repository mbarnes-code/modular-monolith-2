import * as path from 'path';
import { environment } from '../../environments/environment';

export const config = {
  getAssetsPath() {
    return path.join(__dirname, '..', '..', 'assets');
  },

  isProduction() {
    return environment.production;
  },

  getEnvironmentName() {
    return environment.name;
  },

  getPort() {
    return parseInt(process.env['PORT'] || '3333', 10);
  },

  getToolkitComponents() {
    return [
      'Adhoc Scripts (Python, Shell)',
      'Beacon Object Files (BOFs)',
      'Deprecated Payloads',
      'Patch Environment Exit Utilities'
    ];
  }
};