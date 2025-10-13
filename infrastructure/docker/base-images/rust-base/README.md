# Rust Base Image

Multi-stage Docker image optimized for Rust 1.70+ applications in the Jane monorepo.

## Features

- **Base Image**: Rust 1.70-slim
- **cargo-chef**: Optimized dependency caching
- **Multi-stage Build**: Separates build and runtime
- **Security**: Non-root user execution
- **Optimization**: Static binary with minimal runtime

## Environment Variables

- `CARGO_NET_GIT_FETCH_WITH_CLI=true`: Use git CLI for fetching
- `RUSTFLAGS="-C target-cpu=native"`: CPU-specific optimizations

## Usage

### Build

```bash
docker build -t jane-rust-base:1.70 infrastructure/docker/base-images/rust-base/
```

### Use in Application Dockerfile

```dockerfile
FROM jane-rust-base:1.70

COPY . .

EXPOSE 8080

CMD ["./app"]
```

## Stages

1. **base**: Rust base with build dependencies
2. **planner**: cargo-chef dependency planner
3. **builder**: Build dependencies and application
4. **runtime**: Minimal Debian runtime with binary

## Build Dependencies

Pre-installed in build stage:
- pkg-config
- libssl-dev

## Runtime Dependencies

Minimal runtime includes:
- ca-certificates
- libssl3

## Security

- Runs as non-root user `appuser` (UID 1000)
- Minimal attack surface with slim runtime
- No Rust toolchain in runtime image

## Size Optimization

- Uses slim Rust variant for building
- Uses Debian slim for runtime
- cargo-chef for efficient dependency caching
- Only compiled binary in runtime image

## cargo-chef

Uses cargo-chef for optimal Docker layer caching:
1. Prepare recipe from Cargo files
2. Cook (build) dependencies
3. Build application

This ensures dependencies are only rebuilt when Cargo files change.

## Health Check

Default health check expects:
- HTTP endpoint at `/health`
- Port 8080

Requires `curl` in runtime image or modify for your needs.
