#!/usr/bin/env ts-node

/**
 * KasmVNC Service - Main Entry Point
 * 
 * This is the main entry point for the KasmVNC service in the NX monorepo.
 * It provides CLI commands for building, running, and managing KasmVNC.
 */

import { execSync } from 'child_process';
import { program } from 'commander';
import { join } from 'path';

const KASMVNC_ROOT = join(__dirname, '..');

interface BuildOptions {
  docker?: boolean;
  deb?: boolean;
  rpm?: boolean;
  apk?: boolean;
  tarball?: boolean;
  web?: boolean;
}

interface ServeOptions {
  dev?: boolean;
  web?: boolean;
  port?: string;
}

class KasmVNCService {
  private execCommand(command: string, cwd?: string): void {
    console.log(`Executing: ${command}`);
    try {
      execSync(command, { 
        cwd: cwd || KASMVNC_ROOT, 
        stdio: 'inherit',
        env: { ...process.env }
      });
    } catch (error) {
      console.error(`Command failed: ${command}`);
      process.exit(1);
    }
  }

  async setup(): Promise<void> {
    console.log('🚀 Setting up KasmVNC service...');
    
    // Initialize submodules (web interface)
    console.log('📦 Initializing web interface...');
    this.execCommand('git clone --depth 1 https://github.com/kasmtech/noVNC.git src/kasmweb || echo "kasmweb already exists"');
    
    // Install web dependencies
    console.log('📦 Installing web dependencies...');
    this.execCommand('npm install', join(KASMVNC_ROOT, 'src/kasmweb'));
    
    // Install Python dependencies
    console.log('🐍 Installing Python dependencies...');
    this.execCommand('pip install -r Pipfile --break-system-packages || echo "Python dependencies installation complete"');
    
    console.log('✅ KasmVNC service setup complete!');
  }

  async build(options: BuildOptions = {}): Promise<void> {
    console.log('🔨 Building KasmVNC...');

    if (options.web) {
      console.log('🌐 Building web interface...');
      this.execCommand('npm run build', join(KASMVNC_ROOT, 'src/kasmweb'));
      return;
    }

    if (options.docker) {
      console.log('🐳 Building Docker image...');
      this.execCommand('docker build -t kasmvnc:dev -f infrastructure/builder/dockerfile.ubuntu_jammy.dev .');
      return;
    }

    if (options.deb) {
      console.log('📦 Building DEB package...');
      this.execCommand('./infrastructure/builder/build-deb');
      return;
    }

    if (options.rpm) {
      console.log('📦 Building RPM package...');
      this.execCommand('./infrastructure/builder/build-rpm');
      return;
    }

    if (options.apk) {
      console.log('📦 Building APK package...');
      this.execCommand('./infrastructure/builder/build-apk');
      return;
    }

    if (options.tarball) {
      console.log('📦 Building source tarball...');
      this.execCommand('./infrastructure/builder/build-tarball');
      return;
    }

    // Default build
    console.log('🔨 Building KasmVNC server from source...');
    this.execCommand('./infrastructure/builder/build.sh');
    console.log('✅ Build complete!');
  }

  async serve(options: ServeOptions = {}): Promise<void> {
    if (options.web) {
      console.log('🌐 Starting web development server...');
      this.execCommand('npm run serve', join(KASMVNC_ROOT, 'src/kasmweb'));
      return;
    }

    const port = options.port || '6901';
    const sslPort = '8443';

    if (options.dev) {
      console.log(`🐳 Starting KasmVNC development container (ports: ${port}, ${sslPort})...`);
      this.execCommand(`docker run -it --rm -v ./:/src -p ${port}:6901 -p ${sslPort}:8443 --name kasmvnc_dev kasmvnc:dev /bin/bash`);
    } else {
      console.log(`🐳 Starting KasmVNC service (ports: ${port}, ${sslPort})...`);
      this.execCommand(`docker run -it --rm -v ./:/src -p ${port}:6901 -p ${sslPort}:8443 --name kasmvnc_dev kasmvnc:dev`);
    }
  }

  async test(): Promise<void> {
    console.log('🧪 Running KasmVNC tests...');
    this.execCommand('./run-specs');
  }

  async clean(): Promise<void> {
    console.log('🧹 Cleaning build artifacts...');
    this.execCommand('rm -rf xorg.build src/kasmweb/node_modules src/kasmweb/dist');
    console.log('✅ Clean complete!');
  }

  async status(): Promise<void> {
    console.log('📊 KasmVNC Service Status:');
    
    // Check if Docker image exists
    try {
      execSync('docker image inspect kasmvnc:dev', { stdio: 'pipe' });
      console.log('✅ Docker image: kasmvnc:dev exists');
    } catch {
      console.log('❌ Docker image: kasmvnc:dev not found');
    }

    // Check if web dependencies are installed
    try {
      execSync('test -d src/kasmweb/node_modules', { cwd: KASMVNC_ROOT, stdio: 'pipe' });
      console.log('✅ Web dependencies: installed');
    } catch {
      console.log('❌ Web dependencies: not installed');
    }

    // Check if web interface is built
    try {
      execSync('test -d src/kasmweb/dist', { cwd: KASMVNC_ROOT, stdio: 'pipe' });
      console.log('✅ Web interface: built');
    } catch {
      console.log('❌ Web interface: not built');
    }

    // Check if KasmVNC is built
    try {
      execSync('test -d xorg.build', { cwd: KASMVNC_ROOT, stdio: 'pipe' });
      console.log('✅ KasmVNC server: built');
    } catch {
      console.log('❌ KasmVNC server: not built');
    }
  }
}

const service = new KasmVNCService();

// CLI Setup
program
  .name('kasmvnc-service')
  .description('KasmVNC Service Management CLI')
  .version('1.0.0');

program
  .command('setup')
  .description('Initialize and setup KasmVNC service')
  .action(() => service.setup());

program
  .command('build')
  .description('Build KasmVNC server or components')
  .option('-d, --docker', 'Build Docker image')
  .option('--deb', 'Build DEB package')
  .option('--rpm', 'Build RPM package')
  .option('--apk', 'Build APK package')
  .option('--tarball', 'Build source tarball')
  .option('-w, --web', 'Build web interface only')
  .action((options) => service.build(options));

program
  .command('serve')
  .description('Start KasmVNC service')
  .option('-d, --dev', 'Start development container with shell')
  .option('-w, --web', 'Start web development server')
  .option('-p, --port <port>', 'Specify port for VNC (default: 6901)')
  .action((options) => service.serve(options));

program
  .command('test')
  .description('Run KasmVNC tests')
  .action(() => service.test());

program
  .command('clean')
  .description('Clean build artifacts')
  .action(() => service.clean());

program
  .command('status')
  .description('Show service status')
  .action(() => service.status());

// Handle unknown commands
program
  .action(() => {
    console.log('Unknown command. Use --help for available commands.');
    program.help();
  });

if (require.main === module) {
  program.parse(process.argv);
}

export default KasmVNCService;