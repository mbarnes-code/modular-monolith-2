#!/usr/bin/env node

import { OnexService } from '@jane-monorepo/onex-core';
import chalk from 'chalk';
import { Command } from 'commander';

const program = new Command();
const onexService = new OnexService();

// Logo and colors matching the original onex
const logo = chalk.yellow(`
  ___  _ __   ___`) + chalk.red(`__  __
`) + chalk.yellow(` / _ \\| '_ \\ / _ `) + chalk.red(`\\ \\/ /
`) + chalk.yellow(`| (_) | | | |  __/`) + chalk.red(`>  < 
`) + chalk.yellow(` \___/|_| |_|\\___`) + chalk.red(`/_/\\_\\
`);

// Utility functions
function displayLogo() {
  console.log(logo);
}

function prompt(): string {
  return chalk.cyan('[') + chalk.blue('onex') + chalk.cyan('@') + chalk.blue('space') + chalk.cyan(']$');
}

async function interactiveMenu() {
  console.clear();
  const stats = onexService.getStats();
  displayLogo();
  
  console.log(chalk.white(' [1] ') + chalk.green(`All tools `) + chalk.white('(') + chalk.red(`${stats.toolsCount} tools`) + chalk.white(')'));
  console.log(chalk.white(' [2] ') + chalk.green('Tools category'));
  console.log(chalk.white(' [3] ') + chalk.green('Update onex'));
  console.log(chalk.white(' [4] ') + chalk.green('About us'));
  console.log(chalk.white(' [5] ') + chalk.green('Exit'));
  
  console.log('\nUse specific commands:');
  console.log(chalk.blue('  onex list         - List all tools'));
  console.log(chalk.blue('  onex categories   - Show categories'));
  console.log(chalk.blue('  onex search <term> - Search tools'));
  console.log(chalk.blue('  onex install <tool> - Install a tool'));
  console.log(chalk.blue('  onex info <tool>   - Get tool info'));
  console.log(chalk.blue('  onex stats        - Show statistics'));
}



function showAbout() {
  console.clear();
  displayLogo();
  console.log(chalk.yellow(' Onex ') + chalk.red('v1.0.0'));
  console.log(' Onex is a library of all');
  console.log(' hacking tools for termux');
  console.log(' and other linux distribution.');
}

// CLI Commands
program
  .name('onex')
  .description('Onex Hacking Tools Library - CLI Interface')
  .version('1.0.0');

program
  .command('start')
  .description('Start onex interactive menu mode')
  .action(async () => {
    await interactiveMenu();
  });

program
  .command('list')
  .alias('l')
  .description('List all tools')
  .option('-a, --all', 'List all tools (same as default)')
  .action((options) => {
    const tools = onexService.getAllTools();
    tools.forEach((tool, index) => {
      console.log(chalk.green(`${index + 1} ${tool.name}`));
    });
  });

program
  .command('search <query>')
  .alias('s')
  .description('Search tools by name')
  .action((query) => {
    const tools = onexService.searchTools(query);
    if (tools.length === 0) {
      console.log(chalk.red(`No tools found matching '${query}'`));
    } else {
      console.log(chalk.green(`Found ${tools.length} tools matching '${query}':`));
      tools.forEach((tool, index) => {
        console.log(chalk.green(`${index + 1} ${tool.name}`));
      });
    }
  });

program
  .command('install <toolName>')
  .alias('i')
  .description('Install a tool')
  .action(async (toolName) => {
    console.log(chalk.green('Installing ...'));
    const result = await onexService.installTool(toolName);
    
    if (result.success) {
      console.log(chalk.green(result.message));
    } else {
      console.log(chalk.red(result.message));
    }
  });

program
  .command('info <toolName>')
  .description('Get information about a specific tool')
  .action((toolName) => {
    const tool = onexService.getToolByName(toolName);
    
    if (!tool) {
      const suggestions = onexService.searchTools(toolName);
      console.log(chalk.red(`Tool '${toolName}' not found`));
      if (suggestions.length > 0) {
        console.log(chalk.blue('Did you mean:'));
        suggestions.slice(0, 5).forEach(t => {
          console.log(chalk.green(` - ${t.name}`));
        });
      }
      return;
    }

    console.log(chalk.yellow(`\nTool Information:`));
    console.log(chalk.green(`Name: ${tool.name}`));
    console.log(chalk.green(`Package: ${tool.packageName}`));
    console.log(chalk.green(`Category: ${tool.category || 'N/A'}`));
    console.log(chalk.green(`Installer: ${tool.installer}`));
    console.log(chalk.green(`URL: ${tool.url}`));
    console.log(chalk.green(`Dependencies: ${tool.dependencies.length > 0 ? tool.dependencies.join(', ') : 'None'}`));
  });

program
  .command('categories')
  .description('List all tool categories')
  .action(() => {
    const categories = onexService.getAllCategories();
    console.log(chalk.yellow('Available Categories:'));
    categories.forEach((category, index) => {
      console.log(chalk.green(`${index + 1} ${category.displayName} (${category.key})`));
    });
  });

program
  .command('stats')
  .description('Show statistics')
  .action(() => {
    const stats = onexService.getStats();
    const systemInfo = onexService.getSystemInfo();
    
    console.log(chalk.yellow('Onex Statistics:'));
    console.log(chalk.green(`Tools Available: ${stats.toolsCount}`));
    console.log(chalk.green(`Categories: ${stats.categoriesCount}`));
    console.log(chalk.green(`System: ${systemInfo.system}`));
    console.log(chalk.green(`Package Manager: ${systemInfo.packageManager}`));
    console.log(chalk.green(`Root Access: ${systemInfo.hasRoot ? 'Yes' : 'No'}`));
  });

// Default help behavior
if (process.argv.length === 2) {
  console.log(chalk.blue('Usage: onex [command] [options]'));
  console.log(chalk.blue('Type "onex --help" for help or "onex start" for interactive mode'));
}

program.parse();