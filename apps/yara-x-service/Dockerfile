# Multi-stage Dockerfile for YARA-X Service
FROM rust:1.75 AS builder

# Install build dependencies
RUN apt-get update && apt-get install -y \
    pkg-config \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy Cargo files
COPY Cargo.toml Cargo.lock ./
COPY cli/Cargo.toml ./cli/
COPY lib/Cargo.toml ./lib/
COPY capi/Cargo.toml ./capi/
COPY fmt/Cargo.toml ./fmt/
COPY macros/Cargo.toml ./macros/
COPY parser/Cargo.toml ./parser/
COPY proto/Cargo.toml ./proto/
COPY proto-json/Cargo.toml ./proto-json/
COPY proto-yaml/Cargo.toml ./proto-yaml/
COPY py/Cargo.toml ./py/

# Copy source files
COPY . .

# Build the CLI binary
RUN cargo build --release --bin yr

# Runtime stage
FROM debian:bookworm-slim AS runtime

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN useradd -r -s /bin/false yara-x

# Copy binary from builder stage
COPY --from=builder /app/target/release/yr /usr/local/bin/yr

# Set binary permissions
RUN chmod +x /usr/local/bin/yr

# Switch to non-root user
USER yara-x

# Set entrypoint
ENTRYPOINT ["/usr/local/bin/yr"]
CMD ["--help"]

# Metadata
LABEL maintainer="modular-monolith-2"
LABEL description="YARA-X Pattern Matching Service"
LABEL version="1.0.0"