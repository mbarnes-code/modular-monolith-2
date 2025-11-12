import { environment } from '../../environments/environment';

export class ConfigService {
  private static instance: ConfigService;
  
  private constructor() {}
  
  public static getInstance(): ConfigService {
    if (!ConfigService.instance) {
      ConfigService.instance = new ConfigService();
    }
    return ConfigService.instance;
  }
  
  get port(): number {
    return environment.port;
  }
  
  get host(): string {
    return environment.host;
  }
  
  get isProduction(): boolean {
    return environment.production;
  }
  
  get blackarchConfig() {
    return environment.blackarch;
  }
  
  get loggingLevel(): string {
    return environment.logging.level;
  }
}

export const configService = ConfigService.getInstance();