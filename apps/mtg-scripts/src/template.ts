#!/usr/bin/env tsx

import { scryfall } from '@jane-monorepo/mtg-scripting-toolkit';

/**
 * Template script for MTG analysis
 * This is a starting point for custom MTG data analysis scripts
 */

interface AnalysisOptions {
  outputFile?: string;
  format?: string;
  verbose?: boolean;
}

async function runAnalysis(options: AnalysisOptions = {}) {
  console.log('MTG Analysis Template');
  console.log('====================');
  
  try {
    // Example 1: Search for commanders in specific colors
    console.log('\n1. Searching for Sultai commanders...');
    const sultaiCommanders = await scryfall.search('is:commander c:gub');
    console.log(`Found ${sultaiCommanders?.length || 0} Sultai commanders`);
    
    // Example 2: Fetch a specific card
    console.log('\n2. Fetching a specific card...');
    const card = await scryfall.fetchCard({ name: 'Lightning Bolt' });
    if (card && 'name' in card) {
      console.log(`Card: ${card.name}`);
      console.log(`Mana Cost: ${card.mana_cost || 'N/A'}`);
      console.log(`Type: ${card.type_line}`);
    }
    
    // Example 3: Get card catalogs
    console.log('\n3. Fetching creature types...');
    const creatureTypes = await scryfall.fetchCreatureTypes();
    console.log(`Found ${creatureTypes.length} creature types`);
    if (options.verbose) {
      console.log('First 10 creature types:', creatureTypes.slice(0, 10));
    }
    
    // Example 4: Analyze mana costs (if MTG utilities are available)
    console.log('\n4. Analysis complete!');
    
    if (options.outputFile) {
      // Here you could write results to a file
      console.log(`Results would be written to: ${options.outputFile}`);
    }
    
  } catch (error) {
    console.error('Error during analysis:', error);
  }
}

// Command line argument parsing
const args = process.argv.slice(2);
const options: AnalysisOptions = {};

let i = 0;
while (i < args.length) {
  switch (args[i]) {
    case '--output':
    case '-o':
      options.outputFile = args[++i];
      break;
    case '--format':
    case '-f':
      options.format = args[++i];
      break;
    case '--verbose':
    case '-v':
      options.verbose = true;
      break;
    case '--help':
    case '-h':
      console.log(`
MTG Analysis Template

Usage: npx nx template mtg-scripts [options]

Options:
  -o, --output <file>    Output file for results
  -f, --format <format>  MTG format to analyze
  -v, --verbose          Verbose output
  -h, --help            Show this help message

Examples:
  npx nx template mtg-scripts
  npx nx template mtg-scripts --format commander --verbose
  npx nx template mtg-scripts --output results.json
      `);
      process.exit(0);
      break;
    default:
      console.warn(`Unknown option: ${args[i]}`);
      break;
  }
  i++;
}

// Run the analysis
if (require.main === module) {
  runAnalysis(options).catch(console.error);
}

export { runAnalysis };
