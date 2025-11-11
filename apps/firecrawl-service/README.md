# Firecrawl Service

A high-performance web scraping and crawling service built with Express.js and integrated into the NX monorepo architecture.

## Overview

The Firecrawl Service provides powerful web scraping, crawling, and data extraction capabilities. It's designed to handle large-scale operations with features like:

- **Web Scraping**: Extract clean markdown and structured data from web pages
- **Website Crawling**: Crawl entire websites with intelligent link discovery
- **Data Extraction**: AI-powered extraction of structured data
- **Search Integration**: Web search with content scraping capabilities
- **Rate Limiting**: Built-in rate limiting and anti-bot protection
- **Queue Management**: Background job processing with Redis/BullMQ

## Architecture

This service follows NX monorepo best practices with a modular architecture:

```
apps/firecrawl-service/
├── src/
│   ├── app.ts                 # Express app configuration
│   ├── main.ts               # Application entry point
│   ├── environments/         # Environment configurations
│   ├── controllers/          # API route handlers
│   ├── routes/              # API route definitions
│   ├── services/            # Business logic services
│   └── scraper/             # Web scraping engines
├── libs/
│   ├── firecrawl-core/      # Shared business logic
│   ├── firecrawl-types/     # TypeScript type definitions
│   └── firecrawl-ui/        # React UI components
```

## Dependencies

- **@firecrawl/core**: Core business logic and utilities
- **@firecrawl/types**: Shared TypeScript definitions
- **@firecrawl/ui**: React UI components for admin interfaces

## Development

### Prerequisites

- Node.js 18+
- Redis (for job queuing)
- PostgreSQL (for data persistence)

### Environment Variables

Create a `.env` file with the required configuration:

```bash
# Server Configuration
PORT=3002
HOST=0.0.0.0

# Database
SUPABASE_URL=your_supabase_url
SUPABASE_SERVICE_TOKEN=your_supabase_token

# Redis
REDIS_URL=redis://localhost:6379

# Authentication
AUTH_SECRET=your_auth_secret

# AI APIs
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key

# Monitoring
SENTRY_DSN=your_sentry_dsn

# Feature Flags
ENABLE_BULL_BOARD=true
ENABLE_METRICS=true
ENABLE_DEBUG_LOGGING=true
```

### Running the Service

```bash
# Development mode
npx nx serve firecrawl-service

# Production build
npx nx build firecrawl-service

# Run tests
npx nx test firecrawl-service

# Lint code
npx nx lint firecrawl-service
```

### Docker

```bash
# Build Docker image
npx nx docker-build firecrawl-service

# Run with Docker
docker run -p 3002:3002 firecrawl-service
```

## API Endpoints

### Core Scraping

- `POST /v2/scrape` - Scrape a single URL
- `POST /v2/crawl` - Crawl an entire website
- `POST /v2/search` - Search the web and scrape results
- `POST /v2/map` - Generate a sitemap of URLs
- `POST /v2/extract` - Extract structured data with AI

### Management

- `GET /health` - Health check endpoint
- `GET /v1/crawl/:jobId` - Check crawl job status
- `DELETE /v1/crawl/:jobId` - Cancel a crawl job

### Admin (if Bull Board enabled)

- `GET /admin/queues` - Queue management dashboard

## Configuration

The service supports multiple environments:

- **Development**: Full debugging, Bull Board enabled
- **Production**: Optimized performance, reduced logging
- **Test**: Isolated testing environment

Environment-specific configuration is handled through the `environments/` directory.

## Performance

- **Concurrent Processing**: Multi-threaded scraping with worker pools
- **Intelligent Caching**: Redis-based caching for improved response times
- **Rate Limiting**: Configurable rate limits to respect target websites
- **Resource Management**: Memory and CPU optimization for large-scale operations

## Monitoring

- **Health Checks**: Built-in health check endpoint
- **Metrics**: Performance and usage metrics collection
- **Error Tracking**: Sentry integration for error monitoring
- **Logging**: Structured logging with Winston

## Contributing

This service follows the NX monorepo conventions:

1. **Shared Code**: Place reusable utilities in `libs/firecrawl-core`
2. **Types**: Define shared types in `libs/firecrawl-types`
3. **UI Components**: Add React components to `libs/firecrawl-ui`
4. **Testing**: Write comprehensive tests for all new features
5. **Documentation**: Update this README and add JSDoc comments

## License

This project is part of the Jane Mental Prosthetic Platform and follows the project's overall licensing terms.