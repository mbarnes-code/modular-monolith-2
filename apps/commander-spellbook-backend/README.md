# Commander Spellbook - NX Integration

This directory contains the Commander Spellbook backend integrated into the NX monorepo.

## Original Project

[Commander Spellbook](https://commanderspellbook.com/) is a combo database, wiki and engine for [Magic: The Gathering](https://magic.wizards.com/en).
It's designed to be a one-stop shop for all the information you might want about a combo, whether it's a deck you're
building or one you're playing against.

This is an Open Source project, and we welcome contributions from the community.

## NX Integration

### Project Configuration
- **Name**: commander-spellbook-backend
- **Type**: Django Backend Application  
- **Port**: 8081
- **Tags**: `scope:mtg`, `type:backend`, `framework:django`

### Available NX Targets

```bash
# Start development server
npx nx serve commander-spellbook-backend

# Run migrations
npx nx migrate commander-spellbook-backend

# Create migrations  
npx nx makemigrations commander-spellbook-backend

# Run tests
npx nx test commander-spellbook-backend

# Lint code
npx nx lint commander-spellbook-backend

# Collect static files
npx nx collectstatic commander-spellbook-backend
```

### Manual Development

```bash
cd apps/commander-spellbook-backend/backend
python manage.py migrate
python manage.py runserver 0.0.0.0:8081
```

## Architecture

Commander Spellbook consists of three main components:

- A [PostgreSQL](https://www.postgresql.org/) database containing all the combo data
- A [Django](https://www.djangoproject.com/) backend that exposes the data via a REST API
- A [Next.js](https://nextjs.org/) frontend (located at `apps/commander-spellbook-site`) that consumes the API
  - A TS/JS generated client can be found on [npm](https://www.npmjs.com/package/@space-cow-media/spellbook-client)

## Contributing

Anyone is welcome to contribute to Commander Spellbook. You can contribute in a number of ways:

* On the [backend](/backend/), by opening a pull request with your changes
* On the [frontend](https://github.com/SpaceCowMedia/commander-spellbook-site), by opening a pull request with your changes
* By [submitting new combos](https://commanderspellbook.com/submit-a-combo/)

### Contribution Guidelines

You can find the contribution guidelines for the backend [here](CONTRIBUTING.md).

### Documentation

You can read some Markdown documentation [here](https://spacecowmedia.github.io/commander-spellbook-backend/).
