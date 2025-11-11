# Ghostwriter Service Dockerfile - NX Optimized
FROM python:3.11-slim-bookworm as base

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Create app user
RUN groupadd --gid 1000 app && \
    useradd --uid 1000 --gid app --shell /bin/bash --create-home app

# Set work directory
WORKDIR /app

# Install Python dependencies
COPY requirements/ requirements/
RUN pip install -r requirements/production.txt

# Development stage
FROM base as development

# Install development dependencies
RUN pip install -r requirements/local.txt

# Copy project files
COPY . .
RUN chown -R app:app /app

USER app

# Expose port
EXPOSE 8000

# Default command for development
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

# Production stage
FROM base as production

# Copy only necessary files
COPY --chown=app:app src/ src/
COPY --chown=app:app manage.py .
COPY --chown=app:app pyproject.toml .
COPY --chown=app:app compose/production/django/entrypoint /entrypoint
COPY --chown=app:app compose/production/django/start /start

# Make scripts executable
RUN chmod +x /entrypoint /start

USER app

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose port
EXPOSE 8000

# Use entrypoint and start scripts
ENTRYPOINT ["/entrypoint"]
CMD ["/start"]