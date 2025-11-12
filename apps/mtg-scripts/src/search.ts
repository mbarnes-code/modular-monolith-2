#!/usr/bin/env tsx

import { scryfall } from '@jane-monorepo/mtg-scripting-toolkit';
import { createInterface } from 'readline';

interface SearchOptions {
  query?: string;
  format?: string;
  colors?: string;
  commander?: boolean;
  limit?: number;
}

async function searchCards(options: SearchOptions = {}) {
  try {
    let searchQuery = options.query || '';
    
    if (options.format) {
      searchQuery += ` format:${options.format}`;
    }
    
    if (options.colors) {
      searchQuery += ` c:${options.colors}`;
    }
    
    if (options.commander) {
      searchQuery += ' is:commander';
    }
    
    console.log(`Searching for: "${searchQuery}"`);
    
    const results = await scryfall.search(searchQuery);
    
    if (results && results.length > 0) {
      const displayLimit = options.limit || 10;
      const cardsToShow = results.slice(0, displayLimit);
      
      console.log(`\nFound ${results.length} cards. Showing first ${cardsToShow.length}:\n`);
      
      cardsToShow.forEach((card: any, index: number) => {
        console.log(`${index + 1}. ${card.name}`);
        if (card.mana_cost) {
          console.log(`   Mana Cost: ${card.mana_cost}`);
        }
        if (card.type_line) {
          console.log(`   Type: ${card.type_line}`);
        }
        if (card.oracle_text) {
          console.log(`   Text: ${card.oracle_text.substring(0, 100)}${card.oracle_text.length > 100 ? '...' : ''}`);
        }
        console.log(`   Set: ${card.set_name} (${card.set})`);
        console.log('');
      });
    } else {
      console.log('No cards found.');
    }
  } catch (error) {
    console.error('Error searching for cards:', error);
  }
}

async function interactiveMode() {
  const rl = createInterface({
    input: process.stdin,
    output: process.stdout
  });

  const question = (query: string): Promise<string> => {
    return new Promise(resolve => rl.question(query, resolve));
  };

  try {
    console.log('MTG Card Search Tool');
    console.log('==================');
    
    const query = await question('Enter search query: ');
    const format = await question('Format (optional, e.g., "commander", "standard"): ');
    const colors = await question('Colors (optional, e.g., "wr" for white/red): ');
    const isCommander = await question('Commanders only? (y/n): ');
    const limitStr = await question('Limit results (default 10): ');
    
    const options: SearchOptions = {
      query: query.trim() || undefined,
      format: format.trim() || undefined,
      colors: colors.trim() || undefined,
      commander: isCommander.toLowerCase().startsWith('y'),
      limit: limitStr.trim() ? parseInt(limitStr.trim()) : 10
    };

    await searchCards(options);
  } finally {
    rl.close();
  }
}

// Parse command line arguments
const args = process.argv.slice(2);
if (args.length === 0) {
  // Interactive mode
  interactiveMode().catch(console.error);
} else {
  // Command line mode
  const options: SearchOptions = {};
  let i = 0;
  while (i < args.length) {
    switch (args[i]) {
      case '--query':
      case '-q':
        options.query = args[++i];
        break;
      case '--format':
      case '-f':
        options.format = args[++i];
        break;
      case '--colors':
      case '-c':
        options.colors = args[++i];
        break;
      case '--commander':
        options.commander = true;
        break;
      case '--limit':
      case '-l':
        options.limit = parseInt(args[++i]);
        break;
      default:
        if (!options.query) {
          options.query = args[i];
        }
        break;
    }
    i++;
  }
  
  searchCards(options).catch(console.error);
}