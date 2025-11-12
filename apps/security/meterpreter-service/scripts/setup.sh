#!/bin/bash
# Setup script for Meterpreter development environment
set -e

echo "🚀 Setting up Meterpreter development environment"

# Check system dependencies
echo "🔍 Checking system dependencies..."

check_command() {
    if command -v "$1" >/dev/null 2>&1; then
        echo "✅ $1 is available"
        return 0
    else
        echo "❌ $1 is not available"
        return 1
    fi
}

# Required tools
missing_tools=()

if ! check_command gcc; then missing_tools+=("gcc"); fi
if ! check_command make; then missing_tools+=("make"); fi
if ! check_command git; then missing_tools+=("git"); fi

# Optional but recommended
if ! check_command jam; then echo "⚠️  jam is recommended for POSIX builds"; fi
if ! check_command flex; then echo "⚠️  flex is recommended for builds"; fi
if ! check_command bison; then echo "⚠️  bison is recommended for builds"; fi
if ! check_command clang-format; then echo "⚠️  clang-format is recommended for code formatting"; fi
if ! check_command doxygen; then echo "⚠️  doxygen is recommended for documentation"; fi

if [ ${#missing_tools[@]} -ne 0 ]; then
    echo "❌ Missing required tools: ${missing_tools[*]}"
    echo "📦 Install suggestions:"
    echo "   Ubuntu/Debian: apt-get install gcc make git jam flex bison gcc-multilib"
    echo "   Fedora:        yum install gcc make git jam flex patch bison glibc-devel.i686 libgcc.i686"
    echo "   macOS:         brew install gcc make git flex bison"
    exit 1
fi

# Initialize git submodules
echo "🔗 Initializing git submodules..."
if [ -f .gitmodules ]; then
    git submodule init
    git submodule update
    echo "✅ Submodules initialized"
else
    echo "⚠️  No .gitmodules found"
fi

# Create environment file if it doesn't exist
if [ ! -f .env ]; then
    echo "📄 Creating .env file from template..."
    cp .env.example .env
    echo "✅ Created .env file"
    echo "📝 Please review and update .env file with your settings"
else
    echo "✅ .env file already exists"
fi

# Create output directories
mkdir -p output/{x86,x64}
mkdir -p dist/apps/meterpreter-service
echo "✅ Created output directories"

echo ""
echo "🎉 Setup completed successfully!"
echo ""
echo "📚 Next steps:"
echo "   1. Review .env configuration"
echo "   2. Run: nx build meterpreter-service"
echo "   3. Run: nx test meterpreter-service"
echo ""
echo "🔧 Available commands:"
echo "   nx setup meterpreter-service         - Run this setup"
echo "   nx build meterpreter-service         - Build payloads"
echo "   nx build meterpreter-service --configuration=x86"
echo "   nx build meterpreter-service --configuration=x64"
echo "   nx test meterpreter-service          - Run tests"
echo "   nx lint meterpreter-service          - Check code style"
echo "   nx clean meterpreter-service         - Clean build files"
echo ""