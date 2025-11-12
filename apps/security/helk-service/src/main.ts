#!/usr/bin/env node

/**
 * HELK Service - Main Application Entry Point
 * 
 * The Hunting ELK (HELK) is a Docker-based security analysis platform
 * providing advanced analytics capabilities for threat hunting.
 * 
 * This service manages the HELK infrastructure including:
 * - Elasticsearch for data storage
 * - Kibana for visualization  
 * - Logstash for data processing
 * - Apache Spark for analytics
 * - Jupyter notebooks for data science
 */

import { execSync } from 'child_process';
import { Command } from 'commander';
import * as path from 'path';

const program = new Command();

// Infrastructure paths
const DOCKER_DIR = path.join(__dirname, '..', 'infrastructure', 'docker');
const SCRIPTS_DIR = path.join(__dirname, '..', 'infrastructure', 'scripts');

// Docker compose configurations
const BASIC_CONFIG = 'helk-kibana-notebook-analysis-basic.yml';
const FULL_CONFIG = 'helk-kibana-notebook-analysis-alert-basic.yml';

/**
 * Execute Docker Compose command
 */
function runDockerCompose(config: string, command: string, detached = false) {
  const args = ['-f', path.join(DOCKER_DIR, config), command];
  if (detached) args.push('-d');
  
  const cmd = `docker-compose ${args.join(' ')}`;
  console.log(`Running: ${cmd}`);
  
  try {
    execSync(cmd, { 
      stdio: 'inherit', 
      cwd: DOCKER_DIR 
    });
    console.log('✅ Command completed successfully');
  } catch (error) {
    console.error('❌ Command failed:', error instanceof Error ? error.message : String(error));
    process.exit(1);
  }
}

/**
 * Execute shell script
 */
function runScript(scriptName: string) {
  const scriptPath = path.join(DOCKER_DIR, scriptName);
  console.log(`Running script: ${scriptPath}`);
  
  try {
    execSync(`chmod +x ${scriptPath} && ${scriptPath}`, {
      stdio: 'inherit',
      cwd: DOCKER_DIR
    });
    console.log('✅ Script completed successfully');
  } catch (error) {
    console.error('❌ Script failed:', error instanceof Error ? error.message : String(error));
    process.exit(1);
  }
}

// CLI Commands
program
  .name('helk-service')
  .description('HELK Service Management CLI')
  .version('1.0.0');

program
  .command('start')
  .description('Start HELK with basic configuration (Kibana + Jupyter + Analytics)')
  .action(() => {
    runDockerCompose(BASIC_CONFIG, 'up', true);
  });

program
  .command('start:full')
  .description('Start HELK with full configuration (includes alerting)')
  .action(() => {
    runDockerCompose(FULL_CONFIG, 'up', true);
  });

program
  .command('stop')
  .description('Stop all HELK services')
  .action(() => {
    runScript('helk_remove_containers.sh');
  });

program
  .command('build')
  .description('Build HELK Docker images')
  .action(() => {
    runDockerCompose(BASIC_CONFIG, 'build');
  });

program
  .command('install')
  .description('Install HELK (first-time setup)')
  .action(() => {
    runScript('helk_docker_install.sh');
  });

program
  .command('update')
  .description('Update HELK installation')
  .action(() => {
    runScript('helk_update.sh');
  });

program
  .command('setup-firewall')
  .description('Setup firewall rules for HELK')
  .action(() => {
    runScript('helk_setup_firewall.sh');
  });

program
  .command('logs')
  .description('Show logs from HELK services')
  .action(() => {
    runDockerCompose(BASIC_CONFIG, 'logs');
  });

program
  .command('status')
  .description('Show status of HELK services')
  .action(() => {
    runDockerCompose(BASIC_CONFIG, 'ps');
  });

// Parse command line arguments
program.parse();

export default program;