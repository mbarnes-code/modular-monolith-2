# MTG Scripting Toolkit - NX Best Practices Implementation

## Overview

The MTG Scripting Toolkit has been reorganized following NX best practices, with a clear separation between the core library utilities and the applications that use them.

## Project Structure

### Library (`libs/mtg-scripting-toolkit/`)
- **Purpose**: Core MTG data manipulation and API utilities
- **Type**: Buildable library
- **Dependencies**: Independent library with minimal external dependencies
- **Exports**: Scryfall API, MTG utilities, card analysis tools, logging utilities

### Application (`apps/mtg-scripts/`)
- **Purpose**: Command-line scripts and tools that use the MTG library
- **Type**: Node.js application with multiple entry points
- **Dependencies**: Uses `@jane-monorepo/mtg-scripting-toolkit` library
- **Scripts**: Search, template analysis, commander popularity analysis

## Usage

### Building the Library
```bash
npx nx build mtg-scripting-toolkit
```

### Building the Scripts
```bash
npx nx build mtg-scripts
```

### Running Scripts

#### Search for Cards
```bash
npx nx search mtg-scripts -- --query "Lightning Bolt"
npx nx search mtg-scripts -- --query "is:commander" --colors "wr" --limit 5
```

#### Run Template Analysis
```bash
npx nx template mtg-scripts
npx nx template mtg-scripts -- --verbose
```

#### Interactive Search (Command Line Arguments)
```bash
# Search for specific cards
node dist/mtg-scripts/search.js --query "Counterspell" --limit 3

# Search for commanders
node dist/mtg-scripts/search.js --commander --colors "gub"

# Interactive mode (no arguments)
node dist/mtg-scripts/search.js
```

## Library API

### Importing the Library
```typescript
import { scryfall, mtg, cubeCobra, moxfield, log } from '@jane-monorepo/mtg-scripting-toolkit';
```

### Core Modules

#### Scryfall API
- `scryfall.search(query)` - Search for cards
- `scryfall.fetchCard({ name })` - Get specific card
- `scryfall.fetchCreatureTypes()` - Get creature type catalog
- `scryfall.fetchSet(setCode)` - Get set information

#### MTG Utilities
- Card analysis and filtering utilities
- Color identity management
- Format legality checking

#### Cube Cobra Integration
- Cube management and analytics
- Deck import/export functionality

#### Moxfield Integration  
- Deck and collection management
- Price tracking and analysis

## Examples

### Custom Analysis Script
```typescript
#!/usr/bin/env tsx

import { scryfall } from '@jane-monorepo/mtg-scripting-toolkit';

async function analyzeCommanders() {
  const commanders = await scryfall.search('is:commander c:r');
  console.log(`Found ${commanders.length} red commanders`);
  
  commanders.slice(0, 10).forEach((card, index) => {
    console.log(`${index + 1}. ${card.name} - ${card.mana_cost}`);
  });
}

analyzeCommanders();
```

### Interactive Search
```typescript
#!/usr/bin/env tsx

import { createInterface } from 'readline';
import { scryfall } from '@jane-monorepo/mtg-scripting-toolkit';

const rl = createInterface({
  input: process.stdin,
  output: process.stdout
});

rl.question('Enter search query: ', async (query) => {
  const results = await scryfall.search(query);
  console.log(`Found ${results.length} cards`);
  rl.close();
});
```

## Architecture Benefits

### 1. Separation of Concerns
- **Library**: Pure utilities and API wrappers
- **Applications**: User-facing tools and scripts
- **Clear boundaries**: Library is framework-agnostic, applications handle UI/CLI

### 2. Reusability
- Library can be used by other applications in the monorepo
- Applications can focus on specific use cases
- Easy to create new tools without duplicating API logic

### 3. Testing and Maintenance
- Library tests focus on core functionality
- Application tests focus on user workflows
- Independent versioning and deployment possible

### 4. Type Safety
- Strong TypeScript support throughout
- Proper module exports with type definitions
- Clear API contracts between library and applications

## Development

### Adding New Features

#### To the Library
1. Add utilities to `libs/mtg-scripting-toolkit/src/lib/`
2. Export from `libs/mtg-scripting-toolkit/src/index.ts`
3. Update types and documentation
4. Add unit tests

#### To Applications
1. Add scripts to `apps/mtg-scripts/src/`
2. Import library utilities using `@jane-monorepo/mtg-scripting-toolkit`
3. Add NX targets in `project.json` if needed
4. Update build configuration for new entry points

### Testing
```bash
# Test the library
npx nx test mtg-scripting-toolkit

# Test the applications  
npx nx test mtg-scripts

# Run all MTG-related tests
npx nx run-many --target=test --projects=mtg-*
```

### Linting and Formatting
```bash
# Lint the library
npx nx lint mtg-scripting-toolkit

# Lint the applications
npx nx lint mtg-scripts

# Format all code
npx nx format:write --projects=mtg-*
```

## Migration Notes

The original `features/mtg-scripting-toolkit/` has been successfully migrated to this new structure:

- ✅ All utilities moved to `libs/mtg-scripting-toolkit/`
- ✅ Scripts reorganized in `apps/mtg-scripts/`
- ✅ Proper NX library and application structure
- ✅ Working build and execution
- ✅ TypeScript configuration optimized
- ✅ Import paths updated to use workspace aliases
- ✅ All functionality verified and tested

## Future Enhancements

- Add more analysis scripts (meta analysis, price tracking, etc.)
- Integrate with additional MTG data sources
- Add web UI application using the same library
- Implement caching for better performance
- Add comprehensive test suite for all features