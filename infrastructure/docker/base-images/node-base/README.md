# Node.js Base Image

Multi-stage Docker image optimized for Node.js 20 applications in the Jane monorepo.

## Features

- **Base Image**: Node.js 20 Alpine
- **Multi-stage Build**: Separates dependencies, build, and runtime
- **Security**: Non-root user execution
- **Optimization**: Minimal image size with Alpine Linux
- **Health Checks**: Built-in HTTP health check

## Environment Variables

- `NODE_ENV=production`: Production mode
- `NPM_CONFIG_LOGLEVEL=warn`: Reduce npm verbosity
- `NPM_CONFIG_UPDATE_NOTIFIER=false`: Disable update notifications

## Usage

### Build

```bash
docker build -t jane-node-base:20 infrastructure/docker/base-images/node-base/
```

### Use in Application Dockerfile

```dockerfile
FROM jane-node-base:20

COPY . .

EXPOSE 3000

CMD ["npm", "start"]
```

## Stages

1. **base**: Alpine base with build tools
2. **dependencies**: Install production dependencies
3. **builder**: Build application (TypeScript, Next.js, etc.)
4. **runtime**: Minimal runtime with built app and prod dependencies

## Build Dependencies

Pre-installed in build stages:
- python3
- make
- g++

## Security

- Runs as non-root user `appuser` (UID 1000)
- Minimal attack surface with Alpine base
- No unnecessary packages or files

## Size Optimization

- Uses Alpine variant of Node.js
- Multi-stage build removes build dependencies
- npm cache cleaned after install
- Only production dependencies in runtime

## Health Check

Default health check expects:
- HTTP endpoint at `/api/health`
- Port 3000
- Returns 200 OK status

Customize for your application needs.
