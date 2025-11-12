# APIScout Service Dockerfile
FROM python:3.11-slim

LABEL maintainer="APIScout NX Service" \
      description="Windows API usage recovery and similarity assessment service" \
      version="2.0.2"

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first for better Docker layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application
COPY . .

# Install the package in development mode
RUN pip install -e .

# Create non-root user for security
RUN useradd --create-home --shell /bin/bash apiscout
RUN chown -R apiscout:apiscout /app
USER apiscout

# Expose port for potential web interface
EXPOSE 8080

# Default command
CMD ["python", "scout.py", "--help"]