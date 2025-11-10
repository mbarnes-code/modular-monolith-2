# Multi-stage build for HexStrike Service
FROM python:3.12-slim as base

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app/src

# Create app user
RUN useradd --create-home --shell /bin/bash app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Development stage
FROM base as development

# Install development dependencies
COPY pyproject.toml .
RUN pip install -e ".[dev]"

# Copy source code
COPY src/ src/
COPY tests/ tests/
COPY .env.example .env

# Change ownership to app user
RUN chown -R app:app /app
USER app

# Expose port
EXPOSE 8000

# Default command for development
CMD ["python", "-m", "hexstrike.api.main"]

# Production stage
FROM base as production

# Copy only necessary files
COPY src/ src/
COPY pyproject.toml .
COPY .env.example .env

# Change ownership to app user
RUN chown -R app:app /app
USER app

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Expose port
EXPOSE 8000

# Production command
CMD ["python", "-m", "hexstrike.api.main"]