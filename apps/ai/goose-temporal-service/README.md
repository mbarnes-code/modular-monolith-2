# Goose Temporal Service

Go-based temporal workflow service for the Goose AI agent ecosystem.

## Project Structure

This service handles temporal workflows and long-running processes for Goose.

## Development

```bash
# Build the service
npx nx build goose-temporal-service

# Run in development mode
npx nx serve goose-temporal-service

# Run tests
npx nx test goose-temporal-service

# Lint and format code
npx nx lint goose-temporal-service

# Update Go dependencies
npx nx tidy goose-temporal-service

# Build Docker image
npx nx docker:build goose-temporal-service
```

## Dependencies

This service works in conjunction with `goose-service` to provide temporal workflow capabilities.
