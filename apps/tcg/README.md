# TCG (Trading Card Game) Domain Services

This directory contains all Trading Card Game related services, primarily focused on Magic: The Gathering.

## Performance Target

- **Response Time**: <3s (Game analysis complexity)
- **Integration Pattern**: Service adapter with business logic preservation

## Services

### Magic: The Gathering Services

- **commander-spellbook-backend** - Backend API for Commander format combo database
- **commander-spellbook-site** - Frontend website for Commander Spellbook
- **mtg-commander-map-service** - Commander format analysis and mapping
- **mtg-scripts** - Core MTG scripting toolkit and utilities
- **mtg-scripts-e2e** - End-to-end tests for MTG scripts
- **mtg-service** - General MTG service aggregator

## Architecture Patterns

### Service Categories

#### Database & Analysis Services

- **Commander Spellbook**: Comprehensive combo database for EDH/Commander format
- **Commander Map**: Strategic analysis and deck building tools
- **MTG Scripts**: Automation and utility scripts for various MTG tasks

#### Content & Presentation

- **Spellbook Site**: User-friendly interface for combo searching and discovery
- **Service Aggregator**: Unified API for MTG-related queries

### Integration Patterns

#### Data Flow

```bash
mtg-ui → jane-orchestrator → mtg-service → [specific MTG tools]
                           ↓
                       mtg-llm-server (AI analysis)
```

#### Card Data Management

- Card database synchronization
- Rule text analysis and processing
- Combo detection and validation
- Deck analysis and optimization

## Development

### Running Services

```bash
# Individual services
npx nx serve tcg/commander-spellbook-site
npx nx serve tcg/commander-spellbook-backend
npx nx serve tcg/mtg-service

# All TCG services
npx nx run-many --target=serve --projects=tag:domain:tcg

# Testing
npx nx run-many --target=test --projects=tag:domain:tcg

# Building
npx nx run-many --target=build --projects=tag:domain:tcg
```

### Project Tags

All TCG services should include:

- `domain:tcg` - TCG domain identifier
- `scope:backend` or `scope:frontend` - Service type
- `type:service` or `type:application` - Project type

### Performance Monitoring

Monitor game analysis and combo detection performance:

```bash
# Performance validation
python tests/performance/tcg-domain-validation.py
```

## Data Management

### Card Database

- Comprehensive Magic card database
- Regular updates from official sources
- Card image and metadata management
- Rule text processing and normalization

### Combo Database

- Validated combo collections
- Community contributions and curation
- Performance metrics and statistics
- Integration with deck building tools

## Service Dependencies

### External Dependencies

- Scryfall API for card data
- EDHREC for community statistics
- MTG JSON for structured data
- Card image repositories

### Internal Dependencies

- `jane-orchestrator` - Central routing
- `mtg-llm-server` - AI-powered analysis
- `libs/shared` - Common utilities
- `libs/mtg-scripting-toolkit` - Shared MTG utilities

## Game Rule Integration

### Rule Engine

- Comprehensive Magic rules implementation
- Interaction resolution and timing
- State-based effects processing
- Complex combo validation

### Format Support

- **Commander/EDH**: Primary focus with specialized tools
- **Standard**: Current rotation support
- **Modern**: Extended format analysis
- **Legacy**: Historical card interactions

## Community Features

### User Contributions

- Community combo submissions
- Deck sharing and analysis
- Rating and review systems
- Discussion and feedback tools

### Curation

- Expert validation of combinations
- Quality control and verification
- Educational content and guides
- Tournament data integration

## Documentation

Each TCG service maintains:

- Game rule documentation
- API specifications for card data
- Combo validation procedures
- Integration guides for new formats

## Contributing

When adding new TCG services:

1. Maintain rule accuracy and completeness
2. Implement proper card data validation  
3. Add comprehensive game state tests
4. Document rule interactions clearly
5. Include community feedback mechanisms