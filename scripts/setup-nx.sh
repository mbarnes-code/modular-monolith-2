#!/bin/bash
# Nx Development Environment Setup Script
# This script configures optimal settings for large-scale Nx workspaces

echo "🚀 Setting up Nx Development Environment..."

# Start Nx Daemon
echo "📡 Starting Nx Daemon..."
npx nx daemon --start

# Verify daemon is running
if npx nx daemon | grep -q "currently running"; then
    echo "✅ Nx Daemon is running successfully"
else
    echo "❌ Failed to start Nx Daemon"
    exit 1
fi

# Warm up cache by running a quick operation
echo "🔥 Warming up Nx cache..."
npx nx show projects > /dev/null 2>&1

# Display workspace info
echo "📊 Workspace Status:"
echo "  - Projects: $(npx nx show projects 2>/dev/null | wc -l | tr -d ' ')"
echo "  - Daemon: $(npx nx daemon | grep 'currently running' && echo '✅ Running' || echo '❌ Not Running')"
echo "  - Cache Directory: .nx/cache"

echo "🎉 Nx environment setup complete!"
echo ""
echo "💡 Useful commands:"
echo "  - npm run daemon:status    # Check daemon status"
echo "  - npm run daemon:stop     # Stop daemon"  
echo "  - npm run graph           # Open project graph"
echo "  - npm run affected:test   # Test affected projects"
echo "  - npm run clean          # Clear Nx cache"