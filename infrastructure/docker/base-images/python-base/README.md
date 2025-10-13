# Python Base Image

Multi-stage Docker image optimized for Python 3.12 applications in the Jane monorepo.

## Features

- **Base Image**: Python 3.12-slim
- **Multi-stage Build**: Separates build and runtime dependencies
- **Security**: Non-root user execution
- **Optimization**: Minimal image size with no unnecessary packages
- **Health Checks**: Built-in health check support

## Environment Variables

- `PYTHONUNBUFFERED=1`: Disable output buffering
- `PYTHONDONTWRITEBYTECODE=1`: Prevent .pyc files
- `PIP_NO_CACHE_DIR=1`: Disable pip cache
- `PIP_DISABLE_PIP_VERSION_CHECK=1`: Skip version checks

## Usage

### Build

```bash
docker build -t jane-python-base:3.12 infrastructure/docker/base-images/python-base/
```

### Use in Application Dockerfile

```dockerfile
FROM jane-python-base:3.12

COPY . .

CMD ["python", "app.py"]
```

## Stages

1. **base**: Base image with system dependencies
2. **builder**: Install Python packages
3. **runtime**: Minimal runtime with only necessary files

## System Dependencies

Pre-installed:
- gcc
- g++
- make
- libpq-dev (PostgreSQL client library)

## Security

- Runs as non-root user `appuser` (UID 1000)
- Minimal attack surface with slim base image
- No unnecessary packages or files

## Size Optimization

- Uses slim variant of Python
- Multi-stage build removes build dependencies
- No pip cache or .pyc files
