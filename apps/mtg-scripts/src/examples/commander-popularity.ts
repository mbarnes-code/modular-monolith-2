#!/usr/bin/env tsx

/**
 * Example: Commander Popularity Analysis
 * 
 * This script analyzes the most popular commanders in each color combination
 * and generates a report with statistics and recommendations.
 */

import { scryfall } from '@jane-monorepo/mtg-scripting-toolkit';

interface CommanderStats {
  name: string;
  colorIdentity: string[];
  deckCount?: number;
  rank?: number;
  saltScore?: number;
}

const colorCombinations = [
  { name: 'Mono-White', query: 'is:commander c:w' },
  { name: 'Mono-Blue', query: 'is:commander c:u' },
  { name: 'Mono-Black', query: 'is:commander c:b' },
  { name: 'Mono-Red', query: 'is:commander c:r' },
  { name: 'Mono-Green', query: 'is:commander c:g' },
  { name: 'Azorius (WU)', query: 'is:commander c:wu' },
  { name: 'Orzhov (WB)', query: 'is:commander c:wb' },
  { name: 'Boros (WR)', query: 'is:commander c:wr' },
  { name: 'Selesnya (WG)', query: 'is:commander c:wg' },
  { name: 'Dimir (UB)', query: 'is:commander c:ub' },
  { name: 'Izzet (UR)', query: 'is:commander c:ur' },
  { name: 'Simic (UG)', query: 'is:commander c:ug' },
  { name: 'Rakdos (BR)', query: 'is:commander c:br' },
  { name: 'Golgari (BG)', query: 'is:commander c:bg' },
  { name: 'Gruul (RG)', query: 'is:commander c:rg' },
  { name: 'Esper (WUB)', query: 'is:commander c:wub' },
  { name: 'Grixis (UBR)', query: 'is:commander c:ubr' },
  { name: 'Jund (BRG)', query: 'is:commander c:brg' },
  { name: 'Naya (RGW)', query: 'is:commander c:rgw' },
  { name: 'Bant (GWU)', query: 'is:commander c:gwu' },
  { name: 'Mardu (RWB)', query: 'is:commander c:rwb' },
  { name: 'Temur (GUR)', query: 'is:commander c:gur' },
  { name: 'Abzan (WBG)', query: 'is:commander c:wbg' },
  { name: 'Jeskai (URW)', query: 'is:commander c:urw' },
  { name: 'Sultai (BUG)', query: 'is:commander c:bug' },
  { name: 'WUBRG', query: 'is:commander c:wubrg' }
];

async function analyzeCommanderPopularity() {
  console.log('Commander Popularity Analysis');
  console.log('============================\n');

  const results: { [key: string]: CommanderStats[] } = {};

  for (const combo of colorCombinations) {
    console.log(`Analyzing ${combo.name}...`);
    
    try {
      const searchResult = await scryfall.search(`${combo.query} is:commander`);
      
      if (searchResult && searchResult.length > 0) {
        const commanders: CommanderStats[] = searchResult
          .slice(0, 10) // Top 10 for each color combination
          .map((card: any) => ({
            name: card.name,
            colorIdentity: card.color_identity || [],
            // In a real analysis, you'd get deck count from EDHREC or similar
            deckCount: Math.floor(Math.random() * 10000), // Placeholder
            rank: 0, // Will be set later
            saltScore: Math.random() * 4 // Placeholder
          }));

        // Sort by deck count (simulated)
        commanders.sort((a, b) => (b.deckCount || 0) - (a.deckCount || 0));
        
        // Assign ranks
        commanders.forEach((commander, index) => {
          commander.rank = index + 1;
        });

        results[combo.name] = commanders;
        console.log(`  Found ${commanders.length} popular commanders`);
      }
    } catch (error) {
      console.error(`  Error analyzing ${combo.name}:`, error);
      results[combo.name] = [];
    }
  }

  // Generate report
  console.log('\n\nCommander Popularity Report');
  console.log('===========================\n');

  for (const [colorCombo, commanders] of Object.entries(results)) {
    if (commanders.length > 0) {
      console.log(`\n${colorCombo}:`);
      console.log('─'.repeat(colorCombo.length + 1));
      
      commanders.slice(0, 5).forEach((commander) => {
        console.log(`  ${commander.rank}. ${commander.name}`);
        console.log(`     Decks: ${commander.deckCount?.toLocaleString() || 'N/A'}`);
        console.log(`     Salt Score: ${commander.saltScore?.toFixed(2) || 'N/A'}`);
      });
    }
  }

  // Summary statistics
  const totalCommanders = Object.values(results).reduce((sum, commanders) => sum + commanders.length, 0);
  const mostPopularOverall = Object.values(results)
    .flat()
    .sort((a, b) => (b.deckCount || 0) - (a.deckCount || 0))[0];

  console.log('\n\nSummary Statistics');
  console.log('==================');
  console.log(`Total commanders analyzed: ${totalCommanders}`);
  console.log(`Most popular overall: ${mostPopularOverall?.name || 'N/A'}`);
  console.log(`   Decks: ${mostPopularOverall?.deckCount?.toLocaleString() || 'N/A'}`);

  return results;
}

if (require.main === module) {
  analyzeCommanderPopularity().catch(console.error);
}