#!/bin/bash
# Commander Spellbook Development Scripts

set -e

case "$1" in
  "serve-frontend")
    echo "Starting Commander Spellbook Frontend on port 3001..."
    cd apps/commander-spellbook-site
    npx next dev -p 3001
    ;;
  "serve-backend")
    echo "Starting Commander Spellbook Backend on port 8081..."
    cd apps/commander-spellbook-backend/backend
    python manage.py runserver 0.0.0.0:8081
    ;;
  "build-frontend")
    echo "Building Commander Spellbook Frontend..."
    cd apps/commander-spellbook-site
    npx next build
    ;;
  "test-backend")
    echo "Running Commander Spellbook Backend tests..."
    cd apps/commander-spellbook-backend
    python -m pytest
    ;;
  "migrate")
    echo "Running database migrations..."
    cd apps/commander-spellbook-backend/backend
    python manage.py migrate
    ;;
  *)
    echo "Usage: $0 {serve-frontend|serve-backend|build-frontend|test-backend|migrate}"
    echo ""
    echo "Commands:"
    echo "  serve-frontend  - Start Next.js dev server on port 3001"
    echo "  serve-backend   - Start Django dev server on port 8081" 
    echo "  build-frontend  - Build Next.js for production"
    echo "  test-backend    - Run Python tests"
    echo "  migrate         - Run database migrations"
    exit 1
    ;;
esac