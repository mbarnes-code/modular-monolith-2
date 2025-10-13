#!/bin/bash
set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_header() {
    echo -e "\n${BLUE}================================================${NC}"
    echo -e "${BLUE} $1${NC}"
    echo -e "${BLUE}================================================${NC}\n"
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to check if we're in the right directory
check_directory() {
    if [[ ! -f "package.json" ]] || [[ ! -f "nx.json" ]]; then
        print_error "This script must be run from the root of the modular-monolith-2 repository"
        exit 1
    fi
}

# Function to update system packages
update_system() {
    print_header "UPDATING SYSTEM PACKAGES"
    
    print_status "Updating package lists..."
    sudo apt-get update -qq
    
    print_status "Upgrading installed packages..."
    sudo apt-get upgrade -y -qq
    
    print_status "Installing essential build tools..."
    sudo apt-get install -y -qq \
        build-essential \
        curl \
        wget \
        git \
        unzip \
        software-properties-common \
        apt-transport-https \
        ca-certificates \
        gnupg \
        lsb-release
    
    print_success "System packages updated successfully"
}

# Function to install UV (Python package installer)
install_uv() {
    print_header "INSTALLING UV PYTHON PACKAGE INSTALLER"
    
    if command_exists uv; then
        print_warning "UV is already installed, updating..."
    else
        print_status "Installing UV..."
    fi
    
    curl -LsSf https://astral.sh/uv/install.sh | sh
    
    # Source the environment to make uv available
    export PATH="$HOME/.cargo/bin:$PATH"
    
    if command_exists uv; then
        print_success "UV installed successfully"
        uv --version
    else
        print_error "UV installation failed"
        exit 1
    fi
}

# Function to install specify-cli
install_specify_cli() {
    print_header "INSTALLING SPECIFY-CLI"
    
    print_status "Installing specify-cli from GitHub..."
    uv tool install specify-cli --from git+https://github.com/github/spec-kit.git
    
    # Add uv tools to PATH
    export PATH="$HOME/.local/bin:$PATH"
    
    if command_exists specify; then
        print_success "specify-cli installed successfully"
    else
        print_warning "specify-cli may not be in PATH. You may need to restart your shell or run: export PATH=\"\$HOME/.local/bin:\$PATH\""
    fi
}

# Function to verify Node.js and npm versions
check_node_versions() {
    print_header "VERIFYING NODE.JS ENVIRONMENT"
    
    if command_exists node; then
        NODE_VERSION=$(node --version)
        print_status "Node.js version: $NODE_VERSION"
        
        # Check if Node.js version is 20 or higher
        NODE_MAJOR=$(echo $NODE_VERSION | cut -d'v' -f2 | cut -d'.' -f1)
        if [[ $NODE_MAJOR -ge 20 ]]; then
            print_success "Node.js version is compatible"
        else
            print_warning "Node.js version should be 20.x or higher"
        fi
    else
        print_error "Node.js is not installed"
        exit 1
    fi
    
    if command_exists npm; then
        NPM_VERSION=$(npm --version)
        print_status "npm version: $NPM_VERSION"
        print_success "npm is available"
    else
        print_error "npm is not installed"
        exit 1
    fi
}

# Function to verify Python environment
check_python_environment() {
    print_header "VERIFYING PYTHON ENVIRONMENT"
    
    if command_exists python; then
        PYTHON_VERSION=$(python --version)
        print_status "Python version: $PYTHON_VERSION"
        
        # Check if Python version is 3.12
        if python -c "import sys; sys.exit(0 if sys.version_info >= (3, 12) else 1)"; then
            print_success "Python version is compatible"
        else
            print_warning "Python version should be 3.12.x"
        fi
    else
        print_error "Python is not installed"
        exit 1
    fi
    
    if command_exists pip; then
        PIP_VERSION=$(pip --version | cut -d' ' -f2)
        print_status "pip version: $PIP_VERSION"
        print_success "pip is available"
    else
        print_error "pip is not installed"
        exit 1
    fi
}

# Function to upgrade pip
upgrade_pip() {
    print_header "UPGRADING PIP"
    
    print_status "Upgrading pip to latest version..."
    python -m pip install --upgrade pip --quiet
    
    PIP_NEW_VERSION=$(pip --version | cut -d' ' -f2)
    print_success "pip upgraded to version: $PIP_NEW_VERSION"
}

# Function to install project dependencies
install_dependencies() {
    print_header "INSTALLING PROJECT DEPENDENCIES"
    
    print_status "Running make install..."
    make install
    
    print_success "Project dependencies installed successfully"
}

# Function to verify NX installation
verify_nx() {
    print_header "VERIFYING NX WORKSPACE"
    
    print_status "Checking NX installation..."
    if npx nx --version >/dev/null 2>&1; then
        NX_VERSION=$(npx nx --version | grep "Local:" | awk '{print $2}')
        print_success "NX is installed (Local: $NX_VERSION)"
    else
        print_error "NX is not properly installed"
        exit 1
    fi
    
    print_status "Listing available projects..."
    PROJECTS=$(npx nx show projects --type=app)
    print_success "Available applications:"
    echo "$PROJECTS" | sed 's/^/  - /'
}

# Function to verify Docker environment
check_docker() {
    print_header "VERIFYING DOCKER ENVIRONMENT"
    
    if command_exists docker; then
        DOCKER_VERSION=$(docker --version | cut -d' ' -f3 | tr -d ',')
        print_success "Docker is installed (version: $DOCKER_VERSION)"
        
        # Check if Docker daemon is running
        if docker info >/dev/null 2>&1; then
            print_success "Docker daemon is running"
        else
            print_warning "Docker daemon may not be running"
        fi
    else
        print_warning "Docker is not installed (optional for development)"
    fi
    
    if command_exists docker-compose; then
        COMPOSE_VERSION=$(docker-compose --version | cut -d' ' -f4 | tr -d ',')
        print_success "Docker Compose is installed (version: $COMPOSE_VERSION)"
    else
        print_warning "Docker Compose is not installed (optional for development)"
    fi
}

# Function to set up environment files
setup_environment_files() {
    print_header "SETTING UP ENVIRONMENT FILES"
    
    # Find all .env.example files and create corresponding .env files if they don't exist
    find . -name ".env.example" -type f | while read -r env_example; do
        env_file="${env_example%.example}"
        if [[ ! -f "$env_file" ]]; then
            print_status "Creating $env_file from $env_example"
            cp "$env_example" "$env_file"
        else
            print_status "$env_file already exists, skipping..."
        fi
    done
    
    print_success "Environment files setup completed"
}

# Function to test build process
test_build() {
    print_header "TESTING BUILD PROCESS"
    
    print_status "Running build test for jane-ui..."
    if npx nx build jane-ui --skip-nx-cache >/dev/null 2>&1; then
        print_success "Build test passed"
    else
        print_warning "Build test failed, but continuing..."
    fi
}

# Function to display final status
display_final_status() {
    print_header "SETUP COMPLETE - READY TO DEVELOP!"
    
    echo -e "${GREEN}✅ System Environment:${NC}"
    echo "  - System packages updated"
    echo "  - UV Python installer: $(uv --version 2>/dev/null || echo 'Not in PATH')"
    echo "  - specify-cli: $(command_exists specify && echo 'Installed' || echo 'Check PATH')"
    echo ""
    
    echo -e "${GREEN}✅ Development Environment:${NC}"
    echo "  - Node.js: $(node --version)"
    echo "  - Python: $(python --version | cut -d' ' -f2)"
    echo "  - NX: $(npx nx --version 2>/dev/null | grep "Local:" | awk '{print $2}' || echo 'Unknown')"
    echo ""
    
    echo -e "${GREEN}✅ Available Commands:${NC}"
    echo "  - make install         # Install all dependencies"
    echo "  - make build          # Build all applications"
    echo "  - npx nx serve jane-ui        # Start UI (port 3000)"
    echo "  - npx nx serve jane-orchestrator  # Start API (port 8000)"
    echo "  - npx nx serve cyber-llm-server   # Start Cyber LLM (port 8001)"
    echo "  - npx nx serve mtg-llm-server     # Start MTG LLM (port 8002)"
    echo "  - npx nx serve code-llm-server    # Start Code LLM (port 8003)"
    echo ""
    
    echo -e "${GREEN}✅ Docker Services (if needed):${NC}"
    echo "  - cd infrastructure/docker && docker-compose up"
    echo ""
    
    echo -e "${BLUE}💡 Next Steps:${NC}"
    echo "  1. Review .env files in each app directory"
    echo "  2. Start development servers with the commands above"
    echo "  3. Open http://localhost:3000 for the UI"
    echo "  4. Check http://localhost:8000/docs for API documentation"
    echo ""
    
    print_success "Codespace is ready for development! 🚀"
}

# Main execution
main() {
    print_header "MODULAR MONOLITH CODESPACE SETUP"
    print_status "Starting comprehensive setup process..."
    
    # Check if we're in the right directory
    check_directory
    
    # System setup
    update_system
    
    # Install specialized tools
    install_uv
    install_specify_cli
    
    # Verify environments
    check_node_versions
    check_python_environment
    upgrade_pip
    
    # Install project dependencies
    install_dependencies
    
    # Verify installations
    verify_nx
    check_docker
    
    # Setup environment
    setup_environment_files
    
    # Test basic functionality
    test_build
    
    # Display final status
    display_final_status
}

# Run main function
main "$@"