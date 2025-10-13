#!/bin/bash
# Quick setup script for modular-monolith-2 codespace
# This is a minimal version - use setup-codespace.sh for full setup

set -e

echo "🚀 Quick Codespace Setup Starting..."

# Update system
echo "📦 Updating system packages..."
sudo apt-get update -qq && sudo apt-get upgrade -y -qq

# Install UV
echo "🐍 Installing UV..."
curl -LsSf https://astral.sh/uv/install.sh | sh
export PATH="$HOME/.cargo/bin:$PATH"

# Install specify-cli
echo "🔧 Installing specify-cli..."
uv tool install specify-cli --from git+https://github.com/github/spec-kit.git
export PATH="$HOME/.local/bin:$PATH"

# Install project dependencies
echo "📋 Installing project dependencies..."
make install

# Upgrade pip
echo "⬆️ Upgrading pip..."
python -m pip install --upgrade pip --quiet

echo "✅ Quick setup complete!"
echo ""
echo "Available commands:"
echo "  make build                    # Build all projects"
echo "  npx nx serve jane-ui         # Start UI (port 3000)"
echo "  npx nx serve jane-orchestrator # Start API (port 8000)"
echo ""
echo "For full setup with verification, run: ./setup-codespace.sh"