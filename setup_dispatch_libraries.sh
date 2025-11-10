#!/usr/bin/env bash
"""
Setup script for Dispatch Service - Install shared libraries in development mode
"""

set -e

# Get the workspace root
WORKSPACE_ROOT="/workspaces/modular-monolith-2"
cd "$WORKSPACE_ROOT"

echo "🚀 Setting up Dispatch Service with shared libraries..."

# Install dispatch-core library in development mode
echo "📦 Installing dispatch-core library..."
cd "$WORKSPACE_ROOT/libs/dispatch-core"
pip install -e .

# Install dispatch-database library in development mode  
echo "📦 Installing dispatch-database library..."
cd "$WORKSPACE_ROOT/libs/dispatch-database"
pip install -e .

# Install dispatch-service dependencies
echo "📦 Installing dispatch-service dependencies..."
cd "$WORKSPACE_ROOT/apps/dispatch-service"
pip install -e .

echo "✅ Setup complete!"
echo ""
echo "📋 Next Steps:"
echo "1. Test imports: python -c 'import dispatch_core, dispatch_database; print(\"✅ Libraries imported successfully\")'"
echo "2. Run service: npx nx serve dispatch-service"
echo "3. Check health: curl http://localhost:8013/health"
echo ""
echo "🛠️  Development Commands:"
echo "  npx nx test dispatch-service     # Run tests"
echo "  npx nx lint dispatch-service     # Run linting" 
echo "  npx nx format dispatch-service   # Format code"
echo ""