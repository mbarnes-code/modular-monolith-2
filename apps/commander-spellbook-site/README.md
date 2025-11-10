# Commander Spellbook Website - NX Integration

This directory contains the Commander Spellbook frontend integrated into the NX monorepo.

## About Commander's Spellbook

Check out the [about page](https://commanderspellbook.com/about/) for details about the website.

## NX Integration

### Project Configuration
- **Name**: commander-spellbook-site
- **Type**: Next.js Frontend Application
- **Port**: 3001  
- **Tags**: `scope:mtg`, `type:frontend`, `framework:nextjs`

### Available NX Targets

```bash
# Start development server
npx nx serve commander-spellbook-site

# Build for production
npx nx build commander-spellbook-site

# Export static files
npx nx export commander-spellbook-site

# Run tests (when configured)
npx nx test commander-spellbook-site

# Lint code
npx nx lint commander-spellbook-site

# Type check
npx nx type-check commander-spellbook-site

# Run Cypress tests
npx nx cypress:run commander-spellbook-site
npx nx cypress:open commander-spellbook-site
```

### Manual Development

```bash
cd apps/commander-spellbook-site
npm run dev  # Will use workspace dependencies
```

## Development

See [the development docs](https://spacecowmedia.github.io/commander-spellbook-site/) for information on how to contribute to the site.

## Dependencies

All dependencies are managed at the workspace level in the root `package.json`. The Commander Spellbook specific dependencies include:

- `@space-cow-media/spellbook-client` - Generated API client
- `scryfall-client` - Scryfall API client for MTG data
- `react-select`, `react-tooltip`, etc. - UI components
- Cypress for E2E testing
- Tailwind CSS for styling
