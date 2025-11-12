# MTG Scripting Toolkit Library

A comprehensive TypeScript library for Magic: The Gathering data manipulation and analysis.

## Features

- **Scryfall API Integration**: Complete wrapper for the Scryfall API
- **MTG Card Utilities**: Card filtering, sorting, and analysis tools
- **Cube Cobra Integration**: Support for cube management and analytics
- **Logging Utilities**: Structured logging for debugging and analysis
- **Price Tracking**: Card price monitoring and historical data

## Installation

This library is part of the Jane Monorepo workspace. Import it using:

```typescript
import { ScryfallAPI, MTGCard, Logger } from '@jane-monorepo/mtg-scripting-toolkit';
```

## Usage

### Scryfall API

```typescript
import { ScryfallAPI } from '@jane-monorepo/mtg-scripting-toolkit';

const api = new ScryfallAPI();
const cards = await api.search('format:commander');
```

### Card Utilities

```typescript
import { MTGCard } from '@jane-monorepo/mtg-scripting-toolkit';

const card = new MTGCard(cardData);
const isCommander = card.isLegalCommander();
const colors = card.getColorIdentity();
```

### Logging

```typescript
import { Logger } from '@jane-monorepo/mtg-scripting-toolkit';

const logger = new Logger('MTG-Analysis');
logger.info('Starting card analysis...');
```

## API Reference

### Classes

- **ScryfallAPI**: Main interface for Scryfall API interactions
- **MTGCard**: Wrapper class for individual MTG card data
- **Logger**: Structured logging utility
- **CubeCobraAPI**: Interface for Cube Cobra integration

### Types

- **CardData**: Core card data structure
- **SearchOptions**: Options for card searches
- **PriceData**: Price information structure

## Development

This library follows NX best practices and includes:

- TypeScript configuration with relaxed strict mode
- Jest testing setup
- ESLint configuration
- Proper module exports

## Testing

```bash
npx nx test mtg-scripting-toolkit
```

## Building

```bash
npx nx build mtg-scripting-toolkit
```